# AL-3 exact Spine 0.12.0 qualification

Status: source and installed-package technical qualification passed on
2026-11-15 following AL-2 checkpoint
`8082b5d44a1afa2343a52867e3ab5885772f3bb4`. The bounded tooling review returned
`needs_revision` (four majors and three minors). The operator authorized their
bounded repairs, focused checks and affected qualification reruns. Review
closure remains pending. This is not release or deployment approval. The normative boundary
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
losses and exact replay (44 replay cases), including fresh admission refusing
the original complete checkpoint after live binding drift. All v1 source/installed
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

## Authorized audit repairs

The original approved payload and `needs_revision` verdict remain frozen in
`whetstone_runs/spine0120-al3-qualification-audit-001/`. Its sixteen outgoing
files were the audit notes plus fifteen numbered specs/support files. No file
was missing; future recheck descriptions must state that count explicitly.

C01 binds every v1 source/installed run to a parent-selected runtime/schema/pin,
mode, executable paths and code/schema resources. The v1 harness and package
qualifier now require `--runtime-version`; they never select compatibility from
the observed runtime. The matrix checks every v1 cell; the package parent also
checks its installed cell.
C02 checks exactly eleven unique replay commands against the selected reviewed
inventory inside matrix admission, before publishing root `PASS.json`.
C03 checks both observation passes' actual profile-list cursor chains, stable
query/snapshot and all three seeded key/root/revision/contract identities before
claiming mixed-catalog pagination. C04 compares pinned project entry points with
wheel/installed metadata and checks both actual launchers' interpreter and
dispatch syntax. Interpreter, metadata and launcher hashes are recorded and
rechecked before gates and before the matrix pass.

C05 supplies the narrow independent-oracle helper excerpts: official
`Draft202012Validator.validate` raises on failure, as do semantic `require`
checks; neither helper returns an ignored collection of errors. C06 corrects
the completed-checkpoint drift account to refusal above. C07 clarifies the
notes-plus-fifteen count without changing the original approved payload.
Local clarification evidence is retained under that audit's `repair-evidence/`.

Focused regressions and a fresh full source/package matrix are required for
these repairs. Their local success does not close the external audit gate or
authorize another reviewer, commit, push, release or deployment.

## Repair verification result

The repaired working-tree candidate after checkpoint `1abb2d6` passed a fresh
full matrix at `/private/tmp/spine-packs-fr5-o3m6xkrj`. Every ledger was newly
allocated. All ten source/installed runs passed their four parent-selected
scenario IDs without skips (40 scenarios); all four read gates passed nine
checks (36 checks). Each of four v2 runs passed all eleven actual response-loss
replays (44 cases), now admitted against the selected inventory before root
success. The matrix parent checked all six v1 identities; the package parent
also checked each of the three installed identities.

Both read-gate modes at each exact v2 baseline proved the three seeded profiles'
key/root/revision/contract identities in both observation passes. Page size 1
produced three pages per pass; page size 100 produced one. Exact B1/root-B
history, retired reads, deduplication and unchanged-ledger checks also passed.
All five upstream installations were attested against exact Git/export/wheel/
installed bytes and console-entry mappings. Interpreter, launcher and metadata
identities remained unchanged through the matrix. The checker accepts the
recorded Python-launcher form and fails closed on unknown forms; this is
qualification of the recorded toolchain, not every pip/platform combination.

Required checks passed: 140 official contract tests without skips, 320 runtime
tests, 13 focused AL-3 methods, 14 preserved provenance/completion methods, the
204-file repository verifier and whitespace checks. The system-Python contract
run passed with 75 development-validator skips covered by the official run.
An independent post-run check revalidated every source/installed identity,
upstream console proof and replay list. Official schema/oracle validation passed
all 780 saved v2 manifests/artifacts, with exact helper hashes recorded in
`qualification-summary.json`. Its verifier is
`/private/tmp/spine-packs-al3-repair-final-verification.py`.

The matrix's `PASS.json`, `source-identity.json`, `repository-checks.json`,
per-upstream `provenance.json`, read-gate proofs and integration run/result files
retain the complete links. Source inputs stayed unchanged. Direct and
sdist-built wheels agree, resources/import isolation and zero runtime
dependencies passed, and all three package runs produced identical assets:

| Local repaired candidate file | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `55ba2a6e7b1ba9cc7a2ae935b80865e9491f5b32304366aa06b00faba1386758` |
| `spine_packs-0.3.0.tar.gz` | `f4870ece8e1d082c676f46878dde3ac12a8975cfb9ef6f3d19769e83b30fc356` |
| `SHA256SUMS` | `46faec63978f7b4c8302d77cae3a91b925e53067896d2bcf022a362b504b5f1e` |

The wheel equals the earlier local AL-3 candidate; the sdist carries the tooling
and procedure repairs. No published asset is replaced. No installer runtime,
released pack or Spine checkout was changed. The original audit payload and
`needs_revision` verdict remain preserved. A separately staged and approved
focused recheck is still required; local repairs do not close that gate.

## Focused-recheck follow-up

The approved fourteen-file recheck returned three majors and three minors. Its
payload and verdict remain unchanged in
`whetstone_runs/spine0120-al3-qualification-recheck-001/`. The operator authorized
the six narrow follow-ups plus focused/required checks, affected qualification
and preparation of another focused recheck. A changed outgoing payload still
requires exact approval; no reviewer rerun is implied by local checks.

C01-module derives purelib from the selected clean interpreter and compares
exact resolved `spine_packs/artifacts.py` and `_schemas` paths. A coordinated
move elsewhere inside the same prefix fails. C01-installer compares the normal
integration's recorded installer argv with the selected source interpreter/
module command or clean installed CLI. Direct read-only gates check installation
identity without pretending to execute the installer CLI. C03-limit binds every
profile-list request to its expected limit, rejecting full seed coverage with
a consistent wrong limit. C04-mode repeats regular-file and execute-permission
checks after attestation. C01-account distinguishes all six matrix-parent checks
from the package parent's three installed checks. C06-excerpt requires the next
payload to include the actual corrected Local run sentence and its source hash.

All 17 focused methods and the 14 preserved provenance/completion methods passed.
Recorded correct identities from the prior run also pass the stricter path and
argv checks; this is a smoke check, not fresh qualification. The subsequent fresh
matrix passed at `/private/tmp/spine-packs-fr5-k1a7z26g`: 40 scenarios across ten
full source/installed runs without skips, 36 read checks and all 44 v2 replay
cases. Matrix and package parents checked exact locations and installer argv;
all four read gates enforced actual expected limits. Console regular-file and
execute checks, source fingerprints and matching candidate archives passed.

Required checks passed 140 official contract tests without skips, 324 runtime
tests, the 17 focused methods, 14 preserved provenance/completion methods, the
204-file verifier and whitespace checks. The system contract run's 75 validator
skips are covered by the official run. An independent post-run check validated
all identities and console proofs, recorded parent-derived installed locations
and installer argv, and checked the actual profile-list request limits. Official
schema/oracle validation passed all 780 saved v2 manifests/artifacts. These
proofs, exact helper hashes and verifier identity are in the run's
`qualification-summary.json`; the verifier is
`/private/tmp/spine-packs-al3-followup-final-verification.py`.

The local runtime wheel remains identical to the earlier AL-3 candidates;
the sdist carries the follow-up tooling. All three v1 package runs agree on:

| Local follow-up candidate file | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `55ba2a6e7b1ba9cc7a2ae935b80865e9491f5b32304366aa06b00faba1386758` |
| `spine_packs-0.3.0.tar.gz` | `c0d0c6242b9b186e0b68b6a207a362f8b1023d065002280987887f692c8ec1f5` |
| `SHA256SUMS` | `eb04084b5dbd682b2d33374b9fb0155fd99ff41e7ec144f9de87325c4fefdc0e` |

No installer runtime, contract, released pack, Spine checkout or published asset
was changed. Both earlier external verdicts and approved payloads are preserved.
Follow-up evidence is under the first recheck's `followup-evidence/`. A fresh
focused payload still requires approval before another reviewer invocation;
these local results do not close either external verdict or authorize commit,
push, release or deployment.

## Remaining-gap repair scope

The second focused recheck returned two majors and two evidence-reference
minors. Its fourteen-file payload and verdict remain frozen under
`whetstone_runs/spine0120-al3-qualification-recheck-002/`. The operator authorized
the two tooling fixes, consistent evidence packaging, focused checks and staging
another recheck. No new reviewer is authorized by these local repairs.

Every `plan(limit)` now constructs a limit-checked public read adapter. Its
profile-list guard runs before transport and capture, including the initial
empty plan and final retired plan; seeded cursor/identity checks remain in place.
Expected code/schema child paths stay fixed under resolved purelib, while
observed paths resolve before comparison. A real package-directory symlink to
another directory within the same prefix is rejected. Evidence sources are
validated against the selected summary's verifier hash and each check's exact
log path/hash/count before the staging builder includes excerpts.

All 20 focused methods passed. Required full checks, fresh source/installed
read gates at both exact v2 pins and a fresh installed-package gate are the
affected validation scope. The unchanged runtime wheel, harness execution and
previous full-matrix results are retained historical evidence; this increment
does not relabel them as a fresh full matrix or qualify a committed release.

### Remaining-gap validation result

Targeted repair qualification passed in
`/private/tmp/spine-packs-al3-narrow-lbil0yj6`. A fresh clean-wheel package gate
against exact Spine 0.6.0 passed all four scenarios. Fresh source and installed
read gates at exact 0.10.0 and 0.12.0 passed all 36 checks, exercising every
`plan(limit)` through the capture-time guard, including empty and retired plans.
All ledgers were newly allocated. Retained isolated upstream packages and console
launchers were reattested against their exact Git/export/wheel/installed bytes.

All 20 focused tests, 14 preserved provenance/completion tests, 140 official
contract tests and 327 runtime tests passed. The repository verifier and
whitespace checks passed. The targeted verifier binds current log paths, hashes
and test counts and its own source hash before publishing the targeted pass.
The new staging guard rejects old verifier files, old logs and mismatched counts.

The full-matrix execution from `spine-packs-fr5-k1a7z26g` remains historical.
Its runtime wheel and both child harnesses are byte-identical to this candidate;
the completion recorder/checker definitions are unchanged. All ten retained
execution reports passed current parent identity admission. This does not claim
that their 40 scenarios or 44 v2 replay cases ran again in this increment. A
final committed release candidate still requires its separate qualification.

The targeted result is `qualification-summary.json`; `repository-checks.json`
names the actual current logs, and `evidence-references.json` binds those files
to their source hashes/counts. Its actual verifier is `verify.py` inside the new
targeted run directory. Staging must use these metadata paths and hashes, not
earlier repair/follow-up filenames. Both earlier full matrices and all three
external verdicts/payloads remain unchanged. No installer runtime, contract,
released pack, Spine checkout or published asset changed; no commit or push ran.

## Evidence-guard minor follow-up

The separately approved third focused recheck returned
`pass_with_minor_clarification`, with zero majors, four minors and
`boundary_preserved=true`. Neither previous major was reopened. Its payload and
verdict remain frozen in
`whetstone_runs/spine0120-al3-qualification-recheck-003/`.

The operator authorized all four minor repairs and focused checks. The guard
now takes the expected count and successful status from the same terminal
unittest summary. Its failure-status fixture records the failed log's actual
digest and correct path/count. Supplied suite names must exactly match the
selected checks. A summary's current verifier path must match after resolution,
alongside its hash; historical hash-only metadata remains supported.

All 23 focused methods, 14 preserved provenance/completion methods, 140 official
contract tests and 330 runtime tests passed. A new clean-wheel package gate on
exact Spine 0.6.0 passed four scenarios, using only new disposable ledgers. This
also checked the changed helper in the sdist and installed harness. The runtime
wheel remains unchanged. No fresh read gates, full qualification matrix or
release qualification is claimed for these evidence-guard-only repairs.

The actual verifier, log metadata and package proof are retained in
`/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-al3-minor-followup-clhezgfe/`.
The prior four approved payloads/verdicts and earlier qualification records
remain unchanged. These local checks are not another external review. No
installer runtime, contract, released pack or Spine checkout was modified;
no external reviewer, commit, push, deployment or publication was invoked.
