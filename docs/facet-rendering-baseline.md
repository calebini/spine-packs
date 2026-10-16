# Facet/rendering baseline inspection

Inspection date: 2026-10-10. Design authority is
`specs/facet-rendering-packs.md`; this file records evidence, not an alternative
Spine contract. The original inspection and the later narrow qualification below
are distinct; neither is complete installer qualification.

## Current FR-2 baseline: 0.10.0 (2026-10-16)

The operator explicitly adopted commit
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`, schema `19`.
The new public `facet_schema.revision.show` closes the historical revision-to-root
gap documented in `fr2-historical-facet-readback-gap.md`. Its required contracts
are canonical JSON v1, facet-schema-revision-readback v1, facet-schemas v1 and
notification-rendering-integration v1. No HTTP route, migration, receipts or
mutating authority is added by this read.

The separate `contracts/installer-spine-0.10.0-inventory.json` records 23 commands,
12 reads, 11 proposed writes and an 18-contract union. It pins the upstream
registry, request/response/failure closure, packaged registry/schema pins and
fixture authority. The old unchanged schema closure is referenced offline by
the new closure. FR-2 runtime accepts only this exact runtime/schema; installed
Git provenance must be established independently of `system.info`.

See `fr2-qualification.md` for the actual read-only planner gate, including
cross-root historical lookup, installed-package provenance and limitations.
The earlier listing-only gate below remains historical and is not relabelled
as 0.10.0 qualification. The upstream 1,041 tests are not installer test results.

## Historical 0.9.1 repaired baseline and independent listing gate

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
