"""Explicit schema-15 admission and identity binding; synthetic public transport."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))
sys.path.insert(0, str(ROOT / "tests/contract"))

from spine_packs import artifacts as a, manifest as m, planning as p
from spine_packs.apply import apply_initial, apply_continuation
from spine_packs.preflight import preflight_apply
from spine_packs.verification import verify_installation
from test_apply_preflight import approval
from test_continuation import RecoverySpine
from test_planning import manifest, request, info
import test_installer_artifact_contract as independent


def info15(runtime="0.5.0"):
    value = info()
    value.update(runtime_version=runtime, response_contract="spine.system-info.v3",
                 implemented_ledger_schema_version="15", ledger_schema_version="15",
                 ledger_instance_id="ledger_instance_" + "a" * 64,
                 implemented_contract_versions=a.execution_contracts(runtime))
    return value


class Schema15Tests(unittest.TestCase):
    runtime = "0.5.0"

    def setup(self):
        pack = manifest(released=True)
        pack["compatibility"]["spine_runtime_versions"] = sorted({"0.3.0", "0.5.0", self.runtime})
        pack["content_identity"]["digest"] = m.content_digest(pack)
        transport = RecoverySpine(pack, {k: [] for k in p.CATALOGS})
        transport.info = info15(self.runtime)
        return pack, transport

    def test_plan_binds_identity_and_correct_contract_union(self):
        pack, transport = self.setup()
        plan = p.plan_installation(pack, request(), transport)
        self.assertEqual(independent.plan_errors(plan), [])
        self.assertEqual(plan["environment"]["ledger_instance_id"], transport.info["ledger_instance_id"])
        self.assertEqual(plan["required_execution_contracts"], a.execution_contracts(self.runtime))
        transport.info["ledger_instance_id"] = "ledger_instance_" + "b" * 64
        changed = p.plan_installation(pack, request(), transport)
        self.assertNotEqual(plan["content_identity"]["digest"], changed["content_identity"]["digest"])
        self.assertTrue(a.approval_errors(approval(plan), changed))

    def test_public_compatibility_failures_precede_catalog_reads(self):
        mutations = [
            lambda v: v.update(runtime_version="0.4.0"),
            lambda v: v.update(runtime_version="0.7.0"),
            lambda v: v.update(ledger_schema_version="14"),
            lambda v: v.update(implemented_ledger_schema_version="16"),
            lambda v: v.update(response_contract="spine.system-info.v2"),
            lambda v: v.pop("ledger_instance_id"),
            lambda v: v.update(ledger_instance_id="invalid"),
            lambda v: v.update(ledger_instance_id=None),
            lambda v: v["implemented_contract_versions"].remove("spine.ledger-instance.v1"),
            lambda v: v["implemented_contract_versions"].remove("spine.notification-profile-readback.v1"),
            lambda v: v.update(unrecognized=True),
        ]
        for change in mutations:
            with self.subTest(change=change):
                pack, transport = self.setup()
                change(transport.info)
                with self.assertRaises(p.PlanError):
                    p.plan_installation(pack, request(), transport)
                self.assertEqual([c[0] for c in transport.calls], ["system.info"])
                self.assertEqual(transport.writes, [])
        pack, transport = self.setup()
        with self.assertRaises(p.PlanError):
            p.plan_installation(manifest(released=True), request(), transport)
        self.assertEqual([c[0] for c in transport.calls], ["system.info"])

    def test_old_artifact_shape_stays_closed(self):
        pack, transport = self.setup()
        transport.info = info()
        plan = p.plan_installation(pack, request(), transport)
        self.assertNotIn("ledger_instance_id", plan["environment"])
        plan["environment"]["ledger_instance_id"] = info15()["ledger_instance_id"]
        self.assertTrue(a.plan_errors(a.seal(plan)))

    def test_artifact_identity_and_union_cannot_be_omitted_or_downgraded(self):
        pack, transport = self.setup()
        plan = p.plan_installation(pack, request(), transport)
        mutations = [
            lambda v: v["environment"].pop("ledger_instance_id"),
            lambda v: v["environment"].update(ledger_schema_current="12"),
            lambda v: v["environment"].update(ledger_instance_id="bad"),
            lambda v: v.update(required_execution_contracts=a.REQUIRED_EXECUTION_CONTRACTS),
            lambda v: v["environment"]["advertised_contracts"].remove("spine.ledger-instance.v1"),
        ]
        for change in mutations:
            bad = deepcopy(plan)
            change(bad)
            bad = a.seal(bad)
            self.assertTrue(a.plan_errors(bad))
            self.assertTrue(independent.plan_errors(bad))

    def test_changed_identity_blocks_initial_apply_without_writes(self):
        pack, transport = self.setup()
        plan = p.plan_installation(pack, request(), transport)
        transport.info["ledger_instance_id"] = "ledger_instance_" + "b" * 64
        with self.assertRaises(p.PlanError) as caught:
            preflight_apply(pack, plan, approval(plan), transport)
        self.assertEqual(caught.exception.category, "stale_plan_or_target_mismatch")
        self.assertEqual(transport.writes, [])

    def test_recovery_and_verify_keep_identity_and_receipt_boundary(self):
        pack, transport = self.setup()
        plan = p.plan_installation(pack, request(), transport)
        approved = approval(plan)
        transport.lose_after = 0
        checkpoints = []
        partial = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(partial["state"], "partial")
        transport.lose_after = None
        original = transport.info["ledger_instance_id"]
        transport.info["ledger_instance_id"] = "ledger_instance_" + "b" * 64
        writes = len(transport.writes)
        with self.assertRaises(p.PlanError):
            apply_continuation(pack, plan, approved, checkpoints[-1], transport, lambda _: None)
        self.assertEqual(len(transport.writes), writes)
        transport.info["ledger_instance_id"] = original
        result = apply_continuation(pack, plan, approved, checkpoints[-1], transport, lambda _: None)
        self.assertEqual(result["state"], "applied")
        verified = verify_installation(pack, plan, transport, result)
        self.assertEqual(verified["state"], "verified")
        self.assertEqual(verified["receipt_readback"], "captured_responses_only_spine_" + self.runtime)
        self.assertEqual(independent.verification_errors(verified, plan, result), [])
        bad = deepcopy(verified)
        bad["receipt_readback"] = "captured_responses_only_spine_0.3.0"
        self.assertTrue(a.validate_schema(a.seal(bad)))
        for edit in (lambda v: v.update(unrecognized=True), lambda v: v.pop("object_results"),
                     lambda v: v.update(state="invalid")):
            bad = deepcopy(verified)
            edit(bad)
            self.assertTrue(a.validate_schema(a.seal(bad)))
            self.assertTrue(independent.validate_schema(a.seal(bad)))
        transport.info["ledger_instance_id"] = "ledger_instance_" + "b" * 64
        writes = len(transport.writes)
        with self.assertRaises(p.PlanError):
            verify_installation(pack, plan, transport, result)
        self.assertEqual(len(transport.writes), writes)


if __name__ == "__main__":
    unittest.main()
