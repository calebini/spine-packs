"""AL-1 synthetic contract derivations; no runtime/Spine imports or transport.

Derive new artifacts from frozen 0.10.0 vectors, never migrate operator evidence.
Only test-oracle globals are scoped below; production routing is unchanged.
"""
from contextlib import contextmanager
from copy import deepcopy
from unittest.mock import patch

import facet_artifact_oracle as o
import fr4_contract_oracle as fr4
import fr4_fixture_support as companions
from fr3_fixture_support import checkpoint_at, reseal_response
from test_facet_manifest_contract import digest

PIN = '3e65ef0de9e73b62047a0f6328731db08ca91023'
RUNTIME = '0.12.0'
SCHEMA = '20'
RECEIPT = 'captured_responses_only_spine_0.12.0'
INVENTORY = o.load(o.ROOT / 'contracts/installer-spine-0.12.0-inventory.json')


def plan_check(flow):
    plan = flow['plan']
    o.require(plan['environment']['runtime_version'] == RUNTIME, 'exact runtime')
    for field in ('ledger_schema_current', 'ledger_schema_implemented'):
        o.require(plan['environment'][field] == SCHEMA, 'exact ledger schema')
    o.require(flow['manifest']['compatibility']['spine_runtime_versions'] == [RUNTIME],
              'exact manifest compatibility')
    o.require(plan['required_execution_contracts'] == INVENTORY['required_execution_contracts'],
              'exact execution union')
    o.plan_check(flow['manifest'], flow['request'], plan)


@contextmanager
def aligned_contracts():
    def public_schema(command, direction, value):
        o.validator('spine-readback-0.12.0.schema.json',
                    INVENTORY['commands'][command][direction]).validate(value)
    with patch.object(o, 'INVENTORY', INVENTORY), \
            patch.object(o, 'COMMANDS', INVENTORY['commands']), \
            patch.object(o, 'public_schema', public_schema), \
            patch.object(fr4, 'plan_check', plan_check), \
            patch.object(fr4, 'RECEIPT', RECEIPT), \
            patch.object(companions, 'RECEIPT', RECEIPT):
        yield


def derive(source, source_path, source_hash):
    """Pure synthetic flow. Preserve authored bodies, IDs and public semantics."""
    flow = deepcopy(source)
    manifest = flow['manifest']
    manifest['compatibility']['spine_runtime_versions'] = [RUNTIME]
    manifest['content_identity']['digest'] = digest(manifest)
    plan = flow['plan']
    plan['pack']['manifest_digest'] = manifest['content_identity']['digest']
    plan['environment'].update(runtime_version=RUNTIME,
        ledger_schema_current=SCHEMA, ledger_schema_implemented=SCHEMA)
    flow['plan'] = plan = o.seal(plan)
    flow['approval']['plan_digest'] = plan['content_identity']['digest']
    flow['approval'] = approval = o.seal(flow['approval'])
    with aligned_contracts():
        prefix = []
        for action, evidence in zip(plan['actions'], flow['accepted_responses'], strict=True):
            request = o.materialize(plan, approval, action, prefix)
            evidence.update(command_id=request['command_id'], request=o.blob(request))
            response = o.unblob(evidence['response'], True)
            response.get('receipt', response)['command_id'] = request['command_id']
            if evidence['receipt']['family'] == 'catalog':
                response['receipt']['semantic_facts_hash'] = o.hash_value(request)
            elif evidence['receipt']['family'] == 'rendering':
                response['record']['published']['command_id'] = request['command_id']
                if action['command'].endswith('.create'):
                    response['record']['created']['command_id'] = request['command_id']
            reseal_response(evidence, response)
            fr4.evidence_check(plan, approval, action, evidence, prefix)
            prefix.append(evidence)
        flow['initial_checkpoint'].update(plan_digest=plan['content_identity']['digest'],
            approval_digest=approval['content_identity']['digest'])
        flow['initial_checkpoint'] = o.seal(flow['initial_checkpoint'])
        for key in ('final_checkpoint', 'prepared_checkpoint'):
            prior = source[key]
            flow[key] = checkpoint_at(flow, len(prior['accepted_responses']),
                                      prior['unresolved_submission'] is not None)
        for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
            result = flow[key]
            prior = source[key]['checkpoint']
            result['checkpoint'] = checkpoint_at(flow, len(prior['accepted_responses']),
                                                prior['unresolved_submission'] is not None)
            flow[key] = o.seal(result)
        flow.update(companions.refresh(flow, source_path, source_hash))
    return flow


def summary(flow):
    """Saved expectations for every derived artifact and submitted wire value."""
    return dict(manifest_digest=flow['manifest']['content_identity']['digest'],
        artifact_digests={k: v['content_identity']['digest'] for k, v in flow.items()
            if isinstance(v, dict) and 'artifact_schema' in v and 'content_identity' in v},
        wire=[dict(action_id=e['action_id'], command=e['command'], command_id=e['command_id'],
                   request_digest=e['request']['digest'], response_digest=e['response']['digest'])
              for e in flow['accepted_responses']],
        observation_digests=[v['digest'] for v in flow['observations']])


def load_flow(vector):
    path = vector['source']['path']
    raw = (o.ROOT / path).read_bytes()
    o.require(o.sha(raw) == vector['source']['sha256'], 'frozen source hash')
    return derive(o.load(o.ROOT / path), path, vector['source']['sha256'])
