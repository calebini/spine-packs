# Spine 0.12.0 compatibility alignment

Status: AL-0 source comparison complete; the operator subsequently selected the
exact candidate and authorized AL-1 contracts/fixtures. The approved AL-1 audit
returned findings; the operator authorized narrow local repairs and preservation
clarification. The separately approved focused recheck returned
`pass_with_minor_clarification` with preserved boundaries; its remaining test
assertion is now added under operator authorization. No new runtime admission,
staging package identity or baseline
qualification is claimed. Normative extension: `../specs/spine-0.12.0-alignment.md`.

The operator requested compatibility alignment after FR-5's approved two-finding
recheck passed with zero findings at `6ebc1cc`. The exact qualified baseline
remains Spine `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`,
ledger schema `19`. The inspection candidate is exact locally available commit
`3e65ef0de9e73b62047a0f6328731db08ca91023`, runtime `0.12.0`, schema `20`.
Its committed metadata and schema declaration were checked through Git objects
with replacement objects disabled. No uncommitted Spine files or implicit HEAD
substitution were used. The reference checkout has unrelated working-tree changes.

At inspection time, exact target selection was pending. The operator subsequently
selected this commit for alignment. That selection does not attest an installed
staging package or make the source comparison runtime qualification. The JSON
record remains the original candidate-only inspection, including its unconfirmed
staging-identity flag; it is not rewritten as qualification evidence.

## Evidence and scope

`spine-0.12.0-alignment.json` records full old/new file hashes, the selected
registry projection, metadata/dependency comparison and implementation-file
comparison. This is inspection evidence, not an installer command inventory or
public machine contract.

- **31 of 32 existing authority files are byte-identical.** All 20 public JSON
  source-schema files in the old closure, the historical revision-readback
  contract/fixtures and installed revision-readback authority files are unchanged.
  The only changed file among the 32 is `src/spine/commands/registry.py`.
- **The selected registry projection is unchanged:** 23 configuration/read
  commands, 12 reads, 11 writes and the same exact 18-contract execution union.
  Static AST inspection examined literal requirement groups, successor additions,
  access modes and the unchanged prerequisite assembly helpers. It imported or
  executed no Spine code. It cross-checked the old union against our pinned
  inventory before comparing the candidate. Newly added people/recurring-task
  commands do not enter our existing boundary.
- **Several direct implementations are unchanged:** profile commands,
  rendering-profile/catalog commands, facet reads/runtime and core facet types.
  CLI dispatch, the core dispatcher, facet command integration and some ledger
  helpers changed. Equal public schemas do not prove equal runtime behavior.
- **The environment changed:** runtime `0.10.0` → `0.12.0`, ledger schema
  `19` → `20`, and Spine now declares `jsonschema>=4.23` as a runtime dependency.
  Spine Packs still has no runtime dependencies. Isolated Spine qualification
  must provision and record Spine's dependency closure before offline install.

No public-contract mismatch was found in the selected source closure. This is
not a public-CLI gate or general compatibility proof. No ledger was opened,
created or migrated and no Spine process was invoked during this inspection.

## Smallest proposed alignment surface

For the selected exact target, keep the existing 23 commands and 18 contracts
unless contrary public evidence requires an explicit contract change. Preserve
all 0.9.1/0.10.0 schemas, inventories, fixtures, reviews and qualification history.
Do not overwrite released/draft pack bytes or widen v1 compatibility.

The minimum changes to specify and review are:

1. An additive exact-target inventory/readback closure with candidate source,
   registry and packaged-authority pins. Reuse identical schema fragments through
   offline references rather than maintaining divergent copies.
2. Exact `0.12.0` / `20` manifest/artifact admissibility and matching execution
   union, saved environment and captured-response verification label. Historical
   encodings stay decodable and retain their original labels/digests. No runtime
   ranges, automatic artifact migration or relabelled historical approvals.
3. Reviewed baseline selection that retains the qualified 0.10.0 behavior while
   admitting the new exact target. Existing capabilities are preserved; retiring
   an old baseline is outside this additive alignment. Plans, approvals,
   continuations and results must remain bound to their exact baseline.
4. New synthetic create/update/recovery/verification fixtures and negative cases
   for wrong runtime/schema pairing, unavailable contracts, mixed-baseline source
   evidence/approval, stale plans and mismatched verification labels. Keep existing
   provenance, parent suite-identity and completed-checkpoint regressions.
5. Baseline-specific transport/serializer/validator routing, replacing scattered
   hard-coded 0.10.0 checks only after the contract/fixture boundary is reviewed.
   Preserve read-only planning/verify and the separate 11-write adapter.
6. Exact-target source and installed-wheel configuration-only qualification on
   disposable schema-20 ledgers, all 11 response-loss replays, original-approval
   continuation, explicit complete-file drift refusal and v1 regression checks.
   Use Git exports, replacement-disabled attestation and protected synthetic setup.
   Record current dependency wheels and installed provenance; no checkout mutation.

This alignment adds no people/recurring-task provisioning, destination disclosure,
item/facet-value authoring, scheduling, materialization, sends or migration of an
existing/operator ledger. Spine alone owns its schema migration and behavior.

## Ordered bounded increments

| Increment | Deliverable | Gate |
| --- | --- | --- |
| AL-0 — exact candidate inspection | This report and hashed source comparison; preserve the FR-5 closure | Complete; the operator subsequently selected this exact target |
| AL-1 — additive machine agreements | Exact inventory/closure, baseline-selection rules, artifact schema pairs and fixtures | Official meta/semantic tests, unchanged historical vectors, bounded contract review with separately approved payload |
| AL-2 — runtime compatibility routing | Plan/apply/continuation/verify use the selected exact baseline's reviewed schemas and environment | Focused runtime regressions and boundary review; no new command authority |
| AL-3 — independent qualification | Isolated exact-target public-CLI source/installed runs and supported-baseline regressions | Recorded passing gates and scoped review before release readiness |

FR-6 flight content and release publication follow alignment. A final committed
release candidate still needs its release gates and explicit publication/deployment
approval. This initial inspection has made no release, commit, push, deployment
or external reviewer invocation.

## Kickoff verification

Required checks passed after the documentation/evidence update: repository
verification (192 required files), 125 official Draft 2020-12 contract tests
without skips, 288 runtime tests and whitespace checks. The required system-
Python contract run passed with 60 development-validator skips covered by the
official run. These are regressions of the existing supported behavior, not
qualification of the candidate Spine runtime.

The JSON inspection record was checked for 32 authority entries, the 31/1
unchanged/changed split, 23 selected commands, 12/11 read/write split, identical
18-contract unions, exact source schema declarations 19/20 and unconfirmed
staging identity. All three approved FR-5 audit payloads remain hash-identical.
No file under `src/`, `contracts/` or `packs/` changed. No Spine runtime or ledger
was invoked. Logs are retained at:

- `/private/tmp/spine-packs-alignment-initial-contract-system.log`
- `/private/tmp/spine-packs-alignment-initial-contract-official.log`
- `/private/tmp/spine-packs-alignment-initial-runtime.log`

## Operator selection and AL-1 progress

On 2026-11-15 the operator selected exact
`3e65ef0de9e73b62047a0f6328731db08ca91023` (0.12.0/schema 20) and authorized the
contract/fixture slice. AL-1 adds a separate inventory/offline closure, exact
v2 manifest/environment/verification-label variants, a compact derivation fixture
and independent semantic contract tests. The fixture pins new artifact/wire
digests for both flows, 36 recovery boundaries and 25 negative vectors while
preserving all previous inventories, saved fixtures and pack bytes.

No additional product decision is needed for AL-1. Existing 0.10.0 capabilities
are retained. The next gate is a separately approved focused contract recheck;
AL-2 runtime routing and AL-3 installed-package qualification follow. The exact
deployed staging package must still be attested before installation. No content
or disclosure policy was invented in this compatibility slice.

## AL-1 verification

All required checks passed: repository verifier (199 required files), 134
official Draft 2020-12 contract tests without skips, 288 runtime tests and
whitespace checks. The system-Python contract run passed with 69 development-
validator skips, all covered by the official run. Nine new contract methods
exercise 36 recovery boundaries and all 25 indexed negative vectors, including
the unchanged runtime's refusal before transport use. Exact replacement-disabled
Git checks matched all 34 upstream schema/registry/package/identity source hashes.

The package/resource gate passed against the already supported exact Spine
0.6.0 pin: wheel/sdist builds, archive/resource equality, clean install, help,
dependency checks and all four installed v1 integration scenarios without skips.
Those tests allocated fresh disposable configuration-only ledgers through public
CLIs. Reused upstream wheels/installations were reattested against fresh exact
Git exports, leaving the partially cleaned earlier exports untouched. No Spine
0.12.0 process or ledger was invoked. This gate preserves packaging behavior;
it is not AL-3 qualification or permission to replace released 0.3.0 assets.

Evidence:

- `/private/tmp/spine-packs-al1-contract-system.log`
- `/private/tmp/spine-packs-al1-contract-official.log`
- `/private/tmp/spine-packs-al1-runtime.log`
- `/private/tmp/spine-packs-al1-source-verification.json`
- `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-al1-package-sp0xu37q/upstream-provenance.json`
- `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-al1-package-sp0xu37q/spine-packs-package-_a49c1gr/PASS.json`

Runtime source, package metadata and every reusable pack artifact remain
unchanged. Old inventories, readback closures, saved fixtures and all v1 schema
hashes are checked by the new fixture index. At that checkpoint no external
review, commit, push, deployment or publication had occurred.

## AL-1 bounded audit and authorized repairs

The approved 14-file Whetstone audit returned `needs_revision`: two major and
three minor findings. Its payload and verdict remain frozen under
`../whetstone_runs/spine0120-al1-contract-audit-001/`. The operator authorized
patching F01/F02/F04/F05 and clarifying F03 while preserving existing behavior.

- F01: the provisional rendering-record oracle now uses the context-selected
  public-schema helper. A regression checks both create/publish candidates in
  both 0.12.0 and 0.10.0 contexts.
- F02: `stale_preimage` now adds valid unrelated catalog drift, recomputes its
  fingerprints/digest, proves observation and lineage validity, and asserts the
  exact continuation comparison failure.
- F04: absent action-bearing result evidence explicitly requires `missing`
  coverage and `mismatch`, distinct from invalid supplied evidence.
- F05: the alignment specification now supplies the precise inherited public
  code/field/CLI-exit to installer-category/exit mapping and names the existing
  mapping/malformed-envelope regression methods. No failure owner changed.
- F03: the specification and oracle comments clarify the existing distinction:
  invalid embedded correlation yields invalid coverage/mismatch after valid
  observation; known immutable revision contradictions in fresh readback still
  abort under the environment contract without a verification artifact. Two
  added indexed vectors and a both-flow regression preserve that behavior and
  observation-failure precedence. This addresses missing preservation context;
  the reviewer's proposed behavior change was not applied.

The new draft index now covers 27 negative vectors. Both flow derivations,
expected artifact/wire digests, the 36 recovery boundaries, historical fixtures,
command inventory, schemas, runtime source and reusable packs are unchanged by
these repairs. Existing qualification/review history is retained; local repair
success does not change the original audit verdict or qualify 0.12.0 runtime.

### Local repair checks

All 17 focused methods passed: 11 official AL-1 contract methods (including all
36 recovery boundaries and 27 negative vectors), the existing immutable-revision
contract regression, two revision-readback failure/malformed-envelope runtime
methods and three verification failure/precedence runtime methods. The complete
official contract suite passed all 136 tests without skips; all 288 runtime
tests passed. The required system-Python contract run passed with 71 development-
validator skips, covered by the official run. Repository verification (199 files)
and whitespace checks passed.

Integrity checks preserved all 14 original approved payload files, their prompt
and launch controls, plus all 40 indexed historical inventory/fixture/pack/schema
pins. The current 48 packaged modules/schemas and every source member in the
retained qualified sdist match their previously qualified bytes. This repair
changes no packaged input, so no new package build/qualification was needed.
No Spine process or ledger was invoked; no external recheck, commit or push ran.

Logs and integrity proof:

- `/private/tmp/spine-packs-al1-repairs-focused-contract.log`
- `/private/tmp/spine-packs-al1-repairs-focused-inherited-contract.log`
- `/private/tmp/spine-packs-al1-repairs-focused-readback.log`
- `/private/tmp/spine-packs-al1-repairs-focused-verification.log`
- `/private/tmp/spine-packs-al1-repairs-contract-official.log`
- `/private/tmp/spine-packs-al1-repairs-contract-system.log`
- `/private/tmp/spine-packs-al1-repairs-runtime.log`
- `/private/tmp/spine-packs-al1-repairs-integrity.json`

Next is a separately approved focused recheck of these repairs and the clarified
failure ownership. Local tests do not mark the external findings closed or open
AL-2 runtime routing.

## Focused recheck and final minor follow-up

The approved recheck in `../whetstone_runs/spine0120-al1-contract-recheck-001/`
returned `pass_with_minor_clarification`: no blockers or majors, one minor,
`boundary_preserved=true`. It accepted the clarified failure ownership. F03's
remaining minor was limited to the missing invalid captured-evidence assertion
for flight-create; flight-update already exercised it.

The operator authorized that narrow fix and focused checks. The existing indexed
`invalid_same_plan_evidence` vector now iterates both named synthetic flows.
Each case reseals the outer checkpoint/result after changing embedded receipt
correlation, independently validates that artifact and the fresh observation,
then requires both `response_evidence=invalid` and `state=mismatch`. The inherited
immutable-revision failure behavior remains unchanged. No schema, inventory,
saved fixture, runtime, package input or pack content changed in this follow-up.

The original audit and recheck payloads/reports remain frozen. This local
follow-up does not relabel the external verdict as a zero-finding pass, run
another reviewer, or begin AL-2 runtime implementation.

### Final follow-up verification

All 11 focused alignment methods passed. A direct witness of the indexed case
confirmed that both create and update execute the invalid-coverage/mismatch
assertions. All 136 official contract tests passed without skips; the required
system-Python run passed with 71 development-validator skips covered by the
official run. The final full runtime run passed all 288 tests. Repository
verification (199 files) and whitespace checks passed.

Two earlier full runtime attempts hit the existing subprocess success case's
0.5-second startup deadline; its isolated rerun passed. The test harness now
allows five seconds for ordinary subprocess cases while retaining 0.5 seconds
for the explicit two-second-sleep timeout probe. That focused method and the
subsequent full runtime run passed. Production timeouts are unchanged. Both
failed logs remain available; this is test-harness stabilization, not an installer
runtime change or new baseline qualification.

Both approved 14-file audit payloads/controls, all 40 historical machine/pack
pins, the draft fixture, all 48 packaged modules/schemas and sdist inputs remain
unchanged. No package rebuild, Spine invocation, external review, commit or push
ran in this follow-up.

Evidence:

- `/private/tmp/spine-packs-al1-final-minor-focused.log`
- `/private/tmp/spine-packs-al1-final-minor-both-flow-witness.json`
- `/private/tmp/spine-packs-al1-final-minor-contract-official.log`
- `/private/tmp/spine-packs-al1-final-minor-contract-system.log`
- `/private/tmp/spine-packs-al1-final-minor-runtime.log` (first failed attempt)
- `/private/tmp/spine-packs-al1-final-minor-runtime-serial.log` (second failed attempt)
- `/private/tmp/spine-packs-al1-final-minor-timeout-recheck.log` (isolated pass before stabilization)
- `/private/tmp/spine-packs-al1-final-minor-timeout-stabilized.log`
- `/private/tmp/spine-packs-al1-final-minor-runtime-stabilized.log` (full pass)
- `/private/tmp/spine-packs-al1-final-minor-integrity.json`

The remaining minor is addressed locally. The external verdict remains
`pass_with_minor_clarification`; AL-2 implementation is the next separately
scoped increment.
