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


def canonical_value(contract: str, value: Any) -> dict[str, Any]:
    text = canonical_text(value)
    return {
        "contract": contract,
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


def canonical_value_errors(value: dict[str, Any]) -> list[str]:
    try:
        parsed = json.loads(value["canonical_json"], object_pairs_hook=_closed_object)
        canonical = canonical_text(parsed)
    except (ValueError, TypeError, json.JSONDecodeError, DuplicateObjectMember):
        return ["canonical_value_invalid"]
    if canonical != value["canonical_json"]:
        return ["canonical_value_not_canonical"]
    actual = hashlib.sha256(value["canonical_json"].encode("utf-8")).hexdigest()
    return [] if actual == value["digest"] else ["canonical_value_digest_mismatch"]


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


def plan_errors(plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(plan) + content_digest_errors(plan)
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
        errors.extend(canonical_value_errors(classification["desired"]))
        if observed is not None:
            errors.extend(canonical_value_errors(observed))
    class_rank = {"archetype": 0, "profile": 1, "binding": 2}
    classification_order = [
        (class_rank[entry["object_kind"]], entry["object_key"])
        for entry in plan["classifications"]
    ]
    if classification_order != sorted(classification_order):
        errors.append("classification_order")
    for action in plan["actions"]:
        errors.extend(canonical_value_errors(action["desired"]))
        errors.extend(canonical_value_errors(action["request_template"]))
        if action["expected"] is not None:
            errors.extend(canonical_value_errors(action["expected"]))
        if action["change_kind"] == "create" and action["expected"] is not None:
            errors.append("create_has_expected")
        if action["change_kind"] == "update" and action["expected"] is None:
            errors.append("update_without_expected")
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
        errors.extend(canonical_value_errors(response["response"]))
        names = [item["name"] for item in response["generated_ids"]]
        if not _sorted_unique(names):
            errors.append("generated_ids_not_sorted")
    return errors


def checkpoint_errors(
    checkpoint: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = validate_schema(checkpoint) + content_digest_errors(checkpoint)
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
        errors.extend(canonical_value_errors(unresolved["request"]))
    return errors


def apply_result_errors(
    result: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = validate_schema(result) + content_digest_errors(result)
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
    old_profile = canonical_value(
        "spine.notification-profiles.v1",
        {"compatible_item_types": ["event"], "templates": []},
    )
    equivalent_lesson = canonical_value("spine.item-archetypes.v1", {"key": "lesson"})
    equivalent_lesson_profile = canonical_value(
        "spine.notification-profiles.v1", {"key": "lesson_standard"}
    )
    equivalent_lesson_binding = canonical_value(
        "spine.notification-profile-bindings.v1", {"profile_id": "profile_lesson"}
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
                        "revision": json.loads(profile["canonical_json"]),
                    },
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
                ),
            },
        ],
        "decision_action_ids": ["action-000000"],
        "blocked_object_keys": [],
        "apply_eligible": not draft,
    }
    return seal(plan)


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
    plan: dict[str, Any], approval: dict[str, Any], index: int
) -> dict[str, Any]:
    action = plan["actions"][index]
    value = json.loads(action["request_template"]["canonical_json"])
    execution = approval["execution"]
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
    return value


def make_checkpoint(plan: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    request = _materialized_request(plan, approval, 0)
    return seal(
        {
            "artifact_schema": "spine.pack-apply-checkpoint.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approval_digest": approval["content_identity"]["digest"],
            "execution": approval["execution"],
            "accepted_responses": [],
            "unresolved_submission": {
                "action_id": "action-000000",
                "command_id": request["command_id"],
                "submission_state": "prepared_or_submitted",
                "request": canonical_value("spine.notification-profiles.v1", request),
            },
            "next_action_id": "action-000000",
        }
    )


def _response(
    plan: dict[str, Any], approval: dict[str, Any], index: int, *, replay: bool = False
) -> dict[str, Any]:
    action = plan["actions"][index]
    cmd_id = command_id(
        plan["content_identity"]["digest"],
        approval["execution"]["execution_id"],
        action["action_id"],
    )
    contract = (
        "spine.notification-profiles.v1"
        if index == 0
        else "spine.notification-profile-bindings.v1"
    )
    generated = (
        [{"name": "notification_profile_revision_id", "value": "profile_revision_new"}]
        if index == 0
        else [{"name": "notification_profile_binding_id", "value": "binding_medical"}]
    )
    receipt_id = f"receipt_{index}"
    semantic_hash = str(index + 5) * 64
    response_value = {
        "command": action["command"],
        "effect": "revised" if index == 0 else "created",
        **{entry["name"]: entry["value"] for entry in generated},
        "ok": True,
        "receipt": {
            "command_id": cmd_id,
            "command_receipt_id": receipt_id,
            "created_at_utc": approval["execution"]["action_timestamp_utc"],
            "effect": "revised" if index == 0 else "created",
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
        "effect": "revised" if index == 0 else "created",
        "generated_ids": generated,
        "command_receipt_id": receipt_id,
        "semantic_facts_hash": semantic_hash,
        "response": canonical_value(contract, response_value),
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
            sorted(expected_files),
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
                    target = deepcopy(self.plan["request"]["target"])
                    target["host_name"] = "other.local"
                    errors = apply_preflight_errors(
                        self.plan,
                        target,
                        self.plan["environment"],
                        self.plan["catalog_snapshots"],
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
