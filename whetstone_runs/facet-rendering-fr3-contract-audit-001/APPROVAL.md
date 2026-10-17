# Approval request — FR-3 initial-apply contract gate

Status: **NOT APPROVED; no reviewer invoked.**
Candidate commit: `97e09b5db6bff382e1c69054a8db1f961c35a225`.

Approve one reviewer-only Whetstone `audit-change` consistency pass through the
embedded Codex CLI, sending exactly the **15 files** below plus standard
reviewer instructions/output schema. Scope: the exact-0.10.0 initial-apply
fixture refresh and its contract tests, before runtime executor implementation.

Payload: **442,466 bytes**. Locally assembled prompt:
**449,380 characters**, below the previously observed 1,048,576-character
CLI limit. Revalidate executable/model/config and prompt size before launch.

This payload includes synthetic fixture requests/responses, test helper/oracle
source and unchanged read-only planning source for static parity review. It
contains no live ledger, credentials, cursor secrets or operator configuration.
Unchanged schema closures and historical fixture bodies are deliberately omitted;
the reviewer must not claim to inspect them or follow imports to fetch them.
No Editor, tools, shell execution, browsing, tests, unrelated reads, automatic
patches, write enablement, commit, push, deployment or publication is authorized.
A clean audit is not convergence or runtime/package qualification.

Only the listed raw bytes are proposed for transmission. Changed bytes need new
approval; prior FR-2 approvals do not apply. This approval, payload.json and the
launch checklist are local control records, not additional reviewer input.

## Exact proposed files

| # | Repository-relative path | Bytes | SHA-256 |
| ---: | --- | ---: | --- |
| 1 | `whetstone_runs/facet-rendering-fr3-contract-audit-001/audit-notes.md` | 4581 | `629e3e1035b3bb0eb97a8f6ec2359c55cdf53f6f932b65ac014172f9013c7204` |
| 2 | `AGENTS.md` | 7000 | `c8953e3a4e4de4e81bddbf6e22f35e854b56bec5eacb4ea1fa9d58c98c0b2898` |
| 3 | `specs/installer-artifacts-v2.md` | 17558 | `665bbbc3d455c64dbecf37e05a260ed8db7d0541f297fd53ea9be018c76907be` |
| 4 | `specs/facet-rendering-packs.md` | 36533 | `d84c8b16accc0abce76a38a7b5b75529d9ac2c2830ac2b18a4b05ba9586fcdcd` |
| 5 | `specs/implementation-plan.md` | 27094 | `e17b53d929c31e373f45098a013848b2c0ed4593551314c6afc57174be667173` |
| 6 | `docs/fr3-initial-apply-readiness.md` | 4066 | `7cf161353b16bbc558b47a4a9564048fc65b416badcac37062efc154c30f432a` |
| 7 | `contracts/installer-spine-0.10.0-inventory.json` | 29205 | `e4694cfa53fd274df466420cbcca69af71da704a7917381c90f07bfc9a30d2a2` |
| 8 | `contracts/installer-fr3-fixture-manifest.v2.json` | 1693 | `8c6f83fb688d91d94222ddf9a675b01a68895835eb17c7eb816a63653dd660af` |
| 9 | `tests/contract/fr3_fixture_support.py` | 5849 | `d7d022a17c440b193546b05cfb520d6b31799709e8f9dac296f174c455aea228` |
| 10 | `tests/contract/test_fr3_artifact_contract.py` | 9485 | `4bab7719fefabb8faf0002b338a98cbbe0416d81b9a79cdc071ffa97ae3d548c` |
| 11 | `tests/contract/facet_artifact_oracle.py` | 37913 | `7ba9de980c43c0fdf35ddc57746885e4765a174a426c07f07090de8c6ae004bd` |
| 12 | `tests/contract/test_facet_manifest_contract.py` | 10807 | `5e58592fa608795e17413c1eff0253ff3c58e1c3b611b89af938130a49ad9370` |
| 13 | `tests/fixtures/installer-v2/flight-create-0.10.0.json` | 108110 | `9e3e586c95c69e7cdcf944b135fd1e8f52d938dbcc5953f94cb62a82d1945065` |
| 14 | `tests/fixtures/installer-v2/flight-update-0.10.0.json` | 134239 | `ce240e8aec27474e3e086d512eb76ec9766f08250c3b057567773d67a940a146` |
| 15 | `src/spine_packs/facet_planning.py` | 8333 | `134e6f825c455664cecbb03b73ddfc9d9b9547174e973ff09638d96380af8eba` |

## Approval wording

“I approve sending the 15 files listed in this APPROVAL.md to the nested Codex reviewer for the FR-3 contract gate.”
