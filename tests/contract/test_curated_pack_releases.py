"""Check v2 curated pack coverage and immutable release lineage."""
import hashlib
import sys
import unittest

import test_facet_manifest_contract as contract

ROOT = contract.ROOT
sys.path.insert(0, str(ROOT / "src"))
from spine_packs.facet_manifest import validate

PACKS = ROOT / "packs"
PROMOTIONS = (
    (
        "kinflow-flight", "1.0.0-draft.2",
        "35b69a9fa4db9ec7c1b14d5c3b91e5df9f3c19c9efa47785a83a9e4964190624",
        "55b5e3e6da8d5f814c733aae1b71012669c0f32e794c26c16ed3df2f6d6063ae",
    ),
    (
        "kinflow-appointments", "1.0.0-draft.1",
        "840bf42c8a291f25b230a2985a7bf91fd92a79109c72a3f5ac51965256f3ee4d",
        "844c1734fbb2ee496deac87532101ca90946179edcb2ece22f6758c3a36dd23c",
    ),
)


def pack_path(pack_id, version):
    return PACKS / pack_id / f"{pack_id}.{version}.json"


class CuratedPackReleaseTests(unittest.TestCase):
    def test_every_curated_pack_outside_the_v1_index_has_content_coverage(self):
        manifests = {path: contract.load(path)["manifest_schema"] for path in PACKS.rglob("*.json")}
        covered = {pack_path("kinflow-flight", "1.0.0-draft.1")}
        for pack_id, draft, _, _ in PROMOTIONS:
            covered.update((pack_path(pack_id, draft), pack_path(pack_id, "1.0.0")))
        self.assertEqual(
            {path: schema for path, schema in manifests.items() if schema != "spine.pack-manifest.v1"},
            dict.fromkeys(covered, "spine.pack-manifest.v2"),
        )

    def test_stable_manifests_preserve_signed_off_definitions_and_compatibility(self):
        for pack_id, draft_version, draft_hash, release_hash in PROMOTIONS:
            with self.subTest(pack_id=pack_id):
                source = pack_path(pack_id, draft_version)
                release = pack_path(pack_id, "1.0.0")
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), draft_hash)
                self.assertEqual(hashlib.sha256(release.read_bytes()).hexdigest(), release_hash)
                draft = contract.load(source)
                stable = contract.load(release)
                validate(stable)
                self.assertEqual(stable["pack"], {
                    "pack_id": pack_id, "version": "1.0.0", "status": "released",
                })
                self.assertEqual(stable["content_identity"]["digest"], contract.digest(stable))
                self.assertNotEqual(stable["content_identity"]["digest"],
                                    draft["content_identity"]["digest"])
                self.assertEqual({key for key in stable if draft.get(key) != stable[key]},
                                 {"pack", "content_identity"})

    @unittest.skipIf(contract.Draft202012Validator is None,
                     "requires official development jsonschema")
    def test_approved_release_shape_passes_official_schema(self):
        for pack_id, _, _, _ in PROMOTIONS:
            with self.subTest(pack_id=pack_id):
                contract.validate(contract.load(pack_path(pack_id, "1.0.0")))
