"""Repeat schema-15 security boundaries for the separately pinned 0.6.0 baseline."""
from copy import deepcopy
from pathlib import Path
import test_schema15_compatibility as baseline
from spine_packs import artifacts as a, planning as p
from spine_packs.apply import apply_initial
from spine_packs.preflight import preflight_apply
from spine_packs.verification import verify_installation
from test_apply_preflight import approval
from test_planning import FakeSpine, catalog, info, request

ROOT = Path(__file__).resolve().parents[2]


class Spine060Tests(baseline.Schema15Tests):
    runtime = "0.6.0"

    def test_stable_successor_full_and_granular_plans_on_all_pinned_baselines(self):
        pack = a.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json")
        for runtime in ("0.3.0", "0.5.0", "0.6.0"):
            for selection, count in (({"mode": "all"}, 52),
                    ({"mode": "archetypes", "archetype_keys":
                      ["birthday", "flight", "medical_appointment"]}, 3)):
                for equivalent in (False, True):
                    with self.subTest(runtime=runtime, selection=selection, equivalent=equivalent):
                        transport = FakeSpine(catalog(pack) if equivalent else None)
                        transport.info = info() if runtime == "0.3.0" else baseline.info15(runtime)
                        req = request(selection)
                        req["request"]["draft_posture"] = "reject"
                        plan = p.plan_installation(pack, a.seal(req), transport, page_size=7)
                        self.assertTrue(plan["apply_eligible"])
                        self.assertEqual(plan["environment"]["runtime_version"], runtime)
                        self.assertEqual(len(plan["actions"]), 0 if equivalent else count * 3)
                        self.assertEqual(baseline.independent.plan_errors(plan), [])

    def test_released_pack_still_refuses_undeclared_runtime(self):
        _, transport = self.setup()
        pack = a.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0.json")
        with self.assertRaises(p.PlanError) as caught:
            p.plan_installation(pack, request(), transport)
        self.assertEqual(caught.exception.category, "incompatible_spine_runtime_or_contracts")
        self.assertEqual([c[0] for c in transport.calls], ["system.info"])
        self.assertEqual(transport.writes, [])

    def test_runtime_upgrade_stales_old_plan_even_with_same_ledger_identity(self):
        pack, transport = self.setup()
        transport.info = baseline.info15("0.5.0")
        old_plan = p.plan_installation(pack, request(), transport)
        approved = approval(old_plan)
        transport.info = baseline.info15("0.6.0")
        with self.assertRaises(p.PlanError):
            preflight_apply(pack, old_plan, approved, transport)
        self.assertEqual(transport.writes, [])
        fresh = p.plan_installation(pack, request(), transport)
        self.assertNotEqual(fresh["content_identity"], old_plan["content_identity"])
        self.assertTrue(a.approval_errors(approved, fresh))

    def test_extra_web_contracts_do_not_widen_command_or_receipt_surface(self):
        pack, transport = self.setup()
        transport.info["implemented_contract_versions"] = sorted(
            transport.info["implemented_contract_versions"] + ["spine.trusted-web-api.v2"])
        plan = p.plan_installation(pack, request(), transport)
        self.assertEqual(plan["required_execution_contracts"], a.execution_contracts("0.5.0"))
        result = apply_initial(pack, plan, approval(plan), transport, lambda _: None)
        verified = verify_installation(pack, plan, transport, result)
        self.assertEqual(verified["state"], "verified")
        for wrong in ("0.3.0", "0.5.0"):
            bad = deepcopy(verified)
            bad["receipt_readback"] = "captured_responses_only_spine_" + wrong
            self.assertTrue(a.validate_schema(a.seal(bad)))
            self.assertTrue(baseline.independent.validate_schema(a.seal(bad)))

    def test_compatibility_draft_plans_full_and_granular_without_apply_eligibility(self):
        pack = a.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1-draft.1.json")
        for selection, count in (({"mode": "all"}, 52),
                ({"mode": "archetypes", "archetype_keys": ["birthday", "flight"]}, 2)):
            _, transport = self.setup()
            plan = p.plan_installation(pack, request(selection), transport, page_size=7)
            self.assertFalse(plan["apply_eligible"])
            self.assertEqual(len(plan["actions"]), count * 3)
            self.assertEqual(baseline.independent.plan_errors(plan), [])
