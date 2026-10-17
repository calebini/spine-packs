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

## Initial executor increment

The pure helpers were committed as `fc30fab`. This increment wires initial-only
v2 `apply` through a separate configuration write adapter, complete fresh
preflight, public readback and durable checkpoint publication. The component
scaffold guidance keeps this in the existing package and test directories.

The external CLI shape remains:

```sh
spine-packs apply --manifest MANIFEST --plan PLAN --approval APPROVAL --checkpoint CHECKPOINT --output RESULT
```

Manifest-v2 inputs select the exact-0.10.0 path. Complete approval, input digests,
known-ID requests and output destinations are checked before target access.
Fresh two-pass observation must reproduce the saved plan exactly. Later bindings
receive immediate list rechecks, and facet binding requests retain exact CAS.

The write adapter accepts only the 11 inventory commands, preserves stdout
without rewriting JSON and uses the existing bounded public subprocess. Each
response is checked against a fresh current show/list result before acceptance.
The durable writer validates v2 artifacts while preserving its v1 default. Its
file fsync, atomic link/replace and directory fsync complete before submission
or use of producer outputs. Readback/recheck operations have their own existing
global observation budgets; writes retain 30 seconds and 16 MiB each.

After submission, any uncertain/rejected/malformed response or readback failure
produces a partial result embedding the prepared checkpoint and exact request.
There is no automatic retry. A checkpoint publication failure stops without
submitting a consumer; result publication failure can leave the durable
checkpoint as the only completed artifact. No-action plans publish an empty
complete checkpoint. V2 continuation and verify still fail before target access.

Focused tests use synthetic wire responses and projections, the existing full
FR-2 read transcript, temporary artifact files and a synthetic CLI subprocess.
The subprocess's target is a new empty test file used only for path checks;
it is not opened as a Spine ledger. No real Spine command or ledger was used.
The read transcript independently exercises the complete preflight; orchestration
fault tests substitute the preflight result so every write boundary can be
isolated. The official validator additionally checks generated result artifacts
against the independent test oracle. These are not installed-Spine qualification.

Verification results:

- 22 focused apply/transport tests passed in the isolated development environment,
  including independent Draft 2020-12 validation of generated result artifacts.
- Complete required system-Python runtime suite: 175 tests passed, no skips.
- Official contract suite: 99 tests passed, no skips.
- Required system-Python contract suite: 99 ran, with 34 skips for the unavailable
  development validator; the isolated official suite above covers that gate.
- Repository verifier: 171 required files passed; whitespace checks passed.
- Historical and refreshed flight fixture hashes, contracts and released packs
  are unchanged. The exact Spine commit remains available locally.

Draft and blocked inputs retain existing installer exit categories before target
access. Public revision numbers and full rendering records must agree with
fresh readback. Publication faults were injected at every prepared/accepted
boundary and at file fsync, atomic link/replace and directory fsync. A synthetic
subprocess exercises the actual adapter's CLI arguments and exact stdout capture.

The following review closeout supersedes this increment's pre-review status;
its recorded test results above remain historical candidate evidence.

## Runtime review and repair closure

Current status is owned by `specs/implementation-plan.md`, under FR-3 runtime
review and repair closure. Initial executor commit: `540e113`; the repairs remain
uncommitted in `facet_execution.py`, `facet_apply_transport.py` and
`tests/runtime/test_facet_apply.py`.

The original bounded audit found one major and one minor. Contextual facet
failure validation now rejects malformed fields and wrong-family codes as
environment failures without exposing private messages. The first immutable-ID
repair was incomplete: catalog revision responses lack `changed`, and replayed
publication responses may set it false. The final repair therefore follows
declared revision outputs and non-noop effects, rejecting reuse of the approved
preimage revision ID independently of that flag. Metadata-only writes and
legitimate no-op checks retain their semantics.

Focused tests exercise both catalog revise commands and both publication
families, including replay, accepted-prefix preservation, unresolved-request
retention and partial termination before consumers. Positive cases retain
distinct replayed revisions and metadata-only revision preservation.

Recorded repair verification in the existing isolated development environment:

- 27 focused apply/transport tests passed.
- Full runtime suite: 180 passed (83.820 seconds).
- Official Draft 2020-12 contract suite: 99 passed, no skips (5.532 seconds).
- Repository verifier: 171 required files passed; `git diff --check` passed.

The bookkeeping return pass independently reran the local gates: 27 focused
tests passed, all 180 runtime tests passed (90.433 seconds), all 99 official
contract tests passed without skips, and repository/whitespace checks passed.
The required system-Python contract command also ran 99 tests with 34 skips;
the isolated official run covers those development-validator checks. No package
or real-Spine qualification was run.

The independently authorized second focused recheck returned `pass`,
`boundary_preserved=true`, zero findings and recommended action `none`. See
[the retained report](../whetstone_runs/facet-rendering-fr3-runtime-recheck-002/change_audit/change_audit_report.md).
Its prepared inputs and authorization bind 13 source/context files plus notes.
All 13 hashes and the notes were checked against the current files on return to
this thread; no subsequent repair changes were found. The persisted manifest,
brief and feedback/report bindings agree. No reviewer was rerun for bookkeeping.
The first audit/recheck and their follow-ups remain unchanged, including their
historical pending-status wording.

This closes the reviewed repair findings, not qualification against installed
Spine. The review is focused, not a fresh exhaustive runtime audit or convergence
claim. No Spine commands, existing/operator/staging ledger access, deployment,
commit, push or publication is included in this bookkeeping step.

## Remaining qualification and next scope

There is no separately specified FR-3 installed-package completion gate.
The remaining real-Spine initial-apply and package proof belongs to **FR-5**:

1. Attest exact Spine commit `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`
   through isolated export/build, wheel and installed package bytes; runtime
   0.10.0/schema 19 alone does not establish source provenance.
2. Exercise source-tree and clean-installed installer plan/apply/replay/verify
   through public CLIs on newly allocated disposable ledgers with synthetic
   configuration, synthetic owner and separately authorized protected cursor
   setup. No existing-ledger argument, item authoring, disclosure or delivery.
3. Retain target-bound evidence and pass all supported v1 baseline package
   regressions. Existing FR-2 read-only gates and older package runs do not
   qualify the repaired FR-3 initial-apply path.

FR-4 is next in the existing implementation sequence. Its recovery/verify scope
and exact-0.10.0 verification-label/fixture refresh must be authorized before
implementation; full FR-5 replay/verify qualification cannot be completed by the
current initial-only executor. Neither FR-4 nor FR-5 starts in this bookkeeping
task. Packaging/release finalization, staging and operator installation remain
separate gates and approvals. Curated flight/disclosure choices remain FR-6.
