"""Source-tree CLI: PYTHONPATH=src python3 -m spine_packs plan ..."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

from . import artifacts as a
from .planning import INVALID, PACK_INVALID, ENVIRONMENT, PlanError, plan_installation, plan_outcome, require
from .spine_command import SpineCommand
from .manifest import validate_pack


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


def envelope(category, code=None, artifact=None):
    exit_code, status = a.EXIT_MAP[category]
    return {"artifact_schema": "spine.pack-installer-result.v1", "operation": "plan",
            "status": "success" if category == "success" else status, "exit_code": exit_code,
            "artifact": artifact, "error": None if category == "success" else {
                "category": category, "code": code or category,
                "message": "Planning stopped: " + (code or category) + ".", "facts": [],
            }}


def main(argv=None, *, transport_factory=SpineCommand):
    try:
        parser = Parser(prog="spine-packs", description="Read-only local Spine pack planning.")
        parser.add_argument("operation", choices=["plan"])
        parser.add_argument("--manifest", required=True)
        parser.add_argument("--request", required=True)
        parser.add_argument("--output", required=True)
        parser.add_argument("--all", action="store_true", dest="all_flag")
        parser.add_argument("--archetype", action="append")
        args = parser.parse_args(argv)
        manifest = load_input(args.manifest, PACK_INVALID, 16 * 1024 * 1024)
        require(not validate_pack(manifest, a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")),
                "invalid_manifest", PACK_INVALID)
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
    except PlanError as exc:
        result = envelope(exc.category, exc.code)
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        # Do not echo arbitrary input, process output, paths, or environment data.
        result = envelope(INVALID, "invalid_contract_value")
    except OSError:
        result = envelope(ENVIRONMENT, "local_environment_failure")
    print(a.canonical_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
