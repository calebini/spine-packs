# Installer Implementation Plan

## Status and authority

This document sequences implementation of the installer contract in
`specs/installer.md` and `specs/installer-artifacts.md`. Those documents remain
normative when this plan is incomplete or imprecise. A listed slice is not
authorization to implement it; each slice requires separate review and
authorization before runtime scope expands.

The delivery strategy is deliberately vertical. Each slice must leave a usable,
tested boundary and must not introduce behavior assigned to a later slice.

## Delivery sequence

### Slice 1: read-only planning — complete

Implemented in `src/spine_packs/`:

- validate the complete manifest and sealed install request;
- resolve an exact selection and compatible local Spine target;
- query only the pinned public read-command surface;
- classify missing, equivalent, drifted, and blocked desired state;
- emit a deterministic, private, no-clobber plan artifact; and
- reject write commands at the subprocess boundary.

This slice has synthetic runtime and independent contract coverage. It has not
been qualified against a live operator target.

### Slice 2: apply preflight without writes — complete

Add the internal apply-preflight service boundary while keeping all Spine writes
disabled. Do not expose the public `apply` CLI command until Slice 3:

- validate and correlate the saved plan, approval, and complete manifest;
- require an apply-eligible released plan and complete action authorization;
- resolve and revalidate the exact local target and execution-contract union;
- repeat `system.info`, catalog collection, snapshot, and selected-object
  precondition checks;
- validate the complete ordered command templates and all IDs that can be
  materialized before execution;
- classify stale, incompatible, blocked, draft, and incompletely authorized
  attempts using the specified result envelope and exit behavior; and
- prove with negative tests that no subprocess write command can be launched.

Exit gate: every preflight failure is deterministic and non-mutating, and a
successful preflight produces only an in-memory execution-ready description.
It does not create a checkpoint or submit a Spine write.

### Slice 3: initial apply and durable checkpointing — implemented; bounded review pending

Enable an approved initial write sequence:

- establish the stable execution identity, actor, action timestamp, and
  reproducible command IDs;
- atomically publish the prepared checkpoint before each command submission;
- submit only the closed, validated Spine write-command set;
- validate and durably preserve each response before advancing;
- materialize generated-ID references only from validated prior responses;
- stop on the first rejection or malformed response; and
- emit `applied`, `partial`, or `not_applied` terminal results without
  compensation or rollback claims.

Exit gate: fault-injection tests cover every boundary between checkpoint
publication, command submission, response validation, and checkpoint advance.

The initial-only implementation is in `apply.py` and `execution.py`, with a
separate transport write allowlist and explicit CLI checkpoint/output paths.
Tests cover all six write commands, exact receipt/request correlation,
independent checkpoint/result contract validation, binding precondition changes,
empty-prefix partial failure, preflight refusal, no-write plans, and filesystem
publication failures. Qualification uses simulated commands only. Preserve any
interrupted checkpoint: no continuation or uncertainty recovery is implemented.
This slice still needs bounded review before being treated as reviewed delivery;
no real installation, pack release, or deployment is implied.

### Slice 4: continuation and uncertain-response recovery

Resume an interrupted execution without broadening its authority:

- validate checkpoint or terminal partial-result correlation;
- reconstruct the accepted prefix and its exact expected catalog state;
- distinguish the normal prefix state from the single permitted uncertain
  first-unresolved-action state;
- reuse the original command ID and exact semantic request;
- require compatible replay or new acceptance before advancing; and
- reject gaps, unrelated catalog changes, changed approvals, or altered
  execution facts.

Exit gate: restart tests cover every action boundary, including an accepted
write whose response was not durably recorded. No failed or stale execution can
skip, reorder, or regenerate an action.

### Slice 5: non-mutating verification

Implement `verify` independently of apply execution:

- reload and correlate the plan, manifest, target, and optional apply result;
- freshly read selected archetypes, profiles, and bindings;
- verify semantic desired state and selection scope;
- correlate captured command responses and receipt facts without claiming
  later authoritative receipt-row readback; and
- emit the closed verification artifact and specified result status.

Exit gate: verification performs no write or compatible-replay request and
detects target, state, evidence, and correlation mismatches.

### Slice 6: end-to-end qualification and supported packaging

Harden the complete local v1 workflow:

- run plan, approval, initial apply, interrupted continuation, and verify
  scenarios against an isolated disposable Spine ledger through public
  commands only;
- exercise missing, equivalent, authorized drift, rejected drift, stale plan,
  partial apply, uncertain response, and verification mismatch cases;
- confirm artifact permissions, no-clobber behavior, byte and time bounds, and
  secret-safe diagnostics; and
- define the supported package and entrypoint only after the source-tree
  workflow qualifies.

Exit gate: contract, runtime, fault-injection, clean-install, and disposable
integration checks pass from a clean checkout. Release of either the installer
or a pack remains a separate decision.

## Deferred hardening

The following remain explicit follow-ups rather than hidden v1 prerequisites:

- stable Spine ledger-instance identity;
- atomic compare-and-set for binding replacement;
- public command-receipt readback;
- remote transport;
- multi-writer reconciliation; and
- cryptographic approval or Foreman integration.

If one becomes necessary for a delivery slice, update the owning Spine and
Spine Packs contracts before implementation rather than weakening the stated
local, single-operator boundary.

## Per-slice completion rule

A slice is complete only when its normative references, machine contracts,
runtime behavior, focused tests, repository verification, documentation, and
working-tree review agree. Commit and push are separate operator decisions.
