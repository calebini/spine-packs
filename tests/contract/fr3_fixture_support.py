"""Synthetic FR-3 initial-apply vectors; no transport or Spine implementation imports.

Refresh the immutable FR-1 examples using the independent contract oracle, not
the installer implementation. Returned IDs remain explicitly synthetic evidence.
This module neither executes writes nor proves filesystem durability/recovery.
"""
from contextlib import contextmanager
from copy import deepcopy
import json
from unittest.mock import patch

import facet_artifact_oracle as oracle
from test_facet_manifest_contract import digest

INVENTORY = oracle.load(oracle.ROOT / 'contracts/installer-spine-0.10.0-inventory.json')


@contextmanager
def current_contracts():
    """Scope the independent oracle to the exact successor public closure."""
    def public_schema(command, direction, value):
        oracle.validator('spine-readback-0.10.0.schema.json',
                         INVENTORY['commands'][command][direction]).validate(value)

    with patch.object(oracle, 'INVENTORY', INVENTORY), \
            patch.object(oracle, 'COMMANDS', INVENTORY['commands']), \
            patch.object(oracle, 'public_schema', public_schema):
        yield


def plan_check(flow):
    plan = flow['plan']
    oracle.require(plan['environment']['runtime_version'] == '0.10.0', 'exact runtime')
    for field in ('ledger_schema_current', 'ledger_schema_implemented'):
        oracle.require(plan['environment'][field] == '19', 'exact ledger schema')
    oracle.require(flow['manifest']['compatibility']['spine_runtime_versions'] == ['0.10.0'],
                   'exact manifest compatibility')
    oracle.require(plan['required_execution_contracts'] == INVENTORY['required_execution_contracts'],
                   'exact execution union')
    oracle.plan_check(flow['manifest'], flow['request'], plan)


def checkpoint_at(flow, length, prepared=False):
    cp = deepcopy(flow['initial_checkpoint'])
    cp['accepted_responses'] = deepcopy(flow['accepted_responses'][:length])
    actions = flow['plan']['actions']
    cp['next_action_id'] = actions[length]['action_id'] if length < len(actions) else None
    cp['unresolved_submission'] = None
    if prepared:
        action = actions[length]
        request = oracle.materialize(flow['plan'], flow['approval'], action,
                                     cp['accepted_responses'])
        cp['unresolved_submission'] = dict(action_id=action['action_id'],
            command_id=request['command_id'], submission_state='prepared_or_submitted',
            request=oracle.blob(request))
    return oracle.seal(cp)


def reseal_response(evidence, response):
    text = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
    evidence['response'] = dict(json_text=text, digest=oracle.sha(text.encode()))
    evidence['receipt'] = oracle.receipt_projection(evidence['command'], response)


def refresh(historical):
    """Deterministically regenerate an initial-only 0.10.0 fixture in memory."""
    flow = deepcopy(historical)
    # FR-4 owns continuation and verification; do not relabel their old proof.
    for key in ('observations', 'verification', 'envelope'):
        del flow[key]
    manifest = flow['manifest']
    manifest['compatibility']['spine_runtime_versions'] = ['0.10.0']
    manifest['content_identity']['digest'] = digest(manifest)
    plan = flow['plan']
    plan['pack']['manifest_digest'] = manifest['content_identity']['digest']
    plan['environment']['runtime_version'] = '0.10.0'
    plan['environment']['advertised_contracts'] = sorted(set(
        plan['environment']['advertised_contracts'] + INVENTORY['required_execution_contracts']))
    plan['required_execution_contracts'] = INVENTORY['required_execution_contracts']
    flow['plan'] = plan = oracle.seal(plan)
    flow['approval']['plan_digest'] = plan['content_identity']['digest']
    flow['approval'] = approval = oracle.seal(flow['approval'])
    prefix = []
    with current_contracts():
        for action, evidence in zip(plan['actions'], flow['accepted_responses'], strict=True):
            request = oracle.materialize(plan, approval, action, prefix)
            evidence['command_id'] = request['command_id']
            evidence['request'] = oracle.blob(request)
            response = oracle.unblob(evidence['response'], True)
            receipt = response.get('receipt', response)
            receipt['command_id'] = request['command_id']
            if evidence['receipt']['family'] == 'catalog':
                receipt['semantic_facts_hash'] = oracle.hash_value(request)
            if evidence['receipt']['family'] == 'rendering':
                response['record']['published']['command_id'] = request['command_id']
                if action['command'].endswith('.create'):
                    response['record']['created']['command_id'] = request['command_id']
            reseal_response(evidence, response)
            oracle.evidence_check(plan, approval, action, evidence, prefix)
            prefix.append(evidence)
        cp = flow['initial_checkpoint']
        cp.update(plan_digest=plan['content_identity']['digest'],
                  approval_digest=approval['content_identity']['digest'])
        flow['initial_checkpoint'] = oracle.seal(cp)
        for key in ('final_checkpoint', 'prepared_checkpoint'):
            old = historical[key]
            flow[key] = checkpoint_at(flow, len(old['accepted_responses']),
                                      old['unresolved_submission'] is not None)
        for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
            result = flow[key]
            old = result['checkpoint']
            result['checkpoint'] = checkpoint_at(flow, len(old['accepted_responses']),
                                                 old['unresolved_submission'] is not None)
            flow[key] = oracle.seal(result)
    return flow
