"""FR-3 pure execution boundary; saved independent fixtures, no ledgers or writes."""
from copy import deepcopy
import json
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from spine_packs import artifacts as a
from spine_packs.facet_contracts import blob, body, seal
from spine_packs.facet_execution import ExecutionContext, WRITE_COMMANDS, command_id, public_body
from spine_packs.facet_inventory import READ_COMMANDS
from spine_packs.planning import PlanError


def flow(name='flight-create'):
    return json.loads((ROOT / f'tests/fixtures/installer-v2/{name}-0.10.0.json').read_text())


def context(f):
    return ExecutionContext(f['manifest'], f['plan'], f['approval'])


def reseal_plan(f):
    f['plan'] = seal(f['plan'])
    f['approval']['plan_digest'] = f['plan']['content_identity']['digest']
    f['approval'] = seal(f['approval'])


class FacetExecutionTests(unittest.TestCase):
    def test_all_eleven_writes_match_independent_requests_and_evidence(self):
        commands = set()
        # Even accidental use of ordinary transport would fail this pure test.
        with patch('subprocess.Popen', side_effect=AssertionError('no processes')):
            for name in ('flight-create', 'flight-update'):
                f = flow(name); original = deepcopy(f); c = context(f); accepted = []
                for expected in f['accepted_responses']:
                    self.assertEqual(c.materialize(accepted), body(expected['request']))
                    result = c.response_evidence(accepted, expected['response']['json_text'].encode() + b'\n',
                                                 expected['post_observation'])
                    self.assertEqual(result, expected)
                    accepted.append(result); commands.add(expected['command'])
                with self.assertRaises(PlanError):
                    c.materialize(accepted)  # No action beyond the approved suffix.
                self.assertEqual(f, original)
        self.assertEqual(commands, WRITE_COMMANDS)
        self.assertEqual(len(commands), 11)
        self.assertFalse(WRITE_COMMANDS & READ_COMMANDS)

    def test_context_rejects_resealed_graph_and_approval_tampering(self):
        for mutation in ('runtime', 'schema', 'union', 'missing_advertisement', 'template', 'slot',
                         'producer_pointer', 'producer_object', 'future_producer', 'observed_id',
                         'classification', 'snapshot', 'observation_digest', 'pack_digest',
                         'partial_updates', 'stale_approval'):
            with self.subTest(mutation=mutation):
                f = flow('flight-update' if mutation in ('partial_updates', 'observed_id') else 'flight-create')
                p = f['plan']
                if mutation == 'runtime': p['environment']['runtime_version'] = '0.9.1'
                elif mutation == 'schema': p['environment']['ledger_schema_current'] = '20'
                elif mutation == 'union': p['required_execution_contracts'].pop()
                elif mutation == 'missing_advertisement': p['environment']['advertised_contracts'].pop(0)
                elif mutation == 'template':
                    value = body(p['actions'][0]['request_template']); value['revision']['display_name'] = 'Other'
                    p['actions'][0]['request_template'] = blob(value)
                elif mutation == 'slot': p['actions'][2]['slots'].pop()
                elif mutation in ('producer_pointer', 'producer_object', 'future_producer'):
                    source = next(r for r in p['resolutions'] if r['object_key'] == 'schema:flight_details')['revision']
                    if mutation == 'producer_pointer': source['output_pointer'] = '/facet_schema_id'
                    else: source['action_id'] = 'action-000000' if mutation == 'producer_object' else 'action-000005'
                elif mutation == 'observed_id':
                    next(r for r in p['resolutions'] if r['object_key'] == 'schema:flight_details')['root']['value'] = 'other'
                elif mutation == 'classification': p['classifications'][0]['classification'] = 'equivalent'
                elif mutation == 'snapshot': p['observation']['public_catalog_snapshots'][0]['digest'] = '0' * 64
                elif mutation == 'observation_digest': p['observation']['digest'] = '0' * 64
                elif mutation == 'pack_digest': p['pack']['manifest_digest'] = '0' * 64
                reseal_plan(f)
                if mutation == 'partial_updates':
                    f['approval']['authorized_update_action_ids'].pop(); f['approval'] = seal(f['approval'])
                elif mutation == 'stale_approval':
                    f['approval']['plan_digest'] = '0' * 64; f['approval'] = seal(f['approval'])
                with self.assertRaises(PlanError): context(f)

    def test_context_owns_private_copies(self):
        f = flow(); c = context(f)
        f['plan']['actions'].clear(); f['approval']['execution']['actor_subject_id'] = 'changed'
        self.assertEqual(c.materialize([]), body(flow()['accepted_responses'][0]['request']))

    def test_nonobject_inputs_and_wrong_artifact_versions_fail_closed(self):
        f = flow()
        for field in ('manifest', 'plan', 'approval'):
            for invalid in (None, [], 'PRIVATE_SENTINEL'):
                broken = deepcopy(f); broken[field] = invalid
                with self.subTest(field=field, invalid=invalid), self.assertRaises(PlanError):
                    context(broken)
        for field in ('plan', 'approval'):
            broken = deepcopy(f)
            broken[field]['artifact_schema'] = broken[field]['artifact_schema'].replace('.v2', '.v1')
            with self.assertRaises(PlanError): context(broken)

    def test_contiguous_prefix_revalidated_before_consumer(self):
        f = flow(); c = context(f)
        for mutation in ('gap', 'reorder', 'request', 'command', 'wire_digest', 'receipt', 'readback'):
            with self.subTest(mutation=mutation):
                accepted = deepcopy(f['accepted_responses'][:3])
                if mutation == 'gap': accepted.pop(0)
                elif mutation == 'reorder': accepted.reverse()
                elif mutation == 'request':
                    value = body(accepted[1]['request']); value['actor_subject_id'] = 'wrong'; accepted[1]['request'] = blob(value)
                elif mutation == 'command': accepted[1]['command_id'] = 'wrong'
                elif mutation == 'wire_digest': accepted[1]['response']['json_text'] += ' '
                elif mutation == 'receipt': accepted[1]['receipt']['audit_id'] = 'wrong'
                else: accepted[1]['post_observation']['root_id'] = 'wrong'
                with self.assertRaises(PlanError): c.materialize(accepted)
        # Candidate evidence alone does not advance the context or provide IDs.
        e = f['accepted_responses'][0]
        c.response_evidence([], e['response']['json_text'].encode(), e['post_observation'])
        self.assertEqual(c.materialize([]), body(e['request']))

    def test_every_command_rejects_invalid_response_or_post_observation(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name); c = context(f)
            for n, e in enumerate(f['accepted_responses']):
                for mutation in ('command_id', 'command', 'owner', 'root', 'retired', 'object', 'semantic'):
                    with self.subTest(command=e['command'], mutation=mutation):
                        response = json.loads(e['response']['json_text']); post = deepcopy(e['post_observation'])
                        if mutation == 'command_id': response.get('receipt', response)['command_id'] = 'wrong'
                        elif mutation == 'command': response['command'] = 'item.create'
                        elif mutation == 'owner': post['owner']['owner_subject_id'] = 'wrong'
                        elif mutation == 'root': post['root_id'] = 'wrong'
                        elif mutation == 'retired': post['status'] = 'retired'
                        elif mutation == 'object': post['object_key'] = 'schema:wrong'
                        else: post['value'] = blob({})
                        with self.assertRaises(PlanError):
                            c.response_evidence(f['accepted_responses'][:n], json.dumps(response).encode(), post)

    def test_family_specific_correlations_and_noop_rejection(self):
        for name in ('flight-create', 'flight-update'):
            f = flow(name); c = context(f)
            for n, e in enumerate(f['accepted_responses']):
                r = json.loads(e['response']['json_text']); mutations = []
                if 'receipt' in r:
                    mutations += [('receipt', 'semantic_facts_hash', '0' * 64),
                                  ('receipt', 'created_at_utc', '2035-02-02T12:00:00Z')]
                if e['command'] == 'item_archetype.facet_binding.set':
                    mutations += [(None, 'facet_key', 'different_key'), (None, 'facet_schema_revision_id', 'other'),
                                  (None, 'prior_binding_id', 'wrong')]
                if 'record' in r:
                    mutations += [('record', 'definition_hash', '0' * 64), ('record', 'definition_key', 'wrong'),
                                  ('record', 'owner', dict(owner_kind='subject', owner_subject_id='wrong')),
                                  ('published', 'actor_subject_id', 'wrong'), ('published', 'command_id', 'wrong')]
                if 'normalized_revision_hash' in r:
                    mutations.append((None, 'normalized_revision_hash', '0' * 64))
                if e['command'] == 'notification_profile.metadata.update':
                    mutations += [(None, 'display_name', 'Wrong'), (None, 'description', 'Wrong'),
                                  (None, 'notification_profile_revision_id', 'wrong')]
                for section, key, value in mutations:
                    with self.subTest(command=e['command'], section=section, field=key):
                        altered = deepcopy(r)
                        target = altered['record']['published'] if section == 'published' else altered[section] if section else altered
                        target[key] = value
                        with self.assertRaises(PlanError):
                            c.response_evidence(f['accepted_responses'][:n], json.dumps(altered).encode(), e['post_observation'])
        f = flow('flight-update'); c = context(f)
        n = next(i for i, e in enumerate(f['accepted_responses']) if e['command'] == 'notification_rendering_definition.publish')
        e = f['accepted_responses'][n]; r = json.loads(e['response']['json_text'])
        r.update(effect='rendering_definition_publish_noop', changed=False)
        with self.assertRaisesRegex(PlanError, 'noop_cannot_explain_change'):
            c.response_evidence(f['accepted_responses'][:n], json.dumps(r).encode(), e['post_observation'])

    def test_wire_bytes_and_native_integers_are_preserved(self):
        f = flow(); c = context(f); n = 3; e = f['accepted_responses'][n]
        r = json.loads(e['response']['json_text'])
        text = json.dumps(r, indent=2) + '  \n'
        result = c.response_evidence(f['accepted_responses'][:n], text.encode() + b'\n', e['post_observation'])
        self.assertEqual(result['response']['json_text'], text)
        self.assertEqual(json.loads(result['response']['json_text']), r)
        # Generic wire decoding preserves native public integers; the contextual
        # response schema still decides whether a particular field admits them.
        integer_text = '{"revision_number":1}'
        decoded = public_body(dict(json_text=integer_text, digest=hashlib.sha256(integer_text.encode()).hexdigest()))
        self.assertIs(type(decoded['revision_number']), int)

    def test_malformed_wire_is_fail_closed_and_diagnostics_do_not_echo_content(self):
        f = flow(); c = context(f); e = f['accepted_responses'][0]; raw = e['response']['json_text'].encode()
        for bad in (b'\xef\xbb\xbf' + raw, b'\xff', b'{"ok":true,"ok":true}', b'{"n":NaN}',
                    b'"\\ud800"', b'{"n":1.5}', b'not-json-PRIVATE_SENTINEL', raw + b'{}'):
            with self.subTest(raw=bad[:20]), self.assertRaises(PlanError) as raised:
                c.response_evidence([], bad, e['post_observation'])
            self.assertNotIn('PRIVATE_SENTINEL', str(raised.exception))

    def test_resolved_rendering_byte_limit_after_long_producer_id(self):
        from spine_packs.facet_manifest import digest as manifest_digest
        from spine_packs.facet_planning import build_plan
        f = flow(); c = context(f)
        revision = c.materialize(f['accepted_responses'][:3])['revision']
        revision['description'] = ''
        remaining = 8192 - len(a.canonical_text(revision).encode())
        f['manifest']['rendering_definitions'][0]['revision']['description'] = '🛫' * (remaining // 4) + 'x' * (remaining % 4)
        f['manifest']['content_identity']['digest'] = manifest_digest(f['manifest'])
        f['plan'] = build_plan(f['manifest'], f['request'], f['plan']['environment'], f['plan']['observation'])
        reseal_plan(f); c = context(f)
        for schema_id in ('schema_revision_2', 'r' * 256):
            accepted = []
            for n, e in enumerate(f['accepted_responses'][:3]):
                r = json.loads(e['response']['json_text']); post = deepcopy(e['post_observation'])
                request = c.materialize(accepted)
                r.get('receipt', r)['command_id'] = request['command_id']
                if 'receipt' in r: r['receipt']['semantic_facts_hash'] = a.digest(request)
                if n in (1, 2): r['facet_schema_revision_id'] = schema_id
                if n == 1: post['revision_id'] = schema_id
                elif n == 2:
                    value = body(post['value']); value['facet_schema_revision_id'] = schema_id; post['value'] = blob(value)
                accepted.append(c.response_evidence(accepted, json.dumps(r).encode(), post))
            if schema_id == 'schema_revision_2':
                self.assertEqual(len(a.canonical_text(c.materialize(accepted)['revision']).encode()), 8192)
            else:
                with self.assertRaisesRegex(PlanError, 'resolved_rendering_capacity'):
                    c.materialize(accepted)

    def test_command_ids_use_v2_domain_and_execution_identity(self):
        f = flow(); p = f['plan']; execution = f['approval']['execution']['execution_id']; action = p['actions'][0]['action_id']
        expected = f['accepted_responses'][0]['command_id']
        self.assertEqual(command_id(p['content_identity']['digest'], execution, action), expected)
        self.assertNotEqual(command_id(p['content_identity']['digest'], 'other-execution', action), expected)
        from spine_packs.execution import command_id as v1_command_id
        self.assertNotEqual(v1_command_id(p['content_identity']['digest'], execution, action), expected)


if __name__ == '__main__':
    unittest.main()
