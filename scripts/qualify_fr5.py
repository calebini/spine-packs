"""Qualify FR-5 locally using exact Git exports and disposable public CLIs.

No existing-ledger option, checkout mutation, network install, or publication.
Provision build/hatchling/setuptools/wheel in the invoking isolated Python first.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests/integration'))
from qualification_support import (require_full_qualification, require_run_identity, require_installation_identity, V1_BASELINES,
    attest_console_scripts, verify_console_scripts)
SPINE_PINS = {
    '0.3.0': '72203f092de191a7633b1884bf0d61836a25abe4',
    '0.5.0': 'ab18a8a51c9bf548220f67e2db0220bfe9783888',
    '0.6.0': 'ad1db8e1a4c7aa9a525612324d08824802a86351',
    '0.10.0': '8f3c50b6fd1b4aa534e50925b7417a7a80d19122',
}
TICKERD_PIN = 'ffe613c65ea3d6fc70a1dc3603c32068f06350df'
SUCCESSOR_PINS = {
    '0.10.0': dict(commit=SPINE_PINS['0.10.0'], schema='19'),
    '0.12.0': dict(commit='3e65ef0de9e73b62047a0f6328731db08ca91023', schema='20'),
}
READ_GATE_CHECKS = frozenset(('all_missing_read_only_plan', 'A2_B2_B1_actual_root_and_immutable_history',
    'repeated_pins_deduplicated_per_pass', 'mixed_v1_v2_complete_pagination', 'two_pass_page_independent_plan',
    'unchanged_ledger_file_metadata', 'current_historical_retired_public_reads', 'missing_revision_exit4', 'invalid_request_exit2'))


def require(value, message):
    if not value:
        raise RuntimeError(message)


def save(path, value):
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as out:
        json.dump(value, out, indent=2, sort_keys=True)
        out.write('\n')


def pinned_git(repo, *args):
    return ['git', '--no-replace-objects', '-C', str(repo), *args]


def exact_commit(repo, pin):
    actual = subprocess.check_output(pinned_git(repo, 'rev-parse', pin + '^{commit}'), text=True).strip()
    require(actual == pin, 'exact source commit unavailable')


def selected_pins(runtime):
    require(runtime in SUCCESSOR_PINS, 'unsupported qualification baseline')
    return dict(SPINE_PINS, **{runtime: SUCCESSOR_PINS[runtime]['commit']})


def source_snapshot():
    paths = [*ROOT.glob('src/spine_packs/*.py'), *ROOT.glob('contracts/schemas/*.schema.json'), *ROOT.glob('contracts/*.json'),
             *ROOT.glob('tests/integration/*.py'), ROOT/'tests/fixtures/pack-manifest-v2/flight.json',
             ROOT/'tests/fixtures/pack-manifest/positive/medical_and_lesson.json',
             ROOT/'tests/fixtures/installer-v2/flight-create.json']
    paths += [ROOT/p for p in ('pyproject.toml', 'README.md', 'LICENSE', '.gitignore',
        'docs/releases.md', 'docs/local-qualification.md', 'docs/spine-0.6.0-qualification.md',
        'scripts/qualify_fr2.py', 'scripts/qualify_fr5.py', 'scripts/qualify_package.py')]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def require_identity(record, *, runtime, installed, bin_dir, installer_prefix=None):
    require(not installed or installer_prefix is not None, 'missing selected installer prefix')
    expected = (V1_BASELINES[runtime] if runtime in V1_BASELINES else
        dict(commit=SUCCESSOR_PINS[runtime]['commit'], runtime=runtime, schema=SUCCESSOR_PINS[runtime]['schema']))
    require_run_identity(record, baseline=expected, installed=installed, bin_dir=bin_dir,
                         source_root=ROOT, installer_prefix=installer_prefix,
                         expected_installer=([str(installer_prefix/'bin/spine-packs')] if installed
                                             else [sys.executable, '-m', 'spine_packs']))


def require_replay_coverage(run, runtime):
    inventory = json.loads((ROOT/('contracts/installer-spine-'+runtime+'-inventory.json')).read_text())
    expected = {name for name, value in inventory['commands'].items() if value['phase'] is not None}
    paths = list(run.rglob('covered-writes.json'))
    require(len(paths) == 1 and len(expected) == 11, 'missing or ambiguous replay coverage')
    covered = json.loads(paths[0].read_text())
    require(isinstance(covered, list) and len(covered) == 11 and all(isinstance(x, str) for x in covered)
            and len(set(covered)) == 11 and set(covered) == expected, 'incomplete replay coverage')


def require_read_gate(record, *, runtime, installed, bin_dir, wheel, installer_prefix=None):
    proof = record.get('provenance', {})
    require(record.get('status') == 'passed' and set(record.get('checks', [])) == READ_GATE_CHECKS
            and len(record['checks']) == len(READ_GATE_CHECKS), 'incomplete read-only qualification')
    require(proof.get('commit') == SUCCESSOR_PINS[runtime]['commit'] and proof.get('runtime') == runtime
            and proof.get('schema') == SUCCESSOR_PINS[runtime]['schema']
            and proof.get('wheel_sha256') == hashlib.sha256(wheel.read_bytes()).hexdigest(), 'read gate provenance mismatch')
    require_installation_identity(dict(baseline=dict(commit=proof['commit'],runtime=proof['runtime'],schema=proof['schema']),
        installed=record.get('installed_installer'), spine_command=record.get('spine_command'),
        spine_ledger_migrate=record.get('spine_ledger_migrate'), module=record.get('installer_module'),
        schemas=record.get('installer_schemas')),
        baseline=dict(commit=SUCCESSOR_PINS[runtime]['commit'],runtime=runtime,schema=SUCCESSOR_PINS[runtime]['schema']),
        installed=installed, bin_dir=bin_dir, source_root=ROOT, installer_prefix=installer_prefix)


def attest(repo, pin, export, wheel, bin_dir, package):
    """Compare every packaged file with Git, export and installed bytes.

    Also require the complete source Python closure; a thin/substituted wheel
    cannot pass by containing only a subset of the correct source files.
    """
    exact_commit(repo, pin)
    env = dict(PATH=str(bin_dir) + ':/usr/bin:/bin', PYTHONNOUSERSITE='1')
    installed = Path(subprocess.check_output([str(bin_dir / 'python'), '-I', '-c',
        'import sysconfig; print(sysconfig.get_paths()["purelib"])'], text=True, env=env).strip())
    tracked = subprocess.check_output(pinned_git(repo, 'ls-tree', '-r', '--name-only', pin,
                                      '--', 'src/' + package), text=True).splitlines()
    python_names = {n.removeprefix('src/') for n in tracked if n.endswith('.py')}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'duplicate upstream wheel members')
        members = {n for n in names if n.startswith(package + '/') and not n.endswith('/')}
        require({n for n in members if n.endswith('.py')} == python_names,
                'upstream wheel Python closure differs from exact commit')
        for name in sorted(members):
            exact = subprocess.check_output(pinned_git(repo, 'show', pin + ':src/' + name))
            require(exact == (export / 'src' / name).read_bytes() == archive.read(name)
                    == (installed / name).read_bytes(), 'upstream package provenance mismatch: ' + name)
        installed_names = {str(p.relative_to(installed)) for p in (installed / package).rglob('*')
                           if p.is_file() and '__pycache__' not in p.parts}
        require(installed_names == members, 'unexpected installed upstream package files')
    proof = dict(commit=pin, package_files=len(members), python_files=len(python_names),
                wheel=str(wheel), wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),
                installed_root=str(installed / package))
    if package == 'spine':
        project = subprocess.check_output(pinned_git(repo, 'show', pin+':pyproject.toml'))
        require(project == (export/'pyproject.toml').read_bytes(), 'upstream project metadata differs from pin')
        proof['console_scripts'] = attest_console_scripts(project, wheel, bin_dir, installed)
    return proof


def qualify(args, run):
    # Deliberately do not inherit operator Spine configuration, credentials or
    # PYTHONPATH. All test cursor/owner configuration is generated by the harness.
    env = dict(PATH=str(Path(sys.executable).parent) + ':/usr/bin:/bin',
               PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1',
               SOURCE_DATE_EPOCH='315532800', LC_ALL='C')
    selected = getattr(args, 'successor_runtime', '0.10.0')
    spine_pins = selected_pins(selected)
    snapshot = source_snapshot()
    save(run/'source-identity.json', snapshot)
    dependencies = []
    if selected == '0.12.0':
        wheelhouse = getattr(args, 'dependency_wheels', None)
        require(wheelhouse is not None and wheelhouse.is_dir(), '0.12.0 requires a preprovisioned dependency wheelhouse')
        folder = run/'dependency-wheels'; folder.mkdir(mode=0o700)
        for source in sorted(wheelhouse.glob('*.whl')):
            target = folder/source.name; shutil.copyfile(source,target); dependencies.append(target)
        require(bool(dependencies), 'empty dependency wheelhouse')
        save(run/'dependency-wheels.json', {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies})
    for pin in spine_pins.values():
        exact_commit(args.spine_repo, pin)
    exact_commit(args.tickerd_repo, TICKERD_PIN)
    save(run / 'environment.json', dict(python=sys.version, platform=platform.platform(),
        tools={p: importlib.metadata.version(p) for p in ('build', 'hatchling', 'setuptools', 'wheel')},
        source=str(ROOT), source_commit=subprocess.check_output(pinned_git(ROOT, 'rev-parse', 'HEAD'), text=True).strip(),
        qualification='working-tree-local-candidate-not-release', successor_runtime=selected,
        spine_pins=spine_pins, tickerd_pin=TICKERD_PIN))

    def command(label, argv, cwd=run, timeout=1800):
        log = run / (label + '.log')
        print(f'{label}: {log}', flush=True)
        save(run / (label + '-command.json'), dict(argv=[str(x) for x in argv], cwd=str(cwd)))
        with log.open('x') as out:
            result = subprocess.run([str(x) for x in argv], cwd=cwd, env=env,
                                    stdout=out, stderr=subprocess.STDOUT, timeout=timeout)
        require(result.returncode == 0, f'{label} failed; inspect {log}')

    def build(repo, pin, label):
        folder = run / label
        folder.mkdir(mode=0o700)
        archive = folder / 'exact-source.tar'
        command(label + '-export', pinned_git(repo, 'archive', '--format=tar', '--output', archive, pin))
        export = folder / 'source'
        export.mkdir(mode=0o700)
        with tarfile.open(archive) as tar:
            require(all(m.isfile() or m.isdir() for m in tar.getmembers()), 'source archive links forbidden')
            tar.extractall(export, filter='data')
        command(label + '-build', [sys.executable, '-m', 'build', '--no-isolation', '--wheel',
                                  '--outdir', folder / 'wheels', export])
        wheels = list((folder / 'wheels').glob('*.whl'))
        require(len(wheels) == 1, 'expected one exact upstream wheel')
        return export, wheels[0]

    tick_export, tick_wheel = build(args.tickerd_repo, TICKERD_PIN, 'tickerd')
    installs = {}
    for version, pin in spine_pins.items():
        label = 'spine-' + version
        export, wheel = build(args.spine_repo, pin, label)
        prefix = run / label / 'installed'
        command(label + '-venv', [sys.executable, '-m', 'venv', prefix])
        bin_dir = prefix / 'bin'
        command(label + '-install', [bin_dir / 'python', '-m', 'pip', 'install', '--no-index', '--no-deps',
                                    *(dependencies if version == '0.12.0' else ()), tick_wheel, wheel])
        command(label + '-pip-check', [bin_dir / 'python', '-m', 'pip', 'check'])
        proof = dict(spine=attest(args.spine_repo, pin, export, wheel, bin_dir, 'spine'),
                     tickerd=attest(args.tickerd_repo, TICKERD_PIN, tick_export, tick_wheel, bin_dir, 'tickerd'))
        save(run / label / 'provenance.json', proof)
        command(label + '-dependencies', [bin_dir/'python', '-I', '-c',
            'import importlib.metadata as m,json; print(json.dumps({d.metadata["Name"]:d.version for d in m.distributions()},sort_keys=True))'])
        installs[version] = dict(bin=bin_dir, export=export, wheel=wheel, proof=proof['spine'])

    integration_results = {}
    def integration(label, argv, *, harness, runtime=None, installed=False, installer_prefix=None):
        require(runtime is not None, 'parent-selected runtime required')
        verify_console_scripts(installs[runtime]['proof']['console_scripts'], installs[runtime]['bin'])
        parent = run / label
        parent.mkdir(mode=0o700)
        command(label, [*argv, '--evidence-parent', parent], timeout=3600)
        runs = list(parent.glob('spine-packs-*integration-*'))
        require(len(runs) == 1, 'expected one integration result: ' + label)
        result_path = runs[0] / 'result.json'
        require_full_qualification(json.loads(result_path.read_text()), harness=harness)
        require_identity(json.loads((runs[0]/'run.json').read_text()), runtime=runtime, installed=installed,
                         bin_dir=installs[runtime]['bin'], installer_prefix=installer_prefix)
        if harness == 'v2':
            require_replay_coverage(runs[0], runtime)
        integration_results[label] = str(result_path)

    successors = ['0.10.0'] if selected == '0.10.0' else ['0.10.0','0.12.0']
    def read_gate(label, python, runtime, *, installed=False, installer_prefix=None):
        current = installs[runtime]; parent=run/label; parent.mkdir(mode=0o700)
        verify_console_scripts(current['proof']['console_scripts'], current['bin'])
        command(label, [python, '-I', ROOT/'scripts/qualify_fr2.py',
            *(['--installed-installer'] if installed else []), '--runtime-version',runtime,
            '--bin-dir',current['bin'],'--export',current['export'],'--spine-repo',args.spine_repo,
            '--wheel',current['wheel'],'--evidence-parent',parent])
        gates=list(parent.glob('spine-packs-fr2-gate-*')); require(len(gates)==1,'missing read-only gate')
        report=gates[0]/'PASS.json'
        require_read_gate(json.loads(report.read_text()),runtime=runtime,installed=installed,
                          bin_dir=current['bin'],wheel=current['wheel'],installer_prefix=installer_prefix)
        integration_results[label]=str(report)
    for runtime in successors:
        read_gate('source-fr2-'+runtime,sys.executable,runtime)
        current_bin=installs[runtime]['bin']
        integration('source-v2-'+runtime,[sys.executable,ROOT/'tests/integration/test_facet_spine.py',
            '--runtime-version',runtime,'--spine-command',current_bin/'spine-command',
            '--spine-ledger-migrate',current_bin/'spine-ledger-migrate'],harness='v2',runtime=runtime)
    package_runs = []
    for version in ('0.3.0', '0.5.0', '0.6.0'):
        bin_dir = installs[version]['bin']
        options = ['--runtime-version', version, '--spine-command', bin_dir / 'spine-command', '--spine-ledger-migrate', bin_dir / 'spine-ledger-migrate']
        integration('source-v1-' + version, [sys.executable, ROOT / 'tests/integration/test_local_spine.py', *options], harness='v1', runtime=version)
        before = set(run.glob('spine-packs-package-*'))
        verify_console_scripts(installs[version]['proof']['console_scripts'], bin_dir)
        command('package-v1-' + version, [sys.executable, ROOT / 'scripts/qualify_package.py', *options, '--evidence-parent', run])
        added = set(run.glob('spine-packs-package-*')) - before
        require(len(added) == 1, 'expected one package qualification run')
        package_run = added.pop()
        require((package_run / 'PASS.json').is_file(), 'package gate incomplete')
        package_proof = json.loads((package_run / 'PASS.json').read_text())
        result_path = Path(package_proof['integration_result'])
        require(package_proof['passed'] is True, 'package qualification failed')
        require_full_qualification(json.loads(result_path.read_text()), harness='v1')
        require(result_path.parent.parent == package_run and result_path.parent.name.startswith('spine-packs-integration-'),
                'installed v1 report outside current package run')
        require_identity(json.loads((result_path.parent/'run.json').read_text()), runtime=version,
                         installed=True, bin_dir=bin_dir, installer_prefix=package_run/'installed')
        integration_results['installed-v1-' + version] = str(result_path)
        package_runs.append(package_run)

    # Same local candidate, same fixed timestamps and recorded tools for all
    # supported v1 baselines. No per-baseline rebuild substitution is allowed.
    version = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['version']
    asset_names = [f'spine_packs-{version}-py3-none-any.whl', f'spine_packs-{version}.tar.gz', 'SHA256SUMS']
    for name in asset_names:
        require(len({(p / 'assets' / name).read_bytes() for p in package_runs}) == 1,
                'candidate bytes differ across baseline matrix: ' + name)
    package_run = package_runs[0]
    installed_python = package_run / 'installed/bin/python'
    sdist_root = package_run / 'sdist' / f'spine_packs-{version}'
    for runtime in successors:
        current_bin=installs[runtime]['bin']
        integration('installed-v2-'+runtime,[installed_python,'-I',sdist_root/'tests/integration/test_facet_spine.py',
            '--installed','--runtime-version',runtime,'--spine-command',current_bin/'spine-command',
            '--spine-ledger-migrate',current_bin/'spine-ledger-migrate'],harness='v2',runtime=runtime,
            installed=True,installer_prefix=package_run/'installed')
        read_gate('installed-fr2-'+runtime,installed_python,runtime,installed=True,installer_prefix=package_run/'installed')
    require(source_snapshot()==snapshot,'qualification source/harness inputs changed during matrix')
    for current in installs.values():
        verify_console_scripts(current['proof']['console_scripts'], current['bin'])
    save(run / 'PASS.json', dict(passed=True, qualification='working-tree-local-candidate-not-release',
        package_runs=[str(p) for p in package_runs], integration_results=integration_results,
        assets={n:hashlib.sha256((package_run / 'assets' / n).read_bytes()).hexdigest()
        for n in asset_names}, successor_runtime=selected, source_identity='source-identity.json',
        gates=list(integration_results)))
    print(f'FR-5 passed locally; nothing published. Evidence: {run}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spine-repo', required=True, type=Path)
    parser.add_argument('--tickerd-repo', required=True, type=Path)
    parser.add_argument('--evidence-parent', type=Path, default=Path(tempfile.gettempdir()))
    parser.add_argument('--successor-runtime', choices=tuple(SUCCESSOR_PINS), default='0.10.0')
    parser.add_argument('--dependency-wheels', type=Path,
                        help='Preprovisioned jsonschema closure, required for exact 0.12.0; no downloads during qualification')
    args = parser.parse_args()
    if sys.version_info < (3, 12) or sys.prefix == sys.base_prefix:
        parser.error('use an isolated Python 3.12+ build environment')
    run = Path(tempfile.mkdtemp(prefix='spine-packs-fr5-', dir=args.evidence_parent)).resolve()
    print(f'Private FR-5 qualification evidence: {run}', flush=True)
    try:
        qualify(args, run)
    except Exception as error:
        print(f'FR-5 failed: {error}. Evidence retained: {run}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
