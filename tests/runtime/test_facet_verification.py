"""FR-4 read-only verification against synthetic public catalogs, never a ledger."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests/contract')]
from spine_packs import artifacts as a
from spine_packs.facet_apply import checkpoint, result as apply_result
from spine_packs.facet_contracts import blob, body, seal
from spine_packs.facet_execution import ExecutionContext
from spine_packs.facet_inventory import READ_COMMANDS
from spine_packs.facet_manifest import digest as manifest_digest
from spine_packs.facet_planning import build_plan
from spine_packs.facet_verification import verify_installation
from spine_packs.planning import ENVIRONMENT, PlanError
from test_facet_continuation import PublicCatalog, reseal_view
from test_facet_execution import flow
from test_facet_planning import CURSORS
from test_facet_recovery import companion
import facet_artifact_oracle as independent
import fr4_contract_oracle as oracle
from fr3_fixture_support import current_contracts


def final_view(name='flight-create'):
    return deepcopy(companion(name)['observations'][-1])


def approval(plan, execution):
    return seal(dict(artifact_schema='spine.pack-install-approval.v2',
        plan_digest=plan['content_identity']['digest'], approve_complete_plan=True,
        acknowledge_single_operator=True, authorized_update_action_ids=plan['decision_action_ids'],
        execution=deepcopy(execution)))


def no_write_flow(*, draft=False, ordinary_v1=False):
    f=flow(); view=final_view()
    # Independent verification doesn't need unused execution lineage.
    view['historical_revisions']=[]
    if ordinary_v1:
        f['manifest']['facet_schemas']=[]; f['manifest']['archetype_facet_bindings']=[]
        f['manifest']['rendering_definitions']=[]
        for profile in f['manifest']['notification_profiles']:
            for template in profile['revision']['templates']: template['rendering']={'kind':'ordinary'}
        view['entries']=[r for r in view['entries'] if r['object_key'].split(':')[0] in ('archetype','profile','binding')]
        row=next(r for r in view['entries'] if r['object_key'].startswith('profile:'))
        value=body(row['value'])
        for template in value['revision']['templates']: template.pop('rendering')
        row.update(revision_contract='spine.notification-profiles.v1',value=blob(value))
    if draft:
        f['manifest']['pack'].update(status='draft',version='1.0.1-draft.1')
        f['request']['request']['draft_posture']='inspect_only'
        f['request']=seal(f['request'])
    f['manifest']['content_identity']['digest']=manifest_digest(f['manifest'])
    view=reseal_view(view)
    f['plan']=build_plan(f['manifest'],f['request'],f['plan']['environment'],view)
    f['approval']=approval(f['plan'],f['approval']['execution'])
    cp=checkpoint(f['plan'],f['approval'],[])
    f['apply_result']=apply_result(f['plan'],cp,'applied')
    return f,view


def wire(e,response):
    text=json.dumps(response)
    e['response']=dict(json_text=text,digest=hashlib.sha256(text.encode()).hexdigest())


class VerificationTests(unittest.TestCase):
    def check(self,f,view,result=None,*,transport=None,page_size=1):
        t=transport or PublicCatalog(f,6,view)
        original=deepcopy((f,view,result,t.rows))
        t.write=Mock(side_effect=AssertionError('verify cannot write or replay'))
        with patch.dict('os.environ',CURSORS), patch('subprocess.Popen',side_effect=AssertionError('no processes')), patch(
                'spine_packs.facet_apply.apply_continuation',side_effect=AssertionError('no continuation')), patch(
                'spine_packs.facet_recovery.preflight_continuation',side_effect=AssertionError('no recovery')):
            value=verify_installation(f['manifest'],f['plan'],t,result,page_size=page_size)
        t.write.assert_not_called()
        self.assertTrue(all(command in READ_COMMANDS for command,_ in t.reads))
        self.assertEqual(original,(f,view,result,t.rows))
        self.assertEqual(value['receipt_readback'],'captured_responses_only_spine_0.10.0')
        self.assertEqual(value['disclosure'],'separate_operator_configuration_required')
        self.assertEqual([r['object_key'] for r in value['object_results']],f['plan']['closure'])
        if independent.Draft202012Validator is not None:
            with current_contracts(): oracle.verification_check(f,result,value)
        return value,t

    def test_complete_create_update_evidence_and_fresh_state_match_independent_oracle(self):
        for name in ('flight-create','flight-update'):
            f=flow(name); value,t=self.check(f,final_view(name),f['apply_result'])
            self.assertEqual(value['state'],'verified'); self.assertEqual(value['response_evidence'],'complete')
            self.assertEqual(value['apply_result_digest'],f['apply_result']['content_identity']['digest'])
            self.assertTrue(all(r['state']=='equivalent' for r in value['object_results']))
            self.assertEqual(value['observation']['historical_revisions'],[])
            self.assertEqual(sum(command=='system.info' for command,_ in t.reads),2)

    def test_no_write_released_and_draft_plans_need_no_receipt_or_approval(self):
        for draft in (False,True):
            f,view=no_write_flow(draft=draft)
            self.assertFalse(f['plan']['actions'])
            for result in (None,f['apply_result']):
                value,_=self.check(f,view,result)
                invalid=draft and result is not None
                self.assertEqual(value['state'],'mismatch' if invalid else 'verified')
                self.assertEqual(value['response_evidence'],'invalid' if invalid else 'not_required')
                self.assertIsNone(value['apply_result_digest'])
            if draft:
                with self.assertRaises(PlanError): ExecutionContext(f['manifest'],f['plan'],f['approval'])

    def test_missing_evidence_never_guesses_ids_from_matching_current_definitions(self):
        f=flow(); value,_=self.check(f,final_view())
        self.assertEqual(value['state'],'mismatch'); self.assertEqual(value['response_evidence'],'missing')
        self.assertTrue(all(r['state']=='blocked' and r['observed'] is not None for r in value['object_results']))
        self.assertIsNone(value['apply_result_digest'])

    def test_partial_and_not_applied_evidence_remains_missing_even_when_fresh_state_matches(self):
        for name in ('flight-create','flight-update'):
            f=flow(name)
            for result in (f['partial_result'],f['empty_prefix_partial']):
                value,_=self.check(f,final_view(name),result)
                self.assertEqual(value['response_evidence'],'missing'); self.assertEqual(value['state'],'mismatch')
                self.assertEqual(value['apply_result_digest'],result['content_identity']['digest'])
            cp=checkpoint(f['plan'],f['approval'],[])
            result=apply_result(f['plan'],cp,'not_applied',PlanError(ENVIRONMENT,'synthetic_failure'))
            value,_=self.check(f,final_view(name),result)
            self.assertEqual(value['response_evidence'],'missing'); self.assertEqual(value['state'],'mismatch')

    def test_valid_outer_artifact_with_invalid_embedded_evidence_is_completed_mismatch(self):
        f=flow('flight-update'); good=f['apply_result']
        for fault in ('plan','approval','execution','timestamp','checkpoint_digest','order','coverage','next',
                      'request','wire_digest','receipt','metadata_revision','post','immutable'):
            result=deepcopy(good); cp=result['checkpoint']; accepted=cp['accepted_responses']
            if fault=='plan': cp['plan_digest']='0'*64
            elif fault=='approval': cp['approval_digest']='0'*64
            elif fault=='execution': cp['execution']['actor_subject_id']='other'
            elif fault=='timestamp': cp['execution']['action_timestamp_utc']='2035-02-02T12:00:00Z'
            elif fault=='order': accepted.reverse()
            elif fault=='coverage': accepted.pop()
            elif fault=='next': cp['next_action_id']='action-000001'
            elif fault=='request':
                request=body(accepted[0]['request']); request['actor_subject_id']='other'; accepted[0]['request']=blob(request)
            elif fault=='wire_digest': accepted[0]['response']['digest']='0'*64
            elif fault=='receipt': accepted[0]['receipt']['command_receipt_id']='other'
            elif fault=='metadata_revision':
                e=next(e for e in accepted if e['command']=='notification_profile.metadata.update')
                response=json.loads(e['response']['json_text']); response['notification_profile_revision_id']='other'; wire(e,response)
            elif fault=='post': accepted[0]['post_observation']['root_id']='other'
            elif fault=='immutable': accepted[0]['post_observation']['revision_id']=f['plan']['actions'][0]['expected']['revision_id']
            result['checkpoint']=seal(cp)
            if fault=='checkpoint_digest': result['checkpoint']['content_identity']['digest']='0'*64
            result=seal(result)
            with self.subTest(fault=fault):
                value,_=self.check(f,final_view('flight-update'),result)
                self.assertEqual(value['state'],'mismatch'); self.assertEqual(value['response_evidence'],'invalid')
                self.assertEqual(value['apply_result_digest'],result['content_identity']['digest'])

    def test_pending_request_and_partial_suffix_correlations_are_checked(self):
        f=flow('flight-update')
        for fault in ('pending_request','pending_command','failure','unattempted'):
            result=deepcopy(f['partial_result']); cp=result['checkpoint']
            if fault=='pending_request':
                request=body(cp['unresolved_submission']['request']); request['actor_subject_id']='other'
                cp['unresolved_submission']['request']=blob(request)
            elif fault=='pending_command': cp['unresolved_submission']['command_id']='other'
            elif fault=='failure': result['failure']['action_id']='action-000000'
            else: result['unattempted_action_ids']=[]
            result['checkpoint']=seal(cp); result=seal(result)
            with self.subTest(fault=fault):
                value,_=self.check(f,final_view('flight-update'),result)
                self.assertEqual(value['response_evidence'],'invalid')

    def test_invalid_supplied_evidence_cannot_be_ignored_for_no_write_plans(self):
        f,view=no_write_flow()
        bad=deepcopy(f['apply_result']); bad['checkpoint']['approval_digest']='0'*64
        bad['checkpoint']=seal(bad['checkpoint']); bad=seal(bad)
        value,_=self.check(f,view,bad)
        self.assertEqual(value['response_evidence'],'invalid'); self.assertEqual(value['state'],'mismatch')
        self.assertIsNone(value['apply_result_digest'])

    def test_malformed_outer_results_fail_before_any_public_observation(self):
        f=flow()
        for fault in ('kind','shape','digest','size','not_object'):
            bad=deepcopy(f['apply_result'])
            if fault=='kind': bad['artifact_schema']='spine.pack-apply-result.v1'
            elif fault=='shape': bad['extra']='private-sentinel'
            elif fault=='digest': bad['content_identity']['digest']='0'*64
            elif fault=='size': bad['checkpoint']['execution']['actor_subject_id']='x'*(33*1024*1024)
            else: bad=[]
            t=Mock()
            with self.subTest(fault=fault), patch('spine_packs.facet_verification.observe') as read:
                with self.assertRaises(PlanError) as caught: verify_installation(f['manifest'],f['plan'],t,bad)
                read.assert_not_called(); t.write.assert_not_called()
            self.assertNotIn('private-sentinel',str(caught.exception))

    def test_wrong_manifest_resealed_plan_or_baseline_never_reaches_target(self):
        for fault in ('manifest','plan','closure','runtime','schema','contracts'):
            f=flow()
            if fault=='manifest':
                f['manifest']['archetypes'][0]['revision']['display_name']='Other'
                f['manifest']['content_identity']['digest']=manifest_digest(f['manifest'])
            elif fault=='plan': f['plan']['actions'][0]['object_key']='archetype:other'
            elif fault=='closure': f['plan']['closure'].pop()
            elif fault=='runtime': f['plan']['environment']['runtime_version']='0.9.1'
            elif fault=='schema': f['plan']['environment']['ledger_schema_current']='20'
            else: f['plan']['required_execution_contracts'].pop()
            f['plan']=seal(f['plan'])
            with self.subTest(fault=fault), patch('spine_packs.facet_verification.observe') as read:
                with self.assertRaises(PlanError): verify_installation(f['manifest'],f['plan'],Mock())
                read.assert_not_called()

    def test_wrong_target_and_fresh_environment_fail_without_a_verification_artifact(self):
        f=flow(); t=Mock(target=deepcopy(f['plan']['request']['target'])); t.target['host_name']='other.invalid'
        with patch('spine_packs.facet_verification.observe') as read:
            with self.assertRaisesRegex(PlanError,'verification_target_mismatch'):
                verify_installation(f['manifest'],f['plan'],t,f['apply_result'])
            read.assert_not_called()
        t=PublicCatalog(f,6,final_view()); old_read=t.read
        def changed(command,request):
            r=old_read(command,request)
            if command=='system.info': r['ledger_instance_id']='ledger_instance_'+'0'*64
            return r
        t.read=changed
        with self.assertRaisesRegex(PlanError,'verification_environment_mismatch'): self.check(f,final_view(),f['apply_result'],transport=t)

    def test_same_content_new_schema_or_rendering_head_does_not_verify_historical_pin(self):
        for family in ('schema','rendering'):
            f=flow(); view=final_view(); row=next(r for r in view['entries'] if r['object_key'].startswith(family+':'))
            old=deepcopy(row); row['revision_id']='new_equivalent_revision'
            view['historical_revisions']=[old]; reseal_view(view)
            value,_=self.check(f,view,f['apply_result'])
            observed=next(r for r in value['object_results'] if r['object_key']==row['object_key'])
            self.assertEqual(observed['state'],'drifted'); self.assertEqual(value['state'],'mismatch')
            self.assertEqual(len(value['observation']['historical_revisions']),1)

    def test_facet_binding_and_v2_profile_identities_remain_exact(self):
        for family,field in (('facet_binding','binding_id'),('profile','revision_id')):
            f=flow(); view=final_view(); row=next(r for r in view['entries'] if r['object_key'].startswith(family+':'))
            row[field]='equivalent_other_id'; reseal_view(view)
            value,_=self.check(f,view,f['apply_result'])
            self.assertEqual(next(r for r in value['object_results'] if r['object_key']==row['object_key'])['state'],'drifted')

    def test_archetype_equivalent_head_and_same_target_default_binding_replacement_are_allowed(self):
        f=flow(); view=final_view()
        for row in view['entries']:
            if row['object_key'].startswith('archetype:'): row['revision_id']='equivalent_other_revision'
            elif row['object_key'].startswith('binding:'): row['binding_id']='equivalent_other_binding'
        reseal_view(view)
        value,_=self.check(f,view,f['apply_result']); self.assertEqual(value['state'],'verified')

    def test_ordinary_v1_profile_keeps_decoder_and_semantic_revision_equivalence(self):
        f,view=no_write_flow(ordinary_v1=True)
        self.assertFalse(f['plan']['actions'])
        row=next(r for r in view['entries'] if r['object_key'].startswith('profile:'))
        row['revision_id']='equivalent_v1_head'; reseal_view(view)
        value,_=self.check(f,view)
        self.assertEqual(value['state'],'verified')
        observed=next(r['observed'] for r in value['object_results'] if r['object_key'].startswith('profile:'))
        self.assertEqual(observed['revision_contract'],'spine.notification-profiles.v1')

    def test_mutable_profile_metadata_drift_is_not_an_immutable_revision_failure(self):
        f=flow(); view=final_view()
        row=next(r for r in view['entries'] if r['object_key'].startswith('profile:'))
        value=body(row['value']); value['metadata']['display_name']='New mutable display name'
        row['value']=blob(value); reseal_view(view)
        value,_=self.check(f,view,f['apply_result'])
        self.assertEqual(next(r for r in value['object_results'] if r['object_key']==row['object_key'])['state'],'drifted')

    def test_equal_schema_content_on_another_actual_root_cannot_satisfy_a_facet_pin(self):
        f=flow(); view=final_view()
        other=deepcopy(next(r for r in view['entries'] if r['object_key'].startswith('schema:')))
        other.update(object_key='schema:other_details',root_id='other_schema',revision_id='other_schema_revision')
        view['entries'].append(other); view['entries'].sort(key=lambda r:r['object_key'])
        binding=next(r for r in view['entries'] if r['object_key'].startswith('facet_binding:'))
        value=body(binding['value']); value['facet_schema_revision_id']=other['revision_id']; binding['value']=blob(value)
        reseal_view(view)
        value,t=self.check(f,view,f['apply_result'],page_size=100)
        observed=next(r for r in value['object_results'] if r['object_key']==binding['object_key'])
        self.assertEqual(observed['state'],'drifted')
        self.assertTrue(any(cmd=='facet_schema.revision.show' and request['facet_schema_revision_id']==other['revision_id']
                            for cmd,request in t.reads))

    def test_unrelated_unselected_change_does_not_fail_selected_verification(self):
        f=flow(); view=final_view()
        row=deepcopy(next(r for r in view['entries'] if r['object_key'].startswith('archetype:')))
        row.update(object_key='archetype:unselected',root_id='other_root',revision_id='other_revision')
        value=body(row['value']); value['display_name']='Unrelated archetype'; row['value']=blob(value)
        view['entries'].append(row); view['entries'].sort(key=lambda r:r['object_key']); reseal_view(view)
        # The synthetic body source's archetype key must follow its actual row.
        t=PublicCatalog(f,6,view); original=t.record
        def record(row):
            value=original(row)
            if row['object_key'].startswith('archetype:'): value['archetype_key']=row['object_key'].split(':')[1]
            return value
        t.record=record
        value,_=self.check(f,view,f['apply_result'],transport=t,page_size=100)
        self.assertEqual(value['state'],'verified'); self.assertNotIn('archetype:unselected',value['closure'])

    def test_missing_root_is_reported_without_discarding_other_fresh_projections(self):
        f=flow(); view=final_view()
        view['entries']=[r for r in view['entries'] if not r['object_key'].startswith(('archetype:','facet_binding:','binding:'))]
        view['historical_revisions']=[]; reseal_view(view)
        value,_=self.check(f,view,f['apply_result'])
        states={r['object_key']:r['state'] for r in value['object_results']}
        self.assertEqual(states['archetype:flight'],'missing'); self.assertEqual(states['profile:synthetic_flight_details'],'equivalent')

    def test_retired_selected_schema_is_blocked_not_recreated_or_hidden(self):
        f=flow(); view=final_view(); row=next(r for r in view['entries'] if r['object_key'].startswith('schema:'))
        row['status']='retired'; reseal_view(view)
        t=PublicCatalog(f,6,view); original=t.record
        def record(row):
            value=original(row)
            if row['object_key'].startswith('schema:'): value['root']['status']=row['status']
            return value
        t.record=record
        value,_=self.check(f,view,f['apply_result'],transport=t)
        self.assertEqual(next(r for r in value['object_results'] if r['object_key']==row['object_key'])['state'],'blocked')

    def test_known_immutable_body_contradiction_is_environment_failure_not_mismatch(self):
        f=flow(); view=final_view(); row=next(r for r in view['entries'] if r['object_key'].startswith('schema:'))
        value=body(row['value']); value['display_name']='Contradictory immutable definition'; row['value']=blob(value)
        reseal_view(view)
        with self.assertRaisesRegex(PlanError,'immutable_revision_contradiction') as caught:
            self.check(f,view,f['apply_result'])
        self.assertEqual(caught.exception.category,ENVIRONMENT)

    def test_blocked_plan_resolutions_remain_unprovable_even_if_old_rows_are_readable(self):
        f,view=no_write_flow()
        schema=next(r for r in view['entries'] if r['object_key'].startswith('schema:'))
        schema['status']='retired'; reseal_view(view)
        f['manifest']['facet_schemas'][0]['definition']['display_name']='New desired definition'
        f['manifest']['content_identity']['digest']=manifest_digest(f['manifest'])
        f['plan']=build_plan(f['manifest'],f['request'],f['plan']['environment'],view)
        self.assertTrue(f['plan']['blocked_object_keys'])
        t=PublicCatalog(f,6,view); original=t.record
        def record(row):
            value=original(row)
            if row['object_key'].startswith('schema:'): value['root']['status']=row['status']
            return value
        t.record=record
        value,_=self.check(f,view,transport=t)
        self.assertEqual(value['state'],'mismatch')
        states={r['object_key']:r['state'] for r in value['object_results']}
        for key in f['plan']['blocked_object_keys']: self.assertEqual(states[key],'blocked')

    def test_observation_failure_precedence_is_not_converted_to_object_mismatch(self):
        f=flow(); bad=deepcopy(f['apply_result']); bad['checkpoint']['approval_digest']='0'*64
        bad['checkpoint']=seal(bad['checkpoint']); bad=seal(bad)
        for category,code in ((ENVIRONMENT,'observation_capacity'),(ENVIRONMENT,'corrupt_evidence'),
                              ('spine_command_rejection','referenced_revision_missing')):
            t=Mock(target=deepcopy(f['plan']['request']['target']))
            with patch('spine_packs.facet_verification.observe',side_effect=PlanError(category,code)):
                with self.assertRaises(PlanError) as caught: verify_installation(f['manifest'],f['plan'],t,bad)
            self.assertEqual((caught.exception.category,caught.exception.code),(category,code)); t.write.assert_not_called()

    def test_public_wrong_owner_and_hash_are_environment_failures(self):
        for fault in ('owner','hash'):
            f=flow(); view=final_view(); t=PublicCatalog(f,6,view); original=t.read
            def corrupt(command,request):
                response=original(command,request)
                if command=='facet_schema.show':
                    if fault=='owner': response['root']['owner']['owner_subject_id']='foreign'
                    else: response['revision']['definition_hash']='0'*64
                return response
            t.read=corrupt
            with self.subTest(fault=fault), self.assertRaises(PlanError) as caught:
                self.check(f,view,f['apply_result'],transport=t)
            self.assertEqual(caught.exception.category,ENVIRONMENT)

    def test_public_referenced_revision_failure_and_capacity_abort_without_repair(self):
        for fault in ('missing','capacity'):
            f=flow(); view=final_view(); t=PublicCatalog(f,6,view); original=t.read
            def read(command,request):
                if command=='facet_schema.revision.show':
                    if fault=='missing': raise PlanError('spine_command_rejection','referenced_revision_missing')
                    t.budget.calls=4096
                return original(command,request)
            t.read=read
            with self.subTest(fault=fault), self.assertRaises(PlanError) as caught:
                self.check(f,view,f['apply_result'],transport=t)
            self.assertEqual(caught.exception.code,'referenced_revision_missing' if fault=='missing' else 'observation_capacity')


if __name__=='__main__': unittest.main()
