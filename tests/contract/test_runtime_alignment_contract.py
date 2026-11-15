"""Official offline Draft 2020-12 checks of AL-2 executable outputs."""
from copy import deepcopy
import sys
import unittest
from unittest.mock import patch

import alignment_fixture_support as a
import facet_artifact_oracle as o
import fr4_contract_oracle as fr4

sys.path.insert(0, str(o.ROOT / 'tests/runtime'))
import test_runtime_alignment as vectors
from spine_packs.facet_apply import apply_initial, apply_continuation
from spine_packs.facet_contracts import validate
from spine_packs.facet_execution import ExecutionContext
from spine_packs.facet_execution import projected_state
from spine_packs.facet_planning import plan_installation
from spine_packs.facet_verification import verify_installation


@unittest.skipIf(o.Draft202012Validator is None, 'requires official development jsonschema')
class RuntimeAlignmentContractTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(a.aligned_contracts())
        self.enterContext(patch.dict('os.environ', vectors.CURSORS))
        self.enterContext(patch('subprocess.Popen', side_effect=AssertionError('synthetic commands only')))

    def flows(self):
        for name in ('flight-create', 'flight-update'):
            value = vectors.aligned_flow(name)
            indexed = next(v for v in o.load(o.ROOT / 'tests/fixtures/installer-v2/alignment-0.12.0.json')['flows']
                           if v['id'] == name)
            self.assertEqual(value, a.load_flow(indexed))
            yield value

    def test_runtime_plan_matches_independent_oracle_and_official_schema(self):
        f = vectors.cross_root()
        actual = plan_installation(f['manifest'], f['request'], vectors.Replay(f), page_size=1)
        o.plan_check(f['manifest'], f['request'], actual)
        self.assertEqual(actual, f['plan'])

    def test_runtime_requests_evidence_checkpoints_and_results_match_contract(self):
        commands = set()
        for f in self.flows():
            p, approval = f['plan'], f['approval']
            context = ExecutionContext(f['manifest'], p, approval); accepted = []
            for action, expected in zip(p['actions'], f['accepted_responses'], strict=True):
                request = context.materialize(accepted)
                self.assertEqual(request, o.materialize(p, approval, action, accepted))
                evidence = context.response_evidence(accepted,
                    expected['response']['json_text'].encode(), expected['post_observation'])
                fr4.evidence_check(p, approval, action, evidence, accepted)
                accepted.append(evidence); commands.add(action['command'])
            checkpoints = []
            result = apply_initial(f['manifest'], p, approval,
                vectors.AlignedCatalog(f, 0, f['observations'][0]), checkpoints.append)
            for checkpoint in checkpoints: fr4.checkpoint_check(p, approval, checkpoint)
            o.result_check(p, approval, result)
            self.assertEqual(result, f['apply_result'])
            # The independent recovery oracle also accepts the generated
            # continuation output, not just a runtime decoder accepting itself.
            result = apply_continuation(f['manifest'], p, approval, vectors.prepared(f, 3),
                vectors.AlignedCatalog(f, 3, f['observations'][4], lost=True), checkpoints.append)
            o.result_check(p, approval, result)
            self.assertEqual(result['state'], 'applied')
            self.assertEqual([e['request'] for e in result['checkpoint']['accepted_responses']],
                             [e['request'] for e in f['accepted_responses']])
        self.assertEqual(len(commands), 11)

    def test_runtime_verification_and_wrong_label_agree_with_official_schema(self):
        for f in self.flows():
            for result, expected_coverage in ((None, 'missing'), (f['apply_result'], 'complete')):
                value = verify_installation(f['manifest'], f['plan'],
                    vectors.AlignedCatalog(f, 6, f['observations'][-1]), result)
                fr4.verification_check(f, result, value)
                self.assertEqual(value['response_evidence'], expected_coverage)
                changed = deepcopy(value)
                changed['receipt_readback'] = 'captured_responses_only_spine_0.10.0'
                self.assertFalse(o.validator('spine-pack-verification-result.v2.schema.json').is_valid(changed))
                with self.assertRaises(vectors.PlanError):
                    validate(changed, 'spine-pack-verification-result.v2.schema.json')

    def test_v1_profile_reference_chain_and_projection_preserve_embedded_contract(self):
        def terminal(name, definition):
            pointer = '/$defs/' + definition
            while True:
                value = o.load(o.SCHEMAS / name)
                for token in pointer.split('/')[1:]: value = value[token]
                if '$ref' not in value: return name, pointer, value
                sibling, _, pointer = value['$ref'].partition('#')
                name = sibling or name
        prior = terminal('spine-pack-embedded-values.v2.schema.json', 'profile_v1')
        f = vectors.planning_fixture(); owner = f['plan']['request']['owner']
        row = next(r for r in f['plan']['observation']['entries']
                   if r['revision_contract'] == 'spine.notification-profiles.v1')
        for runtime, baseline in vectors.BASELINES.items():
            with self.subTest(runtime=runtime):
                self.assertEqual(terminal(baseline.public_schema, 'semantic_profile_v1'), prior)
                value = o.unblob(row['value'])
                o.validator('spine-pack-embedded-values.v2.schema.json', 'profile_v1').validate(value)
                o.validator(baseline.public_schema, 'semantic_profile_v1').validate(value)
                self.assertEqual(projected_state(row, owner, runtime_version=runtime), value)
                value['revision']['templates'][0]['rendering'] = {'unexpected': 'v2-only'}
                for name, definition in (('spine-pack-embedded-values.v2.schema.json', 'profile_v1'),
                                         (baseline.public_schema, 'semantic_profile_v1')):
                    self.assertFalse(o.validator(name, definition).is_valid(value))


if __name__ == '__main__': unittest.main()
