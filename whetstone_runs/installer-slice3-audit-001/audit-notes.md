# Slice 3: initial approved apply and durable checkpoints

## Change intent and authority

Review the Slice 3 implementation at commit
`00d3d878563f4917c26dcd454b2eacbfdc4bddce`, based on
`495c120675261cbcdc153b12226676aa2f41d6fd`.
This is one bounded, reviewer-only `audit-change` consistency pass over the
submitted current files, not a Phase 1/2 convergence run or an Editor task.
Specs are normative; implementation and tests are evidence, not new authority.
The implementation plan describes slice sequencing, not expanded authorization.

## Expected boundary

- Spine remains sole authority for installed definitions, bindings, receipts,
  and ownership. Packs remain declarative, owner-neutral, and release-immutable.
- This slice enables initial approved apply only, against the pinned local
  Spine 0.3.0 / ledger 12 public contract. No direct database access is allowed.
- Planning retains its strict read allowlist. Apply permits only
  `item_archetype.create`, `item_archetype.revise`,
  `notification_profile.create`, `notification_profile.metadata.update`,
  `notification_profile.revise`, and `notification_profile.binding.set`.
- Complete plan/approval/manifest validation and fresh preflight precede writes.
  Semantic drift requires exact explicit authorization. Binding preconditions
  are re-read immediately before binding submission.
- Execution identity, actor, timestamp, command IDs, and exact requests are
  stable. Generated references come only from validated accepted responses.
- A private, durable prepared checkpoint precedes every write. A response is
  validated and durably recorded before advancing. Failure stops the sequence;
  no compensation, rollback, automatic retry, or continuation is implemented.
- Results preserve `applied`, `partial`, and `not_applied` distinctions. An empty
  accepted prefix does not establish that no write was submitted or committed.
- The threat model is a local single operator, not hostile filesystem actors,
  concurrent writers, distributed locking, or cryptographically signed approval.

## Reviewer questions

1. Can any write escape approval, fresh preflight, exact target compatibility,
   the six-command allowlist, or durable prepared-checkpoint publication?
2. Do all six request/response pairs correlate command ID, semantic request hash,
   receipt timestamp/effect, keys, literal IDs, revisions, metadata, and generated
   IDs sufficiently? Can malformed evidence enter the accepted prefix or feed a
   later action? Examine binding root IDs as well as the binding ID.
3. Does execution stop safely at every publication, submission, response, and
   checkpoint-advance boundary? Include link/replace, file/directory fsync,
   timeout, rejection, malformed response, and terminal-result publication.
4. Is potentially committed work represented conservatively even when the first
   response is invalid or unavailable? Are failure identity, accepted prefix,
   unresolved exact request, and unattempted suffix mutually consistent?
5. Do checkpoint/result artifacts actually satisfy the independent machine and
   semantic contracts, including zero-action success and zero-prefix failure?
6. Are no-clobber behavior, permissions, path aliases/symlinks, preserved prior
   checkpoints, byte/time bounds, and sanitized errors correct for this scope?
7. Do tests exercise meaningful negative and fault-injection cases rather than
   merely mirror implementation assumptions? Identify concrete missing vectors.
8. Do the normative specs, implementation plan, and runtime agree about the
   initial-only boundary and its exit gate? Is this slice ready to close after
   any identified blocking fixes, without claiming real-target qualification?

## Evidence and review limits

The payload contains six normative/sequence documents, all nine current runtime
modules, eleven checked-in schema files, three runtime test modules, and the
independent installer-artifact contract test module, plus these notes.
Supporting preflight/planner/schema material is included to follow dependencies;
do not turn this into a general re-audit of unchanged functionality.
The verification-result schema is reference closure only, not a request to
implement or audit a future verify command.

Local staging checks: repository verifier passed (91 required files), 49 contract
tests passed, 62 runtime tests passed, and `git diff --check` passed. These are
reported evidence, not a substitute for review. Tests use simulated targets;
no actual installation, deployment, or release has been performed.
Fixture trees and pack content are intentionally not transmitted. This is a
static review payload, not a standalone runnable checkout. If omitted evidence
is essential, identify the exact gap rather than reading other workspace files.

## Out of scope and requested output

No Editor, source edits, automatic patches, external browsing, additional file
reads, Spine checkout access, live commands, deployment, commit, or push.
No Slice 4 continuation/recovery, Slice 5 verify, Slice 6 integration/packaging,
pack content changes, presentation hints, or redesign of accepted semantics.
Checkpoint evidence adequacy is in scope; implementing recovery is not.
Deferred CAS, ledger-instance identity, public receipt readback, and multi-writer
hardening are not new prerequisites unless a concrete current-scope failure is
demonstrated within the stated threat model.

Return a verdict, boundary-preservation assessment, and prioritized concrete
findings with file/section or function references, failure scenarios, and minimal
fix/test recommendations. Mark unrelated observations out of scope. Distinguish
proven defects from uncertainties and unavailable evidence. Do not declare
convergence, release readiness, or live-target qualification.
