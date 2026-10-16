# FR-2 bounded audit disposition

Date: 2026-10-16. Attempt 002 completed with valid structured reviewer output.
Whetstone verdict: **needs_revision**, with zero blockers, one major and two
minor findings. This is a bounded audit verdict, not a convergence declaration.
Attempt 001 remains preserved as an input-size infrastructure failure.

## Findings and local triage

1. **Major — desired rendering byte bounds.** Accepted by source inspection.
   Manifest validation checks character limits/normalization, but not the
   canonical UTF-8 rendering revision bound; the planner also lacks a resolved
   byte check. Observed rendering definitions do enforce 8,192 bytes. Long
   multibyte text can therefore make a proposed revision necessarily impossible
   while the outer plan is marked eligible. A narrow patch should reject definite
   oversize content and validate known resolved IDs, without guessing future IDs
   or conflating portable local-reference byte length with final wire length.
   Preserve the future execution materialization check and add boundary tests.
2. **Minor — malformed failure taxonomy.** Accepted by source inspection.
   Invalid revision-handler failure shapes and unsupported exits can fall through
   to an ordinary Spine rejection. Planning stops, so this is not an absence/write
   bypass; it is incorrect machine-readable error ownership. Distinguish recognized
   preflight failures from malformed handler output and assert exact categories.
3. **Minor — stale current spec introductions.** Accepted by direct text check.
   `specs/pack-format.md` still says installer support is unimplemented;
   `specs/installer.md` still introduces the successor as 0.9.1. Align only those
   current cross-references with exact 0.10.0 read-only FR-2 and keep successor
   apply/recovery/verify disabled. Do not rewrite historical baseline evidence.

These dispositions are inspection-based; no tests or new ledger experiments
were executed during this review turn. All three findings are actionable within
the existing FR-2 boundary; none requires inventing product/disclosure policy.

## Integrity and scope

- All 44 approved raw hashes are unchanged after the review. The saved audit
  manifest's normalized hashes also match the approved content under Whetstone's
  documented whitespace normalization.
- The locally preflighted prompt was 923,380 characters, below the CLI's
  1,048,576-character input limit. No additional files or failed-attempt transcript
  were intentionally added to the reviewer payload.
- Execution identity is the recorded embedded CLI and explicitly selected
  `gpt-6.1-sol` in execution-authorization.md/audit_manifest.json. The feedback's
  generic self-reported reviewer metadata is not independent executable/model
  provenance.
- No Editor, source patch, successor apply/recovery/verify, commit, push,
  deployment or publication occurred. Only review-control/result artifacts changed.

Recommended next step: obtain approval for a narrow patch of all three findings,
run the required tests and focused byte-bound/failure vectors, then stage a focused
recheck with a fresh exact payload approval. Do not advance to FR-3 on this verdict.
