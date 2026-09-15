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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/installer-preflight-boundary-audit-001/audit-notes.md
Hash: becaf82992f55ae14c03811b2308bf7dd7283c6c2acbeb980dd4d54c56306bf2

# Installer planning and apply-preflight boundary audit

## Authorization state

This payload is staged only. Do not invoke the nested reviewer until the
operator explicitly approves the exact file list.

## Change intent

Assess the committed read-only installer planner and non-mutating apply
preflight before any Spine write, checkpoint, continuation, or public `apply`
command is implemented.

## Expected boundary

- Spine remains the sole authority for installed state.
- Planning and preflight use only the pinned public Spine read-command surface.
- The preflight validates complete immutable plan and approval artifacts,
  released/apply-eligible posture, manifest and request identity, exact target
  compatibility, fresh catalog state, and all planned command templates.
- Incomplete update authorization, drafts, blocked or ineligible plans,
  mismatched identities, incompatible targets, and stale observations fail
  closed before any write can be launched.
- A successful preflight returns internal execution-ready facts only. It does
  not publish an apply result, checkpoint, or public `apply` command.

## Reviewer questions

1. Can any path in the submitted implementation launch, smuggle, or replay a
   Spine write during planning or preflight?
2. Are the plan, approval, manifest, request, target, environment, catalogs,
   snapshots, classifications, actions, and update authorizations validated and
   correlated strongly enough for the stated local single-operator boundary?
3. Can a changed or stale plan pass by recomputing only an outer digest, by
   exploiting result references, or by changing unselected manifest content?
4. Does the implementation preserve the distinction between eligibility,
   approval, preflight readiness, and successful application?
5. Do the focused tests cover the material positive and negative paths needed
   before the first write-enabled slice begins?
6. Are implementation and documentation consistent, without silently claiming
   write execution, recovery, live-target qualification, or release readiness?

## Out of scope

- Phase One or Phase Two convergence
- Editor invocation or source mutation
- implementation of writes, checkpoints, continuation, verify, or packaging
- redesign of already accepted installer semantics
- cosmetic cleanup

Report verdict, boundary preservation, blocker/major/minor findings, any
out-of-scope observations, and whether Slice 3 may safely begin from this
boundary. This audit does not declare convergence or runtime qualification.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/architecture.md

Hash: 9da39b1ef22d33c4bdacefa850aa76aa240a9e6adab47eac274dce2692b44d3a

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
The bounded read-only planning slice and an internal, non-mutating apply
preflight service are implemented. Public `apply`, Spine writes, checkpointing,
continuation, and verification remain reviewed design targets, not executable
functionality.

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
- `spine_command.py` is the sole subprocess boundary. Its allowlist contains
  only `system.info`, archetype/profile list and show, and binding list.
- `__main__.py` handles explicit files, matching selection assertions, one JSON
  result envelope, and private no-clobber plan publication.

The adapter MUST reject write commands before launching a subprocess, even
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

Hash: 6a0de0b154db8520cc3c33712c9232d487411a7861ea0cff224d5401b4c4e5d1

```markdown
# Installer contract

Status: Draft v0.4; bounded read-only `plan` implementation authorized

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
requirements. The first authorized runtime slice is read-only `plan`, using
the source-tree layout in `specs/architecture.md`. `apply`, `verify`, recovery,
remote transports, and release packaging remain outside that slice and require
separate review and authorization. No Spine runtime change is authorized.

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
spine-packs apply --plan PLAN --approval APPROVAL --output RESULT
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

Hash: 15c1d9f1b835637851ff2f8368ea11642a409b7f43eea37ada0c7c23b19621e2

```markdown
# Installer artifact contracts

Status: Draft v0.1; bounded read-only `plan` implementation authorized

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
has empty response evidence and a non-null failure. `applied` has null failure
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

The authorized read-only slice uses the source-tree `spine_packs` package and
standard-library `argparse`, as recorded in `specs/architecture.md`. This does
not authorize apply, verification, or recovery implementation. Filesystem
configuration and release packaging remain deferred. It does not add section bundles,
remote transports, signatures, install registries, credentials, Windows path
semantics, or Spine runtime changes.
```

### Spec 4: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: b8cb0b09454e3a248778d8811d70683d0cd7673c3417e9d71e79e06d39d7a4ba

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

### Slice 2: apply preflight without writes — implemented locally

Add the `apply` entry boundary while keeping all Spine writes disabled:

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

### Slice 3: initial apply and durable checkpointing

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

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/artifacts.py

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

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/planning.py

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

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/preflight.py

Hash: ac8e53b9d64b586a40cfc30aed624f9b14a73bbf6e7c5067bda4bc5f837b69bc

```markdown
"""Non-mutating apply preflight over an approved installation plan."""

from __future__ import annotations

from copy import deepcopy

from . import artifacts as a
from .manifest import validate_pack
from .planning import INVALID, PACK_INVALID, PlanError, plan_installation, require

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

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/spine_command.py

Hash: d245e4bac486c079f0a27066c7fb3e92a9d9b42ee2bf889f8e14979ace9c1b24

```markdown
"""Local read-only process adapter for the pinned Spine 0.3.0 command surface."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import selectors
import socket
import subprocess
import time

from . import artifacts as a
from .planning import CATALOGS, ENVIRONMENT, PlanError, require, validate_readback


READ_COMMANDS = frozenset({"system.info", "item_archetype.list", "item_archetype.show",
                           "notification_profile.list", "notification_profile.show",
                           "notification_profile.binding.list"})
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
            if response.get("ok") is False:
                validate_readback(response, "commandFailure")
                require(response["command"] == command, "response_command_mismatch")
                raise PlanError("spine_command_rejection", "spine_read_rejected")
            # Read failure never becomes a missing/retained object or an applicable plan.
            require(returncode == 0 and response.get("ok") is True, "spine_read_failed")
            require(response.get("command") == command, "response_command_mismatch")
            return response
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

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_planning.py

Hash: 887038261bb1976102b2c448ae55febdc4c468fbf6048b3d081785e2b985a123

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

    def test_write_operations_are_not_cli_commands(self):
        for command in ("apply", "verify", "recover"):
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

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_apply_preflight.py

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
