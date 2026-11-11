"""FR-4 CLI wiring with synthetic public commands and private local artifacts."""
from copy import deepcopy
import contextlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests/contract')]
from spine_packs import artifacts as a
from spine_packs.__main__ import load_input, main, publish
from spine_packs.facet_contracts import artifact, body, seal, validate
from spine_packs.facet_inventory import READ_COMMANDS
from spine_packs.facet_planning import build_plan
from spine_packs.planning import ENVIRONMENT, PlanError
from test_facet_apply import independent, current_contracts
from test_facet_continuation import PublicCatalog, prepared
from test_facet_execution import flow, reseal_plan
from test_facet_planning import CURSORS
from test_facet_recovery import companion
from test_facet_verification import final_view, no_write_flow
import fr4_contract_oracle as oracle


class FacetCLITests(unittest.TestCase):
    def setUp(self):
        self.directory = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(self.directory); self.serial = 0

    def inputs(self, f, operation, *, source=None, applied=None):
        self.serial += 1
        folder = self.root/str(self.serial); folder.mkdir()
        paths = {key:folder/(key+'.json') for key in (
            'manifest','plan','approval','source','applied','checkpoint','output')}
        args = [operation]
        for key in ('manifest','plan',*(['approval'] if operation=='apply' else [])):
            paths[key].write_text(a.canonical_text(f[key])+'\n')
            args += ['--'+key,str(paths[key])]
        if source is not None:
            paths['source'].write_text(a.canonical_text(source)+'\n')
            args += ['--continue-from',str(paths['source'])]
        if applied is not None:
            paths['applied'].write_text(a.canonical_text(applied)+'\n')
            args += ['--result',str(paths['applied'])]
        if operation=='apply': args += ['--checkpoint',str(paths['checkpoint'])]
        return [*args,'--output',str(paths['output'])], paths

    def invoke(self, args, transport=None, *, default=False, factory=None):
        with contextlib.redirect_stdout(io.StringIO()) as out, patch.dict('os.environ',CURSORS), patch(
                'subprocess.Popen',side_effect=AssertionError('no real CLI subprocess')):
            code = main(args) if default else main(args,transport_factory=factory or (lambda target:transport))
        text = out.getvalue()
        self.assertEqual(len(text.splitlines()),1)
        self.assertTrue(text.endswith('\n'))
        envelope = json.loads(text)
        self.assertEqual(text,a.canonical_text(envelope)+'\n')
        self.assertEqual(envelope['artifact_schema'],'spine.pack-installer-result.v2')
        self.assertEqual(envelope['exit_code'],str(code))
        self.assertEqual(envelope['operation'],args[0])
        validate(envelope,'spine-pack-installer-result.v2.schema.json')
        if independent.Draft202012Validator is not None: independent.artifact(envelope)
        return code,envelope

    def test_checkpoint_partial_and_complete_sources_publish_private_results(self):
        for name in ('flight-create','flight-update'):
            f = flow(name); views = companion(name)['observations']
            partial_n = len(f['partial_result']['checkpoint']['accepted_responses'])
            cases = [(prepared(f,1),1,False),(prepared(f,3),3,True),
                     (f['partial_result'],partial_n,False),(f['final_checkpoint'],6,False)]
            for source,n,lost in cases:
                args,p = self.inputs(f,'apply',source=source)
                original = p['source'].read_bytes()
                t = PublicCatalog(f,n,views[n+int(lost)],lost=lost)
                with self.subTest(flow=name,n=n,lost=lost):
                    code,envelope = self.invoke(args,t)
                    self.assertEqual(code,0)
                    value = a.load_json(p['output']); artifact(value,'apply-result')
                    self.assertEqual(value['state'],'applied')
                    self.assertEqual(a.load_json(p['checkpoint']),value['checkpoint'])
                    self.assertEqual(p['source'].read_bytes(),original)
                    self.assertEqual(envelope['artifact'],dict(path=str(p['output']),digest=value['content_identity']['digest']))
                    self.assertEqual(len(t.writes),6-n)
                    if t.writes: self.assertEqual(t.writes[0][1],body(f['accepted_responses'][n]['request']))
                    for path in (p['output'],p['checkpoint']):
                        self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
                    if independent.Draft202012Validator is not None:
                        with current_contracts(): independent.result_check(f['plan'],f['approval'],value)

    def test_default_continuation_and_verify_factories_use_distinct_adapters(self):
        f = flow(); views = companion('flight-create')['observations']
        args,_ = self.inputs(f,'apply',source=prepared(f,3))
        t = PublicCatalog(f,3,views[4],lost=True)
        with patch('spine_packs.facet_apply_transport.FacetApplyCommand',return_value=t) as writer_factory, patch(
                'spine_packs.facet_transport.FacetSpineCommand',side_effect=AssertionError('wrong apply adapter')):
            self.assertEqual(self.invoke(args,default=True)[0],0)
            writer_factory.assert_called_once_with(f['plan']['request']['target'])
        args,_ = self.inputs(f,'verify',applied=f['apply_result'])
        t = PublicCatalog(f,6,final_view()); t.write = Mock(side_effect=AssertionError('verify cannot write'))
        with patch('spine_packs.facet_transport.FacetSpineCommand',return_value=t) as read_factory, patch(
                'spine_packs.facet_apply_transport.FacetApplyCommand',side_effect=AssertionError('wrong verify adapter')):
            self.assertEqual(self.invoke(args,default=True)[0],0)
            read_factory.assert_called_once_with(f['plan']['request']['target'])
        t.write.assert_not_called()

    def test_verify_status_coverage_and_no_write_draft_without_approval(self):
        for case in ('complete','missing','partial','invalid','drift','no_write','draft','ordinary_v1'):
            f = flow(); view = final_view(); applied = f['apply_result']; expected = 0
            if case=='missing': applied = None; expected = 10
            elif case=='partial': applied = f['partial_result']; expected = 10
            elif case=='invalid':
                applied = deepcopy(applied); applied['checkpoint']['approval_digest'] = '0'*64
                applied['checkpoint'] = seal(applied['checkpoint']); applied = seal(applied); expected = 10
            elif case=='drift':
                row = next(r for r in view['entries'] if r['object_key'].startswith('profile:'))
                from spine_packs.facet_contracts import blob
                content = body(row['value']); content['metadata']['description'] = 'Drift'
                row['value'] = blob(content); expected = 10
            elif case in ('no_write','draft','ordinary_v1'):
                f,view = no_write_flow(draft=case=='draft',ordinary_v1=case=='ordinary_v1'); applied = None
            args,p = self.inputs(f,'verify',applied=applied)
            before = p['applied'].read_bytes() if applied is not None else None
            t = PublicCatalog(f,6,view); t.write = Mock(side_effect=AssertionError('verify cannot write'))
            with self.subTest(case=case), patch('spine_packs.facet_apply.apply_initial',side_effect=AssertionError('no apply')), patch(
                    'spine_packs.facet_apply.apply_continuation',side_effect=AssertionError('no continuation')), patch(
                    'spine_packs.facet_recovery.preflight_continuation',side_effect=AssertionError('no recovery')):
                code,envelope = self.invoke(args,t)
                self.assertEqual(code,expected)
                value = a.load_json(p['output']); artifact(value,'verification-result')
                self.assertEqual(value['state'],'verified' if expected==0 else 'mismatch')
                if case in ('complete','missing','partial','invalid'):
                    self.assertEqual(value['response_evidence'],{'complete':'complete','missing':'missing',
                        'partial':'missing','invalid':'invalid'}[case])
                self.assertEqual(value['disclosure'],'separate_operator_configuration_required')
                self.assertEqual(value['receipt_readback'],'captured_responses_only_spine_0.10.0')
                self.assertEqual(envelope['artifact']['digest'],value['content_identity']['digest'])
                self.assertEqual(stat.S_IMODE(p['output'].stat().st_mode),0o600)
                self.assertFalse(p['checkpoint'].exists()); t.write.assert_not_called()
                self.assertTrue(all(command in READ_COMMANDS for command,_ in t.reads))
                if before is not None: self.assertEqual(p['applied'].read_bytes(),before)
                if independent.Draft202012Validator is not None:
                    with current_contracts(): oracle.verification_check(f,applied,value)

    def test_mixed_plan_and_approval_versions_fail_before_transport(self):
        for operation in ('apply','verify'):
            for kind in (('plan','approval') if operation=='apply' else ('plan',)):
                f = flow(); args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None)
                changed = deepcopy(f[kind]); changed['artifact_schema'] = changed['artifact_schema'].replace('.v2','.v1')
                p[kind].write_text(a.canonical_text(changed)+'\n')
                factory = Mock(side_effect=AssertionError('mixed versions reached target'))
                with self.subTest(operation=operation,kind=kind):
                    code,envelope = self.invoke(args,factory=factory)
                    self.assertEqual(code,2); self.assertIsNone(envelope['artifact'])
                    self.assertFalse(p['checkpoint'].exists() or p['output'].exists()); factory.assert_not_called()

    def test_invalid_source_and_outer_result_fail_before_transport_construction(self):
        f = flow()
        for operation in ('apply','verify'):
            values = [None,[],{'artifact_schema':'spine.pack-apply-checkpoint.v1'}]
            if operation=='apply': values += [f['apply_result']]
            bad = deepcopy(f['prepared_checkpoint'] if operation=='apply' else f['apply_result'])
            bad['content_identity']['digest'] = '0'*64; values.append(bad)
            for value in values:
                args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None,
                                     applied=f['apply_result'] if operation=='verify' else None)
                path = p['source' if operation=='apply' else 'applied']
                path.write_text(json.dumps(value))
                factory = Mock(side_effect=AssertionError('invalid input reached target'))
                with self.subTest(operation=operation,value=type(value).__name__):
                    code,envelope = self.invoke(args,factory=factory)
                    self.assertEqual(code,2); self.assertIsNone(envelope['artifact'])
                    factory.assert_not_called(); self.assertFalse(p['checkpoint'].exists() or p['output'].exists())

    def test_oversized_source_and_result_fail_before_transport_construction(self):
        f = flow()
        for operation in ('apply','verify'):
            args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None,
                                 applied=f['apply_result'] if operation=='verify' else None)
            p['source' if operation=='apply' else 'applied'].write_bytes(b' '*(16*1024*1024+1))
            factory = Mock(side_effect=AssertionError('oversized input reached target'))
            code,envelope = self.invoke(args,factory=factory)
            self.assertEqual((code,envelope['error']['code']),(2,'input_too_large'))
            factory.assert_not_called()

    def test_source_and_result_protected_paths_are_rejected_before_open(self):
        f = flow(); target = f['plan']['request']['target']
        for operation in ('apply','verify'):
            args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None,
                                 applied=f['apply_result'] if operation=='verify' else None)
            flag = '--continue-from' if operation=='apply' else '--result'
            protected = [str(p['manifest']),str(p['plan']),target['ledger']['path'],target['spine_command']['path']]
            if operation=='apply': protected.append(str(p['approval']))
            for path in protected:
                collided = args[:]; collided[collided.index(flag)+1] = path
                factory = Mock(side_effect=AssertionError('collision reached target'))
                with self.subTest(operation=operation,path=path), patch('spine_packs.__main__.load_input',wraps=load_input) as loader:
                    code,envelope = self.invoke(collided,factory=factory)
                    self.assertEqual(code,2); self.assertIn('input_collision',envelope['error']['code'])
                    # Manifest/plan/approval must be loaded normally, never a
                    # second time as the colliding source/result.
                    expected = int(path in [str(p[k]) for k in ('manifest','plan',*(['approval'] if operation=='apply' else []))])
                    self.assertEqual(sum(c.args[0]==path for c in loader.call_args_list),expected)
                    factory.assert_not_called()

    def test_symlink_and_hardlink_source_aliases_to_targets_or_inputs_are_rejected(self):
        for operation in ('apply','verify'):
            f = flow('flight-update')
            command = self.root/(operation+'-command'); command.write_text('PRIVATE_EXECUTABLE')
            ledger = self.root/(operation+'-ledger'); ledger.write_text('PRIVATE_LEDGER')
            target = f['request']['request']['target']
            target['spine_command']['path'] = str(command); target['ledger']['path'] = str(ledger)
            f['request'] = seal(f['request'])
            f['plan'] = build_plan(f['manifest'],f['request'],f['plan']['environment'],f['plan']['observation']); reseal_plan(f)
            args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None,
                                 applied=f['apply_result'] if operation=='verify' else None)
            flag = '--continue-from' if operation=='apply' else '--result'
            for destination in (command,ledger,p['manifest'],p['plan']):
                for mode in ('symlink','hardlink'):
                    alias = p['output'].parent/(destination.name+'-'+mode)
                    if mode=='symlink': alias.symlink_to(destination)
                    else: os.link(destination,alias)
                    collided = args[:]; collided[collided.index(flag)+1] = str(alias)
                    factory = Mock(side_effect=AssertionError('alias reached target'))
                    with self.subTest(operation=operation,mode=mode), patch('spine_packs.__main__.load_input',wraps=load_input) as loader:
                        code,envelope = self.invoke(collided,factory=factory)
                        self.assertEqual(code,2); self.assertIn('input_collision',envelope['error']['code'])
                        self.assertNotIn(str(alias),[c.args[0] for c in loader.call_args_list]); factory.assert_not_called()
            self.assertEqual(ledger.read_text(),'PRIVATE_LEDGER'); self.assertEqual(command.read_text(),'PRIVATE_EXECUTABLE')

    def test_new_destinations_cannot_collide_with_each_other_inputs_sources_or_targets(self):
        f = flow(); target = f['plan']['request']['target']
        for operation in ('apply','verify'):
            args,p = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None,
                                 applied=f['apply_result'] if operation=='verify' else None)
            protected = [str(p['manifest']),str(p['plan']),str(p['source' if operation=='apply' else 'applied']),
                         target['ledger']['path'],target['spine_command']['path']]
            if operation=='apply': protected.append(str(p['approval']))
            for flag in (('--output','--checkpoint') if operation=='apply' else ('--output',)):
                for path in [*protected,*([str(p['checkpoint' if flag=='--output' else 'output'])] if operation=='apply' else [])]:
                    collided = args[:]; collided[collided.index(flag)+1] = path
                    factory = Mock(side_effect=AssertionError('destination collision reached target'))
                    with self.subTest(operation=operation,flag=flag,path=path):
                        self.assertEqual(self.invoke(collided,factory=factory)[0],2)
                        factory.assert_not_called()

    def test_forbidden_flags_fail_before_target(self):
        f = flow()
        for operation in ('apply','verify'):
            args,_ = self.inputs(f,operation,source=prepared(f,1) if operation=='apply' else None)
            extras = [['--all'],['--archetype','flight'],['--request','unread.json']]
            extras += [['--result','unread.json']] if operation=='apply' else [
                ['--approval','unread.json'],['--checkpoint','unread.json'],['--continue-from','unread.json']]
            for extra in extras:
                factory = Mock(side_effect=AssertionError('forbidden flags reached target'))
                self.assertEqual(self.invoke(args+extra,factory=factory)[0],2); factory.assert_not_called()

    def test_stale_admission_and_observation_failure_publish_only_error_envelopes(self):
        f = flow(); args,p = self.inputs(f,'apply',source=prepared(f,3))
        view = deepcopy(companion('flight-create')['observations'][5])
        t = PublicCatalog(f,3,view)
        code,envelope = self.invoke(args,t)
        self.assertEqual(code,7); self.assertIsNone(envelope['artifact'])
        self.assertFalse(p['checkpoint'].exists() or p['output'].exists() or t.writes)
        args,p = self.inputs(f,'verify',applied=f['apply_result']); t = PublicCatalog(f,6,final_view())
        with patch('spine_packs.facet_verification.observe',side_effect=PlanError(ENVIRONMENT,'observation_capacity')):
            code,envelope = self.invoke(args,t)
        self.assertEqual((code,envelope['error']['code']),(11,'observation_capacity'))
        self.assertIsNone(envelope['artifact']); self.assertFalse(p['output'].exists() or t.writes)

    def test_continuation_rejection_returns_partial_with_durable_prepared_checkpoint(self):
        f = flow(); args,p = self.inputs(f,'apply',source=prepared(f,3))
        t = PublicCatalog(f,3,companion('flight-create')['observations'][3],fail_at=0)
        code,envelope = self.invoke(args,t)
        self.assertEqual(code,9); self.assertEqual(envelope['status'],'partial')
        value = a.load_json(p['output']); self.assertEqual(value['state'],'partial')
        self.assertEqual(a.load_json(p['checkpoint']),value['checkpoint'])
        self.assertEqual(value['checkpoint']['unresolved_submission']['request'],f['accepted_responses'][3]['request'])
        self.assertEqual(len(t.writes),1)

    def test_publication_failures_preserve_checkpoint_and_never_claim_success(self):
        f = flow()
        for operation in ('apply','verify'):
            args,p = self.inputs(f,operation,source=prepared(f,3) if operation=='apply' else None,
                                 applied=f['apply_result'] if operation=='verify' else None)
            t = PublicCatalog(f,3,companion('flight-create')['observations'][3]) if operation=='apply' else PublicCatalog(f,6,final_view())
            with patch('spine_packs.__main__.publish',side_effect=PlanError(ENVIRONMENT,'output_publication_failed')):
                code,envelope = self.invoke(args,t)
            self.assertEqual(code,11); self.assertIsNone(envelope['artifact']); self.assertFalse(p['output'].exists())
            if operation=='apply': self.assertIsNone(a.load_json(p['checkpoint'])['next_action_id'])
            else: self.assertFalse(p['checkpoint'].exists() or t.writes)

    def test_output_race_never_clobbers_another_file(self):
        f = flow(); args,p = self.inputs(f,'verify',applied=f['apply_result']); t = PublicCatalog(f,6,final_view())
        def race(path,value):
            path.write_text('sentinel')
            publish(path,value)
        with patch('spine_packs.__main__.publish',side_effect=race): code,envelope = self.invoke(args,t)
        self.assertEqual((code,envelope['error']['code']),(2,'output_already_exists'))
        self.assertIsNone(envelope['artifact']); self.assertEqual(p['output'].read_text(),'sentinel')
        self.assertFalse(list(p['output'].parent.glob('.spine-plan-*')))

    def test_admitted_checkpoint_directory_fsync_failure_stops_before_retry(self):
        f = flow(); args,p = self.inputs(f,'apply',source=prepared(f,3))
        t = PublicCatalog(f,3,companion('flight-create')['observations'][3]); original = os.fsync; count = 0
        def fail(fd):
            nonlocal count
            count += 1
            if count==2: raise OSError('PRIVATE_SENTINEL')
            return original(fd)
        with patch('spine_packs.apply.os.fsync',side_effect=fail): code,envelope = self.invoke(args,t)
        self.assertEqual(code,11); self.assertIsNone(envelope['artifact'])
        self.assertFalse(p['output'].exists() or t.writes); self.assertNotIn('PRIVATE_SENTINEL',a.canonical_text(envelope))


if __name__=='__main__': unittest.main()
