# Local disposable-ledger qualification

This is Slice 6 test tooling, not deployment or pack release. The normative
boundary is in `specs/architecture.md`. No daemon or cloud deployment is needed:
the actual public Spine CLIs operate on newly allocated local ledger files.
Do not point these tests at a real ledger; there is intentionally no ledger
argument. Test setup bootstraps only a synthetic subject, with no delivery
destinations, items, workers, or notification sending.

## Isolated dependency setup

Use Python 3.12 or newer (Spine's requirement; the installer needs 3.11+).
The pinned inspected Spine commits are
`ad1db8e1a4c7aa9a525612324d08824802a86351` (0.6.0, schema 15),
`ab18a8a51c9bf548220f67e2db0220bfe9783888` (0.5.0, schema 15) and
`72203f092de191a7633b1884bf0d61836a25abe4` (0.3.0, schema 12).
Run source-tree and clean-package qualification separately against each one.
The 0.6.0 baseline uses the same Tickerd pin and public CLI setup below; change
only the exported Spine commit in a fresh directory, never an existing environment.
The local current Spine checkout may be newer and is not implicitly compatible.
Do not change its branch, working tree, environment, or database.

Export committed source into a fresh private directory and install it there.
The following example uses explicit checkout locations; adjust those locations
if necessary, but do not substitute a different Spine baseline. Git archives
include no dirty checkout files. Tickerd commit below supplies the exact 0.2.0
capability descriptor admitted by Spine; no Tickerd daemon is launched.

```sh
QUAL_ROOT=$(mktemp -d /private/tmp/spine-packs-slice6.XXXXXX)
mkdir "$QUAL_ROOT/spine" "$QUAL_ROOT/tickerd"
git -C /Users/Shared/Agent-Workspace/repos/personal/cortext1/spine archive \
  ab18a8a51c9bf548220f67e2db0220bfe9783888 | tar -x -C "$QUAL_ROOT/spine"
git -C /Users/Shared/Agent-Workspace/repos/personal/cortext1/tickerd archive \
  ffe613c65ea3d6fc70a1dc3603c32068f06350df | tar -x -C "$QUAL_ROOT/tickerd"
python3 -m venv "$QUAL_ROOT/venv"
"$QUAL_ROOT/venv/bin/python" -m pip install 'setuptools>=69' wheel
"$QUAL_ROOT/venv/bin/python" -m pip install --no-index --no-deps --no-build-isolation \
  "$QUAL_ROOT/spine" "$QUAL_ROOT/tickerd"
```

Installing build tooling may require network access. The actual Spine/Tickerd
builds above use only the exported local source. Do not install into a shared
environment. Record the source commits and tool versions with qualification
evidence; executable hashes alone do not attest installed package contents.

For the `0.3.0` regression pass, allocate another fresh directory and substitute
only its pinned Spine commit above. Do not replace an existing test environment.
The harness checks the observed runtime/schema pair and makes its synthetic
manifest explicitly compatible with that pair. It does not admit unknown
versions, migrate an operator ledger, or relax compatibility for curated packs.

## Execute the source-tree tests

From the spine-packs checkout:

```sh
python3 tests/integration/test_local_spine.py \
  --spine-command "$QUAL_ROOT/venv/bin/spine-command" \
  --spine-ledger-migrate "$QUAL_ROOT/venv/bin/spine-ledger-migrate"
```

The harness requires public executables from the same isolated environment.
It creates a private run directory and fresh ledger for each scenario, invokes
`spine-ledger-migrate --initialize-if-empty`, checks public `system.info`, and
bootstraps an owner/actor using `subject.upsert`. Those are test-administration
steps, not additional installer commands. It never opens SQLite itself or
imports Spine Python internals. Normal unittest discovery skips these tests
unless this explicit opt-in entrypoint configures them.

The harness copies a small reviewed format fixture into a distinct
`slice6-qualification-only` identity. Version 1.0.0 and 1.0.1 manifests with
`status=released` are local test fixtures for apply eligibility, not published
pack releases. Original curated pack files remain unchanged. Each write plan
gets an exact local approval with a fresh execution UUID and explicit update
action IDs; no approval guard or draft refusal is bypassed.

Coverage includes missing/create, equivalent/no-write, granular selection,
metadata/revision/binding drift, incomplete update authorization, stale plans,
verification with missing response evidence, changed desired state, partial
continuation from results, and accepted-before-response recovery across all
six write command kinds. Normal operations and recovery invoke the installer
in fresh processes. Only faulted apply is in-process to inject a narrow transport
failure before a submission or after a real successful response. All admitted
Spine reads/writes remain real subprocess calls. Recovery compares the replayed
response with the discarded real response, not a synthetic success oracle.
Private checkpoint/result permissions, output no-clobber refusal, and refusal
to interpret the ledger path as a verification-result input are also checked.

Use repeated `--test METHOD_NAME` to select scenarios. `--evidence-parent`
selects an existing directory under which a new private child is always created;
it cannot select or reuse a ledger. A failed run is not resumed by this harness:
rerunning creates another isolated run and preserves the old evidence.

## Evidence and limits

The printed run directory contains setup command logs, exact manifests,
requests, plans, approvals, checkpoints, results, verification artifacts, and
one-line installer envelope captures. Files are private and not committed.
Evidence is retained after success and failure for diagnosis; removal is a
separate explicit operator action. Nothing is uploaded or sent to a reviewer
by this harness.

This does not establish cloud, remote-transport, multi-writer, hostile-filesystem,
live-owner, or public-release readiness. Existing simulated tests still cover
adversarial shapes and filesystem faults more broadly. Supported installer
packaging, clean-install checks, full completion-gate review, and public release
are not implied by a passing source-tree integration run.

## Initial qualification environment

The first local pass on 2026-09-17 used Python 3.14.6, the Spine 0.3.0 and
Tickerd commits above, Spine schema 12, and build tooling setuptools 84.0.0,
wheel 0.48.0, packaging 26.3 in a fresh virtual environment. No existing Spine
checkout or environment was changed. The harness identified two setup/test
expectation mistakes during development (JSON parser byte input and the
existing stale-apply result shape); both were corrected in test tooling only.
The resulting installation/verification and six-command recovery pass needed
no installer-runtime patch. Private run evidence, including earlier failed
harness runs, is retained locally rather than checked into this repository.

Final initial-pass results: four real-CLI integration tests passed, including
six uncertain-response subcases; 55 contract and 106 synthetic runtime tests
passed; repository verification (97 required files) and whitespace checks
passed. Ordinary integration discovery skipped all four tests as intended.
This was a working-tree qualification, not the clean-install gate. The separate
[package qualification](releases.md) runs this harness from an extracted sdist
with `--installed`, using the clean venv's CLI, installed module, and bundled
schemas. No source-tree import path is inserted in that mode.
