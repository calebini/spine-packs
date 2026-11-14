# Installer Implementation Plan

## Status and authority

This document sequences implementation of the installer contract in
`specs/installer.md` and `specs/installer-artifacts.md`. Those documents remain
normative when this plan is incomplete or imprecise. A listed slice is not
authorization to implement it; each slice requires separate review and
authorization before runtime scope expands.

The delivery strategy is deliberately vertical. Each slice must leave a usable,
tested boundary and must not introduce behavior assigned to a later slice.

## Delivery sequence

### Slice 1: read-only planning — complete

Implemented in `src/spine_packs/`:

- validate the complete manifest and sealed install request;
- resolve an exact selection and compatible local Spine target;
- query only the pinned public read-command surface;
- classify missing, equivalent, drifted, and blocked desired state;
- emit a deterministic, private, no-clobber plan artifact; and
- reject write commands at the subprocess boundary.

This slice has synthetic runtime and independent contract coverage. It has not
been qualified against a live operator target.

### Slice 2: apply preflight without writes — complete

Add the internal apply-preflight service boundary while keeping all Spine writes
disabled. Do not expose the public `apply` CLI command until Slice 3:

- validate and correlate the saved plan, approval, and complete manifest;
- require an apply-eligible released plan and complete action authorization;
- resolve and revalidate the exact local target and execution-contract union;
- repeat `system.info`, catalog collection, snapshot, and selected-object
  precondition checks;
- validate the complete ordered command templates and all IDs that can be
  materialized before execution;
- classify stale, incompatible, blocked, draft, and incompletely authorized
  attempts using the specified result envelope and exit behavior; and
- prove with negative tests that no subprocess write command can be launched.

Exit gate: every preflight failure is deterministic and non-mutating, and a
successful preflight produces only an in-memory execution-ready description.
It does not create a checkpoint or submit a Spine write.

### Slice 3: initial apply and durable checkpointing — implemented; bounded review complete

Enable an approved initial write sequence:

- establish the stable execution identity, actor, action timestamp, and
  reproducible command IDs;
- atomically publish the prepared checkpoint before each command submission;
- submit only the closed, validated Spine write-command set;
- validate and durably preserve each response before advancing;
- materialize generated-ID references only from validated prior responses;
- stop on the first rejection or malformed response; and
- emit `applied`, `partial`, or `not_applied` terminal results without
  compensation or rollback claims.

Exit gate: fault-injection tests cover every boundary between checkpoint
publication, command submission, response validation, and checkpoint advance.

The initial-only implementation is in `apply.py` and `execution.py`, with a
separate transport write allowlist and explicit CLI checkpoint/output paths.
Tests cover all six write commands, exact receipt/request correlation,
independent checkpoint/result contract validation, binding precondition changes,
empty-prefix partial failure, preflight refusal, no-write plans, and filesystem
publication failures. Qualification uses simulated commands only. Preserve any
interrupted checkpoint; same-execution continuation is implemented in Slice 4 below.
Bounded review returned no blockers or major findings and one minor
owner-template validation gap. The gap is addressed by uniform exact-plan-owner
checks and negative contract/runtime vectors, including unreferenced creates.
The follow-up patch is regression-tested, not separately re-audited. No real
installation, pack release, or deployment is implied.

### Slice 4: continuation and uncertain-response recovery — implemented; bounded review complete

Resume an interrupted execution without broadening its authority:

- validate checkpoint or terminal partial-result correlation;
- reconstruct the accepted prefix and its exact expected catalog state;
- distinguish the normal prefix state from the single permitted uncertain
  first-unresolved-action state;
- reuse the original command ID and exact semantic request;
- require compatible replay or new acceptance before advancing; and
- reject gaps, unrelated catalog changes, changed approvals, or altered
  execution facts.

Exit gate: restart tests cover every action boundary, including an accepted
write whose response was not durably recorded. No failed or stale execution can
skip, reorder, or regenerate an action.

`recovery.py` validates the saved checkpoint or partial result, exhausts fresh
public readback, checks full selected definitions and available provenance,
and compares inverse fingerprints under Section 9.1. Recompiling the original
plan from reconstructed semantic preimages checks the remaining suffix and
untouched selected definitions. Only one candidate may pass. `apply.py` shares
the durable execution loop with initial apply; provisional readback facts must
match the retry response before acceptance is recorded.

The CLI takes `apply --continue-from SOURCE` and fresh checkpoint/result paths,
preserving the recovery source. Simulated tests cover all six command kinds,
every prepared/advanced checkpoint boundary, response loss after commit,
partial-result continuation, unrelated changes, semantic/provenance mismatch,
replay-ID mismatch, binding changes before retry, and publication failures.
These are synthetic tests, not real-target qualification. The bounded review
passed with one package-docstring nit, subsequently patched; no runtime change
was needed. The review artifacts are in `whetstone_runs/installer-slice4-audit-001/`.

### Slice 5: non-mutating verification — implemented; bounded review complete

Implement `verify` independently of apply execution:

- reload and correlate the plan, manifest, target, and optional apply result;
- freshly read selected archetypes, profiles, and bindings;
- verify semantic desired state and selection scope;
- correlate captured command responses and receipt facts without claiming
  later authoritative receipt-row readback; and
- emit the closed verification artifact and specified result status.

Exit gate: verification performs no write or compatible-replay request and
detects target, state, evidence, and correlation mismatches.

`verification.py` and the source-tree `verify` CLI implement selected-state
comparison independently of apply execution. The CLI requires an explicit
manifest and saved plan, accepts an optional apply result, and writes a new
sealed verification artifact. Captured response coverage is distinct from
fresh catalog equivalence. Missing/invalid evidence cannot be repaired by a
write or replay. No-write plans require no receipts. Whole-owner observation
retains read validation and consistency checks without treating unrelated
catalog changes as verification failures.

Focused tests cover all six command response kinds, complete/missing/invalid
coverage, no-write and granular plans, drift and retirement, changed root IDs,
equivalent later revisions, malformed readback, target/compatibility failures,
CLI exits and protected paths, and the read-only transport boundary. Independent
contract checks cover exact ordered object coverage and evidence states.
The bounded review passed with no blockers or majors, one minor CLI-synopsis
clarification, and one stale test-name nit. Both were patched in `490c298`;
the follow-up passed 55 contract and 106 runtime tests, without runtime changes.
The patch has not been separately re-audited. No pack or installer is released.

### Slice 6: end-to-end qualification and supported packaging — technical acceptance passed

The operator authorized kickoff with an isolated throwaway ledger. Start with
local integration qualification; packaging follows only after the source-tree
workflow qualifies. No existing ledger, daemon, cloud deployment, checkout
mutation, or public release is authorized by this test pass.

The first disposable-ledger pass exercises real Spine 0.3.0 public commands
against an isolated installation of the inspected commit. It covers normal
installation, retain and granular planning, drift authorization/refusal,
staleness, verification mismatch, terminal partial-result continuation, and
uncertain-response recovery for all six write kinds. The harness retains all
local evidence and does not modify runtime code, Spine, or curated packs.
Setup, reproducible invocation, evidence, and limits are documented in
`docs/local-qualification.md`. The initial pass passed four integration tests
(including six separate uncertain-response command scenarios), 55 contract
tests, 106 synthetic runtime tests, and repository/whitespace checks.
Local wheel/sdist packaging and an installed console entrypoint are now
authorized for GitHub distribution. `scripts/qualify_package.py` checks archive
contents, rebuilds from the sdist, and runs the disposable suite through a
clean installed CLI outside the checkout. See `docs/releases.md` for the
procedure and publication gates. The initial
clean-installed candidate passed all four integration tests, including the six
uncertain-response subcases, on macOS/Python 3.14.6. Source checks passed 55
contract tests and 109 runtime tests. Direct and sdist-built wheels matched
byte-for-byte. The same checks subsequently passed from a clean detached clone
of `8f7e967db0a0ce178ad19da374deba167b6a6799`, completing the clean-commit gate
for the reviewed implementation candidate.

The authorized 22-file Whetstone `audit-change` consistency review on
2026-09-18 returned `pass`, `boundary_preserved=true`, and zero blockers,
majors, minors, or nits. The reviewed brief SHA-256 is
`e60e388dd1f6f223f7ee3271868033807b00232a25b3f94d2e5bc4f0fea4441d`.
Raw review and target-bound test evidence are retained locally, not shipped.
This completes the bounded Slice 6 technical acceptance; it is not a convergence
declaration or staging/production qualification.

The operator subsequently approved installer version `0.1.0`, MIT licensing,
and tag `installer-v0.1.0`. This release-metadata closeout changes no installer
runtime or pack contract. Its exact final commit must pass qualification before
tag publication. GitHub release assets and curated pack release remain separate
from the approved tag operation.

Harden the complete local v1 workflow:

- run plan, approval, initial apply, interrupted continuation, and verify
  scenarios against an isolated disposable Spine ledger through public
  commands only;
- exercise missing, equivalent, authorized drift, rejected drift, stale plan,
  partial apply, uncertain response, and verification mismatch cases;
- confirm artifact permissions, no-clobber behavior, byte and time bounds, and
  secret-safe diagnostics; and
- define the supported package and entrypoint only after the source-tree
  workflow qualifies.

Exit gate: contract, runtime, fault-injection, clean-install, and disposable
integration checks pass from a clean checkout. Release of either the installer
or a pack remains a separate decision.

## Deferred hardening

### Schema-15 alignment — installer release 0.2.0

The operator supplied Spine commit `ab18a8a51c9bf548220f67e2db0220bfe9783888`
after its independent repair gates. This pins runtime `0.5.0` / schema `15`.
Installer `0.2.0` adds its public `system.info.v3` validator and
runtime-specific execution union while preserving `0.3.0` / `12` support.
The new environment variant binds the ledger-instance ID into plans, approvals
(through the plan digest), continuation checks, and verification evidence.
No public command allowlist or recovery scope expands.

Draft 10 is a compatibility-only copy of draft 9; no profile or archetype
semantics change, and no draft becomes installable. Completion requires contract
and adversarial identity tests plus source-tree and clean-package disposable
qualification on both exact baselines. Installer exact-commit qualification
passed at `57a6776`; its version, tag, and exact assets were separately approved
and published as `installer-v0.2.0`. This does not authorize staging apply.

Working-tree qualification on 2026-09-19 passed repository verification (107
required files), 58 contract tests, 115 synthetic runtime tests, and whitespace
checks. Both pinned Spine baselines passed the four disposable source-tree
integration scenarios and all four clean-installed scenarios, including
uncertain-response recovery across the six write commands. Each package build
matched its direct wheel to its sdist-built wheel byte-for-byte. Spine checkouts,
operator ledgers, published tags/assets, and drafts 1–9 were not changed.

Independent `jsonschema` 4.26.0 Draft 2020-12 checks passed all 12 schema
meta-validations, the complete 35-case pack fixture matrix (lexical and semantic
checks remain separate), and 15 positive installer artifacts. The new public
system-info validator was also compared exactly with the pinned upstream schema.
These results qualify the local implementation candidate, not a clean committed
release or a staged operator environment.

The authorized 29-file schema-15 Whetstone `audit-change` consistency review
returned `pass_with_minor_clarification`, preserved boundaries, and reported
zero blockers, zero majors, one minor and one nit. Its reviewed brief SHA-256 is
`4264d1c0c46b9ff59b25aa3d8180aeb1fad37bc672f156683cbcafb7ecdde965`.
Both wording findings are patched: the required semantic vectors explicitly
cover both runtime-specific receipt disclosures and reject cross-pairing, and
the catalog-fingerprint docstring names both pinned baselines. No behavior
changed in this follow-up, and the patches have not been separately re-audited.
Original payload and review evidence remain local and unchanged.

### kinflow-starter 1.0.0 promotion

The operator approved the unchanged-content promotion of draft 10 and separate
publication under `pack-kinflow-starter-v1.0.0`. The stable manifest changes only
version, status, and digest; exact approved bytes and all 52 definitions in each
collection are pinned by `test_kinflow_release_contract.py` and registered in the
pack fixture matrix. Drafts 1–10 remain unchanged. Required checks and independent
Draft 2020-12 validation must pass from the exact promotion commit before its
tag and assets are published. This is not a new full-content Whetstone audit.
The approval, hashes, qualification evidence, and staging prerequisites are in
`docs/release-finalization.md`. No staging owner, target, selection, or apply
approval is implied by publication.

### Spine 0.6.0 alignment — reviewed; release finalization

Installer candidate `0.3.0` adds exact Spine `0.6.0` / schema `15` at
`ad1db8e1a4c7aa9a525612324d08824802a86351`. The CLI command map, execution
union, public system-info-v3 shape, catalog fingerprints, and replay semantics
are unchanged from the 0.5.0 pin. The true runtime and ledger identity remain
bound into artifacts; old plans cannot survive a runtime upgrade by relabeling.
No HTTP transport or web cursor support is added.

Compatibility-only `kinflow-starter 1.0.1-draft.1` preserves all 1.0.0 content
and adds only 0.6.0 compatibility. Stable 1.0.0 remains immutable and cannot be
applied to 0.6.0. Local checks passed: 63 contract and 125 runtime tests, 115
verifier files, and four source-tree plus four clean-installed disposable
scenarios on each of all three supported baselines. Independent Draft 2020-12
and unchanged-upstream checks passed. Evidence and limits are recorded in
`docs/spine-0.6.0-qualification.md`. The authorized 31-file bounded review
returned `pass_with_minor_clarification`, zero blockers or majors, and two
release-handoff minors. Both were patched and clean-installed qualification
passed again on all three baselines. Original review evidence remains local.
Stable `1.0.1` now promotes the compatibility draft without content changes;
its new digest and immutable file bytes are pinned in contract tests.
Release finalization must qualify the exact committed candidate and obtain
approval for its tags and assets before publication; see
`docs/spine-0.6.0-release-finalization.md`. No staged deployment is implied.

### Remaining hardening follow-ups

The following remain explicit follow-ups rather than hidden v1 prerequisites:

- atomic compare-and-set for binding replacement;
- public command-receipt readback;
- remote transport;
- multi-writer reconciliation; and
- cryptographic approval or Foreman integration.

If one becomes necessary for a delivery slice, update the owning Spine and
Spine Packs contracts before implementation rather than weakening the stated
local, single-operator boundary.

## Per-slice completion rule

A slice is complete only when its normative references, machine contracts,
runtime behavior, focused tests, repository verification, documentation, and
working-tree review agree. Commit and push are separate operator decisions.

## Facet-aware rendering successor — proposed sequence

This new sequence is governed by [facet-rendering-packs.md](facet-rendering-packs.md),
not a reopening of completed installer Slices 1–6. FR-1 contracts/fixtures are
committed; FR-2 read-only planning is operator-authorized, with the historical
lookup blocker resolved by the explicitly adopted 0.10.0 pin below. The separately approved 14-file bounded audit completed
with one minor clarification, addressed by a local wording patch; see the
[audit disposition](../whetstone_runs/facet-rendering-spec-audit-001/local-assessment.md).
FR-3 initial apply is implemented and its repair findings are closed. FR-4's
recovery/verify contract recheck passed. Its next authorized runtime increment
added read-only historical lineage observation and exact accepted-prefix
comparison. Subsequent authorized increments complete uncertain-response
admission/replay correlation and internal durable continuation with synthetic
fault tests and independent internal read-only verification. The FR-4 runtime
repair recheck passed at `965326a`; the operator subsequently authorized CLI
continuation/verify wiring with synthetic public-command tests. Installed-package
qualification is recorded in the separately authorized FR-5 increment below.
The operator has now authorized FR-5 disposable source and installed-package
qualification. Curated pack rewrite, deployment, release and additional
external review remain unauthorized. Source baseline: Spine
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, `0.10.0` / `19`, explicitly approved
on 2026-10-16. The earlier 0.9.1 pin and gate remain historical evidence.
The prior audit covers the original proposal,
not automatic acceptance of new FR-1 machine artifacts.

Use vertical delivery around one flight graph, with a focused contract review
before each runtime boundary. Do not first convert all 52 starter archetypes.

The upstream listing gate passed independently on the exact repaired wheel:
ordinary v2 create/show/list, mixed v1/v2 complete pagination, definition pins,
and preserved v1 rejection. See `docs/facet-rendering-baseline.md`. The original
0.9.0 defect remains historical evidence. This narrow gate does not complete
FR-5 installer qualification or authorize runtime implementation.

| Slice | Deliverable | Exit gate before the next slice |
| --- | --- | --- |
| FR-0: proposal and bounded audit | Proposed manifest v2, reference graph, command/contract inventory, failure/recovery rules, product decisions, audit payload | Approved reviewer-only consistency audit completed: pass with one minor clarification, locally addressed. Further implementation scope still requires authorization |
| FR-1: machine agreements and fixture proof | Manifest v2; seven v2 installer artifact schemas, shared/embedded/readback closure; synthetic scalar + location-label flight flow; independent hash and reference vectors | Repaired listing gate passed; Draft 2020-12 meta/fixture validation, semantic tests, unchanged v1 vectors and bounded machine-contract review. Fix exact reference-slot syntax and aggregate observation budgets before code |
| FR-2: read-only flight plan | Exact 0.10.0 preflight, protected cursor prerequisites, revision-addressed historical lookup, complete public observation view, dependency closure, cascaded drift and typed outputs | Missing/retain/drift/retired and mixed v1/v2 readback tests; pagination/capacity/staleness failures; no writes even dry-run. Independent disposable read-only gate; bounded review before advancing. No release compatibility claim |
| FR-3: approved initial flight apply | New command-specific serializers/evidence validators; ordered dependencies; durable prepared/accepted checkpoints; no-op and binding guards | Every one of the 11 write kinds, all ID-consuming paths and every durability boundary tested; no item/disclosure/send commands; no speculative IDs or automatic drift updates |
| FR-4: same-execution recovery and verify | Forward expected-state comparison from bounded preimages; prefix/prefix-plus-one recovery; exact request replay; read-only exact-pin verification | Lost responses for schema/rendering create/publish, both binding kinds and nested profile refs; unrelated drift rejected; receipt limitations explicit; every old recovery/verify test preserved |
| FR-5: disposable and installed-package qualification | Exact pinned Spine build, isolated temporary catalogs, synthetic owner and protected test cursor configs via separately authorized setup; source and clean-wheel plan/apply/replay/verify | All v1 supported-baseline regression gates plus exact 0.10.0 public-CLI qualification. No existing ledger, item creation, materialization, sends, disclosure grants or Spine checkout edits |
| FR-6: curated flight content and release readiness | Operator-approved field/label/template/default choices; one new immutable pack version and successor installer packaging | Reviewed flight content/digests, unchanged other curated definitions, consumer v2-application readiness and explicit disclosure handoff. Tag/assets/publication/deployment require separate approval |

FR-1 may use synthetic flight fixture choices without pretending they are curated
product decisions. FR-6 must resolve Section 10's actual content, opt-in/default
and distribution choices. Neither reviewer feedback nor test success supplies
those approvals. Ordinary renderer/disclosure behavior is Spine's own tested
authority; qualification here proves configuration publication and readback,
not notification delivery.

The public-read-only evidence design is intentional: new catalogs have no
public snapshot hashes, and facet responses have no nested semantic-hash receipt.
Do not carry the old inverse-fingerprint or universal receipt validators into
FR-3/4 without the new family-specific contracts and fault-injection proof.

### FR-1 progress and next bounded increment

The manifest-only increment is authored: draft v2 schema, synthetic flight graph,
indexed positive/negative mutations and independent Draft 2020-12 plus semantic
checks. Existing runtime and v1 artifacts remain untouched. This is not FR-1
completion or authorization to start FR-2.

The next increment is now authored in `installer-artifacts-v2.md`: seven v2
entry schemas, shared/embedded types, offline pinned public closure, typed null
slots and aggregate observation budgets. Synthetic create and cascading-update
flight flows cover all 11 writes and prepared/response-loss/accepted recovery
boundaries. Family-specific evidence retains complete public response text,
including native public JSON numbers, without inventing a universal receipt.
Upstream wire vectors supplement the independent schema/semantic/hash oracles.

The bounded artifact-contract review completed with no blockers or majors and
one minor key-grammar finding. That finding was fixed with eight vectors across
all ten schema locations and committed with the reviewed increment as `5403680`.
See the preserved review disposition and patch follow-up under
`whetstone_runs/facet-rendering-fr1-artifacts-audit-001/`. The patch passed 83
independent contract tests, 126 runtime tests and repository/whitespace checks;
it was not externally re-audited. These are contract gates, not runtime or package
qualification.

The operator subsequently authorized FR-2. Read-only implementation-readiness
inspection initially identified an unresolved historical facet revision-to-root lookup:
existing pins carry revision IDs, while exact public show also requires the root
ID. See [the FR-2 finding](../docs/fr2-historical-facet-readback-gap.md) for pinned
contract evidence and resolution options. The operator subsequently resolved
that decision by explicitly adopting Spine 0.10.0's revision-addressed public
read. Candidate-root probing and failure suppression remain forbidden.
FR-2 must prove actual full two-pass pagination, cursor-config,
capacity and transport failure handling; FR-3 must prove durable filesystem
ordering; FR-4 must implement and fault-test continuation/verification. The
synthetic oracle cannot stand in for these runtime tests. FR-5 still requires
the exact Spine package and existing-baseline package regression gates.

### FR-2 resumed increment (2026-10-16)

The separate v2 read-only planner is implemented with exact revision lookup,
per-pass deduplication, shared bounded observation, pinned offline decoders,
typed dependency resolution and fail-closed drift planning. No successor writes,
recovery or verify are enabled. New 0.10.0 inventory/closure and synthetic
cross-root public transcripts supplement, not replace, the reviewed FR-1 files.
Independent test and provenance results are recorded in `docs/fr2-qualification.md`.

The focused FR-2 re-audit passed with no findings; its evidence is committed as
`16e5f4a`. See `whetstone_runs/facet-rendering-fr2-recheck-001/`. The operator
subsequently authorized beginning FR-3 initial apply. FR-6 product decisions
remain pending; this synthetic flight gate approves no curated fields, labels,
templates or disclosure policy.

### FR-3 initial contract increment (2026-10-17)

The execution-fixture refresh is authored under the exact 0.10.0 inventory and
offline closure. `contracts/installer-fr3-fixture-manifest.v2.json` pins separate
synthetic create/update flows and their unchanged 0.9.1 sources. The new flows
cover all 11 initial write kinds, typed dependency consumers, complete approval,
prepared/accepted checkpoint shapes and partial results, including failure at
the first submitted action. Plan, approval, command, evidence and checkpoint
digests are regenerated, not relabelled. The existing FR-2 planner must reproduce
these independently refreshed plans exactly.

These are contract tests, not proof of actual writes or filesystem ordering.
No executor or write transport is enabled by this increment. The approved
15-file focused contract review passed with one minor response-correlation
finding. The operator-authorized patch adds exact facet-key/schema-revision
response checks and four negative cases; see
`whetstone_runs/facet-rendering-fr3-contract-audit-001/patch-followup.md`.
The patch passed 99 contract and 142 runtime tests, repository verification and
whitespace checks; it has not been externally re-audited. Next:
implement FR-3 command serializers/evidence validation, write allowlist,
initial apply orchestration and durable publication/fault-injection tests.
Retain the existing read-only plan guard and unchanged v1 execution path.

Do not refresh or claim successor recovery/verification in this increment.
The old verification evidence label belongs to the preserved FR-1 fixtures;
the exact-0.10.0 verification label and fixtures must be reviewed before FR-4.
See `docs/fr3-initial-apply-readiness.md` for gate results and limitations.

### FR-3 pure execution increment

The audit and minor correlation patch are committed as `b2f224e`. The next
bounded runtime increment implements `facet_execution` without enabling writes:
approved-plan reconstruction, typed next-request materialization, revalidated
contiguous producer evidence, exact public response text preservation, and
catalog/facet/rendering-specific response/readback correlation. Saved independent
0.10.0 create/update flows cover all 11 configuration write kinds. Runtime tests
include tampered graph/approval/prefix evidence, malformed wire data, no-op
rejection, metadata revision preservation and post-resolution rendering size.

This increment is not the complete FR-3 executor. The next bound is fresh
preflight/readback integration, explicit write transport, immediate binding
guards, durable prepared/accepted checkpoints, initial-only orchestration and
CLI wiring, with fault injection at every durability boundary. Keep the planning
transport write-disabled. No successor continuation or verify is authorized.
The pure helper's accepted-prefix argument is not proof of filesystem durability;
only the future checkpoint owner may supply it after durable acceptance.

### FR-3 initial executor increment

The pure helpers are committed as `fc30fab`. The authorized next bound implements
`facet_apply` and the separate `FacetApplyCommand` adapter, plus v2 initial-apply
CLI dispatch. Initial preflight rebuilds the entire two-pass public plan and
requires equality with the approved plan. Each response receives public readback
before acceptance; binding rechecks and exact facet CAS precede submission.
Prepared/accepted v2 checkpoints reuse the existing durable writer with an
explicit artifact validator. Partial results retain the first unresolved request.
V2 continuation and verify remain rejected before target access.

Focused tests cover all 11 writes, every prepared/accepted boundary, first and
later uncertain responses/readback failures, file/directory fsync, link/replace,
binding drift, CLI publication and collision behavior, default adapter dispatch,
and the original bounded public-read preflight transcript. A synthetic subprocess
checks CLI word arguments and exact stdout preservation. The independent oracle
checks results when run with the development validator. No actual Spine ledger
is accessed in these tests.

### FR-3 runtime review and repair closure (2026-10-17)

The initial executor is committed as `540e113`. Its approved bounded runtime
audit found one major immutable-revision correlation gap and one minor contextual
facet-failure decoding gap. The first focused recheck retained a major finding:
catalog revise responses have no `changed` flag, and replayed publications may
report `changed=false`. Preserve both reports under
`whetstone_runs/facet-rendering-fr3-runtime-audit-001/` and
`whetstone_runs/facet-rendering-fr3-runtime-recheck-001/` as historical evidence.

The current uncommitted repairs use the declared revision outputs and non-noop
effect semantics rather than `changed`, and validate facet failures against the
pinned contextual contract. Regression tests cover all four revision-producing
update commands, replayed publications, partial stop before consumers, accepted
prefix/unresolved-request preservation, valid distinct replayed revisions and
metadata-only revision preservation. Local repair verification passed 27 focused
tests, 180 runtime tests, 99 official contract tests without skips, repository
verification (171 required files) and whitespace checks.

The separately authorized focused recheck completed with `pass`, preserved
boundaries and zero findings. Its retained
[report](../whetstone_runs/facet-rendering-fr3-runtime-recheck-002/change_audit/change_audit_report.md),
`prepared-inputs.json` and authorization bind 13 source/context files plus notes.
All 13 source/context hashes and the notes still match the current bytes; the
manifest and brief-bound feedback/report agree. This closes the reviewed FR-3
repair findings, not a new full-surface audit or a convergence declaration.
Implementation and repair verification details remain in
[FR-3 readiness](../docs/fr3-initial-apply-readiness.md).

Next checkpoint: the three repaired implementation/test files and the linked
status updates; commit/push require separate direction. No new review is needed
merely to record this retained result. FR-4 recovery/verify is the next planned
implementation slice, but remains unauthorized, including its exact-0.10.0
verification-label/fixture gate.

Installed-package qualification is still pending under **FR-5** in the table
above; there is no separate completed FR-3 installed-package gate. It requires
exact pinned Spine source/wheel/installed-package provenance, source and clean-
installed installer public-CLI plan/apply/replay/verify on new disposable ledgers,
and all supported v1 baseline package regressions. The new initial-apply path
has not yet received that real-Spine qualification. `system.info`, launcher hashes,
synthetic tests and the passing review cannot substitute for it. FR-5 follows
the separately authorized FR-4 implementation and requires its own setup scope;
do not start it as review bookkeeping. No staging, release, packaging-completion
or operator-installation claim follows from this closure.

### FR-4 recovery/verify contract increment (2026-10-18)

The FR-3 repair checkpoint is committed as `52b30e2`; no push was requested.
The operator authorized proceeding with FR-4, starting at the required contract
and fixture refresh rather than immediately enabling runtime recovery/verify.
This supersedes earlier pending-authorization wording without rewriting audits.

The additive shared-schema change pairs the 0.10.0 environment with
`captured_responses_only_spine_0.10.0`, retaining the historical 0.9.1 pair and
rejecting cross-pairing. No v1 contract or released artifact changes. Separate
hash-pinned companions extend unchanged FR-3 create/update sources with complete
prefix views, verification and envelopes. All 36 interruption boundaries across
11 commands are indexed; new negative/positive test-only oracles distinguish
admission from replay acceptance, exact references, immutable lineage,
provenance, binding guards and verification evidence/selection scope.

The exact Spine commit exists and all 20 upstream schema inputs plus the
revision-readback authority pins match its Git tree. No HEAD substitution,
Spine execution, checkout edit, ledger allocation or package build occurred.
Current results, evidence limitations and the staged bounded review scope are
recorded in `../docs/fr4-contract-readiness.md`.

The approved 20-file bounded FR-4 contract audit completed with two major
test-oracle correlation findings; both were reproduced locally. The operator
authorized the narrow repairs: metadata response IDs now correlate to both the
expected and post-observation revisions; a private full rendering candidate
record now survives admission for exact replay-record comparison, including
creation provenance from earlier executions. Four focused regressions cover
resealed metadata evidence through checkpoint/verification, all three creation
provenance fields, valid earlier creation attribution and private record copies.
The original audit and approved payload are preserved unchanged under
`whetstone_runs/facet-rendering-fr4-contract-audit-001/`. These are local fixes,
not independent reviewer closure; a focused recheck needs new payload approval.
Post-patch checks passed 22 focused tests, 121 official contract tests without
skips, 180 runtime tests, the 178-file repository verifier and whitespace checks.
See the separate `patch-followup.md` in that audit root for evidence and limits.

The explicitly approved focused contract recheck passed with its boundary
preserved and zero findings on 2026-10-20. See the retained
[report](../whetstone_runs/facet-rendering-fr4-contract-recheck-001/change_audit/change_audit_report.md).
The operator authorized a local checkpoint, not a push or runtime activation.

Next implementation step: public observation/forward admission and historical
readback; same-execution replay and durable continuation with fault injection;
independent read-only exact-pin verification. This contract increment keeps
runtime CLI guards intact and adds no code under `src/spine_packs/`. FR-5
disposable/installed qualification and FR-6 product/release choices stay separate.

### FR-4 read-only recovery foundation

The reviewed contract checkpoint is `b1379ce`. The operator authorized resuming
the existing local recovery work, without repeating that contract review. This
increment implements `facet_recovery.RecoveryPreimage` in the existing package:
it revalidates the approved graph, checkpoint identity, contiguous accepted
responses and the exact pending request before target use. It forwards accepted
effects into a private expected view, retaining immutable revision preimages
after current consumers move away. It never fabricates public catalog hashes.

`facet_observation` now accepts exact lineage hints. Fresh public historical
reads cover archetypes, mixed v1/v2 profiles, facet schemas and rendering
definitions. Only schema revision-addressed lookup is used for schemas, with
no candidate-root probing. Reads share the existing global observation budget
and per-pass caches; both complete passes must agree. Hint bodies never replace
public evidence; wrong owners/roots, contradictory identities, missing evidence,
corruption and capacity failures fail closed.

The synthetic runtime tests exercise every create/update accepted and prepared
prefix against the independent FR-4 fixture views, immutable identity rules,
malformed checkpoints, all historical families, repeated/current/retired pins,
unreferenced A1 alongside current A2/B2 and pinned B1, failure contracts, global
budgets and changed second-pass history. These are wire simulations, not real
Spine or installed-package qualification. Existing fixtures, schemas, released
packs, v1 behavior and CLI rejection guards are unchanged.

Checks passed: 22 focused recovery-foundation tests, 202 complete runtime tests,
121 contract tests with the official Draft 2020-12 validator (no skips), the
180-file repository verifier and whitespace checks, including the new files.
The required system-Python contract run also passed, with 56 development-
validator skips covered by the complete official run. An additional synthetic
historical v2-profile readback check passed. The exact Spine commit was confirmed
available without invoking Spine or opening a ledger. No external reviewer,
package build/qualification, commit or push was run for this increment.

This foundation accepts only the exact accepted-prefix comparison. It rejects
prefix-plus-one states and performs no replay, checkpoint publication,
continuation, or final verification. Next: implement and fault-test uncertain
candidate admission and exact replay correlation, then durable continuation and
independent read-only verify. External runtime review requires separate approved
payload scope. FR-5 qualification and FR-6 product choices remain pending.

### FR-4 admission/replay and internal continuation (2026-10-27)

The read-only foundation is checkpointed as `3a5e560`. The operator authorized
inspecting and finishing the existing local admission/replay work, then picking
up the next bounded increment. The implementation stays in the existing package
and test layout, without activating CLI continuation or independent verify.

The pure admission handle validates exactly prefix or prefix-plus-one, preserves
the original request and all immutable lineage, and correlates replay response
IDs with the provisional candidate. Full rendering creation/publication records
are retained privately through replay; available archetype root/revision
provenance is checked as well. Missing facet provenance is not invented.
Immediate binding checks use the admitted post-binding only for the unresolved
candidate, otherwise the approved prefix precondition; CAS inputs never change.

The next bounded increment implements `facet_apply.apply_continuation` internally.
Checkpoint or terminal-partial sources are fully correlated before target use;
other terminal results are rejected. Fresh admission uses the real two-pass
observer, with pending head preimages and a bounded single-record capture in
both passes under the existing global budget. New private checkpoint publication
precedes any retry. Initial and continued apply share prepared/accepted durability
ordering. Completed checkpoints can finish without writes; admission errors
publish nothing, later failures remain partial, and durability failures propagate
without manufacturing a result or advancing consumers.

Synthetic tests cover all 11 writes across prepared, lost-response and accepted
boundaries, both source kinds, complete checkpoints, exact request/ID/metadata
correlation, full rendering creation evidence, available archetype provenance,
untouched state, per-pass record drift, binding rechecks, every publication
boundary, response/readback failures, real private checkpoint files and directory
fsync failure. Complete public-wire simulations exercise real observation plus
admission at every prefix and selected replay/suffix flows without stubbing
preflight. They are not actual Spine execution or installed-package qualification.

Verification passed: 26 focused admission/continuation tests (also repeated with
official Draft 2020-12 and independent semantic result checks enabled), all 228
runtime tests, all 121 official contract tests without skips, the 181-file
repository verifier, and whitespace checks including the new test file. The
required system-Python contract run also passed with its 56 development-validator
skips covered by the complete official run. The exact Spine source commit was
confirmed available; no Spine process or real ledger was used. V1 execution,
CLI guards, both transport allowlists, all machine contracts and released pack
bytes remain unchanged. This is local implementation evidence, not independent
runtime-review closure or publication approval.

Next after this checkpoint: independent read-only successor verification; CLI
continuation/verify activation must separately wire all input/source/destination
collision checks and preserve rejection guards until ready. No new ledger,
Spine checkout mutation, package qualification, external reviewer, commit or push
is part of this work. No schema, fixture, released pack, command allowlist,
compatibility range or product-policy choice changes. Runtime review still needs
its own explicit payload approval; FR-5 and FR-6 remain pending.

### FR-4 independent internal read-only verification

The operator authorized the next bounded slice after internal continuation.
`facet_verification` uses shared pure saved-plan validation and the existing
bounded two-pass public observer. It has no apply/recovery/checkpoint path,
receipt/disclosure command, approval-file input or write/replay call. Known
immutable lineage checks now live with pure execution evidence so verification
does not import continuation admission. Apply's strict applicability gate is
unchanged; existing uncommitted recovery/continuation work is preserved.

Malformed outer apply results fail before target use. Valid-shaped outer results
with bad nested digests, plan/approval/execution correlation, evidence, coverage
or unresolved requests produce invalid coverage and mismatch only after fresh
observation succeeds. Reconstructed approval is checksum correlation only.
Missing coverage cannot be filled from current convenient IDs. Supplied execution
claims for ineligible plans are invalid; no-write draft inspection without a
result still verifies state without making the draft installable.

Selected current heads, exact schema/rendering/facet/profile references and
decoder identity are checked independently of captured responses. Archetype,
ordinary-v1 profile and same-target default-binding equivalence are preserved.
Verification does not retain unused execution history or impose continuation's
whole-view staleness rule; unrelated valid unselected changes are not excess.
Public corruption, capacity and missing referenced evidence abort under their
owning contracts, never as a fabricated object mismatch or success.

One test-only oracle gap was reproduced: blocked plan dependencies with null
resolutions could be labelled equivalent from readable old rows. The oracle
now preserves those unresolved blocked identities, with an independent in-memory
contract regression and matching public-wire runtime test. This tightens existing
fail-closed requirements without changing schemas or immutable fixture bytes;
the earlier contract recheck does not independently review this repair/runtime
increment. No product choice or new compatibility policy is introduced.

Synthetic tests cover released/no-write/draft plans, complete/partial/missing/
invalid evidence, failure precedence, immutable corruption versus mutable
metadata drift, active/retired/missing roots, current/historical exact pins,
equal schema content on another actual root, both profile decoders, unrelated
changes and no replay/write behavior. Outputs retain the exact 0.10.0 captured-
response-only label and separate-disclosure requirement.

Verification passed: 24 focused runtime tests, also repeated with the official
Draft 2020-12 validator and independent semantic oracle enabled; 23 focused FR-4
contract tests; all 252 runtime tests; all 122 official contract tests without
skips; the 183-file repository verifier; and whitespace checks, including new
files. The required system-Python contract run also passed, with 57 development-
validator skips covered by the complete official run. The exact Spine commit
was confirmed available without invoking Spine or accessing a ledger. No real
target or package qualification claim follows from these synthetic results.

Next: checkpoint and bounded FR-4 runtime review, then separately gated CLI
continuation/verify activation with collision/private-publication/exit handling.
External review requires explicit payload approval. FR-5 exact installed-package
qualification and FR-6 product/release decisions remain pending. This increment
does not invoke Spine, allocate a ledger, qualify a package, deploy, publish,
commit or push; CLI rejection guards, all public schemas, released artifacts,
v1 runtime behavior and command allowlists remain unchanged.

### FR-4 runtime audit repairs (2026-10-28)

The operator-approved reviewer-only audit of checkpoint `8810c30` completed with
`needs_revision` and two major findings, zero blockers. The retained report is
`whetstone_runs/facet-rendering-fr4-runtime-audit-001/change_audit/change_audit_report.md`.
This is a runtime assessment, separate from the earlier passing contract recheck.
The operator authorized fixing the findings after independent local assessment.

Both defects reproduced before their fixes. The v2 shared error schema now
defines its existing `generatedId` reference as a closed bounded string
`{name, value}` pair. A controlled public write rejection can produce its required
partial result with nonempty facts and the exact prepared request intact.
Regressions cover empty/nonempty accepted prefixes, secret-safe errors, official
schema validation, malformed facts and unused transitive schema references.

Forward recovery comparison now projects an explained profile's current mutable
metadata onto that same root's retained historical rows. Original revision IDs,
decoders and immutable bodies remain exact; fresh public evidence and saved
plan/response artifacts are not rewritten. The independent contract oracle uses
the clarified rule. In-memory vectors exercise preexisting v1/v2 history, both
durable acceptance and lost-response replay, suffix execution and a later
completed-checkpoint restart through the real two-pass public observer.
Unexplained metadata changes, altered historical bodies and decoder changes
still fail before checkpoint publication or submission.

Verification passed: all 255 runtime tests; all 125 official Draft 2020-12
contract tests without skips, including 26 focused FR-4 tests; all three new
runtime regressions repeated with the official validator and independent result
oracle enabled; the 183-file repository verifier; and whitespace checks. The
required system-Python contract run also passed, with 60 development-validator
skips covered by the complete official run. Exact Spine source availability was
checked through Git only; no Spine process, ledger or package qualification was
used. Approved audit payload hashes remain unchanged.

These are local repairs, not independent review closure. No saved fixture or
released pack bytes, v1 schema/behavior, command allowlist or Spine baseline
changed. CLI continuation/verify remain disabled. A focused recheck requires its
own approved payload; FR-5 qualification and FR-6 product decisions stay separate.

### FR-4 runtime review closure and CLI wiring (2026-11-11)

The approved focused recheck of `965326a` completed on 2026-11-10 with `pass`,
boundary preserved and zero findings. Its retained evidence is
[the focused report](../whetstone_runs/facet-rendering-fr4-runtime-recheck-001/change_audit/change_audit_report.md).
It closes both original runtime repair findings within that approved scope;
the later CLI increment below is separately implemented and tested.

The operator authorized the next slice: expose the reviewed continuation and
verification services through the existing noninteractive flags. V2 apply
validates the exact original plan/approval and selected checkpoint or terminal
partial result before transport construction, then uses the existing 11-write
adapter and durable executor. Complete checkpoints finish without writes after
fresh admission. Source/result path checks precede opening those artifacts;
resolved aliases and hard links to protected inputs or target files are refused.
Checkpoint and terminal-output destinations stay new, private and distinct.

V2 verify constructs the FR-2 read adapter, accepts no approval or continuation
flags and invokes no recovery/write boundary. Omitted result input follows the
reviewed coverage rules; an explicitly supplied JSON null is rejected before
transport construction. Verified and mismatch results publish sealed private
artifacts with exits 0 and 10. Continuation partials use exit 9; failed admission,
observation or publication retains the owning error without false success or a
new `not_applied` claim. V1 CLI dispatch and its existing validation remain intact.

`test_facet_cli.py` exercises full synthetic public observation, exact retry,
checkpoint and partial-result sources, complete/no-write recovery, v1/v2
verification semantics, invalid/mixed/oversized inputs, forbidden flags,
protected aliases, input preservation, private files, no-clobber races,
durability failure and result/exit correlation. Official independent structural
and semantic result checks supplement the dependency-free runtime tests.

Verification passed: all 270 runtime tests; all 125 official Draft 2020-12
contract tests without skips; all 15 focused CLI tests with independent envelope,
apply-result and verification-result checks enabled; the 184-file repository
verifier; and whitespace checks including the new test file. The required
system-Python contract run also passed with 60 development-validator skips,
covered by the full official run. Existing v1 runtime tests passed unchanged.
The exact Spine source commit remains available, checked by Git only. No source
qualification or real-target claim follows from these synthetic tests.

No public schema, saved fixture, released pack, compatibility pin or command
allowlist changes. This increment does not allocate a ledger, invoke Spine,
qualify a package, deploy, publish, commit or push. Independent review of the CLI
increment needs its own approved payload. Next: review this CLI increment, then
FR-5 exact-source/installed-package qualification under separate setup authority.
FR-6 content, application/default policy and release decisions remain pending.

### FR-4 CLI audit minor repair (2026-11-13)

The operator-approved bounded CLI audit of `e23ff2a` completed with
`pass_with_minor_clarification`, boundary preserved, zero blockers/majors and one
minor. Its retained
[report](../whetstone_runs/facet-rendering-fr4-cli-audit-001/change_audit/change_audit_report.md)
identified raw loading of writer-produced artifacts at the canonical byte limit:
the writer's terminal LF made an otherwise valid maximum-size file one byte too
large for `--continue-from` or `--result`.

Both cases independently reproduced before the operator-authorized repair.
`load_input` now offers a bounded single-terminal-LF allowance, enabled only for
those two v2 input paths. Canonical artifact ceilings, validators, digests, v1
loading, command allowlists and all other input paths are unchanged. Additional
bytes require rejection; a canonical artifact exceeding its ceiling still fails
before target use. No writer or artifact schema change is needed.

Four new CLI regression methods cover the actual 16,777,216-byte ceiling, real
local checkpoint/result writers and bounded raw framing. A maximum-size result now completes read-only
verification with complete evidence. A maximum-size checkpoint loads and passes
saved-source validation before a deliberate fresh-preflight stop, without writes
or output claims: wrapping that entire checkpoint in a terminal result would
exceed the result's independent ceiling, which this repair does not waive.
Negative cases cover one-byte-too-large canonical artifacts with and without LF,
checkpoint-writer refusal and extra LF/CRLF/space framing. Exact-size input
without LF and unchanged default loader behavior are checked separately.
Saved fixture bytes are preserved through in-memory
extensions using valid public-response whitespace and recomputed local digests.

Verification passed: all 274 runtime tests; all 125 official Draft 2020-12
contract tests without skips; all 19 focused CLI tests with official structural
and independent semantic checks enabled; the 184-file repository verifier; and
whitespace checks. The required system-Python contract run also passed with 60
development-validator skips, covered by the official run. The maximum-size
writer-produced checkpoint/result cases failed before the repair and passed
after it; oversized canonical artifacts remain rejected. All approved audit
payload bytes, public schemas, saved fixtures and released packs are preserved.

This is local repair evidence, not an independent re-review of the patch. No
Spine invocation, ledger, package qualification, new reviewer, commit, push,
deployment or publication belongs to this repair. FR-5 setup and FR-6 product
decisions remain separate from the CLI byte-boundary fix.

### FR-5 disposable and installed-package qualification (2026-11-14)

The operator authorized the next qualification slice after checkpoint
`1c7809309b30153c4b41db8cf5e44934cd0fd85b`. The scope is exact Git exports,
isolated local builds and new disposable configuration-only ledgers. No
existing/operator ledger, Spine checkout change, curated content change,
disclosure grant, items/facet values, reminder or send operation is included.
External review and release/commit/push remain separately authorized actions.

`scripts/qualify_fr5.py` builds and attests exact Spine/Tickerd source, wheel and
installed bytes, then runs the existing FR-2 read gate, new v2 public-CLI
execution/recovery/verify scenarios, and the full source/installed v1 integration
matrix. `tests/integration/test_facet_spine.py` injects loss only around genuine
public-command responses or before submission. It checks all 11 write kinds,
exact request/ID correlation, cascaded updates, private checkpoints, read-only
verification and retained source evidence. Normal continuation/verify runs in
new CLI processes. Installed tests use the extracted sdist harness and bundled
wheel schemas. Provenance rejection tests cover wrong pins, missing modules,
changed installed bytes and extra installed modules.

The sdist adds only that harness and the existing small synthetic flight fixture;
wheel runtime/layout, dependencies, public schemas, supported baseline allowlists,
released packs and frozen audit payloads are unchanged. Package version `0.3.0`
is used only for local candidate builds, with no authorization to replace release
assets. Tooling, exact pins, qualification outcome and limitations are recorded
in `../docs/fr5-qualification.md`.

Technical qualification passed on the working-tree candidate: all 32 source and
installed integration scenarios, source and installed FR-2 gates, exact upstream
Git/export/wheel/installed attestation, identical candidate archives across the
three v1 baselines, and isolated installed v2 resources. Both v2 runs recovered
lost responses for every one of the 11 writes. Additional official schema checks
passed all 390 saved v2 artifacts/manifests. Required checks passed: 188-file
verifier, 125 official contract tests without skips, 279 runtime tests and
whitespace checks. The required system-Python contract run passed with 60
development-validator skips covered by the official run. No runtime repair,
schema/allowlist change, commit, push, deployment or publication was needed.

Next: stage a bounded review of this qualification increment and obtain approval
for its exact external payload. FR-6 curated field/label/template/default and
distribution/release choices remain unresolved; these tests do not settle them.
A committed release candidate still needs exact clean-commit qualification and
separate tag/asset/publication approval.
