# Exact Spine 0.12.0 compatibility alignment

Status: AL-1 contract review and its final minor repair are complete. AL-2 runtime
alignment, synthetic checks and bounded runtime repair review are complete;
the final consistency-02 recheck passed with zero findings on 2026-11-15.
AL-3 source/installed technical qualification passed on 2026-11-15; its bounded
tooling review remains pending. This document extends the v2 successor
specifications only; it does not qualify a deployment or change any v1 agreement
or reusable pack.

## Baseline and preservation

The operator selected exactly Spine commit
`3e65ef0de9e73b62047a0f6328731db08ca91023`, runtime `0.12.0`, ledger schema `20`.
Do not substitute HEAD or infer a range. Selection is not evidence of an installed
staging package. `system.info` reports runtime/schema/contracts/ledger identity,
not a Git commit; source and installed provenance still require AL-3 qualification.

Retain the qualified `0.10.0` / `19` path at exact
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, the historical `0.9.1` evidence,
every v1 capability, and all released/draft pack bytes. Earlier review and
qualification evidence MUST NOT be relabelled or overwritten. Retirement is
outside this additive alignment. The AL-0 comparison remains historical
candidate inspection; subsequent operator selection does not turn it into
runtime or staging qualification.

## Manifest and environment variants

Keep `spine.pack-manifest.v2` and the seven installer-artifact v2 identifiers,
digest domains, limits, typed references, action ordering and comparison rules.
The artifact families have additive exact variants, as in FR-2/FR-4; no operator
artifact migration or release-version assignment is introduced.

The structural manifest schema permits exactly one of `["0.9.1"]`, `["0.10.0"]`
or `["0.12.0"]`. The first is historical decoding only. Mixed lists, ranges,
patch-version inference and unknown runtimes MUST fail. New 0.12.0 content needs
its own recomputed manifest digest and eventual successor immutable pack release;
the alignment MUST NOT modify a reusable pack artifact. Content semantics and
the seven exact content-contract identifiers are unchanged.

The shared environment is closed and admits only these paired encodings:

| Runtime | Implemented schema | Current schema | Verification receipt label |
| --- | --- | --- | --- |
| 0.9.1 (historical) | 19 | 19 | `captured_responses_only_spine_0.9.1` |
| 0.10.0 | 19 | 19 | `captured_responses_only_spine_0.10.0` |
| 0.12.0 | 20 | 20 | `captured_responses_only_spine_0.12.0` |

All variants require the actual public `ledger_instance_id` and sorted unique
advertised contracts. Reject mismatched current/implemented schemas structurally,
including schema 19 on 0.12.0 or schema 20 on 0.10.0. Verification labels MUST be
paired structurally with the environment, and mean captured responses only.
No receipt lookup, delivery, rendering success or disclosure grant is asserted.

Manifest compatibility MUST match the saved plan runtime singleton. Plans bind
the runtime, both schema versions, advertised contracts, ledger-instance ID,
existing target binding and exact manifest digest. Approval/checkpoint/result
correlation remains through the complete plan digest and execution identity.
Changing the baseline therefore requires a new plan and exact approval. Do not
relabel an old approval, checkpoint, request, response or verification artifact.
An unchanged execution-contract union does not make old source evidence reusable.

## Runtime baseline selection

`facet_baselines` holds immutable configurations for only the exact 0.10.0/19
and 0.12.0/20 pins. Resolve the validated manifest singleton before the first
catalog read; do not select a baseline from the observed runtime, an environment
variable, a version range, or a mutable global. Existing direct helper calls may
default to 0.10.0; installer operations explicitly carry their selected runtime.
Bind each concrete public transport once and reject a later attempt to change
its baseline. Independent transports may use different baselines concurrently.

Use that same configuration for both observation passes, exact historical
lookups, semantic projections, saved-plan reconstruction, initial apply readback,
continuation/candidate/replay checks, captured response validation and the
verification receipt label. Shared command and execution-contract maps remain
closed and equal to both reviewed inventories. Public schema entry points stay
baseline-specific even though their current definitions are equivalent.

All saved artifacts bind the manifest and exact environment through the plan
digest; choosing a new baseline requires fresh planning and approval. Fresh
preflight must match that saved environment before initial writes, continuation
publication/replay or completed verification. Invalid cross-baseline approval or
checkpoint input fails before constructing a CLI transport. A structurally valid
result from another plan follows the preserved invalid-coverage rule below.

Initial apply MUST also compare the supplied transport's complete target with
the approved request target before observing or writing. Rebuilding a plan from
the saved request does not establish that equality. A mismatch is
`stale_plan_or_target_mismatch`, returned under initial preflight as `not_applied`,
with no checkpoint publication or configuration writes. Continuation and verify
retain their existing target checks.

### Ordinary public read failures

Before classifying a non-revision read failure, validate its applicable existing
closed failure envelope and actual CLI exit. Facet catalog/binding reads use
`public_0138`; profile show/list use `public_0139` in the selected public entry
point. Families without a contextual failure schema in the reviewed inventory
use the existing shared `commandFailure` compatibility envelope. This adds no
schema or command authority. Public failure schemas alone do not validate exits.

Use the exact `commands/cli.py` `EXIT_BY_ERROR` agreement shared by both reviewed
pins, plus its final `runtime_failure` fallback at exit 1. Valid handler
rejections retain installer `spine_command_rejection` / 8; handler environment
or runtime failures retain `transport_or_environment_failure` / 11. Missing
referenced rows are rejections, never absence evidence. Missing/extra fields,
unknown codes, wrong command correlation or unsupported exit pairings fail as
environment failures, without exposing raw output. In particular, `ok=false`
with exit zero cannot become an ordinary rejection.

Preserve the separately recognized closed common-preflight cases and their
owning rejection category: `invalid_request` for `db`/`input` at CLI exit 3 or
`request` at exit 2; `environment_failure` for `runtime_contracts`/`ledger` at
exit 7. These are not handler failures. A malformed preflight must not fall
through as a handler rejection; `db`/`input` with exit 2 is invalid. The dedicated
`facet_schema.revision.show` schema/field/exit mapping below is unchanged.
An `invalid_request` / `request` signature that fails the closed preflight check,
including an empty message at exit 2, MUST fail as installer environment failure
before handler fallback. The common handler envelope's permissive message shape
does not waive that preflight rule. A valid counterpart retains rejection / 8.

## Exact command agreement and offline closure

`contracts/installer-spine-0.12.0-inventory.json` pins the exact commit,
runtime/schema pair, selected command maps, per-command registry prerequisites,
source hashes and revision-readback package authority. It retains exactly the
0.10.0 inventory's 23 commands: 12 reads and 11 configuration writes, with the
same 18 execution contracts. The additional people/recurring-task commands in
Spine are outside the installer boundary. Contract presence grants no command
authority. Preserve all observation budgets and tighter per-command ceilings.

`spine-readback-0.12.0.schema.json` provides an additive local entry point. Every
definition references its identical 0.10.0 sibling definition, including that
sibling's complete 0.9.1/transitive closure. Never resolve schemas from the
network, import Spine, or omit a branch because fixtures do not exercise it.
The source inventory's schema pointers and hashes are unchanged because the
selected source schemas are byte-identical. The changed registry hash is pinned
separately; matching source schemas alone are not runtime equivalence evidence.

AL-2 MUST choose the matching reviewed baseline before catalog interpretation
and route all plan/apply/continuation/verify public request/response validation
through its exact closure. Missing advertised prerequisites fail before planning.
Environment/target equality MUST be rechecked on initial apply, continuation and
verification. Mixed-baseline approvals or source evidence MUST NOT reach writes.
An otherwise valid result from another plan yields invalid captured-response
coverage and mismatch after successful fresh verification reads; malformed outer
artifacts fail before observation. Existing error ownership and exit codes stay.

### Preserved verification failure precedence

The invalid-coverage rule applies to invalid embedded request/response evidence
or plan/execution correlation. After valid outer artifact input and successful
fresh observation, those failures produce `response_evidence=invalid` and
`state=mismatch`. An absent result on a plan with writes instead produces
`response_evidence=missing` and `state=mismatch`; absence is not invalid evidence.

Preserve the separate known-immutable-revision check: if a fresh row reuses a
revision ID known from the saved plan or validated captured evidence with a
different root, decoder or immutable body, verification MUST abort under
`transport_or_environment_failure` (installer exit 11), without publishing a
verification artifact. Independently schema-valid rows and self-consistent fresh
hashes do not waive combined immutable lineage validation. Do not catch that
contradiction and convert it to invalid coverage/mismatch. Mutable profile
metadata remains outside immutable revision content. Independently corrupt or
unavailable fresh observation also aborts under its owning failure, even when a
supplied result is already stale. These are inherited behaviors, not a new
runtime rule introduced by compatibility alignment.

The inherited contract assertion is
`tests/contract/test_fr4_artifact_contract.py:FR4ArtifactTests.test_verification_rejects_corrupt_known_immutable_definition_not_a_missing_object`.
The corresponding executable-runtime assertion is
`tests/runtime/test_facet_verification.py:VerificationTests.test_known_immutable_body_contradiction_is_environment_failure_not_mismatch`.
The AL-1 gate preserves this exception for both new synthetic flows and separately
checks that otherwise-valid same-plan artifacts with invalid embedded correlation
produce invalid coverage/mismatch. No result claims receipt authenticity.

### Preserved exact-revision readback failures

Historical facet readback remains revision-addressed and deduplicated within
each observation pass under the existing global budgets. Missing/corrupt/capacity
evidence retains the exact failure mapping from
`installer-artifacts-v2.md`'s "FR-2 exact revision lookup":

| Public failure code | Public field | Spine CLI exit | Installer category / exit |
| --- | --- | --- | --- |
| `referenced_row_not_found` | `facet_schema_revision_id` | 4 | `spine_command_rejection` / 8 |
| `environment_failure` (corrupt/unsupported evidence) | `facets` | 7 | `transport_or_environment_failure` / 11 |
| `environment_failure` (capacity exhausted) | `capacity` | 7 | `transport_or_environment_failure` / 11 |
| `invalid_request` (handler request) | `facet_schema_revision_id` | 2 | `spine_command_rejection` / 8 |

All rejected referenced reads abort observation; none supplies absence evidence
or a missing desired-object classification. Recognized closed preflight failures
retain their own contracts and permitted exit pairings. Malformed handler or
preflight envelopes, unknown failure codes/fields and unsupported exit pairings
are `transport_or_environment_failure` / 11. Never copy a Spine CLI exit directly
to the installer exit or disclose raw public error output. Existing observation
and revision-readback ceilings remain unchanged.

The exact existing assertions are
`tests/runtime/test_facet_planning.py:FacetPlanningTests.test_missing_corrupt_capacity_invalid_and_preflight_never_absence`
and `test_malformed_handler_and_preflight_failures_are_environment_failures` in
that same class. They cover the mapping, closed preflight cases, malformed
envelopes/exit combinations and secret-safe errors on the existing supported
baseline; they are preservation evidence, not 0.12.0 CLI qualification.
No key-based root inference,
candidate probing or missing-evidence suppression is introduced. Recovery still
admits only the exact accepted prefix or that prefix plus the single durable
unresolved request. Replay, durability and independent read-only verification
requirements remain unchanged.

## Fixtures and gates

`contracts/installer-alignment-fixture-manifest.v2.json` pins immutable historical
inputs and the new `tests/fixtures/installer-v2/alignment-0.12.0.json`. The latter
is a compact test-only derivation fixture: two frozen 0.10.0 source flows plus
expected new artifact, observation, request and response digests. It is not a
new public artifact family or an operator artifact conversion mechanism.
`tests/contract/alignment_fixture_support.py` deterministically constructs the
synthetic new create/update artifacts through independent test oracles, without
Spine or installer-runtime imports. Synthetic returned IDs and semantic bodies
stay fixed; manifest/plan/approval hashes, command IDs, contextual receipt hashes
and checkpoints are regenerated. They are not actual CLI captures.

The gate MUST validate both complete flows and all 36 prepared/response-loss/
accepted boundaries across the 11 writes. Negative vectors cover wrong runtime/
schema pairs, unavailable contracts, mixed manifest variants, stale plan/approval,
old-baseline checkpoints/partial results/replay/results, changed replay requests,
prefix gaps, fresh environment/preimage drift, wrong replay roots, current heads,
facet pins, missing evidence and receipt labels. Check every schema branch's
offline references, official Draft 2020-12 validity, unchanged historical bytes,
and digest/command-ID derivation. Existing full contract/runtime regressions and
old-baseline package/resource qualification remain mandatory.
The 27 indexed negative vectors include distinct invalid same-plan captured
evidence and known immutable fresh-readback contradiction cases. Valid unrelated
drift MUST pass observation/fingerprint and lineage validation before failing
at continuation comparison. Rendering candidates MUST use the context-selected
public schema entry point; tests must exercise both 0.12.0 and 0.10.0 contexts.

AL-1 does not run Spine 0.12.0. Following its approved bounded contract review
and final minor repair, the operator authorized AL-2 exact routing and synthetic
regressions while preserving 0.10.0 and all v1 paths. AL-2's runtime outputs must
also pass independent official schema and semantic-oracle checks. AL-3
independently qualifies source and installed-package public
CLIs on newly allocated disposable schema-20 configuration ledgers, including
all 11 response-loss replays and complete-checkpoint drift refusal. Spine's new
`jsonschema>=4.23` dependency closure MUST be provisioned and recorded for isolated
qualification; Spine Packs retains zero runtime dependencies. No full new-baseline
support claim precedes those gates. FR-6 content and release work follows.

No existing ledger, SQL/internal API, checkout mutation, migration of operator
state, item/facet-value authoring, disclosure management, reminder materialization,
notification send, deployment, publication, commit or push belongs to AL-1 or
AL-2. AL-2's mandatory package regression may rebuild already supported upstream
pins and use only new disposable ledgers; it is not new-baseline qualification.
External Whetstone review needs approval of its exact staged payload.

## AL-3 qualification execution

The operator authorized this stage after AL-2 checkpoint `8082b5d`. Extend only
the qualification tooling; installer runtime behavior and compatibility remain
the reviewed AL-2 implementation. `qualify_fr5.py --successor-runtime 0.12.0`
selects the exact schema-20 pin above while retaining the 0.10.0 regression path
and all three v1 baselines. The omitted option retains the historical 0.10.0
matrix. No automatic target discovery, range or HEAD substitution is permitted.

For each successor baseline, run the complete read-only historical/mixed-catalog
gate plus all four named v2 scenarios from source and installed package. Require
all 11 actual response-loss replays, exact request/returned-ID correlation,
durable checkpoint completeness and completed-checkpoint drift refusal. The
parent MUST reject incomplete/skipped/focused suites, another baseline's
runtime/schema/commit, wrong upstream CLI paths, wrong installation mode or
source/schema-resource leakage. Child-supplied success flags alone are insufficient.

Build and attest every packaged upstream file against its exact Git object,
export, wheel and installed bytes, with the complete Python closure. Also check
the selected pinned contract authority. Record a source/harness/input snapshot
before the full matrix and require equality afterward. All passes must use the
same candidate wheel/sdist bytes across the v1 regression matrix; installed v2
uses the extracted sdist harness with the clean wheel's code/resources.

Spine 0.12.0 requires its declared `jsonschema>=4.23` dependency closure. Provision
that wheelhouse separately, copy and hash its exact wheels into the private run,
install with `--no-index --no-deps`, record installed distributions and require
`pip check`. Qualification itself performs no downloads. Spine Packs' wheel
MUST still declare no runtime dependencies. No dependency addition is inferred
for any older baseline.

Evidence identifies the exact upstream target, source versus installed mode,
public-CLI transcripts, read-only checks, named integration scenarios and local
assets. It is technical qualification only; scoped tooling review and successor
content/release gates remain separate. Commands never accept an existing ledger.
