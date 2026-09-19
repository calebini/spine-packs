# Schema-15 release preparation

Prepared 2026-09-19. The proposal and pre-publication observations below are
preserved as the approval record; see the authorization update at the end for
subsequent approval and execution. This document never authorizes staging.
The source of truth remains `specs/`; release gates remain in `docs/releases.md`.

## Installer 0.2.0: ready for publication approval

Proposed tag: `installer-v0.2.0`, pointing to exact commit
`57a6776265905090534049f0943d7adcdd651d6e`. Proposed GitHub release title:
`Spine Packs installer 0.2.0`, MIT, regular release rather than prerelease.
The numeric version does not expand the qualification limits below.

The exact commit was checked out detached in a new local clone. It was clean
before and after qualification; the checkout excluded local audit payloads.
The approved bounded review had no blockers or majors; its minor and nit were
patched before this commit, without a separate follow-up audit.

Passed on that exact commit:

- repository verifier: 107 required files;
- 58 contract tests and 115 synthetic runtime tests;
- whitespace checks;
- four clean-installed real-CLI disposable-ledger scenarios on each pinned
  Spine baseline, including uncertain-response recovery for all six writes;
- exact archive membership, bundled source/schema/license bytes, MIT/version
  metadata, isolated offline installation, and entrypoint checks;
- byte-for-byte direct-wheel versus sdist-built-wheel comparison on each
  baseline, with identical release asset checksums across both runs;
- independent Draft 2020-12 meta-validation of all 12 schemas using
  `jsonschema` 4.26.0, the 35-case pack matrix, and 15 positive installer artifacts.

Schema checks are separate from lexical and semantic checks: duplicate JSON
members are rejected before schema validation, and ordering, references, and
content digests remain semantic validation requirements.

Qualification environment: macOS 26.6.2 arm64, Python 3.14.6, build 1.6.1,
Hatchling 1.32.3. External baselines:

| Component | Version / schema | Exact source commit |
| --- | --- | --- |
| Spine | 0.5.0 / 15 | `ab18a8a51c9bf548220f67e2db0220bfe9783888` |
| Spine regression baseline | 0.3.0 / 12 | `72203f092de191a7633b1884bf0d61836a25abe4` |
| Tickerd capability dependency | 0.2.0 | `ffe613c65ea3d6fc70a1dc3603c32068f06350df` |

Publish only these exact qualified assets, without rebuilding:

| Asset | SHA-256 |
| --- | --- |
| `spine_packs-0.2.0-py3-none-any.whl` | `6ce846f4b380cb6168ecc2545962a73a2a476664d04cdded0b7cb2d87f95ce6d` |
| `spine_packs-0.2.0.tar.gz` | `14938e98513dfa4e73c180b0df3ad9eaa85bc3f04ef180dc5aee1487d19839ad` |
| `SHA256SUMS` | `e06da64a1106f0e761bcfe64c5af681e708ccb7b61e4bd042b29f9a6436877a8` |

### Proposed installer release notes

Adds explicit Spine 0.5.0 / schema 15 support while retaining the pinned
0.3.0 / schema 12 baseline. Plans, approvals, continuation, and verification
bind the public ledger-instance identity on 0.5.0. Unknown runtime/schema pairs
fail closed. Public command allowlists and recovery scope are unchanged.

The installer remains standard-library-only, Python 3.11+, local POSIX, and
single-operator. Qualification above used Python 3.14.6 on macOS; it is not an
all-platform/Python matrix or Linux staging qualification. Spine is separately
provisioned. No daemon, notification worker, ledger migration, item creation,
or owner creation is included. Catalog ownership and receipts remain Spine's.
Receipt verification uses captured command responses, not independent receipt
readback. No multi-writer, remote-transport, or hostile-filesystem guarantee is
added. Curated packs are separate downloads and are not bundled in the installer.

## kinflow-starter 1.0.0: proposed promotion

Recommend promoting draft 10 to stable `1.0.0` without content changes. The
current repository still contains only drafts; no stable pack has been
materialized or published during this preparation. Candidate stable bytes were
derived and validated in memory, not installed or treated as release approval.

The only changes from draft 10 would be `pack.version=1.0.0`,
`pack.status=released`, and the recomputed content digest. All 52 archetypes,
52 archetype-specific profiles, 52 default-binding intents, the empty dependency
list, and compatibility declarations remain identical. Drafts 1–10 are preserved.
Compatibility remains exactly Spine 0.3.0 and 0.5.0 and the existing three
content contracts. Presentation hints and other new semantics are excluded.

Proposed distribution: a separate GitHub release titled
`Kinflow Starter 1.0.0`, tagged `pack-kinflow-starter-v1.0.0` at the future
reviewed promotion commit, with `kinflow-starter.1.0.0.json` and its own
`SHA256SUMS`. This tag convention and pack publication are proposals requiring
approval, not additions to the manifest contract. The pack release should not
replace the installer as GitHub's latest installer release.

Proposed manifest identity:

- source draft-10 file SHA-256:
  `5fc5b139e54c49f565219c5fe65cc3e4b29f4419a53e646c83fe1dbad825569b`;
- stable content digest:
  `65d489a84b75ff0051f9df4a507f7104288c58bdda51d0096b030b5a104b5dfb`;
- proposed JSON file SHA-256:
  `a0d73767e5fdfe91080328bf7486734d283c134bb57db76c0af95d9644917d9f`;
- file length: 117621 bytes, serialized as Python
  `json.dumps(candidate, ensure_ascii=False, indent=2)` followed by one newline.

The pack checksum file will contain exactly this line and a trailing newline:

```text
a0d73767e5fdfe91080328bf7486734d283c134bb57db76c0af95d9644917d9f  kinflow-starter.1.0.0.json
```

That checksum file's own SHA-256 would be
`db201d99a55c076b11d6e43c52910486d455e56be77d32c32695eaa77f487435`.

The proposed stable content passed both independent and installer semantic
validators, official Draft 2020-12 validation, and exact unchanged-content
comparisons. Eight synthetic planning checks covered both runtime baselines,
full and granular selection, and empty and equivalent catalogs, with pagination.
Full selection proposed 156 creates/bindings on an empty catalog and no writes
on an equivalent catalog. Granular selection of birthday, flight, and
medical_appointment proposed nine actions, or none when equivalent. These are
simulated plans, not real-ledger qualification of the entire curated pack.

After promotion approval, add the stable manifest, a registered positive fixture
reference, an unchanged-content/digest regression test, and matching normative
lineage/status updates. Re-run required checks and independent pack validation
from the exact promotion commit before tagging or publishing. If bytes or
semantics differ from this proposal, stop for renewed approval. Published pack
bytes are immutable; later corrections require a new version.

## Staging handoff after publication

The Cortext1 agent should install the checksum-verified 0.2.0 wheel in an
isolated tool environment, obtain the separately released pack, and stop after
producing a read-only plan for operator approval. It must first establish:

1. The actual staging runtime/schema, CLI path/hash, normalized local host,
   ledger path, and public ledger-instance identity. Schema 15 alone is not
   sufficient; the supported runtime and contract union must also match.
2. An explicitly chosen existing Spine subject or subject-group catalog owner.
   Do not infer the owner from login identity or create one via the installer.
3. Explicit selection: all archetypes, or a sorted list of archetype keys.
   Each selected archetype brings its bound profile; sections are not CLI bundles.
4. A separately confirmed existing actor subject for later apply attribution,
   not an authentication or permission claim, and a single-operator window.

Suggested first staging selection is `birthday`, `flight`, and
`medical_appointment`, covering calendar-day and elapsed schedules. This is a
recommendation only, not a selected default. The operator may choose the full pack.
The agent must surface unknown owner, actor, target, selection, or compatibility
facts rather than guess them. No production target, owner creation, migration,
delivery setup, or deployment modification is authorized by this document.

The handoff must report plan digest, exact owner/target/selection, create/retain/
drift counts, update action IDs, and blockers. Apply requires separate approval
of that exact plan and every update. It then preserves checkpoint/result evidence
and runs verify. Partial execution must not be restarted as a fresh installation.
No staging connection or installation occurred during local finalization.

## Local evidence and approval checkpoint

Private evidence root:
`/private/tmp/spine-packs-release-finalization.eStmF7/`.
The clean checkout is `source/`; independent checks and their output are
`check_release.py` and `check-release-result.json`.
Schema-15 package evidence and proposed installer assets are under
`spine-packs-package-luah0bpi/`; the schema-12 repeat is under
`spine-packs-package-ugpq1qxh/`. These paths are local evidence locations,
not reusable pack content or public download links. Keep logs, synthetic
operator artifacts, and audit payloads out of all release uploads.

Remaining operator decisions:

1. Approve installer version 0.2.0, its tag at the exact qualified commit, and
   publication of the three checksum-pinned assets above as a regular release.
2. Approve the unchanged-content pack promotion to 1.0.0 and the proposed
   separate pack tag/release/assets, conditional on exact-commit promotion gates.

Neither approval selects a staging owner or authorizes staging apply.
No tag, release, commit, push, or staging operation was performed in this pass.

## Publication authorization and promotion

Following the preparation pass above, the operator approved publishing both
releases with their named tags and exact assets. Installer `0.2.0` was published
at `installer-v0.2.0` on the qualified `57a6776` commit; all three downloaded
GitHub assets matched the approved SHA-256 values. Installer `0.1.0` was not
modified. The stable pack file has now been materialized with exactly the
approved bytes, registered as a positive contract fixture, and pinned by
unchanged-content and digest tests. The promotion commit must pass the checks
specified above before publishing its separate tag and two assets.

Installer release:
[Spine Packs installer 0.2.0](https://github.com/calebini/spine-packs/releases/tag/installer-v0.2.0).
Pack publication uses
[Kinflow Starter 1.0.0](https://github.com/calebini/spine-packs/releases/tag/pack-kinflow-starter-v1.0.0)
after those promotion gates pass. Publish the existing qualified installer
assets, not a rebuild from the later pack-promotion commit. Staging remains a
separate, explicitly targeted plan/approval/apply/verify operation.
