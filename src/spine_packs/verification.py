"""Read-only selected-state verification and captured-response correlation.

Never invokes apply, recovery, or a write/replay command. Captured receipts
are local evidence, not an independent later read of Spine receipt rows.
"""
from copy import deepcopy
import json

from . import artifacts as a
from .execution import execution_artifact, validate_artifact, validate_prefix
from .manifest import validate_pack
from .planning import (CATALOGS, INVALID, PACK_INVALID, PlanError, build_plan,
                       observe_installation, require, selected_definitions)
from .preflight import STALE


def validate_verification_inputs(manifest, plan, result=None):
    """Validate trusted identities and manifest intent before target use."""
    require(not validate_pack(manifest, a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")),
            "invalid_manifest", PACK_INVALID)
    require(isinstance(plan, dict) and plan.get("artifact_schema") == "spine.pack-install-plan.v1"
            and not a.validate_schema(plan), "invalid_plan", INVALID)
    require(not a.plan_errors(plan) and not a.artifact_size_errors(plan), "invalid_plan", INVALID)
    identity = {"manifest_schema": manifest["manifest_schema"], **manifest["pack"],
                "manifest_digest": manifest["content_identity"]["digest"]}
    require(identity == plan["pack"], "manifest_identity_mismatch", STALE)
    archetypes, profiles, bindings = selected_definitions(manifest, plan["request"])
    closure = {"archetype_keys": sorted(archetypes), "profile_keys": sorted(profiles),
               "binding_archetype_keys": sorted(bindings)}
    require(closure == plan["closure"], "manifest_selection_mismatch", INVALID)
    desired = {"archetype:" + k: v["revision"] for k, v in archetypes.items()}
    desired.update({"profile:" + k: {"metadata": {f: v[f] for f in ("display_name", "description")},
                                    "revision": v["revision"]} for k, v in profiles.items()})
    desired.update({"binding:" + k: {"binding_kind": "archetype_default",
                                    "notification_profile_key": v["notification_profile_key"]}
                    for k, v in bindings.items()})
    for c in plan["classifications"]:
        require(json.loads(c["desired"]["canonical_json"]) == desired[c["object_key"]],
                "manifest_desired_state_mismatch", INVALID)
    _validate_actions(plan)
    if result is not None:
        require(isinstance(result, dict) and result.get("artifact_schema") == "spine.pack-apply-result.v1"
                and not a.validate_schema(result), "invalid_apply_result", INVALID)
        # A corrupt digest/shape cannot be cited as a trustworthy artifact identity.
        require(not a.content_digest_errors(result) and not a.artifact_size_errors(result),
                "invalid_apply_result", INVALID)


def _validate_actions(plan):
    """Check action coverage and public request intent against classifications."""
    expected = []
    for c in plan["classifications"]:
        kind, key = c["object_key"].split(":", 1)
        wanted = json.loads(c["desired"]["canonical_json"])
        old = None if c["observed"] is None else json.loads(c["observed"]["canonical_json"])
        commands = []
        if c["classification"] == "missing":
            commands = [{"archetype": "item_archetype.create", "profile": "notification_profile.create",
                         "binding": "notification_profile.binding.set"}[kind]]
        elif c["classification"] == "drifted":
            if kind == "profile":
                if old["metadata"] != wanted["metadata"]:
                    commands.append("notification_profile.metadata.update")
                if old["revision"] != wanted["revision"]:
                    commands.append("notification_profile.revise")
            else:
                commands = ["item_archetype.revise" if kind == "archetype" else "notification_profile.binding.set"]
        expected.extend((c["object_key"], command) for command in commands)
        for action in (v for v in plan["actions"] if v["object_key"] == c["object_key"]):
            command = action["command"]
            body = json.loads(action["request_template"]["canonical_json"])
            require(command in commands and action["desired"] == c["desired"]
                    and action["expected"] == c["observed"]
                    and action["change_kind"] == ("create" if old is None else "update"),
                    "plan_action_intent_mismatch", INVALID)
            if kind != "binding":
                if command.endswith(".create"):
                    require(body["archetype_key" if kind == "archetype" else "profile_key"] == key,
                            "plan_action_intent_mismatch", INVALID)
                else:
                    require(body["item_archetype_id" if kind == "archetype" else "notification_profile_id"]
                            == c["identity"]["catalog_id"], "plan_action_intent_mismatch", INVALID)
                if command.endswith(".update"):
                    require(body["metadata"] == wanted["metadata"] and body["expected_metadata"] == old["metadata"],
                            "plan_action_intent_mismatch", INVALID)
                else:
                    require(body["revision"] == (wanted if kind == "archetype" else wanted["revision"]),
                            "plan_action_intent_mismatch", INVALID)
                    if kind == "profile" and command.endswith(".create"):
                        require({k: body[k] for k in ("display_name", "description")} == wanted["metadata"],
                                "plan_action_intent_mismatch", INVALID)
    require(sorted(expected) == sorted((v["object_key"], v["command"]) for v in plan["actions"]),
            "plan_action_coverage_mismatch", INVALID)


def _response_evidence(plan, result):
    if result is None:
        return ("missing" if plan["actions"] else "not_required"), {}
    try:
        # The closed v1 approval is uniquely reconstructible for correlation.
        # This checks its recorded digest; it NEVER grants or publishes approval.
        approval = a.seal({"artifact_schema": "spine.pack-install-approval.v1",
            "plan_digest": plan["content_identity"]["digest"], "approve_complete_plan": True,
            "acknowledge_single_operator": True, "authorized_update_action_ids": plan["decision_action_ids"],
            "execution": deepcopy(result["execution"])})
        expected = execution_artifact(plan, approval, result["accepted_responses"],
                                      state=result["state"], failure=result["failure"])
        require(expected == result, "apply_result_correlation_mismatch", INVALID)
        decoded = validate_prefix(plan, approval, result["accepted_responses"])
        require(not result["accepted_responses"] or plan["apply_eligible"], "ineligible_response_evidence", INVALID)
    except (PlanError, ValueError, KeyError, TypeError, RecursionError):
        return "invalid", {}
    if not plan["actions"]:
        return "not_required", decoded
    return ("complete" if result["state"] == "applied" else "missing"), decoded


def verify_installation(manifest, plan, transport, result=None, *, page_size=100):
    """Observe selected desired state without replay, checkpointing, or writes."""
    manifest, plan, result = deepcopy((manifest, plan, result))
    validate_verification_inputs(manifest, plan, result)
    evidence, responses = _response_evidence(plan, result)
    request = a.seal({"artifact_schema": "spine.pack-install-request.v1", "request": deepcopy(plan["request"])})
    environment, catalogs, snapshots = observe_installation(manifest, request, transport, page_size=page_size)
    require(environment == plan["environment"], "verification_environment_mismatch", STALE)
    current = build_plan(manifest, request, environment, catalogs, snapshots)
    # Existing IDs remain pinned. Missing roots may be resolved only from
    # validated captured create responses, never from an untrusted ID map.
    expected_ids = {c["object_key"]: c["identity"]["catalog_id"] for c in plan["classifications"]
                    if c["object_kind"] != "binding" and c["identity"] is not None}
    for action in plan["actions"]:
        if action["command"].endswith(".create") and action["action_id"] in responses:
            field = "item_archetype_id" if action["command"] == "item_archetype.create" else "notification_profile_id"
            expected_ids[action["object_key"]] = responses[action["action_id"]][field]
    objects = []
    for c in current["classifications"]:
        state = c["classification"]
        if state == "equivalent":
            if c["object_kind"] == "binding":
                key = c["object_key"].split(":", 1)[1]
                profile = json.loads(c["desired"]["canonical_json"])["notification_profile_key"]
                matches = all(expected_ids.get(k, c["identity"][field]) == c["identity"][field]
                              for k, field in (("archetype:" + key, "item_archetype_id"),
                                               ("profile:" + profile, "notification_profile_id")))
            else:
                matches = expected_ids.get(c["object_key"], c["identity"]["catalog_id"]) == c["identity"]["catalog_id"]
            if not matches:
                state = "drifted"
        objects.append({"object_kind": c["object_kind"], "object_key": c["object_key"],
                        "state": state, "observed": deepcopy(c["observed"])})
    verified = all(o["state"] == "equivalent" for o in objects) and evidence in ("complete", "not_required")
    value = a.seal({"artifact_schema": "spine.pack-verification-result.v1",
        "plan_digest": plan["content_identity"]["digest"],
        "apply_result_digest": result["content_identity"]["digest"] if result is not None and plan["actions"] else None,
        "pack": deepcopy(plan["pack"]), "target": deepcopy(plan["request"]["target"]),
        "environment": environment, "catalog_snapshots": [{"catalog": k, "digest": snapshots[k]} for k in CATALOGS],
        "closure": deepcopy(plan["closure"]), "object_results": objects, "response_evidence": evidence,
        "receipt_readback": "captured_responses_only_spine_" + environment["runtime_version"],
        "state": "verified" if verified else "mismatch"})
    validate_artifact(value)
    for obj in objects:
        require(obj["observed"] is None or not a.canonical_value_errors(obj["observed"], obj["object_kind"] + "Semantics"),
                "invalid_verification_observation", INVALID)
    return value
