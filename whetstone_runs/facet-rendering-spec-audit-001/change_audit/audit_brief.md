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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-spec-audit-001/audit-notes.md
Hash: 16d2a75a98c8dbd8e0310a83d9309f4741dadb7315781629244c65fb9033ad28

# Change intent

Review a specification/planning proposal for one facet-aware flight configuration
slice in Spine Packs. No successor runtime or curated manifest was implemented.
The exact Spine source pin is `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`, runtime
0.9.0, schema 19; do not substitute a newer baseline. Existing installer 0.3.0
and manifest v1 do not already support that target.

# Expected boundary

One reviewer-only `audit-change` pass with the `consistency` profile. No Editor,
convergence claim, source apply-back, runtime implementation, external browsing,
deployment or release. This audit is staged, NOT authorized to run. It requires
operator approval of the exact payload hashes in APPROVAL.md first. No previous
audit's approval carries forward. Model/executable selection is a launch-time
preflight, not permission to contact a client while staging.

Spine owns validation, ownership, rendering, scheduling, immutable history and
receipts. Packs are declarative owner-neutral configuration. Only the closed
public catalog command set is proposed. No database access, internal API calls,
disclosure authorization, actual facet values, item authoring, materialization
or sending. Preserve all v1 capabilities, hashes and released artifacts.

# Review targets

The proposal is specs/facet-rendering-packs.md. Related changes only route to
that proposal or sequence gated implementation; they do not activate support.
The existing v1 specs are preservation context, not targets for wholesale rewrite.
The baseline doc is inspection evidence. The three pinned Spine excerpt files
provide selected upstream text, machine fragments and structural fixtures;
their complete-source hashes and original paths are retained. They are not a
complete executable transitive schema closure or live qualification evidence.

Check especially:

1. Closed manifest v2; one desired revision per key; local refs versus generated
   IDs; deterministic order with presentation-order exception; granular closure.
2. Complete cascade from schema publish to binding/rendering/profile pins;
   exact per-action authorization and unchanged item/history/disclosure boundary.
3. Actual 0.9.0 public commands/selectors and 17-contract compiled execution union;
   base-renderer content compatibility is additional, not an execution shortcut.
4. Three different response/receipt families and missing facet provenance/hash;
   no fabricated universal receipt or speculative consumer outputs.
5. New catalogs lack public snapshot hashes; bounded public observation evidence
   is explicitly local, not a Spine attestation or concurrent-writer guarantee.
6. Prepared/accepted durability, prefix-plus-one recovery, exact request replay,
   CAS versus non-CAS bindings and read-only exact-pin verification.
7. Product choices remain unanswered: flight fields/settings, labels/template
   use, opt-in versus default replacement, and distribution identity. A reviewer
   may identify consequences, not silently choose those policies.
8. Schemas, exact reference slots, aggregate observation budgets and fixtures
   must be reviewed before implementation; distinguish planned tests from results.
9. Inspect the source-level profile-v2-list blocker in spine-readback-blocker.md:
   v2 dispatch calls a legacy projection that rejects stored v2 revisions before
   the v2 projection. The task did not run a ledger reproduction. Confirm or
   challenge the source inference; never substitute a newer baseline or invent
   an internal API/list-skipping workaround. Review remains useful even if an
   upstream fix and separately approved baseline are prerequisites to qualification.

# Out of scope

Do not design a theme engine, general package resolver, arbitrary revision-history
installer, new Spine API, multi-writer reconciler, disclosure wizard or notification
workflow. Do not request the entire Spine source tree or private target state.
No destination/owner secrets are needed. Do not treat synthetic fixtures as approved
curated content or a valid deployment. Report actionable inconsistencies, real
buildability gaps and preservation issues within the above boundary.

# Current evidence

Read-only source inspection completed at the exact commit. Existing repository,
contract/runtime and whitespace checks are preservation checks only. The source
and clean-wheel 0.9.0 qualification, machine-contract implementation and external
review remain future gates. APPROVAL.md records the exact proposed transmission
inventory; any changed bytes require re-hashing and renewed payload approval.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/AGENTS.md

Hash: 541823b3a74099aeba359715c1b88dd3262344df26a0baea5b2fed2124dbb149

```markdown
# Repository instructions

These instructions apply throughout this repository.

## Read first

Before changing pack behavior or format, read:

1. `specs/overview.md`
2. `specs/architecture.md`
3. `specs/compatibility.md`
4. `specs/pack-format.md`

Before changing `kinflow-starter` content, also read `specs/kinflow-starter.md`.
Before changing installer behavior or artifacts, also read
`specs/installer.md` and `specs/installer-artifacts.md`.
For proposed facet-aware rendering work, additionally read
`specs/facet-rendering-packs.md` and its implementation-plan sequence. This is
specification/planning scope only; it does not authorize successor runtime work.

The files in `specs/` are the normative source of truth. `README.md` is
orientation, pack-local READMEs describe pack status, and code must implement
rather than redefine the specs.

## Authority boundaries

- Spine is the sole authority for installed archetypes, notification profiles,
  bindings, receipts, and ownership.
- Treat packs as declarative, owner-neutral content. Never embed owner IDs,
  delivery targets, subjects, routes, credentials, or environment-specific
  facts in reusable pack content.
- Any future installer must interact with Spine only through Spine's existing
  public command surface. Direct database access is forbidden.
- Do not implement a ledger, scheduler, daemon, or competing runtime here.
- Do not make Spine runtime changes from this repository or modify a Spine
  checkout as part of spine-packs work.
- Do not mutate a released pack version. Add a new version and preserve the
  released artifact.

## Stage discipline

This is a draft-contract repository. The current scope is limited to
`spine.pack-manifest.v1`, the draft installer behavior and machine artifacts in
`specs/installer.md` and `specs/installer-artifacts.md`, and the
medical-appointment, lesson,
game-or-competition, flight, birthday, Education, Social, Travel, and Renewals
and administration, Health, and Home, vehicle, and logistics vertical slices
plus the General commitments vertical slice specified for `kinflow-starter`
draft 10 (compatibility-only successor to draft 9) and its approved unchanged-content
stable release `1.0.0`. Preserve the exact released bytes and all draft artifacts;
future content changes require a new version. The schema-15 alignment
supports the exact Spine `0.5.0` / schema `15` commit recorded in the installer
specs alongside `0.3.0` / `12`; it does not authorize broader runtime ranges.
The bounded 0.6.0 compatibility update additionally admits only Spine commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, runtime `0.6.0` / schema `15`,
and compatibility-only `kinflow-starter 1.0.1-draft.1`. Release finalization
materializes stable `1.0.1` with unchanged definitions and compatibility from
that draft; preserve both files. Installer candidate `0.3.0` and stable pack
`1.0.1` require exact-commit qualification and separate publication approval;
previous publication approval does not carry over.
Do not broaden the schema or pack semantics without matching normative spec,
fixture, and contract-test changes. The authorized runtime scope is the bounded
read-only `plan`, non-mutating apply preflight, Slice 3 initial approved
`apply` with durable checkpointing, and Slice 4 same-execution continuation and
bounded uncertain-response recovery, and Slice 5 non-mutating `verify` in
`src/spine_packs/`, described in
`specs/architecture.md`. Slice 6 disposable local integration qualification is
also authorized: the test harness may initialize a new temporary ledger and
bootstrap synthetic subjects through Spine's public administrative CLIs, then
exercise the installer with isolated synthetic manifests and exact approvals.
It MUST NOT accept an existing ledger or change a Spine checkout. Operator
installations still require a separately supplied target, released pack, and
exact approval. Slice 6 also authorizes local wheel/sdist preparation and
clean-install qualification for GitHub Releases as specified in
`specs/architecture.md`; publication requires the gates in `docs/releases.md`.
Do not add broader recovery, remote
transport, or speculative service/adapter/model directories
without separate review and authorization. Planning must retain its strict
read-command allowlist; apply may use only the six reviewed write commands.
Mark unresolved design details explicitly instead of silently choosing them.

When the repository advances, add only the smallest structure required by real
artifacts. Machine-readable public agreements belong in `contracts/`; runtime
implementation belongs in an explicitly reviewed package layout; explanatory
material belongs in `docs/` only when the README is insufficient.

## Change checks

The facet/rendering proposal inspects exact Spine commit
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7` (`0.9.0`, schema `19`). Existing
runtime allowlists, v1 contracts and pack artifacts remain unchanged. Do not
provision destination disclosure, create items, materialize reminders or send
notifications as part of configuration installation. The staged bounded audit
requires explicit payload approval before any external reviewer invocation.

For documentation, contract, and planner changes, run:

```sh
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests/contract -p 'test_*.py'
python3 -m unittest discover -s tests/runtime -p 'test_*.py'
git diff --check
```

For packaging/resource changes, also run `scripts/qualify_package.py` with
isolated public Spine CLI paths as documented in `docs/releases.md`. Never
substitute an existing operator ledger or publish assets as part of testing.

If a future change introduces executable behavior or a contract, add focused
tests appropriate to that behavior. The repository verifier is a handoff and
structure check, not a substitute for behavior or contract tests.
```

### Spec 2: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/overview.md

Hash: a8e480affee439f5608097d6728a3a96b6765c4aa00f33617711b038bd0d92ab

```markdown
# Overview

## Status and normative language

This document is normative for the draft-contract stage. The terms **MUST**,
**MUST NOT**, **SHOULD**, and **MAY** describe requirements.

## Purpose

Spine Packs provides independently versioned collections of reusable Spine
archetype and notification-profile definitions. An operator will eventually be
able to select a compatible pack, review a deterministic plan, apply approved
changes through Spine, and verify the installed result.

Packs MUST be declarative and owner-neutral. They are distribution artifacts,
not running components and not authoritative installation records.

## Ownership and authority

Spine remains the sole authority for:

- installed archetypes;
- installed notification profiles;
- owner and definition bindings;
- operation and installation receipts; and
- ownership of all installed state.

This repository is authoritative only for the source and released content of
the packs it publishes, together with their compatibility declarations. A pack
MUST NOT claim that content is installed. Installation state MUST be observed
from Spine through its public command surface.

Pack releases MUST be immutable. Corrections or semantic changes after release
MUST use a new version.

A draft is reviewable working content, not a release. Draft content MAY change
while its status remains `draft`, provided its content digest is recomputed.
Changing status to `released` creates the immutable release boundary.

## Content neutrality

A reusable pack MUST NOT contain owner IDs, delivery targets, subjects, routes,
credentials, secrets, or environment-specific facts. Where installation needs
such values, they MUST come from explicit operator input or already-authoritative
Spine state and MUST NOT be written back into the reusable pack.

## Non-goals

This repository MUST NOT provide:

- a Spine daemon, service, or runtime fork;
- an alternative ledger, receipt authority, or scheduling implementation;
- direct reads from or writes to Spine's database;
- changes to Spine runtime behavior;
- owner-specific deployment configuration; or
- an installer before its command mapping and reconciliation behavior receive
  separate review.

An installer may be added after contract review, but its role will be bounded
translation and reconciliation through Spine's existing public commands, not
replacement of Spine authority.
```

### Spec 3: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/architecture.md

Hash: 3c1bebaddd306666ef0f81a2d82bc958c95de0b870e506c34f8997e7e6a99b7e

```markdown
# Architecture

## Proposed facet/rendering successor — not implemented

[facet-rendering-packs.md](facet-rendering-packs.md) proposes a separate manifest
and installer-artifact v2 path for exact Spine `0.9.0` / schema `19` at
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`. It adds a bounded configuration graph:
archetype and facet schema -> facet binding -> rendering definition -> profile
revision -> default binding. The proposal does not expand the runtime authority
or compatibility of the implemented slices below. No disclosure authorization,
item authoring, scheduling or sending belongs to that graph. Read its review
gates before successor work; old v1 behavior and released artifacts remain intact.

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
Read-only planning, non-mutating apply preflight, initial approved apply,
bounded continuation, and non-mutating verification are implemented. Synthetic
tests are supplemented by Slice 6's opt-in real-CLI disposable-ledger tests
below; these do not qualify an existing operator target or a public release.

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

The original slice descriptions below record the `0.3.0` implementation
baseline. Schema-15 alignment adds the exact `0.5.0` baseline and environment
variant specified in `installer.md` Section 3 and `installer-artifacts.md`
Section 7. No command, transport, scheduling, ownership, or recovery scope is
expanded. `spine-readback-0.5.0.schema.json` pins the new `system.info.v3`
response; unchanged catalog/request/receipt validators are shared with `0.3.0`.
Plans bind the public ledger identity on `0.5.0`, and all later operations
require exact environment equality. Existing `0.3.0` artifacts remain valid.

Installer candidate `0.3.0` additionally admits Spine `0.6.0` / schema `15` at
`ad1db8e1a4c7aa9a525612324d08824802a86351`. Its exact system-info-v3 shape is
unchanged, so it explicitly shares the `spine-readback-0.5.0.schema.json`
validator, not a runtime-version alias. Artifact environments retain `0.6.0`
and the ledger identity. CLI read/write allowlists, catalog fingerprints,
receipt handling, and transport/recovery boundaries do not expand. The new
web-read contracts are outside this installer. Qualification must cover all
three pinned baselines; existing published distributions remain unchanged.

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
replay. Both execution paths record `outcome=accepted` after receipt
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

## Slice 4: same-execution continuation

`recovery.py` owns continuation admission, using the existing public observation
and pure execution-evidence boundaries. `apply.py` shares one durable execution
loop between initial and continued apply. No contract schema, command family,
Spine runtime behavior, or package hierarchy is added.

Continuation uses `apply --continue-from SOURCE` with the same required manifest,
plan, approval, checkpoint destination, and result destination as initial apply.
SOURCE MUST be the operator-selected most recent checkpoint or terminal `partial`
result for the execution. There is no implicit discovery, local install registry,
or merging of competing evidence. Schema, digest, size, exact execution identity,
ordered prefix, request derivation, and response/receipt correlation MUST pass
before target use. `applied` and `not_applied` results are not continuation sources;
a completed checkpoint is allowed after a crash before result publication.

The checkpoint and result destinations MUST be new and distinct from SOURCE,
all other inputs, each other, and target files. SOURCE MUST remain unchanged.
SOURCE MUST also be distinct from other inputs and target files; target path
collisions MUST be rejected before opening SOURCE as an artifact.
After successful continuation preflight, the validated or derived checkpoint
MUST be durably published at the new destination before any retry. Subsequent
prepared/advanced publications use Slice 3's durability and no-clobber rules.

Preflight repeats manifest, approval, target, environment, and complete public
catalog checks. It MUST validate the unmodified fresh catalog hashes against
the pinned public projections, then admit exactly one of installer Section 11's
two candidates. On private copies only, inverse comparison validates post-action
definitions, identities, semantics, and available creation/revision provenance
before reversing the explained effects. Recompilation of the original plan
from reconstructed semantic preimages and original snapshots MUST reproduce
the exact sealed plan. This also checks unchanged selected definitions and
remaining-suffix preconditions. Reconstructed entries are comparison inputs,
not claimed historical public readbacks; unknown historical audit/template
fields are neither invented as evidence nor persisted.

Readback IDs for the uncertain action are provisional. They MUST NOT change its
original request, enter accepted evidence, or feed suffix references. Its retry
response MUST match every exposed candidate identity and correlated fact before
the response is recorded and the next action becomes eligible. An uncertain
binding retry uses the exact admitted post-binding identity for the immediate
pre-submission re-read; other bindings retain the original observed-binding
precondition. No-op responses cannot explain unrelated changes.

Spine 0.3.0 has no update provenance for mutable profile metadata and no public
receipt readback. Neither snapshot equality nor current metadata proves a past
receipt or excludes a change-and-restore history. Exact request replay and
validated captured responses remain required, under the single-operator posture.

Continuation preflight failures emit only the specific error envelope and
publish no checkpoint/result; they MUST NOT claim `not_applied` for the existing
execution. After admission, a failed suffix precondition or submission produces
`partial` with the preserved prefix, even if it is empty. Checkpoint durability
failure stops without a fabricated terminal result. A complete accepted
checkpoint with matching fresh state publishes `applied` without writes.

This slice is tested using simulated public commands only. Independent `verify`,
remote transport, release packaging, deployment changes, and actual installation
remain outside its authorization.

## Slice 5: non-mutating verification

`verification.py` validates complete manifest/plan identity, selected closure,
desired semantics, and action coverage before target use. It uses the shared
public observation boundary and pure execution-evidence validator, never the
apply loop, continuation admission, checkpoint writer, or transport `write`.

The CLI is `verify --manifest MANIFEST --plan PLAN [--result RESULT] --output
VERIFICATION`. The target is taken from the saved plan. Selection, approval,
checkpoint, and continuation flags are forbidden. Supplied result paths MUST
be distinct from the manifest, plan, executable, and ledger before they are
opened. Output MUST be new and distinct from every input and target file; it
uses the existing private atomic no-clobber publication rules.

Fresh environment evidence MUST match the planned environment. Catalog reads
use the same owner scoping, full pagination, public schema validation, list/show
agreement, and final snapshot rechecks as planning. Malformed, ambiguous,
incomplete, or changing public reads abort with an error envelope, not a
fabricated missing object or partially observed verification artifact.

All selected objects MUST be active and semantically equivalent for success.
Existing root IDs are pinned to plan classification evidence; newly created
root IDs are taken only from validated captured responses. A changed root ID
is `drifted` even if its semantic projection is equal. Selected bindings MUST
point to those planned roots. Historical revision IDs and binding IDs are not
semantic drift by themselves: a later equivalent revision or same-target
active binding can verify. Captured response correlation and fresh state
comparison are separate facts; verification makes no independent historical
receipt-readback or provenance claim.

The original plan's catalog fingerprints are NOT continuation preconditions
for verify. Fresh fingerprints are recorded; unrelated owner-catalog changes
are not excess definitions and do not fail a valid selected-state comparison.
No inverse reconstruction or retry is performed. Permitted draft inspection
can compare a no-write draft plan successfully, but the result retains its
draft pack identity and does not make that pack installable.

Evidence failure behavior is fixed in installer-artifacts Section 11. Full
valid captured coverage is required for a plan with writes. A no-write plan
normally reports `not_required`; any invalid supplied evidence still prevents
success. `receipt_readback` identifies the pinned runtime as specified in
installer-artifacts Section 11; it never claims independent receipt readback.
Verified results exit 0; completed mismatches exit 10 with the sealed artifact.
Input, target, compatibility, transport, and publication failures use their
existing specific error exits and make no verification-success claim.

This is a simulated-command implementation slice. Disposable-target integration,
supported packaging, releases, and deployment remain Slice 6 or separate work.

## Slice 6 disposable qualification boundary

The opt-in harness in `tests/integration/test_local_spine.py` is test tooling,
not an installer mode. It MUST allocate a new private temporary run directory
and new ledgers; it MUST NOT accept an existing ledger path. Setup may invoke
the public `spine-ledger-migrate --initialize-if-empty` administrative CLI and
`subject.upsert` to create a synthetic owner/actor. These setup permissions do
not broaden the installer's read or six-command write allowlists. The harness
must never open a database or import Spine internals.

Qualification uses each exact inspected Spine commit (`0.3.0`, `0.5.0`, and `0.6.0`) and a compatible
Tickerd distribution, installed in an isolated environment from copied source.
The current Spine checkout is not implicitly compatible. No source checkout
may be edited or switched by the harness. Synthetic test manifests use a
distinct test-only pack identity and stable-version status solely to exercise
apply eligibility; no `kinflow-starter` draft is promoted or published.

Tests MUST retain exact target-bound plans, approvals, checkpoints, results,
fresh verification artifacts, and setup evidence in the private run directory.
Synthetic actor/owner facts belong only to those artifacts. Fault injection
may stop immediately before a public write or discard a real successful write
response; it MUST NOT fabricate successful Spine responses or alter the
ledger directly. Continuation must use the same plan and approval and fresh
artifact destinations. Preserve failed runs for diagnosis; deletion is an
explicit operator action. This qualification does not release software or
authorize an installation into an operator ledger.

## Slice 6 installer packaging

The installer MAY be built as the independently versioned `spine-packs` Python
distribution with the `spine-packs` console entrypoint and unchanged
`python -m spine_packs` entrypoint. Packaging MUST NOT change command behavior,
artifact identities, manifest compatibility, or approval requirements.
The runtime remains standard-library-only, Python 3.11+, local POSIX; build
dependencies are not runtime dependencies. Spine MUST remain an external public
CLI dependency, never bundled code or a Python import.

`contracts/schemas/` remains authoritative. Wheel resources MUST be
byte-identical copies shipped inside `spine_packs/_schemas/`, including every
sibling reference. Installed execution MUST use those resources without a
checkout, network fetch, or fallback to adjacent source contracts. Explicit
source-tree execution MAY continue reading `contracts/schemas/` directly.

The wheel MUST contain only installer runtime, required schemas, and package
metadata. The sdist MUST suffice to rebuild the wheel; its bounded integration
harness and format fixture are test tooling, not a released pack. Neither
distribution may contain curated packs, operator artifacts, ledgers, credentials,
Spine/Tickerd code, or audit payloads. Archive membership and resource byte
identity MUST be checked, and the installed CLI MUST pass disposable-ledger
and recovery qualification outside the checkout with source imports disabled.

GitHub Releases is the initial distribution channel. Installer versions and
`installer-v<version>` tags MUST remain separate from pack versions. Published
tags and asset bytes MUST NOT be replaced; changes require a new version.
Local candidate preparation alone does not satisfy the bounded-review and
exact-commit release gates or authorize publication. Operational steps and
remaining release decisions are in `docs/releases.md`.

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

### Spec 4: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/compatibility.md

Hash: 582877297d3f67895bb9a3f0ac73a8fcb799b84655292f3c0bbe0b1442ff0fdc

```markdown
# Compatibility

## Proposed 0.9.0 successor — not a support claim

[facet-rendering-packs.md](facet-rendering-packs.md) proposes manifest v2 and
installer-artifact v2 against exact Spine commit
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`, runtime `0.9.0`, schema `19`.
The inspected command/contract matrix is in
[the baseline evidence](../docs/facet-rendering-baseline.md). This is planning
only: it does not add 0.9.0 to any existing manifest, schema or runtime allowlist.
The new content and compatibility require successor releases, separately reviewed
machine contracts and exact-baseline qualification. Existing v1 support is unchanged.

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

## Schema-15 alignment

The additional inspected baseline is Spine runtime `0.5.0`, schema `15`, commit
`ab18a8a51c9bf548220f67e2db0220bfe9783888`. Installer `0.2.0` admits
that exact pair in addition to the existing `0.3.0` / `12` baseline. `0.4.0`,
schema 14, future schemas, and undeclared runtime versions remain unsupported.
Installer `0.2.0` passed exact-commit release qualification at `57a6776` on both
baselines. This does not qualify a staging deployment. Publication gates and
the qualification record are in `docs/releases.md` and `docs/release-finalization.md`.

`kinflow-starter.1.0.0-draft.10` preserves every draft-9 definition, binding,
and empty dependency list. It changes only draft identity, runtime allowlist
to `["0.3.0", "0.5.0"]`, and the recomputed digest. The three content contracts
remain unchanged. Drafts 1–9 and their fixture bytes remain review evidence.

Stable `kinflow-starter 1.0.0` promotes draft 10 with the same compatibility
declaration and no definition changes. Only version, release status, and content
digest change; drafts 1–10 remain unchanged. Installer `0.2.0` is required for
the declared `0.5.0` runtime; `0.1.0` does not support that baseline.

The public command map is unchanged, but execution on `0.5.0` requires
`spine.system-info.v3` and `spine.ledger-instance.v1` in place of
`spine.system-info.v2`. The installer MUST bind and recheck the returned
ledger identity as defined in the installer specs. Content compatibility alone
does not bypass this gate. Disposable source and installed-package qualification
MUST cover both supported baselines before publishing the extension.

## Spine 0.6.0 candidate alignment

Installer candidate `0.3.0` adds Spine `0.6.0` / schema `15` at exact commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, retaining both prior baselines.
The inspected CLI contracts and handlers are unchanged from the 0.5.0 pin;
new trusted-web read contracts do not enter the CLI installer union. The exact
runtime and ledger-instance identity remain bound into every plan.

Released `kinflow-starter 1.0.0` still excludes `0.6.0` and MUST fail closed on
that runtime. Its bytes MUST NOT change. The proposed successor is
`1.0.1-draft.1`, adding only `0.6.0` to the exact runtime allowlist, changing
draft identity/status, and recomputing the digest. All 52 archetypes, profiles,
bindings, dependencies, and content contracts remain identical to 1.0.0.
This draft cannot be applied. Stable `1.0.1` promotes it with only version,
release status, and digest changes; it preserves the three-runtime allowlist
and requires installer `0.3.0` for Spine `0.6.0`. The stable artifact is prepared
for publication approval alongside installer `0.3.0`; it is not yet published.
Neither extension
qualifies a staged deployment whose source provenance has not been confirmed.

## Content compatibility is not execution readiness

`spine_content_contracts` is intentionally limited to the contracts that give
the owner-neutral definitions their meaning. It MUST NOT be interpreted as the
complete contract union required to execute `plan`, `apply`, or `verify`.

Spine's command registry may require additional contracts for a concrete
command, including `spine.canonical-json.v1`, notification-profile readback,
catalog cursor, response, or receipt contracts. The draft installer contract
in `specs/installer.md` names the command set and derives the complete
per-command requirement union for each inspected baseline. The installer MUST verify
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
- generalized evidence required to widen compatibility beyond the pinned baselines;
- compatibility declarations for dependency packs; and
- evidence and review required to support installer execution against an
  additional Spine runtime.
```

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/pack-format.md

Hash: 26ce02b87adad016798d9c4999d3631ff6b928e0d536a16642cd293ca97df1e3

```markdown
# Pack format requirements

The proposed facet/rendering successor is specified separately in
[facet-rendering-packs.md](facet-rendering-packs.md). It reserves
`spine.pack-manifest.v2`; it is not implemented and does not amend the closed v1
objects below. No curated successor manifest or release is created by that proposal.

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
Schema Draft 2020-12 implementation. This remains a per-release gate, not a
substitute for semantic validation. During schema-15 alignment, an independent
`jsonschema` 4.26.0 check passed all 12 schema meta-validations and the 35-case
pack fixture matrix (including duplicate-member rejection before schema use).
That working-tree result does not release a pack or qualify a later changed
release candidate automatically.

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

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer.md

Hash: 2b082beb18500968570b6a0b92061dabfcb884c2ceb12f0fbae9737122830f7a

```markdown
# Installer contract

Status: Draft v0.4; runtime through Slice 5, Slice 6 disposable qualification authorized

The separate [facet/rendering proposal](facet-rendering-packs.md) specifies a
potential v2 workflow for Spine 0.9.0/schema 19. Its new command families,
reference resolution and response handling are not implemented or authorized
by this v1 contract. Existing operations, approvals and continuation artifacts
retain the rules below; no implicit artifact migration is permitted.

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
initial approved `apply` with durable checkpointing, bounded same-execution
continuation and uncertain-response recovery, and non-mutating `verify`, using
the layout in `specs/architecture.md`. Slice 6 additionally authorizes local
installer packaging and clean-install qualification for GitHub distribution.
Broader recovery and remote transports require separate review and authorization.
No Spine runtime change is authorized.

Slice 6 additionally permits the separate disposable test setup described in
`specs/architecture.md`. It does not add administrative commands to the installer
or authorize an existing operator ledger. Supported packaging follows successful
source-tree qualification; publishing a release remains a separate decision.

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

The schema-15 alignment additionally pins runtime `0.5.0`, ledger schema `15`,
at commit `ab18a8a51c9bf548220f67e2db0220bfe9783888`. Runtime `0.6.0`, schema `15`,
is additionally pinned at `ad1db8e1a4c7aa9a525612324d08824802a86351`.
Only these three exact
runtime/schema pairs are admitted; neither a version range nor schema 14 is
supported. The six catalog write handlers, catalog readback/fingerprint shapes,
and embedded command contracts retain the original public semantics. The ledger
module's command-derived-ID import moved to `spine.core.hashing`; this is not
a new installer interface or permission to import Spine internals.

The 0.5.0-to-0.6.0 comparison found byte-identical command registry/handlers,
core and ledger code, and the public system-info-v3 and catalog command/readback
schemas used here. The new web-read contracts and web cursor v2 do not replace
the CLI catalog cursor contract or enter this installer's execution union.
The runtime-dependent environment still records exactly `0.6.0`, never `0.5.0`.

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

For runtimes `0.5.0` and `0.6.0`, the exact sorted union replaces `spine.system-info.v2`
with `spine.system-info.v3` and adds `spine.ledger-instance.v1` (ten contracts).
The command allowlists do not change. Public `system.info.v3` additionally
requires `ledger_instance_id`; the installer MUST validate, preserve, and bind
it into plan environment evidence. Initial apply, continuation, and verify
MUST reject a changed identity even if paths and catalog contents still match.
This does not replace the single-operator/no-concurrent-writer requirement or
provide atomic protection against filesystem replacement between commands.

`system.info` MUST succeed before catalog interpretation. Its exact
`runtime_version` MUST appear in the pack manifest's runtime allowlist, every
manifest content contract MUST be advertised, and every contract in the
execution union above MUST be advertised. A mismatch fails before a plan is
classified. Content compatibility is not sufficient evidence of execution
readiness.

Supporting any other Spine runtime requires a separately reviewed command map
and execution-contract union. A pack allowing only `0.3.0` MUST still be
rejected on `0.5.0`; installer support does not widen a manifest's allowlist.

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
spine-packs verify --manifest MANIFEST --plan PLAN [--result RESULT] --output VERIFICATION
```

The manifest is explicit so verification can reload the exact complete pack.
`--result` is optional at the CLI boundary: a plan with writes and no supplied
result produces verification mismatch, never successful receipt evidence.
No-write plans need no result. The target and selection come only from the plan;
verify accepts no fresh selection, approval, checkpoint, or continuation flags.

Paths, executable locations, database paths passed through to the Spine CLI,
credentials for a future transport, and similar environment facts are
transport configuration. They MUST NOT enter a pack or its content digest.
Passing a database path to `spine-command` does not authorize the installer to
open that database itself.

The local v1 request MUST name an observable target binding containing the
normalized local host, resolved Spine command executable path and hash, and
resolved ledger path. These facts are recorded in the plan and checked again
by `apply`.
They do not become pack content. On `0.5.0` and `0.6.0`, the separately observed ledger
identity is also bound in environment evidence as required in Section 3.

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
   current schema, contract facts, and (on `0.5.0`/`0.6.0`) ledger identity;
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
plan evidence, validated Spine responses for that prefix, and fresh public
readback, the installer MUST validate the exact catalog state expected after
the prefix. The snapshot component MAY be checked by the inverse fingerprint
comparison in `specs/installer-artifacts.md` Section 9.1; this does not require
persisting complete original catalogs or deriving a new digest from an old
digest alone. It does not replace full selected-object semantic and identity
checks. Generated Spine IDs and revision IDs used by later actions MUST come
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

For case 2, IDs obtained from fresh public readback are provisional candidate
facts, not accepted response evidence. Before retry, the installer MUST validate
the candidate's complete relevant public definition, desired semantics, and
available creation/revision provenance against the exact planned command and
execution. It MUST NOT substitute those IDs into the original request or use
them to advance the suffix. The retry response MUST additionally match the
candidate's observed root, revision, and binding IDs wherever the public
response exposes them before acceptance is recorded and execution advances.
A reconstructed fingerprint match alone MUST NOT authorize recovery.

Spine makes each command atomic, but the command family provides no
whole-pack transaction. An apply result therefore has one of these states:

- `applied`: every planned action succeeded or compatibly replayed;
- `partial`: a deterministic prefix succeeded and a later action failed; or
- `not_applied`: preflight failed or no action was submitted.

The accepted prefix may be empty: a failure after the first write transport
invocation is still `partial`, because its commit outcome may be uncertain.
`not_applied` MUST NOT be inferred merely from the absence of accepted response
evidence. The initial and continuation implementation boundaries and durability-failure
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

Neither pinned Spine baseline exposes a public command-receipt show or list command. Replaying
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

- atomic expected-current or expected-absent preconditions for
  `notification_profile.binding.set`; and
- public command-receipt readback for independent recovery and later audit.

None of this future hardening authorizes a Spine change from this repository.
Any such capability must be proposed, reviewed, and implemented in the Spine
repository as a separate body of work.

Stable ledger identity is no longer deferred for the `0.5.0`/`0.6.0` baselines; Section 3
requires its use. The `0.3.0` baseline retains its weaker observable binding.
```

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer-artifacts.md

Hash: e3f977e2cdc09c12993e4fa20e6da83e320d1635050c8f367429aa9f62e3769e

```markdown
# Installer artifact contracts

Status: Draft v0.1; runtime through Slice 5, Slice 6 disposable qualification authorized

[facet-rendering-packs.md](facet-rendering-packs.md) proposes separately named v2
artifacts for new object/reference families, public observation preimages and
family-specific receipt evidence. Exact schemas/fixtures require review before
implementation. Do not widen the closed v1 shapes below or treat a new catalog's
opaque cursor as the existing public `catalog_snapshot_hash` evidence.

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

The schema-15 extension retains these draft v1 identifiers and existing
`0.3.0` artifact bytes/digests. Its new closed environment variant is identified
by `runtime_version=0.5.0`. Older installer `0.1.0` cannot consume that variant
and MUST reject it rather than discard identity evidence. New approvals are
required for new plans; no artifact migration or rewriting is implied.

The 0.6.0 extension adds another closed environment variant without changing
existing artifact bytes or identifiers. Installer `0.2.0` MUST reject it.
Runtime changes require a fresh plan and approval even if schema and ledger
identity are unchanged. No artifact may relabel a 0.6.0 observation as 0.5.0.

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

Environment is exactly one of three closed shapes:

- `0.3.0`: implemented/current schema both `12`, advertised contracts, and no
  ledger-instance field (the original shape).
- `0.5.0`: implemented/current schema both `15`, advertised contracts, and
  required `ledger_instance_id` matching `^ledger_instance_[0-9a-f]{64}$`.
- `0.6.0`: the same fields and schema-15 constraints as `0.5.0`, but with its
  own exact runtime value. Unknown runtime/schema pairs remain invalid.

The latter identity MUST come from validated public `system.info.v3`, never
from a path hash or local database read. It participates in plan/verification
digests and exact environment comparisons during initial apply, continuation,
and verify. Missing, malformed, or changed identity fails closed. The required
execution union is runtime-specific; mixing the two unions is invalid.

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

Every `item_archetype.create`, `notification_profile.create`, and
`notification_profile.binding.set` template MUST carry an `owner` exactly equal
to the plan's `request.owner`. Plan semantic validation MUST enforce this for
every such action, including creates with no result-reference consumers.
A system owner or a different subject/group owner fails as invalid artifact
input before target observation. This installer restriction supplements the
pinned public Spine owner shape; it does not narrow or redefine that schema.

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

### 9.1 Continuation snapshot comparison

For all pinned Spine baselines in `specs/installer.md` Section 3, continuation
MAY validate the snapshot component by reconstructing the original fingerprint
from fresh public readback. This is a comparison technique, not rollback,
receipt evidence, or an alternative installation ledger. It changes no artifact
fields, contract identifiers, or digest derivations. The authorized Slice 4
implementation boundary is recorded in `specs/architecture.md`.

The exact Spine snapshot preimages are ordered arrays of closed row projections:

| Catalog | Row fields | Ordering / scope |
| --- | --- | --- |
| Archetypes | `id`, `key`, `status`, `current_revision_id` | `(key, id)`; all active and retired roots under the exact plan owner |
| Profiles | `id`, `key`, `status`, `current_revision_id`, `display_name`, `description` | `(key, id)`; all active and retired roots under the exact plan owner |
| Bindings | `notification_profile_binding_id`, `item_archetype_id`, `notification_profile_id`, `status` | `(item_archetype_id, notification_profile_binding_id)`; active bindings under the exact plan owner |

For root projections, `id` and `key` are the public root ID and archetype/profile
key, respectively. Each fingerprint is lowercase SHA-256 over the array's exact
`spine.canonical-json.v1` UTF-8 bytes, with no added wrapper or owner field.
This pins `_list_roots` and `_binding_list` in Spine's
`src/spine/commands/notification_profiles.py` at the inspected baseline; it does
not claim that a differently versioned runtime uses the same derivation.

Before inverse comparison, the installer MUST validate and exhaust fresh public
readbacks with the same owner scope, filters, ordering, and consistency checks
as planning. Each unmodified projection's recomputed hash MUST equal its fresh
Spine `catalog_snapshot_hash`. A mismatch fails closed, not by substituting a
locally invented hash. The original plan hashes MUST remain unchanged.

For each permitted candidate in installer Section 11, the installer MUST first
validate the candidate-specific full selected-object state, prefix evidence,
and remaining-suffix preconditions under that candidate. Then, on a private
in-memory copy of the fresh projections, it MAY reverse only that candidate's
explained effects, in reverse action order:

- A create removes the exact validated post-create root projection.
- A revision restores that root's `expected_current_revision_id`.
- A metadata update restores the exact `expected_metadata`.
- A binding set removes the exact validated post-binding projection and restores
  the classification's original `observed_binding` with `status=active`, or
  restores absence when `observed_binding=null`.

Each inverse step MUST match the action's expected effect for that candidate
at that reverse step. A validated no-op leaves the projection unchanged. Known
response IDs MUST match; the single uncertain action uses only provisional validated public
readback facts subject to installer Section 11's retry-correlation rule. No
other unrecorded action may be explained. All untouched entries and fields,
including unselected catalog entries, MUST be preserved exactly. Missing,
ambiguous, contradictory, or unavailable required evidence fails closed.

Re-sort and hash each reconstructed projection by the rules above. All three
hashes MUST equal the original `plan.catalog_snapshots` digests. A mismatch
rejects that candidate; recovery may proceed only under installer Section 11's
bounded candidate rules and all its other gates. The calculation MUST NOT alter
Spine, the plan, approval, checkpoint, or preserved response evidence.

Fingerprint equality MUST NOT substitute for public-contract validation, full
semantic comparison, exact replay-response correlation, or checkpoint durability.
These hashes do not contain revision bodies, audit history, or receipt rows.
They detect fingerprint-visible state differences, not every intervening write
(for example, metadata changed and later restored). The single-operator posture
and Spine's immutable revision guarantees remain required; no historical-write
or independent receipt-readback claim is introduced.

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

For successful verification of a plan with writes, `apply_result_digest` is
required and `response_evidence` must be `complete`; for successful verification
of a no-write plan it is null and response evidence is `not_required`.
`missing` or `invalid` response evidence
forces overall mismatch. Fresh object states must all be `equivalent` for
overall verification success.

A missing apply result for a plan with writes is represented by null
`apply_result_digest` and `response_evidence=missing`. A supplied, well-formed,
digest-valid partial/not-applied result with valid correlation also has missing
coverage; its digest is retained for a plan with writes. A supplied artifact
whose syntax, outer schema, digest, or size is invalid fails as invalid input
before catalog reads, without emitting a verification artifact. A digest-valid
artifact with invalid embedded evidence, execution/approval/plan correlation,
ordering, or terminal-state coverage instead produces `response_evidence=invalid`
and overall mismatch after fresh observation. Invalid supplied evidence MUST
NOT be ignored even for a no-write plan; that mismatch retains a null result
digest because no write result is required by that plan.

Verification compares the recorded approval digest with the unique closed v1
approval preimage determined by the plan's decision actions, the result's
execution, and the two required true assertions. This is checksum correlation
only: it does not issue approval, authenticate its author, or authorize writes.
All captured requests and responses are revalidated using those execution
facts. No additional approval file or Spine receipt-readback command is implied.

`receipt_readback` MUST be `captured_responses_only_spine_0.3.0` for a `0.3.0`
environment, `captured_responses_only_spine_0.5.0` for a `0.5.0` environment,
and `captured_responses_only_spine_0.6.0` for a `0.6.0` environment.
Cross-pairing is invalid. None claims independent command-receipt readback;
none of the inspected baselines provides a public receipt show/list command.

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
- verification mismatch, runtime-specific receipt-readback disclosures for all
  pinned Spine baselines, and rejection of cross-paired disclosures; and
- exact envelope status/category/exit-code correlation.

The first fixture slice may use one complete vertical flow plus focused
negative mutations, but missing required cases remain contract work rather
than silently becoming implementation assumptions.

## 14. Deferred implementation details

The authorized planning, preflight, initial-apply, bounded continuation, and verification
slices use the source-tree `spine_packs` package and standard-library `argparse`,
as recorded in `specs/architecture.md`. This does not authorize broader recovery
implementation. Slice 6 packaging follows `specs/architecture.md` without changing
artifact contracts; publication remains separately gated. General filesystem
configuration remains deferred. It does not add section bundles,
remote transports, signatures, install registries, credentials, Windows path
semantics, or Spine runtime changes.
```

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: 9b6b0cd5e9aebf934c4c829aaae93008d0a4580cbf8392c2fb7c2af89ecb1a55

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
not a reopening of completed installer Slices 1–6. The only currently authorized
work is specification/planning and staging a bounded audit. No runtime, machine
schema implementation, curated pack rewrite, deployment, release or external
review is authorized here. Source baseline: Spine
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`, `0.9.0` / `19`.

Use vertical delivery around one flight graph, with a focused contract review
before each runtime boundary. Do not first convert all 52 starter archetypes.

Blocking upstream gate: source inspection found that the exact baseline's v2
profile-list handler enters the legacy rejection path for v2 revisions. See
`docs/facet-rendering-baseline.md`. A separately authorized public-CLI disposable
reproduction must resolve that finding before runtime implementation is treated
as buildable against this pin. If it requires a Spine fix, seek explicit approval
of its replacement commit; no newer baseline or list bypass is implicit.

| Slice | Deliverable | Exit gate before the next slice |
| --- | --- | --- |
| FR-0: proposal and bounded audit staging | Proposed manifest v2, reference graph, command/contract inventory, failure/recovery rules, product decisions, audit payload | Operator authorizes exact reviewer payload; reviewer-only consistency pass, findings disposition and accepted scope. No external run has occurred |
| FR-1: machine agreements and fixture proof | Manifest v2; seven v2 installer artifact schemas, shared/embedded/readback closure; synthetic scalar + location-label flight flow; independent hash and reference vectors | Resolve the upstream readback gate; Draft 2020-12 meta/fixture validation, semantic tests, unchanged v1 vectors and bounded machine-contract review. Fix exact reference-slot syntax and aggregate observation budgets before code |
| FR-2: read-only flight plan | Exact 0.9.0 preflight, protected cursor prerequisites, complete public observation view, dependency closure, cascaded drift and typed outputs | Missing/retain/drift/retired and mixed v1/v2 readback tests; all pagination/capacity/staleness failures; no writes even dry-run. No release compatibility claim |
| FR-3: approved initial flight apply | New command-specific serializers/evidence validators; ordered dependencies; durable prepared/accepted checkpoints; no-op and binding guards | Every one of the 11 write kinds, all ID-consuming paths and every durability boundary tested; no item/disclosure/send commands; no speculative IDs or automatic drift updates |
| FR-4: same-execution recovery and verify | Forward expected-state comparison from bounded preimages; prefix/prefix-plus-one recovery; exact request replay; read-only exact-pin verification | Lost responses for schema/rendering create/publish, both binding kinds and nested profile refs; unrelated drift rejected; receipt limitations explicit; every old recovery/verify test preserved |
| FR-5: disposable and installed-package qualification | Exact pinned Spine build, isolated temporary catalogs, synthetic owner and protected test cursor configs via separately authorized setup; source and clean-wheel plan/apply/replay/verify | All v1 supported-baseline regression gates plus exact 0.9.0 public-CLI qualification. No existing ledger, item creation, materialization, sends, disclosure grants or Spine checkout edits |
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
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/facet-rendering-packs.md

Hash: cb33c6e22bd45511aed1f1d29bc1d309ad774a6a0574ddbf17a625f7e5149448

```markdown
# Facet-aware packs: successor contract proposal

Status: proposed; specification and implementation planning only, not accepted
or implemented. Baseline inspected on 2026-10-10. Normative language below defines
the proposed successor, not additional authority for the current installer.

## 1. Scope and authority

Propose `spine.pack-manifest.v2` and a separately versioned v2 installer-artifact
family for one flight configuration vertical slice. Preserve v1 decoders,
schemas, fixtures, installer behavior and every released/draft pack artifact.
Do not add rendering fields to a frozen v1 shape or relabel v1 content as v2.

The exact reference is Spine `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`, runtime
`0.9.0`, implemented/current ledger schema `19`. The object was resolved from
`01ebce7` and inspected through its Git tree, not a newer working tree.
[Baseline evidence](../docs/facet-rendering-baseline.md) records public contracts,
wire differences and qualification gaps. Existing installer `0.3.0` does not
support this baseline. This proposal neither widens its allowlist nor qualifies
a target installation.

Source inspection also found a baseline readback blocker: the v2 profile-list
path calls a legacy list that rejects v2 revisions before successor projection.
See the baseline evidence. Reproduce through the exact public CLI in a separately
authorized disposable investigation before runtime work. Do not work around it
by skipping catalogs, using internal reads, or silently changing the source pin.
If confirmed, a Spine-owned repair and an explicitly approved replacement baseline
are prerequisites to qualifying this proposal; no repair is authorized here.

Spine alone owns validation, authorization, installed catalogs, immutable
revisions, ownership, receipts, rendering, scheduling and historical evidence.
Packs provision configuration through public commands only. Direct database
access, internal Spine imports, runtime changes, deployment and publication are
forbidden in this task. No item creation, facet-value attachment, schedule/profile
application, materialization, notification sending or disclosure management is
an installer operation. No owner, subject/location ID, destination, route,
credential, cursor secret or environment-specific fact belongs in reusable content.
A declaration of a reference *type* is not an actual reference value.

Installation approval is not disclosure approval. Definition selection in a
profile declares an intended rendering, not permission for a destination to
receive it. The installer MUST NOT provision, resolve, inspect or revoke disclosure
authorizations. The handoff MUST report this separate operator requirement.

## 2. Smallest successor manifest

Keep the v1 root members and add exactly `facet_schemas`,
`archetype_facet_bindings`, and `rendering_definitions`. All are required arrays;
empty arrays mean no such desired objects. Retain `dependencies=[]`: these are
intra-manifest references, not inter-pack dependencies or a package resolver.
Retain v1 pack identity/status/version grammar and the draft inspection-only gate.
Do not assign a release version or create a curated manifest in this task.

All objects are closed. Require UTF-8, duplicate-key rejection, no JSON numbers,
valid Unicode, bounded bytes, canonical decimal strings and fail-closed unknown
fields. Preserve v1 timing/late-handling semantics and limits; rendering cannot
add duplicate timing templates or bypass the existing spacing rule.

| Object | Complete owner-neutral members / proposed change |
| --- | --- |
| Archetype | Existing `archetype_key`, `intended_status=active`, `revision`; revision unchanged |
| Facet schema | `schema_key`, `intended_status=active`, `definition` |
| Archetype facet binding | `archetype_key`, `facet_key`, `schema_ref: {schema_key}` |
| Rendering definition | `definition_key`, `intended_status=active`, `revision` |
| Notification profile | Existing key/status/metadata/revision; every template additionally requires explicit `rendering` |
| Default binding intent | Existing `binding_kind=archetype_default`, archetype key and profile key; unchanged |

`definition` uses Spine's `archetype-facet-types.schema.json#/$defs/normalizedDefinition`:
display name, nullable description, compatible item types and 1–32 field
declarations. Require explicit `queryable` as well as `required`; no implicit
authoring default. Support the exact Spine scalar declarations (`text`, `enum`,
`boolean`, `integer`, `date`) and typed `reference` declarations. No arbitrary
JSON Schema, scripts, expressions, defaults or actual item values. Subject
references may be declared but cannot be selected by rendering.

Rendering `revision` mirrors Spine's definition revision, except each selection
replaces `facet_schema_revision_id` with `schema_ref: {schema_key}`. Other members
remain `display_name`, nullable `description`, `compatible_item_types`,
`base_rendering_contract`, `base_rendering_profile`, and ordered `selections`.
Each selection is exactly `selection_key`, `facet_key`, `schema_ref`, `field_key`,
`label`, `projection`. The base constants are `spine.notification-rendering.v1`
and `spine.notification-rendering.concise-en-ca.v1` respectively. There are 1–8
selections; labels are bounded by Spine's 40-scalar normalized limit.

Template rendering is exactly one of:

```json
{"kind":"ordinary"}
```

```json
{"kind":"definition","definition_ref":{"definition_key":"flight_details"}}
```

These are illustrative fragments, not complete manifests. There is no
disclosure ID, effective selection subset, ordinary-on-error flag, wildcard,
latest selector or environment substitution. A definition pin is translated
to Spine's exact root/revision pair, never to a profile default or a runtime lookup.

Validate selected field existence and type: `value` only for the five scalar
types; `location_label` only for `reference` with `target_kind=location`.
For every archetype/default-profile association, each nonordinary template's
selections MUST have matching pack-declared facet bindings by facet key and
schema reference, with compatible item types. Rendering/profile compatibility
must cover their uses; do not silently narrow declared types. This supplements,
not replaces, Spine's authoritative validation. A rendering may be shared where
these exact conditions hold. It is not archetype inference from free text.

## 3. Ordering, normalization and portable identity

Require unique keys per object family and exactly one desired definition per
root key in one manifest. One manifest does not publish a history of revisions.
Facet-binding identity is `(archetype_key, facet_key)`; default-binding identity
remains archetype key (at most one default per archetype).

Sort archetypes, schemas, rendering definitions and profiles by their root key;
facet bindings by `(archetype_key, facet_key)`; defaults by archetype key;
schema fields by field key; enum choices, compatible types and contract lists
lexicographically; profile templates by template key. Reject duplicate identities
and noncanonical ordering rather than repairing a signed/digested manifest.
**Rendering selection order is authored presentation order**, not lexical order.
Preserve and hash it; reject duplicate selection keys and duplicate
`(facet_key, schema_ref.schema_key, field_key)` sources regardless of labels.

Pack authors MUST supply the normalized semantic forms expected by the pinned
Spine contracts. Reject non-NFC schema definitions, omitted queryable flags or
rendering display/label text that would change under Spine normalization. Do
not apply facet NFC rules indiscriminately to other catalogs. Canonical JSON
itself performs no Unicode normalization. Validation must check both the pack
rules and the appropriate catalog-specific normalization before hashing.

Keep `content_identity` exactly `{algorithm, canonical_json_version, digest}`
with SHA-256 and `spine.canonical-json.v1`. As in v1, hash canonical UTF-8 of
`{canonical_json_version: "spine.canonical-json.v1", derivation_version:
"spine-pack-content-sha256.v2", manifest: <complete manifest with
content_identity omitted>}`. The digest names portable bytes with local references.
It is NOT any installed Spine revision hash: those hashes include resolved
ledger-specific revision IDs and use their owning derivations. Do not compare
a pack digest to a Spine definition hash or persist a resolved manifest as a
replacement for the released portable artifact.

Codification must retain the existing 256-object bounds for existing collections,
use at most 256 schemas, rendering definitions and facet-binding declarations
per collection. This is an installer bound, not a claim about how many optional
bindings Spine permits or how many facets an item can hold. Retain the existing manifest
input byte bound (16 MiB) and installer artifact byte bounds; reject overflow, never truncate
a dependency closure. Upstream per-definition/request limits also apply *after*
ID resolution. A flight proof does not justify unbounded generic graph traversal.

## 4. Local reference resolution and selection

A local key identifies the sole desired definition in this immutable manifest.
Its effective identity is `(manifest digest, object kind, key)`, not a guessed
Spine revision number or a globally meaningful key. No pack-authored ledger IDs,
cross-pack lookup, external catalog aliases or cycles are accepted.

Validate the entire manifest before selection. Keep explicit `all` or sorted
archetype-key selection and existing noninteractive CLI semantics. An archetype
unit includes that archetype, all its declared facet bindings and schemas, its
default profile if present, that profile's rendering definitions, and their
schema dependencies. Deduplicate shared objects by typed local key. `all` also
includes unreferenced declared objects; granular selection does not. Do not
automatically select other archetypes sharing those objects. Report shared-root
updates as having possible effects on future uses outside the selected unit;
never claim isolation of a shared catalog root.

For each root resolve only `(explicit installation owner, exact root key)`:

1. Equivalent active current revision: retain root and that exact current
   revision ID from validated public list/show readback.
2. Absent root: plan create; root/revision outputs are unknown until acceptance.
3. Active drift: plan an explicitly approved publish/revise against the observed
   current revision. Retain its root ID but leave its new revision unresolved.
4. Retired, inaccessible, ambiguous or invalid readback: block, never recreate,
   adopt a foreign owner, or search history for a convenient match.

Do not select an equivalent historical revision behind a differing current
pointer as a hidden conflict workaround. Exact historical show is used to
validate observed pins and accepted results, not to choose a different desired
revision. Equal content on another root is not equivalence.

The plan carries an explicit typed resolution table: local object, observed
root/current revision, and each required output supplied either by an observed
literal or by a unique earlier action plus a closed response JSON pointer.
Plan templates use typed reference slots, not general string interpolation.
Only these new ID-consuming paths are added to the reviewed mapping:

| Consumer input | Producer output when unresolved |
| --- | --- |
| Facet binding `item_archetype_id` | Archetype create `/item_archetype_id` |
| Facet binding `facet_schema_revision_id` | Schema create/publish `/facet_schema_revision_id` |
| Rendering revision `selections/<index>/facet_schema_revision_id` | Schema create/publish `/facet_schema_revision_id` |
| Profile template `rendering.definition.notification_rendering_definition_id` | Rendering create `/record/notification_rendering_definition_id` |
| Profile template `rendering.definition.notification_rendering_definition_revision_id` | Rendering create/publish `/record/notification_rendering_definition_revision_id` |
| Default binding root IDs | Existing archetype/profile create output mappings |

Indices identify the already approved ordered arrays; they are not JSONPath
expressions. No arbitrary pointer, recursive evaluation, forward/self reference
or interpolation in names/labels is allowed. A publish supplies a revision,
not a replacement root. Literal roots and observed preconditions are also
correlated to their local objects and exact owner. Materialize only from the
contiguous accepted prefix; validate the complete public request before its
durable prepared checkpoint. Never predict a generated ID or hash to advance.

## 5. Comparison and installation ordering

Compare normalized semantic fields AND exact resolved identities. Hashes
corroborate but do not replace semantic validation. Use separate portable desired
and installed observed representations so ledger IDs never leak into pack bytes.

| Object | Retain / drift / authorized write |
| --- | --- |
| Archetype | Existing metadata/type comparison; create or expected-revision revise |
| Schema | Complete normalized definition including metadata, required/queryable flags and field declarations; create or expected-revision publish |
| Facet binding | Same archetype root, facet key and exact schema revision; set with explicit `expected_binding_id`, null only for absence |
| Rendering | Complete normalized revision, ordered selections and exact resolved schema revision pins; create or expected-revision publish |
| Profile | Existing separate mutable metadata and revision comparisons; compare rendering root/revision pins per template; v2 create/revise, unchanged metadata-update command |
| Default binding | Existing exact archetype/profile roots, with immediate public pre-write recheck; no new CAS assumed |

A producer's pending revision makes each affected retained-looking consumer a
planned update: equal local keys do not hide a changed future pin. For example,
schema publish may require facet binding set, rendering publish and profile
revise. Expose and separately authorize every such cascading update before any
write; do not discover extra writes mid-apply. Render labels/ordering changes
are real revision drift even if timing is unchanged.

Profile v2 readback selects the stored revision's v1/v2 decoder. A historical
v1 all-ordinary revision may be retained when its semantic content is identical
to an all-ordinary desired revision; do not rehash its evidence as v2. Any actual
revision write in this successor workflow uses the v2 selector, with explicit
ordinary or definition rendering on every template. A v1 revise cannot clear
or demote a v2 profile. Metadata-only updates retain their existing selector.

Deterministic phase order, lexical root keys within a phase:

1. Archetype create/revise.
2. Facet schema create/publish.
3. Archetype facet binding sets, by archetype and facet key.
4. Rendering definition create/publish.
5. Profile creates, then metadata updates, then revisions.
6. Default-profile binding sets.

Missing definitions are creates; equivalent definitions have retain classifications
and no command/receipt. Drift fails closed without exact plan approval naming
every update. Blocked dependencies block their consumers and the complete selected
apply. No apply-only-missing shortcut, renaming, retirement, removal, compensation,
automatic policy reapplication or facet snapshot upgrade is permitted.

Catalog changes affect future uses; existing item assignments, facets, policies,
started attempts and historical decoders retain Spine's exact revision evidence.
Bindings are root-level configuration; this proposal does not pretend a facet
binding is part of an immutable archetype revision.

## 6. Compatibility and command boundary

The first v2 pack declares exactly runtime `["0.9.0"]`. Content contracts are:

```text
spine.archetype-facet-bindings.v1
spine.facet-schemas.v1
spine.item-archetypes.v1
spine.notification-profile-bindings.v1
spine.notification-profiles.v2
spine.notification-rendering-definitions.v1
spine.notification-rendering.v1
```

The concise base-renderer profile is a literal algorithm identifier, not a
separately advertised contract. Execution readiness additionally requires the
exact 17-contract registry union in the baseline evidence. Do not infer extra
command authority from a contract's presence. Both implemented/current schema
must be `19`; bind the actual public ledger-instance ID and exact runtime into
plan, approval correlation, continuation and verify. Existing target executable
path/hash and local single-operator rules remain.

`system.info` supplies runtime/schema/contracts/ledger identity, **not Git commit
provenance**. Exact-commit qualification must build from the pinned tree and
record artifact provenance; deployment must separately verify its installed
package against that qualified artifact. Hashing a console-script launcher is
not proof of its imported package bytes. This task makes no installed-target
or clean-wheel qualification claim and may not silently substitute HEAD.

The proposed allowlist is the existing six reads plus `facet_schema.list/show`,
`item_archetype.facet_binding.list`, and
`notification_rendering_definition.list/show` (11 reads); the existing six
writes plus `facet_schema.create/publish`, `item_archetype.facet_binding.set`,
and `notification_rendering_definition.create/publish` (11 writes). Profile
create/revise/list/show use v2 selectors. Exact request mappings and the union
are in the baseline evidence. No write, even dry-run, is available to plan/verify.
No retirement, binding removal, disclosure, access provisioning, item, schedule,
reminder, worker or administrative command enters either allowlist.

The operator provisions protected `SPINE_FACET_CURSOR_CONFIG` and
`SPINE_RENDERING_CURSOR_CONFIG` for the child Spine CLI. Their formats differ;
the latter binds the ledger-instance ID. The installer must not generate keys,
read/log secret contents, serialize them in artifacts, or weaken Spine's file
permission checks. Missing/invalid configuration fails before an applicable
plan, including when a list would fit on one page. Configuration rotation
does not authorize decoding/reissuing a cursor. Requests contain no secrets.

## 7. Observation and successor evidence

V1's three public `catalog_snapshot_hash` values are not a universal abstraction:
facet schema/binding lists and rendering definition lists do NOT return them.
Their signed cursor internals are not public snapshot evidence. Never decode
tokens, manufacture a Spine fingerprint, or apply the old inverse-hash routine
unchanged to these catalogs.

Propose v2 artifacts retaining a bounded, canonical **public observation view**
as plan evidence. It contains complete owner-scoped active/retired archetype,
profile, schema and rendering root inventories with validated current revisions,
and active default/facet bindings (facet bindings enumerated per observed owner
archetype). Include exact historical revisions needed to interpret selected
existing pins, addressed by IDs discovered through those public reads. Do not
read unrelated items, actual facet values or disclosure catalogs.

Validate every family-specific envelope, owner, root/revision membership, hash,
ordering and pagination condition; exhaust each status independently with fixed
filters/limit. Match show to list facts and selected exact revisions to pins.
Collect a second complete view and require semantic/identity equality after
sorting, excluding opaque cursors, pagination segmentation and invocation noise.
Fail on stale cursors, changing views, missing pages, repeated IDs/tokens,
incomplete readback, response/time/byte overflow or source capacity failure.
No internal retries that mix observations. Retain old public fingerprints as
corroborating evidence where supplied; locally computed view digests MUST be
labelled installer evidence, never Spine attestations.

Facet pagination has a 100-candidate/resource ceiling over the bounded source,
not unlimited total capacity obtained by using smaller pages. Rendering lists
are bounded keyset pages (100 maximum); profile v2 lists retain 500 maximum.
Exceeding a Spine or artifact bound blocks this installer workflow; no partial
catalog, selected-only fallback or database inspection is permitted. Codification
must bound aggregate calls/bytes/time as well as individual responses and prove
termination for malicious endless/duplicate pagination before runtime work.

Under the acknowledged single-operator/no-concurrent-catalog-writer condition,
repeat the full view immediately before initial apply and compare with the plan.
This is not an atomic cross-command snapshot, history-of-writes proof or ABA
detector. No multi-writer guarantee is claimed. Preserve the full bounded preimage
to compare forward prefix effects; do not enlarge limits silently to fit a ledger.

Propose the seven existing artifact kinds with `.v2` identifiers, shared types
and embedded public-value schemas versioned separately. Bind manifest v2, the
0.9.0 environment, typed graph/closure and resolution slots, complete observation
preimages/digests, new action kinds and family-tagged response evidence. Preserve
all v1 readers/writers and bytes; reject mixed artifact versions before target
access. Carry existing limits, private/no-clobber publication, approval semantics
and exit codes forward unless machine-contract review identifies a concrete gap.
Use v2 digest domains and `spine.pack-command-id.v2` for v2 actions; never reinterpret
a v1 checkpoint. Exact artifact layouts and hash vectors are the next reviewed
codification deliverable, not implementation discretion.

## 8. Replay, checkpointing and partial failure

Keep a single deterministic action sequence and a contiguous accepted prefix.
Before each submission durably preserve the exact canonical request, digest,
command ID, execution/actor/time and prior accepted responses using the existing
file fsync / atomic replacement / directory fsync discipline. No submission
before prepared durability; no consumer before validated response durability.
Re-derive and byte-compare requests from the saved plan and accepted prefix on
continuation. Never fill an unresolved output from uncorrelated fresh readback.

Validate response evidence by family, not through a fabricated common receipt:

- Existing catalogs and profile v2 return a nested receipt with semantic request
  hash. V2 profile admission normalizes the request before receipt creation;
  require materialized requests to already have that exact normalized form,
  correlate the hash to those submitted bytes, and preserve the
  stored revision decoder/hash. Do not invent a replay boolean they do not expose.
- Facets return top-level command/receipt IDs, effect, changed/replayed, prior
  and resulting revision/binding facts; audit ID is absent on no-op. They expose
  no receipt semantic hash or actor/time provenance in schema show.
- Rendering returns `contract_version` (not `response_contract`), top-level
  command/receipt/audit facts and a `record` with root/revision, definition and
  create/publish provenance. No-op still carries an audit; replay retains the
  stored outcome with `changed=false`. It exposes no receipt semantic hash.

Preserve the complete validated original response and a closed family-specific
evidence projection. Require command/effect/request-target correlation, exact
returned identities, prior preconditions where exposed, correct replay/no-op
rules, semantic/hash equality and fresh public readback before accepting new
schema/binding/rendering outputs. A local request digest is not a Spine receipt
hash. No-op cannot explain a planned semantic change. Compatible replay proves
only the returned stored result, not current state; independently check both.

Continuation admits exactly one of (a) state after the accepted prefix or (b)
that state plus the first unresolved submission. Compare forward projections
from the saved complete preimage, applying only explained changes, retaining
untouched entries and historical pin evidence. Current catalog pointers, full
selected definitions, remaining-suffix preconditions and all returned IDs must
agree. Candidate (b) uses provisional observed IDs only to evaluate the candidate;
it cannot advance dependents or replace any bytes in the saved request.

When public provenance is available (notably rendering records), compare it with
the original execution. For facets, public reads do not prove which command
created the candidate. Admit at most the single exact desired candidate under
the existing single-operator condition; replay only the original durable request
with the same command ID. Require its valid response to match the candidate's
root/revision/binding IDs before recording acceptance. If that evidence cannot
be obtained, stop partial: do not infer a receipt from equivalent content, guess
IDs, read receipt tables or launch a fresh command to bypass uncertainty.

An unexplained change, ambiguous candidate, malformed response or checkpoint
gap blocks continuation. Immediately recheck non-CAS profile bindings as in v1;
facet bindings use Spine's actual expected-binding CAS. In the uncertain case,
recheck the admitted post-state before replaying the unchanged request, not a
new request with a conveniently changed expected binding.

Each command is atomic; the graph is not. Stop at the first failure. Preserve
accepted prefix, first unresolved/failed action and unattempted suffix without
rollback or cleanup commands. A failed first submission is partial even with
zero accepted responses. A checkpoint durability failure cannot manufacture a
terminal result. A new plan needs new approval and cannot inherit an old execution.
No broader recovery or receipt-repair workflow is introduced.

## 9. Verification and operator handoff

Verify remains strictly read-only: no write replay to recover a missing receipt.
Require the exact manifest/plan/target/environment, complete captured responses
for planned writes, and a fresh validated public view. For retained dependencies
use approved observed IDs; for writes use accepted response IDs. Independently
show the exact schema/rendering/profile revisions, validate their semantic bodies
and owning hashes, and check every reference edge and active binding.

Schema/rendering revision pins must match exactly: a later revision with equal
apparent content cannot replace a referenced revision. Current desired catalog
heads must match the resolved installed revisions at verification; a head advance
is reported separately as drift even if the historical pinned definition still
exists. Archetypes and ordinary v1 behavior retain their existing comparison rules.
For v2 profile pins verify exact references and the proper historical decoder;
never discard rendering to force equivalence. Unselected objects are not excess
and are not removed; their unrelated later changes alone do not make final
selected-state verification fail (continuation has stricter whole-view staleness).

Report captured Spine responses and fresh configuration verification separately.
There is no new public receipt show/list command in the inspected registry;
do not claim independent receipt readback, disclosure readiness, attached item
values, rendered-body correctness or delivered notifications. A successful handoff
includes the selected installed root/revision/binding map and explicitly states:
destination disclosure and subsequent item authoring are separate Spine workflows.

Spine 0.9.0 requires a rendering application choice for each surviving definition-
pinned profile template. Fresh trusted-local item creation must explicitly choose
ordinary output, then use Spine's separately authorized ownership/adoption and
presentation workflow if details are wanted. The installer must not silently set
up that workflow or stop services. Making a rendering-enabled profile the default
therefore affects future authoring compatibility, even though it sends nothing.

## 10. Flight proof and unresolved product choices

Keep `flight` event-only and preserve `flight_standard`'s four approved template
keys, offsets and grace windows from `specs/kinflow-starter.md`: 7 days/24h grace,
24h/6h, 4h/1h, 1h/15m. No flight values or notification text bodies go into packs.
Synthetic fixtures may use test-only IDs outside `packs/`; they are not installable
curated content or permission to create an item.

Candidate proof: one `flight_details` schema, one flight facet binding, one
rendering definition with a scalar flight-number selection and a location-label
selection, one profile and one default binding. Test both projections even if
the eventual curated profile initially selects fewer details. Do not copy Spine's
illustrative fixtures as an approved field policy: the facet example uses
`origin`/`destination`, whereas rendering examples also use `terminal` and
`departure_airport`. These are examples, not a canonical shared flight schema.

Decisions requiring operator choice before curated content:

1. Exact field vocabulary and required/queryable settings. Recommendation for
   review: begin with `flight_number`, `origin`, `destination`; leave terminal,
   gate, status and secrets out. Decide which values, if any, are mandatory when
   a facet is attached; the facet itself remains optional.
2. Display labels/order and which reminders pin details. Recommendation: pilot
   only `one_hour_before`, leaving the other three explicitly ordinary. This is
   not yet approved content or a disclosure grant.
3. Opt-in coexistence versus replacing `flight_standard` for future defaults.
   Recommendation: a distinctly keyed opt-in profile until consuming agents
   support v2 applications. A default-binding replacement still requires exact
   update approval and changes future authoring expectations. Do not choose a
   duplicate root name, pack ID or version on the operator's behalf.
4. Distribution identity: a separate flight-focused pack or a successor starter
   release containing unchanged other definitions. Recommendation: qualify with
   synthetic flight-only fixtures first; decide the release layout afterward.

Technical review gates, not product-policy questions: the pinned profile-list
source-path blocker must first be resolved as described in Section 1; exact v2 artifact schemas,
reference-slot syntax, aggregate observation budgets, response correlation and
fault-injection oracles must be codified and reviewed before their runtime slices.
Exact 0.9.0 public-CLI and clean-wheel qualification remains outstanding. If a
public-command gap is found, report it; this task grants no Spine change authority.

## 11. Codification prerequisites and acceptance

The ordered delivery slices are in [implementation-plan.md](implementation-plan.md).
Before implementing new behavior, add and review (not created by this task):

- `contracts/schemas/spine-pack-manifest.v2.schema.json`, a v2 fixture manifest,
  and semantic reference/normalization/digest tests;
- the seven v2 installer-artifact entry schemas, shared v2 types and embedded
  public-value schema closure, plus exact 0.9.0 readback validators;
- a command/contract/source-pin inventory with transitive schema references,
  exact wire selectors, normalization/hash derivations and response projections;
- one synthetic complete flight graph and saved request/plan/approval/checkpoint/
  apply/verify flow with independently computed hashes; and
- a versioned fixture index mapping each structural and semantic vector to its
  expected oracle. Schema validation alone is not behavioral qualification.

Required vector families:

| Family | Required positive and negative oracles |
| --- | --- |
| Preservation | All v1 artifacts and old-baseline tests unchanged; v1 rejects v2; no migration/rewrite of published bytes |
| Pack graph | Complete scalar/location-label flight; ordinary templates; shared dependency deduplication; missing/wrong-kind/cross-pack refs, duplicate defaults/facet keys, incompatible uses, cycles and embedded IDs/grants rejected |
| Canonical form | Correct digest; incorrect digest; unsorted fields/templates; normalized text; omitted queryable; selection reorder changes digest/output order rather than being sorted away; size boundaries before/after resolution |
| Compatibility | Exact runtime/schema/contract union; wrong/newer baseline rejected; missing protected config; no invented commit from system.info |
| Planning | Missing/retain/drift/retired; decoder-aware v1 ordinary retain; transitive pin drift; per-update approval; complete selection closure; no write subprocess |
| Observation | Mixed owner/IDs, v1/v2 profiles, active/retired, historical pins, every pagination family; stale/repeated cursor, hidden/malformed entries, capacity and changed second pass fail closed; no false public fingerprint |
| Publication | All 11 write kinds and dependency slots; expected-revision/binding guards; response family, dry-run rejection, hash/ID/provenance mismatch; retain emits no writes |
| Recovery | Every prepared/accepted boundary; uncertain schema/rendering create and publish, nested profile pin consumption, both binding families; exact replay, mismatch/no-op handling, torn checkpoint, unrelated change, no speculative suffix |
| Verification | Exact pins and historical decoder, wrong owner/root/revision, changed current head, missing/invalid captured response, no-write plan; no replay or disclosure read/write |
| Authority | No item/facet-value authoring, owner provisioning, disclosure, materialization/send or internal database/API access; output does not claim readiness/delivery |

Independent Draft 2020-12 meta-validation and fixture validation must accompany
the repository's semantic oracle, rather than expanding its hand-built subset
silently. Disposable qualification uses the exact pinned package, temporary
synthetic catalogs and operator-prepared test cursor configs only after separate
authorization. It need not create coordination items or send notifications to
prove the installer; Spine's own rendering tests own that downstream behavior.
```

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/docs/facet-rendering-baseline.md

Hash: 5bdfe805dce09350f1d4e097fe58e5b1628ef5edd9d298c2a0e58863713d7621

```markdown
# Facet/rendering baseline inspection

Inspection date: 2026-10-10. Design authority is
`specs/facet-rendering-packs.md`; this file records evidence, not an alternative
Spine contract or an implementation/qualification claim.

## Provenance and limits

Reference checkout:
`/Users/Shared/Agent-Workspace/repos/personal/cortext1/spine`.
`git rev-parse --verify 01ebce7^{commit}` resolved to
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`. Inspection used a temporary export
of that exact Git tree, not whatever the working checkout might later contain.
`src/spine/__init__.py` declares runtime `0.9.0` and schema `19`.
Spine Packs inspection began at `2bd4157c77fb3b701996def1f48957869c64afd2`.
No operator ledger was opened and no Spine command was executed against one.

The authoritative Spine documents read were:

- `specs/archetype-facets.md`;
- `specs/notification-rendering-definitions.md`;
- `specs/notification-rendering-integration.md`; and
- `docs/NOTIFICATION_RENDERING_GUIDE.md`.

Some historical paragraphs/schema titles still say “future”, “source only” or
“not implemented”. The exact commit's runtime declarations, compiled command
registry, activated integration registry and schema-19 operator guide establish
the local release boundary. This inspection does not itself rerun Spine's
release evidence or qualify its installed artifacts. New rendering selectors
are trusted-local, not permission to use the existing web routes.

## Exact proposed public command map

All names below are canonical `spine-command` commands. There is no Python API
or database adapter. Write identities are supplied by installer execution, not
the reusable manifest. “Common” registry requirements mean
`spine.canonical-json.v1` and `spine.notification-rendering-integration.v1`,
which the pinned compiled registry adds to **every** command below.

| Commands | Wire selector | Additional compiled registry requirements beyond common |
| --- | --- | --- |
| `system.info` | Request `{}`; response `spine.system-info.v3` | `spine.system-info.v3`, `spine.ledger-instance.v1`, `spine.tickerd-compatibility.v1` |
| `item_archetype.create`, `.revise`, `.show`, `.list` | `spine.item-archetypes.v1` | Selector plus `spine.notification-profile-readback.v1`, `spine.notification-profile-catalog-cursor.v1` |
| `notification_profile.create`, `.revise`, `.show`, `.list` | `spine.notification-profiles.v2` | Both `spine.notification-profiles.v1` and `.v2`, `spine.notification-profile-readback.v1`, `spine.notification-profile-catalog-cursor.v1` |
| `notification_profile.metadata.update` | `spine.notification-profile-metadata-update.v1` | Selector plus `spine.notification-profiles.v1`, `spine.notification-profile-readback.v1`, `spine.notification-profile-catalog-cursor.v1` |
| `notification_profile.binding.set`, `.list` | `spine.notification-profile-bindings.v1` | Selector plus `spine.item-archetypes.v1`, `spine.notification-profiles.v1`, `spine.notification-profile-readback.v1`, `spine.notification-profile-catalog-cursor.v1` |
| `facet_schema.create`, `.publish`, `.show` | `spine.facet-schemas.v1` | Selector |
| `facet_schema.list` | `spine.facet-schemas.v1` | Selector plus `spine.facet-cursor.v1` |
| `item_archetype.facet_binding.set` | `spine.archetype-facet-bindings.v1` | Selector |
| `item_archetype.facet_binding.list` | `spine.archetype-facet-bindings.v1` | Selector plus `spine.facet-cursor.v1` |
| `notification_rendering_definition.create`, `.publish`, `.show` | `spine.notification-rendering-definitions.v1` | Selector |
| `notification_rendering_definition.list` | `spine.notification-rendering-definitions.v1` | Selector plus `spine.notification-rendering-cursor.v1` |

The exact sorted execution union derived from
`src/spine/commands/registry.py` is 17 contracts:

```text
spine.archetype-facet-bindings.v1
spine.canonical-json.v1
spine.facet-cursor.v1
spine.facet-schemas.v1
spine.item-archetypes.v1
spine.ledger-instance.v1
spine.notification-profile-bindings.v1
spine.notification-profile-catalog-cursor.v1
spine.notification-profile-metadata-update.v1
spine.notification-profile-readback.v1
spine.notification-profiles.v1
spine.notification-profiles.v2
spine.notification-rendering-cursor.v1
spine.notification-rendering-definitions.v1
spine.notification-rendering-integration.v1
spine.system-info.v3
spine.tickerd-compatibility.v1
```

This is not a list of everything Spine implements. In particular, profile v2
catalog commands do not acquire the schedule application's readback-v2 contract
by analogy. Conversely, their compiled dependency union still contains v1
contracts. The manifest content set separately requires the ordinary base
rendering contract. Cursor configuration has its own protected file contract,
not a request field or an extra catalog command.

## Machine authorities inspected

All paths here are relative to the pinned Spine tree.

| Family | Registry, schema and fixture authorities |
| --- | --- |
| Facets | `contracts/archetype-facet-contract-registry.v1.json`; `contracts/schemas/archetype-facet-{types,commands,responses}.schema.json`; `contracts/archetype-facet-fixture-manifest.json` |
| Rendering definitions | `contracts/notification-rendering-definition-contract-registry.v1.json`; `contracts/schemas/notification-rendering-definition-{types,commands,responses}.schema.json`; `contracts/notification-rendering-definition-fixture-manifest.json` |
| Profile successor | `contracts/notification-rendering-integration-contract-registry.v1.json`; `contracts/schemas/notification-profile-{types,commands,responses}-v2.schema.json`; `contracts/notification-rendering-integration-fixture-manifest.json` |
| Shared fragments | `notification-types.schema.json`, `notification-profile-types.schema.json`, `notification-rendering-integration-types.schema.json` under `contracts/schemas/` |
| Environment | `contracts/schemas/system-info-response-v3.schema.json`; `src/spine/__init__.py`; `src/spine/commands/registry.py` |

The planned machine-contract slice must pin the complete transitive schema
closure, including failures/cursor configuration, rather than copying only the
top-level files or assuming this human inventory is an executable validator.
Fixture IDs containing example ledger IDs are structural/test evidence, not
reusable pack content or operator-approved flight definitions.

Representative inspected vectors:

- `tests/fixtures/archetype_facets/contracts/request_facet_schema_create.json`;
  `response_facet_schema_publish_replay.json`;
  `response_item_archetype_facet_binding_set_noop.json`.
- `tests/fixtures/notification_rendering_definitions/contracts/request_definition_create.json`;
  `response_definition_create_replay.json`;
  `response_definition_publish_noop.json`.
- `tests/fixtures/notification_rendering_integration/request_profile_create.json`;
  `response_profile_historical_v1.json`; `response_profile_create.json`;
  `invalid_template_grant.json`.

## Material differences from the installed pack workflow

| Concern | Exact inspected fact | Consequence for the proposal |
| --- | --- | --- |
| Facet revisions | Definition normalizes NFC, sorted fields/choices/types, explicit queryable=false; hash domain `spine.facet-definition.v1` | Validate normalized owner-neutral content; do not use a generic profile hash |
| Facet binding | Targets an archetype root and exact schema revision; set requires `expected_binding_id` including null | Separate graph edge and CAS; no automatic binding advance on schema publication |
| Rendering hash | Hashes `{contract_version, canonical_json_version, revision}` after display-text normalization; selection array order retained | Local schema refs must resolve before installed hash can be computed |
| Profile revision | V2 template/revision hash domains; stored `revision_contract` discriminates v1 history | Retain decoder identity; never rehash or downgrade old evidence |
| Profile reads | V2 returns normalized owner and revision content; list retains `catalog_snapshot_hash`, 1–500 limit | Cannot decode through the current raw v1 readback schema |
| Facet lists | Schema list returns roots; binding list active bindings; no public snapshot hash; authenticated cursor with total 100-candidate/resource ceiling | Exact revision shows and bounded full observation needed; smaller pages cannot evade capacity |
| Rendering lists | Required explicit owner/status/limit; `records` and `limit`; no public snapshot hash; separate protected cursor config | Different envelope and observation evidence; no copied v1 fingerprint claim |
| Facet writes | `response_contract`; top-level receipt/command IDs; `changed`, `replayed`, prior/result facts; no receipt semantic hash; no audit on no-op | Closed facet-specific correlation and recovery evidence |
| Rendering writes | `contract_version`; nested `record`; top-level receipt/audit IDs; no-op includes audit; replay keeps historical record | Extract IDs from `/record/...`; distinguish historical response from fresh state |
| Profile v2 writes | Nested receipt including `semantic_facts_hash`; no replay boolean | Existing full-request receipt hash rule still applies, new revision hashes do not replace it |
| Provenance | Facet schema show omits creator/command; rendering record exposes `created` and `published`; v2 profile readback lacks legacy creator columns | Do not require invented fields; unresolved response needs exact request replay, not content-only receipt inference |
| Default bindings | Existing public set has no expected-binding CAS | Preserve immediate public pre-write comparison and single-operator posture |
| Disclosure | Profiles pin definitions without grants; each surviving pinned application requires an explicit choice | Installation does not make event authoring or destination disclosure ready |

Handler inspection corroborated public semantics in
`src/spine/commands/notification_profiles.py` (v2 create/revise semantic receipt
hash is the request handed to that handler), `rendering_profiles.py` (v2 dispatch/pin
validation/readback), and `facets.py` (stored receipt replay and response flags).
`rendering_candidate.py` normalizes v2 profile revisions before dispatch; require
canonical normalized submissions rather than assuming an arbitrary original
request has the receipt hash. No normalization may silently alter approved intent.
This is source inspection only, not permission to import these implementations
into the installer. No existing public receipt read command was found in the
compiled command registry.

## Source-level qualification blocker: profile v2 listing

At the exact requested pin:

1. `src/spine/commands/rendering_candidate.py` selects the v2 profile handler.
2. `src/spine/commands/rendering_profiles.py`'s `.list` branch calls
   `shared._list_roots(..., kind="notification_profile")` using a v1 selector,
   intending to project returned records to v2 afterward.
3. `src/spine/commands/notification_profiles.py`'s `_list_roots` calls
   `_legacy_profile` on each profile in the page. `_legacy_profile` raises
   `unsupported_contract_version:contract_version` when the selected stored
   revision is v2. The later v2 projection is never reached for such a page.

This is a concrete source-path conflict with the advertised v2 list contract.
Expected consequence: lists can succeed while all returned revisions are v1,
then fail once a v2 profile is present, obstructing repeat planning, recovery
and verification. It has NOT been reproduced against a disposable ledger in
this specification-only task. Source excerpts/hashes are staged in the audit's
`spine-readback-blocker.md` so the finding can be checked independently.

Next gate: separately authorize a minimal public-CLI regression on this exact
pin: create a synthetic v2 ordinary profile, show it with v2, then list its owner
with v2, including mixed v1/v2 and paginated cases. Do not deploy, bypass listing,
read the database, import handlers as an installer shortcut, or claim successful
qualification before that gate. If confirmed, route the defect to Spine's owner;
any repaired baseline must be explicitly approved and separately pinned here.
Do not substitute a newer 0.9.0 build under the original qualification record.

## Unproved until later slices

No successor schema, fixture, installer code or curated pack was implemented.
No exact-baseline disposable ledger, wheel rebuild, recovery fault injection or
consumer authoring workflow was exercised. Planned aggregate observation budgets
and family-specific evidence schemas still need machine-contract review.
Current regression tests can establish preservation of old behavior, not that
the proposed new workflow works. The bounded audit is staged separately and
cannot be called passed or converged before an approved reviewer run.
```

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-spec-audit-001/spine-source-excerpts.md

Hash: 6fc3b16f84f6a2a1816836edcca24fd32bfbc9fe094ca5a1c9ca017022b979b6

```markdown
# Pinned Spine source excerpts

Source: `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`. Verbatim numbered
excerpts for bounded planning review, not a complete specification mirror.
Hashes below are for the complete original files, not individual excerpts.

## specs/archetype-facets.md

SHA-256: `6f5268c62c955c285e743f16a01560475ba99ac4df30c9e6c50b3433dc3f09c6`

Lines 38–127:

```text
38: ## 2. Model and invariants
39:
40: ### 2.1 Schema roots and revisions
41:
42: A schema root has an immutable `facet_schema_id`, owner scope, owner-local
43: `schema_key`, current revision pointer, and status `active` or `retired`.
44: Owner kinds follow existing catalog scopes: system, subject, subject_group. There is
45: no built-in domain taxonomy. Keys are lowercase ASCII `[a-z][a-z0-9_]{0,63}`.
46: The pair (owner scope, schema_key) is unique, including retired roots; keys are not
47: recycled. Retirement is terminal in this slice.
48:
49: A revision has `facet_schema_revision_id`, schema root ID, positive decimal-string
50: `revision_number`, `display_name`, nullable `description`, compatible item types
51: (nonempty subset of event/task), closed field declarations, and `definition_hash`.
52: The exact revision owns validation and query declarations. Revisions are immutable;
53: even description changes publish a new revision. The current pointer is a catalog
54: convenience, never a value-validation input. `flight_details.v1` in prose means the
55: first published definition, not a globally reserved key or a floating lookup alias.
56:
57: ### 2.2 Archetype bindings
58:
59: An active binding associates an exact archetype root with an exact schema revision
60: and a `facet_key`. At most one active binding exists per (archetype ID, facet_key).
61: The archetype and schema must have the same catalog owner in v1. Publishing a schema
62: revision does not move bindings. Explicit binding set supersedes the previous binding;
63: remove retires it. Compare the expected prior binding ID (null for first creation).
64: Bindings are optional eligibility declarations, not required data, defaults, or
65: automatic facet creation. Schema and archetype compatible item types must intersect.
66:
67: ### 2.3 Item values
68:
69: A complete facet snapshot belongs to `(item_id, item_version)` and contains at most
70: eight entries, unique by `facet_key`. Each entry records the exact schema revision,
71: binding ID, archetype assignment evidence, canonical values, and source authoring
72: receipt. Existing items begin with an empty snapshot. Absence differs from an empty
73: object. Field nulls are forbidden; remove an optional field by omitting it in a full
74: replacement. Missing required fields fail validation.
75:
76: Unrelated item edits copy the snapshot forward exactly. Catalog edits, retirement,
77: or binding changes do not rewrite it. Historical values remain decodable using their
78: stored immutable schema revision. A value replacement requires the current active
79: binding and active schema/archetype, including when upgrading an old revision.
80: An unchanged retained entry need not requalify against current catalog status.
81:
82: Every fresh `set`, including a same-value no-op, MUST require the target item's
83: concrete `item_type` in both the item's pinned assigned archetype revision's and
84: the selected pinned facet-schema revision's `compatible_item_types`. The binding's
85: nonempty intersection test alone is insufficient: an event/task archetype can bind
86: an event-only schema, but a task cannot set that facet. After active binding/catalog
87: eligibility and before value validation, incompatibility fails `wrong_item_type`,
88: `field=item_id` (CLI exit 2; admitted web domain_failure, HTTP 422). Remove-only
89: changes, unchanged copy-forward and compatible receipt replay do not re-run this
90: fresh-set test; they do not author a new value against a new schema revision.
91:
92: Changing or clearing an item's archetype while retaining a nonempty facet snapshot
93: fails `facet_archetype_conflict`; callers must explicitly clear facets first in this
94: initial slice. No command silently deletes data. Removing facets remains possible
95: after catalog retirement. Facets apply to the series item, not individual recurrence
96: occurrences; per-occurrence values are out of scope.
97:
98: ## 3. Closed type system and normalization
99:
100: V1 uses a small declarative field language, not arbitrary executable JSON Schema.
101: Each field has a key in the same ASCII key domain, a boolean `required`, and one type:
102:
103: | Type | Value and validation |
104: | --- | --- |
105: | `text` | Nonempty NFC string, no control characters; declared `max_length` 1–1024 Unicode code points. Whitespace is preserved, not trimmed. |
106: | `enum` | One exact string from 1–64 unique NFC choices, each 1–128 code points. Case-sensitive. |
107: | `boolean` | JSON true/false, without string/number coercion. |
108: | `integer` | Canonical signed decimal string: either `0` or an optional ASCII minus sign followed by an ASCII digit `1`–`9` and zero or more ASCII digits `0`–`9`. Leading zeros, plus signs and negative zero are forbidden. Inclusive declared min/max use the same encoding and stay within signed 64-bit range. |
109: | `date` | Valid proleptic Gregorian `YYYY-MM-DD`, years 0001–9999; descriptive only, never a temporal anchor. |
110: | `reference` | Existing Spine `subject` or `location` ID; declaration fixes the target kind. No polymorphic object or arbitrary URI. |
111:
112: Each declaration also has `queryable` (boolean, default false). Unknown schema keys,
113: field keys, types, coercions, floats, nulls, nested objects, arrays of values, regexes,
114: formulas, computed defaults, remote references and scripts are rejected. Definitions
115: have 1–32 fields. Full normalized definition is at most 32 KiB UTF-8 canonical JSON;
116: one values object at most 16 KiB; all item values together at most 64 KiB. Text is
117: normalized to NFC before validation/hashing; enum choices normalize then deduplicate,
118: with duplicate declarations rejected rather than silently collapsed.
119:
120: Definition normalization fills queryable=false, orders fields by key, enum choices
121: lexicographically by Unicode scalar value, and compatible types lexicographically.
122: Integers and dates are validated, not rewritten from permissive input. Hashes use
123: existing `spine.canonical-json.v1` and SHA-256. `definition_hash` covers a preimage
124: with `derivation_version=spine.facet-definition.v1` and the entire normalized revision
125: definition excluding generated IDs, revision number and hash. Catalog owner is a
126: root fact, not part of the portable definition hash.
127:
```

Lines 179–231:

```text
179: ## 4. Proposed command surfaces
180:
181: All mutation requests use the owning proposed family, `command_id`, actor and explicit
182: action timestamp under the existing common command contract. Fresh requests require
183: the expected target revision/version. Read requests do not write receipts. Exact JSON
184: schemas and field spelling of common envelopes are now recorded in Section 10;
185: the remaining implementation gates still apply.
186:
187: | Command | Additional request facts | Terminal effects |
188: | --- | --- | --- |
189: | `facet_schema.create` | owner, schema_key, complete definition | `facet_schema_created` |
190: | `facet_schema.publish` | root ID, expected current revision ID, complete definition | `facet_schema_published`, `facet_schema_publish_noop` |
191: | `facet_schema.retire` | root ID, expected current revision ID | `facet_schema_retired`, `facet_schema_retire_noop` |
192: | `facet_schema.show` | root ID; optional exact revision ID | Complete root/revision readback |
193: | `facet_schema.list` | one explicit owner, status filter, limit/cursor | Bounded catalog page |
194: | `item_archetype.facet_binding.set` | archetype ID, facet_key, exact schema revision ID, expected binding ID | `facet_binding_set`, `facet_binding_set_noop` |
195: | `item_archetype.facet_binding.remove` | archetype ID, facet_key, expected binding ID | `facet_binding_removed`, `facet_binding_remove_noop` |
196: | `item_archetype.facet_binding.list` | archetype ID, limit/cursor | Binding page |
197: | `item.facets.update` | item ID, expected item version, changes | `item_facets_updated`, `item_facets_update_noop` |
198: | `item.facets.show` | item ID; optional exact item version | Complete pinned facet snapshot |
199: | `item.facets.query` | owner, exact schema revision ID, field, equality value, limit/cursor | Bounded matching item IDs/versions |
200:
201: `changes` contains 1–8 operations, sorted by facet_key for normalization; duplicate
202: keys fail. Each operation is `set` with facet_key, expected active binding ID, exact
203: schema revision ID and complete `values`, or `remove` with facet_key. There is no
204: merge/upsert of individual fields. All changes commit atomically in one new item
205: version. A structurally equal normalized final snapshot is a no-op; existing source
206: provenance is retained. Removing an absent key is a no-op. Same-value sets still
207: validate binding, schema and references on a fresh command. Catalog create collisions
208: are conflicts, not implicit overwrite or revival.
209:
210: Success receipts include command/receipt IDs, effect, changed, affected root/revision
211: or item IDs, prior/resulting versions, and sorted changed facet keys. Compatible
212: same-command replay returns recorded stable identities with `replayed=true` and
213: `changed=false`, rather than producing new rows (Section 10.2).
214: Common replay semantics apply before fresh version checks, but never bypass current
215: disclosure authorization in a permission-enforced adapter. Same ID/different normalized
216: semantic request fails `semantic_conflict`. Failed validation changes no state.
217:
218: Validation precedence: envelope/types/bounds; adapter admission; the private receipt
219: lookup and authorized replay branch in Section 6.2; for a fresh command, target/nested
220: authority and visibility/existence; expected versions; active binding/catalog eligibility
221: and concrete item-type compatibility; definition and value validation; reference access;
222: final snapshot limits; transaction. Reference authority is resolved before fresh domain
223: checks; reference lifecycle/value validation remains in the reference-access phase.
224: Inside the write transaction recheck versions and authority before committing.
225: Public errors do not reveal foreign target existence. Proposed domain reasons include
226: `facet_schema_invalid`, `facet_value_invalid`, `facet_binding_conflict`,
227: `facet_archetype_conflict`, `facet_schema_retired`, and `facet_reference_unavailable`;
228: use existing stale/conflict/permission/capacity envelopes where applicable. Field
229: errors carry paths, never echo private values. Machine error mapping is an explicit
230: contract-codification gate, not permission to improvise runtime strings.
231:
```

Lines 614–704:

```text
614: ### 10.1 Wire choices
615:
616: The canonical command is supplied by the transport route, not duplicated inside its
617: request. Each request requires the exact owning `contract_version`. Writes require
618: `command_id`, `actor_subject_id`, `action_timestamp_utc` (whole-second UTC `Z` form).
619: Requests are closed: unknown properties fail. Read requests carry no write identity.
620: IDs use the existing nonempty-string ID domain; generated IDs must additionally obey
621: Section 3.1, as checked by identity vectors rather than invented by a caller.
622:
623: Definitions are passed as `definition`, with `fields` an array of declarations using
624: `key`, `type`, `required`, optional `queryable`, and type-specific properties.
625: `max_length`, integer `min`/`max`, revision/item versions and page limits are canonical
626: decimal strings, not JSON numbers. Integer bounds are both required. Display metadata
627: uses the existing catalog lengths: display_name 1–160 code points, description null
628: or 1–2000 code points. NFC normalization precedes length and byte checks. Text controls
629: mean U+0000–U+001F and U+007F–U+009F; unpaired surrogates are rejected everywhere.
630: The exact definition preimage is
631: `{derivation_version: "spine.facet-definition.v1", definition: <normalized definition>}`.
632: The 32 KiB definition bound measures that normalized definition, not its enclosing
633: hash preimage. The 64 KiB values bound measures a canonical object mapping each
634: facet_key to its values object; per-entry provenance/definitions are not included.
635: Each individual values object remains limited to 16 KiB.
636:
637: Publish/retire use `expected_current_revision_id`. Binding set/remove require
638: `expected_binding_id`, including explicit null for no active binding. A missing active
639: binding with a non-null expectation is a conflict, not the absent-remove no-op.
640: Item updates use `expected_item_version`; optional historical read selection uses
641: `item_version`. A `set` requires `expected_binding_id` non-null; its values are a full
642: replacement. Duplicate declaration/change/entry keys are semantic errors, even when
643: the array elements differ structurally. Arbitrary scalar strings in the envelope are
644: not authorization to bypass the exact pinned field type and declaration constraints.
645:
646: ### 10.2 Success, failure and readback
647:
648: Successes contain `response_contract` equal to the command's owning family. Every
649: write response includes `command_id`, `command_receipt_id`, the closed `effect`,
650: `changed` and `replayed`. Fresh outcomes use `replayed=false`: changed writes include
651: `audit_id`, while fresh no-ops forbid it. Compatible replay uses `replayed=true` and
652: `changed=false`, creates no rows, and returns the stored receipt ID, effect and stable
653: result identities. An original changed effect requires its stored `audit_id`; an
654: original no-op effect forbids that field. On replay this is historical audit evidence,
655: never evidence of a newly performed write. The effect names the stored receipt's
656: outcome; it does not override the current invocation's changed=false result.
657:
658: All six writes support compatible replay. `facet_schema.create` replays only its
659: changed receipt; create collisions remain conflicts and there is no create no-op
660: receipt. Publish, retire, binding set, binding remove and item facet update may replay
661: their changed or no-op receipts. Prior/resulting version and binding facts stay exactly
662: as recorded, even if the target has since advanced; replay is not a current-state read.
663: For `item.facets.update`, replay returns
664: `changed_facet_keys=[]` and `reconciliation_performed=false`, regardless of the
665: original values of those two invocation-activity fields. It neither reconciles work
666: nor advances a version. `replayed` and the activity-field substitutions are response
667: projection facts only: they do not rewrite the receipt, semantic hash, stored effect,
668: or command-derived identities. Section 4's current disclosure checks still apply.
669:
670: Catalog receipts report `prior_revision_id`, `facet_schema_revision_id` and
671: `revision_number`; create has prior=null and number=1. Publish increments only on
672: change; retire and no-op preserve the revision. Binding set reports prior/resulting
673: IDs and schema revision. Remove reports the same retired binding ID as prior/result;
674: the absent-remove no-op reports both IDs as null. Item receipts report prior/resulting
675: item versions and sorted `changed_facet_keys` (empty on no-op or replay). Fresh changed
676: versions advance by one; replay preserves the original version pair.
677: `reconciliation_performed` reports whether committed work reconciliation ran on this invocation;
678: no-op, replay and dry-run require false. The sample changed receipt is for an item with no policies or
679: work and uses false. Section 5 defines verified retention and the exact true/false rule;
680: the boolean is not evidence of delivery or a count of cancelled/created work.
681:
682: Schema show returns a `root` and selected immutable `revision`; the selected revision
683: must belong to that root, but can differ from its current pointer. Stored definitions
684: are fully normalized, including explicit queryable=false. Item show returns sorted
685: `entries`; each contains the pinned schema revision/definition/hash, facet binding ID,
686: `archetype` assignment evidence (root/revision, selection_source and source_ref when
687: present), values, `source_command_receipt_id`, and `references` sorted by field key.
688: Reference state contains exactly one entry for every reference-valued field present.
689: Its ID/kind must agree with the pinned definition and value. An unreadable reference
690: denies the whole result; inactive but readable subject references are returned as
691: inactive. Existing readable location references always return status=active under
692: Section 6; no location-status column is required or inferred.
693: An empty snapshot returns entries=[], not null or an omitted field.
694:
695: Handler failures use the existing ok/command/error envelope. The proposed facet
696: domain reasons in Section 4 are carried as `error.code`; exact CLI exit mappings are
697: in the draft registry. Definition/value errors use exit 2, binding/archetype conflicts
698: 6, retired-schema use 2, and missing/unreadable references or inactive subjects uniformly 4 with
699: `facet_reference_unavailable`. Paths identify fields but never echo private values.
700: Admission/permission and operational-capacity envelopes remain owned by their adapters;
701: the facet handler schema does not replace or freeze them. Section 6.1 defines resolver
702: mappings, admission ordering and capacity wrappers. Fixture error
703: messages are illustrative safe prose, not byte-exact public message constants.
704:
```

Lines 742–821:

```text
742: ### 10.3 Pagination and validation limits
743:
744: Catalog list defaults status=active and limit=25; explicit status selects active or
745: retired. Binding list returns only active bindings. Query returns current matching
746: item IDs/versions. All pages include the accepted decimal-string limit, `has_more`
747: and `next_cursor`; has_more=false requires null, true requires a nonempty opaque
748: cursor at most 4096 characters. Returned collection length cannot exceed limit.
749: Root IDs, facet keys and item IDs respectively determine the existing total order.
750:
751: Section 11 and its machine companion specify token encoding, authenticated binding,
752: snapshot identity, expiry and access context. No fixture with an arbitrary token proves pagination
753: security or freshness. Likewise, JSON Schema checks structure, not NFC, declared-field
754: validation, hash correctness, foreign-key visibility, byte ceilings or transactional
755: invariants. Test-only pure oracles cover selected semantic vectors; no application
756: validator, database migration, index or command handler is introduced by this bundle.
757:
758: ## 11. Authenticated facet pagination v1
759:
760: `contracts/archetype-facet-integration.v1.json` and
761: `contracts/schemas/archetype-facet-cursor.schema.json` define the dedicated
762: `spine.facet-cursor.v1` continuation. It does not extend or replace either existing
763: trusted-web cursor family. The three paginated commands are facet_schema.list,
764: item_archetype.facet_binding.list and item.facets.query. Show is never paginated.
765:
766: ### 11.1 Bytes, key and context
767:
768: Token: `fc1.<base64url(payload)>.<base64url(mac)>`, unpadded canonical base64url,
769: at most 4096 ASCII bytes. Payload is closed canonical Spine JSON UTF-8 per the cursor
770: schema. MAC is HMAC-SHA256 with the preimage `ASCII("spine.facet-cursor.v1")`, one NUL
771: byte, then the exact payload bytes. Reject wrong version, padding, noncanonical
772: base64url, duplicate JSON keys, unknown fields, noncanonical JSON, invalid schema or
773: MAC with invalid_request/field=cursor. Verify MAC with constant-time comparison before
774: interpreting payload fields. Never log token contents or signature diagnostics.
775:
776: Use a separately provisioned deployment secret of at least 32 random bytes per ledger,
777: not a model/request supplied key or the public vector key. Reads never create a key,
778: receipt or cursor cache. Trusted-local CLI receives key and context through protected
779: operator configuration; web receives them through service configuration. Missing config
780: fails preflight for paginated commands, including first pages, rather than issuing unsigned
781: cursors. This is configuration, not executor authentication. Provision a persistent random
782: `cursor_ledger_id` and `cursor_generation` with the key outside the ledger; use distinct
783: values for copies/clones and rotate generation after restore. These config IDs are not
784: canonical coordination IDs. Rotation invalidates outstanding cursors. No new DB columns.
785:
786: `context_hash` is a keyed digest of the closed object containing `mode`,
787: `cursor_ledger_id`, `cursor_generation`, and `principal`. For trusted_local, principal
788: is `{os_uid: <canonical decimal string>}`; full-scope local users still do not assert a
789: web account. For permission_enforced, principal is the exact identity mapping from
790: `contracts/trusted-web-read-cursor.v2.json` (ledger/realm/recovery, account/subject/
791: binding revisions, selection ID and access_epoch). Full-scope single-operator web
792: remains permission_enforced for identity binding; its access proof records that
793: deployment mode. No caller-controlled actor field substitutes for this context.
794:
795: For all three digest fields below, use lowercase hex HMAC-SHA256 over canonical JSON
796: of `{contract_version: <domain>, value: <specified object>}` with the same key.
797: Domains are `spine.facet-cursor-context.v1`, `spine.facet-cursor-access.v1`, and
798: `spine.facet-cursor-source.v1`; signatures retain their separate domain above.
799: Keying prevents a cursor digest becoming an oracle for low-entropy protected facts.
800:
801: ### 11.2 Query, source and access binding
802:
803: `query_hash` is ordinary lowercase SHA-256 over canonical JSON of
804: `{contract_version:"spine.facet-query.v1", command:<canonical command>, request:<normalized request>}`.
805: The request excludes only cursor, includes contract_version and limit (default 25),
806: and fills list status=active. NFC/type normalization follows the pinned schema;
807: owner discriminators and exact schema/archetype IDs are retained. Changing limit,
808: predicate, owner, revision, status or command mid-pagination is invalid_request.
809: Bind this digest and command in every payload. Do not accept a token from another route.
810:
811: Recompute the complete bounded authorized candidate set on each page in one snapshot,
812: not only the page after last_key. Use indexed enumeration plus LIMIT 101; more than 100
813: candidates or resolved resources fails capacity before returning any page. This is a
814: v1 total-candidate ceiling, not just a page limit. Do not silently cap or paginate an
815: incomplete set. Candidate enumeration includes nonmatching items/roots, so a later
816: matching value or newly visible candidate changes the snapshot. No global JSON scan.
817:
818: `source_snapshot_hash` covers a closed `{command, query_hash, facts}` object, with
819: facts exactly as follows, ordered by the specified primary key:
820:
821: - Schema list: facts is `{roots: [...]}` containing all authorized roots in the named owner (before status filter), each
```

## specs/notification-rendering-definitions.md

SHA-256: `f7ec98452f90ca55f78e661a61ff2c036fda84f4931884c0c7f637c076f899a7`

Lines 77–126:

```text
77: ## 3. Logical catalog
78:
79: ### 3.1 Definition root and revision
80:
81: A `notification_rendering_definition` root has an immutable ID, immutable owner
82: (`system|subject|subject_group` with the corresponding owner ID), owner-local key,
83: `active|retired` status, current revision pointer, and creation/retirement provenance.
84: Owner plus key is unique even after retirement. System definitions follow existing
85: read-only system-catalog rules; ordinary operators cannot create them.
86:
87: Each immutable revision contains its root ID, contiguous revision number, display
88: name, nullable description, supported item types (`event`, `task`, or both), a pinned
89: base-renderer contract/profile, ordered field selections and a canonical content hash.
90: Display metadata is revisioned in this proposal; there is no independent mutable
91: metadata operation in the first slice. Section 13 defines IDs, revision preimages
92: and encodings; example strings are not an alternative derivation rule.
93:
94: Publishing never modifies a prior revision. Retiring a root prevents fresh selection
95: or application; historical reads and decoding remain available. Existing policies
96: retain their exact selection. Retirement is not an emergency disclosure revocation;
97: Section 8 separates those meanings.
98:
99: ### 3.2 Field selection
100:
101: Each selection has a unique `selection_key`, `facet_key`, exact
102: `facet_schema_revision_id`, declared `field_key`, a literal display `label`, and
103: `projection=value|location_label`. Projection must agree with the declared field type.
104: Array order is presentation order and hash-bearing. Duplicate selections of the same
105: facet/schema/field are invalid. There is no wildcard, latest-revision selector, nested
106: lookup or cross-item traversal.
107:
108: The referenced schema revision must exist, belong to the definition's owner in this
109: first slice, and declare the field. An applicable item must actually hold that facet
110: key with that exact schema revision. Matching field names in another revision are
111: not sufficient, even if their apparent types happen to match. A definition may be
112: reused by several archetypes that bind the same schema; it need not embed an archetype ID.
113:
114: First-slice value types are `text`, `enum`, `integer`, `boolean`, and `date`.
115: One reference type is also supported by this proposal: a facet `reference` field
116: whose declared target kind is `location`. It may project only that location's
117: canonical `label`, using Section 6.1. Subject references and other reference kinds,
118: arbitrary referenced fields, nested traversal and raw-ID output are rejected at
119: definition authoring. A location remains a reference, never copied into a text field
120: solely to satisfy this renderer. This restriction does not change which field types
121: facets themselves support.
122:
123: All selected values are optional message detail in this first slice. There is no
124: required-detail mode that cancels an otherwise eligible ordinary reminder. Labels
125: and text are plain data, not instructions, HTML, mention syntax or adapter directives.
126:
```

Lines 417–463:

```text
417: ## 9. Command and pack boundary
418:
419: Reserve the `notification_rendering_definition` command family with create,
420: publish, retire, show and list operations. These names are specified, not registered
421: CLI commands. Writes require exact expected revisions where applicable, command IDs,
422: actor/time attribution, atomic audit and replay receipts. Publish of equivalent
423: normalized content and repeated retirement need deterministic no-op semantics. Reads
424: are bounded, permission-aware on protected transports, and nondurable. Section 13
425: defines envelopes, effects, identity preimages and field limits. Cursor authentication
426: and physical query plans remain implementation gates.
427:
428: The `notification_rendering_disclosure` family defines provision/revoke/show/list
429: operations for reusable disclosure authorizations and their application evidence. They share common
430: audit/replay rules but are distinct from publishing a rendering definition. No current
431: catalog, schedule or permission command accepts these new facts by implication.
432:
433: Versioned profile and direct-policy authoring contracts must express exact selection
434: and explicit clearing to ordinary rendering. Existing closed v1/v2 schemas are not
435: extended silently. The implemented `rendering_profile` constant names an algorithm;
436: it is not interchangeable with a reusable definition ID or a notification profile ID.
437:
438: Packs may supply owner-neutral schema definitions, archetype bindings, rendering
439: definitions and profile references. A future installer resolves pack-local references
440: to exact Spine IDs, provisions dependencies before references, and verifies canonical
441: readback. Each command remains its own transaction unless a separate atomic composite
442: is explicitly contracted. Partial installation is reported and replayed, not described
443: as globally atomic. Missing dependencies block dependent writes, not ordinary reminders.
444: Pack upgrades must detect operator divergence and require explicit reconciliation;
445: they cannot overwrite customizations, grant disclosure, or rewrite live item policies
446: merely because a bundled default changed.
447:
448: ## 10. Flight example and expected behavior
449:
450: A pack could supply a `flight_details` schema with scalar `flight_number` and
451: `terminal`, a flight archetype binding to that schema revision, and a rendering
452: definition selecting those fields in that order. An installed notification profile
453: could select it only for the one-hour template while keeping other reminders ordinary.
454:
455: The reminder still fires solely under its existing offset and late-handling policy.
456: If the current item has `AC872` and `1`, approved detail appears as in Section 4.
457: If terminal is absent, only flight number appears. If the facet was upgraded to a
458: different schema revision, neither field is borrowed from history; ordinary prose
459: remains until an explicit compatible selection is applied. Publishing a new catalog
460: revision changes none of these existing reminders. Reference-valued origin/destination
461: fields may select the referenced location's label under Section 6.1 and the approved
462: location set, without replacing primary location.
463:
```

Lines 538–642:

```text
538: ### 13.1 Versions, normalization and identities
539:
540: Implemented local versions are `spine.notification-rendering-definitions.v1` (catalog),
541: `spine.notification-rendering-disclosures.v1` (authorization management),
542: `spine.notification-rendering-presentation.v1` (authoring/application fragments) and
543: `spine.notification-rendering-details-evidence.v1` (attempt evidence extension).
544: The last two are fragments within the integration's versioned successor envelopes,
545: not new fields accepted by frozen profile, schedule or attempt contracts.
546:
547: Use `spine.canonical-json.v1` from the ontology: sorted object keys, preserved array
548: order, UTF-8, explicit nulls/booleans, decimal-string integers, no JSON numbers and no
549: Unicode normalization. Reject invalid scalar Unicode. IDs/keys are exact strings,
550: not whitespace-trimmed or case-folded. Normalize display names, non-null descriptions
551: and selector labels using ordinary renderer text normalization before validation and
552: hashing. Empty normalized strings and forbidden control characters are invalid.
553: Sort compatible item types, approved/effective selection keys and permitted location
554: IDs lexicographically; reject duplicates rather than silently collapsing them. Preserve
555: selection array order. Projection/type equality, unique selection keys and unique
556: `(facet_key, facet_schema_revision_id, field_key)` tuples are semantic checks beyond
557: JSON Schema. Date validity and canonical integer encoding remain facet authority.
558:
559: For SHA-256 below, hash canonical UTF-8 bytes; digests are lowercase hex. Definition
560: content preimage is exactly `{contract_version, canonical_json_version, revision}`
561: using the catalog version and normalized complete revision. Scope preimage is exactly
562: `{contract_version, canonical_json_version, scope}` using the disclosure version and
563: normalized complete immutable scope. Profile revision is absent from scope; it remains
564: in the application origin. Empty permitted-location arrays are explicit and retained.
565: Each disclosed location must be in that list. Extra fields, wildcards and omitted
566: use-scope branches are invalid.
567:
568: New row IDs use the existing `spine.command-id.v1` derivation, not content IDs. These
569: are the exact row roles, prefixes (identical to role), and request paths:
570:
571: | Creation | Row role/prefix | Request path |
572: |---|---|---|
573: | Definition create | `notification_rendering_definition` | `/definition` |
574: | Definition create or publish | `notification_rendering_definition_revision` | `/revision` |
575: | Disclosure provision | `notification_rendering_disclosure` | `/scope` |
576: | Every fresh terminal write, including no-op | `audit` | `/audit` |
577: | Every fresh terminal write, including no-op | `command_receipt` | `/` |
578:
579: The command-derived preimage contains exactly `derivation_version`, full `command`,
580: `command_id`, `row_role`, `request_path`. The ID is `<prefix>_<digest>`. Revision
581: numbers begin at `"1"`, increment only on changed publish, and are not IDs. Root
582: owner/key remain immutable. A different command cannot recreate an occupied owner/key,
583: even if retired. Identical disclosure scopes may be provisioned under distinct command
584: IDs; they remain explicit records and therefore make automatic resolution ambiguous.
585:
586: ### 13.2 Mutation, read and failure semantics
587:
588: The closed request/response schemas bind commands to their exact contract version.
589: New writes carry command ID, actor and UTC timestamp. Dry run uses the existing
590: `CommandContext.dry_run` flag (default false), not a JSON request field. Receipt
591: comparison uses the full normalized request, plus command and contract version.
592: Dry-run performs validation and deterministic preview,
593: but writes no root, revision, grant, audit or receipt. Preview IDs are predictions,
594: not evidence of persistence; return the same would-be audit/receipt IDs as the commit
595: path, qualified by `dry_run=true`, under the shared command contract. Existing receipt
596: replay precedes freshness and lifecycle
597: validation, after current admission/shape checks. Mismatched command ID reuse is
598: `semantic_conflict`. Replay returns the original record/effect/IDs with
599: `replayed=true, changed=false`; it must not render a fresh catalog snapshot or authorize
600: new disclosure. Dry-run replay follows that same branch with `dry_run=true`.
601: Fresh success atomically persists state, one audit and one receipt. Errors persist none;
602: handler-level dry-run errors carry `dry_run=true` under the existing context contract.
603: Every success and handler-failure response, including show/list, replay and no-op,
604: MUST omit `dry_run` on ordinary execution and include only `dry_run=true` for a
605: dry-run context. `dry_run=false` is not a valid wire response. Read previews retain
606: their ordinary read fields; the marker does not imply a mutation or durable evidence.
607:
608: Publish requires an active root and matching `expected_current_revision_id`; equal
609: normalized content is `rendering_definition_publish_noop`. Retire also requires the
610: exact current revision; repeated retirement returns `rendering_definition_retire_noop`
611: only with the same reason code, otherwise `semantic_conflict`. Revocation similarly
612: requires exact immutable `expected_scope_hash`; repeating the same reason is
613: `rendering_disclosure_revoke_noop`, changing it conflicts. No-op records preserve
614: original creation/publish/retirement/revocation provenance. Revocation does not publish
615: a replacement scope. Provision requires an active, accessible definition and validates
616: all fields, owner/use/destination and allowed references before storing the grant.
617:
618: Fresh validation precedence is: bounded decoding and closed shape/version; admission;
619: receipt replay comparison; target/dependency existence and permission; expected revision
620: or scope hash; lifecycle; selector/type/ownership/scope semantics; normalized no-op
621: comparison; atomic persistence. Missing or inaccessible protected resources do not
622: leak their existence. Invalid definition dependencies/types use
623: `rendering_definition_invalid`; retired fresh use uses `rendering_definition_retired`.
624: No matching authorization uses `rendering_disclosure_unavailable`, multiple matching
625: records use `rendering_disclosure_ambiguous`, and an explicit nonmatching scope uses
626: `rendering_disclosure_scope_mismatch`. At attempt start these expected disclosure
627: failures instead omit optional detail after ordinary admission, never author a grant.
628:
629: Show may address an exact historical definition revision belonging to the named root;
630: omission reads the current revision. Definition list returns current revision records
631: in root-ID order; disclosure list returns grant-ID order, filtered by explicit owner
632: and lifecycle status. Limit is a decimal string from 1 through 100; no counts or total
633: ledger scan. Fetch at most limit+1 indexed candidates, return at most limit, and return
634: a non-null cursor exactly when more exist. Both list responses MUST echo the accepted
635: request `limit` as a required decimal string, including empty and dry-run pages;
636: `len(records) <= int(limit)` is a semantic invariant. JSON Schema enforces the wire
637: domain and absolute 100-row cap, not that cross-field count comparison. Read calls
638: write no receipt or audit.
639: Owner-filtered indexes, consistent permissions, signed cursor payload/version/key
640: management and stale-cursor semantics must be specified before implementing these
641: reads; an opaque string in the schema does not complete that contract.
642:
```

## specs/notification-rendering-integration.md

SHA-256: `2a77e5670ba2174c0727b922f1eaa21fe540456fb14f22058ffab95c3783835f`

Lines 35–125:

```text
35: ## 2. Versioned integration surfaces
36:
37: Reserve these successors. They are not added to compiled runtime declarations,
38: packaged web registries or capabilities by this document.
39:
40: | Surface | Specified successor | Integration delta |
41: | --- | --- | --- |
42: | Profile create/revise/show/list and revision content | `spine.notification-profiles.v2` | Optional template rendering reference, exact revision decoder |
43: | Profile application/readback | `spine.notification-profile-application.v2`, `spine.notification-profile-readback.v2` | Per-policy presentation pins and separate presentation hash |
44: | Schedule create/update | `spine.schedule-create.v3`, `spine.schedule-update.v3` | Application selections and explicit policy-presentation edit branch |
45: | Direct reminder authoring/edit | `spine.notification-schedule-authoring.v2` | Optional direct presentation selection; existing timing identity unchanged |
46: | Full schedule readback | `spine.schedule-show.v2` | Current policy presentation plus v1/v2 persisted attempt rendering |
47: | Attempt rendering envelope | `spine.notification-rendering.v2` | Ordinary base plus approved detail evidence in one final rendering |
48: | Integration capability | `spine.notification-rendering-integration.v1` | Atomic enablement of this complete integration |
49:
50: Existing metadata-only profile updates, archetype/binding commands, recurrence,
51: opportunity/materialization and compact/read-only web contracts retain their exact
52: versions and shapes. An old read projection cannot mislabel v2 rendering as v1:
53: retain its documented summary/redaction policy, or reject an unsupported full-evidence
54: projection. No new fields are injected into the frozen web v1/v2 families.
55:
56: Old authoring requests remain ordinary on fresh creation. When they copy existing
57: policies unchanged, they must preserve their presentation supporting facts. An old
58: whole-plan replacement that would remove or change a selected presentation without
59: expressing that intent MUST fail `unsupported_field`, field `notification_plan`,
60: with no writes and a fixed upgrade-contract diagnostic. It must not silently clear
61: details, auto-resolve a new grant or drop sidecar state. Exact stored receipt replay
62: remains unchanged and must not require today's catalogs to be active.
63:
64: For `notification_profile.revise`, compatible stored receipt replay precedes all
65: fresh-execution checks, including the guard below; incompatible command-ID reuse
66: still fails under the existing replay rules. On fresh execution, perform existing
67: root/lifecycle and expected-current-revision checks first. If the current revision
68: uses the v2 decoder, a `spine.notification-profiles.v1` revise request MUST fail
69: `unsupported_field`, field `revision`, with diagnostic
70: `Use spine.notification-profiles.v2 to revise a v2 profile revision.`
71: This includes v2 revisions whose templates are all ordinary and requests that would
72: otherwise be no-ops. Do not demote to v1, copy pins implicitly, or silently clear them.
73: No revision, pointer, audit or receipt is written by that failure. V1-to-v1 revision
74: remains unchanged; a v2 request may revise a v1 or v2 current revision using the v2
75: normalization/hashes. In v2 complete replacements, omitted template rendering means
76: ordinary as specified below. Historical v1 hashes and compatible replay never change.
77: Metadata-only updates and retirement remain governed by their existing contracts.
78:
79: All writers must understand copy-forward before storage activation, even writers
80: whose public schema cannot author rendering. A runtime without the integration
81: capability must reject the activated schema at bounded preflight. Enclosing schemas,
82: runtime family requirements and release manifests must ship atomically, with old
83: history decoders retained. This is internal historical decoding, not a second model.
84:
85: ## 3. Authoring and application
86:
87: ### 3.1 Profile revisions and complete plans
88:
89: V2 profile templates add `rendering` with the closed union `{kind: ordinary}` or
90: `{kind: definition, definition: <definitionReference>}`. Omission normalizes to
91: ordinary. They never store disclosure IDs, destinations or effective field subsets.
92: The existing definitionReference pins root and exact revision. Definition/profile/
93: schema owner equality and compatibility rules remain logical Section 5.
94:
95: V2 revision and template hashes use new preimages: respectively
96: `{derivation_version: spine.notification-profile-revision-hash.v2, canonical_json_version,
97: revision}` and `{derivation_version: spine.notification-profile-template-hash.v2,
98: canonical_json_version, template}`. `revision` is the complete normalized revision;
99: `template` is a normalized template without its derived hash. Neither rewrites v1
100: hashes. The ordinary effective-policy-set hash still excludes presentation; add a
101: separate `effective_presentation_set_hash` defined in Section 4.
102:
103: V3 schedule `notification_plan` and complete replacement plans add an optional
104: `rendering_applications` array, maximum 32, sorted by `(source_kind, source_key)`.
105: Each entry is exactly `{source_kind, source_key, selection}`: source_kind is
106: `profile_template|custom_addition`; source_key is the existing template/policy key;
107: selection is the existing `authoringSelection` schema. Replaced templates still use
108: `profile_template` as address; composition derives `profile_replacement` as origin.
109: No duplicate address, suppressed/missing address or client-supplied origin is legal.
110:
111: For each surviving profile template whose definition is not ordinary, an application
112: entry is required: it selects that exact definition with explicit effective keys and
113: exact/unique-match authorization, or explicitly chooses ordinary. An alternate
114: definition is allowed only on a named complete template replacement and must pass
115: fresh definition checks. For ordinary templates and custom additions, omission means
116: ordinary, while an explicit entry may opt into a definition with fresh validation.
117: Missing required application is `missing_required_field`; unknown/duplicate address
118: or incompatible template pin is `semantic_conflict`, field `rendering_applications`.
119: A missing grant fails authoring rather than silently switching to ordinary.
120:
121: Suppression, replacements and additions compose first; normalize and reject duplicate
122: ordinary policies before applying presentation. Two identical timing/target/recipient
123: policies with different renderings are still duplicates, not two sends. Full-plan
124: replacement is still full replacement, not a new patch/upsert interpretation.
125:
```

Lines 160–214:

```text
160: ### 3.3 Fresh trusted-local creation and explicit adoption
161:
162: This slice does not add an owner input or ownership establishment to the trusted-local
163: schedule-create command. Fresh trusted-local creation is therefore **ordinary-only**:
164: a definition selection fails `rendering_disclosure_unavailable` before any durable
165: item, policy, work, audit or receipt commit. A profile containing definition pins may
166: still be used at creation, but every surviving pinned template must have an explicit
167: ordinary application entry under Section 3.1. Never infer an owner from that profile.
168:
169: `materialization=none` suppresses only the invoking command's work creation. It is
170: not a scheduler hold. Automatic planning can materialize missing actionable work for
171: the committed active policies regardless of pending ownership adoption or presentation
172: setup. Without an operational exclusion, an ordinary reminder may start between any
173: two setup steps, including for a reminder already due within its late-delivery grace.
174:
175: If details must be configured before any reminder can start, the operator MUST establish
176: and verify an operational exclusion of concurrent materialization **before creation**
177: and retain it until the presentation edit commits. This includes automatic schedulers,
178: other explicit materializers and their in-flight operations: for example, quiesce the
179: relevant worker/scheduler processes and exclude other materializing callers. Merely
180: requesting a stop, omitting initial work, or relying on an unadopted owner is not proof
181: of exclusion. Keep the exclusion through step 4 when explicit materialization is to
182: control readiness, allowing only that designated materialization. This is an external
183: operational precondition, not an implicit command lock or new durable hold state.
184: If exclusion cannot be verified or is lost, no details-before-delivery guarantee may
185: be claimed. This amendment authorizes no automatic service stop/restart.
186:
187: The supported detail-enabled setup sequence, subject to that ordering qualification, is:
188:
189: 1. Create the item with ordinary presentations and materialization mode `none` to
190:    avoid work creation by this command; this does not exclude automatic scheduling.
191: 2. Explicitly adopt the created item's exact current version into a subject/group
192:    owner using the existing trusted-local ownership provisioning boundary in
193:    [the web API specification, Section 4](trusted-multi-operator-web-api.md).
194:    Adoption is not ownership transfer and grants no inferred creator entitlement.
195: 3. Read the current item version/policy IDs and apply the Section 3.2 presentation-only
196:    edit against that version, resolving the exact definition/disclosure. This edit
197:    still requires materialization mode `none` and creates no work.
198: 4. When delivery is wanted, invoke the existing bounded notification-work
199:    materialization command explicitly and verify the resulting work/readback.
200:    Release any operational exclusion deliberately after the required setup succeeds.
201:    Normal current-time/late-handling eligibility still applies; setup delay neither
202:    extends grace nor creates a guarantee that an expired opportunity will be delivered.
203:
204: These are separately receipted transactions, not one atomic composite. If adoption
205: or selection fails, the already created item remains ordinary; do not auto-delete it
206: or claim the entire sequence rolled back. If strict ordering was required, do not
207: automatically release the exclusion on failure: the operator must finish setup or
208: explicitly accept ordinary delivery before resuming materialization. Retrying uses
209: each step's own command ID and current-version checks. If ordinary work was already materialized, existing
210: attempt/continuity rules apply; later setup cannot retract an already started send.
211: Protected creation's existing envelope ownership orchestration is not removed, but
212: this amendment neither activates rendering there nor extends its registry. An atomic
213: trusted-local owner-plus-rendering create would require a separate explicit contract.
214:
```

Lines 488–560:

```text
488: ## 8. Catalog reads, indexes and capacity
489:
490: Create `notification_rendering_catalog_state(singleton I PK CHECK=1, generation I)`;
491: initialize to 1. Changed create/publish/retire/provision/revoke increments once per
492: transaction. No-op, replay and reads do not increment. Overflow fails closed. Global
493: generation deliberately invalidates pages across owners; it is not a user-visible count.
494:
495: Required indexes: roots `(owner_kind,owner_subject_id,owner_group_id,status,root_id)`
496: with required owner/status predicates; disclosures likewise ending in
497: disclosure_authorization_id; revisions `(root_id,revision_number)`; fields by revision;
498: policy presentations by `(item_id,item_version,notification_policy_id)` and by grant;
499: template-renderings by definition revision. Root/revision IDs refer to the full column
500: names in Section 5. Add reverse-FK indexes for all reference tables and receipt FKs.
501:
502: `match_hash` hashes exactly `{derivation_version: spine.rendering-disclosure-match.v1,
503: canonical_json_version, item_owner, definition, use_scope, destination}`. These fields
504: come from the normalized scope; fields and permitted locations are intentionally
505: excluded. Index disclosures `(match_hash,status,disclosure_authorization_id)`. Unique
506: resolution inspects at most 101 active candidates; if more than 100 exist, fail capacity,
507: even if an early candidate matched. Under the cap, compare full structural scope,
508: effective-key subset and required authority; zero/multiple matching grants retain
509: existing unavailable/ambiguous errors. Empty facet values do not constrain the allowed
510: location set at authoring; each actual location is checked at attempt time. Exact-ID
511: selection uses a PK lookup and the same semantic checks. Never globally scan grants.
512:
513: List uses binary root/grant keyset order, not OFFSET. Filter owner/lifecycle and
514: authority before page size; no totals. Fetch at most limit+1 authorized candidates.
515: Permission-enforced enumeration must use owner rights or indexed grant candidate
516: unions, not unbounded post-filtering. Up to 101 candidates, 100 returned records,
517: 100 access-proof rows, 4 MiB serialized response, 5 seconds and 100000 SQLite VM
518: steps per read (including fence); lower configured limits win. Exceeding a bound is
519: environment_failure, never a partial successful page. Definitions/scopes have their
520: existing per-record byte bounds. One attempt resolves <=8 selections/unique locations
521: by PK; no catalog discovery at send time. Existing runtime transaction ceilings apply.
522:
523: Reserve `spine.notification-rendering-cursor.v1`, prefix `nrc1`. Token is
524: `nrc1.<key_id>.<base64url(payload)>.<base64url(mac)>`, canonical unpadded base64url.
525: MAC = HMAC-SHA256(key, UTF8(`spine.notification-rendering-cursor.v1`) + NUL +
526: UTF8(key_id) + NUL + canonical payload bytes). Protected key config reuses the facet
527: cursor file lifecycle/permissions and minimum 32-byte secret, but uses a distinct
528: domain; no generated fallback. Max token 4096 bytes, original TTL 900 seconds, fixed
529: expiry across pages. Key retirement, restore-generation change or ledger clone invalidates it.
530:
531: Payload has exactly: contract_version, ledger_instance_id, key_generation, command,
532: query_hash, context_hash, access_hash, catalog_generation, last_id, issued_at_utc,
533: expires_at_utc, access_epoch, access_valid_until_utc. Canonical query is
534: `{owner,status,limit}`. Status is required by both existing closed list contracts:
535: definition lists accept `active|retired`, disclosure lists accept `active|revoked`.
536: Omitted, null or otherwise invalid status fails request validation before cursor
537: processing; there is no unfiltered-list mode or null-status normalization. Use the
538: admitted status enum verbatim. Limit is bound, not adjustable mid-pagination.
539: Hash preimages use the exact
540: objects `{derivation_version,canonical_json_version,<named object>}` with domains
541: `spine.rendering-cursor-query.v1`, `spine.rendering-cursor-context.v1`,
542: `spine.rendering-cursor-access.v1` and keys query, context, access respectively.
543: Context is `{mode,account_id,subject_id,audience,ledger_instance_id}`; trusted-local
544: uses null account/subject and audience `trusted_local_full_scope`. Access is
545: `{access_epoch,valid_until_utc}` from the existing permission resolver;
546: trusted-local uses nulls. Payload access_valid_until_utc is that valid_until_utc,
547: null when no temporal transition exists. It limits expiry to the next temporal access
548: transition. Continuation verifies access_hash against these authenticated payload facts,
549: then recomputes authority at current time, checks current epoch/context and rejects an
550: expired transition bound. It does not compare a fresh evaluation timestamp with the
551: old one. Section 11 and the cursor schemas close token field domains and reference
552: vectors; stateful permission and catalog fences remain runtime obligations.
553:
554: Malformed/MAC/query/expired/source/context mismatch is stale_cursor without payload
555: release; missing key/config or capacity is environment_failure. Revalidate current
556: authority and catalog generation after serialization, before release. First-page
557: source/access change is environment_failure; continuation is stale_cursor. No automatic
558: reconstruction, retry, durable cursor session or read receipt. Concurrent retirement,
559: revocation and access changes must never release a stale page.
560:
```

Lines 668–691:

```text
668: Profile create/revise/show/list v2 use the closed successor schemas. V2 read records
669: project a normalized owner object and selected revision envelope rather than raw SQL
670: joins. revision_contract selects the historical v1 or v2 content decoder; old hashes
671: are never recomputed as v2. V2 normalization preserves existing timing normalization,
672: sorts compatible_item_types and templates by template_key, and inserts explicit
673: ordinary rendering for omission. Hash each template without derived fields first;
674: the complete normalized revision includes those normalized_template_hash values.
675: Catalog IDs, row indexes and timestamps do not enter the revision-content preimage.
676: Profile-list v2 retains the existing 1–500 request limit and a maximum 500-entry
677: response; the separate rendering-definition/disclosure catalog's 100-entry bound
678: does not apply to notification-profile lists.
679:
680: Application v2 is a closed projection of a persisted selected-profile application,
681: not a replacement plan or an instruction to select a profile. It carries explicit
682: application_contract, existing application/profile/revision/binding IDs, selection
683: mode, scope_chain, normalized_profile_revision_hash, suppress_template_keys,
684: replacements, custom_additions, ordinary effective-policy hash,
685: effective_presentation_set_hash and policy
686: mappings ordered by notification_policy_id. Each mapping retains policy_origin and
687: source_key as well as the resolved presentation/hash. No selected profile means null
688: application, including custom-only policies; those policies still expose presentation
689: through ordinary policy projections. Schedule create/update notification_profile is
690: this application projection or null. Full schedule.show uses readback v2 with nullable
691: application, nullable pinned/current revision IDs, and the existing upgrade/divergence
```

## docs/NOTIFICATION_RENDERING_GUIDE.md

SHA-256: `ac62bbad1d786579d109d01d04436df8eb7dbecf7b6ff4bbd33c60d1d70d7e78`

Lines 1–94:

```text
1: # Facet-aware notification rendering
2:
3: This is the trusted-local operator guide for the schema-19 rendering release.
4: Start with ordinary scheduling in [the quickstart](AGENT_QUICKSTART.md); use this
5: guide only when reminders should include explicitly selected facet facts.
6:
7: ## Quick decision
8:
9: - Ordinary reminders need no definition or disclosure configuration. Their wording,
10:   work identity and delivery behavior stay unchanged.
11: - Details such as a flight number or terminal require a rendering definition,
12:   destination-specific disclosure authorization, and a recorded policy presentation.
13: - Full evidence uses `spine.schedule-show.v2`. `--compact` stays the existing short
14:   receipt: it deliberately excludes facet values and disclosure evidence.
15: - This release exposes the new families through the local command surface, **not**
16:   the current web command/facet registries. Existing web reads keep their established
17:   summaries or fail closed when their full old projection cannot represent v2.
18: - No definition, profile, pack or chat membership implicitly approves disclosure.
19:
20: The CLI still requires a concrete ledger path. All examples below are request
21: shapes, not authorization to modify a real ledger or send a message.
22:
23: ## 1. Define what can appear
24:
25: Use `notification_rendering_definition.create` with
26: `contract_version=spine.notification-rendering-definitions.v1`. An owner-scoped
27: definition pins the facet schema revision, field keys, labels and compatible item
28: types. It appends bounded deterministic details to the existing concise reminder;
29: it cannot contain executable templates, network lookups or model instructions.
30:
31: Direct scalar values and explicitly permitted location **labels** are supported.
32: Location references remain references; do not copy addresses into string fields to
33: bypass that model. Location projection never releases an address, coordinates or
34: provider metadata. Canonical facts of referenced locations remain immutable.
35:
36: For request shape and vocabulary, see
37: [definition authoring example](../tests/fixtures/notification_rendering_definitions/contracts/request_definition_create.json)
38: and [the command schemas](../contracts/schemas/notification-rendering-definition-commands.schema.json).
39: Use returned IDs, not fixture IDs, when configuring an actual ledger.
40:
41: Read a root/revision with `notification_rendering_definition.show`. Publish a new
42: immutable revision with `.publish`; retire a root with `.retire`. Publishing does
43: not upgrade existing policy pins. Retirement blocks new selection, but existing
44: reminders retain their selected revision. Retirement is **not** disclosure revocation.
45:
46: ## 2. Record reusable, scoped disclosure
47:
48: Use `notification_rendering_disclosure.provision` with
49: `contract_version=spine.notification-rendering-disclosures.v1`. Record the explicit
50: operator instruction and exact scope: item owner, definition root/revision, approved
51: selection keys, profile or direct-policy use, recipient, delivery target, channel,
52: adapter, destination source, target reference, and permitted location IDs.
53:
54: For example: “Include flight number and terminal for this profile's reminders to
55: this family chat.” This is a reusable configuration, not approval of all fields in
56: the facet, all destinations, future definition revisions, or changes in a chat's
57: audience. Each policy records its resolved authorization and selected keys. An
58: event-specific exception can choose a narrower subset; it cannot broaden the grant.
59:
60: Exact authorization IDs avoid ambiguity. Unique-match resolution succeeds only
61: when exactly one current authorization covers the request; ambiguous or missing
62: matches fail authoring atomically. `.show`/`.list` inspect grants; `.revoke` withdraws
63: one without changing historical attempt evidence. Use a new authorization for a
64: new scope rather than editing an immutable grant.
65:
66: See [the scoped authorization example](../tests/fixtures/notification_rendering_definitions/contracts/request_disclosure_provision.json).
67:
68: ## 3. Apply without confusing presentation with scheduling
69:
70: Select these request families explicitly:
71:
72: | Operation | Request selector |
73: | --- | --- |
74: | Profile create/revise/show/list | `spine.notification-profiles.v2` |
75: | Composite creation | `spine.schedule-create.v3` |
76: | Composite update | `spine.schedule-update.v3` |
77: | Full readback | `spine.schedule-show.v2` |
78: | Direct reminder create/edit | nested `authoring_contract=spine.notification-schedule-authoring.v2` |
79:
80: Profile v2 templates carry a `rendering` pin or explicit ordinary rendering. Applying
81: a profile resolves the actual disclosure authorization on the item policy; the
82: profile itself is not a disclosure grant. Existing v1 revisions and receipts retain
83: their original decoders and hashes. Use v2 full readback for successor revisions;
84: do not silently strip rendering to submit a v1 revision.
85:
86: For a fresh trusted-local item:
87:
88: 1. Create with ordinary presentation and `materialization.mode=none`.
89: 2. Establish the item owner through explicit `web_access.plan`/`web_access.apply`
90:    adoption. Creation does not infer ownership from the actor, route or archetype.
91: 3. Attach/verify facet values and issue a v3 presentation-only update, again with
92:    `materialization.mode=none`, using current policy IDs and target item version.
93: 4. Materialize a deliberate bounded horizon if delivery is wanted; verify evidence.
94:
```

Lines 140–159:

```text
140: file owned by the runtime user or root, with no group/other permissions (normally
141: `0600`), containing:
142:
143: ```json
144: {
145:   "contract_version": "spine.notification-rendering-cursor-config.v1",
146:   "key_id": "rendering-1",
147:   "key_generation": "generation-1",
148:   "ledger_instance_id": "<system.info ledger instance>",
149:   "secret_hex": "<32-64 cryptographically random bytes encoded as lowercase hex>"
150: }
151: ```
152:
153: Generate the secret outside model-authored requests; do not put it in chat, receipts,
154: repository files or logs. Keep filters, status and limit unchanged across pages.
155: Rotation, ledger restore/context changes, catalog/access epoch changes or expiry make
156: old cursors stale. Restart from the first page; do not decode and edit cursor payloads.
157:
158: ## Release and rollback checklist
159:
```
```

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-spec-audit-001/spine-wire-evidence.json

Hash: 5afe978bd9db3daaac11f039c9bd28a3a5308465e46f325b45ab6bfc09e3cc71

```markdown
{"purpose":"Read-only source excerpts, not a validator or complete transitive schema closure","spine_commit":"01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7","sources":[{"path":"contracts/schemas/archetype-facet-types.schema.json","sha256":"689163800b0aaa07b87a1fc75a7bea7150bd70f1bcf2fbad901466cdf594dcda","fragments":{"#/$defs/key":{"type":"string","pattern":"^[a-z][a-z0-9_]{0,63}(?![\\s\\S])"},"#/$defs/definition":{"type":"object","required":["display_name","description","compatible_item_types","fields"],"properties":{"display_name":{"type":"string","minLength":1,"maxLength":160},"description":{"anyOf":[{"type":"string","minLength":1,"maxLength":2000},{"type":"null"}]},"compatible_item_types":{"type":"array","items":{"enum":["event","task"]},"minItems":1,"maxItems":2,"uniqueItems":true},"fields":{"type":"array","items":{"$ref":"archetype-facet-types.schema.json#/$defs/field"},"minItems":1,"maxItems":32}},"additionalProperties":false},"#/$defs/field":{"oneOf":[{"type":"object","required":["key","required","type","max_length"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"text"},"queryable":{"type":"boolean","default":false},"max_length":{"type":"string","pattern":"^([1-9]|[1-9][0-9]{1,2}|10[01][0-9]|102[0-4])(?![\\s\\S])"}},"additionalProperties":false},{"type":"object","required":["key","required","type","choices"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"enum"},"queryable":{"type":"boolean","default":false},"choices":{"type":"array","items":{"type":"string","minLength":1,"maxLength":128},"minItems":1,"maxItems":64,"uniqueItems":true}},"additionalProperties":false},{"type":"object","required":["key","required","type"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"boolean"},"queryable":{"type":"boolean","default":false}},"additionalProperties":false},{"type":"object","required":["key","required","type","min","max"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"integer"},"queryable":{"type":"boolean","default":false},"min":{"$ref":"archetype-facet-types.schema.json#/$defs/signedInteger"},"max":{"$ref":"archetype-facet-types.schema.json#/$defs/signedInteger"}},"additionalProperties":false},{"type":"object","required":["key","required","type"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"date"},"queryable":{"type":"boolean","default":false}},"additionalProperties":false},{"type":"object","required":["key","required","type","target_kind"],"properties":{"key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"required":{"type":"boolean"},"type":{"const":"reference"},"queryable":{"type":"boolean","default":false},"target_kind":{"enum":["subject","location"]}},"additionalProperties":false}]},"#/$defs/normalizedDefinition":{"allOf":[{"$ref":"#/$defs/definition"},{"properties":{"fields":{"items":{"required":["queryable"]}}}}]},"#/$defs/root":{"type":"object","required":["facet_schema_id","owner","schema_key","current_revision_id","status"],"properties":{"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"owner":{"$ref":"archetype-facet-types.schema.json#/$defs/owner"},"schema_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"current_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"status":{"enum":["active","retired"]}},"additionalProperties":false},"#/$defs/revision":{"type":"object","required":["facet_schema_id","facet_schema_revision_id","revision_number","definition","definition_hash"],"properties":{"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"revision_number":{"$ref":"archetype-facet-types.schema.json#/$defs/positiveDecimal"},"definition":{"$ref":"#/$defs/normalizedDefinition"},"definition_hash":{"$ref":"archetype-facet-types.schema.json#/$defs/hash"}},"additionalProperties":false},"#/$defs/binding":{"type":"object","required":["facet_binding_id","item_archetype_id","facet_key","facet_schema_revision_id","status"],"properties":{"facet_binding_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"status":{"enum":["active","superseded","retired"]}},"additionalProperties":false}}},{"path":"contracts/schemas/archetype-facet-commands.schema.json","sha256":"29321672a1b7ba31599080e968c1b30295fe68748560cba0a64468a4d0e341aa","fragments":{"#/$defs/facet_schema.create":{"type":"object","required":["contract_version","command_id","actor_subject_id","action_timestamp_utc","owner","schema_key","definition"],"properties":{"contract_version":{"const":"spine.facet-schemas.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"actor_subject_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"action_timestamp_utc":{"$ref":"notification-types.schema.json#/$defs/utcTimestamp"},"owner":{"$ref":"archetype-facet-types.schema.json#/$defs/owner"},"schema_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"definition":{"$ref":"archetype-facet-types.schema.json#/$defs/definition"}},"additionalProperties":false},"#/$defs/facet_schema.publish":{"type":"object","required":["contract_version","command_id","actor_subject_id","action_timestamp_utc","facet_schema_id","expected_current_revision_id","definition"],"properties":{"contract_version":{"const":"spine.facet-schemas.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"actor_subject_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"action_timestamp_utc":{"$ref":"notification-types.schema.json#/$defs/utcTimestamp"},"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"expected_current_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"definition":{"$ref":"archetype-facet-types.schema.json#/$defs/definition"}},"additionalProperties":false},"#/$defs/facet_schema.show":{"type":"object","required":["contract_version","facet_schema_id"],"properties":{"contract_version":{"const":"spine.facet-schemas.v1"},"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"}},"additionalProperties":false},"#/$defs/facet_schema.list":{"type":"object","required":["contract_version","owner"],"properties":{"contract_version":{"const":"spine.facet-schemas.v1"},"owner":{"$ref":"archetype-facet-types.schema.json#/$defs/owner"},"status":{"enum":["active","retired"]},"limit":{"$ref":"archetype-facet-types.schema.json#/$defs/limit"},"cursor":{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"}},"additionalProperties":false},"#/$defs/item_archetype.facet_binding.set":{"type":"object","required":["contract_version","command_id","actor_subject_id","action_timestamp_utc","item_archetype_id","facet_key","facet_schema_revision_id","expected_binding_id"],"properties":{"contract_version":{"const":"spine.archetype-facet-bindings.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"actor_subject_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"action_timestamp_utc":{"$ref":"notification-types.schema.json#/$defs/utcTimestamp"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"expected_binding_id":{"anyOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/id"},{"type":"null"}]}},"additionalProperties":false},"#/$defs/item_archetype.facet_binding.list":{"type":"object","required":["contract_version","item_archetype_id"],"properties":{"contract_version":{"const":"spine.archetype-facet-bindings.v1"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"limit":{"$ref":"archetype-facet-types.schema.json#/$defs/limit"},"cursor":{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"}},"additionalProperties":false}}},{"path":"contracts/schemas/archetype-facet-responses.schema.json","sha256":"ef713cd19b37b48ee014e7fc7e97a23bb7a4657a080a77d6fac3396c0c0ab49e","fragments":{"#/$defs/facet_schema.create":{"oneOf":[{"type":"object","required":["ok","command","response_contract","command_id","command_receipt_id","effect","changed","audit_id","facet_schema_id","prior_revision_id","facet_schema_revision_id","revision_number","replayed"],"properties":{"ok":{"const":true},"command":{"const":"facet_schema.create"},"response_contract":{"const":"spine.facet-schemas.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"command_receipt_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"effect":{"const":"facet_schema_created"},"changed":{"type":"boolean"},"audit_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"prior_revision_id":{"type":"null"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"revision_number":{"const":"1"},"replayed":{"type":"boolean"},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}}},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":true}}}}]}]},"#/$defs/facet_schema.publish":{"oneOf":[{"type":"object","required":["ok","command","response_contract","command_id","command_receipt_id","effect","changed","audit_id","facet_schema_id","prior_revision_id","facet_schema_revision_id","revision_number","replayed"],"properties":{"ok":{"const":true},"command":{"const":"facet_schema.publish"},"response_contract":{"const":"spine.facet-schemas.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"command_receipt_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"effect":{"const":"facet_schema_published"},"changed":{"type":"boolean"},"audit_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"prior_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"revision_number":{"$ref":"archetype-facet-types.schema.json#/$defs/positiveDecimal"},"replayed":{"type":"boolean"},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}}},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":true}}}}]},{"type":"object","required":["ok","command","response_contract","command_id","command_receipt_id","effect","changed","facet_schema_id","prior_revision_id","facet_schema_revision_id","revision_number","replayed"],"properties":{"ok":{"const":true},"command":{"const":"facet_schema.publish"},"response_contract":{"const":"spine.facet-schemas.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"command_receipt_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"effect":{"const":"facet_schema_publish_noop"},"changed":{"type":"boolean"},"facet_schema_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"prior_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"revision_number":{"$ref":"archetype-facet-types.schema.json#/$defs/positiveDecimal"},"replayed":{"type":"boolean"},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}}},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":false}}}}]}]},"#/$defs/facet_schema.show":{"type":"object","required":["ok","command","response_contract","root","revision"],"properties":{"ok":{"const":true},"command":{"const":"facet_schema.show"},"response_contract":{"const":"spine.facet-schemas.v1"},"root":{"$ref":"archetype-facet-types.schema.json#/$defs/root"},"revision":{"$ref":"archetype-facet-types.schema.json#/$defs/revision"},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/facet_schema.list":{"type":"object","required":["ok","command","response_contract","owner","schemas","limit","has_more","next_cursor"],"properties":{"ok":{"const":true},"command":{"const":"facet_schema.list"},"response_contract":{"const":"spine.facet-schemas.v1"},"owner":{"$ref":"archetype-facet-types.schema.json#/$defs/owner"},"schemas":{"type":"array","items":{"$ref":"archetype-facet-types.schema.json#/$defs/root"},"minItems":0,"maxItems":100},"limit":{"$ref":"archetype-facet-types.schema.json#/$defs/limit"},"has_more":{"type":"boolean"},"next_cursor":{"anyOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"},{"type":"null"}]},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"has_more":{"const":true}}},"then":{"properties":{"next_cursor":{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"}}},"else":{"properties":{"next_cursor":{"type":"null"}}}}]},"#/$defs/item_archetype.facet_binding.set":{"oneOf":[{"type":"object","required":["ok","command","response_contract","command_id","command_receipt_id","effect","changed","audit_id","item_archetype_id","facet_key","prior_binding_id","facet_binding_id","facet_schema_revision_id","replayed"],"properties":{"ok":{"const":true},"command":{"const":"item_archetype.facet_binding.set"},"response_contract":{"const":"spine.archetype-facet-bindings.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"command_receipt_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"effect":{"const":"facet_binding_set"},"changed":{"type":"boolean"},"audit_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"prior_binding_id":{"anyOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/id"},{"type":"null"}]},"facet_binding_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"replayed":{"type":"boolean"},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}}},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":true}}}}]},{"type":"object","required":["ok","command","response_contract","command_id","command_receipt_id","effect","changed","item_archetype_id","facet_key","prior_binding_id","facet_binding_id","facet_schema_revision_id","replayed"],"properties":{"ok":{"const":true},"command":{"const":"item_archetype.facet_binding.set"},"response_contract":{"const":"spine.archetype-facet-bindings.v1"},"command_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"command_receipt_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"effect":{"const":"facet_binding_set_noop"},"changed":{"type":"boolean"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_key":{"$ref":"archetype-facet-types.schema.json#/$defs/key"},"prior_binding_id":{"anyOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/id"},{"type":"null"}]},"facet_binding_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"facet_schema_revision_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"replayed":{"type":"boolean"},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}}},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":false}}}}]}]},"#/$defs/item_archetype.facet_binding.list":{"type":"object","required":["ok","command","response_contract","item_archetype_id","bindings","limit","has_more","next_cursor"],"properties":{"ok":{"const":true},"command":{"const":"item_archetype.facet_binding.list"},"response_contract":{"const":"spine.archetype-facet-bindings.v1"},"item_archetype_id":{"$ref":"archetype-facet-types.schema.json#/$defs/id"},"bindings":{"type":"array","items":{"allOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/binding"},{"properties":{"status":{"const":"active"}}}]},"minItems":0,"maxItems":100},"limit":{"$ref":"archetype-facet-types.schema.json#/$defs/limit"},"has_more":{"type":"boolean"},"next_cursor":{"anyOf":[{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"},{"type":"null"}]},"dry_run":{"const":true}},"additionalProperties":false,"allOf":[{"if":{"properties":{"has_more":{"const":true}}},"then":{"properties":{"next_cursor":{"$ref":"archetype-facet-types.schema.json#/$defs/cursor"}}},"else":{"properties":{"next_cursor":{"type":"null"}}}}]}}},{"path":"contracts/schemas/notification-rendering-definition-types.schema.json","sha256":"3b6ea94ce86bbb06f45c63516700235edba43cd0800ed4be05261fc774848344","fragments":{"#/$defs/revision":{"type":"object","required":["display_name","description","compatible_item_types","base_rendering_contract","base_rendering_profile","selections"],"properties":{"display_name":{"type":"string","minLength":1,"maxLength":160},"description":{"oneOf":[{"type":"string","minLength":1,"maxLength":2000},{"type":"null"}]},"compatible_item_types":{"type":"array","items":{"enum":["event","task"]},"minItems":1,"maxItems":2,"uniqueItems":true},"base_rendering_contract":{"const":"spine.notification-rendering.v1"},"base_rendering_profile":{"const":"spine.notification-rendering.concise-en-ca.v1"},"selections":{"type":"array","minItems":1,"maxItems":8,"items":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/selection"}}},"additionalProperties":false},"#/$defs/selection":{"type":"object","required":["selection_key","facet_key","facet_schema_revision_id","field_key","label","projection"],"properties":{"selection_key":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"facet_key":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"facet_schema_revision_id":{"type":"string","minLength":1,"maxLength":256},"field_key":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"label":{"type":"string","minLength":1,"maxLength":40},"projection":{"enum":["value","location_label"]}},"additionalProperties":false},"#/$defs/definitionReference":{"type":"object","required":["notification_rendering_definition_id","notification_rendering_definition_revision_id"],"properties":{"notification_rendering_definition_id":{"type":"string","minLength":1,"maxLength":256},"notification_rendering_definition_revision_id":{"type":"string","minLength":1,"maxLength":256}},"additionalProperties":false},"#/$defs/definitionRecord":{"type":"object","required":["notification_rendering_definition_id","owner","definition_key","status","current_revision_id","notification_rendering_definition_revision_id","revision_number","revision","definition_hash","created","published","retired"],"properties":{"notification_rendering_definition_id":{"type":"string","minLength":1,"maxLength":256},"owner":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/owner"},"definition_key":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"status":{"enum":["active","retired"]},"current_revision_id":{"type":"string","minLength":1,"maxLength":256},"notification_rendering_definition_revision_id":{"type":"string","minLength":1,"maxLength":256},"revision_number":{"type":"string","pattern":"^[1-9][0-9]{0,18}$"},"revision":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/revision"},"definition_hash":{"type":"string","pattern":"^[0-9a-f]{64}$"},"created":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/provenance"},"published":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/provenance"},"retired":{"oneOf":[{"type":"null"},{"type":"object","required":["reason_code","provenance"],"properties":{"reason_code":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"provenance":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/provenance"}},"additionalProperties":false}]}},"additionalProperties":false},"#/$defs/provenance":{"type":"object","required":["command_id","actor_subject_id","action_timestamp_utc"],"properties":{"command_id":{"type":"string","minLength":1,"maxLength":256},"actor_subject_id":{"type":"string","minLength":1,"maxLength":256},"action_timestamp_utc":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/utcTimestamp"}},"additionalProperties":false}}},{"path":"contracts/schemas/notification-rendering-definition-commands.schema.json","sha256":"755135d632e81e3b492533004f8878ab0a9bf20bd3ccb01b94cb76fdc0f45e6d","fragments":{"#/$defs/notification_rendering_definition.create":{"type":"object","required":["contract_version","command_id","actor_subject_id","action_timestamp_utc","owner","definition_key","revision"],"properties":{"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command_id":{"type":"string","minLength":1,"maxLength":256},"actor_subject_id":{"type":"string","minLength":1,"maxLength":256},"action_timestamp_utc":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/utcTimestamp"},"owner":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/owner"},"definition_key":{"type":"string","pattern":"^[a-z][a-z0-9_-]{0,63}$"},"revision":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/revision"}},"additionalProperties":false},"#/$defs/notification_rendering_definition.publish":{"type":"object","required":["contract_version","command_id","actor_subject_id","action_timestamp_utc","notification_rendering_definition_id","expected_current_revision_id","revision"],"properties":{"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command_id":{"type":"string","minLength":1,"maxLength":256},"actor_subject_id":{"type":"string","minLength":1,"maxLength":256},"action_timestamp_utc":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/utcTimestamp"},"notification_rendering_definition_id":{"type":"string","minLength":1,"maxLength":256},"expected_current_revision_id":{"type":"string","minLength":1,"maxLength":256},"revision":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/revision"}},"additionalProperties":false},"#/$defs/notification_rendering_definition.show":{"type":"object","required":["contract_version","notification_rendering_definition_id"],"properties":{"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"notification_rendering_definition_id":{"type":"string","minLength":1,"maxLength":256},"notification_rendering_definition_revision_id":{"type":"string","minLength":1,"maxLength":256}},"additionalProperties":false},"#/$defs/notification_rendering_definition.list":{"type":"object","required":["contract_version","owner","status","limit"],"properties":{"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"owner":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/owner"},"status":{"enum":["active","retired"]},"limit":{"type":"string","pattern":"^([1-9]|[1-9][0-9]|100)(?![\\s\\S])"},"cursor":{"type":"string","minLength":1,"maxLength":4096}},"additionalProperties":false}}},{"path":"contracts/schemas/notification-rendering-definition-responses.schema.json","sha256":"df4352d013699072b0d37ea38299cae613e7ef2123690523a72d23f815d9f4af","fragments":{"#/$defs/notification_rendering_definition.create":{"type":"object","required":["ok","contract_version","command","command_id","changed","replayed","effect","command_receipt_id","audit_id","record"],"properties":{"ok":{"const":true},"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command":{"const":"notification_rendering_definition.create"},"command_id":{"type":"string","minLength":1,"maxLength":256},"changed":{"type":"boolean"},"replayed":{"type":"boolean"},"dry_run":{"const":true},"effect":{"enum":["rendering_definition_created"]},"command_receipt_id":{"type":"string","minLength":1,"maxLength":256},"audit_id":{"type":"string","minLength":1,"maxLength":256},"record":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/definitionRecord"}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}},"required":["replayed"]},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":true}}}}]},"#/$defs/notification_rendering_definition.publish":{"type":"object","required":["ok","contract_version","command","command_id","changed","replayed","effect","command_receipt_id","audit_id","record"],"properties":{"ok":{"const":true},"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command":{"const":"notification_rendering_definition.publish"},"command_id":{"type":"string","minLength":1,"maxLength":256},"changed":{"type":"boolean"},"replayed":{"type":"boolean"},"dry_run":{"const":true},"effect":{"enum":["rendering_definition_published","rendering_definition_publish_noop"]},"command_receipt_id":{"type":"string","minLength":1,"maxLength":256},"audit_id":{"type":"string","minLength":1,"maxLength":256},"record":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/definitionRecord"}},"additionalProperties":false,"allOf":[{"if":{"properties":{"replayed":{"const":true}},"required":["replayed"]},"then":{"properties":{"changed":{"const":false}}},"else":{"if":{"properties":{"effect":{"enum":["rendering_definition_publish_noop"]}},"required":["effect"]},"then":{"properties":{"changed":{"const":false}}},"else":{"properties":{"changed":{"const":true}}}}}]},"#/$defs/notification_rendering_definition.show":{"type":"object","required":["ok","contract_version","command","record"],"properties":{"ok":{"const":true},"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command":{"const":"notification_rendering_definition.show"},"record":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/definitionRecord"},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/notification_rendering_definition.list":{"type":"object","required":["ok","contract_version","command","records","has_more","next_cursor","limit"],"properties":{"ok":{"const":true},"contract_version":{"const":"spine.notification-rendering-definitions.v1"},"command":{"const":"notification_rendering_definition.list"},"records":{"type":"array","maxItems":100,"items":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/definitionRecord"}},"has_more":{"type":"boolean"},"next_cursor":{"oneOf":[{"type":"string","minLength":1,"maxLength":4096},{"type":"null"}]},"dry_run":{"const":true},"limit":{"type":"string","pattern":"^([1-9]|[1-9][0-9]|100)(?![\\s\\S])"}},"additionalProperties":false,"allOf":[{"if":{"properties":{"has_more":{"const":false}},"required":["has_more"]},"then":{"properties":{"next_cursor":{"type":"null"}}},"else":{"properties":{"next_cursor":{"type":"string","minLength":1,"maxLength":4096}}}}]}}},{"path":"contracts/schemas/notification-profile-types-v2.schema.json","sha256":"e1587494d473198b49f16be89e27de12e32df512821d5670f9c8bf48f654f875","fragments":{"#/$defs/template":{"type":"object","required":["template_key","schedule","late_handling"],"properties":{"template_key":{"$ref":"#/$defs/key"},"schedule":{"$ref":"notification-types.schema.json#/$defs/schedule"},"late_handling":{"$ref":"notification-types.schema.json#/$defs/lateHandling"},"rendering":{"$ref":"notification-rendering-integration-types.schema.json#/$defs/templateRendering"}},"additionalProperties":false},"#/$defs/profileRevision":{"type":"object","required":["compatible_item_types","templates"],"properties":{"compatible_item_types":{"$ref":"#/$defs/itemTypes"},"templates":{"type":"array","minItems":1,"maxItems":32,"items":{"$ref":"#/$defs/template"}}},"additionalProperties":false},"#/$defs/normalizedRevision":{"type":"object","required":["compatible_item_types","templates"],"properties":{"compatible_item_types":{"$ref":"notification-profile-types.schema.json#/$defs/itemTypes"},"templates":{"type":"array","minItems":1,"maxItems":32,"items":{"type":"object","required":["template_key","schedule","late_handling","rendering","normalized_template_hash"],"properties":{"template_key":{"$ref":"notification-profile-types.schema.json#/$defs/key"},"schedule":{"$ref":"notification-types.schema.json#/$defs/schedule"},"late_handling":{"$ref":"notification-types.schema.json#/$defs/lateHandling"},"rendering":{"$ref":"notification-rendering-integration-types.schema.json#/$defs/templateRendering"},"normalized_template_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"}},"additionalProperties":false}}},"additionalProperties":false}}},{"path":"contracts/schemas/notification-profile-commands-v2.schema.json","sha256":"a1ee1cfd3d522426a58d35ef43956c7609456ac1a2224d4482edc3f526bc6d54","fragments":{"#/$defs/writeIdentity":{"type":"object","required":["command_id","actor_subject_id","action_timestamp_utc"],"properties":{"command_id":{"$ref":"notification-types.schema.json#/$defs/id"},"actor_subject_id":{"$ref":"notification-types.schema.json#/$defs/id"},"action_timestamp_utc":{"$ref":"notification-types.schema.json#/$defs/utcTimestamp"}}},"#/$defs/profileCreate":{"allOf":[{"$ref":"#/$defs/writeIdentity"},{"type":"object","required":["contract_version","owner","profile_key","display_name","description","revision"],"properties":{"contract_version":{"const":"spine.notification-profiles.v2"},"owner":{"$ref":"notification-profile-types-v2.schema.json#/$defs/owner"},"profile_key":{"$ref":"notification-profile-types-v2.schema.json#/$defs/key"},"display_name":{"type":"string","minLength":1,"maxLength":160},"description":{"oneOf":[{"type":"string","minLength":1,"maxLength":2000},{"type":"null"}]},"revision":{"$ref":"notification-profile-types-v2.schema.json#/$defs/profileRevision"}}}],"unevaluatedProperties":false},"#/$defs/profileRevise":{"allOf":[{"$ref":"#/$defs/writeIdentity"},{"type":"object","required":["contract_version","notification_profile_id","expected_current_revision_id","revision"],"properties":{"contract_version":{"const":"spine.notification-profiles.v2"},"notification_profile_id":{"$ref":"notification-types.schema.json#/$defs/id"},"expected_current_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"},"revision":{"$ref":"notification-profile-types-v2.schema.json#/$defs/profileRevision"}}}],"unevaluatedProperties":false},"#/$defs/profileShow":{"type":"object","required":["contract_version","notification_profile_id"],"properties":{"contract_version":{"const":"spine.notification-profiles.v2"},"notification_profile_id":{"$ref":"notification-types.schema.json#/$defs/id"},"notification_profile_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"}},"additionalProperties":false},"#/$defs/profileList":{"type":"object","required":["contract_version","owner","limit"],"properties":{"contract_version":{"const":"spine.notification-profiles.v2"},"owner":{"$ref":"notification-profile-types-v2.schema.json#/$defs/owner"},"status":{"enum":["active","retired"]},"cursor":{"type":"string","minLength":1},"limit":{"type":"string","pattern":"^([1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)(?![\\s\\S])"}},"additionalProperties":false}}},{"path":"contracts/schemas/notification-profile-responses-v2.schema.json","sha256":"8edc2234ed3797e571430e0db1404f849cb5e2eadd58580fe01af76bd7bba0b9","fragments":{"#/$defs/receipt":{"type":"object","required":["command_receipt_id","command_id","effect","semantic_facts_hash","created_at_utc"],"properties":{"command_receipt_id":{"$ref":"notification-types.schema.json#/$defs/id"},"command_id":{"$ref":"notification-types.schema.json#/$defs/id"},"effect":{"enum":["notification_profile_created","notification_profile_revised"]},"semantic_facts_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"},"created_at_utc":{"$ref":"notification-types.schema.json#/$defs/utcTimestamp"}},"additionalProperties":false},"#/$defs/revision":{"type":"object","required":["notification_profile_revision_id","revision_number","revision_contract","normalized_revision_hash","content"],"properties":{"notification_profile_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"},"revision_number":{"$ref":"notification-types.schema.json#/$defs/decimalPositive"},"revision_contract":{"enum":["spine.notification-profiles.v1","spine.notification-profiles.v2"]},"normalized_revision_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"},"content":{"oneOf":[{"$ref":"#/$defs/historicalRevision"},{"$ref":"notification-profile-types-v2.schema.json#/$defs/normalizedRevision"}]}},"additionalProperties":false,"allOf":[{"if":{"properties":{"revision_contract":{"const":"spine.notification-profiles.v2"}}},"then":{"properties":{"content":{"$ref":"notification-profile-types-v2.schema.json#/$defs/normalizedRevision"}}},"else":{"properties":{"content":{"$ref":"#/$defs/historicalRevision"}}}}]},"#/$defs/profile":{"type":"object","required":["notification_profile_id","owner","profile_key","display_name","description","status","current_revision_id","revision"],"properties":{"notification_profile_id":{"$ref":"notification-types.schema.json#/$defs/id"},"owner":{"$ref":"notification-profile-types.schema.json#/$defs/owner"},"profile_key":{"$ref":"notification-profile-types.schema.json#/$defs/key"},"display_name":{"type":"string","minLength":1,"maxLength":160},"description":{"oneOf":[{"type":"string","minLength":1,"maxLength":2000},{"type":"null"}]},"status":{"enum":["active","retired"]},"current_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"},"revision":{"$ref":"#/$defs/revision"}},"additionalProperties":false},"#/$defs/create":{"type":"object","required":["ok","command","response_contract","effect","notification_profile_id","notification_profile_revision_id","revision_number","profile_key","status","normalized_revision_hash","receipt"],"properties":{"ok":{"const":true},"command":{"const":"notification_profile.create"},"response_contract":{"const":"spine.notification-profiles.v2"},"effect":{"const":"notification_profile_created"},"notification_profile_id":{"$ref":"notification-types.schema.json#/$defs/id"},"notification_profile_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"},"revision_number":{"$ref":"notification-types.schema.json#/$defs/decimalPositive"},"profile_key":{"$ref":"notification-profile-types.schema.json#/$defs/key"},"status":{"const":"active"},"normalized_revision_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"},"receipt":{"$ref":"#/$defs/receipt"},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/revise":{"type":"object","required":["ok","command","response_contract","effect","notification_profile_id","notification_profile_revision_id","revision_number","status","normalized_revision_hash","receipt"],"properties":{"ok":{"const":true},"command":{"const":"notification_profile.revise"},"response_contract":{"const":"spine.notification-profiles.v2"},"effect":{"const":"notification_profile_revised"},"notification_profile_id":{"$ref":"notification-types.schema.json#/$defs/id"},"notification_profile_revision_id":{"$ref":"notification-types.schema.json#/$defs/id"},"revision_number":{"$ref":"notification-types.schema.json#/$defs/decimalPositive"},"status":{"const":"active"},"normalized_revision_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"},"receipt":{"$ref":"#/$defs/receipt"},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/show":{"type":"object","required":["ok","command","response_contract","notification_profile"],"properties":{"ok":{"const":true},"command":{"const":"notification_profile.show"},"response_contract":{"const":"spine.notification-profiles.v2"},"notification_profile":{"$ref":"#/$defs/profile"},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/list":{"type":"object","required":["ok","command","response_contract","entries","count","catalog_snapshot_hash","has_more","next_cursor"],"properties":{"ok":{"const":true},"command":{"const":"notification_profile.list"},"response_contract":{"const":"spine.notification-profiles.v2"},"entries":{"type":"array","minItems":0,"maxItems":500,"items":{"$ref":"#/$defs/profile"}},"count":{"$ref":"notification-types.schema.json#/$defs/decimalNonNegative"},"catalog_snapshot_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"},"has_more":{"type":"boolean"},"next_cursor":{"oneOf":[{"type":"string","minLength":1,"maxLength":4096},{"type":"null"}]},"dry_run":{"const":true}},"additionalProperties":false},"#/$defs/historicalRevision":{"type":"object","required":["compatible_item_types","templates"],"properties":{"compatible_item_types":{"$ref":"notification-profile-types.schema.json#/$defs/itemTypes"},"templates":{"type":"array","minItems":1,"maxItems":32,"items":{"type":"object","required":["template_key","schedule","late_handling","normalized_template_hash"],"properties":{"template_key":{"$ref":"notification-profile-types.schema.json#/$defs/key"},"schedule":{"$ref":"notification-types.schema.json#/$defs/schedule"},"late_handling":{"$ref":"notification-types.schema.json#/$defs/lateHandling"},"normalized_template_hash":{"$ref":"notification-types.schema.json#/$defs/sha256"}},"additionalProperties":false}}},"additionalProperties":false}}},{"path":"contracts/schemas/notification-rendering-integration-types.schema.json","sha256":"5740b6f3e92cdac2f48daf4f85ea79b37803345dfb54a705f5fd8c37ff320aa6","fragments":{"#/$defs/templateRendering":{"oneOf":[{"type":"object","required":["kind"],"properties":{"kind":{"const":"ordinary"}},"additionalProperties":false},{"type":"object","required":["kind","definition"],"properties":{"kind":{"const":"definition"},"definition":{"$ref":"notification-rendering-definition-types.schema.json#/$defs/definitionReference"}},"additionalProperties":false}]}}},{"path":"contracts/archetype-facet-contract-registry.v1.json","sha256":"a344873005ceca6cb526c4dd1c5737c0c1769168f7916596db026d6b7cc87bf6","content":{"schema_version":"spine.archetype-facet-contract-registry.v1","status":"implemented_trusted_local","integration_contract":"contracts/archetype-facet-integration.v1.json","commands":{"facet_schema.create":{"contract_version":"spine.facet-schemas.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.create","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.create","mutates":true},"facet_schema.publish":{"contract_version":"spine.facet-schemas.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.publish","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.publish","mutates":true},"facet_schema.retire":{"contract_version":"spine.facet-schemas.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.retire","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.retire","mutates":true},"facet_schema.show":{"contract_version":"spine.facet-schemas.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.show","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.show","mutates":false},"facet_schema.list":{"contract_version":"spine.facet-schemas.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.list","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.list","mutates":false},"item_archetype.facet_binding.set":{"contract_version":"spine.archetype-facet-bindings.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item_archetype.facet_binding.set","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item_archetype.facet_binding.set","mutates":true},"item_archetype.facet_binding.remove":{"contract_version":"spine.archetype-facet-bindings.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item_archetype.facet_binding.remove","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item_archetype.facet_binding.remove","mutates":true},"item_archetype.facet_binding.list":{"contract_version":"spine.archetype-facet-bindings.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item_archetype.facet_binding.list","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item_archetype.facet_binding.list","mutates":false},"item.facets.update":{"contract_version":"spine.item-facets.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item.facets.update","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item.facets.update","mutates":true},"item.facets.show":{"contract_version":"spine.item-facets.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item.facets.show","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item.facets.show","mutates":false},"item.facets.query":{"contract_version":"spine.item-facet-query.v1","request_schema":"contracts/schemas/archetype-facet-commands.schema.json#/$defs/item.facets.query","response_schema":"contracts/schemas/archetype-facet-responses.schema.json#/$defs/item.facets.query","mutates":false}},"handler_error_exit_codes":{"facet_schema_invalid":2,"facet_value_invalid":2,"facet_binding_conflict":6,"facet_archetype_conflict":6,"facet_schema_retired":2,"facet_reference_unavailable":4,"invalid_request":2,"unsupported_field":2,"missing_required_field":2,"invalid_timestamp":2,"referenced_row_not_found":4,"wrong_item_type":2,"stale_version":5,"stale_cursor":6,"invalid_state_transition":2,"semantic_conflict":6,"environment_failure":7,"runtime_failure":1},"limits":{"definition_bytes":32768,"values_bytes":16384,"snapshot_values_bytes":65536,"max_entries":8,"max_fields":32,"max_page":100},"open_implementation_gates":["permission_resolver_runtime_proof"],"identity_registry":[{"command":"facet_schema.create","row_role":"facet_schema","prefix":"facet_schema","request_path":"/facet_schema"},{"command":"facet_schema.create","row_role":"facet_schema_revision","prefix":"facet_schema_revision","request_path":"/facet_schema/revision"},{"command":"facet_schema.publish","row_role":"facet_schema_revision","prefix":"facet_schema_revision","request_path":"/facet_schema/revision"},{"command":"item_archetype.facet_binding.set","row_role":"archetype_facet_binding","prefix":"archetype_facet_binding","request_path":"/facet_binding"},{"command":"facet_schema.create","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"facet_schema.create","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"},{"command":"facet_schema.publish","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"facet_schema.publish","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"},{"command":"facet_schema.retire","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"facet_schema.retire","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"},{"command":"item_archetype.facet_binding.set","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"item_archetype.facet_binding.set","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"},{"command":"item_archetype.facet_binding.remove","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"item_archetype.facet_binding.remove","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"},{"command":"item.facets.update","row_role":"audit","prefix":"audit","request_path":"/audit"},{"command":"item.facets.update","row_role":"command_receipt","prefix":"command_receipt","request_path":"/"}]}},{"path":"contracts/notification-rendering-definition-contract-registry.v1.json","sha256":"7c02327d44389ef1ddec32194eafddede02629dec9fb4bb2255706e1e9a93103","content":{"schema_version":"spine.notification-rendering-definition-contract-registry.v1","status":"implemented_local","logical_owner":"specs/notification-rendering-definitions.md","commands":{"notification_rendering_definition.create":{"contract_version":"spine.notification-rendering-definitions.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.create","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.create","mutates":true,"exposure":"trusted_local"},"notification_rendering_definition.publish":{"contract_version":"spine.notification-rendering-definitions.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.publish","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.publish","mutates":true,"exposure":"trusted_local"},"notification_rendering_definition.retire":{"contract_version":"spine.notification-rendering-definitions.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.retire","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.retire","mutates":true,"exposure":"trusted_local"},"notification_rendering_definition.show":{"contract_version":"spine.notification-rendering-definitions.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.show","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.show","mutates":false,"exposure":"trusted_local"},"notification_rendering_definition.list":{"contract_version":"spine.notification-rendering-definitions.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.list","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.list","mutates":false,"exposure":"trusted_local"},"notification_rendering_disclosure.provision":{"contract_version":"spine.notification-rendering-disclosures.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_disclosure.provision","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_disclosure.provision","mutates":true,"exposure":"trusted_local"},"notification_rendering_disclosure.revoke":{"contract_version":"spine.notification-rendering-disclosures.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_disclosure.revoke","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_disclosure.revoke","mutates":true,"exposure":"trusted_local"},"notification_rendering_disclosure.show":{"contract_version":"spine.notification-rendering-disclosures.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_disclosure.show","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_disclosure.show","mutates":false,"exposure":"trusted_local"},"notification_rendering_disclosure.list":{"contract_version":"spine.notification-rendering-disclosures.v1","request_schema":"contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_disclosure.list","response_schema":"contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_disclosure.list","mutates":false,"exposure":"trusted_local"}},"effects":{"notification_rendering_definition.create":["rendering_definition_created"],"notification_rendering_definition.publish":["rendering_definition_published","rendering_definition_publish_noop"],"notification_rendering_definition.retire":["rendering_definition_retired","rendering_definition_retire_noop"],"notification_rendering_disclosure.provision":["rendering_disclosure_provisioned"],"notification_rendering_disclosure.revoke":["rendering_disclosure_revoked","rendering_disclosure_revoke_noop"]},"handler_errors":["invalid_request","unsupported_field","missing_required_field","invalid_timestamp","referenced_row_not_found","permission_denied","stale_version","stale_cursor","semantic_conflict","rendering_definition_invalid","rendering_definition_retired","rendering_disclosure_unavailable","rendering_disclosure_ambiguous","rendering_disclosure_scope_mismatch","environment_failure","runtime_failure"],"contracts":{"catalog":"spine.notification-rendering-definitions.v1","disclosure":"spine.notification-rendering-disclosures.v1","presentation":"spine.notification-rendering-presentation.v1","evidence":"spine.notification-rendering-details-evidence.v1","canonical_json":"spine.canonical-json.v1"},"fragments":{"authoring_selection":"contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/authoringSelection","policy_presentation":"contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/policyPresentation","attempt_evidence":"contracts/schemas/notification-rendering-definition-evidence.schema.json"},"limits":{"max_selections":8,"max_label_scalars":40,"max_value_scalars":120,"max_body_scalars":1024,"max_permitted_locations":64,"max_page":100,"max_request_bytes":32768,"max_definition_bytes":8192,"max_scope_bytes":24576,"max_evidence_extension_bytes":16384,"max_cursor_bytes":4096,"max_location_lookups":8},"implementation_gates":["physical_storage_migration_rollback","versioned_profile_schedule_policy_and_attempt_envelopes","presentation_identity_and_policy_specific_work_continuity","permission_resolver_and_location_release_mapping","authenticated_catalog_cursor_and_index_plans","runtime_capability_activation_and_stateful_conformance","facet_referenced_location_freeze_migration_and_fs14"]}},{"path":"contracts/notification-rendering-integration-contract-registry.v1.json","sha256":"a6eecac5aeb16caa9e88a51f717812626ba9175dc586ae8d65ddec9ec99d624c","content":{"contract_version":"spine.notification-rendering-integration-contract-registry.v1","status":"implemented_local","normative_source":"specs/notification-rendering-integration.md","runtime_activation":true,"schemas":["contracts/schemas/notification-rendering-integration-types.schema.json","contracts/schemas/notification-profile-types-v2.schema.json","contracts/schemas/notification-profile-commands-v2.schema.json","contracts/schemas/notification-authoring-v2.schema.json","contracts/schemas/schedule-create-request-v3.schema.json","contracts/schemas/schedule-update-request-v3.schema.json","contracts/schemas/schedule-show-request-v2.schema.json","contracts/schemas/notification-rendering-v2.schema.json","contracts/schemas/notification-profile-application-v2.schema.json","contracts/schemas/notification-profile-readback-v2.schema.json","contracts/schemas/schedule-create-response-v3.schema.json","contracts/schemas/schedule-update-response-v3.schema.json","contracts/schemas/schedule-show-response-v2.schema.json","contracts/schemas/notification-profile-responses-v2.schema.json","contracts/schemas/notification-rendering-cursor.schema.json","contracts/schemas/notification-rendering-cursor-config.schema.json","contracts/schemas/notification-command-v2.schema.json","contracts/schemas/notification-rendering-integration-failure.schema.json"],"commands":{"notification_profile.create":{"contract_version":"spine.notification-profiles.v2","request_schema":"contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileCreate","response_schema":"contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/create","exposure":"trusted_local","mutates":true,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"notification_profile.revise":{"contract_version":"spine.notification-profiles.v2","request_schema":"contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileRevise","response_schema":"contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/revise","exposure":"trusted_local","mutates":true,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"notification_profile.show":{"contract_version":"spine.notification-profiles.v2","request_schema":"contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileShow","response_schema":"contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/show","exposure":"trusted_local","mutates":false,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"notification_profile.list":{"contract_version":"spine.notification-profiles.v2","request_schema":"contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileList","response_schema":"contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/list","exposure":"trusted_local","mutates":false,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"schedule.create":{"contract_version":"spine.schedule-create.v3","request_schema":"contracts/schemas/schedule-create-request-v3.schema.json","response_schema":"contracts/schemas/schedule-create-response-v3.schema.json","exposure":"trusted_local","mutates":true,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"schedule.update":{"contract_version":"spine.schedule-update.v3","request_schema":"contracts/schemas/schedule-update-request-v3.schema.json","response_schema":"contracts/schemas/schedule-update-response-v3.schema.json","exposure":"trusted_local","mutates":true,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"schedule.show":{"contract_version":"spine.schedule-show.v2","request_schema":"contracts/schemas/schedule-show-request-v2.schema.json","response_schema":"contracts/schemas/schedule-show-response-v2.schema.json","exposure":"trusted_local","mutates":false,"failure_schema":"contracts/schemas/notification-rendering-integration-failure.schema.json"}},"fragments":{"spine.notification-schedule-authoring.v2":"contracts/schemas/notification-authoring-v2.schema.json","spine.notification-profile-application.v2":"contracts/schemas/notification-profile-application-v2.schema.json","spine.notification-profile-readback.v2":"contracts/schemas/notification-profile-readback-v2.schema.json","spine.notification-rendering.v2":"contracts/schemas/notification-rendering-v2.schema.json","spine.notification-rendering-cursor.v1":"contracts/schemas/notification-rendering-cursor.schema.json","spine.notification-rendering-cursor-config.v1":"contracts/schemas/notification-rendering-cursor-config.schema.json","direct_reminder_command_envelopes":"contracts/schemas/notification-command-v2.schema.json","standard_failure":"contracts/schemas/notification-rendering-integration-failure.schema.json"},"verification":{"stateful_runtime_verified":true},"semantic_oracles":["normalized_template_and_revision_hashes","presentation_and_set_hashes","attempt_base_details_binding_and_v2_hashes","canonical_signed_cursor_and_current_context_fences","application_address_uniqueness_and_order","profile_readback_null_and_revision_consistency"],"verified_runtime_families":["RI-01","RI-02","RI-03","RI-04","RI-05","RI-06","RI-07","RI-08","RI-09","RI-10","RI-11","RI-12","RI-13","RI-14"]}},{"path":"tests/fixtures/archetype_facets/contracts/request_facet_schema_create.json","sha256":"345d173c8742eb13af29213ff4085360021e7e3c45a045602b40eea0972a4ea6","content":{"contract_version":"spine.facet-schemas.v1","command_id":"fixture-facet_schema.create","actor_subject_id":"operator","action_timestamp_utc":"2026-09-09T10:00:00Z","owner":{"owner_kind":"subject_group","owner_group_id":"travel-team"},"schema_key":"flight_details","definition":{"display_name":"Flight details","description":"Descriptive flight identifiers and airport references.","compatible_item_types":["event"],"fields":[{"key":"origin","required":true,"type":"reference","target_kind":"location","queryable":true},{"key":"flight_number","required":true,"type":"text","max_length":"32","queryable":true},{"key":"airline","required":false,"type":"text","max_length":"128"},{"key":"destination","required":true,"type":"reference","target_kind":"location","queryable":true}]}}},{"path":"tests/fixtures/archetype_facets/contracts/response_facet_schema_publish_replay.json","sha256":"d570921d4dfb14237e6426fd6aed910ede0a4b137676d15fc2df143947e5d212","content":{"ok":true,"command":"facet_schema.publish","response_contract":"spine.facet-schemas.v1","command_id":"fixture-facet_schema.publish","command_receipt_id":"command_receipt_535c76fe7f398e86b615b7e75880bd42d3de0ed9c45ae8811416215741c8da53","effect":"facet_schema_published","changed":false,"audit_id":"audit_3966e681ca708e88f61508bb38dc45d10a120256d13eaa4f0c78aa9700f5494c","facet_schema_id":"facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4","prior_revision_id":"facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8","facet_schema_revision_id":"facet_schema_revision_1726cea8399ecbb54963f4054eaee4344eb21bd64bac0539cb84ac89a0a48372","revision_number":"2","replayed":true}},{"path":"tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_set_noop.json","sha256":"9675548c27c26e68e13dd398b730b09561c2aba828a550eea08a980ad85ea288","content":{"ok":true,"command":"item_archetype.facet_binding.set","response_contract":"spine.archetype-facet-bindings.v1","command_id":"fixture-item_archetype.facet_binding.set","command_receipt_id":"command_receipt_9c58a4461b76231d30ba00cf235cdc20452b416b40b4229d1e10fbe30875be02","effect":"facet_binding_set_noop","changed":false,"item_archetype_id":"archetype-flight","facet_key":"flight_details","prior_binding_id":"archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f","facet_binding_id":"archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f","facet_schema_revision_id":"facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8","replayed":false}},{"path":"tests/fixtures/notification_rendering_definitions/contracts/request_definition_create.json","sha256":"07e356ea3cb608875974bac5ff8b4edc89227a812bd195fce41406220a15bc08","content":{"contract_version":"spine.notification-rendering-definitions.v1","command_id":"rendering-example-create","actor_subject_id":"example-operator","action_timestamp_utc":"2026-10-03T12:00:00Z","owner":{"owner_kind":"subject_group","owner_group_id":"example-group"},"definition_key":"flight_details","revision":{"display_name":"Flight details","description":null,"compatible_item_types":["event"],"base_rendering_contract":"spine.notification-rendering.v1","base_rendering_profile":"spine.notification-rendering.concise-en-ca.v1","selections":[{"selection_key":"flight","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"flight_number","label":"Flight","projection":"value"},{"selection_key":"terminal","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"terminal","label":"Terminal","projection":"value"},{"selection_key":"departure","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"departure_airport","label":"Departure","projection":"location_label"}]}}},{"path":"tests/fixtures/notification_rendering_definitions/contracts/response_definition_create_replay.json","sha256":"c19b5b249038c43968b7ca53209f7adf0662717bf9571898cc8cdd9c6c934178","content":{"ok":true,"contract_version":"spine.notification-rendering-definitions.v1","command":"notification_rendering_definition.create","command_id":"rendering-example-create","changed":false,"replayed":true,"effect":"rendering_definition_created","command_receipt_id":"command_receipt_dd4776c5d577d6546bfd1a8355f613a2ff15ea56df1d73e9e66e4f0a3d1502b3","audit_id":"audit_dc74aec2532b800cebd3e45400dda9b093ed1bdec7ce94f29eb06d0fc3fa73e1","record":{"notification_rendering_definition_id":"notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe","notification_rendering_definition_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52","owner":{"owner_kind":"subject_group","owner_group_id":"example-group"},"definition_key":"flight_details","status":"active","current_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52","revision_number":"1","revision":{"display_name":"Flight details","description":null,"compatible_item_types":["event"],"base_rendering_contract":"spine.notification-rendering.v1","base_rendering_profile":"spine.notification-rendering.concise-en-ca.v1","selections":[{"selection_key":"flight","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"flight_number","label":"Flight","projection":"value"},{"selection_key":"terminal","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"terminal","label":"Terminal","projection":"value"},{"selection_key":"departure","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"departure_airport","label":"Departure","projection":"location_label"}]},"definition_hash":"6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb","created":{"command_id":"rendering-example-create","actor_subject_id":"example-operator","action_timestamp_utc":"2026-10-03T12:00:00Z"},"published":{"command_id":"rendering-example-create","actor_subject_id":"example-operator","action_timestamp_utc":"2026-10-03T12:00:00Z"},"retired":null}}},{"path":"tests/fixtures/notification_rendering_definitions/contracts/response_definition_publish_noop.json","sha256":"7089a2fdb00c475710db37c55ed22a5e835f606bb8002d9916ba06e3ee18d5f7","content":{"ok":true,"contract_version":"spine.notification-rendering-definitions.v1","command":"notification_rendering_definition.publish","command_id":"rendering-example-publish-noop","changed":false,"replayed":false,"effect":"rendering_definition_publish_noop","command_receipt_id":"command_receipt_c92376d4bcb98d1dec472473e31d6f71bf46ca68921097937fad81a556e9ecd5","audit_id":"audit_7ded09e8e81bdeb89066850363a08ed8ce852b44c4273001d46bf77bbcf95136","record":{"notification_rendering_definition_id":"notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe","notification_rendering_definition_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52","owner":{"owner_kind":"subject_group","owner_group_id":"example-group"},"definition_key":"flight_details","status":"active","current_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52","revision_number":"1","revision":{"display_name":"Flight details","description":null,"compatible_item_types":["event"],"base_rendering_contract":"spine.notification-rendering.v1","base_rendering_profile":"spine.notification-rendering.concise-en-ca.v1","selections":[{"selection_key":"flight","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"flight_number","label":"Flight","projection":"value"},{"selection_key":"terminal","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"terminal","label":"Terminal","projection":"value"},{"selection_key":"departure","facet_key":"flight_details","facet_schema_revision_id":"facet_schema_revision_flight_v1","field_key":"departure_airport","label":"Departure","projection":"location_label"}]},"definition_hash":"6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb","created":{"command_id":"rendering-example-create","actor_subject_id":"example-operator","action_timestamp_utc":"2026-10-03T12:00:00Z"},"published":{"command_id":"rendering-example-create","actor_subject_id":"example-operator","action_timestamp_utc":"2026-10-03T12:00:00Z"},"retired":null}}},{"path":"tests/fixtures/notification_rendering_integration/request_profile_create.json","sha256":"9c7f9ad2483c1a9b784d824e17631d9d3af29ba6c2decdb40332654420343ac4","content":{"contract_version":"spine.notification-profiles.v2","command_id":"fixture-profile-create","actor_subject_id":"subject_agent","action_timestamp_utc":"2035-02-01T12:00:01Z","owner":{"owner_kind":"subject","owner_subject_id":"subject_owner"},"profile_key":"appointment_standard","display_name":"Appointment standard","description":"One day before","revision":{"compatible_item_types":["event"],"templates":[{"template_key":"day_before","schedule":{"kind":"once","at":{"kind":"target_offset","offset_basis":"elapsed","offset_seconds":"-86400"}},"late_handling":{"kind":"skip"},"rendering":{"kind":"definition","definition":{"notification_rendering_definition_id":"notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe","notification_rendering_definition_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"}}}]}}},{"path":"tests/fixtures/notification_rendering_integration/response_profile_historical_v1.json","sha256":"4c3862d38b09e00b5b3c0a3c733fe1274807943bdfd31dac90c85ab864c0e230","content":{"ok":true,"command":"notification_profile.show","response_contract":"spine.notification-profiles.v2","notification_profile":{"notification_profile_id":"profile-example","owner":{"owner_kind":"subject","owner_subject_id":"subject_owner"},"profile_key":"appointment_standard","display_name":"Appointment standard","description":"One day before","status":"active","current_revision_id":"revision-example","revision":{"notification_profile_revision_id":"revision-old","revision_number":"1","revision_contract":"spine.notification-profiles.v1","normalized_revision_hash":"8dcae6cd5b03d21a1945ce6407fe622fdb9f6b9da03dd5449e4ef3022d26a7b6","content":{"compatible_item_types":["event"],"templates":[{"template_key":"day_before","schedule":{"kind":"once","at":{"kind":"target_offset","offset_basis":"elapsed","offset_seconds":"-86400"}},"late_handling":{"kind":"skip"},"normalized_template_hash":"b2316725c7b9ee85862cbe9709d4e0ebe0afbcc7550e74371434ef31ab9628f2"}]}}}}},{"path":"tests/fixtures/notification_rendering_integration/response_profile_create.json","sha256":"5fd1f6cd04e5579111cfcfad5d0f61441cf7b280dee1f4baed2cb1ca3a9f82f2","content":{"ok":true,"command":"notification_profile.create","response_contract":"spine.notification-profiles.v2","effect":"notification_profile_created","notification_profile_id":"profile-example","notification_profile_revision_id":"revision-example","revision_number":"1","status":"active","normalized_revision_hash":"dfde522127e4cdb593d0946e8ea04a0b82692b43db2de933b80fc47bf415816e","receipt":{"command_receipt_id":"receipt-example","command_id":"command-example","effect":"notification_profile_created","semantic_facts_hash":"036d030445d89c3bca7804fec6b020b625df927e23a19d164466e71f5bb2f858","created_at_utc":"2035-02-01T12:00:01Z"},"profile_key":"appointment_standard"}},{"path":"tests/fixtures/notification_rendering_integration/invalid_template_grant.json","sha256":"88a695eff1a7e4e42e06bde8a4c8872745b0e6773314372314e1463d7fe8239c","content":{"contract_version":"spine.notification-profiles.v2","command_id":"fixture-profile-create","actor_subject_id":"subject_agent","action_timestamp_utc":"2035-02-01T12:00:01Z","owner":{"owner_kind":"subject","owner_subject_id":"subject_owner"},"profile_key":"appointment_standard","display_name":"Appointment standard","description":"One day before","revision":{"compatible_item_types":["event"],"templates":[{"template_key":"day_before","schedule":{"kind":"once","at":{"kind":"target_offset","offset_basis":"elapsed","offset_seconds":"-86400"}},"late_handling":{"kind":"skip"},"rendering":{"kind":"definition","definition":{"notification_rendering_definition_id":"notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe","notification_rendering_definition_revision_id":"notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"},"disclosure_authorization_id":"client-grant"}}]}}}],"compiled_registry":{"path":"src/spine/commands/registry.py","sha256":"27a54280f0b1ca19d579be94e7faa68f4cac3f7644a2cd31390f2ce86411ad4e","method":"Literal requirement calls plus profile-v2 successor and common integration/canonical requirements; no Spine imports executed","source_lines_283_339":"_requirements(\n    {\n        \"notification_rendering_definition.create\",\n        \"notification_rendering_definition.publish\",\n        \"notification_rendering_definition.retire\",\n        \"notification_rendering_definition.show\",\n    },\n    \"spine.notification-rendering-definitions.v1\",\n)\n_requirements(\n    {\"notification_rendering_definition.list\"}, \"spine.notification-rendering-definitions.v1\", \"spine.notification-rendering-cursor.v1\"\n)\n_requirements(\n    {\"notification_rendering_disclosure.provision\", \"notification_rendering_disclosure.revoke\", \"notification_rendering_disclosure.show\"},\n    \"spine.notification-rendering-disclosures.v1\",\n)\n_requirements(\n    {\"notification_rendering_disclosure.list\"}, \"spine.notification-rendering-disclosures.v1\", \"spine.notification-rendering-cursor.v1\"\n)\n_SUCCESSOR_REQUIREMENTS = {\n    \"schedule.create\": (\n        \"spine.schedule-create.v3\",\n        \"spine.schedule-create-response.v3\",\n        \"spine.schedule-create-receipt.v3\",\n        \"spine.notification-profile-application.v2\",\n    ),\n    \"schedule.update\": (\n        \"spine.schedule-update.v3\",\n        \"spine.schedule-update-response.v3\",\n        \"spine.schedule-update-receipt.v3\",\n        \"spine.notification-profile-application.v2\",\n    ),\n    \"schedule.show\": (\"spine.schedule-show.v2\", \"spine.notification-profile-readback.v2\", \"spine.notification-rendering.v2\"),\n    **{\n        c: (\"spine.notification-profiles.v2\",)\n        for c in (\"notification_profile.create\", \"notification_profile.revise\", \"notification_profile.show\", \"notification_profile.list\")\n    },\n    **{c: (\"spine.notification-schedule-authoring.v2\",) for c in (\"reminder.create\", \"reminder.edit\")},\n}\nfor _command, _versions in _SUCCESSOR_REQUIREMENTS.items():\n    _ADDITIONAL_REQUIREMENTS[_command] += _versions\nfor _command in _ADDITIONAL_REQUIREMENTS:\n    _ADDITIONAL_REQUIREMENTS[_command] += (\"spine.notification-rendering-integration.v1\",)\n\n\ndef _entry(command: str, additional: tuple[str, ...]) -> CommandContractEntry:\n    return CommandContractEntry(\n        command=command,\n        access_mode=\"read\" if command in _READ_COMMANDS else \"write\",\n        required_contract_versions=tuple(sorted({CANONICAL_JSON_CONTRACT, *additional})),\n    )\n\n\ndef frozen_web_required_contract_versions(command: str) -> tuple[str, ...]:\n    \"\"\"Preserve exact HTTP-family pins while admitting the larger local runtime.\n\n    Only this release's explicitly local additions are subtracted. A changed","proposed_command_requirements":{"facet_schema.create":["spine.canonical-json.v1","spine.facet-schemas.v1","spine.notification-rendering-integration.v1"],"facet_schema.list":["spine.canonical-json.v1","spine.facet-cursor.v1","spine.facet-schemas.v1","spine.notification-rendering-integration.v1"],"facet_schema.publish":["spine.canonical-json.v1","spine.facet-schemas.v1","spine.notification-rendering-integration.v1"],"facet_schema.show":["spine.canonical-json.v1","spine.facet-schemas.v1","spine.notification-rendering-integration.v1"],"item_archetype.create":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-rendering-integration.v1"],"item_archetype.facet_binding.list":["spine.archetype-facet-bindings.v1","spine.canonical-json.v1","spine.facet-cursor.v1","spine.notification-rendering-integration.v1"],"item_archetype.facet_binding.set":["spine.archetype-facet-bindings.v1","spine.canonical-json.v1","spine.notification-rendering-integration.v1"],"item_archetype.list":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-rendering-integration.v1"],"item_archetype.revise":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-rendering-integration.v1"],"item_archetype.show":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-rendering-integration.v1"],"notification_profile.binding.list":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-bindings.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-rendering-integration.v1"],"notification_profile.binding.set":["spine.canonical-json.v1","spine.item-archetypes.v1","spine.notification-profile-bindings.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-rendering-integration.v1"],"notification_profile.create":["spine.canonical-json.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-profiles.v2","spine.notification-rendering-integration.v1"],"notification_profile.list":["spine.canonical-json.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-profiles.v2","spine.notification-rendering-integration.v1"],"notification_profile.metadata.update":["spine.canonical-json.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-metadata-update.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-rendering-integration.v1"],"notification_profile.revise":["spine.canonical-json.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-profiles.v2","spine.notification-rendering-integration.v1"],"notification_profile.show":["spine.canonical-json.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-profiles.v2","spine.notification-rendering-integration.v1"],"notification_rendering_definition.create":["spine.canonical-json.v1","spine.notification-rendering-definitions.v1","spine.notification-rendering-integration.v1"],"notification_rendering_definition.list":["spine.canonical-json.v1","spine.notification-rendering-cursor.v1","spine.notification-rendering-definitions.v1","spine.notification-rendering-integration.v1"],"notification_rendering_definition.publish":["spine.canonical-json.v1","spine.notification-rendering-definitions.v1","spine.notification-rendering-integration.v1"],"notification_rendering_definition.show":["spine.canonical-json.v1","spine.notification-rendering-definitions.v1","spine.notification-rendering-integration.v1"],"system.info":["spine.canonical-json.v1","spine.ledger-instance.v1","spine.notification-rendering-integration.v1","spine.system-info.v3","spine.tickerd-compatibility.v1"]},"execution_union":["spine.archetype-facet-bindings.v1","spine.canonical-json.v1","spine.facet-cursor.v1","spine.facet-schemas.v1","spine.item-archetypes.v1","spine.ledger-instance.v1","spine.notification-profile-bindings.v1","spine.notification-profile-catalog-cursor.v1","spine.notification-profile-metadata-update.v1","spine.notification-profile-readback.v1","spine.notification-profiles.v1","spine.notification-profiles.v2","spine.notification-rendering-cursor.v1","spine.notification-rendering-definitions.v1","spine.notification-rendering-integration.v1","spine.system-info.v3","spine.tickerd-compatibility.v1"]}}
```

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-spec-audit-001/spine-readback-blocker.md

Hash: 476118d87cfd520a2dcba18ceca4325c6dbeb480bafbc057bbca6e7fd0872c82

```markdown
# Exact-baseline profile-list source conflict

Pinned source: `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`.
This is a source inspection inference, not an executed public-CLI regression.
The v2 profile list calls the shared legacy list; that list rejects stored v2
revisions before the caller can project them to v2. A separate disposable
public-CLI reproduction is a gate; no source repair or baseline change is authorized.

The snippets also show v2 request normalization before receipt-producing dispatch.
They are supplied for review only, not an installer internal-API interface.

## src/spine/commands/rendering_candidate.py

Full source SHA-256: `14363914ea733ec9ef9b9b1377b34d1573742050198f8ecfa807aaf4589e400e`

Lines 22–49:

```text
22: def accepts(command, request):
23:     if command.startswith(("notification_rendering_definition.", "notification_rendering_disclosure.")):
24:         return True
25:     selector = request.get("contract_version")
26:     if command in {"notification_profile.create", "notification_profile.revise", "notification_profile.show", "notification_profile.list"}:
27:         return selector == codec.PROFILE_V2
28:     if command in {"schedule.create", "schedule.update"}:
29:         return selector == ("spine.schedule-create.v3" if command.endswith("create") else "spine.schedule-update.v3")
30:     if command in {"reminder.create", "reminder.edit"}:
31:         patch = request.get("patch")
32:         notification = (
33:             request.get("notification") if command.endswith("create") else (patch.get("notification") if isinstance(patch, dict) else None)
34:         )
35:         return isinstance(notification, dict) and notification.get("authoring_contract") == "spine.notification-schedule-authoring.v2"
36:     return False
37:
38:
39: def normalized_request(command, request):
40:     value = copy.deepcopy(dict(request))
41:     codec.bounded(value, 32768, "request")
42:     if command in {"notification_profile.create", "notification_profile.revise"}:
43:         revision = codec.normalize_profile_v2(value.get("revision"))
44:         value["revision"] = {
45:             "compatible_item_types": list(revision.compatible_item_types),
46:             "templates": [{k: v for k, v in template.items() if k != "normalized_template_hash"} for template in revision.templates],
47:         }
48:     patch = value.get("patch", {})
49:     if not isinstance(patch, dict):
```

Lines 72–89:

```text
72: def execute(command, request, context, *, admission=None, cursor_config=None, now=None):
73:     db = context.ledger
74:     admission = admission or RenderingAdmission()
75:     timestamp = now or wire_time(utc_now())
76:     try:
77:         invariant(getattr(db, "_renderings_enabled", False) and not db.in_transaction, "candidate storage is required")
78:         if command.startswith(("notification_rendering_definition.", "notification_rendering_disclosure.")):
79:             return rendering_catalog.execute(command, request, context, admission=admission, cursor_config=cursor_config, now=timestamp)
80:         value = normalized_request(command, request)
81:         if command.startswith("notification_profile."):
82:             budget = FacetBudget()
83:             old_timeout = install_budget(db, budget)
84:             try:
85:                 return rendering_profiles.execute(command, value, context, admission=admission, now=timestamp, budget=budget)
86:             finally:
87:                 db.set_progress_handler(None, 0)
88:                 db.execute(f"PRAGMA busy_timeout={old_timeout}")
89:         handlers = {
```

## src/spine/commands/rendering_profiles.py

Full source SHA-256: `9facbbac4fc237d7eb8344c97c622a48be97e5d7ff099eae7d0e8179c605b53d`

Lines 118–133:

```text
118:                 "notification_profile": project(
119:                     load_profile(db, request["notification_profile_id"], revision_id=request.get("notification_profile_revision_id"))
120:                 ),
121:             }
122:         elif command == "notification_profile.list":
123:             # Preserve the profile family's fixed 1..500, snapshot/key cursor semantics.
124:             old = dict(request, contract_version="spine.notification-profiles.v1")
125:             if permissions and not permissions.scope(codec.owner(request["owner"])):
126:                 codec.fail("permission_denied", "owner")
127:             result = shared._list_roots(old, context, kind="notification_profile")
128:             result["response_contract"] = codec.PROFILE_V2
129:             result["entries"] = [project(load_profile(db, r["notification_profile_id"])) for r in result["entries"]]
130:         else:
131:             codec.fail("invalid_request", "command")
132:         codec.bounded(result, 4 * 1024 * 1024, "capacity")
133:     return result | ({"dry_run": True} if context.dry_run else {})
```

## src/spine/commands/notification_profiles.py

Full source SHA-256: `d33c9b0d51e6c1758a311551d2695cfe6d63cf246a5bce373b86ebd1293797a4`

Lines 818–825:

```text
818: def _legacy_profile(entry):
819:     """A frozen v1 full projection cannot label successor content as v1."""
820:     revision = entry["revision"]
821:     if revision.get("revision_contract") == "spine.notification-profiles.v2":
822:         raise SpineValidationError("unsupported_contract_version:contract_version", "use spine.notification-profiles.v2 for this revision")
823:     revision.pop("revision_contract", None)
824:     return entry
825:
```

Lines 912–932:

```text
912:             row
913:             for row in rows
914:             if (str(row[key_field]), str(row[id_field])) > last
915:         ]
916:     has_more = len(rows) > limit
917:     page = rows[:limit]
918:     loader = load_archetype if kind == "item_archetype" else load_profile
919:     entries = [
920:         loader(connection, str(row[id_field]))
921:         for row in page
922:     ]
923:     if kind == "notification_profile":
924:         entries = [_legacy_profile(entry) for entry in entries]
925:     next_cursor = None
926:     if has_more and page:
927:         final = page[-1]
928:         next_cursor = _encode_catalog_cursor(
929:             {
930:                 "cursor_version": "spine.notification-profile-catalog-cursor.v1",
931:                 "query": query_facts,
932:                 "snapshot_hash": snapshot_hash,
```
```
