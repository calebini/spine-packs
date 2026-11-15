"""Read-only exact-baseline transport; no successor write entry point."""
import os
import time

from .facet_contracts import validate
from .facet_baselines import DEFAULT_RUNTIME, runtime_baseline
from .facet_inventory import COMMANDS, READ_COMMANDS
from .planning import require, PlanError, ENVIRONMENT, INCOMPATIBLE, validate_readback
from .spine_command import SpineCommand

# Exact CLI EXIT_BY_ERROR at both reviewed pins (8f3c50b and 3e65ef0), plus
# runtime_failure's final-handler fallback. Shared with the existing write
# adapter so this repair does not create a second error/exit interpretation.
FAILURE_EXITS = dict.fromkeys(('invalid_request', 'unsupported_command', 'unsupported_field',
    'missing_required_field', 'invalid_timestamp', 'wrong_item_type', 'invalid_state_transition',
    'facet_schema_invalid', 'facet_value_invalid', 'facet_schema_retired',
    'unsupported_contract_version', 'rendering_definition_invalid', 'rendering_definition_retired'), 2)
FAILURE_EXITS.update(dict.fromkeys(('referenced_row_not_found', 'facet_reference_unavailable',
    'rendering_disclosure_unavailable'), 4))
FAILURE_EXITS.update(dict.fromkeys(('semantic_conflict', 'stale_cursor', 'facet_binding_conflict',
    'facet_archetype_conflict', 'rendering_disclosure_scope_mismatch'), 6))
FAILURE_EXITS.update(stale_version=5, environment_failure=7, runtime_failure=1)


def revision_preflight_failure(result, exit_code):
    """Recognize only closed, pinned transport/common-preflight failures.

    Spine 8f3c50b: commands/cli.py and agent-command-contract Section 5.
    These are not the revision handler's missing/corrupt-evidence envelope.
    """
    error = result.get('error')
    if (set(result) != {'ok', 'command', 'error'} or not isinstance(error, dict)
            or set(error) != {'code', 'field', 'message'}
            or not all(isinstance(v, str) and v for v in error.values())):
        return False
    return (error['code'], error['field'], exit_code) in {
        ('invalid_request', 'db', 3), ('invalid_request', 'input', 3),
        ('invalid_request', 'request', 2),
        ('environment_failure', 'runtime_contracts', 7),
        ('environment_failure', 'ledger', 7),
    }


def reject_read_failure(command, result, exit_code, baseline):
    """Validate ordinary handler/preflight failures before assigning ownership.

    The exact-revision handler retains its separate failure contract below.
    Common preflight recognition preserves its existing rejection category.
    """
    if revision_preflight_failure(result, exit_code):
        raise PlanError('spine_command_rejection', 'spine_read_rejected')
    # A recognized preflight signature must pass the closed check above.
    # In particular, the common handler schema permits an empty message; it
    # must not turn an invalid request-preflight envelope into a rejection.
    error = result.get('error')
    require(not (isinstance(error, dict) and error.get('code') == 'invalid_request'
                 and error.get('field') in ('db', 'input', 'request')), 'invalid_read_preflight')
    family = COMMANDS[command]['family']
    if family == 'facet':
        validate(result, baseline.public_schema, 'public_0138', category=ENVIRONMENT)
    elif command in ('notification_profile.list', 'notification_profile.show'):
        validate(result, baseline.public_schema, 'public_0139', category=ENVIRONMENT)
    else:
        # No contextual failure schema is published in the reviewed inventory
        # for these families; retain the common closed compatibility envelope.
        validate_readback(result, 'commandFailure')
    error = result['error']; code = error['code']
    require(type(exit_code) is int and code in FAILURE_EXITS and exit_code == FAILURE_EXITS[code],
            'invalid_read_failure')
    category = ENVIRONMENT if exit_code in (1, 7) else 'spine_command_rejection'
    raise PlanError(category, 'spine_read_rejected')


class ObservationBudget:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.deadline = clock() + 600
        self.calls = 0
        self.bytes = 0

    def start_call(self):
        require(self.calls < 4096 and self.clock() < self.deadline, 'observation_capacity')
        self.calls += 1

    def received(self, chunk):
        self.bytes += len(chunk)
        require(self.bytes <= 128 * 1024 * 1024 and self.clock() < self.deadline, 'observation_capacity')


class FacetSpineCommand(SpineCommand):
    def __init__(self, target, *, runtime_version=None, **kwargs):
        super().__init__(target, **kwargs)
        self._baseline = None if runtime_version is None else runtime_baseline(runtime_version)
        self.budget = None
        self.response_bytes = 0
        self.response_limit = 16 * 1024 * 1024

    @property
    def baseline(self):
        return self._baseline or runtime_baseline(DEFAULT_RUNTIME)

    def select_runtime(self, runtime):
        selected = runtime_baseline(runtime)
        require(self._baseline is None or self._baseline == selected,
                'transport_baseline_mismatch', INCOMPATIBLE)
        self._baseline = selected
        return selected

    def begin_observation(self, budget):
        self.budget = budget
        # Presence only. Spine validates secret contents, permissions, and binding.
        # Never open, serialize, log, generate, or repair these files here.
        require(all(os.environ.get(k) for k in ('SPINE_FACET_CURSOR_CONFIG', 'SPINE_RENDERING_CURSOR_CONFIG')),
                'protected_cursor_config_required')

    def _command_arguments(self, command):
        return command.split('.')

    def _received(self, chunk):
        self.budget.received(chunk)
        self.response_bytes += len(chunk)
        require(self.response_bytes <= self.response_limit, 'spine_response_too_large')

    def write(self, command, request):
        raise PlanError(ENVIRONMENT, 'successor_write_not_authorized')

    def read(self, command, request):
        require(command in READ_COMMANDS, 'read_only_command_required')
        baseline = self.select_runtime(self.baseline.runtime)
        require(self.budget is not None, 'observation_budget_required')
        validate(request, baseline.public_schema, COMMANDS[command]['request'], category=ENVIRONMENT)
        self.budget.start_call()
        self.response_bytes = 0
        self.response_limit = (4 if command == 'facet_schema.revision.show' else 16) * 1024 * 1024
        self.timeout = min(30, self.budget.deadline - self.budget.clock())
        result, exit_code = self._invoke(command, request)
        require(result.get('command') == command and not result.get('dry_run'), 'invalid_public_response')
        if result.get('ok') is False:
            if command == 'facet_schema.revision.show':
                if revision_preflight_failure(result, exit_code):
                    raise PlanError('spine_command_rejection', 'spine_read_rejected')
                validate(result, baseline.public_schema, COMMANDS[command]['failure'], category=ENVIRONMENT)
                error = result['error']
                expected = 4 if error['code'] == 'referenced_row_not_found' else 7 if error['code'] == 'environment_failure' else 2
                require(exit_code == expected, 'invalid_failure_exit')
                category = ENVIRONMENT if exit_code == 7 else 'spine_command_rejection'
                raise PlanError(category, 'referenced_revision_missing' if exit_code == 4 else 'revision_read_failed')
            reject_read_failure(command, result, exit_code, baseline)
        require(exit_code == 0 and result.get('ok') is True, 'spine_read_failed')
        validate(result, baseline.public_schema, COMMANDS[command]['response'], category=ENVIRONMENT)
        return result
