# Installer contract

Status: Draft v0.4; machine-artifact review required before implementation

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

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** describe requirements
for the future reviewed implementation. This draft does not authorize adding
an installer runtime.

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

Blocked objects make the plan ineligible for application. Drift makes a plan
decision-bearing: it is ineligible until every proposed update is individually
authorized. The installer MUST NOT apply only the missing portion of a selected
scope while silently skipping blocked or unauthorized drift.

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
