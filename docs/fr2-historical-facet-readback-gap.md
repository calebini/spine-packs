# FR-2 historical facet-pin readback gap

Inspection date: 2026-10-11. This is implementation-readiness evidence, not a
change to Spine's contract or permission to relax installer failures.

The operator authorized FR-2 read-only planning after commit `5403680`.
The exact Spine commit `57cda1c2d5589360ee8efe7155fd20b503034c2a` is available
locally (`git cat-file -t` returned `commit`). Inspection used `git show` at
that pin, not the reference checkout's working files. The target remains
runtime `0.9.1`, schema `19`; no compatibility range is implied.

## Finding

FR-2 must read exact historical facet-schema revisions needed by selected
existing pins before classifying the desired graph. A valid existing binding
or rendering selection can pin an older revision from a different schema root
than the manifest now desires. The reviewed observation algorithm does not
specify how to discover that revision's root.

At the exact pin:

| Public surface | Relevant facts |
| --- | --- |
| `facet_schema.list` | Roots expose root ID, owner, key, current revision ID and status; no revision history |
| `item_archetype.facet_binding.list` | A binding exposes its schema revision ID, not the schema root ID |
| Rendering definition list/show | Each selection exposes its schema revision ID, not the schema root ID |
| `facet_schema.show` | Requires `facet_schema_id`; optionally accepts `facet_schema_revision_id` |

These are the checked-in readback schema definitions `public_0102`,
`public_0110`, `public_0072`, and `public_0103`, respectively. Their source
pointers are recorded in `contracts/installer-spine-0.9.1-inventory.json`.
The pinned registry has no additional facet revision lookup/list command.

Upstream `src/spine/commands/facet_reads.py:54` confirms that show resolves the
supplied root and revision, requires their membership to match, and returns
`referenced_row_not_found` at field `facet_schema_revision_id` on mismatch.
This was source inspection only; no internal function was invoked.

## Concrete witness and limits

Consider two owner-local roots: `flight_details` currently at A2 and
`legacy_details` currently at B2. An existing flight binding pins B1; the new
manifest desires `flight_details`. Neither list identifies B1's root. Using
the desired root A for show(B1) is not justified and the handler rejects that
pair. The binding's facet key is not a schema-root key.

An independent Draft 2020-12 check against the offline pinned schema confirmed:

- both synthetic root shapes and the old-revision binding shape are valid;
- B1 matches neither root's current revision;
- show with only `facet_schema_revision_id` is invalid (root ID is required);
- binding and rendering-selection schemas contain no schema-root field.

This is a static contract witness, not a disposable-ledger reproduction or a
claim that upstream validation is broken. The simple missing-object flight flow
and known-root historical reads do not have this ambiguity. The gap concerns
general historical observation and cross-root drift required by FR-2.

## Decision before runtime implementation

Two paths need explicit resolution:

1. Ask the Spine agent for an authoritative public revision-to-root lookup
   path. If none exists, propose a bounded public readback extension there.
   Any changed Spine baseline requires explicit pin adoption, contract refresh
   and qualification; do not silently move this repository to a newer checkout.
2. Specify and review bounded candidate-root probing using existing show:
   try only roots from the complete exact-owner inventory, treat only a
   precisely validated membership-mismatch response as a candidate miss, and
   require an unambiguous successful match within the existing global budgets.
   All other failures must abort. This changes the current rule that a rejected
   public read aborts observation and needs explicit failure/capacity fixtures
   and bounded review before implementation. It is not automatic authorization
   to suppress `referenced_row_not_found` generally.

Recommendation: request Spine's supported lookup guidance first. Do not
introduce probing as an undocumented adapter behavior. Do not infer roots from
pack keys, generated-ID spelling, opaque cursor contents, an installer registry,
database access, item reads, or internal Spine APIs. Do not omit historical
readback or silently narrow the FR-2 acceptance gate to all-new catalogs.

No runtime files, schemas, released packs, Spine checkout, ledger, deployment,
or reviewer payloads were changed during this investigation. No external
reviewer was run. FR-2 implementation remains pending this resolution.

## Resolution adopted 2026-10-16

The preceding record is historical and unchanged. The operator explicitly
adopted `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, Spine `0.10.0`, schema `19`.
Its trusted-local `facet_schema.revision.show` resolves an exact observed
revision ID to the actual root and immutable definition, including historical
revisions and retired roots. No root probe or failure-suppression amendment is
needed. The lookup gap is resolved by this public extension, not by changing
the old finding or assuming a desired root.

The new command inventory and full closure are separate 0.10.0 artifacts.
FR-2 uses this command once per referenced revision per observation pass and
validates returned identity/owner/hash against the full owner inventory. Missing
referenced evidence still aborts planning. See `specs/installer-artifacts-v2.md`
for the normative failure mapping and `docs/fr2-qualification.md` for independent
planner qualification; upstream tests alone do not qualify this installer.
