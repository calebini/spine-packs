# Spine 0.6.0 compatibility qualification

Status: local candidate qualification passed on 2026-09-20; not publication,
clean-commit release qualification, or staging authorization.

Installer candidate `0.3.0` admits exact Spine commit
`ad1db8e1a4c7aa9a525612324d08824802a86351`, runtime `0.6.0`, schema `15`,
alongside the existing 0.3.0/schema-12 and 0.5.0/schema-15 pins. Confirm the
staged source provenance separately; equal schema numbers do not establish
runtime compatibility. No Spine checkout or operator ledger may be modified.

## Inspection and implementation

The diff from `ab18a8a51c9bf548220f67e2db0220bfe9783888` changes web-read
implementation/contracts, package version, and advertised web capabilities.
`src/spine/commands/`, `src/spine/core/`, and `src/spine/ledger/` are unchanged.
The public system-info-v3 schema and installer-relevant catalog command/readback
schemas are unchanged. The 0.6.0 system-info validator therefore explicitly
reuses the existing 0.5.0 schema. The environment still records the true runtime.

The execution union remains the ten contracts required on 0.5.0. New web-read
cursor and registry contracts are not the CLI catalog cursor or installer
dependencies. The six read and six write command allowlists do not change.
Ledger identity, exact environment comparison, approval binding, durable
checkpoints, and bounded replay remain required. Verification records
`captured_responses_only_spine_0.6.0`; cross-runtime disclosures are rejected.
Unknown versions/schema pairs fail closed. A runtime upgrade invalidates an
old plan even when the ledger identity and catalogs stay unchanged.

Released `kinflow-starter 1.0.0` remains byte-identical and rejects 0.6.0.
`1.0.1-draft.1` changes only draft identity/status, the exact runtime allowlist,
and its digest. All 52 archetypes, profiles, bindings, and their semantics are
preserved. The draft is not installable. Release finalization materializes
stable `1.0.1` with only version/status/digest changes from the draft; its
publication and any operator installation remain separately authorized.

## Pre-review qualification evidence

All local checks passed. Evidence root:
`/private/tmp/spine-packs-spine060.SvXAse/`.
The 0.6.0 source is exported from the exact commit into `spine/`, built with
existing isolated tooling, and installed into a fresh `venv/` with the pinned
Tickerd 0.2.0 wheel. No shared or Spine checkout environment is changed.
The preserved earlier isolated environments supply the exact 0.3.0 and 0.5.0
regression baselines from `docs/local-qualification.md`.

Results on macOS / Python 3.14.6, build 1.6.1, Hatchling 1.32.3:

- verifier: 115 required files; whitespace checks passed;
- 63 contract tests and 125 synthetic runtime tests passed;
- four source-tree and four clean-installed disposable real-CLI scenarios on
  each of the three baselines, including uncertain-response recovery for every
  one of the six write commands;
- offline clean-wheel installation, bundled schema/source/license checks,
  console/module entrypoints, and direct-versus-sdist wheel byte equality;
- independent jsonschema 4.26.0 Draft 2020-12 checks: 12 schema meta-validations,
  all 37 pack fixture cases (lexical/semantic checks separate), and 16 positive
  installer artifacts;
- exact comparison of the 0.6.0 upstream system-info schema to the reused
  client validator, and unchanged commands/core/ledger source against the 0.5.0 pin;
- released pack and historical drafts remain byte-identical; the existing
  Spine checkout's two documentation edits were left untouched.

Evidence directories relative to the private root:

| Spine baseline | Source-tree tests | Clean-package qualification |
| --- | --- | --- |
| 0.6.0 | `spine-packs-integration-pd4ynz1w` | `spine-packs-package-swc_smux` |
| 0.5.0 | `spine-packs-integration-1j4ag_1j` | `spine-packs-package-df17ekjp` |
| 0.3.0 | `spine-packs-integration-luwmko54` | `spine-packs-package-u4bhiy3p` |

All three pre-review builds produced the same candidate assets:

| Asset | SHA-256 |
| --- | --- |
| `spine_packs-0.3.0-py3-none-any.whl` | `443036451f1124da6ddd9019a084c7309fb54084df7d571f5fbcaeca4418e672` |
| `spine_packs-0.3.0.tar.gz` | `0e169114088263d69c4e132098bfc6dfe156f0d6c883bb8f46d7ac19f85c6f3f` |

These are historical pre-review working-candidate assets, not approved public
release bytes. The bounded review's packaging/documentation patch changes
the sdist inputs, so the hashes above do not identify the patched build.
Requalification must emit fresh `SHA256SUMS` for that build; do not reuse these
hashes for publication. This report is itself included in the patched sdist,
so its containing archive's checksum belongs in the external qualification
evidence and release assets, not in this report.
The compatibility draft's content digest is
`02cacc2dc8c84d1869c4f68c07f780886aa9c34720bc4b325d883616766252c9`;
its file SHA-256 is
`fd915e5cb362c35917588f52a284abfee8b15cf01ae9f39d9ad9b553ecd8e057`.
The installed real-CLI scenarios use isolated synthetic manifests, not an
operator installation of the entire curated pack. No deployment qualification
is implied. The independent checker is retained as `check_contracts.py`.

## Remaining gates

The bounded review returned `pass_with_minor_clarification`, with zero blockers
or majors and two release-handoff minors. The patch includes this report in
the sdist and its exact-membership qualifier and clarifies the separately
provisioned Spine baselines in the release documentation. The original review
payload and findings remain preserved; no follow-up audit is implied.

Post-patch qualification passed all three baselines; the original review and
post-patch evidence are retained locally. The finalization gate requires a
committed release candidate and qualification of that exact commit, followed
by explicit approval of the new installer and pack versions/tags/assets.
Final-commit evidence and checksums are recorded outside the packaged inputs
to avoid self-referential archive hashes. No automatic publication, tag movement, deployment,
migration, or installation follows a passing local test. The previous staging
handoff's 0.2.0/1.0.0 downloads must not be used for a 0.6.0 target.
