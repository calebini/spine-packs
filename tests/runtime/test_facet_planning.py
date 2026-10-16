"""FR-2 replay/fault injection against bounded public-CLI synthetic evidence."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from spine_packs import artifacts as a
from spine_packs.__main__ import main
from spine_packs.facet_contracts import body, blob, seal
from spine_packs.facet_inventory import COMMANDS, CONTRACTS, READ_COMMANDS
from spine_packs.facet_manifest import digest as manifest_digest, validate as validate_manifest, rendering_size_floor
from spine_packs.facet_observation import Observer, state, snapshots
from spine_packs.facet_planning import build_plan, plan_installation
from spine_packs.facet_transport import FacetSpineCommand, ObservationBudget
from spine_packs.planning import PlanError, ENVIRONMENT, PACK_INVALID

FIXTURE = ROOT / 'tests/fixtures/installer-v2/fr2-cross-root.json'
CURSORS = {'SPINE_FACET_CURSOR_CONFIG': '/synthetic/protected-facet',
           'SPINE_RENDERING_CURSOR_CONFIG': '/synthetic/protected-rendering'}


def fixture():
    return json.loads(FIXTURE.read_text())


class Replay(FacetSpineCommand):
    def __init__(self, fixture, mutate=None):
        super().__init__(fixture['request']['request']['target'])
        self.rows = deepcopy(fixture['reads']); self.calls = []; self.mutate = mutate

    def check_target(self):
        pass

    def _invoke(self, command, request):
        if self.mutate and (self.rows[0]['command'], self.rows[0]['request']) != (command, request):
            # Faults such as a premature terminal page legitimately skip later
            # page/show calls. Supply only an exact saved request, never fabricate.
            index = next(i for i, row in enumerate(self.rows) if (row['command'], row['request']) == (command, request))
            self.rows = self.rows[index:]
        row = self.rows.pop(0)
        assert (row['command'], row['request']) == (command, request), (command, request)
        self.calls.append(command)
        response = row['response']; code = 0
        if self.mutate:
            response, code = self.mutate(command, request, response, len(self.calls))
        self._received(json.dumps(response).encode())
        return response, code


class FacetPlanningTests(unittest.TestCase):
    def run_plan(self, f=None, mutate=None):
        f = fixture() if f is None else f
        adapter = Replay(f, mutate)
        with patch.dict('os.environ', CURSORS):
            plan = plan_installation(f['manifest'], f['request'], adapter, page_size=1)
        return plan, adapter

    def test_cross_root_history_dedup_and_determinism(self):
        f = fixture(); plan, adapter = self.run_plan(f)
        self.assertEqual(plan, f['plan']); self.assertFalse(adapter.rows)
        self.assertEqual(adapter.calls.count('facet_schema.revision.show'), 2)
        self.assertEqual(set(adapter.calls), READ_COMMANDS)
        history = plan['observation']['historical_revisions'][0]
        self.assertEqual(history['object_key'], 'schema:legacy_details')
        desired = next(r for r in plan['resolutions'] if r['object_key'] == 'schema:flight_details')
        self.assertNotEqual(history['root_id'], desired['root']['value'])
        self.assertEqual([r['command'] for r in plan['actions']], [
            'item_archetype.facet_binding.set', 'notification_rendering_definition.publish', 'notification_profile.revise'])

    def test_exact_current_and_retired_lookup_and_cache(self):
        f = fixture(); read = next(r for r in f['reads'] if r['command'] == 'facet_schema.revision.show')
        current = next(r['response'] for r in f['reads'] if r['command'] == 'facet_schema.show'
                       and r['response']['root']['facet_schema_id'] == read['response']['root']['facet_schema_id'])
        for retired in (False, True):
            old, now = deepcopy(read['response']), deepcopy(current)
            if retired: old['root']['status'] = now['root']['status'] = 'retired'
            class Exact:
                calls = 0
                def read(self, command, request):
                    self.calls += 1
                    self_response = now if request['facet_schema_revision_id'] == now['revision']['facet_schema_revision_id'] else old
                    return dict(self_response, command=command, response_contract='spine.facet-schema-revision-readback.v1')
            transport = Exact(); observer = Observer(transport, f['request']['request']['owner'], [])
            row = state('schema', now, observer.owner)
            observer.add(row); observer.raw[row['object_key']] = now
            for identity in (now['revision']['facet_schema_revision_id'], old['revision']['facet_schema_revision_id']):
                first = observer.schema_revision(identity)
                self.assertEqual(first, observer.schema_revision(identity))
            self.assertEqual(transport.calls, 2); self.assertEqual(len(observer.history), 1)

    def test_revision_evidence_mismatches_abort(self):
        for fault in ('owner', 'root', 'requested', 'hash', 'definition', 'current', 'status', 'number', 'extra', 'dry_run'):
            def mutate(command, request, response, n):
                if command == 'facet_schema.revision.show':
                    if fault == 'owner': response['root']['owner']['owner_subject_id'] = 'other'
                    elif fault == 'root': response['revision']['facet_schema_id'] = 'wrong-root'
                    elif fault == 'requested': response['revision']['facet_schema_revision_id'] = 'wrong-revision'
                    elif fault == 'hash': response['revision']['definition_hash'] = '0' * 64
                    elif fault == 'definition': response['revision']['definition']['display_name'] += ' changed'
                    elif fault == 'current': response['root']['current_revision_id'] = 'wrong-current'
                    elif fault == 'status': response['root']['status'] = 'retired'
                    elif fault == 'number': response['revision']['revision_number'] = '0'
                    elif fault == 'extra': response['revision']['guessed_owner'] = 'wrong'
                    else: response['dry_run'] = True
                return response, 0
            with self.subTest(fault=fault), self.assertRaises(PlanError): self.run_plan(mutate=mutate)

    def test_missing_corrupt_capacity_invalid_and_preflight_never_absence(self):
        for code, field, exit_code, category in (
            ('referenced_row_not_found', 'facet_schema_revision_id', 4, 'spine_command_rejection'),
            ('environment_failure', 'facets', 7, ENVIRONMENT),
            ('environment_failure', 'capacity', 7, ENVIRONMENT),
            ('invalid_request', 'facet_schema_revision_id', 2, 'spine_command_rejection'),
            ('environment_failure', 'ledger', 7, 'spine_command_rejection'),
            ('environment_failure', 'runtime_contracts', 7, 'spine_command_rejection'),
            ('invalid_request', 'db', 3, 'spine_command_rejection'),
            ('invalid_request', 'input', 3, 'spine_command_rejection'),
            ('invalid_request', 'request', 2, 'spine_command_rejection'),
        ):
            def mutate(command, request, response, n):
                if command == 'facet_schema.revision.show':
                    return dict(ok=False, command=command, error=dict(code=code, field=field, message='secret not echoed')), exit_code
                return response, 0
            with self.subTest(code=code, field=field), self.assertRaises(PlanError) as caught:
                self.run_plan(mutate=mutate)
            self.assertEqual(caught.exception.category, category)
            self.assertNotIn('secret', str(caught.exception))

    def test_malformed_handler_and_preflight_failures_are_environment_failures(self):
        command = 'facet_schema.revision.show'
        request = next(r['request'] for r in fixture()['reads'] if r['command'] == command)
        for fault in ('wrong_field', 'wrong_exit', 'unsupported_exit', 'zero_exit', 'missing_error',
                      'extra', 'missing_message', 'empty_message', 'unknown_code', 'error_type',
                      'preflight_extra', 'preflight_exit', 'preflight_field'):
            response = dict(ok=False, command=command, error=dict(
                code='referenced_row_not_found', field='facet_schema_revision_id', message='secret'))
            exit_code = 4
            if fault == 'wrong_field': response['error']['field'] = 'facets'
            elif fault == 'wrong_exit': exit_code = 7
            elif fault == 'unsupported_exit': exit_code = 99
            elif fault == 'zero_exit': exit_code = 0
            elif fault == 'missing_error': del response['error']
            elif fault == 'extra': response['unexpected'] = True
            elif fault == 'missing_message': del response['error']['message']
            elif fault == 'empty_message': response['error']['message'] = ''
            elif fault == 'unknown_code': response['error']['code'] = 'invented'
            elif fault == 'error_type': response['error'] = 'secret'
            else:
                response['error'].update(code='invalid_request', field='db'); exit_code = 3
                if fault == 'preflight_extra': response['error']['unexpected'] = True
                elif fault == 'preflight_exit': exit_code = 4
                else: response['error']['field'] = 'invented'
            adapter = Replay(fixture()); adapter.budget = ObservationBudget()
            with self.subTest(fault=fault), patch.object(adapter, '_invoke', return_value=(response, exit_code)):
                with self.assertRaises(PlanError) as caught: adapter.read(command, request)
                self.assertEqual(caught.exception.category, ENVIRONMENT)
                self.assertNotEqual(caught.exception.code, 'referenced_revision_missing')
                self.assertNotIn('secret', str(caught.exception))

    def sized_rendering(self, f, size, known=None):
        """Independent wire-byte oracle, including multi-byte author text."""
        revision = f['manifest']['rendering_definitions'][0]['revision']
        revision['display_name'] = '\U0001f680' * 160
        revision['description'] = ''
        wire = deepcopy(revision)
        for selection in wire['selections']:
            key = selection.pop('schema_ref')['schema_key']
            selection['facet_schema_revision_id'] = (known or {}).get(key, 'x')
        remaining = size - len(json.dumps(wire, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        revision['description'] = '\U0001f680' * (remaining // 4) + 'a' * (remaining % 4)
        self.assertLessEqual(len(revision['description']), 2000)
        wire['description'] = revision['description']
        self.assertEqual(len(json.dumps(wire, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()), size)
        f['manifest']['content_identity']['digest'] = manifest_digest(f['manifest'])
        return revision

    def test_intrinsic_rendering_bytes_before_any_observation(self):
        for size in (8192, 8193):
            f = fixture(); self.sized_rendering(f, size)
            adapter = Replay(f)
            if size == 8192:
                validate_manifest(f['manifest'])
            else:
                with self.assertRaises(PlanError) as caught:
                    plan_installation(f['manifest'], f['request'], adapter)
                self.assertEqual(caught.exception.category, PACK_INVALID)
                self.assertFalse(adapter.calls)
        f = fixture(); revision = f['manifest']['rendering_definitions'][0]['revision']
        revision.update(display_name='\U0001f680' * 160, description='\U0001f680' * 2000)
        f['manifest']['content_identity']['digest'] = manifest_digest(f['manifest'])
        with self.assertRaises(PlanError): validate_manifest(f['manifest'])

    def test_resolved_rendering_byte_boundary(self):
        for size in (8192, 8193):
            f = fixture()
            schema = next(r for r in f['plan']['observation']['entries'] if r['object_key'] == 'schema:flight_details')
            known = {'flight_details': schema['revision_id']}
            self.sized_rendering(f, size, known)
            validate_manifest(f['manifest'])  # Only actual IDs expose this overflow.
            if size == 8192:
                plan, _ = self.run_plan(f)
                self.assertTrue(plan['apply_eligible'])
            else:
                with self.assertRaises(PlanError) as caught: self.run_plan(f)
                self.assertEqual(caught.exception.category, PACK_INVALID)
                self.assertEqual(caught.exception.code, 'rendering_definition_too_large')

    def test_unknown_ids_remain_slots_and_local_key_bytes_are_not_wire_bytes(self):
        f = fixture(); revision = self.sized_rendering(f, 8192)
        empty = dict(owner=f['plan']['observation']['owner'], entries=[], historical_revisions=[],
                     public_catalog_snapshots=snapshots([]))
        empty['digest'] = a.digest(dict(derivation_version='spine.pack-observation.v2', view=empty))
        plan = build_plan(f['manifest'], f['request'], f['plan']['environment'], empty)
        action = next(r for r in plan['actions'] if r['command'] == 'notification_rendering_definition.create')
        self.assertTrue(all(s['facet_schema_revision_id'] is None
                            for s in body(action['request_template'])['revision']['selections']))
        for selection in revision['selections']: selection['schema_ref']['schema_key'] = 'a' * 64
        self.assertEqual(rendering_size_floor(revision, {'a' * 64: 'x'}), 8192)
        self.assertGreater(len(a.canonical_text(revision).encode()), 8192)
        # Mixed known/unknown references count known bytes without predicting the rest.
        revision['selections'][1]['schema_ref']['schema_key'] = 'b'
        self.assertEqual(rendering_size_floor(revision, {'a' * 64: 'abc'}), 8194)

    def test_pagination_owner_hash_order_staleness_fail_closed(self):
        for fault in ('missing_page', 'duplicate', 'owner', 'hash', 'second_pass', 'cursor_cycle', 'show_mismatch'):
            first_cursor = None
            def mutate(command, request, response, n):
                nonlocal first_cursor
                if command == 'notification_profile.list':
                    if fault == 'missing_page': response['has_more'] = False; response['next_cursor'] = None
                    elif fault == 'duplicate': response['entries'] *= 2; response['count'] = '2'
                    elif fault == 'owner': response['entries'][0]['owner']['owner_subject_id'] = 'other'
                    elif fault == 'hash': response['catalog_snapshot_hash'] = '0' * 64
                    elif fault == 'cursor_cycle' and response['next_cursor']:
                        first_cursor = first_cursor or response['next_cursor']; response['next_cursor'] = first_cursor
                if fault == 'second_pass' and n == len(fixture()['reads']):
                    response['ledger_instance_id'] = 'other-ledger'
                if fault == 'show_mismatch' and command == 'notification_profile.show':
                    response['notification_profile']['display_name'] = 'Changed'
                return response, 0
            with self.subTest(fault=fault), self.assertRaises(PlanError): self.run_plan(mutate=mutate)

    def test_global_budgets_and_write_denial(self):
        budget = ObservationBudget(clock=lambda: 0)
        budget.calls = 4096
        with self.assertRaises(PlanError): budget.start_call()
        budget.calls = 0; budget.bytes = 128 * 1024 * 1024
        with self.assertRaises(PlanError): budget.received(b'x')
        budget.deadline = 0
        with self.assertRaises(PlanError): budget.start_call()
        adapter = Replay(fixture())
        for name in set(COMMANDS) - READ_COMMANDS | {'item.create', 'disclosure.set'}:
            with self.assertRaises(PlanError): adapter.read(name, {})
            with self.assertRaises(PlanError): adapter.write(name, {})
        self.assertFalse(adapter.calls)
        with patch.dict('os.environ', {}, clear=True), self.assertRaises(PlanError):
            adapter.begin_observation(ObservationBudget())

    def test_entry_and_facet_resource_capacities(self):
        f = fixture(); observer = Observer(None, f['request']['request']['owner'], [])
        row = deepcopy(f['plan']['observation']['entries'][0])
        for n in range(4096): observer.add(dict(row, object_key=f'archetype:k{n}'))
        with self.assertRaises(PlanError): observer.add(dict(row, object_key='archetype:overflow'))

    def test_revision_response_byte_cap_and_transport_failure(self):
        adapter = Replay(fixture()); adapter.budget = ObservationBudget()
        adapter.response_limit = 4 * 1024 * 1024; adapter.response_bytes = adapter.response_limit
        with self.assertRaises(PlanError): adapter._received(b'x')
        def timeout(command, request, response, n):
            if command == 'facet_schema.revision.show': raise PlanError(ENVIRONMENT, 'spine_timeout')
            return response, 0
        with self.assertRaises(PlanError): self.run_plan(mutate=timeout)

    def test_exact_baseline_and_content_contract_preflight(self):
        f = fixture()
        for version in ('0.9.1', '0.10.1'):
            def mutate(command, request, response, n):
                if command == 'system.info': response['runtime_version'] = version
                return response, 0
            with self.assertRaises(PlanError): self.run_plan(mutate=mutate)
        for contract in (CONTRACTS[3], 'spine.notification-rendering.v1'):
            def mutate(command, request, response, n):
                if command == 'system.info': response['implemented_contract_versions'].remove(contract)
                return response, 0
            with self.assertRaises(PlanError): self.run_plan(mutate=mutate)
        f['manifest']['compatibility']['spine_runtime_versions'] = ['0.9.1']
        f['manifest']['content_identity']['digest'] = manifest_digest(f['manifest'])
        with self.assertRaises(PlanError): self.run_plan(f)

    def test_classification_missing_retained_retired_and_cascade(self):
        f = fixture(); m, request = f['manifest'], f['request']; plan = f['plan']
        empty = dict(owner=plan['observation']['owner'], entries=[], historical_revisions=[],
                     public_catalog_snapshots=snapshots([]))
        empty['digest'] = a.digest(dict(derivation_version='spine.pack-observation.v2', view=empty))
        created = build_plan(m, request, plan['environment'], empty)
        self.assertEqual(len(created['actions']), 6)
        for key in ('schema:flight_details', 'archetype:flight'):
            view = deepcopy(plan['observation']); row = next(r for r in view['entries'] if r['object_key'] == key)
            row['status'] = 'retired'
            blocked = build_plan(m, request, plan['environment'], view)
            self.assertFalse(blocked['apply_eligible']); self.assertIn(key, blocked['blocked_object_keys'])
        view = deepcopy(plan['observation']); schema = next(r for r in view['entries'] if r['object_key'] == 'schema:flight_details')
        rev = schema['revision_id']
        for row in view['entries']:
            value = body(row['value'])
            if row['object_key'] == 'facet_binding:flight:flight': value['facet_schema_revision_id'] = rev
            if row['object_key'] == 'rendering:flight_details':
                for selection in value['selections']: selection['facet_schema_revision_id'] = rev
            row['value'] = blob(value)
        retained = build_plan(m, request, plan['environment'], view)
        self.assertFalse(retained['actions']); self.assertTrue(all(c['classification'] == 'equivalent' for c in retained['classifications']))

    def test_cli_dispatch_no_successor_apply_verify_or_output_on_failure(self):
        f = fixture()
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); manifest = base / 'manifest.json'; request = base / 'request.json'
            manifest.write_text(json.dumps(f['manifest'])); request.write_text(json.dumps(f['request']))
            for operation in ('apply', 'verify'):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = main([operation, '--manifest', str(manifest), '--output', str(base / operation)],
                                transport_factory=lambda target: self.fail('unauthorized target access'))
                self.assertEqual(code, 2); self.assertFalse((base / operation).exists())
            def fail(command, request, response, n):
                raise PlanError(ENVIRONMENT, 'injected_failure')
            with patch.dict('os.environ', CURSORS), contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(['plan', '--manifest', str(manifest), '--request', str(request), '--output', str(base / 'plan')],
                            transport_factory=lambda target: Replay(f, fail))
            self.assertEqual(code, 11); self.assertFalse((base / 'plan').exists())
            self.assertEqual(json.loads(output.getvalue())['artifact_schema'], 'spine.pack-installer-result.v2')

    def test_ordinary_v1_equivalence_keeps_original_decoder(self):
        f = fixture(); manifest = f['manifest']; view = f['plan']['observation']
        for template in manifest['notification_profiles'][0]['revision']['templates']:
            template['rendering'] = {'kind': 'ordinary'}
        manifest['content_identity']['digest'] = manifest_digest(manifest)
        row = next(r for r in view['entries'] if r['object_key'] == 'profile:synthetic_flight_details')
        value = body(row['value'])
        for template in value['revision']['templates']: template.pop('rendering')
        row['value'] = blob(value); row['revision_contract'] = 'spine.notification-profiles.v1'
        plan = build_plan(manifest, f['request'], f['plan']['environment'], view)
        classified = next(c for c in plan['classifications'] if c['object_key'] == row['object_key'])
        self.assertEqual(classified['classification'], 'equivalent')
        self.assertEqual(classified['observed'], row)


if __name__ == '__main__': unittest.main()
