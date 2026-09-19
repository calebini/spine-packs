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

## Schema-15 alignment

The additional inspected baseline is Spine runtime `0.5.0`, schema `15`, commit
`ab18a8a51c9bf548220f67e2db0220bfe9783888`. Installer `0.2.0` admits
that exact pair in addition to the existing `0.3.0` / `12` baseline. `0.4.0`,
schema 14, future schemas, and undeclared runtime versions remain unsupported.
Installer `0.2.0` passed exact-commit release qualification at `57a6776` on both
baselines. This does not qualify a staging deployment. Publication gates and
the qualification record are in `docs/releases.md` and `docs/release-finalization.md`.

`kinflow-starter.1.0.0-draft.10` preserves every draft-9 definition, binding,
and empty dependency list. It changes only draft identity, runtime allowlist
to `["0.3.0", "0.5.0"]`, and the recomputed digest. The three content contracts
remain unchanged. Drafts 1–9 and their fixture bytes remain review evidence.

Stable `kinflow-starter 1.0.0` promotes draft 10 with the same compatibility
declaration and no definition changes. Only version, release status, and content
digest change; drafts 1–10 remain unchanged. Installer `0.2.0` is required for
the declared `0.5.0` runtime; `0.1.0` does not support that baseline.

The public command map is unchanged, but execution on `0.5.0` requires
`spine.system-info.v3` and `spine.ledger-instance.v1` in place of
`spine.system-info.v2`. The installer MUST bind and recheck the returned
ledger identity as defined in the installer specs. Content compatibility alone
does not bypass this gate. Disposable source and installed-package qualification
MUST cover both supported baselines before publishing the extension.

## Spine 0.6.0 candidate alignment

Installer candidate `0.3.0` adds Spine `0.6.0` / schema `15` at exact commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, retaining both prior baselines.
The inspected CLI contracts and handlers are unchanged from the 0.5.0 pin;
new trusted-web read contracts do not enter the CLI installer union. The exact
runtime and ledger-instance identity remain bound into every plan.

Released `kinflow-starter 1.0.0` still excludes `0.6.0` and MUST fail closed on
that runtime. Its bytes MUST NOT change. The proposed successor is
`1.0.1-draft.1`, adding only `0.6.0` to the exact runtime allowlist, changing
draft identity/status, and recomputing the digest. All 52 archetypes, profiles,
bindings, dependencies, and content contracts remain identical to 1.0.0.
This draft cannot be applied. Stable `1.0.1` promotes it with only version,
release status, and digest changes; it preserves the three-runtime allowlist
and requires installer `0.3.0` for Spine `0.6.0`. The stable artifact is prepared
for publication approval alongside installer `0.3.0`; it is not yet published.
Neither extension
qualifies a staged deployment whose source provenance has not been confirmed.

## Content compatibility is not execution readiness

`spine_content_contracts` is intentionally limited to the contracts that give
the owner-neutral definitions their meaning. It MUST NOT be interpreted as the
complete contract union required to execute `plan`, `apply`, or `verify`.

Spine's command registry may require additional contracts for a concrete
command, including `spine.canonical-json.v1`, notification-profile readback,
catalog cursor, response, or receipt contracts. The draft installer contract
in `specs/installer.md` names the command set and derives the complete
per-command requirement union for each inspected baseline. The installer MUST verify
that union independently. The v1 pack manifest makes no execution-readiness
claim.

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
- generalized evidence required to widen compatibility beyond the pinned baselines;
- compatibility declarations for dependency packs; and
- evidence and review required to support installer execution against an
  additional Spine runtime.
