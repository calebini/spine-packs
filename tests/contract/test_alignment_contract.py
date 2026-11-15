"""AL-1 exact 0.12.0/schema-20 agreements; synthetic, no Spine processes."""
from copy import deepcopy
import hashlib
import json
import unittest
from unittest.mock import patch

import alignment_fixture_support as a
import facet_artifact_oracle as o
import fr4_contract_oracle as fr4
from fr3_fixture_support import checkpoint_at, current_contracts, reseal_response
from fr4_fixture_support import replay_evidence, load_flow as load_historical_flow
from test_facet_manifest_contract import digest

INDEX = o.ROOT / 'contracts/installer-alignment-fixture-manifest.v2.json'


@unittest.skipIf(o.Draft202012Validator is None, 'AL-1 requires official development jsonschema')
class AlignmentContractTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(a.aligned_contracts())
        self.index = o.load(INDEX)
        self.vectors = o.load(o.ROOT / self.index['fixtures'][0]['path'])

    def flows(self):
        return [a.load_flow(vector) for vector in self.vectors['flows']]

    def test_frozen_evidence_and_deterministic_derived_expectations(self):
        self.assertEqual((self.index['spine_commit'], self.index['runtime_version'],
                          self.index['ledger_schema']), (a.PIN, a.RUNTIME, a.SCHEMA))
        for entry in self.index['preserved_inputs'] + self.index['fixtures']:
            self.assertEqual(o.sha((o.ROOT / entry['path']).read_bytes()), entry['sha256'], entry['path'])
        for vector in self.vectors['flows']:
            flow = a.load_flow(vector)
            self.assertEqual(a.summary(flow), vector['expected'])
            source = o.load(o.ROOT / vector['source']['path'])
            for field in ('archetypes', 'facet_schemas', 'archetype_facet_bindings',
                          'rendering_definitions', 'notification_profiles', 'binding_intents'):
                self.assertEqual(flow['manifest'][field], source['manifest'][field])
            self.assertNotEqual(flow['plan']['content_identity'], source['plan']['content_identity'])
            self.assertEqual(flow['plan']['observation'], source['plan']['observation'])

    def test_inventory_projection_and_full_transitive_offline_closure(self):
        old = o.load(o.ROOT / 'contracts/installer-spine-0.10.0-inventory.json')
        inv = a.INVENTORY
        self.assertEqual(inv['commands'], old['commands'])
        self.assertEqual(inv['required_execution_contracts'], old['required_execution_contracts'])
        self.assertEqual(inv['source_sha256'], old['source_sha256'])
        projection = inv['command_registry_projection']
        self.assertEqual(set(projection), set(inv['commands']))
        self.assertEqual(len(projection), 23)
        self.assertEqual(sum(c['access_mode'] == 'read' for c in projection.values()), 12)
        for name, command in inv['commands'].items():
            self.assertEqual(projection[name]['access_mode'], 'read' if command['phase'] is None else 'write')
        self.assertEqual(sorted({c for row in projection.values() for c in row['required_contracts']}),
                         inv['required_execution_contracts'])
        self.assertEqual(len(inv['required_execution_contracts']), 18)
        self.assertFalse(any('disclosure' in c or c.startswith(('item.', 'person.', 'people.')) for c in projection))
        # Check every reachable reference, including branches no fixture happens to exercise.
        def references(value):
            if isinstance(value, dict):
                if '$ref' in value: yield value['$ref']
                for v in value.values(): yield from references(v)
            elif isinstance(value, list):
                for v in value: yield from references(v)
        pending = ['spine-readback-0.12.0.schema.json', 'spine-pack-manifest.v2.schema.json',
                   'spine-pack-installer-types.v2.schema.json']
        seen = set()
        while pending:
            name = pending.pop()
            if name in seen: continue
            seen.add(name)
            document = o.load(o.SCHEMAS / name)
            o.Draft202012Validator.check_schema(document)
            for ref in references(document):
                file, _, pointer = ref.partition('#'); file = file or name
                self.assertNotIn('/', file); self.assertNotIn(':', file)
                resolved = o.load(o.SCHEMAS / file)
                for token in pointer.split('/')[1:]:
                    resolved = resolved[token.replace('~1', '/').replace('~0', '~')]
                pending.append(file)
        self.assertIn('spine-readback-0.10.0.schema.json', seen)
        self.assertIn('spine-readback-0.9.1.schema.json', seen)
        self.assertEqual(set(o.load(o.SCHEMAS / 'spine-readback-0.12.0.schema.json')['$defs']),
                         set(o.load(o.SCHEMAS / 'spine-readback-0.10.0.schema.json')['$defs']))

    def test_all_prior_public_wire_vectors_validate_under_new_closure(self):
        ordinary = o.load(o.ROOT / 'tests/fixtures/installer-v2/public-wire-vectors.json')['vectors']
        for vector in ordinary:
            o.public_schema(vector['command'], vector['direction'], vector['value'])
        historical = o.load(o.ROOT / 'tests/fixtures/installer-v2/revision-readback-0.10.0.json')['vectors']
        for vector in historical:
            direction = vector['schema'].split('/')[-1].removeprefix(
                'facet-schema-revision-show-').removesuffix('.schema.json')
            validator = o.validator('spine-readback-0.12.0.schema.json',
                                    a.INVENTORY['commands']['facet_schema.revision.show'][direction])
            self.assertEqual(validator.is_valid(vector['value']), vector['valid'])

    def test_exact_environment_pairs_and_manifest_singletons(self):
        schema = o.validator('spine-pack-installer-types.v2.schema.json', 'environment')
        original = self.flows()[0]['plan']['environment']
        for runtime in ('0.9.1', '0.10.0', '0.12.0', '0.12.1', '0.13.0'):
            for current in ('19', '20', '21'):
                for implemented in ('19', '20', '21'):
                    value = dict(original, runtime_version=runtime,
                                 ledger_schema_current=current, ledger_schema_implemented=implemented)
                    expected = ((runtime in ('0.9.1', '0.10.0') and current == implemented == '19') or
                                (runtime == '0.12.0' and current == implemented == '20'))
                    with self.subTest(runtime=runtime, current=current, implemented=implemented):
                        self.assertEqual(schema.is_valid(value), expected)
        manifest = self.flows()[0]['manifest']
        valid = o.validator('spine-pack-manifest.v2.schema.json')
        for versions in (['0.9.1'], ['0.10.0'], ['0.12.0'], ['0.10.0', '0.12.0'],
                         ['0.12.1'], ['>=0.12.0'], []):
            changed = deepcopy(manifest); changed['compatibility']['spine_runtime_versions'] = versions
            self.assertEqual(valid.is_valid(changed), versions in (['0.9.1'], ['0.10.0'], ['0.12.0']))

    def test_complete_create_update_and_verification_flows(self):
        commands = set()
        for flow in self.flows():
            p, approval = flow['plan'], flow['approval']
            a.plan_check(flow); o.approval_check(p, approval)
            for key in ('initial_checkpoint', 'prepared_checkpoint', 'final_checkpoint'):
                fr4.checkpoint_check(p, approval, flow[key])
            for key in ('apply_result', 'partial_result', 'empty_prefix_partial'):
                o.result_check(p, approval, flow[key])
            fr4.verification_check(flow, flow['apply_result'], flow['verification'])
            self.assertEqual(flow['verification']['state'], 'verified')
            o.artifact(flow['envelope'])
            commands.update(action['command'] for action in p['actions'])
            # Independent fixed-vector encoder checks digest domain and command IDs.
            value = deepcopy(p); expected = value['content_identity'].pop('digest')
            encode = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
            self.assertEqual(hashlib.sha256(encode(value)).hexdigest(), expected)
            for action, evidence in zip(p['actions'], flow['accepted_responses'], strict=True):
                preimage = dict(action_id=action['action_id'], derivation_version='spine.pack-command-id.v2',
                    execution_id=approval['execution']['execution_id'], plan_digest=expected)
                self.assertEqual('spack_' + hashlib.sha256(encode(preimage)).hexdigest(), evidence['command_id'])
        self.assertEqual(commands, {c for c, v in a.INVENTORY['commands'].items() if v['phase'] is not None})

    def test_all_36_recovery_boundaries(self):
        flows = dict(zip((v['id'] for v in self.vectors['flows']), self.flows()))
        covered = set()
        for vector in self.vectors['recovery_vectors']:
            flow = flows[vector['flow']]; n = int(vector['prefix_length']); boundary = vector['boundary']
            self.assertEqual(flow['plan']['actions'][n]['command'], vector['command'])
            covered.add(vector['id'])
            accepted = boundary == 'accepted_durable'
            cp = checkpoint_at(flow, n + int(accepted), not accepted); before = deepcopy(cp)
            with self.subTest(vector=vector['id']):
                if boundary == 'accepted_response_lost':
                    candidate = flow['accepted_responses'][n]['post_observation']
                    record = o.unblob(flow['accepted_responses'][n]['response'], True).get('record')
                    handle = fr4.admit(flow, cp, flow['observations'][n+1], provisional=candidate, record=record)
                    self.assertEqual(handle['kind'], 'prefix_plus_one')
                    self.assertEqual(len(handle['checkpoint']['accepted_responses']), n)
                    replay = replay_evidence(flow['accepted_responses'][n])
                    self.assertEqual(fr4.replay_check(flow, handle, replay), replay)
                    self.assertEqual(replay['request'], cp['unresolved_submission']['request'])
                else:
                    handle = fr4.admit(flow, cp, flow['observations'][n+int(accepted)])
                    self.assertEqual(handle['kind'], 'prefix')
                self.assertEqual(cp, before)
        self.assertEqual(len(covered), 36)

    def test_rendering_candidates_use_the_selected_public_schema_entry_point(self):
        historical = [load_historical_flow('tests/fixtures/installer-v2/fr4-' + name + '-0.10.0.json')
                      for name in ('flight-create', 'flight-update')]
        for runtime, flows, context in (('0.12.0', self.flows(), a.aligned_contracts),
                                        ('0.10.0', historical, current_contracts)):
            with context():
                shape = o.COMMANDS['notification_rendering_definition.show']['response']
                for flow in flows:
                    n = 3
                    cp = checkpoint_at(flow, n, True)
                    evidence = flow['accepted_responses'][n]
                    record = o.unblob(evidence['response'], True)['record']
                    with self.subTest(runtime=runtime, command=evidence['command']), \
                            patch.object(o, 'validator', wraps=o.validator) as validate:
                        fr4.candidate_check(flow['plan'], flow['approval'], cp,
                                            evidence['post_observation'], record)
                        response_entries = [call.args[0] for call in validate.call_args_list
                                            if len(call.args) == 2 and call.args[1] == shape]
                        self.assertEqual(response_entries, ['spine-readback-' + runtime + '.schema.json'])

    def test_all_indexed_negative_vectors(self):
        errors = (ValueError, KeyError, fr4.ValidationError)
        exercised = set()
        for vector in self.vectors['negative_vectors']:
            fault, stage = vector['id'], vector['stage']; exercised.add(fault)
            flow = self.flows()[1]; p, approval = flow['plan'], flow['approval']
            old = o.load(o.ROOT / self.vectors['flows'][1]['source']['path'])
            with self.subTest(fault=fault):
                if stage == 'plan':
                    if fault == 'wrong_runtime': p['environment']['runtime_version'] = '0.12.1'
                    elif fault == 'wrong_current_schema': p['environment']['ledger_schema_current'] = '19'
                    elif fault == 'wrong_implemented_schema': p['environment']['ledger_schema_implemented'] = '19'
                    elif fault in ('manifest_runtime_mismatch', 'mixed_manifest_runtimes'):
                        flow['manifest']['compatibility']['spine_runtime_versions'] = (
                            ['0.10.0'] if fault == 'manifest_runtime_mismatch' else ['0.10.0', '0.12.0'])
                        flow['manifest']['content_identity']['digest'] = digest(flow['manifest'])
                    elif fault == 'unavailable_contract': p['environment']['advertised_contracts'].remove('spine.facet-schemas.v1')
                    elif fault == 'wrong_execution_union': p['required_execution_contracts'].pop()
                    elif fault == 'stale_plan_digest': p['content_identity']['digest'] = '0' * 64
                    else: self.fail(fault)
                    if fault != 'stale_plan_digest': flow['plan'] = o.seal(p)
                    with self.assertRaises(errors): a.plan_check(flow)
                elif stage == 'approval':
                    if fault == 'old_baseline_approval': approval = old['approval']
                    elif fault == 'unauthorized_update':
                        approval['authorized_update_action_ids'].pop(); approval = o.seal(approval)
                    else: self.fail(fault)
                    with self.assertRaises(errors): o.approval_check(p, approval)
                elif stage == 'continuation':
                    n = 3; cp = checkpoint_at(flow, n, True); fresh = deepcopy(flow['observations'][n])
                    environment = deepcopy(p['environment'])
                    if fault == 'old_baseline_checkpoint': cp = old['prepared_checkpoint']
                    elif fault == 'old_baseline_partial': cp = old['partial_result']
                    elif fault == 'wrong_fresh_environment': environment = old['plan']['environment']
                    elif fault == 'wrong_fresh_schema': environment['ledger_schema_current'] = '19'
                    elif fault == 'changed_replay_request':
                        req = o.unblob(cp['unresolved_submission']['request']); req['actor_subject_id'] = 'different'
                        cp['unresolved_submission']['request'] = o.blob(req); cp = o.seal(cp)
                    elif fault == 'incomplete_prefix': cp['accepted_responses'].pop(0); cp = o.seal(cp)
                    elif fault == 'stale_preimage':
                        # A valid unrelated change must reach admission comparison,
                        # rather than fail early on a corrupt fingerprint/lineage.
                        extra = deepcopy(fresh['entries'][0])
                        extra.update(object_key='archetype:unselected', root_id='synthetic-unselected-root',
                                     revision_id='synthetic-unselected-revision')
                        fresh['entries'].append(extra)
                        fresh['entries'].sort(key=lambda r: r['object_key'])
                        fresh['public_catalog_snapshots'] = o.public_snapshots(fresh['entries'])
                        fresh['digest'] = o.observation_digest(fresh)
                        o.observation(fresh, p['request']['owner'])
                        fr4.lineage(p['observation']['entries'] + p['observation']['historical_revisions'] +
                            [e['post_observation'] for e in cp['accepted_responses']] +
                            fresh['entries'] + fresh['historical_revisions'])
                        with self.assertRaisesRegex(ValueError, '^unexplained catalog change$'):
                            fr4.admit(flow, cp, fresh, environment=environment)
                        continue
                    elif fault in ('old_baseline_replay', 'wrong_replay_root'):
                        handle = fr4.admit(flow, cp, fresh)
                        evidence = deepcopy(old['accepted_responses'][n] if fault == 'old_baseline_replay'
                                            else flow['accepted_responses'][n])
                        if fault == 'wrong_replay_root': evidence['post_observation']['root_id'] = 'other'
                        with self.assertRaises(errors): fr4.replay_check(flow, handle, evidence)
                        continue
                    else: self.fail(fault)
                    with self.assertRaises(errors): fr4.admit(flow, cp, fresh, environment=environment)
                elif stage == 'verification':
                    if fault in ('wrong_receipt_label', 'old_baseline_verification'):
                        value = deepcopy(flow['verification']) if fault == 'wrong_receipt_label' else o.load(
                            o.ROOT / 'tests/fixtures/installer-v2/fr4-flight-update-0.10.0.json')['verification']
                        if fault == 'wrong_receipt_label': value['receipt_readback'] = 'captured_responses_only_spine_0.10.0'
                        with self.assertRaises(errors): fr4.verification_check(flow, flow['apply_result'], o.seal(value))
                        continue
                    result = flow['apply_result']; fresh = deepcopy(flow['observations'][-1])
                    if fault == 'old_baseline_result': result = old['apply_result']
                    elif fault == 'missing_response_evidence': result = None
                    elif fault == 'invalid_same_plan_evidence':
                        for scenario_vector, scenario in zip(self.vectors['flows'], self.flows(), strict=True):
                            with self.subTest(flow=scenario_vector['id']):
                                supplied = deepcopy(scenario['apply_result'])
                                evidence = supplied['checkpoint']['accepted_responses'][0]
                                response = o.unblob(evidence['response'], True)
                                response['receipt']['command_id'] = 'unrelated-command'
                                reseal_response(evidence, response)
                                supplied['checkpoint'] = o.seal(supplied['checkpoint'])
                                supplied = o.seal(supplied)
                                observed = deepcopy(scenario['observations'][-1])
                                o.artifact(supplied)  # Valid outer artifact, invalid embedded correlation.
                                o.observation(observed, scenario['plan']['request']['owner'])
                                verified = fr4.verification(scenario, observed, supplied)
                                self.assertEqual(verified['response_evidence'], 'invalid')
                                self.assertEqual(verified['state'], 'mismatch')
                        continue
                    elif fault == 'known_immutable_revision_contradiction':
                        row = next(r for r in fresh['entries'] if r['object_key'].startswith('schema:'))
                        body = o.unblob(row['value'])
                        body['display_name'] = 'Contradictory immutable definition'
                        row['value'] = o.blob(body)
                        fresh['public_catalog_snapshots'] = o.public_snapshots(fresh['entries'])
                        fresh['digest'] = o.observation_digest(fresh)
                        o.observation(fresh, p['request']['owner'])
                        fr4.lineage(fresh['entries'] + fresh['historical_revisions'])
                        o.result_check(p, approval, result)
                        fr4.checkpoint_check(p, approval, result['checkpoint'])
                        with self.assertRaisesRegex(ValueError, '^immutable revision identity/content$'):
                            fr4.verification(flow, fresh, result)
                        continue
                    elif fault == 'wrong_current_head':
                        next(r for r in fresh['entries'] if r['object_key'].startswith('schema:'))['revision_id'] = 'later'
                    elif fault == 'wrong_binding_pin':
                        row = next(r for r in fresh['entries'] if r['object_key'].startswith('facet_binding:'))
                        body = o.unblob(row['value']); body['facet_schema_revision_id'] = 'later'; row['value'] = o.blob(body)
                    else: self.fail(fault)
                    fresh['digest'] = o.observation_digest(fresh)
                    result = fr4.verification(flow, fresh, result)
                    self.assertEqual(result['state'], 'mismatch')
                    if fault == 'old_baseline_result':
                        self.assertEqual(result['response_evidence'], 'invalid')
                    if fault == 'missing_response_evidence': self.assertEqual(result['response_evidence'], 'missing')
                else: self.fail(stage)
        self.assertEqual(len(exercised), 27)

    def test_known_immutable_conflict_preserves_failure_and_precedence_for_both_flows(self):
        for flow in self.flows():
            plan = flow['plan']
            fresh = deepcopy(flow['observations'][-1])
            row = next(r for r in fresh['entries'] if r['object_key'].startswith('schema:'))
            body = o.unblob(row['value']); body['description'] = 'Conflicting immutable body'
            row['value'] = o.blob(body)
            fresh['public_catalog_snapshots'] = o.public_snapshots(fresh['entries'])
            fresh['digest'] = o.observation_digest(fresh)
            o.observation(fresh, plan['request']['owner'])
            fr4.lineage(fresh['entries'] + fresh['historical_revisions'])
            # Corruption is in fresh evidence relative to the known immutable
            # revision, not in the otherwise-valid captured execution artifact.
            o.result_check(plan, flow['approval'], flow['apply_result'])
            fr4.checkpoint_check(plan, flow['approval'], flow['apply_result']['checkpoint'])
            with self.subTest(flow=flow['plan']['actions'][0]['command']), \
                    patch.object(o, 'seal', wraps=o.seal) as seal:
                with self.assertRaisesRegex(ValueError, '^immutable revision identity/content$'):
                    fr4.verification(flow, fresh, flow['apply_result'])
                self.assertFalse(any(call.args[0].get('artifact_schema') == 'spine.pack-verification-result.v2'
                                     for call in seal.call_args_list))
            # A stale old-plan result cannot mask an independent corrupt fresh
            # observation by turning it into invalid-coverage mismatch.
            corrupt = deepcopy(fresh); corrupt['digest'] = '0' * 64
            stale = deepcopy(flow['apply_result']); stale['checkpoint']['plan_digest'] = '0' * 64
            stale['checkpoint'] = o.seal(stale['checkpoint']); stale = o.seal(stale)
            with self.assertRaisesRegex(ValueError, '^observation digest$'):
                fr4.verification(flow, corrupt, stale)

    def test_every_receipt_label_is_structurally_paired_with_its_baseline(self):
        values = [o.load(o.ROOT / 'tests/fixtures/installer-v2/flight-create.json')['verification'],
                  o.load(o.ROOT / 'tests/fixtures/installer-v2/fr4-flight-create-0.10.0.json')['verification'],
                  self.flows()[0]['verification']]
        for value in values:
            for label in ('captured_responses_only_spine_0.9.1', 'captured_responses_only_spine_0.10.0', a.RECEIPT):
                changed = deepcopy(value); changed['receipt_readback'] = label
                valid = o.validator('spine-pack-verification-result.v2.schema.json').is_valid(o.seal(changed))
                self.assertEqual(valid, label == 'captured_responses_only_spine_' + value['environment']['runtime_version'])

    def test_v1_rejects_new_artifacts_and_runtime_admission_is_still_closed(self):
        import sys
        from unittest.mock import Mock
        sys.path.insert(0, str(o.ROOT / 'src'))
        from spine_packs.facet_planning import plan_installation, validate_inputs
        from spine_packs.planning import PlanError, INCOMPATIBLE
        for vector, flow in zip(self.vectors['flows'], self.flows(), strict=True):
            for value in flow.values():
                if isinstance(value, dict) and 'artifact_schema' in value:
                    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
                    self.assertFalse(o.validator('spine-pack-' + kind + '.v1.schema.json').is_valid(value))
            source = o.load(o.ROOT / vector['source']['path'])
            validate_inputs(source['manifest'], source['request'])
            transport = Mock()
            with self.assertRaises(PlanError) as caught:
                plan_installation(flow['manifest'], flow['request'], transport)
            self.assertEqual(caught.exception.category, INCOMPATIBLE)
            self.assertEqual(transport.mock_calls, [])


if __name__ == '__main__':
    unittest.main()
