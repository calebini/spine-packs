# Execution authorization — FR-3 contract gate

Operator approval: “I approve sending those files to the nested Codex reviewer”.
This refers to the 15-file APPROVAL.md presented immediately before approval.
This local control record supersedes staged-only status; it is NOT reviewer input.

- One reviewer-only Whetstone audit-change, profile consistency; no Editor/retry.
- Candidate: 97e09b5db6bff382e1c69054a8db1f961c35a225.
- Spine baseline: 8f3c50b6fd1b4aa534e50925b7417a7a80d19122, 0.10.0/schema 19.
- Whetstone pin: 1b813be46236f53687f610907f5b207ce4d8c772, isolated export
  /private/tmp/spine-packs-fr2-recheck-whetstone.bikDpu. All 1,230 tracked
  exported files were reverified against exact Git blob hashes before launch.
- Embedded CLI: /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex,
  version 0.162.0-alpha.17.2, SHA-256
  50ab38ba21d0d9f8346f32f41848382f15b556190f3c7a07e885a4fb73e379c8.
- Model gpt-6.1-sol confirmed in available-model cache; medium reasoning.
- Read-only sandbox, web disabled, ignore-rules, ephemeral. Working directory
  is this isolated audit root. No tools, extra reads or test execution permitted.
- Exact prompt reproduced: 449,380 characters / 449,408 UTF-8 bytes; SHA-256
  6ae4b8199ff282dcd75d289f19243147f40479fe2c8952f6fdbc3bc3ba4022d1.
- Timeout 900 seconds; required nested-client escalation requested before launch.
- No source edits, executor enablement, ledgers, runtime writes, disclosure,
  items, reminders, sends, deployment, publication, commit or push.

Recorded UTC: 2026-10-17T07:23:52.667050+00:00

APPROVAL.md SHA-256: `bd20f0f5fc2620ffbff9393b64ffcc7fde339920e554a404ba27cb4769c9b90a`.

payload.json SHA-256: `c0f98baf8ba602e362dd0d609028e9f9f5630e22d248ee49303c7fbbcfe72796`.

## Exact approved transmission files

- `whetstone_runs/facet-rendering-fr3-contract-audit-001/audit-notes.md` — `629e3e1035b3bb0eb97a8f6ec2359c55cdf53f6f932b65ac014172f9013c7204` (4581 bytes)
- `AGENTS.md` — `c8953e3a4e4de4e81bddbf6e22f35e854b56bec5eacb4ea1fa9d58c98c0b2898` (7000 bytes)
- `specs/installer-artifacts-v2.md` — `665bbbc3d455c64dbecf37e05a260ed8db7d0541f297fd53ea9be018c76907be` (17558 bytes)
- `specs/facet-rendering-packs.md` — `d84c8b16accc0abce76a38a7b5b75529d9ac2c2830ac2b18a4b05ba9586fcdcd` (36533 bytes)
- `specs/implementation-plan.md` — `e17b53d929c31e373f45098a013848b2c0ed4593551314c6afc57174be667173` (27094 bytes)
- `docs/fr3-initial-apply-readiness.md` — `7cf161353b16bbc558b47a4a9564048fc65b416badcac37062efc154c30f432a` (4066 bytes)
- `contracts/installer-spine-0.10.0-inventory.json` — `e4694cfa53fd274df466420cbcca69af71da704a7917381c90f07bfc9a30d2a2` (29205 bytes)
- `contracts/installer-fr3-fixture-manifest.v2.json` — `8c6f83fb688d91d94222ddf9a675b01a68895835eb17c7eb816a63653dd660af` (1693 bytes)
- `tests/contract/fr3_fixture_support.py` — `d7d022a17c440b193546b05cfb520d6b31799709e8f9dac296f174c455aea228` (5849 bytes)
- `tests/contract/test_fr3_artifact_contract.py` — `4bab7719fefabb8faf0002b338a98cbbe0416d81b9a79cdc071ffa97ae3d548c` (9485 bytes)
- `tests/contract/facet_artifact_oracle.py` — `7ba9de980c43c0fdf35ddc57746885e4765a174a426c07f07090de8c6ae004bd` (37913 bytes)
- `tests/contract/test_facet_manifest_contract.py` — `5e58592fa608795e17413c1eff0253ff3c58e1c3b611b89af938130a49ad9370` (10807 bytes)
- `tests/fixtures/installer-v2/flight-create-0.10.0.json` — `9e3e586c95c69e7cdcf944b135fd1e8f52d938dbcc5953f94cb62a82d1945065` (108110 bytes)
- `tests/fixtures/installer-v2/flight-update-0.10.0.json` — `ce240e8aec27474e3e086d512eb76ec9766f08250c3b057567773d67a940a146` (134239 bytes)
- `src/spine_packs/facet_planning.py` — `134e6f825c455664cecbb03b73ddfc9d9b9547174e973ff09638d96380af8eba` (8333 bytes)
