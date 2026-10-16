# FR-2 read-only planner qualification

Date: 2026-10-16. This is local evidence for the authorized read-only increment,
not a release, deployment, or qualification of successor apply/recovery/verify.
Normative authority remains `specs/facet-rendering-packs.md` and
`specs/installer-artifacts-v2.md`.

## Exact baseline and provenance

- Spine: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`, runtime `0.10.0`, schema `19`.
- The exact commit exists locally. Source was exported with `git archive`, not
  taken from HEAD or edited in the reference checkout.
- All **308** packaged `spine/` files match the exact Git tree, exported source,
  wheel and installed files byte-for-byte. **32** upstream schema/registry/spec
  authority files also match the exact Git tree and inventory hashes.
- Spine wheel SHA-256:
  `0cf6d7c1f73463195b274cae269fcb4221bf4a8c3744c9a8a3e026cc0b491963`.
- Isolated build root: `/private/tmp/spine-packs-fr2-0100.WbU0lE`.
- Tickerd `0.2.0` was built from exact export
  `ffe613c65ea3d6fc70a1dc3603c32068f06350df`; Spine's public dependency preflight
  passed. No dependency was substituted from the newer working checkout.

Neither `system.info` nor a console-script hash alone establishes Git provenance.
Earlier 0.9.0/0.9.1 findings, inventories, fixtures and audit payloads remain
unchanged. This baseline does not broaden the existing v1 runtime allowlists.

## Independent gates

| Gate | Result |
| --- | --- |
| Repository verifier and `git diff --check` | Passed |
| Official Draft 2020-12 and independent contract suite | 89 tests passed in the isolated development environment |
| Runtime suite | 139 tests passed, including 13 focused FR-2 tests |
| Source FR-2 public-CLI gate | Passed on a new disposable ledger |
| Installed-wheel FR-2 public-CLI gate | Passed on a separate new disposable ledger |
| Existing package qualification on exact Spine 0.6.0 | Passed: sdist/direct-wheel byte equality, resources, clean install, dependency/help checks and all four installed integration scenarios |

The default system `python3` lacks development `jsonschema`: its required
contract command ran 89 tests with 24 skips. The complete final suite was therefore
rerun with the isolated environment
below, with **no skips**. No upstream test count is substituted for these results.

The FR-2 harness creates synthetic configuration only through public CLI
subprocesses. It proves:

- complete all-missing planning without writes;
- A2/B2 current roots with binding and two rendering selections pinned to B1;
- B1's actual B root, original immutable definition and verified hash retained
  in history, not relabelled as desired A;
- equivalent desired A2 plus drifted facet binding/rendering/profile cascade;
- one B1 revision lookup per pass despite repeated pins;
- complete mixed v1/v2 catalog pagination and identical plans at page sizes 1/100;
- two complete observation passes and current/historical/retired exact reads;
- missing revision CLI exit 4 and invalid request exit 2;
- only read commands during planning, with unchanged ledger/WAL file metadata.

The metadata check reads file size/mtime only. It is corroboration, not a
row-level integrity or no-ABA proof. The harness never opens/hashes the ledger
or WAL. Spine owns the read-only/no-receipt command guarantee. Public readback
does not expose a complete receipt inventory, so no invented audit proof is
claimed.

Fault-injection tests cover missing references, corrupt/unsupported evidence,
capacity/preflight/transport failures, malformed envelopes, hashes, owners,
root membership, wrong requested revisions, changed current pointers, pagination
and staleness, byte/call/time/entry ceilings, cursor-config absence, wrong runtime
or contract advertisements, v1 ordinary equivalence and disabled successor
apply/verify. Corrupt ledger rows and capacity exhaustion are **simulated public
responses**, not database mutations. Saved upstream wire vectors are independently
checked by both the official validator and the separate runtime decoder.

Retained evidence:

- Source run:
  `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr2-gate-c3kwfjqq`.
- Installed run:
  `/private/var/folders/sg/n2czprsx78764j63m_mjcm1m0000gn/T/spine-packs-fr2-gate-2a4qp2ge`.
- Package gate:
  `/private/tmp/spine-packs-fr2-0100.WbU0lE/spine-packs-package-oc9tfqib`.
- Checked-in `tests/fixtures/installer-v2/fr2-cross-root.json` derives from an
  earlier passing synthetic run; target paths and opaque cursor tokens were
  replaced with explicit synthetic values, and request/plan digests resealed.
  It contains no cursor secrets and is not a reusable pack or live ledger snapshot.

An initial package attempt failed at Spine's public `runtime_dependencies`
preflight because the isolated 0.6.0 environment lacked Tickerd. Installing the
already-built exact Tickerd wheel fixed the test setup; no installer compatibility
check was relaxed. Both failed and passing temporary evidence were retained.
The legacy 0.3.0/0.5.0 unit vectors passed; their full package integrations were
not rerun here. All supported-baseline/full successor qualification remains FR-5.

## Reproduction

With the isolated builds above (or newly recreated exact exports):

```sh
python3 scripts/verify_repo.py
/private/tmp/spine-packs-fr2-0100.WbU0lE/env/bin/python -m unittest discover -s tests/contract -p 'test_*.py'
python3 -m unittest discover -s tests/runtime -p 'test_*.py'
git diff --check

/private/tmp/spine-packs-fr2-0100.WbU0lE/env/bin/python scripts/qualify_fr2.py \
  --bin-dir /private/tmp/spine-packs-fr2-0100.WbU0lE/env/bin \
  --export /private/tmp/spine-packs-fr2-0100.WbU0lE/spine \
  --spine-repo /Users/Shared/Agent-Workspace/repos/personal/cortext1/spine \
  --wheel /private/tmp/spine-packs-fr2-0100.WbU0lE/wheels/spine_ledger-0.10.0-py3-none-any.whl
```

For the installed test, call that script using the package gate's
`installed/bin/python -I` and add `--installed-installer`; it refuses a source
installer import. Each invocation creates a new ledger; no existing-ledger
argument exists. Temporary builds are not durable release storage.

## Status and remaining gates

FR-2's historical lookup blocker is resolved; the read-only implementation and
local checks are ready for bounded review. External review requires a newly
approved payload; none was invoked. No commit, push, publication, deployment,
Spine checkout edit, operator ledger access, items, facet values, disclosure
grants, reminder materialization or notification sends occurred.

No new product decision is required for revision lookup or missing-evidence
handling. The already-ratified rule remains: any missing referenced revision
aborts observation; corruption/capacity/preflight failure is never absence.
Before FR-3, separately authorize initial apply and refresh execution-specific
0.10.0 fixtures/evidence labels. FR-6's curated flight fields, labels, templates,
opt-in/default choice and distribution identity still require operator review.

## Subsequent bounded review and local patch

The earlier status and gate results above describe the pre-review candidate.
The approved second bounded review completed with one major and two minor
findings; its report is preserved unchanged. The operator subsequently authorized
all three patches: desired rendering byte bounds, malformed revision-failure
classification, and current specification introductions.

The patched source passed 90 independent contract tests (no skips), 142 runtime
tests (16 focused FR-2), the repository verifier and whitespace checks. The system
Python contract command had 25 skips because development `jsonschema` is absent;
the isolated complete suite supplies that gate. Fresh disposable public-CLI
qualification passed on the same exact 0.10.0 pin, with source/wheel/installed
provenance reverified. Evidence and scope are recorded in the
[patch follow-up](../whetstone_runs/facet-rendering-fr2-audit-002/patch-followup.md).
Earlier installed-installer package qualification was not rerun for this patch.
These fixes have not been externally re-audited; no FR-3 authority or release
qualification is implied.
