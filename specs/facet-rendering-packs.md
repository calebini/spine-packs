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
