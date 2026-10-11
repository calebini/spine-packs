"""FR-1 saved artifact and execution/recovery vectors; no runtime/CLI calls."""
from copy import deepcopy
import hashlib
import json
import unittest

from facet_artifact_oracle import *

FIXTURES = ROOT / 'tests/fixtures/installer-v2'
INDEX = ROOT / 'contracts/installer-fixture-manifest.v2.json'


def checkpoint_at(flow, length, prepared=False):
    cp = deepcopy(flow['initial_checkpoint'])
    cp['accepted_responses'] = deepcopy(flow['accepted_responses'][:length])
    actions = flow['plan']['actions']
    cp['next_action_id'] = actions[length]['action_id'] if length < len(actions) else None
    cp['unresolved_submission'] = None
    if prepared:
        action = actions[length]
        req = materialize(flow['plan'], flow['approval'], action, cp['accepted_responses'])
        cp['unresolved_submission'] = {'action_id': action['action_id'], 'command_id': req['command_id'],
            'submission_state': 'prepared_or_submitted', 'request': blob(req)}
    return seal(cp)


def reseal_response(evidence, value):
    text = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    evidence['response'] = {'json_text': text, 'digest': sha(text.encode())}
    evidence['receipt'] = receipt_projection(evidence['command'], value)


@unittest.skipIf(Draft202012Validator is None, 'FR-1 requires development jsonschema; run isolated gate')
class FacetArtifactTests(unittest.TestCase):
    def flow(self, name='flight-create'):
        return load(FIXTURES / (name + '.json'))

    def test_official_schema_meta_and_offline_reference_closure(self):
        for path in SCHEMAS.glob('*.json'):
            Draft202012Validator.check_schema(load(path))
        readback = load(SCHEMAS / 'spine-readback-0.9.1.schema.json')
        def walk(value):
            if isinstance(value, dict):
                if '$ref' in value:
                    self.assertTrue(value['$ref'].startswith('#/$defs/'))
                    self.assertIn(value['$ref'].split('/')[-1], readback['$defs'])
                for v in value.values():
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
        walk(readback)
        self.assertEqual(len(COMMANDS), 22)
        self.assertEqual(sum(c['phase'] is not None for c in COMMANDS.values()), 11)
        self.assertEqual(len(INVENTORY['required_execution_contracts']), 17)
        self.assertFalse(any('disclosure' in c or c.startswith('item.') for c in COMMANDS))

    def test_typed_object_key_grammar_at_every_schema_location(self):
        schema = load(SCHEMAS / 'spine-pack-installer-types.v2.schema.json')
        locations = (
            '$defs/state/properties/object_key',
            '$defs/source/oneOf/0/properties/object_key',
            '$defs/resolution/properties/object_key',
            '$defs/classification/properties/object_key',
            '$defs/slot/properties/object_key',
            '$defs/action/properties/object_key',
            '$defs/install-plan/properties/closure/items',
            '$defs/install-plan/properties/blocked_object_keys/items',
            '$defs/verification-result/properties/closure/items',
            '$defs/verification-result/properties/object_results/items/properties/object_key',
        )
        for path in locations:
            fragment = schema
            for part in path.split('/'):
                fragment = fragment[int(part)] if isinstance(fragment, list) else fragment[part]
            check = Draft202012Validator(fragment)
            for vector in load(INDEX)['object_key_vectors']:
                with self.subTest(path=path, value=vector['value']):
                    self.assertEqual(check.is_valid(vector['value']), vector['valid'])

    def test_saved_complete_create_and_update_flows(self):
        commands = set()
        for name in ('flight-create','flight-update'):
            with self.subTest(flow=name):
                f = self.flow(name); p = f['plan']; a = f['approval']
                plan_check(f['manifest'], f['request'], p)
                approval_check(p, a)
                for key in ('initial_checkpoint','final_checkpoint','prepared_checkpoint'):
                    checkpoint_check(p, a, f[key])
                for key in ('apply_result','partial_result','empty_prefix_partial'):
                    result_check(p, a, f[key])
                verification_check(p, a, f['apply_result'], f['verification'])
                artifact(f['envelope'])
                commands.update(x['command'] for x in p['actions'])
        self.assertEqual(commands, {c for c,v in COMMANDS.items() if v['phase'] is not None})

    def test_indexed_execution_recovery_boundaries(self):
        vectors = load(INDEX)['vectors']
        for vector in vectors:
            with self.subTest(vector=vector['id']):
                f = load(FIXTURES / vector['fixture']); p=f['plan']; a=f['approval']; n=int(vector['prefix_length'])
                if vector['boundary'] == 'accepted_durable':
                    cp = checkpoint_at(f,n+1)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n+1]),'prefix')
                elif vector['boundary'] == 'prepared_before_submit':
                    cp = checkpoint_at(f,n,True)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n]),'prefix')
                else:
                    cp = checkpoint_at(f,n,True); replay=deepcopy(f['accepted_responses'][n])
                    r=unblob(replay['response'],True)
                    if 'replayed' in r:
                        r.update(replayed=True,changed=False);reseal_response(replay,r)
                    self.assertEqual(recovery_check(p,a,cp,f['observations'][n+1],f['accepted_responses'][n]['post_observation'],replay),'prefix_plus_one')

    def test_negative_typed_references_and_complete_authorization(self):
        for failure in ('forward','wrong_output','wrong_object','missing_slot','non_null_slot','missing_resolution','stale_approval','unauthorized_update','wrong_union','wrong_environment','wrong_owner','closure_gap','wrong_digest'):
            with self.subTest(failure=failure):
                f=self.flow('flight-update' if failure=='unauthorized_update' else 'flight-create');p=f['plan'];a=f['approval']
                if failure=='forward':p['resolutions'][p['closure'].index('schema:flight_details')]['revision']['action_id']='action-000004'
                elif failure=='wrong_output':p['resolutions'][-1]['revision']['output_pointer']='/facet_schema_id'
                elif failure=='wrong_object':p['actions'][2]['slots'][0]['object_key']='rendering:flight_details'
                elif failure=='missing_slot':p['actions'][3]['slots'].pop()
                elif failure=='non_null_slot':
                    body=unblob(p['actions'][2]['request_template']);body['facet_schema_revision_id']='guessed';p['actions'][2]['request_template']=blob(body)
                elif failure=='missing_resolution':p['resolutions'].pop()
                elif failure=='stale_approval':a['plan_digest']='0'*64
                elif failure=='unauthorized_update':a['authorized_update_action_ids'].pop()
                elif failure=='wrong_union':p['required_execution_contracts'].pop()
                elif failure=='wrong_environment':p['environment']['runtime_version']='0.9.2'
                elif failure=='wrong_owner':p['request']['owner']['owner_subject_id']='other'
                elif failure=='closure_gap':p['closure'].pop()
                p=seal(p);a=seal(a)
                if failure=='wrong_digest':p['content_identity']['digest']='0'*64
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    plan_check(f['manifest'],f['request'],p);approval_check(p,a)

    def test_negative_evidence_and_replay(self):
        for failure in ('gap','changed_request','wrong_command_id','wrong_receipt_hash','wrong_output','dry_run','wrong_selector','wrong_projection','wrong_provenance','noop_change','guessed_suffix','unrelated_change','candidate_without_replay','candidate_id_mismatch'):
            with self.subTest(failure=failure):
                f=self.flow();p=f['plan'];a=f['approval'];n=3;cp=checkpoint_at(f,n,True)
                fresh=deepcopy(f['observations'][n+1]);replay=deepcopy(f['accepted_responses'][n]);candidate=deepcopy(replay['post_observation'])
                if failure=='gap':cp['accepted_responses'].pop(0)
                elif failure=='changed_request':
                    r=unblob(cp['unresolved_submission']['request']);r['actor_subject_id']='other';cp['unresolved_submission']['request']=blob(r)
                elif failure=='wrong_command_id':cp['unresolved_submission']['command_id']='other'
                elif failure in ('wrong_receipt_hash','wrong_output'):
                    r=unblob(cp['accepted_responses'][0]['response'],True)
                    if failure=='wrong_receipt_hash':r['receipt']['semantic_facts_hash']='0'*64
                    else:r['item_archetype_id']='other'
                    reseal_response(cp['accepted_responses'][0],r)
                elif failure in ('dry_run','wrong_selector','wrong_provenance','noop_change'):
                    r=unblob(replay['response'],True)
                    if failure=='dry_run':r['dry_run']=True
                    elif failure=='wrong_selector':r['contract_version']='spine.notification-profiles.v2'
                    elif failure=='wrong_provenance':r['record']['published']['actor_subject_id']='other'
                    else:r['effect']='rendering_definition_publish_noop';r['changed']=False
                    reseal_response(replay,r)
                elif failure=='wrong_projection':replay['receipt']['audit_id']='invented'
                elif failure=='guessed_suffix':cp['accepted_responses'].append(f['accepted_responses'][4])
                elif failure=='unrelated_change':fresh['entries'][0]['root_id']='other'
                elif failure=='candidate_without_replay':replay=None
                elif failure=='candidate_id_mismatch':candidate['revision_id']='other'
                cp=seal(cp);fresh['digest']=observation_digest(fresh)
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    recovery_check(p,a,cp,fresh,candidate,replay)

    def test_verification_exact_pins_and_read_only_evidence(self):
        for failure in ('current_head','binding_pin','missing_result','wrong_target','missing_object','false_disclosure'):
            with self.subTest(failure=failure):
                f=self.flow();v=f['verification'];result=f['apply_result']
                if failure=='current_head':
                    row=next(r for r in v['observation']['entries'] if r['object_key'].startswith('schema:'));row['revision_id']='later-equivalent-revision'
                elif failure=='binding_pin':
                    row=next(r for r in v['observation']['entries'] if r['object_key'].startswith('facet_binding:'));body=unblob(row['value']);body['facet_schema_revision_id']='later';row['value']=blob(body)
                elif failure=='missing_result':result=None
                elif failure=='wrong_target':v['target']['host_name']='elsewhere.invalid'
                elif failure=='missing_object':v['object_results'].pop()
                else:v['disclosure']='approved'
                v['observation']['digest']=observation_digest(v['observation']);v=seal(v)
                with self.assertRaises((ValueError, KeyError, __import__('jsonschema').ValidationError)):
                    verification_check(f['plan'],f['approval'],result,v)

    def test_response_text_numbers_and_duplicate_rejection(self):
        text='{"revision_number":1}'
        value={'json_text':text,'digest':sha(text.encode())}
        self.assertEqual(unblob(value,True),{'revision_number':1})
        with self.assertRaises(ValueError):canonical({'revision_number':1})
        for text in ('{"ok":true,"ok":true}','{"n":NaN}','"\\ud800"','\ufeff{}'):
            with self.assertRaises((ValueError,UnicodeError)):
                unblob({'json_text':text,'digest':sha(text.encode())},True)

    def test_retain_no_write_plan_and_draft_refusal(self):
        f=self.flow();p=deepcopy(f['plan']);p['observation']=deepcopy(f['observations'][-1])
        rows={r['object_key']:r for r in p['observation']['entries']}
        p.update(actions=[],decision_action_ids=[])
        for c in p['classifications']:
            c.update(classification='equivalent',observed=rows[c['object_key']])
        for r in p['resolutions']:
            for field in ('root','revision','binding'):
                value=rows[r['object_key']][field+'_id']
                key=('archetype:flight' if field=='root' and r['object_key'].split(':')[0] in ('binding','facet_binding') else r['object_key'])
                r[field]={'kind':'observed','object_key':key,'field':field,'value':value} if value else None
        p=seal(p);plan_check(f['manifest'],f['request'],p)
        a=deepcopy(f['approval']);a['plan_digest']=p['content_identity']['digest'];a=seal(a)
        v=deepcopy(f['verification']);v.update(plan_digest=p['content_identity']['digest'],apply_result_digest=None,response_evidence='not_required');v=seal(v)
        verification_check(p,a,None,v)
        from test_facet_manifest_contract import digest
        m=deepcopy(f['manifest']);m['pack'].update(version='1.0.0-draft.1',status='draft');m['content_identity']['digest']=digest(m)
        req=deepcopy(f['request']);req['request']['draft_posture']='inspect_only';req=seal(req)
        p.update(pack=dict(manifest_schema=m['manifest_schema'],**m['pack'],manifest_digest=m['content_identity']['digest']),request=req['request'],request_digest=req['content_identity']['digest'],apply_eligible=False);p=seal(p)
        plan_check(m,req,p)
        a['plan_digest']=p['content_identity']['digest'];a=seal(a)
        with self.assertRaisesRegex(ValueError,'ineligible apply'):approval_check(p,a)

    def test_all_artifact_digests_and_v1_rejection(self):
        f=self.flow()
        for value in f.values():
            if isinstance(value,dict) and 'artifact_schema' in value:
                artifact(value)
                kind=value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
                self.assertFalse(validator('spine-pack-'+kind+'.v1.schema.json').is_valid(value))
                if 'content_identity' in value:
                    value['content_identity']['digest']='0'*64
                    with self.assertRaises(ValueError):artifact(value)

    def test_command_and_artifact_hash_preimages_independent(self):
        f=self.flow();p=f['plan'];a=f['approval']
        # Fixture text has no control escapes; direct stdlib serialization is an
        # independent encoder for this fixed vector, not a second call to seal.
        value=deepcopy(p);expected=value['content_identity'].pop('digest')
        raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),expected)
        for action,e in zip(p['actions'],f['accepted_responses']):
            value={'action_id':action['action_id'],'derivation_version':'spine.pack-command-id.v2','execution_id':a['execution']['execution_id'],'plan_digest':expected}
            raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
            self.assertEqual('spack_'+hashlib.sha256(raw).hexdigest(),e['command_id'])

    def test_resolved_rendering_byte_limit_inclusive(self):
        f=self.flow();action=deepcopy(f['plan']['actions'][3]);req=unblob(action['request_template'])
        # Resolve first, then fill bounded Unicode description to the exact byte
        # ceiling. Public maxLength counts codepoints, not UTF-8 bytes.
        resolved=materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])
        resolved['revision']['description']=''
        remaining=8192-len(canonical(resolved['revision']))
        req['revision']['description']='🛫'*(remaining//4)+'x'*(remaining%4)
        action['request_template']=blob(req)
        accepted=materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])
        self.assertEqual(len(canonical(accepted['revision'])),8192)
        req['revision']['description']+='x';action['request_template']=blob(req)
        with self.assertRaisesRegex(ValueError,'resolved rendering byte limit'):
            materialize(f['plan'],f['approval'],action,f['accepted_responses'][:3])

    def test_upstream_public_wire_vectors(self):
        vectors=load(FIXTURES/'public-wire-vectors.json')['vectors']
        for vector in vectors:
            with self.subTest(vector=vector['source']):
                public_schema(vector['command'],vector['direction'],vector['value'])


if __name__ == '__main__':
    unittest.main()
