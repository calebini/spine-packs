# Facet/rendering baseline inspection

Inspection date: 2026-10-10. Design authority is
`specs/facet-rendering-packs.md`; this file records evidence, not an alternative
Spine contract or an implementation/qualification claim.

## Provenance and limits

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

## Source-level qualification blocker: profile v2 listing

At the exact requested pin:

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

Next gate: separately authorize a minimal public-CLI regression on this exact
pin: create a synthetic v2 ordinary profile, show it with v2, then list its owner
with v2, including mixed v1/v2 and paginated cases. Do not deploy, bypass listing,
read the database, import handlers as an installer shortcut, or claim successful
qualification before that gate. If confirmed, route the defect to Spine's owner;
any repaired baseline must be explicitly approved and separately pinned here.
Do not substitute a newer 0.9.0 build under the original qualification record.

## Unproved until later slices

No successor schema, fixture, installer code or curated pack was implemented.
No exact-baseline disposable ledger, wheel rebuild, recovery fault injection or
consumer authoring workflow was exercised. Planned aggregate observation budgets
and family-specific evidence schemas still need machine-contract review.
Current regression tests can establish preservation of old behavior, not that
the proposed new workflow works. The bounded audit is staged separately and
cannot be called passed or converged before an approved reviewer run.
