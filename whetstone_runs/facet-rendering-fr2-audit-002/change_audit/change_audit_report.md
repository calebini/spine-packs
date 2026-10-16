# Change Audit Report

- verdict: needs_revision
- boundary_preserved: False
- failure_reason: None
- recommended_next_action: manual_patch
- source_feedback_path: /Users/Shared/Agent-Workspace/repos/personal/spine-packs/whetstone_runs/facet-rendering-fr2-audit-002/change_audit/change_audit_feedback.json

## In-Scope Feedback Counts

- blocker: 0
- major: 1
- minor: 2
- nit: 0

## In-Scope Findings

### feedback_001 - major

- claim: The planner can emit an apply-eligible plan whose proposed rendering revision necessarily exceeds the normative 8,192-byte public bound.
- evidence: facet_manifest.validate checks rendering text normalization and character limits but never checks rendering revision bytes. build_plan constructs and seals templates without checking their resolved byte bounds; artifact() validates only the outer schema, artifact size and digest. A normalized 2,000-character emoji description plus a 160-character emoji display name already exceeds 8,192 UTF-8 bytes before selections and resolved IDs are included, yet both strings satisfy the supplied manifest schema. An all-missing released graph therefore produces an eligible plan containing an impossible rendering create. rendering_semantics enforces the bound only for observed definitions, creating inconsistent treatment of desired and observed content.
- recommended_change: Reject rendering revisions that already exceed the bound before ID resolution, and validate resolved bounds during planning wherever observed IDs are available. Keep future generated IDs unresolved and retain the required final materialization check for the separately authorized execution slice. Add a focused oversized desired-rendering vector.

### feedback_002 - minor

- claim: Malformed revision-handler failures bypass contextual validation and are reported as ordinary Spine rejections.
- evidence: FacetSpineCommand.read validates revision_readback_143 only conditionally. If validation fails, it falls through to spine_command_rejection/spine_read_rejected. For example, referenced_row_not_found with field=facets and CLI exit 4 violates the pinned failure schema but becomes installer exit 8 rather than a malformed-output transport failure. A handler-shaped failure with an unsupported CLI exit similarly skips pairing validation. The focused test only asserts that the error is not referenced_revision_missing, so it does not enforce the specified malformed-output taxonomy.
- recommended_change: Reject malformed owning-handler envelopes and invalid exit pairings as transport_or_environment_failure. Distinguish separately recognized preflight failures before applying the handler schema, and assert the exact installer category for malformed-field and unsupported-exit vectors.

### feedback_003 - minor

- claim: Current normative cross-references still describe the successor as unimplemented and pinned to 0.9.1, conflicting with the FR-2 implementation boundary.
- evidence: pack-format.md says the v2 schema is authored for FR-1 review and 'installer support is not implemented.' installer.md introduces the linked proposal as a workflow for 'Spine 0.9.1/schema 19.' In contrast, architecture.md explicitly implements manifest-v2/request-v2 read-only plan, and compatibility.md requires exactly 0.10.0 while retaining 0.9.1 only for historical decoding. These opening paragraphs are current orientation statements, unlike the explicitly preserved historical evidence.
- recommended_change: Update only these current cross-reference paragraphs to identify exact 0.10.0 FR-2 read-only planning and explicitly retain the disabled successor apply/recovery/verify boundary. Preserve historical investigation and qualification records unchanged.
