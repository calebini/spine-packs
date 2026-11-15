# AL-3 exact Spine 0.12.0 qualification

Status: source and installed-package technical qualification passed on
2026-11-15 following AL-2 checkpoint
`8082b5d44a1afa2343a52867e3ab5885772f3bb4`. The bounded tooling review remains
pending. This is not release or deployment approval. The normative boundary
is in `../specs/spine-0.12.0-alignment.md`.

The target is exactly Spine `3e65ef0de9e73b62047a0f6328731db08ca91023`, runtime
0.12.0, schema 20. The existing 0.10.0/schema-19 baseline and v1 0.3.0/12,
0.5.0/15 and 0.6.0/15 baselines remain in the regression matrix. Tickerd remains
exact `ffe613c65ea3d6fc70a1dc3603c32068f06350df` (0.2.0).

## Procedure

Use an isolated Python 3.12+ environment with `build`, `hatchling`, `setuptools`,
`wheel` and official `jsonschema` development validation. Separately provision
the target's dependency wheelhouse; the qualification run itself is offline:

```sh
"$AL3_BUILD_PYTHON" -m pip download --dest "$AL3_WHEELHOUSE" 'jsonschema>=4.23'
"$AL3_BUILD_PYTHON" scripts/qualify_fr5.py \
  --spine-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/spine \
  --tickerd-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/tickerd \
  --successor-runtime 0.12.0 --dependency-wheels "$AL3_WHEELHOUSE" \
  --evidence-parent "$AL3_EVIDENCE_PARENT"
```

These variables identify an isolated build interpreter and private temporary
directories, never an existing ledger. Leaving `--successor-runtime` unset
retains the historical FR-5 target. Read-only and v2 integration harnesses accept
the matching `--runtime-version` selector; it is test tooling, not an installer
CLI flag or compatibility range.

Exact exports ignore replacement refs and working-tree changes. Every upstream
package file is compared across Git/export/wheel/install, with complete module
closure. Dependency wheels are copied, hashed, installed offline and recorded.
`system.info` corroborates runtime/schema/instance identity, not a Git commit.

## Required matrix

| Exact baseline | Source | Installed wheel |
| --- | --- | --- |
| Spine 0.3.0 / 12 | Four v1 scenarios | Four v1 scenarios |
| Spine 0.5.0 / 15 | Four v1 scenarios | Four v1 scenarios |
| Spine 0.6.0 / 15 | Four v1 scenarios | Four v1 scenarios |
| Spine 0.10.0 / 19 | Nine read-only checks and four v2 scenarios | Same |
| Spine 0.12.0 / 20 | Nine read-only checks and four v2 scenarios | Same |

V2 scenarios include create/retain, approval and cascade updates, every one of
the 11 response-loss replays, before-submission continuation, complete-checkpoint
admission and drift refusal, read-only verify and artifact collision protection.
The read gate covers A2/B2 with pinned B1, actual root ownership, historical and
retired reads, deduplication, mixed v1/v2 complete pagination and stable two-pass
planning without ledger metadata changes.

The parent binds completion to the exact expected scenario IDs, baseline,
installation mode, upstream paths and installed/source resources. It separately
requires the read gate's complete named check set and exact wheel identity.
Focused, skipped, incomplete, mismatched and checkout-fallback results cannot
qualify. Source/harness inputs are fingerprinted before and after the matrix.

## Evidence and limits

The private run retains `environment.json`, `source-identity.json`, dependency
wheel hashes, per-upstream installed distribution lists and `provenance.json`,
command manifests/logs, read-gate `PASS.json`, integration `run.json`/`result.json`,
and candidate package/resource checks. The root `PASS.json` is written only
after all gates pass. Failed runs remain available and are not reused as passes.

All ledgers and owner/cursor setup are fresh, private and synthetic. Public
configuration commands only; no SQL/internal handlers, operator ledger, items,
facet values, disclosure, reminders, sends, deployment, publication, commit or
push. Protected cursor secrets are not reviewer payload material.

The tooling changes require a separately approved bounded review before release
readiness. Curated successor content and release version/publication decisions
remain outside this qualification task. Previous FR-5 evidence stays historical.

The candidate retains the existing project version `0.3.0` for local testing
only. Its rebuilt wheel/sdist are not replacement release assets. A successor
release identity and qualification of its final committed bytes remain separate
gates; this run does not approve an operating-system/Python support matrix.

## Local run

The matrix passed in `/private/tmp/spine-packs-fr5-rsacj94n`, selected with
`--successor-runtime 0.12.0`. The reused driver retains its historical `fr5`
directory prefix; `environment.json` records the actual AL-3 target. The working
candidate starts at checkpoint `8082b5d44a1afa2343a52867e3ab5885772f3bb4`, with
the qualification-tooling changes fingerprinted in `source-identity.json`.

The exact 0.12.0 export, wheel and installation agree on 490 package files,
including 197 Python modules. Its wheel SHA-256 is
`df25c188394c6adb4ea6da0c437b931c499d2fdb5424bb0e6e291412eeee0107`.
The upstream proof is `spine-0.12.0/provenance.json`; dependency identities and
hashes are in `spine-0.12.0-dependencies.log` and `dependency-wheels.json`.
Recorded dependency versions are jsonschema 4.26.0, attrs 26.1.0,
jsonschema-specifications 2025.9.1, referencing 0.37.0 and rpds-py 2026.9.1.
All corresponding installations passed `pip check`.

The environment is macOS 26.7.1 arm64 / Python 3.14.6, build 1.6.1, Hatchling
1.33.0, setuptools 84.2.1 and wheel 0.48.0. Official development schema
validation uses jsonschema 4.26.0. Required checks passed 140 official contract
tests without skips and 312 runtime tests, including the five new AL-3 tooling
methods; all 14 existing provenance/completion methods also passed separately.
The 204-file repository verifier and whitespace checks passed. Log hashes and
paths are retained in `repository-checks.json` under the run root.

The root `PASS.json` links all 14 gates and three package runs. All 40 integration
scenarios passed across ten runs, with the four parent-selected scenario IDs
and zero skips in each. All four read-only gates passed their nine required
checks (36 checks). Each v2 source/installed run covered all 11 write-response
losses and exact replay (44 replay cases), including fresh admission of an
original complete checkpoint after live drift. All v1 source/installed
regressions passed at the three preserved pins.

Each read gate verified the 32 contract-authority pins, recorded 19 setup/direct
calls and 118 planner reads after the initial all-missing plan, and confirmed
unchanged ledger metadata during read-only phases. The source snapshot remained
unchanged through the full matrix. Direct and sdist-built wheels agree, package
code/resources match source bytes, isolated installed imports work, and Spine
Packs still declares zero runtime dependencies. Candidate assets are identical
across all three package runs:

| Local candidate file | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `55ba2a6e7b1ba9cc7a2ae935b80865e9491f5b32304366aa06b00faba1386758` |
| `spine_packs-0.3.0.tar.gz` | `52f94eecbdf61f8490ccff84f3531f0e5b6e792097d71a5f81ae1d643187fc8e` |
| `SHA256SUMS` | `c7aee0c2e7f03af5c5694f29787320c384358033daaed90b707c984cef6720ab` |

An independent post-run check revalidated all parent-selected gates, actual
installed/source identities, exact upstream wheel hashes, all 44 replay-write
entries, unchanged source inputs and identical assets. Official Draft 2020-12
validation and the independent contract oracle passed all 780 saved v2
manifests/artifacts from the four execution runs. The supplemental report is
`qualification-summary.json`; its verifier is retained separately at
`/private/tmp/spine-packs-al3-final-verification.py` with a hash in that report.

No installer runtime repair was needed. No released pack or published package
asset was changed, and the reference Spine checkout's pre-existing working-tree
changes were preserved. The next gate is a bounded review of the AL-3 tooling
and qualification evidence, requiring fresh exact-payload approval. Curated
successor content and final committed release qualification remain separate.
