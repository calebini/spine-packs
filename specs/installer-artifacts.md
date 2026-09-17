# Installer artifact contracts

Status: Draft v0.1; runtime through Slice 5, Slice 6 disposable qualification authorized

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

For the pinned Spine 0.3.0 baseline in `specs/installer.md` Section 3, continuation
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

The authorized planning, preflight, initial-apply, bounded continuation, and verification
slices use the source-tree `spine_packs` package and standard-library `argparse`,
as recorded in `specs/architecture.md`. This does not authorize broader recovery
implementation. Slice 6 packaging follows `specs/architecture.md` without changing
artifact contracts; publication remains separately gated. General filesystem
configuration remains deferred. It does not add section bundles,
remote transports, signatures, install registries, credentials, Windows path
semantics, or Spine runtime changes.
