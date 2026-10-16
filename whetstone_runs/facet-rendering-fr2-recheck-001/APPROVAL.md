# Approval request — focused FR-2 re-audit

Status: **NOT YET APPROVED; no reviewer invoked.**
Candidate: `be64a9c9c42ed7816caca7b78b68283149044be5`.

Approve one reviewer-only Whetstone `audit-change` consistency pass through the
embedded Codex CLI, sending exactly the **20 files** below plus standard
reviewer instructions/output schema. Scope: closure of the three prior findings
and directly introduced regressions, not another whole-installer review.

Payload: **397,415 bytes**. Locally assembled prompt:
**405,296 characters**, below the observed 1,048,576-character CLI limit.
This measurement uses the prior clean Whetstone export; revalidate before launch.

The payload deliberately includes implementation source and tests so the reviewer
can inspect the fixes. Supporting context includes labelled excerpts from the
exact pinned Spine Git tree and existing Spine Packs helpers. The cross-root
fixture contains synthetic IDs/paths/cursors, not live ledger access or secrets.
No failed-run prompt echo, credentials, cursor configuration, ledger, deployment
file or unrelated repository content is included. Omitted dependencies are not
implicit permission to read more files. This is a static review, not test execution.

No Editor, automatic patches, browsing/tools, unrelated reads, successor writes,
commit, push, deployment or publication. Prior approvals do not authorize these
new bytes. Verify every hash before transmission; changed bytes need reapproval.
The payload/checklist/this approval are local control records, not extra input.

## Exact proposed files

| # | Repository-relative path | Bytes | SHA-256 |
| ---: | --- | ---: | --- |
| 1 | `whetstone_runs/facet-rendering-fr2-recheck-001/audit-notes.md` | 5487 | `b7bb5f8b6d77a6eb6706e95d9464b4d073cb85512d09d5370952c4034c003b33` |
| 2 | `whetstone_runs/facet-rendering-fr2-recheck-001/review-context.md` | 28414 | `0ab2c44051bef9204bacd3cac13dadab1bab39089a0d6bdec283c1881515c371` |
| 3 | `AGENTS.md` | 6764 | `327b1c353b1a858bd0d3ba9d4bfbf639ab7d03009fcb667669fb90f6ba1c3076` |
| 4 | `whetstone_runs/facet-rendering-fr2-audit-002/change_audit/change_audit_report.md` | 3720 | `113fc2fd00ba22e686ffd4a97b4e01288e0990ae7f0e8f16e94b324bf1ccacf3` |
| 5 | `whetstone_runs/facet-rendering-fr2-audit-002/patch-followup.md` | 3393 | `507694d94ccdc8d89e5016e69261342059d01a01e89727a5d1e0fae420973253` |
| 6 | `specs/installer-artifacts-v2.md` | 16498 | `953851820cd0a779330fce8182d67c1cd9bcac7bb2a30c40ea42307de9bdb1e7` |
| 7 | `specs/pack-format.md` | 11995 | `37d4747a13cdf854b3cc247277102675d8e3174621d82c52cc178170a39c38a6` |
| 8 | `specs/installer.md` | 39510 | `e065a632f4938c68b1c8c23b69e4e6374a8cdd9e26028a6711497ecffc78ca91` |
| 9 | `specs/compatibility.md` | 10319 | `352e68cb3e1b62f84f6e49a2a6e260e0db65f3c98133dcf27c3d392549743573` |
| 10 | `src/spine_packs/facet_manifest.py` | 7564 | `faacb961f31102d6a5c2d36a2d645460ac229370d8f08f9fce6cba7b84e0fccf` |
| 11 | `src/spine_packs/facet_planning.py` | 8333 | `134e6f825c455664cecbb03b73ddfc9d9b9547174e973ff09638d96380af8eba` |
| 12 | `src/spine_packs/facet_transport.py` | 4439 | `462afbc28d870d153dd000bcf3ee83017aeffffc693cc447812d4e6ecfd42103` |
| 13 | `src/spine_packs/facet_contracts.py` | 6249 | `0830a9b5726af69ac5a1e27347a9e35c822ae729c6a8c2bdb47fbc2182a4bd3a` |
| 14 | `src/spine_packs/facet_graph.py` | 8109 | `de23373085431e92bcb1e8ccc45bdaf5692f18dab25fd88e64bd228e322a630b` |
| 15 | `tests/runtime/test_facet_planning.py` | 22414 | `8c4351540b5c155cd159332f0aba250821df695ff3efd9d919fdf2e3c363315c` |
| 16 | `tests/contract/test_fr2_contract.py` | 7389 | `07d5205495a38540b59cb4f3f668f7e41868edf23fa926c862cca88fb1d00e3f` |
| 17 | `contracts/schemas/spine-pack-manifest.v2.schema.json` | 21307 | `a71fa1b2e020a47291132388424546c3ca917443519147ef175bcc5a3dc850d3` |
| 18 | `contracts/schemas/spine-readback-0.10.0.schema.json` | 19759 | `83af4190bbb1ceab9073b4471e8e60e1d24638f577f10f0b6e1fc416b844b08f` |
| 19 | `docs/fr2-qualification.md` | 8164 | `17d99cd6cc4fd1d33449c32791b7f83020d5069053469c6e3634d88b0e15a3b5` |
| 20 | `tests/fixtures/installer-v2/fr2-cross-root.json` | 157588 | `9e92e3538c1618d9832e189a90c72d9e456df0ffa0beb187b84dc57355614a3a` |

## Approval wording

“I approve sending the 20 files listed in this APPROVAL.md to the nested Codex reviewer for the focused FR-2 re-audit.”
