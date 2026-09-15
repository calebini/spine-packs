# Slice 4: same-execution continuation and uncertain-response recovery

## Change intent and authority

Review Slice 4 at commit `62b4a23b1cd1d819379542f6d741737e37d9520c`,
based on `14d7d31948b18fa5c2466eb816ac5b14a20824f7`.
This is one bounded, reviewer-only Whetstone `audit-change` consistency pass.
It is not an Editor task, a Phase 1/2 loop, or a convergence declaration.
Specs are normative. Source code and tests are implementation evidence, not
new authority; the `--spec` transport label does not make code normative.

The change adds `recovery.py`, shares the durable apply loop, separates fresh
public observation from plan compilation, and exposes `apply --continue-from`.
The existing schemas, six write commands, pack contents, and Spine runtime are
unchanged. Slice 3 dependencies are included only to inspect this new boundary
and regressions introduced by the shared-loop refactor.

## Expected boundary

- Spine remains sole authority for installed definitions, bindings, receipts,
  and ownership. Packs remain declarative, owner-neutral, and release-immutable.
- Only the pinned local Spine 0.3.0 / ledger 12 public command surface is used.
  No direct database access, Spine imports, deployment changes, or real installs.
- Planning retains its read allowlist. Apply permits only archetype create/revise,
  profile create/metadata.update/revise, and notification-profile binding.set.
- Continuation requires the same manifest, plan, exact approval, execution UUID,
  actor, timestamp, stable command IDs, and semantic requests. Accepted evidence
  is a contiguous validated response prefix, never a guess based on current state.
- The operator supplies the most recent checkpoint or terminal partial result.
  No registry, discovery, evidence merge, or automatic new execution is introduced.
  A completed checkpoint can recover a lost terminal-result publication.
- Source evidence is preserved. Checkpoint/result destinations are new and
  distinct from inputs and target files. Source/target path collisions are
  rejected before reading the source as an artifact.
- Fresh preflight must admit exactly the accepted-prefix state or that state
  plus at most the first unresolved action. Gaps, unrelated catalog changes,
  changed approvals, unexplained selected state, and stale suffixes fail closed.
- Installer-artifacts Section 9.1 permits inverse fingerprint comparison only
  alongside complete public readback, full semantic/identity/provenance checks,
  and original-plan reconstruction. Comparison is private computation, not
  rollback, independent receipt evidence, or historical-state authority.
- Case-2 readback IDs are provisional. They cannot alter the original request
  or feed suffix references. Exact retry response correlation and durable
  recording must precede advancement. No ID prediction is allowed.
- Binding preconditions are re-read immediately before submission. Only the
  first unresolved case-2 binding uses its exact admitted post-action identity.
- Prepared checkpoints precede writes; validated responses are durably recorded
  before advancing. Failures stop without compensation or rollback. An empty
  accepted prefix does not prove that nothing was submitted or committed.
- Preflight failure on continuation emits only an error envelope, not a false
  not_applied result. Post-admission failure conservatively preserves partial
  evidence. Durability failures do not fabricate terminal success.
- The threat model is one local operator, no concurrent catalog/artifact writer,
  immutable Spine revisions and receipts, not hostile filesystem actors or
  distributed locking. Metadata ABA history and public receipt readback remain
  unavailable in Spine 0.3.0; snapshot equality does not claim otherwise.

## Reviewer questions

1. Can source validation accept a mismatched plan/approval/execution, reordered
   prefix, altered prepared request, invalid effect, receipt, or generated ID?
   Are partial-result derivation and completed-checkpoint handling consistent?
2. Does admission distinguish exactly the two allowed states across all six
   write kinds? Can inverse reconstruction erase unexplained selected or
   unselected changes, rely on fabricated historical facts, or overlook a
   remaining suffix precondition? Examine metadata-plus-revision sequences.
3. Are full public definitions, semantics, available creation/revision provenance,
   known response IDs, and fresh catalog hashes checked independently enough?
   Examine no-op effects, equivalent selected definitions, and absent bindings.
4. Can provisional case-2 IDs escape into a retry request, accepted evidence,
   or later references before a matching actual response has been recorded?
   Are all exposed root/revision/binding IDs correlated on replay?
5. Does restart preserve the original request and command ID at every action
   boundary, including acceptance before response capture and failed checkpoint
   advancement? Can a retry duplicate, skip, reorder, or regenerate an action?
6. Are both normal and uncertain binding preconditions rechecked correctly?
   Does a post-admission change stop before another binding write?
7. Do CLI source/destination protection, byte limits, private atomic publication,
   source preservation, failure envelopes, and partial results match the specs?
   Can a continuation incorrectly claim not_applied or lose preserved evidence?
8. Do the tests meaningfully establish the recovery promises rather than only
   mirror the implementation? Identify precise missing or misleading vectors.
   Is the Slice 3 initial path preserved by the shared execution loop?
9. Are the normative specs, implemented scope, and Slice 4 completion gate
   consistent without implying Slice 5 verify or real-target qualification?

## Evidence and limitations

The payload is these notes plus six specification/sequence documents, all ten
runtime modules, eleven checked-in schemas, five runtime test modules, and the
independent installer-artifact contract test module: 34 files total.
The verification-result schema is schema dependency closure only, not scope
to implement or review a future verify command.

Local checks against the committed change: repository verifier PASS (93 required
files), contract suite PASS (50 tests), runtime suite PASS (90 tests), staged and
tracked whitespace checks PASS. The 19 continuation tests include parametrized
action-boundary cases. These are synthetic tests, not real Spine qualification.
`test_recovery_evidence.py` is the earlier test-only snapshot feasibility probe
and supplies fixture helpers; it is not production recovery admission. The
full-readback double in `test_continuation.py` is still a synthetic oracle.

Fixture trees and pack contents are intentionally not transmitted. This is a
static-review payload, not a standalone runnable checkout. If omitted evidence
is essential, identify the exact gap rather than reading other workspace files
or guessing that a test was run. The existing authority docs and supplied public
contract schemas are sufficient to inspect the implementation boundary.

## Out of scope and requested output

No Editor, source edits, automatic patches, external browsing, additional file
reads, Spine checkout access, command execution against a target, deployment,
commit, push, or release. No Slice 5 verification, Slice 6 integration/packaging,
remote transport, presentation hints, new pack contents, or redesign of accepted
semantics. Do not promote deferred CAS, stable instance identity, public receipt
readback, or multi-writer hardening to blockers without a concrete failure
inside the declared single-operator threat model.

Return a verdict, boundary-preservation assessment, and prioritized concrete
findings with file/section/function references, failure scenarios, and minimal
fix/test recommendations. Distinguish demonstrated defects from uncertainty
and missing evidence. Mark unrelated observations out of scope. Do not declare
convergence, release readiness, or live-target qualification.
