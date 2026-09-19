"""Additive 0.6.0 environment and compatibility-only successor contract."""
from copy import deepcopy
import hashlib
from pathlib import Path
import unittest
import test_pack_manifest_contract as pack
import test_installer_artifact_contract as artifacts

ROOT = Path(__file__).resolve().parents[2]


class Spine060ContractTests(unittest.TestCase):
    def test_stable_successor_pins_bytes_and_unchanged_promotion(self):
        path = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         "4ad2c351af5fb575827590efa45dabceebff8dfbf6aa3acea5a0ee143c45b491")
        draft_path = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1-draft.1.json"
        self.assertEqual(hashlib.sha256(draft_path.read_bytes()).hexdigest(),
                         "fd915e5cb362c35917588f52a284abfee8b15cf01ae9f39d9ad9b553ecd8e057")
        expected = pack.load_json(draft_path)
        expected["pack"].update(version="1.0.1", status="released")
        expected["content_identity"]["digest"] = pack.content_digest(expected)
        value = pack.load_json(path)
        self.assertEqual(value, expected)
        self.assertEqual(value["content_identity"]["digest"],
                         "5d9986c549ea0fe48157e977dbb41d9f45820b3de1f0611816b325e2f1d862af")
        self.assertEqual(pack.validate_pack(value, pack.load_json(pack.SCHEMA_PATH)), [])
        for field in ("archetypes", "notification_profiles", "binding_intents"):
            self.assertEqual(len(value[field]), 52)

    def test_stable_successor_registered_once_in_fixture_matrix(self):
        entries = [case for case in pack.load_json(pack.FIXTURE_MANIFEST_PATH)["cases"]
                   if case["fixture"] == "packs/kinflow-starter/kinflow-starter.1.0.1.json"]
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0]["valid"])

    def test_successor_changes_only_draft_identity_compatibility_and_digest(self):
        stable = pack.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0.json")
        draft = pack.load_json(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1-draft.1.json")
        expected = deepcopy(stable)
        expected["pack"].update(version="1.0.1-draft.1", status="draft")
        expected["compatibility"]["spine_runtime_versions"] = ["0.3.0", "0.5.0", "0.6.0"]
        expected["content_identity"]["digest"] = pack.content_digest(expected)
        self.assertEqual(draft, expected)
        self.assertEqual(pack.validate_pack(draft, pack.load_json(pack.SCHEMA_PATH)), [])

    def test_closed_environment_and_exact_contract_union(self):
        plan = artifacts.load_json(ROOT / "tests/fixtures/installer/positive/spine060_plan.json")
        self.assertEqual(artifacts.plan_errors(plan), [])
        self.assertEqual(plan["environment"]["runtime_version"], "0.6.0")
        self.assertEqual(len(plan["required_execution_contracts"]), 10)
        for edit in (lambda p: p["environment"].pop("ledger_instance_id"),
                     lambda p: p["environment"].update(ledger_schema_current="16"),
                     lambda p: p["environment"].update(runtime_version="0.7.0"),
                     lambda p: p["environment"].update(unknown=True),
                     lambda p: p.update(required_execution_contracts=artifacts.REQUIRED_EXECUTION_CONTRACTS)):
            bad = deepcopy(plan)
            edit(bad)
            self.assertTrue(artifacts.plan_errors(artifacts.seal(bad)))
