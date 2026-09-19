"""Pin the approved immutable pack bytes and draft-to-release promotion."""
from copy import deepcopy
import hashlib
from pathlib import Path
import unittest

import test_pack_manifest_contract as contract

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0.json"
DRAFT = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.10.json"
FILE_SHA256 = "a0d73767e5fdfe91080328bf7486734d283c134bb57db76c0af95d9644917d9f"
DIGEST = "65d489a84b75ff0051f9df4a507f7104288c58bdda51d0096b030b5a104b5dfb"


class KinflowReleaseContractTests(unittest.TestCase):
    def test_approved_immutable_bytes_and_content_identity(self):
        raw = RELEASE.read_bytes()
        self.assertEqual(len(raw), 117621)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), FILE_SHA256)
        value = contract.load_json(RELEASE)
        self.assertEqual(value["pack"], {
            "pack_id": "kinflow-starter", "version": "1.0.0", "status": "released"})
        self.assertEqual(value["content_identity"]["digest"], DIGEST)
        self.assertEqual(contract.content_digest(value), DIGEST)
        self.assertEqual(contract.validate_pack(value, contract.load_json(contract.SCHEMA_PATH)), [])

    def test_promotion_changes_no_content_or_compatibility(self):
        self.assertEqual(hashlib.sha256(DRAFT.read_bytes()).hexdigest(),
                         "5fc5b139e54c49f565219c5fe65cc3e4b29f4419a53e646c83fe1dbad825569b")
        draft = contract.load_json(DRAFT)
        expected = deepcopy(draft)
        expected["pack"].update(version="1.0.0", status="released")
        expected["content_identity"]["digest"] = contract.content_digest(expected)
        value = contract.load_json(RELEASE)
        self.assertEqual(value, expected)
        for field in ("archetypes", "notification_profiles", "binding_intents"):
            self.assertEqual(len(value[field]), 52)
        self.assertEqual(value["compatibility"]["spine_runtime_versions"], ["0.3.0", "0.5.0"])

    def test_stable_manifest_registered_in_fixture_matrix(self):
        cases = contract.load_json(contract.FIXTURE_MANIFEST_PATH)["cases"]
        entries = [case for case in cases if case["fixture"] == RELEASE.relative_to(ROOT).as_posix()]
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0]["valid"])


if __name__ == "__main__":
    unittest.main()
