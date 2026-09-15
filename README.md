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
3. `verify` confirms resulting catalog state through the public command surface
   and correlates the Spine command responses preserved during `apply` with the
   approved plan.

Read-only `plan`, non-mutating apply preflight, initial approved `apply`, and
same-execution continuation with bounded uncertain-response recovery are
implemented as source-tree slices. `verify` is not implemented.
The normative contract is [specs/installer.md](specs/installer.md).
The ordered delivery slices and their completion gates are recorded in
[specs/implementation-plan.md](specs/implementation-plan.md).

## Read-only planner

From this checkout, using Python 3.11 or newer:

```sh
PYTHONPATH=src python3 -m spine_packs plan \
  --manifest packs/kinflow-starter/kinflow-starter.1.0.0-draft.9.json \
  --request /absolute/operator/path/request.json \
  --output /absolute/operator/path/new-plan.json
```

Supply your own sealed `spine.pack-install-request.v1` artifact with explicit
owner, resolved target, selection, and digest; the request contract and hashing
rules are in [specs/installer-artifacts.md](specs/installer-artifacts.md).
There is no request wizard or environment discovery command in this slice.
Keep environment-specific operator artifacts outside `packs/` and source control.
Existing fixture targets and owner IDs are test data, not usable configuration.

The saved request selects `all` or an exact sorted list of archetype keys.
Optional `--all` or repeated `--archetype KEY` flags only assert that same
selection; they never override it. The current draft pack requires
`draft_posture=inspect_only` and can never produce an apply-eligible plan.

The target must already expose the pinned compatible Spine `0.3.0` public
surface and ledger schema 12. The planner will not downgrade or modify Spine,
open its database, or issue write commands. An incompatible newer runtime is
rejected, not assumed compatible. Run against an operator-selected local
target without concurrent catalog writers.

The command emits one compact JSON result envelope to stdout and publishes a
private plan at a new output path. The parent directory must exist; existing
files and symlinks are never overwritten. Blocked plans exit 6. Unblocked draft
inspection exits 0 even with drift. Released drift exits 5 for a decision;
released no-drift plans exit 0. All four return a reviewable plan. Eligibility
does not authorize execution, and this slice cannot execute any plan.

## Initial approved apply

This is an initial-execution implementation tested with simulated Spine commands,
not yet qualified against a real target. It requires a separately released pack;
the checked-in `kinflow-starter` drafts remain ineligible and unchanged.

```sh
PYTHONPATH=src python3 -m spine_packs apply \
  --manifest /absolute/operator/path/released-pack.json \
  --plan /absolute/operator/path/approved-plan.json \
  --approval /absolute/operator/path/approval.json \
  --checkpoint /absolute/operator/path/new-checkpoint.json \
  --output /absolute/operator/path/new-result.json
```

The approval must bind the exact plan digest, authorize every update action,
acknowledge single-operator operation, and supply a stable execution UUID,
actor, and timestamp. There are no apply selection flags or draft overrides.
Preflight freshly rechecks the complete planned catalog before any write.
Only the six reviewed catalog write commands can be submitted.

The checkpoint is saved before each command and advanced only after its
response is validated and durably recorded. A successful initial apply exits 0;
a failed or uncertain submitted command exits 9 with a `partial` result,
including when the first command's outcome is unknown. A preflight failure
uses its specific error exit and can produce `not_applied` evidence.

Checkpoint and result paths must be new, distinct, and separate from inputs
and the target files. Checkpoints are private and atomically replaced during
the run. Disk failure or interruption may leave only a checkpoint. Preserve it;
do not delete it to retry under a fresh execution.
`applied` is not independent post-install verification.

## Continue an interrupted apply

Use the same manifest, plan, and approval, adding `--continue-from` with the
most recent preserved checkpoint or terminal `partial` result:

```sh
PYTHONPATH=src python3 -m spine_packs apply \
  --manifest /absolute/operator/path/released-pack.json \
  --plan /absolute/operator/path/approved-plan.json \
  --approval /absolute/operator/path/approval.json \
  --continue-from /absolute/operator/path/preserved-checkpoint.json \
  --checkpoint /absolute/operator/path/new-continuation-checkpoint.json \
  --output /absolute/operator/path/new-continuation-result.json
```

Both destination paths must be new; the source is preserved. Choose the latest
evidence for this execution yourself—there is no checkpoint discovery or registry.
Continuation validates the complete accepted prefix and fresh public catalog
state. It permits only that prefix or the prefix plus its first unresolved
action, then retries that action with its original command ID and exact request.
Unexplained changes, altered approvals, and evidence gaps fail closed before
another write. Such preflight failures emit an error envelope, not a misleading
`not_applied` result for an execution that may already have changed Spine.

Slice 4 is tested with simulated public commands and fault injection; bounded
review and real-target qualification remain pending. No current draft pack is
made installable by this feature.

## Repository map

- `specs/` is the normative source of truth for purpose, architecture,
  compatibility, pack-format requirements, installer behavior and artifacts,
  the installer implementation plan, and approved pack content.
- `contracts/schemas/` contains the machine-readable manifest and draft
  installer-artifact contracts.
- `packs/` contains independently versioned pack source material, including
  the draft `kinflow-starter` vertical slices.
- `tests/contract/` and `tests/fixtures/` contain dependency-free contract
  checks and positive/negative manifest fixtures.
- `src/spine_packs/` contains planning, preflight, initial/continued apply, and the local command adapter;
  `tests/runtime/` exercises them with synthetic public readbacks and subprocesses.
- `scripts/verify_repo.py` checks repository shape and high-level boundary
  markers without third-party dependencies.
- `AGENTS.md` gives repository-specific instructions to automated contributors.

## Current maturity

This repository is at the **draft-contract** stage. Schema identity
`spine.pack-manifest.v1` and draft `kinflow-starter` version
`1.0.0-draft.9` covers the established slices plus the approved Education,
Social, Travel, Renewals and administration, Health, and Home, vehicle, and
logistics and General commitments archetypes and archetype-specific
notification profiles.
Earlier drafts remain preserved byte-for-byte.
Approved content is specified in [specs/kinflow-starter.md](specs/kinflow-starter.md).
The drafts are not released or installable, and additional archetypes may be
added before a future immutable `1.0.0` release. The recorded content audit
covers the earlier medical-only slice, not later draft content. A separate
bounded Whetstone audit passed installer prose draft v0.3 with its
public-command and single-operator boundaries preserved.

The installer prose contract is at draft v0.4. It defines the intended
agent-oriented CLI, granular archetype selection, reconciliation
classifications, approval, partial-apply, and verification posture for a local
single-operator v1. It has a draft machine-artifact companion with closed
request, plan, approval,
checkpoint, apply-result, verification-result, and CLI-result schemas and
focused contract vectors. Planning, preflight, initial apply, and bounded
same-execution continuation are implemented.
They have not been validated against a live operator target;
the local tests use synthetic responses pinned to the inspected public surface.
Verification and packaging remain unimplemented. Stable Spine instance identity, binding
compare-and-set, and public receipt readback remain future hardening rather
than v1 blockers.

Run the local structural check with:

```sh
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests/contract -p 'test_*.py'
python3 -m unittest discover -s tests/runtime -p 'test_*.py'
```
