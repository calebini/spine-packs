# Compatibility

## Compatibility dimensions

Every released pack version must declare compatibility independently for:

1. the Spine runtime versions whose public command behavior it can use; and
2. the Spine contract versions that define the relevant archetype,
   notification-profile, binding, and receipt semantics.

Runtime and contract compatibility are separate dimensions. Matching one must
not be treated as evidence that the other matches.

## Installer behavior

Before planning content changes, a future installer must obtain the target
Spine runtime and contract versions through the public command surface and
evaluate them against the pack's declarations. It must fail closed when:

- either target version cannot be determined;
- a required compatibility declaration is absent;
- the target lies outside a declared compatible set; or
- the installer cannot interpret the declaration without ambiguity.

Compatibility failure must not be bypassed implicitly during `apply`. Any
future override mechanism requires explicit contract review and must remain
visible in both the approved plan and Spine-owned receipts where the public
surface supports it.

## Version changes

A released pack's compatibility declaration is part of its immutable content.
Expanding or narrowing compatibility after release requires a new pack version.
Pack publishers should only declare compatibility supported by contract review
and verification evidence.

## Unsettled contract details

The following are intentionally unresolved until pack-format review:

- the version expression syntax for Spine runtime compatibility;
- the version expression syntax and naming scheme for Spine contracts;
- whether compatible sets must be closed ranges, enumerations, or another
  deterministic form;
- how prerelease and development Spine builds are represented;
- the evidence required before a pack may widen compatibility; and
- whether minimum installer-version compatibility is also required.

No manifest example or parser behavior should be inferred from this document.
