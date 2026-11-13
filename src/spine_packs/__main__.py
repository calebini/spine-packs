"""Source-tree CLI: PYTHONPATH=src python3 -m spine_packs plan ..."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

from . import artifacts as a
from .apply import apply_continuation, apply_initial, checkpoint_writer
from .planning import INVALID, PACK_INVALID, ENVIRONMENT, PlanError, plan_installation, plan_outcome, require
from .spine_command import SpineCommand
from .manifest import validate_pack
from .execution import validate_inputs
from .recovery import continuation_checkpoint
from .verification import validate_verification_inputs, verify_installation


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise PlanError(INVALID, "invalid_cli_arguments")


def load_input(path, category, limit, *, allow_terminal_newline=False):
    try:
        with Path(path).open("rb") as handle:
            data = handle.read(limit + int(allow_terminal_newline) + 1)
        # The v2 continuation/result writers append one LF outside the canonical
        # artifact quota. No other extra byte or unbounded formatting is allowed;
        # callers still validate canonical size, schema and digest after parsing.
        require(len(data) <= limit or (allow_terminal_newline
                and len(data) == limit + 1 and data.endswith(b"\n")), "input_too_large", category)
        return a.parse_json(data)
    except (OSError, ValueError, RecursionError) as exc:
        raise PlanError(category, "invalid_input_file") from exc


def output_path(path, inputs):
    p = Path(path)
    require(not p.exists() and not p.is_symlink(), "output_already_exists", INVALID)
    resolved = p.resolve()
    require(resolved not in {Path(i).resolve() for i in inputs}, "output_input_collision", INVALID)
    require(resolved.parent.is_dir(), "output_parent_missing", INVALID)
    return resolved


def distinct_input(path, protected, code, *, file_identity=False):
    """Check aliases before opening a source/result as an artifact."""
    candidate = Path(path)
    require(candidate.resolve() not in {Path(p).resolve() for p in protected}, code, INVALID)
    if file_identity and candidate.exists():
        for other in protected:
            if Path(other).exists():
                require(not candidate.samefile(other), code, INVALID)


def publish(path, plan):
    """Atomically publish without replacing an existing file, even after a race."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".spine-plan-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write((a.canonical_text(plan) + "\n").encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)  # Atomic no-clobber publication on the same filesystem.
        temporary.unlink()
        temporary = None
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except FileExistsError as exc:
        raise PlanError(INVALID, "output_already_exists") from exc
    except OSError as exc:
        raise PlanError(ENVIRONMENT, "output_publication_failed") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def envelope(category, code=None, artifact=None, operation="plan"):
    exit_code, status = a.EXIT_MAP[category]
    return {"artifact_schema": "spine.pack-installer-result.v1", "operation": operation,
            "status": "success" if category == "success" else status, "exit_code": exit_code,
            "artifact": artifact, "error": None if category == "success" else {
                "category": category, "code": code or category,
                "message": "Operation stopped: " + (code or category) + ".", "facts": [],
            }}


def main(argv=None, *, transport_factory=SpineCommand):
    successor = False
    try:
        parser = Parser(prog="spine-packs", description="Local Spine pack plan, approved apply, and read-only verify.")
        parser.add_argument("operation", choices=["plan", "apply", "verify"])
        parser.add_argument("--manifest")
        parser.add_argument("--request")
        parser.add_argument("--plan")
        parser.add_argument("--approval")
        parser.add_argument("--checkpoint")
        parser.add_argument("--continue-from")
        parser.add_argument("--result")
        parser.add_argument("--output")
        parser.add_argument("--all", action="store_true", dest="all_flag")
        parser.add_argument("--archetype", action="append")
        args = parser.parse_args(argv)
        require(args.manifest is not None and args.output is not None, "invalid_cli_arguments", INVALID)
        manifest = load_input(args.manifest, PACK_INVALID, 16 * 1024 * 1024)
        successor = isinstance(manifest, dict) and manifest.get('manifest_schema') == 'spine.pack-manifest.v2'
        if successor:
            from .facet_manifest import validate as validate_successor
            from .facet_planning import validate_inputs as validate_successor_inputs, plan_installation as plan_successor
            from .facet_transport import FacetSpineCommand
            validate_successor(manifest)
        else:
            require(not validate_pack(manifest, a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")),
                    "invalid_manifest", PACK_INVALID)
        if args.operation == "plan":
            require(args.request is not None and args.plan is None and args.approval is None
                    and args.checkpoint is None and args.continue_from is None and args.result is None,
                    "invalid_cli_arguments", INVALID)
            request = load_input(args.request, INVALID, 1024 * 1024)
            if successor:
                validate_successor_inputs(manifest, request)
            else:
                require(not a.validate_schema(request), "invalid_request_shape", INVALID)
            require(not a.selection_assertion_errors(request, all_flag=args.all_flag, archetype_flags=args.archetype),
                    "selection_assertion_mismatch", INVALID)
            target = request["request"]["target"]
            output = output_path(args.output, [args.manifest, args.request,
                                             target["spine_command"]["path"], target["ledger"]["path"]])
            factory = FacetSpineCommand if successor and transport_factory is SpineCommand else transport_factory
            transport = factory(target)
            plan = (plan_successor if successor else plan_installation)(manifest, request, transport)
            publish(output, plan)
            result = envelope(plan_outcome(plan), artifact={"path": args.output, "digest": plan["content_identity"]["digest"]})
        elif args.operation == "verify":
            require(args.plan is not None and args.request is None and args.approval is None
                    and args.checkpoint is None and args.continue_from is None
                    and not args.all_flag and args.archetype is None, "invalid_cli_arguments", INVALID)
            plan = load_input(args.plan, INVALID, a.SIZE_LIMITS["spine.pack-install-plan.v1"])
            if successor:
                from .facet_verification import validate_verification_inputs as validate_successor_verification
                from .facet_verification import verify_installation as verify_successor
            validator = validate_successor_verification if successor else validate_verification_inputs
            validator(manifest, plan)
            target = plan["request"]["target"]
            protected = [args.manifest, args.plan, target["spine_command"]["path"], target["ledger"]["path"]]
            applied = None
            if args.result is not None:
                distinct_input(args.result, protected, "verification_result_input_collision", file_identity=successor)
                applied = load_input(args.result, INVALID, a.SIZE_LIMITS["spine.pack-apply-result.v1"],
                                     allow_terminal_newline=successor)
                if successor:
                    require(isinstance(applied, dict), 'invalid_apply_result', INVALID)
                validator(manifest, plan, applied)
                protected.append(args.result)
            output = output_path(args.output, protected)
            factory = FacetSpineCommand if successor and transport_factory is SpineCommand else transport_factory
            verified = (verify_successor if successor else verify_installation)(manifest, plan, factory(target), applied)
            publish(output, verified)
            result = envelope("success" if verified["state"] == "verified" else "verification_mismatch",
                              artifact={"path": args.output, "digest": verified["content_identity"]["digest"]},
                              operation="verify")
        else:
            require(args.plan is not None and args.approval is not None and args.checkpoint is not None
                    and args.request is None and args.result is None and not args.all_flag and args.archetype is None,
                    "invalid_cli_arguments", INVALID)
            plan = load_input(args.plan, INVALID, a.SIZE_LIMITS["spine.pack-install-plan.v1"])
            approval = load_input(args.approval, INVALID, a.SIZE_LIMITS["spine.pack-install-approval.v1"])
            if successor:
                from .facet_execution import ExecutionContext
                ExecutionContext(manifest, plan, approval).validate_known_requests()
            else:
                validate_inputs(plan, approval)
            target = plan["request"]["target"]
            protected = [args.manifest, args.plan, args.approval,
                         target["spine_command"]["path"], target["ledger"]["path"]]
            source = None
            if args.continue_from is not None:
                distinct_input(args.continue_from, protected, "continuation_source_input_collision", file_identity=successor)
                source = load_input(args.continue_from, INVALID, a.SIZE_LIMITS["spine.pack-apply-checkpoint.v1"],
                                    allow_terminal_newline=successor)
                if successor:
                    from .facet_recovery import continuation_context
                    continuation_context(manifest, plan, approval, source)
                else:
                    continuation_checkpoint(plan, approval, source)
                protected.append(args.continue_from)
            checkpoint = output_path(args.checkpoint, [*protected, args.output])
            output = output_path(args.output, [*protected, args.checkpoint])
            if successor:
                from .facet_apply import apply_initial as apply_successor, checkpoint_writer as successor_writer
                from .facet_apply import apply_continuation as continue_successor
                from .facet_apply_transport import FacetApplyCommand
                writer = successor_writer(checkpoint)
                factory = FacetApplyCommand if transport_factory is SpineCommand else transport_factory
                transport = factory(target)
                applied = (apply_successor(manifest, plan, approval, transport, writer) if source is None else
                           continue_successor(manifest, plan, approval, source, transport, writer))
            else:
                writer = checkpoint_writer(checkpoint)
                transport = transport_factory(target)
                applied = (apply_initial(manifest, plan, approval, transport, writer) if source is None else
                           apply_continuation(manifest, plan, approval, source, transport, writer))
            publish(output, applied)
            category = ("success" if applied["state"] == "applied" else "partial_apply"
                        if applied["state"] == "partial" else applied["failure"]["error"]["category"])
            result = envelope(category, artifact={"path": args.output,
                "digest": applied["content_identity"]["digest"]}, operation="apply")
    except PlanError as exc:
        result = envelope(exc.category, exc.code, operation=(args.operation if 'args' in locals() else "plan"))
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        # Do not echo arbitrary input, process output, paths, or environment data.
        result = envelope(INVALID, "invalid_contract_value", operation=(args.operation if 'args' in locals() else "plan"))
    except OSError:
        result = envelope(ENVIRONMENT, "local_environment_failure", operation=(args.operation if 'args' in locals() else "plan"))
    if successor:
        result['artifact_schema'] = 'spine.pack-installer-result.v2'
    print(a.canonical_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
