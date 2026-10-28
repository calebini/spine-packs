"""FR-4 synthetic fixture refresh, independent of installer runtime and Spine.

Add recovery views and verification to hash-pinned FR-3 flows without copying or
rewriting their bytes. Computed legacy fingerprints are synthetic test data,
never claimed observations of a public CLI. No transport or filesystem writes.
"""
from copy import deepcopy

import facet_artifact_oracle as oracle
from fr3_fixture_support import current_contracts

BASELINE = '8f3c50b6fd1b4aa534e50925b7417a7a80d19122'
RECEIPT = 'captured_responses_only_spine_0.10.0'


def view_at(flow, length):
    value = oracle.forward(flow['plan']['observation'], flow['accepted_responses'][:length])
    value['public_catalog_snapshots'] = oracle.public_snapshots(value['entries'])
    value['digest'] = oracle.observation_digest(value)
    return value


def refresh(initial, path, source_hash):
    """Pure deterministic companion; initial artifacts/IDs remain unchanged."""
    plan = initial['plan']
    views = [view_at(initial, n) for n in range(len(plan['actions']) + 1)]
    final = views[-1]
    rows = {r['object_key']: r for r in final['entries']}
    verification = oracle.seal(dict(
        artifact_schema='spine.pack-verification-result.v2',
        plan_digest=plan['content_identity']['digest'],
        apply_result_digest=initial['apply_result']['content_identity']['digest'],
        pack=deepcopy(plan['pack']), target=deepcopy(plan['request']['target']),
        environment=deepcopy(plan['environment']), observation=deepcopy(final),
        closure=deepcopy(plan['closure']), object_results=[dict(object_key=k,
            state='equivalent', observed=deepcopy(rows[k])) for k in plan['closure']],
        response_evidence='complete', receipt_readback=RECEIPT,
        disclosure='separate_operator_configuration_required', state='verified'))
    return dict(source=dict(path=path, sha256=source_hash), observations=views,
        verification=verification, envelope=dict(artifact_schema='spine.pack-installer-result.v2',
            operation='verify', status='success', exit_code='0',
            artifact=dict(path='/synthetic/verification.json',
                          digest=verification['content_identity']['digest']), error=None))


def load_flow(path):
    companion = oracle.load(oracle.ROOT / path)
    source = companion['source']
    raw = (oracle.ROOT / source['path']).read_bytes()
    oracle.require(oracle.sha(raw) == source['sha256'], 'initial source pin')
    return dict(deepcopy(oracle.load(oracle.ROOT / source['path'])), **deepcopy(companion))


def replay_evidence(evidence):
    """Catalog replay has no replay flag; other families retain stored effect."""
    from fr3_fixture_support import reseal_response
    evidence = deepcopy(evidence)
    response = oracle.unblob(evidence['response'], True)
    if 'replayed' in response:
        response.update(replayed=True, changed=False)
        reseal_response(evidence, response)
    return evidence


def profile_history_flow(decoder='v2'):
    """In-memory metadata-update regression; never rewrite pinned fixture bytes.

    Add a distinct preexisting profile revision, then rebind saved command and
    receipt identities to the changed plan. No runtime helper computes the
    expected historical metadata or immutable content.
    """
    from fr3_fixture_support import reseal_response
    flow = oracle.load(oracle.ROOT / 'tests/fixtures/installer-v2/flight-update-0.10.0.json')
    plan = flow['plan']; view = plan['observation']
    old = deepcopy(next(r for r in view['entries'] if r['object_key'].startswith('profile:')))
    old['revision_id'] = 'profile_revision_before_5'
    old['revision_contract'] = 'spine.notification-profiles.' + decoder
    value = oracle.unblob(old['value'])
    value['revision']['templates'][0]['late_handling']['grace_seconds'] = '1800'
    if decoder == 'v1':
        for template in value['revision']['templates']:
            template.pop('rendering')
    old['value'] = oracle.blob(value)
    view['historical_revisions'].append(old)
    view['historical_revisions'].sort(key=lambda r: (r['object_key'], r['revision_id']))
    view['digest'] = oracle.observation_digest(view)
    flow['plan'] = plan = oracle.seal(plan)
    flow['approval']['plan_digest'] = plan['content_identity']['digest']
    flow['approval'] = oracle.seal(flow['approval'])
    for action, evidence in zip(plan['actions'], flow['accepted_responses'], strict=True):
        request = oracle.unblob(evidence['request'])
        request['command_id'] = oracle.command_id(plan, flow['approval'], action)
        evidence.update(command_id=request['command_id'], request=oracle.blob(request))
        response = oracle.unblob(evidence['response'], True)
        response.get('receipt', response)['command_id'] = request['command_id']
        if evidence['receipt']['family'] == 'catalog':
            response['receipt']['semantic_facts_hash'] = oracle.hash_value(request)
        elif evidence['receipt']['family'] == 'rendering':
            response['record']['published']['command_id'] = request['command_id']
        reseal_response(evidence, response)
    flow['initial_checkpoint'].update(plan_digest=plan['content_identity']['digest'],
        approval_digest=flow['approval']['content_identity']['digest'])
    flow['initial_checkpoint'] = oracle.seal(flow['initial_checkpoint'])
    # Old saved terminal artifacts belong to the original plan, not this case.
    for key in ('final_checkpoint', 'prepared_checkpoint', 'apply_result', 'partial_result', 'empty_prefix_partial'):
        del flow[key]
    return flow
