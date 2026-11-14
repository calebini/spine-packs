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
