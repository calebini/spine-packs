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
