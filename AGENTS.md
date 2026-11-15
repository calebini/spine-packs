# Repository instructions

These instructions apply throughout this repository.

## Read first

Before changing pack behavior or format, read:

1. `specs/overview.md`
2. `specs/architecture.md`
3. `specs/compatibility.md`
4. `specs/pack-format.md`

Before changing `kinflow-starter` content, also read `specs/kinflow-starter.md`.
Before changing installer behavior or artifacts, also read
`specs/installer.md` and `specs/installer-artifacts.md`.
For proposed facet-aware rendering work, additionally read
`specs/facet-rendering-packs.md` and its implementation-plan sequence. This is
reviewed FR-1 contracts plus implemented FR-2 read-only planning. FR-3 initial
apply work is operator-authorized, starting with the exact-0.10.0 execution
fixture refresh and focused contract review before enabling the write boundary.
FR-4's exact-0.10.0 recovery/verify contract and fixture recheck has passed.
Read-only historical lineage observation and exact accepted-prefix comparison
are checkpointed in `3a5e560`. The operator subsequently authorized completing
uncertain-candidate admission/replay correlation and the next bounded internal
same-execution continuation increment, with synthetic public-command/durability
tests only. A subsequent operator-authorized slice added independent internal
read-only verification with synthetic public-command tests, no replay, and no
approval-file input. The FR-4 runtime repair recheck passed with zero findings
at `965326a`. The operator authorized CLI continuation/verify wiring with source,
target and destination collision checks, private publication and result/exit
handling, using synthetic public-command tests only. The operator subsequently
authorized FR-5 source and installed-package qualification: isolated exact Git
exports/builds, new disposable configuration-only ledgers, synthetic subjects and
protected test cursor configuration through public CLIs. No existing/operator
ledger, curated content change, external review, release, commit or push is
authorized by this qualification scope.
The explicitly authorized repaired-baseline listing gate may use
new disposable ledgers through public CLIs only, never an existing ledger.
For successor installer artifacts, also read `specs/installer-artifacts-v2.md`.
Its test-only oracle and v2 schemas do not expand current runtime authority.

The files in `specs/` are the normative source of truth. `README.md` is
orientation, pack-local READMEs describe pack status, and code must implement
rather than redefine the specs.

## Authority boundaries

- Spine is the sole authority for installed archetypes, notification profiles,
  bindings, receipts, and ownership.
- Treat packs as declarative, owner-neutral content. Never embed owner IDs,
  delivery targets, subjects, routes, credentials, or environment-specific
  facts in reusable pack content.
- Any future installer must interact with Spine only through Spine's existing
  public command surface. Direct database access is forbidden.
- Do not implement a ledger, scheduler, daemon, or competing runtime here.
- Do not make Spine runtime changes from this repository or modify a Spine
  checkout as part of spine-packs work.
- Do not mutate a released pack version. Add a new version and preserve the
  released artifact.

## Stage discipline

This is a draft-contract repository. The current scope is limited to
`spine.pack-manifest.v1`, the draft installer behavior and machine artifacts in
`specs/installer.md` and `specs/installer-artifacts.md`, and the
medical-appointment, lesson,
game-or-competition, flight, birthday, Education, Social, Travel, and Renewals
and administration, Health, and Home, vehicle, and logistics vertical slices
plus the General commitments vertical slice specified for `kinflow-starter`
draft 10 (compatibility-only successor to draft 9) and its approved unchanged-content
stable release `1.0.0`. Preserve the exact released bytes and all draft artifacts;
future content changes require a new version. The schema-15 alignment
supports the exact Spine `0.5.0` / schema `15` commit recorded in the installer
specs alongside `0.3.0` / `12`; it does not authorize broader runtime ranges.
The bounded 0.6.0 compatibility update additionally admits only Spine commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, runtime `0.6.0` / schema `15`,
and compatibility-only `kinflow-starter 1.0.1-draft.1`. Release finalization
materializes stable `1.0.1` with unchanged definitions and compatibility from
that draft; preserve both files. Installer candidate `0.3.0` and stable pack
`1.0.1` require exact-commit qualification and separate publication approval;
previous publication approval does not carry over.
Do not broaden the schema or pack semantics without matching normative spec,
fixture, and contract-test changes. The authorized runtime scope is the bounded
read-only `plan`, non-mutating apply preflight, Slice 3 initial approved
`apply` with durable checkpointing, and Slice 4 same-execution continuation and
bounded uncertain-response recovery, and Slice 5 non-mutating `verify` in
`src/spine_packs/`, described in
`specs/architecture.md`. Slice 6 disposable local integration qualification is
also authorized: the test harness may initialize a new temporary ledger and
bootstrap synthetic subjects through Spine's public administrative CLIs, then
exercise the installer with isolated synthetic manifests and exact approvals.
It MUST NOT accept an existing ledger or change a Spine checkout. Operator
installations still require a separately supplied target, released pack, and
exact approval. Slice 6 also authorizes local wheel/sdist preparation and
clean-install qualification for GitHub Releases as specified in
`specs/architecture.md`; publication requires the gates in `docs/releases.md`.
Do not add broader recovery, remote
transport, or speculative service/adapter/model directories
without separate review and authorization. Planning must retain its strict
read-command allowlist. V1 apply may use only its six reviewed write commands;
the separate FR-3 v2 apply adapter may use only the 11 configuration writes
in the exact 0.10.0 inventory.
The separately authorized AL-2 alignment also admits the identical reviewed
12-read/11-write inventory at exact Spine 0.12.0/schema 20 below. It adds no
commands; all v1 and qualified 0.10.0 capabilities remain intact.
Mark unresolved design details explicitly instead of silently choosing them.

When the repository advances, add only the smallest structure required by real
artifacts. Machine-readable public agreements belong in `contracts/`; runtime
implementation belongs in an explicitly reviewed package layout; explanatory
material belongs in `docs/` only when the README is insufficient.

## Change checks

The qualified facet/rendering baseline remains exact Spine commit
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122` (`0.10.0`, schema `19`). AL-2 separately
adds exact `3e65ef0de9e73b62047a0f6328731db08ca91023` (`0.12.0`, schema `20`)
runtime routing under the scope below; it is not new-baseline qualification. The original
`01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7` listing finding and audit are historical
evidence and MUST NOT be rewritten. Existing
runtime allowlists, v1 contracts and pack artifacts remain unchanged. Do not
provision destination disclosure, create items, materialize reminders or send
notifications as part of configuration installation. The staged bounded audit
requires explicit payload approval before any external reviewer invocation.

FR-2 explicitly authorizes the separate v2 read-only planner against this exact
pin, including `facet_schema.revision.show` and new disposable configuration-only
qualification via public CLIs. Never probe candidate roots or suppress missing
referenced evidence. FR-3's focused contract review and minor patch are complete.
Initial-only v2 apply now integrates fresh preflight, public readback, the separate
11-write adapter and durable prepared/accepted checkpoints. The FR-2 planning
adapter remains read-only. The runtime audit's repair findings are closed by a
passing focused recheck recorded in `specs/implementation-plan.md`. FR-5's exact
installed-package technical qualification has now passed locally; see
`docs/fr5-qualification.md` for exact evidence and release limitations. Its new
qualification tooling received a bounded review with three major and three
minor findings. The operator authorized all six repairs plus required checks
and affected source/installed qualification reruns. Those local checks and the
fresh full matrix passed. The approved focused recheck closed four findings and
reopened parent harness identity and explicit on-disk checkpoint completeness.
The operator authorized those two narrow follow-ups and focused checks. The
approved 16-file recheck passed at `6ebc1cc` with zero findings, closing FR-5 on
the recorded baseline. The operator then requested compatibility alignment;
AL-0 candidate inspection of exact `3e65ef0de9e73b62047a0f6328731db08ca91023`
(0.12.0/schema 20) is documented in `docs/spine-0.12.0-alignment.md`. The operator
then selected that exact pin and authorized the AL-1 contract/fixture slice in
`specs/spine-0.12.0-alignment.md`. It adds singleton manifest/environment/label
variants and an additive pinned closure without changing runtime routing,
historical fixture bytes or pack artifacts. Preserve existing qualified
capabilities and immutable evidence. Bounded contract review must precede AL-2
runtime alignment; AL-3 qualification remains separate. Further external review still requires separate
exact-payload approval. The approved 14-file AL-1 audit returned two major and
three minor findings. The operator authorized the four agreed test/context
repairs and clarification of the remaining major while preserving existing
known-immutable-revision failure behavior. Local repair checks do not close
the external review gate or authorize AL-2. Preserve that original payload and
verdict; any focused recheck needs its own exact-payload approval.
The separately approved 14-file AL-1 focused recheck subsequently returned
`pass_with_minor_clarification`, with no major findings and preserved boundaries.
The operator authorized its remaining minor test gap: assert invalid captured
evidence coverage/mismatch for both create and update flows. That assertion is
now added; see the implementation plan for checks. That follow-up did not itself
authorize AL-2. The operator subsequently explicitly authorized AL-2 runtime
alignment: bind each operation to the validated manifest's exact baseline and
route plan/apply/continuation/verify through that reviewed closure, with synthetic
public-command tests and independent contract checks. Preserve all error
ownership, budgets, strict read/write allowlists, cross-baseline evidence refusal,
historical fixtures, v1 routing and released pack bytes. AL-2 may run the required
old-baseline package regression on new disposable configuration ledgers only.
AL-3 new-baseline public-CLI/source/wheel qualification, external review, commit,
push and release remain separately authorized work. The separately approved
20-file AL-2 runtime audit returned two majors and two minors (`needs_revision`,
boundary not preserved). The operator authorized manual repair of initial-apply
transport-target equality, ordinary read-failure envelope/exit validation, the
v1-decoded profile regression/reference-chain evidence, and the package
provenance link, plus focused and required checks. Preserve the original payload
and verdict; local repair success does not close the external findings or
authorize a reviewer rerun or AL-3. No commit or push is part of this repair.
The separately approved 20-file focused AL-2 repair recheck returned only
consistency-02, for an empty invalid_request/request preflight message falling
through to a handler rejection. The other three findings were not reopened.
The same already-authorized failure-validation repair now rejects malformed
request-preflight signatures before handler fallback, with regressions for both
baselines. Preserve both external verdicts and approved payloads; local follow-up
checks do not authorize another reviewer call, AL-3, commit or push.
The separately approved final ten-file consistency-02 recheck passed with zero
findings and boundary_preserved=true. Together with the prior focused recheck,
this closes the AL-2 runtime repair review gate. Preserve all original reports
and approved payloads. The operator subsequently authorized the local AL-2
checkpoint commit only; AL-3 exact-0.12.0 source/installed qualification, push,
deployment and publication remain separate work.
After checkpoint `8082b5d`, the operator explicitly authorized AL-3 source and
installed-package qualification of exact Spine
`3e65ef0de9e73b62047a0f6328731db08ca91023` (0.12.0/schema 20). This permits
the bounded qualification harness updates, isolated exact Git exports/builds,
locally provisioned and recorded dependency wheels, and new disposable
configuration-only ledgers through public CLIs. Retain the 0.10.0 and all v1
source/installed regression gates. Bind every result to the parent-selected
baseline, installation mode and attested upstream paths. Freeze source/harness
inputs throughout each matrix. No Spine checkout edits, existing/operator
ledger, runtime expansion, curated content, disclosure, items, facet values,
reminder materialization, sends, deployment, publication, commit or push is
part of AL-3. Its external review still requires fresh exact-payload approval.
AL-3 technical qualification subsequently passed with 40 source/installed
scenarios, four nine-check read gates, all 11 replay writes on both v2 pins in
both modes, matching candidate archives and unchanged source inputs. See
`docs/al3-qualification.md` for exact evidence and limits. No runtime repair was
needed. The bounded tooling review and final release qualification remain
separate; no external review, commit, push or publication is authorized by this
local pass.
FR-4 contract and
fixture work is authorized; its focused contract recheck passed with zero
findings. The read-only foundation is committed; the operator subsequently
authorized the admission/replay and internal continuation increments above.
The FR-2 adapter remains read-only; internal continuation reuses only the FR-3
11-write adapter and requires fresh admission plus durable checkpoints. Internal
verification is separately authorized and must use only the FR-2 public read
adapter, correlate captured responses without granting approval, and never
invoke apply, recovery, receipt repair or disclosure operations. The
operator-authorized CLI slice exposes these reviewed services with the existing
flags and v2 artifacts, preserving v1 dispatch. Supplied source/result path
aliases, including hard links to protected files, must fail before those paths
are opened as artifacts. No new ledger or package qualification
was part of the CLI increment. FR-5 qualification is now separately authorized
as described above and in `specs/architecture.md`. Preserve the 0.9.1 inventory,
fixtures and earlier investigation as historical evidence.

For documentation, contract, and planner changes, run:

```sh
python3 scripts/verify_repo.py
python3 -m unittest discover -s tests/contract -p 'test_*.py'
python3 -m unittest discover -s tests/runtime -p 'test_*.py'
git diff --check
```

For packaging/resource changes, also run `scripts/qualify_package.py` with
isolated public Spine CLI paths as documented in `docs/releases.md`. Never
substitute an existing operator ledger or publish assets as part of testing.

If a future change introduces executable behavior or a contract, add focused
tests appropriate to that behavior. The repository verifier is a handoff and
structure check, not a substitute for behavior or contract tests.
