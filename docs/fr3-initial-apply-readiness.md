# FR-3 initial-apply readiness

Date: 2026-10-17. The operator requested committing the clean FR-2 re-audit and
beginning implementation. Audit evidence was committed as `16e5f4a`; nothing was
pushed. Normative authority remains `specs/implementation-plan.md` and
`specs/installer-artifacts-v2.md`.

## This increment

FR-3 starts at the required exact-baseline execution-contract refresh. The exact
Spine commit `8f3c50b6fd1b4aa534e50925b7417a7a80d19122` exists locally. All 20
`upstream/` schema inputs in `installer-spine-0.10.0-inventory.json` were compared
with `git show <exact-pin>:<path>` and match their recorded SHA-256 hashes. No
HEAD substitution, Spine checkout modification, build, ledger or Spine command
execution was needed for this synthetic contract increment.

The new fixture index pins two separate initial-only flight flows for runtime
0.10.0/schema 19, plus the unchanged historical 0.9.1 sources. An independent
test-only refresh helper regenerates manifest/plan/approval identities, all
command IDs, submitted requests, correlated responses and checkpoint/results.
Returned IDs and receipts are synthetic; they are not captured public-CLI proof.
The current read-only planner must reproduce the independent plans exactly.

Eight focused contract tests cover all 11 configuration write kinds, all
producer-dependent request slots, prepared and accepted prefixes, first-action
and later partial failures, stale/incomplete approvals, exact version/contract
requirements and malformed receipt/owner/root/byte evidence for every command.
Official Draft 2020-12 validation uses the exact 0.10.0 offline public closure.
The old fixtures and their recovery/verification claims are preserved unchanged.

This does **not** prove filesystem durability, real response validation, writes,
continuation, verification or package qualification. No runtime code, schema,
released pack or existing compatibility allowlist changes in this increment.
The component-scaffold guidance keeps the work in the existing contracts/tests
layout without introducing a new runtime architecture.

## Verification

- Repository verifier: passed, 166 required files.
- Focused FR-3 contract suite: eight tests passed without skips.
- Complete official Draft 2020-12 contract suite: 98 tests passed without skips.
- Required system-Python contract command: 98 tests ran, 33 skipped because
  development `jsonschema` is unavailable there; the complete gate above used
  `/private/tmp/spine-packs-fr2-0100.WbU0lE/env/bin/python`.
- Complete runtime suite: 142 tests passed without skips.
- `git diff --check` and explicit new-file whitespace checks: passed.

Reproduce the focused gate with a development interpreter providing `jsonschema`:

```sh
python -m unittest discover -s tests/contract -p 'test_fr3_artifact_contract.py'
```

## Next gate and implementation

1. The approved 15-file focused contract review completed with one minor
   response-correlation finding and no blockers or majors. The authorized local
   patch adds exact facet-key/schema-revision response checks and four negative
   cases. See [patch follow-up](../whetstone_runs/facet-rendering-fr3-contract-audit-001/patch-followup.md)
   for post-patch verification. The patch has not been externally re-audited.
2. Implement command-specific serializers and response/readback validators.
   Preserve catalog, facet and rendering receipt distinctions; never treat a
   response output or planned producer as acceptance by itself.
3. Implement initial-only apply orchestration with exact approval and fresh
   preflight, an explicit 11-write allowlist, prepared-before-submit and
   accepted-before-consumer durable checkpoints, binding guards and partial
   failure results. Keep the read-only planner transport write-disabled.
4. Add filesystem/transport fault-injection tests at every durability boundary,
   including rendering size checks after resolving real IDs. Preserve all v1
   behavior and reject successor continuation/verify until FR-4 authorization.

No product decision is needed to refresh these synthetic fixtures. Curated
flight fields, templates and disclosure choices remain FR-6 decisions. The
historical verification label naming 0.9.1 is explicitly not refreshed here:
FR-4 must settle its 0.10.0 successor before implementing verification.

## Pure execution increment

Commit `b2f224e` records the bounded audit and minor correlation patch. The next
increment adds one runtime module, `src/spine_packs/facet_execution.py`, and its
focused tests in the existing package/test layout. No service or adapter tree
is introduced; this follows the component-scaffold guidance.

The pure context reconstructs the exact saved plan from manifest and saved
observation, checks complete approval, constructs only the next approved request,
and validates every earlier evidence row before consuming returned IDs. It
preserves original response text (minus one terminal CLI newline), distinguishes
all three receipt families, and compares response/target/owner/revision/hash and
semantic readback evidence. Metadata updates cannot silently advance a revision.
Resolved rendering size is checked after actual producer IDs become available.

Focused tests reproduce all saved independent requests/evidence across all 11
write kinds, reject malformed and resealed inconsistent inputs, and test the
exact 8,192-byte rendering boundary versus longer schema IDs. Public JSON integer
parsing is checked separately from command-specific field schemas, which still
reject inappropriate types. These tests are synthetic and execute no Spine CLI.

Verification results for this increment:

- 11 focused execution tests passed; complete runtime suite: 153 passed.
- Official Draft 2020-12 contract suite: 99 passed without skips.
- Required system-Python contract suite: 99 ran with 34 development-validator
  skips; the complete official suite above supplies the full gate.
- Repository verifier: 168 required files passed; whitespace checks passed.
- Historical/refreshed fixture bytes, contracts, released packs, CLI dispatch
  and write-disabled transport are unchanged.

The exact Spine commit remains available locally; no Spine execution, build,
ledger access or checkout change was needed for this pure-helper increment.

No CLI dispatch, write transport, fresh observation/readback collection, durable
checkpoint publisher or terminal apply-result writer is added here. Supplied
evidence proves consistency, not authenticity or durable acceptance; the future
executor must obtain fresh public evidence and persist a producer before using
its outputs. The next bound implements that orchestration and tests actual
filesystem/transport failure boundaries. Successor recovery/verify remain out
of scope. Historical fixtures, released packs and existing v1 behavior remain
unchanged. No package/disposable-ledger qualification or release claim is made.
