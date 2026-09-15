"""Verification tests use public-response doubles, never a live Spine target."""
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
from spine_packs.apply import apply_initial
from spine_packs.execution import execution_artifact
from spine_packs.manifest import content_digest
from spine_packs.planning import CATALOGS, PlanError, plan_installation
from spine_packs.spine_command import READ_COMMANDS, SpineCommand
from spine_packs.verification import verify_installation
from test_apply_preflight import approval
from test_continuation import RecoverySpine
from test_planning import FakeSpine, catalog, manifest, request
from test_recovery_evidence import FingerprintReads, scenario
import test_installer_artifact_contract as independent


class VerificationTests(unittest.TestCase):
    def installed(self):
        pack, plan, approved, _, entries = scenario()
        server = RecoverySpine(pack, entries)
        result = apply_initial(pack, plan, approved, server, lambda _: None)
        self.assertEqual(result["state"], "applied")
        return pack, plan, approved, result, FingerprintReads(server.entries)

    def check(self, pack, plan, transport, result=None, **kwargs):
        frozen = deepcopy((pack, plan, result, transport.entries))
        with patch.object(SpineCommand, "write", side_effect=AssertionError("verification must never write")):
            value = verify_installation(pack, plan, transport, result, **kwargs)
        self.assertEqual(independent.verification_errors(value, plan, result), [])
        self.assertEqual(frozen, (pack, plan, result, transport.entries))
        self.assertTrue(all(command in READ_COMMANDS for command, _ in transport.calls))
        self.assertEqual(value["receipt_readback"], "captured_responses_only_spine_0.3.0")
        return value

    def test_complete_all_six_command_evidence_and_fresh_state(self):
        pack, plan, _, result, transport = self.installed()
        self.assertEqual(set(a.COMMAND_SHAPES), {r["command"] for r in result["accepted_responses"]})
        value = self.check(pack, plan, transport, result, page_size=1)
        self.assertEqual(value["state"], "verified")
        self.assertEqual(value["response_evidence"], "complete")
        self.assertNotEqual(value["catalog_snapshots"], plan["catalog_snapshots"])
        self.assertEqual(value, self.check(pack, plan, transport, result, page_size=500))

    def test_no_write_plan_needs_no_receipt_or_approval(self):
        for released in (False, True):
            pack = manifest(released=released)
            transport = FingerprintReads(catalog(pack))
            plan = plan_installation(pack, request(), transport)
            value = self.check(pack, plan, transport)
            self.assertEqual(value["state"], "verified")
            self.assertEqual(value["response_evidence"], "not_required")
            self.assertIsNone(value["apply_result_digest"])
            supplied = execution_artifact(plan, approval(plan), [], state="applied")
            self.assertEqual(value, self.check(pack, plan, transport, supplied))
            supplied["approval_digest"] = "f" * 64
            invalid = self.check(pack, plan, transport, a.seal(supplied))
            self.assertEqual(invalid["state"], "mismatch")
            self.assertEqual(invalid["response_evidence"], "invalid")
            self.assertIsNone(invalid["apply_result_digest"])

    def test_missing_and_partial_evidence_cannot_verify_matching_state(self):
        pack, plan, approved, result, transport = self.installed()
        no_result = self.check(pack, plan, transport)
        self.assertEqual(no_result["state"], "mismatch")
        self.assertEqual(no_result["response_evidence"], "missing")
        self.assertTrue(all(o["state"] == "equivalent" for o in no_result["object_results"]))
        self.assertIsNone(no_result["apply_result_digest"])
        for count in (0, 1, len(plan["actions"]) - 1):
            failure = {"action_id": plan["actions"][count]["action_id"], "error": {
                "category": "transport_or_environment_failure", "code": "lost_response", "message": "Lost response", "facts": []}}
            partial = execution_artifact(plan, approved, result["accepted_responses"][:count], state="partial", failure=failure)
            value = self.check(pack, plan, transport, partial)
            self.assertEqual(value["state"], "mismatch")
            self.assertEqual(value["response_evidence"], "missing")
        failed = execution_artifact(plan, approved, [], state="not_applied", failure=failure)
        self.assertEqual(self.check(pack, plan, transport, failed)["response_evidence"], "missing")

    def test_invalid_captured_evidence_is_separate_from_matching_state(self):
        pack, plan, _, result, transport = self.installed()
        mutations = [
            lambda r: r.update(plan_digest="f" * 64),
            lambda r: r.update(approval_digest="f" * 64),
            lambda r: r["execution"].update(actor_subject_id="other_actor"),
            lambda r: r["execution"].update(action_timestamp_utc="2026-01-01T00:00:00Z"),
            lambda r: r["accepted_responses"].reverse(),
            lambda r: r["accepted_responses"].pop(),
            lambda r: r["accepted_responses"][0].update(command_id="spack_" + "f" * 64),
            lambda r: r["accepted_responses"][0].update(semantic_facts_hash="f" * 64),
            lambda r: r["accepted_responses"][0]["generated_ids"][0].update(value="wrong_id"),
            lambda r: r["accepted_responses"][0]["response"].update(canonical_json="{}"),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                bad = deepcopy(result)
                mutate(bad)
                value = self.check(pack, plan, transport, a.seal(bad))
                self.assertEqual(value["state"], "mismatch")
                self.assertEqual(value["response_evidence"], "invalid")

    def test_replayed_outcome_is_accepted_without_replaying_a_write(self):
        pack, plan, _, result, transport = self.installed()
        for evidence in result["accepted_responses"]:
            evidence["outcome"] = "compatible_replay"
        self.assertEqual(self.check(pack, plan, transport, a.seal(result))["state"], "verified")

    def test_missing_retired_and_semantically_drifted_selected_objects(self):
        for name in CATALOGS:
            for change in ("missing", "retired", "drift"):
                if name == "bindings" and change == "retired":
                    continue  # Active-binding list represents retirement as absence.
                with self.subTest(name=name, change=change):
                    pack, plan, _, result, transport = self.installed()
                    field = CATALOGS[name][1]
                    row = next(e for e in transport.entries[name] if "unrelated" not in e[field])
                    if change == "missing":
                        transport.entries[name].remove(row)
                    elif change == "retired":
                        row.update(status="retired", retired_by_subject_id="operator", retired_by_command_id="retire",
                                   retired_at_utc="2026-09-14T00:00:00Z", retirement_reason="Retired")
                    elif name == "archetypes":
                        row["revision"]["description"] = "Changed content"
                    elif name == "profiles":
                        row["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "2"
                    else:
                        row["notification_profile_id"] = next(e["notification_profile_id"] for e in transport.entries["profiles"]
                                                              if e["profile_key"] == "unrelated_standard")
                    value = self.check(pack, plan, transport, result)
                    self.assertEqual(value["state"], "mismatch")
                    self.assertEqual(value["response_evidence"], "complete")

    def test_profile_metadata_and_binding_identity_drift(self):
        pack, plan, _, result, transport = self.installed()
        row = next(e for e in transport.entries["profiles"] if e["profile_key"] == "lesson_standard")
        row["description"] = "Metadata drift"
        value = self.check(pack, plan, transport, result)
        self.assertEqual(next(o["state"] for o in value["object_results"] if o["object_key"] == "profile:lesson_standard"), "drifted")
        pack, plan, _, result, transport = self.installed()
        row = next(e for e in transport.entries["profiles"] if e["profile_key"] == "lesson_standard")
        old_id = row["notification_profile_id"]
        row["notification_profile_id"] = row["revision"]["notification_profile_id"] = "replacement_root"
        for binding in transport.entries["bindings"]:
            if binding["notification_profile_id"] == old_id:
                binding["notification_profile_id"] = "replacement_root"
        value = self.check(pack, plan, transport, result)
        self.assertEqual(value["state"], "mismatch")
        for key in ("profile:lesson_standard", "binding:lesson"):
            self.assertEqual(next(o["state"] for o in value["object_results"] if o["object_key"] == key), "drifted")

    def test_unselected_changes_and_equivalent_new_revision_are_not_excess_or_drift(self):
        pack, plan, _, result, transport = self.installed()
        outsider = next(e for e in transport.entries["profiles"] if e["profile_key"] == "unrelated_standard")
        outsider["display_name"] = "Unrelated edit"
        row = next(e for e in transport.entries["archetypes"] if e["archetype_key"] == "lesson")
        row["current_revision_id"] = row["revision"]["item_archetype_revision_id"] = "later_equivalent_revision"
        row["revision"]["revision_number"] += 1
        value = self.check(pack, plan, transport, result)
        self.assertEqual(value["state"], "verified")
        self.assertNotIn("profile:unrelated_standard", [o["object_key"] for o in value["object_results"]])

    def test_granular_selection_excludes_other_pack_members(self):
        pack = manifest("medical_and_lesson", released=True)
        entries = catalog(pack)
        transport = FingerprintReads(entries)
        plan = plan_installation(pack, request({"mode": "archetypes", "archetype_keys": ["lesson"]}), transport)
        transport.entries["profiles"][1]["display_name"] = "Unselected drift"
        value = self.check(pack, plan, transport)
        self.assertEqual(value["state"], "verified")
        self.assertEqual(value["closure"]["archetype_keys"], ["lesson"])
        self.assertEqual(len(value["object_results"]), 3)

    def test_invalid_inputs_stop_before_reads(self):
        pack, plan, _, result, _ = self.installed()
        cases = []
        bad = deepcopy(result); bad["content_identity"]["digest"] = "0" * 64
        cases.append((pack, plan, bad))
        cases.append((pack, plan, {"artifact_schema": "spine.pack-apply-checkpoint.v1"}))
        bad = deepcopy(plan); bad["content_identity"]["digest"] = "0" * 64
        cases.append((pack, bad, result))
        changed = deepcopy(pack); changed["archetypes"][0]["revision"]["description"] = "New manifest"
        changed["content_identity"]["digest"] = content_digest(changed)
        cases.append((changed, plan, result))
        bad = deepcopy(plan)
        bad["actions"] = []; bad["decision_action_ids"] = []
        cases.append((pack, a.seal(bad), None))
        bad = deepcopy(plan)
        action = next(v for v in bad["actions"] if v["command"] == "item_archetype.create")
        body = json.loads(action["request_template"]["canonical_json"])
        body["revision"]["description"] = "Not the selected pack definition"
        action["request_template"]["canonical_json"] = a.canonical_text(body)
        cases.append((pack, a.seal(bad), None))
        for inputs in cases:
            transport = FakeSpine()
            with self.assertRaises(PlanError):
                verify_installation(inputs[0], inputs[1], transport, inputs[2])
            self.assertEqual(transport.calls, [])

    def test_malformed_or_ambiguous_public_readback_fails_closed(self):
        pack = manifest(released=True)
        plan = plan_installation(pack, request(), FakeSpine(catalog(pack)))
        for change in ("duplicate", "owner", "show", "cursor"):
            transport = FakeSpine(catalog(pack))
            if change == "duplicate":
                transport.entries["archetypes"].append(deepcopy(transport.entries["archetypes"][0]))
            elif change == "owner":
                transport.entries["archetypes"][0]["owner_subject_id"] = "other_owner"
            else:
                def mutate(command, query, response, calls):
                    if change == "show" and command.endswith(".show"):
                        response["response_contract"] = "wrong.contract"
                    if change == "cursor" and command.endswith(".list"):
                        response["has_more"] = True
                transport.mutate = mutate
            with self.assertRaises(PlanError):
                verify_installation(pack, plan, transport)

    def test_compatibility_and_target_checks_precede_catalog_use(self):
        pack = manifest(released=True)
        plan = plan_installation(pack, request(), FakeSpine(catalog(pack)))
        for mutate in (lambda t: t.info.update(runtime_version="0.4.0"),
                       lambda t: t.info.update(ledger_schema_version="13"),
                       lambda t: t.info["implemented_contract_versions"].pop()):
            transport = FakeSpine(catalog(pack)); mutate(transport)
            with self.assertRaises(PlanError):
                verify_installation(pack, plan, transport)
            self.assertEqual([c for c, _ in transport.calls], ["system.info"])
        transport = FakeSpine(catalog(pack))
        with patch.object(transport, "check_target", side_effect=PlanError("stale_plan_or_target_mismatch", "target_binding_mismatch")):
            with self.assertRaises(PlanError):
                verify_installation(pack, plan, transport)
        self.assertEqual(transport.calls, [])

    def test_transport_read_path_cannot_launch_writes(self):
        pack, plan, _, result, fake = self.installed()
        transport = SpineCommand(plan["request"]["target"])
        def invoke(command, body):
            self.assertIn(command, READ_COMMANDS)
            return fake.read(command, body), 0
        with patch.object(transport, "check_target"), patch.object(transport, "_invoke", side_effect=invoke), \
                patch.object(transport, "write", side_effect=AssertionError("write not allowed")):
            self.assertEqual(verify_installation(pack, plan, transport, result)["state"], "verified")

    def test_cli_success_mismatch_and_input_protection(self):
        for with_result in (True, False):
            with tempfile.TemporaryDirectory() as directory:
                folder = Path(directory)
                pack, plan, _, result, transport = self.installed()
                for name, value in (("manifest.json", pack), ("plan.json", plan), ("apply.json", result)):
                    publish(folder / name, value)
                args = ["verify", "--manifest", str(folder / "manifest.json"), "--plan", str(folder / "plan.json"),
                        "--output", str(folder / "verification.json")]
                if with_result:
                    args += ["--result", str(folder / "apply.json")]
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    code = main(args, transport_factory=lambda _: transport)
                self.assertEqual(code, 0 if with_result else 10, stdout.getvalue())
                envelope = json.loads(stdout.getvalue())
                self.assertEqual(envelope["operation"], "verify")
                self.assertEqual(independent.envelope_errors(envelope), [])
                self.assertEqual(len(stdout.getvalue().splitlines()), 1)
                self.assertEqual((folder / "verification.json").stat().st_mode & 0o777, 0o600)
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(main(args, transport_factory=lambda _: self.fail("output exists")), 2)
                for forbidden in (plan["request"]["target"]["ledger"]["path"], plan["request"]["target"]["spine_command"]["path"]):
                    collided = args[:]
                    if with_result:
                        collided[collided.index("--result") + 1] = forbidden
                    else:
                        collided += ["--result", forbidden]
                    with patch("spine_packs.__main__.load_input", wraps=load_input) as reader:
                        with contextlib.redirect_stdout(io.StringIO()) as stdout:
                            self.assertEqual(main(collided, transport_factory=lambda _: self.fail("target collision")), 2)
                        self.assertNotIn(forbidden, [c.args[0] for c in reader.call_args_list])
                    self.assertEqual(json.loads(stdout.getvalue())["error"]["code"], "verification_result_input_collision")

    def test_cli_rejects_mutating_flags_and_never_publishes_on_read_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            pack = manifest(released=True)
            transport = FakeSpine(catalog(pack))
            plan = plan_installation(pack, request(), transport)
            publish(folder / "manifest.json", pack); publish(folder / "plan.json", plan)
            args = ["verify", "--manifest", str(folder / "manifest.json"), "--plan", str(folder / "plan.json"),
                    "--output", str(folder / "out.json")]
            for extra in (["--approval", "unused"], ["--checkpoint", "unused"], ["--continue-from", "unused"],
                          ["--request", "unused"], ["--all"], ["--archetype", "lesson"]):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(main(args + extra, transport_factory=lambda _: self.fail("invalid flags")), 2)
            transport.info["runtime_version"] = "0.4.0"
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(main(args, transport_factory=lambda _: transport), 4)
            self.assertIsNone(json.loads(stdout.getvalue())["artifact"])
            self.assertFalse((folder / "out.json").exists())


if __name__ == "__main__":
    unittest.main()
