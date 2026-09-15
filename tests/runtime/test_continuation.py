"""Full-public-readback continuation tests; no Spine process or database."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.__main__ import load_input, main, publish
from spine_packs.apply import apply_continuation, apply_initial, checkpoint_writer
from spine_packs.execution import execution_artifact, materialize, response_evidence
from spine_packs.planning import CATALOGS, PlanError, plan_installation
from spine_packs.recovery import continuation_checkpoint, preflight_continuation
from test_apply_preflight import approval
from test_planning import catalog, manifest, request
from test_recovery_evidence import FingerprintReads, SnapshotEffects, scenario, saved_checkpoint
import test_installer_artifact_contract as independent


class RecoverySpine(FingerprintReads):
    """Synthetic receipt cache plus full schema-valid mutable public definitions.

    SnapshotEffects supplies arbitrary server IDs/receipts. This double adds
    full revision bodies and provenance, which the snapshot-only probe omitted.
    """
    def __init__(self, pack, entries):
        super().__init__(entries)
        self.prototype = catalog(pack)
        self.server = SnapshotEffects(entries)
        self.writes = []
        self.fail_before = self.lose_after = None
        self.response_mutator = None

    def write(self, command, body):
        index = len(self.writes)
        self.writes.append((command, deepcopy(body)))
        if index == self.fail_before:
            raise PlanError("spine_command_rejection", "synthetic_rejection")
        previous = self.server.mutations
        response = self.server.submit({"command": command}, body)
        if self.server.mutations != previous:
            audit = {"created_by_subject_id": body["actor_subject_id"],
                     "created_by_command_id": body["command_id"],
                     "created_at_utc": body["action_timestamp_utc"]}
            if command == "notification_profile.binding.set":
                row = deepcopy(self.prototype["bindings"][0])
                row.update(audit)
                for k in ("notification_profile_binding_id", "item_archetype_id", "notification_profile_id"):
                    row[k] = response[k]
                self.entries["bindings"] = [e for e in self.entries["bindings"]
                                            if e["item_archetype_id"] != body["item_archetype_id"]]
                self.entries["bindings"].append(row)
            else:
                profile = command.startswith("notification_profile")
                name = "profiles" if profile else "archetypes"
                _, key, identity, _ = CATALOGS[name]
                revision_id = identity.removesuffix("_id") + "_revision_id"
                if command.endswith(".create"):
                    row = deepcopy(next(e for e in self.prototype[name] if e[key] == body[key]))
                    row.update(audit)
                    row[identity] = response[identity]
                    self.entries[name].append(row)
                else:
                    row = next(e for e in self.entries[name] if e[identity] == body[identity])
                if command.endswith(".update"):
                    row.update(body["metadata"])
                else:
                    row["current_revision_id"] = response[revision_id]
                    revision = {**deepcopy(body["revision"]), **audit, identity: row[identity],
                                revision_id: response[revision_id], "revision_number": int(response["revision_number"])}
                    if profile:
                        revision["normalized_revision_hash"] = response["normalized_revision_hash"]
                        for i, template in enumerate(revision["templates"]):
                            template.update(notification_profile_template_id=response[revision_id] + str(i),
                                notification_profile_revision_id=response[revision_id], template_index=i,
                                normalized_template_hash="b" * 64)
                    else:
                        revision["normalized_content_hash"] = "a" * 64
                    row["revision"] = revision
        if index == self.lose_after:
            raise OSError("synthetic lost response after commit")
        if self.response_mutator:
            self.response_mutator(response)
        return response


class ContinuationTests(unittest.TestCase):
    def setup(self):
        pack, plan, approved, _, entries = scenario()
        return pack, plan, approved, RecoverySpine(pack, entries)

    def prefix(self, plan, approved, transport, count):
        accepted = []
        for i in range(count):
            action = plan["actions"][i]
            body = materialize(plan, approved, i, accepted)
            accepted.append(response_evidence(action, body, transport.write(action["command"], body)))
        return accepted

    def assert_rejected(self, pack, plan, approved, source, transport, code=None):
        writes, checkpoints = len(transport.writes), []
        with self.assertRaises(PlanError) as caught:
            apply_continuation(pack, plan, approved, source, transport, checkpoints.append, page_size=1)
        if code:
            self.assertEqual(caught.exception.code, code)
        self.assertEqual(len(transport.writes), writes)
        self.assertEqual(checkpoints, [])

    def test_every_action_before_after_and_response_loss(self):
        for index in range(7):
            for boundary in ("prepared", "lost", "recorded"):
                with self.subTest(index=index, boundary=boundary):
                    pack, plan, approved, transport = self.setup()
                    accepted = self.prefix(plan, approved, transport, index)
                    source = saved_checkpoint(plan, approved, accepted)
                    original = materialize(plan, approved, index, accepted)
                    if boundary != "prepared":
                        response = transport.write(plan["actions"][index]["command"], original)
                        if boundary == "recorded":
                            accepted.append(response_evidence(plan["actions"][index], original, response))
                            source = saved_checkpoint(plan, approved, accepted, prepared=False)
                    frozen = deepcopy((pack, plan, approved, source))
                    writes = len(transport.writes)
                    checkpoints = []
                    result = apply_continuation(pack, plan, approved, source, transport, checkpoints.append, page_size=1)
                    self.assertEqual(result["state"], "applied")
                    self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
                    self.assertEqual(transport.server.mutations, len(plan["actions"]))
                    if boundary != "recorded":
                        self.assertEqual(transport.writes[writes][1], original)
                    self.assertEqual((pack, plan, approved, source), frozen)
                    self.assertIsNone(checkpoints[-1]["next_action_id"])
                    self.assertEqual(checkpoints[-1]["accepted_responses"], result["accepted_responses"])

    def test_partial_sources_before_and_after_commit(self):
        for index in range(7):
            for lost in (False, True):
                with self.subTest(index=index, lost=lost):
                    pack, plan, approved, transport = self.setup()
                    if lost:
                        transport.lose_after = index
                    else:
                        transport.fail_before = index
                    prior = []
                    partial = apply_initial(pack, plan, approved, transport, prior.append)
                    self.assertEqual(partial["state"], "partial")
                    self.assertEqual(len(partial["accepted_responses"]), index)
                    source = json.loads(a.canonical_text(partial))
                    original = deepcopy(transport.writes[-1])
                    transport.lose_after = transport.fail_before = None
                    checkpoints, offset = [], len(transport.writes)
                    result = apply_continuation(pack, plan, approved, source, transport, checkpoints.append)
                    self.assertEqual(checkpoints[0], continuation_checkpoint(plan, approved, source))
                    self.assertEqual(transport.writes[offset], original)
                    self.assertEqual(result["state"], "applied")
                    self.assertEqual(transport.server.mutations, 7)

    def test_rejection_on_continuation_remains_partial_even_empty_prefix(self):
        pack, plan, approved, transport = self.setup()
        transport.fail_before = 0
        result = apply_continuation(pack, plan, approved, saved_checkpoint(plan, approved, []), transport, lambda _: None)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["accepted_responses"], [])
        self.assertEqual(len(transport.writes), 1)

    def test_durable_restart_after_each_prepared_or_advanced_publication(self):
        for boundary in range(1, 15):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
                pack, plan, approved, transport = self.setup()
                first = Path(directory) / "first.json"
                writer, calls = checkpoint_writer(first), []

                def crash(value):
                    writer(value)
                    calls.append(value)
                    if len(calls) == boundary:
                        raise RuntimeError("simulated process loss")

                with self.assertRaises(RuntimeError):
                    apply_initial(pack, plan, approved, transport, crash)
                source = a.load_json(first)
                preserved = first.read_bytes()
                second = Path(directory) / "continued.json"
                result = apply_continuation(pack, plan, approved, source, transport, checkpoint_writer(second))
                self.assertEqual(result["state"], "applied")
                self.assertEqual(transport.server.mutations, 7)
                self.assertEqual(first.read_bytes(), preserved)
                self.assertEqual(second.stat().st_mode & 0o777, 0o600)

    def test_checkpoint_write_failure_never_advances_suffix(self):
        pack, plan, approved, transport = self.setup()
        source = saved_checkpoint(plan, approved, [])
        for fail_call, expected_writes in ((1, 0), (2, 0), (3, 1)):
            with self.subTest(fail_call=fail_call):
                pack, plan, approved, transport = self.setup()
                calls = []

                def writer(value):
                    calls.append(value)
                    if len(calls) == fail_call:
                        raise OSError("synthetic disk failure")

                with self.assertRaises(OSError):
                    apply_continuation(pack, plan, approved, source, transport, writer)
                self.assertEqual(len(transport.writes), expected_writes)

    def test_unrelated_catalog_changes_reject_both_candidates(self):
        for name in CATALOGS:
            for uncertain in (False, True):
                with self.subTest(name=name, uncertain=uncertain):
                    pack, plan, approved, transport = self.setup()
                    accepted = self.prefix(plan, approved, transport, 2)
                    source = saved_checkpoint(plan, approved, accepted)
                    if uncertain:
                        body = materialize(plan, approved, 2, accepted)
                        transport.write(plan["actions"][2]["command"], body)
                    outsider = next(e for e in transport.entries[name] if "unrelated" in e[CATALOGS[name][1]])
                    field = "notification_profile_id" if name == "bindings" else "current_revision_id"
                    outsider[field] += "_changed"
                    if name != "bindings":
                        outsider["revision"][CATALOGS[name][2].removesuffix("_id") + "_revision_id"] = outsider[field]
                        if name == "profiles":
                            for template in outsider["revision"]["templates"]:
                                template["notification_profile_revision_id"] = outsider[field]
                    self.assert_rejected(pack, plan, approved, source, transport, "continuation_state_mismatch")

    def test_two_unrecorded_actions_reject(self):
        pack, plan, approved, transport = self.setup()
        source = saved_checkpoint(plan, approved, [])
        self.prefix(plan, approved, transport, 2)
        self.assert_rejected(pack, plan, approved, source, transport, "continuation_state_mismatch")

    def test_semantics_and_provenance_not_just_hashes(self):
        for index in range(7):
            for change in ("semantics", "actor", "command", "timestamp"):
                # Metadata has no last-updated provenance in the pinned public API.
                if index == 3 and change != "semantics":
                    continue
                with self.subTest(index=index, change=change):
                    pack, plan, approved, transport = self.setup()
                    accepted = self.prefix(plan, approved, transport, index)
                    source = saved_checkpoint(plan, approved, accepted)
                    action = plan["actions"][index]
                    body = materialize(plan, approved, index, accepted)
                    transport.write(action["command"], body)
                    if action["command"].endswith("binding.set"):
                        row = next(e for e in transport.entries["bindings"] if e["item_archetype_id"] == body["item_archetype_id"])
                        if change == "semantics":
                            row["notification_profile_id"] = "other_profile"
                        target = row
                    else:
                        name = "profiles" if action["command"].startswith("notification_profile") else "archetypes"
                        _, key, identity, _ = CATALOGS[name]
                        row = next(e for e in transport.entries[name] if
                                   (e[key] == body[key] if action["command"].endswith(".create") else e[identity] == body[identity]))
                        target = row["revision"]
                        if change == "semantics":
                            if action["command"].endswith(".update"):
                                row["display_name"] = "Wrong metadata"
                            elif name == "archetypes":
                                target["description"] = "Wrong revision body"
                            else:
                                target["templates"][0]["late_handling"]["grace_seconds"] = "2"
                    if change != "semantics":
                        field = {"actor": "created_by_subject_id", "command": "created_by_command_id", "timestamp": "created_at_utc"}[change]
                        target[field] = "2026-08-01T00:00:00Z" if change == "timestamp" else "wrong_provenance"
                    self.assert_rejected(pack, plan, approved, source, transport, "continuation_state_mismatch")

    def test_wrong_replay_generated_id_cannot_advance(self):
        for index in range(7):
            with self.subTest(index=index):
                pack, plan, approved, transport = self.setup()
                accepted = self.prefix(plan, approved, transport, index)
                source = saved_checkpoint(plan, approved, accepted)
                body = materialize(plan, approved, index, accepted)
                action = plan["actions"][index]
                transport.write(action["command"], body)
                field = ("notification_profile_binding_id" if action["command"].endswith("binding.set") else
                         "notification_profile_revision_id" if action["command"].startswith("notification_profile") else
                         "item_archetype_revision_id")
                transport.response_mutator = lambda r: r.update({field: "wrong_replay_id"})
                checkpoints, writes = [], len(transport.writes)
                result = apply_continuation(pack, plan, approved, source, transport, checkpoints.append)
                self.assertEqual(result["state"], "partial")
                self.assertEqual(result["failure"]["error"]["code"], "recovery_response_readback_mismatch")
                self.assertEqual(result["accepted_responses"], accepted)
                self.assertEqual(len(transport.writes), writes + 1)
                self.assertIsNotNone(checkpoints[-1]["unresolved_submission"])

    def test_binding_changes_after_admission_reject_before_retry(self):
        for uncertain in (False, True):
            pack, plan, approved, transport = self.setup()
            accepted = self.prefix(plan, approved, transport, 5)
            source = saved_checkpoint(plan, approved, accepted)
            body = materialize(plan, approved, 5, accepted)
            if uncertain:
                transport.write(plan["actions"][5]["command"], body)
            writes = len(transport.writes)

            def writer(value):
                transport.entries["bindings"] = [e for e in transport.entries["bindings"]
                                                if e["item_archetype_id"] != body["item_archetype_id"]]
                row = deepcopy(transport.prototype["bindings"][0])
                row["item_archetype_id"] = body["item_archetype_id"]
                row["notification_profile_binding_id"] = "intruder_binding"
                transport.entries["bindings"].append(row)

            result = apply_continuation(pack, plan, approved, source, transport, writer)
            self.assertEqual(result["state"], "partial")
            self.assertEqual(result["failure"]["error"]["code"], "binding_precondition_changed")
            self.assertEqual(len(transport.writes), writes)

    def test_invalid_sources_and_changed_approval_before_transport(self):
        pack, plan, approved, transport = self.setup()
        accepted = self.prefix(plan, approved, transport, 2)
        source = saved_checkpoint(plan, approved, accepted)
        cases = []
        for field in ("plan_digest", "approval_digest"):
            bad = deepcopy(source)
            bad[field] = "0" * 64
            cases.append(a.seal(bad))
        bad = deepcopy(source)
        bad["accepted_responses"].reverse()
        cases.append(a.seal(bad))
        bad = deepcopy(source)
        bad["next_action_id"] = "action-000003"
        cases.append(a.seal(bad))
        bad = deepcopy(source)
        bad["unresolved_submission"]["command_id"] = "wrong_command"
        cases.append(a.seal(bad))
        bad = deepcopy(source)
        bad["content_identity"]["digest"] = "0" * 64
        cases.append(bad)
        for bad in cases:
            reads = len(transport.calls)
            self.assert_rejected(pack, plan, approved, bad, transport)
            self.assertEqual(len(transport.calls), reads)
        changed = deepcopy(approved)
        changed["execution"]["actor_subject_id"] = "another_actor"
        self.assert_rejected(pack, plan, a.seal(changed), source, transport)

    def test_bad_public_hash_and_changed_environment_fail(self):
        pack, plan, approved, transport = self.setup()
        source = saved_checkpoint(plan, approved, [])
        with patch("spine_packs.recovery.catalog_digest", return_value="0" * 64):
            self.assert_rejected(pack, plan, approved, source, transport, "public_snapshot_hash_mismatch")
        transport.info["runtime_version"] = "0.4.0"
        self.assert_rejected(pack, plan, approved, source, transport, "incompatible_runtime_or_contracts")
        transport.info["runtime_version"] = "0.3.0"
        with patch.object(transport, "check_target", side_effect=PlanError("stale_plan_or_target_mismatch", "target_changed")):
            self.assert_rejected(pack, plan, approved, source, transport, "target_changed")

    def test_no_write_completed_checkpoint_is_safe(self):
        pack = manifest(released=True)
        transport = RecoverySpine(pack, catalog(pack))
        plan = plan_installation(pack, request(), transport)
        approved = approval(plan)
        result = apply_continuation(pack, plan, approved, saved_checkpoint(plan, approved, []), transport, lambda _: None)
        self.assertEqual(result["state"], "applied")
        self.assertEqual(transport.writes, [])

    def test_untouched_selected_semantics_and_suffix_preconditions(self):
        for existing_actions in (False, True):
            with self.subTest(existing_actions=existing_actions):
                if existing_actions:
                    pack, plan, approved, transport = self.setup()
                else:
                    pack = manifest(released=True)
                    transport = RecoverySpine(pack, catalog(pack))
                    plan = plan_installation(pack, request(), transport)
                    approved = approval(plan)
                source = saved_checkpoint(plan, approved, [])
                # Revision content is not in the catalog hash. Reconstruction
                # must still reject changed equivalent or pending definitions.
                transport.entries["archetypes"][0]["revision"]["description"] = "Unexplained selected drift"
                self.assert_rejected(pack, plan, approved, source, transport, "continuation_state_mismatch")

    def test_recorded_prefix_ids_and_provenance_remain_checked(self):
        for change in ("id", "provenance"):
            with self.subTest(change=change):
                pack, plan, approved, transport = self.setup()
                accepted = self.prefix(plan, approved, transport, 1)
                source = saved_checkpoint(plan, approved, accepted, prepared=False)
                row = next(e for e in transport.entries["archetypes"] if e["archetype_key"] == "lesson")
                if change == "id":
                    row["item_archetype_id"] = "wrong_recorded_root"
                    row["revision"]["item_archetype_id"] = row["item_archetype_id"]
                else:
                    row["created_by_command_id"] = "different_creator"
                self.assert_rejected(pack, plan, approved, source, transport, "continuation_state_mismatch")

    def test_preserved_compatible_replay_outcome_and_page_size(self):
        pack, plan, approved, transport = self.setup()
        accepted = self.prefix(plan, approved, transport, 1)
        accepted[0]["outcome"] = "compatible_replay"
        source = saved_checkpoint(plan, approved, accepted)
        body = materialize(plan, approved, 1, accepted)
        transport.write(plan["actions"][1]["command"], body)
        small = preflight_continuation(pack, plan, approved, source, transport, page_size=1)
        large = preflight_continuation(pack, plan, approved, source, transport, page_size=500)
        self.assertEqual(small, large)
        self.assertIsNotNone(small[1])
        result = apply_continuation(pack, plan, approved, source, transport, lambda _: None)
        self.assertEqual(result["state"], "applied")
        self.assertEqual(result["accepted_responses"][0]["outcome"], "compatible_replay")

    def test_modified_unresolved_request_and_terminal_success_rejected(self):
        pack, plan, approved, transport = self.setup()
        source = saved_checkpoint(plan, approved, [])
        wrapped = source["unresolved_submission"]["request"]
        body = json.loads(wrapped["canonical_json"])
        body["actor_subject_id"] = "another_actor"
        source["unresolved_submission"]["request"] = a.canonical_value(wrapped["contract"], body, wrapped["shape"])
        self.assert_rejected(pack, plan, approved, a.seal(source), transport, "unresolved_request_mismatch")
        accepted = self.prefix(plan, approved, transport, len(plan["actions"]))
        result = execution_artifact(plan, approved, accepted, state="applied")
        self.assert_rejected(pack, plan, approved, result, transport, "continuation_requires_partial_result")

    def test_cli_stale_continuation_emits_only_error_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            pack, plan, approved, transport = self.setup()
            accepted = self.prefix(plan, approved, transport, 2)
            source = saved_checkpoint(plan, approved, accepted)
            transport.entries["profiles"][-1]["description"] = "unrelated drift"
            for filename, value in (("manifest.json", pack), ("plan.json", plan), ("approval.json", approved), ("source.json", source)):
                publish(folder / filename, value)
            args = ["apply", "--manifest", str(folder / "manifest.json"), "--plan", str(folder / "plan.json"),
                    "--approval", str(folder / "approval.json"), "--continue-from", str(folder / "source.json"),
                    "--checkpoint", str(folder / "next.json"), "--output", str(folder / "result.json")]
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(args, transport_factory=lambda _: transport)
            self.assertEqual(code, 7, output.getvalue())
            envelope = json.loads(output.getvalue())
            self.assertIsNone(envelope["artifact"])
            self.assertFalse((folder / "next.json").exists())
            self.assertFalse((folder / "result.json").exists())
            self.assertEqual(len(transport.writes), 2)

    def test_cli_continuation_and_preserved_input_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            pack, plan, approved, transport = self.setup()
            source = saved_checkpoint(plan, approved, [])
            for filename, value in (("manifest.json", pack), ("plan.json", plan), ("approval.json", approved), ("source.json", source)):
                publish(folder / filename, value)
            args = ["apply", "--manifest", str(folder / "manifest.json"), "--plan", str(folder / "plan.json"),
                    "--approval", str(folder / "approval.json"), "--continue-from", str(folder / "source.json"),
                    "--checkpoint", str(folder / "next.json"), "--output", str(folder / "result.json")]
            preserved = (folder / "source.json").read_bytes()
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(args, transport_factory=lambda _: transport)
            self.assertEqual(code, 0, output.getvalue())
            envelope = json.loads(output.getvalue())
            self.assertEqual(envelope["operation"], "apply")
            self.assertEqual(a.validate_schema(envelope), [])
            self.assertEqual(a.load_json(folder / "result.json")["state"], "applied")
            self.assertEqual((folder / "source.json").read_bytes(), preserved)
            for target_file in (plan["request"]["target"]["ledger"]["path"],
                                plan["request"]["target"]["spine_command"]["path"]):
                collided = args[:]
                collided[collided.index("--continue-from") + 1] = target_file
                with patch("spine_packs.__main__.load_input", wraps=load_input) as loader:
                    with contextlib.redirect_stdout(io.StringIO()) as output:
                        code = main(collided, transport_factory=lambda _: self.fail("must not construct transport"))
                    self.assertEqual(code, 2)
                    self.assertEqual(json.loads(output.getvalue())["error"]["code"], "continuation_source_input_collision")
                    self.assertNotIn(target_file, [call.args[0] for call in loader.call_args_list])
            for flag in ("--checkpoint", "--output"):
                collided = args[:]
                collided[collided.index(flag) + 1] = str(folder / "source.json")
                with contextlib.redirect_stdout(io.StringIO()):
                    code = main(collided, transport_factory=lambda _: self.fail("must not construct transport"))
                self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
