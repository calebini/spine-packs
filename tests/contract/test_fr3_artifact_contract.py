"""Exact-0.10.0 initial-apply contract gate, not executor qualification."""
from copy import deepcopy
import sys
import unittest

import facet_artifact_oracle as oracle
from fr3_fixture_support import (INVENTORY, checkpoint_at, current_contracts,
                                 plan_check, refresh, reseal_response)

INDEX = oracle.ROOT / 'contracts/installer-fr3-fixture-manifest.v2.json'


@unittest.skipIf(oracle.Draft202012Validator is None,
                 'FR-3 contract gate requires development jsonschema')
class FR3ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(current_contracts())

    def flows(self):
        return [oracle.load(oracle.ROOT / entry['path'])
                for entry in oracle.load(INDEX)['fixtures']]

    def test_exact_baseline_and_immutable_historical_sources(self):
        index = oracle.load(INDEX)
        self.assertEqual(index['spine_commit'], '8f3c50b6fd1b4aa534e50925b7417a7a80d19122')
        self.assertEqual(index['spine_commit'], INVENTORY['spine_commit'])
        self.assertEqual((index['runtime_version'], index['ledger_schema']), ('0.10.0', '19'))
        self.assertEqual(len(INVENTORY['required_execution_contracts']), 18)
        for entry in index['fixtures']:
            for path, pin in ((entry['path'], entry['sha256']),
                              (entry['historical_source'], entry['historical_sha256'])):
                self.assertEqual(oracle.sha((oracle.ROOT / path).read_bytes()), pin)
            historical = oracle.load(oracle.ROOT / entry['historical_source'])
            current = oracle.load(oracle.ROOT / entry['path'])
            self.assertEqual(current, refresh(historical))
            self.assertEqual(historical['plan']['environment']['runtime_version'], '0.9.1')
            self.assertEqual(entry['commands'], [a['command'] for a in current['plan']['actions']])
            self.assertFalse({'verification', 'observations', 'envelope'} & current.keys())
            self.assertNotEqual(current['plan']['content_identity'], historical['plan']['content_identity'])
            for new, old in zip(current['accepted_responses'], historical['accepted_responses'], strict=True):
                self.assertNotEqual(new['command_id'], old['command_id'])
                self.assertEqual(new['post_observation'], old['post_observation'])

    def test_complete_initial_flows_cover_exactly_eleven_configuration_writes(self):
        commands = set()
        for flow in self.flows():
            plan_check(flow)
            p, a = flow['plan'], flow['approval']
            oracle.approval_check(p, a)
            for key in ('initial_checkpoint', 'prepared_checkpoint', 'final_checkpoint'):
                oracle.checkpoint_check(p, a, flow[key])
            for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
                oracle.result_check(p, a, flow[key])
            commands.update(action['command'] for action in p['actions'])
        expected = {c for c, v in INVENTORY['commands'].items() if v['phase'] is not None}
        self.assertEqual(commands, expected)
        self.assertEqual(len(commands), 11)
        self.assertFalse(any(c.startswith('item.') or 'disclosure' in c or 'send' in c for c in commands))

    def test_current_read_only_planner_reproduces_independent_fixture_plans(self):
        sys.path.insert(0, str(oracle.ROOT / 'src'))
        try:
            from spine_packs.facet_planning import build_plan, validate_inputs
            for flow in self.flows():
                validate_inputs(flow['manifest'], flow['request'])
                p = flow['plan']
                self.assertEqual(build_plan(flow['manifest'], flow['request'],
                                            p['environment'], p['observation']), p)
        finally:
            sys.path.pop(0)

    def test_each_prepared_and_accepted_prefix_and_partial_submission(self):
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            for n, action in enumerate(p['actions']):
                with self.subTest(command=action['command']):
                    before = checkpoint_at(flow, n)
                    prepared = checkpoint_at(flow, n, True)
                    accepted = checkpoint_at(flow, n + 1)
                    for cp in (before, prepared, accepted):
                        oracle.checkpoint_check(p, a, cp)
                    self.assertEqual(prepared['accepted_responses'], before['accepted_responses'])
                    self.assertEqual(prepared['unresolved_submission']['request'],
                                     flow['accepted_responses'][n]['request'])
                    partial = deepcopy(flow['empty_prefix_partial'])
                    partial['checkpoint'] = prepared
                    partial['failure']['action_id'] = action['action_id']
                    partial['unattempted_action_ids'] = [x['action_id'] for x in p['actions'][n + 1:]]
                    oracle.result_check(p, a, oracle.seal(partial))
                    self.assertEqual(partial['state'], 'partial')  # Includes n == 0.
                    partial['state'] = 'not_applied'
                    with self.assertRaises(ValueError):
                        oracle.result_check(p, a, oracle.seal(partial))

    def test_consumers_cannot_resolve_without_accepted_producers(self):
        exercised = set()
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            resolutions = {r['object_key']: r for r in p['resolutions']}
            for n, action in enumerate(p['actions']):
                for slot in action['slots']:
                    source = resolutions[slot['object_key']][slot['field']]
                    if source['kind'] != 'action_result':
                        continue
                    prefix = [e for e in flow['accepted_responses'][:n]
                              if e['action_id'] != source['action_id']]
                    with self.subTest(command=action['command'], slot=slot['request_pointer']):
                        with self.assertRaisesRegex(ValueError, 'consumer before accepted producer'):
                            oracle.materialize(p, a, action, prefix)
                    exercised.add(action['command'])
        self.assertEqual(exercised, {'item_archetype.facet_binding.set',
            'notification_rendering_definition.create', 'notification_rendering_definition.publish',
            'notification_profile.create', 'notification_profile.revise', 'notification_profile.binding.set'})

    def test_each_command_rejects_uncorrelated_receipt_owner_root_and_bytes(self):
        for flow in self.flows():
            p, a = flow['plan'], flow['approval']
            for n, action in enumerate(p['actions']):
                for failure in ('command', 'owner', 'root', 'response_bytes', 'request_bytes'):
                    with self.subTest(command=action['command'], failure=failure):
                        evidence = deepcopy(flow['accepted_responses'][n])
                        if failure == 'command':
                            response = oracle.unblob(evidence['response'], True)
                            response.get('receipt', response)['command_id'] = 'unrelated-command'
                            reseal_response(evidence, response)
                        elif failure == 'owner':
                            evidence['post_observation']['owner']['owner_subject_id'] = 'unrelated-owner'
                        elif failure == 'root':
                            evidence['post_observation']['root_id'] = 'unrelated-root'
                        elif failure == 'response_bytes':
                            evidence['response']['json_text'] += ' '
                        else:
                            evidence['request']['canonical_json'] += ' '
                        with self.assertRaises(ValueError):
                            oracle.evidence_check(p, a, action, evidence, flow['accepted_responses'][:n])

    def test_stale_approval_and_missing_update_authorization(self):
        for flow in self.flows():
            approval = deepcopy(flow['approval'])
            approval['plan_digest'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'stale approval'):
                oracle.approval_check(flow['plan'], oracle.seal(approval))
        flow = self.flows()[1]
        approval = deepcopy(flow['approval'])
        approval['authorized_update_action_ids'].pop()
        with self.assertRaisesRegex(ValueError, 'update authorization'):
            oracle.approval_check(flow['plan'], oracle.seal(approval))

    def test_exact_runtime_and_contract_union_are_not_inferred(self):
        for mutation in ('runtime', 'manifest', 'schema', 'union'):
            flow = self.flows()[0]
            if mutation == 'runtime':
                flow['plan']['environment']['runtime_version'] = '0.10.1'
            elif mutation == 'manifest':
                flow['manifest']['compatibility']['spine_runtime_versions'].append('0.10.1')
            elif mutation == 'schema':
                flow['plan']['environment']['ledger_schema_current'] = '20'
            else:
                flow['plan']['required_execution_contracts'].remove('spine.facet-schema-revision-readback.v1')
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'exact'):
                plan_check(flow)


if __name__ == '__main__':
    unittest.main()
