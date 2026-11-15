"""Initial-apply public CLI adapter; the planning adapter remains read-only."""
import re

from .facet_contracts import validate
from .facet_execution import WRITE_COMMANDS
from .facet_inventory import COMMANDS
from .facet_transport import FacetSpineCommand, FAILURE_EXITS
from .planning import ENVIRONMENT, PlanError, require, validate_readback

# Use the pinned command-family failure contracts where Spine publishes one.
# The older generic envelope remains the compatibility boundary for command
# families without a contextual failure schema in the qualified inventory.
FAMILY_FAILURES = {
    'facet': 'public_0138',
}


class FacetApplyCommand(FacetSpineCommand):
    def __init__(self, target, **kwargs):
        super().__init__(target, **kwargs)
        self._write_bytes = None

    def _received(self, chunk):
        if self._write_bytes is None:
            return super()._received(chunk)
        require(len(self._write_bytes) + len(chunk) <= 16 * 1024 * 1024, 'spine_response_too_large')
        self._write_bytes.extend(chunk)

    def write(self, command, request):
        require(command in WRITE_COMMANDS, 'write_command_not_allowed')
        baseline = self.select_runtime(self.baseline.runtime)
        validate(request, baseline.public_schema, COMMANDS[command]['request'], category=ENVIRONMENT)
        self.timeout = 30
        self._write_bytes = bytearray()
        try:
            response, exit_code = self._invoke(command, request)
            require(response.get('command') == command and not response.get('dry_run'), 'invalid_public_response')
            if response.get('ok') is False:
                family_failure = FAMILY_FAILURES.get(COMMANDS[command]['family'])
                if family_failure:
                    validate(response, baseline.public_schema, family_failure, category=ENVIRONMENT)
                else:
                    validate_readback(response, 'commandFailure')
                code = response['error']['code']
                require(re.fullmatch(r'[a-z][a-z0-9_.:-]{0,159}', code) is not None
                        and code in FAILURE_EXITS and exit_code == FAILURE_EXITS[code], 'invalid_write_failure')
                error = PlanError(ENVIRONMENT if exit_code in (1, 7) else 'spine_command_rejection', 'spine_write_rejected')
                error.facts = [{'name': 'spine_error_code', 'value': code}]
                raise error
            require(exit_code == 0 and response.get('ok') is True, 'spine_write_failed')
            validate(response, baseline.public_schema, COMMANDS[command]['response'], category=ENVIRONMENT)
            require(bool(self._write_bytes), 'missing_write_wire_evidence')
            return bytes(self._write_bytes)
        finally:
            self._write_bytes = None
