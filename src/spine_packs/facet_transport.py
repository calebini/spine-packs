"""Read-only 0.10.0 transport; no successor write entry point."""
import os
import time

from .facet_contracts import validate
from .facet_inventory import COMMANDS, READ_COMMANDS
from .planning import require, PlanError, ENVIRONMENT
from .spine_command import SpineCommand


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
    def __init__(self, target, **kwargs):
        super().__init__(target, **kwargs)
        self.budget = None
        self.response_bytes = 0
        self.response_limit = 16 * 1024 * 1024

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
        require(self.budget is not None, 'observation_budget_required')
        validate(request, 'spine-readback-0.10.0.schema.json', COMMANDS[command]['request'], category=ENVIRONMENT)
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
                validate(result, 'spine-readback-0.10.0.schema.json', COMMANDS[command]['failure'], category=ENVIRONMENT)
                error = result['error']
                expected = 4 if error['code'] == 'referenced_row_not_found' else 7 if error['code'] == 'environment_failure' else 2
                require(exit_code == expected, 'invalid_failure_exit')
                category = ENVIRONMENT if exit_code == 7 else 'spine_command_rejection'
                raise PlanError(category, 'referenced_revision_missing' if exit_code == 4 else 'revision_read_failed')
            raise PlanError('spine_command_rejection', 'spine_read_rejected')
        require(exit_code == 0 and result.get('ok') is True, 'spine_read_failed')
        validate(result, 'spine-readback-0.10.0.schema.json', COMMANDS[command]['response'], category=ENVIRONMENT)
        return result
