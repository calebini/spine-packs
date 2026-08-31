# Pack format requirements

## Status

This is a pre-schema contract for review. It defines required semantics without
choosing a serialization format or final manifest shape. Implementations and
examples must not treat headings or prose ordering here as a field layout.

## Pack identity

A pack must have a stable identity that is distinct from its display name and
does not depend on an owner or environment. The identity must be sufficient to
disambiguate dependency references and released artifacts. Renaming rules,
namespace ownership, allowed characters, and collision governance are
**unsettled**.

`kinflow-starter` is reserved in this repository as the first candidate pack;
the reservation is not a released manifest.

## Versioning and immutability

Every installable pack must identify one explicit version. A released
identity/version pair is immutable: content, compatibility claims, dependency
references, and ordering semantics must not change after release. A semantic
change requires a new version.

The version grammar, prerelease policy, release marker, artifact digest, and
signing or provenance mechanism are **unsettled**. Until they are reviewed, no
pack in this repository is installable or released.

## Archetypes

A pack may declare owner-neutral archetype definitions. Each definition must
have a stable pack-local key and enough semantic content for a future installer
to compare it with Spine's authoritative definition. Archetypes must not embed
owner IDs or environment-specific facts.

The required archetype fields, normalization rules, and semantic-equivalence
algorithm are **unsettled** and must align with Spine's reviewed public
contracts before a schema is created.

## Notification profiles

A pack may declare owner-neutral notification-profile definitions. Each profile
must have a stable pack-local key and semantic content that can be compared
through Spine's public command surface. Profiles must not embed delivery
targets, subjects, routes, credentials, owner IDs, or environment-specific
facts.

The boundary between reusable profile policy and operator-supplied delivery
configuration, plus the profile equivalence rules, is **unsettled**.

## Bindings

Spine is the sole authority for bindings. If the reviewed format permits a pack
to express binding intent, that intent must be owner-neutral and may refer only
to definitions by stable pack-local or dependency-qualified references. A
reusable pack must not identify an owner, subject, route, delivery target, or
environment.

Materializing a binding would require explicit installation inputs and Spine's
public command surface. Whether packs should contain binding templates at all,
which relationships they may express, and how required operator inputs are
declared are **unsettled**. No binding syntax is established here.

## Dependency references

A dependency reference must unambiguously identify a pack and a compatible or
exact version selection, then address referenced definitions by stable keys and
definition kind. Resolution must produce a fully pinned dependency set before
`apply`; missing, ambiguous, conflicting, or cyclic dependencies must fail
closed.

Version-range policy, registry or local-source discovery, vendoring, lock-file
ownership, cycle rules, and dependency integrity proofs are **unsettled**.

## Deterministic ordering

For identical pack bytes, pinned dependencies, explicit operator inputs, and
observed Spine state, `plan` must produce the same ordered operations and
diagnostics. Ordering must derive from stable semantic keys rather than
filesystem enumeration, mapping insertion order, locale, or timestamps.

The final contract must define:

- a total order across definition kinds;
- a total order within each kind;
- dependency-before-dependent behavior;
- stable tie-breaking and collision failures; and
- whether any authored list order has semantic meaning.

The exact canonical ordering algorithm is **unsettled**.

## Reconciliation behavior

The future installer must classify target definitions as missing, equivalent,
or semantically drifted. Missing definitions may be created. Equivalent
definitions must be retained. Semantic drift must fail closed unless an
explicit update is authorized for that operation. Authorization must not be
inferred from the existence of a pack or from a broad compatibility match.

Canonicalization, comparison diagnostics, authorization scope, idempotency
keys, and receipt correlation are **unsettled** and require agreement with
Spine's public contracts.

## Serialization questions

Serialization format, schema language, required and optional field behavior,
unknown-field handling, comments, file splitting, and canonical byte encoding
are all **unsettled**. A final schema, example manifests, and parser must wait
until these semantics have been reviewed.
