#!/usr/bin/env python3
"""Verify the draft-contract Spine Packs repository shape and boundaries."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "contracts/pack-fixture-manifest.v1.json",
    "contracts/schemas/spine-pack-manifest.v1.schema.json",
    "packs/kinflow-starter/README.md",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.2.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.3.json",
    "scripts/verify_repo.py",
    "specs/architecture.md",
    "specs/compatibility.md",
    "specs/kinflow-starter.md",
    "specs/overview.md",
    "specs/pack-format.md",
    "tests/contract/test_pack_manifest_contract.py",
    "tests/fixtures/pack-manifest/positive/medical_vertical_slice.json",
    "tests/fixtures/pack-manifest/positive/medical_and_lesson.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_3.json",
    "tests/fixtures/pack-manifest/negative/birthday_embedded_timezone.json",
    "tests/fixtures/pack-manifest/negative/birthday_profile_recurrence.json",
    "tests/fixtures/pack-manifest/negative/duplicate_archetype_key.json",
    "tests/fixtures/pack-manifest/negative/duplicate_json_object_member.json",
    "tests/fixtures/pack-manifest/negative/embedded_owner_data.json",
    "tests/fixtures/pack-manifest/negative/incompatible_item_types.json",
    "tests/fixtures/pack-manifest/negative/incorrect_content_digest.json",
    "tests/fixtures/pack-manifest/negative/invalid_grace_window.json",
    "tests/fixtures/pack-manifest/negative/invalid_notification_offset.json",
    "tests/fixtures/pack-manifest/negative/lesson_profile_recurrence.json",
    "tests/fixtures/pack-manifest/negative/multiple_defaults_for_archetype.json",
    "tests/fixtures/pack-manifest/negative/noncanonical_array_ordering.json",
    "tests/fixtures/pack-manifest/negative/unknown_fields.json",
    "tests/fixtures/pack-manifest/negative/unresolved_binding_reference.json",
    "tests/fixtures/pack-manifest/negative/version_status_mismatch.json",
)

REQUIRED_MARKERS = {
    "README.md": (
        "Spine remains the sole authority",
        "Direct database access is forbidden",
        "`plan`",
        "`apply`",
        "`verify`",
        "draft-contract",
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
        "exact Spine runtime versions",
        "exact Spine content-contract identifiers",
        "Fail-closed behavior",
    ),
    "specs/pack-format.md": (
        "`spine.pack-manifest.v1`",
        "Every object is closed",
        "Deterministic ordering",
        "Content identity",
        "Deferred decisions",
    ),
    "specs/kinflow-starter.md": (
        "1.0.0-draft.3",
        "Lesson notification profile",
        "Game or competition",
        "Flight",
        "Birthday",
        "Spine-owned item state",
    ),
    "contracts/schemas/spine-pack-manifest.v1.schema.json": (
        "https://json-schema.org/draft/2020-12/schema",
        "spine.pack-manifest.v1",
        "additionalProperties",
    ),
    "tests/contract/test_pack_manifest_contract.py": (
        "Dependency-free contract checks",
        "validate_pack",
        "content_digest",
    ),
}

PACK_ARCHETYPE_NAMES = (
    "medical_appointment",
    "lesson",
    "passport_renewal",
    "game_or_competition",
    "flight",
    "birthday",
)

FORBIDDEN_TOP_LEVEL = (
    "adapters",
    "examples",
    "models",
    "services",
    "src",
)


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
        for name in PACK_ARCHETYPE_NAMES:
            if f"`{name}`" not in text:
                errors.append(f"missing kinflow-starter archetype name: {name}")

    for name in FORBIDDEN_TOP_LEVEL:
        if (ROOT / name).exists():
            errors.append(f"draft-contract repository must not contain: {name}/")

    packs_root = ROOT / "packs"
    if packs_root.is_dir():
        alternate_manifests = sorted(
            path.relative_to(ROOT)
            for path in packs_root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".toml", ".yaml", ".yml"}
        )
        for relative in alternate_manifests:
            errors.append(f"v1 packs must use JSON, found alternate manifest: {relative}")

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
    print("draft-contract boundary markers: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
