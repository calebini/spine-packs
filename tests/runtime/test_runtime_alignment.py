"""AL-2 exact-baseline routing with synthetic public wire data, never ledgers."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'tests/contract')]
from spine_packs import artifacts as artifacts
from spine_packs.__main__ import main, envelope
from spine_packs.facet_baselines import BASELINES, runtime_baseline
from spine_packs.facet_contracts import blob, body, seal
from spine_packs.facet_execution import ExecutionContext, projected_state
from spine_packs.facet_inventory import COMMANDS, CONTRACTS, READ_COMMANDS
from spine_packs.facet_planning import plan_installation
from spine_packs.facet_apply import apply_initial, apply_continuation
from spine_packs.facet_apply_transport import FacetApplyCommand
from spine_packs.facet_transport import FacetSpineCommand, ObservationBudget
from spine_packs.facet_verification import verify_installation
from spine_packs.planning import PlanError, ENVIRONMENT
import facet_artifact_oracle as oracle
from fr4_fixture_support import refresh as companion, load_flow as historical_flow
from test_facet_manifest_contract import digest as portable_digest
from test_facet_planning import Replay, fixture as planning_fixture, CURSORS
from test_facet_continuation import PublicCatalog, prepared, reseal_view
import test_facet_cli as cli_tests


def aligned_flow(name):
    """Dependency-free derivation, checked against the ratified AL-1 digests.

    Transform only baseline identity and dependent hashes in frozen synthetic
    wire values. No runtime compiler/helper produces expected command requests.
    The official contract gate independently validates the same digest vectors.
    """
    index = oracle.load(ROOT / 'tests/fixtures/installer-v2/alignment-0.12.0.json')
    vector = next(v for v in index['flows'] if v['id'] == name)
    source = ROOT / vector['source']['path']
    assert oracle.sha(source.read_bytes()) == vector['source']['sha256']
    f = oracle.load(source); original = deepcopy(f)
    m = f['manifest']; m['compatibility']['spine_runtime_versions'] = ['0.12.0']
    m['content_identity']['digest'] = portable_digest(m)
    p = f['plan']; p['pack']['manifest_digest'] = m['content_identity']['digest']
    p['environment'].update(runtime_version='0.12.0', ledger_schema_current='20', ledger_schema_implemented='20')
    f['plan'] = p = oracle.seal(p)
    f['approval']['plan_digest'] = p['content_identity']['digest']; f['approval'] = oracle.seal(f['approval'])
    for action, e in zip(p['actions'], f['accepted_responses'], strict=True):
        request = oracle.unblob(e['request'])
        request['command_id'] = oracle.command_id(p, f['approval'], action)
        e.update(command_id=request['command_id'], request=oracle.blob(request))
        response = oracle.unblob(e['response'], True)
        response.get('receipt', response)['command_id'] = request['command_id']
        if e['receipt']['family'] == 'catalog':
            response['receipt']['semantic_facts_hash'] = oracle.hash_value(request)
        elif e['receipt']['family'] == 'rendering':
            response['record']['published']['command_id'] = request['command_id']
            if action['command'].endswith('.create'):
                response['record']['created']['command_id'] = request['command_id']
        text = json.dumps(response, ensure_ascii=False, separators=(',', ':'))
        e['response'] = dict(json_text=text, digest=oracle.sha(text.encode()))
        e['receipt'] = oracle.receipt_projection(e['command'], response)
    def cp_at(prior):
        cp = deepcopy(f['initial_checkpoint']); n = len(prior['accepted_responses'])
        cp.update(plan_digest=p['content_identity']['digest'], approval_digest=f['approval']['content_identity']['digest'],
                  accepted_responses=deepcopy(f['accepted_responses'][:n]),
                  next_action_id=p['actions'][n]['action_id'] if n < len(p['actions']) else None,
                  unresolved_submission=None)
        if prior['unresolved_submission'] is not None:
            e = f['accepted_responses'][n]
            cp['unresolved_submission'] = dict(action_id=e['action_id'], command_id=e['command_id'],
                submission_state='prepared_or_submitted', request=deepcopy(e['request']))
        return oracle.seal(cp)
    for key in ('initial_checkpoint', 'final_checkpoint', 'prepared_checkpoint'):
        f[key] = cp_at(original[key])
    for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
        f[key]['checkpoint'] = cp_at(original[key]['checkpoint']); f[key] = oracle.seal(f[key])
    f.update(companion(f, vector['source']['path'], vector['source']['sha256']))
    f['verification']['receipt_readback'] = 'captured_responses_only_spine_0.12.0'
    f['verification'] = oracle.seal(f['verification'])
    f['envelope']['artifact']['digest'] = f['verification']['content_identity']['digest']
    actual = dict(manifest_digest=m['content_identity']['digest'],
        artifact_digests={k: v['content_identity']['digest'] for k, v in f.items()
            if isinstance(v, dict) and 'artifact_schema' in v and 'content_identity' in v},
        wire=[{k:e[k] for k in ('action_id', 'command', 'command_id')} | dict(
            request_digest=e['request']['digest'], response_digest=e['response']['digest']) for e in f['accepted_responses']],
        observation_digests=[v['digest'] for v in f['observations']])
    assert actual == vector['expected'], 'AL-1 independent digest vector mismatch'
    return f


def cross_root():
    f = planning_fixture(); f['manifest']['compatibility']['spine_runtime_versions'] = ['0.12.0']
    f['manifest']['content_identity']['digest'] = portable_digest(f['manifest'])
    f['plan']['pack']['manifest_digest'] = f['manifest']['content_identity']['digest']
    f['plan']['environment'].update(runtime_version='0.12.0', ledger_schema_current='20', ledger_schema_implemented='20')
    f['plan'] = oracle.seal(f['plan'])
    for row in f['reads']:
        if row['command'] == 'system.info':
            row['response'].update(runtime_version='0.12.0', ledger_schema_version='20', implemented_ledger_schema_version='20')
    return f


class AlignedCatalog(PublicCatalog):
    def read(self, command, request):
        response = super().read(command, request)
        if command == 'system.info':
            env = self.original['plan']['environment']
            response.update(runtime_version=env['runtime_version'], ledger_schema_version=env['ledger_schema_current'],
                            implemented_ledger_schema_version=env['ledger_schema_implemented'])
        return response


class RuntimeAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict('os.environ', CURSORS))
        self.enterContext(patch('subprocess.Popen', side_effect=AssertionError('synthetic commands only')))

    def test_registry_matches_both_reviewed_inventories_and_is_closed(self):
        self.assertEqual(set(BASELINES), {'0.10.0', '0.12.0'})
        for runtime, baseline in BASELINES.items():
            inv = oracle.load(ROOT / ('contracts/installer-spine-' + runtime + '-inventory.json'))
            self.assertEqual((baseline.commit, baseline.schema, baseline.runtime),
                             (inv['spine_commit'], inv['ledger_schema'], inv['runtime_version']))
            self.assertEqual(COMMANDS, inv['commands']); self.assertEqual(CONTRACTS, inv['required_execution_contracts'])
        for runtime in ('0.9.1', '0.10.1', '0.11.0', '0.12.1', '0.13.0', None, []):
            with self.subTest(runtime=runtime), self.assertRaises(PlanError): runtime_baseline(runtime)
        with self.assertRaises(TypeError): BASELINES['0.13.0'] = BASELINES['0.12.0']
        with self.assertRaises(AttributeError): BASELINES['0.12.0'].schema = '21'

    def test_planning_uses_new_closure_and_preserves_cross_root_history_and_dedup(self):
        import spine_packs.facet_transport as transport_module
        import spine_packs.facet_observation as observation_module
        f = cross_root(); transport = Replay(f)
        with patch.object(transport_module, 'validate', wraps=transport_module.validate) as wire, \
                patch.object(observation_module, 'validate', wraps=observation_module.validate) as observed:
            actual = plan_installation(f['manifest'], f['request'], transport, page_size=1)
        self.assertEqual(actual, f['plan']); self.assertFalse(transport.rows)
        self.assertEqual(transport.calls.count('facet_schema.revision.show'), 2)
        self.assertEqual(transport.baseline.runtime, '0.12.0')
        for spy in (wire, observed):
            names = [c.args[1] for c in spy.call_args_list if c.args[1].startswith('spine-readback-')]
            self.assertTrue(names); self.assertEqual(set(names), {'spine-readback-0.12.0.schema.json'})
        history = actual['observation']['historical_revisions'][0]
        desired = next(r for r in actual['resolutions'] if r['object_key'] == 'schema:flight_details')
        self.assertNotEqual(history['root_id'], desired['root']['value'])

    def test_preflight_fails_before_catalog_reads_for_wrong_runtime_schema_or_contract(self):
        for fault in ('runtime', 'current', 'implemented', 'contract', 'identity', 'second_pass'):
            f = cross_root()
            def mutate(command, request, response, n):
                if command == 'system.info':
                    if fault == 'runtime': response['runtime_version'] = '0.10.0'
                    elif fault == 'current': response['ledger_schema_version'] = '19'
                    elif fault == 'implemented': response['implemented_ledger_schema_version'] = '19'
                    elif fault == 'contract': response['implemented_contract_versions'].remove('spine.facet-schema-revision-readback.v1')
                    elif fault == 'identity': response['ledger_instance_id'] = 'bad'
                    elif n > 1: response['runtime_version'] = '0.10.0'
                return response, 0
            t = Replay(f, mutate)
            with self.subTest(fault=fault), self.assertRaises(PlanError):
                plan_installation(f['manifest'], f['request'], t, page_size=1)
            if fault != 'second_pass': self.assertEqual(t.calls, ['system.info'])

    def test_transport_binding_cannot_switch_baselines_or_expand_command_authority(self):
        f = cross_root(); t = Replay(f); t.select_runtime('0.10.0')
        with self.assertRaisesRegex(PlanError, 'transport_baseline_mismatch'):
            plan_installation(f['manifest'], f['request'], t)
        self.assertEqual(t.calls, [])
        old, new = FacetSpineCommand({}), FacetSpineCommand({}, runtime_version='0.12.0')
        old.select_runtime('0.10.0'); new.select_runtime('0.12.0')
        self.assertEqual((old.baseline.runtime, new.baseline.runtime), ('0.10.0', '0.12.0'))
        for transport in (old, new):
            with self.assertRaises(PlanError): transport.write('item_archetype.create', {})
            with self.assertRaises(PlanError): transport.read('person.create', {})
        with self.assertRaisesRegex(PlanError, 'transport_baseline_mismatch'): new.select_runtime('0.10.0')

    def test_all_requests_and_responses_match_ratified_flows_under_new_entry_point(self):
        import spine_packs.facet_execution as execution
        commands = set()
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name); c = ExecutionContext(f['manifest'], f['plan'], f['approval']); accepted = []
            with patch.object(execution, 'validate', wraps=execution.validate) as checked:
                for e in f['accepted_responses']:
                    self.assertEqual(c.materialize(accepted), body(e['request']))
                    evidence = c.response_evidence(accepted, e['response']['json_text'].encode(), e['post_observation'])
                    self.assertEqual(evidence, e); accepted.append(evidence); commands.add(e['command'])
            public = [call.args[1] for call in checked.call_args_list if call.args[1].startswith('spine-readback-')]
            self.assertTrue(public); self.assertEqual(set(public), {'spine-readback-0.12.0.schema.json'})
        self.assertEqual(commands, {k for k, v in COMMANDS.items() if v['phase'] is not None})

    def test_initial_apply_and_verify_both_complete_synthetic_flows(self):
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name); t = AlignedCatalog(f, 0, f['observations'][0]); saved = []
            applied = apply_initial(f['manifest'], f['plan'], f['approval'], t, lambda v:saved.append(deepcopy(v)))
            self.assertEqual(applied, f['apply_result']); self.assertEqual(saved[-1], f['final_checkpoint'])
            read = AlignedCatalog(f, 6, f['observations'][-1]); read.write = Mock(side_effect=AssertionError('read-only verify'))
            value = verify_installation(f['manifest'], f['plan'], read, applied)
            # Independent verification retains only currently required pins,
            # whereas the saved execution companion includes retired lineage.
            expected = deepcopy(f['verification'])
            expected['observation']['historical_revisions'] = []
            expected['observation']['digest'] = oracle.observation_digest(expected['observation'])
            self.assertEqual(value, oracle.seal(expected)); read.write.assert_not_called()
            self.assertEqual(value['receipt_readback'], BASELINES['0.12.0'].receipt_readback)

    def test_initial_apply_rejects_different_transport_target_with_identical_catalog(self):
        for runtime in BASELINES:
            f = (aligned_flow('flight-create') if runtime == '0.12.0' else
                 historical_flow('tests/fixtures/installer-v2/fr4-flight-create-0.10.0.json'))
            original = deepcopy(f['plan']); t = AlignedCatalog(f, 0, f['observations'][0])
            # Same ledger, environment and catalog; only the executable differs.
            t.target = deepcopy(t.target)
            t.target['spine_command']['path'] = '/synthetic/other-spine-command'
            t.read = Mock(wraps=t.read); writer = Mock()
            with self.subTest(runtime=runtime):
                result = apply_initial(f['manifest'], f['plan'], f['approval'], t, writer)
                self.assertEqual(result['state'], 'not_applied')
                self.assertEqual(result['failure']['error']['category'], 'stale_plan_or_target_mismatch')
                self.assertEqual(result['checkpoint']['accepted_responses'], [])
                self.assertEqual(t.writes, []); writer.assert_not_called(); t.read.assert_not_called()
                self.assertEqual(f['plan'], original)

    def test_nonrevision_read_failures_validate_shape_exit_and_category_on_both_baselines(self):
        f = planning_fixture()
        for runtime in BASELINES:
            for command in sorted(READ_COMMANDS - {'facet_schema.revision.show'}):
                request = next(row['request'] for row in f['reads'] if row['command'] == command)
                cases = [
                    ('valid_rejection', 'invalid_request', 'contract_version', 2, 'spine_command_rejection'),
                    ('missing_reference', 'referenced_row_not_found', 'id', 4, 'spine_command_rejection'),
                    ('capacity', 'environment_failure', 'capacity', 7, ENVIRONMENT),
                    ('handler_fallback', 'runtime_failure', None, 1, ENVIRONMENT),
                    ('db_preflight', 'invalid_request', 'db', 3, 'spine_command_rejection'),
                    ('runtime_preflight', 'environment_failure', 'runtime_contracts', 7, 'spine_command_rejection'),
                    ('missing_error', 'invalid_request', 'contract_version', 0, ENVIRONMENT),
                    ('bad_exit', 'invalid_request', 'contract_version', 0, ENVIRONMENT),
                    ('unknown_code', 'invented_error', 'id', 2, ENVIRONMENT),
                    ('extra_error', 'invalid_request', 'contract_version', 2, ENVIRONMENT),
                    ('wrong_command', 'invalid_request', 'contract_version', 2, ENVIRONMENT),
                    ('bad_preflight_exit', 'invalid_request', 'db', 2, ENVIRONMENT),
                    ('empty_request_preflight', 'invalid_request', 'request', 2, ENVIRONMENT),
                ]
                for fault, code, field, exit_code, category in cases:
                    response = dict(ok=False, command=command, error=dict(code=code, message='PRIVATE_SENTINEL'))
                    if field is not None: response['error']['field'] = field
                    if fault == 'missing_error': del response['error']
                    elif fault == 'extra_error': response['error']['unexpected'] = 'PRIVATE_SENTINEL'
                    elif fault == 'wrong_command': response['command'] = 'person.create'
                    elif fault == 'empty_request_preflight': response['error']['message'] = ''
                    t = FacetSpineCommand({}, runtime_version=runtime); t.budget = ObservationBudget()
                    with self.subTest(runtime=runtime, command=command, fault=fault), \
                            patch.object(t, '_invoke', return_value=(response, exit_code)):
                        with self.assertRaises(PlanError) as caught: t.read(command, request)
                        self.assertEqual(caught.exception.category, category)
                        output = envelope(category, caught.exception.code)
                        self.assertEqual(output['exit_code'], '11' if category == ENVIRONMENT else '8')
                        self.assertNotIn('PRIVATE_SENTINEL', json.dumps(output))

    def test_cli_malformed_system_info_failure_is_environment_failure_not_rejection(self):
        for runtime in BASELINES:
            for fault, expected in (('missing_error', 11), ('empty_message', 11), ('valid', 8)):
                f = cross_root() if runtime == '0.12.0' else planning_fixture()
                def failure(command, request, response, n):
                    self.assertEqual(command, 'system.info')
                    rejected = dict(ok=False, command=command)
                    if fault != 'missing_error':
                        rejected['error'] = dict(code='invalid_request', field='request',
                                                 message='' if fault == 'empty_message' else 'PRIVATE_SENTINEL')
                    return rejected, 0 if fault == 'missing_error' else 2
                t = Replay(f, failure)
                with self.subTest(runtime=runtime, fault=fault), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    for name in ('manifest', 'request'):
                        (root/name).write_text(artifacts.canonical_text(f[name]))
                    with contextlib.redirect_stdout(io.StringIO()) as stdout:
                        code = main(['plan', '--manifest', str(root/'manifest'), '--request', str(root/'request'),
                                     '--output', str(root/'output')], transport_factory=lambda target:t)
                    self.assertEqual(code, expected)
                    self.assertEqual(json.loads(stdout.getvalue())['exit_code'], str(expected))
                    self.assertEqual(t.calls, ['system.info']); self.assertFalse((root/'output').exists())
                    self.assertNotIn('PRIVATE_SENTINEL', stdout.getvalue())

    def test_v1_decoded_profile_projects_through_each_selected_public_schema(self):
        import spine_packs.facet_execution as execution
        f = planning_fixture(); owner = f['plan']['request']['owner']
        row = next(r for r in f['plan']['observation']['entries']
                   if r['revision_contract'] == 'spine.notification-profiles.v1')
        for runtime in BASELINES:
            with self.subTest(runtime=runtime), patch.object(execution, 'validate', wraps=execution.validate) as checked:
                self.assertEqual(projected_state(row, owner, runtime_version=runtime), body(row['value']))
                self.assertIn(((BASELINES[runtime].public_schema, 'semantic_profile_v1')),
                              [(call.args[1], call.args[2]) for call in checked.call_args_list])
                changed = deepcopy(row); value = body(changed['value'])
                value['revision']['templates'][0]['rendering'] = {'unexpected': 'v2-only'}
                changed['value'] = blob(value)
                with self.assertRaises(PlanError): projected_state(changed, owner, runtime_version=runtime)

    def test_every_response_loss_continues_exact_requests_with_durable_prefix(self):
        import spine_packs.facet_apply as applying
        import spine_packs.facet_recovery as recovery
        commands = set()
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name)
            for n, expected in enumerate(f['accepted_responses']):
                with self.subTest(command=expected['command']):
                    source = prepared(f, n); before = deepcopy(source); durable = []
                    t = AlignedCatalog(f, n, f['observations'][n+1], lost=True)
                    def write_checkpoint(value): durable.append(deepcopy(value))
                    def before_write(index):
                        self.assertIsNotNone(durable[-1]['unresolved_submission'])
                        self.assertEqual(len(durable[-1]['accepted_responses']), n + index)
                    t.before_write = before_write
                    with patch.object(applying, 'validate', wraps=applying.validate) as readback, \
                            patch.object(recovery, 'validate', wraps=recovery.validate) as candidate:
                        applied = apply_continuation(f['manifest'], f['plan'], f['approval'], source, t, write_checkpoint)
                    for spy in (readback, candidate):
                        public = [call.args[1] for call in spy.call_args_list
                                  if call.args[1].startswith('spine-readback-')]
                        if spy is readback or expected['command'] in (
                                'item_archetype.create', 'item_archetype.revise',
                                'notification_rendering_definition.create',
                                'notification_rendering_definition.publish'):
                            self.assertTrue(public)
                        self.assertLessEqual(set(public), {'spine-readback-0.12.0.schema.json'})
                    self.assertEqual(applied['state'], 'applied'); self.assertEqual(source, before)
                    self.assertEqual(t.writes[0], (expected['command'], body(expected['request'])))
                    self.assertEqual(durable[-1]['next_action_id'], None)
                    self.assertEqual(len(durable[-1]['accepted_responses']), len(f['plan']['actions']))
                    commands.add(expected['command'])
        self.assertEqual(len(commands), 11)

    def test_cross_baseline_plan_approval_and_sources_fail_before_transport(self):
        new = aligned_flow('flight-update')
        old = historical_flow('tests/fixtures/installer-v2/fr4-flight-update-0.10.0.json')
        for fault in ('environment', 'approval', 'checkpoint', 'partial'):
            f = deepcopy(new); source = prepared(f, 3)
            if fault == 'environment':
                f['plan']['environment'] = old['plan']['environment']; f['plan'] = seal(f['plan'])
                f['approval']['plan_digest'] = f['plan']['content_identity']['digest']; f['approval'] = seal(f['approval'])
            elif fault == 'approval': f['approval'] = old['approval']
            else: source = old['prepared_checkpoint' if fault == 'checkpoint' else 'partial_result']
            t, writer = Mock(), Mock()
            with self.subTest(fault=fault), self.assertRaises(PlanError):
                apply_continuation(f['manifest'], f['plan'], f['approval'], source, t, writer)
            self.assertEqual(t.mock_calls, []); writer.assert_not_called()

    def test_wrong_fresh_environment_stops_apply_continuation_and_verify(self):
        for operation, index in (('initial', 0), ('continue', 3), ('verify', 6)):
            f = aligned_flow('flight-create'); t = AlignedCatalog(f, index, f['observations'][index]); original = t.read
            def changed(command, request):
                response = original(command, request)
                if command == 'system.info': response['ledger_schema_version'] = '19'
                return response
            t.read = changed; writer = Mock()
            with self.subTest(operation=operation):
                if operation == 'initial':
                    value = apply_initial(f['manifest'], f['plan'], f['approval'], t, writer)
                    self.assertEqual(value['state'], 'not_applied')
                    self.assertEqual(value['failure']['error']['category'], 'incompatible_spine_runtime_or_contracts')
                elif operation == 'continue':
                    with self.assertRaises(PlanError):
                        apply_continuation(f['manifest'], f['plan'], f['approval'], prepared(f, 3), t, writer)
                else:
                    with self.assertRaises(PlanError):
                        verify_installation(f['manifest'], f['plan'], t, f['apply_result'])
            self.assertEqual(t.writes, []); writer.assert_not_called()

    def test_invalid_old_result_and_both_flow_evidence_distinguish_missing_and_corrupt(self):
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name)
            old = historical_flow('tests/fixtures/installer-v2/fr4-' + name + '-0.10.0.json')
            invalid = deepcopy(f['apply_result'])
            evidence = invalid['checkpoint']['accepted_responses'][0]
            response = json.loads(evidence['response']['json_text'])
            response['receipt']['command_id'] = 'synthetic-wrong-command'
            text = json.dumps(response, separators=(',', ':'))
            evidence['response'] = dict(json_text=text, digest=oracle.sha(text.encode()))
            invalid['checkpoint'] = seal(invalid['checkpoint']); invalid = seal(invalid)
            for supplied, coverage in ((None, 'missing'), (old['apply_result'], 'invalid'), (invalid, 'invalid')):
                t = AlignedCatalog(f, 6, f['observations'][-1])
                value = verify_installation(f['manifest'], f['plan'], t, supplied)
                self.assertEqual((value['state'], value['response_evidence']), ('mismatch', coverage))
                self.assertEqual(t.writes, [])
            fresh = deepcopy(f['observations'][-1])
            row = next(r for r in fresh['entries'] if r['object_key'].startswith('schema:'))
            value = body(row['value']); value['display_name'] = 'Conflicting immutable body'; row['value'] = blob(value)
            reseal_view(fresh)
            with self.assertRaisesRegex(PlanError, 'immutable_revision_contradiction') as caught:
                verify_installation(f['manifest'], f['plan'], AlignedCatalog(f, 6, fresh), f['apply_result'])
            self.assertEqual(caught.exception.category, ENVIRONMENT)

    def test_public_write_adapter_routes_all_eleven_responses_and_requests(self):
        import spine_packs.facet_apply_transport as adapter_module
        seen = set()
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name)
            for e in f['accepted_responses']:
                transport = FacetApplyCommand(f['plan']['request']['target'], runtime_version='0.12.0')
                raw = e['response']['json_text'].encode() + b'\n'
                def invoke(command, request):
                    transport._received(raw)
                    return json.loads(raw), 0
                with patch.object(transport, '_invoke', side_effect=invoke), \
                        patch.object(adapter_module, 'validate', wraps=adapter_module.validate) as checked:
                    self.assertEqual(transport.write(e['command'], body(e['request'])), raw)
                    self.assertEqual({call.args[1] for call in checked.call_args_list},
                                     {'spine-readback-0.12.0.schema.json'})
                seen.add(e['command'])
        self.assertEqual(len(seen), 11)

    def test_exact_revision_failure_mapping_and_capacity_do_not_become_absence(self):
        f = cross_root()
        request = next(r['request'] for r in f['reads'] if r['command'] == 'facet_schema.revision.show')
        for code, field, exit_code, category in (
                ('referenced_row_not_found', 'facet_schema_revision_id', 4, 'spine_command_rejection'),
                ('environment_failure', 'facets', 7, ENVIRONMENT),
                ('environment_failure', 'capacity', 7, ENVIRONMENT),
                ('invalid_request', 'facet_schema_revision_id', 2, 'spine_command_rejection')):
            transport = FacetSpineCommand({}, runtime_version='0.12.0'); transport.budget = ObservationBudget()
            response = dict(ok=False, command='facet_schema.revision.show',
                            error=dict(code=code, field=field, message='PRIVATE_SENTINEL'))
            with self.subTest(code=code, field=field), patch.object(transport, '_invoke', return_value=(response, exit_code)):
                with self.assertRaises(PlanError) as caught: transport.read('facet_schema.revision.show', request)
                self.assertEqual(caught.exception.category, category)
                self.assertNotIn('PRIVATE_SENTINEL', str(caught.exception))
        transport.budget.calls = 4096
        with patch.object(transport, '_invoke') as invoke:
            with self.assertRaisesRegex(PlanError, 'observation_capacity'):
                transport.read('facet_schema.revision.show', request)
            invoke.assert_not_called()

    def test_terminal_partial_and_complete_checkpoint_admission_and_drift_refusal(self):
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name); n = len(f['partial_result']['checkpoint']['accepted_responses'])
            saved = []
            value = apply_continuation(f['manifest'], f['plan'], f['approval'], f['partial_result'],
                AlignedCatalog(f, n, f['observations'][n]), saved.append)
            self.assertEqual(value['state'], 'applied'); self.assertEqual(saved[-1]['next_action_id'], None)
            writer = Mock(); t = AlignedCatalog(f, 6, f['observations'][-1])
            self.assertEqual(apply_continuation(f['manifest'], f['plan'], f['approval'],
                f['final_checkpoint'], t, writer), f['apply_result'])
            self.assertEqual(t.writes, []); writer.assert_called_once()
            changed = deepcopy(f['observations'][-1])
            row = next(r for r in changed['entries'] if r['object_key'].startswith('facet_binding:'))
            row['binding_id'] = 'synthetic-later-binding'; reseal_view(changed)
            t = AlignedCatalog(f, 6, changed); writer = Mock()
            with self.assertRaisesRegex(PlanError, 'unexplained_recovery_change'):
                apply_continuation(f['manifest'], f['plan'], f['approval'], f['final_checkpoint'], t, writer)
            writer.assert_not_called(); self.assertEqual(t.writes, [])

    def test_cli_apply_continue_and_verify_keep_private_artifacts_and_exact_label(self):
        helper = cli_tests.FacetCLITests(); helper.setUp(); self.addCleanup(helper.doCleanups)
        for name in ('flight-create', 'flight-update'):
            f = aligned_flow(name)
            args, paths = helper.inputs(f, 'apply')
            self.assertEqual(helper.invoke(args, AlignedCatalog(f, 0, f['observations'][0]))[0], 0)
            self.assertEqual(artifacts.load_json(paths['output']), f['apply_result'])
            args, paths = helper.inputs(f, 'apply', source=prepared(f, 3))
            before = paths['source'].read_bytes()
            self.assertEqual(helper.invoke(args, AlignedCatalog(f, 3, f['observations'][4], lost=True))[0], 0)
            self.assertEqual(paths['source'].read_bytes(), before)
            self.assertEqual(artifacts.load_json(paths['output'])['state'], 'applied')
            args, paths = helper.inputs(f, 'verify', applied=f['apply_result'])
            t = AlignedCatalog(f, 6, f['observations'][-1]); t.write = Mock(side_effect=AssertionError('read-only'))
            self.assertEqual(helper.invoke(args, t)[0], 0)
            verified = artifacts.load_json(paths['output'])
            self.assertEqual(verified['receipt_readback'], 'captured_responses_only_spine_0.12.0')
            self.assertEqual(verified['state'], 'verified'); t.write.assert_not_called()
            self.assertEqual(paths['output'].stat().st_mode & 0o777, 0o600)

    def test_cli_plan_and_mixed_baseline_approval_rejection_before_factory(self):
        f = cross_root()
        # Replay the same small pages under the CLI's default requested ceiling.
        for row in f['reads']:
            if 'limit' in row['request']: row['request']['limit'] = '100'
            if 'limit' in row['response']: row['response']['limit'] = '100'
        t = Replay(f)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = root/'manifest'; request = root/'request'; output = root/'plan'
            manifest.write_text(artifacts.canonical_text(f['manifest'])); request.write_text(artifacts.canonical_text(f['request']))
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                code = main(['plan', '--manifest', str(manifest), '--request', str(request), '--output', str(output)],
                            transport_factory=lambda target:t)
            self.assertEqual(code, 5, stdout.getvalue())
            self.assertEqual(json.loads(stdout.getvalue())['exit_code'], '5')
            self.assertEqual(artifacts.load_json(output), f['plan'])
        helper = cli_tests.FacetCLITests(); helper.setUp(); self.addCleanup(helper.doCleanups)
        f = aligned_flow('flight-create')
        f['approval'] = historical_flow('tests/fixtures/installer-v2/fr4-flight-create-0.10.0.json')['approval']
        args, paths = helper.inputs(f, 'apply'); factory = Mock()
        code, _ = helper.invoke(args, factory=factory)
        self.assertEqual(code, 2); factory.assert_not_called()
        self.assertFalse(paths['checkpoint'].exists()); self.assertFalse(paths['output'].exists())


if __name__ == '__main__': unittest.main()
