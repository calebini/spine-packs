"""Independent checks of the additive runtime/environment contract variant."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import test_installer_artifact_contract as c
import test_pack_manifest_contract as pack

ROOT = Path(__file__).resolve().parents[2]


class Schema15ContractTests(unittest.TestCase):
    def test_checked_in_schema15_plan_and_closed_environment(self):
        plan = c.load_json(ROOT / "tests/fixtures/installer/positive/schema15_plan.json")
        self.assertEqual(c.plan_errors(plan), [])
        self.assertEqual(len(plan["required_execution_contracts"]), 10)
        mutations = [
            lambda p: p["environment"].pop("ledger_instance_id"),
            lambda p: p["environment"].update(ledger_instance_id="ledger_instance_bad"),
            lambda p: p["environment"].update(runtime_version="0.4.0"),
            lambda p: p["environment"].update(ledger_schema_current="14"),
            lambda p: p["environment"].update(ledger_schema_implemented="16"),
            lambda p: p["environment"].update(unknown=True),
            lambda p: p.update(required_execution_contracts=c.REQUIRED_EXECUTION_CONTRACTS),
        ]
        for mutate in mutations:
            value = deepcopy(plan)
            mutate(value)
            self.assertTrue(c.plan_errors(c.seal(value)))

    def test_draft10_is_only_a_compatibility_successor(self):
        previous = pack.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.9.json")
        current = pack.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.10.json")
        self.assertEqual(current["pack"], {**previous["pack"], "version": "1.0.0-draft.10"})
        self.assertEqual(current["compatibility"]["spine_runtime_versions"], ["0.3.0", "0.5.0"])
        for field in ("archetypes", "notification_profiles", "binding_intents", "dependencies", "manifest_schema"):
            self.assertEqual(current[field], previous[field])
        self.assertEqual(current["compatibility"]["spine_content_contracts"],
                         previous["compatibility"]["spine_content_contracts"])
        self.assertEqual(current["content_identity"]["digest"], pack.content_digest(current))

    def test_readback_pin_requires_public_identity_and_new_contract(self):
        schema = json.loads((ROOT / "contracts/schemas/spine-readback-0.5.0.schema.json").read_text())
        self.assertIn("ab18a8a51c9bf548220f67e2db0220bfe9783888", schema["$comment"])
        info = schema["$defs"]["systemInfo"]
        self.assertIn("ledger_instance_id", info["required"])
        self.assertFalse(info["additionalProperties"])
        self.assertEqual(info["properties"]["response_contract"], {"const": "spine.system-info.v3"})


if __name__ == "__main__":
    unittest.main()
