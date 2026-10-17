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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-fr3-contract-audit-001/audit-notes.md
Hash: 629e3e1035b3bb0eb97a8f6ec2359c55cdf53f6f932b65ac014172f9013c7204

# Change Intent

Perform one focused reviewer-only consistency audit of the FR-3 exact-0.10.0
initial-apply contract-fixture refresh committed as
`97e09b5db6bff382e1c69054a8db1f961c35a225`. This is the contract gate before
implementing the successor initial-apply executor, not a whole-installer audit
or a declaration of convergence/runtime qualification.

Spine baseline remains exact commit
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`, schema `19`.
No compatibility range, public schema change, runtime write permission, released
pack mutation, disclosure approval or domain-item behavior is introduced here.

# Expected Boundary

The new synthetic create/update fixtures derive from preserved 0.9.1 FR-1
examples but regenerate compatibility, manifest/plan/approval identities,
command IDs, exact request/response correlations and checkpoint/result digests.
The checked-in index pins new bytes and historical-source bytes independently.
Returned IDs/receipts remain synthetic, never actual Spine execution evidence.

Review these questions:

1. Do both flows consistently use the exact 0.10.0 inventory, 18-contract union
   and current plan identities, without stale command/approval correlations?
2. Does the refresh helper preserve the three receipt families and immutable
   post-observation facts while correctly updating request-bound provenance?
3. Do the independent oracle and eight new tests actually check all 11 write
   kinds, dependency-consuming slots, complete approvals, prepared/accepted
   contiguous prefixes and first-submission partial failure artifacts?
4. Could the refresh create a self-confirming fixture that hides a meaningful
   mismatch with the current read-only planner? Inspect its exact-plan parity
   test; production code is supplied only for that static comparison.
5. Are the claims correctly limited to contracts, with actual write transport,
   response/readback validation and filesystem durability still unimplemented?
6. Is excluding recovery/verification from this increment explicit and coherent,
   including deferral of the historical 0.9.1 verification evidence label to FR-4?

Only report concrete inconsistencies or material holes affecting this refresh
or the ability to begin FR-3 implementation. Do not require FR-3 runtime proof
as a condition of this pre-implementation contract audit. Proposed future write
commands are data in plans, not currently enabled execution authority.

# Specs To Check

The separately approved payload lists exact files and SHA-256 hashes. Normative
authority is `specs/facet-rendering-packs.md`, `specs/installer-artifacts-v2.md`
and `specs/implementation-plan.md`. AGENTS states the same gate. Readiness notes
are evidence summaries, not normative policy. The inventory and new fixture
index define the exact execution baseline and provenance.

The payload intentionally includes test source, the independent test oracle,
its manifest/hash helpers and unchanged read-only planning source. These are
needed to assess whether fixture generation and validation can mask defects;
this is a static review, not permission to execute code or inspect imports.

Unchanged schema closures and historical fixture bodies are omitted to bound
the payload. Do not claim independent inspection of those omitted files. Local
evidence: the official Draft 2020-12 suite passed all 98 tests without skips,
including the eight new tests, and all 142 runtime tests passed. Repository and
whitespace checks passed. On staging, the focused eight tests and verifier were
rerun successfully. Test success supports but does not decide this audit.
Historical-source hashes and deterministic regeneration are checked locally by
the new tests. No upstream test count substitutes for these installer checks.

# Out Of Scope

No Editor, source changes, tools, browsing, tests, shell execution or extra file
reads. Do not follow imports or paths as authority to expand the payload. If an
omission prevents a scoped conclusion, name the missing evidence and stop that
conclusion rather than treating assumed content as inspected.

No reopening unchanged v1 behavior, FR-2 observation/transport, historical
FR-1 contracts or whole-pack content. No successor recovery/verify implementation,
curated flight fields/templates, schema redesign, new error taxonomy, deployed
ledger access, direct SQL, Spine modifications, publication or deployment.
No runtime writes, disclosure grants, items, facets on items, reminders or sends.
Findings do not authorize patches, release, commit, push or compatibility changes.

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/AGENTS.md

Hash: c8953e3a4e4de4e81bddbf6e22f35e854b56bec5eacb4ea1fa9d58c98c0b2898

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
reviewed FR-1 contracts plus implemented FR-2 read-only planning. FR-3 initial
apply work is operator-authorized, starting with the exact-0.10.0 execution
fixture refresh and focused contract review before enabling the write boundary.
Successor recovery/verify remain unauthorized. The explicitly authorized repaired-baseline listing gate may use
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
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122` (`0.10.0`, schema `19`). The original
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7` listing finding and audit are historical
evidence and MUST NOT be rewritten. Existing
runtime allowlists, v1 contracts and pack artifacts remain unchanged. Do not
provision destination disclosure, create items, materialize reminders or send
notifications as part of configuration installation. The staged bounded audit
requires explicit payload approval before any external reviewer invocation.

FR-2 explicitly authorizes the separate v2 read-only planner against this exact
pin, including `facet_schema.revision.show` and new disposable configuration-only
qualification via public CLIs. Never probe candidate roots or suppress missing
referenced evidence. FR-3 is beginning at its contract gate; the current v2
runtime still rejects all writes. Successor recovery/verify remain unauthorized. Preserve
the 0.9.1 inventory, fixtures and earlier investigation as historical evidence.

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

### Spec 2: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/installer-artifacts-v2.md

Hash: 665bbbc3d455c64dbecf37e05a260ed8db7d0541f297fd53ea9be018c76907be

```markdown
# Facet/rendering installer artifacts v2

Status: reviewed FR-1 contracts; implemented FR-2 read-only planning. The operator
has authorized beginning FR-3 initial apply, with a focused contract review before
the runtime write boundary. Successor recovery/verify remain unauthorized.
Read `facet-rendering-packs.md` first. The exact
Spine pin is `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`, schema
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

The offline `spine-readback-0.10.0.schema.json` and embedded-value schema contain
only reachable definitions for the approved command boundary. Their inventory
records source hashes, exact source pointers and mappings. No online schema
resolution, Spine import or handler execution is allowed in contract tests.

## Complete observation preimage

### FR-2 exact revision lookup (2026-10-16)

The current inventory has 23 commands (12 reads, 11 proposed writes) and an
18-contract execution union. The additional read is `facet_schema.revision.show`,
selector `spine.facet-schema-revision-readback.v1`. Invoke public CLI tokens
`facet_schema revision show` with only `contract_version` and the observed
`facet_schema_revision_id`. Its compiled prerequisites are canonical JSON v1,
facet-schema-revision-readback v1, facet-schemas v1 and rendering-integration v1.
No owner, actor, command ID, root ID, cursor configuration or disclosure grant
belongs in this request. Other catalog reads still require their cursor setup.

Resolve selected observed schema pins by exact revision ID. Validate the returned
actual root, owner, key, current pointer and status against the complete owner
inventory; validate the immutable revision, original revision number, root
membership and definition hash. Deduplicate each revision ID within each pass,
not across the two passes. Both passes and all lookups share the existing global
budgets. Historical/retired roots remain readable. If A2/B2 are current and a pin
references B1, retain B/B1 evidence and compare the actual pin with desired A.
Never infer A from the desired key, probe candidate roots, or relabel B1 as A.

A rejected referenced read still aborts observation; it never creates a missing
desired-object classification. The owning readback handler's missing revision
is `referenced_row_not_found`, field `facet_schema_revision_id`, CLI exit 4;
corrupt/unsupported evidence is `environment_failure`, field `facets`, exit 7;
capacity exhaustion is `environment_failure`, field `capacity`, exit 7; invalid
requests exit 2. Validate the command-specific failure schema and exit pairing.
Preflight/transport failures retain their own contracts, never absence evidence.
Only separately recognized, closed preflight envelopes with their owning exit
pairings bypass the revision-handler failure schema. Malformed handler envelopes,
unknown failure shapes and unsupported exit pairings are installer
`transport_or_environment_failure` (exit 11), not ordinary Spine rejection.
Installer failure envelopes retain the existing exit taxonomy (Spine's CLI exit
is not blindly copied as the installer exit). Errors must not leak raw output.

The 0.9.1 inventory, closure and saved FR-1 fixtures remain immutable historical
evidence. The draft v2 schemas permit either singleton baseline declaration for
decoding that evidence; runtime FR-2 accepts only 0.10.0. Plans bind the matching
exact 17- or 18-contract union. This is not a compatibility range or permission
to execute old fixtures. Future execution/recovery/verification codification
must refresh its own gates; the historical receipt-readback label is not changed
as part of this read-only slice.

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
environment and 18-contract union, sorted typed closure, full observation,
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
Before observation, complete-manifest validation MUST reject rendering revisions
whose minimum possible wire encoding exceeds 8,192 bytes. Replace local reference
objects with the wire ID field for this calculation and count at least one UTF-8
byte per unknown nonempty ID; do not count portable key bytes as installed IDs.
Planning MUST repeat this check using every retained observed revision ID. It is
an exact size check when all IDs are known, otherwise a lower bound, and failure
is `invalid_pack_contract_or_digest`. No guessed ID enters an artifact. A passing
lower bound does not waive the final post-resolution materialization check in
the separately authorized execution slice.

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

### FR-3 exact-baseline initial execution fixtures

`contracts/installer-fr3-fixture-manifest.v2.json` indexes separate exact-0.10.0
synthetic initial-apply flows. They use the existing v2 schemas, the 18-contract
execution union and the complete 0.10.0 public closure; no additional artifact
version or runtime range is introduced. Their provenance pins the unchanged
0.9.1 source fixtures. Runtime implementation MUST NOT derive command IDs or
acceptance from the fixture's synthetic returned IDs. Dependent requests may
consume actual public response outputs only after complete evidence validation
and durable acceptance of the producer.

The refresh covers initial apply/checkpoint/result evidence only. The preceding
`captured_responses_only_spine_0.9.1` verification label remains historical FR-1
evidence, not a qualified label for 0.10.0 verification. A successor verification
label and execution/recovery qualification remain FR-4 gates, not FR-3 defaults.
```

### Spec 3: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/facet-rendering-packs.md

Hash: d84c8b16accc0abce76a38a7b5b75529d9ac2c2830ac2b18a4b05ba9586fcdcd

```markdown
# Facet-aware packs: successor contract proposal

Status: reviewed FR-1 contracts; operator-authorized FR-2 read-only planner.
Revision-readback baseline adopted on 2026-10-16. Normative language below defines
the proposed successor, not additional authority for the current installer.

The FR-1 installer-artifact codification is in
[installer-artifacts-v2.md](installer-artifacts-v2.md), with separate v2 schemas,
source inventory and synthetic execution/recovery fixtures. FR-1 review is
complete. FR-2 adds a separate read-only path; it does not widen the v1 runtime's
command allowlists.

## 1. Scope and authority

Propose `spine.pack-manifest.v2` and a separately versioned v2 installer-artifact
family for one flight configuration vertical slice. Preserve v1 decoders,
schemas, fixtures, installer behavior and every released/draft pack artifact.
Do not add rendering fields to a frozen v1 shape or relabel v1 content as v2.

The exact reference is Spine `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime
`0.10.0`, implemented/current ledger schema `19`. The operator explicitly supplied
this replacement pin for historical facet revision readback. The previous
`57cda1c2d5589360ee8efe7155fd20b503034c2a` (`0.9.1`) listing gate remains
historical evidence, not qualification of this new baseline.
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

The first v2 pack declares exactly runtime `["0.10.0"]`. Content contracts are:

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
exact 18-contract registry union in the baseline evidence. Do not infer extra
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
`notification_rendering_definition.list/show`, and `facet_schema.revision.show`
(12 reads); the existing six
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
ordering and pagination condition. Exhaust schema/rendering statuses independently
with fixed filters/limit. Legacy archetype/profile lists use an unfiltered complete
active-and-retired scan so their public fingerprints cover the same full inventory;
default bindings remain active-only. Match show to list facts and selected exact
revisions to pins. Historical facet pins use the revision-addressed algorithm
and failure discipline in `installer-artifacts-v2.md`; no candidate-root probing.
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
0.10.0 environment, typed graph/closure and resolution slots, complete observation
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

Spine 0.10.0 requires a rendering application choice for each surviving definition-
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
The bounded FR-2 read-only public-CLI gate is recorded in
`docs/fr2-qualification.md`; full successor apply/recovery/verify and clean-wheel
qualification remain FR-5 work. If a
public-command gap is found, report it; this task grants no Spine change authority.

## 11. Codification prerequisites and acceptance

The ordered delivery slices are in [implementation-plan.md](implementation-plan.md).
The first FR-1 increment codifies only the manifest in
`contracts/schemas/spine-pack-manifest.v2.schema.json`, with a synthetic draft
flight in `tests/fixtures/pack-manifest-v2/flight.json` and indexed mutation
vectors in `contracts/pack-fixture-manifest.v2.json`. FR-1's bounded reviews are
complete; the schemas remain unreleased. The test oracle lives under
`tests/contract/`, requires
development `jsonschema` for structural/meta-validation, and is not runtime code.
Test-only field names, flags and template choices are not curated product approval.
Post-resolution Spine byte bounds still require the later installer-artifact
vectors; a portable-manifest check alone cannot prove those bounds.

The reviewed FR-1 prerequisites are listed below. The additive 0.10.0 readback
closure belongs to the FR-2 increment, not the preserved 0.9.1 review payload:

- `contracts/schemas/spine-pack-manifest.v2.schema.json`, a v2 fixture manifest,
  and semantic reference/normalization/digest tests;
- the seven v2 installer-artifact entry schemas, shared v2 types and embedded
  public-value schema closure, plus the historical exact 0.9.1 readback validators;
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

### Spec 4: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/implementation-plan.md

Hash: e17b53d929c31e373f45098a013848b2c0ed4593551314c6afc57174be667173

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
not a reopening of completed installer Slices 1–6. FR-1 contracts/fixtures are
committed; FR-2 read-only planning is operator-authorized, with the historical
lookup blocker resolved by the explicitly adopted 0.10.0 pin below. The separately approved 14-file bounded audit completed
with one minor clarification, addressed by a local wording patch; see the
[audit disposition](../whetstone_runs/facet-rendering-spec-audit-001/local-assessment.md).
FR-3 initial apply work is now separately operator-authorized, subject to the
focused contract gate below. Successor recovery/verify, curated pack rewrite,
deployment, release and additional external review remain unauthorized. Source baseline: Spine
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

The focused FR-2 re-audit passed with no findings; its evidence is committed as
`16e5f4a`. See `whetstone_runs/facet-rendering-fr2-recheck-001/`. The operator
subsequently authorized beginning FR-3 initial apply. FR-6 product decisions
remain pending; this synthetic flight gate approves no curated fields, labels,
templates or disclosure policy.

### FR-3 initial contract increment (2026-10-17)

The execution-fixture refresh is authored under the exact 0.10.0 inventory and
offline closure. `contracts/installer-fr3-fixture-manifest.v2.json` pins separate
synthetic create/update flows and their unchanged 0.9.1 sources. The new flows
cover all 11 initial write kinds, typed dependency consumers, complete approval,
prepared/accepted checkpoint shapes and partial results, including failure at
the first submitted action. Plan, approval, command, evidence and checkpoint
digests are regenerated, not relabelled. The existing FR-2 planner must reproduce
these independently refreshed plans exactly.

These are contract tests, not proof of actual writes or filesystem ordering.
No executor or write transport is enabled by this increment. Next: focused
review of this contract increment (external payload requires fresh approval),
then implement FR-3 command serializers/evidence validation, write allowlist,
initial apply orchestration and durable publication/fault-injection tests.
Retain the existing read-only plan guard and unchanged v1 execution path.

Do not refresh or claim successor recovery/verification in this increment.
The old verification evidence label belongs to the preserved FR-1 fixtures;
the exact-0.10.0 verification label and fixtures must be reviewed before FR-4.
See `docs/fr3-initial-apply-readiness.md` for gate results and limitations.
```

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/docs/fr3-initial-apply-readiness.md

Hash: 7cf161353b16bbc558b47a4a9564048fc65b416badcac37062efc154c30f432a

```markdown
# FR-3 initial-apply readiness

Date: 2026-10-17. The operator requested committing the clean FR-2 re-audit and
beginning implementation. Audit evidence was committed as `16e5f4a`; nothing was
pushed. Normative authority remains `specs/implementation-plan.md` and
`specs/installer-artifacts-v2.md`.

## This increment

FR-3 starts at the required exact-baseline execution-contract refresh. The exact
Spine commit `8f3c50b6fd1b4aa534e50925b7417a7a80d19122` exists locally. All 20
`upstream/` schema inputs in `installer-spine-0.10.0-inventory.json` were compared
with `git show <exact-pin>:<path>` and match their recorded SHA-256 hashes. No
HEAD substitution, Spine checkout modification, build, ledger or Spine command
execution was needed for this synthetic contract increment.

The new fixture index pins two separate initial-only flight flows for runtime
0.10.0/schema 19, plus the unchanged historical 0.9.1 sources. An independent
test-only refresh helper regenerates manifest/plan/approval identities, all
command IDs, submitted requests, correlated responses and checkpoint/results.
Returned IDs and receipts are synthetic; they are not captured public-CLI proof.
The current read-only planner must reproduce the independent plans exactly.

Eight focused contract tests cover all 11 configuration write kinds, all
producer-dependent request slots, prepared and accepted prefixes, first-action
and later partial failures, stale/incomplete approvals, exact version/contract
requirements and malformed receipt/owner/root/byte evidence for every command.
Official Draft 2020-12 validation uses the exact 0.10.0 offline public closure.
The old fixtures and their recovery/verification claims are preserved unchanged.

This does **not** prove filesystem durability, real response validation, writes,
continuation, verification or package qualification. No runtime code, schema,
released pack or existing compatibility allowlist changes in this increment.
The component-scaffold guidance keeps the work in the existing contracts/tests
layout without introducing a new runtime architecture.

## Verification

- Repository verifier: passed, 166 required files.
- Focused FR-3 contract suite: eight tests passed without skips.
- Complete official Draft 2020-12 contract suite: 98 tests passed without skips.
- Required system-Python contract command: 98 tests ran, 33 skipped because
  development `jsonschema` is unavailable there; the complete gate above used
  `/private/tmp/spine-packs-fr2-0100.WbU0lE/env/bin/python`.
- Complete runtime suite: 142 tests passed without skips.
- `git diff --check` and explicit new-file whitespace checks: passed.

Reproduce the focused gate with a development interpreter providing `jsonschema`:

```sh
python -m unittest discover -s tests/contract -p 'test_fr3_artifact_contract.py'
```

## Next gate and implementation

1. Focused contract review of the exact-0.10.0 initial-apply refresh. An external
   Whetstone invocation still needs a separately staged, approved payload.
2. Implement command-specific serializers and response/readback validators.
   Preserve catalog, facet and rendering receipt distinctions; never treat a
   response output or planned producer as acceptance by itself.
3. Implement initial-only apply orchestration with exact approval and fresh
   preflight, an explicit 11-write allowlist, prepared-before-submit and
   accepted-before-consumer durable checkpoints, binding guards and partial
   failure results. Keep the read-only planner transport write-disabled.
4. Add filesystem/transport fault-injection tests at every durability boundary,
   including rendering size checks after resolving real IDs. Preserve all v1
   behavior and reject successor continuation/verify until FR-4 authorization.

No product decision is needed to refresh these synthetic fixtures. Curated
flight fields, templates and disclosure choices remain FR-6 decisions. The
historical verification label naming 0.9.1 is explicitly not refreshed here:
FR-4 must settle its 0.10.0 successor before implementing verification.
```

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/installer-spine-0.10.0-inventory.json

Hash: e4694cfa53fd274df466420cbcca69af71da704a7917381c90f07bfc9a30d2a2

```markdown
{
  "spine_commit": "8f3c50b6fd1b4aa534e50925b7417a7a80d19122",
  "runtime_version": "0.10.0",
  "ledger_schema": "19",
  "required_execution_contracts": [
    "spine.archetype-facet-bindings.v1",
    "spine.canonical-json.v1",
    "spine.facet-cursor.v1",
    "spine.facet-schema-revision-readback.v1",
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
    },
    "facet_schema.revision.show": {
      "request": "revision_readback_141",
      "response": "revision_readback_142",
      "failure": "revision_readback_143",
      "family": "facet_revision",
      "selector": "spine.facet-schema-revision-readback.v1",
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
    "upstream/contracts/schemas/system-info-response-v3.schema.json": "d4031875ec3029b907113b650b6634fdf8d0eb7b5814a401f21cc2e92c1bd9e8",
    "upstream/contracts/schemas/facet-schema-revision-show-request.schema.json": "d46eb34485c64624be347d65ae4d8e309cc8ed20dd59459995d947ef8e4a1d12",
    "upstream/contracts/schemas/facet-schema-revision-show-response.schema.json": "48be527872412111b35a964ba172609422465cc7e349693701c420c296a9a2fb",
    "upstream/contracts/schemas/facet-schema-revision-show-failure.schema.json": "bd270c411dbb0442d27450f993bfe4ac907d6498f5c5ebc3783d7ddc6910c04f"
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
    "upstream/contracts/schemas/system-info-response-v3.schema.json#": "public_0115",
    "upstream/contracts/schemas/facet-schema-revision-show-request.schema.json#": "revision_readback_141",
    "upstream/contracts/schemas/facet-schema-revision-show-response.schema.json#": "revision_readback_142",
    "upstream/contracts/schemas/facet-schema-revision-show-failure.schema.json#": "revision_readback_143"
  },
  "limits": {
    "calls": "4096",
    "stdout_bytes": "134217728",
    "elapsed_seconds": "600",
    "entries": "4096",
    "per_call_seconds": "30",
    "per_call_stdout_bytes": "16777216"
  },
  "revision_readback_authority_sha256": {
    "contracts/facet-schema-revision-readback-fixture-manifest.json": "0e0d357b9fb94dbd9b0b0b5aaa9648b9633014bb5e1efc24752394a7d3c18aa1",
    "contracts/facet-schema-revision-readback.v1.json": "3dca53927ac184abda906bbb810b1e1c73d563012b95cabc27c64182e6f8d4b8",
    "specs/facet-schema-revision-readback.md": "be263114ca40f397f392acabce7f5a8b1d10b32ab44692cd9275d67190a88ca6",
    "src/spine/commands/registry.py": "23d67494679ac8bbf1e0d17763a63ad34ecbe3e443ea3143da7296b835674173",
    "src/spine/contracts/revision_readback/facet-schema-revision-readback.v1.json": "3dca53927ac184abda906bbb810b1e1c73d563012b95cabc27c64182e6f8d4b8",
    "src/spine/contracts/revision_readback/pins.v1.json": "3c67785c1a6c9c7d6c8c8a2f5183a464fca8934e763000cd60d59929c32b9816",
    "src/spine/contracts/revision_readback/schemas/archetype-facet-types.schema.json": "689163800b0aaa07b87a1fc75a7bea7150bd70f1bcf2fbad901466cdf594dcda",
    "src/spine/contracts/revision_readback/schemas/facet-schema-revision-show-failure.schema.json": "bd270c411dbb0442d27450f993bfe4ac907d6498f5c5ebc3783d7ddc6910c04f",
    "src/spine/contracts/revision_readback/schemas/facet-schema-revision-show-request.schema.json": "d46eb34485c64624be347d65ae4d8e309cc8ed20dd59459995d947ef8e4a1d12",
    "src/spine/contracts/revision_readback/schemas/facet-schema-revision-show-response.schema.json": "48be527872412111b35a964ba172609422465cc7e349693701c420c296a9a2fb",
    "src/spine/contracts/revision_readback/schemas/notification-profile-types.schema.json": "182353b53719d924cb062d898d7e3cae1f0de9e124bb2b793c26fa6a59ab6b8c",
    "src/spine/contracts/revision_readback/schemas/notification-types.schema.json": "48507bcf78b6df80a6c9ca8ebf7b0a5fa7e26b8b691befdc1e7353ae63b7b2c1"
  },
  "revision_readback_prerequisites": [
    "spine.canonical-json.v1",
    "spine.facet-schema-revision-readback.v1",
    "spine.facet-schemas.v1",
    "spine.notification-rendering-integration.v1"
  ],
  "revision_readback_limits": {
    "request_bytes": 1048576,
    "response_bytes": 4194304,
    "definition_bytes": 32768,
    "max_fields": 32,
    "resolved_resources": 100,
    "sqlite_vm_steps": 100000,
    "operation_seconds": 5
  }
}
```

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/installer-fr3-fixture-manifest.v2.json

Hash: 8c6f83fb688d91d94222ddf9a675b01a68895835eb17c7eb816a63653dd660af

```markdown
{
  "stage": "FR-3 initial-apply contract gate; synthetic, not runtime qualification",
  "spine_commit": "8f3c50b6fd1b4aa534e50925b7417a7a80d19122",
  "runtime_version": "0.10.0",
  "ledger_schema": "19",
  "inventory": "contracts/installer-spine-0.10.0-inventory.json",
  "fixtures": [
    {
      "path": "tests/fixtures/installer-v2/flight-create-0.10.0.json",
      "sha256": "9e3e586c95c69e7cdcf944b135fd1e8f52d938dbcc5953f94cb62a82d1945065",
      "historical_source": "tests/fixtures/installer-v2/flight-create.json",
      "historical_sha256": "22b8a79711c58ce1ca7331dc906679fecba7f32ca5f733e33dbcbb7748d05dee",
      "commands": [
        "item_archetype.create",
        "facet_schema.create",
        "item_archetype.facet_binding.set",
        "notification_rendering_definition.create",
        "notification_profile.create",
        "notification_profile.binding.set"
      ]
    },
    {
      "path": "tests/fixtures/installer-v2/flight-update-0.10.0.json",
      "sha256": "ce240e8aec27474e3e086d512eb76ec9766f08250c3b057567773d67a940a146",
      "historical_source": "tests/fixtures/installer-v2/flight-update.json",
      "historical_sha256": "8ab30f967392fbd1ac1f4afdec08b9eb07171fd091818c2bd83ebcf320db4866",
      "commands": [
        "item_archetype.revise",
        "facet_schema.publish",
        "item_archetype.facet_binding.set",
        "notification_rendering_definition.publish",
        "notification_profile.metadata.update",
        "notification_profile.revise"
      ]
    }
  ],
  "excluded": [
    "continuation",
    "uncertain-response replay",
    "verification",
    "filesystem durability proof",
    "live or installed-package qualification"
  ]
}
```

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/fr3_fixture_support.py

Hash: d7d022a17c440b193546b05cfb520d6b31799709e8f9dac296f174c455aea228

```markdown
"""Synthetic FR-3 initial-apply vectors; no transport or Spine implementation imports.

Refresh the immutable FR-1 examples using the independent contract oracle, not
the installer implementation. Returned IDs remain explicitly synthetic evidence.
This module neither executes writes nor proves filesystem durability/recovery.
"""
from contextlib import contextmanager
from copy import deepcopy
import json
from unittest.mock import patch

import facet_artifact_oracle as oracle
from test_facet_manifest_contract import digest

INVENTORY = oracle.load(oracle.ROOT / 'contracts/installer-spine-0.10.0-inventory.json')


@contextmanager
def current_contracts():
    """Scope the independent oracle to the exact successor public closure."""
    def public_schema(command, direction, value):
        oracle.validator('spine-readback-0.10.0.schema.json',
                         INVENTORY['commands'][command][direction]).validate(value)

    with patch.object(oracle, 'INVENTORY', INVENTORY), \
            patch.object(oracle, 'COMMANDS', INVENTORY['commands']), \
            patch.object(oracle, 'public_schema', public_schema):
        yield


def plan_check(flow):
    plan = flow['plan']
    oracle.require(plan['environment']['runtime_version'] == '0.10.0', 'exact runtime')
    for field in ('ledger_schema_current', 'ledger_schema_implemented'):
        oracle.require(plan['environment'][field] == '19', 'exact ledger schema')
    oracle.require(flow['manifest']['compatibility']['spine_runtime_versions'] == ['0.10.0'],
                   'exact manifest compatibility')
    oracle.require(plan['required_execution_contracts'] == INVENTORY['required_execution_contracts'],
                   'exact execution union')
    oracle.plan_check(flow['manifest'], flow['request'], plan)


def checkpoint_at(flow, length, prepared=False):
    cp = deepcopy(flow['initial_checkpoint'])
    cp['accepted_responses'] = deepcopy(flow['accepted_responses'][:length])
    actions = flow['plan']['actions']
    cp['next_action_id'] = actions[length]['action_id'] if length < len(actions) else None
    cp['unresolved_submission'] = None
    if prepared:
        action = actions[length]
        request = oracle.materialize(flow['plan'], flow['approval'], action,
                                     cp['accepted_responses'])
        cp['unresolved_submission'] = dict(action_id=action['action_id'],
            command_id=request['command_id'], submission_state='prepared_or_submitted',
            request=oracle.blob(request))
    return oracle.seal(cp)


def reseal_response(evidence, response):
    text = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
    evidence['response'] = dict(json_text=text, digest=oracle.sha(text.encode()))
    evidence['receipt'] = oracle.receipt_projection(evidence['command'], response)


def refresh(historical):
    """Deterministically regenerate an initial-only 0.10.0 fixture in memory."""
    flow = deepcopy(historical)
    # FR-4 owns continuation and verification; do not relabel their old proof.
    for key in ('observations', 'verification', 'envelope'):
        del flow[key]
    manifest = flow['manifest']
    manifest['compatibility']['spine_runtime_versions'] = ['0.10.0']
    manifest['content_identity']['digest'] = digest(manifest)
    plan = flow['plan']
    plan['pack']['manifest_digest'] = manifest['content_identity']['digest']
    plan['environment']['runtime_version'] = '0.10.0'
    plan['environment']['advertised_contracts'] = sorted(set(
        plan['environment']['advertised_contracts'] + INVENTORY['required_execution_contracts']))
    plan['required_execution_contracts'] = INVENTORY['required_execution_contracts']
    flow['plan'] = plan = oracle.seal(plan)
    flow['approval']['plan_digest'] = plan['content_identity']['digest']
    flow['approval'] = approval = oracle.seal(flow['approval'])
    prefix = []
    with current_contracts():
        for action, evidence in zip(plan['actions'], flow['accepted_responses'], strict=True):
            request = oracle.materialize(plan, approval, action, prefix)
            evidence['command_id'] = request['command_id']
            evidence['request'] = oracle.blob(request)
            response = oracle.unblob(evidence['response'], True)
            receipt = response.get('receipt', response)
            receipt['command_id'] = request['command_id']
            if evidence['receipt']['family'] == 'catalog':
                receipt['semantic_facts_hash'] = oracle.hash_value(request)
            if evidence['receipt']['family'] == 'rendering':
                response['record']['published']['command_id'] = request['command_id']
                if action['command'].endswith('.create'):
                    response['record']['created']['command_id'] = request['command_id']
            reseal_response(evidence, response)
            oracle.evidence_check(plan, approval, action, evidence, prefix)
            prefix.append(evidence)
        cp = flow['initial_checkpoint']
        cp.update(plan_digest=plan['content_identity']['digest'],
                  approval_digest=approval['content_identity']['digest'])
        flow['initial_checkpoint'] = oracle.seal(cp)
        for key in ('final_checkpoint', 'prepared_checkpoint'):
            old = historical[key]
            flow[key] = checkpoint_at(flow, len(old['accepted_responses']),
                                      old['unresolved_submission'] is not None)
        for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
            result = flow[key]
            old = result['checkpoint']
            result['checkpoint'] = checkpoint_at(flow, len(old['accepted_responses']),
                                                 old['unresolved_submission'] is not None)
            flow[key] = oracle.seal(result)
    return flow
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_fr3_artifact_contract.py

Hash: 4bab7719fefabb8faf0002b338a98cbbe0416d81b9a79cdc071ffa97ae3d548c

```markdown
"""Exact-0.10.0 initial-apply contract gate, not executor qualification."""
from copy import deepcopy
import sys
import unittest

import facet_artifact_oracle as oracle
from fr3_fixture_support import (INVENTORY, checkpoint_at, current_contracts,
                                 plan_check, refresh, reseal_response)

INDEX = oracle.ROOT / 'contracts/installer-fr3-fixture-manifest.v2.json'


@unittest.skipIf(oracle.Draft202012Validator is None,
                 'FR-3 contract gate requires development jsonschema')
class FR3ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(current_contracts())

    def flows(self):
        return [oracle.load(oracle.ROOT / entry['path'])
                for entry in oracle.load(INDEX)['fixtures']]

    def test_exact_baseline_and_immutable_historical_sources(self):
        index = oracle.load(INDEX)
        self.assertEqual(index['spine_commit'], '8f3c50b6fd1b4aa534e50925b7417a7a80d19122')
        self.assertEqual(index['spine_commit'], INVENTORY['spine_commit'])
        self.assertEqual((index['runtime_version'], index['ledger_schema']), ('0.10.0', '19'))
        self.assertEqual(len(INVENTORY['required_execution_contracts']), 18)
        for entry in index['fixtures']:
            for path, pin in ((entry['path'], entry['sha256']),
                              (entry['historical_source'], entry['historical_sha256'])):
                self.assertEqual(oracle.sha((oracle.ROOT / path).read_bytes()), pin)
            historical = oracle.load(oracle.ROOT / entry['historical_source'])
            current = oracle.load(oracle.ROOT / entry['path'])
            self.assertEqual(current, refresh(historical))
            self.assertEqual(historical['plan']['environment']['runtime_version'], '0.9.1')
            self.assertEqual(entry['commands'], [a['command'] for a in current['plan']['actions']])
            self.assertFalse({'verification', 'observations', 'envelope'} & current.keys())
            self.assertNotEqual(current['plan']['content_identity'], historical['plan']['content_identity'])
            for new, old in zip(current['accepted_responses'], historical['accepted_responses'], strict=True):
                self.assertNotEqual(new['command_id'], old['command_id'])
                self.assertEqual(new['post_observation'], old['post_observation'])

    def test_complete_initial_flows_cover_exactly_eleven_configuration_writes(self):
        commands = set()
        for flow in self.flows():
            plan_check(flow)
            p, a = flow['plan'], flow['approval']
            oracle.approval_check(p, a)
            for key in ('initial_checkpoint', 'prepared_checkpoint', 'final_checkpoint'):
                oracle.checkpoint_check(p, a, flow[key])
            for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
                oracle.result_check(p, a, flow[key])
            commands.update(action['command'] for action in p['actions'])
        expected = {c for c, v in INVENTORY['commands'].items() if v['phase'] is not None}
        self.assertEqual(commands, expected)
        self.assertEqual(len(commands), 11)
        self.assertFalse(any(c.startswith('item.') or 'disclosure' in c or 'send' in c for c in commands))

    def test_current_read_only_planner_reproduces_independent_fixture_plans(self):
        sys.path.insert(0, str(oracle.ROOT / 'src'))
        try:
            from spine_packs.facet_planning import build_plan, validate_inputs
            for flow in self.flows():
                validate_inputs(flow['manifest'], flow['request'])
                p = flow['plan']
                self.assertEqual(build_plan(flow['manifest'], flow['request'],
                                            p['environment'], p['observation']), p)
        finally:
            sys.path.pop(0)

    def test_each_prepared_and_accepted_prefix_and_partial_submission(self):
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            for n, action in enumerate(p['actions']):
                with self.subTest(command=action['command']):
                    before = checkpoint_at(flow, n)
                    prepared = checkpoint_at(flow, n, True)
                    accepted = checkpoint_at(flow, n + 1)
                    for cp in (before, prepared, accepted):
                        oracle.checkpoint_check(p, a, cp)
                    self.assertEqual(prepared['accepted_responses'], before['accepted_responses'])
                    self.assertEqual(prepared['unresolved_submission']['request'],
                                     flow['accepted_responses'][n]['request'])
                    partial = deepcopy(flow['empty_prefix_partial'])
                    partial['checkpoint'] = prepared
                    partial['failure']['action_id'] = action['action_id']
                    partial['unattempted_action_ids'] = [x['action_id'] for x in p['actions'][n + 1:]]
                    oracle.result_check(p, a, oracle.seal(partial))
                    self.assertEqual(partial['state'], 'partial')  # Includes n == 0.
                    partial['state'] = 'not_applied'
                    with self.assertRaises(ValueError):
                        oracle.result_check(p, a, oracle.seal(partial))

    def test_consumers_cannot_resolve_without_accepted_producers(self):
        exercised = set()
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            resolutions = {r['object_key']: r for r in p['resolutions']}
            for n, action in enumerate(p['actions']):
                for slot in action['slots']:
                    source = resolutions[slot['object_key']][slot['field']]
                    if source['kind'] != 'action_result':
                        continue
                    prefix = [e for e in flow['accepted_responses'][:n]
                              if e['action_id'] != source['action_id']]
                    with self.subTest(command=action['command'], slot=slot['request_pointer']):
                        with self.assertRaisesRegex(ValueError, 'consumer before accepted producer'):
                            oracle.materialize(p, a, action, prefix)
                    exercised.add(action['command'])
        self.assertEqual(exercised, {'item_archetype.facet_binding.set',
            'notification_rendering_definition.create', 'notification_rendering_definition.publish',
            'notification_profile.create', 'notification_profile.revise', 'notification_profile.binding.set'})

    def test_each_command_rejects_uncorrelated_receipt_owner_root_and_bytes(self):
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            for n, action in enumerate(p['actions']):
                for failure in ('command', 'owner', 'root', 'response_bytes', 'request_bytes'):
                    with self.subTest(command=action['command'], failure=failure):
                        evidence = deepcopy(flow['accepted_responses'][n])
                        if failure == 'command':
                            response = oracle.unblob(evidence['response'], True)
                            response.get('receipt', response)['command_id'] = 'unrelated-command'
                            reseal_response(evidence, response)
                        elif failure == 'owner':
                            evidence['post_observation']['owner']['owner_subject_id'] = 'unrelated-owner'
                        elif failure == 'root':
                            evidence['post_observation']['root_id'] = 'unrelated-root'
                        elif failure == 'response_bytes':
                            evidence['response']['json_text'] += ' '
                        else:
                            evidence['request']['canonical_json'] += ' '
                        with self.assertRaises(ValueError):
                            oracle.evidence_check(p, a, action, evidence, flow['accepted_responses'][:n])

    def test_stale_approval_and_missing_update_authorization(self):
        for flow in self.flows():
            approval = deepcopy(flow['approval'])
            approval['plan_digest'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'stale approval'):
                oracle.approval_check(flow['plan'], oracle.seal(approval))
        flow = self.flows()[1]
        approval = deepcopy(flow['approval'])
        approval['authorized_update_action_ids'].pop()
        with self.assertRaisesRegex(ValueError, 'update authorization'):
            oracle.approval_check(flow['plan'], oracle.seal(approval))

    def test_exact_runtime_and_contract_union_are_not_inferred(self):
        for mutation in ('runtime', 'manifest', 'schema', 'union'):
            flow = self.flows()[0]
            if mutation == 'runtime':
                flow['plan']['environment']['runtime_version'] = '0.10.1'
            elif mutation == 'manifest':
                flow['manifest']['compatibility']['spine_runtime_versions'].append('0.10.1')
            elif mutation == 'schema':
                flow['plan']['environment']['ledger_schema_current'] = '20'
            else:
                flow['plan']['required_execution_contracts'].remove('spine.facet-schema-revision-readback.v1')
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'exact'):
                plan_check(flow)


if __name__ == '__main__':
    unittest.main()
```

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/facet_artifact_oracle.py

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

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_facet_manifest_contract.py

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

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/installer-v2/flight-create-0.10.0.json

Hash: 9e3e586c95c69e7cdcf944b135fd1e8f52d938dbcc5953f94cb62a82d1945065

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
        "0.10.0"
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
      "digest": "1c2aa56dd4be6ac5e303b38bcd57923366f53f1a2791a8cfe242f97709848113"
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
      "manifest_digest": "1c2aa56dd4be6ac5e303b38bcd57923366f53f1a2791a8cfe242f97709848113"
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
      "runtime_version": "0.10.0",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schema-revision-readback.v1",
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
      "spine.facet-schema-revision-readback.v1",
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
      "digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b"
    }
  },
  "approval": {
    "artifact_schema": "spine.pack-install-approval.v2",
    "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
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
      "digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4"
    }
  },
  "accepted_responses": [
    {
      "action_id": "action-000000",
      "command": "item_archetype.create",
      "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
        "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
        "digest": "8be296206763ced8dddaf01cc17b9a29c2981283212a91a7113fc069b3caf677"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_1",
        "effect": "item_archetype_created",
        "semantic_facts_hash": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b",
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
      "command_id": "spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
        "digest": "386d2253c9ccb093b6579323d9d2d7e12fae3fb65c26152a615a7876129b35e9"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
        "digest": "9ee8cb8b9fb89f0b9629340089fc998099955503f11ef6ba8e998cfc05624acb"
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
      "command_id": "spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
        "digest": "3516278a4e12549f514bad3ac8364486a2bf269f7a81dd80607a590a58cc73fb"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
        "digest": "e4feb8946b2ecd2916e75cf1d0a46136cfc698454fcafb223dfe5d9f99c730dd"
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
      "command_id": "spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
        "digest": "eefb39cd2b1f3685ec6dd5009ed56d3fd1c9aec7e835ac7ac01f23a397cfd2bf"
      },
      "response": {
        "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
        "digest": "89d5b87252da8cf3c538d2903946347bda234b26f362eb55857f5953a2bfe13b"
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
      "command_id": "spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
        "digest": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
        "digest": "1589de21b9c93354aa3a21a7b70fd14f7ff9434b4767b0d09a707b11df23472a"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_5",
        "effect": "notification_profile_created",
        "semantic_facts_hash": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f",
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
      "command_id": "spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
        "digest": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
        "digest": "d8ab47fb4acc7e1bd2da0db28c67d8f3a350bc842814e4c40dad0412f0678d25"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_6",
        "effect": "notification_profile_binding_set",
        "semantic_facts_hash": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0",
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
  "initial_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
    "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
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
      "digest": "19b22d5d14906aae930045a50ae0549b866b8e1b4267223251675bc6e6f5a903"
    }
  },
  "final_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
    "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.create",
        "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
          "digest": "8be296206763ced8dddaf01cc17b9a29c2981283212a91a7113fc069b3caf677"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_1",
          "effect": "item_archetype_created",
          "semantic_facts_hash": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b",
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
        "command_id": "spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
          "digest": "386d2253c9ccb093b6579323d9d2d7e12fae3fb65c26152a615a7876129b35e9"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
          "digest": "9ee8cb8b9fb89f0b9629340089fc998099955503f11ef6ba8e998cfc05624acb"
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
        "command_id": "spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "3516278a4e12549f514bad3ac8364486a2bf269f7a81dd80607a590a58cc73fb"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
          "digest": "e4feb8946b2ecd2916e75cf1d0a46136cfc698454fcafb223dfe5d9f99c730dd"
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
        "command_id": "spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "eefb39cd2b1f3685ec6dd5009ed56d3fd1c9aec7e835ac7ac01f23a397cfd2bf"
        },
        "response": {
          "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
          "digest": "89d5b87252da8cf3c538d2903946347bda234b26f362eb55857f5953a2bfe13b"
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
        "command_id": "spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
          "digest": "1589de21b9c93354aa3a21a7b70fd14f7ff9434b4767b0d09a707b11df23472a"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_5",
          "effect": "notification_profile_created",
          "semantic_facts_hash": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f",
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
        "command_id": "spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
          "digest": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
          "digest": "d8ab47fb4acc7e1bd2da0db28c67d8f3a350bc842814e4c40dad0412f0678d25"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_6",
          "effect": "notification_profile_binding_set",
          "semantic_facts_hash": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0",
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
      "digest": "bd7c745205edf42b38089f233cdfa90befc860d298b55118a351ab3a3e740fd0"
    }
  },
  "prepared_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
    "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000001",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.create",
        "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
          "digest": "8be296206763ced8dddaf01cc17b9a29c2981283212a91a7113fc069b3caf677"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_1",
          "effect": "item_archetype_created",
          "semantic_facts_hash": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b",
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
      "command_id": "spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e",
      "submission_state": "prepared_or_submitted",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
        "digest": "386d2253c9ccb093b6579323d9d2d7e12fae3fb65c26152a615a7876129b35e9"
      }
    },
    "next_action_id": "action-000001",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "a5c58232ffc97a87569f2f42cb863b57d65d2eb979da98c3046b294241141bf3"
    }
  },
  "partial_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
      "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.create",
          "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
            "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
            "digest": "8be296206763ced8dddaf01cc17b9a29c2981283212a91a7113fc069b3caf677"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_1",
            "effect": "item_archetype_created",
            "semantic_facts_hash": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b",
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
        "command_id": "spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
          "digest": "386d2253c9ccb093b6579323d9d2d7e12fae3fb65c26152a615a7876129b35e9"
        }
      },
      "next_action_id": "action-000001",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "a5c58232ffc97a87569f2f42cb863b57d65d2eb979da98c3046b294241141bf3"
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
      "digest": "afba8bcb25c9096168adc5cf9840dd9158562db57c02c535333a0a8f0154045b"
    }
  },
  "empty_prefix_partial": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
      "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [],
      "unresolved_submission": {
        "action_id": "action-000000",
        "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
          "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
        }
      },
      "next_action_id": "action-000000",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "7f9a7cbcfff84883d6a71ba4baff1e20038355c54eea4209fb6b7a19af46c0e6"
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
      "digest": "09210681b69fae1976222072f7d38afec18e80b22bd8628c0357ff637d9c5a33"
    }
  },
  "apply_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "09dc5c1af3957a6d455df05d31f2fbed25cdb16e65129ef1ac8326b2efb69d2b",
      "approval_digest": "8da91605dd188941ed9a59879ccda79d74ebd4996f6ea74a70458bff396e97e4",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000001",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.create",
          "command_id": "spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"archetype_key\":\"flight\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"contract_version\":\"spine.item-archetypes.v1\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Flight\"}}",
            "digest": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.create\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_1\",\"command_id\":\"spack_de270f4899a4f85bdaa41dc36f2adac7d9338348a7201d7aada6b24cc712ab5b\",\"effect\":\"item_archetype_created\",\"semantic_facts_hash\":\"03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_1\",\"revision_number\":\"1\",\"archetype_key\":\"flight\"}",
            "digest": "8be296206763ced8dddaf01cc17b9a29c2981283212a91a7113fc069b3caf677"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_1",
            "effect": "item_archetype_created",
            "semantic_facts_hash": "03fa35edd1a33527920983c07386636cd6afa56057b434be754f6cc35cb2ad4b",
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
          "command_id": "spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"schema_key\":\"flight_details\"}",
            "digest": "386d2253c9ccb093b6579323d9d2d7e12fae3fb65c26152a615a7876129b35e9"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"facet_schema.create\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_29fb23c6fb154790dbdeb045c44a9e464c4141e89a102d00fbf705ef40f83d6e\",\"command_receipt_id\":\"receipt_2\",\"effect\":\"facet_schema_created\",\"changed\":true,\"audit_id\":\"audit_2\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":null,\"facet_schema_revision_id\":\"schema_revision_2\",\"revision_number\":\"1\",\"replayed\":false}",
            "digest": "9ee8cb8b9fb89f0b9629340089fc998099955503f11ef6ba8e998cfc05624acb"
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
          "command_id": "spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":null,\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "3516278a4e12549f514bad3ac8364486a2bf269f7a81dd80607a590a58cc73fb"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_3ccae26e5a7f16e2376018c01ca4c3e6c22adc78496b4bc0ed8def2f05ae0cdc\",\"command_receipt_id\":\"receipt_3\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_3\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":null,\"facet_binding_id\":\"facet_binding_binding_3\",\"facet_schema_revision_id\":\"schema_revision_2\",\"replayed\":false}",
            "digest": "e4feb8946b2ecd2916e75cf1d0a46136cfc698454fcafb223dfe5d9f99c730dd"
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
          "command_id": "spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"definition_key\":\"flight_details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
            "digest": "eefb39cd2b1f3685ec6dd5009ed56d3fd1c9aec7e835ac7ac01f23a397cfd2bf"
          },
          "response": {
            "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.create\",\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_created\",\"command_receipt_id\":\"receipt_4\",\"audit_id\":\"audit_4\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_4\",\"revision_number\":\"1\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic flight details\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_2\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"0270f8f49e9f835569cc8a10e8dd116354282de52b44fd8fe5280ef77e31ac67\",\"created\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_3d3fd2633ff714e9521577161d7f14b0fd958f85ec77a0d401477ef09722258d\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
            "digest": "89d5b87252da8cf3c538d2903946347bda234b26f362eb55857f5953a2bfe13b"
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
          "command_id": "spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"contract_version\":\"spine.notification-profiles.v2\",\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"profile_key\":\"synthetic_flight_details\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_4\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.create\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_created\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_5\",\"command_id\":\"spack_6292f1be43b882b50d8b75986c8006943a971e877d787995ae0a7b519ff1aa04\",\"effect\":\"notification_profile_created\",\"semantic_facts_hash\":\"991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"revision_number\":\"1\",\"normalized_revision_hash\":\"689794bd3be44648d72004573c23e416134d13cfef5800daa25b7b5f8b55730b\",\"profile_key\":\"synthetic_flight_details\"}",
            "digest": "1589de21b9c93354aa3a21a7b70fd14f7ff9434b4767b0d09a707b11df23472a"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_5",
            "effect": "notification_profile_created",
            "semantic_facts_hash": "991cb38a212223a3dd0f81ffb2a2923201c1cedff1d3dd11b0cff1998834aa3f",
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
          "command_id": "spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"contract_version\":\"spine.notification-profile-bindings.v1\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"}}",
            "digest": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.binding.set\",\"response_contract\":\"spine.notification-profile-bindings.v1\",\"effect\":\"notification_profile_binding_set\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_6\",\"command_id\":\"spack_83207ca4bba7d86ad71b72c8dee2fbb5d3d0db41e5e5057d45af08ab90096fd0\",\"effect\":\"notification_profile_binding_set\",\"semantic_facts_hash\":\"535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_binding_id\":\"binding_binding_6\",\"item_archetype_id\":\"archetype_1\",\"notification_profile_id\":\"profile_5\",\"compatible_item_types\":[\"event\"]}",
            "digest": "d8ab47fb4acc7e1bd2da0db28c67d8f3a350bc842814e4c40dad0412f0678d25"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_6",
            "effect": "notification_profile_binding_set",
            "semantic_facts_hash": "535969833390a6ee47ad735f4e15afba10c75fb7023fa580aa92938d088b8fa0",
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
        "digest": "bd7c745205edf42b38089f233cdfa90befc860d298b55118a351ab3a3e740fd0"
      }
    },
    "state": "applied",
    "failure": null,
    "unattempted_action_ids": [],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "218b8304a0a19ec316c1a81947b9c72ad75e0024c1aa0f9da425969c38a2cd78"
    }
  }
}
```

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/installer-v2/flight-update-0.10.0.json

Hash: ce240e8aec27474e3e086d512eb76ec9766f08250c3b057567773d67a940a146

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
        "0.10.0"
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
      "digest": "c01b6ce203392c22df465c8c2b0431de7d8c675b860e5eda1f3ab4792723f4d5"
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
      "manifest_digest": "c01b6ce203392c22df465c8c2b0431de7d8c675b860e5eda1f3ab4792723f4d5"
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
      "runtime_version": "0.10.0",
      "ledger_schema_implemented": "19",
      "ledger_schema_current": "19",
      "ledger_instance_id": "ledger_instance_2222222222222222222222222222222222222222222222222222222222222222",
      "advertised_contracts": [
        "spine.archetype-facet-bindings.v1",
        "spine.canonical-json.v1",
        "spine.facet-cursor.v1",
        "spine.facet-schema-revision-readback.v1",
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
      "spine.facet-schema-revision-readback.v1",
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
      "digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f"
    }
  },
  "approval": {
    "artifact_schema": "spine.pack-install-approval.v2",
    "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
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
      "digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf"
    }
  },
  "accepted_responses": [
    {
      "action_id": "action-000000",
      "command": "item_archetype.revise",
      "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
        "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
        "digest": "449356de3c48bf90400d889ed41ec152be23cce4d36b418559dc96b87b1fa7c1"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_101",
        "effect": "item_archetype_revised",
        "semantic_facts_hash": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8",
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
      "command_id": "spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
        "digest": "c75bfd39bd47c9bf1f256c64d891ce7fa23b38493fdecf3d75595999ed5c4dc5"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
        "digest": "2369596a06b12fc4f46679be49995b3da2423fcd5a53c144129944e9a91c24fc"
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
      "command_id": "spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
        "digest": "e95d4e70da01a81ad3eead9ca2fb1877592a3a69d6a4544d34cfc04d6b6470da"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
        "digest": "be60103ed980c2f5e0bdaf5d31ecc0f910131939289d1e2919e8ceea46953e04"
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
      "command_id": "spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
        "digest": "795c9775456972628d9bb75e00dcd6cf8b8944a82f0d8a08f3bfb3a62bd114b0"
      },
      "response": {
        "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
        "digest": "8be81830c3d1f7de986a44375a5329bea91ef0a9687e609d2031d059ea57472f"
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
      "command_id": "spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
        "digest": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
        "digest": "40e3f86ab6b86282b676ff544403359317555920d17ed3064cbad4cb04281acd"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_105",
        "effect": "notification_profile_metadata_updated",
        "semantic_facts_hash": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2",
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
      "command_id": "spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
        "digest": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157"
      },
      "response": {
        "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
        "digest": "4f94c491165de17ade978c584a79bb82e391a63a9891fa51be31af5cded7c49e"
      },
      "receipt": {
        "family": "catalog",
        "command_receipt_id": "receipt_106",
        "effect": "notification_profile_revised",
        "semantic_facts_hash": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157",
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
  "initial_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
    "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
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
      "digest": "200ae30971852b7597952795ddef39fac728c670adb56930ff8c570f6738d75a"
    }
  },
  "final_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
    "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.revise",
        "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
          "digest": "449356de3c48bf90400d889ed41ec152be23cce4d36b418559dc96b87b1fa7c1"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_101",
          "effect": "item_archetype_revised",
          "semantic_facts_hash": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8",
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
        "command_id": "spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
          "digest": "c75bfd39bd47c9bf1f256c64d891ce7fa23b38493fdecf3d75595999ed5c4dc5"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
          "digest": "2369596a06b12fc4f46679be49995b3da2423fcd5a53c144129944e9a91c24fc"
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
        "command_id": "spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
          "digest": "e95d4e70da01a81ad3eead9ca2fb1877592a3a69d6a4544d34cfc04d6b6470da"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
          "digest": "be60103ed980c2f5e0bdaf5d31ecc0f910131939289d1e2919e8ceea46953e04"
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
        "command_id": "spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
          "digest": "795c9775456972628d9bb75e00dcd6cf8b8944a82f0d8a08f3bfb3a62bd114b0"
        },
        "response": {
          "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
          "digest": "8be81830c3d1f7de986a44375a5329bea91ef0a9687e609d2031d059ea57472f"
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
        "command_id": "spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
          "digest": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
          "digest": "40e3f86ab6b86282b676ff544403359317555920d17ed3064cbad4cb04281acd"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_105",
          "effect": "notification_profile_metadata_updated",
          "semantic_facts_hash": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2",
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
        "command_id": "spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
          "digest": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
          "digest": "4f94c491165de17ade978c584a79bb82e391a63a9891fa51be31af5cded7c49e"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_106",
          "effect": "notification_profile_revised",
          "semantic_facts_hash": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157",
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
      "digest": "0d854e42ba73df48b060a80c92fd51da0c44e61be45c7f73c6606828577c2aeb"
    }
  },
  "prepared_checkpoint": {
    "artifact_schema": "spine.pack-apply-checkpoint.v2",
    "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
    "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
    "execution": {
      "execution_id": "12345678-1234-4234-8234-000000000002",
      "actor_subject_id": "synthetic-actor",
      "action_timestamp_utc": "2035-02-01T12:00:00Z"
    },
    "accepted_responses": [
      {
        "action_id": "action-000000",
        "command": "item_archetype.revise",
        "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
        },
        "response": {
          "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
          "digest": "449356de3c48bf90400d889ed41ec152be23cce4d36b418559dc96b87b1fa7c1"
        },
        "receipt": {
          "family": "catalog",
          "command_receipt_id": "receipt_101",
          "effect": "item_archetype_revised",
          "semantic_facts_hash": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8",
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
      "command_id": "spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614",
      "submission_state": "prepared_or_submitted",
      "request": {
        "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
        "digest": "c75bfd39bd47c9bf1f256c64d891ce7fa23b38493fdecf3d75595999ed5c4dc5"
      }
    },
    "next_action_id": "action-000001",
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
      "digest": "c526689d0837d66dcdb263e3966daf69c95bedb604d9415f80b71c9859d1e7de"
    }
  },
  "partial_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
      "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.revise",
          "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
            "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
            "digest": "449356de3c48bf90400d889ed41ec152be23cce4d36b418559dc96b87b1fa7c1"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_101",
            "effect": "item_archetype_revised",
            "semantic_facts_hash": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8",
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
        "command_id": "spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
          "digest": "c75bfd39bd47c9bf1f256c64d891ce7fa23b38493fdecf3d75595999ed5c4dc5"
        }
      },
      "next_action_id": "action-000001",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "c526689d0837d66dcdb263e3966daf69c95bedb604d9415f80b71c9859d1e7de"
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
      "digest": "3b3b6e88fde0a781238191acf8c95bfb3359bbb5b52b0038430fd31ae47ebea2"
    }
  },
  "empty_prefix_partial": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
      "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [],
      "unresolved_submission": {
        "action_id": "action-000000",
        "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
        "submission_state": "prepared_or_submitted",
        "request": {
          "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
          "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
        }
      },
      "next_action_id": "action-000000",
      "content_identity": {
        "algorithm": "sha256",
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine.pack-apply-checkpoint-digest.v2",
        "digest": "c9ce4e9bb9256eabe539238291803cbcb97519a18e46783c9019e84ce7ac5b80"
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
      "digest": "bb2606c272406882c8813060e65f89eb0457cd7672c899897f2eae4a436a1e1a"
    }
  },
  "apply_result": {
    "artifact_schema": "spine.pack-apply-result.v2",
    "checkpoint": {
      "artifact_schema": "spine.pack-apply-checkpoint.v2",
      "plan_digest": "4d2e87560981cd8267406027069ea987f117c1221a188505e5cc802fb857010f",
      "approval_digest": "4192b724277c47338adad7b6074fdf992c070319aa6ce7fbea20d23f5e231baf",
      "execution": {
        "execution_id": "12345678-1234-4234-8234-000000000002",
        "actor_subject_id": "synthetic-actor",
        "action_timestamp_utc": "2035-02-01T12:00:00Z"
      },
      "accepted_responses": [
        {
          "action_id": "action-000000",
          "command": "item_archetype.revise",
          "command_id": "spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"contract_version\":\"spine.item-archetypes.v1\",\"expected_current_revision_id\":\"archetype_revision_1\",\"item_archetype_id\":\"archetype_1\",\"revision\":{\"compatible_item_types\":[\"event\"],\"description\":\"Scheduled flight departures.\",\"display_name\":\"Synthetic revised flight\"}}",
            "digest": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.revise\",\"response_contract\":\"spine.item-archetypes.v1\",\"effect\":\"item_archetype_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_101\",\"command_id\":\"spack_d47f64f0684208a6f81338662de39f4c06393ac79df40a2ed9c84f140f3426d2\",\"effect\":\"item_archetype_revised\",\"semantic_facts_hash\":\"7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"item_archetype_id\":\"archetype_1\",\"item_archetype_revision_id\":\"archetype_revision_101\",\"revision_number\":\"2\"}",
            "digest": "449356de3c48bf90400d889ed41ec152be23cce4d36b418559dc96b87b1fa7c1"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_101",
            "effect": "item_archetype_revised",
            "semantic_facts_hash": "7f22621e7aa7beca93dd3ca5f18bff27adb5d2a8ed9e0498793e3ccf6b6887a8",
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
          "command_id": "spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"contract_version\":\"spine.facet-schemas.v1\",\"definition\":{\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight fields\",\"fields\":[{\"key\":\"flight_number\",\"max_length\":\"32\",\"queryable\":false,\"required\":false,\"type\":\"text\"},{\"key\":\"origin\",\"queryable\":false,\"required\":false,\"target_kind\":\"location\",\"type\":\"reference\"}]},\"expected_current_revision_id\":\"schema_revision_2\",\"facet_schema_id\":\"schema_2\"}",
            "digest": "c75bfd39bd47c9bf1f256c64d891ce7fa23b38493fdecf3d75595999ed5c4dc5"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"facet_schema.publish\",\"response_contract\":\"spine.facet-schemas.v1\",\"command_id\":\"spack_826a6c0a9c17681daf451c41818e310160676d6b39914905d560cdbd18a78614\",\"command_receipt_id\":\"receipt_102\",\"effect\":\"facet_schema_published\",\"changed\":true,\"audit_id\":\"audit_102\",\"facet_schema_id\":\"schema_2\",\"prior_revision_id\":\"schema_revision_2\",\"facet_schema_revision_id\":\"schema_revision_102\",\"revision_number\":\"2\",\"replayed\":false}",
            "digest": "2369596a06b12fc4f46679be49995b3da2423fcd5a53c144129944e9a91c24fc"
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
          "command_id": "spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"contract_version\":\"spine.archetype-facet-bindings.v1\",\"expected_binding_id\":\"facet_binding_binding_3\",\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"item_archetype_id\":\"archetype_1\"}",
            "digest": "e95d4e70da01a81ad3eead9ca2fb1877592a3a69d6a4544d34cfc04d6b6470da"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"item_archetype.facet_binding.set\",\"response_contract\":\"spine.archetype-facet-bindings.v1\",\"command_id\":\"spack_82e10bfae78bfb6285ebdaf70e923ab8b0587e59cd71afea1a0b4f68101a26f0\",\"command_receipt_id\":\"receipt_103\",\"effect\":\"facet_binding_set\",\"changed\":true,\"audit_id\":\"audit_103\",\"item_archetype_id\":\"archetype_1\",\"facet_key\":\"flight\",\"prior_binding_id\":\"facet_binding_binding_3\",\"facet_binding_id\":\"facet_binding_binding_103\",\"facet_schema_revision_id\":\"schema_revision_102\",\"replayed\":false}",
            "digest": "be60103ed980c2f5e0bdaf5d31ecc0f910131939289d1e2919e8ceea46953e04"
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
          "command_id": "spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"expected_current_revision_id\":\"rendering_revision_4\",\"notification_rendering_definition_id\":\"rendering_4\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]}}",
            "digest": "795c9775456972628d9bb75e00dcd6cf8b8944a82f0d8a08f3bfb3a62bd114b0"
          },
          "response": {
            "json_text": "{\"ok\":true,\"contract_version\":\"spine.notification-rendering-definitions.v1\",\"command\":\"notification_rendering_definition.publish\",\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"changed\":true,\"replayed\":false,\"effect\":\"rendering_definition_published\",\"command_receipt_id\":\"receipt_104\",\"audit_id\":\"audit_104\",\"record\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\",\"owner\":{\"owner_kind\":\"subject\",\"owner_subject_id\":\"synthetic-owner\"},\"definition_key\":\"flight_details\",\"status\":\"active\",\"current_revision_id\":\"rendering_revision_104\",\"revision_number\":\"2\",\"revision\":{\"base_rendering_contract\":\"spine.notification-rendering.v1\",\"base_rendering_profile\":\"spine.notification-rendering.concise-en-ca.v1\",\"compatible_item_types\":[\"event\"],\"description\":null,\"display_name\":\"Synthetic revised flight rendering\",\"selections\":[{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"flight_number\",\"label\":\"Flight\",\"projection\":\"value\",\"selection_key\":\"number\"},{\"facet_key\":\"flight\",\"facet_schema_revision_id\":\"schema_revision_102\",\"field_key\":\"origin\",\"label\":\"From\",\"projection\":\"location_label\",\"selection_key\":\"origin\"}]},\"definition_hash\":\"3a70a0ef2bf10cc818a83ad2eea6cbede6914c75bd497feb5e3facc8a48556e5\",\"created\":{\"command_id\":\"spack_fe1d97c7e699937c53f188c70e38d614f879662f890c45f7b9dfbfb7aabbbf92\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"published\":{\"command_id\":\"spack_4ec398978dff62926c2cef35c55d83de3a573120cf5854fbaff3fea643d84a27\",\"actor_subject_id\":\"synthetic-actor\",\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\"},\"retired\":null}}",
            "digest": "8be81830c3d1f7de986a44375a5329bea91ef0a9687e609d2031d059ea57472f"
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
          "command_id": "spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"contract_version\":\"spine.notification-profile-metadata-update.v1\",\"expected_metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic flight details\"},\"metadata\":{\"description\":\"Contract fixture only; not approved curated content.\",\"display_name\":\"Synthetic revised flight reminders\"},\"notification_profile_id\":\"profile_5\"}",
            "digest": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.metadata.update\",\"response_contract\":\"spine.notification-profile-metadata-update.v1\",\"effect\":\"notification_profile_metadata_updated\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_105\",\"command_id\":\"spack_e408e62d0d602764ec1434d6a3c9bee1c8b61a7914c05114257fbde64cdfc408\",\"effect\":\"notification_profile_metadata_updated\",\"semantic_facts_hash\":\"b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_5\",\"display_name\":\"Synthetic revised flight reminders\",\"description\":\"Contract fixture only; not approved curated content.\"}",
            "digest": "40e3f86ab6b86282b676ff544403359317555920d17ed3064cbad4cb04281acd"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_105",
            "effect": "notification_profile_metadata_updated",
            "semantic_facts_hash": "b8b2769ba7badec9ceab0b0cbbb9eab21749e251cae6f3fb7f5bd606556fc9f2",
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
          "command_id": "spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2",
          "request": {
            "canonical_json": "{\"action_timestamp_utc\":\"2035-02-01T12:00:00Z\",\"actor_subject_id\":\"synthetic-actor\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"contract_version\":\"spine.notification-profiles.v2\",\"expected_current_revision_id\":\"profile_revision_5\",\"notification_profile_id\":\"profile_5\",\"revision\":{\"compatible_item_types\":[\"event\"],\"templates\":[{\"late_handling\":{\"grace_seconds\":\"3600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-14400\"},\"kind\":\"once\"},\"template_key\":\"four_hours_before\"},{\"late_handling\":{\"grace_seconds\":\"900\",\"kind\":\"deliver_within\"},\"rendering\":{\"definition\":{\"notification_rendering_definition_id\":\"rendering_4\",\"notification_rendering_definition_revision_id\":\"rendering_revision_104\"},\"kind\":\"definition\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-3600\"},\"kind\":\"once\"},\"template_key\":\"one_hour_before\"},{\"late_handling\":{\"grace_seconds\":\"86400\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-604800\"},\"kind\":\"once\"},\"template_key\":\"seven_days_before\"},{\"late_handling\":{\"grace_seconds\":\"21600\",\"kind\":\"deliver_within\"},\"rendering\":{\"kind\":\"ordinary\"},\"schedule\":{\"at\":{\"kind\":\"target_offset\",\"offset_basis\":\"elapsed\",\"offset_seconds\":\"-86400\"},\"kind\":\"once\"},\"template_key\":\"twenty_four_hours_before\"}]}}",
            "digest": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157"
          },
          "response": {
            "json_text": "{\"ok\":true,\"command\":\"notification_profile.revise\",\"response_contract\":\"spine.notification-profiles.v2\",\"effect\":\"notification_profile_revised\",\"status\":\"active\",\"receipt\":{\"command_receipt_id\":\"receipt_106\",\"command_id\":\"spack_99a8fd5b4371bb19755c28e9fbf5fd77ebc8b93455d858ea4464e2e07d36d0d2\",\"effect\":\"notification_profile_revised\",\"semantic_facts_hash\":\"8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157\",\"created_at_utc\":\"2035-02-01T12:00:00Z\"},\"notification_profile_id\":\"profile_5\",\"notification_profile_revision_id\":\"profile_revision_106\",\"revision_number\":\"2\",\"normalized_revision_hash\":\"7b45a278af7c32d7ed72f69e6597c8ab147b9bd97757c4333b5ad2ce821ad2be\"}",
            "digest": "4f94c491165de17ade978c584a79bb82e391a63a9891fa51be31af5cded7c49e"
          },
          "receipt": {
            "family": "catalog",
            "command_receipt_id": "receipt_106",
            "effect": "notification_profile_revised",
            "semantic_facts_hash": "8714920fcf0a12d631fc460df7bafdd419b7337cf76d4bb81a9c027b6cd1c157",
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
        "digest": "0d854e42ba73df48b060a80c92fd51da0c44e61be45c7f73c6606828577c2aeb"
      }
    },
    "state": "applied",
    "failure": null,
    "unattempted_action_ids": [],
    "content_identity": {
      "algorithm": "sha256",
      "canonical_json_version": "spine.canonical-json.v1",
      "derivation_version": "spine.pack-apply-result-digest.v2",
      "digest": "bc5b24045b55e37b37636c64f19ce47e14f4b528cc7af47905eabb672aa504f9"
    }
  }
}
```

### Spec 14: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/src/spine_packs/facet_planning.py

Hash: 134e6f825c455664cecbb03b73ddfc9d9b9547174e973ff09638d96380af8eba

```markdown
"""FR-2 read-only plan compilation. Proposed write templates are data only."""
from copy import deepcopy

from . import artifacts as a
from .facet_contracts import artifact, blob, body, seal
from .facet_manifest import validate as validate_manifest, rendering_size_floor
from .facet_graph import manifest_objects, closure, desired_semantics, allowed_slots, expected_template
from .facet_inventory import COMMANDS, CONTRACTS
from .facet_observation import observe
from .planning import require, INVALID, PACK_INVALID, INCOMPATIBLE

PREFIX = {'archetype': 'item_archetype', 'schema': 'facet_schema', 'rendering': 'notification_rendering_definition',
          'profile': 'notification_profile', 'facet_binding': 'item_archetype.facet_binding', 'binding': 'notification_profile.binding'}
PHASE = {k: n for n, k in enumerate(('archetype', 'schema', 'facet_binding', 'rendering', 'profile', 'binding'))}


def dependencies(key, desired):
    family = key.split(':')[0]
    if family == 'facet_binding': return ['archetype:' + desired['archetype_key'], 'schema:' + desired['schema_ref']['schema_key']]
    if family == 'binding': return ['archetype:' + desired['archetype_key'], 'profile:' + desired['notification_profile_key']]
    if family == 'rendering': return ['schema:' + s['schema_ref']['schema_key'] for s in desired['revision']['selections']]
    if family == 'profile':
        return ['rendering:' + t['rendering']['definition_ref']['definition_key']
                for t in desired['revision']['templates'] if t['rendering']['kind'] == 'definition']
    return []


def build_plan(manifest, request, environment, observation):
    objects = manifest_objects(manifest)
    selected = closure(manifest, request['request']['selection'])
    existing = {r['object_key']: r for r in observation['entries']}
    resolutions, classifications, actions = {}, {}, []
    owner = request['request']['owner']

    def action(key, command, desired, old):
        index = str(len(actions))
        row = dict(ordinal=index, action_id='pending-' + index, command=command, object_key=key,
                   change_kind='create' if old is None else 'update', desired=blob(desired), expected=old)
        row['request_template'] = blob(expected_template(row, owner))
        row['slots'] = [dict(request_pointer=p, object_key=k, field=f) for p, (k, f) in sorted(allowed_slots(row, desired).items())]
        require('${' not in row['request_template']['canonical_json'], 'interpolation_forbidden', INVALID)
        actions.append(row)
        for field, pointer in COMMANDS[command]['outputs'].items():
            resolutions[key][field] = dict(kind='action_result', action_id=row['action_id'], output_pointer=pointer)

    for key in sorted(selected, key=lambda k: (PHASE[k.split(':')[0]], k)):
        desired, old = objects[key], existing.get(key)
        family = key.split(':')[0]; binding = family in ('binding', 'facet_binding')
        blocked = (old is not None and old['status'] == 'retired') or any(
            classifications[d]['classification'] == 'blocked' for d in dependencies(key, desired))
        resolution = dict(object_key=key, root=None, revision=None, binding=None)
        resolutions[key] = resolution
        if not blocked:
            if old:
                for field in ('root', 'revision', 'binding'):
                    if old[field + '_id'] is not None:
                        resolution[field] = dict(kind='observed', object_key=key, field=field, value=old[field + '_id'])
            if binding:
                resolution['root'] = deepcopy(resolutions['archetype:' + desired['archetype_key']]['root'])
            if family == 'rendering':
                known = {k.removeprefix('schema:'): r['revision']['value']
                         for k, r in resolutions.items() if k.startswith('schema:')
                         and r['revision'] and r['revision']['kind'] == 'observed'}
                require(rendering_size_floor(desired['revision'], known) <= 8192,
                        'rendering_definition_too_large', PACK_INVALID)
            semantic = desired_semantics(key, desired, resolutions)
            observed = body(old['value']) if old else None
            if family == 'profile' and old and old['revision_contract'].endswith('.v1'):
                for template in observed['revision']['templates']: template['rendering'] = {'kind': 'ordinary'}
            classification = 'missing' if old is None else 'equivalent' if semantic == observed else 'drifted'
        else:
            classification = 'blocked'
        classifications[key] = dict(object_key=key, classification=classification, desired=blob(desired), observed=old,
                                   blocked_reason='retired_definition_or_dependency' if blocked else None)
        if classification in ('blocked', 'equivalent'): continue
        prefix = PREFIX[family]
        if classification == 'missing':
            action(key, prefix + ('.set' if binding else '.create'), desired, old)
        elif family == 'profile':
            if semantic['metadata'] != observed['metadata']: action(key, prefix + '.metadata.update', desired, old)
            if semantic['revision'] != observed['revision']: action(key, prefix + '.revise', desired, old)
        else:
            action(key, prefix + ('.set' if binding else '.revise' if family == 'archetype' else '.publish'), desired, old)
    actions.sort(key=lambda row: (COMMANDS[row['command']]['phase'], row['object_key']))
    identities = {row['action_id']: f'action-{i:06d}' for i, row in enumerate(actions)}
    for i, row in enumerate(actions):
        row.update(ordinal=str(i), action_id=f'action-{i:06d}')
    for row in resolutions.values():
        for field in ('root', 'revision', 'binding'):
            source = row[field]
            if source and source['kind'] == 'action_result': source['action_id'] = identities[source['action_id']]
    blocked = sorted(k for k, c in classifications.items() if c['classification'] == 'blocked')
    plan = seal(dict(artifact_schema='spine.pack-install-plan.v2', request_digest=request['content_identity']['digest'],
        request=deepcopy(request['request']), pack=dict(manifest_schema=manifest['manifest_schema'], **manifest['pack'],
            manifest_digest=manifest['content_identity']['digest']), closure=selected, environment=environment,
        required_execution_contracts=CONTRACTS, observation=observation,
        classifications=[classifications[k] for k in selected], resolutions=[resolutions[k] for k in selected],
        actions=actions, decision_action_ids=[r['action_id'] for r in actions if r['change_kind'] == 'update'],
        blocked_object_keys=blocked, apply_eligible=manifest['pack']['status'] == 'released' and not blocked))
    artifact(plan, 'install-plan')
    return plan


def validate_inputs(manifest, request):
    validate_manifest(manifest)
    require(manifest['compatibility']['spine_runtime_versions'] == ['0.10.0'], 'successor_requires_exact_0100', INCOMPATIBLE)
    artifact(request, 'install-request')
    # Request-body semantics and target normalization are unchanged from v1.
    original = a.seal(dict(artifact_schema='spine.pack-install-request.v1', request=request['request']))
    require(not a.request_errors(original), 'invalid_request', INVALID)
    selection = request['request']['selection']
    if selection['mode'] == 'archetypes':
        require(set(selection['archetype_keys']) <= {x['archetype_key'] for x in manifest['archetypes']}, 'unknown_selection', INVALID)
    require(manifest['pack']['status'] != 'draft' or request['request']['draft_posture'] == 'inspect_only',
            'draft_inspection_not_allowed', PACK_INVALID)


def plan_installation(manifest, request, transport, *, page_size=100):
    validate_inputs(manifest, request)
    selected = closure(manifest, request['request']['selection'])
    environment, view = observe(transport, request['request']['owner'], selected, page_size=page_size,
                                content_contracts=manifest['compatibility']['spine_content_contracts'])
    require(set(manifest['compatibility']['spine_content_contracts']) <= set(environment['advertised_contracts']),
            'missing_content_contracts', INCOMPATIBLE)
    return build_plan(manifest, request, environment, view)
```
