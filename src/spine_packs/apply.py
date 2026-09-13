"""Initial approved apply execution with durable checkpointing; no continuation."""
from copy import deepcopy
import os
from pathlib import Path
import tempfile

from . import artifacts as a
from .execution import (command_id, execution_artifact, materialize, response_evidence,
                        validate_artifact, validate_inputs)
from .planning import ENVIRONMENT, INVALID, PlanError, observe_catalog, require
from .preflight import preflight_apply


def checkpoint_writer(path):
    """Create once without clobbering, then replace only this writer's checkpoint."""
    supplied = Path(path)
    require(not supplied.exists() and not supplied.is_symlink(), "checkpoint_already_exists", INVALID)
    target = supplied.resolve()
    require(target.parent.is_dir(), "checkpoint_parent_missing", INVALID)
    previous = None

    def write(value):
        nonlocal previous
        validate_artifact(value)
        require(value["artifact_schema"] == "spine.pack-apply-checkpoint.v1", "invalid_checkpoint", INVALID)
        encoded = (a.canonical_text(value) + "\n").encode("utf-8")
        temporary = None
        try:
            if previous is not None:
                require(not target.is_symlink() and target.is_file(), "checkpoint_changed")
                with target.open("rb") as handle:
                    observed = handle.read(len(previous) + 1)
                require(observed == previous, "checkpoint_changed")
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".spine-checkpoint-", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            if previous is None:
                os.link(temporary, target)
                temporary.unlink()
                temporary = None
            else:
                os.replace(temporary, target)
                temporary = None
            directory = os.open(target.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
            previous = encoded
        except FileExistsError as exc:
            raise PlanError(INVALID, "checkpoint_already_exists") from exc
        except OSError as exc:
            raise PlanError(ENVIRONMENT, "checkpoint_publication_failed") from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return write


def failure(exc, action_id=None):
    # Only controlled diagnostics, never raw transport output or exception text.
    return {"action_id": action_id, "error": {
        "category": exc.category, "code": exc.code,
        "message": "Apply stopped: " + exc.code + ".", "facts": getattr(exc, "facts", []),
    }}


def _binding_precondition(plan, action, request, transport, page_size):
    # V1 has one binding action per archetype, so earlier actions cannot change
    # this binding. Creates resolve its root IDs but still require absent binding.
    classification = next(c for c in plan["classifications"] if c["object_key"] == action["object_key"])
    expected = classification["identity"]["observed_binding"]
    entries, _ = observe_catalog(transport, "bindings", plan["request"]["owner"], page_size=page_size)
    matches = [e for e in entries if e["item_archetype_id"] == request["item_archetype_id"]]
    fields = ("notification_profile_binding_id", "item_archetype_id", "notification_profile_id")
    actual = {k: matches[0][k] for k in fields} if matches else None
    require(actual == expected, "binding_precondition_changed", "stale_plan_or_target_mismatch")


def apply_initial(manifest, plan, approval, transport, checkpoint_writer, *, page_size=100):
    """Execute only a new, fully approved plan; never read/resume saved checkpoints."""
    # Detach caller-owned objects before callbacks or transport can mutate them.
    manifest, plan, approval = deepcopy((manifest, plan, approval))
    validate_inputs(plan, approval)
    accepted = []
    try:
        preflight_apply(manifest, plan, approval, transport, page_size=page_size)
    except PlanError as exc:
        return execution_artifact(plan, approval, [], state="not_applied", failure=failure(exc))
    actions = plan["actions"]
    if not actions:
        checkpoint_writer(execution_artifact(plan, approval, []))
        return execution_artifact(plan, approval, [], state="applied")

    for index, action in enumerate(actions):
        try:
            request = materialize(plan, approval, index, accepted)
            if action["command"] == "notification_profile.binding.set":
                _binding_precondition(plan, action, request, transport, page_size)
        except PlanError as exc:
            return execution_artifact(plan, approval, accepted,
                state="partial" if accepted else "not_applied",
                failure=failure(exc, action["action_id"]))
        prefix, contract = a.COMMAND_SHAPES[action["command"]]
        unresolved = {"action_id": action["action_id"], "command_id": request["command_id"],
            "submission_state": "prepared_or_submitted",
            "request": a.canonical_value(contract, request, prefix + "Request")}
        # Publication failures propagate: no terminal success/rollback claim is made.
        checkpoint_writer(execution_artifact(plan, approval, accepted, unresolved=unresolved))
        try:
            response = transport.write(action["command"], deepcopy(request))
            evidence = response_evidence(action, request, response)
            next_accepted = [*accepted, evidence]
            advanced = execution_artifact(plan, approval, next_accepted)
        except (PlanError, ValueError, TypeError, KeyError, RecursionError, OSError) as exc:
            if not isinstance(exc, PlanError):
                exc = PlanError(ENVIRONMENT, "invalid_or_uncertain_write_response")
            # Once transport is invoked, failure is potentially post-commit, even
            # for the very first action. Never report that nothing was applied.
            return execution_artifact(plan, approval, accepted, state="partial",
                                      failure=failure(exc, action["action_id"]))
        checkpoint_writer(advanced)
        accepted = next_accepted
    return execution_artifact(plan, approval, accepted, state="applied")
