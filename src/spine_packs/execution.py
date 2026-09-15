"""Pure execution materialization and evidence validation; no transport."""
from copy import deepcopy
import json

from . import artifacts as a
from .planning import ENVIRONMENT, INVALID, require


def command_id(plan_digest, execution_id, action_id):
    return "spack_" + a.digest({"action_id": action_id,
        "derivation_version": "spine.pack-command-id.v1",
        "execution_id": execution_id, "plan_digest": plan_digest})


def validate_inputs(plan, approval):
    require(isinstance(plan, dict) and plan.get("artifact_schema") == "spine.pack-install-plan.v1"
            and not a.validate_schema(plan), "invalid_plan", INVALID)
    require(not a.plan_errors(plan) and not a.artifact_size_errors(plan), "invalid_plan", INVALID)
    require(isinstance(approval, dict)
            and approval.get("artifact_schema") == "spine.pack-install-approval.v1"
            and not a.validate_schema(approval), "invalid_or_incomplete_approval", INVALID)
    require(not a.approval_errors(approval, plan) and not a.artifact_size_errors(approval),
            "invalid_or_incomplete_approval", INVALID)


def validate_artifact(value):
    require(not a.validate_schema(value) and not a.content_digest_errors(value)
            and not a.artifact_size_errors(value), "invalid_execution_artifact", INVALID)


def validate_known_requests(plan, approval):
    """Preflight every request not dependent on a still-unknown create response."""
    validate_inputs(plan, approval)
    for index, action in enumerate(plan["actions"]):
        template = json.loads(action["request_template"]["canonical_json"])
        if not a._reference_slots(template):
            _request(plan, approval, index, {})


def _request(plan, approval, index, decoded):
    action = plan["actions"][index]
    prefix, contract = a.COMMAND_SHAPES[action["command"]]
    require(not a.canonical_value_errors(action["request_template"], prefix + "Template"),
            "invalid_command_template", INVALID)
    value = json.loads(action["request_template"]["canonical_json"])
    require(not a.result_reference_errors(value, prefix + "Template", plan, index),
            "invalid_result_reference", INVALID)
    for path, reference in a._reference_slots(value):
        producer_id, field = a.RESULT_REFERENCE.fullmatch(reference).groups()
        require(producer_id in decoded, "result_reference_evidence_missing", INVALID)
        value[path[0]] = decoded[producer_id][field]
    execution = approval["execution"]
    value.update(command_id=command_id(plan["content_identity"]["digest"],
                                     execution["execution_id"], action["action_id"]),
                 actor_subject_id=execution["actor_subject_id"],
                 action_timestamp_utc=execution["action_timestamp_utc"])
    wrapped = a.canonical_value(contract, value, prefix + "Request")
    require(not a.canonical_value_errors(wrapped, prefix + "Request"),
            "invalid_materialized_request", INVALID)
    return value


def response_evidence(action, request, response):
    prefix, contract = a.COMMAND_SHAPES[action["command"]]
    # Raw write responses must themselves be canonical-compatible (no numbers).
    try:
        value = a.canonical_value(contract, response, prefix + "Response")
        valid = not a.canonical_value_errors(value, prefix + "Response")
    except (ValueError, TypeError, KeyError, RecursionError):
        valid = False
    require(valid, "invalid_spine_response", ENVIRONMENT)
    receipt = response["receipt"]
    require(receipt["command_id"] == request["command_id"], "response_command_id_mismatch")
    require(receipt["effect"] == response["effect"], "response_effect_mismatch")
    require(receipt["created_at_utc"] == request["action_timestamp_utc"], "receipt_timestamp_mismatch")
    # Pinned 0.3.0 handlers hash the complete semantic request, including execution fields.
    require(receipt["semantic_facts_hash"] == a.digest(request), "receipt_request_hash_mismatch")
    for field in ("archetype_key", "profile_key", "item_archetype_id", "notification_profile_id"):
        if field in request and field in response:
            require(response[field] == request[field], "response_identity_mismatch")
    if action["command"].endswith(".create"):
        require(response["revision_number"] == "1", "response_revision_mismatch")
    if action["command"].endswith(".revise"):
        revision_id = "item_archetype_revision_id" if prefix == "archetypeRevise" else "notification_profile_revision_id"
        require(response[revision_id] != request["expected_current_revision_id"], "response_revision_mismatch")
    if prefix == "profileMetadataUpdate":
        require({k: response[k] for k in ("display_name", "description")} == request["metadata"],
                "response_metadata_mismatch")
        effect = ("notification_profile_metadata_update_noop" if request["metadata"] == request["expected_metadata"]
                  else "notification_profile_metadata_updated")
        require(response["effect"] == effect, "response_effect_mismatch")
    if prefix == "bindingSet":
        types = response["compatible_item_types"]
        require(types == sorted(set(types)), "response_item_types_not_canonical")
    return {"action_id": action["action_id"], "command": action["command"],
            "command_id": request["command_id"], "outcome": "accepted",
            "response_contract": response["response_contract"], "effect": response["effect"],
            "generated_ids": [{"name": k, "value": response[k]} for k in sorted(response) if k.endswith("_id")],
            "command_receipt_id": receipt["command_receipt_id"],
            "semantic_facts_hash": receipt["semantic_facts_hash"], "response": value}


def validate_prefix(plan, approval, accepted):
    require(isinstance(accepted, list) and len(accepted) <= len(plan["actions"]),
            "invalid_accepted_prefix", INVALID)
    decoded, receipt_ids = {}, set()
    for index, evidence in enumerate(accepted):
        action = plan["actions"][index]
        require(isinstance(evidence, dict) and evidence.get("action_id") == action["action_id"],
                "invalid_accepted_prefix", INVALID)
        shape = a.COMMAND_SHAPES[action["command"]][0] + "Response"
        require(not a.canonical_value_errors(evidence["response"], shape), "invalid_response_evidence", INVALID)
        body = json.loads(evidence["response"]["canonical_json"])
        expected = response_evidence(action, _request(plan, approval, index, decoded), body)
        require(evidence.get("outcome") in ("accepted", "compatible_replay"),
                "invalid_response_evidence", INVALID)
        expected["outcome"] = evidence["outcome"]
        require(evidence == expected, "invalid_response_evidence", INVALID)
        require(expected["command_receipt_id"] not in receipt_ids, "duplicate_receipt_evidence", INVALID)
        receipt_ids.add(expected["command_receipt_id"])
        decoded[action["action_id"]] = body
    return decoded


def materialize(plan, approval, index, accepted):
    validate_inputs(plan, approval)
    require(type(index) is int and 0 <= index < len(plan["actions"]) and len(accepted) == index,
            "invalid_accepted_prefix", INVALID)
    return _request(plan, approval, index, validate_prefix(plan, approval, accepted))


def execution_artifact(plan, approval, accepted, *, unresolved=None, state=None, failure=None):
    """Construct and validate a checkpoint or terminal result from one exact prefix."""
    validate_inputs(plan, approval)
    validate_prefix(plan, approval, accepted)
    remaining = [x["action_id"] for x in plan["actions"][len(accepted):]]
    value = {"artifact_schema": "spine.pack-apply-checkpoint.v1" if state is None else "spine.pack-apply-result.v1",
             "plan_digest": plan["content_identity"]["digest"],
             "approval_digest": approval["content_identity"]["digest"],
             "execution": deepcopy(approval["execution"]), "accepted_responses": deepcopy(accepted)}
    if state is None:
        if unresolved is not None:
            require(bool(remaining), "unexpected_submission", INVALID)
            request = materialize(plan, approval, len(accepted), accepted)
            prefix, contract = a.COMMAND_SHAPES[plan["actions"][len(accepted)]["command"]]
            require(unresolved == {"action_id": remaining[0], "command_id": request["command_id"],
                "submission_state": "prepared_or_submitted",
                "request": a.canonical_value(contract, request, prefix + "Request")},
                "unresolved_request_mismatch", INVALID)
        value.update(unresolved_submission=deepcopy(unresolved), next_action_id=remaining[0] if remaining else None)
    else:
        if state == "applied":
            require(not remaining and failure is None, "applied_not_complete", INVALID)
            unattempted = []
        elif state == "partial":
            require(bool(remaining) and failure is not None and failure["action_id"] == remaining[0],
                    "partial_failure_mismatch", INVALID)
            unattempted = remaining[1:]
        else:
            require(state == "not_applied" and not accepted and failure is not None,
                    "invalid_not_applied", INVALID)
            unattempted = remaining
        value.update(state=state, failure=deepcopy(failure), unattempted_action_ids=unattempted)
    value = a.seal(value)
    validate_artifact(value)
    return value
