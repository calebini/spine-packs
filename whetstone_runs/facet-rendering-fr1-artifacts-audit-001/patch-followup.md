# fb_001 patch follow-up

Date: 2026-10-11. The operator authorized the narrow fix after the bounded
review. The original payload, brief, feedback and disposition remain historical
evidence of the reviewed bytes; this patch has not been externally re-audited.

## Changes

- Split `schema:<key>` from the hyphen-capable catalog-key alternative at all
  ten locations in the shared v2 installer artifact schema. Facet schema keys
  now require `[a-z][a-z0-9_]{0,63}`.
- Added eight indexed positive/negative key vectors and a focused test applying
  them to all ten locations (80 assertions). Ordinary catalog keys and the
  archetype portion of facet-binding keys still accept hyphens; facet schema
  portions do not. This aligns the schema with the existing normative grammar.
- No runtime, manifest, released-pack or Spine changes. The scaffold convention
  kept the fix confined to the existing contract and test files.

Only these three approved-payload source files changed after review:

| File | Patched SHA-256 |
| --- | --- |
| `contracts/installer-fixture-manifest.v2.json` | `d51ff079bb1ca14324f066ac156235e91dcc26ff024ebdd2db5af1a51fbe84e7` |
| `contracts/schemas/spine-pack-installer-types.v2.schema.json` | `0bc77236aff4cfbfefe03a855531c2150583f01d7362e590ee2a67b3ea41bc50` |
| `tests/contract/test_facet_artifact_contract.py` | `9de8ac5d06aa2c75ecb4ed1c533046d03e53cc77b15f2d5e6771ee3bd091a69c` |

The original brief still hashes to
`2a2e2ecda65e14992fd7031270049515e3d6fae6f92a23323891562e21b4fcfa`.

## Checks

- Repository verifier: passed, 143 required files.
- Focused artifact suite with isolated official JSON Schema validator: 13 passed.
- Complete contract suite with that validator: 83 passed, no skips.
- Default Python contract suite: 83 discovered, 18 skipped because the optional
  development JSON Schema dependency is unavailable in that interpreter.
- Runtime suite: 126 passed.
- Tracked diff and changed untracked-file whitespace checks: passed.

Finding `fb_001` is addressed locally. No commit, push, reviewer rerun, ledger
operation, deployment or publication was performed. Package qualification remains
deferred as recorded in the original audit notes; these checks do not qualify
the successor installer runtime or authorize release.
