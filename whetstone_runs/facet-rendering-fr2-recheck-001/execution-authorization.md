# Execution authorization — focused FR-2 recheck

Operator approval: “I approve sending the 20 files listed in APPROVAL.md to the nested Codex reviewer”.

This control record supersedes the staged-only status in the unchanged approval,
notes and checklist. It is NOT additional reviewer input.

- Exactly one reviewer-only audit-change, profile consistency, of the 20 files
  below plus standard Whetstone reviewer instructions and output schema.
- Candidate: be64a9c9c42ed7816caca7b78b68283149044be5.
- Whetstone: exact commit 1b813be46236f53687f610907f5b207ce4d8c772;
  fresh isolated export /private/tmp/spine-packs-fr2-recheck-whetstone.bikDpu.
  All 1,230 Git-tracked exported files verified byte-for-byte. The previous
  temporary export was incomplete; it was not used to execute this review.
- Embedded CLI: /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex.
  Version 0.162.0-alpha.17.2; SHA-256
  50ab38ba21d0d9f8346f32f41848382f15b556190f3c7a07e885a4fb73e379c8.
- Model gpt-6.1-sol confirmed in local available-model cache; medium reasoning.
- Nested client sandbox read-only, web disabled, ignore-rules, ephemeral.
  Working directory is this isolated audit root; no unrelated reads/tools or
  test execution permitted by the approved review instructions.
- Prompt reproduced unchanged: 405,296 characters / 405,338 UTF-8 bytes,
  SHA-256 23cf18bf14d860a02bbfb8815489947572b527e4322f188473dfe7e714f498f7.
- Timeout 900 seconds. No automatic retry, Editor, source edits, successor
  apply/recovery/verify, ledger access, deployment, publication, commit or push.
- Required nested-client execution escalation will be requested before invocation.

Recorded UTC: 2026-10-16T22:39:54.064425+00:00

APPROVAL.md SHA-256: `3ae046ca04cc9eebfa0b10912296a70e2f1208bf32a7da34bc19c29133275f82`.

payload.json SHA-256: `a089fdc0c8752c034be2f95e1a5318f5ef4e4baf3626521e98486315e0f9c19e`.

## Exact approved transmission files

- `whetstone_runs/facet-rendering-fr2-recheck-001/audit-notes.md` — `b7bb5f8b6d77a6eb6706e95d9464b4d073cb85512d09d5370952c4034c003b33` (5487 bytes)
- `whetstone_runs/facet-rendering-fr2-recheck-001/review-context.md` — `0ab2c44051bef9204bacd3cac13dadab1bab39089a0d6bdec283c1881515c371` (28414 bytes)
- `AGENTS.md` — `327b1c353b1a858bd0d3ba9d4bfbf639ab7d03009fcb667669fb90f6ba1c3076` (6764 bytes)
- `whetstone_runs/facet-rendering-fr2-audit-002/change_audit/change_audit_report.md` — `113fc2fd00ba22e686ffd4a97b4e01288e0990ae7f0e8f16e94b324bf1ccacf3` (3720 bytes)
- `whetstone_runs/facet-rendering-fr2-audit-002/patch-followup.md` — `507694d94ccdc8d89e5016e69261342059d01a01e89727a5d1e0fae420973253` (3393 bytes)
- `specs/installer-artifacts-v2.md` — `953851820cd0a779330fce8182d67c1cd9bcac7bb2a30c40ea42307de9bdb1e7` (16498 bytes)
- `specs/pack-format.md` — `37d4747a13cdf854b3cc247277102675d8e3174621d82c52cc178170a39c38a6` (11995 bytes)
- `specs/installer.md` — `e065a632f4938c68b1c8c23b69e4e6374a8cdd9e26028a6711497ecffc78ca91` (39510 bytes)
- `specs/compatibility.md` — `352e68cb3e1b62f84f6e49a2a6e260e0db65f3c98133dcf27c3d392549743573` (10319 bytes)
- `src/spine_packs/facet_manifest.py` — `faacb961f31102d6a5c2d36a2d645460ac229370d8f08f9fce6cba7b84e0fccf` (7564 bytes)
- `src/spine_packs/facet_planning.py` — `134e6f825c455664cecbb03b73ddfc9d9b9547174e973ff09638d96380af8eba` (8333 bytes)
- `src/spine_packs/facet_transport.py` — `462afbc28d870d153dd000bcf3ee83017aeffffc693cc447812d4e6ecfd42103` (4439 bytes)
- `src/spine_packs/facet_contracts.py` — `0830a9b5726af69ac5a1e27347a9e35c822ae729c6a8c2bdb47fbc2182a4bd3a` (6249 bytes)
- `src/spine_packs/facet_graph.py` — `de23373085431e92bcb1e8ccc45bdaf5692f18dab25fd88e64bd228e322a630b` (8109 bytes)
- `tests/runtime/test_facet_planning.py` — `8c4351540b5c155cd159332f0aba250821df695ff3efd9d919fdf2e3c363315c` (22414 bytes)
- `tests/contract/test_fr2_contract.py` — `07d5205495a38540b59cb4f3f668f7e41868edf23fa926c862cca88fb1d00e3f` (7389 bytes)
- `contracts/schemas/spine-pack-manifest.v2.schema.json` — `a71fa1b2e020a47291132388424546c3ca917443519147ef175bcc5a3dc850d3` (21307 bytes)
- `contracts/schemas/spine-readback-0.10.0.schema.json` — `83af4190bbb1ceab9073b4471e8e60e1d24638f577f10f0b6e1fc416b844b08f` (19759 bytes)
- `docs/fr2-qualification.md` — `17d99cd6cc4fd1d33449c32791b7f83020d5069053469c6e3634d88b0e15a3b5` (8164 bytes)
- `tests/fixtures/installer-v2/fr2-cross-root.json` — `9e92e3538c1618d9832e189a90c72d9e456df0ffa0beb187b84dc57355614a3a` (157588 bytes)
