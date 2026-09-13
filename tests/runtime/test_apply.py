"""Initial apply checkpoints before writes and never advances on invalid evidence."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest
import json
import tempfile
import contextlib
import io
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.apply import apply_initial, command_id, checkpoint_writer
from spine_packs.execution import materialize, validate_prefix, validate_artifact
from spine_packs.__main__ import main
from spine_packs.spine_command import SpineCommand
from spine_packs.planning import ENVIRONMENT, PlanError, plan_installation
from test_apply_preflight import approval
from test_planning import FakeSpine, manifest, request, catalog
import test_installer_artifact_contract as independent


class WritableFake(FakeSpine):
    def __init__(self, *, fail_at=None, malformed_at=None):
        super().__init__()
        self.writes = []
        self.fail_at = fail_at
        self.malformed_at = malformed_at

    def write(self, command, request_body):
        index = len(self.writes)
        self.writes.append((command, deepcopy(request_body)))
        if index == self.fail_at:
            raise PlanError("spine_command_rejection", "spine_write_rejected")
        receipt = {
            "command_receipt_id": f"receipt_{index}",
            "command_id": request_body["command_id"],
            "effect": {
                "item_archetype.create": "item_archetype_created",
                "notification_profile.create": "notification_profile_created",
                "notification_profile.binding.set": "notification_profile_binding_set",
            }[command],
            "semantic_facts_hash": a.digest(request_body),
            "created_at_utc": request_body["action_timestamp_utc"],
        }
        if command == "item_archetype.create":
            response = {"ok": True, "command": command, "response_contract": "spine.item-archetypes.v1",
                "effect": receipt["effect"], "item_archetype_id": "created_archetype",
                "item_archetype_revision_id": "created_archetype_revision", "revision_number": "1",
                "status": "active", "archetype_key": request_body["archetype_key"], "receipt": receipt}
        elif command == "notification_profile.create":
            response = {"ok": True, "command": command, "response_contract": "spine.notification-profiles.v1",
                "effect": receipt["effect"], "notification_profile_id": "created_profile",
                "notification_profile_revision_id": "created_profile_revision", "status": "active",
                "revision_number": "1", "normalized_revision_hash": "b" * 64,
                "profile_key": request_body["profile_key"], "receipt": receipt}
        else:
            response = {"ok": True, "command": command,
                "response_contract": "spine.notification-profile-bindings.v1", "effect": receipt["effect"],
                "notification_profile_binding_id": "created_binding",
                "item_archetype_id": request_body["item_archetype_id"],
                "notification_profile_id": request_body["notification_profile_id"],
                "status": "active", "compatible_item_types": ["event"], "receipt": receipt}
        if index == self.malformed_at:
            response["receipt"]["command_id"] = "wrong"
        return response


class InitialApplyTests(unittest.TestCase):
    def setup(self, transport=None):
        pack = manifest(released=True)
        transport = transport or WritableFake()
        plan = plan_installation(pack, request(), transport)
        return pack, plan, approval(plan), transport

    def test_command_identity_is_deterministic_and_bound(self):
        value = command_id("a" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000")
        self.assertRegex(value, r"^spack_[0-9a-f]{64}$")
        self.assertEqual(value, command_id("a" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000"))
        self.assertNotEqual(value, command_id("b" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000"))

    def test_initial_apply_checkpoints_before_every_write_and_materializes_ids(self):
        pack, plan, approved, transport = self.setup()
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, lambda value: checkpoints.append(value))
        self.assertEqual(result["state"], "applied")
        self.assertEqual(len(result["accepted_responses"]), 3)
        self.assertEqual(len(checkpoints), 6)
        for index, (_, body) in enumerate(transport.writes):
            prepared = checkpoints[index * 2]
            self.assertEqual(prepared["unresolved_submission"]["request"]["canonical_json"], a.canonical_text(body))
            self.assertEqual(prepared["unresolved_submission"]["command_id"], body["command_id"])
            self.assertEqual(a.validate_schema(prepared), [])
            self.assertEqual(a.content_digest_errors(prepared), [])
        binding = transport.writes[-1][1]
        self.assertEqual(binding["item_archetype_id"], "created_archetype")
        self.assertEqual(binding["notification_profile_id"], "created_profile")
        self.assertIsNone(checkpoints[-1]["next_action_id"])
        self.assertEqual(a.validate_schema(result), [])
        self.assertEqual(a.content_digest_errors(result), [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
        for checkpoint in checkpoints:
            self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])

    def test_rejection_stops_at_first_action_and_preserves_unresolved_checkpoint(self):
        transport = WritableFake(fail_at=1)
        pack, plan, approved, transport = self.setup(transport)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "partial")
        self.assertEqual([x["action_id"] for x in result["accepted_responses"]], ["action-000000"])
        self.assertEqual(result["failure"]["action_id"], "action-000001")
        self.assertEqual(result["unattempted_action_ids"], ["action-000002"])
        self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], "action-000001")
        self.assertEqual(len(transport.writes), 2)

    def test_invalid_response_never_advances_checkpoint(self):
        transport = WritableFake(malformed_at=0)
        pack, plan, approved, transport = self.setup(transport)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["accepted_responses"], [])
        self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], "action-000000")

    def test_checkpoint_failure_happens_before_transport(self):
        pack, plan, approved, transport = self.setup()
        def fail(_value):
            raise OSError("synthetic checkpoint failure")
        with self.assertRaises(OSError):
            apply_initial(pack, plan, approved, transport, fail)
        self.assertEqual(transport.writes, [])

    def test_rejects_wrong_key_timestamp_hash_and_binding_ids(self):
        mutations = [
            (0, lambda r: r.update(archetype_key="wrong_key")),
            (1, lambda r: r.update(profile_key="wrong_key")),
            (0, lambda r: r["receipt"].update(created_at_utc="2000-01-01T00:00:00Z")),
            (0, lambda r: r["receipt"].update(semantic_facts_hash="0" * 64)),
            (2, lambda r: r.update(item_archetype_id="wrong_root")),
            (2, lambda r: r.update(notification_profile_id="wrong_profile")),
            (0, lambda r: r.update(revision_number="2")),
            (0, lambda r: r.update(item_archetype_id="${not_an_id}")),
            (0, lambda r: r.update(revision_number=1)),
            (0, lambda r: r.update(response_contract="wrong")),
            (0, lambda r: r["receipt"].update(effect="wrong")),
            (0, lambda r: r.update(extra="not_allowed")),
        ]
        for index, mutate in mutations:
            with self.subTest(index=index, mutate=mutate):
                class Corrupt(WritableFake):
                    def write(self, command, body):
                        value = super().write(command, body)
                        if len(self.writes) - 1 == index: mutate(value)
                        return value
                pack, plan, approved, transport = self.setup(Corrupt())
                checkpoints = []
                result = apply_initial(pack, plan, approved, transport, checkpoints.append)
                self.assertEqual(result["state"], "partial")
                self.assertEqual(len(result["accepted_responses"]), index)
                self.assertEqual(len(transport.writes), index + 1)
                self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], f"action-{index:06d}")
                self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_first_rejection_is_partial_with_empty_accepted_prefix(self):
        pack, plan, approved, transport = self.setup(WritableFake(fail_at=0))
        result = apply_initial(pack, plan, approved, transport, lambda value: None)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["accepted_responses"], [])
        self.assertEqual(result["unattempted_action_ids"], ["action-000001", "action-000002"])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_binding_recheck_stops_changed_state_before_binding_write(self):
        pack, plan, approved, transport = self.setup()
        checkpoints = []
        def save(value):
            checkpoints.append(value)
            if len(value["accepted_responses"]) == 2:
                binding = catalog(pack)["bindings"][0]
                binding["item_archetype_id"] = "created_archetype"
                binding["notification_profile_id"] = "unexpected_profile"
                transport.entries["bindings"] = [binding]
        result = apply_initial(pack, plan, approved, transport, save)
        self.assertEqual(len(transport.writes), 2)
        self.assertEqual(result["failure"]["error"]["code"], "binding_precondition_changed")
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_stale_preflight_has_not_applied_artifact_without_checkpoint(self):
        pack, plan, approved, transport = self.setup()
        transport.entries = catalog(pack)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "not_applied")
        self.assertEqual(result["failure"]["error"]["category"], "stale_plan_or_target_mismatch")
        self.assertEqual(result["unattempted_action_ids"], [x["action_id"] for x in plan["actions"]])
        self.assertEqual(checkpoints, [])
        self.assertEqual(transport.writes, [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_no_write_plan_completes_with_empty_evidence(self):
        pack = manifest(released=True)
        transport = WritableFake()
        transport.entries = catalog(pack)
        plan = plan_installation(pack, request(), transport)
        approved = approval(plan)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "applied")
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(transport.writes, [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_every_checkpoint_boundary_failure_stops_execution(self):
        for boundary in range(6):
            with self.subTest(boundary=boundary):
                pack, plan, approved, transport = self.setup()
                durable = []
                def write(value):
                    if len(durable) == boundary:
                        raise OSError("simulated disk failure")
                    durable.append(deepcopy(value))
                with self.assertRaises(OSError):
                    apply_initial(pack, plan, approved, transport, write)
                self.assertEqual(len(transport.writes), (boundary + 1) // 2)
                for checkpoint in durable:
                    self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])

    def test_crash_at_each_submission_leaves_prepared_checkpoint(self):
        for boundary in range(3):
            with self.subTest(boundary=boundary):
                class Crash(WritableFake):
                    def write(self, command, body):
                        value = super().write(command, body)
                        if len(self.writes) == boundary + 1: raise KeyboardInterrupt()
                        return value
                pack, plan, approved, transport = self.setup(Crash())
                durable = []
                with self.assertRaises(KeyboardInterrupt):
                    apply_initial(pack, plan, approved, transport, durable.append)
                self.assertEqual(durable[-1]["next_action_id"], f"action-{boundary:06d}")
                self.assertIsNotNone(durable[-1]["unresolved_submission"])
                self.assertEqual(independent.checkpoint_errors(durable[-1], plan, approved), [])

    def test_materialization_rejects_tampered_or_gapped_prefix(self):
        pack, plan, approved, transport = self.setup()
        result = apply_initial(pack, plan, approved, transport, lambda value: None)
        responses = result["accepted_responses"][:2]
        bad_prefixes = [responses[:1], list(reversed(responses))]
        tampered = deepcopy(responses)
        tampered[0]["generated_ids"][0]["value"] = "untrusted"
        bad_prefixes.append(tampered)
        for prefix in bad_prefixes:
            with self.assertRaises(PlanError):
                materialize(plan, approved, 2, prefix)
        valid = materialize(plan, approved, 2, responses)
        self.assertEqual(valid, transport.writes[2][1])

    def test_metadata_and_revision_updates_and_binding_replacement(self):
        class DriftFake(WritableFake):
            def write(self, command, body):
                if command == "notification_profile.binding.set":
                    return super().write(command, body)
                self.writes.append((command, deepcopy(body)))
                if command == "notification_profile.metadata.update":
                    effect = "notification_profile_metadata_updated"
                    facts = {"notification_profile_id": body["notification_profile_id"],
                             "notification_profile_revision_id": "unchanged_revision", **body["metadata"]}
                else:
                    kind = command.removesuffix(".revise")
                    effect = kind + "_revised"
                    facts = {kind + "_id": body[kind + "_id"], kind + "_revision_id": "new_revision",
                             "revision_number": "2"}
                    if kind == "notification_profile": facts["normalized_revision_hash"] = "b" * 64
                contract = a.COMMAND_SHAPES[command][1]
                return {"ok": True, "command": command, "response_contract": contract, "effect": effect,
                        "status": "active", **facts, "receipt": {
                            "command_id": body["command_id"], "command_receipt_id": "drift_receipt_" + str(len(self.writes)),
                            "effect": effect, "created_at_utc": body["action_timestamp_utc"],
                            "semantic_facts_hash": a.digest(body)}}
        pack = manifest("medical_and_lesson", released=True)
        entries = catalog(pack)
        entries["archetypes"][0]["revision"]["description"] = "Old"
        entries["profiles"][0]["display_name"] = "Old"
        entries["profiles"][0]["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "1"
        entries["bindings"][0]["notification_profile_id"] = entries["profiles"][1]["notification_profile_id"]
        transport = DriftFake()
        transport.entries = entries
        plan = plan_installation(pack, request(), transport)
        approved = approval(plan)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "applied")
        self.assertEqual([x[0] for x in transport.writes], ["item_archetype.revise", "notification_profile.metadata.update",
                                                         "notification_profile.revise", "notification_profile.binding.set"])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
        for checkpoint in checkpoints:
            self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])


class DurableCheckpointTests(unittest.TestCase):
    def checkpoints(self):
        case = InitialApplyTests()
        pack, plan, approved, transport = case.setup()
        values = []
        apply_initial(pack, plan, approved, transport, values.append)
        return values

    def test_private_atomic_replacement_and_existing_file_refusal(self):
        values = self.checkpoints()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            writer = checkpoint_writer(path)
            for value in values:
                writer(value)
                self.assertEqual(a.load_json(path), value)
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            before = path.read_bytes()
            with self.assertRaises(PlanError): checkpoint_writer(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).glob(".spine-checkpoint-*")), [])

    def test_no_clobber_on_first_publication_race(self):
        value = self.checkpoints()[0]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            writer = checkpoint_writer(path)
            path.write_bytes(b"unrelated")
            with self.assertRaises(PlanError): writer(value)
            self.assertEqual(path.read_bytes(), b"unrelated")

    def test_replacement_detects_external_change_and_symlink(self):
        values = self.checkpoints()
        for symlink in (False, True):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "checkpoint.json"
                writer = checkpoint_writer(path)
                writer(values[0])
                if symlink:
                    path.unlink()
                    other = Path(directory) / "other"
                    other.write_bytes(b"preserve")
                    path.symlink_to(other)
                else: path.write_bytes(b"preserve")
                with self.assertRaises(PlanError): writer(values[1])
                self.assertEqual(path.read_bytes(), b"preserve")

    def test_fsync_and_replace_failures_leave_valid_evidence_and_clean_temps(self):
        values = self.checkpoints()
        for phase in ("file_fsync", "replace", "directory_fsync"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "checkpoint.json"
                writer = checkpoint_writer(path)
                writer(values[0])
                target = "spine_packs.apply.os.replace" if phase == "replace" else "spine_packs.apply.os.fsync"
                effect = [None, OSError("disk failure")] if phase == "directory_fsync" else OSError("disk failure")
                with patch(target, side_effect=effect), self.assertRaises(PlanError): writer(values[1])
                self.assertEqual(a.load_json(path), values[1] if phase == "directory_fsync" else values[0])
                self.assertEqual(list(Path(directory).glob(".spine-checkpoint-*")), [])

    def test_byte_limits_fail_before_publication(self):
        value = self.checkpoints()[0]
        key = value["artifact_schema"]
        size = len(a.canonical_text(value).encode())
        with patch.dict(a.SIZE_LIMITS, {key: size}): validate_artifact(value)
        with tempfile.TemporaryDirectory() as directory, patch.dict(a.SIZE_LIMITS, {key: size - 1}):
            path = Path(directory) / "checkpoint.json"
            with self.assertRaises(PlanError): checkpoint_writer(path)(value)
            self.assertFalse(path.exists())


class ApplyCliTests(unittest.TestCase):
    def invoke(self, directory, transport=None, **changes):
        pack, plan, approved, fake = InitialApplyTests().setup()
        directory = Path(directory)
        paths = {k: directory / (k + ".json") for k in ("manifest", "plan", "approval", "checkpoint", "output")}
        for key, value in (("manifest", pack), ("plan", plan), ("approval", approved)):
            paths[key].write_text(a.canonical_text(value), encoding="utf-8")
        paths.update(changes)
        args = ["apply"]
        for key, value in paths.items(): args.extend(["--" + key, str(value)])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(args, transport_factory=lambda target: transport or fake)
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        envelope = json.loads(output.getvalue())
        self.assertEqual(envelope["operation"], "apply")
        self.assertEqual(independent.envelope_errors(envelope), [])
        return code, envelope, paths, fake

    def test_success_and_partial_cli_artifacts(self):
        for transport, expected in ((WritableFake(), 0), (WritableFake(fail_at=0), 9)):
            with tempfile.TemporaryDirectory() as directory:
                code, envelope, paths, _ = self.invoke(directory, transport)
                self.assertEqual(code, expected)
                result = a.load_json(paths["output"])
                self.assertEqual(independent.apply_result_errors(result, a.load_json(paths["plan"]), a.load_json(paths["approval"])), [])
                self.assertEqual(envelope["artifact"]["digest"], result["content_identity"]["digest"])

    def test_stale_plan_exit_and_no_checkpoint(self):
        transport = WritableFake()
        transport.entries = catalog(manifest(released=True))
        with tempfile.TemporaryDirectory() as directory:
            code, envelope, paths, _ = self.invoke(directory, transport)
            self.assertEqual(code, 7)
            self.assertEqual(a.load_json(paths["output"])["state"], "not_applied")
            self.assertFalse(paths["checkpoint"].exists())

    def test_checkpoint_input_and_output_collisions_fail_before_transport(self):
        for name in ("manifest", "plan", "approval", "output"):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / (name + ".json")
                code, _, _, transport = self.invoke(directory, checkpoint=path)
                self.assertEqual(code, 2)
                self.assertEqual(transport.writes, [])

    def test_public_write_allowlist_and_invalid_rejections(self):
        transport = SpineCommand({})
        with patch.object(transport, "_invoke") as invoke:
            for command in ("notification_profile.retire", "item.create", "system.info"):
                with self.assertRaises(PlanError): transport.write(command, {})
            invoke.assert_not_called()
        pack, plan, approved, _ = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        invalid = {"ok": False, "command": "item_archetype.create"}
        with patch.object(transport, "_invoke", return_value=(invalid, 3)), self.assertRaises(PlanError) as caught:
            transport.write("item_archetype.create", body)
        self.assertEqual(caught.exception.category, ENVIRONMENT)

    def test_write_rejection_preserves_only_bounded_machine_code(self):
        _, plan, approved, _ = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        response = {"ok": False, "command": "item_archetype.create", "error": {
            "code": "semantic_conflict:archetype_key", "message": "private unrelated text", "field": None}}
        transport = SpineCommand({})
        with patch.object(transport, "_invoke", return_value=(response, 3)), self.assertRaises(PlanError) as caught:
            transport.write("item_archetype.create", body)
        self.assertEqual(caught.exception.facts, [{"name": "spine_error_code", "value": "semantic_conflict:archetype_key"}])
        self.assertNotIn("private", str(caught.exception))

    def test_real_fake_process_receives_exact_write_request(self):
        _, plan, approved, fake = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        response = fake.write("item_archetype.create", body)
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "fake-spine-command"
            executable.write_text("#!" + sys.executable + "\nimport json,sys\n"
                + "assert sys.argv[1:]==['--db','/not/a/real/ledger','item_archetype.create','--input','-']\n"
                + "assert json.load(sys.stdin)==" + repr(body) + "\n"
                + "print(" + repr(a.canonical_text(response)) + ")\n", encoding="utf-8")
            executable.chmod(0o700)
            transport = SpineCommand({"spine_command": {"path": str(executable)},
                                      "ledger": {"path": "/not/a/real/ledger"}})
            with patch.object(transport, "check_target"):
                self.assertEqual(transport.write("item_archetype.create", body), response)

    def test_result_publication_failure_retains_completed_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory, patch("spine_packs.__main__.publish", side_effect=OSError("disk full")):
            code, envelope, paths, transport = self.invoke(directory)
            self.assertEqual(code, 11)
            self.assertIsNone(envelope["artifact"])
            self.assertEqual(len(transport.writes), 3)
            checkpoint = a.load_json(paths["checkpoint"])
            self.assertIsNone(checkpoint["next_action_id"])
            self.assertEqual(len(checkpoint["accepted_responses"]), 3)

    def test_existing_checkpoint_is_not_a_resume_request(self):
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            checkpoint.write_text("preserve", encoding="utf-8")
            code, _, _, transport = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(transport.writes, [])
            self.assertEqual(checkpoint.read_text(), "preserve")


if __name__ == "__main__":
    unittest.main()
