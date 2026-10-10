# Approval request: FR-1 manifest-contract bounded audit

Status: staged only. No nested reviewer has been invoked.

## Proposed transmission

Approve sending exactly these 16 files (247,954 bytes), plus the standard Whetstone reviewer instructions/response schema, to the nested Codex reviewer through the app's embedded CLI.

- Workflow: one reviewer-only `audit-change`, profile `consistency`.
- Scope: first FR-1 manifest/schema/fixture increment only; not full FR-1 or runtime readiness.
- No Editor, automatic patching, source writes, ledger access, external browsing, deployment, commit, push or publication.
- Includes test-oracle and disposable-gate source plus focused upstream normalization excerpts; no entire source tree or private ledger/configuration.
- Product choices for real flight content and destination disclosure remain deferred.
- Recheck every exact byte hash before transmission. Any payload change requires renewed approval.
- At launch verify the embedded executable/model and use the nested read-only sandbox. Prior audit approval does not carry over.

## Exact payload

| File (repository-relative) | SHA-256 | Bytes |
| --- | --- | ---: |
| `whetstone_runs/facet-rendering-fr1-manifest-audit-001/audit-notes.md` | `9e7a2e86460eb9e3bd97a84d8ae7164d3ae4c9dcb90b60f5cebe27adb2828cee` | 5276 |
| `AGENTS.md` | `4bde9b65981a3d787e17b4d2d8eb37353a5e960f249c9c708c736a24c91df4e0` | 6165 |
| `specs/overview.md` | `a8e480affee439f5608097d6728a3a96b6765c4aa00f33617711b038bd0d92ab` | 2399 |
| `specs/architecture.md` | `4b8d77b0abd6a958d3b8bdc48b2ebaeafc75e4157f91ea1b9762b5f493d1404f` | 24969 |
| `specs/compatibility.md` | `11ee544c49dfb346e5572d54cb29eb82867136203c4c966dce7b750e37e2baa3` | 9449 |
| `specs/pack-format.md` | `bee633028513c1b26515ec6fd0c03e834bf968d73668fa24209a9b63686cb2ac` | 11922 |
| `specs/facet-rendering-packs.md` | `17627e5f9f22a389978bfd87c943360dc8bda857938b18e747de18e8e3576c24` | 35562 |
| `specs/implementation-plan.md` | `a43a79cebf432f805139fee2ed6356357d0ebe2c5668082e31d5926ccbbc23f5` | 22855 |
| `docs/facet-rendering-baseline.md` | `be2143347ed9869dac04e54cce363929eb819e1ca8d5f7eccd06000a361fa409` | 18181 |
| `contracts/schemas/spine-pack-manifest.v1.schema.json` | `e1769666de8f14b84d0c12e370bf97560c9f105cc3cc771a5a41466ae3f2d8d8` | 8201 |
| `contracts/schemas/spine-pack-manifest.v2.schema.json` | `6fafd08fb03be7d03acfe660fc85c983dfa18228c06ff6d3d122fa2e2f58f609` | 20998 |
| `contracts/pack-fixture-manifest.v2.json` | `b2829a2379d10c2a935fc476f570456673dea018332ef87a5f6f94d6dfcb40a6` | 21450 |
| `tests/fixtures/pack-manifest-v2/flight.json` | `ab58374779ea3c960aef2386ea522cd230b6d8a91df6d01c9730a84a807b7019` | 5705 |
| `tests/contract/test_facet_manifest_contract.py` | `5e58592fa608795e17413c1eff0253ff3c58e1c3b611b89af938130a49ad9370` | 10807 |
| `scripts/qualify_profile_v2_listing.py` | `5cc37a27add60a01b0745dc915f7089e8a20e99571fd9e822d64aea55c53342e` | 10478 |
| `whetstone_runs/facet-rendering-fr1-manifest-audit-001/spine-manifest-evidence.md` | `42854e01991fe7663084e0e463a8ddb56f3b18b761b598cf99aa7d3b7b7ac3e1` | 33537 |

## Local bookkeeping

`payload.json` and this approval document are local inventory/authorization aids,
not additional reviewer inputs. They do not assert that approval has been granted.
The original facet-rendering-spec-audit-001 remains unchanged.

## Approval wording

> I approve sending the 16 files listed in this APPROVAL.md to the nested Codex reviewer for the bounded FR-1 manifest-contract audit.
