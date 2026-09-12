#!/usr/bin/env python3
"""Dependency-free contract checks for Spine pack installer artifacts."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts/schemas"
FIXTURE_MANIFEST = ROOT / "contracts/installer-fixture-manifest.v1.json"
POSITIVE_ROOT = ROOT / "tests/fixtures/installer/positive"
NEGATIVE_ROOT = ROOT / "tests/fixtures/installer/negative"
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
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: const")
    if "enum" in schema and value not in schema["enum"]:
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
    name = ENTRYPOINTS[artifact["artifact_schema"]]
    path = SCHEMA_ROOT / name
    schema = _schema_document(path)
    return schema_errors(artifact, schema, path, schema)


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


def command_id(plan_digest: str, execution_id: str, action_id: str) -> str:
    return "spack_" + digest(
        {
            "action_id": action_id,
            "derivation_version": "spine.pack-command-id.v1",
            "execution_id": execution_id,
            "plan_digest": plan_digest,
        }
    )


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


def approval_errors(approval: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(approval) + content_digest_errors(approval)
    if approval["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("approval_plan_digest_mismatch")
    if approval["authorized_update_action_ids"] != plan["decision_action_ids"]:
        errors.append("update_authorization_incomplete")
    return errors


def apply_preflight_errors(
    plan: dict[str, Any],
    target: dict[str, Any],
    environment: dict[str, Any],
    catalog_snapshots: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if target != plan["request"]["target"]:
        errors.append("target_binding_mismatch")
    if environment != plan["environment"]:
        errors.append("stale_plan_environment_mismatch")
    if catalog_snapshots != plan["catalog_snapshots"]:
        errors.append("stale_plan_catalog_snapshot")
    return errors


def _response_prefix_errors(
    responses: list[dict[str, Any]], plan: dict[str, Any], execution: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    schema_path = SCHEMA_ROOT / "spine-pack-installer-types.v1.schema.json"
    schema = _schema_document(schema_path)
    for response in responses:
        errors.extend(schema_errors(response, schema["$defs"]["responseEvidence"], schema_path, schema))
    if errors:
        return ["response_evidence_invalid", *errors]
    expected_actions = plan["actions"][: len(responses)]
    if [entry["action_id"] for entry in responses] != [
        entry["action_id"] for entry in expected_actions
    ]:
        errors.append("accepted_prefix_not_contiguous")
    for response, action in zip(responses, expected_actions):
        expected_command_id = command_id(
            plan["content_identity"]["digest"],
            execution["execution_id"],
            action["action_id"],
        )
        if response["command_id"] != expected_command_id:
            errors.append("command_id_mismatch")
        if response["command"] != action["command"]:
            errors.append("response_command_mismatch")
        shape = COMMAND_SHAPES[action["command"]][0] + "Response"
        embedded_errors = canonical_value_errors(response["response"], shape)
        errors.extend(embedded_errors)
        if not embedded_errors:
            body = json.loads(response["response"]["canonical_json"])
            template = json.loads(action["request_template"]["canonical_json"])
            if action["command"] in ("item_archetype.create", "notification_profile.create"):
                key = "archetype_key" if action["command"] == "item_archetype.create" else "profile_key"
                if body[key] != template[key]:
                    errors.append("response_create_key_mismatch")
            for field in ("command", "response_contract", "effect"):
                if response[field] != body[field]:
                    errors.append("response_evidence_mismatch")
            for field in ("command_id", "command_receipt_id", "semantic_facts_hash", "effect"):
                if response[field] != body["receipt"][field]:
                    errors.append("receipt_evidence_mismatch")
            if body["receipt"]["created_at_utc"] != execution["action_timestamp_utc"]:
                errors.append("receipt_timestamp_mismatch")
            returned_ids = [
                {"name": key, "value": body[key]}
                for key in sorted(body) if key.endswith("_id")
            ]
            if response["generated_ids"] != returned_ids:
                errors.append("response_generated_ids_mismatch")
        names = [item["name"] for item in response["generated_ids"]]
        if not _sorted_unique(names):
            errors.append("generated_ids_not_sorted")
    return errors


def checkpoint_errors(
    checkpoint: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = (validate_schema(checkpoint) + content_digest_errors(checkpoint)
              + plan_errors(plan) + approval_errors(approval, plan))
    if checkpoint["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("checkpoint_plan_digest_mismatch")
    if checkpoint["approval_digest"] != approval["content_identity"]["digest"]:
        errors.append("checkpoint_approval_digest_mismatch")
    if checkpoint["execution"] != approval["execution"]:
        errors.append("checkpoint_execution_mismatch")
    responses = checkpoint["accepted_responses"]
    errors.extend(_response_prefix_errors(responses, plan, checkpoint["execution"]))
    next_index = len(responses)
    expected_next = (
        plan["actions"][next_index]["action_id"]
        if next_index < len(plan["actions"])
        else None
    )
    if checkpoint["next_action_id"] != expected_next:
        errors.append("checkpoint_next_action_mismatch")
    unresolved = checkpoint["unresolved_submission"]
    if unresolved is not None:
        if unresolved["action_id"] != expected_next:
            errors.append("unresolved_action_mismatch")
        expected_command_id = command_id(
            plan["content_identity"]["digest"],
            checkpoint["execution"]["execution_id"],
            unresolved["action_id"],
        )
        if unresolved["command_id"] != expected_command_id:
            errors.append("command_id_mismatch")
        if next_index < len(plan["actions"]):
            action = plan["actions"][next_index]
            prefix = COMMAND_SHAPES[action["command"]][0]
            errors.extend(canonical_value_errors(unresolved["request"], prefix + "Request"))
            try:
                expected_request = _materialized_request(plan, approval, next_index, responses)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if unresolved["request"]["canonical_json"] != canonical_text(expected_request):
                    errors.append("unresolved_request_mismatch")
    return errors


def apply_result_errors(
    result: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = (validate_schema(result) + content_digest_errors(result)
              + plan_errors(plan) + approval_errors(approval, plan))
    if result["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("apply_plan_digest_mismatch")
    if result["approval_digest"] != approval["content_identity"]["digest"]:
        errors.append("apply_approval_digest_mismatch")
    if result["execution"] != approval["execution"]:
        errors.append("apply_execution_mismatch")
    responses = result["accepted_responses"]
    errors.extend(_response_prefix_errors(responses, plan, result["execution"]))
    remaining = [entry["action_id"] for entry in plan["actions"][len(responses) :]]
    if result["state"] == "applied":
        if len(responses) != len(plan["actions"]) or result["failure"] is not None:
            errors.append("applied_not_complete")
        if result["unattempted_action_ids"]:
            errors.append("applied_has_unattempted")
    elif result["state"] == "partial":
        if result["failure"] is None or not remaining:
            errors.append("partial_without_failure")
        else:
            if result["failure"]["action_id"] != remaining[0]:
                errors.append("partial_failed_action_mismatch")
            if result["unattempted_action_ids"] != remaining[1:]:
                errors.append("partial_suffix_mismatch")
    elif responses or result["failure"] is None:
        errors.append("not_applied_shape_mismatch")
    return errors


def verification_errors(
    verification: dict[str, Any], plan: dict[str, Any], result: dict[str, Any]
) -> list[str]:
    errors = validate_schema(verification) + content_digest_errors(verification)
    if verification["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("verification_plan_digest_mismatch")
    if verification["apply_result_digest"] != result["content_identity"]["digest"]:
        errors.append("verification_apply_digest_mismatch")
    if verification["target"] != plan["request"]["target"]:
        errors.append("target_binding_mismatch")
    if verification["pack"] != plan["pack"] or verification["closure"] != plan["closure"]:
        errors.append("verification_scope_mismatch")
    object_states = [entry["state"] for entry in verification["object_results"]]
    for entry in verification["object_results"]:
        if entry["observed"] is not None:
            errors.extend(canonical_value_errors(
                entry["observed"], entry["object_kind"] + "Semantics"
            ))
    should_verify = (
        all(state == "equivalent" for state in object_states)
        and verification["response_evidence"] == "complete"
    )
    if (verification["state"] == "verified") != should_verify:
        errors.append("verification_state_mismatch")
    return errors


def envelope_errors(envelope: dict[str, Any]) -> list[str]:
    errors = validate_schema(envelope) + artifact_size_errors(envelope)
    error = envelope["error"]
    if error is None:
        if envelope["status"] != "success" or envelope["exit_code"] != "0":
            errors.append("envelope_exit_mismatch")
    else:
        expected_exit, expected_status = EXIT_MAP[error["category"]]
        if envelope["exit_code"] != expected_exit or envelope["status"] != expected_status:
            errors.append("envelope_exit_mismatch")
        names = [entry["name"] for entry in error["facts"]]
        if not _sorted_unique(names):
            errors.append("error_facts_not_sorted")
    return errors


def _fixture_request() -> dict[str, Any]:
    value = load_json(POSITIVE_ROOT / "granular_request.json")
    assert isinstance(value, dict)
    return value


def _desired_values() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    archetype = canonical_value(
        "spine.item-archetypes.v1",
        {
            "compatible_item_types": ["event"],
            "description": "A scheduled health appointment.",
            "display_name": "Medical appointment",
        },
    )
    profile = canonical_value(
        "spine.notification-profiles.v1",
        {
            "metadata": {
                "display_name": "Medical appointment standard",
                "description": "Preparation for a medical appointment.",
            },
            "revision": {
                "compatible_item_types": ["event"],
                "templates": [
                {
                    "late_handling": {"grace_seconds": "3600", "kind": "deliver_within"},
                    "schedule": {
                        "at": {
                            "kind": "target_offset",
                            "offset_basis": "elapsed",
                            "offset_seconds": "-7200",
                        },
                        "kind": "once",
                    },
                    "template_key": "two_hours_before",
                }
                ],
            },
        },
    )
    binding = canonical_value(
        "spine.notification-profile-bindings.v1",
        {
            "binding_kind": "archetype_default",
            "notification_profile_key": "medical_appointment_standard",
        },
    )
    return archetype, profile, binding


def make_plan(request: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
    archetype, profile, binding = _desired_values()
    old_profile_value = json.loads(profile["canonical_json"])
    old_profile_value["revision"]["templates"][0]["schedule"]["at"]["offset_seconds"] = "-10800"
    old_profile = canonical_value("spine.notification-profiles.v1", old_profile_value)
    equivalent_lesson = canonical_value("spine.item-archetypes.v1", {
        "display_name": "Lesson", "description": "A scheduled instructional session.",
        "compatible_item_types": ["event"],
    })
    lesson_profile = json.loads(profile["canonical_json"])
    lesson_profile["metadata"] = {
        "display_name": "Lesson standard", "description": "Preparation for a lesson."
    }
    equivalent_lesson_profile = canonical_value(
        "spine.notification-profiles.v1", lesson_profile
    )
    equivalent_lesson_binding = canonical_value(
        "spine.notification-profile-bindings.v1",
        {"binding_kind": "archetype_default", "notification_profile_key": "lesson_standard"}
    )
    plan = {
        "artifact_schema": "spine.pack-install-plan.v1",
        "request_digest": request["content_identity"]["digest"],
        "request": deepcopy(request["request"]),
        "pack": {
            "manifest_schema": "spine.pack-manifest.v1",
            "pack_id": "kinflow-starter",
            "version": "1.0.0-draft.9" if draft else "1.0.0",
            "status": "draft" if draft else "released",
            "manifest_digest": "1" * 64,
        },
        "closure": {
            "archetype_keys": ["lesson", "medical_appointment"],
            "profile_keys": ["lesson_standard", "medical_appointment_standard"],
            "binding_archetype_keys": ["lesson", "medical_appointment"],
        },
        "environment": {
            "runtime_version": "0.3.0",
            "ledger_schema_implemented": "12",
            "ledger_schema_current": "12",
            "advertised_contracts": REQUIRED_EXECUTION_CONTRACTS,
        },
        "required_execution_contracts": REQUIRED_EXECUTION_CONTRACTS,
        "catalog_snapshots": [
            {"catalog": "archetypes", "digest": "2" * 64},
            {"catalog": "profiles", "digest": "3" * 64},
            {"catalog": "bindings", "digest": "4" * 64},
        ],
        "classifications": [
            {"object_kind": "archetype", "object_key": "archetype:lesson", "classification": "equivalent", "desired": equivalent_lesson, "observed": equivalent_lesson, "blocked_reason": None},
            {"object_kind": "archetype", "object_key": "archetype:medical_appointment", "classification": "equivalent", "desired": archetype, "observed": archetype, "blocked_reason": None},
            {"object_kind": "profile", "object_key": "profile:lesson_standard", "classification": "equivalent", "desired": equivalent_lesson_profile, "observed": equivalent_lesson_profile, "blocked_reason": None},
            {"object_kind": "profile", "object_key": "profile:medical_appointment_standard", "classification": "drifted", "desired": profile, "observed": old_profile, "blocked_reason": None},
            {"object_kind": "binding", "object_key": "binding:lesson", "classification": "equivalent", "desired": equivalent_lesson_binding, "observed": equivalent_lesson_binding, "blocked_reason": None},
            {"object_kind": "binding", "object_key": "binding:medical_appointment", "classification": "missing", "desired": binding, "observed": None, "blocked_reason": None},
        ],
        "actions": [
            {
                "ordinal": "0",
                "action_id": "action-000000",
                "command": "notification_profile.revise",
                "object_key": "profile:medical_appointment_standard",
                "change_kind": "update",
                "desired": profile,
                "expected": old_profile,
                "request_template": canonical_value(
                    "spine.notification-profiles.v1",
                    {
                        "contract_version": "spine.notification-profiles.v1",
                        "expected_current_revision_id": "profile_revision_old",
                        "notification_profile_id": "profile_medical",
                        "revision": json.loads(profile["canonical_json"])["revision"],
                    },
                    "profileReviseTemplate",
                ),
            },
            {
                "ordinal": "1",
                "action_id": "action-000001",
                "command": "notification_profile.binding.set",
                "object_key": "binding:medical_appointment",
                "change_kind": "create",
                "desired": binding,
                "expected": None,
                "request_template": canonical_value(
                    "spine.notification-profile-bindings.v1",
                    {
                        "contract_version": "spine.notification-profile-bindings.v1",
                        "item_archetype_id": "archetype_medical",
                        "notification_profile_id": "profile_medical",
                        "owner": {
                            "owner_kind": "subject",
                            "owner_subject_id": "subject_caleb",
                        },
                    },
                    "bindingSetTemplate",
                ),
            },
        ],
        "decision_action_ids": ["action-000000"],
        "blocked_object_keys": [],
        "apply_eligible": not draft,
    }
    identities = [
        {"catalog_id": "archetype_lesson"},
        {"catalog_id": "archetype_medical"},
        {"catalog_id": "profile_lesson"},
        {"catalog_id": "profile_medical"},
        {
            "item_archetype_id": "archetype_lesson",
            "notification_profile_id": "profile_lesson",
            "observed_binding": {
                "notification_profile_binding_id": "binding_lesson",
                "item_archetype_id": "archetype_lesson",
                "notification_profile_id": "profile_lesson",
            },
        },
        {
            "item_archetype_id": "archetype_medical",
            "notification_profile_id": "profile_medical",
            "observed_binding": None,
        },
    ]
    for entry, identity in zip(plan["classifications"], identities):
        entry["identity"] = identity
    return seal(plan)


def make_create_plan(request: dict[str, Any]) -> dict[str, Any]:
    candidate = make_plan(request)
    archetype, profile, binding = [candidate["classifications"][i] for i in (0, 2, 4)]
    for root in (archetype, profile):
        root.update(classification="missing", observed=None, identity=None)
    binding.update(classification="missing", observed=None, identity={
        "item_archetype_id": None, "notification_profile_id": None, "observed_binding": None,
    })
    metadata = json.loads(profile["desired"]["canonical_json"])
    owner = candidate["request"]["owner"]
    creates = []
    for entry, command, contract, shape, body in (
        (archetype, "item_archetype.create", "spine.item-archetypes.v1", "archetypeCreateTemplate", {
            "archetype_key": "lesson", "revision": json.loads(archetype["desired"]["canonical_json"]),
        }),
        (profile, "notification_profile.create", "spine.notification-profiles.v1", "profileCreateTemplate", {
            "profile_key": "lesson_standard", **metadata["metadata"], "revision": metadata["revision"],
        }),
    ):
        creates.append({
            "command": command, "object_key": entry["object_key"], "change_kind": "create",
            "desired": entry["desired"], "expected": None,
            "request_template": canonical_value(contract, {"contract_version": contract, "owner": owner, **body}, shape),
        })
    binding_action = {
        "command": "notification_profile.binding.set", "object_key": binding["object_key"],
        "change_kind": "create", "desired": binding["desired"], "expected": None,
        "request_template": canonical_value("spine.notification-profile-bindings.v1", {
            "contract_version": "spine.notification-profile-bindings.v1", "owner": owner,
            "item_archetype_id": "${spine-pack.result:action-000000:item_archetype_id}",
            "notification_profile_id": "${spine-pack.result:action-000001:notification_profile_id}",
        }, "bindingSetTemplate"),
    }
    candidate["actions"] = [*creates, candidate["actions"][0], binding_action, candidate["actions"][1]]
    for index, action in enumerate(candidate["actions"]):
        action.update(ordinal=str(index), action_id=f"action-{index:06d}")
    candidate["decision_action_ids"] = ["action-000002"]
    return seal(candidate)


def make_approval(plan: dict[str, Any]) -> dict[str, Any]:
    return seal(
        {
            "artifact_schema": "spine.pack-install-approval.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approve_complete_plan": True,
            "acknowledge_single_operator": True,
            "authorized_update_action_ids": plan["decision_action_ids"],
            "execution": {
                "execution_id": "123e4567-e89b-42d3-a456-426614174000",
                "actor_subject_id": "subject_caleb",
                "action_timestamp_utc": "2026-09-09T08:00:00Z",
            },
        }
    )


def _materialized_request(
    plan: dict[str, Any], approval: dict[str, Any], index: int,
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    errors = plan_errors(plan) + approval_errors(approval, plan)
    if errors:
        raise ValueError("result_reference_invalid_plan_or_approval")
    action = plan["actions"][index]
    value = json.loads(action["request_template"]["canonical_json"])
    execution = approval["execution"]
    responses = accepted_responses if accepted_responses is not None else []
    slots = _reference_slots(value)
    if len(responses) > index or (slots and len(responses) != index):
        raise ValueError("result_reference_response_missing")
    errors = _response_prefix_errors(responses, plan, execution)
    if errors:
        raise ValueError("result_reference_response_invalid")
    for path, text in slots:
        producer_id, field = RESULT_REFERENCE.fullmatch(text).groups()
        producer = next((r for r in responses if r["action_id"] == producer_id), None)
        if producer is None:
            raise ValueError("result_reference_response_missing")
        # The exact field and the response are already contextually validated.
        value[path[0]] = json.loads(producer["response"]["canonical_json"])[field]
    value.update(
        {
            "command_id": command_id(
                plan["content_identity"]["digest"],
                execution["execution_id"],
                action["action_id"],
            ),
            "actor_subject_id": execution["actor_subject_id"],
            "action_timestamp_utc": execution["action_timestamp_utc"],
        }
    )
    prefix, contract = COMMAND_SHAPES[action["command"]]
    if canonical_value_errors(canonical_value(contract, value, prefix + "Request"), prefix + "Request"):
        raise ValueError("materialized_request_invalid")
    return value


def make_checkpoint(
    plan: dict[str, Any], approval: dict[str, Any],
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    responses = accepted_responses if accepted_responses is not None else []
    index = len(responses)
    action = plan["actions"][index]
    prefix, contract = COMMAND_SHAPES[action["command"]]
    request = _materialized_request(plan, approval, index, responses)
    return seal(
        {
            "artifact_schema": "spine.pack-apply-checkpoint.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approval_digest": approval["content_identity"]["digest"],
            "execution": approval["execution"],
            "accepted_responses": deepcopy(responses),
            "unresolved_submission": {
                "action_id": action["action_id"],
                "command_id": request["command_id"],
                "submission_state": "prepared_or_submitted",
                "request": canonical_value(contract, request, prefix + "Request"),
            },
            "next_action_id": action["action_id"],
        }
    )


def _response(
    plan: dict[str, Any], approval: dict[str, Any], index: int, *, replay: bool = False,
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    action = plan["actions"][index]
    cmd_id = command_id(
        plan["content_identity"]["digest"],
        approval["execution"]["execution_id"],
        action["action_id"],
    )
    contract = COMMAND_SHAPES[action["command"]][1]
    request = _materialized_request(plan, approval, index, accepted_responses)
    if action["command"] == "item_archetype.create":
        facts = {
            "item_archetype_id": "created_archetype_" + request["archetype_key"],
            "item_archetype_revision_id": "created_archetype_revision_" + request["archetype_key"],
            "archetype_key": request["archetype_key"], "revision_number": "1", "status": "active",
        }
        effect = "item_archetype_created"
    elif action["command"] == "notification_profile.create":
        facts = {
            "notification_profile_id": "created_profile_" + request["profile_key"],
            "notification_profile_revision_id": "created_profile_revision_" + request["profile_key"],
            "profile_key": request["profile_key"], "revision_number": "1",
            "normalized_revision_hash": "b" * 64, "status": "active",
        }
        effect = "notification_profile_created"
    elif action["command"] == "notification_profile.revise":
        facts = {
        "notification_profile_id": "profile_medical",
        "notification_profile_revision_id": "profile_revision_new",
        "revision_number": "2",
        "normalized_revision_hash": "b" * 64,
        "status": "active",
        }
        effect = "notification_profile_revised"
    elif action["command"] == "notification_profile.binding.set":
        facts = {
        "notification_profile_binding_id": "binding_lesson" if action["object_key"] == "binding:lesson" else "binding_medical",
        "item_archetype_id": request["item_archetype_id"],
        "notification_profile_id": request["notification_profile_id"],
        "status": "active",
        "compatible_item_types": ["event"],
        }
        effect = "notification_profile_binding_set"
    else:
        raise ValueError("fixture_response_command_unsupported")
    generated = [
        {"name": key, "value": facts[key]}
        for key in sorted(facts) if key.endswith("_id")
    ]
    receipt_id = f"receipt_{index}"
    semantic_hash = str(index + 5) * 64
    response_value = {
        "command": action["command"],
        "effect": effect,
        **facts,
        "ok": True,
        "receipt": {
            "command_id": cmd_id,
            "command_receipt_id": receipt_id,
            "created_at_utc": approval["execution"]["action_timestamp_utc"],
            "effect": effect,
            "semantic_facts_hash": semantic_hash,
        },
        "response_contract": contract,
    }
    return {
        "action_id": action["action_id"],
        "command": action["command"],
        "command_id": cmd_id,
        "outcome": "compatible_replay" if replay else "accepted",
        "response_contract": contract,
        "effect": effect,
        "generated_ids": generated,
        "command_receipt_id": receipt_id,
        "semantic_facts_hash": semantic_hash,
        "response": canonical_value(
            contract, response_value, COMMAND_SHAPES[action["command"]][0] + "Response"
        ),
    }


def make_apply_result(
    plan: dict[str, Any], approval: dict[str, Any], *, partial: bool = False
) -> dict[str, Any]:
    accepted = [_response(plan, approval, 0, replay=True)]
    if not partial:
        accepted.append(_response(plan, approval, 1))
    failure = None
    if partial:
        failure = {
            "action_id": "action-000001",
            "error": {
                "category": "spine_command_rejection",
                "code": "binding_rejected",
                "message": "Spine rejected the binding command.",
                "facts": [{"name": "command", "value": "notification_profile.binding.set"}],
            },
        }
    return seal(
        {
            "artifact_schema": "spine.pack-apply-result.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approval_digest": approval["content_identity"]["digest"],
            "execution": approval["execution"],
            "state": "partial" if partial else "applied",
            "accepted_responses": accepted,
            "failure": failure,
            "unattempted_action_ids": [],
        }
    )


def make_verification(
    plan: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    object_results = [
        {
            "object_kind": entry["object_kind"],
            "object_key": entry["object_key"],
            "state": "equivalent",
            "observed": entry["desired"],
        }
        for entry in plan["classifications"]
    ]
    return seal(
        {
            "artifact_schema": "spine.pack-verification-result.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "apply_result_digest": result["content_identity"]["digest"],
            "pack": plan["pack"],
            "target": plan["request"]["target"],
            "environment": plan["environment"],
            "catalog_snapshots": [
                {"catalog": "archetypes", "digest": "7" * 64},
                {"catalog": "profiles", "digest": "8" * 64},
                {"catalog": "bindings", "digest": "9" * 64},
            ],
            "closure": plan["closure"],
            "object_results": object_results,
            "response_evidence": "complete",
            "receipt_readback": "captured_responses_only_spine_0.3.0",
            "state": "verified",
        }
    )


def make_create_flow() -> dict[str, Any]:
    """Synthetic command evidence only; never contacts or mutates Spine."""
    request = _fixture_request()
    plan = make_create_plan(request)
    approval = make_approval(plan)
    responses = []
    binding_checkpoint = None
    for index in range(len(plan["actions"])):
        if index == 3:
            binding_checkpoint = make_checkpoint(plan, approval, responses)
        responses.append(_response(plan, approval, index, accepted_responses=responses))
    applied = seal({
        "artifact_schema": "spine.pack-apply-result.v1",
        "plan_digest": plan["content_identity"]["digest"],
        "approval_digest": approval["content_identity"]["digest"],
        "execution": approval["execution"], "state": "applied",
        "accepted_responses": responses, "failure": None, "unattempted_action_ids": [],
    })
    return {
        "fixture_contract": "spine.pack-installer-create-flow.v1",
        "request": request, "plan": plan, "approval": approval,
        "binding_checkpoint": binding_checkpoint, "applied_result": applied,
    }


def make_envelope(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_schema": "spine.pack-installer-result.v1",
        "operation": "apply",
        "status": "success",
        "exit_code": "0",
        "artifact": {
            "path": "/tmp/apply-result.json",
            "digest": result["content_identity"]["digest"],
        },
        "error": None,
    }


class InstallerArtifactContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = _fixture_request()
        self.plan = make_plan(self.request)
        self.approval = make_approval(self.plan)
        self.checkpoint = make_checkpoint(self.plan, self.approval)
        self.applied = make_apply_result(self.plan, self.approval)
        self.partial = make_apply_result(self.plan, self.approval, partial=True)
        self.verification = make_verification(self.plan, self.applied)
        self.envelope = make_envelope(self.applied)

    def test_schema_entrypoints_are_draft_2020_12(self) -> None:
        for filename in ENTRYPOINTS.values():
            schema = _schema_document(SCHEMA_ROOT / filename)
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertIn("$ref", schema)

    def test_drift_eligibility_does_not_depend_on_approval(self) -> None:
        # A reviewable released drift plan is technically eligible before an
        # approval exists. Approval authorizes its exact immutable digest.
        plan = make_plan(self.request)
        before = deepcopy(plan)
        self.assertTrue(plan["decision_action_ids"])
        self.assertTrue(plan["apply_eligible"])
        self.assertEqual(plan_errors(plan), [])

        approval = make_approval(plan)
        self.assertEqual(approval_errors(approval, plan), [])
        self.assertEqual(approval["plan_digest"], before["content_identity"]["digest"])

        unauthorized = deepcopy(approval)
        unauthorized["authorized_update_action_ids"] = []
        unauthorized = seal(unauthorized)
        self.assertIn("update_authorization_incomplete", approval_errors(unauthorized, plan))
        self.assertEqual(plan, before)

        envelope = {
            "artifact_schema": "spine.pack-installer-result.v1",
            "operation": "plan",
            "status": "decision_required",
            "exit_code": "5",
            "artifact": {
                "path": "/operator/review/plan.json",
                "digest": plan["content_identity"]["digest"],
            },
            "error": {
                "category": "decision_required_for_drift",
                "code": "update_approval_required",
                "message": "The plan requires explicit update approval.",
                "facts": [],
            },
        }
        self.assertEqual(envelope_errors(envelope), [])

    def test_installer_prose_separates_eligibility_and_authorization(self) -> None:
        prose = (ROOT / "specs/installer.md").read_text(encoding="utf-8")
        self.assertIn("Eligibility is not execution authorization.", prose)
        self.assertIn("Approval MUST NOT change `apply_eligible` or the plan digest.", prose)
        self.assertNotIn("it is ineligible until every proposed update", prose)

    def test_embedded_schema_uses_only_supported_validation_keywords(self) -> None:
        supported = {
            "$schema", "$id", "$comment", "title", "$defs", "$ref", "type",
            "required", "properties", "additionalProperties", "const", "enum",
            "minLength", "maxLength", "pattern", "minItems", "maxItems",
            "uniqueItems", "items", "oneOf", "anyOf", "allOf", "not", "if",
            "then", "else",
        }
        def visit(node):
            self.assertFalse(set(node) - supported, set(node) - supported)
            for key in ("$defs", "properties"):
                for child in node.get(key, {}).values():
                    visit(child)
            for key in ("oneOf", "anyOf", "allOf"):
                for child in node.get(key, []):
                    visit(child)
            for key in ("items", "not", "if", "then", "else"):
                if key in node:
                    visit(node[key])
        visit(_schema_document(EMBEDDED_SCHEMA))

    def test_materialized_requests_require_execution_identity(self) -> None:
        for index, action in enumerate(self.plan["actions"]):
            with self.subTest(command=action["command"]):
                prefix, contract = COMMAND_SHAPES[action["command"]]
                request = _materialized_request(self.plan, self.approval, index)
                self.assertEqual(canonical_value_errors(
                    canonical_value(contract, request, prefix + "Request"), prefix + "Request"
                ), [])
                del request["command_id"]
                self.assertIn("embedded_contract_invalid", canonical_value_errors(
                    canonical_value(contract, request, prefix + "Request"), prefix + "Request"
                ))

    def test_positive_artifact_family(self) -> None:
        self.assertEqual(request_errors(self.request), [])
        self.assertEqual(plan_errors(self.plan), [])
        self.assertEqual(approval_errors(self.approval, self.plan), [])
        self.assertEqual(checkpoint_errors(self.checkpoint, self.plan, self.approval), [])
        self.assertEqual(apply_result_errors(self.applied, self.plan, self.approval), [])
        self.assertEqual(apply_result_errors(self.partial, self.plan, self.approval), [])
        self.assertEqual(verification_errors(self.verification, self.plan, self.applied), [])
        self.assertEqual(envelope_errors(self.envelope), [])
        for artifact in (
            self.request,
            self.plan,
            self.approval,
            self.checkpoint,
            self.applied,
            self.partial,
            self.verification,
            self.envelope,
        ):
            self.assertEqual(artifact_size_errors(artifact), [])

    def test_static_artifact_suite_matches_and_validates(self) -> None:
        suite = load_json(POSITIVE_ROOT / "profile_drift_artifact_suite.json")
        expected = {
            "fixture_contract": "spine.pack-installer-artifact-suite.v1",
            "request": self.request,
            "plan": self.plan,
            "approval": self.approval,
            "uncertain_checkpoint": self.checkpoint,
            "applied_result": self.applied,
            "partial_result": self.partial,
            "verification": self.verification,
            "success_envelope": self.envelope,
        }
        self.assertEqual(suite, expected)
        self.assertEqual(request_errors(suite["request"]), [])
        self.assertEqual(plan_errors(suite["plan"]), [])
        self.assertEqual(approval_errors(suite["approval"], suite["plan"]), [])
        self.assertEqual(
            checkpoint_errors(
                suite["uncertain_checkpoint"], suite["plan"], suite["approval"]
            ),
            [],
        )
        self.assertEqual(
            apply_result_errors(
                suite["partial_result"], suite["plan"], suite["approval"]
            ),
            [],
        )

    def test_scenario_fixture_describes_generated_flow(self) -> None:
        vector = load_json(POSITIVE_ROOT / "profile_drift_vertical_flow.json")
        actual = [
            f"{entry['object_key']}={entry['classification']}"
            for entry in self.plan["classifications"]
        ]
        self.assertEqual(self.plan["closure"], vector["expected_closure"])
        self.assertEqual(actual, vector["expected_classifications"])
        self.assertEqual(
            [entry["command"] for entry in self.plan["actions"]],
            vector["expected_actions"],
        )
        self.assertEqual(self.plan["decision_action_ids"], vector["expected_decision_action_ids"])
        self.assertEqual([self.applied["state"], self.partial["state"]], vector["expected_terminal_states"])
        self.assertEqual(self.verification["state"], vector["expected_verification_state"])

    def test_negative_fixture_manifest_is_complete_and_sorted(self) -> None:
        fixture_manifest = load_json(FIXTURE_MANIFEST)
        for group in ("positive", "negative"):
            self.assertEqual(fixture_manifest[group], sorted(fixture_manifest[group]))
            for relative in fixture_manifest[group]:
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_negative_semantic_vectors(self) -> None:
        expected_files = {
            "apply_target_mismatch.json": "target_binding_mismatch",
            "draft_apply_eligible.json": "draft_plan_apply_eligible",
            "incorrect_artifact_digest.json": "content_digest_mismatch",
            "noncontiguous_partial_apply.json": "accepted_prefix_not_contiguous",
            "stale_catalog_snapshot.json": "stale_plan_catalog_snapshot",
            "stale_plan_approval.json": "approval_plan_digest_mismatch",
            "target_mismatch.json": "target_binding_mismatch",
            "unauthorized_drift.json": "update_authorization_incomplete",
            "uncertain_replay_command_mismatch.json": "command_id_mismatch",
            "unsorted_selection.json": "selection_not_sorted",
        }
        self.assertEqual(
            [path.name for path in sorted(NEGATIVE_ROOT.glob("*.json"))],
            sorted([*expected_files, "embedded_contract_violations.json",
                    "selection_assertion_mismatch.json", "binding_identity_mismatch.json",
                    "invalid_result_references.json"]),
        )
        for filename, expected in expected_files.items():
            vector = load_json(NEGATIVE_ROOT / filename)
            self.assertEqual(vector["expected_error"], expected)
            with self.subTest(filename=filename):
                if filename == "draft_apply_eligible.json":
                    draft_request = deepcopy(self.request)
                    draft_request["request"]["draft_posture"] = "inspect_only"
                    draft_request = seal(draft_request)
                    candidate = make_plan(draft_request, draft=True)
                    candidate["apply_eligible"] = True
                    candidate = seal(candidate)
                    errors = plan_errors(candidate)
                elif filename == "incorrect_artifact_digest.json":
                    candidate = deepcopy(self.request)
                    candidate["content_identity"]["digest"] = "0" * 64
                    errors = request_errors(candidate)
                elif filename == "noncontiguous_partial_apply.json":
                    candidate = deepcopy(self.partial)
                    candidate["accepted_responses"] = [_response(self.plan, self.approval, 1)]
                    candidate = seal(candidate)
                    errors = apply_result_errors(candidate, self.plan, self.approval)
                elif filename == "stale_catalog_snapshot.json":
                    snapshots = deepcopy(self.plan["catalog_snapshots"])
                    snapshots[1]["digest"] = "f" * 64
                    errors = apply_preflight_errors(
                        self.plan,
                        self.plan["request"]["target"],
                        self.plan["environment"],
                        snapshots,
                    )
                elif filename == "stale_plan_approval.json":
                    candidate = deepcopy(self.approval)
                    candidate["plan_digest"] = "f" * 64
                    candidate = seal(candidate)
                    errors = approval_errors(candidate, self.plan)
                elif filename == "target_mismatch.json":
                    candidate = deepcopy(self.verification)
                    candidate["target"]["host_name"] = "other.local"
                    errors = verification_errors(seal(candidate), self.plan, self.applied)
                elif filename == "apply_target_mismatch.json":
                    target = deepcopy(self.plan["request"]["target"])
                    target["host_name"] = "other.local"
                    errors = apply_preflight_errors(
                        self.plan, target, self.plan["environment"], self.plan["catalog_snapshots"]
                    )
                elif filename == "unauthorized_drift.json":
                    candidate = deepcopy(self.approval)
                    candidate["authorized_update_action_ids"] = []
                    candidate = seal(candidate)
                    errors = approval_errors(candidate, self.plan)
                elif filename == "uncertain_replay_command_mismatch.json":
                    candidate = deepcopy(self.checkpoint)
                    candidate["unresolved_submission"]["command_id"] = "spack_" + "f" * 64
                    candidate = seal(candidate)
                    errors = checkpoint_errors(candidate, self.plan, self.approval)
                else:
                    candidate = deepcopy(self.request)
                    candidate["request"]["selection"]["archetype_keys"].reverse()
                    candidate = seal(candidate)
                    errors = request_errors(candidate)
                self.assertIn(expected, errors)

    def test_unknown_fields_fail_closed(self) -> None:
        candidate = deepcopy(self.approval)
        candidate["allow_updates"] = True
        self.assertTrue(any("unknown" in error for error in validate_schema(candidate)))

    def test_embedded_contracts_reject_validly_hashed_bad_content(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "embedded_contract_violations.json")
        validators = {
            "plan": plan_errors,
            "checkpoint": lambda a: checkpoint_errors(a, self.plan, self.approval),
            "applied": lambda a: apply_result_errors(a, self.plan, self.approval),
            "verification": lambda a: verification_errors(a, self.plan, self.applied),
        }
        for case in vector["cases"]:
            with self.subTest(case=case):
                artifact = deepcopy(getattr(self, case["artifact"]))
                wrapper = artifact
                for token in case["path"]:
                    wrapper = wrapper[int(token)] if isinstance(wrapper, list) else wrapper[token]
                parsed = json.loads(wrapper["canonical_json"])
                parent = parsed
                for token in case["remove"][:-1]:
                    parent = parent[token]
                del parent[case["remove"][-1]]
                wrapper.update(canonical_value(wrapper["contract"], parsed, wrapper["shape"]))
                artifact = seal(artifact)
                self.assertEqual(content_digest_errors(artifact), [])
                self.assertIn(vector["expected_error"], validators[case["artifact"]](artifact))

    def test_contract_and_context_cannot_be_spoofed(self) -> None:
        candidate = deepcopy(self.plan)
        candidate["classifications"][0]["desired"]["contract"] = "spine.unknown.v1"
        self.assertIn("embedded_contract_or_shape_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["actions"][0]["request_template"] = candidate["actions"][0]["desired"]
        self.assertIn("embedded_context_shape_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.applied)
        candidate["accepted_responses"][0]["effect"] = "fabricated"
        self.assertIn("response_evidence_mismatch",
                      apply_result_errors(seal(candidate), self.plan, self.approval))

    def test_request_selection_is_authoritative(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "selection_assertion_mismatch.json")
        self.assertIn(vector["expected_error"], selection_assertion_errors(
            self.request, all_flag=vector["all_flag"]
        ))
        self.assertEqual(selection_assertion_errors(self.request), [])
        self.assertEqual(selection_assertion_errors(
            self.request, archetype_flags=["medical_appointment", "lesson", "lesson"]
        ), [])
        self.assertEqual(selection_assertion_errors(
            self.request, all_flag=True, archetype_flags=["lesson"]
        ), ["selection_flags_conflict"])
        full = deepcopy(self.request)
        full["request"]["selection"] = {"mode": "all"}
        full = seal(full)
        self.assertEqual(selection_assertion_errors(full, all_flag=True), [])
        self.assertEqual(selection_assertion_errors(full, archetype_flags=[]), ["selection_flags_empty"])

    def test_metadata_and_behavior_comparisons_are_independent(self) -> None:
        original = self.plan["classifications"][2]["observed"]
        for section, field, replacement in (
            ("metadata", "description", "Different presentation"),
            ("revision", "compatible_item_types", ["event", "task"]),
        ):
            with self.subTest(section=section):
                candidate = deepcopy(self.plan)
                parsed = json.loads(original["canonical_json"])
                parsed[section][field] = replacement
                candidate["classifications"][2]["observed"] = canonical_value(
                    original["contract"], parsed, original["shape"]
                )
                self.assertIn("equivalence_preimage_mismatch", plan_errors(seal(candidate)))

    def test_binding_identity_vectors(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "binding_identity_mismatch.json")
        for mutation in vector["mutations"]:
            with self.subTest(path=mutation["path"]):
                candidate = deepcopy(self.plan)
                target = candidate
                for part in mutation["path"][:-1]:
                    target = target[int(part)] if isinstance(target, list) else target[part]
                target[mutation["path"][-1]] = mutation["value"]
                candidate = seal(candidate)
                self.assertEqual(validate_schema(candidate), [])
                self.assertEqual(content_digest_errors(candidate), [])
                self.assertIn(mutation["expected_error"], plan_errors(candidate))

    def test_binding_identity_closure_and_state(self) -> None:
        for index in range(len(self.plan["classifications"])):
            candidate = deepcopy(self.plan)
            del candidate["classifications"][index]["identity"]
            self.assertTrue(validate_schema(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][4]["identity"]["unexpected"] = "extra"
        self.assertTrue(validate_schema(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][4]["identity"]["observed_binding"] = None
        self.assertIn("binding_observation_state_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][0]["identity"] = None
        self.assertIn("catalog_identity_state_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        binding = candidate["classifications"][4]
        binding.update(classification="blocked", observed=None, identity=None, blocked_reason="ambiguous_readback")
        candidate["blocked_object_keys"] = [binding["object_key"]]
        candidate["apply_eligible"] = False
        self.assertEqual(plan_errors(seal(candidate)), [])

    def test_binding_requests_match_resolved_identity_and_owner(self) -> None:
        for field, value, expected in (
            ("item_archetype_id", "wrong_archetype", "binding_action_identity_mismatch"),
            ("notification_profile_id", "wrong_profile", "binding_action_identity_mismatch"),
            ("owner", {"owner_kind": "subject", "owner_subject_id": "other_owner"}, "binding_action_owner_mismatch"),
        ):
            candidate = deepcopy(self.plan)
            action = candidate["actions"][1]
            request = json.loads(action["request_template"]["canonical_json"])
            request[field] = value
            action["request_template"] = canonical_value(
                "spine.notification-profile-bindings.v1", request, "bindingSetTemplate"
            )
            self.assertIn(expected, plan_errors(seal(candidate)))

    def test_binding_drift_requires_different_observed_profile_id(self) -> None:
        candidate = deepcopy(self.plan)
        binding = candidate["classifications"][4]
        binding["classification"] = "drifted"
        binding["observed"] = canonical_value("spine.notification-profile-bindings.v1", {
            "binding_kind": "archetype_default", "notification_profile_key": "medical_appointment_standard",
        })
        binding["identity"]["observed_binding"]["notification_profile_id"] = "profile_medical"
        candidate["actions"].insert(1, {
            "command": "notification_profile.binding.set", "object_key": binding["object_key"],
            "change_kind": "update", "desired": binding["desired"], "expected": binding["observed"],
            "request_template": canonical_value("spine.notification-profile-bindings.v1", {
                "contract_version": "spine.notification-profile-bindings.v1",
                "owner": candidate["request"]["owner"],
                "item_archetype_id": "archetype_lesson", "notification_profile_id": "profile_lesson",
            }, "bindingSetTemplate"),
        })
        for index, action in enumerate(candidate["actions"]):
            action.update(ordinal=str(index), action_id=f"action-{index:06d}")
        candidate["decision_action_ids"] = ["action-000000", "action-000001"]
        self.assertEqual(plan_errors(seal(candidate)), [])
        binding["identity"]["observed_binding"]["notification_profile_id"] = "profile_lesson"
        self.assertIn("binding_profile_identity_mismatch", plan_errors(seal(candidate)))

    def test_binding_missing_dependencies_use_create_result_references(self) -> None:
        candidate = make_create_plan(self.request)
        self.assertEqual(plan_errors(candidate), [])
        binding_action = candidate["actions"][3]
        body = json.loads(binding_action["request_template"]["canonical_json"])
        body["notification_profile_id"] = "guessed_profile_id"
        binding_action["request_template"] = canonical_value(
            "spine.notification-profile-bindings.v1", body, "bindingSetTemplate"
        )
        self.assertIn("binding_action_identity_mismatch", plan_errors(seal(candidate)))

    def test_archetype_source_provenance_is_explicit(self) -> None:
        source = _schema_document(EMBEDDED_SCHEMA)["$comment"]
        for reference in (
            "notification-profile-types.schema.json#/$defs/archetypeRevision",
            "notification-profile-commands.schema.json#/$defs/archetypeCreate",
            "#/$defs/archetypeRevise", "src/spine/commands/notification_profiles.py",
            "_archetype_create", "_archetype_revise", "72203f092de191a7633b1884bf0d61836a25abe4",
        ):
            self.assertIn(reference, source)

    def test_create_flow_materializes_and_replays_binding_checkpoint(self) -> None:
        flow = make_create_flow()
        self.assertEqual(flow, load_json(POSITIVE_ROOT / "create_binding_artifact_suite.json"))
        plan, approval = flow["plan"], flow["approval"]
        checkpoint = flow["binding_checkpoint"]
        self.assertEqual(plan_errors(plan), [])
        self.assertEqual(approval_errors(approval, plan), [])
        self.assertEqual(checkpoint_errors(checkpoint, plan, approval), [])
        self.assertEqual(apply_result_errors(flow["applied_result"], plan, approval), [])
        request = json.loads(checkpoint["unresolved_submission"]["request"]["canonical_json"])
        self.assertEqual(request["item_archetype_id"], "created_archetype_lesson")
        self.assertEqual(request["notification_profile_id"], "created_profile_lesson_standard")
        self.assertEqual(_reference_slots(request), [])
        # Compatible replay must produce exactly the same request bytes/command ID.
        replayed = deepcopy(checkpoint["accepted_responses"])
        for response in replayed:
            response["outcome"] = "compatible_replay"
        self.assertEqual(canonical_text(_materialized_request(plan, approval, 3, replayed)),
                         checkpoint["unresolved_submission"]["request"]["canonical_json"])
        candidate = deepcopy(checkpoint)
        unresolved = candidate["unresolved_submission"]["request"]
        vector = load_json(NEGATIVE_ROOT / "invalid_result_references.json")["unresolved_request"]
        request[vector["field"]] = vector["value"]
        candidate["unresolved_submission"]["request"] = canonical_value(
            unresolved["contract"], request, unresolved["shape"]
        )
        self.assertIn(vector["expected_error"], checkpoint_errors(seal(candidate), plan, approval))

    def test_invalid_result_reference_vectors(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "invalid_result_references.json")
        for mutation in vector["mutations"]:
            with self.subTest(case=mutation["case"]):
                plan = make_create_plan(self.request)
                action = plan["actions"][int(mutation["action_index"])]
                template = action["request_template"]
                value = json.loads(template["canonical_json"])
                target = value
                for key in mutation["path"][:-1]:
                    target = target[key]
                target[mutation["path"][-1]] = mutation["value"]
                action["request_template"] = canonical_value(template["contract"], value, template["shape"])
                plan = seal(plan)
                self.assertEqual(validate_schema(plan), [])
                self.assertEqual(content_digest_errors(plan), [])
                self.assertIn(mutation["expected_error"], plan_errors(plan))
                with self.assertRaisesRegex(ValueError, "invalid_plan_or_approval"):
                    _materialized_request(plan, make_approval(plan), int(mutation["action_index"]))

    def test_reference_materialization_rejects_bad_producer_evidence(self) -> None:
        flow = make_create_flow()
        plan, approval = flow["plan"], flow["approval"]
        prefix = flow["binding_checkpoint"]["accepted_responses"]
        for responses in ([], prefix[:1], prefix[:2]):
            with self.assertRaisesRegex(ValueError, "result_reference_response_missing"):
                _materialized_request(plan, approval, 3, responses)
        for field, value in (
            ("command_id", "wrong_command"), ("outcome", "rejected"),
            ("generated_ids", []), ("command_receipt_id", "wrong_receipt"),
        ):
            responses = deepcopy(prefix)
            responses[0][field] = value
            with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
                _materialized_request(plan, approval, 3, responses)
        for field, value in (
            ("archetype_key", "another_key"),
            ("item_archetype_id", "${spine-pack.result:action-000001:notification_profile_id}"),
        ):
            responses = deepcopy(prefix)
            embedded = responses[0]["response"]
            body = json.loads(embedded["canonical_json"])
            body[field] = value
            responses[0]["response"] = canonical_value(embedded["contract"], body, embedded["shape"])
            responses[0]["generated_ids"] = [
                {"name": key, "value": body[key]} for key in sorted(body) if key.endswith("_id")
            ]
            with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
                _materialized_request(plan, approval, 3, responses)
        responses = deepcopy(prefix)
        responses[0], responses[1] = responses[1], responses[0]
        with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
            _materialized_request(plan, approval, 3, responses)

    def test_reference_scan_covers_all_commands_and_nested_members(self) -> None:
        reference = "${spine-pack.result:action-000000:item_archetype_id}"
        for prefix, contract in COMMAND_SHAPES.values():
            for suffix in ("Template", "Request", "Response"):
                with self.subTest(shape=prefix + suffix):
                    self.assertIn("result_reference_context_forbidden", result_reference_errors(
                        {"owner": {"owner_subject_id": reference}}, prefix + suffix
                    ))
                    self.assertTrue(result_reference_errors({reference: "value"}, prefix + suffix))
        self.assertIn("result_reference_syntax_invalid", result_reference_errors(
            {"item_archetype_id": "prefix" + reference}, "bindingSetTemplate"
        ))

    def test_command_identity_changes_with_plan_execution_or_action(self) -> None:
        plan_digest = self.plan["content_identity"]["digest"]
        execution_id = self.approval["execution"]["execution_id"]
        baseline = command_id(plan_digest, execution_id, "action-000000")
        self.assertNotEqual(baseline, command_id("f" * 64, execution_id, "action-000000"))
        self.assertNotEqual(
            baseline,
            command_id(plan_digest, "223e4567-e89b-42d3-a456-426614174000", "action-000000"),
        )
        self.assertNotEqual(baseline, command_id(plan_digest, execution_id, "action-000001"))


if __name__ == "__main__":
    unittest.main()
