# Bounded facet/rendering spec audit — approval required

Status: **staged only; not authorized and not run**.

Proposed transmission: the exact 14 files below to one nested Codex Reviewer
through Whetstone `audit-change`, profile `consistency`. This includes selected
Spine specification/machine-contract/fixture excerpts and short source-code
excerpts needed to examine the pinned profile-list blocker. No full runtime
source tree, operator ledger, secrets or deployment configuration is included.

Reviewer-only consistency assessment, not Phase 1/2, an Editor loop, convergence,
implementation approval, source apply-back, commit, push or publication.

Source baseline: `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`, Spine 0.9.0/schema 19.
The source-level v2 profile-list conflict is explicitly a review target; no
public-CLI ledger reproduction was performed during this planning task.

Total payload bytes: 349,591. Paths below are repository-relative.

| File | SHA-256 |
| --- | --- |
| `whetstone_runs/facet-rendering-spec-audit-001/audit-notes.md` | `16d2a75a98c8dbd8e0310a83d9309f4741dadb7315781629244c65fb9033ad28` |
| `AGENTS.md` | `541823b3a74099aeba359715c1b88dd3262344df26a0baea5b2fed2124dbb149` |
| `specs/overview.md` | `a8e480affee439f5608097d6728a3a96b6765c4aa00f33617711b038bd0d92ab` |
| `specs/architecture.md` | `3c1bebaddd306666ef0f81a2d82bc958c95de0b870e506c34f8997e7e6a99b7e` |
| `specs/compatibility.md` | `582877297d3f67895bb9a3f0ac73a8fcb799b84655292f3c0bbe0b1442ff0fdc` |
| `specs/pack-format.md` | `26ce02b87adad016798d9c4999d3631ff6b928e0d536a16642cd293ca97df1e3` |
| `specs/installer.md` | `2b082beb18500968570b6a0b92061dabfcb884c2ceb12f0fbae9737122830f7a` |
| `specs/installer-artifacts.md` | `e3f977e2cdc09c12993e4fa20e6da83e320d1635050c8f367429aa9f62e3769e` |
| `specs/implementation-plan.md` | `9b6b0cd5e9aebf934c4c829aaae93008d0a4580cbf8392c2fb7c2af89ecb1a55` |
| `specs/facet-rendering-packs.md` | `cb33c6e22bd45511aed1f1d29bc1d309ad774a6a0574ddbf17a625f7e5149448` |
| `docs/facet-rendering-baseline.md` | `5bdfe805dce09350f1d4e097fe58e5b1628ef5edd9d298c2a0e58863713d7621` |
| `whetstone_runs/facet-rendering-spec-audit-001/spine-source-excerpts.md` | `0e47ec1f23418856bd57b8ce429c54c7ebb67b7b6f4e722246f504d39d65b73d` |
| `whetstone_runs/facet-rendering-spec-audit-001/spine-wire-evidence.json` | `5afe978bd9db3daaac11f039c9bd28a3a5308465e46f325b45ab6bfc09e3cc71` |
| `whetstone_runs/facet-rendering-spec-audit-001/spine-readback-blocker.md` | `95f288931e08e632b7f50c5ccabaecb20fcdb778885559a5726ec7c2d2aa2b66` |

## Launch gate

After explicit approval of this inventory, re-hash every file and require exact
matches with payload.json before any client invocation. Changed bytes or extra
files require renewed payload approval. Confirm the local reviewer executable
and available model at that time; do not invoke a live client to probe while
staging. Follow the Whetstone skill’s nested-client execution approval rules.

Use the existing Whetstone `audit-change --root <this directory> --notes
<audit-notes.md> --spec <each other listed file> --profile consistency` surface
with an explicitly configured Codex client. No launch command was run. Expect
outputs only under `change_audit/`; preserve inputs and do not overwrite old runs.

APPROVAL.md and payload.json are local approval/launch bookkeeping, not extra
reviewer input. The full original source files named inside the excerpt bundles
are provenance references, not additional authorization to send those files.

## Checks completed before staging

- Repository verifier passed (117 required files).
- Existing contract suite passed: 65 tests.
- Existing runtime suite passed: 126 tests.
- `git diff --check` passed.

These are preservation checks, not tests of an implemented v2 workflow. No
machine schema, runtime, curated pack, Spine checkout or deployment was changed.
No commit, push, package publication or external reviewer run occurred.
