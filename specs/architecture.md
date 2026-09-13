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
