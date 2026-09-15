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
Read-only planning, non-mutating apply preflight, initial approved apply,
bounded continuation, and non-mutating verification are implemented. Tests use
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
success. `receipt_readback` remains `captured_responses_only_spine_0.3.0`.
Verified results exit 0; completed mismatches exit 10 with the sealed artifact.
Input, target, compatibility, transport, and publication failures use their
existing specific error exits and make no verification-success claim.

This is a simulated-command implementation slice. Disposable-target integration,
supported packaging, releases, and deployment remain Slice 6 or separate work.

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
