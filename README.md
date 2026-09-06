# Spine Packs

Spine Packs is a draft-contract repository for independently versioned,
operator-installable archetype and notification-profile packs for Spine. Packs
are declarative, reusable content; they are not services and do not become
authoritative runtime state merely by existing here.

## Authority and boundaries

Spine remains the sole authority for installed archetypes, notification
profiles, bindings, receipts, and ownership. A future installer may translate a
reviewed pack into operations, but it must use Spine's existing public command
surface. Direct database access is forbidden.

Reusable packs are owner-neutral. They must not embed owner IDs, delivery
targets, subjects, routes, or environment-specific facts. Those values belong
to operator input and Spine-managed state. This repository also contains no
Spine runtime changes, alternative ledger, scheduling implementation, daemon,
or service.

Released pack versions are immutable. A changed definition requires a new pack
version rather than an in-place rewrite of a released version.

## Intended workflow

A future installer is expected to expose three phases:

1. `plan` compares a selected pack with Spine through the public command
   surface and produces a deterministic, reviewable change plan.
2. `apply` creates missing definitions, retains equivalent definitions, and
   refuses semantic drift unless the operator explicitly authorizes an update.
3. `verify` confirms through the public command surface that the intended
   definitions and resulting Spine receipts agree with the approved plan.

This workflow is a design target, not an implemented command. This repository
contains a first-pass manifest contract and draft content, but no
installer or package runtime.

## Repository map

- `specs/` is the normative source of truth for purpose, architecture,
  compatibility, pack-format requirements, and approved pack content.
- `contracts/schemas/` contains the machine-readable manifest contract.
- `packs/` contains independently versioned pack source material, including
  the draft `kinflow-starter` vertical slices.
- `tests/contract/` and `tests/fixtures/` contain dependency-free contract
  checks and positive/negative manifest fixtures.
- `scripts/verify_repo.py` checks repository shape and high-level boundary
  markers without third-party dependencies.
- `AGENTS.md` gives repository-specific instructions to automated contributors.

## Current maturity

This repository is at the **draft-contract** stage. Schema identity
`spine.pack-manifest.v1` and draft `kinflow-starter` version
`1.0.0-draft.6` covers the established slices plus the approved Education,
Social, Travel, and Renewals and administration archetypes and
archetype-specific notification profiles.
Earlier drafts remain preserved byte-for-byte.
Approved content is specified in [specs/kinflow-starter.md](specs/kinflow-starter.md).
The drafts are not released or installable, and additional archetypes may be
added before a future immutable `1.0.0` release. The recorded Whetstone audit
covers the earlier medical-only slice, not later draft content.

Run the local structural check with:

```sh
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests/contract -p 'test_*.py'
```
