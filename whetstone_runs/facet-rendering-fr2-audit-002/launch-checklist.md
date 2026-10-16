# FR-2 reduced retry launch checklist — NOT AUTHORIZED

The only requested operation so far is staging. Stop for explicit payload approval.
No `execution-authorization.md` or `change_audit/` result exists yet.

After approval:

1. Rehash every entry in `payload.json`; require exact count, paths, sizes and
   hashes matching `APPROVAL.md`. If anything changed, stop for renewed approval.
2. Resolve and verify the embedded Codex executable, its version/hash and locally
   available model. Do not silently reuse a stale executable/model from an old
   audit. Record actual Whetstone source pin and clean isolated export, client
   identity and approved scope in a separate local execution authorization file.
3. Confirm supported `audit-change` flags on that executing Whetstone export.
   Stage only the approved input bytes. Keep nested sandbox read-only, web search
   disabled and unrelated repository instruction/file discovery disabled. Do not
   expose cursor configs, ledger files or temporary qualification directories.
4. Request the required execution escalation for the nested CLI. Do not burn a
   first attempt on a known session-access sandbox failure. Invoke exactly one
   reviewer-only audit with `--root` this directory, `--notes` its audit-notes.md,
   repeated `--spec` operands for all other payload entries in order,
   `--profile consistency`, `--client codex`, verified `--command`, `--model`,
   `--client-version` and bounded `--timeout-seconds 900`. No Editor or Phase 1/2.
5. Inspect the persisted change_audit manifest/feedback/report. Treat setup/client
   failures as infrastructure, not spec findings; preserve evidence. Do not retry,
   patch, commit or push automatically. Report actionable findings and scope limits.

The installed Whetstone CLI's local help was inspected during staging. No launch
config, fake review report or inferred approval is created by this checklist.

Before launch also reproduce the assembled prompt-size check in payload.json.
Preserve failed attempt 001; never overwrite or treat it as semantic feedback.
