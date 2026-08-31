#!/usr/bin/env python3
"""Verify the seed-stage Spine Packs repository shape and boundaries."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "packs/kinflow-starter/README.md",
    "scripts/verify_repo.py",
    "specs/architecture.md",
    "specs/compatibility.md",
    "specs/overview.md",
    "specs/pack-format.md",
)

REQUIRED_MARKERS = {
    "README.md": (
        "Spine remains the sole authority",
        "Direct database access is forbidden",
        "`plan`",
        "`apply`",
        "`verify`",
        "seed-spec",
    ),
    "AGENTS.md": (
        "The files in `specs/` are the normative source of truth",
        "Do not make Spine runtime changes",
    ),
    "specs/overview.md": (
        "Packs MUST be declarative and owner-neutral",
        "Pack releases MUST be immutable",
    ),
    "specs/architecture.md": (
        "Spine public command surface",
        "Direct database access is forbidden",
        "semantic drift",
    ),
    "specs/compatibility.md": (
        "Spine runtime versions",
        "Spine contract versions",
        "fail closed",
    ),
    "specs/pack-format.md": (
        "pre-schema contract",
        "identity/version pair is immutable",
        "Deterministic ordering",
        "**unsettled**",
    ),
}

CANDIDATE_NAMES = (
    "medical_appointment",
    "lesson",
    "passport_renewal",
    "game_or_competition",
    "flight",
    "birthday",
)

FORBIDDEN_TOP_LEVEL = (
    "adapters",
    "contracts",
    "examples",
    "models",
    "services",
    "src",
)

MANIFEST_SUFFIXES = (".json", ".toml", ".yaml", ".yml")


def verify() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for relative, markers in REQUIRED_MARKERS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"missing boundary marker in {relative}: {marker!r}")

    pack_readme = ROOT / "packs/kinflow-starter/README.md"
    if pack_readme.is_file():
        text = pack_readme.read_text(encoding="utf-8")
        for name in CANDIDATE_NAMES:
            if f"`{name}`" not in text:
                errors.append(f"missing kinflow-starter candidate name: {name}")

    for name in FORBIDDEN_TOP_LEVEL:
        if (ROOT / name).exists():
            errors.append(f"seed-stage repository must not contain: {name}/")

    packs_root = ROOT / "packs"
    if packs_root.is_dir():
        for path in sorted(packs_root.rglob("*")):
            if path.is_file() and path.suffix.lower() in MANIFEST_SUFFIXES:
                relative = path.relative_to(ROOT)
                errors.append(f"manifest-like file is premature at seed stage: {relative}")

    return errors


def main() -> int:
    errors = verify()
    if errors:
        print("repository verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"repository verification passed ({len(REQUIRED_FILES)} required files)")
    print("source of truth: specs/")
    print("seed-stage boundary markers: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
