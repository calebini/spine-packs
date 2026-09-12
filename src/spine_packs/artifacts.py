"""Installer artifact validation, derived from the existing contract-test helpers.

No command execution lives here. Schemas are shipped in the source checkout.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts/schemas"
EMBEDDED_SCHEMA = SCHEMA_ROOT / "spine-pack-embedded-values.v1.schema.json"
COMMAND_SHAPES = {
    "item_archetype.create": ("archetypeCreate", "spine.item-archetypes.v1"),
    "item_archetype.revise": ("archetypeRevise", "spine.item-archetypes.v1"),
    "notification_profile.create": ("profileCreate", "spine.notification-profiles.v1"),
    "notification_profile.revise": ("profileRevise", "spine.notification-profiles.v1"),
    "notification_profile.metadata.update": (
        "profileMetadataUpdate", "spine.notification-profile-metadata-update.v1"
    ),
    "notification_profile.binding.set": ("bindingSet", "spine.notification-profile-bindings.v1"),
}
SEMANTIC_CONTRACTS = {
    "archetypeSemantics": "spine.item-archetypes.v1",
    "profileSemantics": "spine.notification-profiles.v1",
    "bindingSemantics": "spine.notification-profile-bindings.v1",
}

ENTRYPOINTS = {
    "spine.pack-install-request.v1": "spine-pack-install-request.v1.schema.json",
    "spine.pack-install-plan.v1": "spine-pack-install-plan.v1.schema.json",
    "spine.pack-install-approval.v1": "spine-pack-install-approval.v1.schema.json",
    "spine.pack-apply-checkpoint.v1": "spine-pack-apply-checkpoint.v1.schema.json",
    "spine.pack-apply-result.v1": "spine-pack-apply-result.v1.schema.json",
    "spine.pack-verification-result.v1": "spine-pack-verification-result.v1.schema.json",
    "spine.pack-installer-result.v1": "spine-pack-installer-result.v1.schema.json",
}

DERIVATIONS = {
    "spine.pack-install-request.v1": "spine.pack-install-request-digest.v1",
    "spine.pack-install-plan.v1": "spine.pack-install-plan-digest.v1",
    "spine.pack-install-approval.v1": "spine.pack-install-approval-digest.v1",
    "spine.pack-apply-checkpoint.v1": "spine.pack-apply-checkpoint-digest.v1",
    "spine.pack-apply-result.v1": "spine.pack-apply-result-digest.v1",
    "spine.pack-verification-result.v1": "spine.pack-verification-result-digest.v1",
}

SIZE_LIMITS = {
    "spine.pack-install-request.v1": 65_536,
    "spine.pack-install-plan.v1": 8_388_608,
    "spine.pack-install-approval.v1": 262_144,
    "spine.pack-apply-checkpoint.v1": 16_777_216,
    "spine.pack-apply-result.v1": 16_777_216,
    "spine.pack-verification-result.v1": 16_777_216,
    "spine.pack-installer-result.v1": 1_048_576,
}

REQUIRED_EXECUTION_CONTRACTS = [
    "spine.canonical-json.v1",
    "spine.item-archetypes.v1",
    "spine.notification-profile-bindings.v1",
    "spine.notification-profile-catalog-cursor.v1",
    "spine.notification-profile-metadata-update.v1",
    "spine.notification-profile-readback.v1",
    "spine.notification-profiles.v1",
    "spine.system-info.v2",
    "spine.tickerd-compatibility.v1",
]

EXIT_MAP = {
    "success": ("0", None),
    "invalid_cli_or_artifact_input": ("2", "failed"),
    "invalid_pack_contract_or_digest": ("3", "failed"),
    "incompatible_spine_runtime_or_contracts": ("4", "failed"),
    "decision_required_for_drift": ("5", "decision_required"),
    "blocked_desired_state": ("6", "blocked"),
    "stale_plan_or_target_mismatch": ("7", "failed"),
    "spine_command_rejection": ("8", "failed"),
    "partial_apply": ("9", "partial"),
    "verification_mismatch": ("10", "mismatch"),
    "transport_or_environment_failure": ("11", "failed"),
}


class DuplicateObjectMember(ValueError):
    pass


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateObjectMember(key)
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_closed_object)


def canonical_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        raise ValueError("numbers are not allowed")
    if isinstance(value, str):
        pieces = ['"']
        for char in value:
            codepoint = ord(char)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("surrogates are not allowed")
            if char == '"':
                pieces.append('\\"')
            elif char == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(char)
        return "".join(pieces) + '"'
    if isinstance(value, list):
        return "[" + ",".join(canonical_text(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_text(key)}:{canonical_text(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"unsupported canonical value: {type(value).__name__}")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()


def canonical_value(contract: str, value: Any, shape: str | None = None) -> dict[str, Any]:
    text = canonical_text(value)
    if shape is None:
        shape = next(name for name, family in SEMANTIC_CONTRACTS.items() if family == contract)
    return {
        "contract": contract,
        "shape": shape,
        "canonical_json": text,
        "digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def seal(artifact: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(artifact)
    derivation = DERIVATIONS[value["artifact_schema"]]
    value["content_identity"] = {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": derivation,
    }
    value["content_identity"]["digest"] = digest(value)
    return value


def content_digest_errors(artifact: dict[str, Any]) -> list[str]:
    identity = artifact.get("content_identity")
    if not isinstance(identity, dict):
        return ["content_identity_missing"]
    candidate = deepcopy(artifact)
    claimed = candidate["content_identity"].pop("digest", None)
    if claimed != digest(candidate):
        return ["content_digest_mismatch"]
    expected = DERIVATIONS.get(artifact.get("artifact_schema"))
    if identity.get("derivation_version") != expected:
        return ["content_derivation_mismatch"]
    return []


@lru_cache(maxsize=32)
def _schema_document(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def _resolve_ref(
    reference: str, current_path: Path, current_schema: dict[str, Any]
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    file_part, marker, fragment = reference.partition("#")
    if file_part:
        target_path = (current_path.parent / file_part).resolve()
        root = _schema_document(target_path)
    else:
        target_path = current_path
        root = current_schema
    current: Any = root
    if marker and fragment:
        if not fragment.startswith("/"):
            raise ValueError(reference)
        for token in fragment[1:].split("/"):
            current = current[token.replace("~1", "/").replace("~0", "~")]
    if not isinstance(current, dict):
        raise TypeError(reference)
    return current, target_path, root


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "boolean": isinstance(value, bool),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
        "integer": type(value) is int,
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        target, target_path, target_root = _resolve_ref(
            schema["$ref"], schema_path, root_schema
        )
        return schema_errors(value, target, target_path, target_root, path)
    if "oneOf" in schema:
        candidates = [
            schema_errors(value, branch, schema_path, root_schema, path)
            for branch in schema["oneOf"]
        ]
        return [] if sum(not errors for errors in candidates) == 1 else [f"{path}: oneOf"]

    errors: list[str] = []
    if "const" in schema and json.dumps(value, sort_keys=True) != json.dumps(schema["const"], sort_keys=True):
        errors.append(f"{path}: const")
    if "enum" in schema and json.dumps(value, sort_keys=True) not in [json.dumps(x, sort_keys=True) for x in schema["enum"]]:
        errors.append(f"{path}: enum")
    expected_type = schema.get("type")
    if expected_type and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]
    for branch in schema.get("allOf", []):
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if "anyOf" in schema and all(
        schema_errors(value, branch, schema_path, root_schema, path)
        for branch in schema["anyOf"]
    ):
        errors.append(f"{path}: anyOf")
    if "not" in schema and not schema_errors(
        value, schema["not"], schema_path, root_schema, path
    ):
        errors.append(f"{path}: not")
    if isinstance(value, list) and "contains" in schema:
        count = sum(not schema_errors(item, schema["contains"], schema_path, root_schema)
                    for item in value)
        if not schema.get("minContains", 1) <= count <= schema.get("maxContains", len(value)):
            errors.append(f"{path}: contains")
    if type(value) is int and value < schema.get("minimum", value):
        errors.append(f"{path}: minimum")
    if "if" in schema:
        match = not schema_errors(value, schema["if"], schema_path, root_schema, path)
        branch = schema.get("then" if match else "else", {})
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: minLength")
        if len(value) > schema.get("maxLength", len(value)):
            errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: minItems")
        if len(value) > schema.get("maxItems", len(value)):
            errors.append(f"{path}: maxItems")
        if schema.get("uniqueItems"):
            encodings = [canonical_text(item) for item in value]
            if len(encodings) != len(set(encodings)):
                errors.append(f"{path}: uniqueItems")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(
                    schema_errors(
                        item,
                        schema["items"],
                        schema_path,
                        root_schema,
                        f"{path}[{index}]",
                    )
                )
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, member in value.items():
            if key in properties:
                errors.extend(
                    schema_errors(
                        member,
                        properties[key],
                        schema_path,
                        root_schema,
                        f"{path}.{key}",
                    )
                )
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: unknown")
    return errors


def validate_schema(artifact: dict[str, Any]) -> list[str]:
    if not isinstance(artifact, dict) or artifact.get("artifact_schema") not in ENTRYPOINTS:
        return ["unknown_artifact_schema"]
    name = ENTRYPOINTS[artifact["artifact_schema"]]
    path = SCHEMA_ROOT / name
    schema = _schema_document(path)
    return schema_errors(artifact, schema, path, schema)


def parse_json(data: bytes, *, public_response: bool = False) -> Any:
    """Strict UTF-8 parser; only pinned public readbacks may contain integers."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("byte_order_mark")

    def invalid_constant(value):
        raise ValueError("nonfinite_number")

    value = json.loads(data.decode("utf-8"), object_pairs_hook=_closed_object,
                       parse_constant=invalid_constant)

    def inspect(item):
        if public_response and type(item) is int:
            return
        if isinstance(item, dict):
            for key, child in item.items():
                canonical_text(key)
                inspect(child)
        elif isinstance(item, list):
            for child in item:
                inspect(child)
        else:
            canonical_text(item)

    inspect(value)
    return value


RESULT_REFERENCE = re.compile(r"\$\{spine-pack\.result:(action-[0-9]{6}):([a-z_]+)\}")
REFERENCE_PRODUCERS = {
    "item_archetype_id": ("item_archetype.create", "archetype", "archetype_key"),
    "notification_profile_id": ("notification_profile.create", "profile", "profile_key"),
}


def _reference_slots(value: Any, path: tuple = ()) -> list[tuple]:
    """Find reserved interpolation syntax, including nested values/member names."""
    if isinstance(value, str):
        return [(path, value)] if "${" in value else []
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if "${" in key:
                found.append(((*path, key, "<member-name>"), key))
            found.extend(_reference_slots(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_reference_slots(child, (*path, index)))
    return found


def result_reference_errors(
    value: Any, shape: str, plan: dict[str, Any] | None = None,
    index: int | None = None,
) -> list[str]:
    errors = []
    for path, text in _reference_slots(value):
        match = RESULT_REFERENCE.fullmatch(text)
        if not match:
            errors.append("result_reference_syntax_invalid")
            continue
        if shape != "bindingSetTemplate" or len(path) != 1 or path[0] not in REFERENCE_PRODUCERS:
            errors.append("result_reference_context_forbidden")
            continue
        producer_id, returned_field = match.groups()
        field = path[0]
        if returned_field != field:
            errors.append("result_reference_field_invalid")
            continue
        if plan is None:
            continue  # The containing plan supplies the mandatory correlation stage.
        consumer = plan["actions"][index]
        producers = [(i, a) for i, a in enumerate(plan["actions"]) if a["action_id"] == producer_id]
        if len(producers) != 1:
            errors.append("result_reference_producer_missing")
            continue
        producer_index, producer = producers[0]
        if producer_index >= index:
            errors.append("result_reference_not_earlier")
            continue
        command, kind, key_field = REFERENCE_PRODUCERS[field]
        desired_binding = json.loads(consumer["desired"]["canonical_json"])
        key = (consumer["object_key"].split(":", 1)[1] if kind == "archetype"
               else desired_binding["notification_profile_key"])
        object_key = kind + ":" + key
        roots = [c for c in plan["classifications"] if c["object_key"] == object_key]
        creates = [a for a in plan["actions"] if a["object_key"] == object_key and a["command"] == command]
        if len(roots) != 1 or roots[0]["classification"] != "missing" or roots[0]["identity"] is not None:
            errors.append("result_reference_root_not_missing")
            continue
        if producer["command"] != command or producer["object_key"] != object_key or len(creates) != 1:
            errors.append("result_reference_producer_mismatch")
            continue
        body = json.loads(producer["request_template"]["canonical_json"])
        root_value = json.loads(roots[0]["desired"]["canonical_json"])
        actual_value = (body["revision"] if kind == "archetype" else {
            "metadata": {"display_name": body["display_name"], "description": body["description"]},
            "revision": body["revision"],
        })
        if (body.get(key_field) != key or body.get("owner") != plan["request"]["owner"]
                or producer["desired"] != roots[0]["desired"] or actual_value != root_value):
            errors.append("result_reference_producer_mismatch")
    return errors


def canonical_value_errors(
    value: dict[str, Any], expected_shape: str | None = None
) -> list[str]:
    try:
        parsed = json.loads(value["canonical_json"], object_pairs_hook=_closed_object)
        canonical = canonical_text(parsed)
    except (ValueError, TypeError, json.JSONDecodeError, DuplicateObjectMember):
        return ["canonical_value_invalid"]
    if canonical != value["canonical_json"]:
        return ["canonical_value_not_canonical"]
    actual = hashlib.sha256(value["canonical_json"].encode("utf-8")).hexdigest()
    if actual != value["digest"]:
        return ["canonical_value_digest_mismatch"]
    shape = value.get("shape")
    allowed = dict(SEMANTIC_CONTRACTS)
    for prefix, contract in COMMAND_SHAPES.values():
        for suffix in ("Template", "Request", "Response"):
            allowed[prefix + suffix] = contract
    if shape not in allowed or value.get("contract") != allowed.get(shape):
        return ["embedded_contract_or_shape_mismatch"]
    if expected_shape is not None and shape != expected_shape:
        return ["embedded_context_shape_mismatch"]
    root = _schema_document(EMBEDDED_SCHEMA)
    errors = schema_errors(parsed, root["$defs"][shape], EMBEDDED_SCHEMA, root)
    if errors:
        return ["embedded_contract_invalid", *errors]
    if shape.endswith(("Template", "Request", "Response")):
        return result_reference_errors(parsed, shape)
    return []


def selection_assertion_errors(
    request: dict[str, Any], *, all_flag: bool = False,
    archetype_flags: list[str] | None = None,
) -> list[str]:
    if all_flag and archetype_flags is not None:
        return ["selection_flags_conflict"]
    if archetype_flags is not None and (not archetype_flags or any(not k for k in archetype_flags)):
        return ["selection_flags_empty"]
    if not all_flag and archetype_flags is None:
        return []
    assertion = ({"mode": "all"} if all_flag else
                 {"mode": "archetypes", "archetype_keys": sorted(set(archetype_flags))})
    return [] if assertion == request["request"]["selection"] else ["selection_assertion_mismatch"]


def artifact_size_errors(artifact: dict[str, Any]) -> list[str]:
    size = len(canonical_text(artifact).encode("utf-8"))
    return [] if size <= SIZE_LIMITS[artifact["artifact_schema"]] else ["artifact_too_large"]


def _sorted_unique(values: list[str]) -> bool:
    return values == sorted(set(values))


def _path_is_normalized(path: str) -> bool:
    return (
        path.startswith("/")
        and path != "/"
        and not path.endswith("/")
        and "//" not in path
        and all(part not in {".", ".."} for part in path.split("/"))
    )


def request_errors(request_artifact: dict[str, Any]) -> list[str]:
    errors = validate_schema(request_artifact) + content_digest_errors(request_artifact)
    request = request_artifact.get("request", {})
    selection = request.get("selection", {})
    keys = selection.get("archetype_keys", [])
    if selection.get("mode") == "archetypes" and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    target = request.get("target", {})
    host_name = target.get("host_name", "")
    if host_name != host_name.lower() or host_name.endswith(".") or ".." in host_name:
        errors.append("target_host_not_normalized")
    for value in (
        target.get("spine_command", {}).get("path", ""),
        target.get("ledger", {}).get("path", ""),
    ):
        if not _path_is_normalized(value):
            errors.append("target_path_not_normalized")
    return errors


def binding_identity_errors(plan: dict[str, Any]) -> list[str]:
    """Correlate owner-scoped key resolutions, binding readback, and requests."""
    errors = []
    roots = {}
    seen_ids = set()
    for entry in plan["classifications"]:
        if entry["object_kind"] == "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if identity is not None and set(identity) != {"catalog_id"}:
            errors.append("catalog_identity_shape_mismatch")
            continue
        if (state == "missing" and identity is not None) or (
            state in ("equivalent", "drifted") and identity is None
        ):
            errors.append("catalog_identity_state_mismatch")
        catalog_id = identity["catalog_id"] if identity is not None else None
        if catalog_id is not None:
            marker = (entry["object_kind"], catalog_id)
            if marker in seen_ids or catalog_id.startswith("${"):
                errors.append("catalog_identity_invalid")
            seen_ids.add(marker)
        roots[entry["object_key"]] = (state, catalog_id)

    for entry in plan["classifications"]:
        if entry["object_kind"] != "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if state == "blocked":
            if identity is not None:
                errors.append("blocked_binding_has_identity")
            continue
        if identity is None or set(identity) != {
            "item_archetype_id", "notification_profile_id", "observed_binding"
        }:
            errors.append("binding_identity_missing_or_invalid")
            continue
        desired = json.loads(entry["desired"]["canonical_json"])
        root_keys = {
            "item_archetype_id": "archetype:" + entry["object_key"].split(":", 1)[1],
            "notification_profile_id": "profile:" + desired["notification_profile_key"],
        }
        for field, key in root_keys.items():
            root = roots.get(key)
            if root is None or root[0] == "blocked" or identity[field] != root[1]:
                errors.append("binding_resolution_mismatch")
        observed = identity["observed_binding"]
        if (state == "missing") != (observed is None):
            errors.append("binding_observation_state_mismatch")
        if observed is not None:
            if any(value.startswith("${") for value in observed.values()):
                errors.append("binding_identity_invalid")
            if identity["item_archetype_id"] is None or (
                observed["item_archetype_id"] != identity["item_archetype_id"]
            ):
                errors.append("binding_archetype_identity_mismatch")
            same_profile = (
                identity["notification_profile_id"] is not None
                and observed["notification_profile_id"] == identity["notification_profile_id"]
            )
            if (state == "equivalent") != same_profile:
                errors.append("binding_profile_identity_mismatch")
            observed_value = entry["observed"]
            if observed_value is not None:
                observed_key = json.loads(observed_value["canonical_json"])["notification_profile_key"]
                observed_root = roots.get("profile:" + observed_key)
                if observed_root is not None and observed_root[1] != observed["notification_profile_id"]:
                    errors.append("binding_observed_key_identity_mismatch")

        for action in plan["actions"]:
            if action["object_key"] != entry["object_key"]:
                continue
            if action["command"] != "notification_profile.binding.set":
                errors.append("binding_action_command_mismatch")
                continue
            request = json.loads(action["request_template"]["canonical_json"])
            if request.get("owner") != plan["request"]["owner"]:
                errors.append("binding_action_owner_mismatch")
            for field, key in root_keys.items():
                expected = identity[field]
                if expected is None:
                    command = "item_archetype.create" if field == "item_archetype_id" else "notification_profile.create"
                    creates = [a for a in plan["actions"] if a["object_key"] == key and a["command"] == command]
                    if len(creates) != 1 or int(creates[0]["ordinal"]) >= int(action["ordinal"]):
                        errors.append("binding_create_reference_missing")
                        continue
                    expected = "${spine-pack.result:" + creates[0]["action_id"] + ":" + field + "}"
                if request.get(field) != expected:
                    errors.append("binding_action_identity_mismatch")
    return errors


def plan_errors(plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(plan) + content_digest_errors(plan)
    if validate_schema(plan):
        return errors
    request = plan["request"]
    embedded_request = seal(
        {
            "artifact_schema": "spine.pack-install-request.v1",
            "request": request,
        }
    )
    if plan["request_digest"] != embedded_request["content_identity"]["digest"]:
        errors.append("request_digest_mismatch")
    errors.extend(request_errors(embedded_request))
    keys = request["selection"].get("archetype_keys", [])
    if keys and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    for field in ("archetype_keys", "profile_keys", "binding_archetype_keys"):
        if not _sorted_unique(plan["closure"][field]):
            errors.append(f"closure_{field}_not_sorted")
    if plan["required_execution_contracts"] != REQUIRED_EXECUTION_CONTRACTS:
        errors.append("execution_contract_union_mismatch")
    if not _sorted_unique(plan["environment"]["advertised_contracts"]):
        errors.append("advertised_contracts_not_sorted")
    if not set(REQUIRED_EXECUTION_CONTRACTS).issubset(
        plan["environment"]["advertised_contracts"]
    ):
        errors.append("required_execution_contract_missing")
    if [entry["catalog"] for entry in plan["catalog_snapshots"]] != [
        "archetypes", "profiles", "bindings"
    ]:
        errors.append("catalog_snapshot_order")
    expected_object_keys = (
        [f"archetype:{key}" for key in plan["closure"]["archetype_keys"]]
        + [f"profile:{key}" for key in plan["closure"]["profile_keys"]]
        + [f"binding:{key}" for key in plan["closure"]["binding_archetype_keys"]]
    )
    if [entry["object_key"] for entry in plan["classifications"]] != expected_object_keys:
        errors.append("classification_scope_mismatch")
    expected_ids = [f"action-{index:06d}" for index in range(len(plan["actions"]))]
    if [entry["action_id"] for entry in plan["actions"]] != expected_ids:
        errors.append("action_order_or_identity")
    if [entry["ordinal"] for entry in plan["actions"]] != [
        str(index) for index in range(len(plan["actions"]))
    ]:
        errors.append("action_ordinal")
    action_rank = {
        "item_archetype.create": 0,
        "item_archetype.revise": 0,
        "notification_profile.create": 1,
        "notification_profile.metadata.update": 2,
        "notification_profile.revise": 3,
        "notification_profile.binding.set": 4,
    }
    action_order = [
        (action_rank[entry["command"]], entry["object_key"])
        for entry in plan["actions"]
    ]
    if action_order != sorted(action_order):
        errors.append("action_order")
    updates = [
        entry["action_id"] for entry in plan["actions"] if entry["change_kind"] == "update"
    ]
    if plan["decision_action_ids"] != updates:
        errors.append("decision_action_ids_mismatch")
    blocked = [
        entry["object_key"]
        for entry in plan["classifications"]
        if entry["classification"] == "blocked"
    ]
    if plan["blocked_object_keys"] != sorted(blocked):
        errors.append("blocked_object_keys_mismatch")
    if plan["pack"]["status"] == "draft" and plan["apply_eligible"]:
        errors.append("draft_plan_apply_eligible")
    if plan["pack"]["status"] == "draft" and request["draft_posture"] != "inspect_only":
        errors.append("draft_posture_mismatch")
    if plan["pack"]["status"] == "released" and "-draft." in plan["pack"]["version"]:
        errors.append("pack_version_status_mismatch")
    if plan["pack"]["status"] == "draft" and not re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)-draft\.[1-9][0-9]*",
        plan["pack"]["version"],
    ):
        errors.append("pack_version_status_mismatch")
    if blocked and plan["apply_eligible"]:
        errors.append("blocked_plan_apply_eligible")
    for classification in plan["classifications"]:
        observed = classification["observed"]
        reason = classification["blocked_reason"]
        if classification["classification"] == "missing" and observed is not None:
            errors.append("missing_has_observed")
        if classification["classification"] == "blocked" and reason is None:
            errors.append("blocked_without_reason")
        if classification["classification"] != "blocked" and reason is not None:
            errors.append("unexpected_blocked_reason")
        if classification["classification"] in ("equivalent", "drifted") and observed is None:
            errors.append("classification_observation_missing")
        shape = classification["object_kind"] + "Semantics"
        errors.extend(canonical_value_errors(classification["desired"], shape))
        if observed is not None:
            errors.extend(canonical_value_errors(observed, shape))
            equal = classification["desired"]["canonical_json"] == observed["canonical_json"]
            if classification["classification"] == "equivalent" and not equal:
                errors.append("equivalence_preimage_mismatch")
            if classification["classification"] == "drifted" and equal:
                errors.append("drift_preimages_equal")
    class_rank = {"archetype": 0, "profile": 1, "binding": 2}
    classification_order = [
        (class_rank[entry["object_kind"]], entry["object_key"])
        for entry in plan["classifications"]
    ]
    if classification_order != sorted(classification_order):
        errors.append("classification_order")
    for action in plan["actions"]:
        shape = action["object_key"].split(":")[0] + "Semantics"
        errors.extend(canonical_value_errors(action["desired"], shape))
        prefix = COMMAND_SHAPES[action["command"]][0]
        errors.extend(canonical_value_errors(action["request_template"], prefix + "Template"))
        if action["expected"] is not None:
            errors.extend(canonical_value_errors(action["expected"], shape))
        if action["change_kind"] == "create" and action["expected"] is not None:
            errors.append("create_has_expected")
        if action["change_kind"] == "update" and action["expected"] is None:
            errors.append("update_without_expected")
    # Embedded data must be valid before the identity correlator decodes it.
    if not errors:
        errors.extend(binding_identity_errors(plan))
        for index, action in enumerate(plan["actions"]):
            errors.extend(result_reference_errors(
                json.loads(action["request_template"]["canonical_json"]),
                COMMAND_SHAPES[action["command"]][0] + "Template", plan, index,
            ))
    return errors
