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
