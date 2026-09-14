"""Test-only recovery evidence investigation, NOT a continuation implementation.

The small catalog projections below follow Spine 0.3.0 commit
72203f092de191a7633b1884bf0d61836a25abe4, notification_profiles.py
_list_roots (838-850) and _binding_list (1160-1174). No Spine import,
database, subprocess, deployment, or production recovery path is used.
The model simulates snapshot-visible effects only, not all Spine semantics.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.execution import (execution_artifact, materialize,
                                   response_evidence, validate_inputs, validate_prefix)
from spine_packs.planning import CATALOGS, PlanError, plan_installation
from test_apply_preflight import approval
from test_planning import FakeSpine, catalog, manifest, request
import test_installer_artifact_contract as independent


def projection(name, entries):
    """Exact snapshot fields; audit fields and revision bodies are NOT hashed."""
    if name == "bindings":
        return [{k: row[k] for k in (
            "notification_profile_binding_id", "item_archetype_id",
            "notification_profile_id", "status")}
            for row in entries if row["status"] == "active"]
    _, key, identity, _ = CATALOGS[name]
    result = []
    for row in entries:
        value = {"id": row[identity], "key": row[key], "status": row["status"],
                 "current_revision_id": row["current_revision_id"]}
        if name == "profiles":
            value.update(display_name=row["display_name"], description=row["description"])
        result.append(value)
    return result


def snapshot(name, rows):
    ordering = (("item_archetype_id", "notification_profile_binding_id")
                if name == "bindings" else ("key", "id"))
    return a.digest(sorted(rows, key=lambda row: tuple(row[k] for k in ordering)))


def fingerprints(catalogs):
    return [{"catalog": name, "digest": snapshot(name, catalogs[name])} for name in CATALOGS]


class FingerprintReads(FakeSpine):
    """Existing schema-valid public read fixtures, with content-derived hashes."""
    def read(self, command, query):
        result = super().read(command, query)
        if command.endswith(".list"):
            name = next(n for n, shape in CATALOGS.items() if command == shape[0] + ".list")
            result["catalog_snapshot_hash"] = snapshot(name, projection(name, self.entries[name]))
        return result


class SnapshotEffects:
    """Synthetic server-side oracle. Its state/cache never enter the checker.

    IDs are arbitrary server outputs, not predictions of Spine-generated IDs.
    Replay here illustrates the required contract; it does not qualify real replay.
    """
    def __init__(self, entries):
        self.rows = {name: projection(name, entries[name]) for name in CATALOGS}
        self.receipts = {}
        self.mutations = 0

    def read(self):
        return deepcopy(self.rows)

    def submit(self, action, body):
        command = action["command"]
        identity = body["command_id"]
        encoded = a.canonical_text(body)
        if identity in self.receipts:
            original, response = self.receipts[identity]
            if original != encoded:
                raise ValueError("incompatible replay")
            return deepcopy(response)
        token = str(self.mutations)
        profile = command.startswith("notification_profile")
        kind = "notification_profile" if profile else "item_archetype"
        name = "profiles" if profile else "archetypes"
        if command.endswith(".create"):
            key = body["profile_key" if profile else "archetype_key"]
            row = {"id": "server_root_" + token, "key": key, "status": "active",
                   "current_revision_id": "server_revision_" + token}
            if profile:
                row.update({k: body[k] for k in ("display_name", "description")})
            self.rows[name].append(row)
            facts = {kind + "_id": row["id"], kind + "_revision_id": row["current_revision_id"],
                     "revision_number": "1", "profile_key" if profile else "archetype_key": key}
            if profile:
                facts["normalized_revision_hash"] = "b" * 64
            effect = kind + "_created"
        elif command.endswith(".revise"):
            row = next(r for r in self.rows[name] if r["id"] == body[kind + "_id"])
            assert row["current_revision_id"] == body["expected_current_revision_id"]
            row["current_revision_id"] = "server_revision_" + token
            facts = {kind + "_id": row["id"], kind + "_revision_id": row["current_revision_id"],
                     "revision_number": "2"}
            if profile:
                facts["normalized_revision_hash"] = "b" * 64
            effect = kind + "_revised"
        elif command == "notification_profile.metadata.update":
            row = next(r for r in self.rows["profiles"] if r["id"] == body["notification_profile_id"])
            assert {k: row[k] for k in body["expected_metadata"]} == body["expected_metadata"]
            row.update(body["metadata"])
            facts = {"notification_profile_id": row["id"],
                     "notification_profile_revision_id": row["current_revision_id"], **body["metadata"]}
            effect = "notification_profile_metadata_updated"
        else:
            assert command == "notification_profile.binding.set"
            self.rows["bindings"] = [r for r in self.rows["bindings"]
                                     if r["item_archetype_id"] != body["item_archetype_id"]]
            row = {"notification_profile_binding_id": "server_binding_" + token,
                   "item_archetype_id": body["item_archetype_id"],
                   "notification_profile_id": body["notification_profile_id"], "status": "active"}
            self.rows["bindings"].append(row)
            facts = {**row, "compatible_item_types": ["event"]}
            effect = "notification_profile_binding_set"
        response = {"ok": True, "command": command, "response_contract": a.COMMAND_SHAPES[command][1],
                    "effect": effect, "status": "active", **facts, "receipt": {
                        "command_id": identity, "command_receipt_id": "server_receipt_" + token,
                        "created_at_utc": body["action_timestamp_utc"], "effect": effect,
                        "semantic_facts_hash": a.digest(body)}}
        self.mutations += 1
        self.receipts[identity] = (encoded, deepcopy(response))
        return response


def undo_snapshot_effect(rows, plan, action, body, response):
    """Pure feasibility probe, operating on a COPY of fresh snapshot projections.

    No stored baseline or oracle access. response=None means one uncertain action;
    readback IDs may describe a candidate state but do not establish acceptance.
    This is deliberately NOT sufficient as a production recovery admission gate:
    full public readback/semantic validation must precede snapshot comparison.
    """
    command = action["command"]
    if command == "notification_profile.binding.set":
        found = [r for r in rows["bindings"] if r["item_archetype_id"] == body["item_archetype_id"]]
        assert len(found) == 1
        row = found[0]
        assert row["notification_profile_id"] == body["notification_profile_id"] and row["status"] == "active"
        if response is not None:
            assert row["notification_profile_binding_id"] == response["notification_profile_binding_id"]
        rows["bindings"].remove(row)
        classification = next(c for c in plan["classifications"] if c["object_key"] == action["object_key"])
        old = classification["identity"]["observed_binding"]
        if old is not None:
            rows["bindings"].append({**old, "status": "active"})
        return
    profile = command.startswith("notification_profile")
    kind = "notification_profile" if profile else "item_archetype"
    name = "profiles" if profile else "archetypes"
    if command.endswith(".create"):
        key = body["profile_key" if profile else "archetype_key"]
        found = [r for r in rows[name] if r["key"] == key]
    else:
        found = [r for r in rows[name] if r["id"] == body[kind + "_id"]]
    assert len(found) == 1 and found[0]["status"] == "active"
    row = found[0]
    if response is not None:
        assert row["id"] == response[kind + "_id"]
        assert row["current_revision_id"] == response[kind + "_revision_id"]
    if command.endswith(".create"):
        if profile:
            assert all(row[k] == body[k] for k in ("display_name", "description"))
        rows[name].remove(row)
    elif command.endswith(".revise"):
        assert row["current_revision_id"] != body["expected_current_revision_id"]
        row["current_revision_id"] = body["expected_current_revision_id"]
    else:
        assert command == "notification_profile.metadata.update"
        assert {k: row[k] for k in body["metadata"]} == body["metadata"]
        row.update(body["expected_metadata"])


def snapshot_candidate_matches(plan, approved, checkpoint, fresh, *, uncertain=False):
    """No I/O: can these persisted artifacts reconstruct the baseline digest?"""
    try:
        validate_inputs(plan, approved)
        assert not independent.checkpoint_errors(checkpoint, plan, approved)
        accepted = checkpoint["accepted_responses"]
        validate_prefix(plan, approved, accepted)
        rows = deepcopy(fresh)
        if uncertain:
            index = len(accepted)
            assert index < len(plan["actions"])
            body = materialize(plan, approved, index, accepted)
            undo_snapshot_effect(rows, plan, plan["actions"][index], body, None)
        for index in reversed(range(len(accepted))):
            body = materialize(plan, approved, index, accepted[:index])
            response = json.loads(accepted[index]["response"]["canonical_json"])
            undo_snapshot_effect(rows, plan, plan["actions"][index], body, response)
        return fingerprints(rows) == plan["catalog_snapshots"]
    except (AssertionError, PlanError, ValueError, KeyError, IndexError, TypeError):
        return False


def scenario():
    pack = manifest("medical_and_lesson", released=True)
    entries = catalog(pack)
    # One missing unit, one drifted unit, and one unselected unit in each catalog.
    outsider = deepcopy(pack)
    outsider["archetypes"] = [deepcopy(pack["archetypes"][0])]
    outsider["archetypes"][0]["archetype_key"] = "unrelated"
    outsider["notification_profiles"] = [deepcopy(pack["notification_profiles"][0])]
    outsider["notification_profiles"][0]["profile_key"] = "unrelated_standard"
    outsider["binding_intents"] = [{"archetype_key": "unrelated", "notification_profile_key": "unrelated_standard"}]
    extra = catalog(outsider)
    for name in CATALOGS:
        entries[name] = [entries[name][1], *extra[name]]
    entries["archetypes"][0]["revision"]["description"] = "Old description"
    entries["profiles"][0]["display_name"] = "Old name"
    entries["profiles"][0]["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "1"
    entries["bindings"][0]["notification_profile_id"] = extra["profiles"][0]["notification_profile_id"]
    plan = plan_installation(pack, request(), FingerprintReads(entries), page_size=1)
    return pack, plan, approval(plan), SnapshotEffects(entries), entries


def saved_checkpoint(plan, approved, accepted, prepared=True):
    index = len(accepted)
    unresolved = None
    if prepared and index < len(plan["actions"]):
        body = materialize(plan, approved, index, accepted)
        action = plan["actions"][index]
        shape, contract = a.COMMAND_SHAPES[action["command"]]
        unresolved = {"action_id": action["action_id"], "command_id": body["command_id"],
                      "submission_state": "prepared_or_submitted",
                      "request": a.canonical_value(contract, body, shape + "Request")}
    # Simulated restart has only serialized evidence, never live object aliases.
    return json.loads(a.canonical_text(execution_artifact(plan, approved, accepted, unresolved=unresolved)))


class RecoveryEvidenceTests(unittest.TestCase):
    def test_snapshot_projection_and_page_size(self):
        pack, plan, _, model, entries = scenario()
        self.assertEqual(fingerprints(model.read()), plan["catalog_snapshots"])
        self.assertEqual(plan, plan_installation(pack, request(), FingerprintReads(entries), page_size=100))
        self.assertEqual(snapshot("profiles", []), "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945")
        changed = deepcopy(entries)
        changed["profiles"][0]["created_by_command_id"] = "audit_only_change"
        self.assertEqual(projection("profiles", entries["profiles"]), projection("profiles", changed["profiles"]))
        self.assertNotIn("archetype:unrelated", [c["object_key"] for c in plan["classifications"]])
        self.assertNotIn("profile:unrelated_standard", [c["object_key"] for c in plan["classifications"]])
        self.assertTrue(all(set(s) == {"catalog", "digest"} for s in plan["catalog_snapshots"]))
        self.assertEqual(set(a.COMMAND_SHAPES), {x["command"] for x in plan["actions"]})

    def test_each_action_before_after_and_lost_response(self):
        _, plan, approved, model, _ = scenario()
        accepted = []
        for index, action in enumerate(plan["actions"]):
            with self.subTest(index=index, command=action["command"]):
                checkpoint = saved_checkpoint(plan, approved, accepted)
                self.assertTrue(snapshot_candidate_matches(plan, approved, checkpoint, model.read()))
                self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, model.read(), uncertain=True))
                body = materialize(plan, approved, index, checkpoint["accepted_responses"])
                response = model.submit(action, body)
                self.assertNotEqual(fingerprints(model.read()), plan["catalog_snapshots"])
                # The response is NOT supplied to the uncertain-state checker.
                self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, model.read()))
                self.assertTrue(snapshot_candidate_matches(plan, approved, checkpoint, model.read(), uncertain=True))
                before_replay = model.mutations
                exact_retry = json.loads(checkpoint["unresolved_submission"]["request"]["canonical_json"])
                self.assertEqual(body, exact_retry)
                self.assertEqual(model.submit(action, exact_retry), response)
                self.assertEqual(model.mutations, before_replay)
                accepted.append(response_evidence(action, body, response))
                advanced = saved_checkpoint(plan, approved, accepted, prepared=False)
                self.assertTrue(snapshot_candidate_matches(plan, approved, advanced, model.read()))
        self.assertIsNone(advanced["next_action_id"])
        result = execution_artifact(plan, approved, accepted, state="applied")
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_unrelated_changes_rejected_at_every_boundary(self):
        _, plan, approved, model, _ = scenario()
        accepted = []
        for index, action in enumerate(plan["actions"]):
            checkpoint = saved_checkpoint(plan, approved, accepted)
            body = materialize(plan, approved, index, accepted)
            response = model.submit(action, body)
            for name in CATALOGS:
                for mutation in ("change", "add", "remove"):
                    with self.subTest(index=index, catalog=name, mutation=mutation):
                        fresh = model.read()
                        key = "item_archetype_id" if name == "bindings" else "key"
                        row = next(r for r in fresh[name] if "unrelated" in r[key])
                        if mutation == "remove":
                            fresh[name].remove(row)
                        elif mutation == "add":
                            extra = deepcopy(row)
                            identity = "notification_profile_binding_id" if name == "bindings" else "id"
                            extra[identity] += "_extra"
                            extra[key] += "_extra"
                            fresh[name].append(extra)
                        else:
                            field = {"archetypes": "current_revision_id", "profiles": "description",
                                     "bindings": "notification_profile_id"}[name]
                            row[field] = "unrelated_change"
                        self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, fresh))
                        self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, fresh, uncertain=True))
                        completed = [*accepted, response_evidence(action, body, response)]
                        advanced = saved_checkpoint(plan, approved, completed, prepared=False)
                        self.assertFalse(snapshot_candidate_matches(plan, approved, advanced, fresh))
            accepted.append(response_evidence(action, body, response))

    def test_partial_result_preserves_exact_request_derivation(self):
        _, plan, approved, model, _ = scenario()
        accepted = []
        for index, action in enumerate(plan["actions"]):
            with self.subTest(index=index):
                original = saved_checkpoint(plan, approved, accepted)
                result = execution_artifact(plan, approved, accepted, state="partial", failure={
                    "action_id": action["action_id"], "error": {
                        "category": "transport_or_environment_failure", "code": "response_lost",
                        "message": "Synthetic response loss.", "facts": []}})
                result = json.loads(a.canonical_text(result))
                self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
                derived = saved_checkpoint(plan, approved, result["accepted_responses"])
                self.assertEqual(derived, original)
                body = materialize(plan, approved, index, accepted)
                accepted.append(response_evidence(action, body, model.submit(action, body)))

    def test_acknowledged_id_mismatch_and_two_unrecorded_actions_rejected(self):
        _, plan, approved, model, _ = scenario()
        checkpoint = saved_checkpoint(plan, approved, [])
        body = materialize(plan, approved, 0, [])
        evidence = response_evidence(plan["actions"][0], body, model.submit(plan["actions"][0], body))
        advanced = saved_checkpoint(plan, approved, [evidence])
        corrupted = model.read()
        created = next(r for r in corrupted["archetypes"] if r["key"] == body["archetype_key"])
        created["id"] = "wrong_recorded_identity"
        self.assertFalse(snapshot_candidate_matches(plan, approved, advanced, corrupted))
        # Simulate an impossible two-write jump. Only the first unresolved action
        # may be explained without durable response evidence, never a longer suffix.
        second = materialize(plan, approved, 1, [evidence])
        model.submit(plan["actions"][1], second)
        self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, model.read()))
        self.assertFalse(snapshot_candidate_matches(plan, approved, checkpoint, model.read(), uncertain=True))

    def test_snapshot_is_not_a_history_or_semantic_digest(self):
        _, _, _, model, entries = scenario()
        original = fingerprints(model.read())
        row = next(r for r in model.rows["profiles"] if r["key"] == "unrelated_standard")
        before = row["display_name"]
        row["display_name"] = "temporary metadata edit"
        self.assertNotEqual(fingerprints(model.read()), original)
        row["display_name"] = before
        self.assertEqual(fingerprints(model.read()), original)
        malformed_readback = deepcopy(entries)
        malformed_readback["archetypes"][0]["revision"]["description"] = "wrong content under same revision ID"
        self.assertEqual(projection("archetypes", entries["archetypes"]),
                         projection("archetypes", malformed_readback["archetypes"]))
        # Spine revision immutability forbids that mutation, but fingerprints
        # alone cannot validate a bad readback. Full semantic checks remain needed.

    def test_snapshot_match_is_not_receipt_or_complete_semantic_proof(self):
        _, plan, approved, model, _ = scenario()
        checkpoint = saved_checkpoint(plan, approved, [])
        body = materialize(plan, approved, 0, [])
        model.submit(plan["actions"][0], body)
        fresh = model.read()
        created = next(r for r in fresh["archetypes"] if r["key"] == body["archetype_key"])
        created["id"] = "unproven_public_root"
        created["current_revision_id"] = "unproven_public_revision"
        # An uncertain create's IDs disappear during inverse projection. This
        # candidate is NOT permission to accept a receipt or continue the suffix.
        self.assertTrue(snapshot_candidate_matches(plan, approved, checkpoint, fresh, uncertain=True))
        self.assertEqual(checkpoint["accepted_responses"], [])
        self.assertEqual(checkpoint["unresolved_submission"]["request"]["canonical_json"], a.canonical_text(body))

    def test_tampered_or_mismatched_persisted_evidence_rejected(self):
        _, plan, approved, model, _ = scenario()
        body = materialize(plan, approved, 0, [])
        accepted = [response_evidence(plan["actions"][0], body, model.submit(plan["actions"][0], body))]
        checkpoint = saved_checkpoint(plan, approved, accepted)
        mutations = (
            lambda c: c.update(plan_digest="0" * 64),
            lambda c: c.update(approval_digest="0" * 64),
            lambda c: c["execution"].update(actor_subject_id="wrong_actor"),
            lambda c: c["accepted_responses"][0]["generated_ids"][0].update(value="wrong_root"),
            lambda c: c["accepted_responses"][0].update(action_id="action-000001"),
            lambda c: c["unresolved_submission"].update(command_id="spack_" + "0" * 64),
        )
        for mutate in mutations:
            damaged = deepcopy(checkpoint)
            mutate(damaged)
            for value in (damaged, a.seal(damaged)):
                self.assertFalse(snapshot_candidate_matches(plan, approved, value, model.read()))
                self.assertFalse(snapshot_candidate_matches(plan, approved, value, model.read(), uncertain=True))
        changed_approval = deepcopy(approved)
        changed_approval["execution"]["action_timestamp_utc"] = "2026-09-13T00:00:00Z"
        self.assertFalse(snapshot_candidate_matches(plan, a.seal(changed_approval), checkpoint, model.read()))


if __name__ == "__main__":
    unittest.main()
