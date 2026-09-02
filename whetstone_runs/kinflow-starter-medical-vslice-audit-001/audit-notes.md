# Change Intent

Establish `spine.pack-manifest.v1` through one complete, owner-neutral medical
appointment vertical slice. Confirm that the normative pack-format and
compatibility specifications, JSON Schema, draft manifest, fixtures, and
dependency-free contract tests describe one coherent bounded contract.

# Expected Boundary

- Spine remains the sole authority for installed archetypes, notification
  profiles, bindings, receipts, generated IDs, and ownership.
- The pack contains declarative donor content only and does not assert staging
  or installation state.
- The manifest contains no owner, subject, group, route, delivery target,
  destination, credential, command identity, receipt identity, timestamp, or
  environment-specific data.
- A future installer may map owner-neutral definitions only through Spine's
  existing public commands; no installer is implemented here.
- Draft `1.0.0-draft.1` is not released `1.0.0`.
- V1 is intentionally limited to empty dependencies, once-only negative
  elapsed target offsets, and positive `deliver_within` grace windows.
- Unknown fields, invalid values, duplicate keys, multiple defaults for one
  archetype, unresolved local references, incompatible binding types,
  non-canonical ordering, digest mismatch, and invalid version/status pairings
  fail closed.
- `spine_content_contracts` describes pack definition semantics only. It is not
  the complete contract union required by future installer commands.

# Files To Check

## Normative specifications

- `specs/pack-format.md`
- `specs/compatibility.md`

## Machine contract and draft content

- `contracts/schemas/spine-pack-manifest.v1.schema.json`
- `packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json`

## Fixture index and positive fixtures

- `contracts/pack-fixture-manifest.v1.json`
- `tests/fixtures/pack-manifest/positive/medical_vertical_slice.json`

## Negative fixtures

- `tests/fixtures/pack-manifest/negative/embedded_owner_data.json`
- `tests/fixtures/pack-manifest/negative/unresolved_binding_reference.json`
- `tests/fixtures/pack-manifest/negative/duplicate_keys.json`
- `tests/fixtures/pack-manifest/negative/multiple_defaults_for_archetype.json`
- `tests/fixtures/pack-manifest/negative/invalid_notification_offset.json`
- `tests/fixtures/pack-manifest/negative/invalid_grace_window.json`
- `tests/fixtures/pack-manifest/negative/incompatible_item_types.json`
- `tests/fixtures/pack-manifest/negative/unknown_fields.json`
- `tests/fixtures/pack-manifest/negative/noncanonical_array_ordering.json`
- `tests/fixtures/pack-manifest/negative/incorrect_content_digest.json`
- `tests/fixtures/pack-manifest/negative/version_status_mismatch.json`

## Contract tests

- `tests/contract/test_pack_manifest_contract.py`

# Reviewer Questions

1. Do prose and schema agree on identity, version/status pairing, nullable
   descriptions, closed objects, ordering, and digest derivation?
2. Does the manifest preserve the approved donor values and Spine-compatible
   elapsed-offset/late-handling shapes without importing installation identity?
3. Are binding references exclusively pack-local and checked for existence and
   compatible item-type intersection, with at most one default per archetype?
4. Do fixtures and tests prove every required negative boundary with the
   specified fail-closed validation order?
5. Does exact Spine `0.3.0` plus the three content-contract identifiers avoid any
   claim about unobserved staging, deployment state, or the complete execution
   contract union required by future installer commands?
6. Did the change accidentally introduce installer, runtime, database, ledger,
   scheduling, or release behavior outside the bounded contract?
7. Is the independent standards-conforming Draft 2020-12 validation requirement
   stated strongly enough as a release blocker without making the draft depend
   on unavailable local tooling?

# Out Of Scope

- Whetstone convergence, Phase 1, Phase 2, or Editor mutation
- source mutation or apply-back
- broad redesign or cosmetic cleanup
- staging inspection or database access
- implementation of `plan`, `apply`, or `verify`
- dependency resolution
- additional archetype definitions
- semantic comparison with already-installed Spine definitions

# Submission Status

Explicitly authorized by the operator on 2026-09-02 to send this notes file and
exactly the 18 files listed above to the nested Codex reviewer. Use the
`consistency` profile and do not mutate source files.
