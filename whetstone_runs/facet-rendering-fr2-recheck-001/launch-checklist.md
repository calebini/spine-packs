# FR-2 focused recheck launch checklist

Status: staged, NOT approved for transmission; no reviewer invoked.

1. Obtain affirmative approval for the exact APPROVAL.md payload. Recheck every
   listed raw byte hash and size, candidate commit, and payload count before use.
   Changed content requires renewed approval. Preserve all earlier audit roots.
2. Verify a clean Whetstone export and embedded Codex executable/version/hash
   and available model before launch; do not blindly reuse prior client facts.
   The supported audit-change help was inspected using the prior clean export
   `/private/tmp/spine-packs-whetstone-fr2.Jw90lQ` (pin
   `1b813be46236f53687f610907f5b207ce4d8c772`). Reverify it before execution.
3. Record the user approval and actual execution identity separately. Use only
   approved file bytes plus standard reviewer prompt/output schema. The local
   payload/approval/checklist files are control records, not extra reviewer input.
4. Reproduce the pure in-memory assembled-prompt size check recorded in
   payload.json. No client is required for this check. Keep well below the
   observed 1,048,576-character CLI limit. Do not include failed-attempt reports
   that echo the earlier full prompt.
5. Request required nested-client execution escalation before launch. Keep the
   reviewer read-only, web disabled, repository instruction discovery disabled,
   and use the isolated run root. No unrelated files, credentials, cursor
   configuration or qualification ledgers may be exposed as payload.
6. Invoke exactly one reviewer-only audit-change, --profile consistency,
   --notes audit-notes.md and --spec for each other approved file in payload
   order, verified --client codex/--command/--model/--client-version, and
   --timeout-seconds 900. No Editor, tests, automatic source patch, commit or push.
7. Inspect persisted manifest, feedback and report. Setup failures are not
   semantic findings. Preserve evidence and report results without automatic
   retries or claiming convergence, release readiness or FR-3 authorization.
