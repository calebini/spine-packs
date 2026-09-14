# Slice 4 recovery evidence investigation

Status: test-only investigation, 2026-09-15. This report is explanatory, not a
normative contract change or authorization to implement continuation.

Follow-up: the operator-approved clarification is now recorded in
`specs/installer.md` Section 11 and `specs/installer-artifacts.md` Section 9.1.
The investigation below records the evidence and limitations that motivated it;
its recommendation to clarify the specs is addressed. It remains test-only and
does not authorize or qualify a continuation implementation.

## Result

The existing artifacts support a viable **snapshot comparison** approach for
the six pinned write commands. The tests do not establish a need to add full
original catalogs to the plan or checkpoint. They also do not establish that a
snapshot match is sufficient to admit recovery.

The initial concern was that a saved SHA-256 digest cannot be advanced to a new
catalog digest without its original preimage. That remains true. However, fresh
public readback supplies the catalog after interruption. A test-only checker can
reverse the explained changes **in a private in-memory projection**, retain all
other fresh catalog facts, and compare the reconstructed original fingerprint
with the plan's saved fingerprint. No Spine state is reversed or written.

This establishes feasibility for the tested fingerprint-visible state, not a
production resume algorithm, universal proof of evidence sufficiency, or real
Spine qualification. In particular, uncertain creates/revisions require full
readback validation and exact replay correlation beyond this projection check.

## Evidence sources and boundaries

- Spine Packs baseline: `12e670a003788c3a906f442bb36ef79bba1a31a4`.
- Normative requirements: `specs/installer.md` Sections 7, 11, and 12;
  `specs/installer-artifacts.md` Sections 7 through 10.
- Pinned Spine baseline: `72203f092de191a7633b1884bf0d61836a25abe4`
  (runtime 0.3.0 / ledger schema 12), inspected with read-only `git show`.
- Pinned source: `src/spine/commands/notification_profiles.py`,
  `_list_roots` lines 838-850 and `_binding_list` lines 1160-1174;
  `_show_root`, create/revise/metadata/binding handlers and their replay behavior
  were also inspected. Source-file SHA-256:
  `04a59f1b90d0d0d0bbba67d43a399713e2c34733957e3339d7912310a20ce957`.
- `src/spine/core/hashing.py` confirms SHA-256 over canonical JSON bytes.
- Reproducible tests: `tests/runtime/test_recovery_evidence.py`.

No Spine repository files, runtime code, schemas, pack content, or normative
specifications were modified. No ledger was opened, no Spine command executed,
and no deployment used. The tests require only this checkout and Python's
standard library; they do not import Spine or need its checkout at test time.

## What Spine actually fingerprints

The fingerprints are canonical hashes of ordered lists, not hashes of complete
rows, revision contents, audit history, or an entire database.

| Catalog | Exact hashed facts per row | Order / filter |
| --- | --- | --- |
| Archetypes | `id`, `key`, `status`, `current_revision_id` | key then root ID; all statuses for the planner's query |
| Profiles | archetype-style root facts plus `display_name`, `description` | key then root ID; all statuses |
| Bindings | `notification_profile_binding_id`, `item_archetype_id`, `notification_profile_id`, `status` | archetype ID then binding ID; active only for the planner's query |

Owner scope is enforced by the query/readback validation, not represented as a
separate field in these hash preimages. A matching hash never replaces target,
owner, runtime, contract, pagination, or semantic checks.

The checked-in readback schema constrains the digest's shape, not its derivation.
This investigation pins the derivation to inspected code. Tests use independent
in-memory projections with content-derived hashes, not the existing test double's
canned per-catalog hashes. Cursor encoding itself is not modeled or qualified.

## How persisted evidence supports inverse comparison

Starting from validated fresh projections, walk explained actions in reverse
order. This order matters when metadata and revision updates affect one profile.

| Explained effect | Information already available | In-memory inverse |
| --- | --- | --- |
| Archetype/profile create | requested key and definition; accepted response IDs, or provisional fresh readback IDs for the uncertain action | validate expected post-state, then remove the created root |
| Archetype/profile revise | literal root ID and `expected_current_revision_id`; accepted response revision ID or provisional fresh revision | validate post-state, then restore the prior revision pointer |
| Profile metadata update | literal root ID, `expected_metadata`, desired metadata | validate post-metadata, then restore exact prior metadata |
| Binding set | resolved request IDs; classification's original `observed_binding` or explicit absence | validate post-binding, remove it, and restore the original active binding projection if present |

Unselected entries are preserved verbatim in this calculation. An unexplained
addition, removal, or fingerprint-visible change therefore changes the
reconstructed original digest and fails comparison. This does not attempt to
invert SHA-256 or predict generated IDs.

For an uncertain first unresolved action, examine two bounded candidates:

1. only the accepted prefix is reflected in fresh state;
2. the accepted prefix plus exactly that first unresolved action is reflected.

In either case, its original command ID and exact request remain derivable from
the plan, approval, and accepted responses. Candidate readback IDs MUST NOT be
substituted into the preserved original request, promoted into accepted evidence,
or used to advance later actions without the actual correlated response.

## Focused test results

The fixture scenario contains two selected units (one missing, one drifted) and
an unselected unit in each catalog. Seven ordered actions exercise all six write
commands, including metadata plus revision updates to the same profile and both
missing and replacement bindings. The model generates arbitrary server IDs;
the checker cannot access the model's original state or receipt cache.

Eight test methods cover:

- content-derived fingerprints, fixed empty-list hash, and page-size independence;
- before-submission, accepted-but-response-lost, and response-checkpointed states
  at each of the seven action boundaries;
- same-command, identical-request replay without another modeled mutation;
- 63 unrelated add/remove/change cases across those boundaries and all three
  catalogs, rejected against both uncertain and recorded-prefix states;
- terminal partial-result evidence recreating the same prepared checkpoint at
  every action boundary, including the empty prefix;
- rejection of a recorded generated-ID mismatch and a two-unrecorded-action jump;
- tampered/resealed checkpoint, plan/approval correlation, execution actor,
  response prefix, generated IDs, command identity, and changed approval time;
- explicit counterexamples showing that snapshots alone establish neither
  command receipt evidence nor full semantic or historical equality.

The restart checker accepts only serialized plan/approval/checkpoint evidence
and copied fresh projections. It never receives a saved baseline catalog, a
hidden successful response for the uncertain action, or the modeled receipt
cache. Test assertions themselves may observe the server oracle to check
expected outcomes; the candidate checker may not.

Run the focused investigation:

```sh
python3 -m unittest discover -s tests/runtime -p 'test_recovery_evidence.py' -v
```

The tests deliberately assert known limitations rather than treating them as
passing production recovery cases. Their success means the investigation's
claims and counterexamples are reproducible, not that continuation is ready.

Validation on this checkout:

- focused investigation: 8 tests passed;
- repository verifier: passed, 91 required files;
- complete contract suite: 50 tests passed;
- complete runtime suite: 71 tests passed (including the 8 investigation tests);
- tracked and new-file whitespace checks: passed;
- Spine checkout: unchanged and clean after read-only inspection.

## Limits and unresolved implementation requirements

1. **Snapshot equality is not full readback equality.** Revision bodies and audit
   fields are absent from the fingerprint. Public response validation, immutable
   revision semantics, desired-content comparison, and complete selected-object
   checks remain mandatory. This test-only checker is intentionally not a safe
   standalone recovery admission gate.
2. **An uncertain create can have unproven IDs.** A negative witness substitutes
   other root/revision IDs in its fresh projection and still reconstructs the
   baseline hash after removing that candidate root. No receipt was established.
   Real recovery must check the complete public definition and available creation
   provenance, replay the original request, and correlate the returned IDs with
   the candidate state before accepting it or advancing. Corresponding uncertain
   revision and binding cases need the same discipline.
3. **State is not history.** A metadata edit followed by restoration can produce
   the same fingerprint. Retired bindings outside the active query and receipt
   rows are not represented. The tests do not claim detection of every historical
   write, and no new history/receipt authority is proposed.
4. **The simulator is not Spine.** It covers snapshot-visible effects and models
   compatible replay, but not real persistence, normalization, permissions,
   rejects, cursor encoding, or receipt lookup. No-op/compatible-replay edge cases,
   full readback admission, filesystem restart behavior, and all failure paths
   still require Slice 4 implementation tests and real pinned-Spine qualification.
5. **Specification method needs explicit agreement.** The current prose describes
   deriving expected post-prefix snapshots from the original planned catalog.
   It does not describe reconstructing the original fingerprint from fresh state.
   A narrow normative clarification and pinned projection vectors should precede
   production use of this equivalent comparison strategy. Do not silently change
   the meaning of the original snapshot digest or store a locally invented one.

## Recommended next step

Review and specify inverse fingerprint comparison as one part of continuation
preflight, retaining full readback/semantic checks and exact replay-response
correlation. No artifact-schema expansion is demonstrated necessary by these
tests; do not add complete catalog snapshots preemptively.

Then implement Slice 4 under separate authorization with explicit continuation
inputs, checkpoint/partial-result loading, refreshed public observations, both
bounded state candidates, and durable continuation of the original execution.
Stop if the real pinned public surface cannot supply any required evidence.
Actual Spine qualification should be brought forward if needed to settle those
details; passing this simulation is not a reason to defer an integration blocker.
