# FR-5 disposable and installed-package qualification

This gate exercises the successor installer against exact Spine
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122` (`0.10.0`, schema `19`), while
retaining v1 integration coverage on the three previously supported exact
baselines. It uses synthetic flight configuration, not curated flight content.
The normative safety boundary is in `specs/architecture.md`.

Use an isolated Python 3.12+ environment containing `build`, `hatchling>=1.27,<2`,
`setuptools>=69`, `wheel`, and `jsonschema` for official development checks.
Build dependencies may need an initial network download. Qualification itself
exports the pinned commits locally, builds with `--no-isolation`, and installs
only local wheels with `--no-index --no-deps`:

```sh
"$FR5_BUILD_PYTHON" scripts/qualify_fr5.py \
  --spine-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/spine \
  --tickerd-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/tickerd
```

`FR5_BUILD_PYTHON` is the absolute venv interpreter path. The script refuses a
non-venv interpreter or unavailable exact commits. It has no ledger-path input,
publication, source-checkout modification or dependency-download step. It never
uses a reference checkout's uncommitted files. Tickerd is exported at exact
`ffe613c65ea3d6fc70a1dc3603c32068f06350df` (`0.2.0`). The v1 Spine pins are
`72203f092de191a7633b1884bf0d61836a25abe4` (`0.3.0`),
`ab18a8a51c9bf548220f67e2db0220bfe9783888` (`0.5.0`), and
`ad1db8e1a4c7aa9a525612324d08824802a86351` (`0.6.0`).

The gate compares every installed Spine/Tickerd package file to its wheel,
export and exact Git bytes, including the complete Python module closure.
The existing FR-2 gate additionally verifies the 0.10.0 transitive contract
authority pins and historical/retired schema readback on source and installed
Spine Packs. `system.info` supplies runtime preflight, not Git provenance.

The new four-scenario v2 harness covers missing/create/retain, exact approval,
schema/rendering/profile update cascades, mixed v1/v2 profile catalogs, both
bindings, all 11 write-command response losses and exact same-execution replay,
before-submission recovery, checkpoint/result continuation, complete checkpoint
admission, read-only verify, missing execution coverage, draft refusal and
no-clobber input/output protections. Captured responses come from the real public
CLI. Both response-loss and before-submission faulted apply run in-process;
normal apply, continuation and
verify use new processes. Each scenario allocates fresh ledgers and private
synthetic owner/cursor configuration. Ledger/WAL checks inspect metadata only.

The existing four v1 integration scenarios run from source and clean wheel on
each of the three supported baselines. Package qualification compares direct and
sdist-built wheels, exact archive/resource bytes, license/dependencies and
isolated installed imports. It also requires identical candidate archives across
the v1 matrix. The installed v2 harness is taken from the extracted sdist and
uses only the installed wheel's modules/schemas. Full specs and developer
orchestration remain in the repository, outside the sdist.

All evidence remains in fresh private temporary directories, including failed
runs. The top-level `PASS.json` is emitted only after every gate passes. Build
logs, commands, provenance, CLI transcripts and per-scenario results identify
what ran. No existing/operator ledger, items, facet values, destination approvals,
reminders, notification sends, deployments or publication are part of this gate.

## Initial qualification result — retained evidence

Technical qualification passed on 2026-11-14 for the working-tree candidate
after checkpoint `1c7809309b30153c4b41db8cf5e44934cd0fd85b`. No installer runtime
repair was needed. This is not qualification of a committed release candidate.
The environment was macOS 26.7.1 arm64, Python 3.14.6, build 1.6.1, Hatchling
1.33.0, setuptools 84.2.1 and wheel 0.48.0. Official validation used jsonschema
4.26.0.

| Exact Spine runtime / schema | Source integration | Clean installed wheel |
| --- | --- | --- |
| 0.3.0 / 12, v1 installer | 4 passed | 4 passed |
| 0.5.0 / 15, v1 installer | 4 passed | 4 passed |
| 0.6.0 / 15, v1 installer | 4 passed | 4 passed |
| 0.10.0 / 19, v2 installer | 4 passed | 4 passed |

All 32 integration scenarios passed. Each v2 run covered all 11 response-loss
replays; each v1 run covered all six. Source and installed FR-2 gates also passed:
actual B1 history stays on root B with A2/B2 current heads, repeated pins are
deduplicated per pass, mixed v1/v2 catalogs paginate completely, current/historical/
retired reads work, and missing/invalid requests preserve their owning exits.
Each gate recorded 118 planner reads after the initial all-missing plan, plus
19 setup/direct calls. The reported read counter excludes that initial plan;
ledger metadata was unchanged during read-only phases.

Git/export/wheel/installed attestation covered 308 Spine files for 0.10.0, 90
for 0.3.0, 189 for 0.5.0 and 213 for 0.6.0, plus all 16 Tickerd package files in
each installation. Both FR-2 gates verified the 32 upstream contract-authority
pins. Package checks passed exact wheel/sdist membership, source/resource byte
identity, direct-versus-sdist-built wheel equality, offline installation, private
no-clobber artifacts, installed import/resource isolation, MIT metadata and zero
runtime dependencies. Candidate archives matched across all three v1 baselines.

Additional official Draft 2020-12 validation passed for all 390 saved v2
manifests/artifacts across the source and installed execution runs. Required
repository checks passed: 188 required files, 125 official contract tests without
skips, and 279 runtime tests including five new provenance rejection/control
tests. The required system-Python contract run passed with 60 development-
validator skips, covered by the official run. Ordinary integration discovery
skipped all eight opt-in tests without creating ledgers. Whitespace checks passed.

Private evidence root:
`/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr5-amr1eavd`.
It contains the top-level `PASS.json`, environment, exact command logs, upstream
provenance, three `spine-packs-package-*` runs and both v2 integration runs.
The separate FR-2 private directories are
`/private/tmp/spine-packs-fr2-gate-at_kt_7h` (source) and
`/private/tmp/spine-packs-fr2-gate-objoweuj` (installed), linked by the gate logs.
Repository test logs are retained under
`/private/tmp/spine-packs-fr5-build-wolpcmm2`.

These exact local candidate files are in each package run's `assets/` directory:

| File | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `adc18693db6d6a54cc5c5d4681a82cd4a453694220f65c510f37ebc07c69deb1` |
| `spine_packs-0.3.0.tar.gz` | `3592deb08c5ef9b1e49bcb6081ac83b6ef1293f1ba4a82a28438c32ed8ae79b5` |

The working-tree candidate retains package version `0.3.0` solely for local
qualification; no new release identity or publication is authorized. These bytes
must not replace published assets. Results do not qualify every Python/platform
combination, concurrent operators, consumer rendering or destination disclosure.
FR-6 still requires
operator decisions on fields, labels, template inclusion, profile default and
immutable pack/release identity. A final committed release candidate must be
qualified separately before tag or asset publication.

The approved bounded review returned `needs_revision`: three majors about Git
replacement refs, incomplete/skipped scenario acceptance and fresh admission of
completed checkpoints, plus three reporting/status minors. The original run
above remains retained historical evidence. Local repairs and a fresh qualification
run passed; see the repair record below. A focused external recheck
requires its own approved exact payload. After review closure,
FR-6 must resolve the curated content/distribution choices; qualification does
not approve them. No existing/operator ledger was used, no Spine checkout was
modified by this work, and no deployment, publication, commit or push occurred.

## Bounded audit repairs

The operator authorized all six repairs after the audit of checkpoint `9a96492`.
Upstream Git operations now use `--no-replace-objects`, including the inherited
FR-2 gate. A disposable Git replacement-ref regression proves original pinned
bytes govern export and attestation and replacement bytes are rejected.

Both harnesses use a shared dependency-free completion recorder. Full qualification
requires exactly the four named scenarios to succeed without scenario or subtest
skips. Focused `--test` runs remain available but cannot claim full qualification.
Package and matrix parents validate the full completion evidence before publishing
success. The helper ships beside the harnesses in the sdist, outside wheel runtime.

The update scenario now retains the original approval and completed checkpoint,
introduces live binding drift through public setup, and requires continuation to
refuse with exit 7 / `unexplained_recovery_change`, no checkpoint/result publication,
unchanged ledger metadata, and preserved source/approval bytes. It then continues
the existing explicitly approved update/verification checks.

The three reporting/status statements are corrected without changing historical
logs or approved audit payloads. No successor release or curated content is approved.

### Repair verification result

The repaired working-tree candidate after `9a96492` passed a fresh full matrix on
2026-11-14 with the same exact Spine/Tickerd pins and build tools recorded above:
all 32 scenarios across eight source/installed runs, with four required successful
identities and zero skips in every run. The package and matrix parents validated
those full-completion reports before publishing success. The separate focused
drift investigation passed one scenario and correctly retained
`full_qualification=false`; it cannot qualify a package or matrix.

Both v2 runs exercised all 11 lost-response replays and the new original-approval
completed-checkpoint refusal after live binding drift. Both FR-2 readback gates
passed with replacement objects disabled, 32 authority pins verified, and the
same post-initial-plan 118-read measurement plus 19 setup/direct calls.

Required verification passed: 190-file repository verifier, all 125 official
Draft 2020-12 contract tests without skips, and all 285 runtime tests. Those
include 11 focused provenance/completion test methods covering the real Git
replacement-ref fixture, missing/empty/duplicate scenarios, failed/errored tests,
scenario and subtest skips, focused runs and incomplete parent proof. The
required system-Python contract run passed with 60 development-validator skips,
covered by the official run. Ordinary integration discovery retained its eight
opt-in skips and created no ledgers. Whitespace checks passed.

Supplemental official schema validation passed all 390 saved v2 artifacts and
manifests from the repaired source/installed runs. This remains an additional
local check, separate from the orchestrator's built-in gates.

Fresh private evidence root:
`/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr5-22894rbq`.
Its `PASS.json` identifies all eight completion reports and three package runs;
`repair-official-schema-check.json` records the supplemental check. Source and
installed v2 evidence live under `source-v2/` and `installed-v2/`. Fresh FR-2
evidence is in `/private/tmp/spine-packs-fr2-gate-u48x2dux` and
`/private/tmp/spine-packs-fr2-gate-zi0fct4b`, linked from the gate logs. Required
check logs use the `repair-*` names in
`/private/tmp/spine-packs-fr5-build-wolpcmm2`. The initial focused drift evidence
is `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr5-integration-hz7iyy17`.

Candidate bytes match across the three package runs. The wheel is unchanged;
the new sdist carries the repaired harnesses and test-only completion helper:

| File | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `adc18693db6d6a54cc5c5d4681a82cd4a453694220f65c510f37ebc07c69deb1` |
| `spine_packs-0.3.0.tar.gz` | `5b4f80372a78f43c104c37bc352e68aee624d051232abc2226715476b2a08e29` |

The approved focused recheck closed four findings and reopened consistency-002
and consistency-003; see the follow-up below. Existing platform/Python limitations,
unresolved FR-6 decisions and final clean-commit release gates still apply.
The frozen 21-file audit payload and historical qualification logs are unchanged.
No installer runtime, public contract, allowlist or curated pack changed. No
commit, push, deployment or publication occurred during this repair.

## Focused recheck follow-up

The focused reviewer accepted the replacement-ref repair and the three reporting
corrections. It requested two further qualification safeguards. The operator
authorized both follow-ups and focused checks; the approved recheck payload stays
frozen in `whetstone_runs/facet-rendering-fr5-qualification-recheck-001/`.

The shared helper now owns the exact v1/v2 scenario-ID registry. Each harness
uses that registry, while package and matrix parents explicitly select the
harness they invoked. Both reported ID lists must match the independently
selected registry. Regressions reject valid v1 reports at v2 gates and the reverse,
arbitrary self-consistent IDs, and unknown or omitted parent selectors.

Before introducing drift, the update scenario reads the exact checkpoint path
that will be supplied to continuation. It requires all plan action IDs in order,
null `next_action_id`, null `unresolved_submission`, and equality with the applied
result's checkpoint. The existing original-approval, refusal, private publication,
ledger-metadata and byte-preservation assertions remain in place.

Focused follow-up checks passed on 2026-11-14:

- All 14 provenance/completion unit test methods passed, including cross-suite,
  arbitrary-ID and unknown/omitted-selector rejection. Actual retained v1/v2
  reports also passed their own selected parents and were rejected by the other
  parent. All eight prior completion reports matched the independently selected
  expected registry; this is revalidation, not execution of a new full matrix.
- The v2 update/drift scenario passed from source and a fresh installed wheel
  using the extracted new sdist harness on exact Spine 0.10.0. Both runs explicitly
  read the supplied checkpoint file before drift, verified all six plan actions
  in order, null continuation fields and equality with the applied result, then
  observed the required read-only refusal. Both are focused one-scenario runs
  with `full_qualification=false`.
- Fresh `scripts/qualify_package.py` qualification on exact Spine 0.6.0 passed
  all four installed v1 scenarios with zero skips, parent-selected v1 IDs,
  exact archive membership, offline install, installed resource isolation,
  license/dependency checks and direct/sdist-built wheel equality.
- All 288 runtime tests, all 125 official contract tests without skips,
  the 190-file repository verifier and whitespace checks passed. The required
  system-Python contract run passed with 60 development-validator skips,
  covered by the official run.

The reused isolated Spine/Tickerd installations for 0.10.0/0.6.0 were independently
reattested against the exact Git/export/wheel bytes, including the 32 FR-2
authority pins. No checkout or existing/operator ledger was modified.

Private focused evidence:
`/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr5-followup-p5wx1fxm`.
See `provenance-and-retained-completion.json`, `actual-parent-report-checks.json`,
`checkpoint-completeness-witnesses.json`, source/installed drift logs and required
test logs. The package run is `spine-packs-package-tmh1178a/`; both focused
integration directories are identified in the checkpoint witness file.

| Local candidate file | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `adc18693db6d6a54cc5c5d4681a82cd4a453694220f65c510f37ebc07c69deb1` |
| `spine_packs-0.3.0.tar.gz` | `0c7d151251eed1a7af39547a6743f6ce57bae8293548e1fc26c084dc71021f84` |

Both follow-ups are locally fixed and checked; a new independent focused recheck
remains pending separate exact-payload approval. Prior full-matrix results remain
historical evidence rather than a fresh run of these follow-ups. Frozen audit
payloads, runtime/contracts, packs and released artifacts are unchanged. No
additional reviewer, release, commit or push was performed.
