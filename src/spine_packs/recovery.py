"""Bounded continuation admission using public readback, never ledger access.

Inverse comparison is private computation, not rollback or receipt evidence.
Only a validated retry response can extend the accepted prefix.
"""
from copy import deepcopy
import json

from . import artifacts as a
from .execution import (execution_artifact, materialize, validate_artifact,
                        validate_inputs, validate_prefix)
from .planning import (CATALOGS, INVALID, PlanError, build_plan,
                       observe_installation, require, semantics)
from .preflight import STALE, validate_apply_inputs


def prepared_submission(plan, approval, accepted):
    index = len(accepted)
    request = materialize(plan, approval, index, accepted)
    action = plan["actions"][index]
    prefix, contract = a.COMMAND_SHAPES[action["command"]]
    return {"action_id": action["action_id"], "command_id": request["command_id"],
            "submission_state": "prepared_or_submitted",
            "request": a.canonical_value(contract, request, prefix + "Request")}


def continuation_checkpoint(plan, approval, source):
    """Validate exact source correlation; derive a checkpoint from a partial."""
    validate_inputs(plan, approval)
    require(isinstance(source, dict) and source.get("artifact_schema") in (
        "spine.pack-apply-checkpoint.v1", "spine.pack-apply-result.v1"),
        "invalid_continuation_source", INVALID)
    validate_artifact(source)
    accepted = source["accepted_responses"]
    if source["artifact_schema"] == "spine.pack-apply-checkpoint.v1":
        expected = execution_artifact(plan, approval, accepted,
                                      unresolved=source["unresolved_submission"])
        require(source == expected, "continuation_source_mismatch", INVALID)
        return expected
    require(source["state"] == "partial", "continuation_requires_partial_result", INVALID)
    expected = execution_artifact(plan, approval, accepted, state="partial", failure=source["failure"])
    require(source == expected, "continuation_source_mismatch", INVALID)
    return execution_artifact(plan, approval, accepted,
                              unresolved=prepared_submission(plan, approval, accepted))


def catalog_digest(name, entries):
    """Pinned 0.3.0 public catalog fingerprint, independent of pagination."""
    if name == "bindings":
        fields = ("notification_profile_binding_id", "item_archetype_id",
                  "notification_profile_id", "status")
        rows = [{k: e[k] for k in fields} for e in entries]
        ordering = ("item_archetype_id", "notification_profile_binding_id")
    else:
        _, key, identity, _ = CATALOGS[name]
        rows = [{"id": e[identity], "key": e[key], "status": e["status"],
                 "current_revision_id": e["current_revision_id"],
                 **({k: e[k] for k in ("display_name", "description")} if name == "profiles" else {})}
                for e in entries]
        ordering = ("key", "id")
    return a.digest(sorted(rows, key=lambda r: tuple(r[k] for k in ordering)))


def _match(condition):
    require(condition, "continuation_state_mismatch", STALE)


def _provenance(row, request):
    _match(all(row[k] == request[v] for k, v in (
        ("created_by_subject_id", "actor_subject_id"),
        ("created_by_command_id", "command_id"),
        ("created_at_utc", "action_timestamp_utc"))))


def _undo(catalogs, plan, action, request, response):
    """Validate a full post-action definition, then reverse only its effect.

    The reconstructed entries are classification inputs, NOT public readbacks:
    historical audit/template facts cannot be reconstructed and are not claimed.
    build_plan uses only semantics, identities, status and original snapshots.
    """
    command = action["command"]
    classification = next(c for c in plan["classifications"] if c["object_key"] == action["object_key"])
    if command == "notification_profile.binding.set":
        matches = [e for e in catalogs["bindings"] if e["item_archetype_id"] == request["item_archetype_id"]]
        _match(len(matches) == 1)
        row = matches[0]
        _match(row["status"] == "active" and row["notification_profile_id"] == request["notification_profile_id"])
        facts = {k: row[k] for k in ("notification_profile_binding_id", "item_archetype_id",
                                    "notification_profile_id", "status")}
        roots = []
        for name, field in (("archetypes", "item_archetype_id"), ("profiles", "notification_profile_id")):
            roots.extend(e for e in catalogs[name] if e[field] == request[field] and e["status"] == "active")
        _match(len(roots) == 2)
        facts["compatible_item_types"] = sorted(set(roots[0]["revision"]["compatible_item_types"])
                                                & set(roots[1]["revision"]["compatible_item_types"]))
        _match(bool(facts["compatible_item_types"]))
        noop = response is not None and response["effect"] == "notification_profile_binding_set_noop"
        if not noop:
            _provenance(row, request)
        if response is not None:
            _match(all(response[k] == v for k, v in facts.items()))
        if not noop:
            catalogs["bindings"].remove(row)
            old = classification["identity"]["observed_binding"]
            if old is not None:
                catalogs["bindings"].append({**deepcopy(old), "status": "active"})
        return facts

    profile = command.startswith("notification_profile")
    name, kind = ("profiles", "profile") if profile else ("archetypes", "archetype")
    _, key_field, id_field, _ = CATALOGS[name]
    revision_field = "notification_profile_revision_id" if profile else "item_archetype_revision_id"
    create, revise = command.endswith(".create"), command.endswith(".revise")
    matches = [e for e in catalogs[name] if
               (e[key_field] == request[key_field] if create else e[id_field] == request[id_field])]
    _match(len(matches) == 1)
    row = matches[0]
    _match(row["status"] == "active")
    facts = {id_field: row[id_field], revision_field: row["current_revision_id"], "status": row["status"]}
    if create or revise:
        observed = semantics(row, kind)
        _match((observed["revision"] if profile else observed) == request["revision"])
        _provenance(row["revision"], request)
        facts["revision_number"] = str(row["revision"]["revision_number"])
        if profile:
            facts["normalized_revision_hash"] = row["revision"]["normalized_revision_hash"]
        if create:
            _provenance(row, request)
            _match(row["revision"]["revision_number"] == 1)
            facts[key_field] = row[key_field]
            if profile:
                _match(observed["metadata"] == {k: request[k] for k in ("display_name", "description")})
        else:
            _match(row["current_revision_id"] != request["expected_current_revision_id"]
                   and row["revision"]["revision_number"] > 1)
    else:
        _match({k: row[k] for k in ("display_name", "description")} == request["metadata"])
        facts.update(request["metadata"])
    if response is not None:
        _match(all(response[k] == v for k, v in facts.items()))
    if create:
        catalogs[name].remove(row)
    elif revise:
        row["current_revision_id"] = request["expected_current_revision_id"]
        row["revision"][revision_field] = row["current_revision_id"]
        old = json.loads(action["expected"]["canonical_json"])
        row["revision"].update(deepcopy(old["revision"] if profile else old))
    else:
        row.update(deepcopy(request["expected_metadata"]))
    return facts


def preflight_continuation(manifest, plan, approval, source, transport, *, page_size=100):
    """Admit exactly prefix or prefix+one; return provisional facts, not receipts."""
    checkpoint = continuation_checkpoint(plan, approval, source)
    request = validate_apply_inputs(manifest, plan, approval)
    environment, catalogs, snapshots = observe_installation(manifest, request, transport, page_size=page_size)
    _match(environment == plan["environment"])
    for name in CATALOGS:
        require(catalog_digest(name, catalogs[name]) == snapshots[name], "public_snapshot_hash_mismatch")
    accepted = checkpoint["accepted_responses"]
    decoded = validate_prefix(plan, approval, accepted)
    steps = [(action, materialize(plan, approval, i, accepted[:i]), decoded[action["action_id"]])
             for i, action in enumerate(plan["actions"][:len(accepted)])]
    candidates = []
    for uncertain in (False, True) if len(accepted) < len(plan["actions"]) else (False,):
        restored = deepcopy(catalogs)
        candidate_steps = steps[:]
        if uncertain:
            index = len(accepted)
            candidate_steps.append((plan["actions"][index], materialize(plan, approval, index, accepted), None))
        provisional = None
        try:
            for action, body, response in reversed(candidate_steps):
                facts = _undo(restored, plan, action, body, response)
                if response is None:
                    provisional = facts
            original = {s["catalog"]: s["digest"] for s in plan["catalog_snapshots"]}
            # Recompile the ORIGINAL plan: checks untouched selected semantics,
            # every suffix precondition, closure, exact commands and approval scope.
            reconstructed = build_plan(manifest, request, environment, restored, original)
            _match(reconstructed == plan)
            # Only after full semantic/identity admission compare fingerprints.
            _match(all(catalog_digest(n, restored[n]) == original[n] for n in CATALOGS))
        except PlanError:
            continue
        candidates.append(provisional)
    require(len(candidates) == 1, "continuation_state_mismatch", STALE)
    return checkpoint, candidates[0]
