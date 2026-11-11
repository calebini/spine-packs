"""Independent v2 selected-state verification. Never apply, recovery or replay.

Captured response correlation is checksum evidence, not approval issuance or
independent receipt readback. Only the bounded public read surface is used.
"""
from copy import deepcopy

from .facet_contracts import artifact, body, seal
from .facet_execution import ExecutionContext, guarded, immutable_lineage, observation, validate_saved_plan
from .facet_observation import observe
from .planning import ENVIRONMENT, INVALID, PlanError, require

STALE = 'stale_plan_or_target_mismatch'


@guarded(INVALID)
def validate_verification_inputs(manifest, plan, result=None):
    validate_saved_plan(manifest, plan)
    if result is not None:
        require(isinstance(result, dict), 'invalid_apply_result', INVALID)
        # Outer shape/digest/size failures cannot be cited as an artifact identity.
        # Embedded semantic failures instead become coverage=invalid below.
        artifact(result, 'apply-result')


def response_coverage(manifest, plan, result):
    if result is None:
        return ('missing' if plan['actions'] else 'not_required'), []
    try:
        cp = result['checkpoint']
        # This unique closed checksum preimage neither grants approval nor
        # authenticates its author. It is never published or used to submit.
        approval = seal(dict(artifact_schema='spine.pack-install-approval.v2',
            plan_digest=plan['content_identity']['digest'], approve_complete_plan=True,
            acknowledge_single_operator=True, authorized_update_action_ids=plan['decision_action_ids'],
            execution=deepcopy(cp['execution'])))
        # Ineligible plans cannot claim even an empty applied execution. A
        # no-write draft can still verify state without a supplied result.
        context = ExecutionContext(manifest, plan, approval)
        artifact(cp, 'apply-checkpoint')
        require(cp['plan_digest'] == plan['content_identity']['digest']
                and cp['approval_digest'] == approval['content_identity']['digest']
                and cp['execution'] == approval['execution'], 'checkpoint_execution_mismatch', INVALID)
        accepted = cp['accepted_responses']
        context._prefix(accepted)
        require(not accepted or plan['apply_eligible'], 'ineligible_response_evidence', INVALID)
        immutable_lineage([*plan['observation']['entries'], *plan['observation']['historical_revisions'],
                           *[e['post_observation'] for e in accepted]])
        remaining = [a['action_id'] for a in plan['actions'][len(accepted):]]
        next_id = remaining[0] if remaining else None
        require(cp['next_action_id'] == next_id, 'checkpoint_next_action_mismatch', INVALID)
        pending = cp['unresolved_submission']
        if pending is not None:
            require(next_id is not None, 'completed_checkpoint_has_submission', INVALID)
            request = context.materialize(accepted)
            require(pending['action_id'] == next_id and pending['command_id'] == request['command_id']
                    and body(pending['request']) == request, 'checkpoint_request_mismatch', INVALID)
        state = result['state']
        if state == 'applied':
            require(not remaining and pending is None and result['failure'] is None
                    and result['unattempted_action_ids'] == [], 'applied_coverage_mismatch', INVALID)
        elif state == 'partial':
            require(bool(remaining) and result['failure']['action_id'] == next_id
                    and result['unattempted_action_ids'] == remaining[1:], 'partial_coverage_mismatch', INVALID)
        else:
            require(state == 'not_applied' and not accepted and pending is None
                    and result['failure'] is not None and result['failure']['action_id'] in (None, next_id)
                    and result['unattempted_action_ids'] == remaining, 'not_applied_coverage_mismatch', INVALID)
        coverage = 'not_required' if not plan['actions'] else 'complete' if state == 'applied' else 'missing'
        return coverage, deepcopy(accepted)
    except (PlanError, ValueError, KeyError, TypeError, IndexError, RecursionError, OverflowError):
        return 'invalid', []


def object_results(plan, fresh, accepted):
    expected = {r['object_key']: r for r in plan['observation']['entries']}
    expected.update({e['post_observation']['object_key']: e['post_observation'] for e in accepted})
    pending = {a['object_key'] for a in plan['actions'][len(accepted):]}
    pending.update(plan['blocked_object_keys'])
    rows = {r['object_key']: r for r in fresh['entries']}
    results = []
    for key in plan['closure']:
        row, desired = deepcopy(rows.get(key)), expected.get(key)
        if row is None:
            status = 'missing'
        elif row['status'] != 'active' or key in pending or desired is None:
            status = 'blocked'
        else:
            actual = deepcopy(row)
            if key.startswith('archetype:') or (key.startswith('profile:') and
                    actual['revision_contract'] == desired['revision_contract'] == 'spine.notification-profiles.v1'):
                actual['revision_id'] = desired['revision_id']
            if key.startswith('binding:'):
                actual['binding_id'] = desired['binding_id']  # Existing same-target v1 binding rule only.
            status = 'equivalent' if actual == desired else 'drifted'
        results.append(dict(object_key=key, state=status, observed=row))
    return results


def verify_installation(manifest, plan, transport, result=None, *, page_size=100):
    """Read-only selected-state verification; no approval or write authority."""
    manifest, plan, result = deepcopy((manifest, plan, result))
    validate_verification_inputs(manifest, plan, result)
    coverage, accepted = response_coverage(manifest, plan, result)
    require(transport.target == plan['request']['target'], 'verification_target_mismatch', STALE)
    environment, fresh = observe(transport, plan['request']['owner'], plan['closure'],
        page_size=page_size, content_contracts=manifest['compatibility']['spine_content_contracts'])
    require(environment == plan['environment'], 'verification_environment_mismatch', STALE)
    observation(fresh, plan['request']['owner'])
    immutable_lineage([*plan['observation']['entries'], *plan['observation']['historical_revisions'],
        *[e['post_observation'] for e in accepted], *fresh['entries'], *fresh['historical_revisions']], category=ENVIRONMENT)
    objects = object_results(plan, fresh, accepted)
    success = coverage in ('complete', 'not_required') and all(r['state'] == 'equivalent' for r in objects)
    value = seal(dict(artifact_schema='spine.pack-verification-result.v2',
        plan_digest=plan['content_identity']['digest'], apply_result_digest=(
            result['content_identity']['digest'] if result is not None and plan['actions'] else None),
        pack=deepcopy(plan['pack']), target=deepcopy(plan['request']['target']), environment=environment,
        observation=deepcopy(fresh), closure=deepcopy(plan['closure']), object_results=objects,
        response_evidence=coverage, receipt_readback='captured_responses_only_spine_0.10.0',
        disclosure='separate_operator_configuration_required', state='verified' if success else 'mismatch'))
    artifact(value, 'verification-result')
    return value
