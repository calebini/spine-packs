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
No successor write/recovery runtime, curated pack rewrite, deployment,
release or additional external review is authorized here. Source baseline: Spine
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

Next: review this bounded FR-2 change and its exact payload (external review
requires fresh approval), then separately authorize FR-3 initial apply. Before
FR-3, refresh execution-specific 0.10.0 fixtures and evidence labels without
rewriting 0.9.1 fixtures. FR-6 product decisions remain pending; this synthetic
flight gate approves no curated fields, labels, templates or disclosure policy.
