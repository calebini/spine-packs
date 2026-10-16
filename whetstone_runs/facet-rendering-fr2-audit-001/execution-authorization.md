# Execution authorization — FR-2 bounded review

Operator approval: “I approve sending these 45 files to the nested Codex reviewer”.
Recorded: 2026-10-16T20:41:12.984184+00:00

This record supersedes staged-only wording in the unchanged approval, notes,
payload and launch checklist. It is a local control record, not reviewer input.

- Authorized: one reviewer-only `audit-change`, profile `consistency`, the exact
  45-file payload below plus standard Whetstone reviewer instructions/schema.
- No Editor, source patches, tests, unrelated reads, browsing, ledger access,
  successor apply/recovery/verify, deployment, publication, commit or push.
- Embedded CLI: `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`.
- Version: `0.162.0-alpha.17.2`.
- Executable SHA-256: `50ab38ba21d0d9f8346f32f41848382f15b556190f3c7a07e885a4fb73e379c8`.
- Model: `gpt-6.1-sol`, verified present in current local model cache. The older
  documented `gpt-5.5` default is absent and is not silently reused.
- Whetstone: exact commit `1b813be46236f53687f610907f5b207ce4d8c772`, clean export
  `/private/tmp/spine-packs-whetstone-fr2.Jw90lQ`; all 507 exported files byte-verified against Git.
  Unrelated Whetstone working-tree changes are excluded and untouched.
- Nested sandbox: read-only; web disabled; medium reasoning; ephemeral;
  `--ignore-rules` disables repository rule discovery. Reviewer prompt forbids
  unrelated tool/file access; no filesystem secrecy guarantee is inferred.
- One call, 900-second timeout; no automatic retry or editing workflow.
- APPROVAL.md SHA-256: `874273df33bd0468768537b2e515b1c98f91c24cc0f7d421dc9728a179e05599`.
- payload.json SHA-256: `e0437deea2e0fc251783bfcdad39b9bcf6ebeddcf2ed5fe99861c77ce4262de8`.

## Approved payload, reverified before launch

- `whetstone_runs/facet-rendering-fr2-audit-001/audit-notes.md` — `5a685fb261e551896745d3b8c91c925e9f13c5ea88301a62e415d3ed729c332b` (6871 bytes)
- `AGENTS.md` — `327b1c353b1a858bd0d3ba9d4bfbf639ab7d03009fcb667669fb90f6ba1c3076` (6764 bytes)
- `specs/overview.md` — `a8e480affee439f5608097d6728a3a96b6765c4aa00f33617711b038bd0d92ab` (2399 bytes)
- `specs/architecture.md` — `020ef8d0b7c0777e7177a1024f85927ed2aab158f1dd6c8a4d9909227e8fdf24` (26431 bytes)
- `specs/compatibility.md` — `352e68cb3e1b62f84f6e49a2a6e260e0db65f3c98133dcf27c3d392549743573` (10319 bytes)
- `specs/pack-format.md` — `bee633028513c1b26515ec6fd0c03e834bf968d73668fa24209a9b63686cb2ac` (11922 bytes)
- `specs/installer.md` — `cca13593c863dde3a1757511f72ef30ff19b878442defd40de2c0a20f6f5979b` (39397 bytes)
- `specs/installer-artifacts.md` — `e3f977e2cdc09c12993e4fa20e6da83e320d1635050c8f367429aa9f62e3769e` (33936 bytes)
- `specs/installer-artifacts-v2.md` — `7dc71d4810b23c91ae193a1c38eea5158335163862e8a354a61ae1b94844317a` (15506 bytes)
- `specs/facet-rendering-packs.md` — `d84c8b16accc0abce76a38a7b5b75529d9ac2c2830ac2b18a4b05ba9586fcdcd` (36533 bytes)
- `specs/implementation-plan.md` — `7d5502fea2420aac44dd59ac558810450d6ef5587e2eabf237ac2dd0f720ea6b` (25622 bytes)
- `docs/facet-rendering-baseline.md` — `549cc3705b19252a7d7d800675a3bb5bf6ad833bbf475280d5ad962b3ed1b61c` (19489 bytes)
- `docs/fr2-historical-facet-readback-gap.md` — `2dfc9a9e554896f37f99e402ce542d0eccb33326adfd24f725899c0374daf780` (5662 bytes)
- `docs/fr2-qualification.md` — `bff83304f24c8929776724d22921ab5a603273a103033741cd73f8b5f7fb6724` (7018 bytes)
- `contracts/installer-spine-0.10.0-inventory.json` — `e4694cfa53fd274df466420cbcca69af71da704a7917381c90f07bfc9a30d2a2` (29205 bytes)
- `contracts/installer-spine-0.9.1-inventory.json` — `5837583b796de6b9f9fc90ea511851b271cdbdfcb63fc6a0028e54bc5003282a` (25860 bytes)
- `contracts/schemas/spine-pack-manifest.v2.schema.json` — `a71fa1b2e020a47291132388424546c3ca917443519147ef175bcc5a3dc850d3` (21307 bytes)
- `contracts/schemas/spine-pack-installer-types.v2.schema.json` — `028d901867ee10346078c886bfbf78939559332939611d39e503d53e6e3bfdaf` (43821 bytes)
- `contracts/schemas/spine-pack-install-request.v2.schema.json` — `ee241dc6b97afdf53e974a1847791ddbb9dfbabebe464c5e148bec77f4f18f6b` (240 bytes)
- `contracts/schemas/spine-pack-install-plan.v2.schema.json` — `b9ee69ee49e24846e985651d546ecb3d1ff3a51c0d646ac27685fb210fb1bc9f` (234 bytes)
- `contracts/schemas/spine-pack-installer-result.v2.schema.json` — `7788964b91aa95fc9737fd482136eaab828bf405814382a354e653c8846b34a7` (242 bytes)
- `contracts/schemas/spine-pack-embedded-values.v2.schema.json` — `97d6aefb03028ce25bb7045d56da5d516297b3ac43399c7080029bffb7f18b5f` (882 bytes)
- `contracts/schemas/spine-readback-0.10.0.schema.json` — `83af4190bbb1ceab9073b4471e8e60e1d24638f577f10f0b6e1fc416b844b08f` (19759 bytes)
- `contracts/schemas/spine-readback-0.9.1.schema.json` — `90471d1674233e7b3d47575adf085c4095ddfecc92f1f2e7833f4be56d7d4204` (123676 bytes)
- `src/spine_packs/facet_contracts.py` — `0830a9b5726af69ac5a1e27347a9e35c822ae729c6a8c2bdb47fbc2182a4bd3a` (6249 bytes)
- `src/spine_packs/facet_graph.py` — `f8b2c228394951ca19b0977835d00afe2a789331d5b6c5919ce2c221a5b106d4` (8111 bytes)
- `src/spine_packs/facet_inventory.py` — `ce03c3d6549dfe4cd5ebcb2fbe4af3fde0810c99fa552ce09d932e43eadf050e` (5810 bytes)
- `src/spine_packs/facet_manifest.py` — `7a38f87ef6b022ec8ce1517bd5baae5d79772e9670c74905311ff851f4b67bee` (6675 bytes)
- `src/spine_packs/facet_observation.py` — `3220a0ec918527b68a585bf3969e2c8a13b7e90b8ed4c0b31d80507e2bf5225f` (20838 bytes)
- `src/spine_packs/facet_planning.py` — `cd0f264978be5dd582845ac8c0fdfe2eb45def4925b18c46862bb916500e78b1` (7876 bytes)
- `src/spine_packs/facet_transport.py` — `07902e517df9afb19193038177d731dea61fec10587840f7a97ff6dc55fb2442` (3866 bytes)
- `src/spine_packs/__main__.py` — `6d9817dbb0b1e9ba7fd2ed1c4ece460e1aeb31ac995ccf20df15f02d9d5c297d` (10491 bytes)
- `src/spine_packs/spine_command.py` — `00c0c445b82a25ba74d024fd2f75a13b5206c71bef4db8de38ba1e93a0ba1a24` (7248 bytes)
- `src/spine_packs/artifacts.py` — `6a3333f53f89f7fee00f2dafd0ede70ff112271c82b54d0045f11d358aec42d9` (34285 bytes)
- `src/spine_packs/planning.py` — `445493754591cb04953b235b6d8bb4ee3e6276d1fb4cf7eb348857a4a2e370ae` (19304 bytes)
- `tests/contract/test_fr2_contract.py` — `7fcf9db9d21cfdda1951858c66cbc327f96ab9e6b8b1e15981812425a065ad91` (5968 bytes)
- `tests/contract/facet_artifact_oracle.py` — `7ba9de980c43c0fdf35ddc57746885e4765a174a426c07f07090de8c6ae004bd` (37913 bytes)
- `tests/contract/test_facet_manifest_contract.py` — `5e58592fa608795e17413c1eff0253ff3c58e1c3b611b89af938130a49ad9370` (10807 bytes)
- `tests/runtime/test_facet_planning.py` — `5334a9766fa6ccf3afba003f1a5371af49ed087cc4920a3f6c3c6fad5a59d33a` (16392 bytes)
- `tests/fixtures/installer-v2/fr2-cross-root.json` — `9e92e3538c1618d9832e189a90c72d9e456df0ffa0beb187b84dc57355614a3a` (157588 bytes)
- `tests/fixtures/installer-v2/revision-readback-0.10.0.json` — `f9f07c4222115f5f43aeb0233b3d21e5b0a9f02a3fa0aa434042de16cbc45361` (15984 bytes)
- `tests/fixtures/installer-v2/flight-create.json` — `22b8a79711c58ce1ca7331dc906679fecba7f32ca5f733e33dbcbb7748d05dee` (148927 bytes)
- `scripts/qualify_fr2.py` — `ff0e7f2c9f3cf68cf383ac9aba2de8bef8d43b30e602280def762659f761906c` (14558 bytes)
- `scripts/build_fr2_contracts.py` — `fb365d419c898cb1bc1fccfda899a763a65f920015810a622e3f9ac36bc4e48c` (5873 bytes)
- `pyproject.toml` — `93a4d5b6893e61bd8a36d3df19c0f7a927ba52d911c13dcf5103b848a2e7f101` (1187 bytes)
