"""FR-1 manifest-only oracle; deliberately not imported by installer runtime.

Structural/meta-validation requires the development dependency jsonschema.
Run this module explicitly in the isolated qualification environment before
claiming the FR-1 manifest gate. Missing jsonschema is a visible skip, not proof.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import unittest

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    Draft202012Validator = None
    ValidationError = ValueError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "contracts/schemas/spine-pack-manifest.v2.schema.json"
FIXTURE = ROOT / "tests/fixtures/pack-manifest-v2/flight.json"
INDEX = ROOT / "contracts/pack-fixture-manifest.v2.json"


def load(path):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError("duplicate JSON member")
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def require(value, reason):
    if not value:
        raise ValueError(reason)


def canonical(value):
    def inspect(v):
        require(type(v) not in (int, float), "JSON numbers forbidden")
        if isinstance(v, str):
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in v), "invalid Unicode")
        elif isinstance(v, dict):
            for k, x in v.items():
                inspect(k)
                inspect(x)
        elif isinstance(v, list):
            for x in v:
                inspect(x)
    inspect(value)
    # JSON's short control escapes are not Spine canonical-json.v1 escapes.
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    text = re.sub(r'\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})',
                  lambda m: {r'\b': r'\u0008', r'\f': r'\u000c', r'\n': r'\u000a',
                             r'\r': r'\u000d', r'\t': r'\u0009'}.get(m[0], m[0]), text)
    return text.encode("utf-8")


def digest(manifest):
    return hashlib.sha256(canonical({
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine-pack-content-sha256.v2",
        "manifest": {k: v for k, v in manifest.items() if k != "content_identity"},
    })).hexdigest()


def ordered(values):
    require(values == sorted(set(values)), "duplicate or noncanonical ordering")


def validate(manifest):
    require(len(canonical(manifest)) <= 16 * 1024 * 1024, "manifest byte limit")
    Draft202012Validator(load(SCHEMA)).validate(manifest)
    def catalog_keys(value):
        if isinstance(value, dict):
            for name, member in value.items():
                if name == "key" or name.endswith("_key"):
                    require(re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", member), "noncanonical catalog key")
                catalog_keys(member)
        elif isinstance(value, list):
            for member in value:
                catalog_keys(member)
    catalog_keys(manifest)
    families = {}
    for array, key in (("archetypes", "archetype_key"), ("notification_profiles", "profile_key"),
                       ("facet_schemas", "schema_key"), ("rendering_definitions", "definition_key")):
        ordered([x[key] for x in manifest[array]])
        families[array] = {x[key]: x for x in manifest[array]}
    archetypes, profiles, schemas, renderings = (families[k] for k in (
        "archetypes", "notification_profiles", "facet_schemas", "rendering_definitions"))

    def target(mapping, key):
        require(key in mapping, "missing or wrong-kind local reference")
        return mapping[key]

    def types(revision):
        ordered(revision["compatible_item_types"])
        return set(revision["compatible_item_types"])

    for a in archetypes.values():
        types(a["revision"])
    for s in schemas.values():
        definition = s["definition"]
        types(definition)
        require(len(canonical(definition)) <= 32768, "facet definition byte limit")
        def nfc(v):
            if isinstance(v, str):
                require(v == unicodedata.normalize("NFC", v), "facet NFC")
            elif isinstance(v, list):
                for x in v:
                    nfc(x)
            elif isinstance(v, dict):
                for x in v.values():
                    nfc(x)
        nfc(definition)
        ordered([f["key"] for f in definition["fields"]])
        for f in definition["fields"]:
            if f["type"] == "enum":
                ordered(f["choices"])
            if f["type"] == "integer":
                require(-(2**63) <= int(f["min"]) <= int(f["max"]) < 2**63, "integer range")
    bindings = {}
    ordered([(b["archetype_key"], b["facet_key"]) for b in manifest["archetype_facet_bindings"]])
    for b in manifest["archetype_facet_bindings"]:
        a = target(archetypes, b["archetype_key"])
        s = target(schemas, b["schema_ref"]["schema_key"])
        require(types(a["revision"]) & types(s["definition"]), "incompatible facet binding")
        bindings[(b["archetype_key"], b["facet_key"])] = b["schema_ref"]["schema_key"]
    for r in renderings.values():
        revision = r["revision"]
        used, names = set(), set()
        for text in [revision["display_name"], revision["description"], *[x["label"] for x in revision["selections"]]]:
            if text is not None:
                require(text == " ".join(text.split()) and text, "rendering text normalization")
                require(not any(unicodedata.category(c).startswith("C") for c in text), "rendering control character")
        for selection in revision["selections"]:
            sk = selection["schema_ref"]["schema_key"]
            schema = target(schemas, sk)["definition"]
            require(types(revision) <= types(schema), "rendering/schema type coverage")
            field = target({f["key"]: f for f in schema["fields"]}, selection["field_key"])
            projection = "location_label" if field["type"] == "reference" and field["target_kind"] == "location" else "value"
            require(field["type"] != "reference" or projection == "location_label", "subject disclosure forbidden")
            require(selection["projection"] == projection, "projection type mismatch")
            source = (selection["facet_key"], sk, selection["field_key"])
            require(source not in used and selection["selection_key"] not in names, "duplicate selection")
            used.add(source)
            names.add(selection["selection_key"])
    for p in profiles.values():
        revision = p["revision"]
        types(revision)
        ordered([t["template_key"] for t in revision["templates"]])
        schedules = [canonical(t["schedule"]) for t in revision["templates"]]
        require(len(schedules) == len(set(schedules)), "duplicate timing templates")
        for t in revision["templates"]:
            at = t["schedule"]["at"]
            if at["offset_basis"] == "calendar_days":
                require(-3660 <= int(at["offset_days"]) <= 0, "calendar offset range")
            rendering = t["rendering"]
            if rendering["kind"] == "definition":
                r = target(renderings, rendering["definition_ref"]["definition_key"])
                require(types(revision) <= types(r["revision"]), "profile/rendering type coverage")
    ordered([b["archetype_key"] for b in manifest["binding_intents"]])
    for b in manifest["binding_intents"]:
        a = target(archetypes, b["archetype_key"])
        p = target(profiles, b["notification_profile_key"])
        require(types(a["revision"]) & types(p["revision"]), "incompatible default")
        for t in p["revision"]["templates"]:
            rendering = t["rendering"]
            if rendering["kind"] == "definition":
                r = renderings[rendering["definition_ref"]["definition_key"]]
                for s in r["revision"]["selections"]:
                    require(bindings.get((b["archetype_key"], s["facet_key"])) == s["schema_ref"]["schema_key"],
                            "missing matching archetype facet binding")
    require(manifest["content_identity"]["digest"] == digest(manifest), "content digest mismatch")


@unittest.skipIf(Draft202012Validator is None, "FR-1 requires development jsonschema; run isolated schema gate")
class FacetManifestTests(unittest.TestCase):
    def test_schema_and_fixture(self):
        Draft202012Validator.check_schema(load(SCHEMA))
        validate(load(FIXTURE))

    def test_indexed_vectors(self):
        for vector in load(INDEX)["vectors"]:
            with self.subTest(vector=vector["id"]):
                manifest = load(FIXTURE)
                for edit in vector["edits"]:
                    container = manifest
                    for part in edit["path"][:-1]:
                        container = container[part]
                    final = edit["path"][-1]
                    if edit["op"] == "remove":
                        del container[final]
                    else:
                        container[final] = deepcopy(edit["value"])
                if vector["reseal"]:
                    manifest["content_identity"]["digest"] = digest(manifest)
                if vector["valid"]:
                    validate(manifest)
                else:
                    with self.assertRaises((ValueError, ValidationError)):
                        validate(manifest)

    def test_presentation_order_is_not_sorted_away(self):
        manifest = load(FIXTURE)
        before = digest(manifest)
        manifest["rendering_definitions"][0]["revision"]["selections"].reverse()
        manifest["content_identity"]["digest"] = digest(manifest)
        self.assertNotEqual(before, digest(manifest))
        validate(manifest)

    def test_v1_rejects_v2_and_released_content_is_not_changed(self):
        v1 = load(ROOT / "contracts/schemas/spine-pack-manifest.v1.schema.json")
        self.assertFalse(Draft202012Validator(v1).is_valid(load(FIXTURE)))
        stable = load(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json")
        flight = next(p for p in stable["notification_profiles"] if p["profile_key"] == "flight_standard")
        desired = load(FIXTURE)["notification_profiles"][0]
        without_rendering = [{k: v for k, v in t.items() if k != "rendering"} for t in desired["revision"]["templates"]]
        self.assertEqual(flight["revision"]["templates"], without_rendering)

    def test_canonical_controls_and_numbers(self):
        self.assertEqual(canonical("\n"), b'"\\u000a"')
        self.assertEqual(canonical("\\n"), b'"\\\\n"')
        with self.assertRaises(ValueError):
            canonical({"n": 1})


if __name__ == "__main__":
    unittest.main()
