"""Exact-0.10.0 recovery/verify contract gate; no executor or ledger qualification."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

import facet_artifact_oracle as o
import fr4_contract_oracle as fr4
from fr3_fixture_support import checkpoint_at, current_contracts, reseal_response
from fr4_fixture_support import BASELINE, RECEIPT, load_flow, refresh, replay_evidence

INDEX = o.ROOT / 'contracts/installer-fr4-fixture-manifest.v2.json'


def reseal_view(view):
    view['public_catalog_snapshots'] = o.public_snapshots(view['entries'])
    view['digest'] = o.observation_digest(view)
    return view


def record_for(flow, n):
    return o.unblob(flow['accepted_responses'][n]['response'], True).get('record')


@unittest.skipIf(o.Draft202012Validator is None, 'FR-4 requires official development jsonschema')
class FR4ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(current_contracts())

    def flows(self):
        return [load_flow(e['path']) for e in o.load(INDEX)['fixtures']]

    def test_source_pins_and_deterministic_refresh_preserve_all_prior_fixtures(self):
        index = o.load(INDEX)
        self.assertEqual((index['spine_commit'], index['runtime_version'], index['ledger_schema']),
                         (BASELINE, '0.10.0', '19'))
        for entry in index['preserved_inputs']:
            self.assertEqual(o.sha((o.ROOT / entry['path']).read_bytes()), entry['sha256'])
        for entry in index['fixtures']:
            path = o.ROOT / entry['path']; companion = o.load(path)
            self.assertEqual(o.sha(path.read_bytes()), entry['sha256'])
            source = companion['source']; initial = o.load(o.ROOT / source['path'])
            self.assertEqual(companion, refresh(initial, source['path'], source['sha256']))
            flow = load_flow(entry['path'])
            self.assertEqual({k: flow[k] for k in initial}, initial)
            self.assertEqual(flow['observations'][0], initial['plan']['observation'])

    def test_official_schema_meta_and_runtime_specific_receipt_pairing(self):
        o.Draft202012Validator.check_schema(o.load(o.SCHEMAS / 'spine-pack-installer-types.v2.schema.json'))
        for runtime in ('0.9.1', '0.10.0'):
            value = (o.load(o.ROOT / 'tests/fixtures/installer-v2/flight-create.json')['verification']
                     if runtime == '0.9.1' else self.flows()[0]['verification'])
            o.artifact(value)
            self.assertEqual(value['receipt_readback'], 'captured_responses_only_spine_' + runtime)
            for wrong in ('captured_responses_only_spine_0.9.1', RECEIPT, 'independent_receipt_readback'):
                if wrong == value['receipt_readback']: continue
                changed = deepcopy(value); changed['receipt_readback'] = wrong
                with self.assertRaises(fr4.ValidationError): o.artifact(o.seal(changed))

    def test_every_indexed_boundary_and_all_eleven_commands(self):
        index = o.load(INDEX); commands = set(); boundaries = set()
        for vector in index['recovery_vectors']:
            flow = load_flow(vector['fixture']); n = int(vector['prefix_length'])
            boundary = vector['boundary']; boundaries.add(boundary)
            action = flow['plan']['actions'][n]
            self.assertEqual(action['command'], vector['command']); commands.add(action['command'])
            with self.subTest(command=action['command'], boundary=boundary):
                accepted = boundary == 'accepted_durable'
                cp = checkpoint_at(flow, n + 1 if accepted else n, not accepted)
                before = deepcopy(cp)
                if boundary == 'accepted_response_lost':
                    candidate = flow['accepted_responses'][n]['post_observation']
                    admission = fr4.admit(flow, cp, flow['observations'][n+1],
                                          provisional=candidate, record=record_for(flow, n))
                    self.assertEqual(admission['kind'], 'prefix_plus_one')
                    self.assertEqual(len(admission['checkpoint']['accepted_responses']), n)
                    replay = replay_evidence(flow['accepted_responses'][n])
                    self.assertEqual(fr4.replay_check(flow, admission, replay), replay)
                    self.assertEqual(replay['request'], cp['unresolved_submission']['request'])
                else:
                    admission = fr4.admit(flow, cp, flow['observations'][n+1 if accepted else n])
                    self.assertEqual(admission['kind'], 'prefix')
                self.assertEqual(cp, before)
                fr4.checkpoint_check(flow['plan'], flow['approval'], checkpoint_at(flow, n+1))
        self.assertEqual(commands, {k for k,v in o.COMMANDS.items() if v['phase'] is not None})
        self.assertEqual(boundaries, {'prepared_before_submit', 'accepted_response_lost', 'accepted_durable'})
        self.assertEqual(len(index['recovery_vectors']), 36)

    def test_source_admission_partial_and_complete_but_not_terminal_success_or_not_applied(self):
        for flow in self.flows():
            n = len(flow['partial_result']['checkpoint']['accepted_responses'])
            fr4.admit(flow, flow['partial_result'], flow['observations'][n])
            admission = fr4.admit(flow, flow['final_checkpoint'], flow['observations'][-1])
            self.assertIsNone(admission['checkpoint']['next_action_id'])
            with self.assertRaisesRegex(ValueError, 'partial'):
                fr4.admit(flow, flow['apply_result'], flow['observations'][-1])
            not_applied = deepcopy(flow['empty_prefix_partial'])
            not_applied.update(state='not_applied', checkpoint=checkpoint_at(flow, 0),
                               unattempted_action_ids=[a['action_id'] for a in flow['plan']['actions']])
            with self.assertRaisesRegex(ValueError, 'partial'):
                fr4.admit(flow, o.seal(not_applied), flow['observations'][0])

    def test_changed_source_approval_execution_target_environment_and_prefix_rejected(self):
        flow = self.flows()[1]
        for failure in ('digest', 'gap', 'request', 'command_id', 'approval', 'execution', 'target', 'environment'):
            f = deepcopy(flow); cp = checkpoint_at(f, 3, True); kwargs = {}
            if failure == 'gap': cp['accepted_responses'].pop(0)
            elif failure == 'request':
                req = o.unblob(cp['unresolved_submission']['request']); req['actor_subject_id'] = 'other'
                cp['unresolved_submission']['request'] = o.blob(req)
            elif failure == 'command_id': cp['unresolved_submission']['command_id'] = 'other'
            elif failure == 'approval': cp['approval_digest'] = '0'*64
            elif failure == 'execution': cp['execution']['actor_subject_id'] = 'other'
            elif failure == 'target': kwargs['target'] = dict(f['plan']['request']['target'], host_name='other.invalid')
            elif failure == 'environment': kwargs['environment'] = dict(f['plan']['environment'], runtime_version='0.9.1')
            cp = o.seal(cp)
            if failure == 'digest': cp['content_identity']['digest'] = '0'*64
            with self.subTest(failure=failure), self.assertRaises((ValueError, fr4.ValidationError)):
                fr4.admit(f, cp, f['observations'][3], **kwargs)

    def test_provisional_candidate_is_not_acceptance_or_a_suffix_id_source(self):
        flow = self.flows()[0]; n = 1; cp = checkpoint_at(flow, n, True)
        candidate = flow['accepted_responses'][n]['post_observation']
        admission = fr4.admit(flow, cp, flow['observations'][n+1], provisional=candidate)
        consumer = flow['plan']['actions'][n+1]
        with self.assertRaisesRegex(ValueError, 'consumer before accepted producer'):
            o.materialize(flow['plan'], flow['approval'], consumer, admission['checkpoint']['accepted_responses'])
        with self.assertRaises((ValueError, TypeError)):
            fr4.replay_check(flow, admission, None)
        self.assertEqual(admission['checkpoint'], cp)

    def test_candidate_owner_root_semantics_provenance_history_and_unrelated_drift(self):
        for failure in ('owner','root','semantics','provenance','missing_history','unrelated','suffix','same_revision'):
            f = self.flows()[1]; n = 3; cp = checkpoint_at(f,n,True)
            fresh = deepcopy(f['observations'][n+1]); candidate = deepcopy(f['accepted_responses'][n]['post_observation'])
            record = deepcopy(record_for(f,n))
            if failure == 'owner': candidate['owner']['owner_subject_id'] = 'foreign'
            elif failure == 'root': candidate['root_id'] = 'foreign-root'
            elif failure == 'semantics':
                value=o.unblob(candidate['value']); value['description']='unexpected'; candidate['value']=o.blob(value)
            elif failure == 'provenance': record['published']['actor_subject_id'] = 'foreign'
            elif failure == 'missing_history': fresh['historical_revisions'].pop(0)
            elif failure == 'unrelated': fresh['entries'][0]['status']='retired'
            elif failure == 'suffix': fresh=deepcopy(f['observations'][n+2])
            elif failure == 'same_revision':
                candidate['revision_id']=f['plan']['actions'][n]['expected']['revision_id']
                for row in fresh['entries']:
                    if row['object_key']==candidate['object_key']: row['revision_id']=candidate['revision_id']
            with self.subTest(failure=failure), self.assertRaises((ValueError,fr4.ValidationError)):
                fr4.admit(f,cp,reseal_view(fresh),provisional=candidate,record=record)

    def test_replay_must_correlate_exact_request_ids_provenance_and_non_noop_revision(self):
        for failure in ('actor','timestamp','command','output','provenance','noop','reused_revision'):
            f=self.flows()[1]; n=3; cp=checkpoint_at(f,n,True); original=f['accepted_responses'][n]
            admission=fr4.admit(f,cp,f['observations'][n+1],provisional=original['post_observation'],record=record_for(f,n))
            replay=replay_evidence(original); response=o.unblob(replay['response'],True)
            if failure in ('actor','timestamp'):
                request=o.unblob(replay['request']); request['actor_subject_id' if failure=='actor' else 'action_timestamp_utc']='other'
                replay['request']=o.blob(request)
            elif failure=='command': response['command_id']='other'
            elif failure=='output': response['record']['notification_rendering_definition_revision_id']='other'
            elif failure=='provenance': response['record']['published']['actor_subject_id']='other'
            elif failure=='noop': response['effect']='rendering_definition_publish_noop'
            else:
                old=f['plan']['actions'][n]['expected']['revision_id']
                response['record'].update(notification_rendering_definition_revision_id=old,current_revision_id=old)
                replay['post_observation']['revision_id']=old
            reseal_response(replay,response)
            with self.subTest(failure=failure),self.assertRaises((ValueError,fr4.ValidationError)):
                fr4.replay_check(f,admission,replay)

    def test_both_binding_kinds_recheck_candidate_but_replay_original_cas(self):
        f=self.flows()[0]
        for n,action in enumerate(f['plan']['actions']):
            if action['command'] not in ('item_archetype.facet_binding.set','notification_profile.binding.set'):continue
            cp=checkpoint_at(f,n,True); post=f['accepted_responses'][n]['post_observation']
            admission=fr4.admit(f,cp,f['observations'][n+1],provisional=post)
            fr4.binding_recheck(f,admission,post)
            with self.assertRaisesRegex(ValueError,'immediate binding'):
                fr4.binding_recheck(f,admission,action['expected'])
            replay=replay_evidence(f['accepted_responses'][n]); fr4.replay_check(f,admission,replay)
            req=o.unblob(replay['request'])
            if action['command'].startswith('item_'):self.assertIsNone(req['expected_binding_id'])
            self.assertEqual(replay['request'],cp['unresolved_submission']['request'])

    def test_saved_verification_and_envelope(self):
        for flow in self.flows():
            fr4.verification_check(flow,flow['apply_result'],flow['verification'])
            o.artifact(flow['envelope'])
            self.assertEqual(flow['envelope']['artifact']['digest'],flow['verification']['content_identity']['digest'])

    def test_metadata_response_revision_matches_preimage_post_checkpoint_and_verification(self):
        flow = self.flows()[1]
        n = next(i for i, action in enumerate(flow['plan']['actions'])
                 if action['command'] == 'notification_profile.metadata.update')
        action = flow['plan']['actions'][n]
        result = deepcopy(flow['apply_result'])
        evidence = result['checkpoint']['accepted_responses'][n]
        response = o.unblob(evidence['response'], True)
        preserved = action['expected']['revision_id']
        self.assertEqual(response['notification_profile_revision_id'], preserved)
        self.assertEqual(evidence['post_observation']['revision_id'], preserved)
        response['notification_profile_revision_id'] = 'contradictory-revision'
        o.public_schema(action['command'], 'response', response)
        reseal_response(evidence, response)
        result['checkpoint'] = o.seal(result['checkpoint'])
        result = o.seal(result)
        o.artifact(result)
        o.artifact(result['checkpoint'])
        self.assertEqual(evidence['post_observation'], flow['accepted_responses'][n]['post_observation'])
        with self.assertRaisesRegex(ValueError, 'metadata revision identity'):
            fr4.evidence_check(flow['plan'], flow['approval'], action, evidence,
                               result['checkpoint']['accepted_responses'][:n])
        with self.assertRaisesRegex(ValueError, 'metadata revision identity'):
            fr4.checkpoint_check(flow['plan'], flow['approval'], result['checkpoint'])
        with self.assertRaisesRegex(ValueError, 'metadata revision identity'):
            fr4.admit(flow, result['checkpoint'], flow['observations'][-1])
        verification = fr4.verification(flow, flow['observations'][-1], result)
        self.assertEqual((verification['response_evidence'], verification['state']), ('invalid', 'mismatch'))
        self.assertEqual(verification['apply_result_digest'], result['content_identity']['digest'])
        false_success = deepcopy(flow['verification'])
        false_success['apply_result_digest'] = result['content_identity']['digest']
        with self.assertRaisesRegex(ValueError, 'verification correlation/outcome'):
            fr4.verification_check(flow, result, o.seal(false_success))

    def test_rendering_publish_replay_rejects_inconsistent_candidate_creation_provenance(self):
        flow = self.flows()[1]
        n = next(i for i, action in enumerate(flow['plan']['actions'])
                 if action['command'] == 'notification_rendering_definition.publish')
        cp = checkpoint_at(flow, n, True)
        evidence = flow['accepted_responses'][n]
        for field, replacement in (('actor_subject_id', 'different-creator'),
                                   ('command_id', 'different-creation-command'),
                                   ('action_timestamp_utc', '2030-01-01T12:00:00Z')):
            record = deepcopy(record_for(flow, n))
            record['created'][field] = replacement
            admission = fr4.admit(flow, cp, flow['observations'][n+1],
                                  provisional=evidence['post_observation'], record=record)
            self.assertEqual(admission['kind'], 'prefix_plus_one')
            self.assertEqual(admission['checkpoint'], cp)
            replay = replay_evidence(evidence)
            o.public_schema(evidence['command'], 'response', o.unblob(replay['response'], True))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'rendering replay record mismatch'):
                fr4.replay_check(flow, admission, replay)

    def test_rendering_publish_can_preserve_creation_from_an_earlier_execution(self):
        flow = self.flows()[1]
        n = next(i for i, action in enumerate(flow['plan']['actions'])
                 if action['command'] == 'notification_rendering_definition.publish')
        replay = replay_evidence(flow['accepted_responses'][n])
        response = o.unblob(replay['response'], True)
        response['record']['created'] = dict(actor_subject_id='earlier-creator',
            command_id='earlier-creation-command', action_timestamp_utc='2030-01-01T12:00:00Z')
        self.assertNotEqual(response['record']['created'], response['record']['published'])
        o.public_schema(replay['command'], 'response', response)
        reseal_response(replay, response)
        admission = fr4.admit(flow, checkpoint_at(flow, n, True), flow['observations'][n+1],
                              provisional=replay['post_observation'], record=response['record'])
        self.assertEqual(fr4.replay_check(flow, admission, replay), replay)

    def test_rendering_candidate_record_is_private_after_admission(self):
        flow = self.flows()[1]
        n = next(i for i, action in enumerate(flow['plan']['actions'])
                 if action['command'] == 'notification_rendering_definition.publish')
        record = deepcopy(record_for(flow, n))
        original = deepcopy(record)
        admission = fr4.admit(flow, checkpoint_at(flow, n, True), flow['observations'][n+1],
                              provisional=flow['accepted_responses'][n]['post_observation'], record=record)
        record['created']['actor_subject_id'] = 'caller-mutated-after-admission'
        self.assertEqual(admission['rendering_record'], original)
        replay = replay_evidence(flow['accepted_responses'][n])
        self.assertEqual(fr4.replay_check(flow, admission, replay), replay)

    def test_missing_partial_invalid_evidence_and_invalid_outer_input(self):
        flow=self.flows()[0]; fresh=flow['observations'][-1]
        for result in (None,flow['partial_result'],flow['empty_prefix_partial']):
            value=fr4.verification(flow,fresh,result)
            self.assertEqual((value['response_evidence'],value['state']),('missing','mismatch'))
        invalid=deepcopy(flow['apply_result']); e=invalid['checkpoint']['accepted_responses'][0]
        response=o.unblob(e['response'],True); response['receipt']['command_id']='other'; reseal_response(e,response)
        invalid['checkpoint']=o.seal(invalid['checkpoint']); invalid=o.seal(invalid)
        value=fr4.verification(flow,fresh,invalid)
        self.assertEqual((value['response_evidence'],value['state']),('invalid','mismatch'))
        self.assertEqual(value['apply_result_digest'],invalid['content_identity']['digest'])
        invalid['content_identity']['digest']='0'*64
        with self.assertRaisesRegex(ValueError,'artifact digest'):fr4.verification(flow,fresh,invalid)

    def test_verification_exact_heads_edges_decoders_owners_and_target(self):
        flow=self.flows()[0]
        for failure in ('schema_head','rendering_head','facet_pin','profile_pin','decoder','owner','target','environment'):
            fresh=deepcopy(flow['observations'][-1]); rows={r['object_key']:r for r in fresh['entries']}; kwargs={}
            if failure in ('schema_head','rendering_head'):
                rows[('schema' if failure=='schema_head' else 'rendering')+':flight_details']['revision_id']='later-equivalent'
            elif failure in ('facet_pin','profile_pin'):
                row=rows['facet_binding:flight:flight' if failure=='facet_pin' else 'profile:synthetic_flight_details']
                value=o.unblob(row['value'])
                if failure=='facet_pin':value['facet_schema_revision_id']='later-equivalent'
                else:
                    template=next(t for t in value['revision']['templates'] if t['rendering']['kind']=='definition')
                    template['rendering']['definition']['notification_rendering_definition_revision_id']='later-equivalent'
                    row['revision_id']='changed-profile-reference'
                row['value']=o.blob(value)
            elif failure=='decoder':rows['profile:synthetic_flight_details']['revision_contract']='spine.notification-profiles.v1'
            elif failure=='owner':rows['schema:flight_details']['owner']['owner_subject_id']='foreign'
            elif failure=='target':kwargs['target']=dict(flow['plan']['request']['target'],host_name='other.invalid')
            else:kwargs['environment']=dict(flow['plan']['environment'],ledger_instance_id='ledger_instance_'+'f'*64)
            with self.subTest(failure=failure):
                if failure in ('decoder','owner','target','environment'):
                    with self.assertRaises((ValueError,fr4.ValidationError)):
                        fr4.verification(flow,reseal_view(fresh),flow['apply_result'],**kwargs)
                else:
                    value=fr4.verification(flow,reseal_view(fresh),flow['apply_result'])
                    self.assertEqual(value['state'],'mismatch')

    def test_unselected_changes_pass_verify_but_fail_continuation(self):
        flow=self.flows()[0]; fresh=deepcopy(flow['observations'][-1]); extra=deepcopy(fresh['entries'][0])
        extra.update(object_key='archetype:unselected',root_id='other-root',revision_id='other-revision')
        fresh['entries'].append(extra); fresh['entries'].sort(key=lambda r:r['object_key']); reseal_view(fresh)
        self.assertEqual(fr4.verification(flow,fresh,flow['apply_result'])['state'],'verified')
        with self.assertRaisesRegex(ValueError,'unexplained catalog change'):
            fr4.admit(flow,flow['final_checkpoint'],fresh)

    def test_verify_does_not_require_unused_execution_lineage_or_active_missing_objects(self):
        flow=self.flows()[1]; fresh=deepcopy(flow['observations'][-1])
        fresh['historical_revisions']=[]; reseal_view(fresh)
        self.assertEqual(fr4.verification(flow,fresh,flow['apply_result'])['state'],'verified')
        with self.assertRaisesRegex(ValueError,'unexplained catalog change'):
            fr4.admit(flow,flow['final_checkpoint'],fresh)
        for kind in ('missing','retired'):
            fresh=deepcopy(flow['observations'][-1])
            if kind=='missing':
                fresh['entries']=[r for r in fresh['entries'] if r['object_key']!='binding:flight']
            else:
                next(r for r in fresh['entries'] if r['object_key']=='schema:flight_details')['status']='retired'
            value=fr4.verification(flow,reseal_view(fresh),flow['apply_result'])
            self.assertEqual(value['state'],'mismatch')

    def test_candidate_and_checkpoint_budgets_fail_closed(self):
        flow=self.flows()[0]; fresh=deepcopy(flow['observations'][-1])
        extra=deepcopy(fresh['entries'][0])
        for n in range(4097):
            row=deepcopy(extra); row.update(object_key=f'archetype:extra_{n:04}',
                                          root_id=f'root_{n}',revision_id=f'revision_{n}')
            fresh['entries'].append(row)
        fresh['entries'].sort(key=lambda r:r['object_key']); reseal_view(fresh)
        with self.assertRaises((ValueError,fr4.ValidationError)):
            fr4.admit(flow,flow['final_checkpoint'],fresh)
        cp=deepcopy(flow['prepared_checkpoint']); cp['unresolved_submission']['request']['canonical_json']='{}'
        with self.assertRaisesRegex(ValueError,'embedded digest'):
            fr4.admit(flow,o.seal(cp),flow['observations'][len(cp['accepted_responses'])])

    def test_verification_rejects_corrupt_known_immutable_definition_not_a_missing_object(self):
        flow=self.flows()[0]; fresh=deepcopy(flow['observations'][-1])
        row=next(r for r in fresh['entries'] if r['object_key']=='schema:flight_details')
        value=o.unblob(row['value']); value['description']='corrupt immutable body'; row['value']=o.blob(value)
        with self.assertRaisesRegex(ValueError,'immutable revision identity/content'):
            fr4.verification(flow,reseal_view(fresh),flow['apply_result'])

    def test_no_write_verification_and_invalid_supplied_evidence(self):
        flow=self.flows()[0]; plan=flow['plan']; final=flow['observations'][-1]
        rows={r['object_key']:r for r in final['entries']}
        plan.update(observation=deepcopy(final),actions=[],decision_action_ids=[])
        for c in plan['classifications']:c.update(classification='equivalent',observed=rows[c['object_key']])
        for r in plan['resolutions']:
            for field in ('root','revision','binding'):
                value=rows[r['object_key']][field+'_id']
                key='archetype:flight' if field=='root' and r['object_key'].split(':')[0] in ('binding','facet_binding') else r['object_key']
                r[field]=dict(kind='observed',object_key=key,field=field,value=value) if value else None
        flow['plan']=o.seal(plan)
        value=fr4.verification(flow,final)
        self.assertEqual((value['response_evidence'],value['state'],value['apply_result_digest']),('not_required','verified',None))
        value=fr4.verification(flow,final,flow['apply_result'])
        self.assertEqual((value['response_evidence'],value['state'],value['apply_result_digest']),('invalid','mismatch',None))

    def test_no_transport_or_database_authority_in_contract_proof(self):
        with patch('subprocess.Popen',side_effect=AssertionError('no subprocess')), \
                patch('sqlite3.connect',side_effect=AssertionError('no database')):
            for flow in self.flows():
                fr4.admit(flow,flow['final_checkpoint'],flow['observations'][-1])
                fr4.verification_check(flow,flow['apply_result'],flow['verification'])


if __name__=='__main__':unittest.main()
