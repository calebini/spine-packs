"""Non-mutating apply preflight over an approved installation plan."""

from __future__ import annotations

from copy import deepcopy

from . import artifacts as a
from .manifest import validate_pack
from .planning import INVALID, PACK_INVALID, PlanError, plan_installation, require

STALE = "stale_plan_or_target_mismatch"


def preflight_apply(manifest, plan, approval, transport, *, page_size=100):
    """Return execution facts after complete, fresh, read-only validation."""
    manifest_schema = a._schema_document(
        a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json"
    )
    require(not validate_pack(manifest, manifest_schema), "invalid_manifest", PACK_INVALID)
    require(
        not a.plan_errors(plan) and not a.artifact_size_errors(plan),
        "invalid_plan",
        INVALID,
    )
    require(
        not a.approval_errors(approval, plan)
        and not a.artifact_size_errors(approval),
        "invalid_or_incomplete_approval",
        INVALID,
    )
    require(plan["pack"]["status"] == "released", "draft_plan_not_applicable", PACK_INVALID)
    require(plan["apply_eligible"], "plan_not_apply_eligible", PACK_INVALID)
    require(not plan["blocked_object_keys"], "blocked_plan_not_applicable", PACK_INVALID)

    pack_identity = {
        "manifest_schema": manifest["manifest_schema"],
        **manifest["pack"],
        "manifest_digest": manifest["content_identity"]["digest"],
    }
    require(pack_identity == plan["pack"], "manifest_identity_mismatch", STALE)

    request = a.seal({
        "artifact_schema": "spine.pack-install-request.v1",
        "request": deepcopy(plan["request"]),
    })
    require(
        request["content_identity"]["digest"] == plan["request_digest"],
        "request_identity_mismatch",
        STALE,
    )
    observed_plan = plan_installation(manifest, request, transport, page_size=page_size)
    require(
        observed_plan["content_identity"]["digest"] == plan["content_identity"]["digest"],
        "stale_plan",
        STALE,
    )
    return {
        "plan_digest": plan["content_identity"]["digest"],
        "approval_digest": approval["content_identity"]["digest"],
        "execution": deepcopy(approval["execution"]),
        "action_ids": [action["action_id"] for action in plan["actions"]],
    }
