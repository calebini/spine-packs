"""Initial v2 apply fault tests with synthetic public wire data, never a ledger."""
from copy import deepcopy
import contextlib
import io
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'tests/contract'))
from spine_packs import artifacts as a
from spine_packs.__main__ import main
from spine_packs.facet_apply import apply_initial, checkpoint, checkpoint_writer
from spine_packs.facet_apply_transport import FacetApplyCommand
from spine_packs.facet_contracts import artifact, blob, body, seal, validate
from spine_packs.facet_inventory import COMMANDS, READ_COMMANDS
from spine_packs.facet_transport import FacetSpineCommand
from spine_packs.planning import ENVIRONMENT, PlanError
import facet_artifact_oracle as independent
from fr3_fixture_support import current_contracts
from test_facet_execution import flow, reseal_plan
from test_facet_planning import Replay, CURSORS

TRANSCRIPT = json.loads((ROOT / 'tests/fixtures/installer-v2/fr2-cross-root.json').read_text())


class Catalog:
    """Synthetic post-write show/list source. Preflight is tested separately
    against the existing full public read transcript, including pagination.
    """
    def __init__(self, f, fail_at=None, malformed_at=None, read_fail_at=None):
        self.f = deepcopy(f); self.target = f['plan']['request']['target']
        self.rows = {r['object_key']: deepcopy(r) for r in f['plan']['observation']['entries']}
        self.writes = []; self.events = []; self.fail_at = fail_at
        self.malformed_at = malformed_at; self.read_fail_at = read_fail_at
        self.before_write = None; self.before_read = None
        self.budget = None

    def begin_observation(self, budget): self.budget = budget
    def check_target(self): self.events.append('target')

    def write(self, command, request):
        n = len(self.writes)
        if self.before_write: self.before_write(n)
        e = self.f['accepted_responses'][n]
        assert (command, request) == (e['command'], body(e['request']))
        self.writes.append((command, deepcopy(request))); self.events.append(('write', n))
        if n == self.fail_at: raise PlanError('spine_command_rejection', 'spine_write_rejected')
        self.rows[e['post_observation']['object_key']] = deepcopy(e['post_observation'])
        response = json.loads(e['response']['json_text'])
        if n == self.malformed_at: response.get('receipt', response)['command_id'] = 'wrong'
        return json.dumps(response, separators=(',', ':')).encode() + b'\n'

    def template(self, command):
        return deepcopy(next(r['response'] for r in TRANSCRIPT['reads'] if r['command'] == command))

    def read(self, command, request):
        self.budget.start_call()
        assert command in READ_COMMANDS
        if self.before_read: self.before_read(command, request)
        n = len(self.writes) - 1
        if n == self.read_fail_at: raise PlanError(ENVIRONMENT, 'synthetic_read_failure')
        response = self.template(command); owner = self.f['request']['request']['owner']
        if command.endswith('.list'):
            facet = command == 'item_archetype.facet_binding.list'
            rows = [r for r in self.rows.values() if r['object_key'].startswith('facet_binding:' if facet else 'binding:')]
            values = []
            for r in rows:
                value = dict(body(r['value']), status='active')
                if facet:
                    if r['root_id'] != request['item_archetype_id']: continue
                    value['facet_binding_id'] = r['binding_id']
                else:
                    template = response['entries'][0]
                    value = dict(template, **value, notification_profile_binding_id=r['binding_id'])
                values.append(value)
            if facet:
                response.update(bindings=sorted(values, key=lambda r:r['facet_key']),
                                limit=request['limit'], item_archetype_id=request['item_archetype_id'])
            else:
                values.sort(key=lambda r:(r['item_archetype_id'], r['notification_profile_binding_id']))
                response.update(entries=values, count=str(len(values)), catalog_snapshot_hash=a.digest([
                    {k:r[k] for k in ('item_archetype_id','notification_profile_id','notification_profile_binding_id','status')}
                    for r in values]))
            response.update(has_more=False, next_cursor=None)
        else:
            family = {'item_archetype.show':'archetype', 'notification_profile.show':'profile',
                      'facet_schema.show':'schema', 'notification_rendering_definition.show':'rendering'}[command]
            id_field = {'archetype':'item_archetype_id','profile':'notification_profile_id',
                        'schema':'facet_schema_id','rendering':'notification_rendering_definition_id'}[family]
            row = next(r for r in self.rows.values() if r['object_key'].startswith(family + ':')
                       and r['root_id'] == request[id_field])
            value = body(row['value'])
            if family == 'archetype':
                record = response['item_archetype']; record.update(item_archetype_id=row['root_id'], current_revision_id=row['revision_id'])
                record['revision'].update(value, item_archetype_id=row['root_id'], item_archetype_revision_id=row['revision_id'],
                                          normalized_content_hash=a.digest(value))
            elif family == 'profile':
                record = response['notification_profile']; record.update(value['metadata'], notification_profile_id=row['root_id'],
                    current_revision_id=row['revision_id'], profile_key=row['object_key'].split(':')[1], owner=owner)
                content = deepcopy(value['revision']); v2 = row['revision_contract'].endswith('.v2')
                for t in content['templates']:
                    t['normalized_template_hash'] = a.digest(dict(derivation_version='spine.notification-profile-template-hash.v2',
                        canonical_json_version='spine.canonical-json.v1', template=deepcopy(t))) if v2 else a.digest(t)
                hashed = (dict(derivation_version='spine.notification-profile-revision-hash.v2',
                    canonical_json_version='spine.canonical-json.v1', revision=content) if v2 else
                    dict(contract_version='spine.notification-profiles.v1', **content))
                record['revision'].update(content=content, notification_profile_revision_id=row['revision_id'],
                    revision_contract=row['revision_contract'], normalized_revision_hash=a.digest(hashed))
            elif family == 'schema':
                response['root'].update(owner=owner, facet_schema_id=row['root_id'], current_revision_id=row['revision_id'],
                                        schema_key=row['object_key'].split(':')[1])
                response['revision'].update(definition=value, facet_schema_id=row['root_id'], facet_schema_revision_id=row['revision_id'],
                    definition_hash=a.digest(dict(derivation_version='spine.facet-definition.v1', definition=value)))
            else:
                e = self.f['accepted_responses'][n]
                response['record'] = json.loads(e['response']['json_text'])['record']
            if family != 'rendering':
                last = json.loads(self.f['accepted_responses'][n]['response']['json_text'])
                if 'revision_number' in last:
                    (response if family == 'schema' else record)['revision']['revision_number'] = (
                        int(last['revision_number']) if family == 'archetype' else last['revision_number'])
        self.budget.received(json.dumps(response).encode())
        self.events.append(('read', command))
        return response


class FacetApplyTests(unittest.TestCase):
    def invoke(self, f=None, transport=None, writer=None, fresh=None):
        f = flow() if f is None else f
        transport = transport or Catalog(f)
        saved = []
        def save(cp):
            saved.append(deepcopy(cp)); transport.events.append(('checkpoint', len(cp['accepted_responses']), bool(cp['unresolved_submission'])))
            if writer: writer(cp)
        with patch('spine_packs.facet_apply.plan_installation', return_value=deepcopy(f['plan']) if fresh is None else fresh):
            result = apply_initial(f['manifest'], f['plan'], f['approval'], transport, save)
        return result, transport, saved

    def independent_result(self, f, result):
        # The stdlib runtime suite still exercises behavior without development
        # dependencies; the isolated official gate repeats this suite with the
        # independent Draft 2020-12 oracle enabled.
        if independent.Draft202012Validator is not None:
            with current_contracts(): independent.result_check(f['plan'], f['approval'], result)

    def test_create_and_update_all_eleven_writes_and_checkpoint_order(self):
        commands = set()
        for name in ('flight-create', 'flight-update'):
            f = flow(name); r, t, saved = self.invoke(f)
            self.assertEqual(r['state'], 'applied'); self.independent_result(f, r)
            self.assertEqual(len(saved), 2 * len(f['plan']['actions']))
            for n, e in enumerate(f['accepted_responses']):
                self.assertEqual(saved[2*n]['unresolved_submission']['request'], e['request'])
                self.assertEqual(saved[2*n+1]['accepted_responses'], f['accepted_responses'][:n+1])
            events = [e for e in t.events if isinstance(e, tuple) and e[0] != 'read']
            expected = []
            for n in range(len(t.writes)): expected += [('checkpoint', n, True), ('write', n), ('checkpoint', n+1, False)]
            self.assertEqual(events, expected)
            commands.update(cmd for cmd, _ in t.writes)
        self.assertEqual(commands, {k for k,v in COMMANDS.items() if v['phase'] is not None})

    def test_each_submission_or_readback_failure_preserves_pending_and_stops(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name)
            for field in ('fail_at', 'malformed_at', 'read_fail_at'):
                for n in range(len(f['plan']['actions'])):
                    with self.subTest(flow=name, failure=field, index=n):
                        t = Catalog(f, **{field:n}); r, _, saved = self.invoke(f, t)
                        self.assertEqual(r['state'], 'partial'); self.independent_result(f, r)
                        self.assertEqual(len(t.writes), n+1)
                        self.assertEqual(len(r['checkpoint']['accepted_responses']), n)
                        self.assertEqual(r['checkpoint'], saved[-1])
                        self.assertIsNotNone(r['checkpoint']['unresolved_submission'])

    def test_stale_preflight_and_invalid_approval_never_write(self):
        f = flow(); fresh = deepcopy(f['plan']); fresh['environment']['ledger_instance_id'] = 'other'
        r, t, saved = self.invoke(f, fresh=fresh)
        self.assertEqual(r['state'], 'not_applied'); self.assertFalse(t.writes or saved)
        self.independent_result(f, r)
        f = flow('flight-update'); f['approval']['authorized_update_action_ids'].pop(); f['approval'] = seal(f['approval'])
        t = Catalog(f)
        with patch('spine_packs.facet_apply.plan_installation') as preflight:
            with self.assertRaises(PlanError): self.invoke(f, t)
            preflight.assert_not_called()
        self.assertFalse(t.writes)

    def test_controlled_adapter_rejection_preserves_nonempty_facts_in_partial_result(self):
        for name, n in (('flight-create', 0), ('flight-update', 4)):
            f = flow(name); t = Catalog(f); original_write = t.write
            adapter = FacetApplyCommand(f['plan']['request']['target'])
            command = f['plan']['actions'][n]['command']
            rejection = dict(ok=False, command=command, error=dict(
                code='stale_version', field='request', message='PRIVATE_SENTINEL'))
            def write(actual, request):
                if len(t.writes) != n: return original_write(actual, request)
                t.writes.append((actual, deepcopy(request)))
                with patch.object(adapter, '_invoke', return_value=(rejection, 5)):
                    return adapter.write(actual, request)
            t.write = write
            with self.subTest(flow=name, n=n):
                value, _, saved = self.invoke(f, t)
                self.assertEqual(value['state'], 'partial')
                self.assertEqual(value['checkpoint'], saved[-1])
                self.assertEqual(len(t.writes), n+1)
                self.assertEqual(len(value['checkpoint']['accepted_responses']), n)
                self.assertEqual(value['checkpoint']['unresolved_submission']['request'],
                                 f['accepted_responses'][n]['request'])
                self.assertEqual(value['failure']['error']['facts'],
                                 [dict(name='spine_error_code', value='stale_version')])
                self.assertNotIn('PRIVATE_SENTINEL', a.canonical_text(value))
                artifact(value, 'apply-result'); self.independent_result(f, value)

    def test_public_readback_revision_numbers_and_rendering_provenance_match(self):
        for name in ('flight-create', 'flight-update'):
            f=flow(name)
            for n,e in enumerate(f['accepted_responses']):
                response=json.loads(e['response']['json_text'])
                if 'revision_number' not in response and 'record' not in response: continue
                with self.subTest(flow=name,command=e['command']):
                    t=Catalog(f); original=t.write
                    def write(command,request):
                        raw=original(command,request)
                        if len(t.writes)-1==n:
                            r=json.loads(raw)
                            if 'record' in r:r['record']['created']['command_id']='unrelated'
                            else:r['revision_number']='99'
                            return json.dumps(r).encode()
                        return raw
                    t.write=write
                    result,_,_=self.invoke(f,t)
                    self.assertEqual(result['state'],'partial');self.assertEqual(len(t.writes),n+1)

    def test_changed_revision_cannot_reuse_immutable_prior_identity(self):
        f = flow('flight-update')
        n = next(i for i, e in enumerate(f['accepted_responses']) if e['command'] == 'facet_schema.publish')
        t = Catalog(f); original = t.write
        def write(command, request):
            raw = original(command, request)
            if len(t.writes) - 1 == n:
                response = json.loads(raw)
                old = request['expected_current_revision_id']
                response['facet_schema_revision_id'] = old
                row = t.rows[f['accepted_responses'][n]['post_observation']['object_key']]
                row['revision_id'] = old
                return json.dumps(response, separators=(',', ':')).encode() + b'\n'
            return raw
        t.write = write
        result, _, _ = self.invoke(f, t)
        self.assertEqual(result['state'], 'partial')
        self.assertEqual(len(t.writes), n + 1)
        self.assertEqual(len(result['checkpoint']['accepted_responses']), n)
        self.assertIsNotNone(result['checkpoint']['unresolved_submission'])

    def assert_reused_revision_stops(self, command, replayed=False):
        f = flow('flight-update')
        n = next(i for i, e in enumerate(f['accepted_responses']) if e['command'] == command)
        t = Catalog(f); original = t.write
        def write(actual_command, request):
            raw = original(actual_command, request)
            if len(t.writes) - 1 != n:
                return raw
            response = json.loads(raw)
            old = f['plan']['actions'][n]['expected']['revision_id']
            record = response.get('record', response)
            field = COMMANDS[command]['outputs']['revision'].rsplit('/', 1)[-1]
            record[field] = old
            if 'record' in response:
                record['current_revision_id'] = old
            if replayed:
                response.update(replayed=True, changed=False)
            # Prove the mutation crosses the public schema boundary: rejection
            # must come from immutable preimage correlation, not malformed JSON.
            validate(response, 'spine-readback-0.10.0.schema.json', COMMANDS[command]['response'])
            row = t.rows[f['accepted_responses'][n]['post_observation']['object_key']]
            row['revision_id'] = old
            if 'record' in response:
                t.f['accepted_responses'][n]['response']['json_text'] = json.dumps(response)
            return json.dumps(response, separators=(',', ':')).encode() + b'\n'
        t.write = write
        result, _, saved = self.invoke(f, t)
        self.assertEqual(result['state'], 'partial')
        self.assertEqual(len(t.writes), n + 1)
        self.assertEqual(len(result['checkpoint']['accepted_responses']), n)
        self.assertEqual(result['checkpoint'], saved[-1])
        unresolved = result['checkpoint']['unresolved_submission']
        self.assertIsNotNone(unresolved)
        self.assertEqual(body(unresolved['request']), t.writes[-1][1])

    def test_catalog_revisions_without_changed_flag_cannot_reuse_preimage(self):
        for command in ('item_archetype.revise', 'notification_profile.revise'):
            with self.subTest(command=command):
                self.assert_reused_revision_stops(command)

    def test_replayed_publish_without_changed_flag_cannot_reuse_preimage(self):
        for command in ('facet_schema.publish', 'notification_rendering_definition.publish'):
            with self.subTest(command=command):
                self.assert_reused_revision_stops(command, replayed=True)

    def test_replayed_publish_with_distinct_revision_remains_accepted(self):
        for command in ('facet_schema.publish', 'notification_rendering_definition.publish'):
            with self.subTest(command=command):
                f = flow('flight-update'); t = Catalog(f); original = t.write
                def write(actual_command, request):
                    raw = original(actual_command, request)
                    if actual_command == command:
                        response = json.loads(raw)
                        response.update(replayed=True, changed=False)
                        return json.dumps(response).encode() + b'\n'
                    return raw
                t.write = write
                result, _, _ = self.invoke(f, t)
                self.assertEqual(result['state'], 'applied')
                self.assertEqual(len(t.writes), len(f['plan']['actions']))

    def test_metadata_only_update_still_preserves_prior_revision(self):
        f = flow('flight-update')
        n = next(i for i, e in enumerate(f['accepted_responses'])
                 if e['command'] == 'notification_profile.metadata.update')
        self.assertEqual(f['plan']['actions'][n]['expected']['revision_id'],
                         f['accepted_responses'][n]['post_observation']['revision_id'])
        result, _, _ = self.invoke(f)
        self.assertEqual(result['state'], 'applied')
        self.assertEqual(result['checkpoint']['accepted_responses'][n]['post_observation']['revision_id'],
                         f['plan']['actions'][n]['expected']['revision_id'])

    def test_every_durable_boundary_failure_prevents_the_next_submission(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name)
            for fail in range(2 * len(f['plan']['actions'])):
                calls = []
                def writer(cp):
                    calls.append(cp)
                    if len(calls) == fail+1: raise PlanError(ENVIRONMENT, 'checkpoint_publication_failed')
                t = Catalog(f)
                with self.subTest(flow=name, boundary=fail), self.assertRaises(PlanError): self.invoke(f, t, writer)
                self.assertEqual(len(t.writes), (fail+1)//2)

    def test_binding_recheck_catches_changed_binding_before_submission(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name); t = Catalog(f)
            def mutate(command, request):
                if command == 'item_archetype.facet_binding.list' and len(t.writes) == 2:
                    key = 'facet_binding:flight:flight'
                    existing = deepcopy(f['accepted_responses'][2]['post_observation'])
                    existing['binding_id'] = 'unapproved-binding'; t.rows[key] = existing
            t.before_read = mutate
            r, _, _ = self.invoke(f, t)
            self.assertEqual(r['state'], 'partial'); self.assertEqual(len(t.writes), 2)
            self.assertIsNone(r['checkpoint']['unresolved_submission'])
            self.assertEqual(r['failure']['error']['category'], 'stale_plan_or_target_mismatch')
        f = flow(); t = Catalog(f)
        def mutate_default(command, request):
            if command == 'notification_profile.binding.list' and len(t.writes) == 5:
                row = deepcopy(f['accepted_responses'][5]['post_observation']); row['binding_id'] = 'unapproved'
                t.rows[row['object_key']] = row
        t.before_read = mutate_default
        r, _, _ = self.invoke(f, t)
        self.assertEqual(len(t.writes), 5); self.assertEqual(r['state'], 'partial')

    def test_real_read_only_preflight_transcript_is_consumed_before_checkpoint(self):
        f = deepcopy(TRANSCRIPT)
        f['reads'].append(deepcopy(next(r for r in f['reads'] if r['command'] == 'item_archetype.facet_binding.list')))
        approval = deepcopy(flow()['approval']); approval['plan_digest'] = f['plan']['content_identity']['digest']
        approval['authorized_update_action_ids'] = f['plan']['decision_action_ids']; approval = seal(approval)
        t = Replay(f); saved = []
        def stop(cp):
            saved.append(cp); raise PlanError(ENVIRONMENT, 'stop_before_write')
        with patch.dict(os.environ, CURSORS), self.assertRaisesRegex(PlanError, 'stop_before_write'):
            apply_initial(f['manifest'], f['plan'], approval, t, stop, page_size=1)
        self.assertFalse(t.rows)
        self.assertEqual(len(saved), 1); self.assertIsNotNone(saved[0]['unresolved_submission'])

    def test_v2_checkpoint_files_are_private_owned_and_never_clobber(self):
        f = flow()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'checkpoint.json'; writer = checkpoint_writer(path)
            cp = checkpoint(f['plan'], f['approval'], [])
            writer(cp); self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            with self.assertRaises(PlanError): checkpoint_writer(path)
            path.write_text('changed')
            with self.assertRaises(PlanError): writer(cp)
            self.assertEqual(path.read_text(), 'changed')

    def test_file_and_directory_fsync_failures_stop_at_each_publication(self):
        f = flow()
        for fail_at in (1, 2, 3, 4):
            with self.subTest(fsync=fail_at), tempfile.TemporaryDirectory() as directory:
                t = Catalog(f); path = Path(directory)/'cp.json'; writer = checkpoint_writer(path)
                original = os.fsync; calls = []
                def fsync(fd):
                    calls.append(stat.S_ISDIR(os.fstat(fd).st_mode))
                    if len(calls) == fail_at: raise OSError('PRIVATE_SENTINEL')
                    original(fd)
                with patch('spine_packs.apply.os.fsync', side_effect=fsync), self.assertRaises(PlanError) as error:
                    self.invoke(f, t, writer)
                self.assertNotIn('PRIVATE_SENTINEL', str(error.exception))
                self.assertEqual(len(t.writes), 0 if fail_at < 3 else 1)
                self.assertEqual(calls, [False, True, False, True][:fail_at])
                if path.exists():
                    cp = a.load_json(path); artifact(cp, 'apply-checkpoint')
                    self.assertEqual(len(cp['accepted_responses']), 1 if fail_at == 4 else 0)

    def test_writer_link_and_replace_failure_stop_before_consumers(self):
        f = flow()
        for operation in ('link', 'replace'):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as directory:
                t = Catalog(f); path = Path(directory)/'cp.json'; writer = checkpoint_writer(path)
                with patch('spine_packs.apply.os.' + operation, side_effect=OSError('injected')), self.assertRaises(PlanError):
                    self.invoke(f, t, writer)
                self.assertEqual(len(t.writes), 0 if operation == 'link' else 1)
                if path.exists(): self.assertIsNotNone(a.load_json(path)['unresolved_submission'])

    def test_actual_preflight_environment_change_returns_not_applied(self):
        f = deepcopy(TRANSCRIPT); t = Replay(f, lambda cmd, req, response, n:
            (dict(response, ledger_instance_id='ledger_instance_' + 'a' * 64) if cmd == 'system.info' else response, 0))
        approval = deepcopy(flow()['approval']); approval['plan_digest'] = f['plan']['content_identity']['digest']
        approval['authorized_update_action_ids'] = f['plan']['decision_action_ids']; approval = seal(approval)
        saved = []
        with patch.dict(os.environ, CURSORS):
            r = apply_initial(f['manifest'], f['plan'], approval, t, saved.append, page_size=1)
        self.assertEqual(r['state'], 'not_applied'); self.assertFalse(saved or t.rows)
        self.assertEqual(r['failure']['error']['category'], 'stale_plan_or_target_mismatch')

    def cli(self, directory, f, transport, *, source=None, operation='apply', publish_failure=False, default_factory=False):
        base = Path(directory); inputs = []
        for key in ('manifest', 'plan', 'approval'):
            path = base/(key+'.json'); path.write_text(json.dumps(f[key])); inputs += ['--'+key,str(path)]
        args = [operation, *inputs, '--checkpoint',str(base/'checkpoint.json'),'--output',str(base/'result.json')]
        if source: args += ['--continue-from',source]
        with contextlib.redirect_stdout(io.StringIO()) as out, \
                patch('spine_packs.facet_apply.plan_installation', return_value=deepcopy(f['plan'])):
            if default_factory:
                with patch('spine_packs.facet_apply_transport.FacetApplyCommand', return_value=transport) as factory:
                    code = main(args)
                    factory.assert_called_once_with(f['plan']['request']['target'])
            elif publish_failure:
                with patch('spine_packs.__main__.publish', side_effect=PlanError(ENVIRONMENT,'output_publication_failed')):
                    code = main(args, transport_factory=lambda target: transport)
            else:
                code = main(args, transport_factory=lambda target: transport)
        return code, json.loads(out.getvalue())

    def test_cli_default_uses_apply_adapter(self):
        f=flow();t=Catalog(f)
        with tempfile.TemporaryDirectory() as directory:
            code,_=self.cli(directory,f,t,default_factory=True)
        self.assertEqual(code,0)

    def test_cli_success_partial_and_result_publication_failure(self):
        for scenario in ('success','partial','output_failure'):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as directory:
                f = flow(); t = Catalog(f, fail_at=0 if scenario=='partial' else None)
                code, envelope = self.cli(directory, f, t, publish_failure=scenario=='output_failure')
                self.assertEqual(code, {'success':0,'partial':9,'output_failure':11}[scenario])
                self.assertEqual(envelope['artifact_schema'], 'spine.pack-installer-result.v2')
                self.assertTrue((Path(directory)/'checkpoint.json').exists())
                self.assertEqual((Path(directory)/'result.json').exists(), scenario!='output_failure')
                if scenario!='output_failure':
                    saved = a.load_json(Path(directory)/'result.json'); self.independent_result(f, saved)

    def test_cli_rejects_successor_continuation_and_verify_before_target(self):
        for operation in ('apply','verify'):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as directory:
                f = flow(); t = Catalog(f)
                code, envelope = self.cli(directory, f, t, source='unread-source.json' if operation=='apply' else None,
                                          operation=operation)
                self.assertEqual(code,2); self.assertFalse(t.events or t.writes)
                self.assertEqual(envelope['error']['code'],'successor_operation_not_authorized')

    def test_cli_output_collision_rejected_before_transport_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            f = flow(); t = Catalog(f); path = Path(directory)/'result.json'; path.write_text('sentinel')
            code, _ = self.cli(directory,f,t)
            self.assertEqual(code,2); self.assertFalse(t.events or t.writes)
            self.assertEqual(path.read_text(),'sentinel')

    def test_draft_and_blocked_apply_keep_existing_exit_taxonomy(self):
        from spine_packs.facet_manifest import digest as manifest_digest
        from spine_packs.facet_planning import build_plan
        for mode,expected in (('draft',3),('blocked',6)):
            f=flow('flight-update' if mode=='blocked' else 'flight-create')
            if mode=='draft':
                f['manifest']['pack'].update(status='draft',version='1.0.0-draft.1')
                f['manifest']['content_identity']['digest']=manifest_digest(f['manifest'])
                f['request']['request']['draft_posture']='inspect_only';f['request']=seal(f['request'])
            else:
                view=f['plan']['observation']
                next(r for r in view['entries'] if r['object_key']=='schema:flight_details')['status']='retired'
                view['digest']=a.digest(dict(derivation_version='spine.pack-observation.v2',view={k:v for k,v in view.items() if k!='digest'}))
            f['plan']=build_plan(f['manifest'],f['request'],f['plan']['environment'],f['plan']['observation'])
            f['approval']['authorized_update_action_ids']=f['plan']['decision_action_ids'];reseal_plan(f)
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as directory:
                t=Catalog(f);code,_=self.cli(directory,f,t)
                self.assertEqual(code,expected);self.assertFalse(t.events or t.writes)

    def test_equivalent_no_action_plan_publishes_empty_checkpoint(self):
        from spine_packs.facet_planning import build_plan
        f = flow(); view = deepcopy(json.loads((ROOT/'tests/fixtures/installer-v2/flight-create.json').read_text())['observations'][-1])
        f['plan'] = build_plan(f['manifest'],f['request'],f['plan']['environment'],view); reseal_plan(f)
        self.assertFalse(f['plan']['actions']); r,t,saved=self.invoke(f)
        self.assertEqual(r['state'],'applied'); self.assertEqual(len(saved),1); self.assertFalse(t.writes)
        self.independent_result(f,r)


class ApplyTransportTests(unittest.TestCase):
    def test_public_subprocess_arguments_and_exact_stdout_capture(self):
        f=flow();e=f['accepted_responses'][0];request=body(e['request'])
        raw=e['response']['json_text'].encode()+b'\n'
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory).resolve();command=base/'synthetic-command';ledger=base/'synthetic-target';ledger.touch()
            command.write_text('#!'+sys.executable+'\nimport sys,json\n'
                +'assert sys.argv[3:-2] == '+repr(e['command'].split('.'))+'\n'
                +"assert sys.argv[-2:] == ['--input','-']\n"
                +'assert json.load(sys.stdin) == '+repr(request)+'\n'
                +'sys.stdout.buffer.write('+repr(raw)+')\n')
            command.chmod(0o700)
            target=dict(host_name='synthetic.invalid',ledger=dict(kind='path',path=str(ledger)),
                spine_command=dict(path=str(command),sha256=hashlib.sha256(command.read_bytes()).hexdigest()))
            adapter=FacetApplyCommand(target,host_resolver=lambda:'synthetic.invalid')
            self.assertEqual(adapter.write(e['command'],request),raw)

    def test_write_stdout_limit_stops_before_appending_overflow(self):
        adapter=FacetApplyCommand(flow()['plan']['request']['target']);adapter._write_bytes=bytearray()
        adapter._received(b'x'*(16*1024*1024))
        with self.assertRaisesRegex(PlanError,'spine_response_too_large'):adapter._received(b'x')
        self.assertEqual(len(adapter._write_bytes),16*1024*1024)

    def test_write_wire_bytes_are_exact_and_observation_budget_is_separate(self):
        f=flow(); adapter=FacetApplyCommand(f['plan']['request']['target']);e=f['accepted_responses'][0]
        raw=e['response']['json_text'].encode()+b'  \n'
        def invoke(command,request):
            adapter._received(raw[:50]);adapter._received(raw[50:]);return json.loads(raw),0
        with patch.object(adapter,'_invoke',side_effect=invoke):
            self.assertEqual(adapter.write(e['command'],body(e['request'])),raw)
        self.assertIsNone(adapter._write_bytes); self.assertIsNone(adapter.budget)

    def test_write_allowlist_and_request_validation_precede_invocation(self):
        f=flow();adapter=FacetApplyCommand(f['plan']['request']['target'])
        with patch.object(adapter,'_invoke') as invoke:
            for command in ('item.create','notification.send','notification_rendering_disclosure.provision','facet_schema.show'):
                with self.assertRaises(PlanError):adapter.write(command,{})
            with self.assertRaises(PlanError):adapter.write('facet_schema.create',{})
            invoke.assert_not_called()
        with self.assertRaisesRegex(PlanError,'successor_write_not_authorized'):
            FacetSpineCommand(f['plan']['request']['target']).write('facet_schema.create',{})

    def test_failure_shape_exit_pairing_and_redacted_diagnostics(self):
        f=flow();adapter=FacetApplyCommand(f['plan']['request']['target']);e=f['accepted_responses'][0]
        for code,exit_code,expected in (('semantic_conflict',6,'spine_command_rejection'),
                ('environment_failure',7,ENVIRONMENT),('runtime_failure',1,ENVIRONMENT),
                ('semantic_conflict',7,ENVIRONMENT),('unknown_failure',1,ENVIRONMENT)):
            response=dict(ok=False,command=e['command'],error=dict(code=code,message='PRIVATE_SENTINEL',field='request'))
            with self.subTest(code=code,exit=exit_code),patch.object(adapter,'_invoke',return_value=(response,exit_code)):
                with self.assertRaises(PlanError) as error:adapter.write(e['command'],body(e['request']))
                self.assertEqual(error.exception.category,expected);self.assertNotIn('PRIVATE_SENTINEL',str(error.exception))

        facet_e = next(row for row in f['accepted_responses'] if row['command'] == 'facet_schema.create')
        for error_body in (
            dict(code='semantic_conflict', message='PRIVATE_SENTINEL', field=None),
            dict(code='rendering_definition_invalid', message='PRIVATE_SENTINEL', field='request'),
        ):
            response = dict(ok=False, command=facet_e['command'], error=error_body)
            with self.subTest(error=error_body), patch.object(adapter, '_invoke', return_value=(response, 6)):
                with self.assertRaises(PlanError) as error:
                    adapter.write(facet_e['command'], body(facet_e['request']))
                self.assertEqual(error.exception.category, ENVIRONMENT)
                self.assertNotIn('PRIVATE_SENTINEL', str(error.exception))


if __name__ == '__main__': unittest.main()
