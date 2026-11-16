"""Private qualification evidence gates; stdlib only, never installer runtime."""
import unittest

SCENARIO_IDS = {
    'v1': tuple('__main__.LocalSpineTests.' + name for name in (
        'test_existing_output_and_ledger_input_are_refused',
        'test_install_retain_granular_drift_and_verify',
        'test_lost_response_recovers_each_write_kind',
        'test_partial_before_submission_continues_from_result',
    )),
    'v2': tuple('__main__.FacetSpineTests.' + name for name in (
        'test_create_retain_complete_checkpoint_and_read_only_verify',
        'test_update_cascade_binding_drift_and_approval',
        'test_each_write_response_loss_replays_exact_request_and_ids',
        'test_prepared_before_submission_and_no_clobber',
    )),
}


class QualificationResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successful_scenarios = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successful_scenarios.append(test.id())


def completion_report(result, required, *, focused=False):
    required = list(required)
    succeeded = result.successful_scenarios
    clean = result.wasSuccessful() and not result.skipped and result.testsRun > 0
    complete = (not focused and clean and len(required) == 4
                and len(set(required)) == 4 and result.testsRun == 4
                and len(succeeded) == 4 and sorted(succeeded) == sorted(required))
    return dict(passed=bool(clean if focused else complete), full_qualification=bool(complete),
                focused=focused, required_scenarios=required, successful_scenarios=succeeded,
                tests=result.testsRun, skipped=len(result.skipped),
                failures=len(result.failures), errors=len(result.errors))


def require_full_qualification(report, *, harness):
    """Bind completion to the caller-selected suite, never child-supplied IDs."""
    if harness not in SCENARIO_IDS:
        raise RuntimeError('unknown qualification harness')
    expected = SCENARIO_IDS[harness]
    required = report.get('required_scenarios', [])
    succeeded = report.get('successful_scenarios', [])
    if not (report.get('passed') is True and report.get('full_qualification') is True
            and report.get('focused') is False and report.get('tests') == 4
            and report.get('skipped') == 0 and report.get('failures') == 0 and report.get('errors') == 0
            and isinstance(required, list) and isinstance(succeeded, list)
            and all(isinstance(v, str) for v in required + succeeded)
            and len(required) == len(succeeded) == len(set(required)) == 4
            and sorted(required) == sorted(succeeded) == sorted(expected)):
        raise RuntimeError('full qualification requires all four named scenarios for the requested harness without skips')

# Expected identities are qualification tooling, not runtime compatibility policy.
V1_BASELINES = {
    '0.3.0': dict(runtime='0.3.0', schema='12', commit='72203f092de191a7633b1884bf0d61836a25abe4'),
    '0.5.0': dict(runtime='0.5.0', schema='15', commit='ab18a8a51c9bf548220f67e2db0220bfe9783888'),
    '0.6.0': dict(runtime='0.6.0', schema='15', commit='ad1db8e1a4c7aa9a525612324d08824802a86351'),
}


def installed_package_root(prefix):
    """Obtain the exact wheel location from the parent-selected clean interpreter."""
    import json
    import subprocess
    from pathlib import Path
    prefix = prefix.resolve()
    python = prefix/'bin/python'
    info = json.loads(subprocess.check_output([str(python), '-I', '-c',
        'import json,sys,sysconfig; print(json.dumps(dict(executable=sys.executable, prefix=sys.prefix, purelib=sysconfig.get_path("purelib"))))'],
        text=True))
    purelib = Path(info['purelib']).resolve()
    if not (Path(info['executable']).absolute() == python.absolute()
            and Path(info['prefix']).resolve() == prefix and purelib.is_relative_to(prefix)):
        raise RuntimeError('selected installer interpreter/purelib mismatch')
    return purelib/'spine_packs'


def require_installation_identity(record, *, baseline, installed, bin_dir, source_root, installer_prefix=None):
    from pathlib import Path
    def require(ok, message):
        if not ok:
            raise RuntimeError(message)
    require(record.get('baseline') == baseline and record.get('installed') is installed,
            'integration baseline/mode mismatch')
    require(record.get('spine_command') == str(bin_dir/'spine-command')
            and record.get('spine_ledger_migrate') == str(bin_dir/'spine-ledger-migrate'),
            'integration upstream path mismatch')
    require(isinstance(record.get('module'), str) and isinstance(record.get('schemas'), str),
            'missing integration module/resources')
    module, schemas = Path(record['module']).resolve(), Path(record['schemas']).resolve()
    if installed:
        require(installer_prefix is not None, 'missing selected installer prefix')
        expected_root = installed_package_root(installer_prefix)
        require(module.is_relative_to(installer_prefix.resolve()) and schemas.is_relative_to(installer_prefix.resolve())
                and module == expected_root/'artifacts.py'
                and schemas == expected_root/'_schemas', 'installed integration source/resource leak')
    else:
        require(module == (source_root/'src/spine_packs/artifacts.py').resolve()
                and schemas == (source_root/'contracts/schemas').resolve(), 'source integration identity mismatch')


def require_run_identity(record, *, expected_installer, **selection):
    require_installation_identity(record, **selection)
    if record.get('installer') != expected_installer:
        raise RuntimeError('integration installer command mismatch')


def require_environment(info, baseline):
    if not (info.get('runtime_version') == baseline['runtime']
            and info.get('ledger_schema_version') == baseline['schema']
            and info.get('implemented_ledger_schema_version') == baseline['schema']):
        raise RuntimeError('selected qualification runtime/schema mismatch')


def attest_console_scripts(project_bytes, wheel, bin_dir, installed):
    """Check pinned export -> wheel metadata -> installed metadata -> actual dispatch.

    Deliberately accepts the recorded pip Python-launcher form only. Unknown
    launcher forms fail closed rather than guessing their dispatch semantics.
    """
    import ast
    import configparser
    import hashlib
    import os
    import re
    import tomllib
    import zipfile
    def require(ok, message):
        if not ok:
            raise RuntimeError(message)
    scripts = tomllib.loads(project_bytes.decode())['project']['scripts']
    names = ('spine-command', 'spine-ledger-migrate')
    with zipfile.ZipFile(wheel) as archive:
        entries = [n for n in archive.namelist() if n.endswith('.dist-info/entry_points.txt')]
        require(len(entries) == 1, 'ambiguous console entry-point metadata')
        metadata = archive.read(entries[0])
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(metadata.decode())
    require('console_scripts' in parser, 'missing console entry points')
    metadata_path = installed/entries[0]
    require(metadata_path.read_bytes() == metadata, 'installed console metadata differs from wheel')
    python = bin_dir/'python'
    proof = dict(interpreter_path=str(python), interpreter_resolved=str(python.resolve()),
                 interpreter_sha256=hashlib.sha256(python.read_bytes()).hexdigest(),
                 metadata_path=str(metadata_path), metadata_sha256=hashlib.sha256(metadata).hexdigest(),
                 scripts={})
    for name in names:
        target = scripts[name]
        require(parser['console_scripts'].get(name) == target, 'console mapping differs from pinned source')
        require(re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*:[A-Za-z_]\w*', target) is not None,
                'unsupported console entry-point mapping')
        module, function = target.split(':')
        path = bin_dir/name
        require(not path.is_symlink() and path.is_file() and os.access(path, os.X_OK),
                'console launcher must be a regular executable')
        data = path.read_bytes()
        lines = data.decode().splitlines()
        require(lines and lines[0] == '#!'+str(python), 'console launcher interpreter mismatch')
        expected = ("import sys\nfrom "+module+" import "+function+"\n"
                    "if __name__ == '__main__':\n"
                    "    sys.argv[0] = sys.argv[0].removesuffix('.exe')\n"
                    "    sys.exit("+function+"())\n")
        require(ast.dump(ast.parse('\n'.join(lines[1:]))) == ast.dump(ast.parse(expected)),
                'console launcher dispatch mismatch')
        proof['scripts'][name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), entry_point=target)
    return proof


def verify_console_scripts(proof, bin_dir):
    """Recheck the attested interpreter/metadata/launchers without invoking Spine."""
    import hashlib
    import os
    from pathlib import Path
    def require(ok):
        if not ok:
            raise RuntimeError('attested console installation changed')
    python = bin_dir/'python'
    require(proof['interpreter_path'] == str(python)
            and proof['interpreter_resolved'] == str(python.resolve())
            and proof['interpreter_sha256'] == hashlib.sha256(python.read_bytes()).hexdigest())
    require(hashlib.sha256(Path(proof['metadata_path']).read_bytes()).hexdigest() == proof['metadata_sha256'])
    require(set(proof['scripts']) == {'spine-command', 'spine-ledger-migrate'})
    for name, record in proof['scripts'].items():
        path = bin_dir/name
        require(record['path'] == str(path) and not path.is_symlink()
                and path.is_file() and os.access(path, os.X_OK)
                and hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'])


def require_evidence_references(summary_path, checks_path, verifier_path, log_paths):
    """Bind outgoing verifier/log source files to their current result metadata."""
    import hashlib
    import json
    import re
    from pathlib import Path
    summary = json.loads(summary_path.read_text())
    checks = json.loads(checks_path.read_text())
    if ('verifier_path' in summary
            and verifier_path.resolve() != Path(summary['verifier_path']).resolve()):
        raise RuntimeError('verifier evidence path differs from qualification summary')
    verifier = verifier_path.read_bytes()
    if hashlib.sha256(verifier).hexdigest() != summary['verifier_sha256']:
        raise RuntimeError('verifier evidence differs from qualification summary')
    if set(log_paths) != set(checks):
        raise RuntimeError('test evidence suite references differ from current checks')
    verified = {}
    for name, path in log_paths.items():
        record = checks[name]
        data = path.read_bytes()
        terminal = re.search(
            rb'(?:\A|\n)Ran ([0-9]+) tests? in [^\r\n]+\r?\n[ \t]*\r?\nOK\Z',
            data.rstrip())
        if (path.resolve() != Path(record['log']).resolve()
                or hashlib.sha256(data).hexdigest() != record['sha256']
                or terminal is None or int(terminal.group(1)) != record['tests']):
            raise RuntimeError('test evidence differs from current checks: '+name)
        verified[name] = dict(path=str(path), tests=record['tests'], sha256=record['sha256'])
    return dict(verifier_path=str(verifier_path), verifier_sha256=summary['verifier_sha256'],
                checks_path=str(checks_path), logs=verified)
