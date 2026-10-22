# FR-4 recovery/verify contract readiness

Date: 2026-10-18. Status: authored contract/fixture increment; not runtime
implementation or installed-package qualification. Current execution status is
owned by `specs/implementation-plan.md`. Normative rules are in
`specs/installer-artifacts-v2.md` and `specs/facet-rendering-packs.md`.

## Scope and baseline

The operator authorized proceeding with FR-4, beginning with its recovery/verify
contract and fixture refresh. The reviewed FR-3 repair checkpoint is `52b30e2`.
This increment intentionally adds no installer runtime module and does not
enable `apply --continue-from` or `verify` for v2 artifacts.

Spine is pinned to `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime 0.10.0,
ledger schema 19. The commit exists locally; all 20 upstream schema inputs and
revision-readback authority pins in the 0.10.0 inventory match its Git tree.
This was checked with read-only Git inspection, not HEAD substitution, package
execution, a ledger or Spine handler imports. `system.info` is not source proof.

## Changes

- The draft shared v2 schema admits the exact-0.10.0 captured-response label and
  structurally rejects pairing either runtime with the other runtime's label.
  The historical 0.9.1 shape remains valid; no v1 schema changes.
- Two companion fixtures pin their unchanged FR-3 initial-flow source bytes,
  then supply complete prefix observations, verification and CLI envelopes.
  They do not copy/rewrite manifest, plan, approval, command IDs or acceptance.
- The FR-4 fixture index enumerates 36 interruption boundaries across the two
  six-action flows, covering all 11 distinct configuration write kinds.
- Test-only refresh/oracle modules separate continuation admission from replay
  correlation and independent verification. They do not import runtime code.
- Normative recovery/verification rules now spell out source admission,
  immutable lineage, provisional identity limits, exact replay, rendering
  provenance, both binding guards, verification failure precedence, evidence
  correlation and the historical-receipt limitation.
- Orientation and repository instructions now reflect the authorized contract
  gate, without pretending runtime recovery/verify or FR-5 is complete.

The component-scaffold guidance keeps these artifacts in the existing
specs/contracts/tests layout. No service, transport hierarchy or new public
recovery-artifact kind is introduced.

## Evidence and limitations

The focused suite covers every indexed prepared/response-loss/accepted boundary,
partial and complete checkpoint sources, refused terminal sources, changed
request/approval/execution/target/environment, malformed digests and prefix gaps,
wrong candidate identities/semantics/provenance, missing lineage, unrelated and
suffix changes, budget overflow, no speculative consumer IDs, binding rechecks,
exact replay, paired receipt labels and verification with complete/missing/invalid
evidence. It also checks no-write verification, exact heads/reference edges,
decoders, retired/missing selected objects, and unselected changes accepted by
verify but rejected by continuation. No-write retained objects are not fabricated
as no-op writes merely to create replay fixtures.

These are supplied synthetic observations and captured-response-shaped values.
Their computed legacy fingerprints are test data, not public Spine attestations.
The oracle checks consistency, not authenticity, fresh reads, durable publication,
real replay behavior or user authorization. Rendering candidates include full
synthetic public records so provenance is checked separately from projections.
No ledger, item, facet value, disclosure, reminder or notification was created.

Pre-review local checks passed:

- Repository verifier: 178 required files.
- Focused FR-4 official contract suite: 18 tests, no skips.
- Full official Draft 2020-12 contract suite: 117 tests, no skips (10.384 seconds).
- Required system-Python contract suite: 117 tests, 52 visible skips because its
  development validator is unavailable; the complete official run covers them.
- Full runtime suite: 180 tests passed (90.363 seconds).
- Whitespace and immutable-source checks passed. No changes under `src/`,
  `tests/runtime/` or `packs/`; all indexed historical/source pins match.

These gates do not replace runtime fault tests or source/installed-package
qualification. No packaging workflow or disposable-ledger gate was run.

## Bounded review and next increments

The operator-approved 20-file reviewer-only consistency audit completed under
`whetstone_runs/facet-rendering-fr4-contract-audit-001/`. It returned
`needs_revision` with two major test-oracle findings, both independently
reproduced. The report, approval, prepared inputs and assessment remain unchanged.

The operator authorized patching both findings. Metadata response revision IDs
now equal both the expected and preserved post-observation revisions. Rendering
admission retains a private copy of the complete validated public record and
replay must match it, including creation provenance. A prior creator is allowed
to differ from the current publisher when candidate and replay agree.

Four added regressions exercise correctly resealed metadata contradictions
through evidence/checkpoint/admission/verification; contradictory creation actor,
command and timestamp; consistent earlier creation; and caller mutation after
admission. The schema, all positive fixtures and installer runtime are unchanged
by these repairs. Post-patch verification is recorded in the audit's separate
`patch-followup.md`; local green tests do not independently close the findings.
No new reviewer, Editor, convergence run, commit or push is authorized here.

Post-patch checks passed: 22 focused FR-4 tests, 121 official contract tests
without skips, 180 runtime tests, repository verification (178 required files)
and whitespace checks. The system-Python contract command ran 121 tests with
56 development-validator skips, covered by the complete official run. Both
original reviewer reproductions now reject their contradictory evidence.

The explicitly approved focused recheck passed on 2026-10-20 with zero findings
and its boundary preserved. The retained
[report](../whetstone_runs/facet-rendering-fr4-contract-recheck-001/change_audit/change_audit_report.md)
closes the two correlation findings. The operator authorized a local checkpoint;
this does not activate runtime recovery/verify or authorize pushing.

Next, implement bounded public
observation/forward admission first, then same-execution continuation and its
durability/fault tests, then independent read-only verification. Preserve current
CLI rejection guards until their corresponding runtime boundary is ready.
Exact source/wheel/installed public-CLI qualification remains FR-5 and requires
separate setup authorization. FR-6 still owns curated flight fields, labels,
template choices, default/opt-in policy and distribution identity; this gate
settles none of those product choices. No deployment or publication is implied.

## Subsequent runtime foundation

The reviewed contract checkpoint is `b1379ce`. The operator subsequently
authorized resuming the local read-only recovery foundation, recorded in
`../specs/implementation-plan.md`. It adds fresh historical lineage reads and
exact accepted-prefix comparison, not candidate admission, replay, continuation
or verify. The contract review above is retained evidence, not independent
review of this new runtime code. CLI guards remain disabled; no ledger or
installed-package qualification is part of this increment.
