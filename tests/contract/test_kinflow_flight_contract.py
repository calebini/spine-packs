"""Content and read-only planning checks for the curated flight drafts."""
from copy import deepcopy
import hashlib
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
from spine_packs.planning import PlanError

DRAFT = ROOT / "packs/kinflow-flight/kinflow-flight.1.0.0-draft.1.json"
ARRIVAL_DRAFT = ROOT / "packs/kinflow-flight/kinflow-flight.1.0.0-draft.2.json"
STARTER = ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json"
EMPTY_CATALOG = ROOT / "tests/fixtures/installer-v2/flight-create-0.10.0.json"

DEFAULT_CLOSURE = [
    "archetype:flight",
    "binding:flight",
    "facet_binding:flight:flight",
    "profile:flight_details_standard",
    "rendering:flight_departure_gate",
    "rendering:flight_details",
    "schema:flight_details",
]
WHOLE_CLOSURE = sorted(DEFAULT_CLOSURE + ["profile:flight_standard"])
ARRIVAL_CLOSURE = [
    "archetype:flight_arrival",
    "binding:flight_arrival",
    "facet_binding:flight_arrival:flight_arrival",
    "profile:flight_arrival_standard",
    "rendering:flight_arrival_details",
    "schema:flight_arrival_details",
]


class KinflowFlightContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = manifest_contract.load(DRAFT)

    @unittest.skipIf(manifest_contract.Draft202012Validator is None,
                     "requires official development jsonschema")
    def test_official_manifest_validation(self):
        manifest_contract.validate(self.manifest)

    def test_manifest_has_exact_draft_identity_and_content_contracts(self):
        validate_manifest(self.manifest)
        self.assertEqual(self.manifest["manifest_schema"], "spine.pack-manifest.v2")
        self.assertEqual(self.manifest["pack"], {
            "pack_id": "kinflow-flight", "version": "1.0.0-draft.1", "status": "draft",
        })
        self.assertEqual(self.manifest["compatibility"], {
            "spine_runtime_versions": ["0.12.0"],
            "spine_content_contracts": [
                "spine.archetype-facet-bindings.v1",
                "spine.facet-schemas.v1",
                "spine.item-archetypes.v1",
                "spine.notification-profile-bindings.v1",
                "spine.notification-profiles.v2",
                "spine.notification-rendering-definitions.v1",
                "spine.notification-rendering.v1",
            ],
        })
        self.assertEqual(self.manifest["dependencies"], [])
        self.assertEqual(self.manifest["content_identity"]["digest"],
                         manifest_contract.digest(self.manifest))

    def test_optional_fields_and_rendering_selections(self):
        schema, = self.manifest["facet_schemas"]
        self.assertEqual(schema["schema_key"], "flight_details")
        definition = schema["definition"]
        self.assertEqual(definition["compatible_item_types"], ["event"])
        self.assertEqual(definition["fields"], [
            {"key": "arrival_at", "type": "text", "max_length": "64",
             "required": False, "queryable": False},
            {"key": "arrival_timezone", "type": "text", "max_length": "128",
             "required": False, "queryable": False},
            {"key": "departure_gate", "type": "text", "max_length": "32",
             "required": False, "queryable": False},
            {"key": "destination", "type": "reference", "target_kind": "location",
             "required": False, "queryable": True},
            {"key": "flight_number", "type": "text", "max_length": "32",
             "required": False, "queryable": True},
            {"key": "origin", "type": "reference", "target_kind": "location",
             "required": False, "queryable": False},
        ])
        self.assertEqual(self.manifest["archetype_facet_bindings"], [{
            "archetype_key": "flight", "facet_key": "flight",
            "schema_ref": {"schema_key": "flight_details"},
        }])

        selections = {}
        for row in self.manifest["rendering_definitions"]:
            self.assertEqual(row["revision"]["compatible_item_types"], ["event"])
            selected = row["revision"]["selections"]
            for entry in selected:
                self.assertEqual(entry["selection_key"], entry["field_key"])
                self.assertEqual(entry["facet_key"], "flight")
                self.assertEqual(entry["schema_ref"], {"schema_key": "flight_details"})
            selections[row["definition_key"]] = [
                (entry["field_key"], entry["label"], entry["projection"])
                for entry in selected
            ]
        self.assertEqual(selections, {
            "flight_departure_gate": [("departure_gate", "Gate", "value")],
            "flight_details": [
                ("flight_number", "Flight", "value"),
                ("origin", "From", "location_label"),
                ("destination", "To", "location_label"),
            ],
        })

    def test_details_default_and_explicit_ordinary_preserve_starter_timing(self):
        starter = manifest_contract.load(STARTER)
        self.assertEqual(self.manifest["archetypes"],
                         [row for row in starter["archetypes"] if row["archetype_key"] == "flight"])
        self.assertEqual(self.manifest["binding_intents"], [{
            "binding_kind": "archetype_default", "archetype_key": "flight",
            "notification_profile_key": "flight_details_standard",
        }])
        details, standard = deepcopy(self.manifest["notification_profiles"])
        self.assertEqual(details["profile_key"], "flight_details_standard")
        self.assertEqual(details["intended_status"], "active")
        self.assertEqual(details["revision"]["compatible_item_types"], ["event"])
        legacy = next(row for row in starter["notification_profiles"]
                      if row["profile_key"] == "flight_standard")
        expected_pins = {
            "four_hours_before": {"kind": "definition", "definition_ref": {"definition_key": "flight_details"}},
            "one_hour_before": {"kind": "definition", "definition_ref": {"definition_key": "flight_departure_gate"}},
            "seven_days_before": {"kind": "definition", "definition_ref": {"definition_key": "flight_details"}},
            "twenty_four_hours_before": {"kind": "ordinary"},
        }
        for template in standard["revision"]["templates"]:
            self.assertEqual(template.pop("rendering"), {"kind": "ordinary"})
        actual_pins = {template["template_key"]: template.pop("rendering")
                       for template in details["revision"]["templates"]}
        self.assertEqual(actual_pins, expected_pins)
        self.assertEqual(standard, legacy)
        self.assertEqual(details["revision"], legacy["revision"])

    def test_draft_planner_resolves_details_default_in_both_selection_modes(self):
        fixture = installer_contract.load(EMPTY_CATALOG)
        environment = dict(fixture["plan"]["environment"], runtime_version="0.12.0",
                           ledger_schema_current="20", ledger_schema_implemented="20")
        observation = fixture["plan"]["observation"]
        request = fixture["request"]
        request["request"]["draft_posture"] = "inspect_only"
        for selection, expected in (
            ({"mode": "all"}, WHOLE_CLOSURE),
            ({"mode": "archetypes", "archetype_keys": ["flight"]}, DEFAULT_CLOSURE),
        ):
            with self.subTest(selection=selection):
                request["request"]["selection"] = selection
                request = installer_contract.seal(request)
                # Only the public observation is supplied by the fixture.
                with patch("spine_packs.facet_planning.observe", return_value=(environment, observation)) as observe:
                    plan = plan_installation(self.manifest, request, None)
                self.assertEqual(observe.call_args.args[2], expected)
                self.assertEqual(observe.call_args.kwargs["runtime_version"], "0.12.0")
                self.assertEqual(plan["closure"], expected)
                self.assertCountEqual([action["object_key"] for action in plan["actions"]], expected)
                self.assertFalse(plan["apply_eligible"])
                if installer_contract.Draft202012Validator is not None:
                    with alignment.aligned_contracts():
                        alignment.plan_check({"manifest": self.manifest, "request": request, "plan": plan})

                actions = {action["object_key"]: action for action in plan["actions"]}
                self.assertIn({
                    "request_pointer": "/notification_profile_id",
                    "object_key": "profile:flight_details_standard",
                    "field": "root",
                }, actions["binding:flight"]["slots"])
                profile = actions["profile:flight_details_standard"]
                pins = [(slot["request_pointer"].split("/")[3], slot["object_key"], slot["field"])
                        for slot in profile["slots"]]
                self.assertCountEqual(pins, [
                    ("0", "rendering:flight_details", "root"),
                    ("0", "rendering:flight_details", "revision"),
                    ("1", "rendering:flight_departure_gate", "root"),
                    ("1", "rendering:flight_departure_gate", "revision"),
                    ("2", "rendering:flight_details", "root"),
                    ("2", "rendering:flight_details", "revision"),
                ])

        request["request"]["draft_posture"] = "reject"
        with patch("spine_packs.facet_planning.observe") as observe:
            with self.assertRaises(PlanError) as error:
                plan_installation(self.manifest, installer_contract.seal(request), None)
        self.assertEqual(error.exception.code, "draft_inspection_not_allowed")
        observe.assert_not_called()


class FlightArrivalDraftTests(unittest.TestCase):
    def setUp(self):
        self.manifest = manifest_contract.load(ARRIVAL_DRAFT)

    @unittest.skipIf(manifest_contract.Draft202012Validator is None,
                     "requires official development jsonschema")
    def test_official_manifest_validation(self):
        manifest_contract.validate(self.manifest)

    def test_arrival_is_additive_and_draft_one_bytes_are_preserved(self):
        self.assertEqual(
            hashlib.sha256(DRAFT.read_bytes()).hexdigest(),
            "b273bc36bdbb4d0e9436221698020e9ebf309bd4bed41bafe00d031c4d6f9acd",
        )
        first = manifest_contract.load(DRAFT)
        self.assertEqual(self.manifest["pack"], dict(first["pack"], version="1.0.0-draft.2"))
        for name in ("manifest_schema", "compatibility", "dependencies"):
            self.assertEqual(self.manifest[name], first[name])
        for name in (
            "archetypes", "binding_intents", "archetype_facet_bindings",
            "notification_profiles", "facet_schemas", "rendering_definitions",
        ):
            with self.subTest(collection=name):
                self.assertEqual(len(self.manifest[name]), len(first[name]) + 1)
                self.assertEqual([row for row in self.manifest[name] if row in first[name]], first[name])
        self.assertEqual(self.manifest["content_identity"]["digest"],
                         manifest_contract.digest(self.manifest))

    def test_arrival_field_types_and_reminder_projection(self):
        validate_manifest(self.manifest)
        archetype = next(row for row in self.manifest["archetypes"]
                         if row["archetype_key"] == "flight_arrival")
        self.assertEqual(archetype["revision"]["compatible_item_types"], ["event"])
        schema = next(row for row in self.manifest["facet_schemas"]
                      if row["schema_key"] == "flight_arrival_details")
        self.assertEqual(schema["definition"]["compatible_item_types"], ["event"])
        self.assertEqual(schema["definition"]["fields"], [
            {"key": "arrival_terminal", "type": "text", "max_length": "32",
             "required": False, "queryable": False},
            {"key": "flight_number", "type": "text", "max_length": "32",
             "required": False, "queryable": True},
            {"key": "origin", "type": "reference", "target_kind": "location",
             "required": False, "queryable": False},
        ])
        self.assertIn({
            "archetype_key": "flight_arrival", "facet_key": "flight_arrival",
            "schema_ref": {"schema_key": "flight_arrival_details"},
        }, self.manifest["archetype_facet_bindings"])
        rendering = next(row for row in self.manifest["rendering_definitions"]
                         if row["definition_key"] == "flight_arrival_details")
        self.assertEqual(rendering["revision"]["compatible_item_types"], ["event"])
        self.assertEqual(rendering["revision"]["selections"], [
            {"selection_key": field, "facet_key": "flight_arrival",
             "schema_ref": {"schema_key": "flight_arrival_details"}, "field_key": field,
             "label": label, "projection": projection}
            for field, label, projection in (
                ("flight_number", "Flight", "value"),
                ("origin", "From", "location_label"),
                ("arrival_terminal", "Terminal", "value"),
            )
        ])

    def test_landing_default_and_exact_offsets(self):
        self.assertIn({
            "binding_kind": "archetype_default", "archetype_key": "flight_arrival",
            "notification_profile_key": "flight_arrival_standard",
        }, self.manifest["binding_intents"])
        profile = next(row for row in self.manifest["notification_profiles"]
                       if row["profile_key"] == "flight_arrival_standard")
        self.assertEqual(profile["revision"]["compatible_item_types"], ["event"])
        details = {"kind": "definition", "definition_ref": {"definition_key": "flight_arrival_details"}}
        templates = profile["revision"]["templates"]
        self.assertEqual(
            [(t["template_key"], t["schedule"]["at"]["offset_seconds"],
              t["late_handling"]["grace_seconds"], t["rendering"]) for t in templates],
            [
                ("at_scheduled_landing", "0", "900", details),
                ("one_hour_before", "-3600", "1800", details),
                ("twenty_four_hours_before", "-86400", "21600", {"kind": "ordinary"}),
            ],
        )
        for template in templates:
            self.assertEqual(template["schedule"]["kind"], "once")
            self.assertEqual(template["schedule"]["at"]["kind"], "target_offset")
            self.assertEqual(template["schedule"]["at"]["offset_basis"], "elapsed")
            self.assertEqual(template["late_handling"]["kind"], "deliver_within")

    def test_planner_selects_arrival_independently_of_departure(self):
        fixture = installer_contract.load(EMPTY_CATALOG)
        environment = dict(fixture["plan"]["environment"], runtime_version="0.12.0",
                           ledger_schema_current="20", ledger_schema_implemented="20")
        observation = fixture["plan"]["observation"]
        for selection, expected in (
            ({"mode": "archetypes", "archetype_keys": ["flight_arrival"]}, ARRIVAL_CLOSURE),
            ({"mode": "archetypes", "archetype_keys": ["flight"]}, DEFAULT_CLOSURE),
            ({"mode": "all"}, sorted(WHOLE_CLOSURE + ARRIVAL_CLOSURE)),
        ):
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
                if installer_contract.Draft202012Validator is not None:
                    with alignment.aligned_contracts():
                        alignment.plan_check({"manifest": self.manifest, "request": request, "plan": plan})
                if "binding:flight_arrival" in expected:
                    actions = {action["object_key"]: action for action in plan["actions"]}
                    self.assertIn({
                        "request_pointer": "/notification_profile_id",
                        "object_key": "profile:flight_arrival_standard",
                        "field": "root",
                    }, actions["binding:flight_arrival"]["slots"])
