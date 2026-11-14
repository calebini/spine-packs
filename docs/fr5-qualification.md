# FR-5 disposable and installed-package qualification

This gate exercises the successor installer against exact Spine
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122` (`0.10.0`, schema `19`), while
retaining v1 integration coverage on the three previously supported exact
baselines. It uses synthetic flight configuration, not curated flight content.
The normative safety boundary is in `specs/architecture.md`.

Use an isolated Python 3.12+ environment containing `build`, `hatchling>=1.27,<2`,
`setuptools>=69`, `wheel`, and `jsonschema` for official development checks.
Build dependencies may need an initial network download. Qualification itself
exports the pinned commits locally, builds with `--no-isolation`, and installs
only local wheels with `--no-index --no-deps`:

```sh
"$FR5_BUILD_PYTHON" scripts/qualify_fr5.py \
  --spine-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/spine \
  --tickerd-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/tickerd
```

`FR5_BUILD_PYTHON` is the absolute venv interpreter path. The script refuses a
non-venv interpreter or unavailable exact commits. It has no ledger-path input,
publication, source-checkout modification or dependency-download step. It never
uses a reference checkout's uncommitted files. Tickerd is exported at exact
`ffe613c65ea3d6fc70a1dc3603c32068f06350df` (`0.2.0`). The v1 Spine pins are
`72203f092de191a7633b1884bf0d61836a25abe4` (`0.3.0`),
`ab18a8a51c9bf548220f67e2db0220bfe9783888` (`0.5.0`), and
`ad1db8e1a4c7aa9a525612324d08824802a86351` (`0.6.0`).

The gate compares every installed Spine/Tickerd package file to its wheel,
export and exact Git bytes, including the complete Python module closure.
The existing FR-2 gate additionally verifies the 0.10.0 transitive contract
authority pins and historical/retired schema readback on source and installed
Spine Packs. `system.info` supplies runtime preflight, not Git provenance.

The new four-scenario v2 harness covers missing/create/retain, exact approval,
schema/rendering/profile update cascades, mixed v1/v2 profile catalogs, both
bindings, all 11 write-command response losses and exact same-execution replay,
before-submission recovery, checkpoint/result continuation, complete checkpoint
admission, read-only verify, missing execution coverage, draft refusal and
no-clobber input/output protections. Captured responses come from the real public
CLI. Only response-loss injection is in-process; normal apply, continuation and
verify use new processes. Each scenario allocates fresh ledgers and private
synthetic owner/cursor configuration. Ledger/WAL checks inspect metadata only.

The existing four v1 integration scenarios run from source and clean wheel on
each of the three supported baselines. Package qualification compares direct and
sdist-built wheels, exact archive/resource bytes, license/dependencies and
isolated installed imports. It also requires identical candidate archives across
the v1 matrix. The installed v2 harness is taken from the extracted sdist and
uses only the installed wheel's modules/schemas. Full specs and developer
orchestration remain in the repository, outside the sdist.

All evidence remains in fresh private temporary directories, including failed
runs. The top-level `PASS.json` is emitted only after every gate passes. Build
logs, commands, provenance, CLI transcripts and per-scenario results identify
what ran. No existing/operator ledger, items, facet values, destination approvals,
reminders, notification sends, deployments or publication are part of this gate.

## Qualification result

Technical qualification passed on 2026-11-14 for the working-tree candidate
after checkpoint `1c7809309b30153c4b41db8cf5e44934cd0fd85b`. No installer runtime
repair was needed. This is not qualification of a committed release candidate.
The environment was macOS 26.7.1 arm64, Python 3.14.6, build 1.6.1, Hatchling
1.33.0, setuptools 84.2.1 and wheel 0.48.0. Official validation used jsonschema
4.26.0.

| Exact Spine runtime / schema | Source integration | Clean installed wheel |
| --- | --- | --- |
| 0.3.0 / 12, v1 installer | 4 passed | 4 passed |
| 0.5.0 / 15, v1 installer | 4 passed | 4 passed |
| 0.6.0 / 15, v1 installer | 4 passed | 4 passed |
| 0.10.0 / 19, v2 installer | 4 passed | 4 passed |

All 32 integration scenarios passed. Each v2 run covered all 11 response-loss
replays; each v1 run covered all six. Source and installed FR-2 gates also passed:
actual B1 history stays on root B with A2/B2 current heads, repeated pins are
deduplicated per pass, mixed v1/v2 catalogs paginate completely, current/historical/
retired reads work, and missing/invalid requests preserve their owning exits.
Each gate observed 118 planner reads plus 19 setup/direct calls and unchanged
ledger metadata during read-only phases.

Git/export/wheel/installed attestation covered 308 Spine files for 0.10.0, 90
for 0.3.0, 189 for 0.5.0 and 213 for 0.6.0, plus all 16 Tickerd package files in
each installation. Both FR-2 gates verified the 32 upstream contract-authority
pins. Package checks passed exact wheel/sdist membership, source/resource byte
identity, direct-versus-sdist-built wheel equality, offline installation, private
no-clobber artifacts, installed import/resource isolation, MIT metadata and zero
runtime dependencies. Candidate archives matched across all three v1 baselines.

Additional official Draft 2020-12 validation passed for all 390 saved v2
manifests/artifacts across the source and installed execution runs. Required
repository checks passed: 188 required files, 125 official contract tests without
skips, and 279 runtime tests including five new provenance rejection/control
tests. The required system-Python contract run passed with 60 development-
validator skips, covered by the official run. Ordinary integration discovery
skipped all eight opt-in tests without creating ledgers. Whitespace checks passed.

Private evidence root:
`/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr5-amr1eavd`.
It contains the top-level `PASS.json`, environment, exact command logs, upstream
provenance, three `spine-packs-package-*` runs and both v2 integration runs.
The separate FR-2 private directories are
`/private/tmp/spine-packs-fr2-gate-at_kt_7h` (source) and
`/private/tmp/spine-packs-fr2-gate-objoweuj` (installed), linked by the gate logs.
Repository test logs are retained under
`/private/tmp/spine-packs-fr5-build-wolpcmm2`.

These exact local candidate files are in each package run's `assets/` directory:

| File | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `adc18693db6d6a54cc5c5d4681a82cd4a453694220f65c510f37ebc07c69deb1` |
| `spine_packs-0.3.0.tar.gz` | `3592deb08c5ef9b1e49bcb6081ac83b6ef1293f1ba4a82a28438c32ed8ae79b5` |

The working-tree candidate retains package version `0.3.0` solely for local
qualification; no new release identity or publication is authorized. These bytes
must not replace published assets. Results do not qualify every Python/platform
combination, concurrent operators, consumer rendering or destination disclosure.
FR-6 still requires
operator decisions on fields, labels, template inclusion, profile default and
immutable pack/release identity. A final committed release candidate must be
qualified separately before tag or asset publication.

Next gate: bounded review of this qualification increment, with a separately
approved exact payload before external reviewer invocation. After review closure,
FR-6 must resolve the curated content/distribution choices; qualification does
not approve them. No existing/operator ledger was used, no Spine checkout was
modified by this work, and no deployment, publication, commit or push occurred.
