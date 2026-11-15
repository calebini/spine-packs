"""Opt-in FR-5 public-CLI qualification on newly allocated disposable ledgers.

No existing-ledger argument, Spine imports, SQL, items, facet values, disclosure
or delivery commands. Only faulted apply runs in-process; recovery is a new CLI.
"""
import argparse
from copy import deepcopy
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from qualification_support import QualificationResult, SCENARIO_IDS, completion_report

REQUIRED_SCENARIOS = tuple(name.rsplit('.',1)[1] for name in SCENARIO_IDS['v2'])
if '--installed' not in sys.argv:
    sys.path.insert(0,str(ROOT/'src'))
from spine_packs import artifacts as a
from spine_packs.__main__ import main as installer_main
from spine_packs.facet_apply_transport import FacetApplyCommand
from spine_packs.facet_contracts import artifact, body, seal, validate
from spine_packs.facet_inventory import COMMANDS, READ_COMMANDS
from spine_packs.facet_baselines import BASELINES, DEFAULT_RUNTIME, runtime_baseline
from spine_packs.facet_execution import WRITE_COMMANDS
from spine_packs.facet_manifest import digest as manifest_digest
from spine_packs.planning import PlanError


def save(path,value):
    with os.fdopen(os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'w') as out:
        json.dump(value,out,indent=2,sort_keys=True); out.write('\n')


class WriteFault(FacetApplyCommand):
    def __init__(self,target,command,after_commit=True):
        super().__init__(target)
        self.command=command; self.after_commit=after_commit; self.fired=False
        self.captured=None; self.request=None

    def write(self,command,request):
        if not self.fired and command==self.command:
            self.fired=True; self.request=deepcopy(request)
            if self.after_commit: self.captured=super().write(command,request)
            raise PlanError('transport_or_environment_failure','injected_response_loss')
        return super().write(command,request)


class FacetSpineTests(unittest.TestCase):
    config=None

    def setUp(self):
        if self.config is None: self.skipTest('opt-in disposable public-CLI qualification')
        self.folder=self.config['root']/self._testMethodName; self.folder.mkdir(mode=0o700)
        self.new_ledger('initial')

    def path(self,label):
        self.sequence+=1
        return self.case/f'{self.sequence:04d}-{label}.json'

    def process(self,argv,value=None,expected=0):
        p=subprocess.run([str(x) for x in argv],input=json.dumps(value or {})+'\n',text=True,
            capture_output=True,cwd=self.case,env=self.env,timeout=240)
        log=self.path('process'); save(log,dict(argv=[str(x) for x in argv],exit_code=p.returncode,
            stdout=p.stdout,stderr=p.stderr))
        self.assertEqual(p.returncode,expected,f'unexpected public CLI exit; inspect {log}')
        self.assertLessEqual(len(p.stdout.encode()),16*1024*1024)
        return json.loads(p.stdout)

    def public(self,command,value=None):
        self.assertIn(command,READ_COMMANDS|WRITE_COMMANDS|{'subject.upsert'})
        return self.process([self.config['command'],'--db',self.db,'--input','-',*command.split('.')],value)

    def setup_write(self,command,**fields):
        self.assertIn(command,WRITE_COMMANDS)
        return self.public(command,dict(contract_version=COMMANDS[command]['selector'],
            command_id='fr5-setup-'+str(uuid.uuid4()),actor_subject_id=self.actor,
            action_timestamp_utc='2035-02-01T12:00:00Z',**fields))

    def new_ledger(self,name):
        self.case=self.folder/name; self.case.mkdir(mode=0o700); self.sequence=0
        self.db=self.case/'new.sqlite'; self.assertFalse(self.db.exists())
        self.env=dict(self.config['env'])
        initialized=self.process([self.config['migrate'],'--db',self.db,'--initialize-if-empty'])
        baseline=self.config['baseline']
        self.assertEqual(str(initialized['after_version']),baseline.schema)
        info=self.public('system.info'); self.assertEqual(info['runtime_version'],baseline.runtime)
        self.assertEqual(info['ledger_schema_version'],info['implemented_ledger_schema_version'])
        self.assertEqual(info['ledger_schema_version'],baseline.schema)
        self.actor='fr5_synthetic_operator'; self.owner=dict(owner_kind='subject',owner_subject_id=self.actor)
        self.public('subject.upsert',dict(command_id='fr5-bootstrap',actor_subject_id=self.actor,
            subject_id=self.actor,subject_kind='agent',display_name='Disposable FR-5 operator',
            status='active',updated_at_utc='2035-02-01T12:00:00Z'))
        for key,value in {
            'SPINE_FACET_CURSOR_CONFIG':dict(secret_hex=secrets.token_hex(32),cursor_ledger_id='fr5-test',cursor_generation='1'),
            'SPINE_RENDERING_CURSOR_CONFIG':dict(contract_version='spine.notification-rendering-cursor-config.v1',
                key_id='fr5-key',key_generation='1',ledger_instance_id=info['ledger_instance_id'],secret_hex=secrets.token_hex(32)),
        }.items():
            path=self.case/(key+'.json'); save(path,value); self.env[key]=str(path)
        self.target=dict(host_name=socket.getfqdn().lower().removesuffix('.'),
            spine_command=dict(path=str(self.config['command']),sha256=hashlib.sha256(self.config['command'].read_bytes()).hexdigest()),
            ledger=dict(kind='path',path=str(self.db)))

    def metadata(self):
        # Metadata only. Never read or hash ledger/WAL contents.
        return {p.name:(p.stat().st_size,p.stat().st_mtime_ns) for p in self.case.glob('new.sqlite*')}

    def pack(self,updated=False):
        pack=a.load_json(ROOT/'tests/fixtures/pack-manifest-v2/flight.json')
        pack['pack']=dict(pack_id='fr5-flight-qualification',version='1.0.1' if updated else '1.0.0',status='released')
        pack['compatibility']['spine_runtime_versions']=[self.config['baseline'].runtime]
        if updated:
            pack['archetypes'][0]['revision']['description']='Synthetic revised flight archetype'
            pack['facet_schemas'][0]['definition']['description']='Synthetic revised schema'
            pack['rendering_definitions'][0]['revision']['display_name']='Synthetic revised rendering'
            pack['notification_profiles'][0]['display_name']='Synthetic revised flight reminders'
            pack['notification_profiles'][0]['revision']['templates'][0]['late_handling']['grace_seconds']='1800'
        pack['content_identity']['digest']=manifest_digest(pack)
        path=self.path('manifest'); save(path,pack); return path

    def invoke(self,operation,expected=0,factory=None,**inputs):
        output=self.path(operation); args=[operation,'--output',str(output)]
        for key,value in inputs.items(): args+=['--'+key.replace('_','-'),str(value)]
        before=self.metadata()
        if factory is None:
            envelope=self.process([*self.config['installer'],*args],expected=expected)
        else:
            with patch.dict(os.environ,self.env,clear=True),contextlib.redirect_stdout(io.StringIO()) as out:
                code=installer_main(args,transport_factory=factory)
            save(self.path('fault-envelope'),dict(argv=args,exit_code=code,stdout=out.getvalue()))
            self.assertEqual(code,expected); self.assertEqual(len(out.getvalue().splitlines()),1)
            envelope=json.loads(out.getvalue())
        validate(envelope,'spine-pack-installer-result.v2.schema.json')
        self.assertEqual(envelope['exit_code'],str(expected))
        if operation in ('plan','verify'): self.assertEqual(self.metadata(),before,'read-only invocation changed ledger metadata')
        if envelope['artifact'] is None:
            self.assertFalse(output.exists()); return None,envelope
        value=a.load_json(output); kind={'plan':'install-plan','apply':'apply-result','verify':'verification-result'}[operation]
        artifact(value,kind); self.assertEqual(value['content_identity']['digest'],envelope['artifact']['digest'])
        self.assertEqual(output.stat().st_mode&0o777,0o600)
        return output,value

    def plan(self,manifest,expected=0):
        request=seal(dict(artifact_schema='spine.pack-install-request.v2',request=dict(
            selection=dict(mode='archetypes',archetype_keys=['flight']),owner=self.owner,target=self.target,draft_posture='reject')))
        path=self.path('request'); save(path,request)
        return self.invoke('plan',expected,manifest=manifest,request=path)

    def approve(self,plan,complete=True):
        value=seal(dict(artifact_schema='spine.pack-install-approval.v2',plan_digest=plan['content_identity']['digest'],
            approve_complete_plan=True,acknowledge_single_operator=True,
            authorized_update_action_ids=plan['decision_action_ids'] if complete else [],
            execution=dict(execution_id=str(uuid.uuid4()),actor_subject_id=self.actor,action_timestamp_utc='2035-02-01T12:00:00Z')))
        path=self.path('approval'); save(path,value); return path

    def apply(self,manifest,plan,approval,expected=0,source=None,factory=None):
        cp=self.path('checkpoint'); args=dict(manifest=manifest,plan=plan,approval=approval,checkpoint=cp)
        if source is not None: args['continue_from']=source
        output,value=self.invoke('apply',expected,factory,**args)
        if cp.exists():
            artifact(a.load_json(cp),'apply-checkpoint'); self.assertEqual(cp.stat().st_mode&0o777,0o600)
        return output,value,cp

    def install(self):
        manifest=self.pack(); plan,p=self.plan(manifest); self.assertEqual(len(p['actions']),6)
        approved=self.approve(p)
        result,value,cp=self.apply(manifest,plan,approved); self.assertEqual(value['state'],'applied')
        _,verified=self.invoke('verify',manifest=manifest,plan=plan,result=result)
        self.assertEqual(verified['state'],'verified'); self.assertEqual(verified['response_evidence'],'complete')
        self.assertEqual(verified['receipt_readback'],self.config['baseline'].receipt_readback)
        self.assertEqual(verified['disclosure'],'separate_operator_configuration_required')
        return manifest,plan,result,cp,approved

    def drift_binding(self):
        archetype=self.public('item_archetype.list',dict(contract_version='spine.item-archetypes.v1',owner=self.owner,limit='100'))['entries'][0]
        profile=deepcopy(a.load_json(self.pack())['notification_profiles'][0])
        for t in profile['revision']['templates']: del t['rendering']
        other=self.public('notification_profile.create',dict(contract_version='spine.notification-profiles.v1',
            command_id='fr5-ordinary-'+str(uuid.uuid4()),actor_subject_id=self.actor,action_timestamp_utc='2035-02-01T12:00:00Z',
            owner=self.owner,profile_key='fr5_ordinary',display_name='Synthetic ordinary v1',description=None,revision=profile['revision']))
        self.setup_write('notification_profile.binding.set',owner=self.owner,item_archetype_id=archetype['item_archetype_id'],
                         notification_profile_id=other['notification_profile_id'])
        return other

    def test_create_retain_complete_checkpoint_and_read_only_verify(self):
        manifest,plan,result,cp,_=self.install()
        before=cp.read_bytes(); metadata=self.metadata()
        _,resumed,_=self.apply(manifest,plan,self.approve(a.load_json(plan)),source=cp,expected=2)
        # A new execution cannot adopt an old checkpoint.
        self.assertEqual(resumed['error']['category'],'invalid_cli_or_artifact_input')
        self.assertEqual(cp.read_bytes(),before); self.assertEqual(self.metadata(),metadata)
        retained,p=self.plan(manifest); self.assertEqual(p['actions'],[])
        _,verified=self.invoke('verify',manifest=manifest,plan=retained)
        self.assertEqual(verified['state'],'verified'); self.assertEqual(verified['response_evidence'],'not_required')
        _,missing=self.invoke('verify',10,manifest=manifest,plan=plan)
        self.assertEqual(missing['response_evidence'],'missing')
        draft=a.load_json(manifest); draft['pack'].update(status='draft',version='1.0.1-draft.1')
        draft['content_identity']['digest']=manifest_digest(draft); draft_path=self.path('draft'); save(draft_path,draft)
        self.plan(draft_path,expected=3)

    def test_update_cascade_binding_drift_and_approval(self):
        original,old_plan,old_result,completed,approved=self.install()
        # Reuse the original execution, not a newly generated approval. A
        # completed checkpoint must still be admitted against fresh live state.
        disk_checkpoint=a.load_json(completed)
        self.assertEqual([e['action_id'] for e in disk_checkpoint['accepted_responses']],
                         [action['action_id'] for action in a.load_json(old_plan)['actions']])
        self.assertIsNone(disk_checkpoint['next_action_id'])
        self.assertIsNone(disk_checkpoint['unresolved_submission'])
        self.assertEqual(disk_checkpoint,a.load_json(old_result)['checkpoint'])
        preserved=completed.read_bytes(); approval_bytes=approved.read_bytes()
        self.drift_binding()
        before=self.metadata()
        _,refused,new_checkpoint=self.apply(original,old_plan,approved,source=completed,expected=7)
        self.assertEqual(refused['error']['code'],'unexplained_recovery_change')
        self.assertFalse(new_checkpoint.exists())
        self.assertEqual(completed.read_bytes(),preserved); self.assertEqual(approved.read_bytes(),approval_bytes)
        self.assertEqual(self.metadata(),before,'failed fresh admission changed ledger metadata')
        updated=self.pack(updated=True); plan,p=self.plan(updated,expected=5)
        expected={'item_archetype.revise','facet_schema.publish','item_archetype.facet_binding.set',
            'notification_rendering_definition.publish','notification_profile.metadata.update',
            'notification_profile.revise','notification_profile.binding.set'}
        self.assertEqual({x['command'] for x in p['actions']},expected)
        _,refused,cp=self.apply(updated,plan,self.approve(p,False),expected=2)
        self.assertFalse(cp.exists()); self.assertEqual(refused['error']['category'],'invalid_cli_or_artifact_input')
        result,applied,_=self.apply(updated,plan,self.approve(p)); self.assertEqual(applied['state'],'applied')
        _,verified=self.invoke('verify',manifest=updated,plan=plan,result=result); self.assertEqual(verified['state'],'verified')
        _,old=self.invoke('verify',10,manifest=original,plan=old_plan,result=old_result); self.assertEqual(old['state'],'mismatch')

    def test_each_write_response_loss_replays_exact_request_and_ids(self):
        covered=set()
        for command in sorted(WRITE_COMMANDS):
            with self.subTest(command=command):
                self.new_ledger(command.replace('.','-'))
                update=command.endswith(('.revise','.publish','.update'))
                if update: self.install()
                manifest=self.pack(updated=update); plan,p=self.plan(manifest,expected=5 if update else 0)
                approved=self.approve(p); fault=WriteFault(self.target,command)
                partial,interrupted,cp=self.apply(manifest,plan,approved,expected=9,factory=lambda _:fault)
                self.assertTrue(fault.fired); self.assertIsNotNone(fault.captured)
                index=len(interrupted['checkpoint']['accepted_responses'])
                source=partial if index%2 else cp; preserved=source.read_bytes()
                save(self.path('discarded-real-response'),dict(request=fault.request,response=json.loads(fault.captured)))
                result,resumed,completed=self.apply(manifest,plan,approved,source=source)
                self.assertEqual(source.read_bytes(),preserved); self.assertEqual(resumed['state'],'applied')
                e=resumed['checkpoint']['accepted_responses'][index]
                self.assertEqual(body(e['request']),fault.request)
                replay=json.loads(e['response']['json_text']); expected=json.loads(fault.captured)
                if 'replayed' in expected: expected.update(replayed=True,changed=False)
                self.assertEqual(replay,expected)
                _,verified=self.invoke('verify',manifest=manifest,plan=plan,result=result)
                self.assertEqual(verified['state'],'verified'); covered.add(command)
                before=self.metadata(); preserved=completed.read_bytes()
                _,again,_=self.apply(manifest,plan,approved,source=completed)
                self.assertEqual(again['state'],'applied'); self.assertEqual(self.metadata(),before)
                self.assertEqual(completed.read_bytes(),preserved)
        self.assertEqual(covered,WRITE_COMMANDS)
        save(self.folder/'covered-writes.json',sorted(covered))

    def test_prepared_before_submission_and_no_clobber(self):
        manifest=self.pack(); plan,p=self.plan(manifest); approved=self.approve(p)
        fault=WriteFault(self.target,'item_archetype.create',after_commit=False)
        _,interrupted,cp=self.apply(manifest,plan,approved,expected=9,factory=lambda _:fault)
        self.assertEqual(interrupted['checkpoint']['accepted_responses'],[]); self.assertIsNone(fault.captured)
        result,_,_=self.apply(manifest,plan,approved,source=cp)
        preserved=plan.read_bytes()
        args=[*self.config['installer'],'verify','--manifest',str(manifest),'--plan',str(plan),'--result',str(result),'--output',str(plan)]
        envelope=self.process(args,expected=2); self.assertEqual(envelope['error']['code'],'output_already_exists')
        self.assertEqual(plan.read_bytes(),preserved)
        _,envelope=self.invoke('verify',2,manifest=manifest,plan=plan,result=self.db)
        self.assertEqual(envelope['error']['code'],'verification_result_input_collision')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spine-command',required=True,type=Path)
    parser.add_argument('--spine-ledger-migrate',required=True,type=Path)
    parser.add_argument('--evidence-parent',type=Path,default=Path(tempfile.gettempdir()))
    parser.add_argument('--test',action='append')
    parser.add_argument('--installed',action='store_true')
    parser.add_argument('--runtime-version',choices=tuple(BASELINES),default=DEFAULT_RUNTIME)
    args=parser.parse_args()
    command=args.spine_command.resolve(strict=True); migrate=args.spine_ledger_migrate.resolve(strict=True)
    if command.parent!=migrate.parent: parser.error('use one isolated Spine installation')
    env=dict(PATH=str(command.parent)+':/usr/bin:/bin',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',LC_ALL='C')
    if args.installed:
        prefix=Path(sys.prefix).resolve(); cli=prefix/'bin/spine-packs'
        if sys.prefix==sys.base_prefix or not Path(a.__file__).resolve().is_relative_to(prefix) or not cli.is_file():
            parser.error('installed mode requires an isolated installed wheel')
        if a.SCHEMA_ROOT!=Path(a.__file__).resolve().parent/'_schemas' or not a.SCHEMA_ROOT.is_dir():
            parser.error('installed schema resources unavailable')
        installer=[str(cli)]
    else:
        env['PYTHONPATH']=str(ROOT/'src'); installer=[sys.executable,'-m','spine_packs']
    run=Path(tempfile.mkdtemp(prefix='spine-packs-fr5-integration-',dir=args.evidence_parent)).resolve()
    baseline=runtime_baseline(args.runtime_version)
    FacetSpineTests.config=dict(root=run,command=command,migrate=migrate,env=env,installer=installer,baseline=baseline)
    save(run/'run.json',dict(baseline=dict(commit=baseline.commit,runtime=baseline.runtime,schema=baseline.schema),
        installed=args.installed,installer=installer,module=a.__file__,schemas=str(a.SCHEMA_ROOT),
        spine_command=str(command),spine_ledger_migrate=str(migrate)))
    print(f'Private FR-5 evidence: {run}',flush=True)
    suite=unittest.TestSuite(FacetSpineTests(n) for n in args.test) if args.test else unittest.defaultTestLoader.loadTestsFromTestCase(FacetSpineTests)
    result=unittest.TextTestRunner(verbosity=2,resultclass=QualificationResult).run(suite)
    report=completion_report(result,SCENARIO_IDS['v2'],focused=bool(args.test))
    save(run/'result.json',report)
    return 0 if report['passed'] else 1


if __name__=='__main__': raise SystemExit(main())
