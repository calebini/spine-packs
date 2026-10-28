"""FR-4 synthetic admission/replay and internal durability tests, no ledgers."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from spine_packs import artifacts as a
from spine_packs.facet_apply import apply_continuation, checkpoint, checkpoint_writer
from spine_packs.facet_contracts import blob, body, seal
from spine_packs.facet_inventory import COMMANDS
from spine_packs.facet_observation import FAMILIES, observe, snapshots
from spine_packs.facet_recovery import RecoveryPreimage, continuation_context, preflight_continuation
from spine_packs.facet_transport import ObservationBudget
from spine_packs.planning import ENVIRONMENT, PlanError
from test_facet_apply import Catalog, TRANSCRIPT, independent, current_contracts
from test_facet_execution import flow
from test_facet_recovery import companion
from test_facet_planning import CURSORS, Replay, fixture
from fr4_fixture_support import profile_history_flow


def prepared(f, n):
    e = f['accepted_responses'][n]
    return checkpoint(f['plan'], f['approval'], f['accepted_responses'][:n], dict(
        action_id=e['action_id'], command_id=e['command_id'], submission_state='prepared_or_submitted',
        request=deepcopy(e['request'])))


def context(f, cp):
    return RecoveryPreimage(f['manifest'], f['plan'], f['approval'], cp)


def record_for(f, n):
    e = f['accepted_responses'][n]; response = json.loads(e['response']['json_text'])
    if e['command'].startswith('notification_rendering_definition.'):
        return dict(rendering_record=deepcopy(response['record']))
    if e['command'].startswith('item_archetype.') and e['command'] != 'item_archetype.facet_binding.set':
        record = deepcopy(next(r['response']['item_archetype'] for r in TRANSCRIPT['reads']
                               if r['command'] == 'item_archetype.show'))
        row = e['post_observation']; value = body(row['value']); request = body(e['request'])
        record.update(item_archetype_id=row['root_id'], current_revision_id=row['revision_id'],
                      archetype_key=row['object_key'].split(':')[1])
        provenance = dict(created_by_command_id=request['command_id'],
            created_by_subject_id=request['actor_subject_id'], created_at_utc=request['action_timestamp_utc'])
        record['revision'].update(value, **provenance, item_archetype_id=row['root_id'],
            item_archetype_revision_id=row['revision_id'], normalized_content_hash=a.digest(value),
            revision_number=int(response['revision_number']))
        if e['command'].endswith('.create'): record.update(provenance)
        return dict(archetype_record=record)
    return {}


def replay_bytes(e):
    response = json.loads(e['response']['json_text'])
    if 'replayed' in response: response.update(replayed=True, changed=False)
    return json.dumps(response, separators=(',', ':')).encode() + b'\n'


def admit(f, cp, view, **records):
    return context(f, cp).admit(view, environment=f['plan']['environment'],
                              target=f['plan']['request']['target'], **records)


def reseal_view(view):
    view['public_catalog_snapshots'] = snapshots(view['entries'])
    view['digest'] = a.digest(dict(derivation_version='spine.pack-observation.v2',
                                  view={k:v for k,v in view.items() if k != 'digest'}))
    return view


class AdmissionTests(unittest.TestCase):
    def test_all_eleven_commands_at_every_prepared_lost_and_accepted_boundary(self):
        commands = set()
        with patch('subprocess.Popen', side_effect=AssertionError('no processes')):
            for name in ('flight-create', 'flight-update'):
                f = flow(name); views = companion(name)['observations']; original = deepcopy(f)
                for n, e in enumerate(f['accepted_responses']):
                    cp = prepared(f, n); commands.add(e['command'])
                    for lost in (False, True):
                        view = views[n + int(lost)]; before = deepcopy(view)
                        handle = admit(f, cp, view, **(record_for(f, n) if lost else {}))
                        self.assertEqual(handle.kind, 'prefix_plus_one' if lost else 'prefix')
                        self.assertEqual(handle.checkpoint(), cp)
                        self.assertEqual(handle.retry_request(), body(e['request']))
                        evidence = handle.replay_evidence(replay_bytes(e), e['post_observation'])
                        self.assertEqual(evidence['request'], cp['unresolved_submission']['request'])
                        self.assertEqual(evidence['post_observation'], e['post_observation'])
                        self.assertEqual(handle.checkpoint(), cp)  # Correlation is not acceptance.
                        self.assertEqual(view, before)
                    accepted = checkpoint(f['plan'], f['approval'], f['accepted_responses'][:n+1])
                    self.assertEqual(admit(f, accepted, views[n+1]).kind, 'prefix')
                self.assertEqual(f, original)
        self.assertEqual(commands, {k for k,v in COMMANDS.items() if v['phase'] is not None})

    def test_no_uncertain_request_cannot_explain_a_change_or_infer_a_retry(self):
        f = flow(); views = companion('flight-create')['observations']
        with self.assertRaises(PlanError): admit(f, f['initial_checkpoint'], views[1], **record_for(f, 0))
        handle = admit(f, f['final_checkpoint'], views[-1])
        with self.assertRaises(PlanError): handle.retry_request()
        with self.assertRaises(PlanError): handle.replay_evidence(b'{}', {})

    def test_unexplained_suffix_effects_are_never_admitted(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name); views = companion(name)['observations']
            for n in range(len(f['accepted_responses']) - 1):
                with self.subTest(flow=name, n=n), self.assertRaises(PlanError):
                    admit(f, prepared(f,n), views[n+2], **record_for(f,n))

    def test_owner_status_digest_and_unrelated_drift_fail_closed(self):
        f = flow('flight-update'); views = companion('flight-update')['observations']; n = 1
        for fault in ('owner', 'status', 'digest', 'other_root', 'duplicate', 'missing_history'):
            view = deepcopy(views[n+1])
            if fault == 'owner': view['entries'][0]['owner']['owner_subject_id'] = 'other'
            elif fault == 'status': view['entries'][0]['status'] = 'retired'
            elif fault == 'other_root': view['entries'][0]['root_id'] = 'other'
            elif fault == 'duplicate': view['entries'].append(deepcopy(view['entries'][0]))
            elif fault == 'missing_history': view['historical_revisions'].clear()
            reseal_view(view)
            if fault == 'digest': view['digest'] = '0' * 64
            with self.subTest(fault=fault), self.assertRaises(PlanError): admit(f, prepared(f,n), view)

    def test_rendering_provenance_hash_and_complete_record_are_required(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); n = next(i for i,e in enumerate(f['accepted_responses'])
                if e['command'].startswith('notification_rendering_definition.'))
            cp = prepared(f,n); view = companion(name)['observations'][n+1]
            for fault in ('missing', 'hash', 'root', 'revision', 'current', 'owner', 'actor', 'command', 'time'):
                record = record_for(f,n)['rendering_record']
                if fault == 'missing': record = None
                elif fault == 'hash': record['definition_hash'] = '0' * 64
                elif fault == 'root': record['notification_rendering_definition_id'] = 'other'
                elif fault == 'revision': record['notification_rendering_definition_revision_id'] = 'other'
                elif fault == 'current': record['current_revision_id'] = 'other'
                elif fault == 'owner': record['owner']['owner_subject_id'] = 'other'
                else:
                    field = {'actor':'actor_subject_id', 'command':'command_id', 'time':'action_timestamp_utc'}[fault]
                    record['published'][field] = '2035-02-02T12:00:00Z' if fault == 'time' else 'other'
                with self.subTest(flow=name,fault=fault), self.assertRaises(PlanError):
                    admit(f,cp,view,rendering_record=record)

    def test_rendering_publish_retains_earlier_creation_and_private_record_through_replay(self):
        f = flow('flight-update'); n = next(i for i,e in enumerate(f['accepted_responses'])
            if e['command'] == 'notification_rendering_definition.publish')
        e = f['accepted_responses'][n]; record = record_for(f,n)['rendering_record']
        handle = admit(f, prepared(f,n), companion('flight-update')['observations'][n+1], rendering_record=record)
        record['created']['command_id'] = 'caller-mutated'
        handle.replay_evidence(replay_bytes(e), e['post_observation'])
        for field in ('command_id','actor_subject_id','action_timestamp_utc'):
            response = json.loads(replay_bytes(e))
            response['record']['created'][field] = '2035-02-02T12:00:00Z' if field.endswith('_utc') else 'other'
            with self.subTest(field=field), self.assertRaisesRegex(PlanError, 'replay_rendering_record_mismatch'):
                handle.replay_evidence(json.dumps(response).encode(), e['post_observation'])

    def test_archetype_available_provenance_is_not_discarded(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); cp = prepared(f,0); view = companion(name)['observations'][1]
            for fault in ('missing','revision_actor','revision_command','revision_time','creation'):
                record = record_for(f,0)['archetype_record']
                if fault == 'missing': record = None
                elif fault == 'creation':
                    if name.endswith('update'): continue  # Earlier root creation is legitimate on revise.
                    record['created_by_command_id'] = 'other'
                else:
                    field = {'revision_actor':'created_by_subject_id', 'revision_command':'created_by_command_id',
                             'revision_time':'created_at_utc'}[fault]
                    record['revision'][field] = '2035-02-02T12:00:00Z' if field.endswith('_utc') else 'other'
                with self.subTest(flow=name,fault=fault), self.assertRaises(PlanError):
                    admit(f,cp,view,archetype_record=record)

    def test_replay_candidate_identity_cannot_be_replaced_by_equivalent_content(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); views = companion(name)['observations']
            for n,e in enumerate(f['accepted_responses']):
                if e['command'] == 'notification_profile.metadata.update': continue
                handle = admit(f,prepared(f,n),views[n+1],**record_for(f,n))
                response = json.loads(replay_bytes(e)); post = deepcopy(e['post_observation'])
                field = 'binding' if post['binding_id'] else 'revision'
                pointer = COMMANDS[e['command']]['outputs'][field].strip('/').split('/')
                target = response
                for token in pointer[:-1]: target = target[token]
                target[pointer[-1]] = 'equivalent_but_other_id'; post[field + '_id'] = 'equivalent_but_other_id'
                if e['command'].startswith('notification_rendering_definition.'):
                    response['record']['current_revision_id'] = post['revision_id']
                with self.subTest(command=e['command']), self.assertRaisesRegex(PlanError, 'replay_candidate_mismatch'):
                    handle.replay_evidence(json.dumps(response).encode(),post)

    def test_metadata_replay_must_preserve_both_preimage_and_response_revision(self):
        f = flow('flight-update'); n = next(i for i,e in enumerate(f['accepted_responses'])
            if e['command'] == 'notification_profile.metadata.update'); e = f['accepted_responses'][n]
        handle = admit(f, prepared(f,n), companion('flight-update')['observations'][n+1])
        response = json.loads(replay_bytes(e)); response['notification_profile_revision_id'] = 'other'
        with self.assertRaisesRegex(PlanError,'metadata_response_mismatch'):
            handle.replay_evidence(json.dumps(response).encode(),e['post_observation'])

    def test_both_binding_families_recheck_exact_candidate_without_changing_cas(self):
        f = flow('flight-create'); views = companion('flight-create')['observations']
        for n,e in enumerate(f['accepted_responses']):
            if e['command'] not in ('item_archetype.facet_binding.set','notification_profile.binding.set'): continue
            for lost in (False,True):
                handle = admit(f,prepared(f,n),views[n+int(lost)])
                expected = e['post_observation'] if lost else f['plan']['actions'][n]['expected']
                self.assertTrue(handle.check_binding(expected))
                changed = deepcopy(e['post_observation']); changed['binding_id'] = 'other'
                with self.assertRaises(PlanError): handle.check_binding(changed)
                self.assertEqual(handle.retry_request(),body(e['request']))
                if e['command'].startswith('item_'): self.assertIsNone(handle.retry_request()['expected_binding_id'])


class ContinuedCatalog(Catalog):
    def __init__(self, f, n, view, *, lost=False, **kwargs):
        super().__init__(f, **kwargs)
        self.f['accepted_responses'] = deepcopy(f['accepted_responses'][n:])
        self.rows = {r['object_key']:deepcopy(r) for r in view['entries']}
        self.lost = lost

    def write(self, command, request):
        raw = super().write(command,request)
        if self.lost and len(self.writes) == 1:
            response = json.loads(raw)
            if 'replayed' in response: response.update(replayed=True,changed=False)
            return json.dumps(response,separators=(',',':')).encode() + b'\n'
        return raw


class PublicCatalog(ContinuedCatalog):
    """Complete synthetic public catalog, including exact historical shows.

    Uses the independent saved prefix views; no installer observation is patched
    in the tests below. This is wire simulation, not an installed Spine claim.
    """
    def __init__(self,f,n,view,**kwargs):
        super().__init__(f,n,view,**kwargs)
        self.original=deepcopy(f); self.history=deepcopy(view['historical_revisions']); self.reads=[]

    def record(self,row):
        family=row['object_key'].split(':')[0]; prefix,_,id_field,_=FAMILIES[family]
        matching=next((i for i,e in enumerate(self.original['accepted_responses'])
                       if e['post_observation']['revision_id']==row['revision_id']
                       and e['post_observation']['object_key']==row['object_key']),None)
        if family=='rendering':
            record=(record_for(self.original,matching)['rendering_record'] if matching is not None else
                    self.template(prefix+'.show')['record'])
            record.update(notification_rendering_definition_id=row['root_id'],
                notification_rendering_definition_revision_id=row['revision_id'],current_revision_id=row['revision_id'],
                definition_key=row['object_key'].split(':')[1],revision=body(row['value']),owner=row['owner'],status=row['status'])
            record['definition_hash']=a.digest(dict(contract_version='spine.notification-rendering-definitions.v1',
                canonical_json_version='spine.canonical-json.v1',revision=record['revision']))
        elif family=='archetype' and matching is not None:
            record=record_for(self.original,matching)['archetype_record']
        else:
            generator=Catalog(self.original); generator.rows={row['object_key']:deepcopy(row)}
            generator.writes=[None]*((matching if matching is not None else len(self.original['accepted_responses'])-1)+1)
            generator.begin_observation(ObservationBudget())
            response=generator.read(prefix+'.show',{id_field:row['root_id']})
            record=response if family=='schema' else response[prefix]
        current=self.rows[row['object_key']]
        if current['revision_id']!=row['revision_id']:
            now=self.record(current)
            if family=='schema': record['root']=deepcopy(now['root'])
            elif family=='rendering':
                for k in ('current_revision_id','created','retired','status','owner','definition_key'):
                    record[k]=deepcopy(now[k])
            else: record=dict(deepcopy(now),revision=record['revision'])
        return record

    def read(self,command,request):
        self.reads.append((command,deepcopy(request)))
        if command in ('item_archetype.facet_binding.list','notification_profile.binding.list'):
            return super().read(command,request)
        self.budget.start_call()
        response=self.template(command)
        if command=='system.info':
            env=self.original['plan']['environment']
            response.update(ledger_instance_id=env['ledger_instance_id'],implemented_contract_versions=env['advertised_contracts'])
        elif command.endswith('.list'):
            family=next(k for k,v in FAMILIES.items() if command==v[0]+'.list')
            prefix,key_field,id_field,collection=FAMILIES[family]
            rows=[r for r in self.rows.values() if r['object_key'].startswith(family+':')
                  and ('status' not in request or r['status']==request['status'])]
            values=[self.record(r) for r in rows]
            if family=='schema': values=[r['root'] for r in values]
            values.sort(key=(lambda r:r[id_field]) if family in ('schema','rendering') else
                        (lambda r:(r[key_field],r[id_field])))
            response.update({collection:values,'has_more':False,'next_cursor':None})
            if 'limit' in response: response['limit']=request['limit']
            if 'count' in response: response['count']=str(len(values))
            if 'catalog_snapshot_hash' in response:
                catalog='archetypes' if family=='archetype' else 'profiles'
                response['catalog_snapshot_hash']=next(r['digest'] for r in snapshots(list(self.rows.values()))
                                                       if r['catalog']==catalog)
        else:
            family='schema' if command=='facet_schema.revision.show' else next(
                k for k,v in FAMILIES.items() if command==v[0]+'.show')
            prefix,_,id_field,_=FAMILIES[family]
            candidates=[*self.rows.values(),*self.history]
            revision=request.get(prefix+'_revision_id')
            row=next(r for r in candidates if r['object_key'].startswith(family+':')
                and (id_field not in request or r['root_id']==request[id_field])
                and (revision is None or r['revision_id']==revision))
            record=self.record(row)
            if family=='schema': response.update(root=record['root'],revision=record['revision'])
            else: response['record' if family=='rendering' else prefix]=record
        self.budget.received(json.dumps(response).encode())
        return response


class ContinuationTests(unittest.TestCase):
    def invoke(self, f, n, *, lost=False, source=None, transport=None, save=None, fresh=None):
        cp = prepared(f,n) if n < len(f['plan']['actions']) else f['final_checkpoint']
        source = cp if source is None else source
        name = 'flight-update' if f['plan']['decision_action_ids'] else 'flight-create'
        view = deepcopy(companion(name)['observations'][n + int(lost)])
        transport = transport or ContinuedCatalog(f,n,view,lost=lost)
        saved = []
        def writer(value):
            if save: save(value,len(saved),transport)
            saved.append(deepcopy(value)); transport.events.append(('checkpoint',len(value['accepted_responses']),bool(value['unresolved_submission'])))
        def observe_stub(t, owner, selection, **kwargs):
            transport.events.append('observation')
            self.assertEqual(owner,f['plan']['request']['owner']); self.assertEqual(selection,f['plan']['closure'])
            c = continuation_context(f['manifest'],f['plan'],f['approval'],source)
            self.assertEqual(kwargs['lineage'],c.lineage(include_pending=True))
            observed = deepcopy(view if fresh is None else fresh)
            if kwargs['record_key'] is not None:
                records = record_for(f,n) if lost else {}
                return deepcopy(f['plan']['environment']),observed,next(iter(records.values()),None)
            return deepcopy(f['plan']['environment']),observed
        with patch('spine_packs.facet_recovery.observe',side_effect=observe_stub), patch(
                'subprocess.Popen',side_effect=AssertionError('no processes')):
            r = apply_continuation(f['manifest'],f['plan'],f['approval'],source,transport,writer)
        if independent.Draft202012Validator is not None:
            with current_contracts(): independent.result_check(f['plan'],f['approval'],r)
        return r,transport,saved

    def test_every_checkpoint_prefix_and_lost_response_resumes_same_execution(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); original = deepcopy(f)
            for n in range(len(f['plan']['actions'])+1):
                for lost in ((False,True) if n < len(f['plan']['actions']) else (False,)):
                    with self.subTest(flow=name,n=n,lost=lost):
                        r,t,saved = self.invoke(f,n,lost=lost)
                        self.assertEqual(r['state'],'applied')
                        self.assertEqual(len(t.writes),len(f['plan']['actions'])-n)
                        self.assertEqual(saved[0],prepared(f,n) if n < len(f['plan']['actions']) else f['final_checkpoint'])
                        self.assertEqual(len(saved),1 + 2*len(t.writes))
                        for i,(command,request) in enumerate(t.writes):
                            self.assertEqual((command,request),(f['accepted_responses'][n+i]['command'],body(f['accepted_responses'][n+i]['request'])))
                            self.assertEqual(saved[1+2*i]['unresolved_submission']['request'],f['accepted_responses'][n+i]['request'])
                            self.assertEqual(len(saved[2+2*i]['accepted_responses']),n+i+1)
                        self.assertEqual(r['checkpoint']['execution'],f['approval']['execution'])
                        if n == len(f['plan']['actions']): self.assertFalse(t.writes)
            self.assertEqual(f,original)

    def test_partial_source_and_completed_checkpoint_but_not_other_terminal_results(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); source = f['partial_result']; original = deepcopy(source)
            n = len(source['checkpoint']['accepted_responses'])
            r,_,_ = self.invoke(f,n,source=source)
            self.assertEqual(r['state'],'applied'); self.assertEqual(source,original)
            bad = deepcopy(f['empty_prefix_partial']); bad['unattempted_action_ids'].reverse(); bad=seal(bad)
            for source in (bad,f['apply_result'],None,[],{'artifact_schema':'spine.pack-apply-checkpoint.v1'}):
                with self.assertRaises(PlanError): continuation_context(f['manifest'],f['plan'],f['approval'],source)
            bad=deepcopy(f['partial_result']); bad['failure']['action_id']='action-000005'; bad=seal(bad)
            with self.assertRaises(PlanError): continuation_context(f['manifest'],f['plan'],f['approval'],bad)

    def test_accepted_durable_prefix_without_pending_request_prepares_only_the_suffix(self):
        f=flow('flight-update')
        for n in range(len(f['plan']['actions'])):
            cp=checkpoint(f['plan'],f['approval'],f['accepted_responses'][:n])
            r,t,saved=self.invoke(f,n,source=cp)
            self.assertEqual(r['state'],'applied'); self.assertEqual(saved[0],cp)
            self.assertEqual(t.writes[0][1],body(f['accepted_responses'][n]['request']))

    def test_invalid_source_and_stale_observation_publish_nothing(self):
        f=flow(); cp=prepared(f,0); cp['content_identity']['digest']='0'*64
        transport=Mock(); writer=Mock()
        with patch('spine_packs.facet_recovery.observe') as read:
            with self.assertRaises(PlanError): apply_continuation(f['manifest'],f['plan'],f['approval'],cp,transport,writer)
            read.assert_not_called(); writer.assert_not_called(); transport.write.assert_not_called()
        fresh=companion('flight-create')['observations'][2]
        transport=ContinuedCatalog(f,0,fresh)
        with self.assertRaises(PlanError): self.invoke(f,0,transport=transport,fresh=fresh)
        self.assertFalse(transport.writes)
        self.assertFalse(any(isinstance(e,tuple) and e[0]=='checkpoint' for e in transport.events))

    def test_all_publication_boundaries_stop_before_any_consumer(self):
        f=flow('flight-update'); n=1
        for boundary in range(1 + 2*(len(f['plan']['actions'])-n)):
            seen=[]
            def save(cp,index,t):
                seen.append(t)
                if index==boundary: raise PlanError(ENVIRONMENT,'checkpoint_publication_failed')
            with self.subTest(boundary=boundary), self.assertRaisesRegex(PlanError,'checkpoint_publication_failed'):
                self.invoke(f,n,lost=True,save=save)
            self.assertEqual(len(seen[-1].writes),boundary//2)

    def test_each_rejection_malformed_response_or_failed_readback_stays_partial(self):
        for name in ('flight-create','flight-update'):
            f=flow(name); n=0; view=companion(name)['observations'][1]
            for failure in ('fail_at','malformed_at','read_fail_at'):
                for k in range(len(f['plan']['actions'])):
                    t=ContinuedCatalog(f,n,view,lost=True,**{failure:k})
                    with self.subTest(flow=name,failure=failure,k=k):
                        r,t,saved=self.invoke(f,n,lost=True,transport=t)
                        self.assertEqual(r['state'],'partial'); self.assertEqual(len(t.writes),k+1)
                        self.assertEqual(len(r['checkpoint']['accepted_responses']),k)
                        self.assertEqual(r['checkpoint'],saved[-1])
                        self.assertEqual(r['checkpoint']['unresolved_submission']['request'],f['accepted_responses'][k]['request'])

    def test_binding_drift_after_admission_never_submits_or_rewrites_request(self):
        f=flow(); views=companion('flight-create')['observations']
        for n,e in enumerate(f['accepted_responses']):
            if e['command'] not in ('item_archetype.facet_binding.set','notification_profile.binding.set'): continue
            t=ContinuedCatalog(f,n,views[n+1],lost=True)
            t.rows[e['post_observation']['object_key']]['binding_id']='other'
            r,t,saved=self.invoke(f,n,lost=True,transport=t)
            self.assertEqual(r['state'],'partial'); self.assertFalse(t.writes)
            self.assertEqual(len(saved),1); self.assertEqual(r['checkpoint'],prepared(f,n))

    def test_coherent_replay_other_identity_or_rendering_creation_cannot_advance(self):
        f=flow('flight-update'); views=companion('flight-update')['observations']
        for command in ('facet_schema.publish','notification_rendering_definition.publish'):
            n=next(i for i,e in enumerate(f['accepted_responses']) if e['command']==command)
            t=ContinuedCatalog(f,n,views[n+1],lost=True)
            evidence=t.f['accepted_responses'][0]; response=json.loads(evidence['response']['json_text'])
            if command.startswith('facet_schema'):
                response['facet_schema_revision_id']='other-equivalent-revision'
                evidence['post_observation']['revision_id']='other-equivalent-revision'
            else: response['record']['created']['command_id']='other-earlier-create'
            evidence['response']['json_text']=json.dumps(response)
            r,t,saved=self.invoke(f,n,lost=True,transport=t)
            self.assertEqual(r['state'],'partial'); self.assertEqual(len(t.writes),1)
            self.assertEqual(r['checkpoint'],prepared(f,n))
            self.assertEqual(len(saved),2)  # Admitted/prepared only, no accepted checkpoint.
            self.assertIn('replay_',r['failure']['error']['code'])

    def test_observation_failures_retain_category_without_publication_or_partial_result(self):
        f=flow(); cp=prepared(f,0)
        for category,code in ((ENVIRONMENT,'observation_capacity'),('spine_command_rejection','referenced_revision_missing')):
            t=Mock(target=deepcopy(f['plan']['request']['target'])); writer=Mock()
            with patch('spine_packs.facet_recovery.observe',side_effect=PlanError(category,code)):
                with self.assertRaises(PlanError) as caught:
                    apply_continuation(f['manifest'],f['plan'],f['approval'],cp,t,writer)
            self.assertEqual((caught.exception.category,caught.exception.code),(category,code))
            writer.assert_not_called(); t.write.assert_not_called()

    def test_checkpoint_files_are_new_private_and_source_bytes_unchanged(self):
        f=flow(); source=deepcopy(f['final_checkpoint'])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); src=root/'source.json'; dest=root/'continued.json'
            src.write_text(a.canonical_text(source)+'\n'); before=src.read_bytes()
            writer=checkpoint_writer(dest)
            r,_,_=self.invoke(f,6,source=source,save=lambda cp,i,t:writer(cp))
            self.assertEqual(r['state'],'applied'); self.assertEqual(src.read_bytes(),before)
            self.assertEqual(json.loads(dest.read_text()),source); self.assertEqual(dest.stat().st_mode & 0o777,0o600)
            with self.assertRaises(PlanError): checkpoint_writer(src)

    def test_admitted_directory_fsync_failure_stops_without_a_write_or_terminal_success(self):
        f=flow(); n=0; view=companion('flight-create')['observations'][0]
        t=ContinuedCatalog(f,n,view)
        with tempfile.TemporaryDirectory() as directory:
            writer=checkpoint_writer(Path(directory)/'continued.json'); calls=0
            def fsync(fd):
                nonlocal calls
                calls+=1
                if calls==2: raise OSError('private-sentinel')
            with patch('spine_packs.apply.os.fsync',side_effect=fsync):
                with self.assertRaisesRegex(PlanError,'checkpoint_publication_failed') as caught:
                    self.invoke(f,n,transport=t,save=lambda cp,i,t:writer(cp))
            self.assertFalse(t.writes); self.assertNotIn('private-sentinel',str(caught.exception))


class CaptureTests(unittest.TestCase):
    def test_profile_history_survives_metadata_admission_replay_and_continuation(self):
        for decoder in ('v1', 'v2'):
            f = profile_history_flow(decoder); before = deepcopy(f); n = 4
            view = deepcopy(companion('flight-update')['observations'][n+1])
            history = deepcopy(f['plan']['observation']['historical_revisions'][0])
            view['historical_revisions'].append(history)
            view['historical_revisions'].sort(key=lambda r:(r['object_key'], r['revision_id']))
            # Public historical show rebuilds the current root with the exact
            # old revision, so it exposes new mutable metadata on the old ID.
            for accepted in (False, True):
                cp = checkpoint(f['plan'], f['approval'], f['accepted_responses'][:n+1]) if accepted else prepared(f,n)
                start = n+int(accepted); t = PublicCatalog(f,start,reseal_view(deepcopy(view)),lost=not accepted)
                saved = []
                with self.subTest(decoder=decoder, accepted=accepted), patch.dict('os.environ', CURSORS):
                    value = apply_continuation(f['manifest'],f['plan'],f['approval'],cp,t,
                        lambda cp:saved.append(deepcopy(cp)),page_size=1)
                    self.assertEqual(value['state'],'applied')
                    self.assertEqual(len(t.writes),len(f['plan']['actions'])-start)
                    self.assertEqual(saved[0],cp)
                    self.assertEqual(t.writes[0][1],body(f['accepted_responses'][start]['request']))
                    history_reads=[r for cmd,r in t.reads if cmd=='notification_profile.show'
                                   and r.get('notification_profile_revision_id')==history['revision_id']]
                    self.assertEqual(len(history_reads),2)
                    if independent.Draft202012Validator is not None:
                        with current_contracts(): independent.result_check(f['plan'],f['approval'],value)
                    # A later restart must also retain the revision superseded
                    # by the suffix, with its new current-root metadata.
                    finished = deepcopy(companion('flight-update')['observations'][-1])
                    finished['historical_revisions'].append(deepcopy(history))
                    finished['historical_revisions'].sort(key=lambda r:(r['object_key'],r['revision_id']))
                    t2 = PublicCatalog(f,6,reseal_view(finished)); saved2 = []
                    again = apply_continuation(f['manifest'],f['plan'],f['approval'],value['checkpoint'],t2,
                        lambda cp:saved2.append(deepcopy(cp)),page_size=1)
                    self.assertEqual(again['state'],'applied'); self.assertFalse(t2.writes)
                    self.assertEqual(saved2,[value['checkpoint']])
            self.assertEqual(f,before)

    def test_profile_history_fix_keeps_unexplained_metadata_and_immutable_changes_closed(self):
        f = profile_history_flow(); n = 5
        cp = checkpoint(f['plan'],f['approval'],f['accepted_responses'][:n])
        view = deepcopy(companion('flight-update')['observations'][n])
        historical = deepcopy(f['plan']['observation']['historical_revisions'][0])
        view['historical_revisions'].append(historical)
        view['historical_revisions'].sort(key=lambda r:(r['object_key'],r['revision_id']))
        for fault in ('metadata', 'revision', 'decoder'):
            t = PublicCatalog(f,n,reseal_view(deepcopy(view))); writer = Mock()
            if fault == 'metadata':
                row = t.rows[historical['object_key']]; content = body(row['value'])
                content['metadata']['description'] = 'Unapproved root metadata'
            else:
                row = next(r for r in t.history if r['revision_id']==historical['revision_id'])
                content = body(row['value'])
                if fault == 'revision':
                    content['revision']['templates'][0]['late_handling']['grace_seconds'] = '1200'
                else:
                    row['revision_contract'] = 'spine.notification-profiles.v1'
                    for template in content['revision']['templates']: template.pop('rendering')
            row['value'] = blob(content)
            with self.subTest(fault=fault), patch.dict('os.environ',CURSORS), self.assertRaises(PlanError):
                apply_continuation(f['manifest'],f['plan'],f['approval'],cp,t,writer,page_size=1)
            self.assertFalse(t.writes); writer.assert_not_called()

    def test_real_observer_admits_every_saved_prefix_and_single_lost_action(self):
        for name in ('flight-create','flight-update'):
            f=flow(name); views=companion(name)['observations']
            for n in range(len(f['plan']['actions'])+1):
                for lost in ((False,True) if n<len(f['plan']['actions']) else (False,)):
                    cp=prepared(f,n) if n<len(f['plan']['actions']) else f['final_checkpoint']
                    t=PublicCatalog(f,n,views[n+int(lost)],lost=lost)
                    with self.subTest(flow=name,n=n,lost=lost), patch.dict('os.environ',CURSORS):
                        handle=preflight_continuation(f['manifest'],f['plan'],f['approval'],cp,t,page_size=1)
                        self.assertEqual(handle.kind,'prefix_plus_one' if lost else 'prefix')
                        self.assertEqual(handle.checkpoint(),cp); self.assertFalse(t.writes)
                        self.assertEqual(sum(cmd=='system.info' for cmd,_ in t.reads),2)

    def test_complete_public_observation_then_replay_and_suffix_without_stubs(self):
        for name in ('flight-create','flight-update'):
            f=flow(name); views=companion(name)['observations']
            for n in (1,3,5):
                t=PublicCatalog(f,n,views[n+1],lost=True); saved=[]
                with self.subTest(flow=name,n=n), patch.dict('os.environ',CURSORS):
                    r=apply_continuation(f['manifest'],f['plan'],f['approval'],prepared(f,n),t,
                                         lambda cp:saved.append(deepcopy(cp)),page_size=1)
                self.assertEqual(r['state'],'applied'); self.assertEqual(len(t.writes),6-n)
                self.assertEqual(len(saved),1+2*(6-n))

    def test_full_candidate_record_is_captured_in_existing_two_pass_budget(self):
        f=fixture(); adapter=Replay(f)
        key='archetype:flight'
        with patch.dict('os.environ',CURSORS):
            env,view,record=observe(adapter,f['plan']['request']['owner'],f['plan']['closure'],page_size=1,record_key=key)
        expected=next(r['response']['item_archetype'] for r in f['reads'] if r['command']=='item_archetype.show')
        self.assertEqual(record,expected); self.assertEqual(view,f['plan']['observation'])
        self.assertFalse(adapter.rows); self.assertEqual(len(adapter.calls),len(f['reads']))

    def test_record_provenance_drift_between_passes_aborts_even_with_equal_projection(self):
        f=fixture(); count=0
        def mutate(command,request,response,n):
            nonlocal count
            if command=='item_archetype.list': count+=1
            if count==2 and command in ('item_archetype.list','item_archetype.show'):
                rows=response['entries'] if command.endswith('.list') else [response['item_archetype']]
                for row in rows: row['revision']['created_by_command_id']='other'
            return response,0
        adapter=Replay(f,mutate)
        with patch.dict('os.environ',CURSORS), self.assertRaisesRegex(PlanError,'catalog_changed_between_passes'):
            observe(adapter,f['plan']['request']['owner'],f['plan']['closure'],page_size=1,record_key='archetype:flight')

    def test_pending_head_preimages_are_included_without_accepting_outputs(self):
        f=flow('flight-update')
        for n,e in enumerate(f['accepted_responses']):
            if 'revision' not in COMMANDS[e['command']]['outputs']: continue
            c=context(f,prepared(f,n)); rows=c.lineage(include_pending=True)
            old=next(r for r in c.expected_view()['entries'] if r['object_key']==e['post_observation']['object_key'])
            self.assertIn(old,rows)
            self.assertEqual(c.materialize(f['accepted_responses'][:n]),body(e['request']))


if __name__=='__main__': unittest.main()
