"""Full qualification must reject omitted tests and all forms of skipped work."""
import importlib.util
import io
from pathlib import Path
import unittest
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('qualification_support', ROOT / 'tests/integration/qualification_support.py')
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


class QualificationCompletionTests(unittest.TestCase):
    def report(self, mode='complete', focused=False, harness='v1'):
        # Local synthetic unittest cases, never the public-CLI ledger harness.
        class Scenarios(unittest.TestCase):
            def id(self):
                if mode == 'arbitrary': return super().id()
                return support.SCENARIO_IDS[harness][names.index(self._testMethodName)]
            def test_a(self): pass
            def test_b(self):
                if mode == 'skip': self.skipTest('regression: skip whole scenario')
                if mode == 'subtest_skip':
                    with self.subTest(boundary='skipped'):
                        self.skipTest('regression: skip one required subcase')
                if mode == 'failure': self.fail('regression: scenario failed')
                if mode == 'error': raise RuntimeError('regression: scenario raised')
            def test_c(self): pass
            def test_d(self): pass

        names = ('test_a', 'test_b', 'test_c', 'test_d')
        selected = {'empty': (), 'missing': names[:3], 'duplicate': ('test_a', 'test_b', 'test_c', 'test_c'),
                    'focused': names[:1]}.get(mode, names)
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=support.QualificationResult).run(
            unittest.TestSuite(Scenarios(n) for n in selected))
        return support.completion_report(result, support.SCENARIO_IDS[harness], focused=focused)

    def test_four_successful_named_scenarios_qualify(self):
        for harness in ('v1', 'v2'):
            report = self.report(harness=harness)
            support.require_full_qualification(report, harness=harness)
            self.assertTrue(report['passed'] and report['full_qualification'])

    def test_empty_missing_duplicate_failed_and_errored_suites_fail_closed(self):
        for mode in ('empty', 'missing', 'duplicate', 'failure', 'error'):
            with self.subTest(mode=mode):
                report = self.report(mode)
                self.assertFalse(report['passed'])
                with self.assertRaisesRegex(RuntimeError, 'all four named'):
                    support.require_full_qualification(report, harness='v1')

    def test_scenario_or_subtest_skip_never_qualifies(self):
        for mode in ('skip', 'subtest_skip'):
            with self.subTest(mode=mode):
                report = self.report(mode)
                self.assertFalse(report['passed']); self.assertGreater(report['skipped'], 0)
                with self.assertRaises(RuntimeError): support.require_full_qualification(report, harness='v1')

    def test_focused_success_is_not_full_qualification(self):
        report = self.report('focused', focused=True)
        self.assertTrue(report['passed']); self.assertFalse(report['full_qualification'])
        with self.assertRaises(RuntimeError): support.require_full_qualification(report, harness='v1')
        # Even explicitly selecting all four stays a focused run.
        with self.assertRaises(RuntimeError): support.require_full_qualification(self.report(focused=True), harness='v1')

    def test_parent_rejects_incomplete_success_markers(self):
        good = self.report()
        for field in ('full_qualification', 'skipped', 'required_scenarios', 'successful_scenarios'):
            value = deepcopy(good); del value[field]
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                support.require_full_qualification(value, harness='v1')
        for fields in ({'skipped': 1}, {'tests': 0}, {'focused': True}, {'errors': 1},
                       {'successful_scenarios': good['successful_scenarios'][:3]}):
            with self.subTest(fields=fields), self.assertRaises(RuntimeError):
                support.require_full_qualification(dict(good, **fields), harness='v1')

    def test_parent_rejects_valid_report_from_other_harness(self):
        for actual, requested in (('v1', 'v2'), ('v2', 'v1')):
            report = self.report(harness=actual)
            self.assertTrue(report['full_qualification'])
            with self.subTest(actual=actual, requested=requested), self.assertRaises(RuntimeError):
                support.require_full_qualification(report, harness=requested)

    def test_parent_rejects_self_consistent_arbitrary_ids(self):
        report = self.report('arbitrary')
        # Model the previous false positive: both child-reported lists agree
        # and all success flags/counts look valid, but the IDs are untrusted.
        report.update(passed=True, full_qualification=True)
        report['required_scenarios'] = list(report['successful_scenarios'])
        self.assertEqual(len(report['successful_scenarios']), 4)
        for harness in ('v1', 'v2'):
            with self.subTest(harness=harness), self.assertRaises(RuntimeError):
                support.require_full_qualification(report, harness=harness)

    def test_unknown_or_omitted_parent_harness_cannot_qualify(self):
        with self.assertRaises(RuntimeError): support.require_full_qualification(self.report(), harness='unknown')
        with self.assertRaises(TypeError): support.require_full_qualification(self.report())


if __name__ == '__main__': unittest.main()
