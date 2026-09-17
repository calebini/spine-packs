"""Opt-in integration against public CLIs and newly allocated disposable ledgers.

Run this file with --help. Ordinary discovery skips these tests. Evidence is
retained on both success and failure; this harness never accepts a ledger path.
No Spine Python imports, SQL, mocked successful responses, or real delivery.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[2]
if "--installed" not in sys.argv:
    sys.path.insert(0, str(ROOT / "src"))

from spine_packs import artifacts as a
from spine_packs.__main__ import main as installer_main
from spine_packs.manifest import content_digest
from spine_packs.planning import PlanError
from spine_packs.spine_command import SpineCommand, WRITE_COMMANDS


def save(path, value):
    """Private no-clobber test evidence, including public JSON with numbers."""
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as out:
        json.dump(value, out, indent=2, sort_keys=True)
        out.write("\n")


class WriteFault(SpineCommand):
    """Test-only loss before submission or after a genuine successful response."""
    def __init__(self, target, command, after_commit):
        super().__init__(target)
        self.command = command
        self.after_commit = after_commit
        self.fired = False
        self.captured = None

    def write(self, command, request):
        if not self.fired and command == self.command:
            self.fired = True
            if self.after_commit:
                self.captured = super().write(command, request)
            raise PlanError("transport_or_environment_failure", "injected_response_loss")
        return super().write(command, request)


class LocalSpineTests(unittest.TestCase):
    config = None

    def setUp(self):
        if self.config is None:
            self.skipTest("opt-in: run this file with explicit public CLI paths")
        self.folder = self.config["root"] / self._testMethodName
        self.folder.mkdir(mode=0o700)
        self.sequence = 0
        self.new_ledger("initial")

    def new_ledger(self, name):
        self.case = self.folder / name
        self.case.mkdir(mode=0o700)
        self.db = self.case / "ledger.sqlite3"
        self.assertFalse(self.db.exists())
        initialized = self.public_process([str(self.config["migrate"]), "--db", str(self.db), "--initialize-if-empty"])
        self.assertEqual(initialized["after_version"], 12)
        self.assertTrue(initialized["initialized"] and initialized["verified"])
        self.target = {"host_name": socket.getfqdn().lower().removesuffix("."),
            "spine_command": {"path": str(self.config["command"]),
                              "sha256": hashlib.sha256(self.config["command"].read_bytes()).hexdigest()},
            "ledger": {"kind": "path", "path": str(self.db.resolve())}}
        info = self.public_process([str(self.config["command"]), "--db", str(self.db), "system.info"])
        self.assertEqual(info["runtime_version"], "0.3.0")
        self.assertEqual(info["ledger_schema_version"], "12")
        self.assertTrue(set(a.REQUIRED_EXECUTION_CONTRACTS) <= set(info["implemented_contract_versions"]))
        self.actor = "slice6_synthetic_operator"
        self.public_process([str(self.config["command"]), "--db", str(self.db), "subject.upsert", "--input", "-"], {
            "command_id": "slice6_bootstrap", "actor_subject_id": self.actor, "subject_id": self.actor,
            "subject_kind": "agent", "display_name": "Disposable Slice 6 test operator",
            "status": "active", "updated_at_utc": "2026-09-17T00:00:00Z"})

    def path(self, label):
        self.sequence += 1
        return self.case / f"{self.sequence:03d}-{label}.json"

    def public_process(self, argv, request=None):
        process = subprocess.run(argv, input=json.dumps(request or {}) + "\n", text=True,
                                 capture_output=True, timeout=30, env=self.config["env"])
        evidence = self.path("setup")
        save(evidence, {"argv": argv, "returncode": process.returncode,
                        "stdout": process.stdout, "stderr": process.stderr})
        self.assertEqual(process.returncode, 0, f"public setup failed; inspect {evidence}")
        return json.loads(process.stdout)

    def pack(self, updated=False):
        # Copy a reviewed format fixture, never change or release a curated pack.
        pack = a.load_json(ROOT / "tests/fixtures/pack-manifest/positive/medical_and_lesson.json")
        pack["pack"] = {"pack_id": "slice6-qualification-only", "version": "1.0.1" if updated else "1.0.0",
                        "status": "released"}
        if updated:
            pack["archetypes"][0]["revision"]["description"] = "Synthetic revised archetype"
            profile = pack["notification_profiles"][0]
            profile["description"] = "Synthetic revised profile metadata"
            profile["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "60"
            pack["binding_intents"][0]["notification_profile_key"] = pack["notification_profiles"][1]["profile_key"]
        pack["content_identity"]["digest"] = content_digest(pack)
        path = self.path("manifest")
        save(path, pack)
        return path

    def invoke(self, operation, expected=0, factory=None, **inputs):
        output = self.path(operation)
        argv = [operation, "--output", str(output)]
        for name, value in inputs.items():
            argv.extend(["--" + name.replace("_", "-"), str(value)])
        if factory is None:
            proc = subprocess.run([*self.config["installer"], *argv], env=self.config["env"],
                                  text=True, capture_output=True, timeout=180)
            code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        else:
            # Only the injected-fault invocation is in-process. Resume is a new CLI process.
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = installer_main(argv, transport_factory=factory)
            stdout, stderr = out.getvalue(), ""
        log = self.path("envelope")
        save(log, {"argv": argv, "exit_code": code, "stdout": stdout, "stderr": stderr})
        self.assertEqual(code, expected, f"unexpected installer exit; inspect {log}")
        self.assertEqual(len(stdout.splitlines()), 1)
        envelope = a.parse_json(stdout.encode("utf-8"))
        self.assertEqual(a.validate_schema(envelope), [])
        self.assertEqual(envelope["exit_code"], str(code))
        if envelope["artifact"] is None:
            self.assertFalse(output.exists())
            return None, envelope
        artifact = a.load_json(output)
        self.assertEqual(a.validate_schema(artifact) + a.content_digest_errors(artifact), [])
        self.assertEqual(artifact["content_identity"]["digest"], envelope["artifact"]["digest"])
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        return output, artifact

    def plan(self, manifest, expected=0, keys=None):
        request = a.seal({"artifact_schema": "spine.pack-install-request.v1", "request": {
            "selection": {"mode": "all"} if keys is None else {"mode": "archetypes", "archetype_keys": keys},
            "owner": {"owner_kind": "subject", "owner_subject_id": self.actor},
            "target": self.target, "draft_posture": "reject"}})
        path = self.path("request")
        save(path, request)
        return self.invoke("plan", expected, manifest=manifest, request=path)

    def approve(self, plan, authorize_updates=True):
        approval = a.seal({"artifact_schema": "spine.pack-install-approval.v1",
            "plan_digest": plan["content_identity"]["digest"], "approve_complete_plan": True,
            "acknowledge_single_operator": True,
            "authorized_update_action_ids": plan["decision_action_ids"] if authorize_updates else [],
            "execution": {"execution_id": str(uuid.uuid4()), "actor_subject_id": self.actor,
                          "action_timestamp_utc": "2026-09-17T01:00:00Z"}})
        path = self.path("approval")
        save(path, approval)
        return path

    def apply(self, manifest, plan, approved, expected=0, factory=None, source=None):
        checkpoint = self.path("checkpoint")
        inputs = dict(manifest=manifest, plan=plan, approval=approved, checkpoint=checkpoint)
        if source is not None:
            inputs["continue_from"] = source
        result, artifact = self.invoke("apply", expected, factory, **inputs)
        if checkpoint.exists():
            value = a.load_json(checkpoint)
            self.assertEqual(a.validate_schema(value) + a.content_digest_errors(value), [])
            self.assertEqual(checkpoint.stat().st_mode & 0o777, 0o600)
        return result, artifact, checkpoint

    def install(self):
        manifest = self.pack()
        plan, value = self.plan(manifest)
        approved = self.approve(value)
        result, applied, _ = self.apply(manifest, plan, approved)
        self.assertEqual(applied["state"], "applied")
        _, verified = self.invoke("verify", manifest=manifest, plan=plan, result=result)
        self.assertEqual(verified["state"], "verified")
        return manifest, plan, result

    def test_install_retain_granular_drift_and_verify(self):
        manifest, original_plan, result = self.install()
        plan, retained = self.plan(manifest)
        self.assertEqual(retained["actions"], [])
        _, verified = self.invoke("verify", manifest=manifest, plan=plan)
        self.assertEqual(verified["response_evidence"], "not_required")
        _, selected = self.plan(manifest, keys=["lesson"])
        self.assertEqual(selected["closure"]["archetype_keys"], ["lesson"])
        self.assertEqual(len(selected["classifications"]), 3)
        _, missing = self.invoke("verify", 10, manifest=manifest, plan=original_plan)
        self.assertEqual(missing["response_evidence"], "missing")
        updated = self.pack(updated=True)
        update_plan, drift = self.plan(updated, expected=5)
        self.assertEqual({x["command"] for x in drift["actions"]}, {
            "item_archetype.revise", "notification_profile.metadata.update",
            "notification_profile.revise", "notification_profile.binding.set"})
        refused = self.approve(drift, authorize_updates=False)
        _, error, checkpoint = self.apply(updated, update_plan, refused, expected=2)
        self.assertFalse(checkpoint.exists())
        self.assertEqual(error["error"]["category"], "invalid_cli_or_artifact_input")
        _, still_original = self.invoke("verify", manifest=manifest, plan=original_plan, result=result)
        self.assertEqual(still_original["state"], "verified")
        new_result, _, _ = self.apply(updated, update_plan, self.approve(drift))
        _, verified = self.invoke("verify", manifest=updated, plan=update_plan, result=new_result)
        self.assertEqual(verified["state"], "verified")
        _, mismatch = self.invoke("verify", 10, manifest=manifest, plan=original_plan, result=result)
        self.assertEqual(mismatch["state"], "mismatch")
        _, stale, checkpoint = self.apply(manifest, plan, self.approve(retained), expected=7)
        self.assertFalse(checkpoint.exists())
        self.assertEqual(stale["state"], "not_applied")
        self.assertEqual(stale["failure"]["error"]["category"], "stale_plan_or_target_mismatch")

    def test_partial_before_submission_continues_from_result(self):
        manifest = self.pack()
        plan, value = self.plan(manifest)
        approved = self.approve(value)
        fault = WriteFault(self.target, "notification_profile.create", False)
        result, partial, _ = self.apply(manifest, plan, approved, expected=9, factory=lambda _: fault)
        self.assertTrue(fault.fired)
        self.assertEqual(len(partial["accepted_responses"]), 2)
        preserved = result.read_bytes()
        recovered, _, _ = self.apply(manifest, plan, approved, source=result)
        self.assertEqual(result.read_bytes(), preserved)
        _, verified = self.invoke("verify", manifest=manifest, plan=plan, result=recovered)
        self.assertEqual(verified["state"], "verified")

    def test_existing_output_and_ledger_input_are_refused(self):
        manifest, plan, result = self.install()
        preserved = plan.read_bytes()
        args = [*self.config["installer"], "verify", "--manifest", str(manifest),
                "--plan", str(plan), "--result", str(result), "--output", str(plan)]
        proc = subprocess.run(args, env=self.config["env"], text=True, capture_output=True, timeout=30)
        save(self.path("no-clobber-envelope"), {"argv": args, "exit_code": proc.returncode,
                                               "stdout": proc.stdout, "stderr": proc.stderr})
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["error"]["code"], "output_already_exists")
        self.assertEqual(plan.read_bytes(), preserved)
        _, error = self.invoke("verify", 2, manifest=manifest, plan=plan, result=self.db)
        self.assertEqual(error["error"]["code"], "verification_result_input_collision")
        _, verified = self.invoke("verify", manifest=manifest, plan=plan, result=result)
        self.assertEqual(verified["state"], "verified")

    def test_lost_response_recovers_each_write_kind(self):
        for command in sorted(WRITE_COMMANDS):
            with self.subTest(command=command):
                self.new_ledger(command.replace(".", "-"))
                if command.endswith(".revise") or command.endswith(".update"):
                    self.install()
                    manifest = self.pack(updated=True)
                    plan, value = self.plan(manifest, expected=5)
                else:
                    manifest = self.pack()
                    plan, value = self.plan(manifest)
                approved = self.approve(value)
                fault = WriteFault(self.target, command, True)
                _, partial, checkpoint = self.apply(manifest, plan, approved, expected=9, factory=lambda _: fault)
                self.assertTrue(fault.fired)
                self.assertIsNotNone(fault.captured)
                save(self.path("discarded-real-response"), fault.captured)
                preserved = checkpoint.read_bytes()
                result, applied, _ = self.apply(manifest, plan, approved, source=checkpoint)
                self.assertEqual(checkpoint.read_bytes(), preserved)
                index = len(partial["accepted_responses"])
                replay = json.loads(applied["accepted_responses"][index]["response"]["canonical_json"])
                self.assertEqual(replay, fault.captured)
                _, verified = self.invoke("verify", manifest=manifest, plan=plan, result=result)
                self.assertEqual(verified["state"], "verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spine-command", required=True, type=Path)
    parser.add_argument("--spine-ledger-migrate", required=True, type=Path)
    parser.add_argument("--evidence-parent", type=Path, default=Path(tempfile.gettempdir()))
    parser.add_argument("--test", action="append", help="optional exact unittest method name")
    parser.add_argument("--installed", action="store_true",
                        help="test this virtual environment's installed CLI; never add checkout src")
    args = parser.parse_args()
    command = args.spine_command.resolve(strict=True)
    migrate = args.spine_ledger_migrate.resolve(strict=True)
    if command.parent != migrate.parent or not all(os.access(p, os.X_OK) and p.is_file() for p in (command, migrate)):
        parser.error("use public executables from the same isolated Spine installation")
    run = Path(tempfile.mkdtemp(prefix="spine-packs-integration-", dir=args.evidence_parent)).resolve()
    env = os.environ.copy()
    if args.installed:
        prefix = Path(sys.prefix).resolve()
        installed_cli = prefix / "bin/spine-packs"
        if (sys.prefix == sys.base_prefix or not installed_cli.is_file()
                or not Path(a.__file__).resolve().is_relative_to(prefix)
                or a.SCHEMA_ROOT != Path(a.__file__).resolve().parent / "_schemas"
                or not a.SCHEMA_ROOT.is_dir()):
            parser.error("installed mode requires the wheel's CLI, module, and schemas in this venv")
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env["PYTHONNOUSERSITE"] = "1"
        installer = [str(installed_cli)]
    else:
        env["PYTHONPATH"] = str(ROOT / "src")
        installer = [sys.executable, "-m", "spine_packs"]
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    LocalSpineTests.config = {"root": run, "command": command, "migrate": migrate,
                             "env": env, "installer": installer}
    save(run / "run.json", {"spine_command": str(command), "spine_ledger_migrate": str(migrate),
                           "python": sys.version, "qualification": "synthetic-disposable-ledgers-only",
                           "installed": args.installed, "installer": installer,
                           "module": a.__file__, "schemas": str(a.SCHEMA_ROOT)})
    print(f"Private disposable test evidence: {run}", file=sys.stderr)
    suite = (unittest.TestSuite(LocalSpineTests(name) for name in args.test) if args.test else
             unittest.defaultTestLoader.loadTestsFromTestCase(LocalSpineTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    save(run / "result.json", {"passed": result.wasSuccessful(), "tests": result.testsRun,
                               "failures": len(result.failures), "errors": len(result.errors)})
    print(f"Evidence retained: {run}", file=sys.stderr)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
