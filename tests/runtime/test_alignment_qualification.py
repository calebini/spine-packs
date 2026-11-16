"""AL-3 qualification admission and parent-owned evidence correlation; no ledgers."""
from copy import deepcopy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[2]
def module(name):
    spec=importlib.util.spec_from_file_location('al3_'+name,ROOT/'scripts'/('qualify_'+name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
q=module('fr5');fr2=module('fr2')


class AlignmentQualificationTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch('qualification_support.installed_package_root',
            side_effect=lambda prefix:prefix/'lib/site-packages/spine_packs'))

    def test_only_selected_exact_successor_added_and_old_default_preserved(self):
        self.assertEqual(q.selected_pins('0.10.0'),q.SPINE_PINS)
        selected=q.selected_pins('0.12.0')
        self.assertEqual({k:v for k,v in selected.items() if k!='0.12.0'},q.SPINE_PINS)
        self.assertEqual(selected['0.12.0'],'3e65ef0de9e73b62047a0f6328731db08ca91023')
        for version,baseline in q.SUCCESSOR_PINS.items():
            inv=json.loads((ROOT/('contracts/installer-spine-'+version+'-inventory.json')).read_text())
            self.assertEqual((baseline['commit'],baseline['schema']),(inv['spine_commit'],inv['ledger_schema']))
        for version in ('0.9.1','0.11.0','0.12.1','>=0.12.0'):
            with self.subTest(version=version),self.assertRaises(RuntimeError):q.selected_pins(version)

    def identity(self,runtime,installed):
        prefix=Path('/synthetic/installer');bin_dir=Path('/synthetic/spine/bin')
        baseline=dict(commit=q.SUCCESSOR_PINS[runtime]['commit'],runtime=runtime,schema=q.SUCCESSOR_PINS[runtime]['schema'])
        module=prefix/'lib/site-packages/spine_packs/artifacts.py' if installed else ROOT/'src/spine_packs/artifacts.py'
        schemas=module.parent/'_schemas' if installed else ROOT/'contracts/schemas'
        return dict(baseline=baseline,installed=installed,module=str(module),schemas=str(schemas),
            installer=[str(prefix/'bin/spine-packs')] if installed else [sys.executable,'-m','spine_packs'],
            spine_command=str(bin_dir/'spine-command'),spine_ledger_migrate=str(bin_dir/'spine-ledger-migrate')),prefix,bin_dir

    def test_parent_rejects_mixed_baseline_mode_target_and_source_resource_leaks(self):
        for runtime in q.SUCCESSOR_PINS:
            for installed in (False,True):
                record,prefix,bin_dir=self.identity(runtime,installed)
                q.require_identity(record,runtime=runtime,installed=installed,bin_dir=bin_dir,installer_prefix=prefix)
                for fault in ('commit','schema','runtime','mode','target','migrate','module','schemas'):
                    changed=deepcopy(record)
                    if fault in ('commit','schema','runtime'):changed['baseline'][fault]='wrong'
                    elif fault=='mode':changed['installed']=not installed
                    elif fault=='target':changed['spine_command']='/different/spine-command'
                    elif fault=='migrate':changed['spine_ledger_migrate']='/different/spine-ledger-migrate'
                    else:changed[fault]='/different/checkout'
                    with self.subTest(runtime=runtime,installed=installed,fault=fault),self.assertRaises(RuntimeError):
                        q.require_identity(changed,runtime=runtime,installed=installed,bin_dir=bin_dir,installer_prefix=prefix)

    def test_read_gate_requires_all_named_checks_and_exact_wheel_mode_and_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            wheel=Path(tmp)/'synthetic.whl';wheel.write_bytes(b'synthetic digest only')
            for runtime in q.SUCCESSOR_PINS:
                identity,prefix,bin_dir=self.identity(runtime,True)
                record=dict(status='passed',checks=sorted(q.READ_GATE_CHECKS),
                    provenance=dict(identity['baseline'],wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest()),
                    installed_installer=True,installer_module=identity['module'],installer_schemas=identity['schemas'],
                    spine_command=identity['spine_command'],spine_ledger_migrate=identity['spine_ledger_migrate'])
                options=dict(runtime=runtime,installed=True,bin_dir=bin_dir,wheel=wheel,installer_prefix=prefix)
                q.require_read_gate(record,**options)
                for fault in ('checks','duplicate','commit','wheel','mode','schema_root','target','module'):
                    changed=deepcopy(record)
                    if fault=='checks':changed['checks'].pop()
                    elif fault=='duplicate':changed['checks'].append(changed['checks'][0])
                    elif fault=='commit':changed['provenance']['commit']='wrong'
                    elif fault=='wheel':changed['provenance']['wheel_sha256']='wrong'
                    elif fault=='mode':changed['installed_installer']=False
                    elif fault=='schema_root':changed['installer_schemas']=str(ROOT/'contracts/schemas')
                    elif fault=='target':changed['spine_command']='/wrong/spine-command'
                    else:changed['installer_module']=str(ROOT/'src/spine_packs/artifacts.py')
                    with self.subTest(runtime=runtime,fault=fault),self.assertRaises(RuntimeError):q.require_read_gate(changed,**options)

    def test_thin_fr2_wheel_cannot_pass_before_public_cli_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);wheel=root/'thin.whl'
            with zipfile.ZipFile(wheel,'w') as archive:archive.writestr('spine/__init__.py',b'# exact\n')
            pin=q.SUCCESSOR_PINS['0.12.0']['commit']
            def output(argv,**kwargs):
                if 'rev-parse' in argv:return pin+'\n'
                if '-I' in argv:return str(root/'site-packages')+'\n'
                if 'ls-tree' in argv:return 'src/spine/__init__.py\nsrc/spine/required.py\n'
                raise AssertionError('unexpected subprocess')
            with patch.object(fr2.subprocess,'check_output',side_effect=output):
                with self.assertRaisesRegex(RuntimeError,'Python closure'):
                    fr2.provenance(root,root,wheel,root/'bin','0.12.0')

    def test_source_snapshot_covers_harness_inventory_and_packaged_inputs(self):
        value=q.source_snapshot()
        for name in ('scripts/qualify_fr5.py','scripts/qualify_fr2.py','tests/integration/test_facet_spine.py',
                     'tests/integration/qualification_support.py','contracts/installer-spine-0.12.0-inventory.json',
                     'src/spine_packs/facet_transport.py','tests/fixtures/installer-v2/flight-create.json'):
            self.assertEqual(value[name],hashlib.sha256((ROOT/name).read_bytes()).hexdigest())




class QualificationRepairTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch('qualification_support.installed_package_root',
            side_effect=lambda prefix:prefix/'lib/site-packages/spine_packs'))

    def test_v1_expected_pins_and_same_schema_cross_baseline_refused(self):
        import qualification_support as support
        for version, baseline in support.V1_BASELINES.items():
            self.assertEqual(baseline['commit'], q.SPINE_PINS[version])
            for installed in (False, True):
                prefix=Path('/synthetic/installer');bin_dir=Path('/synthetic/upstream/bin')
                module=prefix/'lib/site-packages/spine_packs/artifacts.py' if installed else ROOT/'src/spine_packs/artifacts.py'
                record=dict(baseline=baseline,installed=installed,module=str(module),
                    installer=[str(prefix/'bin/spine-packs')] if installed else [sys.executable,'-m','spine_packs'],
                    schemas=str(module.parent/'_schemas' if installed else ROOT/'contracts/schemas'),
                    spine_command=str(bin_dir/'spine-command'),spine_ledger_migrate=str(bin_dir/'spine-ledger-migrate'))
                options=dict(runtime=version,installed=installed,bin_dir=bin_dir,installer_prefix=prefix)
                q.require_identity(record,**options)
                for other in support.V1_BASELINES:
                    if other==version:continue
                    changed=deepcopy(record);changed['baseline']=support.V1_BASELINES[other]
                    with self.subTest(version=version,other=other,installed=installed),self.assertRaises(RuntimeError):
                        q.require_identity(changed,**options)
                for field in ('installed','spine_command','spine_ledger_migrate','module','schemas'):
                    changed=deepcopy(record);changed[field]=not installed if field=='installed' else '/wrong'
                    with self.subTest(version=version,field=field),self.assertRaises(RuntimeError):
                        q.require_identity(changed,**options)

    def test_v1_observed_runtime_cannot_select_expected_baseline(self):
        import qualification_support as support
        for version,baseline in support.V1_BASELINES.items():
            info=dict(runtime_version=version,ledger_schema_version=baseline['schema'],
                      implemented_ledger_schema_version=baseline['schema'])
            support.require_environment(info,baseline)
            for field in info:
                bad=dict(info);bad[field]='0.5.0' if field=='runtime_version' and version=='0.6.0' else 'wrong'
                with self.subTest(version=version,field=field),self.assertRaises(RuntimeError):
                    support.require_environment(bad,baseline)

    def test_replay_parent_rejects_missing_duplicate_substituted_and_extra_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'covered-writes.json'
            for version in q.SUCCESSOR_PINS:
                with self.assertRaises(RuntimeError):q.require_replay_coverage(root,version)
                inv=json.loads((ROOT/('contracts/installer-spine-'+version+'-inventory.json')).read_text())
                good=sorted(k for k,v in inv['commands'].items() if v['phase'] is not None)
                path.write_text(json.dumps(good));q.require_replay_coverage(root,version)
                for bad in (good[:-1],good[:-1]+[good[0]],good[:-1]+['item.create'],good+['item.create'],{},[None]*11):
                    path.write_text(json.dumps(bad))
                    with self.subTest(version=version,bad=bad),self.assertRaises(RuntimeError):
                        q.require_replay_coverage(root,version)
                path.unlink()

    def pages(self):
        expected={'a_legacy':('root-a','revision-a','spine.notification-profiles.v1'),
                  'b_ordinary':('root-b','revision-b','spine.notification-profiles.v2'),
                  'definition':('root-c','revision-c','spine.notification-profiles.v2')}
        rows=[]
        for _ in range(2):
            cursor=None
            for index,(key,value) in enumerate(expected.items()):
                request=dict(limit='1',owner='synthetic',contract_version='spine.notification-profiles.v2')
                if cursor is not None:request['cursor']=cursor
                next_cursor='page-'+str(index+1) if index<2 else None
                rows.append(dict(command='notification_profile.list',request=request,response=dict(
                    catalog_snapshot_hash='snapshot',count='1',has_more=index<2,next_cursor=next_cursor,
                    entries=[dict(profile_key=key,notification_profile_id=value[0],current_revision_id=value[1],
                                  revision=dict(revision_contract=value[2]))])))
                cursor=next_cursor
        return rows,expected

    def test_pagination_requires_all_seeded_identities_in_each_pass(self):
        rows,expected=self.pages()
        self.assertEqual(fr2.require_profile_pagination(rows,expected,limit=1)['pages'],[3,3])
        for fault in ('omit_both','wrong_root','wrong_revision','wrong_contract','duplicate','one_pass','truncated'):
            bad=deepcopy(rows)
            if fault=='omit_both':
                for i in (1,4):bad[i]['response'].update(entries=[],count='0')
            elif fault.startswith('wrong_'):
                field={'wrong_root':'notification_profile_id','wrong_revision':'current_revision_id'}.get(fault)
                if field:bad[0]['response']['entries'][0][field]='wrong'
                else:bad[0]['response']['entries'][0]['revision']['revision_contract']='wrong'
            elif fault=='duplicate':bad[1]['response']['entries']=deepcopy(bad[0]['response']['entries'])
            elif fault=='one_pass':bad=bad[:3]
            else:bad=bad[:-1]
            with self.subTest(fault=fault),self.assertRaises(RuntimeError):fr2.require_profile_pagination(bad,expected,limit=1)

    def test_pagination_rejects_broken_chains_query_snapshot_and_continuations(self):
        rows,expected=self.pages()
        for fault in ('cursor','missing_next','cycle','snapshot','query','count','premature_end','unterminated'):
            bad=deepcopy(rows)
            if fault=='cursor':bad[1]['request']['cursor']='wrong'
            elif fault=='missing_next':bad[0]['response']['next_cursor']=None
            elif fault=='cycle':bad[1]['response']['next_cursor']='page-1'
            elif fault=='snapshot':bad[1]['response']['catalog_snapshot_hash']='wrong'
            elif fault=='query':bad[1]['request']['owner']='wrong'
            elif fault=='count':bad[1]['response']['count']='0'
            elif fault=='premature_end':bad[0]['response'].update(has_more=False,next_cursor=None)
            else:bad[-1]['response'].update(has_more=True,next_cursor='another')
            with self.subTest(fault=fault),self.assertRaises(RuntimeError):fr2.require_profile_pagination(bad,expected,limit=1)

    def console_fixture(self,root):
        import qualification_support as support
        bin_dir=root/'installed/bin';bin_dir.mkdir(parents=True)
        (bin_dir/'python').write_bytes(b'synthetic interpreter identity; never executed')
        site=root/'site-packages';meta=site/'spine_ledger-0.12.0.dist-info/entry_points.txt'
        meta.parent.mkdir(parents=True)
        scripts={'spine-command':'spine.commands.cli:main','spine-ledger-migrate':'spine.ledger.migrate:main'}
        project=('[project]\nname="spine-ledger"\n[project.scripts]\n'+
                 ''.join('"'+k+'"="'+v+'"\n' for k,v in scripts.items())).encode()
        metadata=('[console_scripts]\n'+''.join(k+' = '+v+'\n' for k,v in scripts.items())).encode()
        meta.write_bytes(metadata)
        wheel=root/'upstream.whl'
        with zipfile.ZipFile(wheel,'w') as archive:archive.writestr(str(meta.relative_to(site)),metadata)
        for name,target in scripts.items():
            module,function=target.split(':')
            text=('#!'+str(bin_dir/'python')+'\nimport sys\nfrom '+module+' import '+function+
                "\nif __name__ == '__main__':\n    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n    sys.exit("+function+"())\n")
            path=bin_dir/name;path.write_text(text);path.chmod(0o700)
        return support,project,wheel,bin_dir,site,meta

    def test_console_provenance_rejects_wrong_interpreter_dispatch_extra_code_and_links(self):
        for name in ('spine-command','spine-ledger-migrate'):
            for fault in ('interpreter','dispatch','extra_code','link'):
                with self.subTest(name=name,fault=fault),tempfile.TemporaryDirectory() as tmp:
                    support,project,wheel,bin_dir,site,_=self.console_fixture(Path(tmp))
                    good=support.attest_console_scripts(project,wheel,bin_dir,site)
                    support.verify_console_scripts(good,bin_dir)
                    path=bin_dir/name
                    if fault=='interpreter':path.write_text(path.read_text().replace(str(bin_dir/'python'),'/another/python'))
                    elif fault=='dispatch':path.write_text(path.read_text().replace('import main','import other'))
                    elif fault=='extra_code':path.write_text(path.read_text()+"print('wrong dispatch')\n")
                    else:
                        original=bin_dir/(name+'-original');path.rename(original);path.symlink_to(original)
                    with self.assertRaises(RuntimeError):support.attest_console_scripts(project,wheel,bin_dir,site)

    def test_console_metadata_must_match_pinned_export_and_installed_copy(self):
        for fault in ('mapping','installed_metadata'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as tmp:
                support,project,wheel,bin_dir,site,meta=self.console_fixture(Path(tmp))
                if fault=='mapping':project=project.replace(b'spine.commands.cli:main',b'spine.commands.cli:other')
                else:meta.write_bytes(b'[console_scripts]\nwrong = wrong:main\n')
                with self.assertRaises(RuntimeError):support.attest_console_scripts(project,wheel,bin_dir,site)

    def test_attested_launchers_interpreter_and_metadata_cannot_change_after_proof(self):
        for fault in ('spine-command','spine-ledger-migrate','python','metadata'):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as tmp:
                support,project,wheel,bin_dir,site,meta=self.console_fixture(Path(tmp))
                proof=support.attest_console_scripts(project,wheel,bin_dir,site)
                target=meta if fault=='metadata' else bin_dir/fault
                target.write_bytes(target.read_bytes()+b'\n# changed\n')
                with self.assertRaises(RuntimeError):support.verify_console_scripts(proof,bin_dir)



class QualificationFollowupTests(unittest.TestCase):
    def test_parent_rejects_paired_in_prefix_relocation_and_wrong_installer(self):
        import qualification_support as support
        prefix=Path('/synthetic/installer');bin_dir=Path('/synthetic/spine/bin')
        selected_root=prefix/'lib/python3.14/site-packages/spine_packs'
        for runtime in (*support.V1_BASELINES,*q.SUCCESSOR_PINS):
            baseline=(support.V1_BASELINES[runtime] if runtime in support.V1_BASELINES else
                dict(runtime=runtime,commit=q.SUCCESSOR_PINS[runtime]['commit'],schema=q.SUCCESSOR_PINS[runtime]['schema']))
            for installed in (False,True):
                module=selected_root/'artifacts.py' if installed else ROOT/'src/spine_packs/artifacts.py'
                record=dict(baseline=baseline,installed=installed,module=str(module),
                    schemas=str(selected_root/'_schemas' if installed else ROOT/'contracts/schemas'),
                    installer=[str(prefix/'bin/spine-packs')] if installed else [sys.executable,'-m','spine_packs'],
                    spine_command=str(bin_dir/'spine-command'),spine_ledger_migrate=str(bin_dir/'spine-ledger-migrate'))
                options=dict(runtime=runtime,installed=installed,bin_dir=bin_dir,installer_prefix=prefix)
                with patch.object(support,'installed_package_root',return_value=selected_root):
                    q.require_identity(record,**options)
                    wrong=deepcopy(record);wrong['installer']=['/other/venv/bin/spine-packs']
                    with self.subTest(runtime=runtime,installed=installed),self.assertRaisesRegex(RuntimeError,'installer command'):
                        q.require_identity(wrong,**options)
                    missing=deepcopy(record);missing.pop('installer')
                    with self.assertRaisesRegex(RuntimeError,'installer command'):q.require_identity(missing,**options)
                    if installed:
                        relocated=deepcopy(record);relocated['module']=str(prefix/'other/spine_packs/artifacts.py')
                        relocated['schemas']=str(prefix/'other/spine_packs/_schemas')
                        with self.assertRaisesRegex(RuntimeError,'source/resource leak'):q.require_identity(relocated,**options)

    def test_exact_package_root_comes_from_selected_clean_interpreter(self):
        import qualification_support as support
        prefix=Path('/synthetic/clean');purelib=prefix/'lib/python3.14/site-packages'
        info=dict(executable=str(prefix/'bin/python'),prefix=str(prefix),purelib=str(purelib))
        with patch('subprocess.check_output',return_value=json.dumps(info)) as call:
            self.assertEqual(support.installed_package_root(prefix),purelib/'spine_packs')
            argv=call.call_args.args[0]
            self.assertEqual(argv[:3],[str(prefix/'bin/python'),'-I','-c'])
            self.assertIn('sysconfig.get_path("purelib")',argv[3])
        for field in ('executable','prefix','purelib'):
            wrong=dict(info);wrong[field]='/other/environment'
            with self.subTest(field=field),patch('subprocess.check_output',return_value=json.dumps(wrong)):
                with self.assertRaises(RuntimeError):support.installed_package_root(prefix)

    def test_complete_pagination_at_consistent_wrong_limit_is_rejected(self):
        rows,expected=QualificationRepairTests.pages(self)
        big=[]
        for offset in (0,3):
            row=deepcopy(rows[offset]);row['request']['limit']='100'
            row['response'].update(entries=[deepcopy(rows[i]['response']['entries'][0]) for i in range(offset,offset+3)],
                count='3',has_more=False,next_cursor=None)
            big.append(row)
        self.assertEqual(fr2.require_profile_pagination(big,expected,limit=100)['pages'],[1,1])
        with self.assertRaisesRegex(RuntimeError,'selected limit'):
            fr2.require_profile_pagination(big,expected,limit=1)
        with self.assertRaisesRegex(RuntimeError,'selected limit'):
            fr2.require_profile_pagination(rows,expected,limit=100)
        mixed=rows[:3]+big[1:]
        with self.assertRaisesRegex(RuntimeError,'selected limit'):
            fr2.require_profile_pagination(mixed,expected,limit=1)

    def test_permission_only_launcher_change_is_rejected(self):
        for name in ('spine-command','spine-ledger-migrate'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as tmp:
                support,project,wheel,bin_dir,site,_=QualificationRepairTests.console_fixture(self,Path(tmp))
                proof=support.attest_console_scripts(project,wheel,bin_dir,site)
                support.verify_console_scripts(proof,bin_dir)
                path=bin_dir/name;before=path.read_bytes();path.chmod(0o600)
                self.assertEqual(path.read_bytes(),before)
                with self.assertRaises(RuntimeError):support.verify_console_scripts(proof,bin_dir)





class RemainingQualificationGapTests(unittest.TestCase):
    def test_real_directory_symlink_relocation_cannot_redefine_expected_paths(self):
        import qualification_support as support
        with tempfile.TemporaryDirectory() as tmp:
            prefix=Path(tmp).resolve()/'selected';purelib=prefix/'lib/python3.14/site-packages'
            package=purelib/'spine_packs';(package/'_schemas').mkdir(parents=True)
            (package/'artifacts.py').write_text('# synthetic identity fixture only\n')
            info=dict(executable=str(prefix/'bin/python'),prefix=str(prefix),purelib=str(purelib))
            bin_dir=Path('/synthetic/upstream/bin')
            record=dict(baseline=support.V1_BASELINES['0.6.0'],installed=True,
                module=str(package/'artifacts.py'),schemas=str(package/'_schemas'),
                installer=[str(prefix/'bin/spine-packs')],spine_command=str(bin_dir/'spine-command'),
                spine_ledger_migrate=str(bin_dir/'spine-ledger-migrate'))
            options=dict(runtime='0.6.0',installed=True,bin_dir=bin_dir,installer_prefix=prefix)
            with patch('subprocess.check_output',return_value=json.dumps(info)):
                q.require_identity(record,**options)
                relocated=prefix/'other/spine_packs';relocated.parent.mkdir()
                package.rename(relocated);package.symlink_to(relocated,target_is_directory=True)
                for actual_paths in (False,True):
                    changed=deepcopy(record)
                    if actual_paths:
                        changed.update(module=str(relocated/'artifacts.py'),schemas=str(relocated/'_schemas'))
                    with self.subTest(actual_paths=actual_paths),self.assertRaisesRegex(RuntimeError,'source/resource leak'):
                        q.require_identity(changed,**options)

    def test_capture_boundary_rejects_retired_only_and_initial_only_wrong_limits(self):
        phases=(('empty',100),('seeded-small',1),('seeded-large',100),('retired',1))
        for bad_phase in ('empty','retired'):
            with self.subTest(bad_phase=bad_phase),patch.object(fr2.FacetSpineCommand,'read',return_value={'synthetic':'transport-result'}) as transport:
                for phase,limit in phases:
                    adapter=fr2.LimitCheckedFacetCommand({},expected_profile_limit=limit)
                    before=transport.call_count
                    if phase==bad_phase:
                        wrong='100' if limit==1 else '1'
                        with self.assertRaisesRegex(RuntimeError,'selected plan limit'):
                            adapter.read('notification_profile.list',dict(limit=wrong))
                        self.assertEqual(transport.call_count,before,'wrong request reached transport')
                    else:
                        adapter.read('notification_profile.list',dict(limit=str(limit)))
                        self.assertEqual(transport.call_count,before+1)

    def test_evidence_guard_rejects_old_verifier_logs_and_inconsistent_counts(self):
        import qualification_support as support
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);summary=root/'summary.json';checks=root/'checks.json'
            verifier=root/'fresh-verifier.py';verifier.write_bytes(b'# current evidence procedure\n')
            log=root/'fresh-focused.log';log.write_text('Ran 20 tests in 0.1s\n\nOK\n')
            old_verifier=root/'old-verifier.py';old_verifier.write_bytes(b'# earlier procedure\n')
            old_log=root/'old-focused.log';old_log.write_text('Ran 17 tests in 0.1s\n\nOK\n')
            metadata=dict(focused=dict(log=str(log),tests=20,sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
            summary.write_text(json.dumps(dict(verifier_sha256=hashlib.sha256(verifier.read_bytes()).hexdigest())))
            checks.write_text(json.dumps(metadata))
            call=lambda v=verifier,p=log:support.require_evidence_references(summary,checks,v,dict(focused=p))
            self.assertEqual(call()['logs']['focused']['tests'],20)
            with self.assertRaisesRegex(RuntimeError,'verifier evidence'):call(v=old_verifier)
            with self.assertRaisesRegex(RuntimeError,'test evidence'):call(p=old_log)
            changed=deepcopy(metadata);changed['focused']['tests']=17
            checks.write_text(json.dumps(changed))
            with self.assertRaisesRegex(RuntimeError,'test evidence'):call()
            log.write_text('Ran 20 tests in 0.1s\n\nFAILED\n')
            metadata['focused']['sha256']=hashlib.sha256(log.read_bytes()).hexdigest()
            checks.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(RuntimeError,'test evidence'):call()


class EvidenceReferenceFollowupTests(unittest.TestCase):
    def setUp(self):
        import qualification_support as support
        self.support=support
        self.root=Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.summary=self.root/'summary.json';self.checks=self.root/'checks.json'
        self.verifier=self.root/'verify.py';self.verifier.write_bytes(b'# selected verifier\n')
        self.summary_value=dict(verifier_path=str(self.verifier),
            verifier_sha256=hashlib.sha256(self.verifier.read_bytes()).hexdigest())
        self.summary.write_text(json.dumps(self.summary_value))
        self.logs={};self.metadata={}
        for name,count in dict(focused=20,preserved=14,contract=140,runtime=327).items():
            path=self.root/(name+'.log');path.write_text(f'Ran {count} tests in 0.1s\n\nOK\n')
            self.logs[name]=path
            self.metadata[name]=dict(log=str(path),tests=count,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        self.checks.write_text(json.dumps(self.metadata))

    def references(self, *, verifier=None, logs=None):
        return self.support.require_evidence_references(self.summary,self.checks,
            self.verifier if verifier is None else verifier,self.logs if logs is None else logs)

    def test_count_and_success_must_belong_to_terminal_summary(self):
        self.assertEqual(set(self.references()['logs']),set(self.metadata))
        path=self.logs['focused']
        for earlier,terminal in ((20,17),(17,20)):
            with self.subTest(earlier=earlier,terminal=terminal):
                path.write_text(f'Ran {earlier} tests in 0.1s\n\nOK\nRan {terminal} tests in 0.2s\n\nOK\n')
                self.metadata['focused']['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
                self.checks.write_text(json.dumps(self.metadata))
                if terminal==20:
                    self.assertEqual(self.references()['logs']['focused']['tests'],20)
                else:
                    with self.assertRaisesRegex(RuntimeError,'test evidence'):self.references()

    def test_all_selected_suites_are_required(self):
        self.assertEqual(set(self.references()['logs']),set(self.metadata))
        for logs in ({k:v for k,v in self.logs.items() if k!='runtime'},
                     {},dict(self.logs,unexpected=self.logs['focused'])):
            with self.subTest(suites=sorted(logs)),self.assertRaisesRegex(RuntimeError,'suite references'):
                self.references(logs=logs)

    def test_current_verifier_path_is_bound_and_historical_digest_only_is_preserved(self):
        copy=self.root/'identical-copy.py';copy.write_bytes(self.verifier.read_bytes())
        self.assertEqual(hashlib.sha256(copy.read_bytes()).hexdigest(),self.summary_value['verifier_sha256'])
        self.assertEqual(self.references()['verifier_path'],str(self.verifier))
        with self.assertRaisesRegex(RuntimeError,'verifier evidence path'):
            self.references(verifier=copy)
        del self.summary_value['verifier_path']
        self.summary.write_text(json.dumps(self.summary_value))
        self.assertEqual(self.references(verifier=copy)['verifier_path'],str(copy))
        copy.write_bytes(b'# wrong historical verifier\n')
        with self.assertRaisesRegex(RuntimeError,'verifier evidence differs'):
            self.references(verifier=copy)


if __name__=='__main__':unittest.main()
