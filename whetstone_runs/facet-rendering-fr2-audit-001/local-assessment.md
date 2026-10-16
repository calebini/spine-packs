# FR-2 audit attempt 001 — infrastructure failure

The approved 45-file audit was attempted once on 2026-10-16. The embedded CLI
rejected `turn/start` before semantic review:

- `input_too_large`: maximum 1,048,576 characters; actual 1,071,799.
- Whetstone verdict: `audit_failed`; boundary preservation is unknown.
- No reviewer feedback was produced. Zero finding counts are not a passing audit.
- The failed report includes the CLI's echoed prompt and is large; preserve it
  as evidence, not as an additional payload for another review.

All 45 approved raw SHA-256 hashes remain unchanged. Whetstone's manifest uses
its documented normalized draft hash, not always raw-byte SHA-256. Two source
files contain pre-existing whitespace; their normalized hashes were independently
rechecked and match. The initial raw-versus-normalized comparison failed because
of that representation distinction, not because source content changed.

No automatic retry, source patch, commit or push occurred. A separate attempt
002 is staged for renewed approval, omitting the 148,927-byte historical
flight-create fixture and explaining that evidence limit in its new notes.
The new cross-root fixture includes the synthetic manifest/request, public read
responses and expected plan needed for the focused FR-2 planner review. Runtime
execution/recovery fixtures remain outside this audit's scope.
