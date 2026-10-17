# FR-3 contract gate launch checklist

Status: staged only. No reviewer has been invoked; no payload approval received.

1. Obtain explicit approval for the exact files/hashes in APPROVAL.md. Earlier
   FR-2 approvals do not carry over. Recheck candidate commit, every raw file
   hash/size and payload count; changed bytes require renewed approval.
2. Verify a clean Whetstone export, supported audit-change help, embedded Codex
   executable/version/hash and available model before launch. The staging-only
   prompt measurement may use the previous pinned clean export, not as proof
   that the later execution environment is intact or authorized.
3. Record approval and execution identity in a separate local control record.
   Only audit-notes and the other listed payload files, plus standard reviewer
   instructions/output schema, may be transmitted. APPROVAL.md, payload.json
   and this checklist are control records, not additional reviewer input.
4. Reproduce the pure assembled-prompt measurement; stay below the previously
   observed 1,048,576-character limit. Do not include prior failed prompt echoes.
5. Request nested-client execution escalation before running. Use an isolated
   run root, read-only reviewer, web disabled and repository instruction
   discovery disabled. No unapproved reads, commands, tools or tests.
6. Run one reviewer-only `audit-change --profile consistency` with the notes and
   all other approved files in payload order; use verified client/executable/
   model/version and a 900-second timeout. No Editor or automatic retries.
7. Inspect persisted manifest/feedback/report and recheck input hashes. Setup
   failures are not semantic findings. Report the verdict without automatic
   patches, runtime enablement, commit, push or convergence/release claims.
