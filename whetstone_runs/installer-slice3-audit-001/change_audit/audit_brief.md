# Whetstone Change Audit Brief

Workflow: audit_change
Profile: consistency

Reviewer instructions:
- Evaluate only the stated change intent and expected boundary.
- Do not perform a full convergence review.
- Treat unrelated polish, completeness, or future hardening concerns as out of scope.
- Report an issue only when it directly affects the change intent, expected boundary, or listed source specs.
- If a concern is outside the stated audit boundary, set in_scope=false.

## Audit Notes

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/installer-slice3-audit-001/audit-notes.md
Hash: e692d571f5104c0f1c00a6f6ff0934eaa175cb240e21c0cfb867512308cdf688

# Slice 3: initial approved apply and durable checkpoints

## Change intent and authority

Review the Slice 3 implementation at commit
`00d3d878563f4917c26dcd454b2eacbfdc4bddce`, based on
`495c120675261cbcdc153b12226676aa2f41d6fd`.
This is one bounded, reviewer-only `audit-change` consistency pass over the
submitted current files, not a Phase 1/2 convergence run or an Editor task.
Specs are normative; implementation and tests are evidence, not new authority.
The implementation plan describes slice sequencing, not expanded authorization.

## Expected boundary

- Spine remains sole authority for installed definitions, bindings, receipts,
  and ownership. Packs remain declarative, owner-neutral, and release-immutable.
- This slice enables initial approved apply only, against the pinned local
  Spine 0.3.0 / ledger 12 public contract. No direct database access is allowed.
- Planning retains its strict read allowlist. Apply permits only
  `item_archetype.create`, `item_archetype.revise`,
  `notification_profile.create`, `notification_profile.metadata.update`,
  `notification_profile.revise`, and `notification_profile.binding.set`.
- Complete plan/approval/manifest validation and fresh preflight precede writes.
  Semantic drift requires exact explicit authorization. Binding preconditions
  are re-read immediately before binding submission.
- Execution identity, actor, timestamp, command IDs, and exact requests are
  stable. Generated references come only from validated accepted responses.
- A private, durable prepared checkpoint precedes every write. A response is
  validated and durably recorded before advancing. Failure stops the sequence;
  no compensation, rollback, automatic retry, or continuation is implemented.
- Results preserve `applied`, `partial`, and `not_applied` distinctions. An empty
  accepted prefix does not establish that no write was submitted or committed.
- The threat model is a local single operator, not hostile filesystem actors,
  concurrent writers, distributed locking, or cryptographically signed approval.

## Reviewer questions

1. Can any write escape approval, fresh preflight, exact target compatibility,
   the six-command allowlist, or durable prepared-checkpoint publication?
2. Do all six request/response pairs correlate command ID, semantic request hash,
   receipt timestamp/effect, keys, literal IDs, revisions, metadata, and generated
   IDs sufficiently? Can malformed evidence enter the accepted prefix or feed a
   later action? Examine binding root IDs as well as the binding ID.
3. Does execution stop safely at every publication, submission, response, and
   checkpoint-advance boundary? Include link/replace, file/directory fsync,
   timeout, rejection, malformed response, and terminal-result publication.
4. Is potentially committed work represented conservatively even when the first
   response is invalid or unavailable? Are failure identity, accepted prefix,
   unresolved exact request, and unattempted suffix mutually consistent?
5. Do checkpoint/result artifacts actually satisfy the independent machine and
   semantic contracts, including zero-action success and zero-prefix failure?
6. Are no-clobber behavior, permissions, path aliases/symlinks, preserved prior
   checkpoints, byte/time bounds, and sanitized errors correct for this scope?
7. Do tests exercise meaningful negative and fault-injection cases rather than
   merely mirror implementation assumptions? Identify concrete missing vectors.
8. Do the normative specs, implementation plan, and runtime agree about the
   initial-only boundary and its exit gate? Is this slice ready to close after
   any identified blocking fixes, without claiming real-target qualification?

## Evidence and review limits

The payload contains six normative/sequence documents, all nine current runtime
modules, eleven checked-in schema files, three runtime test modules, and the
independent installer-artifact contract test module, plus these notes.
Supporting preflight/planner/schema material is included to follow dependencies;
do not turn this into a general re-audit of unchanged functionality.
The verification-result schema is reference closure only, not a request to
implement or audit a future verify command.

Local staging checks: repository verifier passed (91 required files), 49 contract
tests passed, 62 runtime tests passed, and `git diff --check` passed. These are
reported evidence, not a substitute for review. Tests use simulated targets;
no actual installation, deployment, or release has been performed.
Fixture trees and pack content are intentionally not transmitted. This is a
static review payload, not a standalone runnable checkout. If omitted evidence
is essential, identify the exact gap rather than reading other workspace files.

## Out of scope and requested output

No Editor, source edits, automatic patches, external browsing, additional file
reads, Spine checkout access, live commands, deployment, commit, or push.
No Slice 4 continuation/recovery, Slice 5 verify, Slice 6 integration/packaging,
pack content changes, presentation hints, or redesign of accepted semantics.
Checkpoint evidence adequacy is in scope; implementing recovery is not.
Deferred CAS, ledger-instance identity, public receipt readback, and multi-writer
hardening are not new prerequisites unless a concrete current-scope failure is
demonstrated within the stated threat model.

Return a verdict, boundary-preservation assessment, and prioritized concrete
findings with file/section or function references, failure scenarios, and minimal
fix/test recommendations. Mark unrelated observations out of scope. Distinguish
proven defects from uncertainties and unavailable evidence. Do not declare
convergence, release readiness, or live-target qualification.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/architecture.md

Hash: d94d77447ac032dd8da76475c8b49a23b89a4011789a7caf477e68ad83263695

```markdown
# Architecture

## Relationship

The intended data and authority flow is:

```text
declarative pack
      |
      v
installer: plan -> apply -> verify
      |
      v
Spine public command surface
      |
      v
Spine-owned definitions, bindings, receipts, and ownership
```

The arrows represent requests and observations, not transfers of authority.
Spine remains authoritative for every installed object and receipt.

## Declarative packs

A v1 pack describes owner-neutral desired definitions, compatibility
requirements, and deterministic content identity. Its required `dependencies`
field is reserved and MUST be empty. Dependency references require a future
manifest-contract version. A pack contains no execution loop, database client,
delivery integration, scheduler, or Spine runtime code.

Pack content is the installer's input. It is not evidence that an installation
occurred and cannot substitute for a Spine receipt.

## Installer boundary

The installer is a client of Spine's existing public command
surface only. Direct database access is forbidden, including read-only access
used for planning or verification.

The installer is expected to provide:

- `plan`: validate the selected v1 pack, including `dependencies=[]`, query
  Spine through public commands, classify definitions, and emit a
  deterministic plan; v1 performs no dependency resolution;
- `apply`: execute an explicitly approved plan through public commands; and
- `verify`: query Spine through public commands, compare authoritative state
  with the approved plan, and correlate the Spine command responses preserved
  by apply without claiming a second receipt authority.

For each definition, planning must distinguish at least:

- **missing**: eligible to be created;
- **equivalent**: retained without replacement; and
- **semantic drift**: reported as a failure unless the operator explicitly
  authorizes an update.

The draft equivalence algorithm, granular selection boundary, and
update-authorization requirements are specified in `specs/installer.md`. Their
machine-readable representations are specified in `specs/installer-artifacts.md`.
Read-only planning, non-mutating apply preflight, and initial approved apply
with durable checkpointing are implemented. Continuation and verification
remain reviewed design targets, not executable functionality. Tests use
simulated commands; this is not qualification against an actual Spine target.

Dependency references and resolution remain attached to a future manifest and
installer contract. They are not implied by the v1 `plan` operation.

### Public command mapping

The v1 manifest deliberately mirrors only semantic inputs accepted by Spine
runtime `0.3.0`:

- an archetype becomes the `archetype_key` and `revision` inputs to
  `item_archetype.create` under `spine.item-archetypes.v1`;
- a notification profile becomes the `profile_key`, presentation metadata, and
  `revision` inputs to `notification_profile.create` under
  `spine.notification-profiles.v1`; and
- a binding intent resolves its pack-local archetype and profile keys to the
  Spine-owned IDs returned or retained by those commands, then becomes a
  `notification_profile.binding.set` request under
  `spine.notification-profile-bindings.v1`.

The future installer supplies command IDs, actor identity, action timestamps,
owner scope, and resolved Spine IDs at installation time. None of those facts
belong in the pack. This mapping documents a boundary; it does not implement or
authorize installation.

The manifest's `spine_content_contracts` declaration identifies only the Spine
contracts needed to interpret pack definitions. It is not a complete execution
dependency set. `specs/installer.md` derives the draft command set and complete
execution-contract union from the inspected Spine runtime. A future installer
MUST verify that union independently of manifest content compatibility before
it interprets catalog state or emits an applicable plan.

The exact portable artifact family, local target binding, and recovery
checkpoint are specified in `specs/installer-artifacts.md`. These remain
client evidence and never become an alternate Spine ledger.

## First runtime slice: read-only planning

The source-tree package `src/spine_packs/` is the smallest authorized runtime
layout. It requires Python 3.11 or newer and the standard library only:

- `manifest.py` validates the complete pack, not merely its selected objects.
- `artifacts.py` validates requests, canonical embedded values, and plans
  against the checked-in contract vocabulary and semantic rules.
- `planning.py` resolves selection and compares public observations, then
  constructs deterministic classifications and proposed command templates.
- `spine_command.py` is the sole subprocess boundary. Its read allowlist contains
  only `system.info`, archetype/profile list and show, and binding list.
- `__main__.py` handles explicit files, matching selection assertions, one JSON
  result envelope, and private no-clobber plan publication.

The adapter's `read` entry MUST reject write commands before launching a subprocess, even
when a caller asks for dry-run execution. Proposed writes inside a plan are
data only. There is no apply, verify, recovery, remote transport, install-state
registry, or release packaging in this slice. Runtime code MUST NOT import
test helpers or Spine internals. Existing contract-test validators are kept
independent and cross-check generated plans.

Public readbacks and the emitted read-request subset are pinned in
`contracts/schemas/spine-readback-0.3.0.schema.json` to inspected Spine commit
`72203f092de191a7633b1884bf0d61836a25abe4`. That file is a client-side validator,
not a new Spine contract. Its source provenance is recorded in `$comment`.
Spine's raw JSON readbacks contain native integer revision numbers and template
indices; the adapter MAY parse these fields only in public responses and MUST
validate their pinned shape. Installer artifacts still forbid JSON numbers.
Only semantic fields enter embedded comparison values; source integer fields
are not silently rewritten into a different public contract.

The planner MUST preserve the public `catalog_snapshot_hash` returned by Spine,
not invent a local substitute. It exhausts owner-scoped root catalogs (active
and retired), observes active bindings, checks current show results against
listed definitions, and rechecks each first page and snapshot after collection.
These checks detect observed changes; they do not provide an atomic multi-catalog
snapshot or replace the single-operator/no-concurrent-writer requirement.

Local target resolution uses `socket.getfqdn()` and resolved existing file
paths. The adapter hashes the executable and repeats target checks around
observations. It MUST NOT open the ledger; it passes the validated path only
to the public CLI. A path/hash match is not a stable Spine instance identity
or protection against arbitrary concurrent filesystem replacement.

Operational bounds are 30 seconds and 16 MiB of stdout per public command,
16 MiB raw manifest input, and 1 MiB raw request-file input. Canonical artifact
byte limits remain those in `specs/installer-artifacts.md`; whitespace allowance
does not relax them. Process stderr and raw responses MUST NOT be echoed in
installer errors. An explicit Spine rejection produces exit 8; malformed,
inconsistent, timed-out, or oversized transport output fails closed at exit 11.
This source-tree invocation does not configure or deploy Spine.

The output parent MUST already exist. Plan publication uses a same-directory
private temporary file, flush/fsync, and an atomic no-clobber hard link, followed
by parent-directory fsync. Existing outputs, including symlinks, MUST NOT be
replaced or reused. The operator must choose a new output path for each fresh
observation. No result path enters the plan digest. These are POSIX-local
implementation choices, not support for Windows paths or remote storage.

## Slice 3: initial approved apply

`execution.py` is the pure request-materialization and execution-evidence
boundary. `apply.py` orchestrates initial execution and owns checkpoint file
publication. `preflight.py` remains non-mutating. No new package hierarchy or
Spine implementation is introduced. The transport's separate `write` entry
accepts only the six commands in installer Section 3 and validates their
materialized request shapes; it cannot be reached through `read`.

The CLI requires explicit `--manifest`, `--plan`, `--approval`, `--checkpoint`,
and `--output` paths for initial apply. Input identities and complete approval
are validated before target use. Output and checkpoint paths MUST be distinct
from one another and from all inputs, the executable, and the ledger. Existing
checkpoints are refused, including same-execution checkpoints: continuation is
not implemented in this slice. Existing output files are never overwritten.

Initial preflight revalidates the complete manifest and saved plan, materializes
all requests whose IDs are already known, and freshly checks target and catalog
state. Each remaining request is materialized only from a fully correlated
accepted-response prefix. In v1 there is one binding action per archetype;
preceding creates/revisions cannot change that archetype's binding. Immediately
before preparing a binding write, apply exhausts the active owner-scoped binding
catalog and requires its binding identity to match the plan's observed binding
or explicit absence. This is not atomic compare-and-set.

Before every submission, apply durably saves the exact request in a prepared
checkpoint. Before advancing, it validates the response and durably saves the
expanded accepted prefix. Public envelopes, effects, receipt command identity,
receipt timestamp, requested create keys, returned target IDs, metadata, and
complete generated-ID evidence are correlated. The receipt semantic hash MUST
equal the canonical materialized request hash, as specified by the pinned
Spine 0.3.0 handlers. All top-level returned `*_id` fields are retained, including
the archetype and profile IDs of binding responses.

Spine 0.3.0 returns the same success shape for initial acceptance and compatible
replay. This initial-only slice records `outcome=accepted` after receipt
correlation; this means validated command acceptance, not proof of a fresh
mutation. It MUST NOT invent a replay flag or later receipt-row readback.

Checkpoint and result artifacts MUST pass schema, digest, canonical byte-limit,
and contextual prefix validation before publication. Checkpoints use private
same-directory temporary files, file fsync, initial no-clobber publication,
subsequent atomic replacement, and directory fsync. A writer refuses externally
changed checkpoint contents or a substituted symlink. The single-operator
posture also excludes concurrent mutation of operator artifacts; this is not
a hostile-filesystem locking protocol.

Once a write transport is invoked, a rejection, timeout, or malformed response
produces `partial`, even when the accepted prefix is empty. It never claims
that the first write could not have committed. Failure before any submission
may produce `not_applied`; untrusted plan/approval identities produce only an
error envelope, not fabricated correlated artifacts. A binding precondition
failure after earlier writes stops at that action and reports the accepted
prefix. Error facts may retain a bounded public Spine machine error code, not
arbitrary response messages or raw process output.

Checkpoint publication failure stops immediately: no next command is submitted
and no terminal success is fabricated. A crash or durability failure may leave
only the previous or replacement checkpoint. Result-file publication failure
also retains the checkpoint. Preserve these files; do not delete the checkpoint
and rerun as a fresh installation. Resume/recovery belongs to Slice 4.

## Input boundary

Owner IDs, delivery targets, subjects, routes, and environment-specific facts
must enter, if needed, as explicit operator-supplied installation inputs or as
Spine-owned state. They must never be persisted into a reusable pack. The
installer must expose the distinction between pack content and operator input
in its plan.

## Repository boundary

No Spine runtime change belongs in this repository. If installation reveals a
missing Spine command, that gap must be raised with Spine as a separate design
and change process; it must not be bypassed with database access or an embedded
runtime patch here.
```

### Spec 2: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer.md

Hash: d8aad07ed095e99b63ed34b59490106b8aab5217eb7eb9ee9f18e59915c56e02

```markdown
# Installer contract

Status: Draft v0.4; planning, preflight, and initial apply implementation authorized

## 1. Purpose and authority

This document specifies the intended first installer for declarative Spine
packs. The installer is a bounded client and reconciler. It validates one pack,
resolves an operator-selected portion of that pack, compares the desired
definitions with one Spine owner-scoped catalog, applies an explicitly approved
plan through Spine's public command surface, and verifies the resulting state.

The installer is not an authority for installed state. Spine remains the sole authority
for archetypes, notification profiles, default bindings, command
receipts, ownership, and current catalog state. Installer request, plan,
approval, result, and verification artifacts are portable evidence and
operator intent; none is a second ledger or proof that Spine still has a given
state.

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** describe implementation
requirements. Authorized slices are read-only `plan`, non-mutating preflight,
and initial approved `apply` with durable checkpointing, using the source-tree
layout in `specs/architecture.md`. Continuation, `verify`, recovery, remote
transports, and release packaging require separate review and authorization.
No Spine runtime change is authorized.

## 2. Inputs and non-goals

Installation requires four distinct inputs:

1. one complete `spine.pack-manifest.v1` manifest;
2. an explicit selection of the whole pack or one or more archetype keys;
3. one exact operator-owned Spine catalog scope; and
4. transport configuration for one Spine target.

The owner scope and target configuration are installation facts, not pack
content. They MUST NOT be copied into a reusable pack. Operator artifacts MAY
contain owner and actor IDs because they are environment-specific by design;
they MUST remain separate from `packs/` and MUST NOT be presented as reusable
content.

Version 1 does not provide:

- direct Spine database access, including read-only access;
- a daemon, service, scheduler, ledger, or background reconciliation loop;
- pack discovery, registry lookup, download, signing, or publisher trust;
- dependency resolution, because v1 manifests require `dependencies=[]`;
- profile-only or template-level selection;
- section selection such as `Travel` or `Health`;
- interactive prompts or a wizard;
- uninstall, retirement, pruning, or removal of definitions omitted from a
  selection;
- mutation of existing item schedules or profile applications; or
- whole-pack transactional atomicity across separate Spine commands.

## 3. Inspected Spine baseline

This draft is grounded in the committed Spine runtime `0.3.0` artifacts at
commit `72203f092de191a7633b1884bf0d61836a25abe4`, ledger schema `12`.
Uncommitted Spine checkout state is not evidence for this contract.

The supported command set is deliberately closed:

| Phase | Spine public commands |
| --- | --- |
| Environment preflight | `system.info` |
| Catalog discovery and comparison | `item_archetype.list`, `item_archetype.show`, `notification_profile.list`, `notification_profile.show`, `notification_profile.binding.list` |
| Archetype writes | `item_archetype.create`, `item_archetype.revise` |
| Profile writes | `notification_profile.create`, `notification_profile.metadata.update`, `notification_profile.revise` |
| Binding writes | `notification_profile.binding.set` |

The installer MUST NOT call retirement, binding-removal, item-scheduling,
notification-delivery, owner-creation, or lower-level ledger commands. It MUST
NOT use an internal Spine Python API as a substitute for the public command
surface. The v1 implementation uses the local `spine-command` CLI transport
and MUST submit and validate the same closed public request and response objects
used by every Spine transport. The exact local transport configuration fields
and normalization rules are defined in `specs/installer-artifacts.md`.

The complete execution-contract union derived from the Spine `0.3.0` compiled
command registry for the commands above is:

- `spine.canonical-json.v1`;
- `spine.item-archetypes.v1`;
- `spine.notification-profile-bindings.v1`;
- `spine.notification-profile-catalog-cursor.v1`;
- `spine.notification-profile-metadata-update.v1`;
- `spine.notification-profile-readback.v1`;
- `spine.notification-profiles.v1`;
- `spine.system-info.v2`; and
- `spine.tickerd-compatibility.v1`.

`system.info` MUST succeed before catalog interpretation. Its exact
`runtime_version` MUST appear in the pack manifest's runtime allowlist, every
manifest content contract MUST be advertised, and every contract in the
execution union above MUST be advertised. A mismatch fails before a plan is
classified. Content compatibility is not sufficient evidence of execution
readiness.

Supporting another Spine runtime requires a separately reviewed command map
and execution-contract union. In particular, the currently inspected committed
Spine `0.4.0` head MUST NOT be treated as compatible with a pack that allows
only `0.3.0`.

## 4. Agent-oriented CLI surface

The first control surface SHOULD be a local, non-interactive CLI with exactly
three top-level operations:

```text
spine-packs plan
spine-packs apply
spine-packs verify
```

The CLI MUST emit exactly one structured JSON result to standard output. Human
diagnostics MAY be written to standard error, but they MUST NOT contain the
only copy of a decision, error code, or receipt reference. Pretty-printed text
MAY be offered explicitly; JSON remains the automation contract.

No operation may prompt. Missing choices fail closed. Full-pack selection MUST
be explicit rather than a default.

The request file is the authoritative input, including selection:

```sh
spine-packs plan --manifest PATH --request REQUEST --output PLAN
```

Optional `--all` or repeated `--archetype KEY` flags are assertions about that
input. They MUST normalize to exactly its selection. Repeated archetype flags
are sorted and deduplicated before comparison; supplying both flag modes, an
empty key, or a mismatch fails as `invalid_cli_or_artifact_input` before
catalog reads. Flags never override or repair the saved request or its digest.
With no selection flags, the validated request alone supplies selection.

`apply` MUST consume a saved plan and an explicit approval. It MUST NOT accept
fresh pack-selection flags:

```sh
spine-packs apply --manifest MANIFEST --plan PLAN --approval APPROVAL --checkpoint CHECKPOINT --output RESULT
```

`verify` MUST consume the approved plan, target configuration, and any apply
result whose receipt evidence is being correlated:

```sh
spine-packs verify --plan PLAN --result RESULT --output VERIFICATION
```

Paths, executable locations, database paths passed through to the Spine CLI,
credentials for a future transport, and similar environment facts are
transport configuration. They MUST NOT enter a pack or its content digest.
Passing a database path to `spine-command` does not authorize the installer to
open that database itself.

The local v1 request MUST name an observable target binding containing the
normalized local host, resolved Spine command executable path and hash, and
resolved ledger path. These facts are recorded in the plan and checked again
by `apply`.
They do not become pack content and do not claim a globally stable Spine ledger
identity.

## 5. Pack validation and selection

### 5.1 Complete-pack validation

`plan` MUST validate the complete manifest in the order required by
`specs/pack-format.md` before applying a selection. Selection MUST NOT turn an
invalid pack into a valid subset or hide an invalid unselected definition.

A released manifest is eligible for application. A draft manifest MAY be
planned only when the request explicitly permits draft inspection. A plan for
a draft MUST be marked ineligible for `apply`; there is no implicit
development override.

The installer MUST reject non-empty dependencies under
`spine.pack-manifest.v1` rather than ignoring them.

### 5.2 Selection modes

A request selects exactly one mode:

- `all`, which selects every archetype, profile, and binding intent in the
  manifest; or
- `archetypes`, which contains a sorted, unique, non-empty list of exact
  `archetype_key` values.

Unknown keys, duplicate keys, unsorted request-file keys, an empty archetype
selection, both modes, or neither mode fail closed. Repeated CLI flags MAY be
normalized to sorted unique request values before the normalized request is
shown to the operator.

### 5.3 Inferred archetype units

For each selected archetype key, the installer includes:

1. that archetype definition;
2. its pack-local `archetype_default` binding intent when one exists; and
3. the notification profile referenced by that intent.

The selected objects form an inferred installation unit. The unit is not a new
manifest object and is never written to Spine. If selected archetypes reference
the same profile, their closure contains one profile and each applicable
binding. An archetype with no default intent selects only the archetype.

Granular selection does not include unreferenced profiles. Full-pack selection
does include them. Version 1 therefore supports exact archetype-key selection,
not human documentation sections or arbitrary template edits.

## 6. Exact owner scope

One plan targets exactly one canonical owner object:

- `owner_kind=subject` with one `owner_subject_id`; or
- `owner_kind=subject_group` with one `owner_group_id`.

The selected owner applies to every definition and binding in the plan. System
ownership is not accepted because Spine `0.3.0` dynamic-catalog writes reject
operator creation or modification of system-owned roots. Cross-owner fallback,
membership inference, and multi-owner installation are outside v1.

The actor used for writes is distinct from the catalog owner. Spine `0.3.0`
treats `actor_subject_id` as command attribution and requires it to resolve;
the installer MUST NOT claim that this is authentication or authorization.
Admission and permission checks remain the responsibility of the selected
Spine transport and deployment.

## 7. Catalog observation

Planning MUST observe Spine only through the bounded list and show commands in
Section 3. Lists MUST use Spine's explicit limits, ordering, and cursors until
the relevant owner-scoped catalog is exhausted. The installer MUST validate
every response envelope, canonical command name, response-contract identifier,
pagination fact, and entry shape before using it.

`plan` MUST NOT invoke a Spine write command, including with Spine's dry-run
transport flag. Planning is an independent read-only comparison, not a batch of
speculative write requests.

A stale catalog cursor, malformed response, missing page, duplicated page
entry, unresolved owner, transport failure, or changing snapshot fails the
plan. The operator or agent may start a new plan; the installer MUST NOT merge
pages from different catalog snapshots.

The completed owner-scoped archetype, profile, and binding catalog snapshot
hashes are observable target facts. They MUST be included in the plan together
with the normalized host, resolved executable path and hash, resolved ledger
path, exact owner scope,
runtime version, implemented and current ledger schema versions, and required
contract evidence.

Matching is by exact owner-local `archetype_key` or `profile_key`. Generated
Spine IDs, revision numbers, audit IDs, timestamps, and normalized hashes are
observed provenance and precondition facts; they are not pack identity.

## 8. Equivalence and drift

Comparison occurs against Spine's normalized public readback. The installer
MUST compare closed semantic values, not presentation produced by a human CLI
renderer. Strings are exact, including case and whitespace. `null` and a string
are distinct. Arrays are compared in their canonical contract order.

Spine normalized hashes MAY corroborate comparison, but a hash alone MUST NOT
replace validation and comparison of the corresponding public semantic fields.

### 8.1 Archetypes

An archetype is:

- **missing** when no owner-local root has the selected key;
- **equivalent** when the root is active and its current revision exactly
  matches `display_name`, `description`, and `compatible_item_types`;
- **drifted** when the root is active but any of those current-revision fields
  differs; or
- **blocked** when the matching root is retired or public readback is
  ambiguous or incomplete.

An authorized drift update maps to `item_archetype.revise` with the observed
current revision ID as its expected precondition. Historical revision number
or identity differences do not themselves constitute drift.

### 8.2 Notification profiles

A notification profile root has separate presentation metadata and behavioral
revision semantics:

- root metadata is exactly `display_name` and nullable `description`;
- behavioral revision content is exactly `compatible_item_types` and the
  normalized ordered templates, including schedule and late handling.

A missing key maps to one `notification_profile.create`. An active profile with
equal metadata and revision content is equivalent. Metadata drift maps, when
explicitly authorized, to `notification_profile.metadata.update` with the
complete observed metadata preimage. Behavioral drift maps, when explicitly
authorized, to `notification_profile.revise` with the observed current revision
ID. If both differ, the plan contains two separately visible update actions.

A matching retired profile or incomplete readback is blocked. Revising a
profile changes only its current revision for future applications; the
installer MUST NOT claim that existing item-owned policies were upgraded.

### 8.3 Default bindings

A selected binding intent is:

- **missing** when no active binding exists for the selected owner and resolved
  archetype ID;
- **equivalent** when the active binding points to the resolved desired profile
  ID; or
- **drifted** when it points to another profile ID.

The plan MUST preserve the desired keys' resolved owner-local root IDs and
the observed active binding's ID, archetype ID, and profile ID separately from
semantic key projections, using the closed identity evidence in
`specs/installer-artifacts.md` Section 7. Matching projected keys alone MUST NOT
establish equivalence. Missing roots have no generated ID until Spine creates
them; their binding requests reference the earlier create action's result.

An authorized missing or drifted binding maps to
`notification_profile.binding.set`. Historical retired bindings do not cause
drift. Replacing a binding affects future default resolution only and MUST NOT
be described as changing existing item schedules.

### 8.4 Plan-wide posture

Every selected object receives one classification. The plan MUST expose both
desired and observed semantic preimages for every drift and enough identity to
review the proposed Spine command.

Blocked objects make the plan intrinsically ineligible for application.
Drift makes a plan decision-bearing, but does not by itself make the stored
`apply_eligible` value false. A released, compatible, unblocked plan remains
intrinsically eligible when every drift has its corresponding update action,
as specified in `specs/installer-artifacts.md` Section 7.

Eligibility is not execution authorization. The unchanged plan MUST NOT be
executed until an explicit approval authorizes the complete plan and every
proposed update. Approval MUST NOT change `apply_eligible` or the plan digest.
An otherwise eligible released plan with drift produces `decision_required`
and exit 5, not permission to execute. The installer MUST NOT apply only the
missing portion of a selected scope while silently skipping blocked or
unauthorized drift.

## 9. Deterministic plan

A plan is a closed, immutable artifact for one manifest digest, normalized
selection, owner scope, Spine target, and observed state. It MUST include:

- the pack schema, ID, version, status, and content digest;
- the normalized selection and inferred closure;
- the exact owner scope;
- the normalized local host, resolved Spine command executable path and hash,
  resolved ledger path, and environment compatibility evidence;
- the closed installer command set and required execution-contract union;
- observed catalog identities, current revision IDs, semantic preimages, and
  relevant snapshot hashes;
- one classification for every selected object;
- ordered proposed actions and their preconditions;
- an explicit list of decision-bearing and blocked action IDs;
- whether the plan is apply-eligible; and
- a content identity under `spine.canonical-json.v1`.

The plan digest preimage MUST omit only its own digest field. Its exact
derivation identifier and JSON Schema are defined in
`specs/installer-artifacts.md` and `contracts/schemas/`.
Ambient timestamps, manifest source and output paths, random IDs, terminal
formatting, and catalog page size MUST NOT affect plan identity. The configured
target host, executable path and hash, and ledger path are target-binding facts
and MUST affect plan identity.

Actions MUST be deterministically ordered:

1. archetype creates and revisions by `archetype_key`;
2. profile creates by `profile_key`;
3. profile metadata updates by `profile_key`;
4. profile revisions by `profile_key`; and
5. binding sets by `archetype_key`.

Equivalent objects produce explicit retain classifications but no Spine write
action. The plan MUST never claim that a retain created a Spine receipt.

## 10. Approval and update authorization

An approval is a separate closed artifact bound to exactly one plan digest. It
MUST authorize application of the complete plan. For each drift update, it
must additionally name the exact action ID being authorized. A blanket
`allow_updates=true`, wildcard, archetype prefix, or approval of a different
plan digest is insufficient.

Create actions need no drift-specific authorization, but they still require
approval of the complete plan. Binding replacement, archetype revision,
profile metadata replacement, and profile behavioral revision are updates and
require individual authorization.

Changing a selection, desired value, observed preimage, owner, target,
compatibility fact, or proposed action changes the plan digest and invalidates
the approval. Approval does not waive compatibility or blocked-state failures.

The first local CLI may treat approval as an operator assertion. It MUST NOT
claim a cryptographic signer, authentication ceremony, or Foreman approval
unless a later reviewed integration provides that evidence.

## 11. Apply behavior

An apply invocation is either an initial execution or a continuation of the
same execution identity. A continuation MUST retain the exact plan digest,
approval digest, execution identity, actor, action timestamp, ordered requests,
and derived command IDs. Changing any of those facts starts a different
execution and MUST NOT inherit an accepted prefix or preserved response
evidence.

On an initial execution, before the first write, `apply` MUST:

1. validate the plan and approval contracts and digests;
2. reload and validate the complete manifest and require its identity to match
   the plan;
3. confirm the exact planned local host, Spine command executable path and
   hash, and configured ledger path;
4. reconnect through `spine-command` to that configured target;
5. repeat `system.info` and require the planned runtime, implemented and
   current schema, and contract facts;
6. re-read the owner-scoped catalogs and require the planned catalog snapshot
   hashes and every selected precondition;
7. fail if the plan is stale, blocked, draft-based, or incompletely
   authorized; and
8. validate every ordered command template and its generated-ID references.

Requests whose IDs are already known can be materialized at initial preflight.
A request consuming an earlier create result MUST be materialized only after
the required response prefix has been validated, and before its own durable
pre-submit checkpoint. The shared validation and materialization rules in
`specs/installer-artifacts.md` Section 7 apply to every command; initial
preflight MUST NOT guess future generated IDs.

The initial preflight is all-or-nothing: no planned write may occur if any
selected target fact, original catalog snapshot, or object precondition has
changed. The final initial-preflight observation MUST occur immediately before
the write sequence begins.

Each apply invocation requires a stable execution identity, exact
`actor_subject_id`, and exact `action_timestamp_utc`. Every planned action MUST
receive a stable, globally unique Spine `command_id` derived reproducibly as
defined in `specs/installer-artifacts.md`. Retrying the same execution MUST
reuse the exact command ID, actor, timestamp, and semantic request so Spine's
compatible replay returns the original command receipt.

The installer MUST validate each Spine response before proceeding and record
its command, effect, generated IDs, and command-receipt facts. It stops at the
first rejected or malformed response. It MUST NOT compensate by retiring,
removing, or reversing an already accepted earlier action.

Each validated command response MUST be preserved in the local recovery
checkpoint before the installer advances to the next action. If the process
stops after Spine accepted a command but before that response was durably
recorded, retry
uses the same stable command ID and exact semantic request so Spine can return
the compatible replay response. Checkpoint replacement and durability follow
`specs/installer-artifacts.md` Section 9.

A continuation MUST load the most recent preserved recovery checkpoint for the
same execution identity, or derive the equivalent checkpoint from a validated
terminal partial result, before submitting a command. When a terminal result is
the source, continuation persists the derived checkpoint before any retry. The
continuation MUST validate its digest and exact correlation to the plan,
approval, execution
identity, ordered action prefix, requests, command IDs, actor, timestamps,
response contracts, effects, generated IDs, and receipt facts. Missing,
non-contiguous, contradictory, or invalid preserved evidence fails closed.

The longest contiguous sequence of actions with validated successful or
compatible-replay responses is the **accepted prefix**. Using the original
planned catalog and the validated Spine responses for that prefix, the
installer MUST derive the exact catalog state and snapshot expected after the
prefix. Generated Spine IDs and revision IDs used by later actions MUST come
from those validated responses or matching public readback; they MUST NOT be
guessed.

Before resuming, `apply` MUST repeat the target, manifest, approval, and
`system.info` checks required by initial preflight, then re-read the complete
relevant owner-scoped catalogs. That observation MUST match exactly one of:

1. the derived state after the accepted prefix, with the first unresolved
   action not reflected; or
2. when the first unresolved action lacks a durably recorded validated success
   response, the exact state that would result from that one action succeeding.

Case 2 represents an uncertain response-recording boundary, not proof of a
receipt. In either case, the installer MUST submit the first unresolved action
with its original command ID and exact request. Spine's compatible replay or
new acceptance response MUST be validated and durably recorded before the
remaining suffix can proceed. A previously recorded validated rejection is not
an accepted action; replaying its unchanged request may reproduce the rejection
and the installer then stops again.

The continuation preflight MUST also require every remaining suffix
precondition against the derived expected state. Any catalog difference not
explained exactly by the accepted prefix and, at most, the first unresolved
action makes continuation stale and aborts before another command is
submitted. Preserved local evidence is not installation authority: Spine
public readback and compatible command replay remain authoritative.

Spine makes each command atomic, but the command family provides no
whole-pack transaction. An apply result therefore has one of these states:

- `applied`: every planned action succeeded or compatibly replayed;
- `partial`: a deterministic prefix succeeded and a later action failed; or
- `not_applied`: preflight failed or no action was submitted.

The accepted prefix may be empty: a failure after the first write transport
invocation is still `partial`, because its commit outcome may be uncertain.
`not_applied` MUST NOT be inferred merely from the absence of accepted response
evidence. The initial-only implementation boundary and durability-failure
handling are specified in `specs/architecture.md`.

A partial result MUST identify the accepted prefix, failed action, exact Spine
error, and unattempted suffix. Safe continuation uses the same execution
identity and exact requests; it does not generate a fresh command ID for an
already attempted action.

The result is an operator artifact, not a new receipt authority. Spine command
receipts remain authoritative.

## 12. Staleness and single-operator concurrency posture

Local v1 installation assumes one operator and no concurrent dynamic-catalog
writer against the selected target for the duration of `plan` and `apply`. The
approval MUST acknowledge this operating condition. If an operator cannot
provide it, v1 apply is unsupported and MUST NOT run.

The plan pins the observable target binding, complete relevant owner-scoped
catalog snapshot hashes, semantic preimages, and current revision IDs. Before
the first submitted command of an initial execution, any catalog snapshot
change makes the plan stale, including an unrelated catalog change. The agent
must produce and approve a new plan.

For a continuation of the same execution identity, changes caused by its
validated accepted prefix do not by themselves make the plan stale. The
continuation instead requires the exact derived prefix-aware state defined in
Section 11. Any unrelated change, unexplained selected-object change, response
evidence gap, or mismatch from that derived state makes the continuation stale
and requires a new plan. A new plan is a new execution and cannot reuse the old
execution's accepted-prefix claim.

Archetype and profile revisions use Spine's expected-current-revision
preconditions. Profile metadata updates use Spine's complete expected-metadata
preimage. Owner-local create uniqueness prevents silent duplicate creation.

Spine `0.3.0` `notification_profile.binding.set` does not accept an expected
current binding ID or explicit absent precondition. Immediately before each
binding mutation, the installer MUST re-read that archetype's binding and
compare it with the state expected after the already accepted plan prefix.
This accepted-prefix comparison applies to initial execution and to every
continuation binding except the bounded uncertain-action case below. A mismatch
aborts the remaining suffix without submitting the binding command.

When the binding set is the first unresolved action and continuation preflight
validated Section 11 case 2, the immediate re-read MUST instead match the exact
post-action binding state already validated by that preflight. The installer
may then submit only the original command ID and exact request. The resulting
compatible-replay or new-acceptance response MUST be validated and durably
recorded as required by Section 11. If the immediate re-read no longer matches
that post-action state, the installer MUST abort without submitting the
request. This exception recovers the missing response evidence; it does not
authorize a changed binding request against an unexpected state.

That re-read is sufficient for the declared local single-operator v1 posture;
it is not atomic compare-and-set and MUST NOT be represented as safe
multi-writer reconciliation. True binding compare-and-set is future Spine
hardening for concurrent operators or automation and is not a v1 installer
blocker.

## 13. Verify behavior

`verify` MUST be non-mutating. It repeats environment compatibility checks,
reloads the exact manifest and selected closure, and reads each planned
archetype, profile, and binding through the public command surface.

State verification succeeds only when:

- every selected archetype and profile is active and semantically equivalent
  to the pack definition;
- every selected binding points to the planned profile under the exact planned
  owner;
- no selected object has incomplete or ambiguous readback; and
- the observable target binding and pack identity still match the approved
  plan.

Verification is scoped. It does not report unselected definitions as excess,
does not remove anything, and does not claim the entire pack is installed after
a granular selection.

When an apply result is supplied, verification MUST validate its digest,
plan correlation, ordered action coverage, response contracts, effects,
command IDs, and returned receipt facts. A copied apply response is evidence
that Spine returned a receipt; it is not an authoritative later read of that
receipt.

For a plan containing writes, v1 verification requires the locally preserved
apply result and one captured, validated Spine command response for every
planned write. It then independently verifies resulting catalog state through
fresh public catalog reads. A no-write plan needs no command receipt.

Spine `0.3.0` exposes no public command-receipt show or list command. Replaying
a write request is not acceptable verification because, if the receipt were
absent, it could perform a mutation. V1 therefore reports captured Spine
response evidence and fresh state verification as distinct facts and MUST NOT
claim independent later receipt-row readback. This limitation does not prevent
v1 success when all required command responses are preserved and resulting
state verifies. Public receipt readback remains useful future Spine recovery
and audit hardening, not a v1 installer blocker.

## 14. Structured results and exit behavior

Every operation MUST return a closed result with a stable machine-readable
status and error category. At minimum the categories distinguish:

- invalid CLI or artifact input;
- invalid pack contract or digest;
- incompatible Spine runtime or contracts;
- decision required for drift;
- blocked desired state;
- stale plan or target mismatch;
- Spine command rejection;
- partial apply;
- verification mismatch;
- transport or environment failure; and
- success.

The numeric exit mapping, exact result objects, byte limits, and artifact
contract identifiers are fixed in `specs/installer-artifacts.md`. An
implementation MUST use that mapping rather than inventing another v1 surface.

Plan generation that successfully discovers drift still produces the complete
plan artifact. Its structured status must distinguish a reviewable
decision-required plan from malformed input or environment failure.

For a successfully observed, compatible plan, the following precedence is
normative. The first matching row wins; drift does not override blocked state
or permitted draft inspection.

| Condition | Status / exit | `apply_eligible` |
| --- | --- | --- |
| Any blocked selected object, with or without drift | `blocked` / 6 | false |
| Draft with `inspect_only`, no blocked objects, with or without drift | `success` / 0 | false |
| Released, no blocked objects, with drift | `decision_required` / 5 | true |
| Released, no blocked objects or drift | `success` / 0 | true |

All four outcomes MUST include the complete plan artifact. Draft inspection
MUST preserve drift classifications and proposed update actions for review.
Drafts with `draft_posture=reject` fail before observation with exit 3.
Neither success nor intrinsic eligibility authorizes execution: a future
`apply` still requires approval of the exact immutable plan and every update.

## 15. Sensitive data and output discipline

Reusable packs contain no owner IDs, actor IDs, database paths, credentials,
routes, recipients, delivery targets, or subjects. Installation artifacts MAY
contain the minimum owner, actor, and target references necessary to bind a
plan, but MUST NOT collect notification recipients or delivery routes because
catalog installation does not require them.

Credentials MUST enter through the selected Spine transport's protected
configuration rather than a reusable request file or command-line value likely
to be retained in shell history. JSON output and error messages MUST not echo
credentials or unrelated environment variables.

## 16. Machine-contract layer

The reviewed prose contract now has a draft machine layer in
`specs/installer-artifacts.md`. Closed JSON Schemas and positive and negative
fixtures cover:

- installation request;
- deterministic plan and plan identity;
- approval and per-update authorization;
- apply result and partial-apply recovery;
- verification result; and
- the common error envelope.

Contract tests must cover at least full-pack and granular selection, inferred
closure, draft apply refusal, incompatible runtime and execution contracts,
missing/equivalent/drifted/blocked classifications, metadata-only and
behavioral profile drift, unauthorized updates, stale plan refusal, stable
command replay identity, prefix-aware continuation from a recorded partial
result, accepted-before-response replay, rejection of an unexplained catalog
change during continuation, verification mismatch, and receipt readback
disclosure.

The initial executable vectors cover one complete granular drift flow plus
focused failures for draft eligibility, digest mismatch, authorization,
staleness, prefix continuity, uncertain-response command identity, and target
binding. The remaining cases named above are required before implementation
can claim full behavioral coverage.

No installer package, service, adapter directory, example installation file,
or executable CLI should be added before the machine contracts and fixtures
receive bounded review.

## 17. Review gate and future hardening

The product decisions for the first implementation are settled: it is a local,
single-operator, non-interactive CLI using Spine's public `spine-command`
transport. Exact artifact shapes, digest and command-ID derivations, size
limits, exit codes, checkpoint durability, and local target normalization are
specified in `specs/installer-artifacts.md`. They require bounded review before
runtime scaffolding begins.

The following are useful general Spine hardening, but are not blockers under
the explicit local single-operator v1 assumptions:

- a stable ledger-instance identity exposed by `system.info`, stronger than the
  observable host, configured ledger reference, runtime/schema, owner, and
  catalog snapshots bound into a v1 plan;
- atomic expected-current or expected-absent preconditions for
  `notification_profile.binding.set`; and
- public command-receipt readback for independent recovery and later audit.

None of this future hardening authorizes a Spine change from this repository.
Any such capability must be proposed, reviewed, and implemented in the Spine
repository as a separate body of work.
```

### Spec 3: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer-artifacts.md

Hash: 68ac6dbd6eb3a0cd2c14e6b70147cc80623279eb63e402b47bc5ab1b00832c4f

```markdown
# Installer artifact contracts

Status: Draft v0.1; planning, preflight, and initial apply implementation authorized

## 1. Scope and authority

This document fixes the machine-readable artifact layer for the local v1
installer specified by `specs/installer.md`. It defines the exact artifact
identifiers, target binding, normalization, identities, ordering, continuation
checkpoint, result statuses, size limits, and process exit codes.

These artifacts are operator intent and portable evidence. They are not a
ledger, receipt authority, ownership authority, or proof of current installed
state. Spine remains authoritative. An implementation MUST validate Spine's
public request and response contracts independently of these schemas and MUST
interact with Spine only through `spine-command`.
Direct database access is forbidden.

The schemas in `contracts/schemas/` and the semantic rules in this document
together form the contract. JSON Schema alone cannot express digest
derivation, canonical ordering, cross-artifact correlation, contiguous-prefix
rules, or public-contract validation of embedded canonical JSON.

## 2. Contract family

The v1 family contains these closed artifacts:

| Artifact | `artifact_schema` |
| --- | --- |
| normalized request | `spine.pack-install-request.v1` |
| deterministic plan | `spine.pack-install-plan.v1` |
| approval and execution authorization | `spine.pack-install-approval.v1` |
| durable apply checkpoint | `spine.pack-apply-checkpoint.v1` |
| terminal apply result | `spine.pack-apply-result.v1` |
| verification result | `spine.pack-verification-result.v1` |
| one-line CLI result envelope | `spine.pack-installer-result.v1` |

The public schemas are stable entry points into the shared definitions in
`spine-pack-installer-types.v1.schema.json`. Consumers MUST resolve that sibling
schema and select the
schema named by `artifact_schema`; accepting a structurally similar artifact
under another identifier is forbidden.

## 3. Encoding, closure, and limits

Artifacts MUST be UTF-8 JSON with no byte-order mark, duplicate object member,
unpaired Unicode surrogate, or JSON number. Decimal quantities are canonical
decimal strings: `0` or a non-zero leading digit followed by digits. Timestamps
are second-precision UTC values ending in `Z`.

Every artifact object and nested object defined here is closed. The only
intentionally embedded open data is Spine public data represented as a
`canonical_value`: its `canonical_json` member is a string containing one
complete `spine.canonical-json.v1` value. The installer MUST parse that string,
reject duplicate members and numbers, require byte-for-byte canonical form,
validate it against the named contract AND its required `shape`, and verify
its SHA-256 digest before use. `shape` names a definition in
`spine-pack-embedded-values.v1.schema.json`. Unknown contracts, unknown shapes,
and a shape inappropriate for the containing field fail closed. The contract
identifier alone identifies a family, not a unique request/response shape.

The embedded schema pins reachable public definitions from Spine commit
`72203f092de191a7633b1884bf0d61836a25abe4`; command templates omit only the
three execution fields, and materialized requests require them. Response
definitions preserve the six public commands' actual fields and effects.
Semantic projections below are installer comparison values extracted only
after public readback validation; they are not full Spine response envelopes.
The schema's source comment records the derivation. No Spine code is imported
or executed by these repository checks.

Limits apply to the complete compact canonical UTF-8 encoding of an artifact:

| Artifact | Maximum bytes |
| --- | ---: |
| request | 65,536 |
| plan | 8,388,608 |
| approval | 262,144 |
| checkpoint | 16,777,216 |
| apply result | 16,777,216 |
| verification result | 16,777,216 |
| CLI result envelope | 1,048,576 |

An artifact at the limit is accepted. A larger artifact fails as
`invalid_cli_or_artifact_input` before semantic use.

## 4. Canonical ordering

Object-member order is insignificant on input and canonicalized by Unicode
codepoint. Array order is significant and MUST already be canonical as follows:

- selected, closure, contract, decision, blocked, generated-ID, unattempted,
  and fact-name arrays are strictly ascending by the named string key;
- catalog snapshots are `archetypes`, `profiles`, then `bindings`;
- classifications are archetypes by `archetype_key`, profiles by
  `profile_key`, then bindings by `archetype_key`;
- actions use the ordering in `specs/installer.md` Section 9 and contiguous
  decimal ordinals beginning with `0`;
- response evidence follows action order and is a contiguous plan prefix;
- verification object results follow classification order.

Duplicate array identities fail closed even when the schema's structural
uniqueness check would not catch two differently encoded entries with the same
semantic key.

## 5. Content identity

Every artifact except the CLI result envelope has `content_identity` with:

- `algorithm=sha256`;
- `canonical_json_version=spine.canonical-json.v1`;
- the artifact-specific `derivation_version` below; and
- a lowercase 64-character hexadecimal `digest`.

The digest is SHA-256 over the UTF-8 bytes of `spine.canonical-json.v1` applied
to the complete artifact while omitting only
`content_identity.digest`. The remaining `content_identity` members stay in
the preimage.

| Artifact | `derivation_version` |
| --- | --- |
| request | `spine.pack-install-request-digest.v1` |
| plan | `spine.pack-install-plan-digest.v1` |
| approval | `spine.pack-install-approval-digest.v1` |
| checkpoint | `spine.pack-apply-checkpoint-digest.v1` |
| apply result | `spine.pack-apply-result-digest.v1` |
| verification result | `spine.pack-verification-result-digest.v1` |

Embedded `canonical_value.digest` values are SHA-256 over the exact UTF-8
bytes in `canonical_json`, after canonical form has been proven.

## 6. Normalized request and local target

A request contains exactly one selection, one owner, one local target, and a
draft posture. `selection` is either `{ "mode": "all" }` or
`mode=archetypes` with a sorted unique non-empty `archetype_keys` array.
`draft_posture` is `reject` or `inspect_only`; draft-based plans are never
apply-eligible under either posture.

The saved request is authoritative. Optional CLI selection flags are matching
assertions only, following `specs/installer.md` Section 4. Conflicting flags or
flags that disagree with the request fail before catalog reads.

Owner shape is exactly one of:

- `owner_kind=subject` and `owner_subject_id`; or
- `owner_kind=subject_group` and `owner_group_id`.

The local target contains:

- `host_name`: the lowercase ASCII fully qualified host name returned by the
  configured local host resolver after removing one trailing dot;
- `spine_command.path`: the absolute, symlink-resolved executable path;
- `spine_command.sha256`: SHA-256 of the executable bytes at plan time; and
- `ledger.path`: the absolute, symlink-resolved existing ledger file path.

Paths use `/`, contain no empty component, `.` or `..` component, and have no
trailing slash. The root path is not valid for either field. `~`, environment
variables, relative paths, URI forms, and opaque ledger aliases are unsupported
in local v1. The request producer resolves paths before serializing the
request. `plan`, `apply`, and `verify` repeat resolution and fail on a mismatch.
The installer passes `ledger.path` to `spine-command`; it MUST NOT open the
ledger itself.

The executable hash is target-binding evidence, not a software-signing or
publisher-trust claim. Credentials are not request fields.

## 7. Plan

The plan embeds the normalized request without its request
`content_identity`, references the request digest separately, and includes:

- pack identity and manifest content digest;
- inferred closure;
- environment evidence from validated `system.info`;
- the fixed execution-contract union;
- all three complete catalog snapshot hashes;
- one desired/observed classification for every selected object;
- deterministic proposed actions;
- decision-bearing action IDs and blocked object keys;
- `apply_eligible`; and
- plan content identity.

`environment.ledger_schema_implemented` and
`environment.ledger_schema_current` are decimal strings. Advertised contracts
are sorted and unique. `required_execution_contracts` is exactly the closed
union in `specs/installer.md` Section 3.

Each classification names its object kind, canonical object key,
classification, desired semantic value, nullable observed semantic value,
identity evidence, and nullable blocked reason. Archetype keys are encoded as `archetype:<key>`,
profile keys as `profile:<key>`, and bindings as `binding:<archetype-key>`.
`missing` has `observed=null`; `blocked` has a non-null reason; every other
classification has observed data and no blocked reason.

Every non-null desired, observed, or expected comparison value has the same
closed projection shape for its object kind, independent of classification:

| Object | Shape | Complete comparison value |
| --- | --- | --- |
| archetype | `archetypeSemantics` | `display_name`, `description`, `compatible_item_types` |
| profile | `profileSemantics` | `metadata: {display_name, description}` and `revision: {compatible_item_types, templates}` |
| binding | `bindingSemantics` | `binding_kind=archetype_default`, `notification_profile_key` |

These use `spine.item-archetypes.v1`, `spine.notification-profiles.v1`, and
`spine.notification-profile-bindings.v1`, respectively. Profile action
preimages retain BOTH metadata and revision even if only one is being changed.
Action requests project the appropriate fields into the public command.
Binding profile keys are resolved through the exact owner-local catalog;
equivalence additionally requires the resolved Spine IDs to match as specified
in installer Section 8.3. A key projection does not replace ID preconditions.
Incomplete or ambiguous readback yields a blocked classification with
`observed=null`, never a fabricated partial projection.

`identity` is required and separate from the owner-neutral semantic projection:

- An existing archetype or profile has `{catalog_id}` containing its exact
  Spine root ID resolved by that key under the plan's owner. A missing root has
  `identity=null`. Blocked roots MAY use null when identity cannot be resolved
  unambiguously. Two keys of the same object kind MUST NOT claim the same ID.
- A non-blocked binding has `{item_archetype_id, notification_profile_id,
  observed_binding}`. The first two fields resolve its archetype key and desired
  profile key and MUST match the corresponding root classifications' catalog
  IDs. A field is null only when that root is missing; IDs MUST NOT be guessed
  before creation. A blocked dependency requires a blocked binding.
- `observed_binding` is null for missing bindings; otherwise it contains exactly
  `notification_profile_binding_id`, `item_archetype_id`, and
  `notification_profile_id` from validated active-binding readback under the
  exact plan owner. Its archetype ID MUST match the resolved archetype ID.
  An equivalent binding requires a non-null resolved desired profile ID equal
  to its observed profile ID, as well as equal semantic projections. Drift
  requires a different observed profile ID (including when the desired profile
  is missing). Contradictory key and ID evidence fails closed; a matching key
  cannot hide an ID mismatch. A blocked binding uses `identity=null` rather
  than partial or ambiguous evidence.

Identity evidence participates in the plan digest. Binding-set templates MUST
use those resolved IDs and the exact plan owner. For a missing dependency,
the ID-valued field MUST instead reference the corresponding earlier create
action's returned root ID using the reference syntax below. Existing IDs and
observed binding identities are never result-reference strings. Initial apply
preflight rechecks this evidence through Spine public readback; stored evidence
does not replace authoritative observation.

Command-specific shapes use the prefixes `archetypeCreate`, `archetypeRevise`,
`profileCreate`, `profileMetadataUpdate`, `profileRevise`, and `bindingSet`,
followed by `Template`, `Request`, or `Response`. The surrounding action's
command determines the required prefix and contract; the containing field
determines the suffix. The data cannot choose a weaker shape. All semantic
preimages, templates, checkpoint requests, captured responses, and verification
observations MUST pass their contextual shape checks.

Each action has a zero-based ordinal, an `action-NNNNNN` ID where the numeric
portion equals the ordinal, exact Spine command, catalog object key,
`change_kind` of `create` or `update`, desired and nullable expected preimages,
and a canonical request template with its digest. Create actions have
`expected=null`; updates have a non-null expected preimage.

The request template is the exact Spine request except that it omits
`command_id`, `actor_subject_id`, and `action_timestamp_utc`. It MAY contain a
generated-ID reference string only in an ID-valued field:

```text
${spine-pack.result:<earlier-action-id>:<field-name>}
```

The referenced action MUST precede the consumer, and `<field-name>` MUST be an
ID returned by that action's validated public response. The closed v1 reference
mapping is:

| Consumer command | Top-level field | Required producer | Returned field |
| --- | --- | --- | --- |
| `notification_profile.binding.set` | `item_archetype_id` | `item_archetype.create` for that binding's archetype key | `item_archetype_id` |
| `notification_profile.binding.set` | `notification_profile_id` | `notification_profile.create` for that binding's desired profile key | `notification_profile_id` |

The root classification MUST be missing with null identity. The producer MUST
be its unique create action, with the same owner, key, and complete desired
definition. A root with a resolved catalog ID MUST use that literal ID, never
a result reference. No other command, field, nested member, or returned field
permits a reference in v1; in particular, revisions and metadata updates target
already-existing roots and use literal observed IDs and preconditions.

One shared validation rule MUST inspect all command templates. `${` is reserved
for interpolation in command values and member names; malformed, partial,
concatenated, unknown, self, forward, missing-producer, or contextually forbidden
references fail closed. A reference must occupy the entire allowed field value.
This installer rule is additional to Spine's public non-empty-string ID shapes.

Materialization MUST revalidate the plan, approval, template, and reference
mapping. For a referenced action, it requires a contiguous validated accepted
response prefix through the action immediately before the consumer. Each
producer response MUST match its action, derived command ID, public response
shape, effect, receipt facts, generated-ID evidence, and requested create key.
Values come from the decoded validated public response, not an uncorrelated ID
map. Rejected, missing, malformed, or contradictory evidence fails closed.

Materialization replaces references exactly once, injects the three execution
members, rejects any remaining interpolation syntax anywhere in the request,
then validates the complete public command shape. Captured responses MUST NOT
contain interpolation syntax either; a returned reference is never evaluated
recursively. The resulting canonical bytes and digest are preserved in the
checkpoint before submission. Continuation re-derives them from the same
validated prefix and MUST match those bytes, including on compatible replay.
Like every embedded canonical value, the template digest is SHA-256 of its
exact canonical UTF-8 bytes, as specified in Section 5.

`decision_action_ids` contains exactly every update action and no create.
`blocked_object_keys` contains exactly every blocked classification. A plan is
apply-eligible only when the manifest is released, no object is blocked, every
required compatibility fact matches, and every drift has a corresponding
update action. Approval is separate; absence of approval does not change the
plan's `apply_eligible` value.

Manifest source path, request path, output path, page size, planning timestamp,
terminal formatting, and random values are absent and cannot affect identity.

## 8. Approval and command identity

An approval binds exactly one plan digest, asserts approval of the complete
plan, acknowledges the single-operator/no-concurrent-writer condition, names
exactly every update action being authorized, and fixes one execution object:

- `execution_id`: a lowercase RFC 4122 UUID version 4;
- `actor_subject_id`: the exact existing Spine subject used for attribution;
  and
- `action_timestamp_utc`: one timestamp reused by every command in the
  execution.

`authorized_update_action_ids` MUST equal the plan's
`decision_action_ids`. An approval for a create-only plan uses an empty array.

For each action, command identity is:

```text
spack_<sha256(canonical({
  "action_id": action_id,
  "derivation_version": "spine.pack-command-id.v1",
  "execution_id": execution_id,
  "plan_digest": plan_digest
}))>
```

The angle-bracket expression contributes the lowercase 64-character digest,
so the final command ID is 70 characters. This form is valid under Spine
0.3.0's non-empty ID contract. The exact command ID, actor, timestamp, and
materialized request MUST be reused for continuation or uncertain-response
replay. Reusing an execution ID with a different plan or approval is invalid.

## 9. Durable checkpoint and recovery

The checkpoint is the only non-terminal apply artifact. It correlates the
plan, approval, execution, a contiguous accepted response prefix, and the next
possibly submitted action.

Before submitting each Spine write, apply MUST atomically replace the
checkpoint with:

- all previously accepted response evidence;
- `unresolved_submission` containing the next action ID, exact derived command
  ID, exact materialized request as canonical JSON, and its digest; and
- `next_action_id` equal to that action.

The checkpoint uses `submission_state=prepared_or_submitted` because a crash
cannot reliably distinguish the instant before transport submission from an
accepted command whose response was not recorded. On a validated success or
compatible replay, apply atomically replaces the checkpoint again: it appends
the response evidence, clears `unresolved_submission`, and advances
`next_action_id`. After the last action, `next_action_id` is null. Atomic
replacement means write a same-directory temporary file, flush file contents,
rename over the checkpoint, and flush the containing directory.

An initial execution MUST refuse an existing checkpoint for another
plan/approval/execution. A continuation MUST verify the checkpoint digest,
derive and validate every command ID and request again, and require its
responses to form the exact action prefix. If `unresolved_submission` is
present, it MUST name the first action outside that prefix and match
`next_action_id`. The continuation performs the prefix-aware Spine readback in
`specs/installer.md`, then submits that exact request even when it may never
have reached Spine; the stable command ID makes both cases safe.

The checkpoint is local recovery evidence, not authority to skip Spine
readback. A missing, torn, oversized, noncanonical, contradictory, or
uncorrelated checkpoint fails closed.

## 10. Apply result

An apply result is terminal and has state:

- `applied`: all actions have accepted or compatible-replay evidence;
- `partial`: a contiguous prefix has evidence, one action has a validated
  rejection or transport/response failure, and the remaining suffix is
  unattempted; or
- `not_applied`: preflight failed or no command was submitted.

Response evidence records action ID, command, derived command ID, outcome,
response contract, effect, sorted generated IDs, Spine receipt facts, exact
canonical response JSON, and its digest. `accepted` and `compatible_replay`
both belong to the accepted prefix. The installer MUST derive outcome from the
validated public response and receipt correlation, not from HTTP/process
success alone.

`partial` has a non-null failure naming the first action outside the accepted
prefix and `unattempted_action_ids` equal to the later suffix. `not_applied`
has empty response evidence and a non-null failure. Its unattempted list names
every plan action. A `partial` prefix may be empty when the first submission
fails or has an uncertain response; lack of evidence is not evidence that no
command was submitted. `applied` has null failure
and no unattempted actions. A process crash may leave only a checkpoint; it
MUST NOT fabricate a terminal result.

## 11. Verification result

A verification result binds the plan, optional apply result, pack, exact
target, fresh environment evidence, fresh catalog snapshots, selected closure,
and one object result per classification. Its overall state is `verified` or
`mismatch`.

For a plan with writes, `apply_result_digest` is required and
`response_evidence` must be `complete`; for a no-write plan it is null and
response evidence is `not_required`. `missing` or `invalid` response evidence
forces overall mismatch. Fresh object states must all be `equivalent` for
overall verification success.

`receipt_readback` is fixed to
`captured_responses_only_spine_0.3.0`. It explicitly prevents the artifact from
claiming independent command-receipt readback that Spine 0.3.0 cannot provide.

## 12. CLI result envelope and exit codes

Every command writes exactly one compact JSON envelope followed by one newline
to standard output. The envelope names the operation, status, process exit
code, optional output-artifact reference, and nullable structured error. An
artifact reference contains the path requested by the operator and its
validated content digest; the path does not enter that artifact's identity.
The operating-system process status uses the integer in the table; the JSON
`exit_code` field encodes the same value as a canonical decimal string because
the artifact family contains no JSON numbers.

The stable mapping is:

| Exit | Status | Category |
| ---: | --- | --- |
| 0 | `success` | none |
| 2 | `failed` | `invalid_cli_or_artifact_input` |
| 3 | `failed` | `invalid_pack_contract_or_digest` |
| 4 | `failed` | `incompatible_spine_runtime_or_contracts` |
| 5 | `decision_required` | `decision_required_for_drift` |
| 6 | `blocked` | `blocked_desired_state` |
| 7 | `failed` | `stale_plan_or_target_mismatch` |
| 8 | `failed` | `spine_command_rejection` |
| 9 | `partial` | `partial_apply` |
| 10 | `mismatch` | `verification_mismatch` |
| 11 | `failed` | `transport_or_environment_failure` |

Exit 5 MUST reference the complete reviewable plan. Exit 9 MUST reference the
terminal partial result. A successful draft inspection may exit 0 with a plan
whose `apply_eligible` is false; attempting to apply it fails at exit 3.

For `plan`, the precedence table in `specs/installer.md` Section 14 is
normative: blocked objects take priority, then permitted draft inspection,
then released drift, then released no-drift success. All four outcomes
reference a complete plan. Draft inspection preserves decision action IDs
but does not require an approval or become intrinsically eligible.

Errors contain only category, stable code, bounded human message, and an array
of closed `{name, value}` objects with string members, strictly sorted by unique
`name`. They MUST NOT contain credentials, environment dumps,
or raw command output. One failure chooses one primary category; additional
facts do not change the process exit code.

## 13. Required semantic vectors

Before the corresponding behavior is implemented, tests MUST demonstrate at least:

- full-pack and granular request normalization and inferred closure;
- closed objects, ordering, size limits, and every artifact digest;
- draft apply refusal and incompatible runtime/contract evidence;
- missing, equivalent, drifted, blocked, metadata-only drift, and behavioral
  drift classifications;
- complete per-update authorization and rejection of blanket or stale
  authorization;
- target host, executable path/hash, and ledger-path mismatch refusal;
- stable command-ID and request derivation;
- contiguous-prefix continuation from a partial result;
- accepted-before-response recovery from a prepared checkpoint;
- rejection of an unexplained catalog change;
- verification mismatch and the Spine 0.3 receipt-readback disclosure; and
- exact envelope status/category/exit-code correlation.

The first fixture slice may use one complete vertical flow plus focused
negative mutations, but missing required cases remain contract work rather
than silently becoming implementation assumptions.

## 14. Deferred implementation details

The authorized planning, preflight, and initial-apply slices use the source-tree
`spine_packs` package and standard-library `argparse`, as recorded in
`specs/architecture.md`. This does not authorize continuation, verification,
or recovery implementation. Filesystem
configuration and release packaging remain deferred. It does not add section bundles,
remote transports, signatures, install registries, credentials, Windows path
semantics, or Spine runtime changes.
```

### Spec 4: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: c1dfb2553e18d1da0e2d4509840457ac5f5a2cd7f46d1e8a87629860a1e152d1

```markdown
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

### Slice 3: initial apply and durable checkpointing — implemented; bounded review pending

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
interrupted checkpoint: no continuation or uncertainty recovery is implemented.
This slice still needs bounded review before being treated as reviewed delivery;
no real installation, pack release, or deployment is implied.

### Slice 4: continuation and uncertain-response recovery

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

### Slice 5: non-mutating verification

Implement `verify` independently of apply execution:

- reload and correlate the plan, manifest, target, and optional apply result;
- freshly read selected archetypes, profiles, and bindings;
- verify semantic desired state and selection scope;
- correlate captured command responses and receipt facts without claiming
  later authoritative receipt-row readback; and
- emit the closed verification artifact and specified result status.

Exit gate: verification performs no write or compatible-replay request and
detects target, state, evidence, and correlation mismatches.

### Slice 6: end-to-end qualification and supported packaging

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

The following remain explicit follow-ups rather than hidden v1 prerequisites:

- stable Spine ledger-instance identity;
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
```

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/compatibility.md

Hash: 4729196b9831b544dd32ec05ad735a9b1028b5e1eacdc7961278b13877ce7007

```markdown
# Compatibility

## Compatibility dimensions

Every manifest MUST declare compatibility independently for:

1. exact Spine runtime versions; and
2. exact Spine content-contract identifiers needed to interpret the pack's
   definitions.

Runtime and contract compatibility are separate dimensions. Matching one MUST
NOT be treated as evidence that the other matches.

## Version 1 declaration shape

`spine.pack-manifest.v1` uses closed, non-empty allowlists:

- `spine_runtime_versions` contains stable semantic versions in ascending
  order; and
- `spine_content_contracts` contains contract identifiers in bytewise
  lexicographic order.

Ranges, wildcards, prerelease runtimes, development builds, and implicit
compatibility are not supported by v1. A future installer MUST obtain both
values through Spine's public `system.info` command and MUST require exact
membership before interpreting pack content.

The first `kinflow-starter` draft is based exclusively on the inspected Spine
runtime `0.3.0` public artifacts and requires:

- `spine.item-archetypes.v1`;
- `spine.notification-profile-bindings.v1`; and
- `spine.notification-profiles.v1`.

These declarations do not assert that any staging or production environment is
compatible. No environment was queried.

`kinflow-starter` draft `1.0.0-draft.2` retains exactly the same runtime and
content-contract allowlists as `1.0.0-draft.1`. The lesson slice uses only the
existing v1 content shapes; it does not widen compatibility or assert support
for any item-level recurrence command.

Draft `1.0.0-draft.3` retains those exact allowlists. Its birthday templates
use Spine's existing calendar-day target-offset shape and inherit timezone
facts from the applicable local item target. The pack does not declare a
timezone, timezone-database version, or recurrence capability.

Draft `1.0.0-draft.4` retains those exact allowlists. Its Education and Social
profiles use only the already-declared elapsed and calendar-day target-offset
forms. The exact-target dinner and visitor templates use the supported
`offset_seconds=0` form described below.

Draft `1.0.0-draft.5` retains those exact allowlists. Its Travel profiles use
only the same elapsed and calendar-day target-offset forms. Item relationships,
including a packing task's relationship to a trip, are not manifest content
and make no additional compatibility claim.

Draft `1.0.0-draft.6` retains those exact allowlists. Its Renewals and
administration profiles use only the existing calendar-day target-offset form.
The 365-day and 270-day passport boundaries do not claim unsupported
calendar-year or calendar-month arithmetic.

Draft `1.0.0-draft.7` retains those exact allowlists. Its Health profiles use
only the existing calendar-day target-offset form. The 365-day and 180-day
vaccination boundaries do not claim calendar-year or calendar-month
arithmetic, recurrence, or clinical-guidance semantics.

Draft `1.0.0-draft.8` retains those exact allowlists. Its Home, vehicle, and
logistics profiles use only the existing elapsed and calendar-day target-offset
forms, including the already-supported exact-target elapsed form. The delivery
window definition does not claim range-scheduling semantics.

Draft `1.0.0-draft.9` retains those exact allowlists. Its General commitments
profiles use only the existing elapsed and calendar-day target-offset forms,
including the already-supported exact-target elapsed form. General archetypes
do not introduce runtime fallback or item-dependency semantics.

The v1 pack contract's exact-target elapsed form, `offset_seconds=0`, is within
the signed elapsed-offset semantics accepted by the inspected Spine runtime
`0.3.0` under `spine.notification-profiles.v1`. Supporting that form does not
widen the runtime or content-contract allowlists. The pack contract continues
to exclude positive, post-target elapsed offsets.

## Content compatibility is not execution readiness

`spine_content_contracts` is intentionally limited to the contracts that give
the owner-neutral definitions their meaning. It MUST NOT be interpreted as the
complete contract union required to execute `plan`, `apply`, or `verify`.

Spine's command registry may require additional contracts for a concrete
command, including `spine.canonical-json.v1`, notification-profile readback,
catalog cursor, response, or receipt contracts. The draft installer contract
in `specs/installer.md` names its Spine `0.3.0` command set and derives the
complete per-command requirement union. A future implementation MUST verify
that union independently. The v1 pack manifest makes no execution-readiness
claim.

## Fail-closed behavior

Compatibility evaluation MUST fail before content planning when:

- the runtime version cannot be obtained;
- implemented contract identifiers cannot be obtained;
- the runtime is absent from `spine_runtime_versions`;
- any declared content contract is absent from Spine's advertised contracts;
  or
- the manifest declaration is missing, unsorted, duplicated, or invalid.

Compatibility failure MUST NOT be bypassed implicitly during a future `apply`.
Any override mechanism requires a later contract revision.

## Version changes

A released pack's compatibility declaration is part of its immutable content.
Expanding or narrowing compatibility after release requires a new pack version.
Draft compatibility MAY change only with a recomputed content digest and review
against the newly named public artifacts.

## Deferred compatibility decisions

The following remain intentionally unresolved:

- version-range syntax;
- prerelease and development runtime policy;
- minimum installer-version declarations;
- evidence required to widen compatibility;
- compatibility declarations for dependency packs; and
- evidence and review required to support installer execution against an
  additional Spine runtime.
```

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/pack-format.md

Hash: 979afd8323f646b0d18d874f3ecdee9f68061ee517046c918ee4cbab92ff652d

```markdown
# Pack format requirements

## Status and identity

This document defines the first-pass pack contract,
`spine.pack-manifest.v1`. Its machine-readable authority is
`contracts/schemas/spine-pack-manifest.v1.schema.json`, identified by:

```text
https://spine-packs.local/contracts/schemas/spine-pack-manifest.v1.schema.json
```

Manifests MUST be UTF-8 JSON objects and MUST declare
`manifest_schema=spine.pack-manifest.v1`. YAML, TOML, split manifests, comments,
and alternate encodings are not supported by v1.

Every object is closed. Unknown fields, duplicate JSON object member names,
missing required fields, and invalid field types MUST fail validation. V1 has
no optional fields. `description` is required for archetypes and profiles but
is explicitly nullable; absent and `null` are not equivalent.

Duplicate JSON object member names and duplicate definition keys are distinct
failure classes. A repeated member name in one JSON object is a lexical input
failure rejected before schema validation. Repeated `archetype_key`,
`profile_key`, or `template_key` values occur across separate array entries and
are semantic uniqueness failures rejected after schema validation.

## Pack identity and version

`pack_id` MUST match `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` and contain at most 64
characters. It is owner-neutral and stable across versions.

Version 1 supports two lifecycle forms:

- a draft version matching semantic version core plus
  `-draft.<positive-decimal>`, paired with `status=draft`; or
- a stable semantic version with no prerelease or build suffix, paired with
  `status=released`.

Numeric components MUST NOT contain leading zeroes. `1.0.0-draft.1` is a draft
toward `1.0.0`; it is not the `1.0.0` release.

Draft content MAY change before release, but its content digest MUST be updated.
Once a manifest is published with `status=released`, the entire pack
identity/version/digest tuple and its content are immutable. Any later semantic,
compatibility, or metadata change requires a new stable pack version.

## Top-level shape

A v1 manifest contains exactly:

- `manifest_schema`;
- `pack`, containing `pack_id`, `version`, and `status`;
- `compatibility`;
- `dependencies`;
- `archetypes`;
- `notification_profiles`;
- `binding_intents`; and
- `content_identity`.

The first schema requires at least one archetype, one notification profile, and
one binding intent because it establishes the complete vertical-slice shape.

## Compatibility

`compatibility.spine_runtime_versions` and
`compatibility.spine_content_contracts` are required exact allowlists governed
by `specs/compatibility.md`. They MUST be unique and deterministically ordered.
The content-contract list describes definition semantics only and MUST NOT be
used as proof that every contract needed by a future installer command is
available.

## Dependencies

`dependencies` is required and MUST be an empty array in
`spine.pack-manifest.v1`. A future manifest-contract version must define pack
reference identity, version selection, integrity, cycle handling, and ordering
before dependencies may be added. An installer MUST fail closed rather than
ignore a non-empty dependency array.

## Archetypes

Each archetype contains exactly:

- `archetype_key`, matching Spine's public catalog-key grammar;
- `intended_status`, currently fixed to `active`; and
- `revision`, containing required `display_name`, required nullable
  `description`, and required `compatible_item_types`.

The revision shape is the owner-neutral semantic subset of Spine
`item_archetype.create`. Owner, command, actor, timestamp, generated ID,
revision ID, receipt, and normalized hash fields are forbidden.

Compatible item types are a sorted, unique, non-empty subset of `event` and
`task`. Archetype keys MUST be unique within the pack.

## Notification profiles and templates

Each profile contains exactly:

- `profile_key`, matching Spine's public catalog-key grammar;
- required `display_name` and required nullable `description`;
- `intended_status`, currently fixed to `active`; and
- `revision`, containing required `compatible_item_types` and `templates`.

V1 templates contain exactly `template_key`, `schedule`, and `late_handling`.
The v1 schedule subset permits a once-only elapsed target offset:

```json
{
  "kind": "once",
  "at": {
    "kind": "target_offset",
    "offset_basis": "elapsed",
    "offset_seconds": "-86400"
  }
}
```

`offset_seconds` MUST be a canonical non-positive decimal string: either `0`
or a negative value without leading zeroes. A negative value represents
elapsed seconds before the target anchor; `0` represents exactly the target
instant. Positive, post-target elapsed offsets are not supported by v1.

The subset also permits a once-only calendar-day target offset:

```json
{
  "kind": "once",
  "at": {
    "kind": "target_offset",
    "offset_basis": "calendar_days",
    "offset_days": "-1",
    "local_time": "09:00:00"
  }
}
```

`offset_days` MUST be a canonical decimal string from `-3660` through `0`.
Negative values are local calendar days before the target date; `0` is the
target date. `local_time` MUST be a canonical `HH:MM:SS` wall-clock time.
Calendar-day arithmetic preserves that wall-clock time across UTC-offset
changes; it MUST NOT be treated as elapsed seconds.

Reusable packs MUST omit `timezone` and `timezone_database_version` from a
calendar-day boundary. Those facts are inherited from the applicable local
item target at profile application time. Application to a target that cannot
supply both facts MUST fail closed in Spine. This inheritance does not make the
pack authoritative for the target, timezone, or recurrence.

V1 late handling is:

```json
{
  "kind": "deliver_within",
  "grace_seconds": "21600"
}
```

`grace_seconds` MUST be a positive decimal string. The pack restriction is
stricter than Spine's general non-negative decimal type because a zero-width
`deliver_within` window has no useful meaning in curated pack content.

The manifest schema validates each template's late-handling window in
isolation. It does not infer cross-template spacing because the resolved gap
between calendar-day and elapsed boundaries can depend on the applicable item
target and timezone. A pack that imposes a stronger spacing policy MUST state
that policy in its normative pack specification and pin every approved grace
value in contract tests. `kinflow-starter` uses the 75-percent rule defined in
`specs/kinflow-starter.md`.

Profile keys MUST be unique within the pack. Template keys MUST be unique
within each profile. Compatible item types and templates MUST be sorted.
Recipients, subjects, groups, routes, channels, delivery targets, destinations,
credentials, target anchors, embedded timezones, timezone-database versions,
recurrence scope, generated hashes, and any environment fact are forbidden.

## Binding intents and local references

A binding intent contains exactly:

- `binding_kind=archetype_default`;
- `archetype_key`; and
- `notification_profile_key`.

Both keys are pack-local references. The archetype and profile MUST exist in the
same manifest, and their compatible item-type sets MUST intersect. Binding pairs
MUST be unique, and each `archetype_key` MUST appear in at most one binding
intent. Two profiles therefore cannot both claim to be the default for the same
archetype. V1 does not permit dependency-qualified references.

The intent says that the named profile should become the default for the named
archetype under an owner chosen at installation time. It is not a Spine binding
and contains no owner or Spine-generated ID. A future installer must resolve or
create both definitions through public commands, then submit the resolved IDs
and explicit owner to `notification_profile.binding.set`.

## Deterministic ordering

Array order is contract-bearing and MUST be normalized before digesting:

1. runtime versions by semantic-version numeric order;
2. content contracts by bytewise lexicographic order;
3. compatible item types by bytewise lexicographic order;
4. archetypes by `archetype_key`;
5. profiles by `profile_key`;
6. templates by `template_key`; and
7. binding intents by `archetype_key`, which is unique within this collection.

`dependencies` is empty. Input that is valid in content but not in canonical
order MUST fail validation rather than be silently reordered.

## Content identity

`content_identity` contains exactly:

- `algorithm=sha256`;
- `canonical_json_version=spine.canonical-json.v1`; and
- a lowercase 64-character hexadecimal `digest`.

The digest preimage is the following object:

```text
{
  "canonical_json_version": "spine.canonical-json.v1",
  "derivation_version": "spine-pack-content-sha256.v1",
  "manifest": <the complete manifest with content_identity omitted>
}
```

The preimage is encoded exactly under Spine canonical JSON v1: valid UTF-8; no
insignificant whitespace; object keys sorted lexicographically by Unicode
codepoint; duplicate keys forbidden; array order preserved; strings preserved
without implicit normalization; invalid surrogate code points rejected; only
quote, backslash, and U+0000 through U+001F escaped; lowercase `\\u00xx` control
escapes; slash never escaped; and JSON numbers forbidden. The digest is SHA-256
over those bytes, encoded as lowercase hexadecimal.

The manifest uses decimal strings rather than JSON numbers, so every current
semantic value is legal in the canonical preimage. A digest mismatch fails
closed. Draft edits recompute the digest; released content must never change.

## Validation order and fail-closed behavior

Validation MUST proceed in this order:

1. reject malformed JSON and duplicate object members;
2. validate the closed JSON Schema;
3. validate unique definition keys, binding pairs, one default binding per
   archetype key, and calendar-day offset bounds;
4. resolve binding references and compatible item-type intersections;
5. validate deterministic ordering; and
6. recompute and compare the content digest.

Any failure rejects the complete pack. Implementations MUST NOT drop unknown
fields, skip invalid definitions, guess references, coerce values, reorder input
silently, or install a valid subset.

The dependency-free repository test implements the closed JSON Schema subset
used by v1 plus the semantic, ordering, and digest stages above. Before any pack
version is released, development or CI MUST also meta-validate the schema and
run the complete fixture matrix with an independent standards-conforming JSON
Schema Draft 2020-12 implementation. That independent check is not available in
the current local environment and is a release blocker, not evidence against
the passing local contract suite.

## Deferred decisions

The following remain outside `spine.pack-manifest.v1`:

- dependency references and resolution;
- broader Spine notification schedule and late-handling variants;
- semantic-equivalence comparison against installed definitions;
- update-authorization and receipt-correlation forms;
- installer version compatibility;
- signing, publisher identity, registries, and release transport; and
- the machine-readable `plan`, `apply`, and `verify` contracts and installer
  implementation; their draft behavioral requirements are specified in
  `specs/installer.md`.
```

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/__init__.py

Hash: d5f7b028c63f3d248548b2e106958b6eb620ee8b4b692c3f7469d12ed505b7b8

```markdown
"""Spine pack planning, non-mutating preflight, and initial approved apply."""
```

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/__main__.py

Hash: 4b19b6ec6987ece1d17e3d8156d6c2b8b18b1e53ef7ac755d6b6237bd6e5ee5f

```markdown
"""Source-tree CLI: PYTHONPATH=src python3 -m spine_packs plan ..."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

from . import artifacts as a
from .apply import apply_initial, checkpoint_writer
from .planning import INVALID, PACK_INVALID, ENVIRONMENT, PlanError, plan_installation, plan_outcome, require
from .spine_command import SpineCommand
from .manifest import validate_pack
from .execution import validate_inputs


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


def envelope(category, code=None, artifact=None, operation="plan"):
    exit_code, status = a.EXIT_MAP[category]
    return {"artifact_schema": "spine.pack-installer-result.v1", "operation": operation,
            "status": "success" if category == "success" else status, "exit_code": exit_code,
            "artifact": artifact, "error": None if category == "success" else {
                "category": category, "code": code or category,
                "message": "Operation stopped: " + (code or category) + ".", "facts": [],
            }}


def main(argv=None, *, transport_factory=SpineCommand):
    try:
        parser = Parser(prog="spine-packs", description="Local Spine pack plan and approved apply.")
        parser.add_argument("operation", choices=["plan", "apply"])
        parser.add_argument("--manifest")
        parser.add_argument("--request")
        parser.add_argument("--plan")
        parser.add_argument("--approval")
        parser.add_argument("--checkpoint")
        parser.add_argument("--output")
        parser.add_argument("--all", action="store_true", dest="all_flag")
        parser.add_argument("--archetype", action="append")
        args = parser.parse_args(argv)
        require(args.manifest is not None and args.output is not None, "invalid_cli_arguments", INVALID)
        manifest = load_input(args.manifest, PACK_INVALID, 16 * 1024 * 1024)
        require(not validate_pack(manifest, a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")),
                "invalid_manifest", PACK_INVALID)
        if args.operation == "plan":
            require(args.request is not None and args.plan is None and args.approval is None
                    and args.checkpoint is None, "invalid_cli_arguments", INVALID)
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
        else:
            require(args.plan is not None and args.approval is not None and args.checkpoint is not None
                    and args.request is None and not args.all_flag and args.archetype is None,
                    "invalid_cli_arguments", INVALID)
            plan = load_input(args.plan, INVALID, a.SIZE_LIMITS["spine.pack-install-plan.v1"])
            approval = load_input(args.approval, INVALID, a.SIZE_LIMITS["spine.pack-install-approval.v1"])
            validate_inputs(plan, approval)
            target = plan["request"]["target"]
            protected = [args.manifest, args.plan, args.approval,
                         target["spine_command"]["path"], target["ledger"]["path"]]
            checkpoint = output_path(args.checkpoint, [*protected, args.output])
            output = output_path(args.output, [args.manifest, args.plan, args.approval, args.checkpoint,
                                             target["spine_command"]["path"], target["ledger"]["path"]])
            writer = checkpoint_writer(checkpoint)
            applied = apply_initial(manifest, plan, approval, transport_factory(target), writer)
            publish(output, applied)
            category = ("success" if applied["state"] == "applied" else "partial_apply"
                        if applied["state"] == "partial" else applied["failure"]["error"]["category"])
            result = envelope(category, artifact={"path": args.output,
                "digest": applied["content_identity"]["digest"]}, operation="apply")
    except PlanError as exc:
        result = envelope(exc.category, exc.code, operation=(args.operation if 'args' in locals() else "plan"))
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        # Do not echo arbitrary input, process output, paths, or environment data.
        result = envelope(INVALID, "invalid_contract_value", operation=(args.operation if 'args' in locals() else "plan"))
    except OSError:
        result = envelope(ENVIRONMENT, "local_environment_failure", operation=(args.operation if 'args' in locals() else "plan"))
    print(a.canonical_text(result))
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/apply.py

Hash: 295f81022b9f504ebf497de636b42809fef657533fdfdbb64316ed54a2adcb21

```markdown
"""Initial approved apply execution with durable checkpointing; no continuation."""
from copy import deepcopy
import os
from pathlib import Path
import tempfile

from . import artifacts as a
from .execution import (command_id, execution_artifact, materialize, response_evidence,
                        validate_artifact, validate_inputs)
from .planning import ENVIRONMENT, INVALID, PlanError, observe_catalog, require
from .preflight import preflight_apply


def checkpoint_writer(path):
    """Create once without clobbering, then replace only this writer's checkpoint."""
    supplied = Path(path)
    require(not supplied.exists() and not supplied.is_symlink(), "checkpoint_already_exists", INVALID)
    target = supplied.resolve()
    require(target.parent.is_dir(), "checkpoint_parent_missing", INVALID)
    previous = None

    def write(value):
        nonlocal previous
        validate_artifact(value)
        require(value["artifact_schema"] == "spine.pack-apply-checkpoint.v1", "invalid_checkpoint", INVALID)
        encoded = (a.canonical_text(value) + "\n").encode("utf-8")
        temporary = None
        try:
            if previous is not None:
                require(not target.is_symlink() and target.is_file(), "checkpoint_changed")
                with target.open("rb") as handle:
                    observed = handle.read(len(previous) + 1)
                require(observed == previous, "checkpoint_changed")
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".spine-checkpoint-", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            if previous is None:
                os.link(temporary, target)
                temporary.unlink()
                temporary = None
            else:
                os.replace(temporary, target)
                temporary = None
            directory = os.open(target.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
            previous = encoded
        except FileExistsError as exc:
            raise PlanError(INVALID, "checkpoint_already_exists") from exc
        except OSError as exc:
            raise PlanError(ENVIRONMENT, "checkpoint_publication_failed") from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return write


def failure(exc, action_id=None):
    # Only controlled diagnostics, never raw transport output or exception text.
    return {"action_id": action_id, "error": {
        "category": exc.category, "code": exc.code,
        "message": "Apply stopped: " + exc.code + ".", "facts": getattr(exc, "facts", []),
    }}


def _binding_precondition(plan, action, request, transport, page_size):
    # V1 has one binding action per archetype, so earlier actions cannot change
    # this binding. Creates resolve its root IDs but still require absent binding.
    classification = next(c for c in plan["classifications"] if c["object_key"] == action["object_key"])
    expected = classification["identity"]["observed_binding"]
    entries, _ = observe_catalog(transport, "bindings", plan["request"]["owner"], page_size=page_size)
    matches = [e for e in entries if e["item_archetype_id"] == request["item_archetype_id"]]
    fields = ("notification_profile_binding_id", "item_archetype_id", "notification_profile_id")
    actual = {k: matches[0][k] for k in fields} if matches else None
    require(actual == expected, "binding_precondition_changed", "stale_plan_or_target_mismatch")


def apply_initial(manifest, plan, approval, transport, checkpoint_writer, *, page_size=100):
    """Execute only a new, fully approved plan; never read/resume saved checkpoints."""
    # Detach caller-owned objects before callbacks or transport can mutate them.
    manifest, plan, approval = deepcopy((manifest, plan, approval))
    validate_inputs(plan, approval)
    accepted = []
    try:
        preflight_apply(manifest, plan, approval, transport, page_size=page_size)
    except PlanError as exc:
        return execution_artifact(plan, approval, [], state="not_applied", failure=failure(exc))
    actions = plan["actions"]
    if not actions:
        checkpoint_writer(execution_artifact(plan, approval, []))
        return execution_artifact(plan, approval, [], state="applied")

    for index, action in enumerate(actions):
        try:
            request = materialize(plan, approval, index, accepted)
            if action["command"] == "notification_profile.binding.set":
                _binding_precondition(plan, action, request, transport, page_size)
        except PlanError as exc:
            return execution_artifact(plan, approval, accepted,
                state="partial" if accepted else "not_applied",
                failure=failure(exc, action["action_id"]))
        prefix, contract = a.COMMAND_SHAPES[action["command"]]
        unresolved = {"action_id": action["action_id"], "command_id": request["command_id"],
            "submission_state": "prepared_or_submitted",
            "request": a.canonical_value(contract, request, prefix + "Request")}
        # Publication failures propagate: no terminal success/rollback claim is made.
        checkpoint_writer(execution_artifact(plan, approval, accepted, unresolved=unresolved))
        try:
            response = transport.write(action["command"], deepcopy(request))
            evidence = response_evidence(action, request, response)
            next_accepted = [*accepted, evidence]
            advanced = execution_artifact(plan, approval, next_accepted)
        except (PlanError, ValueError, TypeError, KeyError, RecursionError, OSError) as exc:
            if not isinstance(exc, PlanError):
                exc = PlanError(ENVIRONMENT, "invalid_or_uncertain_write_response")
            # Once transport is invoked, failure is potentially post-commit, even
            # for the very first action. Never report that nothing was applied.
            return execution_artifact(plan, approval, accepted, state="partial",
                                      failure=failure(exc, action["action_id"]))
        checkpoint_writer(advanced)
        accepted = next_accepted
    return execution_artifact(plan, approval, accepted, state="applied")
```

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/execution.py

Hash: 9d05e288af37b4522fde88ec5bf91feaebdf89d67f2fac38974f76aac1404f6f

```markdown
"""Pure initial-execution materialization and evidence validation; no transport."""
from copy import deepcopy
import json

from . import artifacts as a
from .planning import ENVIRONMENT, INVALID, require


def command_id(plan_digest, execution_id, action_id):
    return "spack_" + a.digest({"action_id": action_id,
        "derivation_version": "spine.pack-command-id.v1",
        "execution_id": execution_id, "plan_digest": plan_digest})


def validate_inputs(plan, approval):
    require(isinstance(plan, dict) and plan.get("artifact_schema") == "spine.pack-install-plan.v1"
            and not a.validate_schema(plan), "invalid_plan", INVALID)
    require(not a.plan_errors(plan) and not a.artifact_size_errors(plan), "invalid_plan", INVALID)
    require(isinstance(approval, dict)
            and approval.get("artifact_schema") == "spine.pack-install-approval.v1"
            and not a.validate_schema(approval), "invalid_or_incomplete_approval", INVALID)
    require(not a.approval_errors(approval, plan) and not a.artifact_size_errors(approval),
            "invalid_or_incomplete_approval", INVALID)


def validate_artifact(value):
    require(not a.validate_schema(value) and not a.content_digest_errors(value)
            and not a.artifact_size_errors(value), "invalid_execution_artifact", INVALID)


def validate_known_requests(plan, approval):
    """Preflight every request not dependent on a still-unknown create response."""
    validate_inputs(plan, approval)
    for index, action in enumerate(plan["actions"]):
        template = json.loads(action["request_template"]["canonical_json"])
        if not a._reference_slots(template):
            _request(plan, approval, index, {})


def _request(plan, approval, index, decoded):
    action = plan["actions"][index]
    prefix, contract = a.COMMAND_SHAPES[action["command"]]
    require(not a.canonical_value_errors(action["request_template"], prefix + "Template"),
            "invalid_command_template", INVALID)
    value = json.loads(action["request_template"]["canonical_json"])
    require(not a.result_reference_errors(value, prefix + "Template", plan, index),
            "invalid_result_reference", INVALID)
    for path, reference in a._reference_slots(value):
        producer_id, field = a.RESULT_REFERENCE.fullmatch(reference).groups()
        require(producer_id in decoded, "result_reference_evidence_missing", INVALID)
        value[path[0]] = decoded[producer_id][field]
    execution = approval["execution"]
    value.update(command_id=command_id(plan["content_identity"]["digest"],
                                     execution["execution_id"], action["action_id"]),
                 actor_subject_id=execution["actor_subject_id"],
                 action_timestamp_utc=execution["action_timestamp_utc"])
    wrapped = a.canonical_value(contract, value, prefix + "Request")
    require(not a.canonical_value_errors(wrapped, prefix + "Request"),
            "invalid_materialized_request", INVALID)
    return value


def response_evidence(action, request, response):
    prefix, contract = a.COMMAND_SHAPES[action["command"]]
    # Raw write responses must themselves be canonical-compatible (no numbers).
    try:
        value = a.canonical_value(contract, response, prefix + "Response")
        valid = not a.canonical_value_errors(value, prefix + "Response")
    except (ValueError, TypeError, KeyError, RecursionError):
        valid = False
    require(valid, "invalid_spine_response", ENVIRONMENT)
    receipt = response["receipt"]
    require(receipt["command_id"] == request["command_id"], "response_command_id_mismatch")
    require(receipt["effect"] == response["effect"], "response_effect_mismatch")
    require(receipt["created_at_utc"] == request["action_timestamp_utc"], "receipt_timestamp_mismatch")
    # Pinned 0.3.0 handlers hash the complete semantic request, including execution fields.
    require(receipt["semantic_facts_hash"] == a.digest(request), "receipt_request_hash_mismatch")
    for field in ("archetype_key", "profile_key", "item_archetype_id", "notification_profile_id"):
        if field in request and field in response:
            require(response[field] == request[field], "response_identity_mismatch")
    if action["command"].endswith(".create"):
        require(response["revision_number"] == "1", "response_revision_mismatch")
    if action["command"].endswith(".revise"):
        revision_id = "item_archetype_revision_id" if prefix == "archetypeRevise" else "notification_profile_revision_id"
        require(response[revision_id] != request["expected_current_revision_id"], "response_revision_mismatch")
    if prefix == "profileMetadataUpdate":
        require({k: response[k] for k in ("display_name", "description")} == request["metadata"],
                "response_metadata_mismatch")
        effect = ("notification_profile_metadata_update_noop" if request["metadata"] == request["expected_metadata"]
                  else "notification_profile_metadata_updated")
        require(response["effect"] == effect, "response_effect_mismatch")
    if prefix == "bindingSet":
        types = response["compatible_item_types"]
        require(types == sorted(set(types)), "response_item_types_not_canonical")
    return {"action_id": action["action_id"], "command": action["command"],
            "command_id": request["command_id"], "outcome": "accepted",
            "response_contract": response["response_contract"], "effect": response["effect"],
            "generated_ids": [{"name": k, "value": response[k]} for k in sorted(response) if k.endswith("_id")],
            "command_receipt_id": receipt["command_receipt_id"],
            "semantic_facts_hash": receipt["semantic_facts_hash"], "response": value}


def validate_prefix(plan, approval, accepted):
    require(isinstance(accepted, list) and len(accepted) <= len(plan["actions"]),
            "invalid_accepted_prefix", INVALID)
    decoded, receipt_ids = {}, set()
    for index, evidence in enumerate(accepted):
        action = plan["actions"][index]
        require(isinstance(evidence, dict) and evidence.get("action_id") == action["action_id"],
                "invalid_accepted_prefix", INVALID)
        shape = a.COMMAND_SHAPES[action["command"]][0] + "Response"
        require(not a.canonical_value_errors(evidence["response"], shape), "invalid_response_evidence", INVALID)
        body = json.loads(evidence["response"]["canonical_json"])
        expected = response_evidence(action, _request(plan, approval, index, decoded), body)
        require(evidence == expected, "invalid_response_evidence", INVALID)
        require(expected["command_receipt_id"] not in receipt_ids, "duplicate_receipt_evidence", INVALID)
        receipt_ids.add(expected["command_receipt_id"])
        decoded[action["action_id"]] = body
    return decoded


def materialize(plan, approval, index, accepted):
    validate_inputs(plan, approval)
    require(type(index) is int and 0 <= index < len(plan["actions"]) and len(accepted) == index,
            "invalid_accepted_prefix", INVALID)
    return _request(plan, approval, index, validate_prefix(plan, approval, accepted))


def execution_artifact(plan, approval, accepted, *, unresolved=None, state=None, failure=None):
    """Construct and validate a checkpoint or terminal result from one exact prefix."""
    validate_inputs(plan, approval)
    validate_prefix(plan, approval, accepted)
    remaining = [x["action_id"] for x in plan["actions"][len(accepted):]]
    value = {"artifact_schema": "spine.pack-apply-checkpoint.v1" if state is None else "spine.pack-apply-result.v1",
             "plan_digest": plan["content_identity"]["digest"],
             "approval_digest": approval["content_identity"]["digest"],
             "execution": deepcopy(approval["execution"]), "accepted_responses": deepcopy(accepted)}
    if state is None:
        if unresolved is not None:
            require(bool(remaining), "unexpected_submission", INVALID)
            request = materialize(plan, approval, len(accepted), accepted)
            prefix, contract = a.COMMAND_SHAPES[plan["actions"][len(accepted)]["command"]]
            require(unresolved == {"action_id": remaining[0], "command_id": request["command_id"],
                "submission_state": "prepared_or_submitted",
                "request": a.canonical_value(contract, request, prefix + "Request")},
                "unresolved_request_mismatch", INVALID)
        value.update(unresolved_submission=deepcopy(unresolved), next_action_id=remaining[0] if remaining else None)
    else:
        if state == "applied":
            require(not remaining and failure is None, "applied_not_complete", INVALID)
            unattempted = []
        elif state == "partial":
            require(bool(remaining) and failure is not None and failure["action_id"] == remaining[0],
                    "partial_failure_mismatch", INVALID)
            unattempted = remaining[1:]
        else:
            require(state == "not_applied" and not accepted and failure is not None,
                    "invalid_not_applied", INVALID)
            unattempted = remaining
        value.update(state=state, failure=deepcopy(failure), unattempted_action_ids=unattempted)
    value = a.seal(value)
    validate_artifact(value)
    return value
```

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/preflight.py

Hash: b56ce5439301f48268316c172c2403336e1508f772982110e09f73a017402d7a

```markdown
"""Non-mutating apply preflight over an approved installation plan."""

from __future__ import annotations

from copy import deepcopy

from . import artifacts as a
from .manifest import validate_pack
from .planning import INVALID, PACK_INVALID, PlanError, plan_installation, require
from .execution import validate_known_requests

STALE = "stale_plan_or_target_mismatch"


def preflight_apply(manifest, plan, approval, transport, *, page_size=100):
    """Return execution facts after complete, fresh, read-only validation."""
    manifest_schema = a._schema_document(
        a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json"
    )
    require(not validate_pack(manifest, manifest_schema), "invalid_manifest", PACK_INVALID)
    require(
        not a.plan_errors(plan) and not a.artifact_size_errors(plan),
        "invalid_plan",
        INVALID,
    )
    require(
        not a.approval_errors(approval, plan)
        and not a.artifact_size_errors(approval),
        "invalid_or_incomplete_approval",
        INVALID,
    )
    require(plan["pack"]["status"] == "released", "draft_plan_not_applicable", PACK_INVALID)
    require(plan["apply_eligible"], "plan_not_apply_eligible", PACK_INVALID)
    require(not plan["blocked_object_keys"], "blocked_plan_not_applicable", PACK_INVALID)
    validate_known_requests(plan, approval)

    pack_identity = {
        "manifest_schema": manifest["manifest_schema"],
        **manifest["pack"],
        "manifest_digest": manifest["content_identity"]["digest"],
    }
    require(pack_identity == plan["pack"], "manifest_identity_mismatch", STALE)

    request = a.seal({
        "artifact_schema": "spine.pack-install-request.v1",
        "request": deepcopy(plan["request"]),
    })
    require(
        request["content_identity"]["digest"] == plan["request_digest"],
        "request_identity_mismatch",
        STALE,
    )
    observed_plan = plan_installation(manifest, request, transport, page_size=page_size)
    require(
        observed_plan["content_identity"]["digest"] == plan["content_identity"]["digest"],
        "stale_plan",
        STALE,
    )
    return {
        "plan_digest": plan["content_identity"]["digest"],
        "approval_digest": approval["content_identity"]["digest"],
        "execution": deepcopy(approval["execution"]),
        "action_ids": [action["action_id"] for action in plan["actions"]],
    }
```

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/spine_command.py

Hash: 3789dead7dff335d667974c61ef9bc82ee41d13179167344523beba023cd38f3

```markdown
"""Local process adapter for the pinned Spine 0.3.0 command surface."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import selectors
import socket
import subprocess
import time
import re

from . import artifacts as a
from .planning import CATALOGS, ENVIRONMENT, PlanError, require, validate_readback


READ_COMMANDS = frozenset({"system.info", "item_archetype.list", "item_archetype.show",
                           "notification_profile.list", "notification_profile.show",
                           "notification_profile.binding.list"})
WRITE_COMMANDS = frozenset(a.COMMAND_SHAPES)
RESPONSE_LIMIT = 16 * 1024 * 1024


class SpineCommand:
    """Only this adapter may spawn Spine. It never opens the ledger itself."""
    def __init__(self, target, *, timeout=30, host_resolver=socket.getfqdn):
        self.target = target
        self.timeout = timeout
        self.host_resolver = host_resolver

    def check_target(self):
        try:
            host = self.host_resolver().lower().removesuffix(".")
            require(host.isascii() and "." in host and ".." not in host,
                    "target_host_unresolved")
            executable = Path(self.target["spine_command"]["path"]).resolve(strict=True)
            ledger = Path(self.target["ledger"]["path"]).resolve(strict=True)
            require(executable.is_file() and ledger.is_file() and os.access(executable, os.X_OK),
                    "target_unavailable")
            with executable.open("rb") as handle:
                sha = hashlib.file_digest(handle, "sha256").hexdigest()
            observed = {"host_name": host, "spine_command": {"path": str(executable), "sha256": sha},
                        "ledger": {"kind": "path", "path": str(ledger)}}
            require(observed == self.target, "target_binding_mismatch", "stale_plan_or_target_mismatch")
        except OSError as exc:
            raise PlanError(ENVIRONMENT, "target_unavailable") from exc

    def read(self, command, request):
        # A write name is rejected before target inspection or process creation.
        require(command in READ_COMMANDS, "read_only_command_required")
        if command == "system.info":
            require(request == {}, "invalid_read_request")
        else:
            catalog = next(k for k, v in CATALOGS.items() if command.startswith(v[0] + ".")
                           and (k == "bindings") == command.startswith("notification_profile.binding."))
            validate_readback(request, catalog + ("ListRequest" if command.endswith(".list") else "ShowRequest"))
        response, returncode = self._invoke(command, request)
        if response.get("ok") is False:
            validate_readback(response, "commandFailure")
            require(response["command"] == command, "response_command_mismatch")
            raise PlanError("spine_command_rejection", "spine_read_rejected")
        # Read failure never becomes a missing/retained object or an applicable plan.
        require(returncode == 0 and response.get("ok") is True, "spine_read_failed")
        require(response.get("command") == command, "response_command_mismatch")
        return response

    def write(self, command, request):
        require(command in WRITE_COMMANDS, "write_command_not_allowed")
        prefix, contract = a.COMMAND_SHAPES[command]
        value = a.canonical_value(contract, request, prefix + "Request")
        require(not a.canonical_value_errors(value, prefix + "Request"), "invalid_write_request")
        response, returncode = self._invoke(command, request)
        if response.get("ok") is False:
            validate_readback(response, "commandFailure")
            require(response.get("command") == command, "response_command_mismatch")
            # Keep only the public machine error code, never its arbitrary message.
            code = response["error"]["code"]
            require(re.fullmatch(r"[a-z][a-z0-9_.:-]{0,159}", code) is not None, "invalid_spine_error_code")
            error = PlanError("spine_command_rejection", "spine_write_rejected")
            error.facts = [{"name": "spine_error_code", "value": code}]
            raise error
        require(returncode == 0 and response.get("ok") is True, "spine_write_failed", ENVIRONMENT)
        require(response.get("command") == command, "response_command_mismatch", ENVIRONMENT)
        return response

    def _invoke(self, command, request):
        self.check_target()
        argv = [self.target["spine_command"]["path"], "--db", self.target["ledger"]["path"],
                command, "--input", "-"]
        data = (a.canonical_text(request) + "\n").encode("utf-8")
        process = None
        try:
            process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL, shell=False)
            output = bytearray()
            deadline = time.monotonic() + self.timeout
            os.set_blocking(process.stdin.fileno(), False)
            written = 0
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                selector.register(process.stdin, selectors.EVENT_WRITE)
                while selector.get_map():
                    remaining = deadline - time.monotonic()
                    require(remaining > 0, "spine_timeout")
                    for key, _ in selector.select(min(remaining, 0.2)):
                        if key.fileobj is process.stdin:
                            written += os.write(key.fd, data[written:written + 4096])
                            if written == len(data):
                                selector.unregister(process.stdin)
                                process.stdin.close()
                            continue
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                        else:
                            output.extend(chunk)
                            require(len(output) <= RESPONSE_LIMIT, "spine_response_too_large")
            returncode = process.wait(timeout=max(0.01, deadline - time.monotonic()))
            response = a.parse_json(bytes(output), public_response=True)
            require(isinstance(response, dict), "invalid_public_response")
            return response, returncode
        except (OSError, ValueError, RecursionError, subprocess.TimeoutExpired) as exc:
            raise PlanError(ENVIRONMENT, "spine_transport_failed") from exc
        finally:
            if process is not None:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                if process.stdout is not None:
                    process.stdout.close()
                if process.stdin is not None and not process.stdin.closed:
                    process.stdin.close()
```

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/artifacts.py

Hash: 412e8d74072527cd319cd80082e3f6cecb79613ca13b44fe22ff52d1399fccf1

```markdown
"""Installer artifact validation, derived from the existing contract-test helpers.

No command execution lives here. Schemas are shipped in the source checkout.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts/schemas"
EMBEDDED_SCHEMA = SCHEMA_ROOT / "spine-pack-embedded-values.v1.schema.json"
COMMAND_SHAPES = {
    "item_archetype.create": ("archetypeCreate", "spine.item-archetypes.v1"),
    "item_archetype.revise": ("archetypeRevise", "spine.item-archetypes.v1"),
    "notification_profile.create": ("profileCreate", "spine.notification-profiles.v1"),
    "notification_profile.revise": ("profileRevise", "spine.notification-profiles.v1"),
    "notification_profile.metadata.update": (
        "profileMetadataUpdate", "spine.notification-profile-metadata-update.v1"
    ),
    "notification_profile.binding.set": ("bindingSet", "spine.notification-profile-bindings.v1"),
}
SEMANTIC_CONTRACTS = {
    "archetypeSemantics": "spine.item-archetypes.v1",
    "profileSemantics": "spine.notification-profiles.v1",
    "bindingSemantics": "spine.notification-profile-bindings.v1",
}

ENTRYPOINTS = {
    "spine.pack-install-request.v1": "spine-pack-install-request.v1.schema.json",
    "spine.pack-install-plan.v1": "spine-pack-install-plan.v1.schema.json",
    "spine.pack-install-approval.v1": "spine-pack-install-approval.v1.schema.json",
    "spine.pack-apply-checkpoint.v1": "spine-pack-apply-checkpoint.v1.schema.json",
    "spine.pack-apply-result.v1": "spine-pack-apply-result.v1.schema.json",
    "spine.pack-verification-result.v1": "spine-pack-verification-result.v1.schema.json",
    "spine.pack-installer-result.v1": "spine-pack-installer-result.v1.schema.json",
}

DERIVATIONS = {
    "spine.pack-install-request.v1": "spine.pack-install-request-digest.v1",
    "spine.pack-install-plan.v1": "spine.pack-install-plan-digest.v1",
    "spine.pack-install-approval.v1": "spine.pack-install-approval-digest.v1",
    "spine.pack-apply-checkpoint.v1": "spine.pack-apply-checkpoint-digest.v1",
    "spine.pack-apply-result.v1": "spine.pack-apply-result-digest.v1",
    "spine.pack-verification-result.v1": "spine.pack-verification-result-digest.v1",
}

SIZE_LIMITS = {
    "spine.pack-install-request.v1": 65_536,
    "spine.pack-install-plan.v1": 8_388_608,
    "spine.pack-install-approval.v1": 262_144,
    "spine.pack-apply-checkpoint.v1": 16_777_216,
    "spine.pack-apply-result.v1": 16_777_216,
    "spine.pack-verification-result.v1": 16_777_216,
    "spine.pack-installer-result.v1": 1_048_576,
}

REQUIRED_EXECUTION_CONTRACTS = [
    "spine.canonical-json.v1",
    "spine.item-archetypes.v1",
    "spine.notification-profile-bindings.v1",
    "spine.notification-profile-catalog-cursor.v1",
    "spine.notification-profile-metadata-update.v1",
    "spine.notification-profile-readback.v1",
    "spine.notification-profiles.v1",
    "spine.system-info.v2",
    "spine.tickerd-compatibility.v1",
]

EXIT_MAP = {
    "success": ("0", None),
    "invalid_cli_or_artifact_input": ("2", "failed"),
    "invalid_pack_contract_or_digest": ("3", "failed"),
    "incompatible_spine_runtime_or_contracts": ("4", "failed"),
    "decision_required_for_drift": ("5", "decision_required"),
    "blocked_desired_state": ("6", "blocked"),
    "stale_plan_or_target_mismatch": ("7", "failed"),
    "spine_command_rejection": ("8", "failed"),
    "partial_apply": ("9", "partial"),
    "verification_mismatch": ("10", "mismatch"),
    "transport_or_environment_failure": ("11", "failed"),
}


class DuplicateObjectMember(ValueError):
    pass


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateObjectMember(key)
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_closed_object)


def canonical_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        raise ValueError("numbers are not allowed")
    if isinstance(value, str):
        pieces = ['"']
        for char in value:
            codepoint = ord(char)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("surrogates are not allowed")
            if char == '"':
                pieces.append('\\"')
            elif char == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(char)
        return "".join(pieces) + '"'
    if isinstance(value, list):
        return "[" + ",".join(canonical_text(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_text(key)}:{canonical_text(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"unsupported canonical value: {type(value).__name__}")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()


def canonical_value(contract: str, value: Any, shape: str | None = None) -> dict[str, Any]:
    text = canonical_text(value)
    if shape is None:
        shape = next(name for name, family in SEMANTIC_CONTRACTS.items() if family == contract)
    return {
        "contract": contract,
        "shape": shape,
        "canonical_json": text,
        "digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def seal(artifact: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(artifact)
    derivation = DERIVATIONS[value["artifact_schema"]]
    value["content_identity"] = {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": derivation,
    }
    value["content_identity"]["digest"] = digest(value)
    return value


def content_digest_errors(artifact: dict[str, Any]) -> list[str]:
    identity = artifact.get("content_identity")
    if not isinstance(identity, dict):
        return ["content_identity_missing"]
    candidate = deepcopy(artifact)
    claimed = candidate["content_identity"].pop("digest", None)
    if claimed != digest(candidate):
        return ["content_digest_mismatch"]
    expected = DERIVATIONS.get(artifact.get("artifact_schema"))
    if identity.get("derivation_version") != expected:
        return ["content_derivation_mismatch"]
    return []


@lru_cache(maxsize=32)
def _schema_document(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def _resolve_ref(
    reference: str, current_path: Path, current_schema: dict[str, Any]
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    file_part, marker, fragment = reference.partition("#")
    if file_part:
        target_path = (current_path.parent / file_part).resolve()
        root = _schema_document(target_path)
    else:
        target_path = current_path
        root = current_schema
    current: Any = root
    if marker and fragment:
        if not fragment.startswith("/"):
            raise ValueError(reference)
        for token in fragment[1:].split("/"):
            current = current[token.replace("~1", "/").replace("~0", "~")]
    if not isinstance(current, dict):
        raise TypeError(reference)
    return current, target_path, root


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "boolean": isinstance(value, bool),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
        "integer": type(value) is int,
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        target, target_path, target_root = _resolve_ref(
            schema["$ref"], schema_path, root_schema
        )
        return schema_errors(value, target, target_path, target_root, path)
    if "oneOf" in schema:
        candidates = [
            schema_errors(value, branch, schema_path, root_schema, path)
            for branch in schema["oneOf"]
        ]
        return [] if sum(not errors for errors in candidates) == 1 else [f"{path}: oneOf"]

    errors: list[str] = []
    if "const" in schema and json.dumps(value, sort_keys=True) != json.dumps(schema["const"], sort_keys=True):
        errors.append(f"{path}: const")
    if "enum" in schema and json.dumps(value, sort_keys=True) not in [json.dumps(x, sort_keys=True) for x in schema["enum"]]:
        errors.append(f"{path}: enum")
    expected_type = schema.get("type")
    if expected_type and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]
    for branch in schema.get("allOf", []):
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if "anyOf" in schema and all(
        schema_errors(value, branch, schema_path, root_schema, path)
        for branch in schema["anyOf"]
    ):
        errors.append(f"{path}: anyOf")
    if "not" in schema and not schema_errors(
        value, schema["not"], schema_path, root_schema, path
    ):
        errors.append(f"{path}: not")
    if isinstance(value, list) and "contains" in schema:
        count = sum(not schema_errors(item, schema["contains"], schema_path, root_schema)
                    for item in value)
        if not schema.get("minContains", 1) <= count <= schema.get("maxContains", len(value)):
            errors.append(f"{path}: contains")
    if type(value) is int and value < schema.get("minimum", value):
        errors.append(f"{path}: minimum")
    if "if" in schema:
        match = not schema_errors(value, schema["if"], schema_path, root_schema, path)
        branch = schema.get("then" if match else "else", {})
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: minLength")
        if len(value) > schema.get("maxLength", len(value)):
            errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: minItems")
        if len(value) > schema.get("maxItems", len(value)):
            errors.append(f"{path}: maxItems")
        if schema.get("uniqueItems"):
            encodings = [canonical_text(item) for item in value]
            if len(encodings) != len(set(encodings)):
                errors.append(f"{path}: uniqueItems")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(
                    schema_errors(
                        item,
                        schema["items"],
                        schema_path,
                        root_schema,
                        f"{path}[{index}]",
                    )
                )
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, member in value.items():
            if key in properties:
                errors.extend(
                    schema_errors(
                        member,
                        properties[key],
                        schema_path,
                        root_schema,
                        f"{path}.{key}",
                    )
                )
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: unknown")
    return errors


def validate_schema(artifact: dict[str, Any]) -> list[str]:
    if not isinstance(artifact, dict) or artifact.get("artifact_schema") not in ENTRYPOINTS:
        return ["unknown_artifact_schema"]
    name = ENTRYPOINTS[artifact["artifact_schema"]]
    path = SCHEMA_ROOT / name
    schema = _schema_document(path)
    return schema_errors(artifact, schema, path, schema)


def parse_json(data: bytes, *, public_response: bool = False) -> Any:
    """Strict UTF-8 parser; only pinned public readbacks may contain integers."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("byte_order_mark")

    def invalid_constant(value):
        raise ValueError("nonfinite_number")

    value = json.loads(data.decode("utf-8"), object_pairs_hook=_closed_object,
                       parse_constant=invalid_constant)

    def inspect(item):
        if public_response and type(item) is int:
            return
        if isinstance(item, dict):
            for key, child in item.items():
                canonical_text(key)
                inspect(child)
        elif isinstance(item, list):
            for child in item:
                inspect(child)
        else:
            canonical_text(item)

    inspect(value)
    return value


RESULT_REFERENCE = re.compile(r"\$\{spine-pack\.result:(action-[0-9]{6}):([a-z_]+)\}")
REFERENCE_PRODUCERS = {
    "item_archetype_id": ("item_archetype.create", "archetype", "archetype_key"),
    "notification_profile_id": ("notification_profile.create", "profile", "profile_key"),
}


def _reference_slots(value: Any, path: tuple = ()) -> list[tuple]:
    """Find reserved interpolation syntax, including nested values/member names."""
    if isinstance(value, str):
        return [(path, value)] if "${" in value else []
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if "${" in key:
                found.append(((*path, key, "<member-name>"), key))
            found.extend(_reference_slots(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_reference_slots(child, (*path, index)))
    return found


def result_reference_errors(
    value: Any, shape: str, plan: dict[str, Any] | None = None,
    index: int | None = None,
) -> list[str]:
    errors = []
    for path, text in _reference_slots(value):
        match = RESULT_REFERENCE.fullmatch(text)
        if not match:
            errors.append("result_reference_syntax_invalid")
            continue
        if shape != "bindingSetTemplate" or len(path) != 1 or path[0] not in REFERENCE_PRODUCERS:
            errors.append("result_reference_context_forbidden")
            continue
        producer_id, returned_field = match.groups()
        field = path[0]
        if returned_field != field:
            errors.append("result_reference_field_invalid")
            continue
        if plan is None:
            continue  # The containing plan supplies the mandatory correlation stage.
        consumer = plan["actions"][index]
        producers = [(i, a) for i, a in enumerate(plan["actions"]) if a["action_id"] == producer_id]
        if len(producers) != 1:
            errors.append("result_reference_producer_missing")
            continue
        producer_index, producer = producers[0]
        if producer_index >= index:
            errors.append("result_reference_not_earlier")
            continue
        command, kind, key_field = REFERENCE_PRODUCERS[field]
        desired_binding = json.loads(consumer["desired"]["canonical_json"])
        key = (consumer["object_key"].split(":", 1)[1] if kind == "archetype"
               else desired_binding["notification_profile_key"])
        object_key = kind + ":" + key
        roots = [c for c in plan["classifications"] if c["object_key"] == object_key]
        creates = [a for a in plan["actions"] if a["object_key"] == object_key and a["command"] == command]
        if len(roots) != 1 or roots[0]["classification"] != "missing" or roots[0]["identity"] is not None:
            errors.append("result_reference_root_not_missing")
            continue
        if producer["command"] != command or producer["object_key"] != object_key or len(creates) != 1:
            errors.append("result_reference_producer_mismatch")
            continue
        body = json.loads(producer["request_template"]["canonical_json"])
        root_value = json.loads(roots[0]["desired"]["canonical_json"])
        actual_value = (body["revision"] if kind == "archetype" else {
            "metadata": {"display_name": body["display_name"], "description": body["description"]},
            "revision": body["revision"],
        })
        if (body.get(key_field) != key or body.get("owner") != plan["request"]["owner"]
                or producer["desired"] != roots[0]["desired"] or actual_value != root_value):
            errors.append("result_reference_producer_mismatch")
    return errors


def canonical_value_errors(
    value: dict[str, Any], expected_shape: str | None = None
) -> list[str]:
    try:
        parsed = json.loads(value["canonical_json"], object_pairs_hook=_closed_object)
        canonical = canonical_text(parsed)
    except (ValueError, TypeError, json.JSONDecodeError, DuplicateObjectMember):
        return ["canonical_value_invalid"]
    if canonical != value["canonical_json"]:
        return ["canonical_value_not_canonical"]
    actual = hashlib.sha256(value["canonical_json"].encode("utf-8")).hexdigest()
    if actual != value["digest"]:
        return ["canonical_value_digest_mismatch"]
    shape = value.get("shape")
    allowed = dict(SEMANTIC_CONTRACTS)
    for prefix, contract in COMMAND_SHAPES.values():
        for suffix in ("Template", "Request", "Response"):
            allowed[prefix + suffix] = contract
    if shape not in allowed or value.get("contract") != allowed.get(shape):
        return ["embedded_contract_or_shape_mismatch"]
    if expected_shape is not None and shape != expected_shape:
        return ["embedded_context_shape_mismatch"]
    root = _schema_document(EMBEDDED_SCHEMA)
    errors = schema_errors(parsed, root["$defs"][shape], EMBEDDED_SCHEMA, root)
    if errors:
        return ["embedded_contract_invalid", *errors]
    if shape.endswith(("Template", "Request", "Response")):
        return result_reference_errors(parsed, shape)
    return []


def selection_assertion_errors(
    request: dict[str, Any], *, all_flag: bool = False,
    archetype_flags: list[str] | None = None,
) -> list[str]:
    if all_flag and archetype_flags is not None:
        return ["selection_flags_conflict"]
    if archetype_flags is not None and (not archetype_flags or any(not k for k in archetype_flags)):
        return ["selection_flags_empty"]
    if not all_flag and archetype_flags is None:
        return []
    assertion = ({"mode": "all"} if all_flag else
                 {"mode": "archetypes", "archetype_keys": sorted(set(archetype_flags))})
    return [] if assertion == request["request"]["selection"] else ["selection_assertion_mismatch"]


def artifact_size_errors(artifact: dict[str, Any]) -> list[str]:
    size = len(canonical_text(artifact).encode("utf-8"))
    return [] if size <= SIZE_LIMITS[artifact["artifact_schema"]] else ["artifact_too_large"]


def _sorted_unique(values: list[str]) -> bool:
    return values == sorted(set(values))


def _path_is_normalized(path: str) -> bool:
    return (
        path.startswith("/")
        and path != "/"
        and not path.endswith("/")
        and "//" not in path
        and all(part not in {".", ".."} for part in path.split("/"))
    )


def request_errors(request_artifact: dict[str, Any]) -> list[str]:
    errors = validate_schema(request_artifact) + content_digest_errors(request_artifact)
    request = request_artifact.get("request", {})
    selection = request.get("selection", {})
    keys = selection.get("archetype_keys", [])
    if selection.get("mode") == "archetypes" and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    target = request.get("target", {})
    host_name = target.get("host_name", "")
    if host_name != host_name.lower() or host_name.endswith(".") or ".." in host_name:
        errors.append("target_host_not_normalized")
    for value in (
        target.get("spine_command", {}).get("path", ""),
        target.get("ledger", {}).get("path", ""),
    ):
        if not _path_is_normalized(value):
            errors.append("target_path_not_normalized")
    return errors


def approval_errors(approval: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    """Validate an approval and bind it to one complete immutable plan."""
    errors = validate_schema(approval) + content_digest_errors(approval)
    if errors:
        return errors
    if approval["plan_digest"] != plan.get("content_identity", {}).get("digest"):
        errors.append("approval_plan_digest_mismatch")
    if approval["authorized_update_action_ids"] != plan.get("decision_action_ids"):
        errors.append("update_authorization_incomplete")
    return errors


def binding_identity_errors(plan: dict[str, Any]) -> list[str]:
    """Correlate owner-scoped key resolutions, binding readback, and requests."""
    errors = []
    roots = {}
    seen_ids = set()
    for entry in plan["classifications"]:
        if entry["object_kind"] == "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if identity is not None and set(identity) != {"catalog_id"}:
            errors.append("catalog_identity_shape_mismatch")
            continue
        if (state == "missing" and identity is not None) or (
            state in ("equivalent", "drifted") and identity is None
        ):
            errors.append("catalog_identity_state_mismatch")
        catalog_id = identity["catalog_id"] if identity is not None else None
        if catalog_id is not None:
            marker = (entry["object_kind"], catalog_id)
            if marker in seen_ids or catalog_id.startswith("${"):
                errors.append("catalog_identity_invalid")
            seen_ids.add(marker)
        roots[entry["object_key"]] = (state, catalog_id)

    for entry in plan["classifications"]:
        if entry["object_kind"] != "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if state == "blocked":
            if identity is not None:
                errors.append("blocked_binding_has_identity")
            continue
        if identity is None or set(identity) != {
            "item_archetype_id", "notification_profile_id", "observed_binding"
        }:
            errors.append("binding_identity_missing_or_invalid")
            continue
        desired = json.loads(entry["desired"]["canonical_json"])
        root_keys = {
            "item_archetype_id": "archetype:" + entry["object_key"].split(":", 1)[1],
            "notification_profile_id": "profile:" + desired["notification_profile_key"],
        }
        for field, key in root_keys.items():
            root = roots.get(key)
            if root is None or root[0] == "blocked" or identity[field] != root[1]:
                errors.append("binding_resolution_mismatch")
        observed = identity["observed_binding"]
        if (state == "missing") != (observed is None):
            errors.append("binding_observation_state_mismatch")
        if observed is not None:
            if any(value.startswith("${") for value in observed.values()):
                errors.append("binding_identity_invalid")
            if identity["item_archetype_id"] is None or (
                observed["item_archetype_id"] != identity["item_archetype_id"]
            ):
                errors.append("binding_archetype_identity_mismatch")
            same_profile = (
                identity["notification_profile_id"] is not None
                and observed["notification_profile_id"] == identity["notification_profile_id"]
            )
            if (state == "equivalent") != same_profile:
                errors.append("binding_profile_identity_mismatch")
            observed_value = entry["observed"]
            if observed_value is not None:
                observed_key = json.loads(observed_value["canonical_json"])["notification_profile_key"]
                observed_root = roots.get("profile:" + observed_key)
                if observed_root is not None and observed_root[1] != observed["notification_profile_id"]:
                    errors.append("binding_observed_key_identity_mismatch")

        for action in plan["actions"]:
            if action["object_key"] != entry["object_key"]:
                continue
            if action["command"] != "notification_profile.binding.set":
                errors.append("binding_action_command_mismatch")
                continue
            request = json.loads(action["request_template"]["canonical_json"])
            if request.get("owner") != plan["request"]["owner"]:
                errors.append("binding_action_owner_mismatch")
            for field, key in root_keys.items():
                expected = identity[field]
                if expected is None:
                    command = "item_archetype.create" if field == "item_archetype_id" else "notification_profile.create"
                    creates = [a for a in plan["actions"] if a["object_key"] == key and a["command"] == command]
                    if len(creates) != 1 or int(creates[0]["ordinal"]) >= int(action["ordinal"]):
                        errors.append("binding_create_reference_missing")
                        continue
                    expected = "${spine-pack.result:" + creates[0]["action_id"] + ":" + field + "}"
                if request.get(field) != expected:
                    errors.append("binding_action_identity_mismatch")
    return errors


def plan_errors(plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(plan) + content_digest_errors(plan)
    if validate_schema(plan):
        return errors
    request = plan["request"]
    embedded_request = seal(
        {
            "artifact_schema": "spine.pack-install-request.v1",
            "request": request,
        }
    )
    if plan["request_digest"] != embedded_request["content_identity"]["digest"]:
        errors.append("request_digest_mismatch")
    errors.extend(request_errors(embedded_request))
    keys = request["selection"].get("archetype_keys", [])
    if keys and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    for field in ("archetype_keys", "profile_keys", "binding_archetype_keys"):
        if not _sorted_unique(plan["closure"][field]):
            errors.append(f"closure_{field}_not_sorted")
    if plan["required_execution_contracts"] != REQUIRED_EXECUTION_CONTRACTS:
        errors.append("execution_contract_union_mismatch")
    if not _sorted_unique(plan["environment"]["advertised_contracts"]):
        errors.append("advertised_contracts_not_sorted")
    if not set(REQUIRED_EXECUTION_CONTRACTS).issubset(
        plan["environment"]["advertised_contracts"]
    ):
        errors.append("required_execution_contract_missing")
    if [entry["catalog"] for entry in plan["catalog_snapshots"]] != [
        "archetypes", "profiles", "bindings"
    ]:
        errors.append("catalog_snapshot_order")
    expected_object_keys = (
        [f"archetype:{key}" for key in plan["closure"]["archetype_keys"]]
        + [f"profile:{key}" for key in plan["closure"]["profile_keys"]]
        + [f"binding:{key}" for key in plan["closure"]["binding_archetype_keys"]]
    )
    if [entry["object_key"] for entry in plan["classifications"]] != expected_object_keys:
        errors.append("classification_scope_mismatch")
    expected_ids = [f"action-{index:06d}" for index in range(len(plan["actions"]))]
    if [entry["action_id"] for entry in plan["actions"]] != expected_ids:
        errors.append("action_order_or_identity")
    if [entry["ordinal"] for entry in plan["actions"]] != [
        str(index) for index in range(len(plan["actions"]))
    ]:
        errors.append("action_ordinal")
    action_rank = {
        "item_archetype.create": 0,
        "item_archetype.revise": 0,
        "notification_profile.create": 1,
        "notification_profile.metadata.update": 2,
        "notification_profile.revise": 3,
        "notification_profile.binding.set": 4,
    }
    action_order = [
        (action_rank[entry["command"]], entry["object_key"])
        for entry in plan["actions"]
    ]
    if action_order != sorted(action_order):
        errors.append("action_order")
    updates = [
        entry["action_id"] for entry in plan["actions"] if entry["change_kind"] == "update"
    ]
    if plan["decision_action_ids"] != updates:
        errors.append("decision_action_ids_mismatch")
    blocked = [
        entry["object_key"]
        for entry in plan["classifications"]
        if entry["classification"] == "blocked"
    ]
    if plan["blocked_object_keys"] != sorted(blocked):
        errors.append("blocked_object_keys_mismatch")
    if plan["pack"]["status"] == "draft" and plan["apply_eligible"]:
        errors.append("draft_plan_apply_eligible")
    if plan["pack"]["status"] == "draft" and request["draft_posture"] != "inspect_only":
        errors.append("draft_posture_mismatch")
    if plan["pack"]["status"] == "released" and "-draft." in plan["pack"]["version"]:
        errors.append("pack_version_status_mismatch")
    if plan["pack"]["status"] == "draft" and not re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)-draft\.[1-9][0-9]*",
        plan["pack"]["version"],
    ):
        errors.append("pack_version_status_mismatch")
    if blocked and plan["apply_eligible"]:
        errors.append("blocked_plan_apply_eligible")
    for classification in plan["classifications"]:
        observed = classification["observed"]
        reason = classification["blocked_reason"]
        if classification["classification"] == "missing" and observed is not None:
            errors.append("missing_has_observed")
        if classification["classification"] == "blocked" and reason is None:
            errors.append("blocked_without_reason")
        if classification["classification"] != "blocked" and reason is not None:
            errors.append("unexpected_blocked_reason")
        if classification["classification"] in ("equivalent", "drifted") and observed is None:
            errors.append("classification_observation_missing")
        shape = classification["object_kind"] + "Semantics"
        errors.extend(canonical_value_errors(classification["desired"], shape))
        if observed is not None:
            errors.extend(canonical_value_errors(observed, shape))
            equal = classification["desired"]["canonical_json"] == observed["canonical_json"]
            if classification["classification"] == "equivalent" and not equal:
                errors.append("equivalence_preimage_mismatch")
            if classification["classification"] == "drifted" and equal:
                errors.append("drift_preimages_equal")
    class_rank = {"archetype": 0, "profile": 1, "binding": 2}
    classification_order = [
        (class_rank[entry["object_kind"]], entry["object_key"])
        for entry in plan["classifications"]
    ]
    if classification_order != sorted(classification_order):
        errors.append("classification_order")
    for action in plan["actions"]:
        shape = action["object_key"].split(":")[0] + "Semantics"
        errors.extend(canonical_value_errors(action["desired"], shape))
        prefix = COMMAND_SHAPES[action["command"]][0]
        errors.extend(canonical_value_errors(action["request_template"], prefix + "Template"))
        if action["expected"] is not None:
            errors.extend(canonical_value_errors(action["expected"], shape))
        if action["change_kind"] == "create" and action["expected"] is not None:
            errors.append("create_has_expected")
        if action["change_kind"] == "update" and action["expected"] is None:
            errors.append("update_without_expected")
    # Embedded data must be valid before the identity correlator decodes it.
    if not errors:
        errors.extend(binding_identity_errors(plan))
        for index, action in enumerate(plan["actions"]):
            errors.extend(result_reference_errors(
                json.loads(action["request_template"]["canonical_json"]),
                COMMAND_SHAPES[action["command"]][0] + "Template", plan, index,
            ))
    return errors
```

### Spec 14: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/planning.py

Hash: 39e7e53782e185f5ac338f2a6006947bb54d2b9974566cdd3cd816a03fd28864

```markdown
"""Read-only planning over a supplied public-command transport.

The transport owns process/filesystem interaction. This module never submits
the write templates it constructs, and never imports Spine internals.
"""
from __future__ import annotations

from copy import deepcopy

from . import artifacts as a
from .manifest import validate_pack


class PlanError(Exception):
    def __init__(self, category: str, code: str):
        super().__init__(code)
        self.category = category
        self.code = code


INVALID = "invalid_cli_or_artifact_input"
PACK_INVALID = "invalid_pack_contract_or_digest"
ENVIRONMENT = "transport_or_environment_failure"
INCOMPATIBLE = "incompatible_spine_runtime_or_contracts"


def require(condition, code, category=ENVIRONMENT):
    if not condition:
        raise PlanError(category, code)


CATALOGS = {
    "archetypes": ("item_archetype", "archetype_key", "item_archetype_id", "archetype"),
    "profiles": ("notification_profile", "profile_key", "notification_profile_id", "profile"),
    "bindings": ("notification_profile.binding", "item_archetype_id", "notification_profile_binding_id", "binding"),
}
FAMILIES = {
    "archetypes": "spine.item-archetypes.v1",
    "profiles": "spine.notification-profiles.v1",
    "bindings": "spine.notification-profile-bindings.v1",
}


def validate_readback(value, shape):
    path = a.SCHEMA_ROOT / "spine-readback-0.3.0.schema.json"
    schema = a._schema_document(path)
    require(not a.schema_errors(value, schema["$defs"][shape], path, schema),
            "invalid_public_response")


def owner_matches(entry, owner):
    return (entry["owner_kind"] == owner["owner_kind"]
            and entry["owner_subject_id"] == owner.get("owner_subject_id")
            and entry["owner_group_id"] == owner.get("owner_group_id"))


def semantics(entry, kind):
    revision = entry["revision"]
    if kind == "archetype":
        return {k: deepcopy(revision[k]) for k in
                ("display_name", "description", "compatible_item_types")}
    return {
        "metadata": {k: entry[k] for k in ("display_name", "description")},
        "revision": {
            "compatible_item_types": deepcopy(revision["compatible_item_types"]),
            "templates": [{k: deepcopy(t[k]) for k in ("template_key", "schedule", "late_handling")}
                          for t in revision["templates"]],
        },
    }


def validate_entry(entry, owner, kind):
    require(owner_matches(entry, owner), "catalog_owner_mismatch")
    retired = entry["status"] == "retired"
    require(all((entry[k] is not None) == retired for k in
                ("retired_by_subject_id", "retired_by_command_id", "retired_at_utc")),
            "catalog_retirement_mismatch")
    if kind == "binding":
        return
    prefix = "item_archetype" if kind == "archetype" else "notification_profile"
    revision = entry["revision"]
    require(revision[prefix + "_id"] == entry[prefix + "_id"]
            and revision[prefix + "_revision_id"] == entry["current_revision_id"],
            "revision_identity_mismatch")
    require(revision["compatible_item_types"] == sorted(set(revision["compatible_item_types"])),
            "readback_item_types_not_canonical")
    if kind == "profile":
        templates = revision["templates"]
        require([t["template_key"] for t in templates] == sorted({t["template_key"] for t in templates}),
                "readback_templates_not_canonical")
        require([t["template_index"] for t in templates] == list(range(len(templates))),
                "readback_template_indices_invalid")
        require(len({t["notification_profile_template_id"] for t in templates}) == len(templates)
                and all(t["notification_profile_revision_id"] == entry["current_revision_id"]
                        for t in templates), "template_identity_mismatch")


def observe_catalog(transport, catalog, owner, *, page_size=100):
    command, key_field, id_field, kind = CATALOGS[catalog]
    query = {"contract_version": FAMILIES[catalog], "owner": owner, "limit": str(page_size)}
    # Roots include active and retired definitions. Only active bindings affect defaults.
    if kind == "binding":
        query["status"] = "active"
    entries, ids, keys, cursors = [], set(), set(), set()
    snapshot, previous = None, None
    while True:
        page = transport.read(command + ".list", query)
        validate_readback(page, catalog + "Page")
        require(page["count"] == str(len(page["entries"])) and len(page["entries"]) <= page_size,
                "invalid_page_count")
        require(snapshot is None or snapshot == page["catalog_snapshot_hash"], "catalog_changed")
        snapshot = page["catalog_snapshot_hash"]
        for entry in page["entries"]:
            validate_entry(entry, owner, kind)
            ordering = (entry[key_field], entry[id_field])
            require(previous is None or ordering > previous, "catalog_order_invalid")
            require(entry[id_field] not in ids and entry[key_field] not in keys, "catalog_duplicate")
            if kind == "binding":
                require(entry["status"] == "active", "inactive_binding_readback")
            previous = ordering
            ids.add(entry[id_field])
            keys.add(entry[key_field])
            if kind != "binding":
                shown = transport.read(command + ".show", {
                    "contract_version": FAMILIES[catalog], id_field: entry[id_field],
                })
                validate_readback(shown, kind + "Show")
                require(shown[command] == entry, "catalog_show_changed")
            entries.append(entry)
        cursor = page["next_cursor"]
        require(page["has_more"] == (cursor is not None), "cursor_presence_invalid")
        if not page["has_more"]:
            break
        require(bool(page["entries"]) and cursor not in cursors, "cursor_cycle_or_empty_page")
        cursors.add(cursor)
        query = {**query, "cursor": cursor}
    return entries, snapshot


def selected_definitions(manifest, request):
    archetypes = {x["archetype_key"]: x for x in manifest["archetypes"]}
    profiles = {x["profile_key"]: x for x in manifest["notification_profiles"]}
    bindings = {x["archetype_key"]: x for x in manifest["binding_intents"]}
    selection = request["selection"]
    if selection["mode"] == "archetypes":
        keys = selection["archetype_keys"]
        require(set(keys) <= archetypes.keys(), "unknown_archetype_selection", INVALID)
        archetypes = {k: archetypes[k] for k in keys}
        bindings = {k: b for k, b in bindings.items() if k in archetypes}
        profile_keys = {b["notification_profile_key"] for b in bindings.values()}
        profiles = {k: p for k, p in profiles.items() if k in profile_keys}
    return archetypes, profiles, bindings


def build_plan(manifest, request_artifact, environment, catalogs, snapshots):
    """Compile validated, owner-scoped public observations to a sealed plan."""
    request = request_artifact["request"]
    archetypes, profiles, bindings = selected_definitions(manifest, request)
    classifications, pending = [], []
    roots = {}

    def value(kind, semantic):
        return a.canonical_value(a.SEMANTIC_CONTRACTS[kind + "Semantics"], semantic)

    def classify(kind, key, desired, observed, state, identity, reason=None):
        c = {"object_kind": kind, "object_key": kind + ":" + key,
             "classification": state, "desired": value(kind, desired),
             "observed": None if observed is None else value(kind, observed),
             "identity": identity, "blocked_reason": reason}
        classifications.append(c)
        return c

    def action(c, command, body, rank):
        pending.append((rank, c["object_key"], command, c, body))

    for kind, desired_by_key, catalog, prefix in (
        ("archetype", archetypes, "archetypes", "item_archetype"),
        ("profile", profiles, "profiles", "notification_profile"),
    ):
        by_key = {r["archetype_key" if kind == "archetype" else "profile_key"]: r
                  for r in catalogs[catalog]}
        for key in sorted(desired_by_key):
            definition = desired_by_key[key]
            desired = (deepcopy(definition["revision"]) if kind == "archetype" else {
                "metadata": {k: definition[k] for k in ("display_name", "description")},
                "revision": deepcopy(definition["revision"]),
            })
            existing = by_key.get(key)
            observed = None if existing is None else semantics(existing, kind)
            state = ("missing" if existing is None else "blocked" if existing["status"] == "retired"
                     else "equivalent" if desired == observed else "drifted")
            c = classify(kind, key, desired, observed, state,
                         None if existing is None else {"catalog_id": existing[prefix + "_id"]},
                         "retired_definition" if state == "blocked" else None)
            roots[(kind, key)] = c
            contract = FAMILIES[catalog]
            if state == "missing":
                body = {"contract_version": contract, "owner": deepcopy(request["owner"]),
                        "archetype_key" if kind == "archetype" else "profile_key": key,
                        "revision": deepcopy(definition["revision"])}
                if kind == "profile":
                    body.update(desired["metadata"])
                action(c, prefix + ".create", body, 0 if kind == "archetype" else 1)
            elif state == "drifted":
                if kind == "profile" and desired["metadata"] != observed["metadata"]:
                    action(c, "notification_profile.metadata.update", {
                        "contract_version": "spine.notification-profile-metadata-update.v1",
                        "notification_profile_id": existing["notification_profile_id"],
                        "expected_metadata": deepcopy(observed["metadata"]),
                        "metadata": deepcopy(desired["metadata"]),
                    }, 2)
                if kind == "archetype" or desired["revision"] != observed["revision"]:
                    action(c, prefix + ".revise", {
                        "contract_version": contract, prefix + "_id": existing[prefix + "_id"],
                        "expected_current_revision_id": existing["current_revision_id"],
                        "revision": deepcopy(definition["revision"]),
                    }, 0 if kind == "archetype" else 3)

    profiles_by_id = {p["notification_profile_id"]: p for p in catalogs["profiles"]}
    bindings_by_archetype = {b["item_archetype_id"]: b for b in catalogs["bindings"]}
    for key in sorted(bindings):
        profile_key = bindings[key]["notification_profile_key"]
        root_a, root_p = roots[("archetype", key)], roots[("profile", profile_key)]
        desired = {"binding_kind": "archetype_default", "notification_profile_key": profile_key}
        archetype_id = root_a["identity"]["catalog_id"] if root_a["identity"] else None
        profile_id = root_p["identity"]["catalog_id"] if root_p["identity"] else None
        binding = bindings_by_archetype.get(archetype_id)
        observed_profile = profiles_by_id.get(binding["notification_profile_id"]) if binding else None
        if ("blocked" in (root_a["classification"], root_p["classification"])
                or (binding is not None and observed_profile is None)):
            classify("binding", key, desired, None, "blocked", None, "unresolved_binding_dependency")
            continue
        observed = None if binding is None else {
            "binding_kind": "archetype_default", "notification_profile_key": observed_profile["profile_key"],
        }
        state = ("missing" if binding is None else "equivalent"
                 if binding["notification_profile_id"] == profile_id else "drifted")
        identity = {"item_archetype_id": archetype_id, "notification_profile_id": profile_id,
                    "observed_binding": None if binding is None else
                    {k: binding[k] for k in ("notification_profile_binding_id", "item_archetype_id", "notification_profile_id")}}
        c = classify("binding", key, desired, observed, state, identity)
        if state != "equivalent":
            action(c, "notification_profile.binding.set", {
                "contract_version": FAMILIES["bindings"], "owner": deepcopy(request["owner"]),
                "item_archetype_id": archetype_id, "notification_profile_id": profile_id,
            }, 4)

    actions, producers = [], {}
    for index, (_, key, command, c, body) in enumerate(sorted(pending, key=lambda p: (p[0], p[1]))):
        action_id = f"action-{index:06d}"
        if command.endswith(".create"):
            producers[key] = action_id
        if command == "notification_profile.binding.set":
            binding_key = key.split(":", 1)[1]
            for field, producer_key in (
                ("item_archetype_id", "archetype:" + binding_key),
                ("notification_profile_id", "profile:" + bindings[binding_key]["notification_profile_key"]),
            ):
                if body[field] is None:
                    body[field] = "${spine-pack.result:" + producers[producer_key] + ":" + field + "}"
        prefix, contract = a.COMMAND_SHAPES[command]
        actions.append({"ordinal": str(index), "action_id": action_id, "command": command,
                        "object_key": key, "change_kind": "create" if c["classification"] == "missing" else "update",
                        "desired": deepcopy(c["desired"]), "expected": deepcopy(c["observed"]),
                        "request_template": a.canonical_value(contract, body, prefix + "Template")})
    blocked = sorted(c["object_key"] for c in classifications if c["classification"] == "blocked")
    plan = a.seal({
        "artifact_schema": "spine.pack-install-plan.v1",
        "request_digest": request_artifact["content_identity"]["digest"],
        "request": deepcopy(request),
        "pack": {"manifest_schema": manifest["manifest_schema"], **manifest["pack"],
                 "manifest_digest": manifest["content_identity"]["digest"]},
        "closure": {"archetype_keys": sorted(archetypes), "profile_keys": sorted(profiles),
                    "binding_archetype_keys": sorted(bindings)},
        "environment": deepcopy(environment), "required_execution_contracts": a.REQUIRED_EXECUTION_CONTRACTS[:],
        "catalog_snapshots": [{"catalog": k, "digest": snapshots[k]} for k in CATALOGS],
        "classifications": classifications, "actions": actions,
        "decision_action_ids": [x["action_id"] for x in actions if x["change_kind"] == "update"],
        "blocked_object_keys": blocked,
        "apply_eligible": manifest["pack"]["status"] == "released" and not blocked,
    })
    require(not a.plan_errors(plan) and not a.artifact_size_errors(plan), "invalid_generated_plan", INVALID)
    return plan


def plan_outcome(plan):
    if plan["blocked_object_keys"]:
        return "blocked_desired_state"
    if plan["pack"]["status"] == "draft":
        return "success"
    if plan["decision_action_ids"]:
        return "decision_required_for_drift"
    return "success"


def plan_installation(manifest, request, transport, *, page_size=100):
    """Validate all inputs before any Spine observation; produce no writes."""
    manifest_schema = a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")
    require(not validate_pack(manifest, manifest_schema), "invalid_manifest", PACK_INVALID)
    require(not a.validate_schema(request), "invalid_request_shape", INVALID)
    require(not a.request_errors(request) and not a.artifact_size_errors(request), "invalid_request", INVALID)
    require(manifest["pack"]["status"] != "draft" or request["request"]["draft_posture"] == "inspect_only",
            "draft_inspection_not_allowed", PACK_INVALID)
    selected_definitions(manifest, request["request"])
    require(type(page_size) is int and 1 <= page_size <= 500, "invalid_page_size", INVALID)
    transport.check_target()
    info = transport.read("system.info", {})
    require(isinstance(info, dict) and isinstance(info.get("runtime_version"), str)
            and bool(info["runtime_version"]), "invalid_public_response")
    # Reject a different runtime before interpreting its version-specific payload.
    require(info["runtime_version"] == "0.3.0"
            and info["runtime_version"] in manifest["compatibility"]["spine_runtime_versions"],
            "incompatible_runtime_or_contracts", INCOMPATIBLE)
    validate_readback(info, "systemInfo")
    advertised = info["implemented_contract_versions"]
    require(advertised == sorted(set(advertised)), "contracts_not_canonical")
    require(set(a.REQUIRED_EXECUTION_CONTRACTS + manifest["compatibility"]["spine_content_contracts"]) <= set(advertised)
            and info["implemented_ledger_schema_version"] == info["ledger_schema_version"] == "12",
            "incompatible_runtime_or_contracts", INCOMPATIBLE)
    environment = {"runtime_version": info["runtime_version"],
                   "ledger_schema_implemented": info["implemented_ledger_schema_version"],
                   "ledger_schema_current": info["ledger_schema_version"], "advertised_contracts": advertised}
    owner = request["request"]["owner"]
    catalogs, snapshots = {}, {}
    for catalog in CATALOGS:
        catalogs[catalog], snapshots[catalog] = observe_catalog(transport, catalog, owner, page_size=page_size)
    # Detect changes across catalogs and show calls, including single-page scans.
    for catalog, (command, _, _, kind) in CATALOGS.items():
        query = {"contract_version": FAMILIES[catalog], "owner": owner, "limit": "1"}
        if kind == "binding":
            query["status"] = "active"
        page = transport.read(command + ".list", query)
        validate_readback(page, catalog + "Page")
        require(page["catalog_snapshot_hash"] == snapshots[catalog], "catalog_changed")
        require(page["entries"] == catalogs[catalog][:1]
                and page["count"] == str(len(page["entries"]))
                and page["has_more"] == (len(catalogs[catalog]) > 1)
                and page["has_more"] == (page["next_cursor"] is not None),
                "catalog_recheck_changed")
    transport.check_target()
    return build_plan(manifest, request, environment, catalogs, snapshots)
```

### Spec 15: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/manifest.py

Hash: 52ce4448cef7356688888f1079f457903f2a49caf1c637f052816ebbf7c4e71f

```markdown
"""Manifest validation derived from the existing v1 contract checks."""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any

def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[token]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return current


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate the deliberately small Draft 2020-12 subset used by the schema."""

    if "$ref" in schema:
        return schema_errors(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path)

    if "oneOf" in schema:
        branch_errors = [
            schema_errors(value, branch, root_schema, path)
            for branch in schema["oneOf"]
        ]
        matches = sum(not errors for errors in branch_errors)
        if matches != 1:
            return [f"{path}: must match exactly one allowed shape"]
        return []

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in the allowed set")

    expected_type = schema.get("type")
    if expected_type is not None and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: string is too long")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern mismatch")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}.{required}: required field is missing")
        for key, member in value.items():
            member_path = f"{path}.{key}"
            if key in properties:
                errors.extend(schema_errors(member, properties[key], root_schema, member_path))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{member_path}: unknown field")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array has too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: array has too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, item_schema, root_schema, f"{path}[{index}]"))

    return errors


def _duplicate_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def check(values: list[str], label: str, path: str) -> None:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                errors.append(f"{path}: duplicate {label} {value!r}")
            seen.add(value)

    check(
        [entry["archetype_key"] for entry in manifest["archetypes"]],
        "archetype_key",
        "$.archetypes",
    )
    check(
        [entry["profile_key"] for entry in manifest["notification_profiles"]],
        "profile_key",
        "$.notification_profiles",
    )
    for index, profile in enumerate(manifest["notification_profiles"]):
        check(
            [entry["template_key"] for entry in profile["revision"]["templates"]],
            "template_key",
            f"$.notification_profiles[{index}].revision.templates",
        )
    check(
        [entry["archetype_key"] for entry in manifest["binding_intents"]],
        "archetype_default for archetype_key",
        "$.binding_intents",
    )
    return errors


def _reference_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    archetypes = {entry["archetype_key"]: entry for entry in manifest["archetypes"]}
    profiles = {
        entry["profile_key"]: entry for entry in manifest["notification_profiles"]
    }
    for index, binding in enumerate(manifest["binding_intents"]):
        archetype_key = binding["archetype_key"]
        profile_key = binding["notification_profile_key"]
        archetype = archetypes.get(archetype_key)
        profile = profiles.get(profile_key)
        if archetype is None:
            errors.append(
                f"$.binding_intents[{index}]: unresolved archetype_key {archetype_key!r}"
            )
        if profile is None:
            errors.append(
                "$.binding_intents[{}]: unresolved notification_profile_key {!r}".format(
                    index, profile_key
                )
            )
        if archetype is not None and profile is not None:
            archetype_types = set(archetype["revision"]["compatible_item_types"])
            profile_types = set(profile["revision"]["compatible_item_types"])
            if not archetype_types.intersection(profile_types):
                errors.append(
                    f"$.binding_intents[{index}]: binding has no compatible item type"
                )
    return errors


def _schedule_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for profile_index, profile in enumerate(manifest["notification_profiles"]):
        for template_index, template in enumerate(profile["revision"]["templates"]):
            at = template["schedule"]["at"]
            if at["offset_basis"] == "calendar_days" and int(at["offset_days"]) < -3660:
                errors.append(
                    f"$.notification_profiles[{profile_index}].revision.templates[{template_index}]"
                    ".schedule.at.offset_days: outside supported range -3660..0"
                )
    return errors


def _ordering_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def ordered(values: list[Any], expected: list[Any], path: str) -> None:
        if values != expected:
            errors.append(f"{path}: values are not in deterministic order")

    runtime_versions = manifest["compatibility"]["spine_runtime_versions"]
    ordered(
        runtime_versions,
        sorted(runtime_versions, key=lambda value: tuple(int(part) for part in value.split("."))),
        "$.compatibility.spine_runtime_versions",
    )
    contracts = manifest["compatibility"]["spine_content_contracts"]
    ordered(contracts, sorted(contracts), "$.compatibility.spine_content_contracts")

    archetypes = manifest["archetypes"]
    ordered(
        [entry["archetype_key"] for entry in archetypes],
        sorted(entry["archetype_key"] for entry in archetypes),
        "$.archetypes",
    )
    for index, archetype in enumerate(archetypes):
        item_types = archetype["revision"]["compatible_item_types"]
        ordered(item_types, sorted(item_types), f"$.archetypes[{index}].revision.compatible_item_types")

    profiles = manifest["notification_profiles"]
    ordered(
        [entry["profile_key"] for entry in profiles],
        sorted(entry["profile_key"] for entry in profiles),
        "$.notification_profiles",
    )
    for index, profile in enumerate(profiles):
        item_types = profile["revision"]["compatible_item_types"]
        ordered(
            item_types,
            sorted(item_types),
            f"$.notification_profiles[{index}].revision.compatible_item_types",
        )
        template_keys = [
            entry["template_key"] for entry in profile["revision"]["templates"]
        ]
        ordered(
            template_keys,
            sorted(template_keys),
            f"$.notification_profiles[{index}].revision.templates",
        )

    binding_keys = [entry["archetype_key"] for entry in manifest["binding_intents"]]
    ordered(binding_keys, sorted(binding_keys), "$.binding_intents")
    return errors


def canonical_json(value: Any) -> str:
    """Encode the no-number subset of spine.canonical-json.v1."""

    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        pieces = ['"']
        for character in value:
            codepoint = ord(character)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("invalid surrogate code point in canonical JSON")
            if character == '"':
                pieces.append('\\"')
            elif character == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(character)
        pieces.append('"')
        return "".join(pieces)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("canonical JSON object keys must be strings")
        return "{" + ",".join(
            canonical_json(key) + ":" + canonical_json(value[key])
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"JSON numbers and unsupported values are forbidden: {value!r}")


def content_digest(manifest: dict[str, Any]) -> str:
    semantic_manifest = {
        key: value for key, value in manifest.items() if key != "content_identity"
    }
    preimage = {
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine-pack-content-sha256.v1",
        "manifest": semantic_manifest,
    }
    encoded = canonical_json(preimage).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_pack(manifest: Any, schema: dict[str, Any]) -> list[str]:
    errors = schema_errors(manifest, schema, schema)
    if errors:
        return errors
    assert isinstance(manifest, dict)

    errors = _duplicate_errors(manifest)
    if errors:
        return errors
    errors = _schedule_errors(manifest)
    if errors:
        return errors
    errors = _reference_errors(manifest)
    if errors:
        return errors
    errors = _ordering_errors(manifest)
    if errors:
        return errors

    actual = manifest["content_identity"]["digest"]
    expected = content_digest(manifest)
    if actual != expected:
        return [f"$.content_identity.digest: expected {expected}, got {actual}"]
    return []
```

### Spec 16: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-apply-checkpoint.v1.schema.json

Hash: 3796907a3740ea8a130b2c024c11a48d92007bfec481dd046715181c604f4ac6

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-apply-checkpoint.v1.schema.json",
  "title": "Spine Pack Apply Checkpoint v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/applyCheckpoint"
}
```

### Spec 17: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-apply-result.v1.schema.json

Hash: a6a036e88233904537e8ed44466e73e68a584f0f1d695ccaa19f977851c47c55

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-apply-result.v1.schema.json",
  "title": "Spine Pack Apply Result v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/applyResult"
}
```

### Spec 18: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json

Hash: 35f34ee2df956e44706545b973645ed4c979164d5145665f086aeb189d385d8c

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-embedded-values.v1.schema.json",
  "title": "Spine pack embedded semantic projections and public command values",
  "$comment": "Source: Spine 0.3.0 commit 72203f092de191a7633b1884bf0d61836a25abe4. Archetype semantics derive from contracts/schemas/notification-profile-types.schema.json#/$defs/archetypeRevision; archetype requests derive from contracts/schemas/notification-profile-commands.schema.json#/$defs/archetypeCreate and #/$defs/archetypeRevise, including writeIdentity. Archetype responses derive from src/spine/commands/notification_profiles.py functions _archetype_create, _archetype_revise, and _success. That pinned runtime defines archetypes in these shared notification-profile files, not a separate item-archetype schema or command module. Profile/binding definitions also derive from contracts/schemas/notification-profile-types.schema.json, contracts/schemas/notification-profile-commands.schema.json, contracts/schemas/notification-types.schema.json, and src/spine/commands/notification_profiles.py facts and _success. Reachable definitions copied with local references; six write commands flattened. Semantics are installer projections, not full Spine readback envelopes.",
  "$defs": {
    "notifications_id": {
      "type": "string",
      "minLength": 1
    },
    "notifications_utcTimestamp": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "notifications_sha256": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "types_archetypeRevision": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "compatible_item_types": {
          "$ref": "#/$defs/types_itemTypes"
        }
      },
      "additionalProperties": false
    },
    "types_itemTypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 2,
      "uniqueItems": true,
      "items": {
        "enum": [
          "event",
          "task"
        ]
      }
    },
    "archetypeSemantics": {
      "$ref": "#/$defs/types_archetypeRevision"
    },
    "commands_profileMetadata": {
      "type": "object",
      "required": [
        "display_name",
        "description"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "types_profileRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/types_itemTypes"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/types_template"
          }
        }
      },
      "additionalProperties": false
    },
    "types_template": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/types_key"
        },
        "schedule": {
          "$ref": "#/$defs/notifications_schedule"
        },
        "late_handling": {
          "$ref": "#/$defs/notifications_lateHandling"
        }
      },
      "additionalProperties": false
    },
    "types_key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "notifications_schedule": {
      "oneOf": [
        {
          "$ref": "#/$defs/notifications_onceSchedule"
        },
        {
          "$ref": "#/$defs/notifications_offsetsSchedule"
        },
        {
          "$ref": "#/$defs/notifications_repeatWindowSchedule"
        }
      ]
    },
    "notifications_onceSchedule": {
      "type": "object",
      "required": [
        "kind",
        "at"
      ],
      "properties": {
        "kind": {
          "const": "once"
        },
        "at": {
          "$ref": "#/$defs/notifications_boundary"
        }
      },
      "additionalProperties": false
    },
    "notifications_boundary": {
      "oneOf": [
        {
          "$ref": "#/$defs/notifications_absoluteBoundary"
        },
        {
          "$ref": "#/$defs/notifications_targetOffset"
        }
      ]
    },
    "notifications_absoluteBoundary": {
      "type": "object",
      "required": [
        "kind",
        "at_utc"
      ],
      "properties": {
        "kind": {
          "const": "absolute_utc"
        },
        "at_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        }
      },
      "additionalProperties": false
    },
    "notifications_targetOffset": {
      "oneOf": [
        {
          "$ref": "#/$defs/notifications_elapsedTargetOffset"
        },
        {
          "$ref": "#/$defs/notifications_calendarTargetOffset"
        }
      ]
    },
    "notifications_elapsedTargetOffset": {
      "type": "object",
      "required": [
        "kind",
        "offset_basis",
        "offset_seconds"
      ],
      "properties": {
        "kind": {
          "const": "target_offset"
        },
        "offset_basis": {
          "const": "elapsed"
        },
        "offset_seconds": {
          "$ref": "#/$defs/notifications_signedDecimal"
        }
      },
      "additionalProperties": false
    },
    "notifications_signedDecimal": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)$"
    },
    "notifications_calendarTargetOffset": {
      "type": "object",
      "required": [
        "kind",
        "offset_basis",
        "offset_days",
        "local_time"
      ],
      "properties": {
        "kind": {
          "const": "target_offset"
        },
        "offset_basis": {
          "const": "calendar_days"
        },
        "offset_days": {
          "$ref": "#/$defs/notifications_signedDecimal"
        },
        "local_time": {
          "$ref": "#/$defs/notifications_localTime"
        },
        "timezone": {
          "type": "string",
          "minLength": 1
        },
        "timezone_database_version": {
          "type": "string",
          "minLength": 1
        }
      },
      "additionalProperties": false
    },
    "notifications_localTime": {
      "type": "string",
      "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
    },
    "notifications_offsetsSchedule": {
      "type": "object",
      "required": [
        "kind",
        "at"
      ],
      "properties": {
        "kind": {
          "const": "offsets"
        },
        "at": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/notifications_targetOffset"
          }
        }
      },
      "additionalProperties": false
    },
    "notifications_repeatWindowSchedule": {
      "type": "object",
      "required": [
        "kind",
        "start",
        "stop",
        "stop_inclusive",
        "cadence"
      ],
      "properties": {
        "kind": {
          "const": "repeat_window"
        },
        "start": {
          "$ref": "#/$defs/notifications_boundary"
        },
        "stop": {
          "$ref": "#/$defs/notifications_boundary"
        },
        "stop_inclusive": {
          "type": "boolean"
        },
        "cadence": {
          "$ref": "#/$defs/notifications_cadence"
        }
      },
      "additionalProperties": false
    },
    "notifications_cadence": {
      "oneOf": [
        {
          "$ref": "#/$defs/notifications_fixedElapsedCadence"
        },
        {
          "$ref": "#/$defs/notifications_localCalendarCadence"
        }
      ]
    },
    "notifications_fixedElapsedCadence": {
      "type": "object",
      "required": [
        "kind",
        "interval_seconds"
      ],
      "properties": {
        "kind": {
          "const": "fixed_elapsed"
        },
        "interval_seconds": {
          "$ref": "#/$defs/notifications_decimalPositive"
        }
      },
      "additionalProperties": false
    },
    "notifications_decimalPositive": {
      "type": "string",
      "pattern": "^[1-9][0-9]*$"
    },
    "notifications_localCalendarCadence": {
      "type": "object",
      "required": [
        "kind",
        "frequency",
        "seed_local_date",
        "local_time",
        "timezone",
        "timezone_database_version"
      ],
      "properties": {
        "kind": {
          "const": "local_calendar"
        },
        "frequency": {
          "enum": [
            "DAILY",
            "WEEKLY",
            "MONTHLY",
            "YEARLY"
          ]
        },
        "interval": {
          "$ref": "#/$defs/notifications_decimalPositive"
        },
        "seed_local_date": {
          "$ref": "#/$defs/notifications_localDate"
        },
        "local_time": {
          "$ref": "#/$defs/notifications_localTime"
        },
        "timezone": {
          "type": "string",
          "minLength": 1
        },
        "timezone_database_version": {
          "type": "string",
          "minLength": 1
        },
        "by_month": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "type": "string",
            "pattern": "^([1-9]|1[0-2])$"
          }
        },
        "by_month_day": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "type": "string",
            "pattern": "^-?([1-9]|[12][0-9]|3[01])$"
          }
        },
        "by_weekday": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/notifications_weekday"
          }
        },
        "by_set_position": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "type": "string",
            "pattern": "^-?([1-9]|[1-9][0-9]|[12][0-9]{2}|3[0-5][0-9]|36[0-6])$"
          }
        },
        "week_start": {
          "$ref": "#/$defs/notifications_weekday"
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "frequency": {
                "enum": [
                  "MONTHLY",
                  "YEARLY"
                ]
              }
            },
            "required": [
              "frequency"
            ]
          },
          "then": {
            "not": {
              "required": [
                "by_month_day",
                "by_weekday"
              ]
            }
          }
        },
        {
          "if": {
            "required": [
              "by_set_position"
            ]
          },
          "then": {
            "required": [
              "by_weekday"
            ]
          }
        },
        {
          "if": {
            "properties": {
              "frequency": {
                "const": "DAILY"
              }
            },
            "required": [
              "frequency"
            ]
          },
          "then": {
            "not": {
              "anyOf": [
                {
                  "required": [
                    "by_month"
                  ]
                },
                {
                  "required": [
                    "by_month_day"
                  ]
                },
                {
                  "required": [
                    "by_weekday"
                  ]
                },
                {
                  "required": [
                    "by_set_position"
                  ]
                },
                {
                  "required": [
                    "week_start"
                  ]
                }
              ]
            }
          }
        },
        {
          "if": {
            "properties": {
              "frequency": {
                "const": "WEEKLY"
              }
            },
            "required": [
              "frequency"
            ]
          },
          "then": {
            "not": {
              "anyOf": [
                {
                  "required": [
                    "by_month"
                  ]
                },
                {
                  "required": [
                    "by_month_day"
                  ]
                },
                {
                  "required": [
                    "by_set_position"
                  ]
                }
              ]
            }
          }
        },
        {
          "if": {
            "properties": {
              "frequency": {
                "const": "MONTHLY"
              }
            },
            "required": [
              "frequency"
            ]
          },
          "then": {
            "not": {
              "anyOf": [
                {
                  "required": [
                    "by_month"
                  ]
                },
                {
                  "required": [
                    "week_start"
                  ]
                }
              ]
            }
          }
        },
        {
          "if": {
            "properties": {
              "frequency": {
                "const": "YEARLY"
              }
            },
            "required": [
              "frequency"
            ]
          },
          "then": {
            "not": {
              "required": [
                "week_start"
              ]
            }
          }
        }
      ],
      "additionalProperties": false
    },
    "notifications_localDate": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    },
    "notifications_weekday": {
      "enum": [
        "MO",
        "TU",
        "WE",
        "TH",
        "FR",
        "SA",
        "SU"
      ]
    },
    "notifications_lateHandling": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "kind"
          ],
          "properties": {
            "kind": {
              "const": "skip"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "kind",
            "grace_seconds"
          ],
          "properties": {
            "kind": {
              "const": "deliver_within"
            },
            "grace_seconds": {
              "$ref": "#/$defs/notifications_decimalNonNegative"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "notifications_decimalNonNegative": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)$"
    },
    "profileSemantics": {
      "type": "object",
      "required": [
        "metadata",
        "revision"
      ],
      "properties": {
        "metadata": {
          "$ref": "#/$defs/commands_profileMetadata"
        },
        "revision": {
          "$ref": "#/$defs/types_profileRevision"
        }
      },
      "additionalProperties": false
    },
    "bindingSemantics": {
      "type": "object",
      "required": [
        "binding_kind",
        "notification_profile_key"
      ],
      "properties": {
        "binding_kind": {
          "const": "archetype_default"
        },
        "notification_profile_key": {
          "$ref": "#/$defs/types_key"
        }
      },
      "additionalProperties": false
    },
    "commands_writeIdentity": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        }
      }
    },
    "types_owner": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "owner_kind"
          ],
          "properties": {
            "owner_kind": {
              "const": "system"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "owner_kind",
            "owner_subject_id"
          ],
          "properties": {
            "owner_kind": {
              "const": "subject"
            },
            "owner_subject_id": {
              "$ref": "#/$defs/notifications_id"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "owner_kind",
            "owner_group_id"
          ],
          "properties": {
            "owner_kind": {
              "const": "subject_group"
            },
            "owner_group_id": {
              "$ref": "#/$defs/notifications_id"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "archetypeCreateTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "archetype_key",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "archetype_key": {
          "$ref": "#/$defs/types_key"
        },
        "revision": {
          "$ref": "#/$defs/types_archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "archetypeCreateRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "owner",
        "archetype_key",
        "revision"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "archetype_key": {
          "$ref": "#/$defs/types_key"
        },
        "revision": {
          "$ref": "#/$defs/types_archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "archetypeCreateResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "item_archetype_id",
        "item_archetype_revision_id",
        "revision_number",
        "status",
        "archetype_key",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "item_archetype.create"
        },
        "response_contract": {
          "const": "spine.item-archetypes.v1"
        },
        "effect": {
          "enum": [
            "item_archetype_created"
          ]
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "item_archetype_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision_number": {
          "$ref": "#/$defs/notifications_decimalPositive"
        },
        "status": {
          "const": "active"
        },
        "archetype_key": {
          "$ref": "#/$defs/types_key"
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "item_archetype_created"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "archetypeReviseTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "item_archetype_id",
        "expected_current_revision_id",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_current_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision": {
          "$ref": "#/$defs/types_archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "archetypeReviseRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "item_archetype_id",
        "expected_current_revision_id",
        "revision"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_current_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision": {
          "$ref": "#/$defs/types_archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "archetypeReviseResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "item_archetype_id",
        "item_archetype_revision_id",
        "revision_number",
        "status",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "item_archetype.revise"
        },
        "response_contract": {
          "const": "spine.item-archetypes.v1"
        },
        "effect": {
          "enum": [
            "item_archetype_revised"
          ]
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "item_archetype_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision_number": {
          "$ref": "#/$defs/notifications_decimalPositive"
        },
        "status": {
          "const": "active"
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "item_archetype_revised"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "profileCreateTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "profile_key",
        "display_name",
        "description",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "profile_key": {
          "$ref": "#/$defs/types_key"
        },
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "revision": {
          "$ref": "#/$defs/types_profileRevision"
        }
      },
      "additionalProperties": false
    },
    "profileCreateRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "owner",
        "profile_key",
        "display_name",
        "description",
        "revision"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "profile_key": {
          "$ref": "#/$defs/types_key"
        },
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "revision": {
          "$ref": "#/$defs/types_profileRevision"
        }
      },
      "additionalProperties": false
    },
    "profileCreateResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_id",
        "notification_profile_revision_id",
        "status",
        "revision_number",
        "normalized_revision_hash",
        "profile_key",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.create"
        },
        "response_contract": {
          "const": "spine.notification-profiles.v1"
        },
        "effect": {
          "enum": [
            "notification_profile_created"
          ]
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "status": {
          "const": "active"
        },
        "revision_number": {
          "$ref": "#/$defs/notifications_decimalPositive"
        },
        "normalized_revision_hash": {
          "$ref": "#/$defs/notifications_sha256"
        },
        "profile_key": {
          "$ref": "#/$defs/types_key"
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "notification_profile_created"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "profileMetadataUpdateTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "notification_profile_id",
        "expected_metadata",
        "metadata"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profile-metadata-update.v1"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_metadata": {
          "$ref": "#/$defs/commands_profileMetadata"
        },
        "metadata": {
          "$ref": "#/$defs/commands_profileMetadata"
        }
      },
      "additionalProperties": false
    },
    "profileMetadataUpdateRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "notification_profile_id",
        "expected_metadata",
        "metadata"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.notification-profile-metadata-update.v1"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_metadata": {
          "$ref": "#/$defs/commands_profileMetadata"
        },
        "metadata": {
          "$ref": "#/$defs/commands_profileMetadata"
        }
      },
      "additionalProperties": false
    },
    "profileMetadataUpdateResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_id",
        "notification_profile_revision_id",
        "status",
        "display_name",
        "description",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.metadata.update"
        },
        "response_contract": {
          "const": "spine.notification-profile-metadata-update.v1"
        },
        "effect": {
          "enum": [
            "notification_profile_metadata_updated",
            "notification_profile_metadata_update_noop"
          ]
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "status": {
          "const": "active"
        },
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "notification_profile_metadata_updated",
                "notification_profile_metadata_update_noop"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "profileReviseTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "notification_profile_id",
        "expected_current_revision_id",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_current_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision": {
          "$ref": "#/$defs/types_profileRevision"
        }
      },
      "additionalProperties": false
    },
    "profileReviseRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "notification_profile_id",
        "expected_current_revision_id",
        "revision"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "expected_current_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "revision": {
          "$ref": "#/$defs/types_profileRevision"
        }
      },
      "additionalProperties": false
    },
    "profileReviseResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_id",
        "notification_profile_revision_id",
        "status",
        "revision_number",
        "normalized_revision_hash",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.revise"
        },
        "response_contract": {
          "const": "spine.notification-profiles.v1"
        },
        "effect": {
          "enum": [
            "notification_profile_revised"
          ]
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "status": {
          "const": "active"
        },
        "revision_number": {
          "$ref": "#/$defs/notifications_decimalPositive"
        },
        "normalized_revision_hash": {
          "$ref": "#/$defs/notifications_sha256"
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "notification_profile_revised"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "bindingSetTemplate": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "item_archetype_id",
        "notification_profile_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        }
      },
      "additionalProperties": false
    },
    "bindingSetRequest": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "contract_version",
        "owner",
        "item_archetype_id",
        "notification_profile_id"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/notifications_utcTimestamp"
        },
        "contract_version": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "owner": {
          "$ref": "#/$defs/types_owner"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        }
      },
      "additionalProperties": false
    },
    "bindingSetResponse": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_binding_id",
        "item_archetype_id",
        "notification_profile_id",
        "status",
        "compatible_item_types",
        "receipt"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.binding.set"
        },
        "response_contract": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "effect": {
          "enum": [
            "notification_profile_binding_set",
            "notification_profile_binding_set_noop"
          ]
        },
        "notification_profile_binding_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/notifications_id"
        },
        "status": {
          "const": "active"
        },
        "compatible_item_types": {
          "$ref": "#/$defs/types_itemTypes"
        },
        "receipt": {
          "type": "object",
          "required": [
            "command_receipt_id",
            "command_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "properties": {
            "command_receipt_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "command_id": {
              "$ref": "#/$defs/notifications_id"
            },
            "effect": {
              "enum": [
                "notification_profile_binding_set",
                "notification_profile_binding_set_noop"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/notifications_sha256"
            },
            "created_at_utc": {
              "$ref": "#/$defs/notifications_utcTimestamp"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 19: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-approval.v1.schema.json

Hash: be392d002c2139f4ff614f2de9a04e01c2fc34b0159af6f4e61cbf5433085d14

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-approval.v1.schema.json",
  "title": "Spine Pack Installation Approval v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/installationApproval"
}
```

### Spec 20: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-plan.v1.schema.json

Hash: 9e115dcf525f5d7e9de3459d75e6a5adf0980eab91fc6b93aa64e817dac8fb14

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-plan.v1.schema.json",
  "title": "Spine Pack Installation Plan v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/installationPlan"
}
```

### Spec 21: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-request.v1.schema.json

Hash: fe673791f20df6f274728efa87bae571c2246d5ca76657ab3f6b31d7d991ce0d

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-request.v1.schema.json",
  "title": "Spine Pack Installation Request v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/installationRequest"
}
```

### Spec 22: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-installer-result.v1.schema.json

Hash: bb363061fc907ceb04d683f22818a96b56b19ef3b8af83ffc44b47afa6631753

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-installer-result.v1.schema.json",
  "title": "Spine Pack Installer CLI Result v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/installerResult"
}
```

### Spec 23: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-installer-types.v1.schema.json

Hash: c96ed63d07fe9368dfa2dac9445998b8f511bea0fea037e31e6c281861f11e18

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-installer-types.v1.schema.json",
  "title": "Spine Pack Installer Shared Types v1",
  "$defs": {
    "id": { "type": "string", "minLength": 1, "maxLength": 256 },
    "key": { "type": "string", "pattern": "^[a-z][a-z0-9_-]{0,63}$" },
    "decimal": { "type": "string", "pattern": "^(0|[1-9][0-9]*)$" },
    "sha256": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
    "utc": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$" },
    "uuid4": { "type": "string", "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$" },
    "absolutePath": { "type": "string", "minLength": 2, "maxLength": 4096, "pattern": "^/.*[^/]$" },
    "nullableString": {
      "oneOf": [
        { "type": "string", "minLength": 1, "maxLength": 4096 },
        { "type": "null" }
      ]
    },
    "contentIdentity": {
      "type": "object",
      "required": ["algorithm", "canonical_json_version", "derivation_version", "digest"],
      "properties": {
        "algorithm": { "const": "sha256" },
        "canonical_json_version": { "const": "spine.canonical-json.v1" },
        "derivation_version": {
          "enum": [
            "spine.pack-install-request-digest.v1",
            "spine.pack-install-plan-digest.v1",
            "spine.pack-install-approval-digest.v1",
            "spine.pack-apply-checkpoint-digest.v1",
            "spine.pack-apply-result-digest.v1",
            "spine.pack-verification-result-digest.v1"
          ]
        },
        "digest": { "$ref": "#/$defs/sha256" }
      },
      "additionalProperties": false
    },
    "canonicalValue": {
      "type": "object",
      "required": ["contract", "shape", "canonical_json", "digest"],
      "properties": {
        "shape": { "enum": ["archetypeSemantics","profileSemantics","bindingSemantics","archetypeCreateTemplate","archetypeCreateRequest","archetypeCreateResponse","archetypeReviseTemplate","archetypeReviseRequest","archetypeReviseResponse","profileCreateTemplate","profileCreateRequest","profileCreateResponse","profileMetadataUpdateTemplate","profileMetadataUpdateRequest","profileMetadataUpdateResponse","profileReviseTemplate","profileReviseRequest","profileReviseResponse","bindingSetTemplate","bindingSetRequest","bindingSetResponse"] },
        "contract": { "type": "string", "minLength": 1, "maxLength": 160 },
        "canonical_json": { "type": "string", "minLength": 2, "maxLength": 8388608 },
        "digest": { "$ref": "#/$defs/sha256" }
      },
      "additionalProperties": false
    },
    "selection": {
      "oneOf": [
        {
          "type": "object",
          "required": ["mode"],
          "properties": { "mode": { "const": "all" } },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": ["mode", "archetype_keys"],
          "properties": {
            "mode": { "const": "archetypes" },
            "archetype_keys": {
              "type": "array",
              "minItems": 1,
              "maxItems": 256,
              "uniqueItems": true,
              "items": { "$ref": "#/$defs/key" }
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "owner": {
      "oneOf": [
        {
          "type": "object",
          "required": ["owner_kind", "owner_subject_id"],
          "properties": {
            "owner_kind": { "const": "subject" },
            "owner_subject_id": { "$ref": "#/$defs/id" }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": ["owner_kind", "owner_group_id"],
          "properties": {
            "owner_kind": { "const": "subject_group" },
            "owner_group_id": { "$ref": "#/$defs/id" }
          },
          "additionalProperties": false
        }
      ]
    },
    "target": {
      "type": "object",
      "required": ["host_name", "spine_command", "ledger"],
      "properties": {
        "host_name": { "type": "string", "minLength": 1, "maxLength": 253, "pattern": "^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$" },
        "spine_command": {
          "type": "object",
          "required": ["path", "sha256"],
          "properties": {
            "path": { "$ref": "#/$defs/absolutePath" },
            "sha256": { "$ref": "#/$defs/sha256" }
          },
          "additionalProperties": false
        },
        "ledger": {
          "type": "object",
          "required": ["kind", "path"],
          "properties": {
            "kind": { "const": "path" },
            "path": { "$ref": "#/$defs/absolutePath" }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "requestBody": {
      "type": "object",
      "required": ["selection", "owner", "target", "draft_posture"],
      "properties": {
        "selection": { "$ref": "#/$defs/selection" },
        "owner": { "$ref": "#/$defs/owner" },
        "target": { "$ref": "#/$defs/target" },
        "draft_posture": { "enum": ["reject", "inspect_only"] }
      },
      "additionalProperties": false
    },
    "packIdentity": {
      "type": "object",
      "required": ["manifest_schema", "pack_id", "version", "status", "manifest_digest"],
      "properties": {
        "manifest_schema": { "const": "spine.pack-manifest.v1" },
        "pack_id": { "type": "string", "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", "maxLength": 64 },
        "version": { "type": "string", "minLength": 5, "maxLength": 64 },
        "status": { "enum": ["draft", "released"] },
        "manifest_digest": { "$ref": "#/$defs/sha256" }
      },
      "additionalProperties": false
    },
    "closure": {
      "type": "object",
      "required": ["archetype_keys", "profile_keys", "binding_archetype_keys"],
      "properties": {
        "archetype_keys": { "type": "array", "maxItems": 256, "uniqueItems": true, "items": { "$ref": "#/$defs/key" } },
        "profile_keys": { "type": "array", "maxItems": 256, "uniqueItems": true, "items": { "$ref": "#/$defs/key" } },
        "binding_archetype_keys": { "type": "array", "maxItems": 256, "uniqueItems": true, "items": { "$ref": "#/$defs/key" } }
      },
      "additionalProperties": false
    },
    "environment": {
      "type": "object",
      "required": ["runtime_version", "ledger_schema_implemented", "ledger_schema_current", "advertised_contracts"],
      "properties": {
        "runtime_version": { "const": "0.3.0" },
        "ledger_schema_implemented": { "const": "12" },
        "ledger_schema_current": { "const": "12" },
        "advertised_contracts": {
          "type": "array",
          "minItems": 1,
          "maxItems": 512,
          "uniqueItems": true,
          "items": { "type": "string", "minLength": 1, "maxLength": 160 }
        }
      },
      "additionalProperties": false
    },
    "catalogSnapshot": {
      "type": "object",
      "required": ["catalog", "digest"],
      "properties": {
        "catalog": { "enum": ["archetypes", "profiles", "bindings"] },
        "digest": { "$ref": "#/$defs/sha256" }
      },
      "additionalProperties": false
    },
    "catalogIdentity": {
      "type": "object",
      "required": ["catalog_id"],
      "properties": { "catalog_id": { "$ref": "#/$defs/id" } },
      "additionalProperties": false
    },
    "observedBindingIdentity": {
      "type": "object",
      "required": ["notification_profile_binding_id", "item_archetype_id", "notification_profile_id"],
      "properties": {
        "notification_profile_binding_id": { "$ref": "#/$defs/id" },
        "item_archetype_id": { "$ref": "#/$defs/id" },
        "notification_profile_id": { "$ref": "#/$defs/id" }
      },
      "additionalProperties": false
    },
    "bindingIdentity": {
      "type": "object",
      "required": ["item_archetype_id", "notification_profile_id", "observed_binding"],
      "properties": {
        "item_archetype_id": { "oneOf": [{ "$ref": "#/$defs/id" }, { "type": "null" }] },
        "notification_profile_id": { "oneOf": [{ "$ref": "#/$defs/id" }, { "type": "null" }] },
        "observed_binding": { "oneOf": [{ "$ref": "#/$defs/observedBindingIdentity" }, { "type": "null" }] }
      },
      "additionalProperties": false
    },
    "classification": {
      "type": "object",
      "required": ["object_kind", "object_key", "classification", "desired", "observed", "identity", "blocked_reason"],
      "properties": {
        "object_kind": { "enum": ["archetype", "profile", "binding"] },
        "object_key": { "type": "string", "minLength": 11, "maxLength": 96 },
        "classification": { "enum": ["missing", "equivalent", "drifted", "blocked"] },
        "desired": { "$ref": "#/$defs/canonicalValue" },
        "observed": {
          "oneOf": [
            { "$ref": "#/$defs/canonicalValue" },
            { "type": "null" }
          ]
        },
        "identity": {
          "oneOf": [
            { "$ref": "#/$defs/catalogIdentity" },
            { "$ref": "#/$defs/bindingIdentity" },
            { "type": "null" }
          ]
        },
        "blocked_reason": { "$ref": "#/$defs/nullableString" }
      },
      "additionalProperties": false
    },
    "action": {
      "type": "object",
      "required": ["ordinal", "action_id", "command", "object_key", "change_kind", "desired", "expected", "request_template"],
      "properties": {
        "ordinal": { "$ref": "#/$defs/decimal" },
        "action_id": { "type": "string", "pattern": "^action-[0-9]{6}$" },
        "command": {
          "enum": [
            "item_archetype.create",
            "item_archetype.revise",
            "notification_profile.create",
            "notification_profile.metadata.update",
            "notification_profile.revise",
            "notification_profile.binding.set"
          ]
        },
        "object_key": { "type": "string", "minLength": 11, "maxLength": 96 },
        "change_kind": { "enum": ["create", "update"] },
        "desired": { "$ref": "#/$defs/canonicalValue" },
        "expected": {
          "oneOf": [
            { "$ref": "#/$defs/canonicalValue" },
            { "type": "null" }
          ]
        },
        "request_template": { "$ref": "#/$defs/canonicalValue" }
      },
      "additionalProperties": false
    },
    "execution": {
      "type": "object",
      "required": ["execution_id", "actor_subject_id", "action_timestamp_utc"],
      "properties": {
        "execution_id": { "$ref": "#/$defs/uuid4" },
        "actor_subject_id": { "$ref": "#/$defs/id" },
        "action_timestamp_utc": { "$ref": "#/$defs/utc" }
      },
      "additionalProperties": false
    },
    "generatedId": {
      "type": "object",
      "required": ["name", "value"],
      "properties": {
        "name": { "type": "string", "minLength": 1, "maxLength": 160 },
        "value": { "$ref": "#/$defs/id" }
      },
      "additionalProperties": false
    },
    "responseEvidence": {
      "type": "object",
      "required": ["action_id", "command", "command_id", "outcome", "response_contract", "effect", "generated_ids", "command_receipt_id", "semantic_facts_hash", "response"],
      "properties": {
        "action_id": { "type": "string", "pattern": "^action-[0-9]{6}$" },
        "command": { "type": "string", "minLength": 1, "maxLength": 160 },
        "command_id": { "type": "string", "pattern": "^spack_[0-9a-f]{64}$" },
        "outcome": { "enum": ["accepted", "compatible_replay"] },
        "response_contract": { "type": "string", "minLength": 1, "maxLength": 160 },
        "effect": { "type": "string", "minLength": 1, "maxLength": 160 },
        "generated_ids": { "type": "array", "maxItems": 16, "items": { "$ref": "#/$defs/generatedId" } },
        "command_receipt_id": { "$ref": "#/$defs/id" },
        "semantic_facts_hash": { "$ref": "#/$defs/sha256" },
        "response": { "$ref": "#/$defs/canonicalValue" }
      },
      "additionalProperties": false
    },
    "error": {
      "type": "object",
      "required": ["category", "code", "message", "facts"],
      "properties": {
        "category": {
          "enum": [
            "invalid_cli_or_artifact_input",
            "invalid_pack_contract_or_digest",
            "incompatible_spine_runtime_or_contracts",
            "decision_required_for_drift",
            "blocked_desired_state",
            "stale_plan_or_target_mismatch",
            "spine_command_rejection",
            "partial_apply",
            "verification_mismatch",
            "transport_or_environment_failure"
          ]
        },
        "code": { "type": "string", "pattern": "^[a-z][a-z0-9_]{0,95}$" },
        "message": { "type": "string", "minLength": 1, "maxLength": 2000 },
        "facts": { "type": "array", "maxItems": 64, "items": { "$ref": "#/$defs/generatedId" } }
      },
      "additionalProperties": false
    },
    "installationRequest": {
      "type": "object",
      "required": ["artifact_schema", "request", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-install-request.v1" },
        "request": { "$ref": "#/$defs/requestBody" },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "installationPlan": {
      "type": "object",
      "required": ["artifact_schema", "request_digest", "request", "pack", "closure", "environment", "required_execution_contracts", "catalog_snapshots", "classifications", "actions", "decision_action_ids", "blocked_object_keys", "apply_eligible", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-install-plan.v1" },
        "request_digest": { "$ref": "#/$defs/sha256" },
        "request": { "$ref": "#/$defs/requestBody" },
        "pack": { "$ref": "#/$defs/packIdentity" },
        "closure": { "$ref": "#/$defs/closure" },
        "environment": { "$ref": "#/$defs/environment" },
        "required_execution_contracts": { "type": "array", "minItems": 9, "maxItems": 9, "uniqueItems": true, "items": { "type": "string", "minLength": 1, "maxLength": 160 } },
        "catalog_snapshots": { "type": "array", "minItems": 3, "maxItems": 3, "items": { "$ref": "#/$defs/catalogSnapshot" } },
        "classifications": { "type": "array", "maxItems": 768, "items": { "$ref": "#/$defs/classification" } },
        "actions": { "type": "array", "maxItems": 1024, "items": { "$ref": "#/$defs/action" } },
        "decision_action_ids": { "type": "array", "maxItems": 1024, "uniqueItems": true, "items": { "type": "string", "pattern": "^action-[0-9]{6}$" } },
        "blocked_object_keys": { "type": "array", "maxItems": 768, "uniqueItems": true, "items": { "type": "string", "minLength": 11, "maxLength": 96 } },
        "apply_eligible": { "type": "boolean" },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "installationApproval": {
      "type": "object",
      "required": ["artifact_schema", "plan_digest", "approve_complete_plan", "acknowledge_single_operator", "authorized_update_action_ids", "execution", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-install-approval.v1" },
        "plan_digest": { "$ref": "#/$defs/sha256" },
        "approve_complete_plan": { "const": true },
        "acknowledge_single_operator": { "const": true },
        "authorized_update_action_ids": { "type": "array", "maxItems": 1024, "uniqueItems": true, "items": { "type": "string", "pattern": "^action-[0-9]{6}$" } },
        "execution": { "$ref": "#/$defs/execution" },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "unresolvedSubmission": {
      "type": "object",
      "required": ["action_id", "command_id", "submission_state", "request"],
      "properties": {
        "action_id": { "type": "string", "pattern": "^action-[0-9]{6}$" },
        "command_id": { "type": "string", "pattern": "^spack_[0-9a-f]{64}$" },
        "submission_state": { "const": "prepared_or_submitted" },
        "request": { "$ref": "#/$defs/canonicalValue" }
      },
      "additionalProperties": false
    },
    "applyCheckpoint": {
      "type": "object",
      "required": ["artifact_schema", "plan_digest", "approval_digest", "execution", "accepted_responses", "unresolved_submission", "next_action_id", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-apply-checkpoint.v1" },
        "plan_digest": { "$ref": "#/$defs/sha256" },
        "approval_digest": { "$ref": "#/$defs/sha256" },
        "execution": { "$ref": "#/$defs/execution" },
        "accepted_responses": { "type": "array", "maxItems": 1024, "items": { "$ref": "#/$defs/responseEvidence" } },
        "unresolved_submission": {
          "oneOf": [
            { "$ref": "#/$defs/unresolvedSubmission" },
            { "type": "null" }
          ]
        },
        "next_action_id": {
          "oneOf": [
            { "type": "string", "pattern": "^action-[0-9]{6}$" },
            { "type": "null" }
          ]
        },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "applyFailure": {
      "type": "object",
      "required": ["action_id", "error"],
      "properties": {
        "action_id": {
          "oneOf": [
            { "type": "string", "pattern": "^action-[0-9]{6}$" },
            { "type": "null" }
          ]
        },
        "error": { "$ref": "#/$defs/error" }
      },
      "additionalProperties": false
    },
    "applyResult": {
      "type": "object",
      "required": ["artifact_schema", "plan_digest", "approval_digest", "execution", "state", "accepted_responses", "failure", "unattempted_action_ids", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-apply-result.v1" },
        "plan_digest": { "$ref": "#/$defs/sha256" },
        "approval_digest": { "$ref": "#/$defs/sha256" },
        "execution": { "$ref": "#/$defs/execution" },
        "state": { "enum": ["applied", "partial", "not_applied"] },
        "accepted_responses": { "type": "array", "maxItems": 1024, "items": { "$ref": "#/$defs/responseEvidence" } },
        "failure": {
          "oneOf": [
            { "$ref": "#/$defs/applyFailure" },
            { "type": "null" }
          ]
        },
        "unattempted_action_ids": { "type": "array", "maxItems": 1024, "uniqueItems": true, "items": { "type": "string", "pattern": "^action-[0-9]{6}$" } },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "verificationObject": {
      "type": "object",
      "required": ["object_kind", "object_key", "state", "observed"],
      "properties": {
        "object_kind": { "enum": ["archetype", "profile", "binding"] },
        "object_key": { "type": "string", "minLength": 11, "maxLength": 96 },
        "state": { "enum": ["equivalent", "missing", "drifted", "blocked", "ambiguous"] },
        "observed": {
          "oneOf": [
            { "$ref": "#/$defs/canonicalValue" },
            { "type": "null" }
          ]
        }
      },
      "additionalProperties": false
    },
    "verificationResult": {
      "type": "object",
      "required": ["artifact_schema", "plan_digest", "apply_result_digest", "pack", "target", "environment", "catalog_snapshots", "closure", "object_results", "response_evidence", "receipt_readback", "state", "content_identity"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-verification-result.v1" },
        "plan_digest": { "$ref": "#/$defs/sha256" },
        "apply_result_digest": {
          "oneOf": [
            { "$ref": "#/$defs/sha256" },
            { "type": "null" }
          ]
        },
        "pack": { "$ref": "#/$defs/packIdentity" },
        "target": { "$ref": "#/$defs/target" },
        "environment": { "$ref": "#/$defs/environment" },
        "catalog_snapshots": { "type": "array", "minItems": 3, "maxItems": 3, "items": { "$ref": "#/$defs/catalogSnapshot" } },
        "closure": { "$ref": "#/$defs/closure" },
        "object_results": { "type": "array", "maxItems": 768, "items": { "$ref": "#/$defs/verificationObject" } },
        "response_evidence": { "enum": ["not_required", "complete", "missing", "invalid"] },
        "receipt_readback": { "const": "captured_responses_only_spine_0.3.0" },
        "state": { "enum": ["verified", "mismatch"] },
        "content_identity": { "$ref": "#/$defs/contentIdentity" }
      },
      "additionalProperties": false
    },
    "artifactReference": {
      "type": "object",
      "required": ["path", "digest"],
      "properties": {
        "path": { "type": "string", "minLength": 1, "maxLength": 4096 },
        "digest": { "$ref": "#/$defs/sha256" }
      },
      "additionalProperties": false
    },
    "installerResult": {
      "type": "object",
      "required": ["artifact_schema", "operation", "status", "exit_code", "artifact", "error"],
      "properties": {
        "artifact_schema": { "const": "spine.pack-installer-result.v1" },
        "operation": { "enum": ["plan", "apply", "verify"] },
        "status": { "enum": ["success", "failed", "decision_required", "blocked", "partial", "mismatch"] },
        "exit_code": { "enum": ["0", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"] },
        "artifact": {
          "oneOf": [
            { "$ref": "#/$defs/artifactReference" },
            { "type": "null" }
          ]
        },
        "error": {
          "oneOf": [
            { "$ref": "#/$defs/error" },
            { "type": "null" }
          ]
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 24: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-manifest.v1.schema.json

Hash: e1769666de8f14b84d0c12e370bf97560c9f105cc3cc771a5a41466ae3f2d8d8

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-manifest.v1.schema.json",
  "title": "Spine Pack Manifest v1",
  "type": "object",
  "required": [
    "manifest_schema",
    "pack",
    "compatibility",
    "dependencies",
    "archetypes",
    "notification_profiles",
    "binding_intents",
    "content_identity"
  ],
  "properties": {
    "manifest_schema": { "const": "spine.pack-manifest.v1" },
    "pack": { "$ref": "#/$defs/pack" },
    "compatibility": { "$ref": "#/$defs/compatibility" },
    "dependencies": {
      "type": "array",
      "maxItems": 0
    },
    "archetypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/archetype" }
    },
    "notification_profiles": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/notificationProfile" }
    },
    "binding_intents": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/bindingIntent" }
    },
    "content_identity": { "$ref": "#/$defs/contentIdentity" }
  },
  "additionalProperties": false,
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "packId": {
      "type": "string",
      "maxLength": 64,
      "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
    },
    "stableVersion": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)$"
    },
    "draftVersion": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)-draft\\.[1-9][0-9]*$"
    },
    "pack": {
      "oneOf": [
        {
          "type": "object",
          "required": ["pack_id", "version", "status"],
          "properties": {
            "pack_id": { "$ref": "#/$defs/packId" },
            "version": { "$ref": "#/$defs/draftVersion" },
            "status": { "const": "draft" }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": ["pack_id", "version", "status"],
          "properties": {
            "pack_id": { "$ref": "#/$defs/packId" },
            "version": { "$ref": "#/$defs/stableVersion" },
            "status": { "const": "released" }
          },
          "additionalProperties": false
        }
      ]
    },
    "compatibility": {
      "type": "object",
      "required": ["spine_runtime_versions", "spine_content_contracts"],
      "properties": {
        "spine_runtime_versions": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": { "$ref": "#/$defs/stableVersion" }
        },
        "spine_content_contracts": {
          "type": "array",
          "minItems": 3,
          "maxItems": 3,
          "uniqueItems": true,
          "items": {
            "enum": [
              "spine.item-archetypes.v1",
              "spine.notification-profile-bindings.v1",
              "spine.notification-profiles.v1"
            ]
          }
        }
      },
      "additionalProperties": false
    },
    "itemTypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 2,
      "uniqueItems": true,
      "items": { "enum": ["event", "task"] }
    },
    "description": {
      "oneOf": [
        { "type": "string", "minLength": 1, "maxLength": 2000 },
        { "type": "null" }
      ]
    },
    "archetypeRevision": {
      "type": "object",
      "required": ["display_name", "description", "compatible_item_types"],
      "properties": {
        "display_name": { "type": "string", "minLength": 1, "maxLength": 160 },
        "description": { "$ref": "#/$defs/description" },
        "compatible_item_types": { "$ref": "#/$defs/itemTypes" }
      },
      "additionalProperties": false
    },
    "archetype": {
      "type": "object",
      "required": ["archetype_key", "intended_status", "revision"],
      "properties": {
        "archetype_key": { "$ref": "#/$defs/key" },
        "intended_status": { "const": "active" },
        "revision": { "$ref": "#/$defs/archetypeRevision" }
      },
      "additionalProperties": false
    },
    "elapsedAtOrBeforeSchedule": {
      "type": "object",
      "required": ["kind", "at"],
      "properties": {
        "kind": { "const": "once" },
        "at": {
          "type": "object",
          "required": ["kind", "offset_basis", "offset_seconds"],
          "properties": {
            "kind": { "const": "target_offset" },
            "offset_basis": { "const": "elapsed" },
            "offset_seconds": {
              "type": "string",
              "pattern": "^(?:0|-[1-9][0-9]*)$"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "calendarDaySchedule": {
      "type": "object",
      "required": ["kind", "at"],
      "properties": {
        "kind": { "const": "once" },
        "at": {
          "type": "object",
          "required": ["kind", "offset_basis", "offset_days", "local_time"],
          "properties": {
            "kind": { "const": "target_offset" },
            "offset_basis": { "const": "calendar_days" },
            "offset_days": {
              "type": "string",
              "pattern": "^(?:0|-[1-9][0-9]{0,3})$"
            },
            "local_time": {
              "type": "string",
              "pattern": "^(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "lateHandling": {
      "type": "object",
      "required": ["kind", "grace_seconds"],
      "properties": {
        "kind": { "const": "deliver_within" },
        "grace_seconds": {
          "type": "string",
          "pattern": "^[1-9][0-9]*$"
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": ["template_key", "schedule", "late_handling"],
      "properties": {
        "template_key": { "$ref": "#/$defs/key" },
        "schedule": {
          "oneOf": [
            { "$ref": "#/$defs/elapsedAtOrBeforeSchedule" },
            { "$ref": "#/$defs/calendarDaySchedule" }
          ]
        },
        "late_handling": { "$ref": "#/$defs/lateHandling" }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": ["compatible_item_types", "templates"],
      "properties": {
        "compatible_item_types": { "$ref": "#/$defs/itemTypes" },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": { "$ref": "#/$defs/template" }
        }
      },
      "additionalProperties": false
    },
    "notificationProfile": {
      "type": "object",
      "required": [
        "profile_key",
        "display_name",
        "description",
        "intended_status",
        "revision"
      ],
      "properties": {
        "profile_key": { "$ref": "#/$defs/key" },
        "display_name": { "type": "string", "minLength": 1, "maxLength": 160 },
        "description": { "$ref": "#/$defs/description" },
        "intended_status": { "const": "active" },
        "revision": { "$ref": "#/$defs/profileRevision" }
      },
      "additionalProperties": false
    },
    "bindingIntent": {
      "type": "object",
      "required": ["binding_kind", "archetype_key", "notification_profile_key"],
      "properties": {
        "binding_kind": { "const": "archetype_default" },
        "archetype_key": { "$ref": "#/$defs/key" },
        "notification_profile_key": { "$ref": "#/$defs/key" }
      },
      "additionalProperties": false
    },
    "contentIdentity": {
      "type": "object",
      "required": ["algorithm", "canonical_json_version", "digest"],
      "properties": {
        "algorithm": { "const": "sha256" },
        "canonical_json_version": { "const": "spine.canonical-json.v1" },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 25: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-verification-result.v1.schema.json

Hash: c4d357a3641729f40aac6ff670403bed65016b9c3953669a5d79e8b4ada64808

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-verification-result.v1.schema.json",
  "title": "Spine Pack Verification Result v1",
  "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/verificationResult"
}
```

### Spec 26: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json

Hash: 80bcc0fbb003b7702fdc17424db6287ebdd696cc5e2d8a1411c359573004a69f

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-readback-0.3.0.schema.json",
  "$comment": "Pinned to Spine commit 72203f092de191a7633b1884bf0d61836a25abe4. systemInfo is copied from contracts/schemas/system-info-response-v2.schema.json. Catalog success shapes derive from src/spine/commands/notification_profiles.py _list_roots, _show_root, _binding_list and src/spine/ledger/notification_profiles.py load_archetype/load_profile; returned column shapes are pinned from migrations/0010_notification_profiles.sql. This is a public response validator, not database access. Native integer revision_number/template_index values occur only in raw public readbacks and never in installer artifacts. ListRequest/ShowRequest definitions deliberately narrow the public surface to fields emitted by this planner.",
  "$defs": {
    "id": {
      "type": "string",
      "minLength": 1
    },
    "systemInfo": {
      "title": "Spine System Information Response v2",
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "runtime_version",
        "implemented_ledger_schema_version",
        "ledger_schema_version",
        "timezone_database_version",
        "implemented_contract_versions",
        "runtime_dependencies"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "system.info"
        },
        "response_contract": {
          "const": "spine.system-info.v2"
        },
        "runtime_version": {
          "type": "string",
          "minLength": 1
        },
        "implemented_ledger_schema_version": {
          "type": "string",
          "pattern": "^[1-9][0-9]*$"
        },
        "ledger_schema_version": {
          "type": "string",
          "pattern": "^[1-9][0-9]*$"
        },
        "timezone_database_version": {
          "type": "string",
          "minLength": 1
        },
        "implemented_contract_versions": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "type": "string",
            "minLength": 1
          },
          "allOf": [
            {
              "contains": {
                "const": "spine.system-info.v2"
              },
              "minContains": 1,
              "maxContains": 1
            },
            {
              "contains": {
                "const": "spine.tickerd-compatibility.v1"
              },
              "minContains": 1,
              "maxContains": 1
            }
          ]
        },
        "runtime_dependencies": {
          "type": "array",
          "minItems": 1,
          "maxItems": 1,
          "uniqueItems": true,
          "items": {
            "type": "object",
            "required": [
              "name",
              "package_version",
              "capability_id",
              "descriptor_sha256",
              "compatibility_contract",
              "status"
            ],
            "properties": {
              "name": {
                "const": "tickerd"
              },
              "package_version": {
                "const": "0.2.0"
              },
              "capability_id": {
                "const": "tickerd.runtime-capabilities.v1"
              },
              "descriptor_sha256": {
                "const": "215f9aa6b54e6c0e6186796a55d78e1c5a270adc9b3ccefb433df5a3bb87b58b"
              },
              "compatibility_contract": {
                "const": "spine.tickerd-compatibility.v1"
              },
              "status": {
                "const": "compatible"
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": [
        "notification_profile_template_id",
        "notification_profile_revision_id",
        "template_index",
        "normalized_template_hash",
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "notification_profile_template_id": {
          "$ref": "#/$defs/id"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/id"
        },
        "template_index": {
          "type": "integer",
          "minimum": 0
        },
        "normalized_template_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "template_key": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_key"
        },
        "schedule": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_schedule"
        },
        "late_handling": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_lateHandling"
        }
      },
      "additionalProperties": false
    },
    "archetypeRevision": {
      "type": "object",
      "required": [
        "item_archetype_revision_id",
        "item_archetype_id",
        "revision_number",
        "created_by_subject_id",
        "created_by_command_id",
        "created_at_utc",
        "display_name",
        "description",
        "compatible_item_types",
        "normalized_content_hash"
      ],
      "properties": {
        "item_archetype_revision_id": {
          "$ref": "#/$defs/id"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/id"
        },
        "revision_number": {
          "type": "integer",
          "minimum": 1
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/id"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/id"
        },
        "created_at_utc": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
        },
        "display_name": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/display_name"
        },
        "description": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/description"
        },
        "compatible_item_types": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_itemTypes"
        },
        "normalized_content_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": [
        "notification_profile_revision_id",
        "notification_profile_id",
        "revision_number",
        "created_by_subject_id",
        "created_by_command_id",
        "created_at_utc",
        "compatible_item_types",
        "normalized_revision_hash",
        "templates"
      ],
      "properties": {
        "notification_profile_revision_id": {
          "$ref": "#/$defs/id"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/id"
        },
        "revision_number": {
          "type": "integer",
          "minimum": 1
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/id"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/id"
        },
        "created_at_utc": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
        },
        "compatible_item_types": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_itemTypes"
        },
        "normalized_revision_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/template"
          }
        }
      },
      "additionalProperties": false
    },
    "archetype": {
      "type": "object",
      "required": [
        "owner_kind",
        "owner_subject_id",
        "owner_group_id",
        "status",
        "created_by_subject_id",
        "created_by_command_id",
        "created_at_utc",
        "retired_by_subject_id",
        "retired_by_command_id",
        "retired_at_utc",
        "item_archetype_id",
        "archetype_key",
        "current_revision_id",
        "retirement_reason",
        "revision"
      ],
      "properties": {
        "owner_kind": {
          "enum": [
            "system",
            "subject",
            "subject_group"
          ]
        },
        "owner_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "owner_group_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/id"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/id"
        },
        "created_at_utc": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
        },
        "retired_by_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_by_command_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_at_utc": {
          "oneOf": [
            {
              "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
            },
            {
              "type": "null"
            }
          ]
        },
        "item_archetype_id": {
          "$ref": "#/$defs/id"
        },
        "archetype_key": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_key"
        },
        "current_revision_id": {
          "$ref": "#/$defs/id"
        },
        "retirement_reason": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1
            },
            {
              "type": "null"
            }
          ]
        },
        "revision": {
          "$ref": "#/$defs/archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "profile": {
      "type": "object",
      "required": [
        "owner_kind",
        "owner_subject_id",
        "owner_group_id",
        "status",
        "created_by_subject_id",
        "created_by_command_id",
        "created_at_utc",
        "retired_by_subject_id",
        "retired_by_command_id",
        "retired_at_utc",
        "notification_profile_id",
        "profile_key",
        "display_name",
        "description",
        "current_revision_id",
        "retirement_reason",
        "revision"
      ],
      "properties": {
        "owner_kind": {
          "enum": [
            "system",
            "subject",
            "subject_group"
          ]
        },
        "owner_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "owner_group_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/id"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/id"
        },
        "created_at_utc": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
        },
        "retired_by_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_by_command_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_at_utc": {
          "oneOf": [
            {
              "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
            },
            {
              "type": "null"
            }
          ]
        },
        "notification_profile_id": {
          "$ref": "#/$defs/id"
        },
        "profile_key": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_key"
        },
        "display_name": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/display_name"
        },
        "description": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/description"
        },
        "current_revision_id": {
          "$ref": "#/$defs/id"
        },
        "retirement_reason": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1
            },
            {
              "type": "null"
            }
          ]
        },
        "revision": {
          "$ref": "#/$defs/profileRevision"
        }
      },
      "additionalProperties": false
    },
    "binding": {
      "type": "object",
      "required": [
        "owner_kind",
        "owner_subject_id",
        "owner_group_id",
        "status",
        "created_by_subject_id",
        "created_by_command_id",
        "created_at_utc",
        "retired_by_subject_id",
        "retired_by_command_id",
        "retired_at_utc",
        "notification_profile_binding_id",
        "item_archetype_id",
        "notification_profile_id"
      ],
      "properties": {
        "owner_kind": {
          "enum": [
            "system",
            "subject",
            "subject_group"
          ]
        },
        "owner_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "owner_group_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/id"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/id"
        },
        "created_at_utc": {
          "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
        },
        "retired_by_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_by_command_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/id"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_at_utc": {
          "oneOf": [
            {
              "$ref": "spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp"
            },
            {
              "type": "null"
            }
          ]
        },
        "notification_profile_binding_id": {
          "$ref": "#/$defs/id"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/id"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/id"
        }
      },
      "additionalProperties": false
    },
    "archetypesPage": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "entries",
        "count",
        "catalog_snapshot_hash",
        "has_more",
        "next_cursor"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "item_archetype.list"
        },
        "response_contract": {
          "const": "spine.item-archetypes.v1"
        },
        "entries": {
          "type": "array",
          "maxItems": 500,
          "items": {
            "$ref": "#/$defs/archetype"
          }
        },
        "count": {
          "type": "string",
          "pattern": "^(0|[1-9][0-9]*)$"
        },
        "catalog_snapshot_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "archetypeShow": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "item_archetype"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "item_archetype.show"
        },
        "response_contract": {
          "const": "spine.item-archetypes.v1"
        },
        "item_archetype": {
          "$ref": "#/$defs/archetype"
        }
      },
      "additionalProperties": false
    },
    "profilesPage": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "entries",
        "count",
        "catalog_snapshot_hash",
        "has_more",
        "next_cursor"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.list"
        },
        "response_contract": {
          "const": "spine.notification-profiles.v1"
        },
        "entries": {
          "type": "array",
          "maxItems": 500,
          "items": {
            "$ref": "#/$defs/profile"
          }
        },
        "count": {
          "type": "string",
          "pattern": "^(0|[1-9][0-9]*)$"
        },
        "catalog_snapshot_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "profileShow": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "notification_profile"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.show"
        },
        "response_contract": {
          "const": "spine.notification-profiles.v1"
        },
        "notification_profile": {
          "$ref": "#/$defs/profile"
        }
      },
      "additionalProperties": false
    },
    "bindingsPage": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "entries",
        "count",
        "catalog_snapshot_hash",
        "has_more",
        "next_cursor"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "notification_profile.binding.list"
        },
        "response_contract": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "entries": {
          "type": "array",
          "maxItems": 500,
          "items": {
            "$ref": "#/$defs/binding"
          }
        },
        "count": {
          "type": "string",
          "pattern": "^(0|[1-9][0-9]*)$"
        },
        "catalog_snapshot_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "archetypesListRequest": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "limit"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "owner": {
          "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/owner"
        },
        "limit": {
          "type": "string",
          "pattern": "^(?:[1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)$"
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        }
      },
      "additionalProperties": false
    },
    "archetypesShowRequest": {
      "type": "object",
      "required": [
        "contract_version",
        "item_archetype_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.item-archetypes.v1"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/id"
        }
      },
      "additionalProperties": false
    },
    "profilesListRequest": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "limit"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "owner": {
          "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/owner"
        },
        "limit": {
          "type": "string",
          "pattern": "^(?:[1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)$"
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        }
      },
      "additionalProperties": false
    },
    "profilesShowRequest": {
      "type": "object",
      "required": [
        "contract_version",
        "notification_profile_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v1"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/id"
        }
      },
      "additionalProperties": false
    },
    "bindingsListRequest": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "limit",
        "status"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "owner": {
          "$ref": "spine-pack-installer-types.v1.schema.json#/$defs/owner"
        },
        "limit": {
          "type": "string",
          "pattern": "^(?:[1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)$"
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        },
        "status": {
          "const": "active"
        }
      },
      "additionalProperties": false
    },
    "commandFailure": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "error"
      ],
      "properties": {
        "ok": {
          "const": false
        },
        "command": {
          "type": "string",
          "minLength": 1
        },
        "error": {
          "type": "object",
          "required": [
            "code",
            "message"
          ],
          "properties": {
            "code": {
              "type": "string",
              "minLength": 1
            },
            "message": {
              "type": "string"
            },
            "field": {
              "oneOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 27: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_apply.py

Hash: 2693a7f96e2472ae2d6b3a706a5d3e0f86b41b9f1e84d83872e4798459b602e7

```markdown
"""Initial apply checkpoints before writes and never advances on invalid evidence."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest
import json
import tempfile
import contextlib
import io
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.apply import apply_initial, command_id, checkpoint_writer
from spine_packs.execution import materialize, validate_prefix, validate_artifact
from spine_packs.__main__ import main
from spine_packs.spine_command import SpineCommand
from spine_packs.planning import ENVIRONMENT, PlanError, plan_installation
from test_apply_preflight import approval
from test_planning import FakeSpine, manifest, request, catalog
import test_installer_artifact_contract as independent


class WritableFake(FakeSpine):
    def __init__(self, *, fail_at=None, malformed_at=None):
        super().__init__()
        self.writes = []
        self.fail_at = fail_at
        self.malformed_at = malformed_at

    def write(self, command, request_body):
        index = len(self.writes)
        self.writes.append((command, deepcopy(request_body)))
        if index == self.fail_at:
            raise PlanError("spine_command_rejection", "spine_write_rejected")
        receipt = {
            "command_receipt_id": f"receipt_{index}",
            "command_id": request_body["command_id"],
            "effect": {
                "item_archetype.create": "item_archetype_created",
                "notification_profile.create": "notification_profile_created",
                "notification_profile.binding.set": "notification_profile_binding_set",
            }[command],
            "semantic_facts_hash": a.digest(request_body),
            "created_at_utc": request_body["action_timestamp_utc"],
        }
        if command == "item_archetype.create":
            response = {"ok": True, "command": command, "response_contract": "spine.item-archetypes.v1",
                "effect": receipt["effect"], "item_archetype_id": "created_archetype",
                "item_archetype_revision_id": "created_archetype_revision", "revision_number": "1",
                "status": "active", "archetype_key": request_body["archetype_key"], "receipt": receipt}
        elif command == "notification_profile.create":
            response = {"ok": True, "command": command, "response_contract": "spine.notification-profiles.v1",
                "effect": receipt["effect"], "notification_profile_id": "created_profile",
                "notification_profile_revision_id": "created_profile_revision", "status": "active",
                "revision_number": "1", "normalized_revision_hash": "b" * 64,
                "profile_key": request_body["profile_key"], "receipt": receipt}
        else:
            response = {"ok": True, "command": command,
                "response_contract": "spine.notification-profile-bindings.v1", "effect": receipt["effect"],
                "notification_profile_binding_id": "created_binding",
                "item_archetype_id": request_body["item_archetype_id"],
                "notification_profile_id": request_body["notification_profile_id"],
                "status": "active", "compatible_item_types": ["event"], "receipt": receipt}
        if index == self.malformed_at:
            response["receipt"]["command_id"] = "wrong"
        return response


class InitialApplyTests(unittest.TestCase):
    def setup(self, transport=None):
        pack = manifest(released=True)
        transport = transport or WritableFake()
        plan = plan_installation(pack, request(), transport)
        return pack, plan, approval(plan), transport

    def test_command_identity_is_deterministic_and_bound(self):
        value = command_id("a" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000")
        self.assertRegex(value, r"^spack_[0-9a-f]{64}$")
        self.assertEqual(value, command_id("a" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000"))
        self.assertNotEqual(value, command_id("b" * 64, "123e4567-e89b-42d3-a456-426614174000", "action-000000"))

    def test_initial_apply_checkpoints_before_every_write_and_materializes_ids(self):
        pack, plan, approved, transport = self.setup()
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, lambda value: checkpoints.append(value))
        self.assertEqual(result["state"], "applied")
        self.assertEqual(len(result["accepted_responses"]), 3)
        self.assertEqual(len(checkpoints), 6)
        for index, (_, body) in enumerate(transport.writes):
            prepared = checkpoints[index * 2]
            self.assertEqual(prepared["unresolved_submission"]["request"]["canonical_json"], a.canonical_text(body))
            self.assertEqual(prepared["unresolved_submission"]["command_id"], body["command_id"])
            self.assertEqual(a.validate_schema(prepared), [])
            self.assertEqual(a.content_digest_errors(prepared), [])
        binding = transport.writes[-1][1]
        self.assertEqual(binding["item_archetype_id"], "created_archetype")
        self.assertEqual(binding["notification_profile_id"], "created_profile")
        self.assertIsNone(checkpoints[-1]["next_action_id"])
        self.assertEqual(a.validate_schema(result), [])
        self.assertEqual(a.content_digest_errors(result), [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
        for checkpoint in checkpoints:
            self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])

    def test_rejection_stops_at_first_action_and_preserves_unresolved_checkpoint(self):
        transport = WritableFake(fail_at=1)
        pack, plan, approved, transport = self.setup(transport)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "partial")
        self.assertEqual([x["action_id"] for x in result["accepted_responses"]], ["action-000000"])
        self.assertEqual(result["failure"]["action_id"], "action-000001")
        self.assertEqual(result["unattempted_action_ids"], ["action-000002"])
        self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], "action-000001")
        self.assertEqual(len(transport.writes), 2)

    def test_invalid_response_never_advances_checkpoint(self):
        transport = WritableFake(malformed_at=0)
        pack, plan, approved, transport = self.setup(transport)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["accepted_responses"], [])
        self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], "action-000000")

    def test_checkpoint_failure_happens_before_transport(self):
        pack, plan, approved, transport = self.setup()
        def fail(_value):
            raise OSError("synthetic checkpoint failure")
        with self.assertRaises(OSError):
            apply_initial(pack, plan, approved, transport, fail)
        self.assertEqual(transport.writes, [])

    def test_rejects_wrong_key_timestamp_hash_and_binding_ids(self):
        mutations = [
            (0, lambda r: r.update(archetype_key="wrong_key")),
            (1, lambda r: r.update(profile_key="wrong_key")),
            (0, lambda r: r["receipt"].update(created_at_utc="2000-01-01T00:00:00Z")),
            (0, lambda r: r["receipt"].update(semantic_facts_hash="0" * 64)),
            (2, lambda r: r.update(item_archetype_id="wrong_root")),
            (2, lambda r: r.update(notification_profile_id="wrong_profile")),
            (0, lambda r: r.update(revision_number="2")),
            (0, lambda r: r.update(item_archetype_id="${not_an_id}")),
            (0, lambda r: r.update(revision_number=1)),
            (0, lambda r: r.update(response_contract="wrong")),
            (0, lambda r: r["receipt"].update(effect="wrong")),
            (0, lambda r: r.update(extra="not_allowed")),
        ]
        for index, mutate in mutations:
            with self.subTest(index=index, mutate=mutate):
                class Corrupt(WritableFake):
                    def write(self, command, body):
                        value = super().write(command, body)
                        if len(self.writes) - 1 == index: mutate(value)
                        return value
                pack, plan, approved, transport = self.setup(Corrupt())
                checkpoints = []
                result = apply_initial(pack, plan, approved, transport, checkpoints.append)
                self.assertEqual(result["state"], "partial")
                self.assertEqual(len(result["accepted_responses"]), index)
                self.assertEqual(len(transport.writes), index + 1)
                self.assertEqual(checkpoints[-1]["unresolved_submission"]["action_id"], f"action-{index:06d}")
                self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_first_rejection_is_partial_with_empty_accepted_prefix(self):
        pack, plan, approved, transport = self.setup(WritableFake(fail_at=0))
        result = apply_initial(pack, plan, approved, transport, lambda value: None)
        self.assertEqual(result["state"], "partial")
        self.assertEqual(result["accepted_responses"], [])
        self.assertEqual(result["unattempted_action_ids"], ["action-000001", "action-000002"])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_binding_recheck_stops_changed_state_before_binding_write(self):
        pack, plan, approved, transport = self.setup()
        checkpoints = []
        def save(value):
            checkpoints.append(value)
            if len(value["accepted_responses"]) == 2:
                binding = catalog(pack)["bindings"][0]
                binding["item_archetype_id"] = "created_archetype"
                binding["notification_profile_id"] = "unexpected_profile"
                transport.entries["bindings"] = [binding]
        result = apply_initial(pack, plan, approved, transport, save)
        self.assertEqual(len(transport.writes), 2)
        self.assertEqual(result["failure"]["error"]["code"], "binding_precondition_changed")
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_stale_preflight_has_not_applied_artifact_without_checkpoint(self):
        pack, plan, approved, transport = self.setup()
        transport.entries = catalog(pack)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "not_applied")
        self.assertEqual(result["failure"]["error"]["category"], "stale_plan_or_target_mismatch")
        self.assertEqual(result["unattempted_action_ids"], [x["action_id"] for x in plan["actions"]])
        self.assertEqual(checkpoints, [])
        self.assertEqual(transport.writes, [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_no_write_plan_completes_with_empty_evidence(self):
        pack = manifest(released=True)
        transport = WritableFake()
        transport.entries = catalog(pack)
        plan = plan_installation(pack, request(), transport)
        approved = approval(plan)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "applied")
        self.assertEqual(len(checkpoints), 1)
        self.assertEqual(transport.writes, [])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])

    def test_every_checkpoint_boundary_failure_stops_execution(self):
        for boundary in range(6):
            with self.subTest(boundary=boundary):
                pack, plan, approved, transport = self.setup()
                durable = []
                def write(value):
                    if len(durable) == boundary:
                        raise OSError("simulated disk failure")
                    durable.append(deepcopy(value))
                with self.assertRaises(OSError):
                    apply_initial(pack, plan, approved, transport, write)
                self.assertEqual(len(transport.writes), (boundary + 1) // 2)
                for checkpoint in durable:
                    self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])

    def test_crash_at_each_submission_leaves_prepared_checkpoint(self):
        for boundary in range(3):
            with self.subTest(boundary=boundary):
                class Crash(WritableFake):
                    def write(self, command, body):
                        value = super().write(command, body)
                        if len(self.writes) == boundary + 1: raise KeyboardInterrupt()
                        return value
                pack, plan, approved, transport = self.setup(Crash())
                durable = []
                with self.assertRaises(KeyboardInterrupt):
                    apply_initial(pack, plan, approved, transport, durable.append)
                self.assertEqual(durable[-1]["next_action_id"], f"action-{boundary:06d}")
                self.assertIsNotNone(durable[-1]["unresolved_submission"])
                self.assertEqual(independent.checkpoint_errors(durable[-1], plan, approved), [])

    def test_materialization_rejects_tampered_or_gapped_prefix(self):
        pack, plan, approved, transport = self.setup()
        result = apply_initial(pack, plan, approved, transport, lambda value: None)
        responses = result["accepted_responses"][:2]
        bad_prefixes = [responses[:1], list(reversed(responses))]
        tampered = deepcopy(responses)
        tampered[0]["generated_ids"][0]["value"] = "untrusted"
        bad_prefixes.append(tampered)
        for prefix in bad_prefixes:
            with self.assertRaises(PlanError):
                materialize(plan, approved, 2, prefix)
        valid = materialize(plan, approved, 2, responses)
        self.assertEqual(valid, transport.writes[2][1])

    def test_metadata_and_revision_updates_and_binding_replacement(self):
        class DriftFake(WritableFake):
            def write(self, command, body):
                if command == "notification_profile.binding.set":
                    return super().write(command, body)
                self.writes.append((command, deepcopy(body)))
                if command == "notification_profile.metadata.update":
                    effect = "notification_profile_metadata_updated"
                    facts = {"notification_profile_id": body["notification_profile_id"],
                             "notification_profile_revision_id": "unchanged_revision", **body["metadata"]}
                else:
                    kind = command.removesuffix(".revise")
                    effect = kind + "_revised"
                    facts = {kind + "_id": body[kind + "_id"], kind + "_revision_id": "new_revision",
                             "revision_number": "2"}
                    if kind == "notification_profile": facts["normalized_revision_hash"] = "b" * 64
                contract = a.COMMAND_SHAPES[command][1]
                return {"ok": True, "command": command, "response_contract": contract, "effect": effect,
                        "status": "active", **facts, "receipt": {
                            "command_id": body["command_id"], "command_receipt_id": "drift_receipt_" + str(len(self.writes)),
                            "effect": effect, "created_at_utc": body["action_timestamp_utc"],
                            "semantic_facts_hash": a.digest(body)}}
        pack = manifest("medical_and_lesson", released=True)
        entries = catalog(pack)
        entries["archetypes"][0]["revision"]["description"] = "Old"
        entries["profiles"][0]["display_name"] = "Old"
        entries["profiles"][0]["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "1"
        entries["bindings"][0]["notification_profile_id"] = entries["profiles"][1]["notification_profile_id"]
        transport = DriftFake()
        transport.entries = entries
        plan = plan_installation(pack, request(), transport)
        approved = approval(plan)
        checkpoints = []
        result = apply_initial(pack, plan, approved, transport, checkpoints.append)
        self.assertEqual(result["state"], "applied")
        self.assertEqual([x[0] for x in transport.writes], ["item_archetype.revise", "notification_profile.metadata.update",
                                                         "notification_profile.revise", "notification_profile.binding.set"])
        self.assertEqual(independent.apply_result_errors(result, plan, approved), [])
        for checkpoint in checkpoints:
            self.assertEqual(independent.checkpoint_errors(checkpoint, plan, approved), [])


class DurableCheckpointTests(unittest.TestCase):
    def checkpoints(self):
        case = InitialApplyTests()
        pack, plan, approved, transport = case.setup()
        values = []
        apply_initial(pack, plan, approved, transport, values.append)
        return values

    def test_private_atomic_replacement_and_existing_file_refusal(self):
        values = self.checkpoints()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            writer = checkpoint_writer(path)
            for value in values:
                writer(value)
                self.assertEqual(a.load_json(path), value)
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            before = path.read_bytes()
            with self.assertRaises(PlanError): checkpoint_writer(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).glob(".spine-checkpoint-*")), [])

    def test_no_clobber_on_first_publication_race(self):
        value = self.checkpoints()[0]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            writer = checkpoint_writer(path)
            path.write_bytes(b"unrelated")
            with self.assertRaises(PlanError): writer(value)
            self.assertEqual(path.read_bytes(), b"unrelated")

    def test_replacement_detects_external_change_and_symlink(self):
        values = self.checkpoints()
        for symlink in (False, True):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "checkpoint.json"
                writer = checkpoint_writer(path)
                writer(values[0])
                if symlink:
                    path.unlink()
                    other = Path(directory) / "other"
                    other.write_bytes(b"preserve")
                    path.symlink_to(other)
                else: path.write_bytes(b"preserve")
                with self.assertRaises(PlanError): writer(values[1])
                self.assertEqual(path.read_bytes(), b"preserve")

    def test_fsync_and_replace_failures_leave_valid_evidence_and_clean_temps(self):
        values = self.checkpoints()
        for phase in ("file_fsync", "replace", "directory_fsync"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "checkpoint.json"
                writer = checkpoint_writer(path)
                writer(values[0])
                target = "spine_packs.apply.os.replace" if phase == "replace" else "spine_packs.apply.os.fsync"
                effect = [None, OSError("disk failure")] if phase == "directory_fsync" else OSError("disk failure")
                with patch(target, side_effect=effect), self.assertRaises(PlanError): writer(values[1])
                self.assertEqual(a.load_json(path), values[1] if phase == "directory_fsync" else values[0])
                self.assertEqual(list(Path(directory).glob(".spine-checkpoint-*")), [])

    def test_byte_limits_fail_before_publication(self):
        value = self.checkpoints()[0]
        key = value["artifact_schema"]
        size = len(a.canonical_text(value).encode())
        with patch.dict(a.SIZE_LIMITS, {key: size}): validate_artifact(value)
        with tempfile.TemporaryDirectory() as directory, patch.dict(a.SIZE_LIMITS, {key: size - 1}):
            path = Path(directory) / "checkpoint.json"
            with self.assertRaises(PlanError): checkpoint_writer(path)(value)
            self.assertFalse(path.exists())


class ApplyCliTests(unittest.TestCase):
    def invoke(self, directory, transport=None, **changes):
        pack, plan, approved, fake = InitialApplyTests().setup()
        directory = Path(directory)
        paths = {k: directory / (k + ".json") for k in ("manifest", "plan", "approval", "checkpoint", "output")}
        for key, value in (("manifest", pack), ("plan", plan), ("approval", approved)):
            paths[key].write_text(a.canonical_text(value), encoding="utf-8")
        paths.update(changes)
        args = ["apply"]
        for key, value in paths.items(): args.extend(["--" + key, str(value)])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(args, transport_factory=lambda target: transport or fake)
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        envelope = json.loads(output.getvalue())
        self.assertEqual(envelope["operation"], "apply")
        self.assertEqual(independent.envelope_errors(envelope), [])
        return code, envelope, paths, fake

    def test_success_and_partial_cli_artifacts(self):
        for transport, expected in ((WritableFake(), 0), (WritableFake(fail_at=0), 9)):
            with tempfile.TemporaryDirectory() as directory:
                code, envelope, paths, _ = self.invoke(directory, transport)
                self.assertEqual(code, expected)
                result = a.load_json(paths["output"])
                self.assertEqual(independent.apply_result_errors(result, a.load_json(paths["plan"]), a.load_json(paths["approval"])), [])
                self.assertEqual(envelope["artifact"]["digest"], result["content_identity"]["digest"])

    def test_stale_plan_exit_and_no_checkpoint(self):
        transport = WritableFake()
        transport.entries = catalog(manifest(released=True))
        with tempfile.TemporaryDirectory() as directory:
            code, envelope, paths, _ = self.invoke(directory, transport)
            self.assertEqual(code, 7)
            self.assertEqual(a.load_json(paths["output"])["state"], "not_applied")
            self.assertFalse(paths["checkpoint"].exists())

    def test_checkpoint_input_and_output_collisions_fail_before_transport(self):
        for name in ("manifest", "plan", "approval", "output"):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / (name + ".json")
                code, _, _, transport = self.invoke(directory, checkpoint=path)
                self.assertEqual(code, 2)
                self.assertEqual(transport.writes, [])

    def test_public_write_allowlist_and_invalid_rejections(self):
        transport = SpineCommand({})
        with patch.object(transport, "_invoke") as invoke:
            for command in ("notification_profile.retire", "item.create", "system.info"):
                with self.assertRaises(PlanError): transport.write(command, {})
            invoke.assert_not_called()
        pack, plan, approved, _ = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        invalid = {"ok": False, "command": "item_archetype.create"}
        with patch.object(transport, "_invoke", return_value=(invalid, 3)), self.assertRaises(PlanError) as caught:
            transport.write("item_archetype.create", body)
        self.assertEqual(caught.exception.category, ENVIRONMENT)

    def test_write_rejection_preserves_only_bounded_machine_code(self):
        _, plan, approved, _ = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        response = {"ok": False, "command": "item_archetype.create", "error": {
            "code": "semantic_conflict:archetype_key", "message": "private unrelated text", "field": None}}
        transport = SpineCommand({})
        with patch.object(transport, "_invoke", return_value=(response, 3)), self.assertRaises(PlanError) as caught:
            transport.write("item_archetype.create", body)
        self.assertEqual(caught.exception.facts, [{"name": "spine_error_code", "value": "semantic_conflict:archetype_key"}])
        self.assertNotIn("private", str(caught.exception))

    def test_real_fake_process_receives_exact_write_request(self):
        _, plan, approved, fake = InitialApplyTests().setup()
        body = materialize(plan, approved, 0, [])
        response = fake.write("item_archetype.create", body)
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "fake-spine-command"
            executable.write_text("#!" + sys.executable + "\nimport json,sys\n"
                + "assert sys.argv[1:]==['--db','/not/a/real/ledger','item_archetype.create','--input','-']\n"
                + "assert json.load(sys.stdin)==" + repr(body) + "\n"
                + "print(" + repr(a.canonical_text(response)) + ")\n", encoding="utf-8")
            executable.chmod(0o700)
            transport = SpineCommand({"spine_command": {"path": str(executable)},
                                      "ledger": {"path": "/not/a/real/ledger"}})
            with patch.object(transport, "check_target"):
                self.assertEqual(transport.write("item_archetype.create", body), response)

    def test_result_publication_failure_retains_completed_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory, patch("spine_packs.__main__.publish", side_effect=OSError("disk full")):
            code, envelope, paths, transport = self.invoke(directory)
            self.assertEqual(code, 11)
            self.assertIsNone(envelope["artifact"])
            self.assertEqual(len(transport.writes), 3)
            checkpoint = a.load_json(paths["checkpoint"])
            self.assertIsNone(checkpoint["next_action_id"])
            self.assertEqual(len(checkpoint["accepted_responses"]), 3)

    def test_existing_checkpoint_is_not_a_resume_request(self):
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            checkpoint.write_text("preserve", encoding="utf-8")
            code, _, _, transport = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(transport.writes, [])
            self.assertEqual(checkpoint.read_text(), "preserve")


if __name__ == "__main__":
    unittest.main()
```

### Spec 28: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_apply_preflight.py

Hash: a1d447574b752a9c6577da7542ea0733db2e9e657ed0399a95e2153448d9dab1

```markdown
"""Apply preflight is fresh, deterministic, and incapable of Spine writes."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.planning import PlanError, plan_installation
from spine_packs.preflight import preflight_apply
from test_planning import FakeSpine, catalog, manifest, request


def approval(plan):
    return a.seal({
        "artifact_schema": "spine.pack-install-approval.v1",
        "plan_digest": plan["content_identity"]["digest"],
        "approve_complete_plan": True,
        "acknowledge_single_operator": True,
        "authorized_update_action_ids": plan["decision_action_ids"],
        "execution": {
            "execution_id": "123e4567-e89b-42d3-a456-426614174000",
            "actor_subject_id": "subject_operator",
            "action_timestamp_utc": "2026-09-12T10:00:00Z",
        },
    })


class ApplyPreflightTests(unittest.TestCase):
    def released_missing(self):
        pack = manifest(released=True)
        plan = plan_installation(pack, request(), FakeSpine())
        self.assertTrue(plan["apply_eligible"])
        return pack, plan

    def assert_failure(self, code, pack, plan, approved, transport=None):
        with self.assertRaises(PlanError) as caught:
            preflight_apply(pack, plan, approved, transport or FakeSpine())
        self.assertEqual(caught.exception.code, code)

    def test_success_reobserves_plan_and_returns_execution_facts(self):
        pack, plan = self.released_missing()
        approved = approval(plan)
        transport = FakeSpine()
        result = preflight_apply(pack, plan, approved, transport)
        self.assertEqual(result["plan_digest"], plan["content_identity"]["digest"])
        self.assertEqual(result["approval_digest"], approved["content_identity"]["digest"])
        self.assertEqual(result["action_ids"], [x["action_id"] for x in plan["actions"]])
        self.assertTrue(transport.calls)
        self.assertTrue(all(command in {
            "system.info", "item_archetype.list", "item_archetype.show",
            "notification_profile.list", "notification_profile.show",
            "notification_profile.binding.list",
        } for command, _ in transport.calls))

    def test_draft_plan_stops_before_transport(self):
        pack = manifest()
        plan = plan_installation(pack, request(), FakeSpine())
        transport = FakeSpine()
        self.assert_failure("draft_plan_not_applicable", pack, plan, approval(plan), transport)
        self.assertEqual(transport.calls, [])

    def test_wrong_plan_or_incomplete_update_approval_is_rejected(self):
        pack, plan = self.released_missing()
        approved = approval(plan)
        approved["plan_digest"] = "f" * 64
        self.assert_failure("invalid_or_incomplete_approval", pack, plan, a.seal(approved))

        entries = catalog(pack)
        entries["profiles"][0]["display_name"] = "Old name"
        drift_plan = plan_installation(pack, request(), FakeSpine(entries))
        incomplete = approval(drift_plan)
        incomplete["authorized_update_action_ids"] = []
        self.assert_failure(
            "invalid_or_incomplete_approval", pack, drift_plan, a.seal(incomplete)
        )

    def test_manifest_or_catalog_change_is_stale(self):
        pack, plan = self.released_missing()
        changed_pack = manifest("medical_and_lesson", released=True)
        self.assert_failure("manifest_identity_mismatch", changed_pack, plan, approval(plan))

        self.assert_failure("stale_plan", pack, plan, approval(plan), FakeSpine(catalog(pack)))

    def test_invalid_plan_stops_before_transport(self):
        pack, plan = self.released_missing()
        invalid = deepcopy(plan)
        invalid["actions"][0]["command"] = "notification_profile.binding.set"
        transport = FakeSpine()
        self.assert_failure("invalid_plan", pack, invalid, approval(plan), transport)
        self.assertEqual(transport.calls, [])


if __name__ == "__main__":
    unittest.main()
```

### Spec 29: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_planning.py

Hash: fa55f80941150f704a9bc3f9ef3faab061ddb602c1f4487539b4b502a980d0ac

```markdown
"""Planner tests use synthetic public responses; never a live Spine ledger."""
from copy import deepcopy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/contract"))
import test_installer_artifact_contract as independent
import test_pack_manifest_contract as pack_contract
from spine_packs import artifacts as a, manifest as m, planning as p
from spine_packs.__main__ import main, publish
from spine_packs.spine_command import SpineCommand, READ_COMMANDS


def manifest(name="medical_vertical_slice", released=False):
    value = a.load_json(ROOT / f"tests/fixtures/pack-manifest/positive/{name}.json")
    if released:
        value["pack"].update(status="released", version="1.0.0")
        value["content_identity"]["digest"] = m.content_digest(value)
    return value


def request(selection=None):
    value = a.load_json(ROOT / "tests/fixtures/installer/positive/granular_request.json")
    value["request"]["selection"] = selection or {"mode": "all"}
    value["request"]["draft_posture"] = "inspect_only"
    return a.seal(value)


def info():
    return {"ok": True, "command": "system.info", "response_contract": "spine.system-info.v2",
            "runtime_version": "0.3.0", "implemented_ledger_schema_version": "12",
            "ledger_schema_version": "12", "timezone_database_version": "2026a",
            "implemented_contract_versions": a.REQUIRED_EXECUTION_CONTRACTS[:],
            "runtime_dependencies": [{"name": "tickerd", "package_version": "0.2.0",
                "capability_id": "tickerd.runtime-capabilities.v1",
                "descriptor_sha256": "215f9aa6b54e6c0e6186796a55d78e1c5a270adc9b3ccefb433df5a3bb87b58b",
                "compatibility_contract": "spine.tickerd-compatibility.v1", "status": "compatible"}]}


def catalog(pack, owner=None):
    owner = owner or request()["request"]["owner"]
    audit = {"created_by_subject_id": "actor_test", "created_by_command_id": "command_test",
             "created_at_utc": "2026-08-01T00:00:00Z"}
    common = {**owner, **audit, "owner_subject_id": owner.get("owner_subject_id"),
              "owner_group_id": owner.get("owner_group_id"), "status": "active",
              "retired_by_subject_id": None, "retired_by_command_id": None, "retired_at_utc": None}
    result = {k: [] for k in p.CATALOGS}
    for name, definitions, prefix, key_field in (
        ("archetypes", pack["archetypes"], "item_archetype", "archetype_key"),
        ("profiles", pack["notification_profiles"], "notification_profile", "profile_key"),
    ):
        for definition in definitions:
            key = definition[key_field]
            root_id, revision_id = prefix + "_" + key, prefix + "_revision_" + key
            revision = {**deepcopy(definition["revision"]), **audit, prefix + "_id": root_id,
                        prefix + "_revision_id": revision_id, "revision_number": 1}
            revision["normalized_content_hash" if name == "archetypes" else "normalized_revision_hash"] = "a" * 64
            if name == "profiles":
                for index, template in enumerate(revision["templates"]):
                    template.update(notification_profile_template_id=revision_id + str(index),
                                    notification_profile_revision_id=revision_id, template_index=index,
                                    normalized_template_hash="b" * 64)
            entry = {**common, prefix + "_id": root_id, key_field: key, "current_revision_id": revision_id,
                     "retirement_reason": None, "revision": revision}
            if name == "profiles":
                entry.update(display_name=definition["display_name"], description=definition["description"])
            result[name].append(entry)
    for binding in pack["binding_intents"]:
        result["bindings"].append({**common,
            "notification_profile_binding_id": "binding_" + binding["archetype_key"],
            "item_archetype_id": "item_archetype_" + binding["archetype_key"],
            "notification_profile_id": "notification_profile_" + binding["notification_profile_key"]})
    return result


class FakeSpine:
    def __init__(self, entries=None, mutate=None):
        self.entries = deepcopy(entries or {k: [] for k in p.CATALOGS})
        self.mutate = mutate
        self.calls = []
        self.checks = 0
        self.info = info()

    def check_target(self):
        self.checks += 1

    def read(self, command, query):
        assert command in READ_COMMANDS, command
        self.calls.append((command, deepcopy(query)))
        if command == "system.info":
            response = deepcopy(self.info)
        else:
            name = next(k for k, v in p.CATALOGS.items() if command in (v[0] + ".list", v[0] + ".show"))
            p.validate_readback(query, name + ("ListRequest" if command.endswith(".list") else "ShowRequest"))
            prefix, key_field, id_field, _ = p.CATALOGS[name]
            response = {"ok": True, "command": command, "response_contract": p.FAMILIES[name]}
            entries = sorted(self.entries[name], key=lambda e: (e[key_field], e[id_field]))
            if command.endswith(".show"):
                response[prefix] = deepcopy(next(e for e in entries if e[id_field] == query[id_field]))
            else:
                start, limit = int(query.get("cursor", "0")), int(query["limit"])
                page = entries[start:start + limit]
                more = start + limit < len(entries)
                response.update(entries=deepcopy(page), count=str(len(page)), has_more=more,
                                next_cursor=str(start + limit) if more else None,
                                catalog_snapshot_hash=hashlib.sha256(name.encode()).hexdigest())
        if self.mutate:
            self.mutate(command, query, response, self.calls)
        return response


class PlanningTests(unittest.TestCase):
    def plan(self, pack=None, req=None, transport=None, **kwargs):
        plan = p.plan_installation(pack or manifest(), req or request(), transport or FakeSpine(), **kwargs)
        self.assertEqual(independent.plan_errors(plan), [])
        self.assertEqual(independent.artifact_size_errors(plan), [])
        return plan

    def fails(self, transport, code, pack=None, req=None, **kwargs):
        with self.assertRaises(p.PlanError) as caught:
            self.plan(pack, req, transport, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_missing_plan_create_order_and_future_binding_references(self):
        plan = self.plan()
        self.assertEqual([x["command"] for x in plan["actions"]],
                         ["item_archetype.create", "notification_profile.create", "notification_profile.binding.set"])
        body = json.loads(plan["actions"][-1]["request_template"]["canonical_json"])
        self.assertEqual(body["item_archetype_id"], "${spine-pack.result:action-000000:item_archetype_id}")
        self.assertEqual(body["notification_profile_id"], "${spine-pack.result:action-000001:notification_profile_id}")
        self.assertFalse(plan["apply_eligible"])

    def test_equivalent_keeps_definitions_and_no_write_actions(self):
        pack = manifest(released=True)
        transport = FakeSpine(catalog(pack))
        before = deepcopy(transport.entries)
        plan = self.plan(pack, transport=transport)
        self.assertEqual(plan["actions"], [])
        self.assertTrue(plan["apply_eligible"])
        self.assertEqual(transport.entries, before)
        self.assertEqual({x["classification"] for x in plan["classifications"]}, {"equivalent"})

    def test_profile_metadata_revision_and_both_drift(self):
        pack = manifest(released=True)
        for metadata, revision in ((True, False), (False, True), (True, True)):
            with self.subTest(metadata=metadata, revision=revision):
                entries = catalog(pack)
                profile = entries["profiles"][0]
                if metadata:
                    profile["display_name"] = "Old name"
                if revision:
                    profile["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "1"
                plan = self.plan(pack, transport=FakeSpine(entries))
                expected = (["notification_profile.metadata.update"] if metadata else []) + (["notification_profile.revise"] if revision else [])
                self.assertEqual([a["command"] for a in plan["actions"]], expected)
                self.assertTrue(plan["apply_eligible"])
                self.assertEqual(p.plan_outcome(plan), "decision_required_for_drift")
                for action in plan["actions"]:
                    self.assertEqual(action["expected"], plan["classifications"][1]["observed"])

    def test_archetype_revision_and_binding_drift(self):
        pack = manifest("medical_and_lesson", released=True)
        entries = catalog(pack)
        entries["archetypes"][0]["revision"]["description"] = "Earlier description"
        entries["bindings"][0]["notification_profile_id"] = entries["profiles"][1]["notification_profile_id"]
        plan = self.plan(pack, transport=FakeSpine(entries))
        self.assertEqual([a["command"] for a in plan["actions"]], ["item_archetype.revise", "notification_profile.binding.set"])

    def test_approved_outcome_precedence(self):
        for draft in (True, False):
            for blocked in (True, False):
                for drift in (True, False):
                    with self.subTest(draft=draft, blocked=blocked, drift=drift):
                        pack = manifest(released=not draft)
                        entries = catalog(pack)
                        if drift:
                            entries["profiles"][0]["display_name"] = "Old"
                        if blocked:
                            root = entries["archetypes"][0]
                            root.update(status="retired", retirement_reason="Retired",
                                        retired_by_subject_id="actor", retired_by_command_id="cmd",
                                        retired_at_utc="2026-08-02T00:00:00Z")
                        plan = self.plan(pack, transport=FakeSpine(entries))
                        self.assertEqual(plan["apply_eligible"], not draft and not blocked)
                        expected = "blocked_desired_state" if blocked else "success" if draft or not drift else "decision_required_for_drift"
                        self.assertEqual(p.plan_outcome(plan), expected)

    def test_granular_closure_and_page_size_independent_digest(self):
        pack = manifest("medical_and_lesson")
        req = request({"mode": "archetypes", "archetype_keys": ["lesson"]})
        small = self.plan(pack, req, FakeSpine(catalog(pack)), page_size=1)
        large = self.plan(pack, req, FakeSpine(catalog(pack)), page_size=100)
        self.assertEqual(small, large)
        self.assertEqual(small["closure"], {"archetype_keys": ["lesson"], "profile_keys": ["lesson_standard"], "binding_archetype_keys": ["lesson"]})

    def test_latest_draft_all_content(self):
        plan = self.plan(manifest("kinflow_starter_draft_9"))
        self.assertEqual(len(plan["closure"]["archetype_keys"]), 52)
        self.assertEqual(len(plan["actions"]), 156)

    def test_shared_profile_unbound_archetype_and_orphan_profile_selection(self):
        pack = manifest("medical_and_lesson")
        pack["binding_intents"][0]["notification_profile_key"] = pack["binding_intents"][1]["notification_profile_key"]
        pack["content_identity"]["digest"] = m.content_digest(pack)
        req = request({"mode": "archetypes", "archetype_keys": ["lesson", "medical_appointment"]})
        self.assertEqual(len(self.plan(pack, req)["closure"]["profile_keys"]), 1)
        self.assertEqual(len(self.plan(pack)["closure"]["profile_keys"]), 2)
        pack["binding_intents"] = pack["binding_intents"][1:]
        pack["content_identity"]["digest"] = m.content_digest(pack)
        req = request({"mode": "archetypes", "archetype_keys": ["lesson"]})
        self.assertEqual(self.plan(pack, req)["closure"]["profile_keys"], [])

    def test_invalid_unselected_manifest_rejected_before_transport(self):
        pack = manifest("medical_and_lesson")
        pack["archetypes"][1]["owner"] = "forbidden"
        pack["content_identity"]["digest"] = m.content_digest(pack)
        transport = FakeSpine()
        self.fails(transport, "invalid_manifest", pack=pack,
                   req=request({"mode": "archetypes", "archetype_keys": ["lesson"]}))
        self.assertEqual(transport.calls, [])
        self.assertEqual(transport.checks, 0)

    def test_bad_digest_draft_rejection_and_unknown_selection_before_reads(self):
        bad = request()
        bad["content_identity"]["digest"] = "0" * 64
        reject = request()
        reject["request"]["draft_posture"] = "reject"
        cases = [(bad, "invalid_request"), (a.seal(reject), "draft_inspection_not_allowed"),
                 (request({"mode": "archetypes", "archetype_keys": ["missing"]}), "unknown_archetype_selection")]
        for req, code in cases:
            transport = FakeSpine()
            self.fails(transport, code, req=req)
            self.assertEqual(transport.calls, [])

    def test_incompatible_runtime_and_execution_contract_fail_before_catalog(self):
        for field, value in (("runtime_version", "0.4.0"), ("ledger_schema_version", "13"),
                             ("implemented_contract_versions", a.REQUIRED_EXECUTION_CONTRACTS[1:])):
            transport = FakeSpine()
            transport.info[field] = value
            self.fails(transport, "incompatible_runtime_or_contracts")
            self.assertEqual(len(transport.calls), 1)

    def test_owner_scope_group(self):
        req = request()
        req["request"]["owner"] = {"owner_kind": "subject_group", "owner_group_id": "family_test"}
        req = a.seal(req)
        pack = manifest()
        self.assertEqual(self.plan(pack, req, FakeSpine(catalog(pack, req["request"]["owner"])))["actions"], [])

    def test_malformed_or_unstable_readback_fails_closed(self):
        cases = [
            ("owner", "catalog_owner_mismatch"), ("count", "invalid_page_count"),
            ("contract", "invalid_public_response"), ("show", "catalog_show_changed"),
            ("snapshot", "catalog_changed"), ("cursor", "cursor_presence_invalid"),
            ("index", "readback_template_indices_invalid"), ("revision", "revision_identity_mismatch"),
        ]
        for defect, expected in cases:
            with self.subTest(defect=defect):
                def mutate(command, query, response, calls):
                    if defect == "show" and command.endswith(".show"):
                        response[command.removesuffix(".show")]["revision"]["description"] = "Changed"
                    if command == "item_archetype.list":
                        if defect == "owner": response["entries"][0]["owner_subject_id"] = "wrong"
                        if defect == "count": response["count"] = "2"
                        if defect == "contract": response["response_contract"] = "unknown"
                        if defect == "cursor": response["next_cursor"] = "bad"
                        if defect == "revision": response["entries"][0]["current_revision_id"] = "wrong"
                        if defect == "snapshot" and len(calls) > 5: response["catalog_snapshot_hash"] = "0" * 64
                    if defect == "index" and command == "notification_profile.list":
                        response["entries"][0]["revision"]["templates"][0]["template_index"] = 9
                self.fails(FakeSpine(catalog(manifest()), mutate), expected)

    def test_unresolvable_binding_blocks_not_missing(self):
        entries = catalog(manifest())
        entries["bindings"][0]["notification_profile_id"] = "unknown_root"
        plan = self.plan(transport=FakeSpine(entries))
        self.assertEqual(plan["blocked_object_keys"], ["binding:medical_appointment"])
        self.assertEqual(plan["actions"], [])

    def test_duplicate_and_repeated_pages_rejected(self):
        pack = manifest("medical_and_lesson")
        def mutate(command, query, response, calls):
            if command == "item_archetype.list" and "cursor" in query:
                response["entries"][0] = deepcopy(catalog(pack)["archetypes"][0])
        self.fails(FakeSpine(catalog(pack), mutate), "catalog_order_invalid", pack=pack, page_size=1)

    def test_empty_continuation_and_cursor_cycle_fail_closed(self):
        for empty, code in ((True, "cursor_cycle_or_empty_page"), (False, "cursor_cycle_or_empty_page")):
            def mutate(command, query, response, calls):
                if command == "item_archetype.list":
                    response.update(has_more=True, next_cursor="1")
                    if empty:
                        response.update(entries=[], count="0")
            pack = manifest("medical_and_lesson")
            self.fails(FakeSpine(catalog(pack), mutate), code, pack=pack, page_size=1)

    def test_changed_target_and_snapshot_never_yield_partial_plan(self):
        transport = FakeSpine()
        def changed_target():
            transport.checks += 1
            if transport.checks > 1:
                raise p.PlanError("stale_plan_or_target_mismatch", "target_binding_mismatch")
        transport.check_target = changed_target
        self.fails(transport, "target_binding_mismatch")

    def test_runtime_manifest_validator_matches_all_contract_vectors(self):
        schema = a.load_json(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")
        for path in (ROOT / "tests/fixtures/pack-manifest").rglob("*.json"):
            with self.subTest(path=path.name):
                try:
                    value = a.parse_json(path.read_bytes())
                except ValueError:
                    self.assertEqual(path.parent.name, "negative")
                    continue
                actual = m.validate_pack(value, schema)
                self.assertEqual(actual, pack_contract.validate_pack(value, schema))
                self.assertEqual(bool(actual), path.parent.name == "negative")

    def test_pinned_schema_vocabulary_is_supported(self):
        supported = {"$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
                     "type", "const", "enum", "properties", "required", "additionalProperties",
                     "minLength", "maxLength", "pattern", "items", "minItems", "maxItems", "uniqueItems",
                     "oneOf", "anyOf", "allOf", "not", "if", "then", "else", "contains", "minContains",
                     "maxContains", "minimum"}
        def inspect(schema):
            self.assertEqual(set(schema) - supported, set())
            for key in ("$defs", "properties"):
                for child in schema.get(key, {}).values(): inspect(child)
            for key in ("items", "not", "if", "then", "else", "contains"):
                if isinstance(schema.get(key), dict): inspect(schema[key])
            for key in ("oneOf", "anyOf", "allOf"):
                for child in schema.get(key, []): inspect(child)
        for path in a.SCHEMA_ROOT.glob("*.json"):
            with self.subTest(schema=path.name): inspect(a.load_json(path))

    def test_public_boolean_is_not_a_json_integer(self):
        response = info()
        response["ok"] = 1
        with self.assertRaises(p.PlanError):
            p.validate_readback(response, "systemInfo")


class CliAndAdapterTests(unittest.TestCase):
    def invoke(self, directory, *, pack=None, req=None, flags=(), transport=None):
        directory = Path(directory)
        (directory / "pack.json").write_text(a.canonical_text(pack or manifest()), encoding="utf-8")
        (directory / "request.json").write_text(a.canonical_text(req or request()), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["plan", "--manifest", str(directory / "pack.json"), "--request", str(directory / "request.json"),
                         "--output", str(directory / "plan.json"), *flags], transport_factory=lambda target: transport or FakeSpine())
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        result = json.loads(lines[0])
        self.assertEqual(independent.validate_schema(result), [])
        self.assertEqual(str(code), result["exit_code"])
        return code, result

    def test_cli_publishes_private_artifact_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory)
            self.assertEqual(code, 0)
            output = Path(directory) / "plan.json"
            before = output.read_bytes()
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(a.load_json(output)["content_identity"]["digest"], result["artifact"]["digest"])
            code, result = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(result["error"]["code"], "output_already_exists")
            self.assertEqual(output.read_bytes(), before)
            self.assertFalse(list(Path(directory).glob(".spine-plan-*")))

    def test_cli_drift_and_blocked_results_keep_reviewable_artifact(self):
        pack = manifest(released=True)
        entries = catalog(pack)
        entries["profiles"][0]["display_name"] = "Old"
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, pack=pack, transport=FakeSpine(entries))
            self.assertEqual(code, 5)
            self.assertIsNotNone(result["artifact"])
        entries["bindings"][0]["notification_profile_id"] = "missing"
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, pack=pack, transport=FakeSpine(entries))
            self.assertEqual(code, 6)
            self.assertIsNotNone(result["artifact"])

    def test_cli_assertion_failure_and_missing_input_no_transport(self):
        transport = FakeSpine()
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, flags=["--archetype", "lesson"], transport=transport)
            self.assertEqual(code, 2)
            self.assertEqual(transport.calls, [])
            self.assertFalse((Path(directory) / "plan.json").exists())

    def test_unimplemented_operations_are_not_cli_commands(self):
        for command in ("verify", "recover"):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([command]), 2)
            self.assertEqual(json.loads(output.getvalue())["error"]["code"], "invalid_cli_arguments")

    def test_publication_race_and_symlink_never_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "existing"
            existing.write_bytes(b"preserve")
            with self.assertRaises(p.PlanError):
                publish(existing, {})
            self.assertEqual(existing.read_bytes(), b"preserve")
            (Path(directory) / "plan.json").symlink_to(existing)
            code, _ = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(existing.read_bytes(), b"preserve")
            self.assertEqual(list(Path(directory).glob(".spine-plan-*")), [])

    def test_invalid_read_request_rejected_before_spawn(self):
        transport = SpineCommand({})
        with patch.object(transport, "check_target") as check, patch("subprocess.Popen") as spawn:
            for body in ({}, {"contract_version": p.FAMILIES["archetypes"], "owner": request()["request"]["owner"], "limit": "501"}):
                with self.assertRaises(p.PlanError):
                    transport.read("item_archetype.list", body)
            check.assert_not_called()
            spawn.assert_not_called()

    def test_strict_json_boundary(self):
        for raw in (b'{"x":1}', b'{"x":1.5}', b'{"x":NaN}', b'{"x":null,"x":true}',
                    b'\xef\xbb\xbf{}', b'{"x":"\\ud800"}', b'{} trailing'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                a.parse_json(raw)
        self.assertEqual(a.parse_json(b'{"revision_number":1}', public_response=True), {"revision_number": 1})
        with self.assertRaises(ValueError):
            a.parse_json(b'{"revision_number":1.5}', public_response=True)

    def test_adapter_rejects_write_before_target_or_spawn(self):
        transport = SpineCommand({})
        with patch.object(transport, "check_target") as check, patch("subprocess.Popen") as spawn:
            for command in a.COMMAND_SHAPES:
                with self.assertRaises(p.PlanError):
                    transport.read(command, {})
            check.assert_not_called()
            spawn.assert_not_called()

    def test_adapter_target_identity_without_opening_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            exe, ledger = Path(directory) / "fake-command", Path(directory) / "ledger"
            exe.write_bytes(b"#!/bin/sh\nexit 0\n")
            exe.chmod(0o700)
            ledger.write_bytes(b"not a database")
            target = {"host_name": "test.local", "spine_command": {"path": str(exe.resolve()),
                      "sha256": hashlib.sha256(exe.read_bytes()).hexdigest()},
                      "ledger": {"kind": "path", "path": str(ledger.resolve())}}
            transport = SpineCommand(target, host_resolver=lambda: "TEST.LOCAL.")
            original = Path.open
            def safe_open(path, *args, **kwargs):
                self.assertNotEqual(path, ledger.resolve(), "adapter must never open ledger")
                return original(path, *args, **kwargs)
            with patch.object(Path, "open", safe_open):
                transport.check_target()
            target["spine_command"]["sha256"] = "0" * 64
            with self.assertRaises(p.PlanError) as caught:
                transport.check_target()
            self.assertEqual(caught.exception.category, "stale_plan_or_target_mismatch")

    def test_real_subprocess_argv_stdin_and_bounded_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            exe = Path(directory) / "fake command"
            target = request()["request"]["target"]
            target["spine_command"]["path"] = str(exe)
            programs = [
                ("import json,sys\nassert sys.argv[1:]==['--db','/var/lib/spine/ledger.sqlite3','system.info','--input','-']\nassert sys.stdin.read()=='{}\\n'\nprint(json.dumps({'ok':True,'command':'system.info'}))\n", None),
                ("print('not json')\n", "spine_transport_failed"),
                ("import json\nprint(json.dumps({'ok':True,'command':'wrong'}))\n", "response_command_mismatch"),
                ("import json,sys\nprint(json.dumps({'ok':False,'command':'system.info','error':{'code':'invalid_request','message':'private detail','field':None}}))\nsys.exit(3)\n", "spine_read_rejected"),
                ("import time\ntime.sleep(2)\n", "spine_timeout"),
                ("print('x'*2048)\n", "spine_response_too_large"),
            ]
            for program, error in programs:
                with self.subTest(error=error):
                    exe.write_text("#!" + sys.executable + "\n" + program, encoding="utf-8")
                    exe.chmod(0o700)
                    transport = SpineCommand(target, timeout=0.5)
                    with patch.object(transport, "check_target"), patch("spine_packs.spine_command.RESPONSE_LIMIT", 1024):
                        if error:
                            with self.assertRaises(p.PlanError) as caught:
                                transport.read("system.info", {})
                            self.assertEqual(caught.exception.code, error)
                        else:
                            self.assertTrue(transport.read("system.info", {})["ok"])


if __name__ == "__main__":
    unittest.main()
```

### Spec 30: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_installer_artifact_contract.py

Hash: d5e6348e818bca1d5dd837f81e0290f40402b214060dc53b90966ec744110c53

```markdown
#!/usr/bin/env python3
"""Dependency-free contract checks for Spine pack installer artifacts."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts/schemas"
FIXTURE_MANIFEST = ROOT / "contracts/installer-fixture-manifest.v1.json"
POSITIVE_ROOT = ROOT / "tests/fixtures/installer/positive"
NEGATIVE_ROOT = ROOT / "tests/fixtures/installer/negative"
EMBEDDED_SCHEMA = SCHEMA_ROOT / "spine-pack-embedded-values.v1.schema.json"
COMMAND_SHAPES = {
    "item_archetype.create": ("archetypeCreate", "spine.item-archetypes.v1"),
    "item_archetype.revise": ("archetypeRevise", "spine.item-archetypes.v1"),
    "notification_profile.create": ("profileCreate", "spine.notification-profiles.v1"),
    "notification_profile.revise": ("profileRevise", "spine.notification-profiles.v1"),
    "notification_profile.metadata.update": (
        "profileMetadataUpdate", "spine.notification-profile-metadata-update.v1"
    ),
    "notification_profile.binding.set": ("bindingSet", "spine.notification-profile-bindings.v1"),
}
SEMANTIC_CONTRACTS = {
    "archetypeSemantics": "spine.item-archetypes.v1",
    "profileSemantics": "spine.notification-profiles.v1",
    "bindingSemantics": "spine.notification-profile-bindings.v1",
}

ENTRYPOINTS = {
    "spine.pack-install-request.v1": "spine-pack-install-request.v1.schema.json",
    "spine.pack-install-plan.v1": "spine-pack-install-plan.v1.schema.json",
    "spine.pack-install-approval.v1": "spine-pack-install-approval.v1.schema.json",
    "spine.pack-apply-checkpoint.v1": "spine-pack-apply-checkpoint.v1.schema.json",
    "spine.pack-apply-result.v1": "spine-pack-apply-result.v1.schema.json",
    "spine.pack-verification-result.v1": "spine-pack-verification-result.v1.schema.json",
    "spine.pack-installer-result.v1": "spine-pack-installer-result.v1.schema.json",
}

DERIVATIONS = {
    "spine.pack-install-request.v1": "spine.pack-install-request-digest.v1",
    "spine.pack-install-plan.v1": "spine.pack-install-plan-digest.v1",
    "spine.pack-install-approval.v1": "spine.pack-install-approval-digest.v1",
    "spine.pack-apply-checkpoint.v1": "spine.pack-apply-checkpoint-digest.v1",
    "spine.pack-apply-result.v1": "spine.pack-apply-result-digest.v1",
    "spine.pack-verification-result.v1": "spine.pack-verification-result-digest.v1",
}

SIZE_LIMITS = {
    "spine.pack-install-request.v1": 65_536,
    "spine.pack-install-plan.v1": 8_388_608,
    "spine.pack-install-approval.v1": 262_144,
    "spine.pack-apply-checkpoint.v1": 16_777_216,
    "spine.pack-apply-result.v1": 16_777_216,
    "spine.pack-verification-result.v1": 16_777_216,
    "spine.pack-installer-result.v1": 1_048_576,
}

REQUIRED_EXECUTION_CONTRACTS = [
    "spine.canonical-json.v1",
    "spine.item-archetypes.v1",
    "spine.notification-profile-bindings.v1",
    "spine.notification-profile-catalog-cursor.v1",
    "spine.notification-profile-metadata-update.v1",
    "spine.notification-profile-readback.v1",
    "spine.notification-profiles.v1",
    "spine.system-info.v2",
    "spine.tickerd-compatibility.v1",
]

EXIT_MAP = {
    "success": ("0", None),
    "invalid_cli_or_artifact_input": ("2", "failed"),
    "invalid_pack_contract_or_digest": ("3", "failed"),
    "incompatible_spine_runtime_or_contracts": ("4", "failed"),
    "decision_required_for_drift": ("5", "decision_required"),
    "blocked_desired_state": ("6", "blocked"),
    "stale_plan_or_target_mismatch": ("7", "failed"),
    "spine_command_rejection": ("8", "failed"),
    "partial_apply": ("9", "partial"),
    "verification_mismatch": ("10", "mismatch"),
    "transport_or_environment_failure": ("11", "failed"),
}


class DuplicateObjectMember(ValueError):
    pass


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateObjectMember(key)
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_closed_object)


def canonical_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        raise ValueError("numbers are not allowed")
    if isinstance(value, str):
        pieces = ['"']
        for char in value:
            codepoint = ord(char)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("surrogates are not allowed")
            if char == '"':
                pieces.append('\\"')
            elif char == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(char)
        return "".join(pieces) + '"'
    if isinstance(value, list):
        return "[" + ",".join(canonical_text(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_text(key)}:{canonical_text(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"unsupported canonical value: {type(value).__name__}")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()


def canonical_value(contract: str, value: Any, shape: str | None = None) -> dict[str, Any]:
    text = canonical_text(value)
    if shape is None:
        shape = next(name for name, family in SEMANTIC_CONTRACTS.items() if family == contract)
    return {
        "contract": contract,
        "shape": shape,
        "canonical_json": text,
        "digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def seal(artifact: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(artifact)
    derivation = DERIVATIONS[value["artifact_schema"]]
    value["content_identity"] = {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": derivation,
    }
    value["content_identity"]["digest"] = digest(value)
    return value


def content_digest_errors(artifact: dict[str, Any]) -> list[str]:
    identity = artifact.get("content_identity")
    if not isinstance(identity, dict):
        return ["content_identity_missing"]
    candidate = deepcopy(artifact)
    claimed = candidate["content_identity"].pop("digest", None)
    if claimed != digest(candidate):
        return ["content_digest_mismatch"]
    expected = DERIVATIONS.get(artifact.get("artifact_schema"))
    if identity.get("derivation_version") != expected:
        return ["content_derivation_mismatch"]
    return []


def _schema_document(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def _resolve_ref(
    reference: str, current_path: Path, current_schema: dict[str, Any]
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    file_part, marker, fragment = reference.partition("#")
    if file_part:
        target_path = (current_path.parent / file_part).resolve()
        root = _schema_document(target_path)
    else:
        target_path = current_path
        root = current_schema
    current: Any = root
    if marker and fragment:
        if not fragment.startswith("/"):
            raise ValueError(reference)
        for token in fragment[1:].split("/"):
            current = current[token.replace("~1", "/").replace("~0", "~")]
    if not isinstance(current, dict):
        raise TypeError(reference)
    return current, target_path, root


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "boolean": isinstance(value, bool),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    schema_path: Path,
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        target, target_path, target_root = _resolve_ref(
            schema["$ref"], schema_path, root_schema
        )
        return schema_errors(value, target, target_path, target_root, path)
    if "oneOf" in schema:
        candidates = [
            schema_errors(value, branch, schema_path, root_schema, path)
            for branch in schema["oneOf"]
        ]
        return [] if sum(not errors for errors in candidates) == 1 else [f"{path}: oneOf"]

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: enum")
    expected_type = schema.get("type")
    if expected_type and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]
    for branch in schema.get("allOf", []):
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if "anyOf" in schema and all(
        schema_errors(value, branch, schema_path, root_schema, path)
        for branch in schema["anyOf"]
    ):
        errors.append(f"{path}: anyOf")
    if "not" in schema and not schema_errors(
        value, schema["not"], schema_path, root_schema, path
    ):
        errors.append(f"{path}: not")
    if "if" in schema:
        match = not schema_errors(value, schema["if"], schema_path, root_schema, path)
        branch = schema.get("then" if match else "else", {})
        errors.extend(schema_errors(value, branch, schema_path, root_schema, path))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: minLength")
        if len(value) > schema.get("maxLength", len(value)):
            errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: minItems")
        if len(value) > schema.get("maxItems", len(value)):
            errors.append(f"{path}: maxItems")
        if schema.get("uniqueItems"):
            encodings = [canonical_text(item) for item in value]
            if len(encodings) != len(set(encodings)):
                errors.append(f"{path}: uniqueItems")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(
                    schema_errors(
                        item,
                        schema["items"],
                        schema_path,
                        root_schema,
                        f"{path}[{index}]",
                    )
                )
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, member in value.items():
            if key in properties:
                errors.extend(
                    schema_errors(
                        member,
                        properties[key],
                        schema_path,
                        root_schema,
                        f"{path}.{key}",
                    )
                )
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: unknown")
    return errors


def validate_schema(artifact: dict[str, Any]) -> list[str]:
    name = ENTRYPOINTS[artifact["artifact_schema"]]
    path = SCHEMA_ROOT / name
    schema = _schema_document(path)
    return schema_errors(artifact, schema, path, schema)


RESULT_REFERENCE = re.compile(r"\$\{spine-pack\.result:(action-[0-9]{6}):([a-z_]+)\}")
REFERENCE_PRODUCERS = {
    "item_archetype_id": ("item_archetype.create", "archetype", "archetype_key"),
    "notification_profile_id": ("notification_profile.create", "profile", "profile_key"),
}


def _reference_slots(value: Any, path: tuple = ()) -> list[tuple]:
    """Find reserved interpolation syntax, including nested values/member names."""
    if isinstance(value, str):
        return [(path, value)] if "${" in value else []
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if "${" in key:
                found.append(((*path, key, "<member-name>"), key))
            found.extend(_reference_slots(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_reference_slots(child, (*path, index)))
    return found


def result_reference_errors(
    value: Any, shape: str, plan: dict[str, Any] | None = None,
    index: int | None = None,
) -> list[str]:
    errors = []
    for path, text in _reference_slots(value):
        match = RESULT_REFERENCE.fullmatch(text)
        if not match:
            errors.append("result_reference_syntax_invalid")
            continue
        if shape != "bindingSetTemplate" or len(path) != 1 or path[0] not in REFERENCE_PRODUCERS:
            errors.append("result_reference_context_forbidden")
            continue
        producer_id, returned_field = match.groups()
        field = path[0]
        if returned_field != field:
            errors.append("result_reference_field_invalid")
            continue
        if plan is None:
            continue  # The containing plan supplies the mandatory correlation stage.
        consumer = plan["actions"][index]
        producers = [(i, a) for i, a in enumerate(plan["actions"]) if a["action_id"] == producer_id]
        if len(producers) != 1:
            errors.append("result_reference_producer_missing")
            continue
        producer_index, producer = producers[0]
        if producer_index >= index:
            errors.append("result_reference_not_earlier")
            continue
        command, kind, key_field = REFERENCE_PRODUCERS[field]
        desired_binding = json.loads(consumer["desired"]["canonical_json"])
        key = (consumer["object_key"].split(":", 1)[1] if kind == "archetype"
               else desired_binding["notification_profile_key"])
        object_key = kind + ":" + key
        roots = [c for c in plan["classifications"] if c["object_key"] == object_key]
        creates = [a for a in plan["actions"] if a["object_key"] == object_key and a["command"] == command]
        if len(roots) != 1 or roots[0]["classification"] != "missing" or roots[0]["identity"] is not None:
            errors.append("result_reference_root_not_missing")
            continue
        if producer["command"] != command or producer["object_key"] != object_key or len(creates) != 1:
            errors.append("result_reference_producer_mismatch")
            continue
        body = json.loads(producer["request_template"]["canonical_json"])
        root_value = json.loads(roots[0]["desired"]["canonical_json"])
        actual_value = (body["revision"] if kind == "archetype" else {
            "metadata": {"display_name": body["display_name"], "description": body["description"]},
            "revision": body["revision"],
        })
        if (body.get(key_field) != key or body.get("owner") != plan["request"]["owner"]
                or producer["desired"] != roots[0]["desired"] or actual_value != root_value):
            errors.append("result_reference_producer_mismatch")
    return errors


def canonical_value_errors(
    value: dict[str, Any], expected_shape: str | None = None
) -> list[str]:
    try:
        parsed = json.loads(value["canonical_json"], object_pairs_hook=_closed_object)
        canonical = canonical_text(parsed)
    except (ValueError, TypeError, json.JSONDecodeError, DuplicateObjectMember):
        return ["canonical_value_invalid"]
    if canonical != value["canonical_json"]:
        return ["canonical_value_not_canonical"]
    actual = hashlib.sha256(value["canonical_json"].encode("utf-8")).hexdigest()
    if actual != value["digest"]:
        return ["canonical_value_digest_mismatch"]
    shape = value.get("shape")
    allowed = dict(SEMANTIC_CONTRACTS)
    for prefix, contract in COMMAND_SHAPES.values():
        for suffix in ("Template", "Request", "Response"):
            allowed[prefix + suffix] = contract
    if shape not in allowed or value.get("contract") != allowed.get(shape):
        return ["embedded_contract_or_shape_mismatch"]
    if expected_shape is not None and shape != expected_shape:
        return ["embedded_context_shape_mismatch"]
    root = _schema_document(EMBEDDED_SCHEMA)
    errors = schema_errors(parsed, root["$defs"][shape], EMBEDDED_SCHEMA, root)
    if errors:
        return ["embedded_contract_invalid", *errors]
    if shape.endswith(("Template", "Request", "Response")):
        return result_reference_errors(parsed, shape)
    return []


def selection_assertion_errors(
    request: dict[str, Any], *, all_flag: bool = False,
    archetype_flags: list[str] | None = None,
) -> list[str]:
    if all_flag and archetype_flags is not None:
        return ["selection_flags_conflict"]
    if archetype_flags is not None and (not archetype_flags or any(not k for k in archetype_flags)):
        return ["selection_flags_empty"]
    if not all_flag and archetype_flags is None:
        return []
    assertion = ({"mode": "all"} if all_flag else
                 {"mode": "archetypes", "archetype_keys": sorted(set(archetype_flags))})
    return [] if assertion == request["request"]["selection"] else ["selection_assertion_mismatch"]


def artifact_size_errors(artifact: dict[str, Any]) -> list[str]:
    size = len(canonical_text(artifact).encode("utf-8"))
    return [] if size <= SIZE_LIMITS[artifact["artifact_schema"]] else ["artifact_too_large"]


def _sorted_unique(values: list[str]) -> bool:
    return values == sorted(set(values))


def _path_is_normalized(path: str) -> bool:
    return (
        path.startswith("/")
        and path != "/"
        and not path.endswith("/")
        and "//" not in path
        and all(part not in {".", ".."} for part in path.split("/"))
    )


def request_errors(request_artifact: dict[str, Any]) -> list[str]:
    errors = validate_schema(request_artifact) + content_digest_errors(request_artifact)
    request = request_artifact.get("request", {})
    selection = request.get("selection", {})
    keys = selection.get("archetype_keys", [])
    if selection.get("mode") == "archetypes" and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    target = request.get("target", {})
    host_name = target.get("host_name", "")
    if host_name != host_name.lower() or host_name.endswith(".") or ".." in host_name:
        errors.append("target_host_not_normalized")
    for value in (
        target.get("spine_command", {}).get("path", ""),
        target.get("ledger", {}).get("path", ""),
    ):
        if not _path_is_normalized(value):
            errors.append("target_path_not_normalized")
    return errors


def command_id(plan_digest: str, execution_id: str, action_id: str) -> str:
    return "spack_" + digest(
        {
            "action_id": action_id,
            "derivation_version": "spine.pack-command-id.v1",
            "execution_id": execution_id,
            "plan_digest": plan_digest,
        }
    )


def binding_identity_errors(plan: dict[str, Any]) -> list[str]:
    """Correlate owner-scoped key resolutions, binding readback, and requests."""
    errors = []
    roots = {}
    seen_ids = set()
    for entry in plan["classifications"]:
        if entry["object_kind"] == "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if identity is not None and set(identity) != {"catalog_id"}:
            errors.append("catalog_identity_shape_mismatch")
            continue
        if (state == "missing" and identity is not None) or (
            state in ("equivalent", "drifted") and identity is None
        ):
            errors.append("catalog_identity_state_mismatch")
        catalog_id = identity["catalog_id"] if identity is not None else None
        if catalog_id is not None:
            marker = (entry["object_kind"], catalog_id)
            if marker in seen_ids or catalog_id.startswith("${"):
                errors.append("catalog_identity_invalid")
            seen_ids.add(marker)
        roots[entry["object_key"]] = (state, catalog_id)

    for entry in plan["classifications"]:
        if entry["object_kind"] != "binding":
            continue
        identity = entry["identity"]
        state = entry["classification"]
        if state == "blocked":
            if identity is not None:
                errors.append("blocked_binding_has_identity")
            continue
        if identity is None or set(identity) != {
            "item_archetype_id", "notification_profile_id", "observed_binding"
        }:
            errors.append("binding_identity_missing_or_invalid")
            continue
        desired = json.loads(entry["desired"]["canonical_json"])
        root_keys = {
            "item_archetype_id": "archetype:" + entry["object_key"].split(":", 1)[1],
            "notification_profile_id": "profile:" + desired["notification_profile_key"],
        }
        for field, key in root_keys.items():
            root = roots.get(key)
            if root is None or root[0] == "blocked" or identity[field] != root[1]:
                errors.append("binding_resolution_mismatch")
        observed = identity["observed_binding"]
        if (state == "missing") != (observed is None):
            errors.append("binding_observation_state_mismatch")
        if observed is not None:
            if any(value.startswith("${") for value in observed.values()):
                errors.append("binding_identity_invalid")
            if identity["item_archetype_id"] is None or (
                observed["item_archetype_id"] != identity["item_archetype_id"]
            ):
                errors.append("binding_archetype_identity_mismatch")
            same_profile = (
                identity["notification_profile_id"] is not None
                and observed["notification_profile_id"] == identity["notification_profile_id"]
            )
            if (state == "equivalent") != same_profile:
                errors.append("binding_profile_identity_mismatch")
            observed_value = entry["observed"]
            if observed_value is not None:
                observed_key = json.loads(observed_value["canonical_json"])["notification_profile_key"]
                observed_root = roots.get("profile:" + observed_key)
                if observed_root is not None and observed_root[1] != observed["notification_profile_id"]:
                    errors.append("binding_observed_key_identity_mismatch")

        for action in plan["actions"]:
            if action["object_key"] != entry["object_key"]:
                continue
            if action["command"] != "notification_profile.binding.set":
                errors.append("binding_action_command_mismatch")
                continue
            request = json.loads(action["request_template"]["canonical_json"])
            if request.get("owner") != plan["request"]["owner"]:
                errors.append("binding_action_owner_mismatch")
            for field, key in root_keys.items():
                expected = identity[field]
                if expected is None:
                    command = "item_archetype.create" if field == "item_archetype_id" else "notification_profile.create"
                    creates = [a for a in plan["actions"] if a["object_key"] == key and a["command"] == command]
                    if len(creates) != 1 or int(creates[0]["ordinal"]) >= int(action["ordinal"]):
                        errors.append("binding_create_reference_missing")
                        continue
                    expected = "${spine-pack.result:" + creates[0]["action_id"] + ":" + field + "}"
                if request.get(field) != expected:
                    errors.append("binding_action_identity_mismatch")
    return errors


def plan_errors(plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(plan) + content_digest_errors(plan)
    if validate_schema(plan):
        return errors
    request = plan["request"]
    embedded_request = seal(
        {
            "artifact_schema": "spine.pack-install-request.v1",
            "request": request,
        }
    )
    if plan["request_digest"] != embedded_request["content_identity"]["digest"]:
        errors.append("request_digest_mismatch")
    errors.extend(request_errors(embedded_request))
    keys = request["selection"].get("archetype_keys", [])
    if keys and not _sorted_unique(keys):
        errors.append("selection_not_sorted")
    for field in ("archetype_keys", "profile_keys", "binding_archetype_keys"):
        if not _sorted_unique(plan["closure"][field]):
            errors.append(f"closure_{field}_not_sorted")
    if plan["required_execution_contracts"] != REQUIRED_EXECUTION_CONTRACTS:
        errors.append("execution_contract_union_mismatch")
    if not _sorted_unique(plan["environment"]["advertised_contracts"]):
        errors.append("advertised_contracts_not_sorted")
    if not set(REQUIRED_EXECUTION_CONTRACTS).issubset(
        plan["environment"]["advertised_contracts"]
    ):
        errors.append("required_execution_contract_missing")
    if [entry["catalog"] for entry in plan["catalog_snapshots"]] != [
        "archetypes", "profiles", "bindings"
    ]:
        errors.append("catalog_snapshot_order")
    expected_object_keys = (
        [f"archetype:{key}" for key in plan["closure"]["archetype_keys"]]
        + [f"profile:{key}" for key in plan["closure"]["profile_keys"]]
        + [f"binding:{key}" for key in plan["closure"]["binding_archetype_keys"]]
    )
    if [entry["object_key"] for entry in plan["classifications"]] != expected_object_keys:
        errors.append("classification_scope_mismatch")
    expected_ids = [f"action-{index:06d}" for index in range(len(plan["actions"]))]
    if [entry["action_id"] for entry in plan["actions"]] != expected_ids:
        errors.append("action_order_or_identity")
    if [entry["ordinal"] for entry in plan["actions"]] != [
        str(index) for index in range(len(plan["actions"]))
    ]:
        errors.append("action_ordinal")
    action_rank = {
        "item_archetype.create": 0,
        "item_archetype.revise": 0,
        "notification_profile.create": 1,
        "notification_profile.metadata.update": 2,
        "notification_profile.revise": 3,
        "notification_profile.binding.set": 4,
    }
    action_order = [
        (action_rank[entry["command"]], entry["object_key"])
        for entry in plan["actions"]
    ]
    if action_order != sorted(action_order):
        errors.append("action_order")
    updates = [
        entry["action_id"] for entry in plan["actions"] if entry["change_kind"] == "update"
    ]
    if plan["decision_action_ids"] != updates:
        errors.append("decision_action_ids_mismatch")
    blocked = [
        entry["object_key"]
        for entry in plan["classifications"]
        if entry["classification"] == "blocked"
    ]
    if plan["blocked_object_keys"] != sorted(blocked):
        errors.append("blocked_object_keys_mismatch")
    if plan["pack"]["status"] == "draft" and plan["apply_eligible"]:
        errors.append("draft_plan_apply_eligible")
    if plan["pack"]["status"] == "draft" and request["draft_posture"] != "inspect_only":
        errors.append("draft_posture_mismatch")
    if plan["pack"]["status"] == "released" and "-draft." in plan["pack"]["version"]:
        errors.append("pack_version_status_mismatch")
    if plan["pack"]["status"] == "draft" and not re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)-draft\.[1-9][0-9]*",
        plan["pack"]["version"],
    ):
        errors.append("pack_version_status_mismatch")
    if blocked and plan["apply_eligible"]:
        errors.append("blocked_plan_apply_eligible")
    for classification in plan["classifications"]:
        observed = classification["observed"]
        reason = classification["blocked_reason"]
        if classification["classification"] == "missing" and observed is not None:
            errors.append("missing_has_observed")
        if classification["classification"] == "blocked" and reason is None:
            errors.append("blocked_without_reason")
        if classification["classification"] != "blocked" and reason is not None:
            errors.append("unexpected_blocked_reason")
        if classification["classification"] in ("equivalent", "drifted") and observed is None:
            errors.append("classification_observation_missing")
        shape = classification["object_kind"] + "Semantics"
        errors.extend(canonical_value_errors(classification["desired"], shape))
        if observed is not None:
            errors.extend(canonical_value_errors(observed, shape))
            equal = classification["desired"]["canonical_json"] == observed["canonical_json"]
            if classification["classification"] == "equivalent" and not equal:
                errors.append("equivalence_preimage_mismatch")
            if classification["classification"] == "drifted" and equal:
                errors.append("drift_preimages_equal")
    class_rank = {"archetype": 0, "profile": 1, "binding": 2}
    classification_order = [
        (class_rank[entry["object_kind"]], entry["object_key"])
        for entry in plan["classifications"]
    ]
    if classification_order != sorted(classification_order):
        errors.append("classification_order")
    for action in plan["actions"]:
        shape = action["object_key"].split(":")[0] + "Semantics"
        errors.extend(canonical_value_errors(action["desired"], shape))
        prefix = COMMAND_SHAPES[action["command"]][0]
        errors.extend(canonical_value_errors(action["request_template"], prefix + "Template"))
        if action["expected"] is not None:
            errors.extend(canonical_value_errors(action["expected"], shape))
        if action["change_kind"] == "create" and action["expected"] is not None:
            errors.append("create_has_expected")
        if action["change_kind"] == "update" and action["expected"] is None:
            errors.append("update_without_expected")
    # Embedded data must be valid before the identity correlator decodes it.
    if not errors:
        errors.extend(binding_identity_errors(plan))
        for index, action in enumerate(plan["actions"]):
            errors.extend(result_reference_errors(
                json.loads(action["request_template"]["canonical_json"]),
                COMMAND_SHAPES[action["command"]][0] + "Template", plan, index,
            ))
    return errors


def approval_errors(approval: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    errors = validate_schema(approval) + content_digest_errors(approval)
    if approval["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("approval_plan_digest_mismatch")
    if approval["authorized_update_action_ids"] != plan["decision_action_ids"]:
        errors.append("update_authorization_incomplete")
    return errors


def apply_preflight_errors(
    plan: dict[str, Any],
    target: dict[str, Any],
    environment: dict[str, Any],
    catalog_snapshots: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if target != plan["request"]["target"]:
        errors.append("target_binding_mismatch")
    if environment != plan["environment"]:
        errors.append("stale_plan_environment_mismatch")
    if catalog_snapshots != plan["catalog_snapshots"]:
        errors.append("stale_plan_catalog_snapshot")
    return errors


def _response_prefix_errors(
    responses: list[dict[str, Any]], plan: dict[str, Any], execution: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    schema_path = SCHEMA_ROOT / "spine-pack-installer-types.v1.schema.json"
    schema = _schema_document(schema_path)
    for response in responses:
        errors.extend(schema_errors(response, schema["$defs"]["responseEvidence"], schema_path, schema))
    if errors:
        return ["response_evidence_invalid", *errors]
    expected_actions = plan["actions"][: len(responses)]
    if [entry["action_id"] for entry in responses] != [
        entry["action_id"] for entry in expected_actions
    ]:
        errors.append("accepted_prefix_not_contiguous")
    for response, action in zip(responses, expected_actions):
        expected_command_id = command_id(
            plan["content_identity"]["digest"],
            execution["execution_id"],
            action["action_id"],
        )
        if response["command_id"] != expected_command_id:
            errors.append("command_id_mismatch")
        if response["command"] != action["command"]:
            errors.append("response_command_mismatch")
        shape = COMMAND_SHAPES[action["command"]][0] + "Response"
        embedded_errors = canonical_value_errors(response["response"], shape)
        errors.extend(embedded_errors)
        if not embedded_errors:
            body = json.loads(response["response"]["canonical_json"])
            template = json.loads(action["request_template"]["canonical_json"])
            if action["command"] in ("item_archetype.create", "notification_profile.create"):
                key = "archetype_key" if action["command"] == "item_archetype.create" else "profile_key"
                if body[key] != template[key]:
                    errors.append("response_create_key_mismatch")
            for field in ("command", "response_contract", "effect"):
                if response[field] != body[field]:
                    errors.append("response_evidence_mismatch")
            for field in ("command_id", "command_receipt_id", "semantic_facts_hash", "effect"):
                if response[field] != body["receipt"][field]:
                    errors.append("receipt_evidence_mismatch")
            if body["receipt"]["created_at_utc"] != execution["action_timestamp_utc"]:
                errors.append("receipt_timestamp_mismatch")
            returned_ids = [
                {"name": key, "value": body[key]}
                for key in sorted(body) if key.endswith("_id")
            ]
            if response["generated_ids"] != returned_ids:
                errors.append("response_generated_ids_mismatch")
        names = [item["name"] for item in response["generated_ids"]]
        if not _sorted_unique(names):
            errors.append("generated_ids_not_sorted")
    return errors


def checkpoint_errors(
    checkpoint: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = (validate_schema(checkpoint) + content_digest_errors(checkpoint)
              + plan_errors(plan) + approval_errors(approval, plan))
    if checkpoint["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("checkpoint_plan_digest_mismatch")
    if checkpoint["approval_digest"] != approval["content_identity"]["digest"]:
        errors.append("checkpoint_approval_digest_mismatch")
    if checkpoint["execution"] != approval["execution"]:
        errors.append("checkpoint_execution_mismatch")
    responses = checkpoint["accepted_responses"]
    errors.extend(_response_prefix_errors(responses, plan, checkpoint["execution"]))
    next_index = len(responses)
    expected_next = (
        plan["actions"][next_index]["action_id"]
        if next_index < len(plan["actions"])
        else None
    )
    if checkpoint["next_action_id"] != expected_next:
        errors.append("checkpoint_next_action_mismatch")
    unresolved = checkpoint["unresolved_submission"]
    if unresolved is not None:
        if unresolved["action_id"] != expected_next:
            errors.append("unresolved_action_mismatch")
        expected_command_id = command_id(
            plan["content_identity"]["digest"],
            checkpoint["execution"]["execution_id"],
            unresolved["action_id"],
        )
        if unresolved["command_id"] != expected_command_id:
            errors.append("command_id_mismatch")
        if next_index < len(plan["actions"]):
            action = plan["actions"][next_index]
            prefix = COMMAND_SHAPES[action["command"]][0]
            errors.extend(canonical_value_errors(unresolved["request"], prefix + "Request"))
            try:
                expected_request = _materialized_request(plan, approval, next_index, responses)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if unresolved["request"]["canonical_json"] != canonical_text(expected_request):
                    errors.append("unresolved_request_mismatch")
    return errors


def apply_result_errors(
    result: dict[str, Any], plan: dict[str, Any], approval: dict[str, Any]
) -> list[str]:
    errors = (validate_schema(result) + content_digest_errors(result)
              + plan_errors(plan) + approval_errors(approval, plan))
    if result["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("apply_plan_digest_mismatch")
    if result["approval_digest"] != approval["content_identity"]["digest"]:
        errors.append("apply_approval_digest_mismatch")
    if result["execution"] != approval["execution"]:
        errors.append("apply_execution_mismatch")
    responses = result["accepted_responses"]
    errors.extend(_response_prefix_errors(responses, plan, result["execution"]))
    remaining = [entry["action_id"] for entry in plan["actions"][len(responses) :]]
    if result["state"] == "applied":
        if len(responses) != len(plan["actions"]) or result["failure"] is not None:
            errors.append("applied_not_complete")
        if result["unattempted_action_ids"]:
            errors.append("applied_has_unattempted")
    elif result["state"] == "partial":
        if result["failure"] is None or not remaining:
            errors.append("partial_without_failure")
        else:
            if result["failure"]["action_id"] != remaining[0]:
                errors.append("partial_failed_action_mismatch")
            if result["unattempted_action_ids"] != remaining[1:]:
                errors.append("partial_suffix_mismatch")
    elif responses or result["failure"] is None:
        errors.append("not_applied_shape_mismatch")
    elif result["unattempted_action_ids"] != remaining:
        errors.append("not_applied_suffix_mismatch")
    return errors


def verification_errors(
    verification: dict[str, Any], plan: dict[str, Any], result: dict[str, Any]
) -> list[str]:
    errors = validate_schema(verification) + content_digest_errors(verification)
    if verification["plan_digest"] != plan["content_identity"]["digest"]:
        errors.append("verification_plan_digest_mismatch")
    if verification["apply_result_digest"] != result["content_identity"]["digest"]:
        errors.append("verification_apply_digest_mismatch")
    if verification["target"] != plan["request"]["target"]:
        errors.append("target_binding_mismatch")
    if verification["pack"] != plan["pack"] or verification["closure"] != plan["closure"]:
        errors.append("verification_scope_mismatch")
    object_states = [entry["state"] for entry in verification["object_results"]]
    for entry in verification["object_results"]:
        if entry["observed"] is not None:
            errors.extend(canonical_value_errors(
                entry["observed"], entry["object_kind"] + "Semantics"
            ))
    should_verify = (
        all(state == "equivalent" for state in object_states)
        and verification["response_evidence"] == "complete"
    )
    if (verification["state"] == "verified") != should_verify:
        errors.append("verification_state_mismatch")
    return errors


def envelope_errors(envelope: dict[str, Any]) -> list[str]:
    errors = validate_schema(envelope) + artifact_size_errors(envelope)
    error = envelope["error"]
    if error is None:
        if envelope["status"] != "success" or envelope["exit_code"] != "0":
            errors.append("envelope_exit_mismatch")
    else:
        expected_exit, expected_status = EXIT_MAP[error["category"]]
        if envelope["exit_code"] != expected_exit or envelope["status"] != expected_status:
            errors.append("envelope_exit_mismatch")
        names = [entry["name"] for entry in error["facts"]]
        if not _sorted_unique(names):
            errors.append("error_facts_not_sorted")
    return errors


def _fixture_request() -> dict[str, Any]:
    value = load_json(POSITIVE_ROOT / "granular_request.json")
    assert isinstance(value, dict)
    return value


def _desired_values() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    archetype = canonical_value(
        "spine.item-archetypes.v1",
        {
            "compatible_item_types": ["event"],
            "description": "A scheduled health appointment.",
            "display_name": "Medical appointment",
        },
    )
    profile = canonical_value(
        "spine.notification-profiles.v1",
        {
            "metadata": {
                "display_name": "Medical appointment standard",
                "description": "Preparation for a medical appointment.",
            },
            "revision": {
                "compatible_item_types": ["event"],
                "templates": [
                {
                    "late_handling": {"grace_seconds": "3600", "kind": "deliver_within"},
                    "schedule": {
                        "at": {
                            "kind": "target_offset",
                            "offset_basis": "elapsed",
                            "offset_seconds": "-7200",
                        },
                        "kind": "once",
                    },
                    "template_key": "two_hours_before",
                }
                ],
            },
        },
    )
    binding = canonical_value(
        "spine.notification-profile-bindings.v1",
        {
            "binding_kind": "archetype_default",
            "notification_profile_key": "medical_appointment_standard",
        },
    )
    return archetype, profile, binding


def make_plan(request: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
    archetype, profile, binding = _desired_values()
    old_profile_value = json.loads(profile["canonical_json"])
    old_profile_value["revision"]["templates"][0]["schedule"]["at"]["offset_seconds"] = "-10800"
    old_profile = canonical_value("spine.notification-profiles.v1", old_profile_value)
    equivalent_lesson = canonical_value("spine.item-archetypes.v1", {
        "display_name": "Lesson", "description": "A scheduled instructional session.",
        "compatible_item_types": ["event"],
    })
    lesson_profile = json.loads(profile["canonical_json"])
    lesson_profile["metadata"] = {
        "display_name": "Lesson standard", "description": "Preparation for a lesson."
    }
    equivalent_lesson_profile = canonical_value(
        "spine.notification-profiles.v1", lesson_profile
    )
    equivalent_lesson_binding = canonical_value(
        "spine.notification-profile-bindings.v1",
        {"binding_kind": "archetype_default", "notification_profile_key": "lesson_standard"}
    )
    plan = {
        "artifact_schema": "spine.pack-install-plan.v1",
        "request_digest": request["content_identity"]["digest"],
        "request": deepcopy(request["request"]),
        "pack": {
            "manifest_schema": "spine.pack-manifest.v1",
            "pack_id": "kinflow-starter",
            "version": "1.0.0-draft.9" if draft else "1.0.0",
            "status": "draft" if draft else "released",
            "manifest_digest": "1" * 64,
        },
        "closure": {
            "archetype_keys": ["lesson", "medical_appointment"],
            "profile_keys": ["lesson_standard", "medical_appointment_standard"],
            "binding_archetype_keys": ["lesson", "medical_appointment"],
        },
        "environment": {
            "runtime_version": "0.3.0",
            "ledger_schema_implemented": "12",
            "ledger_schema_current": "12",
            "advertised_contracts": REQUIRED_EXECUTION_CONTRACTS,
        },
        "required_execution_contracts": REQUIRED_EXECUTION_CONTRACTS,
        "catalog_snapshots": [
            {"catalog": "archetypes", "digest": "2" * 64},
            {"catalog": "profiles", "digest": "3" * 64},
            {"catalog": "bindings", "digest": "4" * 64},
        ],
        "classifications": [
            {"object_kind": "archetype", "object_key": "archetype:lesson", "classification": "equivalent", "desired": equivalent_lesson, "observed": equivalent_lesson, "blocked_reason": None},
            {"object_kind": "archetype", "object_key": "archetype:medical_appointment", "classification": "equivalent", "desired": archetype, "observed": archetype, "blocked_reason": None},
            {"object_kind": "profile", "object_key": "profile:lesson_standard", "classification": "equivalent", "desired": equivalent_lesson_profile, "observed": equivalent_lesson_profile, "blocked_reason": None},
            {"object_kind": "profile", "object_key": "profile:medical_appointment_standard", "classification": "drifted", "desired": profile, "observed": old_profile, "blocked_reason": None},
            {"object_kind": "binding", "object_key": "binding:lesson", "classification": "equivalent", "desired": equivalent_lesson_binding, "observed": equivalent_lesson_binding, "blocked_reason": None},
            {"object_kind": "binding", "object_key": "binding:medical_appointment", "classification": "missing", "desired": binding, "observed": None, "blocked_reason": None},
        ],
        "actions": [
            {
                "ordinal": "0",
                "action_id": "action-000000",
                "command": "notification_profile.revise",
                "object_key": "profile:medical_appointment_standard",
                "change_kind": "update",
                "desired": profile,
                "expected": old_profile,
                "request_template": canonical_value(
                    "spine.notification-profiles.v1",
                    {
                        "contract_version": "spine.notification-profiles.v1",
                        "expected_current_revision_id": "profile_revision_old",
                        "notification_profile_id": "profile_medical",
                        "revision": json.loads(profile["canonical_json"])["revision"],
                    },
                    "profileReviseTemplate",
                ),
            },
            {
                "ordinal": "1",
                "action_id": "action-000001",
                "command": "notification_profile.binding.set",
                "object_key": "binding:medical_appointment",
                "change_kind": "create",
                "desired": binding,
                "expected": None,
                "request_template": canonical_value(
                    "spine.notification-profile-bindings.v1",
                    {
                        "contract_version": "spine.notification-profile-bindings.v1",
                        "item_archetype_id": "archetype_medical",
                        "notification_profile_id": "profile_medical",
                        "owner": {
                            "owner_kind": "subject",
                            "owner_subject_id": "subject_caleb",
                        },
                    },
                    "bindingSetTemplate",
                ),
            },
        ],
        "decision_action_ids": ["action-000000"],
        "blocked_object_keys": [],
        "apply_eligible": not draft,
    }
    identities = [
        {"catalog_id": "archetype_lesson"},
        {"catalog_id": "archetype_medical"},
        {"catalog_id": "profile_lesson"},
        {"catalog_id": "profile_medical"},
        {
            "item_archetype_id": "archetype_lesson",
            "notification_profile_id": "profile_lesson",
            "observed_binding": {
                "notification_profile_binding_id": "binding_lesson",
                "item_archetype_id": "archetype_lesson",
                "notification_profile_id": "profile_lesson",
            },
        },
        {
            "item_archetype_id": "archetype_medical",
            "notification_profile_id": "profile_medical",
            "observed_binding": None,
        },
    ]
    for entry, identity in zip(plan["classifications"], identities):
        entry["identity"] = identity
    return seal(plan)


def make_create_plan(request: dict[str, Any]) -> dict[str, Any]:
    candidate = make_plan(request)
    archetype, profile, binding = [candidate["classifications"][i] for i in (0, 2, 4)]
    for root in (archetype, profile):
        root.update(classification="missing", observed=None, identity=None)
    binding.update(classification="missing", observed=None, identity={
        "item_archetype_id": None, "notification_profile_id": None, "observed_binding": None,
    })
    metadata = json.loads(profile["desired"]["canonical_json"])
    owner = candidate["request"]["owner"]
    creates = []
    for entry, command, contract, shape, body in (
        (archetype, "item_archetype.create", "spine.item-archetypes.v1", "archetypeCreateTemplate", {
            "archetype_key": "lesson", "revision": json.loads(archetype["desired"]["canonical_json"]),
        }),
        (profile, "notification_profile.create", "spine.notification-profiles.v1", "profileCreateTemplate", {
            "profile_key": "lesson_standard", **metadata["metadata"], "revision": metadata["revision"],
        }),
    ):
        creates.append({
            "command": command, "object_key": entry["object_key"], "change_kind": "create",
            "desired": entry["desired"], "expected": None,
            "request_template": canonical_value(contract, {"contract_version": contract, "owner": owner, **body}, shape),
        })
    binding_action = {
        "command": "notification_profile.binding.set", "object_key": binding["object_key"],
        "change_kind": "create", "desired": binding["desired"], "expected": None,
        "request_template": canonical_value("spine.notification-profile-bindings.v1", {
            "contract_version": "spine.notification-profile-bindings.v1", "owner": owner,
            "item_archetype_id": "${spine-pack.result:action-000000:item_archetype_id}",
            "notification_profile_id": "${spine-pack.result:action-000001:notification_profile_id}",
        }, "bindingSetTemplate"),
    }
    candidate["actions"] = [*creates, candidate["actions"][0], binding_action, candidate["actions"][1]]
    for index, action in enumerate(candidate["actions"]):
        action.update(ordinal=str(index), action_id=f"action-{index:06d}")
    candidate["decision_action_ids"] = ["action-000002"]
    return seal(candidate)


def make_approval(plan: dict[str, Any]) -> dict[str, Any]:
    return seal(
        {
            "artifact_schema": "spine.pack-install-approval.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approve_complete_plan": True,
            "acknowledge_single_operator": True,
            "authorized_update_action_ids": plan["decision_action_ids"],
            "execution": {
                "execution_id": "123e4567-e89b-42d3-a456-426614174000",
                "actor_subject_id": "subject_caleb",
                "action_timestamp_utc": "2026-09-09T08:00:00Z",
            },
        }
    )


def _materialized_request(
    plan: dict[str, Any], approval: dict[str, Any], index: int,
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    errors = plan_errors(plan) + approval_errors(approval, plan)
    if errors:
        raise ValueError("result_reference_invalid_plan_or_approval")
    action = plan["actions"][index]
    value = json.loads(action["request_template"]["canonical_json"])
    execution = approval["execution"]
    responses = accepted_responses if accepted_responses is not None else []
    slots = _reference_slots(value)
    if len(responses) > index or (slots and len(responses) != index):
        raise ValueError("result_reference_response_missing")
    errors = _response_prefix_errors(responses, plan, execution)
    if errors:
        raise ValueError("result_reference_response_invalid")
    for path, text in slots:
        producer_id, field = RESULT_REFERENCE.fullmatch(text).groups()
        producer = next((r for r in responses if r["action_id"] == producer_id), None)
        if producer is None:
            raise ValueError("result_reference_response_missing")
        # The exact field and the response are already contextually validated.
        value[path[0]] = json.loads(producer["response"]["canonical_json"])[field]
    value.update(
        {
            "command_id": command_id(
                plan["content_identity"]["digest"],
                execution["execution_id"],
                action["action_id"],
            ),
            "actor_subject_id": execution["actor_subject_id"],
            "action_timestamp_utc": execution["action_timestamp_utc"],
        }
    )
    prefix, contract = COMMAND_SHAPES[action["command"]]
    if canonical_value_errors(canonical_value(contract, value, prefix + "Request"), prefix + "Request"):
        raise ValueError("materialized_request_invalid")
    return value


def make_checkpoint(
    plan: dict[str, Any], approval: dict[str, Any],
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    responses = accepted_responses if accepted_responses is not None else []
    index = len(responses)
    action = plan["actions"][index]
    prefix, contract = COMMAND_SHAPES[action["command"]]
    request = _materialized_request(plan, approval, index, responses)
    return seal(
        {
            "artifact_schema": "spine.pack-apply-checkpoint.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approval_digest": approval["content_identity"]["digest"],
            "execution": approval["execution"],
            "accepted_responses": deepcopy(responses),
            "unresolved_submission": {
                "action_id": action["action_id"],
                "command_id": request["command_id"],
                "submission_state": "prepared_or_submitted",
                "request": canonical_value(contract, request, prefix + "Request"),
            },
            "next_action_id": action["action_id"],
        }
    )


def _response(
    plan: dict[str, Any], approval: dict[str, Any], index: int, *, replay: bool = False,
    accepted_responses: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    action = plan["actions"][index]
    cmd_id = command_id(
        plan["content_identity"]["digest"],
        approval["execution"]["execution_id"],
        action["action_id"],
    )
    contract = COMMAND_SHAPES[action["command"]][1]
    request = _materialized_request(plan, approval, index, accepted_responses)
    if action["command"] == "item_archetype.create":
        facts = {
            "item_archetype_id": "created_archetype_" + request["archetype_key"],
            "item_archetype_revision_id": "created_archetype_revision_" + request["archetype_key"],
            "archetype_key": request["archetype_key"], "revision_number": "1", "status": "active",
        }
        effect = "item_archetype_created"
    elif action["command"] == "notification_profile.create":
        facts = {
            "notification_profile_id": "created_profile_" + request["profile_key"],
            "notification_profile_revision_id": "created_profile_revision_" + request["profile_key"],
            "profile_key": request["profile_key"], "revision_number": "1",
            "normalized_revision_hash": "b" * 64, "status": "active",
        }
        effect = "notification_profile_created"
    elif action["command"] == "notification_profile.revise":
        facts = {
        "notification_profile_id": "profile_medical",
        "notification_profile_revision_id": "profile_revision_new",
        "revision_number": "2",
        "normalized_revision_hash": "b" * 64,
        "status": "active",
        }
        effect = "notification_profile_revised"
    elif action["command"] == "notification_profile.binding.set":
        facts = {
        "notification_profile_binding_id": "binding_lesson" if action["object_key"] == "binding:lesson" else "binding_medical",
        "item_archetype_id": request["item_archetype_id"],
        "notification_profile_id": request["notification_profile_id"],
        "status": "active",
        "compatible_item_types": ["event"],
        }
        effect = "notification_profile_binding_set"
    else:
        raise ValueError("fixture_response_command_unsupported")
    generated = [
        {"name": key, "value": facts[key]}
        for key in sorted(facts) if key.endswith("_id")
    ]
    receipt_id = f"receipt_{index}"
    semantic_hash = str(index + 5) * 64
    response_value = {
        "command": action["command"],
        "effect": effect,
        **facts,
        "ok": True,
        "receipt": {
            "command_id": cmd_id,
            "command_receipt_id": receipt_id,
            "created_at_utc": approval["execution"]["action_timestamp_utc"],
            "effect": effect,
            "semantic_facts_hash": semantic_hash,
        },
        "response_contract": contract,
    }
    return {
        "action_id": action["action_id"],
        "command": action["command"],
        "command_id": cmd_id,
        "outcome": "compatible_replay" if replay else "accepted",
        "response_contract": contract,
        "effect": effect,
        "generated_ids": generated,
        "command_receipt_id": receipt_id,
        "semantic_facts_hash": semantic_hash,
        "response": canonical_value(
            contract, response_value, COMMAND_SHAPES[action["command"]][0] + "Response"
        ),
    }


def make_apply_result(
    plan: dict[str, Any], approval: dict[str, Any], *, partial: bool = False
) -> dict[str, Any]:
    accepted = [_response(plan, approval, 0, replay=True)]
    if not partial:
        accepted.append(_response(plan, approval, 1))
    failure = None
    if partial:
        failure = {
            "action_id": "action-000001",
            "error": {
                "category": "spine_command_rejection",
                "code": "binding_rejected",
                "message": "Spine rejected the binding command.",
                "facts": [{"name": "command", "value": "notification_profile.binding.set"}],
            },
        }
    return seal(
        {
            "artifact_schema": "spine.pack-apply-result.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "approval_digest": approval["content_identity"]["digest"],
            "execution": approval["execution"],
            "state": "partial" if partial else "applied",
            "accepted_responses": accepted,
            "failure": failure,
            "unattempted_action_ids": [],
        }
    )


def make_verification(
    plan: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    object_results = [
        {
            "object_kind": entry["object_kind"],
            "object_key": entry["object_key"],
            "state": "equivalent",
            "observed": entry["desired"],
        }
        for entry in plan["classifications"]
    ]
    return seal(
        {
            "artifact_schema": "spine.pack-verification-result.v1",
            "plan_digest": plan["content_identity"]["digest"],
            "apply_result_digest": result["content_identity"]["digest"],
            "pack": plan["pack"],
            "target": plan["request"]["target"],
            "environment": plan["environment"],
            "catalog_snapshots": [
                {"catalog": "archetypes", "digest": "7" * 64},
                {"catalog": "profiles", "digest": "8" * 64},
                {"catalog": "bindings", "digest": "9" * 64},
            ],
            "closure": plan["closure"],
            "object_results": object_results,
            "response_evidence": "complete",
            "receipt_readback": "captured_responses_only_spine_0.3.0",
            "state": "verified",
        }
    )


def make_create_flow() -> dict[str, Any]:
    """Synthetic command evidence only; never contacts or mutates Spine."""
    request = _fixture_request()
    plan = make_create_plan(request)
    approval = make_approval(plan)
    responses = []
    binding_checkpoint = None
    for index in range(len(plan["actions"])):
        if index == 3:
            binding_checkpoint = make_checkpoint(plan, approval, responses)
        responses.append(_response(plan, approval, index, accepted_responses=responses))
    applied = seal({
        "artifact_schema": "spine.pack-apply-result.v1",
        "plan_digest": plan["content_identity"]["digest"],
        "approval_digest": approval["content_identity"]["digest"],
        "execution": approval["execution"], "state": "applied",
        "accepted_responses": responses, "failure": None, "unattempted_action_ids": [],
    })
    return {
        "fixture_contract": "spine.pack-installer-create-flow.v1",
        "request": request, "plan": plan, "approval": approval,
        "binding_checkpoint": binding_checkpoint, "applied_result": applied,
    }


def make_envelope(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_schema": "spine.pack-installer-result.v1",
        "operation": "apply",
        "status": "success",
        "exit_code": "0",
        "artifact": {
            "path": "/tmp/apply-result.json",
            "digest": result["content_identity"]["digest"],
        },
        "error": None,
    }


class InstallerArtifactContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = _fixture_request()
        self.plan = make_plan(self.request)
        self.approval = make_approval(self.plan)
        self.checkpoint = make_checkpoint(self.plan, self.approval)
        self.applied = make_apply_result(self.plan, self.approval)
        self.partial = make_apply_result(self.plan, self.approval, partial=True)
        self.verification = make_verification(self.plan, self.applied)
        self.envelope = make_envelope(self.applied)

    def test_empty_prefix_partial_is_valid_uncertain_submission_evidence(self):
        result = deepcopy(self.partial)
        result["accepted_responses"] = []
        result["failure"]["action_id"] = self.plan["actions"][0]["action_id"]
        result["unattempted_action_ids"] = [x["action_id"] for x in self.plan["actions"][1:]]
        self.assertEqual(apply_result_errors(seal(result), self.plan, self.approval), [])

    def test_not_applied_preserves_complete_unattempted_scope(self):
        result = deepcopy(self.partial)
        result["state"] = "not_applied"
        result["accepted_responses"] = []
        result["failure"]["action_id"] = None
        result["unattempted_action_ids"] = [x["action_id"] for x in self.plan["actions"]]
        self.assertEqual(apply_result_errors(seal(result), self.plan, self.approval), [])
        result["unattempted_action_ids"] = []
        self.assertIn("not_applied_suffix_mismatch", apply_result_errors(seal(result), self.plan, self.approval))

    def test_schema_entrypoints_are_draft_2020_12(self) -> None:
        for filename in ENTRYPOINTS.values():
            schema = _schema_document(SCHEMA_ROOT / filename)
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertIn("$ref", schema)

    def test_drift_eligibility_does_not_depend_on_approval(self) -> None:
        # A reviewable released drift plan is technically eligible before an
        # approval exists. Approval authorizes its exact immutable digest.
        plan = make_plan(self.request)
        before = deepcopy(plan)
        self.assertTrue(plan["decision_action_ids"])
        self.assertTrue(plan["apply_eligible"])
        self.assertEqual(plan_errors(plan), [])

        approval = make_approval(plan)
        self.assertEqual(approval_errors(approval, plan), [])
        self.assertEqual(approval["plan_digest"], before["content_identity"]["digest"])

        unauthorized = deepcopy(approval)
        unauthorized["authorized_update_action_ids"] = []
        unauthorized = seal(unauthorized)
        self.assertIn("update_authorization_incomplete", approval_errors(unauthorized, plan))
        self.assertEqual(plan, before)

        envelope = {
            "artifact_schema": "spine.pack-installer-result.v1",
            "operation": "plan",
            "status": "decision_required",
            "exit_code": "5",
            "artifact": {
                "path": "/operator/review/plan.json",
                "digest": plan["content_identity"]["digest"],
            },
            "error": {
                "category": "decision_required_for_drift",
                "code": "update_approval_required",
                "message": "The plan requires explicit update approval.",
                "facts": [],
            },
        }
        self.assertEqual(envelope_errors(envelope), [])

    def test_installer_prose_separates_eligibility_and_authorization(self) -> None:
        prose = (ROOT / "specs/installer.md").read_text(encoding="utf-8")
        self.assertIn("Eligibility is not execution authorization.", prose)
        self.assertIn("Approval MUST NOT change `apply_eligible` or the plan digest.", prose)
        self.assertNotIn("it is ineligible until every proposed update", prose)

    def test_embedded_schema_uses_only_supported_validation_keywords(self) -> None:
        supported = {
            "$schema", "$id", "$comment", "title", "$defs", "$ref", "type",
            "required", "properties", "additionalProperties", "const", "enum",
            "minLength", "maxLength", "pattern", "minItems", "maxItems",
            "uniqueItems", "items", "oneOf", "anyOf", "allOf", "not", "if",
            "then", "else",
        }
        def visit(node):
            self.assertFalse(set(node) - supported, set(node) - supported)
            for key in ("$defs", "properties"):
                for child in node.get(key, {}).values():
                    visit(child)
            for key in ("oneOf", "anyOf", "allOf"):
                for child in node.get(key, []):
                    visit(child)
            for key in ("items", "not", "if", "then", "else"):
                if key in node:
                    visit(node[key])
        visit(_schema_document(EMBEDDED_SCHEMA))

    def test_materialized_requests_require_execution_identity(self) -> None:
        for index, action in enumerate(self.plan["actions"]):
            with self.subTest(command=action["command"]):
                prefix, contract = COMMAND_SHAPES[action["command"]]
                request = _materialized_request(self.plan, self.approval, index)
                self.assertEqual(canonical_value_errors(
                    canonical_value(contract, request, prefix + "Request"), prefix + "Request"
                ), [])
                del request["command_id"]
                self.assertIn("embedded_contract_invalid", canonical_value_errors(
                    canonical_value(contract, request, prefix + "Request"), prefix + "Request"
                ))

    def test_positive_artifact_family(self) -> None:
        self.assertEqual(request_errors(self.request), [])
        self.assertEqual(plan_errors(self.plan), [])
        self.assertEqual(approval_errors(self.approval, self.plan), [])
        self.assertEqual(checkpoint_errors(self.checkpoint, self.plan, self.approval), [])
        self.assertEqual(apply_result_errors(self.applied, self.plan, self.approval), [])
        self.assertEqual(apply_result_errors(self.partial, self.plan, self.approval), [])
        self.assertEqual(verification_errors(self.verification, self.plan, self.applied), [])
        self.assertEqual(envelope_errors(self.envelope), [])
        for artifact in (
            self.request,
            self.plan,
            self.approval,
            self.checkpoint,
            self.applied,
            self.partial,
            self.verification,
            self.envelope,
        ):
            self.assertEqual(artifact_size_errors(artifact), [])

    def test_static_artifact_suite_matches_and_validates(self) -> None:
        suite = load_json(POSITIVE_ROOT / "profile_drift_artifact_suite.json")
        expected = {
            "fixture_contract": "spine.pack-installer-artifact-suite.v1",
            "request": self.request,
            "plan": self.plan,
            "approval": self.approval,
            "uncertain_checkpoint": self.checkpoint,
            "applied_result": self.applied,
            "partial_result": self.partial,
            "verification": self.verification,
            "success_envelope": self.envelope,
        }
        self.assertEqual(suite, expected)
        self.assertEqual(request_errors(suite["request"]), [])
        self.assertEqual(plan_errors(suite["plan"]), [])
        self.assertEqual(approval_errors(suite["approval"], suite["plan"]), [])
        self.assertEqual(
            checkpoint_errors(
                suite["uncertain_checkpoint"], suite["plan"], suite["approval"]
            ),
            [],
        )
        self.assertEqual(
            apply_result_errors(
                suite["partial_result"], suite["plan"], suite["approval"]
            ),
            [],
        )

    def test_scenario_fixture_describes_generated_flow(self) -> None:
        vector = load_json(POSITIVE_ROOT / "profile_drift_vertical_flow.json")
        actual = [
            f"{entry['object_key']}={entry['classification']}"
            for entry in self.plan["classifications"]
        ]
        self.assertEqual(self.plan["closure"], vector["expected_closure"])
        self.assertEqual(actual, vector["expected_classifications"])
        self.assertEqual(
            [entry["command"] for entry in self.plan["actions"]],
            vector["expected_actions"],
        )
        self.assertEqual(self.plan["decision_action_ids"], vector["expected_decision_action_ids"])
        self.assertEqual([self.applied["state"], self.partial["state"]], vector["expected_terminal_states"])
        self.assertEqual(self.verification["state"], vector["expected_verification_state"])

    def test_negative_fixture_manifest_is_complete_and_sorted(self) -> None:
        fixture_manifest = load_json(FIXTURE_MANIFEST)
        for group in ("positive", "negative"):
            self.assertEqual(fixture_manifest[group], sorted(fixture_manifest[group]))
            for relative in fixture_manifest[group]:
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_negative_semantic_vectors(self) -> None:
        expected_files = {
            "apply_target_mismatch.json": "target_binding_mismatch",
            "draft_apply_eligible.json": "draft_plan_apply_eligible",
            "incorrect_artifact_digest.json": "content_digest_mismatch",
            "noncontiguous_partial_apply.json": "accepted_prefix_not_contiguous",
            "stale_catalog_snapshot.json": "stale_plan_catalog_snapshot",
            "stale_plan_approval.json": "approval_plan_digest_mismatch",
            "target_mismatch.json": "target_binding_mismatch",
            "unauthorized_drift.json": "update_authorization_incomplete",
            "uncertain_replay_command_mismatch.json": "command_id_mismatch",
            "unsorted_selection.json": "selection_not_sorted",
        }
        self.assertEqual(
            [path.name for path in sorted(NEGATIVE_ROOT.glob("*.json"))],
            sorted([*expected_files, "embedded_contract_violations.json",
                    "selection_assertion_mismatch.json", "binding_identity_mismatch.json",
                    "invalid_result_references.json"]),
        )
        for filename, expected in expected_files.items():
            vector = load_json(NEGATIVE_ROOT / filename)
            self.assertEqual(vector["expected_error"], expected)
            with self.subTest(filename=filename):
                if filename == "draft_apply_eligible.json":
                    draft_request = deepcopy(self.request)
                    draft_request["request"]["draft_posture"] = "inspect_only"
                    draft_request = seal(draft_request)
                    candidate = make_plan(draft_request, draft=True)
                    candidate["apply_eligible"] = True
                    candidate = seal(candidate)
                    errors = plan_errors(candidate)
                elif filename == "incorrect_artifact_digest.json":
                    candidate = deepcopy(self.request)
                    candidate["content_identity"]["digest"] = "0" * 64
                    errors = request_errors(candidate)
                elif filename == "noncontiguous_partial_apply.json":
                    candidate = deepcopy(self.partial)
                    candidate["accepted_responses"] = [_response(self.plan, self.approval, 1)]
                    candidate = seal(candidate)
                    errors = apply_result_errors(candidate, self.plan, self.approval)
                elif filename == "stale_catalog_snapshot.json":
                    snapshots = deepcopy(self.plan["catalog_snapshots"])
                    snapshots[1]["digest"] = "f" * 64
                    errors = apply_preflight_errors(
                        self.plan,
                        self.plan["request"]["target"],
                        self.plan["environment"],
                        snapshots,
                    )
                elif filename == "stale_plan_approval.json":
                    candidate = deepcopy(self.approval)
                    candidate["plan_digest"] = "f" * 64
                    candidate = seal(candidate)
                    errors = approval_errors(candidate, self.plan)
                elif filename == "target_mismatch.json":
                    candidate = deepcopy(self.verification)
                    candidate["target"]["host_name"] = "other.local"
                    errors = verification_errors(seal(candidate), self.plan, self.applied)
                elif filename == "apply_target_mismatch.json":
                    target = deepcopy(self.plan["request"]["target"])
                    target["host_name"] = "other.local"
                    errors = apply_preflight_errors(
                        self.plan, target, self.plan["environment"], self.plan["catalog_snapshots"]
                    )
                elif filename == "unauthorized_drift.json":
                    candidate = deepcopy(self.approval)
                    candidate["authorized_update_action_ids"] = []
                    candidate = seal(candidate)
                    errors = approval_errors(candidate, self.plan)
                elif filename == "uncertain_replay_command_mismatch.json":
                    candidate = deepcopy(self.checkpoint)
                    candidate["unresolved_submission"]["command_id"] = "spack_" + "f" * 64
                    candidate = seal(candidate)
                    errors = checkpoint_errors(candidate, self.plan, self.approval)
                else:
                    candidate = deepcopy(self.request)
                    candidate["request"]["selection"]["archetype_keys"].reverse()
                    candidate = seal(candidate)
                    errors = request_errors(candidate)
                self.assertIn(expected, errors)

    def test_unknown_fields_fail_closed(self) -> None:
        candidate = deepcopy(self.approval)
        candidate["allow_updates"] = True
        self.assertTrue(any("unknown" in error for error in validate_schema(candidate)))

    def test_embedded_contracts_reject_validly_hashed_bad_content(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "embedded_contract_violations.json")
        validators = {
            "plan": plan_errors,
            "checkpoint": lambda a: checkpoint_errors(a, self.plan, self.approval),
            "applied": lambda a: apply_result_errors(a, self.plan, self.approval),
            "verification": lambda a: verification_errors(a, self.plan, self.applied),
        }
        for case in vector["cases"]:
            with self.subTest(case=case):
                artifact = deepcopy(getattr(self, case["artifact"]))
                wrapper = artifact
                for token in case["path"]:
                    wrapper = wrapper[int(token)] if isinstance(wrapper, list) else wrapper[token]
                parsed = json.loads(wrapper["canonical_json"])
                parent = parsed
                for token in case["remove"][:-1]:
                    parent = parent[token]
                del parent[case["remove"][-1]]
                wrapper.update(canonical_value(wrapper["contract"], parsed, wrapper["shape"]))
                artifact = seal(artifact)
                self.assertEqual(content_digest_errors(artifact), [])
                self.assertIn(vector["expected_error"], validators[case["artifact"]](artifact))

    def test_contract_and_context_cannot_be_spoofed(self) -> None:
        candidate = deepcopy(self.plan)
        candidate["classifications"][0]["desired"]["contract"] = "spine.unknown.v1"
        self.assertIn("embedded_contract_or_shape_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["actions"][0]["request_template"] = candidate["actions"][0]["desired"]
        self.assertIn("embedded_context_shape_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.applied)
        candidate["accepted_responses"][0]["effect"] = "fabricated"
        self.assertIn("response_evidence_mismatch",
                      apply_result_errors(seal(candidate), self.plan, self.approval))

    def test_request_selection_is_authoritative(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "selection_assertion_mismatch.json")
        self.assertIn(vector["expected_error"], selection_assertion_errors(
            self.request, all_flag=vector["all_flag"]
        ))
        self.assertEqual(selection_assertion_errors(self.request), [])
        self.assertEqual(selection_assertion_errors(
            self.request, archetype_flags=["medical_appointment", "lesson", "lesson"]
        ), [])
        self.assertEqual(selection_assertion_errors(
            self.request, all_flag=True, archetype_flags=["lesson"]
        ), ["selection_flags_conflict"])
        full = deepcopy(self.request)
        full["request"]["selection"] = {"mode": "all"}
        full = seal(full)
        self.assertEqual(selection_assertion_errors(full, all_flag=True), [])
        self.assertEqual(selection_assertion_errors(full, archetype_flags=[]), ["selection_flags_empty"])

    def test_metadata_and_behavior_comparisons_are_independent(self) -> None:
        original = self.plan["classifications"][2]["observed"]
        for section, field, replacement in (
            ("metadata", "description", "Different presentation"),
            ("revision", "compatible_item_types", ["event", "task"]),
        ):
            with self.subTest(section=section):
                candidate = deepcopy(self.plan)
                parsed = json.loads(original["canonical_json"])
                parsed[section][field] = replacement
                candidate["classifications"][2]["observed"] = canonical_value(
                    original["contract"], parsed, original["shape"]
                )
                self.assertIn("equivalence_preimage_mismatch", plan_errors(seal(candidate)))

    def test_binding_identity_vectors(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "binding_identity_mismatch.json")
        for mutation in vector["mutations"]:
            with self.subTest(path=mutation["path"]):
                candidate = deepcopy(self.plan)
                target = candidate
                for part in mutation["path"][:-1]:
                    target = target[int(part)] if isinstance(target, list) else target[part]
                target[mutation["path"][-1]] = mutation["value"]
                candidate = seal(candidate)
                self.assertEqual(validate_schema(candidate), [])
                self.assertEqual(content_digest_errors(candidate), [])
                self.assertIn(mutation["expected_error"], plan_errors(candidate))

    def test_binding_identity_closure_and_state(self) -> None:
        for index in range(len(self.plan["classifications"])):
            candidate = deepcopy(self.plan)
            del candidate["classifications"][index]["identity"]
            self.assertTrue(validate_schema(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][4]["identity"]["unexpected"] = "extra"
        self.assertTrue(validate_schema(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][4]["identity"]["observed_binding"] = None
        self.assertIn("binding_observation_state_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        candidate["classifications"][0]["identity"] = None
        self.assertIn("catalog_identity_state_mismatch", plan_errors(seal(candidate)))
        candidate = deepcopy(self.plan)
        binding = candidate["classifications"][4]
        binding.update(classification="blocked", observed=None, identity=None, blocked_reason="ambiguous_readback")
        candidate["blocked_object_keys"] = [binding["object_key"]]
        candidate["apply_eligible"] = False
        self.assertEqual(plan_errors(seal(candidate)), [])

    def test_binding_requests_match_resolved_identity_and_owner(self) -> None:
        for field, value, expected in (
            ("item_archetype_id", "wrong_archetype", "binding_action_identity_mismatch"),
            ("notification_profile_id", "wrong_profile", "binding_action_identity_mismatch"),
            ("owner", {"owner_kind": "subject", "owner_subject_id": "other_owner"}, "binding_action_owner_mismatch"),
        ):
            candidate = deepcopy(self.plan)
            action = candidate["actions"][1]
            request = json.loads(action["request_template"]["canonical_json"])
            request[field] = value
            action["request_template"] = canonical_value(
                "spine.notification-profile-bindings.v1", request, "bindingSetTemplate"
            )
            self.assertIn(expected, plan_errors(seal(candidate)))

    def test_binding_drift_requires_different_observed_profile_id(self) -> None:
        candidate = deepcopy(self.plan)
        binding = candidate["classifications"][4]
        binding["classification"] = "drifted"
        binding["observed"] = canonical_value("spine.notification-profile-bindings.v1", {
            "binding_kind": "archetype_default", "notification_profile_key": "medical_appointment_standard",
        })
        binding["identity"]["observed_binding"]["notification_profile_id"] = "profile_medical"
        candidate["actions"].insert(1, {
            "command": "notification_profile.binding.set", "object_key": binding["object_key"],
            "change_kind": "update", "desired": binding["desired"], "expected": binding["observed"],
            "request_template": canonical_value("spine.notification-profile-bindings.v1", {
                "contract_version": "spine.notification-profile-bindings.v1",
                "owner": candidate["request"]["owner"],
                "item_archetype_id": "archetype_lesson", "notification_profile_id": "profile_lesson",
            }, "bindingSetTemplate"),
        })
        for index, action in enumerate(candidate["actions"]):
            action.update(ordinal=str(index), action_id=f"action-{index:06d}")
        candidate["decision_action_ids"] = ["action-000000", "action-000001"]
        self.assertEqual(plan_errors(seal(candidate)), [])
        binding["identity"]["observed_binding"]["notification_profile_id"] = "profile_lesson"
        self.assertIn("binding_profile_identity_mismatch", plan_errors(seal(candidate)))

    def test_binding_missing_dependencies_use_create_result_references(self) -> None:
        candidate = make_create_plan(self.request)
        self.assertEqual(plan_errors(candidate), [])
        binding_action = candidate["actions"][3]
        body = json.loads(binding_action["request_template"]["canonical_json"])
        body["notification_profile_id"] = "guessed_profile_id"
        binding_action["request_template"] = canonical_value(
            "spine.notification-profile-bindings.v1", body, "bindingSetTemplate"
        )
        self.assertIn("binding_action_identity_mismatch", plan_errors(seal(candidate)))

    def test_archetype_source_provenance_is_explicit(self) -> None:
        source = _schema_document(EMBEDDED_SCHEMA)["$comment"]
        for reference in (
            "notification-profile-types.schema.json#/$defs/archetypeRevision",
            "notification-profile-commands.schema.json#/$defs/archetypeCreate",
            "#/$defs/archetypeRevise", "src/spine/commands/notification_profiles.py",
            "_archetype_create", "_archetype_revise", "72203f092de191a7633b1884bf0d61836a25abe4",
        ):
            self.assertIn(reference, source)

    def test_create_flow_materializes_and_replays_binding_checkpoint(self) -> None:
        flow = make_create_flow()
        self.assertEqual(flow, load_json(POSITIVE_ROOT / "create_binding_artifact_suite.json"))
        plan, approval = flow["plan"], flow["approval"]
        checkpoint = flow["binding_checkpoint"]
        self.assertEqual(plan_errors(plan), [])
        self.assertEqual(approval_errors(approval, plan), [])
        self.assertEqual(checkpoint_errors(checkpoint, plan, approval), [])
        self.assertEqual(apply_result_errors(flow["applied_result"], plan, approval), [])
        request = json.loads(checkpoint["unresolved_submission"]["request"]["canonical_json"])
        self.assertEqual(request["item_archetype_id"], "created_archetype_lesson")
        self.assertEqual(request["notification_profile_id"], "created_profile_lesson_standard")
        self.assertEqual(_reference_slots(request), [])
        # Compatible replay must produce exactly the same request bytes/command ID.
        replayed = deepcopy(checkpoint["accepted_responses"])
        for response in replayed:
            response["outcome"] = "compatible_replay"
        self.assertEqual(canonical_text(_materialized_request(plan, approval, 3, replayed)),
                         checkpoint["unresolved_submission"]["request"]["canonical_json"])
        candidate = deepcopy(checkpoint)
        unresolved = candidate["unresolved_submission"]["request"]
        vector = load_json(NEGATIVE_ROOT / "invalid_result_references.json")["unresolved_request"]
        request[vector["field"]] = vector["value"]
        candidate["unresolved_submission"]["request"] = canonical_value(
            unresolved["contract"], request, unresolved["shape"]
        )
        self.assertIn(vector["expected_error"], checkpoint_errors(seal(candidate), plan, approval))

    def test_invalid_result_reference_vectors(self) -> None:
        vector = load_json(NEGATIVE_ROOT / "invalid_result_references.json")
        for mutation in vector["mutations"]:
            with self.subTest(case=mutation["case"]):
                plan = make_create_plan(self.request)
                action = plan["actions"][int(mutation["action_index"])]
                template = action["request_template"]
                value = json.loads(template["canonical_json"])
                target = value
                for key in mutation["path"][:-1]:
                    target = target[key]
                target[mutation["path"][-1]] = mutation["value"]
                action["request_template"] = canonical_value(template["contract"], value, template["shape"])
                plan = seal(plan)
                self.assertEqual(validate_schema(plan), [])
                self.assertEqual(content_digest_errors(plan), [])
                self.assertIn(mutation["expected_error"], plan_errors(plan))
                with self.assertRaisesRegex(ValueError, "invalid_plan_or_approval"):
                    _materialized_request(plan, make_approval(plan), int(mutation["action_index"]))

    def test_reference_materialization_rejects_bad_producer_evidence(self) -> None:
        flow = make_create_flow()
        plan, approval = flow["plan"], flow["approval"]
        prefix = flow["binding_checkpoint"]["accepted_responses"]
        for responses in ([], prefix[:1], prefix[:2]):
            with self.assertRaisesRegex(ValueError, "result_reference_response_missing"):
                _materialized_request(plan, approval, 3, responses)
        for field, value in (
            ("command_id", "wrong_command"), ("outcome", "rejected"),
            ("generated_ids", []), ("command_receipt_id", "wrong_receipt"),
        ):
            responses = deepcopy(prefix)
            responses[0][field] = value
            with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
                _materialized_request(plan, approval, 3, responses)
        for field, value in (
            ("archetype_key", "another_key"),
            ("item_archetype_id", "${spine-pack.result:action-000001:notification_profile_id}"),
        ):
            responses = deepcopy(prefix)
            embedded = responses[0]["response"]
            body = json.loads(embedded["canonical_json"])
            body[field] = value
            responses[0]["response"] = canonical_value(embedded["contract"], body, embedded["shape"])
            responses[0]["generated_ids"] = [
                {"name": key, "value": body[key]} for key in sorted(body) if key.endswith("_id")
            ]
            with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
                _materialized_request(plan, approval, 3, responses)
        responses = deepcopy(prefix)
        responses[0], responses[1] = responses[1], responses[0]
        with self.assertRaisesRegex(ValueError, "result_reference_response_invalid"):
            _materialized_request(plan, approval, 3, responses)

    def test_reference_scan_covers_all_commands_and_nested_members(self) -> None:
        reference = "${spine-pack.result:action-000000:item_archetype_id}"
        for prefix, contract in COMMAND_SHAPES.values():
            for suffix in ("Template", "Request", "Response"):
                with self.subTest(shape=prefix + suffix):
                    self.assertIn("result_reference_context_forbidden", result_reference_errors(
                        {"owner": {"owner_subject_id": reference}}, prefix + suffix
                    ))
                    self.assertTrue(result_reference_errors({reference: "value"}, prefix + suffix))
        self.assertIn("result_reference_syntax_invalid", result_reference_errors(
            {"item_archetype_id": "prefix" + reference}, "bindingSetTemplate"
        ))

    def test_command_identity_changes_with_plan_execution_or_action(self) -> None:
        plan_digest = self.plan["content_identity"]["digest"]
        execution_id = self.approval["execution"]["execution_id"]
        baseline = command_id(plan_digest, execution_id, "action-000000")
        self.assertNotEqual(baseline, command_id("f" * 64, execution_id, "action-000000"))
        self.assertNotEqual(
            baseline,
            command_id(plan_digest, "223e4567-e89b-42d3-a456-426614174000", "action-000000"),
        )
        self.assertNotEqual(baseline, command_id(plan_digest, execution_id, "action-000001"))


if __name__ == "__main__":
    unittest.main()
```
