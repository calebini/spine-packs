"""AL-3 qualification admission and parent-owned evidence correlation; no ledgers."""
from copy import deepcopy
import hashlib
import importlib.util
import json
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


if __name__=='__main__':unittest.main()
