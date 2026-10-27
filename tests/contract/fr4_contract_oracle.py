"""Pure FR-4 contract oracle; not an installer, transport, or approval issuer.

Run under fr3_fixture_support.current_contracts(). No src/spine_packs imports.
Admission, replay correlation and verification are deliberately separate so a
provisional public identity can never masquerade as an accepted response.
"""
from copy import deepcopy

import facet_artifact_oracle as o
from fr3_fixture_support import plan_check
from fr4_fixture_support import RECEIPT

try:
    from jsonschema.exceptions import ValidationError
except ImportError:
    ValidationError = ValueError  # Discovery still works without development dependencies.


def lineage(rows):
    known = {}
    for row in rows:
        if row['revision_id'] is None:
            continue
        value = o.unblob(row['value'])
        # Profile metadata belongs to the mutable root, not the revision.
        if row['object_key'].startswith('profile:'):
            value = value['revision']
        identity = (row['root_id'], row['revision_contract'], value)
        revision = row['revision_id']
        o.require(revision not in known or known[revision] == identity,
                  'immutable revision identity/content')
        known[revision] = identity


def evidence_check(plan, approval, action, evidence, prefix):
    o.evidence_check(plan, approval, action, evidence, prefix)
    post = evidence['post_observation']
    o.require(post['status'] == 'active', 'accepted post status')
    response = o.unblob(evidence['response'], True)
    cmd = action['command']
    if action['expected'] and 'revision' in o.COMMANDS[cmd]['outputs']:
        if not response['effect'].endswith('noop'):
            o.require(post['revision_id'] != action['expected']['revision_id'],
                      'immutable preimage revision reused')
    if cmd == 'notification_profile.metadata.update':
        o.require(response['notification_profile_revision_id'] == post['revision_id'] ==
                  action['expected']['revision_id'] and
                  post['revision_contract'] == action['expected']['revision_contract'],
                  'metadata revision identity')
    lineage(plan['observation']['entries'] + plan['observation']['historical_revisions'] +
            [e['post_observation'] for e in prefix] + [post])


def checkpoint_check(plan, approval, cp):
    o.checkpoint_check(plan, approval, cp)
    for n, e in enumerate(cp['accepted_responses']):
        evidence_check(plan, approval, plan['actions'][n], e, cp['accepted_responses'][:n])


def candidate_check(plan, approval, cp, row, record=None):
    n = len(cp['accepted_responses'])
    action = plan['actions'][n]
    request = o.materialize(plan, approval, action, cp['accepted_responses'])
    cmd = action['command']
    o.validate_state(row, plan['request']['owner'])
    o.require(row['object_key'] == action['object_key'] and row['status'] == 'active',
              'provisional object/status')
    if action['expected']:
        o.require(row['root_id'] == action['expected']['root_id'], 'provisional root')
    value = o.unblob(row['value'])
    if cmd in ('item_archetype.create', 'item_archetype.revise'):
        desired = request['revision']
    elif cmd.startswith('facet_schema.'):
        desired = request['definition']
    elif cmd.startswith('notification_rendering_definition.'):
        desired = request['revision']
        # The semantic projection alone carries no publication provenance.
        o.require(record is not None, 'missing rendering provenance')
        o.validator('spine-readback-0.10.0.schema.json',
                    o.COMMANDS['notification_rendering_definition.show']['response']).validate(
            dict(ok=True, command='notification_rendering_definition.show',
                 contract_version='spine.notification-rendering-definitions.v1', record=record))
        o.require(record['revision'] == desired and record['owner'] == row['owner'] and
                  record['status'] == row['status'] and
                  record['definition_key'] == row['object_key'].split(':')[1] and
                  record['notification_rendering_definition_id'] == row['root_id'] and
                  record['notification_rendering_definition_revision_id'] == row['revision_id'] and
                  record['current_revision_id'] == row['revision_id'], 'rendering candidate identity')
        provenance = {k: request[k] for k in ('command_id', 'actor_subject_id', 'action_timestamp_utc')}
        o.require(record['published'] == provenance, 'rendering candidate provenance')
        if cmd.endswith('.create'):
            o.require(record['created'] == provenance, 'rendering create provenance')
        o.require(record['definition_hash'] == o.hash_value(dict(
            contract_version='spine.notification-rendering-definitions.v1',
            canonical_json_version='spine.canonical-json.v1', revision=desired)), 'rendering candidate hash')
    elif cmd in ('item_archetype.facet_binding.set', 'notification_profile.binding.set'):
        fields = ('item_archetype_id', 'facet_key', 'facet_schema_revision_id') if cmd.startswith('item_') else (
            'item_archetype_id', 'notification_profile_id')
        desired = {k: request[k] for k in fields}
    elif cmd == 'notification_profile.metadata.update':
        desired = dict(metadata=request['metadata'], revision=o.unblob(action['expected']['value'])['revision'])
        o.require(row['revision_id'] == action['expected']['revision_id'] and
                  row['revision_contract'] == action['expected']['revision_contract'], 'metadata candidate revision')
    else:
        authored = o.unblob(action['desired'])
        desired = dict(metadata={k: authored[k] for k in ('display_name', 'description')}, revision=request['revision'])
        o.require(row['revision_contract'] == 'spine.notification-profiles.v2', 'candidate decoder')
    o.require(value == desired, 'provisional semantics')
    lineage(plan['observation']['entries'] + plan['observation']['historical_revisions'] +
            [e['post_observation'] for e in cp['accepted_responses']] + [row])


def admit(flow, source, fresh, *, provisional=None, record=None, environment=None, target=None):
    plan, approval = flow['plan'], flow['approval']
    plan_check(flow)
    o.require((plan['environment'] if environment is None else environment) == plan['environment'],
              'recovery environment')
    o.require((plan['request']['target'] if target is None else target) == plan['request']['target'],
              'recovery target')
    if source['artifact_schema'] == 'spine.pack-apply-result.v2':
        o.result_check(plan, approval, source)
        o.require(source['state'] == 'partial', 'continuation source must be partial')
        cp = source['checkpoint']
    else:
        o.require(source['artifact_schema'] == 'spine.pack-apply-checkpoint.v2', 'continuation source kind')
        cp = source
    checkpoint_check(plan, approval, cp)
    o.observation(fresh, plan['request']['owner'])
    lineage(plan['observation']['entries'] + plan['observation']['historical_revisions'] +
            [e['post_observation'] for e in cp['accepted_responses']] +
            fresh['entries'] + fresh['historical_revisions'])
    prefix = o.forward(plan['observation'], cp['accepted_responses'])
    actual = o.forward(fresh, [])
    if actual == prefix:
        if provisional is not None:
            o.require(cp['unresolved_submission'] is not None, 'unexpected candidate')
            candidate_check(plan, approval, cp, provisional, record)
            same = o.forward(plan['observation'], cp['accepted_responses'] +
                             [dict(post_observation=provisional)])
            o.require(same == prefix, 'nonidentical duplicate candidate')
        kind = 'prefix'  # Identical no-op candidates deduplicate; no acceptance inferred.
    else:
        o.require(cp['unresolved_submission'] is not None and provisional is not None,
                  'unexplained catalog change')
        candidate_check(plan, approval, cp, provisional, record)
        candidate = o.forward(plan['observation'], cp['accepted_responses'] +
                              [dict(post_observation=provisional)])
        o.require(actual == candidate, 'unrelated catalog change')
        kind = 'prefix_plus_one'
    rendering_record = (record if provisional is not None and
        plan['actions'][len(cp['accepted_responses'])]['command'].startswith(
            'notification_rendering_definition.') else None)
    # Keep the full validated public record, not only its reduced projection.
    # In particular, a publish preserves creation provenance from an earlier
    # execution; replay must corroborate it, not replace it with the publisher.
    return dict(kind=kind, checkpoint=deepcopy(cp), provisional=deepcopy(provisional),
                rendering_record=deepcopy(rendering_record))


def replay_check(flow, admission, evidence):
    plan, approval = flow['plan'], flow['approval']
    cp = admission['checkpoint']
    o.require(cp['unresolved_submission'] is not None, 'no uncertain request')
    n = len(cp['accepted_responses'])
    evidence_check(plan, approval, plan['actions'][n], evidence, cp['accepted_responses'])
    o.require(evidence['request'] == cp['unresolved_submission']['request'], 'exact replay request')
    if admission['provisional'] is not None:
        o.require(evidence['post_observation'] == admission['provisional'], 'replay candidate mismatch')
    if admission['rendering_record'] is not None:
        response = o.unblob(evidence['response'], True)
        o.require(response['record'] == admission['rendering_record'], 'rendering replay record mismatch')
    # Still only candidate evidence: a runtime must obtain readback and durably
    # publish an accepted checkpoint before making this prefix available.
    return deepcopy(evidence)


def binding_recheck(flow, admission, current):
    cp = admission['checkpoint']
    action = flow['plan']['actions'][len(cp['accepted_responses'])]
    o.require(action['command'] in ('item_archetype.facet_binding.set',
                                  'notification_profile.binding.set'), 'binding command required')
    expected = admission['provisional'] if admission['kind'] == 'prefix_plus_one' else action['expected']
    o.require(current == expected, 'immediate binding precondition')


def approval_from_result(plan, result):
    return o.seal(dict(artifact_schema='spine.pack-install-approval.v2',
        plan_digest=plan['content_identity']['digest'], approve_complete_plan=True,
        acknowledge_single_operator=True, authorized_update_action_ids=plan['decision_action_ids'],
        execution=deepcopy(result['checkpoint']['execution'])))


def verification(flow, fresh, result=None, *, environment=None, target=None):
    plan = flow['plan']
    plan_check(flow)
    if result is not None:
        o.artifact(result)  # Invalid outer syntax/schema/digest is an input failure.
        o.require(result['artifact_schema'] == 'spine.pack-apply-result.v2', 'verification result kind')
    o.require((plan['environment'] if environment is None else environment) == plan['environment'],
              'verification environment')
    o.require((plan['request']['target'] if target is None else target) == plan['request']['target'],
              'verification target')
    o.observation(fresh, plan['request']['owner'])
    accepted, coverage = [], 'missing' if plan['actions'] else 'not_required'
    if result is not None:
        try:
            approval = approval_from_result(plan, result)
            o.result_check(plan, approval, result)
            checkpoint_check(plan, approval, result['checkpoint'])
            accepted = result['checkpoint']['accepted_responses']
            if plan['actions']:
                coverage = 'complete' if result['state'] == 'applied' else 'missing'
        except (ValueError, KeyError, ValidationError):
            coverage, accepted = 'invalid', []
    lineage(plan['observation']['entries'] + plan['observation']['historical_revisions'] +
            [e['post_observation'] for e in accepted] + fresh['entries'] + fresh['historical_revisions'])
    expected = {r['object_key']: r for r in plan['observation']['entries']}
    expected.update({e['post_observation']['object_key']: e['post_observation'] for e in accepted})
    pending = {a['object_key'] for a in plan['actions'][len(accepted):]}
    # Blocked resolutions are null: readable old rows are not proof of the
    # desired configuration, and verify must not resolve them speculatively.
    pending.update(plan['blocked_object_keys'])
    rows = {r['object_key']: r for r in fresh['entries']}
    results = []
    for key in plan['closure']:
        row, desired = deepcopy(rows.get(key)), deepcopy(expected.get(key))
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
                actual['binding_id'] = desired['binding_id']  # Existing v1 same-target binding rule.
            status = 'equivalent' if actual == desired else 'drifted'
        results.append(dict(object_key=key, state=status, observed=row))
    success = coverage in ('complete', 'not_required') and all(r['state'] == 'equivalent' for r in results)
    value = o.seal(dict(artifact_schema='spine.pack-verification-result.v2',
        plan_digest=plan['content_identity']['digest'], apply_result_digest=(
            result['content_identity']['digest'] if result is not None and plan['actions'] else None),
        pack=deepcopy(plan['pack']), target=deepcopy(plan['request']['target']),
        environment=deepcopy(plan['environment']), observation=deepcopy(fresh),
        closure=deepcopy(plan['closure']), object_results=results, response_evidence=coverage,
        receipt_readback=RECEIPT, disclosure='separate_operator_configuration_required',
        state='verified' if success else 'mismatch'))
    o.artifact(value)
    return value


def verification_check(flow, result, value):
    o.artifact(value)
    o.require(value == verification(flow, value['observation'], result,
        environment=value['environment'], target=value['target']), 'verification correlation/outcome')
