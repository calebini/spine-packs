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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-fr1-manifest-audit-001/audit-notes.md
Hash: 9e7a2e86460eb9e3bd97a84d8ae7164d3ae4c9dcb90b60f5cebe27adb2828cee

# Change intent

Review the first, manifest-only increment of FR-1 for facet-aware Spine packs.
The draft v2 manifest schema, synthetic flight fixture, indexed mutation vectors,
and test-only semantic oracle are authored. This is NOT the complete FR-1 slice:
the seven installer artifact schemas, public request/response closure, exact
resolution-slot encoding, aggregate observation budgets and execution/recovery
fixture suite have not been implemented. Their absence must remain visible;
do not mistake this bounded review for their acceptance or permission for FR-2.

The operator explicitly selected repaired Spine commit
`57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema `19`.
The old `01ebce7` / `0.9.0` profile-v2 listing issue is historical evidence.
Spine Packs independently passed the narrow installed-wheel public-CLI listing
gate. That does not qualify an installer on 0.9.1. Existing runtime support,
v1 contracts and released pack bytes remain unchanged.

# Expected boundary

One reviewer-only `audit-change` with profile `consistency`; no Editor,
automatic patches, convergence claim, ledger access, tools to inspect unrelated
files, external browsing, deployment or publication. This package is staged
only and requires approval of the exact inventory in APPROVAL.md before any
nested reviewer invocation. Model/executable selection is a launch-time preflight.

Packs remain owner-neutral declarative configuration. Spine alone owns installed
state, authorization, rendering, scheduling and history. An installer must use
public commands only, never direct SQL or internal handler shortcuts. Installation
does not authorize disclosure, create events, attach item facets, materialize
reminders or send notifications.

The user explicitly deferred real flight-field, label/order, template-selection,
default-profile and destination-disclosure decisions. Synthetic fixture choices
are test data, not a product decision. Flag a design that forecloses those choices;
do not choose policy on the user's behalf.

# Review targets

Primary: `contracts/schemas/spine-pack-manifest.v2.schema.json`,
`contracts/pack-fixture-manifest.v2.json`,
`tests/fixtures/pack-manifest-v2/flight.json`, and
`tests/contract/test_facet_manifest_contract.py`, against the proposed normative
requirements in `specs/facet-rendering-packs.md`, especially Sections 2–4 and 11.
Other supplied repository docs and the v1 manifest schema are preservation context.
The supplied public-CLI gate script and baseline doc support only the narrow
repaired-listing claim. The supplied Spine evidence file includes focused public
schema/normalization excerpts with exact Git source hashes; it is not a complete
transitive schema closure or authorization to read the Spine checkout.

Check especially:

1. Closed v2 manifest shape, explicit ordinary/definition rendering, strict
   facet key grammar versus other catalog keys, required normalized fields,
   owner neutrality, and preservation of v1 identity/timing bounds.
2. Pack-local references and graph validation: missing/wrong-kind/cross-pack
   references; unique defaults and facet bindings; field/type/projection checks;
   item-type compatibility through bindings and profile/rendering/schema uses.
3. Canonical ordering and digest behavior, including rendering selections as
   authored presentation order, not a sortable set. Unicode/normalization and
   duplicate-member/number rules must not be silently weakened by the oracle.
4. Fixture proof and test quality: do the 35 indexed vectors test the claimed
   failure stage rather than passing by unrelated failure? Identify missing
   high-value vectors and schema/prose/oracle disagreement within this increment.
5. Exact compatibility: only the approved 0.9.1 pin is the successor target;
   no implicit range, rewritten v1 artifact or assumption that system.info proves
   source provenance. The current installer cannot consume this draft manifest.
6. Honest boundaries: test-only scalar/location-label choices are not curated
   content or disclosure grants; installed-wheel listing is not full installer
   qualification; a manifest review does not close the remaining FR-1 work.

Report actionable findings with exact affected file/section and minimal proposed
correction. Do not rewrite or widen the architecture. Unfinished later deliverables
are known remaining gates, not automatically defects in this manifest increment;
however, any false completion claim or unsafe dependency assumption is in scope.

# Current checks and exclusions

Before staging: repository verifier passed (125 required files); all 70 contract
tests passed under the isolated Python with jsonschema 4.26.0, including independent
Draft 2020-12 schema checking and the v2 matrix; tracked whitespace checks passed.
The preceding unchanged runtime suite passed 126 tests; it was not rerun merely
to stage this package. Default Python lacks jsonschema and visibly skips the
five new test methods, so its result alone is not the v2 schema gate.

No successor installer behavior, executable runtime validator, curated pack,
release, live target or full installer-artifact review is claimed. Do not request
private ledger state, credentials, disclosure catalogs or an entire source tree.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/AGENTS.md

Hash: 4bde9b65981a3d787e17b4d2d8eb37353a5e960f249c9c708c736a24c91df4e0

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
specification and FR-1 contract/fixture scope; it does not authorize successor
runtime work. The explicitly authorized repaired-baseline listing gate may use
new disposable ledgers through public CLIs only, never an existing ledger.

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

The facet/rendering proposal now pins exact Spine commit
`57cda1c2d5589360ee8efe7155fd20b503034c2a` (`0.9.1`, schema `19`). The original
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7` listing finding and audit are historical
evidence and MUST NOT be rewritten. Existing
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

Hash: 4b8d77b0abd6a958d3b8bdc48b2ebaeafc75e4157f91ea1b9762b5f493d1404f

```markdown
# Architecture

## Proposed facet/rendering successor — not implemented

[facet-rendering-packs.md](facet-rendering-packs.md) proposes a separate manifest
and installer-artifact v2 path for exact Spine `0.9.1` / schema `19` at
`57cda1c2d5589360ee8efe7155fd20b503034c2a`. It adds a bounded configuration graph:
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

Hash: 11ee544c49dfb346e5572d54cb29eb82867136203c4c966dce7b750e37e2baa3

```markdown
# Compatibility

## Proposed 0.9.1 successor — not a support claim

[facet-rendering-packs.md](facet-rendering-packs.md) proposes manifest v2 and
installer-artifact v2 against exact Spine commit
`57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema `19`.
The inspected command/contract matrix is in
[the baseline evidence](../docs/facet-rendering-baseline.md). The repaired listing
gate passed; the draft v2 manifest schema now permits exactly `0.9.1`. This adds
nothing to any existing v1 manifest, schema or runtime allowlist.
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

Hash: bee633028513c1b26515ec6fd0c03e834bf968d73668fa24209a9b63686cb2ac

```markdown
# Pack format requirements

The proposed facet/rendering successor is specified separately in
[facet-rendering-packs.md](facet-rendering-packs.md). It reserves
`spine.pack-manifest.v2`; its draft manifest schema and test-only fixture are now
authored for FR-1 review, but installer support is not implemented. It does not
amend the closed v1 objects below. No curated successor manifest or release is
created by that proposal.

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

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/facet-rendering-packs.md

Hash: 17627e5f9f22a389978bfd87c943360dc8bda857938b18e747de18e8e3576c24

```markdown
# Facet-aware packs: successor contract proposal

Status: proposed; FR-1 contract/fixture work in progress, runtime not implemented.
Repaired baseline inspected on 2026-10-10. Normative language below defines
the proposed successor, not additional authority for the current installer.

## 1. Scope and authority

Propose `spine.pack-manifest.v2` and a separately versioned v2 installer-artifact
family for one flight configuration vertical slice. Preserve v1 decoders,
schemas, fixtures, installer behavior and every released/draft pack artifact.
Do not add rendering fields to a frozen v1 shape or relabel v1 content as v2.

The exact reference is Spine `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime
`0.9.1`, implemented/current ledger schema `19`. The operator explicitly supplied
this replacement pin; inspection and the disposable listing gate used an export
of its exact Git tree, not a newer working tree.
[Baseline evidence](../docs/facet-rendering-baseline.md) records public contracts,
wire differences and qualification gaps. Existing installer `0.3.0` does not
support this baseline. This proposal neither widens its allowlist nor qualifies
a target installation.

The original `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7` / `0.9.0` baseline
had a profile-v2-list blocker. Its finding and approved audit remain historical
evidence, not a qualified target. The repaired pin passed the independent
public-CLI listing gate described in the baseline evidence. That narrow gate
does not qualify installer plan/apply/recovery/verify or authorize runtime work.
No list bypass, internal read, or implicit compatibility range is permitted.

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

Use Spine's facet-key grammar (lowercase letters, digits and underscores, no
hyphens) for schema keys, facet-binding keys, schema references and selected field
keys. Other catalog keys retain their existing grammar. A rendering selection
cannot widen the grammar of a field or facet it must resolve.

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
For a definition-pinned profile template, the portable manifest field is
`rendering.definition_ref.definition_key`. Resolution replaces `definition_ref`
with Spine's `rendering.definition` object containing the exact root and revision
IDs; it does not rename the portable field or add ledger IDs to pack content.
The consumer paths below refer to materialized Spine requests, not manifest
fields. Only these new ID-consuming paths are added to the reviewed mapping:

| Materialized Spine request input | Producer output when unresolved |
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

The first v2 pack declares exactly runtime `["0.9.1"]`. Content contracts are:

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
0.9.1 environment, typed graph/closure and resolution slots, complete observation
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

Spine 0.9.1 requires a rendering application choice for each surviving definition-
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

Technical review gates, not product-policy questions: the repaired profile-list gate
has passed as described in Section 1; exact v2 artifact schemas,
reference-slot syntax, aggregate observation budgets, response correlation and
fault-injection oracles must be codified and reviewed before their runtime slices.
Exact 0.9.1 public-CLI and clean-wheel qualification remains outstanding. If a
public-command gap is found, report it; this task grants no Spine change authority.

## 11. Codification prerequisites and acceptance

The ordered delivery slices are in [implementation-plan.md](implementation-plan.md).
The first FR-1 increment codifies only the manifest in
`contracts/schemas/spine-pack-manifest.v2.schema.json`, with a synthetic draft
flight in `tests/fixtures/pack-manifest-v2/flight.json` and indexed mutation
vectors in `contracts/pack-fixture-manifest.v2.json`. The schema remains draft
pending bounded review. The test oracle lives under `tests/contract/`, requires
development `jsonschema` for structural/meta-validation, and is not runtime code.
Test-only field names, flags and template choices are not curated product approval.
Post-resolution Spine byte bounds still require the later installer-artifact
vectors; a portable-manifest check alone cannot prove those bounds.

Before implementing new behavior, complete and review the following FR-1 work:

- `contracts/schemas/spine-pack-manifest.v2.schema.json`, a v2 fixture manifest,
  and semantic reference/normalization/digest tests;
- the seven v2 installer-artifact entry schemas, shared v2 types and embedded
  public-value schema closure, plus exact 0.9.1 readback validators;
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

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: a43a79cebf432f805139fee2ed6356357d0ebe2c5668082e31d5926ccbbc23f5

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
not a reopening of completed installer Slices 1–6. The current scope remains
specification and FR-1 contracts/fixtures. The separately approved 14-file bounded audit completed
with one minor clarification, addressed by a local wording patch; see the
[audit disposition](../whetstone_runs/facet-rendering-spec-audit-001/local-assessment.md).
No runtime, curated pack rewrite, deployment,
release or additional external review is authorized here. Source baseline: Spine
`57cda1c2d5589360ee8efe7155fd20b503034c2a`, `0.9.1` / `19`, explicitly approved
as the repaired replacement. The prior audit covers the original proposal,
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
| FR-2: read-only flight plan | Exact 0.9.1 preflight, protected cursor prerequisites, complete public observation view, dependency closure, cascaded drift and typed outputs | Missing/retain/drift/retired and mixed v1/v2 readback tests; all pagination/capacity/staleness failures; no writes even dry-run. No release compatibility claim |
| FR-3: approved initial flight apply | New command-specific serializers/evidence validators; ordered dependencies; durable prepared/accepted checkpoints; no-op and binding guards | Every one of the 11 write kinds, all ID-consuming paths and every durability boundary tested; no item/disclosure/send commands; no speculative IDs or automatic drift updates |
| FR-4: same-execution recovery and verify | Forward expected-state comparison from bounded preimages; prefix/prefix-plus-one recovery; exact request replay; read-only exact-pin verification | Lost responses for schema/rendering create/publish, both binding kinds and nested profile refs; unrelated drift rejected; receipt limitations explicit; every old recovery/verify test preserved |
| FR-5: disposable and installed-package qualification | Exact pinned Spine build, isolated temporary catalogs, synthetic owner and protected test cursor configs via separately authorized setup; source and clean-wheel plan/apply/replay/verify | All v1 supported-baseline regression gates plus exact 0.9.1 public-CLI qualification. No existing ledger, item creation, materialization, sends, disclosure grants or Spine checkout edits |
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

Next: codify the seven v2 installer artifacts, shared/embedded/readback schema
closure, exact typed reference slots, aggregate observation budgets and one
request/plan/approval/checkpoint/apply/verify fixture flow. Complete the remaining
normalization, resolved-byte-limit and recovery evidence oracles, then stage a
bounded machine-contract review. External review still requires exact-payload
approval; FR-2 runtime implementation must wait for that gate.
```

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/docs/facet-rendering-baseline.md

Hash: be2143347ed9869dac04e54cce363929eb819e1ca8d5f7eccd06000a361fa409

```markdown
# Facet/rendering baseline inspection

Inspection date: 2026-10-10. Design authority is
`specs/facet-rendering-packs.md`; this file records evidence, not an alternative
Spine contract. The original inspection and the later narrow qualification below
are distinct; neither is complete installer qualification.

## Current repaired baseline and independent listing gate

The operator explicitly replaced the broken baseline with locally available
commit `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema `19`.
`git cat-file -t` confirmed the exact commit. A fresh `git archive` export was
built into a wheel offline and installed into a new isolated environment; no
checkout files were edited and no fetch, push or release was required.

The diff from the original pin changes pagination/projection wiring and version
declarations, plus upstream tests/docs. The four authoritative documents, public
schemas, contract registries and compiled command registry below are unchanged.
The existing 22-command map and 17-contract union therefore remain the proposed
execution boundary; this does not add 0.9.1 to existing installer allowlists.

Independent gate: **passed**, using `scripts/qualify_profile_v2_listing.py` and
only installed public CLI subprocesses. It allocated a fresh private temporary
ledger and synthetic owner, then checked:

- ordinary v2 create, exact-revision show and list agreement;
- complete mixed v1/v2 pagination at limits 1, 2 and 500, with no missing,
  duplicated or reordered entries and one consistent catalog snapshot;
- a definition-pinned profile retaining its exact rendering root/revision;
- stored v1/v2 decoder identity and the unchanged v1 rejection guard; and
- v2 public response schemas and system-info-v3 with Draft 2020-12 validation.

The 28 public invocations include migration and synthetic owner setup. There
were no SQL reads, internal handler imports, existing ledger access, items,
disclosure authorizations, materialization or notifications. No proof of general
read-only ledger integrity is inferred merely from successful list responses.

Provenance:

- Spine wheel SHA-256:
  `f1783e020ae5de97c0c772b0e1de2c7ed48f5b56f94d2f7398279b7581bf332b`.
- All 299 packaged `spine/` files match both the exact exported source and the
  installed files byte-for-byte. This verifies imported-package provenance,
  rather than relying on the console-script hash or runtime version alone.
- Tickerd 0.2.0 wheel SHA-256:
  `7c23fc1910ec8db1f88cb674f2bec8b7d6055b54cd255d56d50c6972367d2a71`;
  `system.info` validated its required descriptor/compatibility evidence.
- Retained disposable run:
  `/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-profile-v2-gate-nx393onr`.
- `public-cli-transcript.json` SHA-256:
  `ae336a793c48f86fa4495edf0437bd0c01c0fc5d9b445c1996ce502eb16ad171`.
- Isolated source/build/runtime root:
  `/private/tmp/spine-packs-spine091-source.dZGujO`.

Re-run the gate with that isolated installed environment (or independently build
the same exact Git tree into a new one):

```sh
/private/tmp/spine-packs-spine091-source.dZGujO/runtime-env/bin/python -I \
  /Users/Shared/Agent-Workspace/repos/personal/spine-packs/scripts/qualify_profile_v2_listing.py \
  --bin-dir /private/tmp/spine-packs-spine091-source.dZGujO/runtime-env/bin \
  --schemas-dir /private/tmp/spine-packs-spine091-source.dZGujO/contracts/schemas
```

The harness accepts no ledger path. Each invocation allocates and retains a new
private run directory. Source commit provenance must be established by the
build/export check separately; `system.info` does not attest a Git commit.

This is independent evidence for the listing repair only. The upstream report
of 1,023 tests, six CLI regressions and wheel checks is handoff evidence, not
tests rerun by Spine Packs. FR-5 still must qualify the actual successor
installer's plan/apply/recovery/verify and installed package. Neither baseline
nor new pack content is released or deployable through the existing installer.

## Original 0.9.0 inspection provenance and limits

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

## Historical blocker: profile v2 listing at 01ebce7

At the original exact requested pin (not the repaired 57cda1c pin):

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

The original next gate was to separately authorize a minimal public-CLI regression on this exact
pin: create a synthetic v2 ordinary profile, show it with v2, then list its owner
with v2, including mixed v1/v2 and paginated cases. Do not deploy, bypass listing,
read the database, import handlers as an installer shortcut, or claim successful
qualification before that gate. If confirmed, route the defect to Spine's owner;
any repaired baseline must be explicitly approved and separately pinned here.
Do not substitute a newer 0.9.0 build under the original qualification record.

The Spine handoff reports reproducing and repairing that original failure.
Spine Packs has now independently tested only the repaired pin as recorded above.
The original 14-file audit payload, source excerpts, finding and report remain
unchanged in `whetstone_runs/facet-rendering-spec-audit-001/`.

## Unproved until later slices

FR-1 has begun with a draft successor manifest schema, synthetic flight fixture
and positive/negative contract vectors. No installer runtime or curated pack was
changed. Seven v2 installer artifacts, full public request/response schema closure,
aggregate observation budgets, resolution slots and recovery/verification flow
fixtures remain FR-1 work. The original audit passed with one minor clarification
(locally addressed); it does not review these new machine artifacts. A further
bounded review needs separately approved exact payload bytes.

## Spine Packs preservation and manifest checks

After the baseline update and first manifest-only FR-1 increment:

- `python3 scripts/verify_repo.py`: passed, 125 required files.
- Standard contract discovery: 65 passed, five development-schema checks visibly
  skipped because the default Python lacks `jsonschema`.
- Isolated contract discovery with `jsonschema` 4.26.0: all 70 tests passed,
  including v2 Draft 2020-12 meta-validation and 35 indexed manifest vectors.
- Standard runtime discovery: all 126 tests passed.
- Tracked and new-file whitespace checks: passed.
- Existing installer runtime, v1 schemas, all pack artifacts and the original
  bounded audit are unchanged. Unrelated local audit directories were preserved.

The new v2 checks can be rerun with the isolated environment's Python:

```sh
/private/tmp/spine-packs-spine091-source.dZGujO/runtime-env/bin/python \
  -m unittest discover -s tests/contract -p 'test_facet_manifest_contract.py'
```

No external reviewer was invoked and no commit, push, deployment or publication
was performed. These checks do not complete FR-1's installer-artifact work or
FR-5's successor installer package qualification.
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-manifest.v1.schema.json

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

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-manifest.v2.schema.json

Hash: 6fafd08fb03be7d03acfe660fc85c983dfa18228c06ff6d3d122fa2e2f58f609

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-manifest.v2.schema.json",
  "title": "Spine Pack Manifest v2 (draft, FR-1 manifest slice)",
  "type": "object",
  "required": [
    "manifest_schema",
    "pack",
    "compatibility",
    "dependencies",
    "archetypes",
    "notification_profiles",
    "binding_intents",
    "content_identity",
    "facet_schemas",
    "archetype_facet_bindings",
    "rendering_definitions"
  ],
  "properties": {
    "manifest_schema": {
      "const": "spine.pack-manifest.v2"
    },
    "pack": {
      "$ref": "#/$defs/pack"
    },
    "compatibility": {
      "$ref": "#/$defs/compatibility"
    },
    "dependencies": {
      "type": "array",
      "maxItems": 0
    },
    "archetypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/archetype"
      }
    },
    "notification_profiles": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/notificationProfile"
      }
    },
    "binding_intents": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/bindingIntent"
      }
    },
    "content_identity": {
      "$ref": "#/$defs/contentIdentity"
    },
    "facet_schemas": {
      "type": "array",
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/facetSchema"
      }
    },
    "archetype_facet_bindings": {
      "type": "array",
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/facetBinding"
      }
    },
    "rendering_definitions": {
      "type": "array",
      "maxItems": 256,
      "items": {
        "$ref": "#/$defs/renderingDefinition"
      }
    }
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
          "required": [
            "pack_id",
            "version",
            "status"
          ],
          "properties": {
            "pack_id": {
              "$ref": "#/$defs/packId"
            },
            "version": {
              "$ref": "#/$defs/draftVersion"
            },
            "status": {
              "const": "draft"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "pack_id",
            "version",
            "status"
          ],
          "properties": {
            "pack_id": {
              "$ref": "#/$defs/packId"
            },
            "version": {
              "$ref": "#/$defs/stableVersion"
            },
            "status": {
              "const": "released"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "compatibility": {
      "type": "object",
      "required": [
        "spine_runtime_versions",
        "spine_content_contracts"
      ],
      "properties": {
        "spine_runtime_versions": {
          "const": [
            "0.9.1"
          ]
        },
        "spine_content_contracts": {
          "const": [
            "spine.archetype-facet-bindings.v1",
            "spine.facet-schemas.v1",
            "spine.item-archetypes.v1",
            "spine.notification-profile-bindings.v1",
            "spine.notification-profiles.v2",
            "spine.notification-rendering-definitions.v1",
            "spine.notification-rendering.v1"
          ]
        }
      },
      "additionalProperties": false
    },
    "itemTypes": {
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
    "archetypeRevision": {
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
          "$ref": "#/$defs/description"
        },
        "compatible_item_types": {
          "$ref": "#/$defs/itemTypes"
        }
      },
      "additionalProperties": false
    },
    "archetype": {
      "type": "object",
      "required": [
        "archetype_key",
        "intended_status",
        "revision"
      ],
      "properties": {
        "archetype_key": {
          "$ref": "#/$defs/key"
        },
        "intended_status": {
          "const": "active"
        },
        "revision": {
          "$ref": "#/$defs/archetypeRevision"
        }
      },
      "additionalProperties": false
    },
    "elapsedAtOrBeforeSchedule": {
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
      "required": [
        "kind",
        "at"
      ],
      "properties": {
        "kind": {
          "const": "once"
        },
        "at": {
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
      "required": [
        "kind",
        "grace_seconds"
      ],
      "properties": {
        "kind": {
          "const": "deliver_within"
        },
        "grace_seconds": {
          "type": "string",
          "pattern": "^[1-9][0-9]*$"
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling",
        "rendering"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "oneOf": [
            {
              "$ref": "#/$defs/elapsedAtOrBeforeSchedule"
            },
            {
              "$ref": "#/$defs/calendarDaySchedule"
            }
          ]
        },
        "late_handling": {
          "$ref": "#/$defs/lateHandling"
        },
        "rendering": {
          "$ref": "#/$defs/templateRendering"
        }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/itemTypes"
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
        "profile_key": {
          "$ref": "#/$defs/key"
        },
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "$ref": "#/$defs/description"
        },
        "intended_status": {
          "const": "active"
        },
        "revision": {
          "$ref": "#/$defs/profileRevision"
        }
      },
      "additionalProperties": false
    },
    "bindingIntent": {
      "type": "object",
      "required": [
        "binding_kind",
        "archetype_key",
        "notification_profile_key"
      ],
      "properties": {
        "binding_kind": {
          "const": "archetype_default"
        },
        "archetype_key": {
          "$ref": "#/$defs/key"
        },
        "notification_profile_key": {
          "$ref": "#/$defs/key"
        }
      },
      "additionalProperties": false
    },
    "contentIdentity": {
      "type": "object",
      "required": [
        "algorithm",
        "canonical_json_version",
        "digest"
      ],
      "properties": {
        "algorithm": {
          "const": "sha256"
        },
        "canonical_json_version": {
          "const": "spine.canonical-json.v1"
        },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    },
    "facetKey": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]{0,63}(?![\\s\\S])"
    },
    "facetInteger": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)(?![\\s\\S])",
      "maxLength": 20,
      "$comment": "Semantic validation enforces signed 64-bit range."
    },
    "facetField": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "max_length",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "text"
            },
            "queryable": {
              "type": "boolean"
            },
            "max_length": {
              "type": "string",
              "pattern": "^([1-9]|[1-9][0-9]{1,2}|10[01][0-9]|102[0-4])(?![\\s\\S])"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "choices",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "enum"
            },
            "queryable": {
              "type": "boolean"
            },
            "choices": {
              "type": "array",
              "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "minItems": 1,
              "maxItems": 64,
              "uniqueItems": true
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "boolean"
            },
            "queryable": {
              "type": "boolean"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "min",
            "max",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "integer"
            },
            "queryable": {
              "type": "boolean"
            },
            "min": {
              "$ref": "#/$defs/facetInteger"
            },
            "max": {
              "$ref": "#/$defs/facetInteger"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "date"
            },
            "queryable": {
              "type": "boolean"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "target_kind",
            "queryable"
          ],
          "properties": {
            "key": {
              "$ref": "#/$defs/facetKey"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "reference"
            },
            "queryable": {
              "type": "boolean"
            },
            "target_kind": {
              "enum": [
                "subject",
                "location"
              ]
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "facetDefinition": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "fields"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "anyOf": [
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
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/facetField"
          },
          "minItems": 1,
          "maxItems": 32
        }
      },
      "additionalProperties": false
    },
    "schemaRef": {
      "type": "object",
      "required": [
        "schema_key"
      ],
      "properties": {
        "schema_key": {
          "$ref": "#/$defs/facetKey"
        }
      },
      "additionalProperties": false
    },
    "facetSchema": {
      "type": "object",
      "required": [
        "schema_key",
        "intended_status",
        "definition"
      ],
      "properties": {
        "schema_key": {
          "$ref": "#/$defs/facetKey"
        },
        "intended_status": {
          "const": "active"
        },
        "definition": {
          "$ref": "#/$defs/facetDefinition"
        }
      },
      "additionalProperties": false
    },
    "facetBinding": {
      "type": "object",
      "required": [
        "archetype_key",
        "facet_key",
        "schema_ref"
      ],
      "properties": {
        "archetype_key": {
          "$ref": "#/$defs/key"
        },
        "facet_key": {
          "$ref": "#/$defs/facetKey"
        },
        "schema_ref": {
          "$ref": "#/$defs/schemaRef"
        }
      },
      "additionalProperties": false
    },
    "renderingSelection": {
      "type": "object",
      "required": [
        "selection_key",
        "facet_key",
        "schema_ref",
        "field_key",
        "label",
        "projection"
      ],
      "properties": {
        "selection_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "facet_key": {
          "$ref": "#/$defs/facetKey"
        },
        "field_key": {
          "$ref": "#/$defs/facetKey"
        },
        "label": {
          "type": "string",
          "minLength": 1,
          "maxLength": 40
        },
        "projection": {
          "enum": [
            "value",
            "location_label"
          ]
        },
        "schema_ref": {
          "$ref": "#/$defs/schemaRef"
        }
      },
      "additionalProperties": false
    },
    "renderingRevision": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "base_rendering_contract",
        "base_rendering_profile",
        "selections"
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
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "base_rendering_contract": {
          "const": "spine.notification-rendering.v1"
        },
        "base_rendering_profile": {
          "const": "spine.notification-rendering.concise-en-ca.v1"
        },
        "selections": {
          "type": "array",
          "minItems": 1,
          "maxItems": 8,
          "items": {
            "$ref": "#/$defs/renderingSelection"
          }
        }
      },
      "additionalProperties": false
    },
    "renderingDefinition": {
      "type": "object",
      "required": [
        "definition_key",
        "intended_status",
        "revision"
      ],
      "properties": {
        "definition_key": {
          "$ref": "#/$defs/key"
        },
        "intended_status": {
          "const": "active"
        },
        "revision": {
          "$ref": "#/$defs/renderingRevision"
        }
      },
      "additionalProperties": false
    },
    "templateRendering": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "kind"
          ],
          "properties": {
            "kind": {
              "const": "ordinary"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "kind",
            "definition_ref"
          ],
          "properties": {
            "kind": {
              "const": "definition"
            },
            "definition_ref": {
              "type": "object",
              "required": [
                "definition_key"
              ],
              "properties": {
                "definition_key": {
                  "$ref": "#/$defs/key"
                }
              },
              "additionalProperties": false
            }
          },
          "additionalProperties": false
        }
      ]
    }
  },
  "$comment": "Draft manifest-only codification of specs/facet-rendering-packs.md. Exact Spine 57cda1c2d5589360ee8efe7155fd20b503034c2a, runtime 0.9.1/schema 19. Not installer runtime support. Facet definition/key/integer/field fragments derive from archetype-facet-types.schema.json; rendering revision/selection fragments from notification-rendering-definition-types.schema.json, with portable references substituted. Normalization, graph, ordering and digest rules require semantic validation."
}
```

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/pack-fixture-manifest.v2.json

Hash: b2829a2379d10c2a935fc476f570456673dea018332ef87a5f6f94d6dfcb40a6

```markdown
{
  "fixture_manifest": "spine.pack-fixture-manifest.v2",
  "status": "draft_manifest_only",
  "schema": "contracts/schemas/spine-pack-manifest.v2.schema.json",
  "base_fixture": "tests/fixtures/pack-manifest-v2/flight.json",
  "source_commit": "57cda1c2d5589360ee8efe7155fd20b503034c2a",
  "oracle": "tests/contract/test_facet_manifest_contract.py",
  "mutation_semantics": "Apply ordered set/remove edits at typed path segments to a fresh base fixture, then reseal only when reseal=true. valid=true requires schema, graph, normalization, ordering and digest acceptance; valid=false requires validation rejection. These are test vectors, not installable manifests.",
  "vectors": [
    {
      "id": "wrong_runtime",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "compatibility",
            "spine_runtime_versions"
          ],
          "value": [
            "0.9.0"
          ]
        }
      ]
    },
    {
      "id": "future_runtime",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "compatibility",
            "spine_runtime_versions"
          ],
          "value": [
            "0.9.2"
          ]
        }
      ]
    },
    {
      "id": "embedded_owner",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "owner"
          ],
          "value": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic"
          }
        }
      ]
    },
    {
      "id": "schema_ref_contains_ledger_id",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "archetype_facet_bindings",
            0,
            "schema_ref"
          ],
          "value": {
            "facet_schema_revision_id": "synthetic"
          }
        }
      ]
    },
    {
      "id": "missing_schema_reference",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "archetype_facet_bindings",
            0,
            "schema_ref",
            "schema_key"
          ],
          "value": "missing"
        }
      ]
    },
    {
      "id": "missing_rendering_reference",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates",
            1,
            "rendering",
            "definition_ref",
            "definition_key"
          ],
          "value": "missing"
        }
      ]
    },
    {
      "id": "wire_definition_not_portable",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates",
            1,
            "rendering"
          ],
          "value": {
            "kind": "definition",
            "definition": {
              "notification_rendering_definition_id": "synthetic",
              "notification_rendering_definition_revision_id": "synthetic"
            }
          }
        }
      ]
    },
    {
      "id": "disclosure_in_template",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates",
            1,
            "rendering",
            "disclosure_authorization_id"
          ],
          "value": "synthetic"
        }
      ]
    },
    {
      "id": "missing_queryable",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "remove",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0,
            "queryable"
          ]
        }
      ]
    },
    {
      "id": "noncanonical_fields",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields"
          ],
          "value": [
            {
              "key": "origin",
              "type": "reference",
              "target_kind": "location",
              "required": false,
              "queryable": false
            },
            {
              "key": "flight_number",
              "type": "text",
              "max_length": "32",
              "required": false,
              "queryable": false
            }
          ]
        }
      ]
    },
    {
      "id": "noncanonical_templates",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates"
          ],
          "value": [
            {
              "template_key": "twenty_four_hours_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-86400"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "21600"
              },
              "rendering": {
                "kind": "ordinary"
              }
            },
            {
              "template_key": "seven_days_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-604800"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "86400"
              },
              "rendering": {
                "kind": "ordinary"
              }
            },
            {
              "template_key": "one_hour_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-3600"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "900"
              },
              "rendering": {
                "kind": "definition",
                "definition_ref": {
                  "definition_key": "flight_details"
                }
              }
            },
            {
              "template_key": "four_hours_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-14400"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "3600"
              },
              "rendering": {
                "kind": "ordinary"
              }
            }
          ]
        }
      ]
    },
    {
      "id": "incorrect_digest",
      "valid": false,
      "reseal": false,
      "edits": [
        {
          "op": "set",
          "path": [
            "content_identity",
            "digest"
          ],
          "value": "0000000000000000000000000000000000000000000000000000000000000000"
        }
      ]
    },
    {
      "id": "draft_status_mismatch",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "pack",
            "status"
          ],
          "value": "released"
        }
      ]
    },
    {
      "id": "duplicate_defaults",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "binding_intents"
          ],
          "value": [
            {
              "binding_kind": "archetype_default",
              "archetype_key": "flight",
              "notification_profile_key": "synthetic_flight_details"
            },
            {
              "binding_kind": "archetype_default",
              "archetype_key": "flight",
              "notification_profile_key": "synthetic_flight_details"
            }
          ]
        }
      ]
    },
    {
      "id": "duplicate_facet_bindings",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "archetype_facet_bindings"
          ],
          "value": [
            {
              "archetype_key": "flight",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              }
            },
            {
              "archetype_key": "flight",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              }
            }
          ]
        }
      ]
    },
    {
      "id": "missing_facet_binding",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "archetype_facet_bindings"
          ],
          "value": []
        }
      ]
    },
    {
      "id": "unknown_selected_field",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "rendering_definitions",
            0,
            "revision",
            "selections",
            0,
            "field_key"
          ],
          "value": "missing"
        }
      ]
    },
    {
      "id": "wrong_projection",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "rendering_definitions",
            0,
            "revision",
            "selections",
            1,
            "projection"
          ],
          "value": "value"
        }
      ]
    },
    {
      "id": "subject_reference_selected",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            1,
            "target_kind"
          ],
          "value": "subject"
        }
      ]
    },
    {
      "id": "duplicate_selection",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "rendering_definitions",
            0,
            "revision",
            "selections"
          ],
          "value": [
            {
              "selection_key": "number",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "flight_number",
              "label": "Flight",
              "projection": "value"
            },
            {
              "selection_key": "origin",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "origin",
              "label": "From",
              "projection": "location_label"
            },
            {
              "selection_key": "number",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "flight_number",
              "label": "Flight",
              "projection": "value"
            },
            {
              "selection_key": "origin",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "origin",
              "label": "From",
              "projection": "location_label"
            }
          ]
        }
      ]
    },
    {
      "id": "non_nfc_schema",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "display_name"
          ],
          "value": "Cafe\u0301"
        }
      ]
    },
    {
      "id": "non_normalized_label",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "rendering_definitions",
            0,
            "revision",
            "selections",
            0,
            "label"
          ],
          "value": " Flight  number "
        }
      ]
    },
    {
      "id": "incompatible_schema",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "compatible_item_types"
          ],
          "value": [
            "task"
          ]
        }
      ]
    },
    {
      "id": "wrong_kind_reference",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates",
            1,
            "rendering",
            "definition_ref"
          ],
          "value": {
            "schema_key": "flight_details"
          }
        }
      ]
    },
    {
      "id": "cross_pack_reference",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates",
            1,
            "rendering",
            "definition_ref",
            "pack_id"
          ],
          "value": "elsewhere"
        }
      ]
    },
    {
      "id": "json_number",
      "valid": false,
      "reseal": false,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0,
            "max_length"
          ],
          "value": 32
        }
      ]
    },
    {
      "id": "out_of_range_integer",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "integer",
            "required": false,
            "queryable": false,
            "min": "0",
            "max": "9223372036854775808"
          }
        }
      ]
    },
    {
      "id": "inverted_integer_bounds",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "integer",
            "required": false,
            "queryable": false,
            "min": "2",
            "max": "1"
          }
        }
      ]
    },
    {
      "id": "unsorted_enum",
      "valid": false,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "enum",
            "required": false,
            "queryable": false,
            "choices": [
              "B",
              "A"
            ]
          }
        }
      ]
    },
    {
      "id": "scalar_boolean",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "boolean",
            "required": false,
            "queryable": false
          }
        }
      ]
    },
    {
      "id": "scalar_date",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "date",
            "required": false,
            "queryable": false
          }
        }
      ]
    },
    {
      "id": "scalar_integer",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "integer",
            "required": false,
            "queryable": false,
            "min": "-2",
            "max": "2"
          }
        }
      ]
    },
    {
      "id": "scalar_enum",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "facet_schemas",
            0,
            "definition",
            "fields",
            0
          ],
          "value": {
            "key": "flight_number",
            "type": "enum",
            "required": false,
            "queryable": false,
            "choices": [
              "A",
              "B"
            ]
          }
        }
      ]
    },
    {
      "id": "ordinary_only_templates",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "notification_profiles",
            0,
            "revision",
            "templates"
          ],
          "value": [
            {
              "template_key": "four_hours_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-14400"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "3600"
              },
              "rendering": {
                "kind": "ordinary"
              }
            },
            {
              "template_key": "one_hour_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-3600"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "900"
              },
              "rendering": {
                "kind": "ordinary"
              }
            },
            {
              "template_key": "seven_days_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-604800"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "86400"
              },
              "rendering": {
                "kind": "ordinary"
              }
            },
            {
              "template_key": "twenty_four_hours_before",
              "schedule": {
                "kind": "once",
                "at": {
                  "kind": "target_offset",
                  "offset_basis": "elapsed",
                  "offset_seconds": "-86400"
                }
              },
              "late_handling": {
                "kind": "deliver_within",
                "grace_seconds": "21600"
              },
              "rendering": {
                "kind": "ordinary"
              }
            }
          ]
        }
      ]
    },
    {
      "id": "presentation_order_retained",
      "valid": true,
      "reseal": true,
      "edits": [
        {
          "op": "set",
          "path": [
            "rendering_definitions",
            0,
            "revision",
            "selections"
          ],
          "value": [
            {
              "selection_key": "origin",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "origin",
              "label": "From",
              "projection": "location_label"
            },
            {
              "selection_key": "number",
              "facet_key": "flight",
              "schema_ref": {
                "schema_key": "flight_details"
              },
              "field_key": "flight_number",
              "label": "Flight",
              "projection": "value"
            }
          ]
        }
      ]
    }
  ]
}
```

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest-v2/flight.json

Hash: ab58374779ea3c960aef2386ea522cd230b6d8a91df6d01c9730a84a807b7019

```markdown
{
  "manifest_schema": "spine.pack-manifest.v2",
  "pack": {
    "pack_id": "synthetic-flight-proof",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.9.1"
    ],
    "spine_content_contracts": [
      "spine.archetype-facet-bindings.v1",
      "spine.facet-schemas.v1",
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v2",
      "spine.notification-rendering-definitions.v1",
      "spine.notification-rendering.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "flight",
      "intended_status": "active",
      "revision": {
        "display_name": "Flight",
        "description": "Scheduled flight departures.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "synthetic_flight_details",
      "display_name": "Synthetic flight details",
      "description": "Contract fixture only; not approved curated content.",
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
          {
            "template_key": "four_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-14400"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            },
            "rendering": {
              "kind": "ordinary"
            }
          },
          {
            "template_key": "one_hour_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-3600"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
            },
            "rendering": {
              "kind": "definition",
              "definition_ref": {
                "definition_key": "flight_details"
              }
            }
          },
          {
            "template_key": "seven_days_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-604800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "86400"
            },
            "rendering": {
              "kind": "ordinary"
            }
          },
          {
            "template_key": "twenty_four_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-86400"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "21600"
            },
            "rendering": {
              "kind": "ordinary"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "flight",
      "notification_profile_key": "synthetic_flight_details"
    }
  ],
  "facet_schemas": [
    {
      "schema_key": "flight_details",
      "intended_status": "active",
      "definition": {
        "display_name": "Synthetic flight details",
        "description": null,
        "compatible_item_types": [
          "event"
        ],
        "fields": [
          {
            "key": "flight_number",
            "type": "text",
            "max_length": "32",
            "required": false,
            "queryable": false
          },
          {
            "key": "origin",
            "type": "reference",
            "target_kind": "location",
            "required": false,
            "queryable": false
          }
        ]
      }
    }
  ],
  "archetype_facet_bindings": [
    {
      "archetype_key": "flight",
      "facet_key": "flight",
      "schema_ref": {
        "schema_key": "flight_details"
      }
    }
  ],
  "rendering_definitions": [
    {
      "definition_key": "flight_details",
      "intended_status": "active",
      "revision": {
        "display_name": "Synthetic flight details",
        "description": null,
        "compatible_item_types": [
          "event"
        ],
        "base_rendering_contract": "spine.notification-rendering.v1",
        "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
        "selections": [
          {
            "selection_key": "number",
            "facet_key": "flight",
            "schema_ref": {
              "schema_key": "flight_details"
            },
            "field_key": "flight_number",
            "label": "Flight",
            "projection": "value"
          },
          {
            "selection_key": "origin",
            "facet_key": "flight",
            "schema_ref": {
              "schema_key": "flight_details"
            },
            "field_key": "origin",
            "label": "From",
            "projection": "location_label"
          }
        ]
      }
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "80cb80492a6072d3992d6cf22ff31d49ab103912ce76485ca73361db4469d405"
  }
}
```

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_facet_manifest_contract.py

Hash: 5e58592fa608795e17413c1eff0253ff3c58e1c3b611b89af938130a49ad9370

```markdown
"""FR-1 manifest-only oracle; deliberately not imported by installer runtime.

Structural/meta-validation requires the development dependency jsonschema.
Run this module explicitly in the isolated qualification environment before
claiming the FR-1 manifest gate. Missing jsonschema is a visible skip, not proof.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import unittest

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    Draft202012Validator = None
    ValidationError = ValueError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "contracts/schemas/spine-pack-manifest.v2.schema.json"
FIXTURE = ROOT / "tests/fixtures/pack-manifest-v2/flight.json"
INDEX = ROOT / "contracts/pack-fixture-manifest.v2.json"


def load(path):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError("duplicate JSON member")
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def require(value, reason):
    if not value:
        raise ValueError(reason)


def canonical(value):
    def inspect(v):
        require(type(v) not in (int, float), "JSON numbers forbidden")
        if isinstance(v, str):
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in v), "invalid Unicode")
        elif isinstance(v, dict):
            for k, x in v.items():
                inspect(k)
                inspect(x)
        elif isinstance(v, list):
            for x in v:
                inspect(x)
    inspect(value)
    # JSON's short control escapes are not Spine canonical-json.v1 escapes.
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    text = re.sub(r'\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})',
                  lambda m: {r'\b': r'\u0008', r'\f': r'\u000c', r'\n': r'\u000a',
                             r'\r': r'\u000d', r'\t': r'\u0009'}.get(m[0], m[0]), text)
    return text.encode("utf-8")


def digest(manifest):
    return hashlib.sha256(canonical({
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine-pack-content-sha256.v2",
        "manifest": {k: v for k, v in manifest.items() if k != "content_identity"},
    })).hexdigest()


def ordered(values):
    require(values == sorted(set(values)), "duplicate or noncanonical ordering")


def validate(manifest):
    require(len(canonical(manifest)) <= 16 * 1024 * 1024, "manifest byte limit")
    Draft202012Validator(load(SCHEMA)).validate(manifest)
    def catalog_keys(value):
        if isinstance(value, dict):
            for name, member in value.items():
                if name == "key" or name.endswith("_key"):
                    require(re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", member), "noncanonical catalog key")
                catalog_keys(member)
        elif isinstance(value, list):
            for member in value:
                catalog_keys(member)
    catalog_keys(manifest)
    families = {}
    for array, key in (("archetypes", "archetype_key"), ("notification_profiles", "profile_key"),
                       ("facet_schemas", "schema_key"), ("rendering_definitions", "definition_key")):
        ordered([x[key] for x in manifest[array]])
        families[array] = {x[key]: x for x in manifest[array]}
    archetypes, profiles, schemas, renderings = (families[k] for k in (
        "archetypes", "notification_profiles", "facet_schemas", "rendering_definitions"))

    def target(mapping, key):
        require(key in mapping, "missing or wrong-kind local reference")
        return mapping[key]

    def types(revision):
        ordered(revision["compatible_item_types"])
        return set(revision["compatible_item_types"])

    for a in archetypes.values():
        types(a["revision"])
    for s in schemas.values():
        definition = s["definition"]
        types(definition)
        require(len(canonical(definition)) <= 32768, "facet definition byte limit")
        def nfc(v):
            if isinstance(v, str):
                require(v == unicodedata.normalize("NFC", v), "facet NFC")
            elif isinstance(v, list):
                for x in v:
                    nfc(x)
            elif isinstance(v, dict):
                for x in v.values():
                    nfc(x)
        nfc(definition)
        ordered([f["key"] for f in definition["fields"]])
        for f in definition["fields"]:
            if f["type"] == "enum":
                ordered(f["choices"])
            if f["type"] == "integer":
                require(-(2**63) <= int(f["min"]) <= int(f["max"]) < 2**63, "integer range")
    bindings = {}
    ordered([(b["archetype_key"], b["facet_key"]) for b in manifest["archetype_facet_bindings"]])
    for b in manifest["archetype_facet_bindings"]:
        a = target(archetypes, b["archetype_key"])
        s = target(schemas, b["schema_ref"]["schema_key"])
        require(types(a["revision"]) & types(s["definition"]), "incompatible facet binding")
        bindings[(b["archetype_key"], b["facet_key"])] = b["schema_ref"]["schema_key"]
    for r in renderings.values():
        revision = r["revision"]
        used, names = set(), set()
        for text in [revision["display_name"], revision["description"], *[x["label"] for x in revision["selections"]]]:
            if text is not None:
                require(text == " ".join(text.split()) and text, "rendering text normalization")
                require(not any(unicodedata.category(c).startswith("C") for c in text), "rendering control character")
        for selection in revision["selections"]:
            sk = selection["schema_ref"]["schema_key"]
            schema = target(schemas, sk)["definition"]
            require(types(revision) <= types(schema), "rendering/schema type coverage")
            field = target({f["key"]: f for f in schema["fields"]}, selection["field_key"])
            projection = "location_label" if field["type"] == "reference" and field["target_kind"] == "location" else "value"
            require(field["type"] != "reference" or projection == "location_label", "subject disclosure forbidden")
            require(selection["projection"] == projection, "projection type mismatch")
            source = (selection["facet_key"], sk, selection["field_key"])
            require(source not in used and selection["selection_key"] not in names, "duplicate selection")
            used.add(source)
            names.add(selection["selection_key"])
    for p in profiles.values():
        revision = p["revision"]
        types(revision)
        ordered([t["template_key"] for t in revision["templates"]])
        schedules = [canonical(t["schedule"]) for t in revision["templates"]]
        require(len(schedules) == len(set(schedules)), "duplicate timing templates")
        for t in revision["templates"]:
            at = t["schedule"]["at"]
            if at["offset_basis"] == "calendar_days":
                require(-3660 <= int(at["offset_days"]) <= 0, "calendar offset range")
            rendering = t["rendering"]
            if rendering["kind"] == "definition":
                r = target(renderings, rendering["definition_ref"]["definition_key"])
                require(types(revision) <= types(r["revision"]), "profile/rendering type coverage")
    ordered([b["archetype_key"] for b in manifest["binding_intents"]])
    for b in manifest["binding_intents"]:
        a = target(archetypes, b["archetype_key"])
        p = target(profiles, b["notification_profile_key"])
        require(types(a["revision"]) & types(p["revision"]), "incompatible default")
        for t in p["revision"]["templates"]:
            rendering = t["rendering"]
            if rendering["kind"] == "definition":
                r = renderings[rendering["definition_ref"]["definition_key"]]
                for s in r["revision"]["selections"]:
                    require(bindings.get((b["archetype_key"], s["facet_key"])) == s["schema_ref"]["schema_key"],
                            "missing matching archetype facet binding")
    require(manifest["content_identity"]["digest"] == digest(manifest), "content digest mismatch")


@unittest.skipIf(Draft202012Validator is None, "FR-1 requires development jsonschema; run isolated schema gate")
class FacetManifestTests(unittest.TestCase):
    def test_schema_and_fixture(self):
        Draft202012Validator.check_schema(load(SCHEMA))
        validate(load(FIXTURE))

    def test_indexed_vectors(self):
        for vector in load(INDEX)["vectors"]:
            with self.subTest(vector=vector["id"]):
                manifest = load(FIXTURE)
                for edit in vector["edits"]:
                    container = manifest
                    for part in edit["path"][:-1]:
                        container = container[part]
                    final = edit["path"][-1]
                    if edit["op"] == "remove":
                        del container[final]
                    else:
                        container[final] = deepcopy(edit["value"])
                if vector["reseal"]:
                    manifest["content_identity"]["digest"] = digest(manifest)
                if vector["valid"]:
                    validate(manifest)
                else:
                    with self.assertRaises((ValueError, ValidationError)):
                        validate(manifest)

    def test_presentation_order_is_not_sorted_away(self):
        manifest = load(FIXTURE)
        before = digest(manifest)
        manifest["rendering_definitions"][0]["revision"]["selections"].reverse()
        manifest["content_identity"]["digest"] = digest(manifest)
        self.assertNotEqual(before, digest(manifest))
        validate(manifest)

    def test_v1_rejects_v2_and_released_content_is_not_changed(self):
        v1 = load(ROOT / "contracts/schemas/spine-pack-manifest.v1.schema.json")
        self.assertFalse(Draft202012Validator(v1).is_valid(load(FIXTURE)))
        stable = load(ROOT / "packs/kinflow-starter/kinflow-starter.1.0.1.json")
        flight = next(p for p in stable["notification_profiles"] if p["profile_key"] == "flight_standard")
        desired = load(FIXTURE)["notification_profiles"][0]
        without_rendering = [{k: v for k, v in t.items() if k != "rendering"} for t in desired["revision"]["templates"]]
        self.assertEqual(flight["revision"]["templates"], without_rendering)

    def test_canonical_controls_and_numbers(self):
        self.assertEqual(canonical("\n"), b'"\\u000a"')
        self.assertEqual(canonical("\\n"), b'"\\\\n"')
        with self.assertRaises(ValueError):
            canonical({"n": 1})


if __name__ == "__main__":
    unittest.main()
```

### Spec 14: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/scripts/qualify_profile_v2_listing.py

Hash: 5cc37a27add60a01b0745dc915f7089e8a20e99571fd9e822d64aea55c53342e

```markdown
"""Bounded public-CLI listing gate; always allocates a new disposable ledger.

This is test tooling, not installer behavior or full installer qualification.
Run with an isolated installed Spine 0.9.1 bin directory. Retains the private
temporary run directory and transcripts on success or failure. No ledger input,
Spine imports, SQL, item authoring, disclosure, or delivery commands are allowed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

V1 = "spine.notification-profiles.v1"
V2 = "spine.notification-profiles.v2"
NOW = "2035-02-01T12:00:00Z"
OWNER = {"owner_kind": "subject", "owner_subject_id": "listing_gate_owner"}
COMMANDS = frozenset({
    "system.info", "subject.upsert", "notification_profile.create",
    "notification_profile.show", "notification_profile.list",
    "facet_schema.create", "notification_rendering_definition.create",
})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def qualify(bin_dir: Path, schemas_dir: Path):
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource

    schemas = [json.loads(p.read_text()) for p in schemas_dir.glob("*.schema.json")]
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas)
    run = Path(tempfile.mkdtemp(prefix="spine-packs-profile-v2-gate-"))
    ledger = run / "new.sqlite"
    command = bin_dir / "spine-command"
    migrate = bin_dir / "spine-ledger-migrate"
    # Deliberately do not inherit PYTHONPATH or operator Spine configuration.
    env = {"PATH": str(bin_dir) + ":/usr/bin:/bin", "PYTHONNOUSERSITE": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"}
    transcript, checks = [], []

    def invoke(argv, request=None, expected=0):
        require(len(transcript) < 100, "command budget exhausted")
        result = subprocess.run(argv, input=json.dumps(request) if request is not None else None,
                                text=True, capture_output=True, cwd=run, env=env, timeout=30)
        require(len(result.stdout.encode()) <= 4 * 1024 * 1024, "response too large")
        response = json.loads(result.stdout)
        transcript.append({"argv": argv, "request": request, "exit_code": result.returncode,
                           "response": response})
        require(result.returncode == expected, f"unexpected exit for {argv[-2:]}: {response}")
        return response

    def cli(name, request, expected=0):
        require(name in COMMANDS, "command outside qualification allowlist")
        response = invoke([str(command), "--db", str(ledger), "--input", "-", *name.split(".")], request, expected)
        require(response["ok"] == (expected == 0), "inconsistent success envelope")
        if expected == 0:
            require(response["command"] == name, "wrong response command")
            if name.startswith("notification_profile."):
                require(response["response_contract"] == request["contract_version"], "wrong profile decoder")
                if request["contract_version"] == V2:
                    uri = "https://cortext.local/spine/contracts/schemas/notification-profile-responses-v2.schema.json"
                    Draft202012Validator({"$ref": uri + "#/$defs/" + name.rsplit(".", 1)[1]},
                                         registry=registry, format_checker=FormatChecker()).validate(response)
        return response

    def write(name, contract, **fields):
        return cli(name, {"contract_version": contract, "command_id": f"listing-gate-{len(transcript)}",
                          "actor_subject_id": OWNER["owner_subject_id"], "action_timestamp_utc": NOW, **fields})

    def create(key, version=V2, rendering=None):
        template = {"template_key": "one_hour_before",
                    "schedule": {"kind": "once", "at": {"kind": "target_offset", "offset_basis": "elapsed", "offset_seconds": "-3600"}},
                    "late_handling": {"kind": "deliver_within", "grace_seconds": "900"}}
        if version == V2:
            template["rendering"] = rendering or {"kind": "ordinary"}
        return write("notification_profile.create", version, owner=OWNER, profile_key=key,
                     display_name=key, description=None,
                     revision={"compatible_item_types": ["event"], "templates": [template]})

    def show(created):
        return cli("notification_profile.show", {"contract_version": V2,
                   "notification_profile_id": created["notification_profile_id"],
                   "notification_profile_revision_id": created["notification_profile_revision_id"]})["notification_profile"]

    def listing(limit="500", cursor=None, version=V2, expected=0):
        request = {"contract_version": version, "owner": OWNER, "status": "active", "limit": limit}
        if cursor is not None:
            request["cursor"] = cursor
        return cli("notification_profile.list", request, expected)

    try:
        require(not ledger.exists(), "refusing existing ledger")
        invoke([str(migrate), "--db", str(ledger), "--initialize-if-empty"])
        info = cli("system.info", {})
        require(info["runtime_version"] == "0.9.1", "wrong runtime")
        require(str(info["ledger_schema_version"]) == "19", "wrong current schema")
        require(info["implemented_ledger_schema_version"] == "19", "wrong implemented schema")
        Draft202012Validator(json.loads((schemas_dir / "system-info-response-v3.schema.json").read_text()),
                             registry=registry).validate(info)
        cli("subject.upsert", {"command_id": "listing-gate-owner", "actor_subject_id": OWNER["owner_subject_id"],
            "subject_id": OWNER["owner_subject_id"], "subject_kind": "person", "display_name": "Synthetic listing gate owner",
            "updated_at_utc": NOW})
        require(listing()["entries"] == [], "new owner catalog is not empty")
        ordinary = create("b_ordinary")
        ordinary_show = show(ordinary)
        require(listing()["entries"] == [ordinary_show], "ordinary create/show/list mismatch")
        checks.append("ordinary_v2_create_show_list")
        profiles = [create("a_legacy", V1), ordinary, create("c_legacy", V1), create("d_ordinary")]
        schema = write("facet_schema.create", "spine.facet-schemas.v1", owner=OWNER, schema_key="gate_flight",
            definition={"display_name": "Synthetic flight", "description": None, "compatible_item_types": ["event"],
                        "fields": [{"key": "flight_number", "type": "text", "max_length": "32", "required": False, "queryable": False}]})
        definition = write("notification_rendering_definition.create", "spine.notification-rendering-definitions.v1",
            owner=OWNER, definition_key="gate_flight", revision={"display_name": "Synthetic details", "description": None,
                "compatible_item_types": ["event"], "base_rendering_contract": "spine.notification-rendering.v1",
                "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
                "selections": [{"selection_key": "flight", "facet_key": "flight", "facet_schema_revision_id": schema["facet_schema_revision_id"],
                                "field_key": "flight_number", "label": "Flight", "projection": "value"}]})["record"]
        rendering = {"kind": "definition", "definition": {
            "notification_rendering_definition_id": definition["notification_rendering_definition_id"],
            "notification_rendering_definition_revision_id": definition["current_revision_id"]}}
        profiles.append(create("e_pinned", rendering=rendering))
        expected = [show(p) for p in profiles]
        require(expected[-1]["revision"]["content"]["templates"][0]["rendering"] == rendering, "lost definition pin")
        snapshots = set()
        for limit in ("1", "2", "500"):
            entries, seen, cursor = [], set(), None
            for _ in range(len(profiles) + 1):
                page = listing(limit, cursor)
                require(page["count"] == str(len(page["entries"])), "wrong count")
                require(len(page["entries"]) <= int(limit), "page exceeds requested limit")
                entries.extend(page["entries"])
                snapshots.add(page["catalog_snapshot_hash"])
                if not page["has_more"]:
                    require(page["next_cursor"] is None, "terminal cursor not null")
                    break
                cursor = page["next_cursor"]
                require(isinstance(cursor, str) and cursor and cursor not in seen, "repeated or missing cursor")
                seen.add(cursor)
            else:
                raise RuntimeError("pagination did not terminate")
            require(entries == expected, "pagination lost, duplicated, reordered or changed profiles")
            checks.append(f"mixed_v1_v2_complete_pagination_limit_{limit}")
        require(len(snapshots) == 1, "snapshot changed between page sizes")
        require([e["revision"]["revision_contract"] for e in expected] == [V1, V2, V1, V2, V2], "historical decoder lost")
        checks.append("definition_pins_and_decoder_identity_preserved")
        guard = listing(version=V1, expected=2)
        require(guard["error"]["code"] == "unsupported_contract_version", "v1 guard changed")
        checks.append("v1_guard_preserved")
        return {"status": "passed", "runtime": "0.9.1", "schema": "19", "checks": checks,
                "command_count": len(transcript), "run_directory": str(run), "installer_qualification": False}
    finally:
        # Generated test evidence only; no database reads, even for diagnostics.
        evidence = json.dumps(transcript, indent=2) + "\n"
        (run / "public-cli-transcript.json").write_text(evidence)
        print(json.dumps({"transcript": str(run / "public-cli-transcript.json"),
                          "sha256": hashlib.sha256(evidence.encode()).hexdigest()}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin-dir", required=True, type=Path)
    parser.add_argument("--schemas-dir", required=True, type=Path,
                        help="Public schemas from the exact repaired Git export")
    args = parser.parse_args()
    print(json.dumps(qualify(args.bin_dir.resolve(), args.schemas_dir.resolve()), sort_keys=True))
```

### Spec 15: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-fr1-manifest-audit-001/spine-manifest-evidence.md

Hash: 42854e01991fe7663084e0e463a8ddb56f3b18b761b598cf99aa7d3b7b7ac3e1

```markdown
# Exact Spine evidence for the FR-1 manifest review

Source pin: `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema `19`.
These are focused schema fragments and normalization-source excerpts, not a
complete executable public schema closure. No Spine code was imported.
The reviewer may inspect this supplied evidence only; no further checkout access
or external browsing is authorized. All full-source hashes use exact Git blob bytes.

## contracts/schemas/archetype-facet-types.schema.json

Full-source SHA-256: `689163800b0aaa07b87a1fc75a7bea7150bd70f1bcf2fbad901466cdf594dcda`.

```json
{
  "$id": "https://cortext.local/spine/contracts/schemas/archetype-facet-types.schema.json",
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]{0,63}(?![\\s\\S])"
    },
    "signedInteger": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)(?![\\s\\S])",
      "maxLength": 20,
      "$comment": "Semantic validation enforces signed 64-bit range."
    },
    "field": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "max_length"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "text"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "max_length": {
              "type": "string",
              "pattern": "^([1-9]|[1-9][0-9]{1,2}|10[01][0-9]|102[0-4])(?![\\s\\S])"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "choices"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "enum"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "choices": {
              "type": "array",
              "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "minItems": 1,
              "maxItems": 64,
              "uniqueItems": true
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "boolean"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "min",
            "max"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "integer"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "min": {
              "$ref": "archetype-facet-types.schema.json#/$defs/signedInteger"
            },
            "max": {
              "$ref": "archetype-facet-types.schema.json#/$defs/signedInteger"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "date"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "target_kind"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "reference"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "target_kind": {
              "enum": [
                "subject",
                "location"
              ]
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "definition": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "fields"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "anyOf": [
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
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "archetype-facet-types.schema.json#/$defs/field"
          },
          "minItems": 1,
          "maxItems": 32
        }
      },
      "additionalProperties": false
    },
    "normalizedDefinition": {
      "allOf": [
        {
          "$ref": "#/$defs/definition"
        },
        {
          "properties": {
            "fields": {
              "items": {
                "required": [
                  "queryable"
                ]
              }
            }
          }
        }
      ]
    }
  }
}
```

## contracts/schemas/notification-rendering-definition-types.schema.json

Full-source SHA-256: `3b6ea94ce86bbb06f45c63516700235edba43cd0800ed4be05261fc774848344`.

```json
{
  "$id": "https://cortext.local/spine/contracts/schemas/notification-rendering-definition-types.schema.json",
  "$defs": {
    "selection": {
      "type": "object",
      "required": [
        "selection_key",
        "facet_key",
        "facet_schema_revision_id",
        "field_key",
        "label",
        "projection"
      ],
      "properties": {
        "selection_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "facet_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "facet_schema_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "field_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "label": {
          "type": "string",
          "minLength": 1,
          "maxLength": 40
        },
        "projection": {
          "enum": [
            "value",
            "location_label"
          ]
        }
      },
      "additionalProperties": false
    },
    "revision": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "base_rendering_contract",
        "base_rendering_profile",
        "selections"
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
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "base_rendering_contract": {
          "const": "spine.notification-rendering.v1"
        },
        "base_rendering_profile": {
          "const": "spine.notification-rendering.concise-en-ca.v1"
        },
        "selections": {
          "type": "array",
          "minItems": 1,
          "maxItems": 8,
          "items": {
            "$ref": "notification-rendering-definition-types.schema.json#/$defs/selection"
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

## contracts/schemas/notification-profile-types-v2.schema.json

Full-source SHA-256: `e1587494d473198b49f16be89e27de12e32df512821d5670f9c8bf48f654f875`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cortext.local/spine/contracts/schemas/notification-profile-types-v2.schema.json",
  "title": "Spine Notification Profile Types v2 (source only)",
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}(?![\\s\\S])"
    },
    "owner": {
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
              "$ref": "notification-types.schema.json#/$defs/id"
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
              "$ref": "notification-types.schema.json#/$defs/id"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "itemTypes": {
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
    "archetypeRevision": {
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
          "$ref": "#/$defs/itemTypes"
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        },
        "rendering": {
          "$ref": "notification-rendering-integration-types.schema.json#/$defs/templateRendering"
        }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/itemTypes"
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
    "archetypeSelection": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "item_archetype_id",
            "revision_resolution",
            "selection_source"
          ],
          "properties": {
            "item_archetype_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "const": "current"
            },
            "selection_source": {
              "enum": [
                "operator_explicit",
                "agent_selected",
                "imported"
              ]
            },
            "source_ref": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "item_archetype_id",
            "revision_resolution",
            "item_archetype_revision_id",
            "selection_source"
          ],
          "properties": {
            "item_archetype_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "const": "exact"
            },
            "item_archetype_revision_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "selection_source": {
              "enum": [
                "operator_explicit",
                "agent_selected",
                "imported"
              ]
            },
            "source_ref": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "replacement": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        }
      },
      "additionalProperties": false
    },
    "customAddition": {
      "type": "object",
      "required": [
        "policy_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "policy_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        }
      },
      "additionalProperties": false
    },
    "overlays": {
      "type": "object",
      "properties": {
        "suppress_template_keys": {
          "type": "array",
          "maxItems": 32,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/key"
          }
        },
        "replacements": {
          "type": "array",
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/replacement"
          }
        },
        "custom_additions": {
          "type": "array",
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/customAddition"
          }
        }
      }
    },
    "createPlan": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "mode",
            "custom_additions"
          ],
          "properties": {
            "mode": {
              "const": "none"
            },
            "custom_additions": {
              "type": "array",
              "minItems": 1,
              "maxItems": 32,
              "items": {
                "$ref": "#/$defs/customAddition"
              }
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "mode",
            "notification_profile_id",
            "revision_resolution"
          ],
          "properties": {
            "mode": {
              "const": "explicit"
            },
            "notification_profile_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "enum": [
                "current",
                "exact"
              ]
            },
            "notification_profile_revision_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "suppress_template_keys": {
              "$ref": "#/$defs/overlays/properties/suppress_template_keys"
            },
            "replacements": {
              "$ref": "#/$defs/overlays/properties/replacements"
            },
            "custom_additions": {
              "$ref": "#/$defs/overlays/properties/custom_additions"
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "allOf": [
            {
              "if": {
                "properties": {
                  "revision_resolution": {
                    "const": "exact"
                  }
                },
                "required": [
                  "revision_resolution"
                ]
              },
              "then": {
                "required": [
                  "notification_profile_revision_id"
                ]
              },
              "else": {
                "not": {
                  "required": [
                    "notification_profile_revision_id"
                  ]
                }
              }
            }
          ],
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "mode",
            "scope_chain",
            "on_no_match"
          ],
          "properties": {
            "mode": {
              "const": "archetype_default"
            },
            "scope_chain": {
              "type": "array",
              "minItems": 1,
              "maxItems": 8,
              "uniqueItems": true,
              "items": {
                "$ref": "#/$defs/owner"
              }
            },
            "on_no_match": {
              "enum": [
                "fail",
                "use_custom_only"
              ]
            },
            "suppress_template_keys": {
              "$ref": "#/$defs/overlays/properties/suppress_template_keys"
            },
            "replacements": {
              "$ref": "#/$defs/overlays/properties/replacements"
            },
            "custom_additions": {
              "$ref": "#/$defs/overlays/properties/custom_additions"
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "normalizedRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "notification-profile-types.schema.json#/$defs/itemTypes"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "type": "object",
            "required": [
              "template_key",
              "schedule",
              "late_handling",
              "rendering",
              "normalized_template_hash"
            ],
            "properties": {
              "template_key": {
                "$ref": "notification-profile-types.schema.json#/$defs/key"
              },
              "schedule": {
                "$ref": "notification-types.schema.json#/$defs/schedule"
              },
              "late_handling": {
                "$ref": "notification-types.schema.json#/$defs/lateHandling"
              },
              "rendering": {
                "$ref": "notification-rendering-integration-types.schema.json#/$defs/templateRendering"
              },
              "normalized_template_hash": {
                "$ref": "notification-types.schema.json#/$defs/sha256"
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

## src/spine/core/facets.py:1–132

Full-source SHA-256: `b89544dc0fb9b508ac5dd616219b1bffd3466e58620c59cdb55ae744fe0ec60f`.

```python
"""Pure, version-pinned facet codecs. No catalog, reference or permission I/O."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import date
from typing import Any, NoReturn

from spine.core.canonical_json import canonical_json_bytes, canonical_json_text
from spine.core.errors import SpineValidationError

DEFINITION_VERSION = "spine.facet-schemas.v1"
VALUE_VERSION = "spine.item-facets.v1"
CANONICAL_VERSION = "spine.canonical-json.v1"
KEY = re.compile(r"[a-z][a-z0-9_]{0,63}\Z", re.ASCII)
INTEGER = re.compile(r"(?:0|-?[1-9][0-9]*)\Z", re.ASCII)


def fail(code: str = "facet_value_invalid") -> NoReturn:
    raise SpineValidationError(code, "facet facts do not satisfy the pinned contract")


def nfc(value: str) -> str:
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        fail()
    return unicodedata.normalize("NFC", value)


def key(value: object) -> str:
    if not isinstance(value, str) or not KEY.fullmatch(value):
        fail()
    return str(value)


def integer(value: object) -> int:
    if not isinstance(value, str) or len(value) > 20 or not INTEGER.fullmatch(value):
        fail()
    result = int(value)
    if not -(2**63) <= result < 2**63:
        fail()
    return result


def _text(value: object, maximum: int, *, controls: bool = False) -> str:
    if not isinstance(value, str):
        fail()
    value = nfc(str(value))
    if not 1 <= len(value) <= maximum or (controls and any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value)):
        fail()
    return value


def _object(value: object, required: set[str], optional: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - required - (optional or set()) or required - set(value):
        fail()
    return dict(value)


def normalize_definition(value: object) -> dict[str, Any]:
    try:
        result = _object(value, {"display_name", "description", "compatible_item_types", "fields"})
        result["display_name"] = _text(result["display_name"], 160)
        if result["description"] is not None:
            result["description"] = _text(result["description"], 2000)
        types = result["compatible_item_types"]
        if not isinstance(types, list) or not 1 <= len(types) <= 2 or any(t not in ("event", "task") for t in types):
            fail()
        if len(set(types)) != len(types):
            fail()
        result["compatible_item_types"] = sorted(types)
        fields = result["fields"]
        if not isinstance(fields, list) or not 1 <= len(fields) <= 32:
            fail()
        normalized = []
        for raw in fields:
            if not isinstance(raw, dict):
                fail()
            extras = {
                "text": {"max_length"},
                "enum": {"choices"},
                "integer": {"min", "max"},
                "boolean": set(),
                "date": set(),
                "reference": {"target_kind"},
            }
            kind = raw.get("type")
            if not isinstance(kind, str) or kind not in extras:
                fail()
            field = _object(raw, {"key", "type", "required"} | extras[kind], {"queryable"})
            field["key"] = key(field["key"])
            field.setdefault("queryable", False)
            if type(field["required"]) is not bool or type(field["queryable"]) is not bool:
                fail()
            if kind == "text" and not 1 <= integer(field["max_length"]) <= 1024:
                fail()
            if kind == "integer" and integer(field["min"]) > integer(field["max"]):
                fail()
            if kind == "reference" and field["target_kind"] not in ("subject", "location"):
                fail()
            if kind == "enum":
                choices = field["choices"]
                if not isinstance(choices, list) or not 1 <= len(choices) <= 64:
                    fail()
                choices = [_text(c, 128) for c in choices]
                if len(set(choices)) != len(choices):
                    fail()
                field["choices"] = sorted(choices)
            normalized.append(field)
        if len({f["key"] for f in normalized}) != len(normalized):
            fail()
        result["fields"] = sorted(normalized, key=lambda f: f["key"])
        if len(canonical_json_bytes(result)) > 32768:
            fail()
        return result
    except SpineValidationError as exc:
        raise SpineValidationError("facet_schema_invalid", "invalid facet definition") from exc


def definition_hash(definition: dict[str, Any]) -> str:
    return hashlib.sha256(
        canonical_json_bytes(
            {
                "derivation_version": "spine.facet-definition.v1",
                "definition": definition,
            }
        )
    ).hexdigest()


```

## src/spine/core/rendering_definitions.py:1–130

Full-source SHA-256: `b62b92250578bd19dd286bf60e63a111649c8b48ed8dbf95109af9b6623ace9a`.

```python
"""Pure codecs for the candidate rendering integration; no capability activation."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from spine.core.canonical_json import canonical_json_bytes, canonical_json_text
from spine.core.errors import SpineValidationError
from spine.core.facets import parse_object
from spine.core.hashing import hash_canonical_json
from spine.core.notification_profiles import (
    NormalizedProfileRevision,
    normalize_catalog_key,
    normalize_owner,
    normalize_profile_revision,
)
from spine.core.notification_rendering import _normalized_text

CANON = "spine.canonical-json.v1"
DEFINITIONS = "spine.notification-rendering-definitions.v1"
DISCLOSURES = "spine.notification-rendering-disclosures.v1"
PRESENTATION = "spine.notification-rendering-presentation.v1"
PROFILE_V2 = "spine.notification-profiles.v2"
MAX_INTEGER = 9223372036854775807


def fail(code: str, field: str, message: str = "rendering request could not complete") -> Any:
    raise SpineValidationError(f"{code}:{field}", message)


def exact(value: object, required: set[str], optional: set[str] | None = None, field: str = "request") -> dict[str, Any]:
    if not isinstance(value, Mapping):
        fail("invalid_request", field)
    result = copy.deepcopy(dict(value))
    extra = set(result) - required - (optional or set())
    prefix = "" if field == "request" else field + "."
    if extra:
        fail("unsupported_field", prefix + sorted(extra)[0])
    missing = required - set(result)
    if missing:
        fail("missing_required_field", prefix + sorted(missing)[0])
    canonical_json_bytes(result)  # Reject numbers and invalid Unicode before interpretation.
    return result


def identity(value: object, field: str, maximum: int = 256) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= maximum:
        fail("invalid_request", field)
    canonical_json_bytes(value)
    return value


def text(value: object, field: str, maximum: int) -> str:
    try:
        result = _normalized_text(identity(value, field, max(maximum, 32768)), field)
    except SpineValidationError as exc:
        fail("invalid_request", field, str(exc))
    if not result or len(result) > maximum:
        fail("invalid_request", field)
    return result


def owner(value: object) -> dict[str, Any]:
    normalized = normalize_owner(value)
    return {k: v for k, v in normalized.items() if v is not None}


def sorted_strings(value: object, field: str, maximum: int, *, minimum: int = 0, keys: bool = False) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        fail("invalid_request", field)
    values = [normalize_catalog_key(v, field) if keys else identity(v, field) for v in value]
    if len(values) != len(set(values)):
        fail("semantic_conflict", field, "duplicate values are not permitted")
    return sorted(values)


def definition_reference(value: object) -> dict[str, str]:
    result = exact(value, {"notification_rendering_definition_id", "notification_rendering_definition_revision_id"}, field="definition")
    return {k: identity(v, "definition." + k) for k, v in result.items()}


def normalize_revision(value: object) -> dict[str, Any]:
    revision = exact(
        value,
        {"display_name", "description", "compatible_item_types", "base_rendering_contract", "base_rendering_profile", "selections"},
        field="revision",
    )
    revision["display_name"] = text(revision["display_name"], "revision.display_name", 160)
    if revision["description"] is not None:
        revision["description"] = text(revision["description"], "revision.description", 2000)
    types = revision["compatible_item_types"]
    if not isinstance(types, list) or not 1 <= len(types) <= 2 or any(not isinstance(v, str) or v not in {"event", "task"} for v in types):
        fail("rendering_definition_invalid", "revision.compatible_item_types")
    if len(types) != len(set(types)):
        fail("rendering_definition_invalid", "revision.compatible_item_types")
    revision["compatible_item_types"] = sorted(types)
    if (
        revision["base_rendering_contract"] != "spine.notification-rendering.v1"
        or revision["base_rendering_profile"] != "spine.notification-rendering.concise-en-ca.v1"
    ):
        fail("rendering_definition_invalid", "revision.base_rendering_contract")
    selections = revision["selections"]
    if not isinstance(selections, list) or not 1 <= len(selections) <= 8:
        fail("rendering_definition_invalid", "revision.selections")
    names, sources = set(), set()
    normalized = []
    for selection in selections:
        selection = exact(
            selection,
            {"selection_key", "facet_key", "facet_schema_revision_id", "field_key", "label", "projection"},
            field="revision.selections",
        )
        for k in ("selection_key", "facet_key", "field_key"):
            selection[k] = normalize_catalog_key(selection[k], "revision.selections." + k)
        identity(selection["facet_schema_revision_id"], "revision.selections.facet_schema_revision_id")
        selection["label"] = text(selection["label"], "revision.selections.label", 40)
        if selection["projection"] not in {"value", "location_label"}:
            fail("rendering_definition_invalid", "revision.selections.projection")
        source = tuple(selection[k] for k in ("facet_key", "facet_schema_revision_id", "field_key"))
        if selection["selection_key"] in names or source in sources:
            fail("rendering_definition_invalid", "revision.selections", "duplicate selection")
        names.add(selection["selection_key"])
        sources.add(source)
        normalized.append(selection)
    revision["selections"] = normalized
    bounded(revision, 8192, "revision")
    return revision

```

## src/spine/core/notification_rendering.py:412–420

Full-source SHA-256: `6bfe60d40701d6049d1fdaccaae25a283b764efe2a9dc19abf18ddd5d0459d2b`.

```python
def _normalized_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} must be text")
    result = _WHITESPACE.sub(" ", value.strip())
    if not result:
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} normalizes to empty")
    if any(unicodedata.category(char).startswith("C") for char in result):
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} contains a control character")
    return result
```
```
