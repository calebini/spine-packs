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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-fr1-artifacts-audit-001/audit-notes.md
Hash: 570fa57f7fc592bbe117159b2124bd6d6735c8032383e43dda04e8fd03461f20

# Change intent

Review the remaining FR-1 installer artifact-contract increment: seven separate
v2 artifact schemas, shared/embedded/readback closure, exact typed reference
slots, bounded observation preimages, command-family evidence and synthetic
execution/recovery fixtures. The manifest increment was previously reviewed;
this is a new review gate, not inherited approval or full installer qualification.

Baseline: exact Spine `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`,
schema `19`. The commit was verified available. All 17 upstream schema source
file hashes in the new inventory were independently compared to `git show` at
that exact pin. Four legacy write-response and three legacy read-response
validators reuse existing client projections, explicitly recorded in provenance;
their future package integration still requires exact-baseline qualification.

# Expected boundary

One reviewer-only Whetstone `audit-change`, profile `consistency`, through the
embedded Codex CLI after approval of the exact payload. No Editor, automatic
patching, convergence claim, unrelated file reads, web browsing, ledger access,
Spine changes, runtime implementation, deployment, commit, push or publication.
This directory is staged only; no reviewer has been invoked or authorized.

Packs are owner-neutral declarative configuration. Operator artifacts alone may
hold synthetic owner/actor/target IDs. No disclosure grants, actual facet values,
coordination items, notifications, schedules or destination facts are installed.
Real flight fields, labels/order, selected reminder templates and default-profile
policy remain operator decisions. Synthetic stable-status manifests under tests
are not curated or distributable pack releases.

# Specs and machine agreements to check

Primary authority is `specs/installer-artifacts-v2.md` together with
`specs/facet-rendering-packs.md`. V1 encoding/limits/approval/durability/exit
requirements explicitly carried forward are in `specs/installer-artifacts.md`.
The proposed runtime command map and exact source/pointer closure are in
`contracts/installer-spine-0.9.1-inventory.json`. No network schema fetch is needed.
The pure semantic oracle is test code, not an implemented installer or proof of
real public observations. It is intentionally included in this contract review.

Check especially:

1. Closure, target/owner/manifest correlation, exact environment/contract union,
   schema versions and digest domains. Unknown versions must fail before use.
2. Typed null slots and resolution ownership: only approved paths, correct
   producers/fields, earlier accepted prefix, observed IDs for retain, immutable
   revision pins and complete cascaded update approval. No guessed IDs, string
   interpolation or choosing equivalent historical revisions behind current heads.
3. Exact public request mapping and response differences. Canonical request blobs
   forbid JSON numbers; public response text preserves valid public native numbers.
   Facets have no receipt semantic hash; rendering uses `contract_version` and
   top-level evidence. No fabricated universal receipt or catalog fingerprint.
4. Forward recovery from complete bounded preimages, original selected history,
   unchanged suffix preconditions, prefix/prefix-plus-one candidates, exact replay
   and matching provisional IDs before acceptance. Partial results embed the
   checkpoint so they cannot discard a prepared request. No speculative suffix.
5. Verification is read-only and exact-pin-aware; captured responses are separate
   from fresh state, and no success grants disclosure or asserts notification
   delivery. Preserve the old archetype/v1-ordinary comparison rules.
6. Fixture quality: 36 indexed recovery boundaries across create/update flows,
   all 11 write commands, 33 named negative cases, 27 unchanged upstream wire
   vectors, independent hash preimages and post-resolution byte-limit boundary.
   Identify false-positive negative tests, unsound oracle assumptions or material
   spec/schema/test disagreement. Do not assume a passing oracle proves its own
   correctness or the later runtime gates.

# Checks and explicit remaining gates

At staging: verifier passed (143 required files); independent jsonschema 4.26.0
Draft 2020-12 meta/fixture checks and all 82 contract tests passed; 126 runtime
tests passed. Default Python lacks jsonschema and reports 17 explicit skips;
the isolated validator run, not that skipped run, supplies the schema gate.
Tracked and new-file whitespace checks are required before transmission.

No `src/spine_packs/`, v1 contract or released/draft curated pack bytes changed.
One runtime test now explicitly checks the original 12 runtime-consumed schemas,
instead of assuming every future schema is supported by the v1 subset validator.
V2 schemas remain independently standards-validated, not newly admitted at runtime.

Package qualification has NOT run in this increment: `build`/`hatchling` and the
previous isolated supported-Spine CLI builds are unavailable. New schema files
would be included by the existing packaging rule; before any release, run the
package gate on all supported old baselines plus the separately implemented
successor. Do not substitute the 0.9.1 reference CLI into the current installer.
No build, release, staging or deployment readiness is claimed.

FR-2 still requires real read-transport observation/pagination/config/capacity
adversaries, FR-3 durable filesystem fault injection, FR-4 actual continuation
and verification tests, and FR-5 exact-package disposable qualification. Those
are not implemented here. Flag missing machine-contract prerequisites for those
slices, but do not request implementation of their runtime as an audit patch.

Report actionable findings by file/section with minimal proposed correction.
Product decisions must remain open; do not invent policy to close them.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/AGENTS.md

Hash: b4a3fc77487883da120132dc3af9324d9dfa6e8e8d7bd26ec800f4b95d74a5b1

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
For successor installer artifacts, also read `specs/installer-artifacts-v2.md`.
Its test-only oracle and v2 schemas do not expand current runtime authority.

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

Hash: ab4021ee583e6fb6e7fe611166315aa69516bb701faef4486b7212f774f78153

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

The draft successor machine layer is specified in
[installer-artifacts-v2.md](installer-artifacts-v2.md). Its pure test oracle lives
under `tests/contract/`, not `src/spine_packs/`. Saved synthetic execution and
recovery fixtures are not results from an implemented successor installer.

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

Hash: 4d610ce51736d86085445b4d51107ae69dca995fb23429ea9425d9b3dde11b0c

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

The FR-1 draft artifact schemas and offline public closure pin only this repaired
baseline; `contracts/installer-spine-0.9.1-inventory.json` records the 22-command
map, 17-contract union and source hashes. Draft artifacts are not accepted by
the existing installer. Public response JSON numbers are preserved as validated
text inside v2 evidence, never coerced into v1 canonical comparison values.

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

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer-artifacts.md

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

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer-artifacts-v2.md

Hash: a111640ef10e3c4f6a082bb0b02964ccee0e04a89be690b39d780adef8f52290

```markdown
# Facet/rendering installer artifacts v2

Status: FR-1 draft; machine-contract review required. No successor runtime is
authorized by this document. Read `facet-rendering-packs.md` first. The exact
Spine pin is `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema
`19`. Existing v1 artifacts, runtime compatibility and released packs are unchanged.

## Encoding and entry points

The seven artifact identifiers in `installer-artifacts.md` have separately
named `.v2` successors. Each entry schema references
`spine-pack-installer-types.v2.schema.json`. Shared definitions are not permission
to accept mixed-version artifacts. The v1 encoding, artifact byte ceilings,
local target normalization, approval assertions, private publication, durability,
exit codes and secret-safe errors carry forward. All objects are closed.

Artifact and request JSON MUST reject duplicate members, BOMs, numbers and
invalid Unicode. Decimal quantities remain strings. Digests omit only
`content_identity.digest`, retain the other identity members, and use the
artifact's `spine.pack-<kind>-digest.v2` domain. Command IDs retain the `spack_`
prefix but use `spine.pack-command-id.v2` in the existing four-member preimage.

Two embedded encodings are intentionally distinct:

- `canonical_value` contains `canonical_json` and its SHA-256 `digest`. It is
  parsed with duplicate rejection and MUST equal Spine canonical JSON v1 bytes.
  Its enclosing field, never an author-supplied schema name, chooses validation.
- `public_response` contains `json_text` and its SHA-256 `digest`. Preserve the
  complete UTF-8 public response text after removing only the terminal CLI
  newline. Validate the contextual command's pinned public response schema.
  Public integer revision/index/count fields remain JSON integers inside the
  string; they MUST NOT be relabelled canonical JSON v1 or rewritten as strings.
  Reject duplicate members, nonfinite numbers, BOMs and invalid Unicode. This
  blob can make evidence artifacts differ for equivalent wire whitespace;
  deterministic plans never contain it. Its digest is local byte evidence,
  not a receipt semantic hash or authenticity assertion.

The offline `spine-readback-0.9.1.schema.json` and embedded-value schema contain
only reachable definitions for the approved command boundary. Their inventory
records source hashes, exact source pointers and mappings. No online schema
resolution, Spine import or handler execution is allowed in contract tests.

## Complete observation preimage

An observation contains exact `owner`, sorted unique `entries`, sorted unique
`historical_revisions`, the three available old `public_catalog_snapshots`, and
an installer `digest`. Hash the canonical complete view without `digest`, with
wrapper `{"derivation_version":"spine.pack-observation.v2","view":...}`.
This is explicitly NOT a public Spine snapshot hash.

An entry is a closed semantic projection: typed `object_key`, exact `owner`,
`status`, nullable `root_id`, `revision_id`, `binding_id`, `revision_contract`,
and `value` (canonical semantic body). Root families use archetype revision,
normalized facet definition, rendering revision, or profile metadata plus
revision. Binding bodies carry the actual referenced IDs, not local keys.
Facet/default binding entries require their binding ID and archetype root ID;
they have no independent revision. Root entries have no binding ID. Profile
revision bodies retain their v1/v2 decoder; v1 ordinary semantics may compare
equal to v2 ordinary semantics without changing historical hashes.

Keys are `archetype:<key>`, `schema:<key>`, `facet_binding:<archetype>:<facet>`,
`rendering:<key>`, `profile:<key>`, `binding:<archetype>`. Arrays sort bytewise
by the complete typed key, not action phase; history sorts by `(object_key,
revision_id)`. History contains the exact non-current revisions needed by
selected observed pins, not an arbitrary dump. Root/revision membership and
public definition hashes are validated before projection. Provenance available
in public responses is checked separately; projections do not invent facet
actor/time or receipt evidence.

During execution/recovery, retain original selected revision preimages when an
accepted revision advances their heads, addressed by the old root/revision pair.
This bounded lineage remains in history after the last consumer moves to the
new pin; it supports comparison of the original approved execution. A fresh
independent verification need only read the currently required exact pins.

Collect two complete views, compare their semantic bodies/identities and old
public fingerprints, and fail on any difference. Cursor tokens/page boundaries
are excluded. Each observation operation (including both passes and rechecks)
has hard ceilings: 4,096 public calls, 128 MiB aggregate stdout, 600 seconds
monotonic elapsed time, and 4,096 projected entries including history. Individual
calls retain 30 seconds/16 MiB. Stop BEFORE exceeding a count or starting a call
after the deadline; bound reads while receiving bytes. The tighter public facet
100-candidate ceiling, per-family page limits and artifact byte ceilings still
apply. No truncation, selected-only fallback, unbounded retry or limit override.
These are installer safety budgets, not new Spine capacity promises.

## Plans, resolutions and typed slots

A plan carries the normalized request/digest, manifest-v2 identity, exact
environment and 17-contract union, sorted typed closure, full observation,
classifications, resolutions, actions, decision/blocked lists and eligibility.
Every selected object has exactly one classification and one resolution row.
Classification `desired` is the portable manifest object. `observed` is the
matching observation entry or null; ambiguous/retired dependencies block.

Resolution rows contain `object_key` and nullable `root`, `revision`, `binding`
sources. A source is exactly either:

```json
{"kind":"observed","object_key":"schema:flight_details","field":"revision","value":"example-revision-id"}
```

```json
{"kind":"action_result","action_id":"action-000001","output_pointer":"/facet_schema_revision_id"}
```

Observed sources MUST equal validated observation identity fields for that exact
object and owner. Action sources MUST be the unique approved producer for that
object/field. Publish never supplies a new root. Blocked objects have null
resolutions. Retain uses observed identities; create/publish outputs are unknown
until accepted. Do not select an equivalent historical revision as a substitute.
For either binding family, `root` explicitly aliases its archetype's root source;
the binding's own identity is in `binding`, and its `revision` source is null.

Each action contains ordinal/ID, exact command, typed object key, create/update,
portable desired body, nullable expected observation, a canonical request
template and `slots`. A slot is `{request_pointer, object_key, field}`. The
pointer identifies one complete null-valued ID input in the template; the
object/field selects the resolution table. Arrays of slots sort uniquely by
pointer. This syntax replaces v1 string interpolation; `${` is forbidden
anywhere. No arbitrary pointer or partial text substitution is evaluated.

Only the consumer paths in facet-rendering Section 4 are action-result slots.
Existing-root targets and expected revision/binding preconditions are literal
validated observed IDs, not future outputs. Definition-root/profile-root slots
are distinct from revision slots. Nested selection/template indices refer to
the already-approved arrays and preserve presentation order. Null outside an
approved slot must be permitted by the public request (not treated as a hole).
Every referenced producer must be earlier than its consumer. Complete public
request validation occurs after resolution and execution-field injection.
Rendering revision canonical bytes MUST be <=8,192 after resolution; facet
definition bytes <=32,768. Public bounds also apply to fully resolved values.

Action order is archetypes, schemas, facet bindings, rendering definitions,
profile creates, metadata updates, profile revisions, defaults; lexical key
within phase. Ordinals start at zero; IDs are `action-NNNNNN`. Cascaded pin
changes require separately listed update actions even when local keys match.
Approval authorizes exactly all update IDs plus the complete plan. No runtime
discovery of extra writes is permitted. Drafts remain inspection-only.

## Evidence, checkpoints and recovery

Accepted evidence contains action/command/command ID, exact canonical request,
complete public response and a closed `receipt` tagged by family:

- `catalog`: nested receipt ID, semantic-facts hash and timestamp; effect is
  correlated to the contextual command. Profile v2 requests must already be
  normalized before hashing. Do not invent a replay flag.
- `facet`: top-level receipt ID, effect, changed/replayed and nullable audit ID.
  No semantic hash or actor/time fields. No-op has no audit; replay may retain
  the original effect with `changed=false`.
- `rendering`: top-level receipt/audit IDs, effect and changed/replayed.
  No-op still has an audit. Check `record` ownership, key, revision, hash and
  create/publish provenance; selector is `contract_version`.

The projection MUST exactly equal the validated original response. Derive all
output IDs from that response, not a second editable generated-ID map. Correlate
request target, owner, preconditions, returned IDs, effects, hashes and available
provenance. Fresh schema/binding/rendering readback must agree before accepting
their response; preserve that readback as `post_observation` in evidence.
It is a validated selected-object projection, not a claim to observe a receipt.
No-op cannot satisfy a planned semantic change. A compatible replay response
does not by itself establish current state.

Checkpoints bind plan/approval/execution and a contiguous accepted prefix.
`unresolved_submission` preserves the first unresolved exact request and command
ID with `submission_state=prepared_or_submitted`. Durably publish before
submission and durably append validated evidence before any consumer. Replay
MUST reproduce all request bytes, actor, time and command ID; never inject
provisional readback IDs into a request or into later consumers.

Continuation compares fresh complete view against forward application of the
accepted prefix to the saved preimage, or that prefix plus exactly one unresolved
action. Untouched entries/history must remain unchanged. Missing public facet
provenance does not authorize a receipt inference: only exact original request
replay and matching returned identities can accept the provisional candidate.
Reject gaps, suffix effects, unexplained changes and ambiguous candidates.
When a genuine no-op makes both candidates identical, deduplicate identical
states and still replay the unresolved request; never infer acceptance from it.
Default bindings retain immediate non-CAS rechecks; facet bindings retain exact
`expected_binding_id` CAS including null for absence, also during uncertain replay.

Terminal results embed the final checkpoint as `checkpoint`, plus state,
failure and unattempted IDs. This avoids losing the exact prepared request when
continuing from `partial`. All nested identities must correlate. First submitted
failure is partial even with an empty prefix. `not_applied` is initial-only,
has no accepted responses or unresolved submission, and cannot be a continuation
source. A durability failure may leave only a checkpoint, never fabricated
success. No rollback, compensation or fresh execution to bypass uncertainty.

## Verification and fixture gate

Verification binds plan, optional apply-result digest, pack, target, environment,
fresh complete observation, closure, ordered object results and response-evidence
coverage. Every object result carries actual observed state and exact resolved
identity. Current schema/rendering heads and all reference edges must match;
historical availability alone is insufficient. Unrelated unselected changes do
not fail final verification (but do fail continuation).

`receipt_readback=captured_responses_only_spine_0.9.1` and
`disclosure=separate_operator_configuration_required` are mandatory. No missing
receipt is repaired by replay in verify. No result claims item creation,
disclosure approval, rendering correctness or notification delivery.

The versioned fixture index names structural and semantic oracles separately.
Synthetic stable-status manifests exist only under tests to exercise eligibility;
they are not pack releases. Saved execution/recovery scenarios are test evidence,
not results from a real installer. FR-2/3/4 still require transport, observation,
durability and fault-injection tests; FR-5 still requires exact-package public
CLI qualification. Contract test success does not waive bounded review.
```

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/facet-rendering-packs.md

Hash: f8f901a65824df8235b63fc8eb1141d78286a5329d1a6c4cc43d6dc341346651

```markdown
# Facet-aware packs: successor contract proposal

Status: proposed; FR-1 contract/fixture work in progress, runtime not implemented.
Repaired baseline inspected on 2026-10-10. Normative language below defines
the proposed successor, not additional authority for the current installer.

The FR-1 installer-artifact codification is in
[installer-artifacts-v2.md](installer-artifacts-v2.md), with separate v2 schemas,
source inventory and synthetic execution/recovery fixtures. It remains pending
bounded review; it does not widen the current runtime's command allowlists.

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

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: be1387960a8c02a08f0db24dc276acf9eddf555b29c1d1cbc266c3127ea0d241

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

The next increment is now authored in `installer-artifacts-v2.md`: seven v2
entry schemas, shared/embedded types, offline pinned public closure, typed null
slots and aggregate observation budgets. Synthetic create and cascading-update
flight flows cover all 11 writes and prepared/response-loss/accepted recovery
boundaries. Family-specific evidence retains complete public response text,
including native public JSON numbers, without inventing a universal receipt.
Upstream wire vectors supplement the independent schema/semantic/hash oracles.

Next: approve and run the bounded artifact-contract review, address findings,
then separately authorize FR-2. This is not FR-1 review completion or runtime
qualification. FR-2 must prove actual full two-pass pagination, cursor-config,
capacity and transport failure handling; FR-3 must prove durable filesystem
ordering; FR-4 must implement and fault-test continuation/verification. The
synthetic oracle cannot stand in for these runtime tests. FR-5 still requires
the exact Spine package and existing-baseline package regression gates.
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/docs/facet-rendering-baseline.md

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

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/installer-spine-0.9.1-inventory.json

Hash: 5837583b796de6b9f9fc90ea511851b271cdbdfcb63fc6a0028e54bc5003282a

```markdown
{
  "spine_commit": "57cda1c2d5589360ee8efe7155fd20b503034c2a",
  "runtime_version": "0.9.1",
  "ledger_schema": "19",
  "required_execution_contracts": [
    "spine.archetype-facet-bindings.v1",
    "spine.canonical-json.v1",
    "spine.facet-cursor.v1",
    "spine.facet-schemas.v1",
    "spine.item-archetypes.v1",
    "spine.ledger-instance.v1",
    "spine.notification-profile-bindings.v1",
    "spine.notification-profile-catalog-cursor.v1",
    "spine.notification-profile-metadata-update.v1",
    "spine.notification-profile-readback.v1",
    "spine.notification-profiles.v1",
    "spine.notification-profiles.v2",
    "spine.notification-rendering-cursor.v1",
    "spine.notification-rendering-definitions.v1",
    "spine.notification-rendering-integration.v1",
    "spine.system-info.v3",
    "spine.tickerd-compatibility.v1"
  ],
  "commands": {
    "facet_schema.create": {
      "request": "public_0055",
      "response": "public_0062",
      "family": "facet",
      "selector": "spine.facet-schemas.v1",
      "phase": 1,
      "outputs": {
        "root": "/facet_schema_id",
        "revision": "/facet_schema_revision_id"
      }
    },
    "facet_schema.list": {
      "request": "public_0098",
      "response": "public_0101",
      "family": "facet",
      "selector": "spine.facet-schemas.v1",
      "phase": null,
      "outputs": {}
    },
    "facet_schema.publish": {
      "request": "public_0063",
      "response": "public_0064",
      "family": "facet",
      "selector": "spine.facet-schemas.v1",
      "phase": 1,
      "outputs": {
        "revision": "/facet_schema_revision_id"
      }
    },
    "facet_schema.show": {
      "request": "public_0103",
      "response": "public_0104",
      "family": "facet",
      "selector": "spine.facet-schemas.v1",
      "phase": null,
      "outputs": {}
    },
    "item_archetype.create": {
      "request": "public_0000",
      "response": "public_0008",
      "family": "catalog",
      "selector": "spine.item-archetypes.v1",
      "phase": 0,
      "outputs": {
        "root": "/item_archetype_id",
        "revision": "/item_archetype_revision_id"
      }
    },
    "item_archetype.facet_binding.list": {
      "request": "public_0108",
      "response": "public_0109",
      "family": "facet",
      "selector": "spine.archetype-facet-bindings.v1",
      "phase": null,
      "outputs": {}
    },
    "item_archetype.facet_binding.set": {
      "request": "public_0066",
      "response": "public_0067",
      "family": "facet",
      "selector": "spine.archetype-facet-bindings.v1",
      "phase": 2,
      "outputs": {
        "binding": "/facet_binding_id"
      }
    },
    "item_archetype.list": {
      "request": "public_0078",
      "response": "public_0079",
      "family": "catalog",
      "selector": "spine.item-archetypes.v1",
      "phase": null,
      "outputs": {}
    },
    "item_archetype.revise": {
      "request": "public_0014",
      "response": "public_0015",
      "family": "catalog",
      "selector": "spine.item-archetypes.v1",
      "phase": 0,
      "outputs": {
        "revision": "/item_archetype_revision_id"
      }
    },
    "item_archetype.show": {
      "request": "public_0085",
      "response": "public_0086",
      "family": "catalog",
      "selector": "spine.item-archetypes.v1",
      "phase": null,
      "outputs": {}
    },
    "notification_profile.binding.list": {
      "request": "public_0087",
      "response": "public_0088",
      "family": "catalog",
      "selector": "spine.notification-profile-bindings.v1",
      "phase": null,
      "outputs": {}
    },
    "notification_profile.binding.set": {
      "request": "public_0019",
      "response": "public_0020",
      "family": "catalog",
      "selector": "spine.notification-profile-bindings.v1",
      "phase": 7,
      "outputs": {
        "binding": "/notification_profile_binding_id"
      }
    },
    "notification_profile.create": {
      "request": "public_0022",
      "response": "public_0050",
      "family": "catalog",
      "selector": "spine.notification-profiles.v2",
      "phase": 4,
      "outputs": {
        "revision": "/notification_profile_revision_id",
        "root": "/notification_profile_id"
      }
    },
    "notification_profile.list": {
      "request": "public_0090",
      "response": "public_0091",
      "family": "catalog",
      "selector": "spine.notification-profiles.v2",
      "phase": null,
      "outputs": {}
    },
    "notification_profile.metadata.update": {
      "request": "public_0016",
      "response": "public_0018",
      "family": "catalog",
      "selector": "spine.notification-profile-metadata-update.v1",
      "phase": 5,
      "outputs": {}
    },
    "notification_profile.revise": {
      "request": "public_0053",
      "response": "public_0054",
      "family": "catalog",
      "selector": "spine.notification-profiles.v2",
      "phase": 6,
      "outputs": {
        "revision": "/notification_profile_revision_id"
      }
    },
    "notification_profile.show": {
      "request": "public_0096",
      "response": "public_0097",
      "family": "catalog",
      "selector": "spine.notification-profiles.v2",
      "phase": null,
      "outputs": {}
    },
    "notification_rendering_definition.create": {
      "request": "public_0068",
      "response": "public_0073",
      "family": "rendering",
      "selector": "spine.notification-rendering-definitions.v1",
      "phase": 3,
      "outputs": {
        "revision": "/record/notification_rendering_definition_revision_id",
        "root": "/record/notification_rendering_definition_id"
      }
    },
    "notification_rendering_definition.list": {
      "request": "public_0111",
      "response": "public_0112",
      "family": "rendering",
      "selector": "spine.notification-rendering-definitions.v1",
      "phase": null,
      "outputs": {}
    },
    "notification_rendering_definition.publish": {
      "request": "public_0076",
      "response": "public_0077",
      "family": "rendering",
      "selector": "spine.notification-rendering-definitions.v1",
      "phase": 3,
      "outputs": {
        "revision": "/record/notification_rendering_definition_revision_id"
      }
    },
    "notification_rendering_definition.show": {
      "request": "public_0113",
      "response": "public_0114",
      "family": "rendering",
      "selector": "spine.notification-rendering-definitions.v1",
      "phase": null,
      "outputs": {}
    },
    "system.info": {
      "request": "emptyRequest",
      "response": "public_0115",
      "family": "environment",
      "selector": null,
      "phase": null,
      "outputs": {}
    }
  },
  "source_sha256": {
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json": "35f34ee2df956e44706545b973645ed4c979164d5145665f086aeb189d385d8c",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json": "80bcc0fbb003b7702fdc17424db6287ebdd696cc5e2d8a1411c359573004a69f",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json": "29321672a1b7ba31599080e968c1b30295fe68748560cba0a64468a4d0e341aa",
    "upstream/contracts/schemas/archetype-facet-failure.schema.json": "eaaee30acf5002f3da4bb5d41c622d648ed19254ab2323799a6e1632cfa3a25b",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json": "ef713cd19b37b48ee014e7fc7e97a23bb7a4657a080a77d6fac3396c0c0ab49e",
    "upstream/contracts/schemas/archetype-facet-types.schema.json": "689163800b0aaa07b87a1fc75a7bea7150bd70f1bcf2fbad901466cdf594dcda",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json": "a1ee1cfd3d522426a58d35ef43956c7609456ac1a2224d4482edc3f526bc6d54",
    "upstream/contracts/schemas/notification-profile-commands.schema.json": "573d7b1bed42a1190887291f860c6edac0b6b52199c72023c3afd2b354743781",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json": "8edc2234ed3797e571430e0db1404f849cb5e2eadd58580fe01af76bd7bba0b9",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json": "e1587494d473198b49f16be89e27de12e32df512821d5670f9c8bf48f654f875",
    "upstream/contracts/schemas/notification-profile-types.schema.json": "182353b53719d924cb062d898d7e3cae1f0de9e124bb2b793c26fa6a59ab6b8c",
    "upstream/contracts/schemas/notification-rendering-cursor-config.schema.json": "ac4a753ebb403db3b0d430b8e412b15fdf38fcc71135854ed35bc1e8ac106829",
    "upstream/contracts/schemas/notification-rendering-definition-commands.schema.json": "755135d632e81e3b492533004f8878ab0a9bf20bd3ccb01b94cb76fdc0f45e6d",
    "upstream/contracts/schemas/notification-rendering-definition-responses.schema.json": "df4352d013699072b0d37ea38299cae613e7ef2123690523a72d23f815d9f4af",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json": "3b6ea94ce86bbb06f45c63516700235edba43cd0800ed4be05261fc774848344",
    "upstream/contracts/schemas/notification-rendering-integration-failure.schema.json": "25a887ebb1569d299ede8353fec2c0752cdccca92dc29e615290d6387e68cc8e",
    "upstream/contracts/schemas/notification-rendering-integration-types.schema.json": "5740b6f3e92cdac2f48daf4f85ea79b37803345dfb54a705f5fd8c37ff320aa6",
    "upstream/contracts/schemas/notification-types.schema.json": "48507bcf78b6df80a6c9ca8ebf7b0a5fa7e26b8b691befdc1e7353ae63b7b2c1",
    "upstream/contracts/schemas/system-info-response-v3.schema.json": "d4031875ec3029b907113b650b6634fdf8d0eb7b5814a401f21cc2e92c1bd9e8"
  },
  "source_pointers": {
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/archetypeCreateResponse": "public_0008",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/archetypeReviseResponse": "public_0015",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/bindingSetResponse": "public_0020",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/commands_profileMetadata": "public_0116",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_absoluteBoundary": "public_0123",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_boundary": "public_0122",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_cadence": "public_0131",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_calendarTargetOffset": "public_0127",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_decimalNonNegative": "public_0137",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_decimalPositive": "public_0010",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_elapsedTargetOffset": "public_0125",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_fixedElapsedCadence": "public_0132",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_id": "public_0009",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_lateHandling": "public_0136",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_localCalendarCadence": "public_0133",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_localDate": "public_0134",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_localTime": "public_0128",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_offsetsSchedule": "public_0129",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_onceSchedule": "public_0121",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_repeatWindowSchedule": "public_0130",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_schedule": "public_0120",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_sha256": "public_0012",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_signedDecimal": "public_0126",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_targetOffset": "public_0124",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_utcTimestamp": "public_0013",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/notifications_weekday": "public_0135",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/profileMetadataUpdateResponse": "public_0018",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/profileSemantics": "public_0117",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/description": "public_0084",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_archetypeRevision/properties/display_name": "public_0083",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_itemTypes": "public_0021",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_key": "public_0011",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_profileRevision": "public_0118",
    "spine-packs/contracts/schemas/spine-pack-embedded-values.v1.schema.json#/$defs/types_template": "public_0119",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/archetype": "public_0080",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/archetypeRevision": "public_0082",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/archetypeShow": "public_0086",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/archetypesPage": "public_0079",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/binding": "public_0089",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/bindingsPage": "public_0088",
    "spine-packs/contracts/schemas/spine-readback-0.3.0.schema.json#/$defs/id": "public_0081",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.create": "public_0055",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.list": "public_0098",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.publish": "public_0063",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/facet_schema.show": "public_0103",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/item_archetype.facet_binding.list": "public_0108",
    "upstream/contracts/schemas/archetype-facet-commands.schema.json#/$defs/item_archetype.facet_binding.set": "public_0066",
    "upstream/contracts/schemas/archetype-facet-failure.schema.json#": "public_0138",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.create": "public_0062",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.list": "public_0101",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.publish": "public_0064",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/facet_schema.show": "public_0104",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/item_archetype.facet_binding.list": "public_0109",
    "upstream/contracts/schemas/archetype-facet-responses.schema.json#/$defs/item_archetype.facet_binding.set": "public_0067",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/binding": "public_0110",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/cursor": "public_0100",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/definition": "public_0059",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/field": "public_0060",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/hash": "public_0107",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/id": "public_0056",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/key": "public_0058",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/limit": "public_0099",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/normalizedDefinition": "public_0106",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/owner": "public_0057",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/positiveDecimal": "public_0065",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/revision": "public_0105",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/root": "public_0102",
    "upstream/contracts/schemas/archetype-facet-types.schema.json#/$defs/signedInteger": "public_0061",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileCreate": "public_0022",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileList": "public_0090",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileRevise": "public_0053",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/profileShow": "public_0096",
    "upstream/contracts/schemas/notification-profile-commands-v2.schema.json#/$defs/writeIdentity": "public_0023",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/archetypeCreate": "public_0000",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/archetypeList": "public_0078",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/archetypeRevise": "public_0014",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/archetypeShow": "public_0085",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/bindingList": "public_0087",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/bindingSet": "public_0019",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/profileMetadata": "public_0017",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/profileMetadataUpdate": "public_0016",
    "upstream/contracts/schemas/notification-profile-commands.schema.json#/$defs/writeIdentity": "public_0001",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/create": "public_0050",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/historicalRevision": "public_0094",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/list": "public_0091",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/profile": "public_0092",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/receipt": "public_0052",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/revise": "public_0054",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/revision": "public_0093",
    "upstream/contracts/schemas/notification-profile-responses-v2.schema.json#/$defs/show": "public_0097",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/itemTypes": "public_0027",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/key": "public_0025",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/normalizedRevision": "public_0095",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/owner": "public_0024",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/profileRevision": "public_0026",
    "upstream/contracts/schemas/notification-profile-types-v2.schema.json#/$defs/template": "public_0028",
    "upstream/contracts/schemas/notification-profile-types.schema.json#/$defs/archetypeRevision": "public_0006",
    "upstream/contracts/schemas/notification-profile-types.schema.json#/$defs/itemTypes": "public_0007",
    "upstream/contracts/schemas/notification-profile-types.schema.json#/$defs/key": "public_0005",
    "upstream/contracts/schemas/notification-profile-types.schema.json#/$defs/owner": "public_0004",
    "upstream/contracts/schemas/notification-rendering-cursor-config.schema.json#": "public_0140",
    "upstream/contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.create": "public_0068",
    "upstream/contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.list": "public_0111",
    "upstream/contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.publish": "public_0076",
    "upstream/contracts/schemas/notification-rendering-definition-commands.schema.json#/$defs/notification_rendering_definition.show": "public_0113",
    "upstream/contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.create": "public_0073",
    "upstream/contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.list": "public_0112",
    "upstream/contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.publish": "public_0077",
    "upstream/contracts/schemas/notification-rendering-definition-responses.schema.json#/$defs/notification_rendering_definition.show": "public_0114",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/definitionRecord": "public_0074",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/definitionReference": "public_0049",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/owner": "public_0070",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/provenance": "public_0075",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/revision": "public_0071",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/selection": "public_0072",
    "upstream/contracts/schemas/notification-rendering-definition-types.schema.json#/$defs/utcTimestamp": "public_0069",
    "upstream/contracts/schemas/notification-rendering-integration-failure.schema.json#": "public_0139",
    "upstream/contracts/schemas/notification-rendering-integration-types.schema.json#/$defs/templateRendering": "public_0048",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/absoluteBoundary": "public_0032",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/boundary": "public_0031",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/cadence": "public_0040",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/calendarTargetOffset": "public_0036",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/decimalNonNegative": "public_0047",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/decimalPositive": "public_0042",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/elapsedTargetOffset": "public_0034",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/fixedElapsedCadence": "public_0041",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/id": "public_0002",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/lateHandling": "public_0046",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/localCalendarCadence": "public_0043",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/localDate": "public_0044",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/localTime": "public_0037",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/offsetsSchedule": "public_0038",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/onceSchedule": "public_0030",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/repeatWindowSchedule": "public_0039",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/schedule": "public_0029",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/sha256": "public_0051",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/signedDecimal": "public_0035",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/targetOffset": "public_0033",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/utcTimestamp": "public_0003",
    "upstream/contracts/schemas/notification-types.schema.json#/$defs/weekday": "public_0045",
    "upstream/contracts/schemas/system-info-response-v3.schema.json#": "public_0115"
  },
  "limits": {
    "calls": "4096",
    "stdout_bytes": "134217728",
    "elapsed_seconds": "600",
    "entries": "4096",
    "per_call_seconds": "30",
    "per_call_stdout_bytes": "16777216"
  }
}
```

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/installer-fixture-manifest.v2.json

Hash: 53633bd2f7b459a2b22d9ba18b2f5c254dc18ea8cd94eedff8b8fdbca14d37c6

```markdown
{
  "contract": "spine.pack-installer-fixtures.v2",
  "status": "synthetic_contract_proof_not_runtime_qualification",
  "fixtures": [
    "tests/fixtures/installer-v2/flight-create.json",
    "tests/fixtures/installer-v2/flight-update.json",
    "tests/fixtures/installer-v2/public-wire-vectors.json"
  ],
  "vectors": [
    {
      "id": "flight-create-0-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "0",
      "command": "item_archetype.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-0-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "0",
      "command": "item_archetype.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-0-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "0",
      "command": "item_archetype.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-1-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "1",
      "command": "facet_schema.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-1-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "1",
      "command": "facet_schema.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-1-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "1",
      "command": "facet_schema.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-2-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-create-2-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-create-2-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-create-3-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "3",
      "command": "notification_rendering_definition.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-3-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "3",
      "command": "notification_rendering_definition.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-3-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "3",
      "command": "notification_rendering_definition.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-4-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "4",
      "command": "notification_profile.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-4-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "4",
      "command": "notification_profile.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-4-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "4",
      "command": "notification_profile.create",
      "expected": "accept"
    },
    {
      "id": "flight-create-5-prepared_before_submit",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "5",
      "command": "notification_profile.binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-create-5-accepted_response_lost",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "5",
      "command": "notification_profile.binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-create-5-accepted_durable",
      "fixture": "flight-create.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "5",
      "command": "notification_profile.binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-update-0-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "0",
      "command": "item_archetype.revise",
      "expected": "accept"
    },
    {
      "id": "flight-update-0-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "0",
      "command": "item_archetype.revise",
      "expected": "accept"
    },
    {
      "id": "flight-update-0-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "0",
      "command": "item_archetype.revise",
      "expected": "accept"
    },
    {
      "id": "flight-update-1-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "1",
      "command": "facet_schema.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-1-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "1",
      "command": "facet_schema.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-1-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "1",
      "command": "facet_schema.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-2-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-update-2-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-update-2-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "2",
      "command": "item_archetype.facet_binding.set",
      "expected": "accept"
    },
    {
      "id": "flight-update-3-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "3",
      "command": "notification_rendering_definition.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-3-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "3",
      "command": "notification_rendering_definition.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-3-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "3",
      "command": "notification_rendering_definition.publish",
      "expected": "accept"
    },
    {
      "id": "flight-update-4-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "4",
      "command": "notification_profile.metadata.update",
      "expected": "accept"
    },
    {
      "id": "flight-update-4-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "4",
      "command": "notification_profile.metadata.update",
      "expected": "accept"
    },
    {
      "id": "flight-update-4-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "4",
      "command": "notification_profile.metadata.update",
      "expected": "accept"
    },
    {
      "id": "flight-update-5-prepared_before_submit",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "prepared_before_submit",
      "prefix_length": "5",
      "command": "notification_profile.revise",
      "expected": "accept"
    },
    {
      "id": "flight-update-5-accepted_response_lost",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_response_lost",
      "prefix_length": "5",
      "command": "notification_profile.revise",
      "expected": "accept"
    },
    {
      "id": "flight-update-5-accepted_durable",
      "fixture": "flight-update.json",
      "oracle": "recovery",
      "boundary": "accepted_durable",
      "prefix_length": "5",
      "command": "notification_profile.revise",
      "expected": "accept"
    }
  ],
  "required_followups": [
    "bounded machine-contract review",
    "FR-2 transport observation adversaries",
    "FR-3 durable filesystem fault injection",
    "FR-4 actual continuation/verify implementation",
    "FR-5 exact-package disposable qualification"
  ],
  "negative_vector_groups": [
    {
      "oracle": "test_negative_typed_references_and_complete_authorization",
      "cases": [
        "forward",
        "wrong_output",
        "wrong_object",
        "missing_slot",
        "non_null_slot",
        "missing_resolution",
        "stale_approval",
        "unauthorized_update",
        "wrong_union",
        "wrong_environment",
        "wrong_owner",
        "closure_gap",
        "wrong_digest"
      ]
    },
    {
      "oracle": "test_negative_evidence_and_replay",
      "cases": [
        "gap",
        "changed_request",
        "wrong_command_id",
        "wrong_receipt_hash",
        "wrong_output",
        "dry_run",
        "wrong_selector",
        "wrong_projection",
        "wrong_provenance",
        "noop_change",
        "guessed_suffix",
        "unrelated_change",
        "candidate_without_replay",
        "candidate_id_mismatch"
      ]
    },
    {
      "oracle": "test_verification_exact_pins_and_read_only_evidence",
      "cases": [
        "current_head",
        "binding_pin",
        "missing_result",
        "wrong_target",
        "missing_object",
        "false_disclosure"
      ]
    }
  ],
  "additional_oracles": [
    "test_resolved_rendering_byte_limit_inclusive",
    "test_response_text_numbers_and_duplicate_rejection",
    "test_all_artifact_digests_and_v1_rejection",
    "test_command_and_artifact_hash_preimages_independent",
    "test_retain_no_write_plan_and_draft_refusal",
    "test_upstream_public_wire_vectors"
  ]
}
```

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-manifest.v2.schema.json

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

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-apply-checkpoint.v2.schema.json

Hash: 145b83affdf237a72de33e9e1ca287816b42ecb345cd328e2a43a37c3c8c54b8

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-apply-checkpoint.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/apply-checkpoint"
}
```

### Spec 14: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-apply-result.v2.schema.json

Hash: 7cfec6adfaec65521e5fd8e490dc01652bceb0509d104348e7f417ac780d29e8

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-apply-result.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/apply-result"
}
```

### Spec 15: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-embedded-values.v2.schema.json

Hash: 97d6aefb03028ce25bb7045d56da5d516297b3ac43399c7080029bffb7f18b5f

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-embedded-values.v2.schema.json",
  "$defs": {
    "archetype": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_archetype"
    },
    "schema": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_schema"
    },
    "rendering": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_rendering"
    },
    "profile": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_profile"
    },
    "profile_v1": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_profile_v1"
    },
    "facet_binding": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_facet_binding"
    },
    "binding": {
      "$ref": "spine-readback-0.9.1.schema.json#/$defs/semantic_binding"
    }
  }
}
```

### Spec 16: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-approval.v2.schema.json

Hash: 89418696ca63403d6f3e56b8f2c6b3da2a3474149679360dadd5904eabe5f2e9

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-approval.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/install-approval"
}
```

### Spec 17: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-plan.v2.schema.json

Hash: b9ee69ee49e24846e985651d546ecb3d1ff3a51c0d646ac27685fb210fb1bc9f

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-plan.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/install-plan"
}
```

### Spec 18: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-install-request.v2.schema.json

Hash: ee241dc6b97afdf53e974a1847791ddbb9dfbabebe464c5e148bec77f4f18f6b

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-install-request.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/install-request"
}
```

### Spec 19: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-installer-result.v2.schema.json

Hash: 7788964b91aa95fc9737fd482136eaab828bf405814382a354e653c8846b34a7

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-installer-result.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/installer-result"
}
```

### Spec 20: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-installer-types.v2.schema.json

Hash: 8f036f0a893d4a1eacd4a2916133bee1704d9aab579c349a6e92f527fdce4355

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-installer-types.v2.schema.json",
  "$comment": "Draft FR-1. Semantic correlation, contextual embedded validation, canonical ordering, digests and byte ceilings are normative in specs/installer-artifacts-v2.md.",
  "$defs": {
    "id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "decimal": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)$"
    },
    "sha256": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "utc": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "uuid4": {
      "type": "string",
      "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    },
    "absolutePath": {
      "type": "string",
      "minLength": 2,
      "maxLength": 4096,
      "pattern": "^/.*[^/]$"
    },
    "nullableString": {
      "oneOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 4096
        },
        {
          "type": "null"
        }
      ]
    },
    "selection": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "mode"
          ],
          "properties": {
            "mode": {
              "const": "all"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "mode",
            "archetype_keys"
          ],
          "properties": {
            "mode": {
              "const": "archetypes"
            },
            "archetype_keys": {
              "type": "array",
              "minItems": 1,
              "maxItems": 256,
              "uniqueItems": true,
              "items": {
                "$ref": "#/$defs/key"
              }
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
          "required": [
            "owner_kind",
            "owner_subject_id"
          ],
          "properties": {
            "owner_kind": {
              "const": "subject"
            },
            "owner_subject_id": {
              "$ref": "#/$defs/id"
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
              "$ref": "#/$defs/id"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "target": {
      "type": "object",
      "required": [
        "host_name",
        "spine_command",
        "ledger"
      ],
      "properties": {
        "host_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 253,
          "pattern": "^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
        },
        "spine_command": {
          "type": "object",
          "required": [
            "path",
            "sha256"
          ],
          "properties": {
            "path": {
              "$ref": "#/$defs/absolutePath"
            },
            "sha256": {
              "$ref": "#/$defs/sha256"
            }
          },
          "additionalProperties": false
        },
        "ledger": {
          "type": "object",
          "required": [
            "kind",
            "path"
          ],
          "properties": {
            "kind": {
              "const": "path"
            },
            "path": {
              "$ref": "#/$defs/absolutePath"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "requestBody": {
      "type": "object",
      "required": [
        "selection",
        "owner",
        "target",
        "draft_posture"
      ],
      "properties": {
        "selection": {
          "$ref": "#/$defs/selection"
        },
        "owner": {
          "$ref": "#/$defs/owner"
        },
        "target": {
          "$ref": "#/$defs/target"
        },
        "draft_posture": {
          "enum": [
            "reject",
            "inspect_only"
          ]
        }
      },
      "additionalProperties": false
    },
    "execution": {
      "type": "object",
      "required": [
        "execution_id",
        "actor_subject_id",
        "action_timestamp_utc"
      ],
      "properties": {
        "execution_id": {
          "$ref": "#/$defs/uuid4"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/id"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/utc"
        }
      },
      "additionalProperties": false
    },
    "error": {
      "type": "object",
      "required": [
        "category",
        "code",
        "message",
        "facts"
      ],
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
        "code": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_]{0,95}$"
        },
        "message": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "facts": {
          "type": "array",
          "maxItems": 64,
          "items": {
            "$ref": "#/$defs/generatedId"
          }
        }
      },
      "additionalProperties": false
    },
    "artifactReference": {
      "type": "object",
      "required": [
        "path",
        "digest"
      ],
      "properties": {
        "path": {
          "type": "string",
          "minLength": 1,
          "maxLength": 4096
        },
        "digest": {
          "$ref": "#/$defs/sha256"
        }
      },
      "additionalProperties": false
    },
    "applyFailure": {
      "type": "object",
      "required": [
        "action_id",
        "error"
      ],
      "properties": {
        "action_id": {
          "oneOf": [
            {
              "type": "string",
              "pattern": "^action-[0-9]{6}$"
            },
            {
              "type": "null"
            }
          ]
        },
        "error": {
          "$ref": "#/$defs/error"
        }
      },
      "additionalProperties": false
    },
    "canonicalValue": {
      "type": "object",
      "properties": {
        "canonical_json": {
          "type": "string",
          "maxLength": 16777216
        },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "required": [
        "canonical_json",
        "digest"
      ],
      "additionalProperties": false
    },
    "publicResponse": {
      "type": "object",
      "properties": {
        "json_text": {
          "type": "string",
          "maxLength": 16777216
        },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "required": [
        "json_text",
        "digest"
      ],
      "additionalProperties": false
    },
    "packIdentity": {
      "type": "object",
      "required": [
        "manifest_schema",
        "pack_id",
        "version",
        "status",
        "manifest_digest"
      ],
      "properties": {
        "manifest_schema": {
          "const": "spine.pack-manifest.v2"
        },
        "pack_id": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$",
          "maxLength": 64
        },
        "version": {
          "type": "string",
          "minLength": 5,
          "maxLength": 64
        },
        "status": {
          "enum": [
            "draft",
            "released"
          ]
        },
        "manifest_digest": {
          "$ref": "#/$defs/sha256"
        }
      },
      "additionalProperties": false
    },
    "environment": {
      "type": "object",
      "properties": {
        "runtime_version": {
          "const": "0.9.1"
        },
        "ledger_schema_implemented": {
          "const": "19"
        },
        "ledger_schema_current": {
          "const": "19"
        },
        "ledger_instance_id": {
          "type": "string",
          "pattern": "^ledger_instance_[0-9a-f]{64}$"
        },
        "advertised_contracts": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 256
          },
          "maxItems": 256
        }
      },
      "required": [
        "runtime_version",
        "ledger_schema_implemented",
        "ledger_schema_current",
        "ledger_instance_id",
        "advertised_contracts"
      ],
      "additionalProperties": false
    },
    "state": {
      "type": "object",
      "properties": {
        "object_key": {
          "type": "string",
          "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
        },
        "owner": {
          "$ref": "#/$defs/owner"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "root_id": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            {
              "type": "null"
            }
          ]
        },
        "revision_id": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            {
              "type": "null"
            }
          ]
        },
        "binding_id": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            {
              "type": "null"
            }
          ]
        },
        "revision_contract": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            {
              "type": "null"
            }
          ]
        },
        "value": {
          "$ref": "#/$defs/canonicalValue"
        }
      },
      "required": [
        "object_key",
        "owner",
        "status",
        "root_id",
        "revision_id",
        "binding_id",
        "revision_contract",
        "value"
      ],
      "additionalProperties": false
    },
    "observation": {
      "type": "object",
      "properties": {
        "owner": {
          "$ref": "#/$defs/owner"
        },
        "entries": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/state"
          },
          "maxItems": 4096
        },
        "historical_revisions": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/state"
          },
          "maxItems": 4096
        },
        "public_catalog_snapshots": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "catalog": {
                "enum": [
                  "archetypes",
                  "profiles",
                  "bindings"
                ]
              },
              "digest": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$"
              }
            },
            "required": [
              "catalog",
              "digest"
            ],
            "additionalProperties": false
          },
          "maxItems": 3
        },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "required": [
        "owner",
        "entries",
        "historical_revisions",
        "public_catalog_snapshots",
        "digest"
      ],
      "additionalProperties": false
    },
    "source": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "kind": {
              "const": "observed"
            },
            "object_key": {
              "type": "string",
              "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
            },
            "field": {
              "enum": [
                "root",
                "revision",
                "binding"
              ]
            },
            "value": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            }
          },
          "required": [
            "kind",
            "object_key",
            "field",
            "value"
          ],
          "additionalProperties": false
        },
        {
          "type": "object",
          "properties": {
            "kind": {
              "const": "action_result"
            },
            "action_id": {
              "type": "string",
              "pattern": "^action-[0-9]{6}$"
            },
            "output_pointer": {
              "enum": [
                "/facet_binding_id",
                "/facet_schema_id",
                "/facet_schema_revision_id",
                "/item_archetype_id",
                "/item_archetype_revision_id",
                "/notification_profile_binding_id",
                "/notification_profile_id",
                "/notification_profile_revision_id",
                "/record/notification_rendering_definition_id",
                "/record/notification_rendering_definition_revision_id"
              ]
            }
          },
          "required": [
            "kind",
            "action_id",
            "output_pointer"
          ],
          "additionalProperties": false
        }
      ]
    },
    "resolution": {
      "type": "object",
      "properties": {
        "object_key": {
          "type": "string",
          "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
        },
        "root": {
          "oneOf": [
            {
              "$ref": "#/$defs/source"
            },
            {
              "type": "null"
            }
          ]
        },
        "revision": {
          "oneOf": [
            {
              "$ref": "#/$defs/source"
            },
            {
              "type": "null"
            }
          ]
        },
        "binding": {
          "oneOf": [
            {
              "$ref": "#/$defs/source"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "object_key",
        "root",
        "revision",
        "binding"
      ],
      "additionalProperties": false
    },
    "classification": {
      "type": "object",
      "properties": {
        "object_key": {
          "type": "string",
          "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
        },
        "classification": {
          "enum": [
            "missing",
            "equivalent",
            "drifted",
            "blocked"
          ]
        },
        "desired": {
          "$ref": "#/$defs/canonicalValue"
        },
        "observed": {
          "oneOf": [
            {
              "$ref": "#/$defs/state"
            },
            {
              "type": "null"
            }
          ]
        },
        "blocked_reason": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "object_key",
        "classification",
        "desired",
        "observed",
        "blocked_reason"
      ],
      "additionalProperties": false
    },
    "slot": {
      "type": "object",
      "properties": {
        "request_pointer": {
          "type": "string",
          "pattern": "^/[a-z0-9_/]+$",
          "maxLength": 256
        },
        "object_key": {
          "type": "string",
          "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
        },
        "field": {
          "enum": [
            "root",
            "revision",
            "binding"
          ]
        }
      },
      "required": [
        "request_pointer",
        "object_key",
        "field"
      ],
      "additionalProperties": false
    },
    "action": {
      "type": "object",
      "properties": {
        "ordinal": {
          "type": "string",
          "pattern": "^(0|[1-9][0-9]*)$"
        },
        "action_id": {
          "type": "string",
          "pattern": "^action-[0-9]{6}$"
        },
        "command": {
          "enum": [
            "facet_schema.create",
            "facet_schema.publish",
            "item_archetype.create",
            "item_archetype.facet_binding.set",
            "item_archetype.revise",
            "notification_profile.binding.set",
            "notification_profile.create",
            "notification_profile.metadata.update",
            "notification_profile.revise",
            "notification_rendering_definition.create",
            "notification_rendering_definition.publish"
          ]
        },
        "object_key": {
          "type": "string",
          "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
        },
        "change_kind": {
          "enum": [
            "create",
            "update"
          ]
        },
        "desired": {
          "$ref": "#/$defs/canonicalValue"
        },
        "expected": {
          "oneOf": [
            {
              "$ref": "#/$defs/state"
            },
            {
              "type": "null"
            }
          ]
        },
        "request_template": {
          "$ref": "#/$defs/canonicalValue"
        },
        "slots": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/slot"
          },
          "maxItems": 256
        }
      },
      "required": [
        "ordinal",
        "action_id",
        "command",
        "object_key",
        "change_kind",
        "desired",
        "expected",
        "request_template",
        "slots"
      ],
      "additionalProperties": false
    },
    "receipt": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "family": {
              "const": "catalog"
            },
            "command_receipt_id": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "effect": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "semantic_facts_hash": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            },
            "created_at_utc": {
              "$ref": "#/$defs/utc"
            }
          },
          "required": [
            "family",
            "command_receipt_id",
            "effect",
            "semantic_facts_hash",
            "created_at_utc"
          ],
          "additionalProperties": false
        },
        {
          "type": "object",
          "properties": {
            "family": {
              "const": "facet"
            },
            "command_receipt_id": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "effect": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "changed": {
              "type": "boolean"
            },
            "replayed": {
              "type": "boolean"
            },
            "audit_id": {
              "oneOf": [
                {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 256
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "required": [
            "family",
            "command_receipt_id",
            "effect",
            "changed",
            "replayed",
            "audit_id"
          ],
          "additionalProperties": false
        },
        {
          "type": "object",
          "properties": {
            "family": {
              "const": "rendering"
            },
            "command_receipt_id": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "effect": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "changed": {
              "type": "boolean"
            },
            "replayed": {
              "type": "boolean"
            },
            "audit_id": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            }
          },
          "required": [
            "family",
            "command_receipt_id",
            "effect",
            "changed",
            "replayed",
            "audit_id"
          ],
          "additionalProperties": false
        }
      ]
    },
    "evidence": {
      "type": "object",
      "properties": {
        "action_id": {
          "type": "string",
          "pattern": "^action-[0-9]{6}$"
        },
        "command": {
          "enum": [
            "facet_schema.create",
            "facet_schema.publish",
            "item_archetype.create",
            "item_archetype.facet_binding.set",
            "item_archetype.revise",
            "notification_profile.binding.set",
            "notification_profile.create",
            "notification_profile.metadata.update",
            "notification_profile.revise",
            "notification_rendering_definition.create",
            "notification_rendering_definition.publish"
          ]
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "request": {
          "$ref": "#/$defs/canonicalValue"
        },
        "response": {
          "$ref": "#/$defs/publicResponse"
        },
        "receipt": {
          "$ref": "#/$defs/receipt"
        },
        "post_observation": {
          "$ref": "#/$defs/state"
        }
      },
      "required": [
        "action_id",
        "command",
        "command_id",
        "request",
        "response",
        "receipt",
        "post_observation"
      ],
      "additionalProperties": false
    },
    "unresolved": {
      "type": "object",
      "properties": {
        "action_id": {
          "type": "string",
          "pattern": "^action-[0-9]{6}$"
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "submission_state": {
          "const": "prepared_or_submitted"
        },
        "request": {
          "$ref": "#/$defs/canonicalValue"
        }
      },
      "required": [
        "action_id",
        "command_id",
        "submission_state",
        "request"
      ],
      "additionalProperties": false
    },
    "install-request": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-install-request.v2"
        },
        "request": {
          "$ref": "#/$defs/requestBody"
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-install-request-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "request",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "install-plan": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-install-plan.v2"
        },
        "request_digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "request": {
          "$ref": "#/$defs/requestBody"
        },
        "pack": {
          "$ref": "#/$defs/packIdentity"
        },
        "closure": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
          },
          "maxItems": 1536
        },
        "environment": {
          "$ref": "#/$defs/environment"
        },
        "required_execution_contracts": {
          "const": [
            "spine.archetype-facet-bindings.v1",
            "spine.canonical-json.v1",
            "spine.facet-cursor.v1",
            "spine.facet-schemas.v1",
            "spine.item-archetypes.v1",
            "spine.ledger-instance.v1",
            "spine.notification-profile-bindings.v1",
            "spine.notification-profile-catalog-cursor.v1",
            "spine.notification-profile-metadata-update.v1",
            "spine.notification-profile-readback.v1",
            "spine.notification-profiles.v1",
            "spine.notification-profiles.v2",
            "spine.notification-rendering-cursor.v1",
            "spine.notification-rendering-definitions.v1",
            "spine.notification-rendering-integration.v1",
            "spine.system-info.v3",
            "spine.tickerd-compatibility.v1"
          ]
        },
        "observation": {
          "$ref": "#/$defs/observation"
        },
        "classifications": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/classification"
          },
          "maxItems": 1536
        },
        "resolutions": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/resolution"
          },
          "maxItems": 1536
        },
        "actions": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/action"
          },
          "maxItems": 2048
        },
        "decision_action_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^action-[0-9]{6}$"
          },
          "maxItems": 2048
        },
        "blocked_object_keys": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
          },
          "maxItems": 1536
        },
        "apply_eligible": {
          "type": "boolean"
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-install-plan-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "request_digest",
        "request",
        "pack",
        "closure",
        "environment",
        "required_execution_contracts",
        "observation",
        "classifications",
        "resolutions",
        "actions",
        "decision_action_ids",
        "blocked_object_keys",
        "apply_eligible",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "install-approval": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-install-approval.v2"
        },
        "plan_digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "approve_complete_plan": {
          "const": true
        },
        "acknowledge_single_operator": {
          "const": true
        },
        "authorized_update_action_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^action-[0-9]{6}$"
          },
          "maxItems": 2048
        },
        "execution": {
          "$ref": "#/$defs/execution"
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-install-approval-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "plan_digest",
        "approve_complete_plan",
        "acknowledge_single_operator",
        "authorized_update_action_ids",
        "execution",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "apply-checkpoint": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-apply-checkpoint.v2"
        },
        "plan_digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "approval_digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "execution": {
          "$ref": "#/$defs/execution"
        },
        "accepted_responses": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/evidence"
          },
          "maxItems": 2048
        },
        "unresolved_submission": {
          "oneOf": [
            {
              "$ref": "#/$defs/unresolved"
            },
            {
              "type": "null"
            }
          ]
        },
        "next_action_id": {
          "oneOf": [
            {
              "type": "string",
              "pattern": "^action-[0-9]{6}$"
            },
            {
              "type": "null"
            }
          ]
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-apply-checkpoint-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "plan_digest",
        "approval_digest",
        "execution",
        "accepted_responses",
        "unresolved_submission",
        "next_action_id",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "apply-result": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-apply-result.v2"
        },
        "checkpoint": {
          "$ref": "#/$defs/apply-checkpoint"
        },
        "state": {
          "enum": [
            "applied",
            "partial",
            "not_applied"
          ]
        },
        "failure": {
          "oneOf": [
            {
              "$ref": "#/$defs/applyFailure"
            },
            {
              "type": "null"
            }
          ]
        },
        "unattempted_action_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^action-[0-9]{6}$"
          },
          "maxItems": 2048
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-apply-result-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "checkpoint",
        "state",
        "failure",
        "unattempted_action_ids",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "verification-result": {
      "type": "object",
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-verification-result.v2"
        },
        "plan_digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "apply_result_digest": {
          "oneOf": [
            {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            },
            {
              "type": "null"
            }
          ]
        },
        "pack": {
          "$ref": "#/$defs/packIdentity"
        },
        "target": {
          "$ref": "#/$defs/target"
        },
        "environment": {
          "$ref": "#/$defs/environment"
        },
        "observation": {
          "$ref": "#/$defs/observation"
        },
        "closure": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
          },
          "maxItems": 1536
        },
        "object_results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "object_key": {
                "type": "string",
                "pattern": "^(archetype|schema|rendering|profile|binding):[a-z][a-z0-9_-]{0,63}$|^facet_binding:[a-z][a-z0-9_-]{0,63}:[a-z][a-z0-9_]{0,63}$"
              },
              "state": {
                "enum": [
                  "equivalent",
                  "missing",
                  "drifted",
                  "blocked"
                ]
              },
              "observed": {
                "oneOf": [
                  {
                    "$ref": "#/$defs/state"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            },
            "required": [
              "object_key",
              "state",
              "observed"
            ],
            "additionalProperties": false
          },
          "maxItems": 1536
        },
        "response_evidence": {
          "enum": [
            "complete",
            "not_required",
            "missing",
            "invalid"
          ]
        },
        "receipt_readback": {
          "const": "captured_responses_only_spine_0.9.1"
        },
        "disclosure": {
          "const": "separate_operator_configuration_required"
        },
        "state": {
          "enum": [
            "verified",
            "mismatch"
          ]
        },
        "content_identity": {
          "type": "object",
          "properties": {
            "algorithm": {
              "const": "sha256"
            },
            "canonical_json_version": {
              "const": "spine.canonical-json.v1"
            },
            "derivation_version": {
              "const": "spine.pack-verification-result-digest.v2"
            },
            "digest": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          },
          "required": [
            "algorithm",
            "canonical_json_version",
            "derivation_version",
            "digest"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "artifact_schema",
        "plan_digest",
        "apply_result_digest",
        "pack",
        "target",
        "environment",
        "observation",
        "closure",
        "object_results",
        "response_evidence",
        "receipt_readback",
        "disclosure",
        "state",
        "content_identity"
      ],
      "additionalProperties": false
    },
    "installer-result": {
      "type": "object",
      "required": [
        "artifact_schema",
        "operation",
        "status",
        "exit_code",
        "artifact",
        "error"
      ],
      "properties": {
        "artifact_schema": {
          "const": "spine.pack-installer-result.v2"
        },
        "operation": {
          "enum": [
            "plan",
            "apply",
            "verify"
          ]
        },
        "status": {
          "enum": [
            "success",
            "failed",
            "decision_required",
            "blocked",
            "partial",
            "mismatch"
          ]
        },
        "exit_code": {
          "enum": [
            "0",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11"
          ]
        },
        "artifact": {
          "oneOf": [
            {
              "$ref": "#/$defs/artifactReference"
            },
            {
              "type": "null"
            }
          ]
        },
        "error": {
          "oneOf": [
            {
              "$ref": "#/$defs/error"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 21: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-verification-result.v2.schema.json

Hash: 76493cdd075796fd7ed0957cecb7df80447b4fbb6bfa3bee30b2075281d75c95

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-verification-result.v2.schema.json",
  "$ref": "spine-pack-installer-types.v2.schema.json#/$defs/verification-result"
}
```

### Spec 22: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-readback-0.9.1.schema.json

Hash: 90471d1674233e7b3d47575adf085c4095ddfecc92f1f2e7833f4be56d7d4204

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-readback-0.9.1.schema.json",
  "$comment": "Client-only offline closure at Spine 57cda1c2d5589360ee8efe7155fd20b503034c2a. Public fragments are copied with only $ref relocation and $id/$schema removal. Four legacy write and three legacy read responses use the existing client projections, pending exact-baseline FR-5 qualification. See source inventory; no permission for commands outside that inventory.",
  "$defs": {
    "public_0002": {
      "type": "string",
      "minLength": 1
    },
    "public_0003": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "public_0001": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/public_0002"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/public_0002"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0003"
        }
      }
    },
    "public_0004": {
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
              "$ref": "#/$defs/public_0002"
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
              "$ref": "#/$defs/public_0002"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0005": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "public_0007": {
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
    "public_0006": {
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
          "$ref": "#/$defs/public_0007"
        }
      },
      "additionalProperties": false
    },
    "public_0000": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0001"
        },
        {
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
              "$ref": "#/$defs/public_0004"
            },
            "archetype_key": {
              "$ref": "#/$defs/public_0005"
            },
            "revision": {
              "$ref": "#/$defs/public_0006"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0009": {
      "type": "string",
      "minLength": 1
    },
    "public_0010": {
      "type": "string",
      "pattern": "^[1-9][0-9]*$"
    },
    "public_0011": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "public_0012": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "public_0013": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "public_0008": {
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
          "$ref": "#/$defs/public_0009"
        },
        "item_archetype_revision_id": {
          "$ref": "#/$defs/public_0009"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0010"
        },
        "status": {
          "const": "active"
        },
        "archetype_key": {
          "$ref": "#/$defs/public_0011"
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
              "$ref": "#/$defs/public_0009"
            },
            "command_id": {
              "$ref": "#/$defs/public_0009"
            },
            "effect": {
              "enum": [
                "item_archetype_created"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/public_0012"
            },
            "created_at_utc": {
              "$ref": "#/$defs/public_0013"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "public_0014": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0001"
        },
        {
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
              "$ref": "#/$defs/public_0002"
            },
            "expected_current_revision_id": {
              "$ref": "#/$defs/public_0002"
            },
            "revision": {
              "$ref": "#/$defs/public_0006"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0015": {
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
          "$ref": "#/$defs/public_0009"
        },
        "item_archetype_revision_id": {
          "$ref": "#/$defs/public_0009"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0010"
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
              "$ref": "#/$defs/public_0009"
            },
            "command_id": {
              "$ref": "#/$defs/public_0009"
            },
            "effect": {
              "enum": [
                "item_archetype_revised"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/public_0012"
            },
            "created_at_utc": {
              "$ref": "#/$defs/public_0013"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "public_0017": {
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
    "public_0016": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0001"
        },
        {
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
              "$ref": "#/$defs/public_0002"
            },
            "expected_metadata": {
              "$ref": "#/$defs/public_0017"
            },
            "metadata": {
              "$ref": "#/$defs/public_0017"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0018": {
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
          "$ref": "#/$defs/public_0009"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/public_0009"
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
              "$ref": "#/$defs/public_0009"
            },
            "command_id": {
              "$ref": "#/$defs/public_0009"
            },
            "effect": {
              "enum": [
                "notification_profile_metadata_updated",
                "notification_profile_metadata_update_noop"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/public_0012"
            },
            "created_at_utc": {
              "$ref": "#/$defs/public_0013"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "public_0019": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0001"
        },
        {
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
              "$ref": "#/$defs/public_0004"
            },
            "item_archetype_id": {
              "$ref": "#/$defs/public_0002"
            },
            "notification_profile_id": {
              "$ref": "#/$defs/public_0002"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0021": {
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
    "public_0020": {
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
          "$ref": "#/$defs/public_0009"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0009"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/public_0009"
        },
        "status": {
          "const": "active"
        },
        "compatible_item_types": {
          "$ref": "#/$defs/public_0021"
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
              "$ref": "#/$defs/public_0009"
            },
            "command_id": {
              "$ref": "#/$defs/public_0009"
            },
            "effect": {
              "enum": [
                "notification_profile_binding_set",
                "notification_profile_binding_set_noop"
              ]
            },
            "semantic_facts_hash": {
              "$ref": "#/$defs/public_0012"
            },
            "created_at_utc": {
              "$ref": "#/$defs/public_0013"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "public_0023": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc"
      ],
      "properties": {
        "command_id": {
          "$ref": "#/$defs/public_0002"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/public_0002"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0003"
        }
      }
    },
    "public_0024": {
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
              "$ref": "#/$defs/public_0002"
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
              "$ref": "#/$defs/public_0002"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0025": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}(?![\\s\\S])"
    },
    "public_0027": {
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
    "public_0032": {
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
          "$ref": "#/$defs/public_0003"
        }
      },
      "additionalProperties": false
    },
    "public_0035": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)$"
    },
    "public_0034": {
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
          "$ref": "#/$defs/public_0035"
        }
      },
      "additionalProperties": false
    },
    "public_0037": {
      "type": "string",
      "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
    },
    "public_0036": {
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
          "$ref": "#/$defs/public_0035"
        },
        "local_time": {
          "$ref": "#/$defs/public_0037"
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
    "public_0033": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0034"
        },
        {
          "$ref": "#/$defs/public_0036"
        }
      ]
    },
    "public_0031": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0032"
        },
        {
          "$ref": "#/$defs/public_0033"
        }
      ]
    },
    "public_0030": {
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
          "$ref": "#/$defs/public_0031"
        }
      },
      "additionalProperties": false
    },
    "public_0038": {
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
            "$ref": "#/$defs/public_0033"
          }
        }
      },
      "additionalProperties": false
    },
    "public_0042": {
      "type": "string",
      "pattern": "^[1-9][0-9]*$"
    },
    "public_0041": {
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
          "$ref": "#/$defs/public_0042"
        }
      },
      "additionalProperties": false
    },
    "public_0044": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    },
    "public_0045": {
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
    "public_0043": {
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
          "$ref": "#/$defs/public_0042"
        },
        "seed_local_date": {
          "$ref": "#/$defs/public_0044"
        },
        "local_time": {
          "$ref": "#/$defs/public_0037"
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
            "$ref": "#/$defs/public_0045"
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
          "$ref": "#/$defs/public_0045"
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
    "public_0040": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0041"
        },
        {
          "$ref": "#/$defs/public_0043"
        }
      ]
    },
    "public_0039": {
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
          "$ref": "#/$defs/public_0031"
        },
        "stop": {
          "$ref": "#/$defs/public_0031"
        },
        "stop_inclusive": {
          "type": "boolean"
        },
        "cadence": {
          "$ref": "#/$defs/public_0040"
        }
      },
      "additionalProperties": false
    },
    "public_0029": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0030"
        },
        {
          "$ref": "#/$defs/public_0038"
        },
        {
          "$ref": "#/$defs/public_0039"
        }
      ]
    },
    "public_0047": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)$"
    },
    "public_0046": {
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
              "$ref": "#/$defs/public_0047"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0049": {
      "type": "object",
      "required": [
        "notification_rendering_definition_id",
        "notification_rendering_definition_revision_id"
      ],
      "properties": {
        "notification_rendering_definition_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "notification_rendering_definition_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        }
      },
      "additionalProperties": false
    },
    "public_0048": {
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
            "definition"
          ],
          "properties": {
            "kind": {
              "const": "definition"
            },
            "definition": {
              "$ref": "#/$defs/public_0049"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0028": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/public_0025"
        },
        "schedule": {
          "$ref": "#/$defs/public_0029"
        },
        "late_handling": {
          "$ref": "#/$defs/public_0046"
        },
        "rendering": {
          "$ref": "#/$defs/public_0048"
        }
      },
      "additionalProperties": false
    },
    "public_0026": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/public_0027"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/public_0028"
          }
        }
      },
      "additionalProperties": false
    },
    "public_0022": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0023"
        },
        {
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
              "const": "spine.notification-profiles.v2"
            },
            "owner": {
              "$ref": "#/$defs/public_0024"
            },
            "profile_key": {
              "$ref": "#/$defs/public_0025"
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
              "$ref": "#/$defs/public_0026"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0051": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "public_0052": {
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
          "$ref": "#/$defs/public_0002"
        },
        "command_id": {
          "$ref": "#/$defs/public_0002"
        },
        "effect": {
          "enum": [
            "notification_profile_created",
            "notification_profile_revised"
          ]
        },
        "semantic_facts_hash": {
          "$ref": "#/$defs/public_0051"
        },
        "created_at_utc": {
          "$ref": "#/$defs/public_0003"
        }
      },
      "additionalProperties": false
    },
    "public_0050": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_id",
        "notification_profile_revision_id",
        "revision_number",
        "profile_key",
        "status",
        "normalized_revision_hash",
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
          "const": "spine.notification-profiles.v2"
        },
        "effect": {
          "const": "notification_profile_created"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/public_0002"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/public_0002"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0042"
        },
        "profile_key": {
          "$ref": "#/$defs/public_0005"
        },
        "status": {
          "const": "active"
        },
        "normalized_revision_hash": {
          "$ref": "#/$defs/public_0051"
        },
        "receipt": {
          "$ref": "#/$defs/public_0052"
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0053": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0023"
        },
        {
          "type": "object",
          "required": [
            "contract_version",
            "notification_profile_id",
            "expected_current_revision_id",
            "revision"
          ],
          "properties": {
            "contract_version": {
              "const": "spine.notification-profiles.v2"
            },
            "notification_profile_id": {
              "$ref": "#/$defs/public_0002"
            },
            "expected_current_revision_id": {
              "$ref": "#/$defs/public_0002"
            },
            "revision": {
              "$ref": "#/$defs/public_0026"
            }
          }
        }
      ],
      "unevaluatedProperties": false
    },
    "public_0054": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "effect",
        "notification_profile_id",
        "notification_profile_revision_id",
        "revision_number",
        "status",
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
          "const": "spine.notification-profiles.v2"
        },
        "effect": {
          "const": "notification_profile_revised"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/public_0002"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/public_0002"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0042"
        },
        "status": {
          "const": "active"
        },
        "normalized_revision_hash": {
          "$ref": "#/$defs/public_0051"
        },
        "receipt": {
          "$ref": "#/$defs/public_0052"
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0056": {
      "$ref": "#/$defs/public_0002"
    },
    "public_0057": {
      "$ref": "#/$defs/public_0004"
    },
    "public_0058": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]{0,63}(?![\\s\\S])"
    },
    "public_0061": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)(?![\\s\\S])",
      "maxLength": 20,
      "$comment": "Semantic validation enforces signed 64-bit range."
    },
    "public_0060": {
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
              "$ref": "#/$defs/public_0058"
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
              "$ref": "#/$defs/public_0058"
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
              "$ref": "#/$defs/public_0058"
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
              "$ref": "#/$defs/public_0058"
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
              "$ref": "#/$defs/public_0061"
            },
            "max": {
              "$ref": "#/$defs/public_0061"
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
              "$ref": "#/$defs/public_0058"
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
              "$ref": "#/$defs/public_0058"
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
    "public_0059": {
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
            "$ref": "#/$defs/public_0060"
          },
          "minItems": 1,
          "maxItems": 32
        }
      },
      "additionalProperties": false
    },
    "public_0055": {
      "type": "object",
      "required": [
        "contract_version",
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "owner",
        "schema_key",
        "definition"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.facet-schemas.v1"
        },
        "command_id": {
          "$ref": "#/$defs/public_0056"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/public_0056"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0003"
        },
        "owner": {
          "$ref": "#/$defs/public_0057"
        },
        "schema_key": {
          "$ref": "#/$defs/public_0058"
        },
        "definition": {
          "$ref": "#/$defs/public_0059"
        }
      },
      "additionalProperties": false
    },
    "public_0062": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "ok",
            "command",
            "response_contract",
            "command_id",
            "command_receipt_id",
            "effect",
            "changed",
            "audit_id",
            "facet_schema_id",
            "prior_revision_id",
            "facet_schema_revision_id",
            "revision_number",
            "replayed"
          ],
          "properties": {
            "ok": {
              "const": true
            },
            "command": {
              "const": "facet_schema.create"
            },
            "response_contract": {
              "const": "spine.facet-schemas.v1"
            },
            "command_id": {
              "$ref": "#/$defs/public_0056"
            },
            "command_receipt_id": {
              "$ref": "#/$defs/public_0056"
            },
            "effect": {
              "const": "facet_schema_created"
            },
            "changed": {
              "type": "boolean"
            },
            "audit_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_id": {
              "$ref": "#/$defs/public_0056"
            },
            "prior_revision_id": {
              "type": "null"
            },
            "facet_schema_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "revision_number": {
              "const": "1"
            },
            "replayed": {
              "type": "boolean"
            },
            "dry_run": {
              "const": true
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": {
                "properties": {
                  "replayed": {
                    "const": true
                  }
                }
              },
              "then": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              },
              "else": {
                "properties": {
                  "changed": {
                    "const": true
                  }
                }
              }
            }
          ]
        }
      ]
    },
    "public_0063": {
      "type": "object",
      "required": [
        "contract_version",
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "facet_schema_id",
        "expected_current_revision_id",
        "definition"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.facet-schemas.v1"
        },
        "command_id": {
          "$ref": "#/$defs/public_0056"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/public_0056"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0003"
        },
        "facet_schema_id": {
          "$ref": "#/$defs/public_0056"
        },
        "expected_current_revision_id": {
          "$ref": "#/$defs/public_0056"
        },
        "definition": {
          "$ref": "#/$defs/public_0059"
        }
      },
      "additionalProperties": false
    },
    "public_0065": {
      "type": "string",
      "pattern": "^[1-9][0-9]*(?![\\s\\S])"
    },
    "public_0064": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "ok",
            "command",
            "response_contract",
            "command_id",
            "command_receipt_id",
            "effect",
            "changed",
            "audit_id",
            "facet_schema_id",
            "prior_revision_id",
            "facet_schema_revision_id",
            "revision_number",
            "replayed"
          ],
          "properties": {
            "ok": {
              "const": true
            },
            "command": {
              "const": "facet_schema.publish"
            },
            "response_contract": {
              "const": "spine.facet-schemas.v1"
            },
            "command_id": {
              "$ref": "#/$defs/public_0056"
            },
            "command_receipt_id": {
              "$ref": "#/$defs/public_0056"
            },
            "effect": {
              "const": "facet_schema_published"
            },
            "changed": {
              "type": "boolean"
            },
            "audit_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_id": {
              "$ref": "#/$defs/public_0056"
            },
            "prior_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "revision_number": {
              "$ref": "#/$defs/public_0065"
            },
            "replayed": {
              "type": "boolean"
            },
            "dry_run": {
              "const": true
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": {
                "properties": {
                  "replayed": {
                    "const": true
                  }
                }
              },
              "then": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              },
              "else": {
                "properties": {
                  "changed": {
                    "const": true
                  }
                }
              }
            }
          ]
        },
        {
          "type": "object",
          "required": [
            "ok",
            "command",
            "response_contract",
            "command_id",
            "command_receipt_id",
            "effect",
            "changed",
            "facet_schema_id",
            "prior_revision_id",
            "facet_schema_revision_id",
            "revision_number",
            "replayed"
          ],
          "properties": {
            "ok": {
              "const": true
            },
            "command": {
              "const": "facet_schema.publish"
            },
            "response_contract": {
              "const": "spine.facet-schemas.v1"
            },
            "command_id": {
              "$ref": "#/$defs/public_0056"
            },
            "command_receipt_id": {
              "$ref": "#/$defs/public_0056"
            },
            "effect": {
              "const": "facet_schema_publish_noop"
            },
            "changed": {
              "type": "boolean"
            },
            "facet_schema_id": {
              "$ref": "#/$defs/public_0056"
            },
            "prior_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "revision_number": {
              "$ref": "#/$defs/public_0065"
            },
            "replayed": {
              "type": "boolean"
            },
            "dry_run": {
              "const": true
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": {
                "properties": {
                  "replayed": {
                    "const": true
                  }
                }
              },
              "then": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              },
              "else": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              }
            }
          ]
        }
      ]
    },
    "public_0066": {
      "type": "object",
      "required": [
        "contract_version",
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "item_archetype_id",
        "facet_key",
        "facet_schema_revision_id",
        "expected_binding_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.archetype-facet-bindings.v1"
        },
        "command_id": {
          "$ref": "#/$defs/public_0056"
        },
        "actor_subject_id": {
          "$ref": "#/$defs/public_0056"
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0003"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0056"
        },
        "facet_key": {
          "$ref": "#/$defs/public_0058"
        },
        "facet_schema_revision_id": {
          "$ref": "#/$defs/public_0056"
        },
        "expected_binding_id": {
          "anyOf": [
            {
              "$ref": "#/$defs/public_0056"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "public_0067": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "ok",
            "command",
            "response_contract",
            "command_id",
            "command_receipt_id",
            "effect",
            "changed",
            "audit_id",
            "item_archetype_id",
            "facet_key",
            "prior_binding_id",
            "facet_binding_id",
            "facet_schema_revision_id",
            "replayed"
          ],
          "properties": {
            "ok": {
              "const": true
            },
            "command": {
              "const": "item_archetype.facet_binding.set"
            },
            "response_contract": {
              "const": "spine.archetype-facet-bindings.v1"
            },
            "command_id": {
              "$ref": "#/$defs/public_0056"
            },
            "command_receipt_id": {
              "$ref": "#/$defs/public_0056"
            },
            "effect": {
              "const": "facet_binding_set"
            },
            "changed": {
              "type": "boolean"
            },
            "audit_id": {
              "$ref": "#/$defs/public_0056"
            },
            "item_archetype_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_key": {
              "$ref": "#/$defs/public_0058"
            },
            "prior_binding_id": {
              "anyOf": [
                {
                  "$ref": "#/$defs/public_0056"
                },
                {
                  "type": "null"
                }
              ]
            },
            "facet_binding_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "replayed": {
              "type": "boolean"
            },
            "dry_run": {
              "const": true
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": {
                "properties": {
                  "replayed": {
                    "const": true
                  }
                }
              },
              "then": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              },
              "else": {
                "properties": {
                  "changed": {
                    "const": true
                  }
                }
              }
            }
          ]
        },
        {
          "type": "object",
          "required": [
            "ok",
            "command",
            "response_contract",
            "command_id",
            "command_receipt_id",
            "effect",
            "changed",
            "item_archetype_id",
            "facet_key",
            "prior_binding_id",
            "facet_binding_id",
            "facet_schema_revision_id",
            "replayed"
          ],
          "properties": {
            "ok": {
              "const": true
            },
            "command": {
              "const": "item_archetype.facet_binding.set"
            },
            "response_contract": {
              "const": "spine.archetype-facet-bindings.v1"
            },
            "command_id": {
              "$ref": "#/$defs/public_0056"
            },
            "command_receipt_id": {
              "$ref": "#/$defs/public_0056"
            },
            "effect": {
              "const": "facet_binding_set_noop"
            },
            "changed": {
              "type": "boolean"
            },
            "item_archetype_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_key": {
              "$ref": "#/$defs/public_0058"
            },
            "prior_binding_id": {
              "anyOf": [
                {
                  "$ref": "#/$defs/public_0056"
                },
                {
                  "type": "null"
                }
              ]
            },
            "facet_binding_id": {
              "$ref": "#/$defs/public_0056"
            },
            "facet_schema_revision_id": {
              "$ref": "#/$defs/public_0056"
            },
            "replayed": {
              "type": "boolean"
            },
            "dry_run": {
              "const": true
            }
          },
          "additionalProperties": false,
          "allOf": [
            {
              "if": {
                "properties": {
                  "replayed": {
                    "const": true
                  }
                }
              },
              "then": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              },
              "else": {
                "properties": {
                  "changed": {
                    "const": false
                  }
                }
              }
            }
          ]
        }
      ]
    },
    "public_0069": {
      "type": "string",
      "format": "date-time",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "public_0070": {
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
              "type": "string",
              "minLength": 1,
              "maxLength": 256
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
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0072": {
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
    "public_0071": {
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
            "$ref": "#/$defs/public_0072"
          }
        }
      },
      "additionalProperties": false
    },
    "public_0068": {
      "type": "object",
      "required": [
        "contract_version",
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "owner",
        "definition_key",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "actor_subject_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0069"
        },
        "owner": {
          "$ref": "#/$defs/public_0070"
        },
        "definition_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "revision": {
          "$ref": "#/$defs/public_0071"
        }
      },
      "additionalProperties": false
    },
    "public_0075": {
      "type": "object",
      "required": [
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc"
      ],
      "properties": {
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "actor_subject_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0069"
        }
      },
      "additionalProperties": false
    },
    "public_0074": {
      "type": "object",
      "required": [
        "notification_rendering_definition_id",
        "owner",
        "definition_key",
        "status",
        "current_revision_id",
        "notification_rendering_definition_revision_id",
        "revision_number",
        "revision",
        "definition_hash",
        "created",
        "published",
        "retired"
      ],
      "properties": {
        "notification_rendering_definition_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "owner": {
          "$ref": "#/$defs/public_0070"
        },
        "definition_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "current_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "notification_rendering_definition_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "revision_number": {
          "type": "string",
          "pattern": "^[1-9][0-9]{0,18}$"
        },
        "revision": {
          "$ref": "#/$defs/public_0071"
        },
        "definition_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "created": {
          "$ref": "#/$defs/public_0075"
        },
        "published": {
          "$ref": "#/$defs/public_0075"
        },
        "retired": {
          "oneOf": [
            {
              "type": "null"
            },
            {
              "type": "object",
              "required": [
                "reason_code",
                "provenance"
              ],
              "properties": {
                "reason_code": {
                  "type": "string",
                  "pattern": "^[a-z][a-z0-9_-]{0,63}$"
                },
                "provenance": {
                  "$ref": "#/$defs/public_0075"
                }
              },
              "additionalProperties": false
            }
          ]
        }
      },
      "additionalProperties": false
    },
    "public_0073": {
      "type": "object",
      "required": [
        "ok",
        "contract_version",
        "command",
        "command_id",
        "changed",
        "replayed",
        "effect",
        "command_receipt_id",
        "audit_id",
        "record"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command": {
          "const": "notification_rendering_definition.create"
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "changed": {
          "type": "boolean"
        },
        "replayed": {
          "type": "boolean"
        },
        "dry_run": {
          "const": true
        },
        "effect": {
          "enum": [
            "rendering_definition_created"
          ]
        },
        "command_receipt_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "audit_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "record": {
          "$ref": "#/$defs/public_0074"
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "replayed": {
                "const": true
              }
            },
            "required": [
              "replayed"
            ]
          },
          "then": {
            "properties": {
              "changed": {
                "const": false
              }
            }
          },
          "else": {
            "properties": {
              "changed": {
                "const": true
              }
            }
          }
        }
      ]
    },
    "public_0076": {
      "type": "object",
      "required": [
        "contract_version",
        "command_id",
        "actor_subject_id",
        "action_timestamp_utc",
        "notification_rendering_definition_id",
        "expected_current_revision_id",
        "revision"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "actor_subject_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "action_timestamp_utc": {
          "$ref": "#/$defs/public_0069"
        },
        "notification_rendering_definition_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "expected_current_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "revision": {
          "$ref": "#/$defs/public_0071"
        }
      },
      "additionalProperties": false
    },
    "public_0077": {
      "type": "object",
      "required": [
        "ok",
        "contract_version",
        "command",
        "command_id",
        "changed",
        "replayed",
        "effect",
        "command_receipt_id",
        "audit_id",
        "record"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command": {
          "const": "notification_rendering_definition.publish"
        },
        "command_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "changed": {
          "type": "boolean"
        },
        "replayed": {
          "type": "boolean"
        },
        "dry_run": {
          "const": true
        },
        "effect": {
          "enum": [
            "rendering_definition_published",
            "rendering_definition_publish_noop"
          ]
        },
        "command_receipt_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "audit_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "record": {
          "$ref": "#/$defs/public_0074"
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "replayed": {
                "const": true
              }
            },
            "required": [
              "replayed"
            ]
          },
          "then": {
            "properties": {
              "changed": {
                "const": false
              }
            }
          },
          "else": {
            "if": {
              "properties": {
                "effect": {
                  "enum": [
                    "rendering_definition_publish_noop"
                  ]
                }
              },
              "required": [
                "effect"
              ]
            },
            "then": {
              "properties": {
                "changed": {
                  "const": false
                }
              }
            },
            "else": {
              "properties": {
                "changed": {
                  "const": true
                }
              }
            }
          }
        }
      ]
    },
    "public_0078": {
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
          "$ref": "#/$defs/public_0004"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        },
        "limit": {
          "type": "string",
          "pattern": "^([1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)$"
        }
      },
      "additionalProperties": false
    },
    "public_0081": {
      "type": "string",
      "minLength": 1
    },
    "public_0083": {
      "type": "string",
      "minLength": 1,
      "maxLength": 160
    },
    "public_0084": {
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
    "public_0082": {
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
          "$ref": "#/$defs/public_0081"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0081"
        },
        "revision_number": {
          "type": "integer",
          "minimum": 1
        },
        "created_by_subject_id": {
          "$ref": "#/$defs/public_0081"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/public_0081"
        },
        "created_at_utc": {
          "$ref": "#/$defs/public_0013"
        },
        "display_name": {
          "$ref": "#/$defs/public_0083"
        },
        "description": {
          "$ref": "#/$defs/public_0084"
        },
        "compatible_item_types": {
          "$ref": "#/$defs/public_0021"
        },
        "normalized_content_hash": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    },
    "public_0080": {
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
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "owner_group_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
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
          "$ref": "#/$defs/public_0081"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/public_0081"
        },
        "created_at_utc": {
          "$ref": "#/$defs/public_0013"
        },
        "retired_by_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_by_command_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_at_utc": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0013"
            },
            {
              "type": "null"
            }
          ]
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0081"
        },
        "archetype_key": {
          "$ref": "#/$defs/public_0011"
        },
        "current_revision_id": {
          "$ref": "#/$defs/public_0081"
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
          "$ref": "#/$defs/public_0082"
        }
      },
      "additionalProperties": false
    },
    "public_0079": {
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
            "$ref": "#/$defs/public_0080"
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
    "public_0085": {
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
          "$ref": "#/$defs/public_0002"
        },
        "item_archetype_revision_id": {
          "$ref": "#/$defs/public_0002"
        }
      },
      "additionalProperties": false
    },
    "public_0086": {
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
          "$ref": "#/$defs/public_0080"
        }
      },
      "additionalProperties": false
    },
    "public_0087": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "limit"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profile-bindings.v1"
        },
        "owner": {
          "$ref": "#/$defs/public_0004"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0002"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        },
        "limit": {
          "type": "string",
          "pattern": "^([1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)$"
        }
      },
      "additionalProperties": false
    },
    "public_0089": {
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
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "owner_group_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
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
          "$ref": "#/$defs/public_0081"
        },
        "created_by_command_id": {
          "$ref": "#/$defs/public_0081"
        },
        "created_at_utc": {
          "$ref": "#/$defs/public_0013"
        },
        "retired_by_subject_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_by_command_id": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0081"
            },
            {
              "type": "null"
            }
          ]
        },
        "retired_at_utc": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0013"
            },
            {
              "type": "null"
            }
          ]
        },
        "notification_profile_binding_id": {
          "$ref": "#/$defs/public_0081"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0081"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/public_0081"
        }
      },
      "additionalProperties": false
    },
    "public_0088": {
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
            "$ref": "#/$defs/public_0089"
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
    "public_0090": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "limit"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v2"
        },
        "owner": {
          "$ref": "#/$defs/public_0024"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "cursor": {
          "type": "string",
          "minLength": 1
        },
        "limit": {
          "type": "string",
          "pattern": "^([1-9]|[1-9][0-9]|[1-4][0-9]{2}|500)(?![\\s\\S])"
        }
      },
      "additionalProperties": false
    },
    "public_0094": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/public_0007"
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
              "normalized_template_hash"
            ],
            "properties": {
              "template_key": {
                "$ref": "#/$defs/public_0005"
              },
              "schedule": {
                "$ref": "#/$defs/public_0029"
              },
              "late_handling": {
                "$ref": "#/$defs/public_0046"
              },
              "normalized_template_hash": {
                "$ref": "#/$defs/public_0051"
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },
    "public_0095": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/public_0007"
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
                "$ref": "#/$defs/public_0005"
              },
              "schedule": {
                "$ref": "#/$defs/public_0029"
              },
              "late_handling": {
                "$ref": "#/$defs/public_0046"
              },
              "rendering": {
                "$ref": "#/$defs/public_0048"
              },
              "normalized_template_hash": {
                "$ref": "#/$defs/public_0051"
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },
    "public_0093": {
      "type": "object",
      "required": [
        "notification_profile_revision_id",
        "revision_number",
        "revision_contract",
        "normalized_revision_hash",
        "content"
      ],
      "properties": {
        "notification_profile_revision_id": {
          "$ref": "#/$defs/public_0002"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0042"
        },
        "revision_contract": {
          "enum": [
            "spine.notification-profiles.v1",
            "spine.notification-profiles.v2"
          ]
        },
        "normalized_revision_hash": {
          "$ref": "#/$defs/public_0051"
        },
        "content": {
          "oneOf": [
            {
              "$ref": "#/$defs/public_0094"
            },
            {
              "$ref": "#/$defs/public_0095"
            }
          ]
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "revision_contract": {
                "const": "spine.notification-profiles.v2"
              }
            }
          },
          "then": {
            "properties": {
              "content": {
                "$ref": "#/$defs/public_0095"
              }
            }
          },
          "else": {
            "properties": {
              "content": {
                "$ref": "#/$defs/public_0094"
              }
            }
          }
        }
      ]
    },
    "public_0092": {
      "type": "object",
      "required": [
        "notification_profile_id",
        "owner",
        "profile_key",
        "display_name",
        "description",
        "status",
        "current_revision_id",
        "revision"
      ],
      "properties": {
        "notification_profile_id": {
          "$ref": "#/$defs/public_0002"
        },
        "owner": {
          "$ref": "#/$defs/public_0004"
        },
        "profile_key": {
          "$ref": "#/$defs/public_0005"
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
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "current_revision_id": {
          "$ref": "#/$defs/public_0002"
        },
        "revision": {
          "$ref": "#/$defs/public_0093"
        }
      },
      "additionalProperties": false
    },
    "public_0091": {
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
          "const": "spine.notification-profiles.v2"
        },
        "entries": {
          "type": "array",
          "minItems": 0,
          "maxItems": 500,
          "items": {
            "$ref": "#/$defs/public_0092"
          }
        },
        "count": {
          "$ref": "#/$defs/public_0047"
        },
        "catalog_snapshot_hash": {
          "$ref": "#/$defs/public_0051"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            },
            {
              "type": "null"
            }
          ]
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0096": {
      "type": "object",
      "required": [
        "contract_version",
        "notification_profile_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-profiles.v2"
        },
        "notification_profile_id": {
          "$ref": "#/$defs/public_0002"
        },
        "notification_profile_revision_id": {
          "$ref": "#/$defs/public_0002"
        }
      },
      "additionalProperties": false
    },
    "public_0097": {
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
          "const": "spine.notification-profiles.v2"
        },
        "notification_profile": {
          "$ref": "#/$defs/public_0092"
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0099": {
      "type": "string",
      "pattern": "^([1-9]|[1-9][0-9]|100)(?![\\s\\S])",
      "default": "25"
    },
    "public_0100": {
      "type": "string",
      "minLength": 1,
      "maxLength": 4096,
      "$comment": "Opaque spine.facet-cursor.v1 token. Section 11 of specs/archetype-facets.md owns MAC, context, snapshot and expiry semantics; structural string validation alone proves none of them."
    },
    "public_0098": {
      "type": "object",
      "required": [
        "contract_version",
        "owner"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.facet-schemas.v1"
        },
        "owner": {
          "$ref": "#/$defs/public_0057"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "limit": {
          "$ref": "#/$defs/public_0099"
        },
        "cursor": {
          "$ref": "#/$defs/public_0100"
        }
      },
      "additionalProperties": false
    },
    "public_0102": {
      "type": "object",
      "required": [
        "facet_schema_id",
        "owner",
        "schema_key",
        "current_revision_id",
        "status"
      ],
      "properties": {
        "facet_schema_id": {
          "$ref": "#/$defs/public_0056"
        },
        "owner": {
          "$ref": "#/$defs/public_0057"
        },
        "schema_key": {
          "$ref": "#/$defs/public_0058"
        },
        "current_revision_id": {
          "$ref": "#/$defs/public_0056"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        }
      },
      "additionalProperties": false
    },
    "public_0101": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "owner",
        "schemas",
        "limit",
        "has_more",
        "next_cursor"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "facet_schema.list"
        },
        "response_contract": {
          "const": "spine.facet-schemas.v1"
        },
        "owner": {
          "$ref": "#/$defs/public_0057"
        },
        "schemas": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/public_0102"
          },
          "minItems": 0,
          "maxItems": 100
        },
        "limit": {
          "$ref": "#/$defs/public_0099"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "anyOf": [
            {
              "$ref": "#/$defs/public_0100"
            },
            {
              "type": "null"
            }
          ]
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "has_more": {
                "const": true
              }
            }
          },
          "then": {
            "properties": {
              "next_cursor": {
                "$ref": "#/$defs/public_0100"
              }
            }
          },
          "else": {
            "properties": {
              "next_cursor": {
                "type": "null"
              }
            }
          }
        }
      ]
    },
    "public_0103": {
      "type": "object",
      "required": [
        "contract_version",
        "facet_schema_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.facet-schemas.v1"
        },
        "facet_schema_id": {
          "$ref": "#/$defs/public_0056"
        },
        "facet_schema_revision_id": {
          "$ref": "#/$defs/public_0056"
        }
      },
      "additionalProperties": false
    },
    "public_0106": {
      "allOf": [
        {
          "$ref": "#/$defs/public_0059"
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
    },
    "public_0107": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}(?![\\s\\S])"
    },
    "public_0105": {
      "type": "object",
      "required": [
        "facet_schema_id",
        "facet_schema_revision_id",
        "revision_number",
        "definition",
        "definition_hash"
      ],
      "properties": {
        "facet_schema_id": {
          "$ref": "#/$defs/public_0056"
        },
        "facet_schema_revision_id": {
          "$ref": "#/$defs/public_0056"
        },
        "revision_number": {
          "$ref": "#/$defs/public_0065"
        },
        "definition": {
          "$ref": "#/$defs/public_0106"
        },
        "definition_hash": {
          "$ref": "#/$defs/public_0107"
        }
      },
      "additionalProperties": false
    },
    "public_0104": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "root",
        "revision"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "facet_schema.show"
        },
        "response_contract": {
          "const": "spine.facet-schemas.v1"
        },
        "root": {
          "$ref": "#/$defs/public_0102"
        },
        "revision": {
          "$ref": "#/$defs/public_0105"
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0108": {
      "type": "object",
      "required": [
        "contract_version",
        "item_archetype_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.archetype-facet-bindings.v1"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0056"
        },
        "limit": {
          "$ref": "#/$defs/public_0099"
        },
        "cursor": {
          "$ref": "#/$defs/public_0100"
        }
      },
      "additionalProperties": false
    },
    "public_0110": {
      "type": "object",
      "required": [
        "facet_binding_id",
        "item_archetype_id",
        "facet_key",
        "facet_schema_revision_id",
        "status"
      ],
      "properties": {
        "facet_binding_id": {
          "$ref": "#/$defs/public_0056"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0056"
        },
        "facet_key": {
          "$ref": "#/$defs/public_0058"
        },
        "facet_schema_revision_id": {
          "$ref": "#/$defs/public_0056"
        },
        "status": {
          "enum": [
            "active",
            "superseded",
            "retired"
          ]
        }
      },
      "additionalProperties": false
    },
    "public_0109": {
      "type": "object",
      "required": [
        "ok",
        "command",
        "response_contract",
        "item_archetype_id",
        "bindings",
        "limit",
        "has_more",
        "next_cursor"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "item_archetype.facet_binding.list"
        },
        "response_contract": {
          "const": "spine.archetype-facet-bindings.v1"
        },
        "item_archetype_id": {
          "$ref": "#/$defs/public_0056"
        },
        "bindings": {
          "type": "array",
          "items": {
            "allOf": [
              {
                "$ref": "#/$defs/public_0110"
              },
              {
                "properties": {
                  "status": {
                    "const": "active"
                  }
                }
              }
            ]
          },
          "minItems": 0,
          "maxItems": 100
        },
        "limit": {
          "$ref": "#/$defs/public_0099"
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "anyOf": [
            {
              "$ref": "#/$defs/public_0100"
            },
            {
              "type": "null"
            }
          ]
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "has_more": {
                "const": true
              }
            }
          },
          "then": {
            "properties": {
              "next_cursor": {
                "$ref": "#/$defs/public_0100"
              }
            }
          },
          "else": {
            "properties": {
              "next_cursor": {
                "type": "null"
              }
            }
          }
        }
      ]
    },
    "public_0111": {
      "type": "object",
      "required": [
        "contract_version",
        "owner",
        "status",
        "limit"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "owner": {
          "$ref": "#/$defs/public_0070"
        },
        "status": {
          "enum": [
            "active",
            "retired"
          ]
        },
        "limit": {
          "type": "string",
          "pattern": "^([1-9]|[1-9][0-9]|100)(?![\\s\\S])"
        },
        "cursor": {
          "type": "string",
          "minLength": 1,
          "maxLength": 4096
        }
      },
      "additionalProperties": false
    },
    "public_0112": {
      "type": "object",
      "required": [
        "ok",
        "contract_version",
        "command",
        "records",
        "has_more",
        "next_cursor",
        "limit"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command": {
          "const": "notification_rendering_definition.list"
        },
        "records": {
          "type": "array",
          "maxItems": 100,
          "items": {
            "$ref": "#/$defs/public_0074"
          }
        },
        "has_more": {
          "type": "boolean"
        },
        "next_cursor": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            },
            {
              "type": "null"
            }
          ]
        },
        "dry_run": {
          "const": true
        },
        "limit": {
          "type": "string",
          "pattern": "^([1-9]|[1-9][0-9]|100)(?![\\s\\S])"
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "has_more": {
                "const": false
              }
            },
            "required": [
              "has_more"
            ]
          },
          "then": {
            "properties": {
              "next_cursor": {
                "type": "null"
              }
            }
          },
          "else": {
            "properties": {
              "next_cursor": {
                "type": "string",
                "minLength": 1,
                "maxLength": 4096
              }
            }
          }
        }
      ]
    },
    "public_0113": {
      "type": "object",
      "required": [
        "contract_version",
        "notification_rendering_definition_id"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "notification_rendering_definition_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "notification_rendering_definition_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        }
      },
      "additionalProperties": false
    },
    "public_0114": {
      "type": "object",
      "required": [
        "ok",
        "contract_version",
        "command",
        "record"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "contract_version": {
          "const": "spine.notification-rendering-definitions.v1"
        },
        "command": {
          "const": "notification_rendering_definition.show"
        },
        "record": {
          "$ref": "#/$defs/public_0074"
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "emptyRequest": {
      "type": "object",
      "properties": {},
      "required": [],
      "additionalProperties": false
    },
    "public_0115": {
      "title": "Spine System Information Response v3",
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
        "runtime_dependencies",
        "ledger_instance_id"
      ],
      "properties": {
        "ok": {
          "const": true
        },
        "command": {
          "const": "system.info"
        },
        "response_contract": {
          "const": "spine.system-info.v3"
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
                "const": "spine.system-info.v3"
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
            },
            {
              "contains": {
                "const": "spine.ledger-instance.v1"
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
        },
        "ledger_instance_id": {
          "type": "string",
          "pattern": "^ledger_instance_[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    },
    "public_0116": {
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
    "public_0123": {
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
          "$ref": "#/$defs/public_0013"
        }
      },
      "additionalProperties": false
    },
    "public_0126": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)$"
    },
    "public_0125": {
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
          "$ref": "#/$defs/public_0126"
        }
      },
      "additionalProperties": false
    },
    "public_0128": {
      "type": "string",
      "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
    },
    "public_0127": {
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
          "$ref": "#/$defs/public_0126"
        },
        "local_time": {
          "$ref": "#/$defs/public_0128"
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
    "public_0124": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0125"
        },
        {
          "$ref": "#/$defs/public_0127"
        }
      ]
    },
    "public_0122": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0123"
        },
        {
          "$ref": "#/$defs/public_0124"
        }
      ]
    },
    "public_0121": {
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
          "$ref": "#/$defs/public_0122"
        }
      },
      "additionalProperties": false
    },
    "public_0129": {
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
            "$ref": "#/$defs/public_0124"
          }
        }
      },
      "additionalProperties": false
    },
    "public_0132": {
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
          "$ref": "#/$defs/public_0010"
        }
      },
      "additionalProperties": false
    },
    "public_0134": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    },
    "public_0135": {
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
    "public_0133": {
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
          "$ref": "#/$defs/public_0010"
        },
        "seed_local_date": {
          "$ref": "#/$defs/public_0134"
        },
        "local_time": {
          "$ref": "#/$defs/public_0128"
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
            "$ref": "#/$defs/public_0135"
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
          "$ref": "#/$defs/public_0135"
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
    "public_0131": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0132"
        },
        {
          "$ref": "#/$defs/public_0133"
        }
      ]
    },
    "public_0130": {
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
          "$ref": "#/$defs/public_0122"
        },
        "stop": {
          "$ref": "#/$defs/public_0122"
        },
        "stop_inclusive": {
          "type": "boolean"
        },
        "cadence": {
          "$ref": "#/$defs/public_0131"
        }
      },
      "additionalProperties": false
    },
    "public_0120": {
      "oneOf": [
        {
          "$ref": "#/$defs/public_0121"
        },
        {
          "$ref": "#/$defs/public_0129"
        },
        {
          "$ref": "#/$defs/public_0130"
        }
      ]
    },
    "public_0137": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)$"
    },
    "public_0136": {
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
              "$ref": "#/$defs/public_0137"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "public_0119": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/public_0011"
        },
        "schedule": {
          "$ref": "#/$defs/public_0120"
        },
        "late_handling": {
          "$ref": "#/$defs/public_0136"
        }
      },
      "additionalProperties": false
    },
    "public_0118": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/public_0021"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/public_0119"
          }
        }
      },
      "additionalProperties": false
    },
    "public_0117": {
      "type": "object",
      "required": [
        "metadata",
        "revision"
      ],
      "properties": {
        "metadata": {
          "$ref": "#/$defs/public_0116"
        },
        "revision": {
          "$ref": "#/$defs/public_0118"
        }
      },
      "additionalProperties": false
    },
    "semantic_archetype": {
      "$ref": "#/$defs/public_0006"
    },
    "semantic_schema": {
      "$ref": "#/$defs/public_0106"
    },
    "semantic_rendering": {
      "$ref": "#/$defs/public_0071"
    },
    "semantic_profile": {
      "type": "object",
      "properties": {
        "metadata": {
          "$ref": "#/$defs/public_0116"
        },
        "revision": {
          "$ref": "#/$defs/public_0026"
        }
      },
      "required": [
        "metadata",
        "revision"
      ],
      "additionalProperties": false
    },
    "semantic_profile_v1": {
      "$ref": "#/$defs/public_0117"
    },
    "semantic_facet_binding": {
      "type": "object",
      "properties": {
        "item_archetype_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "facet_key": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "facet_schema_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        }
      },
      "required": [
        "item_archetype_id",
        "facet_key",
        "facet_schema_revision_id"
      ],
      "additionalProperties": false
    },
    "semantic_binding": {
      "type": "object",
      "properties": {
        "item_archetype_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "notification_profile_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        }
      },
      "required": [
        "item_archetype_id",
        "notification_profile_id"
      ],
      "additionalProperties": false
    },
    "public_0138": {
      "title": "Spine facet handler failures (draft v1)",
      "$comment": "Draft, not implemented or advertised. Normative source: specs/archetype-facets.md.",
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
          "enum": [
            "facet_schema.create",
            "facet_schema.publish",
            "facet_schema.retire",
            "facet_schema.show",
            "facet_schema.list",
            "item_archetype.facet_binding.set",
            "item_archetype.facet_binding.remove",
            "item_archetype.facet_binding.list",
            "item.facets.update",
            "item.facets.show",
            "item.facets.query"
          ]
        },
        "error": {
          "type": "object",
          "required": [
            "code",
            "message"
          ],
          "properties": {
            "code": {
              "enum": [
                "facet_schema_invalid",
                "facet_value_invalid",
                "facet_binding_conflict",
                "facet_archetype_conflict",
                "facet_schema_retired",
                "facet_reference_unavailable",
                "invalid_request",
                "unsupported_field",
                "missing_required_field",
                "invalid_timestamp",
                "referenced_row_not_found",
                "wrong_item_type",
                "stale_version",
                "stale_cursor",
                "invalid_state_transition",
                "semantic_conflict",
                "environment_failure",
                "runtime_failure"
              ]
            },
            "message": {
              "type": "string",
              "minLength": 1
            },
            "field": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        },
        "dry_run": {
          "const": true
        }
      },
      "additionalProperties": false
    },
    "public_0139": {
      "title": "Rendering integration standard command failure (source only)",
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
          "enum": [
            "notification_profile.create",
            "notification_profile.revise",
            "notification_profile.show",
            "notification_profile.list",
            "schedule.create",
            "schedule.update",
            "schedule.show",
            "reminder.create",
            "reminder.edit"
          ]
        },
        "dry_run": {
          "const": true
        },
        "error": {
          "type": "object",
          "required": [
            "code",
            "message"
          ],
          "properties": {
            "code": {
              "enum": [
                "invalid_request",
                "unsupported_field",
                "missing_required_field",
                "invalid_timestamp",
                "referenced_row_not_found",
                "semantic_conflict",
                "stale_version",
                "stale_cursor",
                "permission_denied",
                "environment_failure",
                "runtime_failure",
                "rendering_definition_invalid",
                "rendering_definition_retired",
                "rendering_disclosure_unavailable",
                "rendering_disclosure_ambiguous",
                "rendering_disclosure_scope_mismatch"
              ]
            },
            "message": {
              "type": "string",
              "minLength": 1
            },
            "field": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "public_0140": {
      "title": "Spine notification-rendering-cursor-config (source only)",
      "type": "object",
      "required": [
        "contract_version",
        "key_id",
        "key_generation",
        "ledger_instance_id",
        "secret_hex"
      ],
      "properties": {
        "contract_version": {
          "const": "spine.notification-rendering-cursor-config.v1"
        },
        "key_id": {
          "type": "string",
          "pattern": "^[A-Za-z0-9_-]{1,64}(?![\\s\\S])"
        },
        "key_generation": {
          "type": "string",
          "pattern": "^[A-Za-z0-9_-]{1,64}(?![\\s\\S])"
        },
        "ledger_instance_id": {
          "$ref": "#/$defs/public_0002"
        },
        "secret_hex": {
          "type": "string",
          "minLength": 64,
          "maxLength": 128,
          "pattern": "^(?:[0-9a-f]{2}){32,64}(?![\\s\\S])"
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 23: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_facet_manifest_contract.py

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

### Spec 24: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/facet_artifact_oracle.py

Hash: 7ba9de980c43c0fdf35ddc57746885e4765a174a426c07f07090de8c6ae004bd

```markdown
"""Independent FR-1 artifact oracle. No transport, filesystem writes or Spine imports.

This is executable contract evidence, not the successor installer implementation.
"""
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import re

from test_facet_manifest_contract import ROOT, canonical, load, require, ordered, validate as validate_manifest

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    Draft202012Validator = None

SCHEMAS = ROOT / 'contracts/schemas'
INVENTORY = load(ROOT / 'contracts/installer-spine-0.9.1-inventory.json')
COMMANDS = INVENTORY['commands']
LIMITS = dict(zip(('install-request', 'install-plan', 'install-approval', 'apply-checkpoint',
                   'apply-result', 'verification-result', 'installer-result'),
                  (65536, 8388608, 262144, 16777216, 16777216, 16777216, 1048576)))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def hash_value(value):
    return sha(canonical(value))


def blob(value):
    text = canonical(value).decode()
    return {'canonical_json': text, 'digest': sha(text.encode())}


def parse(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON member')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON number')
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)
    def unicode_check(v):
        if isinstance(v, str):
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in v), 'invalid Unicode')
        elif isinstance(v, dict):
            for k, x in v.items():
                unicode_check(k)
                unicode_check(x)
        elif isinstance(v, list):
            for x in v:
                unicode_check(x)
    unicode_check(value)
    return value


def unblob(value, public=False):
    text = value['json_text' if public else 'canonical_json']
    require(sha(text.encode()) == value['digest'], 'embedded digest')
    decoded = parse(text)
    if not public:
        require(canonical(decoded).decode() == text, 'noncanonical embedded value')
    return decoded


def seal(value):
    value = deepcopy(value)
    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
    value['content_identity'] = {'algorithm': 'sha256', 'canonical_json_version': 'spine.canonical-json.v1',
                                 'derivation_version': 'spine.pack-' + kind + '-digest.v2'}
    value['content_identity']['digest'] = hash_value(value)
    return value


@lru_cache(maxsize=None)
def validator(filename, definition=None):
    resources = [(s['$id'], Resource.from_contents(s)) for p in SCHEMAS.glob('*.json')
                 if '$id' in (s := load(p))]
    registry = Registry().with_resources(resources)
    schema = load(SCHEMAS / filename)
    if definition:
        schema = {'$ref': schema['$id'] + '#/$defs/' + definition}
    return Draft202012Validator(schema, registry=registry)


def public_schema(command, direction, value):
    validator('spine-readback-0.9.1.schema.json', COMMANDS[command][direction]).validate(value)


def artifact(value):
    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
    require(kind in LIMITS and value['artifact_schema'].endswith('.v2'), 'artifact version')
    require(len(canonical(value)) <= LIMITS[kind], 'artifact size')
    validator('spine-pack-' + kind + '.v2.schema.json').validate(value)
    if kind != 'installer-result':
        require(value == seal(value), 'artifact digest')
    else:
        mapping={'0':('success',None),'2':('failed','invalid_cli_or_artifact_input'),
                 '3':('failed','invalid_pack_contract_or_digest'),'4':('failed','incompatible_spine_runtime_or_contracts'),
                 '5':('decision_required','decision_required_for_drift'),'6':('blocked','blocked_desired_state'),
                 '7':('failed','stale_plan_or_target_mismatch'),'8':('failed','spine_command_rejection'),
                 '9':('partial','partial_apply'),'10':('mismatch','verification_mismatch'),
                 '11':('failed','transport_or_environment_failure')}
        status,category=mapping[value['exit_code']]
        require(value['status']==status and (value['error']['category'] if value['error'] else None)==category,'exit/category correlation')
        if value['exit_code'] in ('0','5','6','9','10'): require(value['artifact'] is not None,'required output artifact')


def pointer(value, path, replacement=None, write=False):
    parts = path.split('/')[1:]
    for p in parts[:-1]:
        value = value[int(p)] if isinstance(value, list) else value[p]
    p = int(parts[-1]) if isinstance(value, list) else parts[-1]
    if write:
        value[p] = replacement
    else:
        return value[p]


def command_id(plan, approval, action):
    return 'spack_' + hash_value({'action_id': action['action_id'], 'derivation_version': 'spine.pack-command-id.v2',
                                 'execution_id': approval['execution']['execution_id'],
                                 'plan_digest': plan['content_identity']['digest']})


def manifest_objects(manifest):
    result = {}
    for family, array, key in [('archetype', 'archetypes', 'archetype_key'), ('schema', 'facet_schemas', 'schema_key'),
                                ('rendering', 'rendering_definitions', 'definition_key'),
                                ('profile', 'notification_profiles', 'profile_key'), ('binding', 'binding_intents', 'archetype_key')]:
        for item in manifest[array]:
            result[family + ':' + item[key]] = item
    for item in manifest['archetype_facet_bindings']:
        result['facet_binding:' + item['archetype_key'] + ':' + item['facet_key']] = item
    return result


def closure(manifest, selection):
    objects = manifest_objects(manifest)
    if selection['mode'] == 'all':
        return sorted(objects)
    selected = set()
    def visit(key):
        require(key in objects, 'missing local object')
        if key in selected:
            return
        selected.add(key)
        obj = objects[key]
        if key.startswith('archetype:'):
            default = 'binding:' + obj['archetype_key']
            if default in objects:
                visit(default)
            for k in objects:
                if k.startswith('facet_binding:' + obj['archetype_key'] + ':'):
                    visit(k)
        elif key.startswith('binding:'):
            visit('profile:' + obj['notification_profile_key'])
        elif key.startswith('facet_binding:'):
            visit('schema:' + obj['schema_ref']['schema_key'])
        elif key.startswith('profile:'):
            for t in obj['revision']['templates']:
                if t['rendering']['kind'] == 'definition':
                    visit('rendering:' + t['rendering']['definition_ref']['definition_key'])
        elif key.startswith('rendering:'):
            for s in obj['revision']['selections']:
                visit('schema:' + s['schema_ref']['schema_key'])
    for key in selection['archetype_keys']:
        visit('archetype:' + key)
    return sorted(selected)


def observation_digest(view):
    return hash_value({'derivation_version': 'spine.pack-observation.v2',
                       'view': {k: v for k, v in view.items() if k != 'digest'}})


def public_snapshots(entries):
    """Only the three pinned legacy public fingerprints; no new-catalog hash."""
    rows = {'archetypes': [], 'profiles': [], 'bindings': []}
    for r in entries:
        family, key = r['object_key'].split(':',1)
        if family in ('archetype','profile'):
            row = {'id':r['root_id'],'key':key,'status':r['status'],'current_revision_id':r['revision_id']}
            if family=='profile': row.update(unblob(r['value'])['metadata'])
            rows['archetypes' if family=='archetype' else 'profiles'].append(row)
        elif family=='binding' and r['status']=='active':
            rows['bindings'].append(dict(unblob(r['value']), notification_profile_binding_id=r['binding_id'],status='active'))
    for key in ('archetypes','profiles'): rows[key].sort(key=lambda r:(r['key'],r['id']))
    rows['bindings'].sort(key=lambda r:(r['item_archetype_id'],r['notification_profile_binding_id']))
    return [{'catalog':k,'digest':hash_value(rows[k])} for k in ('archetypes','profiles','bindings')]


def validate_state(row, owner):
    validator('spine-pack-installer-types.v2.schema.json', 'state').validate(row)
    require(row['owner'] == owner, 'foreign owner')
    family = row['object_key'].split(':')[0]
    require(row['root_id'] is not None, 'missing root identity')
    binding = family in ('binding', 'facet_binding')
    require((row['binding_id'] is not None) == binding, 'binding identity')
    require((row['revision_id'] is None) == binding, 'revision identity')
    require((row['revision_contract'] is None) == binding, 'revision decoder')
    if family == 'profile':
        require(row['revision_contract'] in ('spine.notification-profiles.v1', 'spine.notification-profiles.v2'), 'profile decoder')
        if row['revision_contract'].endswith('.v1'):
            family = 'profile_v1'
    elif not binding:
        require(row['revision_contract']=={'archetype':'spine.item-archetypes.v1',
                    'schema':'spine.facet-schemas.v1','rendering':'spine.notification-rendering-definitions.v1'}[family], 'wrong revision contract')
    validator('spine-pack-embedded-values.v2.schema.json', family).validate(unblob(row['value']))
    if binding:
        require(row['root_id']==unblob(row['value'])['item_archetype_id'], 'binding archetype identity')


def observation(view, owner):
    validator('spine-pack-installer-types.v2.schema.json', 'observation').validate(view)
    require(view['owner'] == owner, 'observation owner')
    require(view['digest'] == observation_digest(view), 'observation digest')
    require(len(view['entries']) + len(view['historical_revisions']) <= 4096, 'aggregate entries')
    ordered([r['object_key'] for r in view['entries']])
    ordered([(r['object_key'], r['revision_id']) for r in view['historical_revisions']])
    require([x['catalog'] for x in view['public_catalog_snapshots']] == ['archetypes', 'profiles', 'bindings'], 'public snapshots')
    require(view['public_catalog_snapshots'] == public_snapshots(view['entries']), 'public fingerprint mismatch')
    for row in view['entries'] + view['historical_revisions']:
        validate_state(row, owner)
    current={r['object_key']:r for r in view['entries']}
    for row in view['historical_revisions']:
        require(row['object_key'] in current and row['root_id']==current[row['object_key']]['root_id'] and
                row['revision_id']!=current[row['object_key']]['revision_id'],'historical root/revision membership')
    roots = [r['root_id'] for r in view['entries'] if r['binding_id'] is None]
    require(len(roots) == len(set(roots)), 'duplicate root identity')


def allowed_slots(action, desired):
    cmd = action['command']
    result = {}
    if cmd == 'item_archetype.facet_binding.set':
        result['/item_archetype_id'] = ('archetype:' + desired['archetype_key'], 'root')
        result['/facet_schema_revision_id'] = ('schema:' + desired['schema_ref']['schema_key'], 'revision')
    elif cmd.startswith('notification_rendering_definition.'):
        for i, s in enumerate(desired['revision']['selections']):
            result[f'/revision/selections/{i}/facet_schema_revision_id'] = ('schema:' + s['schema_ref']['schema_key'], 'revision')
    elif cmd in ('notification_profile.create', 'notification_profile.revise'):
        for i, t in enumerate(desired['revision']['templates']):
            r = t['rendering']
            if r['kind'] == 'definition':
                key = 'rendering:' + r['definition_ref']['definition_key']
                p = f'/revision/templates/{i}/rendering/definition/notification_rendering_definition'
                result[p + '_id'] = (key, 'root')
                result[p + '_revision_id'] = (key, 'revision')
    elif cmd == 'notification_profile.binding.set':
        result['/item_archetype_id'] = ('archetype:' + desired['archetype_key'], 'root')
        result['/notification_profile_id'] = ('profile:' + desired['notification_profile_key'], 'root')
    return result


def expected_template(action, owner):
    """Exact declarative mapping; nulls are typed holes, never predicted IDs."""
    d = unblob(action['desired']); cmd = action['command']; old = action['expected']
    req = {'contract_version': COMMANDS[cmd]['selector']}
    if cmd == 'item_archetype.create':
        req.update(owner=owner, archetype_key=d['archetype_key'], revision=d['revision'])
    elif cmd == 'item_archetype.revise':
        req.update(item_archetype_id=old['root_id'], expected_current_revision_id=old['revision_id'], revision=d['revision'])
    elif cmd.startswith('facet_schema.'):
        req['definition'] = d['definition']
        if cmd.endswith('.create'):
            req.update(owner=owner, schema_key=d['schema_key'])
        else:
            req.update(facet_schema_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'item_archetype.facet_binding.set':
        req.update(item_archetype_id=None, facet_key=d['facet_key'], facet_schema_revision_id=None,
                   expected_binding_id=old['binding_id'] if old else None)
    elif cmd.startswith('notification_rendering_definition.'):
        req['revision'] = deepcopy(d['revision'])
        for s in req['revision']['selections']:
            del s['schema_ref']; s['facet_schema_revision_id'] = None
        if cmd.endswith('.create'):
            req.update(owner=owner, definition_key=d['definition_key'])
        else:
            req.update(notification_rendering_definition_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'notification_profile.metadata.update':
        req.update(notification_profile_id=old['root_id'], expected_metadata=unblob(old['value'])['metadata'],
                   metadata={k: d[k] for k in ('display_name', 'description')})
    elif cmd in ('notification_profile.create', 'notification_profile.revise'):
        req['revision'] = deepcopy(d['revision'])
        for t in req['revision']['templates']:
            if t['rendering']['kind'] == 'definition':
                t['rendering'] = {'kind': 'definition', 'definition': {
                    'notification_rendering_definition_id': None, 'notification_rendering_definition_revision_id': None}}
        if cmd.endswith('.create'):
            req.update(owner=owner, profile_key=d['profile_key'], **{k: d[k] for k in ('display_name', 'description')})
        else:
            req.update(notification_profile_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'notification_profile.binding.set':
        req.update(owner=owner, item_archetype_id=None, notification_profile_id=None)
    return req


def desired_semantics(key, desired, resolutions):
    def resolve(k, f):
        source = resolutions[k][f]
        require(source is not None, 'missing resolution')
        # A tagged comparison token, never a guessed ID or a submitted request.
        return source['value'] if source['kind'] == 'observed' else '@pending/' + source['action_id'] + source['output_pointer']
    family = key.split(':')[0]
    if family == 'archetype': return desired['revision']
    if family == 'schema': return desired['definition']
    if family == 'rendering':
        body = deepcopy(desired['revision'])
        for s in body['selections']:
            s['facet_schema_revision_id'] = resolve('schema:' + s.pop('schema_ref')['schema_key'], 'revision')
        return body
    if family == 'profile':
        revision = deepcopy(desired['revision'])
        for t in revision['templates']:
            r = t['rendering']
            if r['kind'] == 'definition':
                k = 'rendering:' + r.pop('definition_ref')['definition_key']
                r['definition'] = {'notification_rendering_definition_id': resolve(k,'root'),
                                   'notification_rendering_definition_revision_id': resolve(k,'revision')}
        return {'metadata': {k:desired[k] for k in ('display_name','description')}, 'revision':revision}
    body = {'item_archetype_id':resolve('archetype:' + desired['archetype_key'],'root')}
    if family == 'facet_binding':
        body.update(facet_key=desired['facet_key'],facet_schema_revision_id=resolve('schema:' + desired['schema_ref']['schema_key'],'revision'))
    else:
        body['notification_profile_id'] = resolve('profile:' + desired['notification_profile_key'],'root')
    return body


def plan_check(manifest, request, plan):
    validate_manifest(manifest); artifact(request); artifact(plan)
    require(plan['request'] == request['request'] and plan['request_digest'] == request['content_identity']['digest'], 'request correlation')
    require(plan['pack'] == dict(manifest_schema=manifest['manifest_schema'], **manifest['pack'], manifest_digest=manifest['content_identity']['digest']), 'pack correlation')
    selection = plan['request']['selection']
    if selection['mode'] == 'archetypes':
        ordered(selection['archetype_keys'])
    require(plan['closure'] == closure(manifest, selection), 'selection closure')
    ordered(plan['environment']['advertised_contracts'])
    require(set(INVENTORY['required_execution_contracts']) <= set(plan['environment']['advertised_contracts']), 'missing execution contracts')
    require(set(manifest['compatibility']['spine_content_contracts']) <= set(plan['environment']['advertised_contracts']), 'missing content contracts')
    observation(plan['observation'], plan['request']['owner'])
    rows = {r['object_key']: r for r in plan['observation']['entries']}
    require([c['object_key'] for c in plan['classifications']] == plan['closure'], 'classification coverage')
    require([r['object_key'] for r in plan['resolutions']] == plan['closure'], 'resolution coverage')
    objects = manifest_objects(manifest)
    for c in plan['classifications']:
        require(unblob(c['desired']) == objects[c['object_key']], 'desired content')
        require(c['observed'] == rows.get(c['object_key']), 'observed preimage')
        require(c['classification'] == 'blocked' or (c['classification'] == 'missing') == (c['observed'] is None), 'missing classification')
        require((c['blocked_reason'] is not None) == (c['classification'] == 'blocked'), 'blocked classification')
        if c['observed'] and c['observed']['status'] == 'retired':
            require(c['classification'] == 'blocked', 'retired object')
    actions = {a['action_id']: a for a in plan['actions']}
    require(len(actions) == len(plan['actions']), 'duplicate actions')
    phases = []
    for i, a in enumerate(plan['actions']):
        require(a['ordinal'] == str(i) and a['action_id'] == f'action-{i:06d}', 'action ordinal')
        require(a['object_key'] in plan['closure'], 'unselected action')
        require(unblob(a['desired']) == objects[a['object_key']], 'action desired')
        require(a['expected'] == rows.get(a['object_key']), 'action preimage')
        require((a['change_kind'] == 'create') == (a['expected'] is None), 'change kind')
        phases.append((COMMANDS[a['command']]['phase'], a['object_key']))
        require(unblob(a['request_template']) == expected_template(a, plan['request']['owner']), 'request template mapping')
        require('${' not in a['request_template']['canonical_json'], 'interpolation forbidden')
        slots = allowed_slots(a, objects[a['object_key']])
        require(a['slots'] == [dict(request_pointer=p, object_key=k, field=f) for p, (k, f) in sorted(slots.items())], 'typed slots')
        resolutions = {r['object_key']: r for r in plan['resolutions']}
        for k, f in slots.values():
            source = resolutions[k][f]
            require(source is not None, 'unresolved dependency')
            if source['kind'] == 'action_result':
                require(int(actions[source['action_id']]['ordinal']) < i, 'forward/self reference')
    require(phases == sorted(set(phases)), 'action phase order or duplicate')
    for row in plan['resolutions']:
        for field in ('root', 'revision', 'binding'):
            source = row[field]
            if source is None:
                continue
            if source['kind'] == 'observed':
                key = ('archetype:' + row['object_key'].split(':')[1]
                       if field == 'root' and row['object_key'].split(':')[0] in ('binding', 'facet_binding') else row['object_key'])
                require(source['object_key'] == key and source['field'] == field, 'observed source kind')
                require(source['value'] == rows[key][field + '_id'], 'observed source identity')
            else:
                producer = actions[source['action_id']]
                key = ('archetype:' + row['object_key'].split(':')[1]
                       if field == 'root' and row['object_key'].split(':')[0] in ('binding', 'facet_binding') else row['object_key'])
                require(producer['object_key'] == key, 'wrong producer object')
                require(COMMANDS[producer['command']]['outputs'].get(field) == source['output_pointer'], 'wrong producer output')
    require(plan['decision_action_ids'] == [a['action_id'] for a in plan['actions'] if a['change_kind'] == 'update'], 'update coverage')
    require(plan['blocked_object_keys'] == [c['object_key'] for c in plan['classifications'] if c['classification'] == 'blocked'], 'blocked coverage')
    require(plan['apply_eligible'] == (manifest['pack']['status'] == 'released' and not plan['blocked_object_keys']), 'draft or blocked eligibility')
    resolutions = {r['object_key']:r for r in plan['resolutions']}
    expected_commands = []
    for c in plan['classifications']:
        key=c['object_key']; family=key.split(':')[0]; old=c['observed']; resolution=resolutions[key]
        if c['classification'] == 'blocked':
            require(all(resolution[f] is None for f in ('root','revision','binding')), 'blocked resolution')
            continue
        require(resolution['root'] is not None, 'missing root source')
        binding=family in ('binding','facet_binding')
        require((resolution['revision'] is None) == binding and (resolution['binding'] is not None) == binding, 'resolution identity shape')
        desired=desired_semantics(key,objects[key],resolutions)
        observed=unblob(old['value']) if old else None
        if family=='profile' and old and old['revision_contract']=='spine.notification-profiles.v1':
            for t in observed['revision']['templates']:t['rendering']={'kind':'ordinary'}
        classification='missing' if old is None else 'equivalent' if desired==observed else 'drifted'
        require(c['classification']==classification, 'semantic classification')
        if classification=='equivalent':continue
        cmd={'archetype':'item_archetype','schema':'facet_schema','rendering':'notification_rendering_definition','facet_binding':'item_archetype.facet_binding','binding':'notification_profile.binding','profile':'notification_profile'}[family]
        if classification=='missing':
            expected_commands.append((key,cmd+('.set' if binding else '.create')))
        elif family=='profile':
            if desired['metadata']!=observed['metadata']:expected_commands.append((key,cmd+'.metadata.update'))
            if desired['revision']!=observed['revision']:expected_commands.append((key,cmd+'.revise'))
        else:
            expected_commands.append((key,cmd+('.set' if binding else '.revise' if family=='archetype' else '.publish')))
    require(sorted(expected_commands)==sorted((a['object_key'],a['command']) for a in plan['actions']), 'complete action coverage')


def approval_check(plan, approval):
    artifact(approval)
    require(approval['plan_digest'] == plan['content_identity']['digest'], 'stale approval')
    require(approval['authorized_update_action_ids'] == plan['decision_action_ids'], 'update authorization')
    require(plan['apply_eligible'], 'ineligible apply')


def materialize(plan, approval, action, prefix):
    request = unblob(action['request_template'])
    rows = {r['object_key']: r for r in plan['resolutions']}
    for slot in action['slots']:
        source = rows[slot['object_key']][slot['field']]
        if source['kind'] == 'observed':
            value = source['value']
        else:
            evidence = next((e for e in prefix if e['action_id'] == source['action_id']), None)
            require(evidence is not None, 'consumer before accepted producer')
            value = pointer(unblob(evidence['response'], True), source['output_pointer'])
        require(pointer(request, slot['request_pointer']) is None, 'non-null slot')
        pointer(request, slot['request_pointer'], value, True)
    request.update({k: approval['execution'][k] for k in ('actor_subject_id', 'action_timestamp_utc')},
                   command_id=command_id(plan, approval, action))
    public_schema(action['command'], 'request', request)
    if action['command'].startswith('notification_rendering_definition.'):
        require(len(canonical(request['revision'])) <= 8192, 'resolved rendering byte limit')
    if action['command'].startswith('facet_schema.'):
        require(len(canonical(request['definition'])) <= 32768, 'facet byte limit')
    if action['command'] in ('notification_profile.create', 'notification_profile.revise'):
        require(len(canonical(request)) <= 32768, 'resolved profile request byte limit')
    return request


def receipt_projection(command, response):
    family = COMMANDS[command]['family']
    if family == 'catalog':
        return dict(family=family, **{k: response['receipt'][k] for k in ('command_receipt_id', 'effect', 'semantic_facts_hash', 'created_at_utc')})
    return dict(family=family, **{k: response[k] for k in ('command_receipt_id', 'effect', 'changed', 'replayed')}, audit_id=response.get('audit_id'))


def evidence_check(plan, approval, action, evidence, prefix):
    req = materialize(plan, approval, action, prefix)
    require(evidence['action_id'] == action['action_id'] and evidence['command'] == action['command'], 'evidence prefix')
    require(evidence['command_id'] == req['command_id'] and unblob(evidence['request']) == req, 'exact submitted request')
    response = unblob(evidence['response'], True)
    public_schema(action['command'], 'response', response)
    require(not response.get('dry_run'), 'dry-run evidence')
    require(evidence['receipt'] == receipt_projection(action['command'], response), 'receipt projection')
    receipt = response.get('receipt', response)
    require(receipt['command_id'] == req['command_id'], 'receipt command identity')
    if evidence['receipt']['family'] == 'catalog':
        require(receipt['semantic_facts_hash'] == hash_value(req), 'receipt request hash')
        require(receipt['created_at_utc'] == req['action_timestamp_utc'], 'receipt timestamp')
        require(receipt['effect'] == response['effect'], 'receipt effect')
    post = evidence['post_observation']; validate_state(post, plan['request']['owner'])
    require(post['object_key'] == action['object_key'], 'post object')
    for field, path in COMMANDS[action['command']]['outputs'].items():
        require(post[field + '_id'] == pointer(response, path), 'response output/readback mismatch')
    for field in ('item_archetype_id', 'notification_profile_id', 'facet_schema_id', 'notification_rendering_definition_id'):
        if field in req and field in response:
            require(req[field] == response[field], 'response target')
    for field in ('archetype_key', 'profile_key'):
        if field in req:
            require(response[field] == req[field], 'create key')
    if 'prior_revision_id' in response:
        require(response['prior_revision_id'] == req.get('expected_current_revision_id'), 'prior revision')
    if 'prior_binding_id' in response:
        require(response['prior_binding_id'] == req['expected_binding_id'], 'prior binding')
    body = unblob(post['value']); cmd = action['command']
    if cmd.startswith('item_archetype.') and cmd != 'item_archetype.facet_binding.set':
        require(body == req['revision'], 'archetype readback semantics')
    elif cmd.startswith('facet_schema.'):
        require(body == req['definition'], 'facet readback semantics')
    elif cmd.startswith('notification_rendering_definition.'):
        record = response['record']
        require(body == req['revision'] == record['revision'], 'rendering readback semantics')
        require(record['owner'] == plan['request']['owner'], 'rendering owner')
        require(record['status']=='active', 'rendering status')
        require(record['definition_key'] == action['object_key'].split(':')[1], 'rendering key')
        require(record['current_revision_id'] == post['revision_id'] and record['notification_rendering_definition_id'] == post['root_id'], 'rendering current/root')
        require(record['definition_hash'] == hash_value({'contract_version':'spine.notification-rendering-definitions.v1','canonical_json_version':'spine.canonical-json.v1','revision':req['revision']}), 'rendering hash')
        require(record['published'] == {k:req[k] for k in ('command_id','actor_subject_id','action_timestamp_utc')}, 'rendering provenance')
        if cmd.endswith('.create'):require(record['created']==record['published'],'rendering create provenance')
    elif cmd == 'item_archetype.facet_binding.set':
        require(body == {k:req[k] for k in ('item_archetype_id','facet_key','facet_schema_revision_id')}, 'facet binding semantics')
    elif cmd == 'notification_profile.binding.set':
        require(body == {k:req[k] for k in ('item_archetype_id','notification_profile_id')}, 'default binding semantics')
    elif cmd == 'notification_profile.metadata.update':
        require(body['metadata'] == req['metadata'], 'metadata semantics')
        require(body['revision'] == unblob(action['expected']['value'])['revision'], 'metadata changed revision')
    else:
        require(body['revision'] == req['revision'], 'profile readback semantics')
        desired = unblob(action['desired'])
        require(body['metadata'] == {k:desired[k] for k in ('display_name','description')}, 'profile metadata')
        templates=[]
        for template in req['revision']['templates']:
            templates.append(dict(template, normalized_template_hash=hash_value({
                'derivation_version':'spine.notification-profile-template-hash.v2',
                'canonical_json_version':'spine.canonical-json.v1','template':template})))
        require(response['normalized_revision_hash']==hash_value({
            'derivation_version':'spine.notification-profile-revision-hash.v2',
            'canonical_json_version':'spine.canonical-json.v1',
            'revision':dict(req['revision'],templates=templates)}), 'profile revision hash')
    if action['expected']:
        require(post['root_id'] == action['expected']['root_id'], 'changed root')
    if response['effect'].endswith('noop'):
        require(action['expected'] == post, 'no-op cannot explain change')


def checkpoint_check(plan, approval, checkpoint):
    artifact(checkpoint); approval_check(plan, approval)
    require(checkpoint['plan_digest'] == plan['content_identity']['digest'], 'checkpoint plan')
    require(checkpoint['approval_digest'] == approval['content_identity']['digest'] and checkpoint['execution'] == approval['execution'], 'checkpoint execution')
    prefix = checkpoint['accepted_responses']; actions = plan['actions']
    require(len(prefix) <= len(actions), 'prefix overflow')
    for i, evidence in enumerate(prefix):
        evidence_check(plan, approval, actions[i], evidence, prefix[:i])
    next_id = actions[len(prefix)]['action_id'] if len(prefix) < len(actions) else None
    require(checkpoint['next_action_id'] == next_id, 'next action')
    pending = checkpoint['unresolved_submission']
    if pending:
        require(pending['action_id'] == next_id, 'uncertain gap')
        request = materialize(plan, approval, actions[len(prefix)], prefix)
        require(pending['command_id'] == request['command_id'] and unblob(pending['request']) == request, 'changed replay bytes')


def forward(view, evidence):
    result = deepcopy(view)
    entries = {r['object_key']: r for r in result['entries']}
    history = {(r['object_key'], r['revision_id']): r for r in result['historical_revisions']}
    for e in evidence:
        post = e['post_observation']; old = entries.get(post['object_key'])
        if old and old['revision_id'] and old['revision_id'] != post['revision_id']:
            history[(old['object_key'], old['revision_id'])] = old
        entries[post['object_key']] = post
    result['entries'] = [entries[k] for k in sorted(entries)]
    result['historical_revisions'] = [history[k] for k in sorted(history)]
    # Old fingerprints are independently validated by the observer; they cannot
    # be invented from this reduced semantic view. Recovery compares the full
    # semantic/identity projection, not unknown future public hash strings.
    result.pop('public_catalog_snapshots'); result.pop('digest')
    return result


def recovery_check(plan, approval, checkpoint, fresh, provisional=None, replay=None):
    checkpoint_check(plan, approval, checkpoint)
    observation(fresh, plan['request']['owner'])
    prefix = checkpoint['accepted_responses']
    baseline = forward(plan['observation'], prefix)
    actual = forward(fresh, [])
    if actual == baseline:
        require(provisional is None, 'unexplained provisional candidate')
        return 'prefix'
    require(checkpoint['unresolved_submission'] is not None and provisional is not None, 'unexplained catalog change')
    require(provisional['object_key'] == plan['actions'][len(prefix)]['object_key'], 'uncertain suffix')
    validate_state(provisional, plan['request']['owner'])
    candidate = forward(plan['observation'], prefix + [{'post_observation': provisional}])
    require(actual == candidate, 'unrelated catalog change')
    require(replay is not None, 'candidate is not acceptance evidence')
    evidence_check(plan, approval, plan['actions'][len(prefix)], replay, prefix)
    require(replay['post_observation'] == provisional, 'replay candidate identity mismatch')
    return 'prefix_plus_one'


def result_check(plan, approval, result):
    artifact(result); checkpoint_check(plan, approval, result['checkpoint'])
    cp = result['checkpoint']; n = len(cp['accepted_responses']); actions = plan['actions']
    if result['state'] == 'applied':
        require(n == len(actions) and not cp['unresolved_submission'] and result['failure'] is None and result['unattempted_action_ids'] == [], 'applied coverage')
    elif result['state'] == 'partial':
        require(n < len(actions) and result['failure']['action_id'] == actions[n]['action_id'], 'partial failure')
        require(result['unattempted_action_ids'] == [a['action_id'] for a in actions[n+1:]], 'partial suffix')
    else:
        require(n == 0 and cp['unresolved_submission'] is None and result['failure'] is not None, 'not-applied evidence')
        require(result['unattempted_action_ids'] == [a['action_id'] for a in actions], 'not-applied suffix')


def verification_check(plan, approval, result, verification):
    artifact(verification)
    require(verification['plan_digest'] == plan['content_identity']['digest'], 'verification plan')
    for field in ('pack', 'environment', 'closure'):
        require(verification[field] == plan[field], 'verification ' + field)
    require(verification['target'] == plan['request']['target'], 'verification target')
    observation(verification['observation'], plan['request']['owner'])
    require([r['object_key'] for r in verification['object_results']] == plan['closure'], 'verification coverage')
    fresh = {r['object_key']: r for r in verification['observation']['entries']}
    expected = {r['object_key']: r for r in plan['observation']['entries']}
    if result is not None:
        result_check(plan, approval, result)
        expected.update({e['post_observation']['object_key']: e['post_observation'] for e in result['checkpoint']['accepted_responses']})
    complete = bool(result and result['state'] == 'applied')
    coverage = ('complete' if complete else 'missing') if plan['actions'] else 'not_required'
    require(verification['response_evidence'] == coverage, 'verification evidence coverage')
    require(verification['apply_result_digest'] == (result['content_identity']['digest'] if result and plan['actions'] else None), 'verification result correlation')
    for r in verification['object_results']:
        require(r['observed'] == fresh.get(r['object_key']), 'verification observation')
        if r['state'] == 'equivalent':
            actual=deepcopy(r['observed']); desired=deepcopy(expected.get(r['object_key']))
            if actual and desired and (r['object_key'].startswith('archetype:') or
                    r['object_key'].startswith('profile:') and actual['revision_contract']==desired['revision_contract']=='spine.notification-profiles.v1'):
                actual['revision_id']=desired['revision_id']
            require(actual is not None and actual == desired and actual['status'] == 'active', 'exact current pin/identity')
    success = coverage in ('complete','not_required') and all(r['state'] == 'equivalent' for r in verification['object_results'])
    require((verification['state'] == 'verified') == success, 'verification outcome')
```

### Spec 25: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_facet_artifact_contract.py

Hash: 22d9417169d72910fb2c69a3c9226add1a2d75c56eea106feeef22bcea11bbc5

```markdown
"""FR-1 saved artifact and execution/recovery vectors; no runtime/CLI calls."""
from copy import deepcopy
import hashlib
import json
import unittest

from facet_artifact_oracle import *

FIXTURES = ROOT / 'tests/fixtures/installer-v2'
INDEX = ROOT / 'contracts/installer-fixture-manifest.v2.json'


def checkpoint_at(flow, length, prepared=False):
    cp = deepcopy(flow['initial_checkpoint'])
    cp['accepted_responses'] = deepcopy(flow['accepted_responses'][:length])
    actions = flow['plan']['actions']
    cp['next_action_id'] = actions[length]['action_id'] if length < len(actions) else None
    cp['unresolved_submission'] = None
    if prepared:
        action = actions[length]
        req = materialize(flow['plan'], flow['approval'], action, cp['accepted_responses'])
        cp['unresolved_submission'] = {'action_id': action['action_id'], 'command_id': req['command_id'],
            'submission_state': 'prepared_or_submitted', 'request': blob(req)}
    return seal(cp)


def reseal_response(evidence, value):
    text = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    evidence['response'] = {'json_text': text, 'digest': sha(text.encode())}
    evidence['receipt'] = receipt_projection(evidence['command'], value)


@unittest.skipIf(Draft202012Validator is None, 'FR-1 requires development jsonschema; run isolated gate')
class FacetArtifactTests(unittest.TestCase):
    def flow(self, name='flight-create'):
        return load(FIXTURES / (name + '.json'))

    def test_official_schema_meta_and_offline_reference_closure(self):
        for path in SCHEMAS.glob('*.json'):
            Draft202012Validator.check_schema(load(path))
        readback = load(SCHEMAS / 'spine-readback-0.9.1.schema.json')
        def walk(value):
            if isinstance(value, dict):
                if '$ref' in value:
                    self.assertTrue(value['$ref'].startswith('#/$defs/'))
                    self.assertIn(value['$ref'].split('/')[-1], readback['$defs'])
                for v in value.values():
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
        walk(readback)
        self.assertEqual(len(COMMANDS), 22)
        self.assertEqual(sum(c['phase'] is not None for c in COMMANDS.values()), 11)
        self.assertEqual(len(INVENTORY['required_execution_contracts']), 17)
        self.assertFalse(any('disclosure' in c or c.startswith('item.') for c in COMMANDS))

    def test_saved_complete_create_and_update_flows(self):
        commands = set()
        for name in ('flight-create','flight-update'):
            with self.subTest(flow=name):
                f = self.flow(name); p = f['plan']; a = f['approval']
                plan_check(f['manifest'], f['request'], p)
                approval_check(p, a)
                for key in ('initial_checkpoint','final_checkpoint','prepared_checkpoint'):
                    checkpoint_check(p, a, f[key])
                for key in ('apply_result','partial_result','empty_prefix_partial'):
                    result_check(p, a, f[key])
                verification_check(p, a, f['apply_result'], f['verification'])
                artifact(f['envelope'])
                commands.update(x['command'] for x in p['actions'])
        self.assertEqual(commands, {c for c,v in COMMANDS.items() if v['phase'] is not None})

    def test_indexed_execution_recovery_boundaries(self):
        vectors = load(INDEX)['vectors']
        for vector in vectors:
            with self.subTest(vector=vector['id']):
                f = load(FIXTURES / vector['fixture']); p=f['plan']; a=f['approval']; n=int(vector['prefix_length'])
                if vector['boundary'] == 'accepted_durable':
                    cp = checkpoint_at(f,n+1)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n+1]),'prefix')
                elif vector['boundary'] == 'prepared_before_submit':
                    cp = checkpoint_at(f,n,True)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n]),'prefix')
                else:
                    cp = checkpoint_at(f,n,True); replay=deepcopy(f['accepted_responses'][n])
                    r=unblob(replay['response'],True)
                    if 'replayed' in r:
                        r.update(replayed=True,changed=False);reseal_response(replay,r)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n+1],f['accepted_responses'][n]['post_observation'],replay),'prefix_plus_one')

    def test_negative_typed_references_and_complete_authorization(self):
        for failure in ('forward','wrong_output','wrong_object','missing_slot','non_null_slot','missing_resolution','stale_approval','unauthorized_update','wrong_union','wrong_environment','wrong_owner','closure_gap','wrong_digest'):
            with self.subTest(failure=failure):
                f=self.flow('flight-update' if failure=='unauthorized_update' else 'flight-create');p=f['plan'];a=f['approval']
                if failure=='forward':p['resolutions'][p['closure'].index('schema:flight_details')]['revision']['action_id']='action-000004'
                elif failure=='wrong_output':p['resolutions'][-1]['revision']['output_pointer']='/facet_schema_id'
                elif failure=='wrong_object':p['actions'][2]['slots'][0]['object_key']='rendering:flight_details'
                elif failure=='missing_slot':p['actions'][3]['slots'].pop()
                elif failure=='non_null_slot':
                    body=unblob(p['actions'][2]['request_template']);body['facet_schema_revision_id']='guessed';p['actions'][2]['request_template']=blob(body)
                elif failure=='missing_resolution':p['resolutions'].pop()
                elif failure=='stale_approval':a['plan_digest']='0'*64
                elif failure=='unauthorized_update':a['authorized_update_action_ids'].pop()
                elif failure=='wrong_union':p['required_execution_contracts'].pop()
                elif failure=='wrong_environment':p['environment']['runtime_version']='0.9.2'
                elif failure=='wrong_owner':p['request']['owner']['owner_subject_id']='other'
                elif failure=='closure_gap':p['closure'].pop()
                p=seal(p);a=seal(a)
                if failure=='wrong_digest':p['content_identity']['digest']='0'*64
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    plan_check(f['manifest'],f['request'],p);approval_check(p,a)

    def test_negative_evidence_and_replay(self):
        for failure in ('gap','changed_request','wrong_command_id','wrong_receipt_hash','wrong_output','dry_run','wrong_selector','wrong_projection','wrong_provenance','noop_change','guessed_suffix','unrelated_change','candidate_without_replay','candidate_id_mismatch'):
            with self.subTest(failure=failure):
                f=self.flow();p=f['plan'];a=f['approval'];n=3;cp=checkpoint_at(f,n,True)
                fresh=deepcopy(f['observations'][n+1]);replay=deepcopy(f['accepted_responses'][n]);candidate=deepcopy(replay['post_observation'])
                if failure=='gap':cp['accepted_responses'].pop(0)
                elif failure=='changed_request':
                    r=unblob(cp['unresolved_submission']['request']);r['actor_subject_id']='other';cp['unresolved_submission']['request']=blob(r)
                elif failure=='wrong_command_id':cp['unresolved_submission']['command_id']='other'
                elif failure in ('wrong_receipt_hash','wrong_output'):
                    r=unblob(cp['accepted_responses'][0]['response'],True)
                    if failure=='wrong_receipt_hash':r['receipt']['semantic_facts_hash']='0'*64
                    else:r['item_archetype_id']='other'
                    reseal_response(cp['accepted_responses'][0],r)
                elif failure in ('dry_run','wrong_selector','wrong_provenance','noop_change'):
                    r=unblob(replay['response'],True)
                    if failure=='dry_run':r['dry_run']=True
                    elif failure=='wrong_selector':r['contract_version']='spine.notification-profiles.v2'
                    elif failure=='wrong_provenance':r['record']['published']['actor_subject_id']='other'
                    else:r['effect']='rendering_definition_publish_noop';r['changed']=False
                    reseal_response(replay,r)
                elif failure=='wrong_projection':replay['receipt']['audit_id']='invented'
                elif failure=='guessed_suffix':cp['accepted_responses'].append(f['accepted_responses'][4])
                elif failure=='unrelated_change':fresh['entries'][0]['root_id']='other'
                elif failure=='candidate_without_replay':replay=None
                elif failure=='candidate_id_mismatch':candidate['revision_id']='other'
                cp=seal(cp);fresh['digest']=observation_digest(fresh)
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    recovery_check(p,a,cp,fresh,candidate,replay)

    def test_verification_exact_pins_and_read_only_evidence(self):
        for failure in ('current_head','binding_pin','missing_result','wrong_target','missing_object','false_disclosure'):
            with self.subTest(failure=failure):
                f=self.flow();v=f['verification'];result=f['apply_result']
                if failure=='current_head':
                    row=next(r for r in v['observation']['entries'] if r['object_key'].startswith('schema:'));row['revision_id']='later-equivalent-revision'
                elif failure=='binding_pin':
                    row=next(r for r in v['observation']['entries'] if r['object_key'].startswith('facet_binding:'));body=unblob(row['value']);body['facet_schema_revision_id']='later';row['value']=blob(body)
                elif failure=='missing_result':result=None
                elif failure=='wrong_target':v['target']['host_name']='elsewhere.invalid'
                elif failure=='missing_object':v['object_results'].pop()
                else:v['disclosure']='approved'
                v['observation']['digest']=observation_digest(v['observation']);v=seal(v)
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    verification_check(f['plan'],f['approval'],result,v)

    def test_response_text_numbers_and_duplicate_rejection(self):
        text='{"revision_number":1}'
        value={'json_text':text,'digest':sha(text.encode())}
        self.assertEqual(unblob(value,True),{'revision_number':1})
        with self.assertRaises(ValueError):canonical({'revision_number':1})
        for text in ('{"ok":true,"ok":true}','{"n":NaN}','"\\ud800"','\ufeff{}'):
            with self.assertRaises((ValueError,UnicodeError)):
                unblob({'json_text':text,'digest':sha(text.encode())},True)

    def test_retain_no_write_plan_and_draft_refusal(self):
        f=self.flow();p=deepcopy(f['plan']);p['observation']=deepcopy(f['observations'][-1])
        rows={r['object_key']:r for r in p['observation']['entries']}
        p.update(actions=[],decision_action_ids=[])
        for c in p['classifications']:
            c.update(classification='equivalent',observed=rows[c['object_key']])
        for r in p['resolutions']:
            for field in ('root','revision','binding'):
                value=rows[r['object_key']][field+'_id']
                key=('archetype:flight' if field=='root' and r['object_key'].split(':')[0] in ('binding','facet_binding') else r['object_key'])
                r[field]={'kind':'observed','object_key':key,'field':field,'value':value} if value else None
        p=seal(p);plan_check(f['manifest'],f['request'],p)
        a=deepcopy(f['approval']);a['plan_digest']=p['content_identity']['digest'];a=seal(a)
        v=deepcopy(f['verification']);v.update(plan_digest=p['content_identity']['digest'],apply_result_digest=None,response_evidence='not_required');v=seal(v)
        verification_check(p,a,None,v)
        from test_facet_manifest_contract import digest
        m=deepcopy(f['manifest']);m['pack'].update(version='1.0.0-draft.1',status='draft');m['content_identity']['digest']=digest(m)
        req=deepcopy(f['request']);req['request']['draft_posture']='inspect_only';req=seal(req)
        p.update(pack=dict(manifest_schema=m['manifest_schema'],**m['pack'],manifest_digest=m['content_identity']['digest']),request=req['request'],request_digest=req['content_identity']['digest'],apply_eligible=False);p=seal(p)
        plan_check(m,req,p)
        a['plan_digest']=p['content_identity']['digest'];a=seal(a)
        with self.assertRaisesRegex(ValueError,'ineligible apply'):approval_check(p,a)

    def test_all_artifact_digests_and_v1_rejection(self):
        f=self.flow()
        for value in f.values():
            if isinstance(value,dict) and 'artifact_schema' in value:
                artifact(value)
                kind=value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
                self.assertFalse(validator('spine-pack-'+kind+'.v1.schema.json').is_valid(value))
                if 'content_identity' in value:
                    value['content_identity']['digest']='0'*64
                    with self.assertRaises(ValueError):artifact(value)

    def test_command_and_artifact_hash_preimages_independent(self):
        f=self.flow();p=f['plan'];a=f['approval']
        # Fixture text has no control escapes; direct stdlib serialization is an
        # independent encoder for this fixed vector, not a second call to seal.
        value=deepcopy(p);expected=value['content_identity'].pop('digest')
        raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),expected)
        for action,e in zip(p['actions'],f['accepted_responses']):
            value={'action_id':action['action_id'],'derivation_version':'spine.pack-command-id.v2','execution_id':a['execution']['execution_id'],'plan_digest':expected}
            raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
            self.assertEqual('spack_'+hashlib.sha256(raw).hexdigest(),e['command_id'])

    def test_resolved_rendering_byte_limit_inclusive(self):
        f=self.flow();action=deepcopy(f['plan']['actions'][3]);req=unblob(action['request_template'])
        # Resolve first, then fill bounded Unicode description to the exact byte
        # ceiling. Public maxLength counts codepoints, not UTF-8 bytes.
        resolved=materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])
        resolved['revision']['description']=''
        remaining=8192-len(canonical(resolved['revision']))
        req['revision']['description']='🛫'*(remaining//4)+'x'*(remaining%4)
        action['request_template']=blob(req)
        accepted=materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])
        self.assertEqual(len(canonical(accepted['revision'])),8192)
        req['revision']['description']+='x';action['request_template']=blob(req)
        with self.assertRaisesRegex(ValueError,'resolved rendering byte limit'):
            materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])

    def test_upstream_public_wire_vectors(self):
        vectors=load(FIXTURES/'public-wire-vectors.json')['vectors']
        for vector in vectors:
            with self.subTest(vector=vector['source']):
                public_schema(vector['command'],vector['direction'],vector['value'])


if __name__ == '__main__':
    unittest.main()
```

### Spec 26: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/installer-v2/flight-create.json

Hash: 22b8a79711c58ce1ca7331dc906679fecba7f32ca5f733e33dbcbb7748d05dee

```markdown
{
  "manifest": {
    "manifest_schema": "spine.pack-manifest.v2",
    "pack": {
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.0",
      "status": "released"
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
      "digest": "29896a54b3c27059044cf8975de79eafe37f61fd268a0a7211c4949db298546a"
    }
  },
  "request": {
    "artifact_schema": "spine.pack-install-request.v2",
    "request": {
      "selection": {
        "mode": "archetypes",
        "archetype_keys": [
          "flight"
        ]
      },
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "target": {
        "host_name": "fixture.invalid",
        "spine_command": {
          "path": "/synthetic/bin/spine-command",
          "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
        },
        "ledger": {
          "kind": "path",
          "path": "/synthetic/ledger.db"
        }
      },
      "draft_posture": "reject"
    },
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-request-digest.v2",
      "digest": "ee2d217423d9ffa0b0a697933ff39c811f7032b3b099da4055af730a9641589e"
    }
  },
  "plan": {
    "artifact_schema": "spine.pack-install-plan.v2",
    "request_digest": "ee2d217423d9ffa0b0a697933ff39c811f7032b3b099da4055af730a9641589e",
    "request": {
      "selection": {
        "mode": "archetypes",
        "archetype_keys": [
          "flight"
        ]
      },
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "target": {
        "host_name": "fixture.invalid",
        "spine_command": {
          "path": "/synthetic/bin/spine-command",
          "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
        },
        "ledger": {
          "kind": "path",
          "path": "/synthetic/ledger.db"
        }
      },
      "draft_posture": "reject"
    },
    "pack": {
      "manifest_schema": "spine.pack-manifest.v2",
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.0",
      "status": "released",
      "manifest_digest": "29896a54b3c27059044cf8975de79eafe37f61fd268a0a7211c4949db298546a"
    },
    "closure": [
      "archetype:flight",
      "binding:flight",
      "facet_binding:flight:flight",
      "profile:synthetic_flight_details",
      "rendering:flight_details",
      "schema:flight_details"
    ],
    "environment": {
      "runtime_version": "0.9.1",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schemas.v1",
        "spine.item-archetypes.v1",
        "spine.ledger-instance.v1",
        "spine.notification-profile-bindings.v1",
        "spine.notification-profile-catalog-cursor.v1",
        "spine.notification-profile-metadata-update.v1",
        "spine.notification-profile-readback.v1",
        "spine.notification-profiles.v1",
        "spine.notification-profiles.v2",
        "spine.notification-rendering-cursor.v1",
        "spine.notification-rendering-definitions.v1",
        "spine.notification-rendering-integration.v1",
        "spine.notification-rendering.v1",
        "spine.system-info.v3",
        "spine.tickerd-compatibility.v1"
      ]
    },
    "required_execution_contracts": [
      "spine.archetype-facet-bindings.v1",
      "spine.canonical-json.v1",
      "spine.facet-cursor.v1",
      "spine.facet-schemas.v1",
      "spine.item-archetypes.v1",
      "spine.ledger-instance.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profile-catalog-cursor.v1",
      "spine.notification-profile-metadata-update.v1",
      "spine.notification-profile-readback.v1",
      "spine.notification-profiles.v1",
      "spine.notification-profiles.v2",
      "spine.notification-rendering-cursor.v1",
      "spine.notification-rendering-definitions.v1",
      "spine.notification-rendering-integration.v1",
      "spine.system-info.v3",
      "spine.tickerd-compatibility.v1"
    ],
    "observation": {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "536131d08f76699d0d1962a6dfa33b77cd1cc52ee1bd2693c28655afe1a483df"
    },
    "classifications": [
      {
        "object_key": "archetype:flight",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"intended_status\":\"active\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "f2a8940953febe71a35d1a1990ebe07e38fb8fb9f10907fcf14e93441cc1d6bf"
        },
        "observed": null,
        "blocked_reason": null
      },
      {
        "object_key": "binding:flight",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"binding_kind\":\"archetype_default\",\"notification_profile_key\":\"synthetic_flight_details\"}",
          "digest": "76bcc28de81de3d4bd28b247dd394ea58b1f5fcfcc923beaa69cade6c3e0f34b"
        },
        "observed": null,
        "blocked_reason": null
      },
      {
        "object_key": "facet_binding:flight:flight",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"facet_key\":\"flight\",\"schema_ref\":{\"schema_key\":\"flight_details\"}}",
          "digest": "d305d7ca81d388049f2671fc9a37fd4bc79582b90fe4accba14c6dc4ab553a74"
        },
        "observed": null,
        "blocked_reason": null
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"intended_status\":\"active\",\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition_ref\":{\"definition_key\":\"flight_details\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "f1c625045b794ad603c16495f21cf9863d5bbe1c5cf007b316d1c5fc915f73ae"
        },
        "observed": null,
        "blocked_reason": null
      },
      {
        "object_key": "rendering:flight_details",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"definition_key\":\"flight_details\",\"intended_status\":\"active\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"origin\"}]}}",
          "digest": "9a65eba8e3d6af38e8edd37b26cb731062ef7984b1a57ffa3f66b9a74854997c"
        },
        "observed": null,
        "blocked_reason": null
      },
      {
        "object_key": "schema:flight_details",
        "classification": "missing",
        "desired": {
          "canonical_json": "{\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"intended_status\":\"active\",\"schema_key\":\"flight_details\"}",
          "digest": "d2b7739eba2623e5d9e66538898655586b0fa612ffbbae5a8cb2de8d59216b91"
        },
        "observed": null,
        "blocked_reason": null
      }
    ],
    "resolutions": [
      {
        "object_key": "archetype:flight",
        "root": {
          "kind": "action_result",
          "action_id": "action-000000",
          "output_pointer": "/item_archetype_id"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000000",
          "output_pointer": "/item_archetype_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "binding:flight",
        "root": {
          "kind": "action_result",
          "action_id": "action-000000",
          "output_pointer": "/item_archetype_id"
        },
        "revision": null,
        "binding": {
          "kind": "action_result",
          "action_id": "action-000005",
          "output_pointer": "/notification_profile_binding_id"
        }
      },
      {
        "object_key": "facet_binding:flight:flight",
        "root": {
          "kind": "action_result",
          "action_id": "action-000000",
          "output_pointer": "/item_archetype_id"
        },
        "revision": null,
        "binding": {
          "kind": "action_result",
          "action_id": "action-000002",
          "output_pointer": "/facet_binding_id"
        }
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "root": {
          "kind": "action_result",
          "action_id": "action-000004",
          "output_pointer": "/notification_profile_id"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000004",
          "output_pointer": "/notification_profile_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "rendering:flight_details",
        "root": {
          "kind": "action_result",
          "action_id": "action-000003",
          "output_pointer": "/record/notification_rendering_definition_id"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000003",
          "output_pointer": "/record/notification_rendering_definition_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "schema:flight_details",
        "root": {
          "kind": "action_result",
          "action_id": "action-000001",
          "output_pointer": "/facet_schema_id"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000001",
          "output_pointer": "/facet_schema_revision_id"
        },
        "binding": null
      }
    ],
    "actions": [
      {
        "ordinal": "0",
        "action_id": "action-000000",
        "command": "item_archetype.create",
        "object_key": "archetype:flight",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"intended_status\":\"active\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "f2a8940953febe71a35d1a1990ebe07e38fb8fb9f10907fcf14e93441cc1d6bf"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "6d02dcf207d79526bc9e0ee6922ca1f3d4517f2051ce54bc4e62171c6fc378eb"
        },
        "slots": []
      },
      {
        "ordinal": "1",
        "action_id": "action-000001",
        "command": "facet_schema.create",
        "object_key": "schema:flight_details",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"intended_status\":\"active\",\"schema_key\":\"flight_details\"}",
          "digest": "d2b7739eba2623e5d9e66538898655586b0fa612ffbbae5a8cb2de8d59216b91"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
          "digest": "b0e492717d2278e1c0809e31527b5db79b9035c5b73f239b18bb3886dcf26018"
        },
        "slots": []
      },
      {
        "ordinal": "2",
        "action_id": "action-000002",
        "command": "item_archetype.facet_binding.set",
        "object_key": "facet_binding:flight:flight",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"facet_key\":\"flight\",\"schema_ref\":{\"schema_key\":\"flight_details\"}}",
          "digest": "d305d7ca81d388049f2671fc9a37fd4bc79582b90fe4accba14c6dc4ab553a74"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"item_archetype_id\":null}",
          "digest": "07ad8df67d1e1b4d826a4a4e83ebc65e9ec10f47c6c35ed6c4574ca7ba47cfca"
        },
        "slots": [
          {
            "request_pointer": "/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          },
          {
            "request_pointer": "/item_archetype_id",
            "object_key": "archetype:flight",
            "field": "root"
          }
        ]
      },
      {
        "ordinal": "3",
        "action_id": "action-000003",
        "command": "notification_rendering_definition.create",
        "object_key": "rendering:flight_details",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"definition_key\":\"flight_details\",\"intended_status\":\"active\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"origin\"}]}}",
          "digest": "9a65eba8e3d6af38e8edd37b26cb731062ef7984b1a57ffa3f66b9a74854997c"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "b4f1594f65a3e1dd5859cc18ca046624a786cd3b99f70b40425e6887f233ec95"
        },
        "slots": [
          {
            "request_pointer": "/revision/selections/0/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          },
          {
            "request_pointer": "/revision/selections/1/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          }
        ]
      },
      {
        "ordinal": "4",
        "action_id": "action-000004",
        "command": "notification_profile.create",
        "object_key": "profile:synthetic_flight_details",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"intended_status\":\"active\",\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition_ref\":{\"definition_key\":\"flight_details\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "f1c625045b794ad603c16495f21cf9863d5bbe1c5cf007b316d1c5fc915f73ae"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":null,\"notification_rendering_definition_revision_id\":null},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "837d1feaa9a8267e54597068437621aca6e9945e3e6743bde0c6b2bf0f365372"
        },
        "slots": [
          {
            "request_pointer": "/revision/templates/1/rendering/definition/notification_rendering_definition_id",
            "object_key": "rendering:flight_details",
            "field": "root"
          },
          {
            "request_pointer": "/revision/templates/1/rendering/definition/notification_rendering_definition_revision_id",
            "object_key": "rendering:flight_details",
            "field": "revision"
          }
        ]
      },
      {
        "ordinal": "5",
        "action_id": "action-000005",
        "command": "notification_profile.binding.set",
        "object_key": "binding:flight",
        "change_kind": "create",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"binding_kind\":\"archetype_default\",\"notification_profile_key\":\"synthetic_flight_details\"}",
          "digest": "76bcc28de81de3d4bd28b247dd394ea58b1f5fcfcc923beaa69cade6c3e0f34b"
        },
        "expected": null,
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":null,\"notification_profile_id\":null,\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
          "digest": "ec791c66b8a06b29b4db3c83bb9d517526938dfc0ff657d8af666380445c70f0"
        },
        "slots": [
          {
            "request_pointer": "/item_archetype_id",
            "object_key": "archetype:flight",
            "field": "root"
          },
          {
            "request_pointer": "/notification_profile_id",
            "object_key": "profile:synthetic_flight_details",
            "field": "root"
          }
        ]
      }
    ],
    "decision_action_ids": [],
    "blocked_object_keys": [],
    "apply_eligible": true,
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-plan-digest.v2",
      "digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8"
    }
  },
  "approval": {
    "artifact_schema": "spine.pack-install-approval.v2",
    "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
    "approve_complete_plan": true,
    "acknowledge_single_operator": true,
    "authorized_update_action_ids": [],
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-approval-digest.v2",
      "digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c"
    }
  },
  "accepted_responses": [
    {
      "action_id": "action-000000",
      "command": "item_archetype.create",
      "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
        "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
        "digest": "274f463863aa60d727e5fbf1a89359b4c2522d42b55b078da04f5730031a3eaf"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_1",
        "effect": "item_archetype_created",
        "semantic_facts_hash": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "archetype:flight",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "archetype_1",
        "revision_id": "archetype_revision_1",
        "binding_id": null,
        "revision_contract": "spine.item-archetypes.v1",
        "value": {
          "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
          "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
        }
      }
    },
    {
      "action_id": "action-000001",
      "command": "facet_schema.create",
      "command_id": "spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
        "digest": "968a712302e1d0c22108ff2ef303bce341fd1f16f8d9c593598d0ac0fd5e4034"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
        "digest": "b9c41711428467c5a38d0361ae371594fe6260f290d48f6d7ef14e18844a2812"
      },
      "receipt": {
        "family": "facet",
        "command_receipt_id": "receipt_2",
        "effect": "facet_schema_created",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_2"
      },
      "post_observation": {
        "object_key": "schema:flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "schema_2",
        "revision_id": "schema_revision_2",
        "binding_id": null,
        "revision_contract": "spine.facet-schemas.v1",
        "value": {
          "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
          "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
        }
      }
    },
    {
      "action_id": "action-000002",
      "command": "item_archetype.facet_binding.set",
      "command_id": "spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
        "digest": "cff0f51114e5ca302c14a4e4860a45e7ce12aa7a223cc8314aa3cae1da5a9e55"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
        "digest": "4594ecc34e41437a6393408f6d950034ccbe1351d2cd9af340974ca25141bd73"
      },
      "receipt": {
        "family": "facet",
        "command_receipt_id": "receipt_3",
        "effect": "facet_binding_set",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_3"
      },
      "post_observation": {
        "object_key": "facet_binding:flight:flight",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "archetype_1",
        "revision_id": null,
        "binding_id": "facet_binding_binding_3",
        "revision_contract": null,
        "value": {
          "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
        }
      }
    },
    {
      "action_id": "action-000003",
      "command": "notification_rendering_definition.create",
      "command_id": "spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
        "digest": "12df1f2243b9495710d017dd88c02832c27d763d336bb99953628297bbe67c5f"
      },
      "response": {
        "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
        "digest": "cb042a379c1e9d1702ac6aaf3af84bc5307859b987696532610ca13a4eeaab2c"
      },
      "receipt": {
        "family": "rendering",
        "command_receipt_id": "receipt_4",
        "effect": "rendering_definition_created",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_4"
      },
      "post_observation": {
        "object_key": "rendering:flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "rendering_4",
        "revision_id": "rendering_revision_4",
        "binding_id": null,
        "revision_contract": "spine.notification-rendering-definitions.v1",
        "value": {
          "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
          "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
        }
      }
    },
    {
      "action_id": "action-000004",
      "command": "notification_profile.create",
      "command_id": "spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
        "digest": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
        "digest": "7f026c815f96e6e6d74bbbd95d34d6fc8d161b376e52370d3e0be18490227b82"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_5",
        "effect": "notification_profile_created",
        "semantic_facts_hash": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "profile:synthetic_flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "profile_5",
        "revision_id": "profile_revision_5",
        "binding_id": null,
        "revision_contract": "spine.notification-profiles.v2",
        "value": {
          "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
        }
      }
    },
    {
      "action_id": "action-000005",
      "command": "notification_profile.binding.set",
      "command_id": "spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
        "digest": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
        "digest": "f6fcac4a5c4cecf4653ec4422f9a15bc677951ba304edeb9ec840afd1d0a4bdd"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_6",
        "effect": "notification_profile_binding_set",
        "semantic_facts_hash": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "binding:flight",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "archetype_1",
        "revision_id": null,
        "binding_id": "binding_binding_6",
        "revision_contract": null,
        "value": {
          "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
          "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
        }
      }
    }
  ],
  "observations": [
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "536131d08f76699d0d1962a6dfa33b77cd1cc52ee1bd2693c28655afe1a483df"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "9e92730b4c3c70390ab94bbb3474882019a6c5d9e93dc668b329e064e8b3f295"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "876226b21960e354f2e21e20d685406bd96dea880a5fa29a6e7709cb2405d467"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "1782faad9a968c68521af1fe4744b1d58e597d699693afa069b1bf1389e1acc9"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "6b77dffb84d38c8e191956ebbf105b9abe06e41105a287768d15017fa2b8c261"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        }
      ],
      "digest": "043e5dea799be2d6311fac6a15b435cde4a04ba9ee1b4d233ca2ce9c49284077"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "ca12ca1fb56f106bf1871e82ac945da1da6454656e01463a790b3dd37e7a98cc"
    }
  ],
  "initial_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
    "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [],
    "unresolved_submission": null,
    "next_action_id": "action-000000",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "563009cb7b94d60c2b8e60f2f342beb31f5e32249a2b151c0b7981cb5779d024"
    }
  },
  "final_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
    "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.create",
        "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
          "digest": "274f463863aa60d727e5fbf1a89359b4c2522d42b55b078da04f5730031a3eaf"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_1",
          "effect": "item_archetype_created",
          "semantic_facts_hash": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        }
      },
      {
        "action_id": "action-000001",
        "command": "facet_schema.create",
        "command_id": "spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
          "digest": "968a712302e1d0c22108ff2ef303bce341fd1f16f8d9c593598d0ac0fd5e4034"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
          "digest": "b9c41711428467c5a38d0361ae371594fe6260f290d48f6d7ef14e18844a2812"
        },
        "receipt": {
          "family": "facet",
          "command_receipt_id": "receipt_2",
          "effect": "facet_schema_created",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_2"
        },
        "post_observation": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      },
      {
        "action_id": "action-000002",
        "command": "item_archetype.facet_binding.set",
        "command_id": "spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "cff0f51114e5ca302c14a4e4860a45e7ce12aa7a223cc8314aa3cae1da5a9e55"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
          "digest": "4594ecc34e41437a6393408f6d950034ccbe1351d2cd9af340974ca25141bd73"
        },
        "receipt": {
          "family": "facet",
          "command_receipt_id": "receipt_3",
          "effect": "facet_binding_set",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_3"
        },
        "post_observation": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        }
      },
      {
        "action_id": "action-000003",
        "command": "notification_rendering_definition.create",
        "command_id": "spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "12df1f2243b9495710d017dd88c02832c27d763d336bb99953628297bbe67c5f"
        },
        "response": {
          "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
          "digest": "cb042a379c1e9d1702ac6aaf3af84bc5307859b987696532610ca13a4eeaab2c"
        },
        "receipt": {
          "family": "rendering",
          "command_receipt_id": "receipt_4",
          "effect": "rendering_definition_created",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_4"
        },
        "post_observation": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        }
      },
      {
        "action_id": "action-000004",
        "command": "notification_profile.create",
        "command_id": "spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
          "digest": "7f026c815f96e6e6d74bbbd95d34d6fc8d161b376e52370d3e0be18490227b82"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_5",
          "effect": "notification_profile_created",
          "semantic_facts_hash": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        }
      },
      {
        "action_id": "action-000005",
        "command": "notification_profile.binding.set",
        "command_id": "spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
          "digest": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
          "digest": "f6fcac4a5c4cecf4653ec4422f9a15bc677951ba304edeb9ec840afd1d0a4bdd"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_6",
          "effect": "notification_profile_binding_set",
          "semantic_facts_hash": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        }
      }
    ],
    "unresolved_submission": null,
    "next_action_id": null,
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "63e519c747e2ab517a2222685d5eefa73805163924beb8989938e54416d9a102"
    }
  },
  "prepared_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
    "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.create",
        "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
          "digest": "274f463863aa60d727e5fbf1a89359b4c2522d42b55b078da04f5730031a3eaf"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_1",
          "effect": "item_archetype_created",
          "semantic_facts_hash": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        }
      }
    ],
    "unresolved_submission": {
      "action_id": "action-000001",
      "command_id": "spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15",
      "submission_state": "prepared_or_submitted",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
        "digest": "968a712302e1d0c22108ff2ef303bce341fd1f16f8d9c593598d0ac0fd5e4034"
      }
    },
    "next_action_id": "action-000001",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "55987f9b1d64028f825b40bf25d5f6f35dbb5a91aa3617147b0418fb57fff4be"
    }
  },
  "partial_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
      "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.create",
          "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
            "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
            "digest": "274f463863aa60d727e5fbf1a89359b4c2522d42b55b078da04f5730031a3eaf"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_1",
            "effect": "item_archetype_created",
            "semantic_facts_hash": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "archetype:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": "archetype_revision_1",
            "binding_id": null,
            "revision_contract": "spine.item-archetypes.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
              "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
            }
          }
        }
      ],
      "unresolved_submission": {
        "action_id": "action-000001",
        "command_id": "spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
          "digest": "968a712302e1d0c22108ff2ef303bce341fd1f16f8d9c593598d0ac0fd5e4034"
        }
      },
      "next_action_id": "action-000001",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "55987f9b1d64028f825b40bf25d5f6f35dbb5a91aa3617147b0418fb57fff4be"
      }
    },
    "state": "partial",
    "failure": {
      "action_id": "action-000001",
      "error": {
        "category": "partial_apply",
        "code": "uncertain_response",
        "message": "Synthetic response loss",
        "facts": []
      }
    },
    "unattempted_action_ids": [
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "4f501abd540221570b8ad79cd15663de37efe8e25222b841462a2489511d5b75"
    }
  },
  "empty_prefix_partial": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
      "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [],
      "unresolved_submission": {
        "action_id": "action-000000",
        "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
        }
      },
      "next_action_id": "action-000000",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "ffa4cbb897df05363b8b9e83f6e9342c5f219a1776fb014ed0154eab981099f9"
      }
    },
    "state": "partial",
    "failure": {
      "action_id": "action-000000",
      "error": {
        "category": "partial_apply",
        "code": "uncertain_response",
        "message": "Synthetic response loss",
        "facts": []
      }
    },
    "unattempted_action_ids": [
      "action-000001",
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "d11d31b038d7f64537a458b5943f004101b9d6e21880c625f8b97591cf669329"
    }
  },
  "apply_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
      "approval_digest": "f61afa0c8d2a4c532fc2e6ae4eb4c4ae8917672974d32136556c04dd1a531a0c",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.create",
          "command_id": "spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
            "digest": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_6e6e1cc801c3192b347eca75bbce095406571ffa49897e75342246f14bb89329\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
            "digest": "274f463863aa60d727e5fbf1a89359b4c2522d42b55b078da04f5730031a3eaf"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_1",
            "effect": "item_archetype_created",
            "semantic_facts_hash": "2223edd0e808880f636b251f5a8b827f0a2a8bcc7870e6dccb546ae50922705d",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "archetype:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": "archetype_revision_1",
            "binding_id": null,
            "revision_contract": "spine.item-archetypes.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
              "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
            }
          }
        },
        {
          "action_id": "action-000001",
          "command": "facet_schema.create",
          "command_id": "spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
            "digest": "968a712302e1d0c22108ff2ef303bce341fd1f16f8d9c593598d0ac0fd5e4034"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_f0aae1816d5204a24e075c2709f100e5135b6cb509eb81252d99def42f479a15\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
            "digest": "b9c41711428467c5a38d0361ae371594fe6260f290d48f6d7ef14e18844a2812"
          },
          "receipt": {
            "family": "facet",
            "command_receipt_id": "receipt_2",
            "effect": "facet_schema_created",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_2"
          },
          "post_observation": {
            "object_key": "schema:flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "schema_2",
            "revision_id": "schema_revision_2",
            "binding_id": null,
            "revision_contract": "spine.facet-schemas.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
              "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
            }
          }
        },
        {
          "action_id": "action-000002",
          "command": "item_archetype.facet_binding.set",
          "command_id": "spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "cff0f51114e5ca302c14a4e4860a45e7ce12aa7a223cc8314aa3cae1da5a9e55"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_874f6e3732229dc995f9522c192ad5493522ecc4ade1c854a5dfe9675c9144b3\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
            "digest": "4594ecc34e41437a6393408f6d950034ccbe1351d2cd9af340974ca25141bd73"
          },
          "receipt": {
            "family": "facet",
            "command_receipt_id": "receipt_3",
            "effect": "facet_binding_set",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_3"
          },
          "post_observation": {
            "object_key": "facet_binding:flight:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": null,
            "binding_id": "facet_binding_binding_3",
            "revision_contract": null,
            "value": {
              "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
              "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
            }
          }
        },
        {
          "action_id": "action-000003",
          "command": "notification_rendering_definition.create",
          "command_id": "spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
            "digest": "12df1f2243b9495710d017dd88c02832c27d763d336bb99953628297bbe67c5f"
          },
          "response": {
            "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_54e23ca7b8cd5140f626db86b04256a6e45479358d97600ca6454b4e186c80be\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
            "digest": "cb042a379c1e9d1702ac6aaf3af84bc5307859b987696532610ca13a4eeaab2c"
          },
          "receipt": {
            "family": "rendering",
            "command_receipt_id": "receipt_4",
            "effect": "rendering_definition_created",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_4"
          },
          "post_observation": {
            "object_key": "rendering:flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "rendering_4",
            "revision_id": "rendering_revision_4",
            "binding_id": null,
            "revision_contract": "spine.notification-rendering-definitions.v1",
            "value": {
              "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
              "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
            }
          }
        },
        {
          "action_id": "action-000004",
          "command": "notification_profile.create",
          "command_id": "spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_f1cc1c335beeb1258b69ddbd85b90f658478a9c438320ae55b5559e38e0daadc\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
            "digest": "7f026c815f96e6e6d74bbbd95d34d6fc8d161b376e52370d3e0be18490227b82"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_5",
            "effect": "notification_profile_created",
            "semantic_facts_hash": "cc7b11f0aba61f0050338c12adef422dbb8c50a2b854b69a8becadf926f495f2",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "profile:synthetic_flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "profile_5",
            "revision_id": "profile_revision_5",
            "binding_id": null,
            "revision_contract": "spine.notification-profiles.v2",
            "value": {
              "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
              "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
            }
          }
        },
        {
          "action_id": "action-000005",
          "command": "notification_profile.binding.set",
          "command_id": "spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
            "digest": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_a526ddeefbe658d04665851d6b030d4fd7b7978db52ed84415c4c3241a1aec7d\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
            "digest": "f6fcac4a5c4cecf4653ec4422f9a15bc677951ba304edeb9ec840afd1d0a4bdd"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_6",
            "effect": "notification_profile_binding_set",
            "semantic_facts_hash": "d05bf0488082f506f312d325eef9fb6980af2aa7a0a42188c998af2145f0570c",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "binding:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": null,
            "binding_id": "binding_binding_6",
            "revision_contract": null,
            "value": {
              "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
              "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
            }
          }
        }
      ],
      "unresolved_submission": null,
      "next_action_id": null,
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "63e519c747e2ab517a2222685d5eefa73805163924beb8989938e54416d9a102"
      }
    },
    "state": "applied",
    "failure": null,
    "unattempted_action_ids": [],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "f7b2512cf14d8d4f5b24902530c9f0df7ff001039a03466812b3d050cbafbb08"
    }
  },
  "verification": {
    "artifact_schema": "spine.pack-verification-result.v2",
    "plan_digest": "01afa6ca3e760308e62c9379196fe66edbbc6e0380fec5531b1b11587ceac7d8",
    "apply_result_digest": "f7b2512cf14d8d4f5b24902530c9f0df7ff001039a03466812b3d050cbafbb08",
    "pack": {
      "manifest_schema": "spine.pack-manifest.v2",
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.0",
      "status": "released",
      "manifest_digest": "29896a54b3c27059044cf8975de79eafe37f61fd268a0a7211c4949db298546a"
    },
    "target": {
      "host_name": "fixture.invalid",
      "spine_command": {
        "path": "/synthetic/bin/spine-command",
        "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
      },
      "ledger": {
        "kind": "path",
        "path": "/synthetic/ledger.db"
      }
    },
    "environment": {
      "runtime_version": "0.9.1",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schemas.v1",
        "spine.item-archetypes.v1",
        "spine.ledger-instance.v1",
        "spine.notification-profile-bindings.v1",
        "spine.notification-profile-catalog-cursor.v1",
        "spine.notification-profile-metadata-update.v1",
        "spine.notification-profile-readback.v1",
        "spine.notification-profiles.v1",
        "spine.notification-profiles.v2",
        "spine.notification-rendering-cursor.v1",
        "spine.notification-rendering-definitions.v1",
        "spine.notification-rendering-integration.v1",
        "spine.notification-rendering.v1",
        "spine.system-info.v3",
        "spine.tickerd-compatibility.v1"
      ]
    },
    "observation": {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "ca12ca1fb56f106bf1871e82ac945da1da6454656e01463a790b3dd37e7a98cc"
    },
    "closure": [
      "archetype:flight",
      "binding:flight",
      "facet_binding:flight:flight",
      "profile:synthetic_flight_details",
      "rendering:flight_details",
      "schema:flight_details"
    ],
    "object_results": [
      {
        "object_key": "archetype:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        }
      },
      {
        "object_key": "binding:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        }
      },
      {
        "object_key": "facet_binding:flight:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        }
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        }
      },
      {
        "object_key": "rendering:flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        }
      },
      {
        "object_key": "schema:flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      }
    ],
    "response_evidence": "complete",
    "receipt_readback": "captured_responses_only_spine_0.9.1",
    "disclosure": "separate_operator_configuration_required",
    "state": "verified",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-verification-result-digest.v2",
      "digest": "b6dd63f6d99075974c0acc5628e25b14f2e5b9c4a0f4586cbd26a03897d1c9d2"
    }
  },
  "envelope": {
    "artifact_schema": "spine.pack-installer-result.v2",
    "operation": "verify",
    "status": "success",
    "exit_code": "0",
    "artifact": {
      "path": "/synthetic/verification.json",
      "digest": "b6dd63f6d99075974c0acc5628e25b14f2e5b9c4a0f4586cbd26a03897d1c9d2"
    },
    "error": null
  }
}
```

### Spec 27: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/installer-v2/flight-update.json

Hash: 8ab30f967392fbd1ac1f4afdec08b9eb07171fd091818c2bd83ebcf320db4866

```markdown
{
  "manifest": {
    "manifest_schema": "spine.pack-manifest.v2",
    "pack": {
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.1",
      "status": "released"
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
          "display_name": "Synthetic revised flight",
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
        "display_name": "Synthetic revised flight reminders",
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
          "display_name": "Synthetic revised flight fields",
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
          "display_name": "Synthetic revised flight rendering",
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
      "digest": "dc68bd727a0318eec36c7f580913cab20fd6c1a1fb09dffd4da1c27a52b86bb7"
    }
  },
  "request": {
    "artifact_schema": "spine.pack-install-request.v2",
    "request": {
      "selection": {
        "mode": "archetypes",
        "archetype_keys": [
          "flight"
        ]
      },
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "target": {
        "host_name": "fixture.invalid",
        "spine_command": {
          "path": "/synthetic/bin/spine-command",
          "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
        },
        "ledger": {
          "kind": "path",
          "path": "/synthetic/ledger.db"
        }
      },
      "draft_posture": "reject"
    },
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-request-digest.v2",
      "digest": "ee2d217423d9ffa0b0a697933ff39c811f7032b3b099da4055af730a9641589e"
    }
  },
  "plan": {
    "artifact_schema": "spine.pack-install-plan.v2",
    "request_digest": "ee2d217423d9ffa0b0a697933ff39c811f7032b3b099da4055af730a9641589e",
    "request": {
      "selection": {
        "mode": "archetypes",
        "archetype_keys": [
          "flight"
        ]
      },
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "target": {
        "host_name": "fixture.invalid",
        "spine_command": {
          "path": "/synthetic/bin/spine-command",
          "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
        },
        "ledger": {
          "kind": "path",
          "path": "/synthetic/ledger.db"
        }
      },
      "draft_posture": "reject"
    },
    "pack": {
      "manifest_schema": "spine.pack-manifest.v2",
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.1",
      "status": "released",
      "manifest_digest": "dc68bd727a0318eec36c7f580913cab20fd6c1a1fb09dffd4da1c27a52b86bb7"
    },
    "closure": [
      "archetype:flight",
      "binding:flight",
      "facet_binding:flight:flight",
      "profile:synthetic_flight_details",
      "rendering:flight_details",
      "schema:flight_details"
    ],
    "environment": {
      "runtime_version": "0.9.1",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schemas.v1",
        "spine.item-archetypes.v1",
        "spine.ledger-instance.v1",
        "spine.notification-profile-bindings.v1",
        "spine.notification-profile-catalog-cursor.v1",
        "spine.notification-profile-metadata-update.v1",
        "spine.notification-profile-readback.v1",
        "spine.notification-profiles.v1",
        "spine.notification-profiles.v2",
        "spine.notification-rendering-cursor.v1",
        "spine.notification-rendering-definitions.v1",
        "spine.notification-rendering-integration.v1",
        "spine.notification-rendering.v1",
        "spine.system-info.v3",
        "spine.tickerd-compatibility.v1"
      ]
    },
    "required_execution_contracts": [
      "spine.archetype-facet-bindings.v1",
      "spine.canonical-json.v1",
      "spine.facet-cursor.v1",
      "spine.facet-schemas.v1",
      "spine.item-archetypes.v1",
      "spine.ledger-instance.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profile-catalog-cursor.v1",
      "spine.notification-profile-metadata-update.v1",
      "spine.notification-profile-readback.v1",
      "spine.notification-profiles.v1",
      "spine.notification-profiles.v2",
      "spine.notification-rendering-cursor.v1",
      "spine.notification-rendering-definitions.v1",
      "spine.notification-rendering-integration.v1",
      "spine.system-info.v3",
      "spine.tickerd-compatibility.v1"
    ],
    "observation": {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "ca12ca1fb56f106bf1871e82ac945da1da6454656e01463a790b3dd37e7a98cc"
    },
    "classifications": [
      {
        "object_key": "archetype:flight",
        "classification": "drifted",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"intended_status\":\"active\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "ff721550079081dce08c903ebc9114ef3885cc4c0bcc17b9b04a9b68976b32b3"
        },
        "observed": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        "blocked_reason": null
      },
      {
        "object_key": "binding:flight",
        "classification": "equivalent",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"binding_kind\":\"archetype_default\",\"notification_profile_key\":\"synthetic_flight_details\"}",
          "digest": "76bcc28de81de3d4bd28b247dd394ea58b1f5fcfcc923beaa69cade6c3e0f34b"
        },
        "observed": {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        "blocked_reason": null
      },
      {
        "object_key": "facet_binding:flight:flight",
        "classification": "drifted",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"facet_key\":\"flight\",\"schema_ref\":{\"schema_key\":\"flight_details\"}}",
          "digest": "d305d7ca81d388049f2671fc9a37fd4bc79582b90fe4accba14c6dc4ab553a74"
        },
        "observed": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        "blocked_reason": null
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "classification": "drifted",
        "desired": {
          "canonical_json": "{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\",\"intended_status\":\"active\",\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition_ref\":{\"definition_key\":\"flight_details\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "ec10c68c1d61ce2afde0f8a59f17ef81902c3affb6d9ad245ef6372ae1c03219"
        },
        "observed": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        "blocked_reason": null
      },
      {
        "object_key": "rendering:flight_details",
        "classification": "drifted",
        "desired": {
          "canonical_json": "{\"definition_key\":\"flight_details\",\"intended_status\":\"active\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"origin\"}]}}",
          "digest": "c8f989139167f5f859772336b1a33c248ae49be0e49e81cdb7e47dc3d462920b"
        },
        "observed": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        "blocked_reason": null
      },
      {
        "object_key": "schema:flight_details",
        "classification": "drifted",
        "desired": {
          "canonical_json": "{\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"intended_status\":\"active\",\"schema_key\":\"flight_details\"}",
          "digest": "4f86770c69de5be7f36cdb09a3e88aad8ccc40ba0769782c4134a09cab04d994"
        },
        "observed": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        },
        "blocked_reason": null
      }
    ],
    "resolutions": [
      {
        "object_key": "archetype:flight",
        "root": {
          "kind": "observed",
          "object_key": "archetype:flight",
          "field": "root",
          "value": "archetype_1"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000000",
          "output_pointer": "/item_archetype_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "binding:flight",
        "root": {
          "kind": "observed",
          "object_key": "archetype:flight",
          "field": "root",
          "value": "archetype_1"
        },
        "revision": null,
        "binding": {
          "kind": "observed",
          "object_key": "binding:flight",
          "field": "binding",
          "value": "binding_binding_6"
        }
      },
      {
        "object_key": "facet_binding:flight:flight",
        "root": {
          "kind": "observed",
          "object_key": "archetype:flight",
          "field": "root",
          "value": "archetype_1"
        },
        "revision": null,
        "binding": {
          "kind": "action_result",
          "action_id": "action-000002",
          "output_pointer": "/facet_binding_id"
        }
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "root": {
          "kind": "observed",
          "object_key": "profile:synthetic_flight_details",
          "field": "root",
          "value": "profile_5"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000005",
          "output_pointer": "/notification_profile_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "rendering:flight_details",
        "root": {
          "kind": "observed",
          "object_key": "rendering:flight_details",
          "field": "root",
          "value": "rendering_4"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000003",
          "output_pointer": "/record/notification_rendering_definition_revision_id"
        },
        "binding": null
      },
      {
        "object_key": "schema:flight_details",
        "root": {
          "kind": "observed",
          "object_key": "schema:flight_details",
          "field": "root",
          "value": "schema_2"
        },
        "revision": {
          "kind": "action_result",
          "action_id": "action-000001",
          "output_pointer": "/facet_schema_revision_id"
        },
        "binding": null
      }
    ],
    "actions": [
      {
        "ordinal": "0",
        "action_id": "action-000000",
        "command": "item_archetype.revise",
        "object_key": "archetype:flight",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"intended_status\":\"active\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "ff721550079081dce08c903ebc9114ef3885cc4c0bcc17b9b04a9b68976b32b3"
        },
        "expected": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "2b7112a8be81b8549239b99bc154ea4151602fd8e1fdcd8eafe099976b428ee8"
        },
        "slots": []
      },
      {
        "ordinal": "1",
        "action_id": "action-000001",
        "command": "facet_schema.publish",
        "object_key": "schema:flight_details",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"intended_status\":\"active\",\"schema_key\":\"flight_details\"}",
          "digest": "4f86770c69de5be7f36cdb09a3e88aad8ccc40ba0769782c4134a09cab04d994"
        },
        "expected": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
          "digest": "cb3b9d085417ca28cba03b5eb27227d4a7cc9470b334aacf7254e5024c093687"
        },
        "slots": []
      },
      {
        "ordinal": "2",
        "action_id": "action-000002",
        "command": "item_archetype.facet_binding.set",
        "object_key": "facet_binding:flight:flight",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"archetype_key\":\"flight\",\"facet_key\":\"flight\",\"schema_ref\":{\"schema_key\":\"flight_details\"}}",
          "digest": "d305d7ca81d388049f2671fc9a37fd4bc79582b90fe4accba14c6dc4ab553a74"
        },
        "expected": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"item_archetype_id\":null}",
          "digest": "7737cd6ea44045e98931d5ff6b032e8f773305b6d0d5505189d33fe33529ef65"
        },
        "slots": [
          {
            "request_pointer": "/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          },
          {
            "request_pointer": "/item_archetype_id",
            "object_key": "archetype:flight",
            "field": "root"
          }
        ]
      },
      {
        "ordinal": "3",
        "action_id": "action-000003",
        "command": "notification_rendering_definition.publish",
        "object_key": "rendering:flight_details",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"definition_key\":\"flight_details\",\"intended_status\":\"active\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"schema_ref\":{\"schema_key\":\"flight_details\"},\"selection_key\":\"origin\"}]}}",
          "digest": "c8f989139167f5f859772336b1a33c248ae49be0e49e81cdb7e47dc3d462920b"
        },
        "expected": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":null,\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "ecdc625b2bda4ca9d5316eb3e294b24ce01a5b640c14f173e13208e27b29933e"
        },
        "slots": [
          {
            "request_pointer": "/revision/selections/0/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          },
          {
            "request_pointer": "/revision/selections/1/facet_schema_revision_id",
            "object_key": "schema:flight_details",
            "field": "revision"
          }
        ]
      },
      {
        "ordinal": "4",
        "action_id": "action-000004",
        "command": "notification_profile.metadata.update",
        "object_key": "profile:synthetic_flight_details",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\",\"intended_status\":\"active\",\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition_ref\":{\"definition_key\":\"flight_details\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "ec10c68c1d61ce2afde0f8a59f17ef81902c3affb6d9ad245ef6372ae1c03219"
        },
        "expected": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
          "digest": "445ea034023892e70df16ac8539d925c3ed967df46ade8988bd7bcf6a8ad600a"
        },
        "slots": []
      },
      {
        "ordinal": "5",
        "action_id": "action-000005",
        "command": "notification_profile.revise",
        "object_key": "profile:synthetic_flight_details",
        "change_kind": "update",
        "desired": {
          "canonical_json": "{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\",\"intended_status\":\"active\",\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition_ref\":{\"definition_key\":\"flight_details\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "ec10c68c1d61ce2afde0f8a59f17ef81902c3affb6d9ad245ef6372ae1c03219"
        },
        "expected": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        "request_template": {
          "canonical_json": "{\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":null,\"notification_rendering_definition_revision_id\":null},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "dac9598114bc1074d7d128070bc4bd82500eceb02935ce3cb209139166de9e74"
        },
        "slots": [
          {
            "request_pointer": "/revision/templates/1/rendering/definition/notification_rendering_definition_id",
            "object_key": "rendering:flight_details",
            "field": "root"
          },
          {
            "request_pointer": "/revision/templates/1/rendering/definition/notification_rendering_definition_revision_id",
            "object_key": "rendering:flight_details",
            "field": "revision"
          }
        ]
      }
    ],
    "decision_action_ids": [
      "action-000000",
      "action-000001",
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "blocked_object_keys": [],
    "apply_eligible": true,
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-plan-digest.v2",
      "digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b"
    }
  },
  "approval": {
    "artifact_schema": "spine.pack-install-approval.v2",
    "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
    "approve_complete_plan": true,
    "acknowledge_single_operator": true,
    "authorized_update_action_ids": [
      "action-000000",
      "action-000001",
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-install-approval-digest.v2",
      "digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27"
    }
  },
  "accepted_responses": [
    {
      "action_id": "action-000000",
      "command": "item_archetype.revise",
      "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
        "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
        "digest": "7358595b547993686c34a71532667a0d91b9c4cf7b90c2b9fbf2bda70160519c"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_101",
        "effect": "item_archetype_revised",
        "semantic_facts_hash": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "archetype:flight",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "archetype_1",
        "revision_id": "archetype_revision_101",
        "binding_id": null,
        "revision_contract": "spine.item-archetypes.v1",
        "value": {
          "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
          "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
        }
      }
    },
    {
      "action_id": "action-000001",
      "command": "facet_schema.publish",
      "command_id": "spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
        "digest": "a1beb1e0073996d5418e4da6ef0b3306df0e2f061584ce61135c3928539a595e"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
        "digest": "a7b52c3cb7105214f94c6056dfc15e3e44de38e25bf0bf5f64c0562dfe7ebf63"
      },
      "receipt": {
        "family": "facet",
        "command_receipt_id": "receipt_102",
        "effect": "facet_schema_published",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_102"
      },
      "post_observation": {
        "object_key": "schema:flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "schema_2",
        "revision_id": "schema_revision_102",
        "binding_id": null,
        "revision_contract": "spine.facet-schemas.v1",
        "value": {
          "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
          "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
        }
      }
    },
    {
      "action_id": "action-000002",
      "command": "item_archetype.facet_binding.set",
      "command_id": "spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
        "digest": "544b92de1e11da39dad831d8dfd68c2bcede9e1f44d5af3e61498ba6232bee7a"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
        "digest": "881d35e56bbbf5e2a2eb0c25e240e1221e960396e4fb2467b422a2d729f34118"
      },
      "receipt": {
        "family": "facet",
        "command_receipt_id": "receipt_103",
        "effect": "facet_binding_set",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_103"
      },
      "post_observation": {
        "object_key": "facet_binding:flight:flight",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "archetype_1",
        "revision_id": null,
        "binding_id": "facet_binding_binding_103",
        "revision_contract": null,
        "value": {
          "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
        }
      }
    },
    {
      "action_id": "action-000003",
      "command": "notification_rendering_definition.publish",
      "command_id": "spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
        "digest": "8ec673bd18f5bdc58d5e45eef6dc59cac30419a1d5469e831f5014cb180fe49a"
      },
      "response": {
        "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
        "digest": "49e7aeac031be231cccc8d38c2f65e90e3ca91d03e8a936c170ff502043cd222"
      },
      "receipt": {
        "family": "rendering",
        "command_receipt_id": "receipt_104",
        "effect": "rendering_definition_published",
        "changed": true,
        "replayed": false,
        "audit_id": "audit_104"
      },
      "post_observation": {
        "object_key": "rendering:flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "rendering_4",
        "revision_id": "rendering_revision_104",
        "binding_id": null,
        "revision_contract": "spine.notification-rendering-definitions.v1",
        "value": {
          "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
          "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
        }
      }
    },
    {
      "action_id": "action-000004",
      "command": "notification_profile.metadata.update",
      "command_id": "spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
        "digest": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
        "digest": "525cc50981b6b8dd19f5d6218c02eb9785492ef2eb035c82b690a38e5be89ed1"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_105",
        "effect": "notification_profile_metadata_updated",
        "semantic_facts_hash": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "profile:synthetic_flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "profile_5",
        "revision_id": "profile_revision_5",
        "binding_id": null,
        "revision_contract": "spine.notification-profiles.v2",
        "value": {
          "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
        }
      }
    },
    {
      "action_id": "action-000005",
      "command": "notification_profile.revise",
      "command_id": "spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
        "digest": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
        "digest": "5df6b8f271b9a7d08df0534786bd97dd46f3b824673d1bc3a3fc90a089b6a0f4"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_106",
        "effect": "notification_profile_revised",
        "semantic_facts_hash": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450",
        "created_at_utc": "2035-02-01T12:00:00Z"
      },
      "post_observation": {
        "object_key": "profile:synthetic_flight_details",
        "owner": {
          "owner_kind": "subject",
          "owner_subject_id": "synthetic-owner"
        },
        "status": "active",
        "root_id": "profile_5",
        "revision_id": "profile_revision_106",
        "binding_id": null,
        "revision_contract": "spine.notification-profiles.v2",
        "value": {
          "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
        }
      }
    }
  ],
  "observations": [
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "6b277d56555a33e6f3c1ea11ee80e4c3cb98d4dd14e4f343ce092d81f8903530"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "ca12ca1fb56f106bf1871e82ac945da1da6454656e01463a790b3dd37e7a98cc"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "145f9c592bd0c4f9f00bc8f4d4b033f33e38919bd204ea9f25822f718b63854e"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_3",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "f12313557c80caa275da2b6f4a5ff8941ae1f707a0f86bcc2a9939c150e9e77c"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "0dabfbfaf07c4a90fb158cf04eb3ee3143eebcfcfdb019f1ee050848071dcf01"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "b84415cfcd78c0a4dfaa35e4884c8eb8a1cab72b04e803c0d6410080548e9490"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "0f07443cd1794106253fe23adefdd6c74ec5f3d6e5e0a75a651ae1c54f9f2409"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "b193173e4bc6fe96d074e4b76d11502f550f391aba8e1b66e0c685a2028080e2"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "7d8cf3bbb69bad708b18ef6985b68fce5671d6799f863eb56dea111685daf7d9"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "1d41ac6b76c2aa48fe7bac7341b51efcb5e3445f370b10dfa3848d9c85a78cc3"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "d2034924fe607c4f65c60ad578cf229ed0712e4f30eb00b58edaf7f13d3dc5b2"
    },
    {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_106",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "5fb316e90b3d46eab1ea2893616f59aa00536a97df1d92d9832c57d9bf88403c"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "4276146d155c68db88587c3a0a0f698143a3a145620c5b47906be3209beb0f8d"
    }
  ],
  "initial_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
    "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [],
    "unresolved_submission": null,
    "next_action_id": "action-000000",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "83dbfd4de1a418ca0cbc039ce185b36751e6a45bb044ab6bca815263e781f66b"
    }
  },
  "final_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
    "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.revise",
        "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
          "digest": "7358595b547993686c34a71532667a0d91b9c4cf7b90c2b9fbf2bda70160519c"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_101",
          "effect": "item_archetype_revised",
          "semantic_facts_hash": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        }
      },
      {
        "action_id": "action-000001",
        "command": "facet_schema.publish",
        "command_id": "spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
          "digest": "a1beb1e0073996d5418e4da6ef0b3306df0e2f061584ce61135c3928539a595e"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
          "digest": "a7b52c3cb7105214f94c6056dfc15e3e44de38e25bf0bf5f64c0562dfe7ebf63"
        },
        "receipt": {
          "family": "facet",
          "command_receipt_id": "receipt_102",
          "effect": "facet_schema_published",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_102"
        },
        "post_observation": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      },
      {
        "action_id": "action-000002",
        "command": "item_archetype.facet_binding.set",
        "command_id": "spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "544b92de1e11da39dad831d8dfd68c2bcede9e1f44d5af3e61498ba6232bee7a"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
          "digest": "881d35e56bbbf5e2a2eb0c25e240e1221e960396e4fb2467b422a2d729f34118"
        },
        "receipt": {
          "family": "facet",
          "command_receipt_id": "receipt_103",
          "effect": "facet_binding_set",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_103"
        },
        "post_observation": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        }
      },
      {
        "action_id": "action-000003",
        "command": "notification_rendering_definition.publish",
        "command_id": "spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "8ec673bd18f5bdc58d5e45eef6dc59cac30419a1d5469e831f5014cb180fe49a"
        },
        "response": {
          "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
          "digest": "49e7aeac031be231cccc8d38c2f65e90e3ca91d03e8a936c170ff502043cd222"
        },
        "receipt": {
          "family": "rendering",
          "command_receipt_id": "receipt_104",
          "effect": "rendering_definition_published",
          "changed": true,
          "replayed": false,
          "audit_id": "audit_104"
        },
        "post_observation": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        }
      },
      {
        "action_id": "action-000004",
        "command": "notification_profile.metadata.update",
        "command_id": "spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
          "digest": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
          "digest": "525cc50981b6b8dd19f5d6218c02eb9785492ef2eb035c82b690a38e5be89ed1"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_105",
          "effect": "notification_profile_metadata_updated",
          "semantic_facts_hash": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
          }
        }
      },
      {
        "action_id": "action-000005",
        "command": "notification_profile.revise",
        "command_id": "spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
          "digest": "5df6b8f271b9a7d08df0534786bd97dd46f3b824673d1bc3a3fc90a089b6a0f4"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_106",
          "effect": "notification_profile_revised",
          "semantic_facts_hash": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_106",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
          }
        }
      }
    ],
    "unresolved_submission": null,
    "next_action_id": null,
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "cf873a1a689ea80cd443d66c31b9ef47d9ca03e947fa46c08780ad4a52e2c52d"
    }
  },
  "prepared_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
    "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.revise",
        "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
          "digest": "7358595b547993686c34a71532667a0d91b9c4cf7b90c2b9fbf2bda70160519c"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_101",
          "effect": "item_archetype_revised",
          "semantic_facts_hash": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b",
          "created_at_utc": "2035-02-01T12:00:00Z"
        },
        "post_observation": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        }
      }
    ],
    "unresolved_submission": {
      "action_id": "action-000001",
      "command_id": "spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a",
      "submission_state": "prepared_or_submitted",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
        "digest": "a1beb1e0073996d5418e4da6ef0b3306df0e2f061584ce61135c3928539a595e"
      }
    },
    "next_action_id": "action-000001",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "44b7933dbaaf80598d5c87e33eaa6f35181d32a1b8842ce7a6a8caf24e8615b5"
    }
  },
  "partial_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
      "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.revise",
          "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
            "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
            "digest": "7358595b547993686c34a71532667a0d91b9c4cf7b90c2b9fbf2bda70160519c"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_101",
            "effect": "item_archetype_revised",
            "semantic_facts_hash": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "archetype:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": "archetype_revision_101",
            "binding_id": null,
            "revision_contract": "spine.item-archetypes.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
              "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
            }
          }
        }
      ],
      "unresolved_submission": {
        "action_id": "action-000001",
        "command_id": "spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
          "digest": "a1beb1e0073996d5418e4da6ef0b3306df0e2f061584ce61135c3928539a595e"
        }
      },
      "next_action_id": "action-000001",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "44b7933dbaaf80598d5c87e33eaa6f35181d32a1b8842ce7a6a8caf24e8615b5"
      }
    },
    "state": "partial",
    "failure": {
      "action_id": "action-000001",
      "error": {
        "category": "partial_apply",
        "code": "uncertain_response",
        "message": "Synthetic response loss",
        "facts": []
      }
    },
    "unattempted_action_ids": [
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "d58ba99a9a577582068ae1c823b65c71446ac784f63000200405df31f2a4667e"
    }
  },
  "empty_prefix_partial": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
      "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [],
      "unresolved_submission": {
        "action_id": "action-000000",
        "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
        }
      },
      "next_action_id": "action-000000",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "d01fd875a227549aca6ec89ce54ea7af5e06ed402ab2fdf94bb7640702546288"
      }
    },
    "state": "partial",
    "failure": {
      "action_id": "action-000000",
      "error": {
        "category": "partial_apply",
        "code": "uncertain_response",
        "message": "Synthetic response loss",
        "facts": []
      }
    },
    "unattempted_action_ids": [
      "action-000001",
      "action-000002",
      "action-000003",
      "action-000004",
      "action-000005"
    ],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "5cc16f455a536027cc37e50ee9cf77b817f679a49415581a44a6dc620c7392f7"
    }
  },
  "apply_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
      "approval_digest": "cf1f4db758a006415216358f142b7f10e3bb35fe982ee74d27f97bd2772efa27",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.revise",
          "command_id": "spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
            "digest": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_dfd755212e433632584474f48a12d3cdd9f7cecdae169b91ae3a9e9c36e3667a\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
            "digest": "7358595b547993686c34a71532667a0d91b9c4cf7b90c2b9fbf2bda70160519c"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_101",
            "effect": "item_archetype_revised",
            "semantic_facts_hash": "1e70741abe215d49443afbb71f9c040381146ff13b198415969cf6b7d917649b",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "archetype:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": "archetype_revision_101",
            "binding_id": null,
            "revision_contract": "spine.item-archetypes.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
              "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
            }
          }
        },
        {
          "action_id": "action-000001",
          "command": "facet_schema.publish",
          "command_id": "spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
            "digest": "a1beb1e0073996d5418e4da6ef0b3306df0e2f061584ce61135c3928539a595e"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_97f727d4d7e7bb326ce297118de3340c6f886b3c74ee137f596492ac53b20b0a\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
            "digest": "a7b52c3cb7105214f94c6056dfc15e3e44de38e25bf0bf5f64c0562dfe7ebf63"
          },
          "receipt": {
            "family": "facet",
            "command_receipt_id": "receipt_102",
            "effect": "facet_schema_published",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_102"
          },
          "post_observation": {
            "object_key": "schema:flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "schema_2",
            "revision_id": "schema_revision_102",
            "binding_id": null,
            "revision_contract": "spine.facet-schemas.v1",
            "value": {
              "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
              "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
            }
          }
        },
        {
          "action_id": "action-000002",
          "command": "item_archetype.facet_binding.set",
          "command_id": "spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "544b92de1e11da39dad831d8dfd68c2bcede9e1f44d5af3e61498ba6232bee7a"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_e1d94e04eaa5054372a4408a43ee5d6f8a009054e58699fa294bff20a8316298\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
            "digest": "881d35e56bbbf5e2a2eb0c25e240e1221e960396e4fb2467b422a2d729f34118"
          },
          "receipt": {
            "family": "facet",
            "command_receipt_id": "receipt_103",
            "effect": "facet_binding_set",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_103"
          },
          "post_observation": {
            "object_key": "facet_binding:flight:flight",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "archetype_1",
            "revision_id": null,
            "binding_id": "facet_binding_binding_103",
            "revision_contract": null,
            "value": {
              "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
              "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
            }
          }
        },
        {
          "action_id": "action-000003",
          "command": "notification_rendering_definition.publish",
          "command_id": "spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
            "digest": "8ec673bd18f5bdc58d5e45eef6dc59cac30419a1d5469e831f5014cb180fe49a"
          },
          "response": {
            "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
            "digest": "49e7aeac031be231cccc8d38c2f65e90e3ca91d03e8a936c170ff502043cd222"
          },
          "receipt": {
            "family": "rendering",
            "command_receipt_id": "receipt_104",
            "effect": "rendering_definition_published",
            "changed": true,
            "replayed": false,
            "audit_id": "audit_104"
          },
          "post_observation": {
            "object_key": "rendering:flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "rendering_4",
            "revision_id": "rendering_revision_104",
            "binding_id": null,
            "revision_contract": "spine.notification-rendering-definitions.v1",
            "value": {
              "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
              "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
            }
          }
        },
        {
          "action_id": "action-000004",
          "command": "notification_profile.metadata.update",
          "command_id": "spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
            "digest": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_61cc6596b9d4343121e03e6512ae8afdd9b62f144f7ad4e7da17bb9c39e33ade\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
            "digest": "525cc50981b6b8dd19f5d6218c02eb9785492ef2eb035c82b690a38e5be89ed1"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_105",
            "effect": "notification_profile_metadata_updated",
            "semantic_facts_hash": "c46b4be87dbf28d6f0a2809b158e78ba5ef6fc6748e4a408ea4f5455968bffc9",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "profile:synthetic_flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "profile_5",
            "revision_id": "profile_revision_5",
            "binding_id": null,
            "revision_contract": "spine.notification-profiles.v2",
            "value": {
              "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
              "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
            }
          }
        },
        {
          "action_id": "action-000005",
          "command": "notification_profile.revise",
          "command_id": "spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_89b5f9e391778c7c6e6b0f23f0be1f171af235b8fe901e3aafe53fe6a60736d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
            "digest": "5df6b8f271b9a7d08df0534786bd97dd46f3b824673d1bc3a3fc90a089b6a0f4"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_106",
            "effect": "notification_profile_revised",
            "semantic_facts_hash": "f89e1ad16f1e02fa82992cfb789fee869ac5939946a41afb00894b3adb1d7450",
            "created_at_utc": "2035-02-01T12:00:00Z"
          },
          "post_observation": {
            "object_key": "profile:synthetic_flight_details",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "synthetic-owner"
            },
            "status": "active",
            "root_id": "profile_5",
            "revision_id": "profile_revision_106",
            "binding_id": null,
            "revision_contract": "spine.notification-profiles.v2",
            "value": {
              "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
              "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
            }
          }
        }
      ],
      "unresolved_submission": null,
      "next_action_id": null,
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "cf873a1a689ea80cd443d66c31b9ef47d9ca03e947fa46c08780ad4a52e2c52d"
      }
    },
    "state": "applied",
    "failure": null,
    "unattempted_action_ids": [],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "d011a520676924ccf197a14064d2ae25109023e26d1ad52a2149d48c46d74917"
    }
  },
  "verification": {
    "artifact_schema": "spine.pack-verification-result.v2",
    "plan_digest": "f03812abfca1538ffb72379f7b6901673e4547b7e323bfa04c589977afa9d54b",
    "apply_result_digest": "d011a520676924ccf197a14064d2ae25109023e26d1ad52a2149d48c46d74917",
    "pack": {
      "manifest_schema": "spine.pack-manifest.v2",
      "pack_id": "synthetic-flight-execution",
      "version": "1.0.1",
      "status": "released",
      "manifest_digest": "dc68bd727a0318eec36c7f580913cab20fd6c1a1fb09dffd4da1c27a52b86bb7"
    },
    "target": {
      "host_name": "fixture.invalid",
      "spine_command": {
        "path": "/synthetic/bin/spine-command",
        "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
      },
      "ledger": {
        "kind": "path",
        "path": "/synthetic/ledger.db"
      }
    },
    "environment": {
      "runtime_version": "0.9.1",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schemas.v1",
        "spine.item-archetypes.v1",
        "spine.ledger-instance.v1",
        "spine.notification-profile-bindings.v1",
        "spine.notification-profile-catalog-cursor.v1",
        "spine.notification-profile-metadata-update.v1",
        "spine.notification-profile-readback.v1",
        "spine.notification-profiles.v1",
        "spine.notification-profiles.v2",
        "spine.notification-rendering-cursor.v1",
        "spine.notification-rendering-definitions.v1",
        "spine.notification-rendering-integration.v1",
        "spine.notification-rendering.v1",
        "spine.system-info.v3",
        "spine.tickerd-compatibility.v1"
      ]
    },
    "observation": {
      "owner": {
        "owner_kind": "subject",
        "owner_subject_id": "synthetic-owner"
      },
      "entries": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        },
        {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        },
        {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_106",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      ],
      "historical_revisions": [
        {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_1",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}",
            "digest": "dd9483a4ee700cd496de2a7f8a4091a58f21b22fa28068aad26d63651301a978"
          }
        },
        {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_5",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "7bfbc1abe3edb7f9c3f43861644fb2f669e5ea6e9da90cf0ad82e03ef40c79be"
          }
        },
        {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_4",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "a0d1d68b9f11085cf9618516cca46a28092bdfd70c2d2809524773d51f698f64"
          }
        },
        {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_2",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "3e31e0d4d0f94d5adce1c09287cb30e63fdcdd9514e6b3a90de75bd14764f862"
          }
        }
      ],
      "public_catalog_snapshots": [
        {
          "catalog": "archetypes",
          "digest": "9ca195808fb3be8b88996a63408d596d3a27af55d92028a100d6c4789f2ca139"
        },
        {
          "catalog": "profiles",
          "digest": "5fb316e90b3d46eab1ea2893616f59aa00536a97df1d92d9832c57d9bf88403c"
        },
        {
          "catalog": "bindings",
          "digest": "f5b5fdc226b9964c49d16f01b1915ce3e7152109886040a7ce00fb4a56840f70"
        }
      ],
      "digest": "4276146d155c68db88587c3a0a0f698143a3a145620c5b47906be3209beb0f8d"
    },
    "closure": [
      "archetype:flight",
      "binding:flight",
      "facet_binding:flight:flight",
      "profile:synthetic_flight_details",
      "rendering:flight_details",
      "schema:flight_details"
    ],
    "object_results": [
      {
        "object_key": "archetype:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "archetype:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": "archetype_revision_101",
          "binding_id": null,
          "revision_contract": "spine.item-archetypes.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}",
            "digest": "60f5e002f9b2c5ae9d215da7c77ca3b6715601a3588a947a185aa28206e01404"
          }
        }
      },
      {
        "object_key": "binding:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "binding:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "binding_binding_6",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\"}",
            "digest": "8dbd7cb63d655b3afd590e855c382ea8fb18d86db6a1303a127a88244a6fe8d3"
          }
        }
      },
      {
        "object_key": "facet_binding:flight:flight",
        "state": "equivalent",
        "observed": {
          "object_key": "facet_binding:flight:flight",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "archetype_1",
          "revision_id": null,
          "binding_id": "facet_binding_binding_103",
          "revision_contract": null,
          "value": {
            "canonical_json": "{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "9c7eea933e8af52f493eb1e7becc7e59b10a943e809d65942b1f52bcfa0efac2"
          }
        }
      },
      {
        "object_key": "profile:synthetic_flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "profile:synthetic_flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "profile_5",
          "revision_id": "profile_revision_106",
          "binding_id": null,
          "revision_contract": "spine.notification-profiles.v2",
          "value": {
            "canonical_json": "{\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "e95361ef0ef8d698b1423f3d855323a75874e30265b46300d88fbbd476cd5ce3"
          }
        }
      },
      {
        "object_key": "rendering:flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "rendering:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "rendering_4",
          "revision_id": "rendering_revision_104",
          "binding_id": null,
          "revision_contract": "spine.notification-rendering-definitions.v1",
          "value": {
            "canonical_json": "{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}",
            "digest": "37929e452e02b12e4c2f9664f74c287649aab1dea926e14d94c114aa823558df"
          }
        }
      },
      {
        "object_key": "schema:flight_details",
        "state": "equivalent",
        "observed": {
          "object_key": "schema:flight_details",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "synthetic-owner"
          },
          "status": "active",
          "root_id": "schema_2",
          "revision_id": "schema_revision_102",
          "binding_id": null,
          "revision_contract": "spine.facet-schemas.v1",
          "value": {
            "canonical_json": "{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]}",
            "digest": "8eb7676508c4bcba759591a1db40effcf95f0beca7f6a363c9976ee3fd9880de"
          }
        }
      }
    ],
    "response_evidence": "complete",
    "receipt_readback": "captured_responses_only_spine_0.9.1",
    "disclosure": "separate_operator_configuration_required",
    "state": "verified",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-verification-result-digest.v2",
      "digest": "5b7fdda74d8f42f4f0a8cec18c96938f8193232bc69842942b340a5fba27683c"
    }
  },
  "envelope": {
    "artifact_schema": "spine.pack-installer-result.v2",
    "operation": "verify",
    "status": "success",
    "exit_code": "0",
    "artifact": {
      "path": "/synthetic/verification.json",
      "digest": "5b7fdda74d8f42f4f0a8cec18c96938f8193232bc69842942b340a5fba27683c"
    },
    "error": null
  }
}
```

### Spec 28: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/installer-v2/public-wire-vectors.json

Hash: d50469833dc229a09b328ffa9b044f5ef076054f6f4106356c5ac970e24ec159

```markdown
{
  "spine_commit": "57cda1c2d5589360ee8efe7155fd20b503034c2a",
  "purpose": "Unchanged upstream structural vectors; not installer acceptance or target qualification",
  "vectors": [
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_create.json",
      "source_sha256": "101fad9c030dc8cbb08ec1a8f3048cc1fb01dfe5c5b83db1ecd8cea0c49eee67",
      "command": "facet_schema.create",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.create",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.create",
        "command_receipt_id": "command_receipt_f56a6df1a40911c984227d9140b10edf8717255b01fc4246629b4222816e2cf3",
        "effect": "facet_schema_created",
        "changed": true,
        "audit_id": "audit_bee5bab0fb7802517627e79802080fcf1a9a53d6a08a9eeb70289314999640b4",
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": null,
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "revision_number": "1",
        "replayed": false
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_create_preview.json",
      "source_sha256": "f4a8d6be08f8826c9aab2d2cc9563e3041dffa5ad88eef94df687c4a92b7db52",
      "command": "facet_schema.create",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.create",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.create",
        "command_receipt_id": "command_receipt_f56a6df1a40911c984227d9140b10edf8717255b01fc4246629b4222816e2cf3",
        "effect": "facet_schema_created",
        "changed": true,
        "audit_id": "audit_bee5bab0fb7802517627e79802080fcf1a9a53d6a08a9eeb70289314999640b4",
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": null,
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "revision_number": "1",
        "replayed": false,
        "dry_run": true
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_create_replay.json",
      "source_sha256": "1046acd5688dd8c5024b814bd0141cf27a7eb67bc7d2b712f2f955f60e7888d8",
      "command": "facet_schema.create",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.create",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.create",
        "command_receipt_id": "command_receipt_f56a6df1a40911c984227d9140b10edf8717255b01fc4246629b4222816e2cf3",
        "effect": "facet_schema_created",
        "changed": false,
        "audit_id": "audit_bee5bab0fb7802517627e79802080fcf1a9a53d6a08a9eeb70289314999640b4",
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": null,
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "revision_number": "1",
        "replayed": true
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_list.json",
      "source_sha256": "5a14f8c1c76194562f6b5377e220399bdd6c35c71329c36dc11a08435c833366",
      "command": "facet_schema.list",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.list",
        "response_contract": "spine.facet-schemas.v1",
        "owner": {
          "owner_kind": "subject_group",
          "owner_group_id": "travel-team"
        },
        "schemas": [
          {
            "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
            "owner": {
              "owner_kind": "subject_group",
              "owner_group_id": "travel-team"
            },
            "schema_key": "flight_details",
            "current_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
            "status": "active"
          }
        ],
        "limit": "25",
        "has_more": false,
        "next_cursor": null
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_publish.json",
      "source_sha256": "6334a9860920846002c131ed615d47adfa9046b5ba5ec5e190e09f5258c1114e",
      "command": "facet_schema.publish",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.publish",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.publish",
        "command_receipt_id": "command_receipt_535c76fe7f398e86b615b7e75880bd42d3de0ed9c45ae8811416215741c8da53",
        "effect": "facet_schema_published",
        "changed": true,
        "audit_id": "audit_3966e681ca708e88f61508bb38dc45d10a120256d13eaa4f0c78aa9700f5494c",
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "facet_schema_revision_id": "facet_schema_revision_1726cea8399ecbb54963f4054eaee4344eb21bd64bac0539cb84ac89a0a48372",
        "revision_number": "2",
        "replayed": false
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_publish_noop.json",
      "source_sha256": "66bf856ee07876508e6d2c9e3949851a32d19fcc138e3669f49061331d9b4e26",
      "command": "facet_schema.publish",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.publish",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.publish",
        "command_receipt_id": "command_receipt_535c76fe7f398e86b615b7e75880bd42d3de0ed9c45ae8811416215741c8da53",
        "effect": "facet_schema_publish_noop",
        "changed": false,
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "revision_number": "1",
        "replayed": false
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_publish_noop_replay.json",
      "source_sha256": "d61904f311e9a444dad516b389f3b321f8bf8d1306eb3451effc29b2db2f6e16",
      "command": "facet_schema.publish",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.publish",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.publish",
        "command_receipt_id": "command_receipt_535c76fe7f398e86b615b7e75880bd42d3de0ed9c45ae8811416215741c8da53",
        "effect": "facet_schema_publish_noop",
        "changed": false,
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "revision_number": "1",
        "replayed": true
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_publish_replay.json",
      "source_sha256": "d570921d4dfb14237e6426fd6aed910ede0a4b137676d15fc2df143947e5d212",
      "command": "facet_schema.publish",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.publish",
        "response_contract": "spine.facet-schemas.v1",
        "command_id": "fixture-facet_schema.publish",
        "command_receipt_id": "command_receipt_535c76fe7f398e86b615b7e75880bd42d3de0ed9c45ae8811416215741c8da53",
        "effect": "facet_schema_published",
        "changed": false,
        "audit_id": "audit_3966e681ca708e88f61508bb38dc45d10a120256d13eaa4f0c78aa9700f5494c",
        "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
        "prior_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "facet_schema_revision_id": "facet_schema_revision_1726cea8399ecbb54963f4054eaee4344eb21bd64bac0539cb84ac89a0a48372",
        "revision_number": "2",
        "replayed": true
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_facet_schema_show.json",
      "source_sha256": "c8b11476cf04de531a05ce6fa13f2abb561ab22b8327a88b1b9d93a354608ffe",
      "command": "facet_schema.show",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "facet_schema.show",
        "response_contract": "spine.facet-schemas.v1",
        "root": {
          "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "travel-team"
          },
          "schema_key": "flight_details",
          "current_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
          "status": "active"
        },
        "revision": {
          "facet_schema_id": "facet_schema_c0742a134b0891560b65c377fd3ef4936b12fb8aa1f6a3aba7087760479261c4",
          "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
          "revision_number": "1",
          "definition": {
            "display_name": "Flight details",
            "description": "Descriptive flight identifiers and airport references.",
            "compatible_item_types": [
              "event"
            ],
            "fields": [
              {
                "key": "airline",
                "required": false,
                "type": "text",
                "max_length": "128",
                "queryable": false
              },
              {
                "key": "destination",
                "required": true,
                "type": "reference",
                "target_kind": "location",
                "queryable": true
              },
              {
                "key": "flight_number",
                "required": true,
                "type": "text",
                "max_length": "32",
                "queryable": true
              },
              {
                "key": "origin",
                "required": true,
                "type": "reference",
                "target_kind": "location",
                "queryable": true
              }
            ]
          },
          "definition_hash": "27ef8c40d4fa989f1d99830286b541d04d91c2ea3648c8f67172b5fc199aacdc"
        }
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_list.json",
      "source_sha256": "f2c6b44251acf04ca6da1f25cb7c52ab37a2c6a2c67a7be63335b235aad69bf6",
      "command": "item_archetype.facet_binding.list",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "item_archetype.facet_binding.list",
        "response_contract": "spine.archetype-facet-bindings.v1",
        "item_archetype_id": "archetype-flight",
        "bindings": [
          {
            "facet_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
            "item_archetype_id": "archetype-flight",
            "facet_key": "flight_details",
            "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
            "status": "active"
          }
        ],
        "limit": "25",
        "has_more": false,
        "next_cursor": null
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_set.json",
      "source_sha256": "8b404eb948c26e3d9a2a12a14b23fe051d604f89c37e3eb9e947dd80899f7c9d",
      "command": "item_archetype.facet_binding.set",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "item_archetype.facet_binding.set",
        "response_contract": "spine.archetype-facet-bindings.v1",
        "command_id": "fixture-item_archetype.facet_binding.set",
        "command_receipt_id": "command_receipt_9c58a4461b76231d30ba00cf235cdc20452b416b40b4229d1e10fbe30875be02",
        "effect": "facet_binding_set",
        "changed": true,
        "audit_id": "audit_c317d75dc51ea6267b3357de77439879f26001f2ed87606e968e7c91c6ea03c5",
        "item_archetype_id": "archetype-flight",
        "facet_key": "flight_details",
        "prior_binding_id": null,
        "facet_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "replayed": false
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_set_noop.json",
      "source_sha256": "9675548c27c26e68e13dd398b730b09561c2aba828a550eea08a980ad85ea288",
      "command": "item_archetype.facet_binding.set",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "item_archetype.facet_binding.set",
        "response_contract": "spine.archetype-facet-bindings.v1",
        "command_id": "fixture-item_archetype.facet_binding.set",
        "command_receipt_id": "command_receipt_9c58a4461b76231d30ba00cf235cdc20452b416b40b4229d1e10fbe30875be02",
        "effect": "facet_binding_set_noop",
        "changed": false,
        "item_archetype_id": "archetype-flight",
        "facet_key": "flight_details",
        "prior_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "replayed": false
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_set_noop_replay.json",
      "source_sha256": "b86fbe60569348773b59bd203922e0ac24bc1a6f23abce64c4aae8e599b56f6c",
      "command": "item_archetype.facet_binding.set",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "item_archetype.facet_binding.set",
        "response_contract": "spine.archetype-facet-bindings.v1",
        "command_id": "fixture-item_archetype.facet_binding.set",
        "command_receipt_id": "command_receipt_9c58a4461b76231d30ba00cf235cdc20452b416b40b4229d1e10fbe30875be02",
        "effect": "facet_binding_set_noop",
        "changed": false,
        "item_archetype_id": "archetype-flight",
        "facet_key": "flight_details",
        "prior_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "replayed": true
      }
    },
    {
      "source": "tests/fixtures/archetype_facets/contracts/response_item_archetype_facet_binding_set_replay.json",
      "source_sha256": "3107e95609af1cdaf2887c457d3ae7dab7fdd3127223bb668189f81baba7221e",
      "command": "item_archetype.facet_binding.set",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "item_archetype.facet_binding.set",
        "response_contract": "spine.archetype-facet-bindings.v1",
        "command_id": "fixture-item_archetype.facet_binding.set",
        "command_receipt_id": "command_receipt_9c58a4461b76231d30ba00cf235cdc20452b416b40b4229d1e10fbe30875be02",
        "effect": "facet_binding_set",
        "changed": false,
        "audit_id": "audit_c317d75dc51ea6267b3357de77439879f26001f2ed87606e968e7c91c6ea03c5",
        "item_archetype_id": "archetype-flight",
        "facet_key": "flight_details",
        "prior_binding_id": null,
        "facet_binding_id": "archetype_facet_binding_db3fa09d817a7b76f9a2ec442900d7051d04b284a771ef7d998ff001774a305f",
        "facet_schema_revision_id": "facet_schema_revision_fcbda5c8b6c18df146f519ce33d83e46ab7a59017b0912c41b0eda4b363af4a8",
        "replayed": true
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_create.json",
      "source_sha256": "f946fd5197bd47c40c54880696d13f4838eb66d974b20d42dffa569ed049a7f4",
      "command": "notification_rendering_definition.create",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.create",
        "command_id": "rendering-example-create",
        "changed": true,
        "replayed": false,
        "effect": "rendering_definition_created",
        "command_receipt_id": "command_receipt_dd4776c5d577d6546bfd1a8355f613a2ff15ea56df1d73e9e66e4f0a3d1502b3",
        "audit_id": "audit_dc74aec2532b800cebd3e45400dda9b093ed1bdec7ce94f29eb06d0fc3fa73e1",
        "record": {
          "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
          "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "example-group"
          },
          "definition_key": "flight_details",
          "status": "active",
          "current_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "revision_number": "1",
          "revision": {
            "display_name": "Flight details",
            "description": null,
            "compatible_item_types": [
              "event"
            ],
            "base_rendering_contract": "spine.notification-rendering.v1",
            "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
            "selections": [
              {
                "selection_key": "flight",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "flight_number",
                "label": "Flight",
                "projection": "value"
              },
              {
                "selection_key": "terminal",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "terminal",
                "label": "Terminal",
                "projection": "value"
              },
              {
                "selection_key": "departure",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "departure_airport",
                "label": "Departure",
                "projection": "location_label"
              }
            ]
          },
          "definition_hash": "6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb",
          "created": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "published": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "retired": null
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_create_dry_run.json",
      "source_sha256": "bd07400d3ed100a2620b6084718e911b07faee8de5289c2ab392fe1bfd3dcce9",
      "command": "notification_rendering_definition.create",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.create",
        "command_id": "rendering-example-create",
        "changed": true,
        "replayed": false,
        "dry_run": true,
        "effect": "rendering_definition_created",
        "command_receipt_id": "command_receipt_dd4776c5d577d6546bfd1a8355f613a2ff15ea56df1d73e9e66e4f0a3d1502b3",
        "audit_id": "audit_dc74aec2532b800cebd3e45400dda9b093ed1bdec7ce94f29eb06d0fc3fa73e1",
        "record": {
          "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
          "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "example-group"
          },
          "definition_key": "flight_details",
          "status": "active",
          "current_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "revision_number": "1",
          "revision": {
            "display_name": "Flight details",
            "description": null,
            "compatible_item_types": [
              "event"
            ],
            "base_rendering_contract": "spine.notification-rendering.v1",
            "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
            "selections": [
              {
                "selection_key": "flight",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "flight_number",
                "label": "Flight",
                "projection": "value"
              },
              {
                "selection_key": "terminal",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "terminal",
                "label": "Terminal",
                "projection": "value"
              },
              {
                "selection_key": "departure",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "departure_airport",
                "label": "Departure",
                "projection": "location_label"
              }
            ]
          },
          "definition_hash": "6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb",
          "created": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "published": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "retired": null
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_create_replay.json",
      "source_sha256": "c19b5b249038c43968b7ca53209f7adf0662717bf9571898cc8cdd9c6c934178",
      "command": "notification_rendering_definition.create",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.create",
        "command_id": "rendering-example-create",
        "changed": false,
        "replayed": true,
        "effect": "rendering_definition_created",
        "command_receipt_id": "command_receipt_dd4776c5d577d6546bfd1a8355f613a2ff15ea56df1d73e9e66e4f0a3d1502b3",
        "audit_id": "audit_dc74aec2532b800cebd3e45400dda9b093ed1bdec7ce94f29eb06d0fc3fa73e1",
        "record": {
          "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
          "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "example-group"
          },
          "definition_key": "flight_details",
          "status": "active",
          "current_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "revision_number": "1",
          "revision": {
            "display_name": "Flight details",
            "description": null,
            "compatible_item_types": [
              "event"
            ],
            "base_rendering_contract": "spine.notification-rendering.v1",
            "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
            "selections": [
              {
                "selection_key": "flight",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "flight_number",
                "label": "Flight",
                "projection": "value"
              },
              {
                "selection_key": "terminal",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "terminal",
                "label": "Terminal",
                "projection": "value"
              },
              {
                "selection_key": "departure",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "departure_airport",
                "label": "Departure",
                "projection": "location_label"
              }
            ]
          },
          "definition_hash": "6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb",
          "created": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "published": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "retired": null
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_list_dry_run.json",
      "source_sha256": "03822daa5a287b332a4fbe7f62bac74c98b4447747415edf83a62aa1313a5e9c",
      "command": "notification_rendering_definition.list",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.list",
        "records": [],
        "has_more": false,
        "next_cursor": null,
        "limit": "20",
        "dry_run": true
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_list_empty.json",
      "source_sha256": "aeeed7167a39cbf3c60627f8db80abafb32aa7989e2f07a310b1d52f1d25a15d",
      "command": "notification_rendering_definition.list",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.list",
        "records": [],
        "has_more": false,
        "next_cursor": null,
        "limit": "20"
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_publish_noop.json",
      "source_sha256": "7089a2fdb00c475710db37c55ed22a5e835f606bb8002d9916ba06e3ee18d5f7",
      "command": "notification_rendering_definition.publish",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.publish",
        "command_id": "rendering-example-publish-noop",
        "changed": false,
        "replayed": false,
        "effect": "rendering_definition_publish_noop",
        "command_receipt_id": "command_receipt_c92376d4bcb98d1dec472473e31d6f71bf46ca68921097937fad81a556e9ecd5",
        "audit_id": "audit_7ded09e8e81bdeb89066850363a08ed8ce852b44c4273001d46bf77bbcf95136",
        "record": {
          "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
          "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "example-group"
          },
          "definition_key": "flight_details",
          "status": "active",
          "current_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "revision_number": "1",
          "revision": {
            "display_name": "Flight details",
            "description": null,
            "compatible_item_types": [
              "event"
            ],
            "base_rendering_contract": "spine.notification-rendering.v1",
            "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
            "selections": [
              {
                "selection_key": "flight",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "flight_number",
                "label": "Flight",
                "projection": "value"
              },
              {
                "selection_key": "terminal",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "terminal",
                "label": "Terminal",
                "projection": "value"
              },
              {
                "selection_key": "departure",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "departure_airport",
                "label": "Departure",
                "projection": "location_label"
              }
            ]
          },
          "definition_hash": "6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb",
          "created": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "published": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "retired": null
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_definitions/contracts/response_definition_show_dry_run.json",
      "source_sha256": "c1ef5e22d92e5b80f32a48cdb4f7a8c16886240f394d17388bdc8a3c7490018e",
      "command": "notification_rendering_definition.show",
      "direction": "response",
      "value": {
        "ok": true,
        "contract_version": "spine.notification-rendering-definitions.v1",
        "command": "notification_rendering_definition.show",
        "record": {
          "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
          "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "owner": {
            "owner_kind": "subject_group",
            "owner_group_id": "example-group"
          },
          "definition_key": "flight_details",
          "status": "active",
          "current_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52",
          "revision_number": "1",
          "revision": {
            "display_name": "Flight details",
            "description": null,
            "compatible_item_types": [
              "event"
            ],
            "base_rendering_contract": "spine.notification-rendering.v1",
            "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
            "selections": [
              {
                "selection_key": "flight",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "flight_number",
                "label": "Flight",
                "projection": "value"
              },
              {
                "selection_key": "terminal",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "terminal",
                "label": "Terminal",
                "projection": "value"
              },
              {
                "selection_key": "departure",
                "facet_key": "flight_details",
                "facet_schema_revision_id": "facet_schema_revision_flight_v1",
                "field_key": "departure_airport",
                "label": "Departure",
                "projection": "location_label"
              }
            ]
          },
          "definition_hash": "6d8aaffc80a2e54efa76fcd02be0a1f65881e111f5902b8fd271a6ae0a7d5fdb",
          "created": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "published": {
            "command_id": "rendering-example-create",
            "actor_subject_id": "example-operator",
            "action_timestamp_utc": "2026-10-03T12:00:00Z"
          },
          "retired": null
        },
        "dry_run": true
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_create.json",
      "source_sha256": "5fd1f6cd04e5579111cfcfad5d0f61441cf7b280dee1f4baed2cb1ca3a9f82f2",
      "command": "notification_profile.create",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.create",
        "response_contract": "spine.notification-profiles.v2",
        "effect": "notification_profile_created",
        "notification_profile_id": "profile-example",
        "notification_profile_revision_id": "revision-example",
        "revision_number": "1",
        "status": "active",
        "normalized_revision_hash": "dfde522127e4cdb593d0946e8ea04a0b82692b43db2de933b80fc47bf415816e",
        "receipt": {
          "command_receipt_id": "receipt-example",
          "command_id": "command-example",
          "effect": "notification_profile_created",
          "semantic_facts_hash": "036d030445d89c3bca7804fec6b020b625df927e23a19d164466e71f5bb2f858",
          "created_at_utc": "2035-02-01T12:00:01Z"
        },
        "profile_key": "appointment_standard"
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_historical_v1.json",
      "source_sha256": "4c3862d38b09e00b5b3c0a3c733fe1274807943bdfd31dac90c85ab864c0e230",
      "command": "notification_profile.show",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.show",
        "response_contract": "spine.notification-profiles.v2",
        "notification_profile": {
          "notification_profile_id": "profile-example",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "subject_owner"
          },
          "profile_key": "appointment_standard",
          "display_name": "Appointment standard",
          "description": "One day before",
          "status": "active",
          "current_revision_id": "revision-example",
          "revision": {
            "notification_profile_revision_id": "revision-old",
            "revision_number": "1",
            "revision_contract": "spine.notification-profiles.v1",
            "normalized_revision_hash": "8dcae6cd5b03d21a1945ce6407fe622fdb9f6b9da03dd5449e4ef3022d26a7b6",
            "content": {
              "compatible_item_types": [
                "event"
              ],
              "templates": [
                {
                  "template_key": "day_before",
                  "schedule": {
                    "kind": "once",
                    "at": {
                      "kind": "target_offset",
                      "offset_basis": "elapsed",
                      "offset_seconds": "-86400"
                    }
                  },
                  "late_handling": {
                    "kind": "skip"
                  },
                  "normalized_template_hash": "b2316725c7b9ee85862cbe9709d4e0ebe0afbcc7550e74371434ef31ab9628f2"
                }
              ]
            }
          }
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_list.json",
      "source_sha256": "a5a2bd2c48cc1d8ea1c304736fead1c4de0d29b35f69bf19e820751a5de73b38",
      "command": "notification_profile.list",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.list",
        "response_contract": "spine.notification-profiles.v2",
        "entries": [
          {
            "notification_profile_id": "profile-example",
            "owner": {
              "owner_kind": "subject",
              "owner_subject_id": "subject_owner"
            },
            "profile_key": "appointment_standard",
            "display_name": "Appointment standard",
            "description": "One day before",
            "status": "active",
            "current_revision_id": "revision-example",
            "revision": {
              "notification_profile_revision_id": "revision-example",
              "revision_number": "2",
              "revision_contract": "spine.notification-profiles.v2",
              "normalized_revision_hash": "dfde522127e4cdb593d0946e8ea04a0b82692b43db2de933b80fc47bf415816e",
              "content": {
                "compatible_item_types": [
                  "event"
                ],
                "templates": [
                  {
                    "template_key": "day_before",
                    "schedule": {
                      "kind": "once",
                      "at": {
                        "kind": "target_offset",
                        "offset_basis": "elapsed",
                        "offset_seconds": "-86400"
                      }
                    },
                    "late_handling": {
                      "kind": "skip"
                    },
                    "rendering": {
                      "kind": "definition",
                      "definition": {
                        "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
                        "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"
                      }
                    },
                    "normalized_template_hash": "767aea675f91719c3574baf19657c8cc8d99c9cce70cacf71f97fb9d29774c17"
                  }
                ]
              }
            }
          }
        ],
        "count": "1",
        "catalog_snapshot_hash": "461b0879b23e3f32f98b1ecf622ff8e5f2d5e1976d31dc37a421c330cfcdd185",
        "has_more": false,
        "next_cursor": null
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_overlay_revision.json",
      "source_sha256": "167bf4a5ca011c2e8310e75661fc9a4dd12f2eaaad420c11bca6c62740c70fa3",
      "command": "notification_profile.show",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.show",
        "response_contract": "spine.notification-profiles.v2",
        "notification_profile": {
          "notification_profile_id": "profile-example",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "subject_owner"
          },
          "profile_key": "appointment_standard",
          "display_name": "Appointment standard",
          "description": "One day before",
          "status": "active",
          "current_revision_id": "revision-example",
          "revision": {
            "notification_profile_revision_id": "revision-example",
            "revision_number": "2",
            "revision_contract": "spine.notification-profiles.v2",
            "normalized_revision_hash": "f4c2ffc6dbfabcc20da20ac1b6a70744493a73344c7d597185554b7720081591",
            "content": {
              "compatible_item_types": [
                "event"
              ],
              "templates": [
                {
                  "template_key": "day_before",
                  "schedule": {
                    "kind": "once",
                    "at": {
                      "kind": "target_offset",
                      "offset_basis": "elapsed",
                      "offset_seconds": "-86400"
                    }
                  },
                  "late_handling": {
                    "kind": "skip"
                  },
                  "rendering": {
                    "kind": "definition",
                    "definition": {
                      "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
                      "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"
                    }
                  },
                  "normalized_template_hash": "767aea675f91719c3574baf19657c8cc8d99c9cce70cacf71f97fb9d29774c17"
                },
                {
                  "template_key": "suppressed",
                  "schedule": {
                    "kind": "once",
                    "at": {
                      "kind": "target_offset",
                      "offset_basis": "elapsed",
                      "offset_seconds": "-172800"
                    }
                  },
                  "late_handling": {
                    "kind": "skip"
                  },
                  "rendering": {
                    "kind": "definition",
                    "definition": {
                      "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
                      "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"
                    }
                  },
                  "normalized_template_hash": "24a8dac32b45e4efc12a47a26c113dfe21164d85429987f286f46082f6f10d34"
                }
              ]
            }
          }
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_revise.json",
      "source_sha256": "7e79d7b4c2e9475f60ba4e175285161a9290ca9c5e42a969cea85624b48b56be",
      "command": "notification_profile.revise",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.revise",
        "response_contract": "spine.notification-profiles.v2",
        "effect": "notification_profile_revised",
        "notification_profile_id": "profile-example",
        "notification_profile_revision_id": "revision-example",
        "revision_number": "2",
        "status": "active",
        "normalized_revision_hash": "dfde522127e4cdb593d0946e8ea04a0b82692b43db2de933b80fc47bf415816e",
        "receipt": {
          "command_receipt_id": "receipt-example",
          "command_id": "command-example",
          "effect": "notification_profile_revised",
          "semantic_facts_hash": "036d030445d89c3bca7804fec6b020b625df927e23a19d164466e71f5bb2f858",
          "created_at_utc": "2035-02-01T12:00:01Z"
        }
      }
    },
    {
      "source": "tests/fixtures/notification_rendering_integration/response_profile_show.json",
      "source_sha256": "385d6b3ce16d677c496694b044233bd685353d1808a234624f83d8208cacdc34",
      "command": "notification_profile.show",
      "direction": "response",
      "value": {
        "ok": true,
        "command": "notification_profile.show",
        "response_contract": "spine.notification-profiles.v2",
        "notification_profile": {
          "notification_profile_id": "profile-example",
          "owner": {
            "owner_kind": "subject",
            "owner_subject_id": "subject_owner"
          },
          "profile_key": "appointment_standard",
          "display_name": "Appointment standard",
          "description": "One day before",
          "status": "active",
          "current_revision_id": "revision-example",
          "revision": {
            "notification_profile_revision_id": "revision-example",
            "revision_number": "2",
            "revision_contract": "spine.notification-profiles.v2",
            "normalized_revision_hash": "dfde522127e4cdb593d0946e8ea04a0b82692b43db2de933b80fc47bf415816e",
            "content": {
              "compatible_item_types": [
                "event"
              ],
              "templates": [
                {
                  "template_key": "day_before",
                  "schedule": {
                    "kind": "once",
                    "at": {
                      "kind": "target_offset",
                      "offset_basis": "elapsed",
                      "offset_seconds": "-86400"
                    }
                  },
                  "late_handling": {
                    "kind": "skip"
                  },
                  "rendering": {
                    "kind": "definition",
                    "definition": {
                      "notification_rendering_definition_id": "notification_rendering_definition_02f257fab5ae9d05c29ad78672208f2329671a72dbb76fa6773c9623950fa1fe",
                      "notification_rendering_definition_revision_id": "notification_rendering_definition_revision_e0ba4b36ee5a68085a16c17068ce0091ef1fc0834da7cd9fbcf7c55302dddc52"
                    }
                  },
                  "normalized_template_hash": "767aea675f91719c3574baf19657c8cc8d99c9cce70cacf71f97fb9d29774c17"
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

### Spec 29: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/runtime/test_planning.py

Hash: 7b20c5b22e91392e6b6d8136abab52b1eb7d8b9d569661478df1e629c666d82d

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
        # This is the implemented v1 decoder's vocabulary gate, not an assertion
        # that proposed successor contracts are accepted by the current runtime.
        # Keep every original runtime schema covered explicitly. FR-1 v2 uses
        # independent Draft 2020-12 validation under tests/contract/.
        runtime_schema_names = (
            "spine-pack-manifest.v1.schema.json",
            "spine-pack-installer-types.v1.schema.json",
            "spine-pack-embedded-values.v1.schema.json",
            "spine-pack-install-request.v1.schema.json",
            "spine-pack-install-plan.v1.schema.json",
            "spine-pack-install-approval.v1.schema.json",
            "spine-pack-apply-checkpoint.v1.schema.json",
            "spine-pack-apply-result.v1.schema.json",
            "spine-pack-verification-result.v1.schema.json",
            "spine-pack-installer-result.v1.schema.json",
            "spine-readback-0.3.0.schema.json",
            "spine-readback-0.5.0.schema.json",
        )
        for name in runtime_schema_names:
            path = a.SCHEMA_ROOT / name
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

    def test_recover_is_not_a_supported_cli_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["recover"]), 2)
        self.assertEqual(json.loads(output.getvalue())["error"]["code"], "invalid_cli_arguments")

    def test_verify_requires_arguments(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["verify"]), 2)
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

### Spec 30: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/scripts/verify_repo.py

Hash: 3a3177acf6107115b8b3f40f265350012786cbb170283242aafba0809a66b9bc

```markdown
#!/usr/bin/env python3
"""Verify the draft-contract Spine Packs repository shape and boundaries."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "docs/releases.md",
    "docs/release-finalization.md",
    "docs/spine-0.6.0-qualification.md",
    "docs/facet-rendering-baseline.md",
    "specs/facet-rendering-packs.md",
    "specs/installer-artifacts-v2.md",
    "contracts/installer-spine-0.9.1-inventory.json",
    "contracts/installer-fixture-manifest.v2.json",
    "contracts/schemas/spine-pack-installer-types.v2.schema.json",
    "contracts/schemas/spine-pack-embedded-values.v2.schema.json",
    "contracts/schemas/spine-readback-0.9.1.schema.json",
    "contracts/schemas/spine-pack-install-request.v2.schema.json",
    "contracts/schemas/spine-pack-install-plan.v2.schema.json",
    "contracts/schemas/spine-pack-install-approval.v2.schema.json",
    "contracts/schemas/spine-pack-apply-checkpoint.v2.schema.json",
    "contracts/schemas/spine-pack-apply-result.v2.schema.json",
    "contracts/schemas/spine-pack-verification-result.v2.schema.json",
    "contracts/schemas/spine-pack-installer-result.v2.schema.json",
    "tests/contract/facet_artifact_oracle.py",
    "tests/contract/test_facet_artifact_contract.py",
    "tests/fixtures/installer-v2/flight-create.json",
    "tests/fixtures/installer-v2/flight-update.json",
    "tests/fixtures/installer-v2/public-wire-vectors.json",
    "specs/implementation-plan.md",
    "scripts/qualify_profile_v2_listing.py",
    "contracts/schemas/spine-pack-manifest.v2.schema.json",
    "contracts/pack-fixture-manifest.v2.json",
    "tests/fixtures/pack-manifest-v2/flight.json",
    "tests/contract/test_facet_manifest_contract.py",
    "tests/contract/test_spine060_contract.py",
    "tests/runtime/test_spine060_compatibility.py",
    "tests/fixtures/installer/positive/spine060_plan.json",
    "packs/kinflow-starter/kinflow-starter.1.0.1-draft.1.json",
    "packs/kinflow-starter/kinflow-starter.1.0.1.json",
    "docs/spine-0.6.0-release-finalization.md",
    "tests/contract/test_kinflow_release_contract.py",
    "packs/kinflow-starter/kinflow-starter.1.0.0.json",
    "scripts/qualify_package.py",
    "tests/runtime/test_package_resources.py",
    "contracts/installer-fixture-manifest.v1.json",
    "contracts/pack-fixture-manifest.v1.json",
    "contracts/schemas/spine-pack-apply-checkpoint.v1.schema.json",
    "contracts/schemas/spine-pack-apply-result.v1.schema.json",
    "contracts/schemas/spine-pack-embedded-values.v1.schema.json",
    "contracts/schemas/spine-pack-install-approval.v1.schema.json",
    "contracts/schemas/spine-pack-install-plan.v1.schema.json",
    "contracts/schemas/spine-pack-install-request.v1.schema.json",
    "contracts/schemas/spine-pack-installer-result.v1.schema.json",
    "contracts/schemas/spine-pack-installer-types.v1.schema.json",
    "contracts/schemas/spine-pack-manifest.v1.schema.json",
    "contracts/schemas/spine-pack-verification-result.v1.schema.json",
    "contracts/schemas/spine-readback-0.3.0.schema.json",
    "contracts/schemas/spine-readback-0.5.0.schema.json",
    "tests/runtime/test_schema15_compatibility.py",
    "tests/contract/test_schema15_contract.py",
    "tests/fixtures/installer/positive/schema15_plan.json",
    "src/spine_packs/__init__.py",
    "src/spine_packs/__main__.py",
    "src/spine_packs/artifacts.py",
    "src/spine_packs/apply.py",
    "src/spine_packs/execution.py",
    "src/spine_packs/manifest.py",
    "src/spine_packs/planning.py",
    "src/spine_packs/preflight.py",
    "src/spine_packs/recovery.py",
    "src/spine_packs/verification.py",
    "src/spine_packs/spine_command.py",
    "tests/runtime/test_apply_preflight.py",
    "tests/runtime/test_apply.py",
    "tests/runtime/test_continuation.py",
    "tests/runtime/test_verification.py",
    "tests/runtime/test_planning.py",
    "tests/integration/test_local_spine.py",
    "docs/local-qualification.md",
    "packs/kinflow-starter/README.md",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.2.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.3.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.4.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.5.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.6.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.7.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.8.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.9.json",
    "packs/kinflow-starter/kinflow-starter.1.0.0-draft.10.json",
    "scripts/verify_repo.py",
    "specs/architecture.md",
    "specs/compatibility.md",
    "specs/installer-artifacts.md",
    "specs/installer.md",
    "specs/kinflow-starter.md",
    "specs/overview.md",
    "specs/pack-format.md",
    "tests/contract/test_pack_manifest_contract.py",
    "tests/contract/test_installer_artifact_contract.py",
    "tests/fixtures/installer/positive/granular_request.json",
    "tests/fixtures/installer/positive/profile_drift_artifact_suite.json",
    "tests/fixtures/installer/positive/profile_drift_vertical_flow.json",
    "tests/fixtures/installer/negative/draft_apply_eligible.json",
    "tests/fixtures/installer/negative/apply_target_mismatch.json",
    "tests/fixtures/installer/negative/embedded_contract_violations.json",
    "tests/fixtures/installer/negative/binding_identity_mismatch.json",
    "tests/fixtures/installer/negative/invalid_result_references.json",
    "tests/fixtures/installer/positive/create_binding_artifact_suite.json",
    "tests/fixtures/installer/negative/selection_assertion_mismatch.json",
    "tests/fixtures/installer/negative/incorrect_artifact_digest.json",
    "tests/fixtures/installer/negative/noncontiguous_partial_apply.json",
    "tests/fixtures/installer/negative/stale_catalog_snapshot.json",
    "tests/fixtures/installer/negative/stale_plan_approval.json",
    "tests/fixtures/installer/negative/target_mismatch.json",
    "tests/fixtures/installer/negative/unauthorized_drift.json",
    "tests/fixtures/installer/negative/uncertain_replay_command_mismatch.json",
    "tests/fixtures/installer/negative/unsorted_selection.json",
    "tests/fixtures/pack-manifest/positive/medical_vertical_slice.json",
    "tests/fixtures/pack-manifest/positive/medical_and_lesson.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_3.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_4.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_5.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_6.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_7.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_8.json",
    "tests/fixtures/pack-manifest/positive/kinflow_starter_draft_9.json",
    "tests/fixtures/pack-manifest/positive/exact_target_elapsed_offset.json",
    "tests/fixtures/pack-manifest/negative/birthday_embedded_timezone.json",
    "tests/fixtures/pack-manifest/negative/birthday_profile_recurrence.json",
    "tests/fixtures/pack-manifest/negative/duplicate_archetype_key.json",
    "tests/fixtures/pack-manifest/negative/duplicate_json_object_member.json",
    "tests/fixtures/pack-manifest/negative/embedded_owner_data.json",
    "tests/fixtures/pack-manifest/negative/incompatible_item_types.json",
    "tests/fixtures/pack-manifest/negative/incorrect_content_digest.json",
    "tests/fixtures/pack-manifest/negative/invalid_grace_window.json",
    "tests/fixtures/pack-manifest/negative/invalid_notification_offset.json",
    "tests/fixtures/pack-manifest/negative/lesson_profile_recurrence.json",
    "tests/fixtures/pack-manifest/negative/multiple_defaults_for_archetype.json",
    "tests/fixtures/pack-manifest/negative/noncanonical_array_ordering.json",
    "tests/fixtures/pack-manifest/negative/unknown_fields.json",
    "tests/fixtures/pack-manifest/negative/unresolved_binding_reference.json",
    "tests/fixtures/pack-manifest/negative/version_status_mismatch.json",
)

REQUIRED_MARKERS = {
    "README.md": (
        "Spine remains the sole authority",
        "Direct database access is forbidden",
        "`plan`",
        "`apply`",
        "`verify`",
        "draft-contract",
    ),
    "AGENTS.md": (
        "The files in `specs/` are the normative source of truth",
        "Do not make Spine runtime changes",
    ),
    "specs/overview.md": (
        "Packs MUST be declarative and owner-neutral",
        "Pack releases MUST be immutable",
    ),
    "specs/architecture.md": (
        "Spine public command surface",
        "Direct database access is forbidden",
        "semantic drift",
    ),
    "specs/compatibility.md": (
        "exact Spine runtime versions",
        "exact Spine content-contract identifiers",
        "Fail-closed behavior",
    ),
    "specs/installer.md": (
        "Spine remains the sole authority",
        "direct Spine database access",
        "Inferred archetype units",
        "Deterministic plan",
        "single-operator concurrency posture",
        "captured, validated Spine command response",
        "Machine-contract layer",
        "useful general Spine hardening",
    ),
    "specs/installer-artifacts.md": (
        "Spine remains authoritative",
        "spine.pack-install-plan.v1",
        "spine.pack-command-id.v1",
        "prepared_or_submitted",
        "captured_responses_only_spine_0.3.0",
        "Direct database access",
    ),
    "specs/pack-format.md": (
        "`spine.pack-manifest.v1`",
        "Every object is closed",
        "Deterministic ordering",
        "Content identity",
        "Deferred decisions",
    ),
    "specs/kinflow-starter.md": (
        "1.0.0-draft.9",
        "Lesson notification profile",
        "Game or competition",
        "Flight",
        "Birthday",
        "Education and activities",
        "Social",
        "Travel",
        "Renewals and administration",
        "Health",
        "Home, vehicle, and logistics",
        "General commitments",
        "Late-delivery spacing policy",
        "Spine-owned item state",
    ),
    "contracts/schemas/spine-pack-manifest.v1.schema.json": (
        "https://json-schema.org/draft/2020-12/schema",
        "spine.pack-manifest.v1",
        "additionalProperties",
    ),
    "contracts/schemas/spine-pack-installer-types.v1.schema.json": (
        "https://json-schema.org/draft/2020-12/schema",
        "spine.pack-install-request.v1",
        "spine.pack-install-plan.v1",
        "spine.pack-apply-checkpoint.v1",
        "additionalProperties",
    ),
    "tests/contract/test_installer_artifact_contract.py": (
        "Dependency-free contract checks",
        "content_digest_errors",
        "accepted_prefix_not_contiguous",
        "command_id_mismatch",
        "target_binding_mismatch",
    ),
    "tests/contract/test_pack_manifest_contract.py": (
        "Dependency-free contract checks",
        "validate_pack",
        "content_digest",
    ),
}

PACK_ARCHETYPE_NAMES = (
    "application_deadline",
    "birthday",
    "camp_or_program",
    "check_in_required",
    "community_event",
    "delivery_window",
    "dinner_reservation",
    "document_renewal",
    "dropoff",
    "errand",
    "flight",
    "follow_up",
    "game_or_competition",
    "home_maintenance",
    "home_service_appointment",
    "insurance_renewal",
    "interview",
    "lesson",
    "license_renewal",
    "lodging_checkin",
    "lodging_checkout",
    "medical_appointment",
    "medication_refill",
    "meeting",
    "packing",
    "parent_teacher_meeting",
    "party",
    "passport_renewal",
    "payment_due",
    "performance",
    "personal_deadline",
    "pet_appointment",
    "pickup",
    "playdate",
    "prescription_pickup",
    "purchase_required",
    "registration_deadline",
    "reservation",
    "school_deadline",
    "school_event",
    "social_gathering",
    "subscription_renewal",
    "tax_deadline",
    "ticketed_event",
    "train_or_bus_trip",
    "travel_preparation",
    "travel_transfer",
    "trip_departure",
    "vaccination_due",
    "vehicle_service",
    "visitor_arrival",
    "work_deadline",
)

FORBIDDEN_TOP_LEVEL = (
    "adapters",
    "examples",
    "models",
    "services",
)


def verify() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for relative, markers in REQUIRED_MARKERS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"missing boundary marker in {relative}: {marker!r}")

    pack_readme = ROOT / "packs/kinflow-starter/README.md"
    if pack_readme.is_file():
        text = pack_readme.read_text(encoding="utf-8")
        for name in PACK_ARCHETYPE_NAMES:
            if f"`{name}`" not in text:
                errors.append(f"missing kinflow-starter archetype name: {name}")

    for name in FORBIDDEN_TOP_LEVEL:
        if (ROOT / name).exists():
            errors.append(f"draft-contract repository must not contain: {name}/")

    source_root = ROOT / "src"
    if source_root.is_dir():
        allowed_source = {p for p in REQUIRED_FILES if p.startswith("src/")}
        for path in source_root.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                relative = path.relative_to(ROOT).as_posix()
                if relative not in allowed_source:
                    errors.append(f"outside the reviewed installer layout: {relative}")

    packs_root = ROOT / "packs"
    if packs_root.is_dir():
        alternate_manifests = sorted(
            path.relative_to(ROOT)
            for path in packs_root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".toml", ".yaml", ".yml"}
        )
        for relative in alternate_manifests:
            errors.append(f"v1 packs must use JSON, found alternate manifest: {relative}")

    return errors


def main() -> int:
    errors = verify()
    if errors:
        print("repository verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"repository verification passed ({len(REQUIRED_FILES)} required files)")
    print("source of truth: specs/")
    print("draft-contract boundary markers: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
