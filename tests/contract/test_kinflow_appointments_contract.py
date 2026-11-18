"""Content and planning checks for the generic appointment draft."""
import sys
import unittest
from unittest.mock import patch

import alignment_fixture_support as alignment
import facet_artifact_oracle as installer_contract
import test_facet_manifest_contract as manifest_contract

ROOT = manifest_contract.ROOT
sys.path.insert(0, str(ROOT / "src"))
from spine_packs.facet_manifest import validate as validate_manifest
from spine_packs.facet_planning import plan_installation

DRAFT = ROOT / "packs/kinflow-appointments/kinflow-appointments.1.0.0-draft.1.json"
STARTER = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json"
EMPTY_CATALOG = ROOT / "tests/fixtures/installer-v2/flight-create-0.10.0.json"


class KinflowAppointmentsContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = manifest_contract.load(DRAFT)

    @unittest.skipIf(manifest_contract.Draft202012Validator is None,
                     "requires official development jsonschema")
    def test_official_manifest_validation(self):
        manifest_contract.validate(self.manifest)

    def test_draft_defines_only_the_ordinary_appointment_bundle(self):
        validate_manifest(self.manifest)
        self.assertEqual(self.manifest["content_identity"]["digest"],
                         manifest_contract.digest(self.manifest))
        self.assertEqual(self.manifest["pack"], {
            "pack_id": "kinflow-appointments", "version": "1.0.0-draft.1", "status": "draft",
        })
        self.assertEqual(self.manifest["compatibility"]["spine_runtime_versions"], ["0.12.0"])
        for collection in (
            "dependencies", "facet_schemas", "archetype_facet_bindings", "rendering_definitions",
        ):
            with self.subTest(collection=collection):
                self.assertEqual(self.manifest[collection], [])
        archetype, = self.manifest["archetypes"]
        self.assertEqual(archetype["archetype_key"], "appointment")
        self.assertEqual(archetype["revision"]["compatible_item_types"], ["event"])
        self.assertEqual(self.manifest["binding_intents"], [{
            "binding_kind": "archetype_default",
            "archetype_key": "appointment",
            "notification_profile_key": "appointment_standard",
        }])

    def test_own_profile_preserves_medical_appointment_templates(self):
        profile, = self.manifest["notification_profiles"]
        self.assertEqual(profile["profile_key"], "appointment_standard")
        self.assertEqual(profile["display_name"], "Appointment standard")
        legacy = next(
            row for row in manifest_contract.load(STARTER)["notification_profiles"]
            if row["profile_key"] == "medical_appointment_standard"
        )
        for template in profile["revision"]["templates"]:
            self.assertEqual(template.pop("rendering"), {"kind": "ordinary"})
        self.assertEqual(profile["revision"], legacy["revision"])

    def test_both_selection_modes_plan_the_same_default_and_cannot_apply(self):
        fixture = installer_contract.load(EMPTY_CATALOG)
        environment = dict(fixture["plan"]["environment"], runtime_version="0.12.0",
                           ledger_schema_current="20", ledger_schema_implemented="20")
        observation = fixture["plan"]["observation"]
        expected = ["archetype:appointment", "binding:appointment", "profile:appointment_standard"]
        for selection in ({"mode": "all"}, {"mode": "archetypes", "archetype_keys": ["appointment"]}):
            with self.subTest(selection=selection):
                request = installer_contract.seal({
                    "artifact_schema": fixture["request"]["artifact_schema"],
                    "request": dict(fixture["request"]["request"], selection=selection,
                                    draft_posture="inspect_only"),
                })
                with patch("spine_packs.facet_planning.observe", return_value=(environment, observation)):
                    plan = plan_installation(self.manifest, request, None)
                self.assertEqual(plan["closure"], expected)
                self.assertFalse(plan["apply_eligible"])
                actions = {action["object_key"]: action for action in plan["actions"]}
                self.assertCountEqual(actions, expected)
                self.assertIn({
                    "request_pointer": "/notification_profile_id",
                    "object_key": "profile:appointment_standard",
                    "field": "root",
                }, actions["binding:appointment"]["slots"])
                if installer_contract.Draft202012Validator is not None:
                    with alignment.aligned_contracts():
                        alignment.plan_check({"manifest": self.manifest, "request": request, "plan": plan})
