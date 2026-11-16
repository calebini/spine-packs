"""FR-2 public-CLI gate. Creates only a new disposable configuration ledger.

Requires an exact isolated source export and installed wheel. No existing-ledger
argument, SQL, internal Spine imports, items, facet values, disclosure or sends.
Synthetic setup writes are test tooling, never successor installer apply.
"""
from copy import deepcopy
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests/integration'))
from qualification_support import attest_console_scripts, verify_console_scripts
if '--installed-installer' not in sys.argv:
    sys.path.insert(0, str(ROOT / 'src'))
from spine_packs import artifacts as a
from spine_packs.facet_contracts import seal, body
from spine_packs.facet_inventory import COMMANDS, READ_COMMANDS
from spine_packs.facet_baselines import BASELINES, DEFAULT_RUNTIME, runtime_baseline
from spine_packs.facet_manifest import digest as manifest_digest
from spine_packs.facet_planning import plan_installation
from spine_packs.facet_transport import FacetSpineCommand


def require(value, message):
    if not value:
        raise RuntimeError(message)


def pinned_git(repo, *args):
    return ['git', '--no-replace-objects', '-C', str(repo), *args]


class LimitCheckedFacetCommand(FacetSpineCommand):
    """Enforce plan(limit) on every profile-list read, before transport/capture."""
    def __init__(self, *args, expected_profile_limit, **kwargs):
        super().__init__(*args, **kwargs)
        require(type(expected_profile_limit) is int and expected_profile_limit > 0,
                'invalid expected profile limit')
        self.expected_profile_limit = expected_profile_limit

    def read(self, command, value):
        if command == 'notification_profile.list':
            require(value.get('limit') == str(self.expected_profile_limit),
                    'profile page limit differs from selected plan limit')
        return super().read(command, value)


def require_profile_pagination(reads, expected, *, limit):
    """Both observation passes must finish a stable chain and contain each seed."""
    rows = [row for row in reads if row['command'] == 'notification_profile.list']
    require(type(limit) is int and limit > 0, 'invalid expected profile limit')
    cursor, observed, starts, completed = None, {}, 0, 0
    snapshot, query = None, None
    used_cursors = set()
    page_counts, pages = [], 0
    for row in rows:
        request, response = row['request'], row['response']
        require(request.get('limit') == str(limit), 'profile page limit differs from selected limit')
        require(request.get('cursor') == cursor, 'profile page cursor chain mismatch')
        if cursor is None:
            starts += 1
            require(starts <= 2 and not observed, 'unexpected profile observation pass')
            snapshot = response['catalog_snapshot_hash']
            query = {k:v for k,v in request.items() if k != 'cursor'}
            used_cursors = set()
            pages = 0
        require(response['catalog_snapshot_hash'] == snapshot
                and {k:v for k,v in request.items() if k != 'cursor'} == query, 'profile page query/snapshot changed')
        entries = response['entries']
        require(response['count'] == str(len(entries)) and len(entries) <= int(request['limit']),
                'profile page count mismatch')
        for entry in entries:
            key = entry['profile_key']
            require(key not in observed, 'duplicate profile identity in pagination')
            observed[key] = (entry['notification_profile_id'], entry['current_revision_id'],
                             entry['revision']['revision_contract'])
        pages += 1
        require(type(response['has_more']) is bool, 'invalid profile continuation')
        cursor = response['next_cursor']
        if response['has_more']:
            require(isinstance(cursor, str) and cursor and cursor not in used_cursors, 'missing/repeated profile cursor')
            used_cursors.add(cursor)
        else:
            require(cursor is None and observed == expected, 'incomplete seeded profile catalog')
            completed += 1
            page_counts.append(pages)
            observed = {}
    require(starts == completed == 2 and cursor is None, 'incomplete profile observation passes')
    return dict(passes=completed, pages=page_counts, profile_keys=sorted(expected))




def provenance(repo, export, wheel, bin_dir, runtime_version=DEFAULT_RUNTIME):
    baseline = runtime_baseline(runtime_version)
    pin = baseline.commit
    require(subprocess.check_output(pinned_git(repo, 'rev-parse', pin + '^{commit}'), text=True).strip() == pin,
            'exact commit unavailable')
    installed = Path(subprocess.check_output([str(bin_dir / 'python'), '-I', '-c',
        'import sysconfig; print(sysconfig.get_paths()["purelib"])'], text=True).strip())
    count = 0
    tracked = subprocess.check_output(pinned_git(repo, 'ls-tree', '-r', '--name-only', pin,
                                      '--', 'src/spine'), text=True).splitlines()
    expected_python = {name.removeprefix('src/') for name in tracked if name.endswith('.py')}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'duplicate Spine wheel members')
        members = {name for name in names if name.startswith('spine/') and not name.endswith('/')}
        require({name for name in members if name.endswith('.py')} == expected_python,
                'Spine wheel Python closure mismatch')
        for name in archive.namelist():
            if not name.startswith('spine/') or name.endswith('/'):
                continue
            exact = subprocess.check_output(pinned_git(repo, 'show', pin + ':src/' + name))
            require(archive.read(name) == exact == (export / 'src' / name).read_bytes()
                    == (installed / name).read_bytes(), 'package source/installed provenance mismatch')
            count += 1
    require(count > 299, 'incomplete Spine wheel')
    installed_names = {str(p.relative_to(installed)) for p in (installed / 'spine').rglob('*')
                       if p.is_file() and '__pycache__' not in p.parts}
    require(installed_names == members, 'unexpected installed Spine files')
    inventory = json.loads((ROOT / ('contracts/installer-spine-' + baseline.runtime + '-inventory.json')).read_text())
    authorities = dict(inventory['revision_readback_authority_sha256'])
    authorities.update({k.removeprefix('upstream/'): v for k, v in inventory['source_sha256'].items()
                        if k.startswith('upstream/')})
    for name, digest in authorities.items():
        exact = subprocess.check_output(pinned_git(repo, 'show', pin + ':' + name))
        require(exact == (export / name).read_bytes() and hashlib.sha256(exact).hexdigest() == digest,
                'contract/source inventory provenance mismatch')
    project = subprocess.check_output(pinned_git(repo, 'show', pin+':pyproject.toml'))
    require(project == (export/'pyproject.toml').read_bytes(), 'pinned project metadata mismatch')
    return dict(commit=pin, runtime=baseline.runtime, schema=baseline.schema, package_files=count, authority_files=len(authorities),
                console_scripts=attest_console_scripts(project, wheel, bin_dir, installed),
                wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest())


def qualify(bin_dir, export, repo, wheel, *, runtime_version=DEFAULT_RUNTIME, evidence_parent=None):
    baseline = runtime_baseline(runtime_version)
    if '--installed-installer' in sys.argv:
        require((ROOT / 'src') not in Path(a.__file__).resolve().parents, 'source installer leaked into installed gate')
    proof = provenance(repo, export, wheel, bin_dir, runtime_version)
    run = Path(tempfile.mkdtemp(prefix='spine-packs-fr2-gate-', dir=evidence_parent)).resolve()
    ledger = run / 'new.sqlite'
    executable = (bin_dir / 'spine-command').resolve()
    env = {'PATH': str(bin_dir) + ':/usr/bin:/bin', 'PYTHONNOUSERSITE': '1',
           'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C'}
    transcript, reads, checks = [], [], []
    flow = json.loads((ROOT / 'tests/fixtures/installer-v2/flight-create.json').read_text())
    manifest, request = flow['manifest'], flow['request']
    manifest['compatibility']['spine_runtime_versions'] = [baseline.runtime]
    manifest['content_identity']['digest'] = manifest_digest(manifest)
    owner = request['request']['owner']
    setup = {'subject.upsert', 'item_archetype.create', 'facet_schema.create', 'facet_schema.publish',
             'facet_schema.retire', 'item_archetype.facet_binding.set', 'notification_rendering_definition.create',
             'notification_profile.create', 'notification_profile.binding.set'}

    def invoke(argv, value=None, expected=0):
        require(len(transcript) < 500, 'qualification call capacity')
        result = subprocess.run(argv, input=json.dumps(value) if value is not None else None, text=True,
            capture_output=True, cwd=run, env=env, timeout=30)
        response = json.loads(result.stdout)
        transcript.append(dict(command=argv[-1], request=value, response=response, exit_code=result.returncode))
        require(result.returncode == expected, f'public CLI failure: {response}')
        return response

    def cli(name, value, expected=0):
        require(name in setup | READ_COMMANDS, 'test command not allowed')
        return invoke([str(executable), '--db', str(ledger), '--input', '-', *name.split('.')], value, expected)

    def write(name, **fields):
        contract = COMMANDS[name]['selector'] if name in COMMANDS else 'spine.facet-schemas.v1'
        return cli(name, dict(contract_version=contract, command_id=f'fr2-setup-{len(transcript)}',
            actor_subject_id=owner['owner_subject_id'], action_timestamp_utc='2035-02-01T12:00:00Z', **fields))

    class Logged(LimitCheckedFacetCommand):
        def read(self, command, value):
            result = super().read(command, value)
            reads.append(dict(command=command, request=deepcopy(value), response=deepcopy(result)))
            return result

    def stat_ledger():
        # Metadata only, never open/hash the database or WAL.
        return {p.name: (p.stat().st_size, p.stat().st_mtime_ns) for p in run.glob('new.sqlite*')}

    try:
        require(not ledger.exists(), 'refusing existing ledger')
        invoke([str(bin_dir / 'spine-ledger-migrate'), '--db', str(ledger), '--initialize-if-empty'])
        info = cli('system.info', {})
        require(info['runtime_version'] == baseline.runtime
                and info['ledger_schema_version'] == info['implemented_ledger_schema_version'] == baseline.schema,
                'baseline mismatch')
        cli('subject.upsert', dict(command_id='fr2-owner', actor_subject_id=owner['owner_subject_id'],
            subject_id=owner['owner_subject_id'], subject_kind='person', display_name='Synthetic FR-2 owner',
            updated_at_utc='2035-02-01T12:00:00Z'))
        for key, value in {
            'SPINE_FACET_CURSOR_CONFIG': dict(secret_hex=secrets.token_hex(32), cursor_ledger_id='fr2-ledger', cursor_generation='fr2-generation'),
            'SPINE_RENDERING_CURSOR_CONFIG': dict(contract_version='spine.notification-rendering-cursor-config.v1',
                key_id='fr2-key', key_generation='fr2-generation', ledger_instance_id=info['ledger_instance_id'], secret_hex=secrets.token_hex(32)),
        }.items():
            path = run / (key + '.json')
            with path.open('x') as handle:
                os.chmod(path, 0o600)
                json.dump(value, handle)
            env[key] = str(path)
        request['request']['target'] = dict(host_name='fr2-test.invalid',
            spine_command=dict(path=str(executable), sha256=hashlib.sha256(executable.read_bytes()).hexdigest()),
            ledger=dict(kind='path', path=str(ledger)))
        request = seal(request)

        def plan(limit):
            before = stat_ledger()
            with patch.dict(os.environ, env, clear=True):
                adapter = Logged(request['request']['target'], expected_profile_limit=limit,
                                 host_resolver=lambda: 'fr2-test.invalid')
                result = plan_installation(manifest, request, adapter, page_size=limit)
            require(before == stat_ledger(), 'ledger file metadata changed during read-only planning')
            return result

        empty = plan(100)
        require(len(empty['actions']) == 6, 'missing graph not planned')
        checks.append('all_missing_read_only_plan')
        arch = write('item_archetype.create', owner=owner, archetype_key='flight', revision=manifest['archetypes'][0]['revision'])
        desired = manifest['facet_schemas'][0]['definition']
        older = dict(desired, display_name='Earlier details')
        root_a = write('facet_schema.create', owner=owner, schema_key='flight_details', definition=older)
        root_b = write('facet_schema.create', owner=owner, schema_key='legacy_details', definition=older)
        a2 = write('facet_schema.publish', facet_schema_id=root_a['facet_schema_id'],
            expected_current_revision_id=root_a['facet_schema_revision_id'], definition=desired)
        b2 = write('facet_schema.publish', facet_schema_id=root_b['facet_schema_id'],
            expected_current_revision_id=root_b['facet_schema_revision_id'], definition=desired)
        write('item_archetype.facet_binding.set', item_archetype_id=arch['item_archetype_id'], facet_key='flight',
              facet_schema_revision_id=root_b['facet_schema_revision_id'], expected_binding_id=None)
        revision = deepcopy(manifest['rendering_definitions'][0]['revision'])
        for selection in revision['selections']:
            del selection['schema_ref']
            selection['facet_schema_revision_id'] = root_b['facet_schema_revision_id']
        rendering = write('notification_rendering_definition.create', owner=owner, definition_key='flight_details', revision=revision)['record']
        profile = deepcopy(manifest['notification_profiles'][0])
        for template in profile['revision']['templates']:
            if template['rendering']['kind'] == 'definition':
                template['rendering'] = dict(kind='definition', definition={k: rendering[k] for k in (
                    'notification_rendering_definition_id', 'notification_rendering_definition_revision_id')})
        del profile['intended_status']
        created = write('notification_profile.create', owner=owner, **profile)
        expected_profiles = {created['profile_key']: (created['notification_profile_id'],
            created['notification_profile_revision_id'], 'spine.notification-profiles.v2')}
        write('notification_profile.binding.set', owner=owner, item_archetype_id=arch['item_archetype_id'],
              notification_profile_id=created['notification_profile_id'])
        for key, version in [('a_legacy', 'v1'), ('b_ordinary', 'v2')]:
            ordinary = deepcopy(profile['revision']); ordinary['templates'] = ordinary['templates'][:1]
            if version == 'v1': del ordinary['templates'][0]['rendering']
            payload = dict(contract_version='spine.notification-profiles.' + version, command_id='fr2-' + key,
                actor_subject_id=owner['owner_subject_id'], action_timestamp_utc='2035-02-01T12:00:00Z',
                owner=owner, profile_key=key, display_name=key, description=None, revision=ordinary)
            ordinary_created = cli('notification_profile.create', payload)
            expected_profiles[key] = (ordinary_created['notification_profile_id'],
                ordinary_created['notification_profile_revision_id'], 'spine.notification-profiles.'+version)
        reads.clear()
        first = plan(1)
        first_reads = deepcopy(reads)
        small_pages = require_profile_pagination(first_reads, expected_profiles, limit=1)
        reads.clear()
        second = plan(100)
        large_pages = require_profile_pagination(reads, expected_profiles, limit=100)
        reads[:0] = first_reads
        require(first == second, 'page boundaries changed plan')
        b1 = root_b['facet_schema_revision_id']
        exact = [r for r in first_reads if r['command'] == 'facet_schema.revision.show']
        require(len(exact) == 2 and all(r['request']['facet_schema_revision_id'] == b1 for r in exact),
                'repeated schema pins were not deduplicated per pass')
        history = first['observation']['historical_revisions']
        require(len(history) == 1 and history[0]['root_id'] == root_b['facet_schema_id']
                and history[0]['revision_id'] == b1 and body(history[0]['value']) == older, 'B1 evidence lost or misattributed')
        classified = {r['object_key']: r['classification'] for r in first['classifications']}
        require(classified['schema:flight_details'] == 'equivalent' and
                all(classified[k] == 'drifted' for k in ('facet_binding:flight:flight', 'rendering:flight_details',
                                                       'profile:synthetic_flight_details')), 'cross-root drift not cascaded')
        checks += ['A2_B2_B1_actual_root_and_immutable_history', 'repeated_pins_deduplicated_per_pass',
                   'mixed_v1_v2_complete_pagination', 'two_pass_page_independent_plan', 'unchanged_ledger_file_metadata']
        read_contract = dict(contract_version='spine.facet-schema-revision-readback.v1')
        for identity, root in [(a2['facet_schema_revision_id'], root_a), (b1, root_b)]:
            result = cli('facet_schema.revision.show', dict(read_contract, facet_schema_revision_id=identity))
            require(result['root']['facet_schema_id'] == root['facet_schema_id'] and
                    result['revision']['facet_schema_revision_id'] == identity, 'exact public read mismatch')
        write('facet_schema.retire', facet_schema_id=root_b['facet_schema_id'], expected_current_revision_id=b2['facet_schema_revision_id'])
        retired = plan(1)
        require(retired['observation']['historical_revisions'][0]['status'] == 'retired', 'retired history unreadable')
        missing = cli('facet_schema.revision.show', dict(read_contract, facet_schema_revision_id='missing-revision'), 4)
        require(missing['error']['code'] == 'referenced_row_not_found' and missing['error']['field'] == 'facet_schema_revision_id', 'wrong missing failure')
        cli('facet_schema.revision.show', read_contract, 2)
        checks += ['current_historical_retired_public_reads', 'missing_revision_exit4', 'invalid_request_exit2']
        (run / 'plan.json').write_text(json.dumps(first, indent=2) + '\n')
        (run / 'fixture.json').write_text(json.dumps(dict(manifest=manifest, request=request, reads=first_reads, plan=first), indent=2) + '\n')
        verify_console_scripts(proof['console_scripts'], bin_dir)
        report = dict(status='passed', provenance=proof, checks=checks, run_directory=str(run),
                    profile_pagination=dict(page_size_1=small_pages, page_size_100=large_pages),
                    installer_module=str(Path(a.__file__).resolve()),
                    installer_schemas=str(a.SCHEMA_ROOT.resolve()),
                    installed_installer='--installed-installer' in sys.argv,
                    spine_command=str(executable), spine_ledger_migrate=str((bin_dir / 'spine-ledger-migrate').resolve()),
                    setup_and_direct_read_calls=len(transcript), planner_read_calls=len(reads),
                    qualification='FR-2 read-only only; not successor apply/recovery/verify or release')
        (run / 'PASS.json').write_text(json.dumps(report, indent=2) + '\n')
        return report
    finally:
        (run / 'public-cli-transcript.json').write_text(json.dumps(transcript, indent=2) + '\n')
        (run / 'planner-reads.json').write_text(json.dumps(reads, indent=2) + '\n')
        print(json.dumps(dict(run_directory=str(run))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('bin-dir', 'export', 'spine-repo', 'wheel'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--installed-installer', action='store_true',
                        help='Use the calling isolated interpreter\'s installed Spine Packs, not source-tree imports')
    parser.add_argument('--runtime-version', choices=tuple(BASELINES), default=DEFAULT_RUNTIME)
    parser.add_argument('--evidence-parent', type=Path, default=Path(tempfile.gettempdir()))
    args = parser.parse_args()
    print(json.dumps(qualify(args.bin_dir.resolve(), args.export.resolve(), args.spine_repo.resolve(), args.wheel.resolve(),
        runtime_version=args.runtime_version, evidence_parent=args.evidence_parent), indent=2))
