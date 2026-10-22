"""FR-4 read-only prefix foundation; synthetic public wire evidence, no ledger."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from spine_packs import artifacts as a
from spine_packs.facet_apply import checkpoint
from spine_packs.facet_contracts import blob, body, seal
from spine_packs.facet_inventory import COMMANDS, READ_COMMANDS
from spine_packs.facet_observation import FAMILIES, Observer, observe, state
from spine_packs.facet_recovery import RecoveryPreimage, forward_view, immutable_lineage
from spine_packs.planning import ENVIRONMENT, PlanError
from test_facet_execution import flow
from test_facet_planning import CURSORS, Replay, fixture


def companion(name):
    return json.loads((ROOT / f'tests/fixtures/installer-v2/fr4-{name}-0.10.0.json').read_text())


def context(f, cp):
    return RecoveryPreimage(f['manifest'], f['plan'], f['approval'], cp)


def projection(view):
    return {k: deepcopy(v) for k, v in view.items() if k not in ('digest', 'public_catalog_snapshots')}


class PrefixTests(unittest.TestCase):
    def test_every_exact_prefix_and_prepared_boundary_matches_independent_fixture(self):
        with patch('subprocess.Popen', side_effect=AssertionError('no processes')):
            for name in ('flight-create', 'flight-update'):
                f = flow(name); original = deepcopy(f); views = companion(name)['observations']
                for n, view in enumerate(views):
                    cp = checkpoint(f['plan'], f['approval'], f['accepted_responses'][:n])
                    c = context(f, cp)
                    self.assertEqual(c.expected_view(), projection(view))
                    self.assertTrue(c.compare_prefix(view, environment=f['plan']['environment'],
                                                     target=f['plan']['request']['target']))
                    if n < len(f['accepted_responses']):
                        request = c.materialize(cp['accepted_responses'])
                        cp['unresolved_submission'] = dict(action_id=cp['next_action_id'],
                            command_id=request['command_id'], submission_state='prepared_or_submitted', request=blob(request))
                        c = context(f, seal(cp))
                        self.assertTrue(c.compare_prefix(view, environment=f['plan']['environment'],
                                                         target=f['plan']['request']['target']))
                        with self.assertRaisesRegex(PlanError, 'recovery_prefix_changed'):
                            c.compare_prefix(views[n + 1], environment=f['plan']['environment'],
                                             target=f['plan']['request']['target'])
                self.assertEqual(f, original)

    def test_checkpoint_identity_prefix_and_pending_request_fail_closed(self):
        for fault in ('digest', 'plan', 'approval', 'execution', 'gap', 'next', 'action', 'command',
                      'request', 'wire', 'receipt', 'post'):
            f = flow('flight-update'); cp = deepcopy(f['prepared_checkpoint'])
            if fault == 'plan': cp['plan_digest'] = '0' * 64
            elif fault == 'approval': cp['approval_digest'] = '0' * 64
            elif fault == 'execution': cp['execution']['execution_id'] = 'different'
            elif fault == 'gap': cp['accepted_responses'] = f['accepted_responses'][1:2]
            elif fault == 'next': cp['next_action_id'] = 'action-000005'
            elif fault == 'action': cp['unresolved_submission']['action_id'] = 'action-000005'
            elif fault == 'command': cp['unresolved_submission']['command_id'] = 'wrong'
            elif fault == 'request':
                request = body(cp['unresolved_submission']['request']); request['actor_subject_id'] = 'other'
                cp['unresolved_submission']['request'] = blob(request)
            elif fault == 'wire': cp['accepted_responses'][0]['response']['json_text'] += ' '
            elif fault == 'receipt': cp['accepted_responses'][0]['receipt']['command_receipt_id'] = 'wrong'
            elif fault == 'post': cp['accepted_responses'][0]['post_observation']['root_id'] = 'wrong'
            cp = seal(cp)
            if fault == 'digest': cp['content_identity']['digest'] = '0' * 64
            with self.subTest(fault=fault), self.assertRaises(PlanError): context(f, cp)
        for bad in (None, [], 'private-sentinel'):
            with self.assertRaises(PlanError): context(flow(), bad)

    def test_completed_checkpoint_cannot_have_a_pending_submission(self):
        f = flow(); cp = deepcopy(f['final_checkpoint'])
        cp['unresolved_submission'] = f['prepared_checkpoint']['unresolved_submission']
        with self.assertRaises(PlanError): context(f, seal(cp))

    def test_private_copies_and_no_fabricated_public_fingerprints(self):
        f = flow('flight-update'); c = context(f, f['final_checkpoint']); expected = c.expected_view()
        self.assertNotIn('digest', expected); self.assertNotIn('public_catalog_snapshots', expected)
        c.expected_view()['entries'].clear(); c.lineage().clear()
        f['plan']['actions'].clear(); f['final_checkpoint']['accepted_responses'].clear()
        self.assertEqual(c.expected_view(), expected)
        old_keys = {r['object_key'] for r in c.lineage()}
        self.assertTrue({'archetype:flight', 'schema:flight_details',
                         'rendering:flight_details', 'profile:synthetic_flight_details'} <= old_keys)

    def test_target_environment_and_unrelated_drift_fail_closed(self):
        f = flow(); c = context(f, f['final_checkpoint']); good = companion('flight-create')['observations'][-1]
        for fault in ('target', 'environment', 'status', 'owner', 'digest', 'snapshots', 'missing_history'):
            view = deepcopy(good); env = deepcopy(f['plan']['environment']); target = deepcopy(f['plan']['request']['target'])
            if fault == 'target': target['host_name'] = 'other.invalid'
            elif fault == 'environment': env['ledger_instance_id'] = 'other'
            elif fault == 'status': view['entries'][0]['status'] = 'retired'
            elif fault == 'owner': view['entries'][0]['owner']['owner_subject_id'] = 'other'
            elif fault == 'snapshots': view['public_catalog_snapshots'][0]['digest'] = '0' * 64
            elif fault == 'missing_history': view['historical_revisions'] = [view['entries'][0]]
            view['digest'] = a.digest(dict(derivation_version='spine.pack-observation.v2',
                view={k: v for k, v in view.items() if k != 'digest'}))
            if fault == 'digest': view['digest'] = '0' * 64
            with self.subTest(fault=fault), self.assertRaises(PlanError):
                c.compare_prefix(view, environment=env, target=target)

    def test_immutable_revision_cannot_change_root_decoder_or_content(self):
        f = flow('flight-update'); rows = companion('flight-update')['observations'][-1]['historical_revisions']
        for original in rows:
            for fault in ('root', 'decoder', 'content'):
                changed = deepcopy(original)
                if fault == 'root': changed['root_id'] = 'other'
                elif fault == 'decoder': changed['revision_contract'] = 'other'
                else:
                    value = body(changed['value'])
                    if original['object_key'].startswith('profile:'): value['revision']['compatible_item_types'] = ['task']
                    else: value['display_name'] = 'Changed'
                    changed['value'] = blob(value)
                with self.subTest(object=original['object_key'], fault=fault), self.assertRaisesRegex(
                        PlanError, 'immutable_revision_contradiction'):
                    immutable_lineage([original, changed])
        profile = next(r for r in rows if r['object_key'].startswith('profile:'))
        changed = deepcopy(profile); value = body(changed['value']); value['metadata']['display_name'] = 'New metadata'
        changed['value'] = blob(value)
        immutable_lineage([profile, changed])  # Metadata is mutable; full prefix comparison still includes it.

    def test_forward_capacity_is_combined_current_and_history(self):
        view = companion('flight-update')['observations'][-1]
        row = view['entries'][0]
        view['entries'] = [dict(deepcopy(row), object_key=f'archetype:x{i:04}') for i in range(4096)]
        with self.assertRaisesRegex(PlanError, 'observation_capacity'): forward_view(view, [])

    def test_bounded_observer_integration_is_read_only_and_checks_target_first(self):
        f = flow('flight-update'); c = context(f, f['final_checkpoint'])
        good = companion('flight-update')['observations'][-1]; original = deepcopy(good)
        transport = Mock(target=deepcopy(f['plan']['request']['target']))
        with patch('spine_packs.facet_recovery.observe', return_value=(f['plan']['environment'], good)) as read:
            self.assertEqual(c.observe_prefix(transport), good)
            self.assertEqual(read.call_args.kwargs['lineage'], c.lineage())
            self.assertEqual(read.call_args.args[2], f['plan']['closure'])
            self.assertEqual(read.call_args.kwargs['content_contracts'], tuple(f['manifest']['compatibility']['spine_content_contracts']))
            transport.write.assert_not_called()
            transport.target['host_name'] = 'other.invalid'
            with self.assertRaisesRegex(PlanError, 'recovery_target_changed'): c.observe_prefix(transport)
            self.assertEqual(read.call_count, 1)
        self.assertEqual(good, original)


class HistoryReplay(Replay):
    """Existing complete two-pass wire transcript plus exact historical reads."""
    def __init__(self, f, extras, fault=None):
        super().__init__(f)
        self.extras = extras; self.extra_calls = []; self.fault = fault

    def _invoke(self, command, request):
        key = (command, a.canonical_text(request))
        if key not in self.extras:
            return super()._invoke(command, request)
        self.calls.append(command); self.extra_calls.append(key)
        result = deepcopy(self.extras[key]); code = 0
        if self.fault: result, code = self.fault(command, request, result, len(self.extra_calls), self)
        self._received(json.dumps(result).encode())
        return result, code


def history_fixture():
    f = fixture(); extras = {}; hints = []
    for family in ('archetype', 'profile', 'rendering'):
        prefix, _, id_field, _ = FAMILIES[family]; command = prefix + '.show'
        source = next(r['response'] for r in f['reads'] if r['command'] == command)
        record = source['record' if family == 'rendering' else prefix]
        revision_field = prefix + '_revision_id'
        current = record[revision_field] if family == 'rendering' else record['revision'][revision_field]
        def advance(value):
            if isinstance(value, dict):
                if value.get(revision_field) == current and 'revision_number' in value:
                    value['revision_number'] = 2 if type(value['revision_number']) is int else '2'
                for child in value.values(): advance(child)
            elif isinstance(value, list):
                for child in value: advance(child)
        advance(f['reads'])
        historical = deepcopy(source); record = historical['record' if family == 'rendering' else prefix]
        revision = 'historical_' + family
        if family == 'rendering': record.update({revision_field: revision, 'revision_number': '1'})
        else:
            record['revision'].update({revision_field: revision,
                'revision_number': 1 if family == 'archetype' else '1'})
        request = dict(contract_version=COMMANDS[command]['selector'], **{id_field: record[id_field], revision_field: revision})
        extras[(command, a.canonical_text(request))] = historical
        hints.append(state(family, record, f['request']['request']['owner'], historical=True))
    # A1 is no longer referenced by any current consumer. Its actual root A
    # is returned by the revision-only read; do not enumerate candidate roots.
    old_schema = deepcopy(next(r['response'] for r in f['reads'] if r['command'] == 'facet_schema.show'
        and r['response']['root']['schema_key'] == 'flight_details'))
    old_schema.update(command='facet_schema.revision.show', response_contract='spine.facet-schema-revision-readback.v1')
    old_schema['revision'].update(facet_schema_revision_id='historical_schema', revision_number='1')
    request = dict(contract_version=COMMANDS['facet_schema.revision.show']['selector'],
                   facet_schema_revision_id='historical_schema')
    extras[('facet_schema.revision.show', a.canonical_text(request))] = old_schema
    hints.append(state('schema', old_schema, f['request']['request']['owner'], historical=True))
    # Existing B1 is already read by current rendering/binding pins. Lineage
    # must reuse that read, not probe A or read B1 again in the same pass.
    hints.extend(deepcopy(f['plan']['observation']['historical_revisions']))
    return f, extras, hints


class HistoricalObservationTests(unittest.TestCase):
    def run_observation(self, f, adapter, hints):
        with patch.dict('os.environ', CURSORS), patch('subprocess.Popen', side_effect=AssertionError('no processes')):
            return observe(adapter, f['request']['request']['owner'], f['plan']['closure'],
                page_size=1, content_contracts=f['manifest']['compatibility']['spine_content_contracts'], lineage=hints)

    def test_all_history_families_read_fresh_once_per_pass_without_root_probing(self):
        f, extras, hints = history_fixture(); original = deepcopy(hints)
        adapter = HistoryReplay(f, extras)
        _, view = self.run_observation(f, adapter, hints + hints)
        self.assertFalse(adapter.rows); self.assertEqual(len(adapter.extra_calls), 8)
        for key in extras: self.assertEqual(adapter.extra_calls.count(key), 2)
        self.assertEqual(adapter.calls.count('facet_schema.revision.show'), 4)
        self.assertTrue(set(adapter.calls) <= READ_COMMANDS)
        self.assertEqual(hints, original)
        self.assertEqual({r['revision_id'] for r in view['historical_revisions']}, {r['revision_id'] for r in hints})
        for expected in hints: self.assertIn(expected, view['historical_revisions'])

    def test_saved_bodies_are_not_fresh_evidence(self):
        f, extras, hints = history_fixture(); expected = deepcopy(hints)
        for hint in hints: hint['value'] = blob({})
        _, view = self.run_observation(f, HistoryReplay(f, extras), hints)
        self.assertEqual(view['historical_revisions'], sorted(expected, key=lambda r: (r['object_key'], r['revision_id'])))

    def test_bad_lineage_shape_and_conflicting_identity_rejected_before_reads(self):
        f, _, hints = history_fixture(); owner = f['request']['request']['owner']
        for fault in ('owner', 'root', 'revision', 'binding', 'decoder', 'family', 'conflict'):
            rows = deepcopy(hints)
            if fault == 'owner': rows[0]['owner']['owner_subject_id'] = 'other'
            elif fault == 'root': rows[0]['root_id'] = None
            elif fault == 'revision': rows[0]['revision_id'] = None
            elif fault == 'binding': rows[0]['binding_id'] = 'other'
            elif fault == 'decoder': rows[0]['revision_contract'] = 'spine.facet-schemas.v1'
            elif fault == 'family': rows[0]['object_key'] = 'binding:flight'
            else: rows.append(dict(deepcopy(rows[0]), root_id='other'))
            transport = Mock()
            with self.subTest(fault=fault), self.assertRaises(PlanError): Observer(transport, owner, [], lineage=rows)
            transport.read.assert_not_called()

    def test_missing_catalog_root_never_triggers_candidate_probing(self):
        f, extras, hints = history_fixture(); hints[0]['root_id'] = 'not-in-catalog'
        adapter = HistoryReplay(f, extras)
        with self.assertRaisesRegex(PlanError, 'lineage_root_not_in_catalog'): self.run_observation(f, adapter, hints)
        self.assertFalse(adapter.extra_calls)

    def test_current_pins_use_current_evidence_and_exact_schema_lookup(self):
        f = fixture(); hints = [r for r in f['plan']['observation']['entries'] if r['binding_id'] is None]
        # A2 is a current schema not already needed by the old B1 consumers.
        current = next(r['response'] for r in f['reads'] if r['command'] == 'facet_schema.show'
                       and r['response']['root']['schema_key'] == 'flight_details')
        request = dict(contract_version=COMMANDS['facet_schema.revision.show']['selector'],
                       facet_schema_revision_id=current['revision']['facet_schema_revision_id'])
        response = dict(deepcopy(current), command='facet_schema.revision.show',
                        response_contract='spine.facet-schema-revision-readback.v1')
        # The other current schema B2 likewise needs its own exact lookup.
        extras = {('facet_schema.revision.show', a.canonical_text(request)): response}
        for read in f['reads']:
            if read['command'] == 'facet_schema.show':
                value = read['response']; req = dict(request, facet_schema_revision_id=value['revision']['facet_schema_revision_id'])
                extras[('facet_schema.revision.show', a.canonical_text(req))] = dict(deepcopy(value),
                    command='facet_schema.revision.show', response_contract='spine.facet-schema-revision-readback.v1')
        adapter = HistoryReplay(f, extras)
        _, view = self.run_observation(f, adapter, hints)
        self.assertEqual(view, f['plan']['observation'])
        self.assertFalse(adapter.rows)

    def test_historical_root_revision_owner_hash_and_decoder_corruption_abort(self):
        for family in ('archetype', 'profile', 'rendering'):
            for fault in ('root', 'revision', 'owner', 'current', 'hash', 'content', 'decoder', 'dry_run'):
                f, extras, hints = history_fixture(); prefix, _, id_field, _ = FAMILIES[family]
                def corrupt(command, request, response, n, adapter):
                    if command != prefix + '.show': return response, 0
                    record = response['record' if family == 'rendering' else prefix]
                    rev = record if family == 'rendering' else record['revision']
                    if fault == 'root': record[id_field] = 'wrong'
                    elif fault == 'revision': rev[prefix + '_revision_id'] = 'wrong'
                    elif fault == 'owner':
                        (record if family == 'archetype' else record['owner'])['owner_subject_id'] = 'wrong'
                    elif fault == 'current': record['current_revision_id'] = 'wrong'
                    elif fault == 'hash':
                        rev[{'archetype': 'normalized_content_hash', 'profile': 'normalized_revision_hash',
                             'rendering': 'definition_hash'}[family]] = '0' * 64
                    elif fault == 'content':
                        if family == 'archetype': rev['display_name'] = 'Other'
                        elif family == 'profile': rev['content']['compatible_item_types'] = ['task']
                        else: record['revision']['display_name'] = 'Other'
                    elif fault == 'decoder': rev['revision_contract'] = 'unsupported'
                    else: response['dry_run'] = True
                    return response, 0
                with self.subTest(family=family, fault=fault), self.assertRaises(PlanError):
                    self.run_observation(f, HistoryReplay(f, extras, corrupt), hints)

    def test_historical_missing_failure_is_not_absence(self):
        f, extras, hints = history_fixture()
        def missing(command, request, response, n, adapter):
            return dict(ok=False, command=command, error=dict(code='referenced_row_not_found',
                field='revision', message='private-sentinel')), 4
        with self.assertRaises(PlanError) as caught:
            self.run_observation(f, HistoryReplay(f, extras, missing), hints)
        self.assertEqual(caught.exception.category, 'spine_command_rejection')
        self.assertNotIn('private-sentinel', str(caught.exception))

    def test_exact_lineage_schema_failures_keep_their_owning_contract(self):
        for code, field, exit_code, category, diagnostic in (
            ('referenced_row_not_found', 'facet_schema_revision_id', 4, 'spine_command_rejection', 'referenced_revision_missing'),
            ('environment_failure', 'facets', 7, ENVIRONMENT, 'revision_read_failed'),
            ('environment_failure', 'capacity', 7, ENVIRONMENT, 'revision_read_failed'),
            ('invalid_request', 'facet_schema_revision_id', 2, 'spine_command_rejection', 'revision_read_failed'),
            ('environment_failure', 'runtime_contracts', 7, 'spine_command_rejection', 'spine_read_rejected'),
            ('invalid_request', 'db', 3, 'spine_command_rejection', 'spine_read_rejected'),
        ):
            f, extras, hints = history_fixture()
            def fail(command, request, response, n, adapter):
                if command == 'facet_schema.revision.show':
                    return dict(ok=False, command=command, error=dict(code=code, field=field,
                        message='private-sentinel')), exit_code
                return response, 0
            with self.subTest(code=code, field=field), self.assertRaises(PlanError) as caught:
                self.run_observation(f, HistoryReplay(f, extras, fail), hints)
            self.assertEqual((caught.exception.category, caught.exception.code), (category, diagnostic))
            self.assertNotIn('private-sentinel', str(caught.exception))

    def test_unreferenced_schema_lineage_never_reassigns_a_revision_to_desired_root(self):
        for fault in ('other_root', 'owner', 'revision', 'current', 'hash', 'malformed'):
            f, extras, hints = history_fixture()
            def corrupt(command, request, response, n, adapter):
                if command == 'facet_schema.revision.show':
                    if fault == 'other_root':
                        # Structurally coherent actual root B is still not A.
                        b = next(r['response'] for r in f['reads'] if r['command'] == 'facet_schema.revision.show')
                        response['root'] = deepcopy(b['root'])
                        response['revision']['facet_schema_id'] = b['root']['facet_schema_id']
                    elif fault == 'owner': response['root']['owner']['owner_subject_id'] = 'other'
                    elif fault == 'revision': response['revision']['facet_schema_revision_id'] = 'other'
                    elif fault == 'current': response['root']['current_revision_id'] = 'other'
                    elif fault == 'hash': response['revision']['definition_hash'] = '0' * 64
                    else: response['revision'] = None
                return response, 0
            with self.subTest(fault=fault), self.assertRaises(PlanError):
                self.run_observation(f, HistoryReplay(f, extras, corrupt), hints)

    def test_global_call_byte_and_deadline_budgets_include_lineage(self):
        for fault in ('calls', 'bytes', 'deadline'):
            f, extras, hints = history_fixture()
            def exhaust(command, request, response, n, adapter):
                if fault == 'calls': adapter.budget.calls = 4096
                elif fault == 'bytes': adapter.budget.bytes = 128 * 1024 * 1024
                else: adapter.budget.deadline = adapter.budget.clock() - 1
                return response, 0
            with self.subTest(fault=fault), self.assertRaisesRegex(PlanError, 'observation_capacity') as caught:
                self.run_observation(f, HistoryReplay(f, extras, exhaust), hints)
            self.assertEqual(caught.exception.category, ENVIRONMENT)

    def test_second_pass_history_drift_is_not_hidden_by_cross_pass_cache(self):
        f, extras, hints = history_fixture()
        def drift(command, request, response, n, adapter):
            if n == 5:
                revision = response['item_archetype']['revision']; revision['description'] = 'Changed immutable body'
                semantic = {k: revision[k] for k in ('display_name', 'description', 'compatible_item_types')}
                revision['normalized_content_hash'] = a.digest(semantic)
            return response, 0
        with self.assertRaisesRegex(PlanError, 'catalog_changed_between_passes'):
            self.run_observation(f, HistoryReplay(f, extras, drift), hints)

    def test_historical_and_retired_roots_share_the_same_exact_read_path(self):
        f, extras, hints = history_fixture(); owner = f['request']['request']['owner']
        for family in ('archetype', 'profile'):
            prefix, _, _, _ = FAMILIES[family]
            original = deepcopy(next(r['response'][prefix] for r in f['reads'] if r['command'] == prefix + '.show'))
            old_response = deepcopy(next(v for (cmd, _), v in extras.items() if cmd == prefix + '.show'))
            original['status'] = old_response[prefix]['status'] = 'retired'
            if family == 'archetype':
                for record in (original, old_response[prefix]):
                    record.update(retired_at_utc='2035-02-01T12:00:00Z', retired_by_command_id='retired',
                                  retired_by_subject_id='synthetic-actor', retirement_reason='Synthetic retirement')
            transport = Mock(); transport.read.return_value = old_response
            observer = Observer(transport, owner, [], lineage=[r for r in hints if r['object_key'].startswith(family + ':')])
            current = state(family, original, owner); observer.add(current); observer.raw[current['object_key']] = original
            observer.retain_lineage()
            self.assertEqual(len(observer.history), 1); self.assertEqual(transport.read.call_count, 1)
            self.assertEqual(next(iter(observer.history.values()))['status'], 'retired')

    def test_retired_rendering_history_still_checks_its_schema_pin(self):
        f, extras, hints = history_fixture(); owner = f['request']['request']['owner']
        current = deepcopy(next(r['response']['record'] for r in f['reads']
                                if r['command'] == 'notification_rendering_definition.show'))
        response = deepcopy(next(v for (cmd, _), v in extras.items()
                                 if cmd == 'notification_rendering_definition.show'))
        retired = dict(reason_code='superseded', provenance=deepcopy(current['published']))
        for record in (current, response['record']): record.update(status='retired', retired=retired)
        transport = Mock(); transport.read.return_value = response
        observer = Observer(transport, owner, [], lineage=[r for r in hints if r['object_key'].startswith('rendering:')])
        row = state('rendering', current, owner); observer.add(row); observer.raw[row['object_key']] = current
        schema = deepcopy(f['plan']['observation']['historical_revisions'][0])
        observer.exact[schema['revision_id']] = schema  # Validated earlier in this same pass.
        observer.retain_lineage()
        self.assertEqual(next(iter(observer.history.values()))['status'], 'retired')
        # Cache membership cannot excuse an invalid historical projection.
        response['record']['revision']['selections'][0]['field_key'] = 'not_in_schema'
        from spine_packs.facet_observation import rendering_semantics
        rendering_semantics(response['record']['revision'])
        response['record']['definition_hash'] = a.digest(dict(
            contract_version='spine.notification-rendering-definitions.v1', canonical_json_version='spine.canonical-json.v1',
            revision=response['record']['revision']))
        observer.exact.pop((row['root_id'], 'historical_rendering'))
        observer.history.clear()
        with self.assertRaisesRegex(PlanError, 'rendering_schema_mismatch'): observer.retain_lineage()

    def test_lineage_insertion_and_hint_count_retain_global_entry_limit(self):
        f, extras, hints = history_fixture(); owner = f['request']['request']['owner']
        with self.assertRaisesRegex(PlanError, 'observation_entry_capacity'):
            Observer(Mock(), owner, [], lineage=[hints[0]] * 4097)
        original = next(r['response']['item_archetype'] for r in f['reads'] if r['command'] == 'item_archetype.show')
        response = next(v for (cmd, _), v in extras.items() if cmd == 'item_archetype.show')
        transport = Mock(); transport.read.return_value = response
        observer = Observer(transport, owner, [], lineage=hints[:1]); row = state('archetype', original, owner)
        observer.add(row); observer.raw[row['object_key']] = original
        for n in range(4095): observer.add(dict(deepcopy(row), object_key=f'archetype:other_{n:04}'))
        with self.assertRaisesRegex(PlanError, 'observation_entry_capacity'): observer.retain_lineage()


if __name__ == '__main__':
    unittest.main()
