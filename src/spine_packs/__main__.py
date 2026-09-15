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


def load_input(path, category, limit):
    try:
        with Path(path).open("rb") as handle:
            data = handle.read(limit + 1)
        require(len(data) <= limit, "input_too_large", category)
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
        require(not validate_pack(manifest, a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")),
                "invalid_manifest", PACK_INVALID)
        if args.operation == "plan":
            require(args.request is not None and args.plan is None and args.approval is None
                    and args.checkpoint is None and args.continue_from is None and args.result is None,
                    "invalid_cli_arguments", INVALID)
            request = load_input(args.request, INVALID, 1024 * 1024)
            require(not a.validate_schema(request), "invalid_request_shape", INVALID)
            require(not a.selection_assertion_errors(request, all_flag=args.all_flag, archetype_flags=args.archetype),
                    "selection_assertion_mismatch", INVALID)
            target = request["request"]["target"]
            output = output_path(args.output, [args.manifest, args.request,
                                             target["spine_command"]["path"], target["ledger"]["path"]])
            transport = transport_factory(target)
            plan = plan_installation(manifest, request, transport)
            publish(output, plan)
            result = envelope(plan_outcome(plan), artifact={"path": args.output, "digest": plan["content_identity"]["digest"]})
        elif args.operation == "verify":
            require(args.plan is not None and args.request is None and args.approval is None
                    and args.checkpoint is None and args.continue_from is None
                    and not args.all_flag and args.archetype is None, "invalid_cli_arguments", INVALID)
            plan = load_input(args.plan, INVALID, a.SIZE_LIMITS["spine.pack-install-plan.v1"])
            validate_verification_inputs(manifest, plan)
            target = plan["request"]["target"]
            protected = [args.manifest, args.plan, target["spine_command"]["path"], target["ledger"]["path"]]
            applied = None
            if args.result is not None:
                require(Path(args.result).resolve() not in {Path(p).resolve() for p in protected},
                        "verification_result_input_collision", INVALID)
                applied = load_input(args.result, INVALID, a.SIZE_LIMITS["spine.pack-apply-result.v1"])
                validate_verification_inputs(manifest, plan, applied)
                protected.append(args.result)
            output = output_path(args.output, protected)
            verified = verify_installation(manifest, plan, transport_factory(target), applied)
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
            validate_inputs(plan, approval)
            target = plan["request"]["target"]
            protected = [args.manifest, args.plan, args.approval,
                         target["spine_command"]["path"], target["ledger"]["path"]]
            source = None
            if args.continue_from is not None:
                require(Path(args.continue_from).resolve() not in {Path(p).resolve() for p in protected},
                        "continuation_source_input_collision", INVALID)
                source = load_input(args.continue_from, INVALID, a.SIZE_LIMITS["spine.pack-apply-checkpoint.v1"])
                continuation_checkpoint(plan, approval, source)
                protected.append(args.continue_from)
            checkpoint = output_path(args.checkpoint, [*protected, args.output])
            output = output_path(args.output, [*protected, args.checkpoint])
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
    print(a.canonical_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
