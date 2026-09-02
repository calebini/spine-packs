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

Path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/kinflow-starter-medical-vslice-audit-001/audit-notes.md
Hash: b17cafe46c463344273bdff77002b8f09ff718bce26ec3feb97706e18ce7a717

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

## Specs To Check

### Spec 1: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/pack-format.md

Hash: efa26dd11195e3357ab32c27d6e250a1694ad95a13ec06c8eab8fea7b8ba2c12

```markdown
# Pack format requirements

## Status and identity

This document defines the first-pass pack contract,
`spine.pack-manifest.v1`. Its machine-readable authority is
`contracts/schemas/spine-pack-manifest.v1.schema.json`, identified by:

```text
https://spine-packs.local/contracts/schemas/spine-pack-manifest.v1.schema.json
```

Manifests MUST be UTF-8 JSON objects and MUST declare
`manifest_schema=spine.pack-manifest.v1`. YAML, TOML, split manifests, comments,
and alternate encodings are not supported by v1.

Every object is closed. Unknown fields, duplicate JSON object member names,
missing required fields, and invalid field types MUST fail validation. V1 has
no optional fields. `description` is required for archetypes and profiles but
is explicitly nullable; absent and `null` are not equivalent.

## Pack identity and version

`pack_id` MUST match `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` and contain at most 64
characters. It is owner-neutral and stable across versions.

Version 1 supports two lifecycle forms:

- a draft version matching semantic version core plus
  `-draft.<positive-decimal>`, paired with `status=draft`; or
- a stable semantic version with no prerelease or build suffix, paired with
  `status=released`.

Numeric components MUST NOT contain leading zeroes. `1.0.0-draft.1` is a draft
toward `1.0.0`; it is not the `1.0.0` release.

Draft content MAY change before release, but its content digest MUST be updated.
Once a manifest is published with `status=released`, the entire pack
identity/version/digest tuple and its content are immutable. Any later semantic,
compatibility, or metadata change requires a new stable pack version.

## Top-level shape

A v1 manifest contains exactly:

- `manifest_schema`;
- `pack`, containing `pack_id`, `version`, and `status`;
- `compatibility`;
- `dependencies`;
- `archetypes`;
- `notification_profiles`;
- `binding_intents`; and
- `content_identity`.

The first schema requires at least one archetype, one notification profile, and
one binding intent because it establishes the complete vertical-slice shape.

## Compatibility

`compatibility.spine_runtime_versions` and
`compatibility.spine_content_contracts` are required exact allowlists governed
by `specs/compatibility.md`. They MUST be unique and deterministically ordered.
The content-contract list describes definition semantics only and MUST NOT be
used as proof that every contract needed by a future installer command is
available.

## Dependencies

`dependencies` is required and MUST be an empty array in
`spine.pack-manifest.v1`. A future manifest-contract version must define pack
reference identity, version selection, integrity, cycle handling, and ordering
before dependencies may be added. An installer MUST fail closed rather than
ignore a non-empty dependency array.

## Archetypes

Each archetype contains exactly:

- `archetype_key`, matching Spine's public catalog-key grammar;
- `intended_status`, currently fixed to `active`; and
- `revision`, containing required `display_name`, required nullable
  `description`, and required `compatible_item_types`.

The revision shape is the owner-neutral semantic subset of Spine
`item_archetype.create`. Owner, command, actor, timestamp, generated ID,
revision ID, receipt, and normalized hash fields are forbidden.

Compatible item types are a sorted, unique, non-empty subset of `event` and
`task`. Archetype keys MUST be unique within the pack.

## Notification profiles and templates

Each profile contains exactly:

- `profile_key`, matching Spine's public catalog-key grammar;
- required `display_name` and required nullable `description`;
- `intended_status`, currently fixed to `active`; and
- `revision`, containing required `compatible_item_types` and `templates`.

V1 templates contain exactly `template_key`, `schedule`, and `late_handling`.
The v1 schedule subset is intentionally narrow:

```json
{
  "kind": "once",
  "at": {
    "kind": "target_offset",
    "offset_basis": "elapsed",
    "offset_seconds": "-86400"
  }
}
```

`offset_seconds` MUST be a negative, non-zero decimal string. It represents
elapsed seconds before the target anchor. Calendar-day and fixed-local-time
interpretations are forbidden.

V1 late handling is:

```json
{
  "kind": "deliver_within",
  "grace_seconds": "21600"
}
```

`grace_seconds` MUST be a positive decimal string. The pack restriction is
stricter than Spine's general non-negative decimal type because a zero-width
`deliver_within` window has no useful meaning in curated pack content.

Profile keys MUST be unique within the pack. Template keys MUST be unique
within each profile. Compatible item types and templates MUST be sorted.
Recipients, subjects, groups, routes, channels, delivery targets, destinations,
credentials, target anchors, recurrence scope, generated hashes, and any
environment fact are forbidden.

## Binding intents and local references

A binding intent contains exactly:

- `binding_kind=archetype_default`;
- `archetype_key`; and
- `notification_profile_key`.

Both keys are pack-local references. The archetype and profile MUST exist in the
same manifest, and their compatible item-type sets MUST intersect. Binding pairs
MUST be unique, and each `archetype_key` MUST appear in at most one binding
intent. Two profiles therefore cannot both claim to be the default for the same
archetype. V1 does not permit dependency-qualified references.

The intent says that the named profile should become the default for the named
archetype under an owner chosen at installation time. It is not a Spine binding
and contains no owner or Spine-generated ID. A future installer must resolve or
create both definitions through public commands, then submit the resolved IDs
and explicit owner to `notification_profile.binding.set`.

## Deterministic ordering

Array order is contract-bearing and MUST be normalized before digesting:

1. runtime versions by semantic-version numeric order;
2. content contracts by bytewise lexicographic order;
3. compatible item types by bytewise lexicographic order;
4. archetypes by `archetype_key`;
5. profiles by `profile_key`;
6. templates by `template_key`; and
7. binding intents by `archetype_key`, which is unique within this collection.

`dependencies` is empty. Input that is valid in content but not in canonical
order MUST fail validation rather than be silently reordered.

## Content identity

`content_identity` contains exactly:

- `algorithm=sha256`;
- `canonical_json_version=spine.canonical-json.v1`; and
- a lowercase 64-character hexadecimal `digest`.

The digest preimage is the following object:

```text
{
  "canonical_json_version": "spine.canonical-json.v1",
  "derivation_version": "spine-pack-content-sha256.v1",
  "manifest": <the complete manifest with content_identity omitted>
}
```

The preimage is encoded exactly under Spine canonical JSON v1: valid UTF-8; no
insignificant whitespace; object keys sorted lexicographically by Unicode
codepoint; duplicate keys forbidden; array order preserved; strings preserved
without implicit normalization; invalid surrogate code points rejected; only
quote, backslash, and U+0000 through U+001F escaped; lowercase `\\u00xx` control
escapes; slash never escaped; and JSON numbers forbidden. The digest is SHA-256
over those bytes, encoded as lowercase hexadecimal.

The manifest uses decimal strings rather than JSON numbers, so every current
semantic value is legal in the canonical preimage. A digest mismatch fails
closed. Draft edits recompute the digest; released content must never change.

## Validation order and fail-closed behavior

Validation MUST proceed in this order:

1. reject malformed JSON and duplicate object members;
2. validate the closed JSON Schema;
3. validate unique definition keys, binding pairs, and one default binding per
   archetype key;
4. resolve binding references and compatible item-type intersections;
5. validate deterministic ordering; and
6. recompute and compare the content digest.

Any failure rejects the complete pack. Implementations MUST NOT drop unknown
fields, skip invalid definitions, guess references, coerce values, reorder input
silently, or install a valid subset.

The dependency-free repository test implements the closed JSON Schema subset
used by v1 plus the semantic, ordering, and digest stages above. Before any pack
version is released, development or CI MUST also meta-validate the schema and
run the complete fixture matrix with an independent standards-conforming JSON
Schema Draft 2020-12 implementation. That independent check is not available in
the current local environment and is a release blocker, not evidence against
the passing local contract suite.

## Deferred decisions

The following remain outside `spine.pack-manifest.v1`:

- dependency references and resolution;
- broader Spine notification schedule and late-handling variants;
- semantic-equivalence comparison against installed definitions;
- update-authorization and receipt-correlation forms;
- installer version compatibility;
- signing, publisher identity, registries, and release transport; and
- the `plan`, `apply`, and `verify` command contracts and implementation.
```

### Spec 2: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/specs/compatibility.md

Hash: 755aacb83316675fdf3de34083b5c0e79ecfa4d915a6d130f0c77ce5412b410e

```markdown
# Compatibility

## Compatibility dimensions

Every manifest MUST declare compatibility independently for:

1. exact Spine runtime versions; and
2. exact Spine content-contract identifiers needed to interpret the pack's
   definitions.

Runtime and contract compatibility are separate dimensions. Matching one MUST
NOT be treated as evidence that the other matches.

## Version 1 declaration shape

`spine.pack-manifest.v1` uses closed, non-empty allowlists:

- `spine_runtime_versions` contains stable semantic versions in ascending
  order; and
- `spine_content_contracts` contains contract identifiers in bytewise
  lexicographic order.

Ranges, wildcards, prerelease runtimes, development builds, and implicit
compatibility are not supported by v1. A future installer MUST obtain both
values through Spine's public `system.info` command and MUST require exact
membership before interpreting pack content.

The first `kinflow-starter` draft is based exclusively on the inspected Spine
runtime `0.3.0` public artifacts and requires:

- `spine.item-archetypes.v1`;
- `spine.notification-profile-bindings.v1`; and
- `spine.notification-profiles.v1`.

These declarations do not assert that any staging or production environment is
compatible. No environment was queried.

## Content compatibility is not execution readiness

`spine_content_contracts` is intentionally limited to the contracts that give
the owner-neutral definitions their meaning. It MUST NOT be interpreted as the
complete contract union required to execute `plan`, `apply`, or `verify`.

Spine's command registry may require additional contracts for a concrete
command, including `spine.canonical-json.v1`, notification-profile readback,
catalog cursor, response, or receipt contracts. A future installer contract
MUST name its command set, derive the complete per-command requirement union
from the supported Spine public surface, and verify that union independently.
The v1 pack manifest makes no execution-readiness claim.

## Fail-closed behavior

Compatibility evaluation MUST fail before content planning when:

- the runtime version cannot be obtained;
- implemented contract identifiers cannot be obtained;
- the runtime is absent from `spine_runtime_versions`;
- any declared content contract is absent from Spine's advertised contracts;
  or
- the manifest declaration is missing, unsorted, duplicated, or invalid.

Compatibility failure MUST NOT be bypassed implicitly during a future `apply`.
Any override mechanism requires a later contract revision.

## Version changes

A released pack's compatibility declaration is part of its immutable content.
Expanding or narrowing compatibility after release requires a new pack version.
Draft compatibility MAY change only with a recomputed content digest and review
against the newly named public artifacts.

## Deferred compatibility decisions

The following remain intentionally unresolved:

- version-range syntax;
- prerelease and development runtime policy;
- minimum installer-version declarations;
- evidence required to widen compatibility; and
- compatibility declarations for dependency packs; and
- the full execution-contract union for a future installer.
```

### Spec 3: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/schemas/spine-pack-manifest.v1.schema.json

Hash: 67e6ba43cc3a7f840d29643318cb88d0362c746ee19b3933e28a27203bae350a

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spine-packs.local/contracts/schemas/spine-pack-manifest.v1.schema.json",
  "title": "Spine Pack Manifest v1",
  "type": "object",
  "required": [
    "manifest_schema",
    "pack",
    "compatibility",
    "dependencies",
    "archetypes",
    "notification_profiles",
    "binding_intents",
    "content_identity"
  ],
  "properties": {
    "manifest_schema": { "const": "spine.pack-manifest.v1" },
    "pack": { "$ref": "#/$defs/pack" },
    "compatibility": { "$ref": "#/$defs/compatibility" },
    "dependencies": {
      "type": "array",
      "maxItems": 0
    },
    "archetypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/archetype" }
    },
    "notification_profiles": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/notificationProfile" }
    },
    "binding_intents": {
      "type": "array",
      "minItems": 1,
      "maxItems": 256,
      "items": { "$ref": "#/$defs/bindingIntent" }
    },
    "content_identity": { "$ref": "#/$defs/contentIdentity" }
  },
  "additionalProperties": false,
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$"
    },
    "packId": {
      "type": "string",
      "maxLength": 64,
      "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
    },
    "stableVersion": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)$"
    },
    "draftVersion": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)-draft\\.[1-9][0-9]*$"
    },
    "pack": {
      "oneOf": [
        {
          "type": "object",
          "required": ["pack_id", "version", "status"],
          "properties": {
            "pack_id": { "$ref": "#/$defs/packId" },
            "version": { "$ref": "#/$defs/draftVersion" },
            "status": { "const": "draft" }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": ["pack_id", "version", "status"],
          "properties": {
            "pack_id": { "$ref": "#/$defs/packId" },
            "version": { "$ref": "#/$defs/stableVersion" },
            "status": { "const": "released" }
          },
          "additionalProperties": false
        }
      ]
    },
    "compatibility": {
      "type": "object",
      "required": ["spine_runtime_versions", "spine_content_contracts"],
      "properties": {
        "spine_runtime_versions": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": { "$ref": "#/$defs/stableVersion" }
        },
        "spine_content_contracts": {
          "type": "array",
          "minItems": 3,
          "maxItems": 3,
          "uniqueItems": true,
          "items": {
            "enum": [
              "spine.item-archetypes.v1",
              "spine.notification-profile-bindings.v1",
              "spine.notification-profiles.v1"
            ]
          }
        }
      },
      "additionalProperties": false
    },
    "itemTypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 2,
      "uniqueItems": true,
      "items": { "enum": ["event", "task"] }
    },
    "description": {
      "oneOf": [
        { "type": "string", "minLength": 1, "maxLength": 2000 },
        { "type": "null" }
      ]
    },
    "archetypeRevision": {
      "type": "object",
      "required": ["display_name", "description", "compatible_item_types"],
      "properties": {
        "display_name": { "type": "string", "minLength": 1, "maxLength": 160 },
        "description": { "$ref": "#/$defs/description" },
        "compatible_item_types": { "$ref": "#/$defs/itemTypes" }
      },
      "additionalProperties": false
    },
    "archetype": {
      "type": "object",
      "required": ["archetype_key", "intended_status", "revision"],
      "properties": {
        "archetype_key": { "$ref": "#/$defs/key" },
        "intended_status": { "const": "active" },
        "revision": { "$ref": "#/$defs/archetypeRevision" }
      },
      "additionalProperties": false
    },
    "elapsedBeforeSchedule": {
      "type": "object",
      "required": ["kind", "at"],
      "properties": {
        "kind": { "const": "once" },
        "at": {
          "type": "object",
          "required": ["kind", "offset_basis", "offset_seconds"],
          "properties": {
            "kind": { "const": "target_offset" },
            "offset_basis": { "const": "elapsed" },
            "offset_seconds": {
              "type": "string",
              "pattern": "^-[1-9][0-9]*$"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "lateHandling": {
      "type": "object",
      "required": ["kind", "grace_seconds"],
      "properties": {
        "kind": { "const": "deliver_within" },
        "grace_seconds": {
          "type": "string",
          "pattern": "^[1-9][0-9]*$"
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": ["template_key", "schedule", "late_handling"],
      "properties": {
        "template_key": { "$ref": "#/$defs/key" },
        "schedule": { "$ref": "#/$defs/elapsedBeforeSchedule" },
        "late_handling": { "$ref": "#/$defs/lateHandling" }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": ["compatible_item_types", "templates"],
      "properties": {
        "compatible_item_types": { "$ref": "#/$defs/itemTypes" },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": { "$ref": "#/$defs/template" }
        }
      },
      "additionalProperties": false
    },
    "notificationProfile": {
      "type": "object",
      "required": [
        "profile_key",
        "display_name",
        "description",
        "intended_status",
        "revision"
      ],
      "properties": {
        "profile_key": { "$ref": "#/$defs/key" },
        "display_name": { "type": "string", "minLength": 1, "maxLength": 160 },
        "description": { "$ref": "#/$defs/description" },
        "intended_status": { "const": "active" },
        "revision": { "$ref": "#/$defs/profileRevision" }
      },
      "additionalProperties": false
    },
    "bindingIntent": {
      "type": "object",
      "required": ["binding_kind", "archetype_key", "notification_profile_key"],
      "properties": {
        "binding_kind": { "const": "archetype_default" },
        "archetype_key": { "$ref": "#/$defs/key" },
        "notification_profile_key": { "$ref": "#/$defs/key" }
      },
      "additionalProperties": false
    },
    "contentIdentity": {
      "type": "object",
      "required": ["algorithm", "canonical_json_version", "digest"],
      "properties": {
        "algorithm": { "const": "sha256" },
        "canonical_json_version": { "const": "spine.canonical-json.v1" },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      },
      "additionalProperties": false
    }
  }
}
```

### Spec 4: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json

Hash: c0baa85773b72d69e5e0a27ef0ddf4d3faa1eabb705fb368768ec630ab2bc21f

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": ["0.3.0"],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": ["event"]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": ["event"],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "db2f29d75be93c7e2f5dd68b28be00a981368b1bdab27ccde77ed2528b8b668d"
  }
}
```

### Spec 5: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/contracts/pack-fixture-manifest.v1.json

Hash: 7f520570969f34584fb382fdba7deec6b2bdbbdd8ed2c9869d69fc2abb3bac09

```markdown
{
  "schema_version": "spine.pack-contract-fixtures.v1",
  "schema": "contracts/schemas/spine-pack-manifest.v1.schema.json",
  "cases": [
    {
      "case_id": "published_draft_manifest",
      "fixture": "packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json",
      "valid": true
    },
    {
      "case_id": "positive_medical_vertical_slice",
      "fixture": "tests/fixtures/pack-manifest/positive/medical_vertical_slice.json",
      "valid": true
    },
    {
      "case_id": "negative_embedded_owner_data",
      "fixture": "tests/fixtures/pack-manifest/negative/embedded_owner_data.json",
      "valid": false,
      "expected_error": "$.owner: unknown field"
    },
    {
      "case_id": "negative_unresolved_binding_reference",
      "fixture": "tests/fixtures/pack-manifest/negative/unresolved_binding_reference.json",
      "valid": false,
      "expected_error": "unresolved notification_profile_key"
    },
    {
      "case_id": "negative_duplicate_keys",
      "fixture": "tests/fixtures/pack-manifest/negative/duplicate_keys.json",
      "valid": false,
      "expected_error": "duplicate archetype_key"
    },
    {
      "case_id": "negative_multiple_defaults_for_archetype",
      "fixture": "tests/fixtures/pack-manifest/negative/multiple_defaults_for_archetype.json",
      "valid": false,
      "expected_error": "duplicate archetype_default for archetype_key"
    },
    {
      "case_id": "negative_notification_offset",
      "fixture": "tests/fixtures/pack-manifest/negative/invalid_notification_offset.json",
      "valid": false,
      "expected_error": "offset_seconds: pattern mismatch"
    },
    {
      "case_id": "negative_grace_window",
      "fixture": "tests/fixtures/pack-manifest/negative/invalid_grace_window.json",
      "valid": false,
      "expected_error": "grace_seconds: pattern mismatch"
    },
    {
      "case_id": "negative_incompatible_item_types",
      "fixture": "tests/fixtures/pack-manifest/negative/incompatible_item_types.json",
      "valid": false,
      "expected_error": "no compatible item type"
    },
    {
      "case_id": "negative_unknown_fields",
      "fixture": "tests/fixtures/pack-manifest/negative/unknown_fields.json",
      "valid": false,
      "expected_error": "unexpected_field: unknown field"
    },
    {
      "case_id": "negative_noncanonical_array_ordering",
      "fixture": "tests/fixtures/pack-manifest/negative/noncanonical_array_ordering.json",
      "valid": false,
      "expected_error": "$.compatibility.spine_content_contracts: values are not in deterministic order"
    },
    {
      "case_id": "negative_incorrect_content_digest",
      "fixture": "tests/fixtures/pack-manifest/negative/incorrect_content_digest.json",
      "valid": false,
      "expected_error": "$.content_identity.digest: expected"
    },
    {
      "case_id": "negative_version_status_mismatch",
      "fixture": "tests/fixtures/pack-manifest/negative/version_status_mismatch.json",
      "valid": false,
      "expected_error": "$.pack: must match exactly one allowed shape"
    }
  ]
}
```

### Spec 6: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/positive/medical_vertical_slice.json

Hash: c0baa85773b72d69e5e0a27ef0ddf4d3faa1eabb705fb368768ec630ab2bc21f

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": ["0.3.0"],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": ["event"]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": ["event"],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "db2f29d75be93c7e2f5dd68b28be00a981368b1bdab27ccde77ed2528b8b668d"
  }
}
```

### Spec 7: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/embedded_owner_data.json

Hash: 8e7ababa9aa18c93c532219af357a6bb2bee64757ea454e0206e76dd181f9a60

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  },
  "owner": {
    "owner_kind": "subject",
    "owner_subject_id": "subject_forbidden"
  }
}
```

### Spec 8: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/unresolved_binding_reference.json

Hash: 3027869314116318c9c59072e137333aec8a59b24c8adb2c2456a3da2815da10

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "missing_profile"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 9: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/duplicate_keys.json

Hash: 794d0fa652e4fccb9ae30efb998a50e0f771ea9f904f8c1eb0f4e3407c963774

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    },
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 10: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/multiple_defaults_for_archetype.json

Hash: d9b1b9f7d966ed215b67d272810387189f5c7f45558ed85ab5e889a770907e8f

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_alternate",
      "display_name": "Medical appointment alternate",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    },
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_alternate"
    },
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 11: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/invalid_notification_offset.json

Hash: 2b81c31e7405e87e77dbb6d8ce0054ad7a49bc0f7c07f36c4c2bf586c52d31f5

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
          {
            "template_key": "seven_days_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "604800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "86400"
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 12: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/invalid_grace_window.json

Hash: 5c8e1c6ea843ce34c3279b0db57f5995e2b63b5594ec435b692316bc34cfcd60

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
              "grace_seconds": "0"
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 13: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/incompatible_item_types.json

Hash: 8bc7b1da07a93b35bf1b94381d8d87df12d7eb1d599ef2109c72d1df2e5bbf5d

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "task"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 14: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/unknown_fields.json

Hash: 0f230182a1aa6b8d3e5301858cd85ef12791cf75dbb5ab3fa691b70eeae66345

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      },
      "unexpected_field": "forbidden"
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 15: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/noncanonical_array_ordering.json

Hash: 45f8ecfe905257d35f402cf4e0d712aa35bf966883d10deec70b31f2a693313d

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.notification-profiles.v1",
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 16: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/incorrect_content_digest.json

Hash: aae723a33c49d2e6d09aa51df4495baa04322f2b335339bf3faed35ab6af2b1b

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0-draft.1",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 17: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/fixtures/pack-manifest/negative/version_status_mismatch.json

Hash: 53043c7aeff2838398f5bf032eeec9e2c87a6e6a153e9a8d52fec2d06df8fda3

```markdown
{
  "manifest_schema": "spine.pack-manifest.v1",
  "pack": {
    "pack_id": "kinflow-starter",
    "version": "1.0.0",
    "status": "draft"
  },
  "compatibility": {
    "spine_runtime_versions": [
      "0.3.0"
    ],
    "spine_content_contracts": [
      "spine.item-archetypes.v1",
      "spine.notification-profile-bindings.v1",
      "spine.notification-profiles.v1"
    ]
  },
  "dependencies": [],
  "archetypes": [
    {
      "archetype_key": "medical_appointment",
      "intended_status": "active",
      "revision": {
        "display_name": "Medical appointment",
        "description": "Medical, dental, vision, therapy, diagnostic, and other scheduled healthcare appointments.",
        "compatible_item_types": [
          "event"
        ]
      }
    }
  ],
  "notification_profiles": [
    {
      "profile_key": "medical_appointment_standard",
      "display_name": "Medical appointment standard",
      "description": null,
      "intended_status": "active",
      "revision": {
        "compatible_item_types": [
          "event"
        ],
        "templates": [
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
            }
          },
          {
            "template_key": "thirty_minutes_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-1800"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "900"
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
            }
          },
          {
            "template_key": "two_hours_before",
            "schedule": {
              "kind": "once",
              "at": {
                "kind": "target_offset",
                "offset_basis": "elapsed",
                "offset_seconds": "-7200"
              }
            },
            "late_handling": {
              "kind": "deliver_within",
              "grace_seconds": "3600"
            }
          }
        ]
      }
    }
  ],
  "binding_intents": [
    {
      "binding_kind": "archetype_default",
      "archetype_key": "medical_appointment",
      "notification_profile_key": "medical_appointment_standard"
    }
  ],
  "content_identity": {
    "algorithm": "sha256",
    "canonical_json_version": "spine.canonical-json.v1",
    "digest": "0000000000000000000000000000000000000000000000000000000000000000"
  }
}
```

### Spec 18: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/tests/contract/test_pack_manifest_contract.py

Hash: 69f501f536b706cf9bc9a15890b5d25d8ba860fac9ff84fdfc271d218b0a9a26

```markdown
#!/usr/bin/env python3
"""Dependency-free contract checks for Spine pack manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "contracts/schemas/spine-pack-manifest.v1.schema.json"
FIXTURE_MANIFEST_PATH = ROOT / "contracts/pack-fixture-manifest.v1.json"
DRAFT_MANIFEST_PATH = (
    ROOT / "packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json"
)
POSITIVE_FIXTURE_PATH = (
    ROOT / "tests/fixtures/pack-manifest/positive/medical_vertical_slice.json"
)


class DuplicateObjectMember(ValueError):
    """Raised when a JSON object repeats a member name."""


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, member in pairs:
        if key in value:
            raise DuplicateObjectMember(f"duplicate JSON object member: {key}")
        value[key] = member
    return value


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_closed_object)


def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[token]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return current


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "null": value is None,
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, False)


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate the deliberately small Draft 2020-12 subset used by the schema."""

    if "$ref" in schema:
        return schema_errors(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path)

    if "oneOf" in schema:
        branch_errors = [
            schema_errors(value, branch, root_schema, path)
            for branch in schema["oneOf"]
        ]
        matches = sum(not errors for errors in branch_errors)
        if matches != 1:
            return [f"{path}: must match exactly one allowed shape"]
        return []

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in the allowed set")

    expected_type = schema.get("type")
    if expected_type is not None and not _is_type(value, expected_type):
        return [f"{path}: expected {expected_type}"]

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: string is too long")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern mismatch")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}.{required}: required field is missing")
        for key, member in value.items():
            member_path = f"{path}.{key}"
            if key in properties:
                errors.extend(schema_errors(member, properties[key], root_schema, member_path))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{member_path}: unknown field")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array has too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: array has too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, item_schema, root_schema, f"{path}[{index}]"))

    return errors


def _duplicate_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def check(values: list[str], label: str, path: str) -> None:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                errors.append(f"{path}: duplicate {label} {value!r}")
            seen.add(value)

    check(
        [entry["archetype_key"] for entry in manifest["archetypes"]],
        "archetype_key",
        "$.archetypes",
    )
    check(
        [entry["profile_key"] for entry in manifest["notification_profiles"]],
        "profile_key",
        "$.notification_profiles",
    )
    for index, profile in enumerate(manifest["notification_profiles"]):
        check(
            [entry["template_key"] for entry in profile["revision"]["templates"]],
            "template_key",
            f"$.notification_profiles[{index}].revision.templates",
        )
    check(
        [entry["archetype_key"] for entry in manifest["binding_intents"]],
        "archetype_default for archetype_key",
        "$.binding_intents",
    )
    return errors


def _reference_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    archetypes = {entry["archetype_key"]: entry for entry in manifest["archetypes"]}
    profiles = {
        entry["profile_key"]: entry for entry in manifest["notification_profiles"]
    }
    for index, binding in enumerate(manifest["binding_intents"]):
        archetype_key = binding["archetype_key"]
        profile_key = binding["notification_profile_key"]
        archetype = archetypes.get(archetype_key)
        profile = profiles.get(profile_key)
        if archetype is None:
            errors.append(
                f"$.binding_intents[{index}]: unresolved archetype_key {archetype_key!r}"
            )
        if profile is None:
            errors.append(
                "$.binding_intents[{}]: unresolved notification_profile_key {!r}".format(
                    index, profile_key
                )
            )
        if archetype is not None and profile is not None:
            archetype_types = set(archetype["revision"]["compatible_item_types"])
            profile_types = set(profile["revision"]["compatible_item_types"])
            if not archetype_types.intersection(profile_types):
                errors.append(
                    f"$.binding_intents[{index}]: binding has no compatible item type"
                )
    return errors


def _ordering_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def ordered(values: list[Any], expected: list[Any], path: str) -> None:
        if values != expected:
            errors.append(f"{path}: values are not in deterministic order")

    runtime_versions = manifest["compatibility"]["spine_runtime_versions"]
    ordered(
        runtime_versions,
        sorted(runtime_versions, key=lambda value: tuple(int(part) for part in value.split("."))),
        "$.compatibility.spine_runtime_versions",
    )
    contracts = manifest["compatibility"]["spine_content_contracts"]
    ordered(contracts, sorted(contracts), "$.compatibility.spine_content_contracts")

    archetypes = manifest["archetypes"]
    ordered(
        [entry["archetype_key"] for entry in archetypes],
        sorted(entry["archetype_key"] for entry in archetypes),
        "$.archetypes",
    )
    for index, archetype in enumerate(archetypes):
        item_types = archetype["revision"]["compatible_item_types"]
        ordered(item_types, sorted(item_types), f"$.archetypes[{index}].revision.compatible_item_types")

    profiles = manifest["notification_profiles"]
    ordered(
        [entry["profile_key"] for entry in profiles],
        sorted(entry["profile_key"] for entry in profiles),
        "$.notification_profiles",
    )
    for index, profile in enumerate(profiles):
        item_types = profile["revision"]["compatible_item_types"]
        ordered(
            item_types,
            sorted(item_types),
            f"$.notification_profiles[{index}].revision.compatible_item_types",
        )
        template_keys = [
            entry["template_key"] for entry in profile["revision"]["templates"]
        ]
        ordered(
            template_keys,
            sorted(template_keys),
            f"$.notification_profiles[{index}].revision.templates",
        )

    binding_keys = [entry["archetype_key"] for entry in manifest["binding_intents"]]
    ordered(binding_keys, sorted(binding_keys), "$.binding_intents")
    return errors


def canonical_json(value: Any) -> str:
    """Encode the no-number subset of spine.canonical-json.v1."""

    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        pieces = ['"']
        for character in value:
            codepoint = ord(character)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("invalid surrogate code point in canonical JSON")
            if character == '"':
                pieces.append('\\"')
            elif character == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(character)
        pieces.append('"')
        return "".join(pieces)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("canonical JSON object keys must be strings")
        return "{" + ",".join(
            canonical_json(key) + ":" + canonical_json(value[key])
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"JSON numbers and unsupported values are forbidden: {value!r}")


def content_digest(manifest: dict[str, Any]) -> str:
    semantic_manifest = {
        key: value for key, value in manifest.items() if key != "content_identity"
    }
    preimage = {
        "canonical_json_version": "spine.canonical-json.v1",
        "derivation_version": "spine-pack-content-sha256.v1",
        "manifest": semantic_manifest,
    }
    encoded = canonical_json(preimage).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_pack(manifest: Any, schema: dict[str, Any]) -> list[str]:
    errors = schema_errors(manifest, schema, schema)
    if errors:
        return errors
    assert isinstance(manifest, dict)

    errors = _duplicate_errors(manifest)
    if errors:
        return errors
    errors = _reference_errors(manifest)
    if errors:
        return errors
    errors = _ordering_errors(manifest)
    if errors:
        return errors

    actual = manifest["content_identity"]["digest"]
    expected = content_digest(manifest)
    if actual != expected:
        return [f"$.content_identity.digest: expected {expected}, got {actual}"]
    return []


class PackManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.fixture_manifest = load_json(FIXTURE_MANIFEST_PATH)

    def test_schema_identity_and_dialect(self) -> None:
        self.assertEqual(
            self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(
            self.schema["$id"],
            "https://spine-packs.local/contracts/schemas/"
            "spine-pack-manifest.v1.schema.json",
        )

    def test_every_fixture_has_expected_schema_result(self) -> None:
        for case in self.fixture_manifest["cases"]:
            with self.subTest(case=case["case_id"]):
                fixture = load_json(ROOT / case["fixture"])
                errors = validate_pack(fixture, self.schema)
                if case["valid"]:
                    self.assertEqual(errors, [])
                else:
                    self.assertTrue(errors, "negative fixture unexpectedly validated")
                    self.assertIn(case["expected_error"], "\n".join(errors))

    def test_fixture_manifest_covers_every_test_fixture(self) -> None:
        fixture_root = ROOT / "tests/fixtures/pack-manifest"
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in fixture_root.rglob("*.json")
        }
        declared = {
            case["fixture"]
            for case in self.fixture_manifest["cases"]
            if case["fixture"].startswith("tests/fixtures/pack-manifest/")
        }
        self.assertEqual(actual, declared)

    def test_published_manifest_matches_positive_vector(self) -> None:
        self.assertEqual(load_json(DRAFT_MANIFEST_PATH), load_json(POSITIVE_FIXTURE_PATH))

    def test_published_manifest_contains_no_installation_identity(self) -> None:
        manifest = load_json(DRAFT_MANIFEST_PATH)
        forbidden = {
            "actor_subject_id",
            "command_id",
            "delivery_target_id",
            "destination",
            "owner",
            "owner_group_id",
            "owner_subject_id",
            "receipt_id",
            "route",
            "subject_id",
            "timestamp",
        }

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for member in value.values():
                    visit(member)
            elif isinstance(value, list):
                for member in value:
                    visit(member)

        visit(manifest)


if __name__ == "__main__":
    unittest.main()
```
