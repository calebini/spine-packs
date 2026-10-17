# FR-3 minor finding patch

Finding: `fr3-consistency-001`. Operator authorization: “Okay, go ahead and patch.”

The independent test oracle now requires response `facet_key` and
`facet_schema_revision_id` to equal both the exact submitted request and the
post-observation. This implements the existing evidence-correlation contract;
it introduces no new schema, runtime command or compatibility policy.

One focused regression test covers both fields in both create and update flows.
Each mutation has a schema-valid replacement, resealed response digest and
receipt projection, with unchanged request and readback. All four cases failed
before the oracle patch because no error was raised. After the patch, all four
are rejected by the specific field-correlation check; original evidence passes.

## Verification

- Focused FR-3 suite: 9 tests passed, no skips.
- Complete official Draft 2020-12 contract suite: 99 tests passed, no skips.
- Required system-Python contract suite: 99 tests ran, 34 skipped due to missing
  development `jsonschema`; the official suite above supplies the complete gate.
- Complete runtime suite: 142 tests passed, no skips.
- Repository verifier: passed, 166 required files.
- Historical 0.9.1 and refreshed 0.10.0 create/update fixture hashes: all four
  unchanged against the committed index.
- Whitespace checks: passed.

The original approval, payload, audit brief, report, feedback and disposition
remain unchanged historical evidence. Their source hashes intentionally describe
the pre-patch candidate. No external re-audit was run or approved for these new
bytes. The component-scaffold guidance kept the repair in the existing test
oracle and contract tests, with status documentation only.

No runtime code, fixture bytes, schemas, released packs or Spine files changed.
No ledger access, write enablement, commit or push. After the local gate passes,
the next implementation work remains FR-3 initial apply, not FR-4 recovery/verify.
