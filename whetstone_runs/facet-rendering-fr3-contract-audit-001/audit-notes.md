# Change Intent

Perform one focused reviewer-only consistency audit of the FR-3 exact-0.10.0
initial-apply contract-fixture refresh committed as
`97e09b5db6bff382e1c69054a8db1f961c35a225`. This is the contract gate before
implementing the successor initial-apply executor, not a whole-installer audit
or a declaration of convergence/runtime qualification.

Spine baseline remains exact commit
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`, schema `19`.
No compatibility range, public schema change, runtime write permission, released
pack mutation, disclosure approval or domain-item behavior is introduced here.

# Expected Boundary

The new synthetic create/update fixtures derive from preserved 0.9.1 FR-1
examples but regenerate compatibility, manifest/plan/approval identities,
command IDs, exact request/response correlations and checkpoint/result digests.
The checked-in index pins new bytes and historical-source bytes independently.
Returned IDs/receipts remain synthetic, never actual Spine execution evidence.

Review these questions:

1. Do both flows consistently use the exact 0.10.0 inventory, 18-contract union
   and current plan identities, without stale command/approval correlations?
2. Does the refresh helper preserve the three receipt families and immutable
   post-observation facts while correctly updating request-bound provenance?
3. Do the independent oracle and eight new tests actually check all 11 write
   kinds, dependency-consuming slots, complete approvals, prepared/accepted
   contiguous prefixes and first-submission partial failure artifacts?
4. Could the refresh create a self-confirming fixture that hides a meaningful
   mismatch with the current read-only planner? Inspect its exact-plan parity
   test; production code is supplied only for that static comparison.
5. Are the claims correctly limited to contracts, with actual write transport,
   response/readback validation and filesystem durability still unimplemented?
6. Is excluding recovery/verification from this increment explicit and coherent,
   including deferral of the historical 0.9.1 verification evidence label to FR-4?

Only report concrete inconsistencies or material holes affecting this refresh
or the ability to begin FR-3 implementation. Do not require FR-3 runtime proof
as a condition of this pre-implementation contract audit. Proposed future write
commands are data in plans, not currently enabled execution authority.

# Specs To Check

The separately approved payload lists exact files and SHA-256 hashes. Normative
authority is `specs/facet-rendering-packs.md`, `specs/installer-artifacts-v2.md`
and `specs/implementation-plan.md`. AGENTS states the same gate. Readiness notes
are evidence summaries, not normative policy. The inventory and new fixture
index define the exact execution baseline and provenance.

The payload intentionally includes test source, the independent test oracle,
its manifest/hash helpers and unchanged read-only planning source. These are
needed to assess whether fixture generation and validation can mask defects;
this is a static review, not permission to execute code or inspect imports.

Unchanged schema closures and historical fixture bodies are omitted to bound
the payload. Do not claim independent inspection of those omitted files. Local
evidence: the official Draft 2020-12 suite passed all 98 tests without skips,
including the eight new tests, and all 142 runtime tests passed. Repository and
whitespace checks passed. On staging, the focused eight tests and verifier were
rerun successfully. Test success supports but does not decide this audit.
Historical-source hashes and deterministic regeneration are checked locally by
the new tests. No upstream test count substitutes for these installer checks.

# Out Of Scope

No Editor, source changes, tools, browsing, tests, shell execution or extra file
reads. Do not follow imports or paths as authority to expand the payload. If an
omission prevents a scoped conclusion, name the missing evidence and stop that
conclusion rather than treating assumed content as inspected.

No reopening unchanged v1 behavior, FR-2 observation/transport, historical
FR-1 contracts or whole-pack content. No successor recovery/verify implementation,
curated flight fields/templates, schema redesign, new error taxonomy, deployed
ledger access, direct SQL, Spine modifications, publication or deployment.
No runtime writes, disclosure grants, items, facets on items, reminders or sends.
Findings do not authorize patches, release, commit, push or compatibility changes.
