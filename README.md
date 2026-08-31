# Spine Packs

Spine Packs is a seed-stage repository for independently versioned,
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

This workflow is a design target, not an implemented command. The installer,
manifest schema, example manifests, and package runtime are intentionally
deferred until the pack-format contract has been reviewed.

## Repository map

- `specs/` is the normative source of truth for purpose, architecture,
  compatibility, and the pre-schema pack-format requirements.
- `packs/` contains independently versioned pack source material. At this
  stage, `packs/kinflow-starter/README.md` only reserves the first pack.
- `scripts/verify_repo.py` checks the seed repository shape and high-level
  boundary markers without third-party dependencies.
- `AGENTS.md` gives repository-specific instructions to automated contributors.

## Current maturity

This repository is at the **seed-spec** stage. It defines ownership and design
constraints but does not yet define an installable pack or stable
machine-readable contract. Review and resolve the open questions in
`specs/pack-format.md` before defining `kinflow-starter.v1`.

Run the local structural check with:

```sh
python3 scripts/verify_repo.py
```
