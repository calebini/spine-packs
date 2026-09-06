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

`kinflow-starter` draft `1.0.0-draft.2` retains exactly the same runtime and
content-contract allowlists as `1.0.0-draft.1`. The lesson slice uses only the
existing v1 content shapes; it does not widen compatibility or assert support
for any item-level recurrence command.

Draft `1.0.0-draft.3` retains those exact allowlists. Its birthday templates
use Spine's existing calendar-day target-offset shape and inherit timezone
facts from the applicable local item target. The pack does not declare a
timezone, timezone-database version, or recurrence capability.

Draft `1.0.0-draft.4` retains those exact allowlists. Its Education and Social
profiles use only the already-declared elapsed and calendar-day target-offset
forms. The exact-target dinner and visitor templates use the supported
`offset_seconds=0` form described below.

Draft `1.0.0-draft.5` retains those exact allowlists. Its Travel profiles use
only the same elapsed and calendar-day target-offset forms. Item relationships,
including a packing task's relationship to a trip, are not manifest content
and make no additional compatibility claim.

Draft `1.0.0-draft.6` retains those exact allowlists. Its Renewals and
administration profiles use only the existing calendar-day target-offset form.
The 365-day and 270-day passport boundaries do not claim unsupported
calendar-year or calendar-month arithmetic.

Draft `1.0.0-draft.7` retains those exact allowlists. Its Health profiles use
only the existing calendar-day target-offset form. The 365-day and 180-day
vaccination boundaries do not claim calendar-year or calendar-month
arithmetic, recurrence, or clinical-guidance semantics.

Draft `1.0.0-draft.8` retains those exact allowlists. Its Home, vehicle, and
logistics profiles use only the existing elapsed and calendar-day target-offset
forms, including the already-supported exact-target elapsed form. The delivery
window definition does not claim range-scheduling semantics.

Draft `1.0.0-draft.9` retains those exact allowlists. Its General commitments
profiles use only the existing elapsed and calendar-day target-offset forms,
including the already-supported exact-target elapsed form. General archetypes
do not introduce runtime fallback or item-dependency semantics.

The v1 pack contract's exact-target elapsed form, `offset_seconds=0`, is within
the signed elapsed-offset semantics accepted by the inspected Spine runtime
`0.3.0` under `spine.notification-profiles.v1`. Supporting that form does not
widen the runtime or content-contract allowlists. The pack contract continues
to exclude positive, post-target elapsed offsets.

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
