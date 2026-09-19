# Spine 0.6.0 release finalization

Prepared 2026-09-20 under operator authorization to finalize the releases.
This authorizes local stable-pack preparation, a release-candidate commit,
and qualification, not tag creation, push, GitHub publication, or staging.
The source of truth remains `specs/`; publication gates remain in
`docs/releases.md`. Earlier published tags and assets must remain unchanged.

## Proposed releases

- Installer `0.3.0`: tag `installer-v0.3.0`, title `Spine Packs installer 0.3.0`,
  MIT, regular release. Publish only the exact qualified wheel, sdist and
  their `SHA256SUMS`; do not rebuild after asset approval.
- Pack `kinflow-starter 1.0.1`: tag `pack-kinflow-starter-v1.0.1`, title
  `Kinflow Starter 1.0.1`, regular release, with its JSON manifest and a
  separate `SHA256SUMS`. Do not make the pack replace the installer as the
  latest installer release.

Both tags are proposed to point to the exact finalization commit after it
passes clean-checkout qualification. Final commit identity, evidence paths
and all asset hashes must be presented together for publication approval.
That record stays outside packaged inputs so recording an archive checksum
cannot change the archive whose checksum it records.

## Reviewed compatibility boundary

The installer adds exactly Spine `0.6.0` / schema `15`, source commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, while retaining these baselines:

| Spine version / schema | Exact source commit |
| --- | --- |
| `0.5.0` / `15` | `ab18a8a51c9bf548220f67e2db0220bfe9783888` |
| `0.3.0` / `12` | `72203f092de191a7633b1884bf0d61836a25abe4` |

Tickerd remains `0.2.0` at `ffe613c65ea3d6fc70a1dc3603c32068f06350df`.
Unknown runtime/schema pairs fail closed. System-info validation reuses the
unchanged schema-15 shape but records the actual runtime and ledger identity.
Upgrading a runtime invalidates an earlier plan and approval even if the
ledger identity and catalog definitions remain unchanged.

The public CLI allowlists, content semantics, contract union for schema 15,
receipt handling, and recovery behavior are unchanged. There is no HTTP
transport, web-read feature, database access, scheduler, or Spine runtime patch.
Captured command responses remain the receipt evidence; there is no independent
receipt readback. The installer remains Python 3.11+, standard-library-only,
local POSIX, and single-operator. Qualification on macOS/Python 3.14.6 does not
establish Windows, all-Python, Linux staging, or multi-writer support.

The 31-file reviewer-only bounded audit returned
`pass_with_minor_clarification`, with no blockers or majors. Its two minors
were corrected: the linked qualification report is included in the sdist and
its exact-membership checks, and release compatibility prose names the 0.6.0
candidate separately from published 0.2.0. All three package-baseline repeats
passed after that patch. There was no follow-up reviewer invocation and no
new full-content audit of the 52-archetype pack.

## Stable pack promotion

Stable `1.0.1` changes only version, status and digest from
`1.0.1-draft.1`. It preserves all 52 archetypes, 52 archetype-specific profiles,
52 default-binding intents, empty dependencies and compatibility declarations.
Compared with released `1.0.0`, only runtime `0.6.0` compatibility is added,
along with version and digest. Every earlier draft and release remains intact.

- Manifest: `packs/kinflow-starter/kinflow-starter.1.0.1.json`.
- File SHA-256: `4ad2c351af5fb575827590efa45dabceebff8dfbf6aa3acea5a0ee143c45b491`.
- Content digest: `5d9986c549ea0fe48157e977dbb41d9f45820b3de1f0611816b325e2f1d862af`.
- Exact runtime allowlist: `0.3.0`, `0.5.0`, `0.6.0`; installer `0.3.0` is
  required for `0.6.0`. The existing three content contracts do not change.

The stable file is immutable from preparation onward. If final validation
finds a content problem, stop rather than silently modifying its pinned bytes.
Release status enables planning for apply; it does not authorize installation.
The pack is a separate download, never bundled into the installer wheel/sdist.

## Exact-commit gates

From a clean isolated checkout of the finalization commit, run:

1. Repository verifier, contract tests, runtime tests and whitespace checks.
2. Full package qualification against each of the three pinned public CLI
   environments, always allocating new disposable ledgers. Require identical
   assets across runs and direct-wheel/sdist-wheel byte equality.
3. Independent Draft 2020-12 meta-validation and the full pack fixture matrix,
   plus positive installer artifacts. Keep lexical/semantic validation separate.
4. Stable-pack file/digest pins, exact unchanged-content comparisons, and
   synthetic full/granular plans against missing and equivalent catalogs on
   all three baselines. These plans are not real-target curated-pack installs.
5. Confirm all released and historical draft bytes remain unchanged and the
   detached checkout stays clean. Record source commit and asset identities.

Private qualification logs, ledgers, synthetic approvals, audit payloads and
local environments must not be committed or uploaded as release assets.
Failed evidence is preserved, never reused as an installation target.

## Staging remains separate

After publication, a Cortext1 agent may download checksum-verified installer
0.3.0 and pack 1.0.1 when separately authorized. It must confirm staging's
actual runtime, schema, source provenance, advertised contracts, executable,
ledger identity and paths. Schema 15 alone is insufficient.

The operator must explicitly select an existing Spine catalog owner, actor
for later apply, and either all archetypes or a sorted archetype-key list.
Do not infer identity from a login, create an owner, or configure delivery.
Produce a read-only plan first and obtain approval of its exact digest and
every update action before apply. Preserve checkpoints/results and run verify;
do not restart partial executions as fresh installations. No migration,
production change, deployment, or staging access is authorized here.
