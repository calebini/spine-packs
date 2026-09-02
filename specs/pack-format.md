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

Duplicate JSON object member names and duplicate definition keys are distinct
failure classes. A repeated member name in one JSON object is a lexical input
failure rejected before schema validation. Repeated `archetype_key`,
`profile_key`, or `template_key` values occur across separate array entries and
are semantic uniqueness failures rejected after schema validation.

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
