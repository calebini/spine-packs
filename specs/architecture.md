# Architecture

## Facet/rendering successor — planning, apply, recovery and verification

[facet-rendering-packs.md](facet-rendering-packs.md) proposes a separate manifest
and installer-artifact v2 path for exact Spine `0.10.0` / schema `19` at
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`. It adds a bounded configuration graph:
archetype and facet schema -> facet binding -> rendering definition -> profile
revision -> default binding. The proposal does not expand the runtime authority
or compatibility of the implemented slices below. No disclosure authorization,
item authoring, scheduling or sending belongs to that graph. Read its review
gates before successor work; old v1 behavior and released artifacts remain intact.

The draft successor machine layer is specified in
[installer-artifacts-v2.md](installer-artifacts-v2.md). Its pure test oracle lives
under `tests/contract/`, not `src/spine_packs/`. Saved synthetic execution and
recovery fixtures remain synthetic contract evidence. Runtime tests distinguish
public wire simulations from exact installed-Spine qualification.

FR-3 initial apply work is authorized to begin with the exact-0.10.0 contract
fixture refresh. The focused contract gate precedes enabling the write boundary;
see `implementation-plan.md` and `../docs/fr3-initial-apply-readiness.md`.
That contract gate passed with a minor finding, now patched. `facet_execution`
supplies request/evidence helpers; `facet_apply` and `facet_apply_transport` now
integrate initial apply. The runtime audit's repair findings are closed by a
passing focused recheck; see `implementation-plan.md` for current status and
evidence. Exact installed-package/public-Spine technical qualification has now
passed locally under FR-5; see `../docs/fr5-qualification.md` and the boundary below.
FR-4's recovery/verify contract and fixture recheck has passed. Its first runtime
increment added read-only historical lineage observation and exact accepted-prefix
comparison. Subsequent authorized increments add candidate/replay correlation and
internal same-execution continuation and independent read-only verification.
Their runtime repair recheck passed at `965326a` with zero findings. The next
operator-authorized increment exposes CLI continuation and verify with synthetic
public-command tests; its separate FR-5 qualification evidence does not authorize
a release or curated pack content.

## Relationship

FR-2 adds `facet_manifest`, `facet_graph`, `facet_contracts`, `facet_inventory`,
`facet_observation`, `facet_transport` and `facet_planning` in the existing package.
They implement manifest-v2/request-v2 read-only `plan`. The CLI uses the same
selection assertions and private no-clobber output publication. V1 dispatch and
supported-baseline allowlists are unchanged. The planning transport rejects every
write; initial and continued v2 apply use the same separate 11-command adapter.
V2 verify constructs only the FR-2 read adapter. CLI flags and artifact families
are unchanged; input validation precedes transport construction.

`facet_recovery.RecoveryPreimage` revalidates the approved graph, checkpoint,
contiguous accepted evidence and any exact unresolved request before observation.
It derives a private semantic/identity comparison view by forwarding only
accepted effects. Original immutable revisions survive head changes in lineage;
known revisions cannot change root, decoder or body. Mutable profile metadata
is not immutable revision content, but remains part of full state comparison.
`observe_prefix` uses the existing two-pass public observer and global budget,
with exact historical reads deduplicated only within each pass. Saved lineage
bodies are hints, never fresh read evidence. Current public fingerprints are
validated independently, not predicted or republished as Spine attestations.
`compare_prefix` retains its strict exact-prefix boundary. The separate `admit`
method admits that prefix or prefix plus only the durable unresolved action,
without advancing evidence or resolving a suffix producer. Fresh observation
also retains a pending head advance's original revision and captures the relevant
full archetype/rendering record in both existing passes under the same budget.
Available archetype creation/revision provenance and rendering creation/publish
provenance must correlate. No facet provenance is invented. A private admission
handle retains rendering records for exact replay comparison, the unchanged retry
request and the appropriate immediate binding precondition.

`facet_apply.apply_continuation` validates an operator-selected same-execution checkpoint or
terminal partial result, performs bounded fresh admission, and publishes the
admitted checkpoint at a new private destination before retry. It shares the
existing initial-apply loop: prepared durability before submission and accepted
durability before consumers. Only validated responses and fresh readback can
extend the prefix; provisional IDs cannot alter requests or CAS inputs. Complete
checkpoints can produce applied results without writes after admission.
Admission failures propagate without publication or a false `not_applied` claim;
post-admission failures preserve a partial checkpoint, while durability failures
stop without fabricating terminal success. Source evidence is never overwritten.
The service takes decoded source artifacts and a new checkpoint writer. The CLI
uses the inherited `apply --continue-from SOURCE` flags and validates SOURCE
before constructing a transport. Checkpoint and result destinations MUST be new
and distinct from each other, SOURCE, manifest, plan, approval and target files.
SOURCE MUST be distinct from other inputs and target files before it is opened.
For v2 source and verification-result inputs, compare resolved paths and existing
file identities so symlink and hard-link aliases to protected files fail closed.
No source discovery, source overwrite or artifact merging is introduced. The
reviewed runtime services and this later CLI wiring have separate test evidence;
FR-5 technical qualification is recorded in `../docs/fr5-qualification.md`;
bounded review of that qualification increment remains pending.

`facet_verification.verify_installation` is a separate internal read-only
boundary, with manifest/plan and optional captured apply-result input, no
approval file. Shared pure plan validation rebuilds saved intent before target
use without requiring applicability for draft inspection. The stricter execution
context remains mandatory for validating supplied execution claims. Invalid
outer result syntax/schema/digest/size fails before public observation; valid
outer artifacts with contradictory embedded evidence instead yield invalid
coverage and a completed mismatch after successful fresh reads. Checksum-only
approval reconstruction neither authorizes writes nor authenticates an operator.

Verification uses the existing complete two-pass observer without retaining
unused execution lineage or replaying writes. It compares selected active state
with identities from approved retained observations and validated responses only.
Schema/rendering heads, facet pins, facet bindings and v2 profile pins remain
exact; readable old revisions or equal content on another root are insufficient.
Archetypes, ordinary v1 profiles and same-target default bindings preserve their
existing equivalence rules. Missing or blocked identities cannot be filled from
fresh convenient rows, and blocked plan resolutions remain blocked. Unselected
valid changes alone do not fail verification. Corrupt or unavailable public
evidence aborts observation rather than becoming an object mismatch.

The sealed v2 result separates captured-response coverage from fresh state, with
the exact 0.10.0 captured-only receipt label and mandatory separate-disclosure
marker. No-write draft state may verify without a result, but a supplied execution
claim for an ineligible plan is invalid. Completed verification publishes a new
private sealed artifact and exits 0 for verified state or 10 for mismatch. It
never invokes apply, continuation, checkpoint writers, receipt/disclosure reads
or writes. Synthetic public-command tests are not installed-package qualification.

The v2 CLI takes `verify --manifest MANIFEST --plan PLAN [--result RESULT]
--output VERIFICATION`. Supplied RESULT must be distinct from manifest, plan and
target files before opening; output must be new and distinct from every input
and target. An explicitly supplied JSON null is invalid artifact input, not an
omitted result. Input/observation/publication failures emit only their owning
error envelope, never a fabricated verification artifact. Continuation admission
failure likewise publishes no checkpoint/result and makes no `not_applied` claim.
After admission, partial application publishes the terminal partial result and
exits 9; durability/publication errors retain their owning error handling without
fabricating success. Existing private no-clobber publication is reused.

`facet_execution.ExecutionContext` checks the manifest, saved plan, observation
projection and complete approval, and rebuilds the plan before constructing any
request. It owns private input copies. It validates a contiguous evidence prefix
before resolving typed producer outputs for the next action. Public response
bytes and family-specific receipt/readback correlations are validated using only
pinned local schemas, without transport or artifact writes. Returning candidate evidence does not advance
the context and does not authorize a consumer or attest durable acceptance.

The initial-apply executor MUST perform fresh public preflight before
submitting constructed requests and obtain validated public readback before
validating response evidence. It MUST durably publish
accepted evidence before passing it in a subsequent consumer's accepted prefix.
The helper cannot prove authenticity, freshness or durability from supplied data.
`facet_apply` now repeats the complete two-pass plan observation and requires the
exact saved plan before submission. Known-ID requests are validated before
target access. Each binding receives an immediate bounded public recheck; facet
requests also retain `expected_binding_id` CAS, including null for absence.

`facet_apply_transport.FacetApplyCommand` inherits the public CLI process boundary
but admits exactly the 11 reviewed configuration writes and preserves stdout
bytes. Writes retain a 30-second/16-MiB ceiling independent of read budgets.
Malformed envelopes, unknown failure codes and inconsistent CLI exits fail closed;
controlled write rejections retain the public code without arbitrary messages.

After each response, initial apply obtains current public show/list readback,
validates ownership, immutable hashes and exact requested state, and only then
constructs accepted evidence. Each readback/recheck operation uses the existing
global observation budget and per-call limits. No item/facet-value/disclosure
or delivery command belongs to the adapter.

The existing durable writer is reused with a v2-specific artifact validator;
its v1 default is unchanged. A prepared checkpoint is durable before submission;
an accepted checkpoint is durable before the next consumer. Once submitted,
any write/response/readback failure returns `partial` with the exact unresolved
request retained. Failures before the first submission return `not_applied`.
Publication failures propagate without a success claim; a result-file failure
may leave only the valid durable checkpoint. No-action plans publish an empty
complete checkpoint. CLI input/output/checkpoint collision protections remain.

Runtime tests use synthetic wire data, saved full read transcripts and local
filesystem faults. These are not FR-5 installed-package/Spine qualification.
Existing v1 execution remains unchanged.

The bounded pinned-vocabulary validator is independent of the frozen v1 decoder
and cross-checked with official Draft 2020-12 in development. Unknown vocabulary
fails closed. Offline sibling schema references supply the complete transitive
closure without runtime dependencies or network schema resolution.

`scripts/qualify_fr2.py` is isolated test setup, not installer apply. It accepts
no existing ledger, attests exported/wheel/installed Spine bytes against the
exact Git tree, and exercises synthetic configuration through public CLIs only.
This narrow gate does not complete FR-5 or authorize release/installation.

### FR-5 qualification boundary

The operator authorized `scripts/qualify_fr5.py` and the opt-in
`tests/integration/test_facet_spine.py` harness to qualify source and clean-wheel
v2 plan/apply/continuation/verify against exact Spine `0.10.0` above. This tooling
MUST export exact Git commits into new private directories, build isolated
packages, and attest Git/export/wheel/installed bytes before execution. It MUST
retain all existing v1 supported-baseline source and installed regression gates.
It MUST NOT substitute the reference checkout's HEAD or broaden any allowlist.
Upstream Git invocations MUST disable replacement objects so local replacement
refs cannot change the bytes attributed to an exact pin.

Only newly allocated disposable ledgers are permitted. Public administrative
CLIs may initialize them and bootstrap synthetic subjects; configuration setup
may use the reviewed public commands. Protected cursor files contain generated
test configuration. No existing-ledger argument is accepted. The harness MUST
NOT import Spine internals, open database contents, author items/facet values,
grant disclosure, materialize reminders or send notifications. Read-only phases
check ledger/WAL file metadata without opening those files.

Normal operations and continuation run in fresh CLI processes. Test-only fault
injection may intercept the installer transport in-process to lose a genuine
successful public response or fail before submission; it MUST NOT fabricate
successful Spine responses. All 11 v2 writes require exact replay/request and
returned-ID correlation. Installed tests MUST use bundled resources with no
checkout module/schema fallback. Failures retain private evidence; success is
local candidate qualification, not a release, deployment or consumer rendering
claim. Version/content decisions and publication remain FR-6/separate approval.
Full qualification MUST require all four named scenarios in each harness to
succeed without skipped scenarios or subtests; focused runs cannot authorize a
full-matrix success marker. Package and matrix parents MUST validate completion
evidence. Completed-checkpoint continuation MUST be tested with the original
approval after live binding drift, requiring fresh-admission refusal without
ledger mutation, source overwrite or new checkpoint/result publication.
Parent completion checks MUST select their expected scenario IDs independently
of the child report, using the shared v1/v2 registry for the harness invoked.
Both reported ID lists MUST match that selected registry. Before drift, tests
MUST read the exact continuation checkpoint file and assert its full ordered
accepted-action sequence, null next action and null unresolved submission.

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
