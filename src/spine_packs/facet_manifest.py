"""Complete portable manifest-v2 validation; no Spine imports or execution.

Semantic rules derived from the reviewed FR-1 oracle; the original oracle stays
independent and cross-checks runtime output with official Draft 2020-12.
"""
import re
import unicodedata
from copy import deepcopy
from . import artifacts as a
from .facet_contracts import validate as validate_schema, ordered
from .planning import require as need, PACK_INVALID

def require(condition, reason):
    need(condition, 'invalid_manifest_semantics', PACK_INVALID)

def canonical(value):
    return a.canonical_text(value).encode('utf-8')

def rendering_size_floor(revision, observed_revisions=None):
    """Exact wire size when resolved; a conservative lower bound otherwise.

    Local references are not wire IDs. Count unknown IDs as empty JSON strings
    plus one byte (the public nonempty-string minimum), without predicting or
    publishing an ID. Only the byte count leaves this helper.
    """
    observed_revisions = observed_revisions or {}
    wire = deepcopy(revision)
    unknown = 0
    for selection in wire['selections']:
        key = selection.pop('schema_ref')['schema_key']
        identity = observed_revisions.get(key)
        selection['facet_schema_revision_id'] = identity if identity is not None else ''
        unknown += identity is None
    return len(canonical(wire)) + unknown

def digest(manifest):
    return a.digest({'canonical_json_version': 'spine.canonical-json.v1',
                     'derivation_version': 'spine-pack-content-sha256.v2',
                     'manifest': {k: v for k, v in manifest.items() if k != 'content_identity'}})

def validate(manifest):
    require(len(canonical(manifest)) <= 16 * 1024 * 1024, "manifest byte limit")
    validate_schema(manifest, "spine-pack-manifest.v2.schema.json", category=PACK_INVALID)
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
        require(rendering_size_floor(revision) <= 8192, "rendering definition byte limit")
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
