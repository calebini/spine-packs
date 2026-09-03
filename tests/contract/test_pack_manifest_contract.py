#!/usr/bin/env python3
"""Dependency-free contract checks for Spine pack manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "contracts/schemas/spine-pack-manifest.v1.schema.json"
FIXTURE_MANIFEST_PATH = ROOT / "contracts/pack-fixture-manifest.v1.json"
DRAFT_MANIFEST_PATH = (
    ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.3.json"
)
POSITIVE_FIXTURE_PATH = (
    ROOT / "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_3.json"
)
EXACT_TARGET_FIXTURE_PATH = (
    ROOT / "tests/fixtures/pack-manifest/positive/exact_target_elapsed_offset.json"
)
PREVIOUS_DRAFT_MANIFEST_PATH = (
    ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.2.json"
)
PREVIOUS_POSITIVE_FIXTURE_PATH = (
    ROOT / "tests/fixtures/pack-manifest/positive/medical_and_lesson.json"
)
FIRST_DRAFT_MANIFEST_PATH = (
    ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json"
)
FIRST_POSITIVE_FIXTURE_PATH = (
    ROOT / "tests/fixtures/pack-manifest/positive/medical_vertical_slice.json"
)
DRAFT_FIXTURE_PAIRS = (
    (FIRST_DRAFT_MANIFEST_PATH, FIRST_POSITIVE_FIXTURE_PATH),
    (PREVIOUS_DRAFT_MANIFEST_PATH, PREVIOUS_POSITIVE_FIXTURE_PATH),
    (DRAFT_MANIFEST_PATH, POSITIVE_FIXTURE_PATH),
)


class DuplicateObjectMember(ValueError):
    """Raised when a JSON object repeats a member name."""


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, member in pairs:
        if key in value:
            raise DuplicateObjectMember(f"duplicate JSON object member: {key}")
        value[key] = member
    return value


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_closed_object)


def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[token]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return current


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate the deliberately small Draft 2020-12 subset used by the schema."""

    if "$ref" in schema:
        return schema_errors(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path)

    if "oneOf" in schema:
        branch_errors = [
            schema_errors(value, branch, root_schema, path)
            for branch in schema["oneOf"]
        ]
        matches = sum(not errors for errors in branch_errors)
        if matches != 1:
            return [f"{path}: must match exactly one allowed shape"]
        return []

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in the allowed set")

    expected_type = schema.get("type")
    if expected_type is not None and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: string is too long")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern mismatch")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}.{required}: required field is missing")
        for key, member in value.items():
            member_path = f"{path}.{key}"
            if key in properties:
                errors.extend(schema_errors(member, properties[key], root_schema, member_path))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{member_path}: unknown field")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array has too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: array has too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, item_schema, root_schema, f"{path}[{index}]"))

    return errors


def _duplicate_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def check(values: list[str], label: str, path: str) -> None:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                errors.append(f"{path}: duplicate {label} {value!r}")
            seen.add(value)

    check(
        [entry["archetype_key"] for entry in manifest["archetypes"]],
        "archetype_key",
        "$.archetypes",
    )
    check(
        [entry["profile_key"] for entry in manifest["notification_profiles"]],
        "profile_key",
        "$.notification_profiles",
    )
    for index, profile in enumerate(manifest["notification_profiles"]):
        check(
            [entry["template_key"] for entry in profile["revision"]["templates"]],
            "template_key",
            f"$.notification_profiles[{index}].revision.templates",
        )
    check(
        [entry["archetype_key"] for entry in manifest["binding_intents"]],
        "archetype_default for archetype_key",
        "$.binding_intents",
    )
    return errors


def _reference_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    archetypes = {entry["archetype_key"]: entry for entry in manifest["archetypes"]}
    profiles = {
        entry["profile_key"]: entry for entry in manifest["notification_profiles"]
    }
    for index, binding in enumerate(manifest["binding_intents"]):
        archetype_key = binding["archetype_key"]
        profile_key = binding["notification_profile_key"]
        archetype = archetypes.get(archetype_key)
        profile = profiles.get(profile_key)
        if archetype is None:
            errors.append(
                f"$.binding_intents[{index}]: unresolved archetype_key {archetype_key!r}"
            )
        if profile is None:
            errors.append(
                "$.binding_intents[{}]: unresolved notification_profile_key {!r}".format(
                    index, profile_key
                )
            )
        if archetype is not None and profile is not None:
            archetype_types = set(archetype["revision"]["compatible_item_types"])
            profile_types = set(profile["revision"]["compatible_item_types"])
            if not archetype_types.intersection(profile_types):
                errors.append(
                    f"$.binding_intents[{index}]: binding has no compatible item type"
                )
    return errors


def _schedule_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for profile_index, profile in enumerate(manifest["notification_profiles"]):
        for template_index, template in enumerate(profile["revision"]["templates"]):
            at = template["schedule"]["at"]
            if at["offset_basis"] == "calendar_days" and int(at["offset_days"]) < -3660:
                errors.append(
                    f"$.notification_profiles[{profile_index}].revision.templates[{template_index}]"
                    ".schedule.at.offset_days: outside supported range -3660..0"
                )
    return errors


def _ordering_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def ordered(values: list[Any], expected: list[Any], path: str) -> None:
        if values != expected:
            errors.append(f"{path}: values are not in deterministic order")

    runtime_versions = manifest["compatibility"]["spine_runtime_versions"]
    ordered(
        runtime_versions,
        sorted(runtime_versions, key=lambda value: tuple(int(part) for part in value.split("."))),
        "$.compatibility.spine_runtime_versions",
    )
    contracts = manifest["compatibility"]["spine_content_contracts"]
    ordered(contracts, sorted(contracts), "$.compatibility.spine_content_contracts")

    archetypes = manifest["archetypes"]
    ordered(
        [entry["archetype_key"] for entry in archetypes],
        sorted(entry["archetype_key"] for entry in archetypes),
        "$.archetypes",
    )
    for index, archetype in enumerate(archetypes):
        item_types = archetype["revision"]["compatible_item_types"]
        ordered(item_types, sorted(item_types), f"$.archetypes[{index}].revision.compatible_item_types")

    profiles = manifest["notification_profiles"]
    ordered(
        [entry["profile_key"] for entry in profiles],
        sorted(entry["profile_key"] for entry in profiles),
        "$.notification_profiles",
    )
    for index, profile in enumerate(profiles):
        item_types = profile["revision"]["compatible_item_types"]
        ordered(
            item_types,
            sorted(item_types),
            f"$.notification_profiles[{index}].revision.compatible_item_types",
        )
        template_keys = [
            entry["template_key"] for entry in profile["revision"]["templates"]
        ]
        ordered(
            template_keys,
            sorted(template_keys),
            f"$.notification_profiles[{index}].revision.templates",
        )

    binding_keys = [entry["archetype_key"] for entry in manifest["binding_intents"]]
    ordered(binding_keys, sorted(binding_keys), "$.binding_intents")
    return errors


def canonical_json(value: Any) -> str:
    """Encode the no-number subset of spine.canonical-json.v1."""

    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        pieces = ['"']
        for character in value:
            codepoint = ord(character)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("invalid surrogate code point in canonical JSON")
            if character == '"':
                pieces.append('\\"')
            elif character == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(character)
        pieces.append('"')
        return "".join(pieces)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("canonical JSON object keys must be strings")
        return "{" + ",".join(
            canonical_json(key) + ":" + canonical_json(value[key])
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"JSON numbers and unsupported values are forbidden: {value!r}")


def content_digest(manifest: dict[str, Any]) -> str:
    semantic_manifest = {
        key: value for key, value in manifest.items() if key != "content_identity"
    }
    preimage = {
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine-pack-content-sha256.v1",
        "manifest": semantic_manifest,
    }
    encoded = canonical_json(preimage).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_pack(manifest: Any, schema: dict[str, Any]) -> list[str]:
    errors = schema_errors(manifest, schema, schema)
    if errors:
        return errors
    assert isinstance(manifest, dict)

    errors = _duplicate_errors(manifest)
    if errors:
        return errors
    errors = _schedule_errors(manifest)
    if errors:
        return errors
    errors = _reference_errors(manifest)
    if errors:
        return errors
    errors = _ordering_errors(manifest)
    if errors:
        return errors

    actual = manifest["content_identity"]["digest"]
    expected = content_digest(manifest)
    if actual != expected:
        return [f"$.content_identity.digest: expected {expected}, got {actual}"]
    return []


class PackManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.fixture_manifest = load_json(FIXTURE_MANIFEST_PATH)

    def test_schema_identity_and_dialect(self) -> None:
        self.assertEqual(
            self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(
            self.schema["$id"],
            "https://spine-packs.local/contracts/schemas/"
            "spine-pack-manifest.v1.schema.json",
        )

    def test_every_fixture_has_expected_schema_result(self) -> None:
        for case in self.fixture_manifest["cases"]:
            with self.subTest(case=case["case_id"]):
                try:
                    fixture = load_json(ROOT / case["fixture"])
                except (json.JSONDecodeError, DuplicateObjectMember) as error:
                    errors = [str(error)]
                else:
                    errors = validate_pack(fixture, self.schema)
                if case["valid"]:
                    self.assertEqual(errors, [])
                else:
                    self.assertTrue(errors, "negative fixture unexpectedly validated")
                    self.assertIn(case["expected_error"], "\n".join(errors))

    def test_fixture_manifest_covers_every_test_fixture(self) -> None:
        fixture_root = ROOT / "tests/fixtures/pack-manifest"
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in fixture_root.rglob("*.json")
        }
        declared = {
            case["fixture"]
            for case in self.fixture_manifest["cases"]
            if case["fixture"].startswith("tests/fixtures/pack-manifest/")
        }
        self.assertEqual(actual, declared)

    def test_published_manifest_matches_positive_vector(self) -> None:
        for manifest_path, fixture_path in DRAFT_FIXTURE_PAIRS:
            with self.subTest(manifest=manifest_path.name):
                self.assertEqual(load_json(manifest_path), load_json(fixture_path))

    def test_fixture_manifest_covers_every_pack_manifest(self) -> None:
        actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "packs").rglob("*.json")}
        declared = {
            case["fixture"] for case in self.fixture_manifest["cases"]
            if case["fixture"].startswith("packs/") and case["valid"]
        }
        self.assertEqual(actual, declared)

    def test_elapsed_target_offset_allows_zero_but_rejects_positive_values(self) -> None:
        manifest = load_json(EXACT_TARGET_FIXTURE_PATH)
        self.assertEqual(validate_pack(manifest, self.schema), [])

        at = manifest["notification_profiles"][0]["revision"]["templates"][0][
            "schedule"
        ]["at"]
        self.assertEqual(at["offset_seconds"], "0")
        for invalid in ("1", "-0", "00"):
            with self.subTest(invalid=invalid):
                at["offset_seconds"] = invalid
                manifest["content_identity"]["digest"] = content_digest(manifest)
                self.assertIn(
                    "schedule: must match exactly one allowed shape",
                    "\n".join(validate_pack(manifest, self.schema)),
                )

    def test_predecessor_drafts_are_preserved(self) -> None:
        # Pin the reviewed artifact bytes, not just its mutable semantic digest.
        reviewed_hash = "c0baa85773b72d69e5e0a27ef0ddf4d3faa1eabb705fb368768ec630ab2bc21f"
        for path in (FIRST_DRAFT_MANIFEST_PATH, FIRST_POSITIVE_FIXTURE_PATH):
            with self.subTest(path=path.name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), reviewed_hash)
        previous = load_json(PREVIOUS_DRAFT_MANIFEST_PATH)
        current = load_json(DRAFT_MANIFEST_PATH)
        self.assertEqual(current["pack"], {
            "pack_id": "kinflow-starter", "version": "1.0.0-draft.3", "status": "draft",
        })
        reviewed_hash = "28c1f6358908a63b2b6cde0f1aadeec32bee3c3bd3a8912fd12b3f5295b122ab"
        for path in (PREVIOUS_DRAFT_MANIFEST_PATH, PREVIOUS_POSITIVE_FIXTURE_PATH):
            with self.subTest(path=path.name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), reviewed_hash)
        for field in ("manifest_schema", "compatibility", "dependencies"):
            self.assertEqual(current[field], previous[field])
        for field in ("archetypes", "notification_profiles", "binding_intents"):
            previous_keys = {
                "archetypes": "archetype_key", "notification_profiles": "profile_key",
                "binding_intents": "archetype_key",
            }
            key = previous_keys[field]
            retained = [entry for entry in current[field] if entry[key] in {v[key] for v in previous[field]}]
            self.assertEqual(retained, previous[field])
        self.assertEqual(content_digest(current), current["content_identity"]["digest"])
        self.assertNotEqual(current["content_identity"], previous["content_identity"])

    def test_lesson_matches_approved_content(self) -> None:
        manifest = load_json(DRAFT_MANIFEST_PATH)
        lesson = next(v for v in manifest["archetypes"] if v["archetype_key"] == "lesson")
        self.assertEqual(lesson, {
            "archetype_key": "lesson",
            "intended_status": "active",
            "revision": {
                "display_name": "Lesson",
                "description": "Scheduled instructional sessions such as classes, tutoring, coaching, or private lessons.",
                "compatible_item_types": ["event"],
            },
        })
        expected_templates = [
            {
                "template_key": key,
                "schedule": {
                    "kind": "once",
                    "at": {"kind": "target_offset", "offset_basis": "elapsed", "offset_seconds": offset},
                },
                "late_handling": {"kind": "deliver_within", "grace_seconds": grace},
            }
            for key, offset, grace in (
                ("one_hour_before", "-3600", "1800"),
                ("twenty_four_hours_before", "-86400", "21600"),
            )
        ]
        lesson_profile = next(v for v in manifest["notification_profiles"] if v["profile_key"] == "lesson_standard")
        self.assertEqual(lesson_profile, {
            "profile_key": "lesson_standard",
            "display_name": "Lesson standard",
            "description": "Default reminders for an upcoming lesson.",
            "intended_status": "active",
            "revision": {"compatible_item_types": ["event"], "templates": expected_templates},
        })
        lesson_binding = next(v for v in manifest["binding_intents"] if v["archetype_key"] == "lesson")
        self.assertEqual(lesson_binding, {
            "binding_kind": "archetype_default",
            "archetype_key": "lesson",
            "notification_profile_key": "lesson_standard",
        })

    def test_expanded_pack_rejects_reordered_arrays(self) -> None:
        for path in (
            ("archetypes",), ("notification_profiles",), ("binding_intents",),
            ("notification_profiles", 0, "revision", "templates"),
        ):
            with self.subTest(path=path):
                manifest = load_json(DRAFT_MANIFEST_PATH)
                collection = manifest
                for key in path:
                    collection = collection[key]
                collection.reverse()
                manifest["content_identity"]["digest"] = content_digest(manifest)
                errors = validate_pack(manifest, self.schema)
                self.assertIn("not in deterministic order", "\n".join(errors))

    def test_lesson_rejects_recurrence_and_localization_fields(self) -> None:
        for path, field, value in (
            (("notification_profiles", 0, "revision"), "recurrence_scope", "series"),
            (("notification_profiles", 0, "revision", "templates", 0, "schedule"), "recurrence", "weekly"),
            (("archetypes", 0, "revision"), "localized_display_names", {"en": "Lesson"}),
            (("notification_profiles", 0), "localized_display_names", {"en": "Lesson standard"}),
        ):
            with self.subTest(path=path, field=field):
                manifest = load_json(DRAFT_MANIFEST_PATH)
                target = manifest
                for key in path:
                    target = target[key]
                target[field] = value
                manifest["content_identity"]["digest"] = content_digest(manifest)
                errors = validate_pack(manifest, self.schema)
                expected = (
                    "schedule: must match exactly one allowed shape"
                    if field == "recurrence" else f"{field}: unknown field"
                )
                self.assertIn(expected, "\n".join(errors))

    def test_lesson_binding_references_and_default_uniqueness(self) -> None:
        manifest = load_json(DRAFT_MANIFEST_PATH)
        manifest["notification_profiles"] = [
            value for value in manifest["notification_profiles"]
            if value["profile_key"] != "lesson_standard"
        ]
        self.assertIn(
            "unresolved notification_profile_key 'lesson_standard'",
            "\n".join(validate_pack(manifest, self.schema)),
        )

    def test_draft_three_matches_approved_content(self) -> None:
        manifest = load_json(DRAFT_MANIFEST_PATH)
        archetypes = {v["archetype_key"]: v for v in manifest["archetypes"]}
        profiles = {v["profile_key"]: v for v in manifest["notification_profiles"]}
        expected = {
            "birthday": ("Birthday", "Annual birthday occasions for advance planning and day-of recognition."),
            "flight": ("Flight", "Scheduled flight departures."),
            "game_or_competition": ("Game or competition", "Scheduled sports games, tournaments, and competitions."),
        }
        for key, (name, description) in expected.items():
            self.assertEqual(archetypes[key]["revision"], {
                "display_name": name, "description": description, "compatible_item_types": ["event"],
            })
            self.assertEqual(profiles[key + "_standard"]["revision"]["compatible_item_types"], ["event"])
        schedules = {
            key: [
                (t["template_key"], t["schedule"]["at"], t["late_handling"]["grace_seconds"])
                for t in profiles[key]["revision"]["templates"]
            ]
            for key in ("birthday_standard", "flight_standard", "game_or_competition_standard")
        }
        self.assertEqual(schedules["game_or_competition_standard"], [
            ("twenty_four_hours_before", {"kind": "target_offset", "offset_basis": "elapsed", "offset_seconds": "-86400"}, "21600"),
            ("two_hours_before", {"kind": "target_offset", "offset_basis": "elapsed", "offset_seconds": "-7200"}, "3600"),
        ])
        self.assertEqual(
            [(key, at["offset_seconds"], grace) for key, at, grace in schedules["flight_standard"]],
            [("four_hours_before", "-14400", "3600"), ("one_hour_before", "-3600", "900"),
             ("seven_days_before", "-604800", "86400"), ("twenty_four_hours_before", "-86400", "21600")],
        )
        self.assertEqual(
            [(key, at["offset_days"], at["local_time"], grace) for key, at, grace in schedules["birthday_standard"]],
            [("birthday_day_at_nine", "0", "09:00:00", "43200"),
             ("one_day_before_at_nine", "-1", "09:00:00", "43200"),
             ("seven_days_before_at_nine", "-7", "09:00:00", "86400"),
             ("thirty_days_before_at_nine", "-30", "09:00:00", "259200")],
        )
        for key in expected:
            binding = next(v for v in manifest["binding_intents"] if v["archetype_key"] == key)
            self.assertEqual(binding["notification_profile_key"], key + "_standard")

    def test_calendar_day_boundaries_fail_closed(self) -> None:
        for field, value, expected in (
            ("offset_days", "-3661", "outside supported range -3660..0"),
            ("offset_days", "1", "must match exactly one allowed shape"),
            ("local_time", "9:00:00", "must match exactly one allowed shape"),
        ):
            with self.subTest(field=field, value=value):
                manifest = load_json(DRAFT_MANIFEST_PATH)
                manifest["notification_profiles"][0]["revision"]["templates"][0]["schedule"]["at"][field] = value
                manifest["content_identity"]["digest"] = content_digest(manifest)
                self.assertIn(expected, "\n".join(validate_pack(manifest, self.schema)))
        manifest = load_json(DRAFT_MANIFEST_PATH)
        manifest["binding_intents"].append({
            "binding_kind": "archetype_default",
            "archetype_key": "lesson",
            "notification_profile_key": "medical_appointment_standard",
        })
        self.assertIn(
            "duplicate archetype_default for archetype_key 'lesson'",
            "\n".join(validate_pack(manifest, self.schema)),
        )

    def test_published_manifest_contains_no_installation_identity(self) -> None:
        forbidden = {
            "actor_subject_id",
            "command_id",
            "delivery_target_id",
            "destination",
            "owner",
            "owner_group_id",
            "owner_subject_id",
            "receipt_id",
            "route",
            "subject_id",
            "timestamp",
        }

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for member in value.values():
                    visit(member)
            elif isinstance(value, list):
                for member in value:
                    visit(member)

        for manifest_path, _ in DRAFT_FIXTURE_PAIRS:
            with self.subTest(manifest=manifest_path.name):
                visit(load_json(manifest_path))


if __name__ == "__main__":
    unittest.main()
