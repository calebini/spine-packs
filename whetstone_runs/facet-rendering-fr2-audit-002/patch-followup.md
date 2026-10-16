# FR-2 audit patch follow-up

Date: 2026-10-16. Operator authorized all three manual patches. This is local
implementation and verification evidence, not a new reviewer verdict. The original
payload, approval, report, feedback and inspection-based disposition are unchanged.

## Changes

1. Desired rendering revisions now fail complete-manifest validation when their
   minimum possible public wire encoding exceeds 8,192 canonical UTF-8 bytes.
   Planning repeats the check with retained observed revision IDs. Unknown IDs
   contribute only the public nonempty-string minimum to a size calculation;
   no guessed ID enters a plan. All-known references receive an exact check.
   Final materialization validation remains a required future execution gate.
2. Revision-readback failures now require the contextual handler schema and
   matching CLI exit, except separately recognized closed preflight envelopes.
   Malformed fields, shapes and unsupported exits produce installer environment
   failure, never ordinary rejection or absence evidence. Valid missing-reference
   rejection still aborts observation. Raw messages are not exposed.
3. Current pack-format and installer introductions now identify exact Spine
   0.10.0/schema 19 and implemented FR-2 read-only planning. Successor
   apply/recovery/verify remain disabled and unauthorized. Historical baselines,
   v1 compatibility and released pack bytes remain unchanged.

The artifact-v2 spec records the byte calculation and failure taxonomy. Focused
tests cover 8,192/8,193-byte boundaries, multi-byte text, retained and pending IDs,
mixed known/unknown references, portable keys versus wire IDs, malformed handler
responses and closed preflight recognition. Official JSON Schema validation
independently demonstrates why character limits alone do not enforce byte limits.

## Verification

- Repository verifier: passed, 160 required files.
- Required system-Python contract command: 90 tests, 25 development-dependency
  skips. Complete isolated Draft 2020-12 contract suite: **90 passed, no skips**.
- Runtime suite: **142 passed**, including **16 focused FR-2 tests**.
- Tracked diff whitespace check and checks of all five patched untracked
  Python files: passed.
- Source FR-2 disposable public-CLI qualification: passed against exact
  `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime 0.10.0/schema 19.
  Reverified 308 installed package files and 32 authority files against the
  exact source/export/wheel; wheel SHA-256
  `0cf6d7c1f73463195b274cae269fcb4221bf4a8c3744c9a8a3e026cc0b491963`.
  Evidence: `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr2-gate-qxtoyswk`.
  All-missing planning, A2/B2/B1 history, repeated-pin deduplication, mixed-catalog
  pagination, two-pass equality, current/historical/retired reads and unchanged
  ledger file metadata passed. Setup/direct reads: 19; planner reads: 118.

No package/resource layout changed; the earlier installed-installer and v1 package
qualification was not rerun for this patch and remains earlier evidence only.
No Spine checkout or operator ledger was modified. No item/facet-value authoring,
disclosure, reminder materialization, sends, commit, push, publication or external
re-review occurred. A focused external recheck still needs a fresh exact payload
approval; the original `needs_revision` verdict is not relabelled as a pass.
