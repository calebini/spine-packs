"""Initial-apply public CLI adapter; the planning adapter remains read-only."""
import re

from .facet_contracts import validate
from .facet_execution import PUBLIC_SCHEMA, WRITE_COMMANDS
from .facet_inventory import COMMANDS
from .facet_transport import FacetSpineCommand
from .planning import ENVIRONMENT, PlanError, require, validate_readback

# Exact 8f3c50b commands/cli.py EXIT_BY_ERROR; runtime_failure is the final
# handler fallback (exit 1). Unknown shapes/codes/exits are environment failures.
FAILURE_EXITS = dict.fromkeys(('invalid_request', 'unsupported_command', 'unsupported_field',
    'missing_required_field', 'invalid_timestamp', 'wrong_item_type', 'invalid_state_transition',
    'facet_schema_invalid', 'facet_value_invalid', 'facet_schema_retired',
    'unsupported_contract_version', 'rendering_definition_invalid', 'rendering_definition_retired'), 2)
FAILURE_EXITS.update(dict.fromkeys(('referenced_row_not_found', 'facet_reference_unavailable',
    'rendering_disclosure_unavailable'), 4))
FAILURE_EXITS.update(dict.fromkeys(('semantic_conflict', 'stale_cursor', 'facet_binding_conflict',
    'facet_archetype_conflict', 'rendering_disclosure_scope_mismatch'), 6))
FAILURE_EXITS.update(stale_version=5, environment_failure=7, runtime_failure=1)


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
        validate(request, PUBLIC_SCHEMA, COMMANDS[command]['request'], category=ENVIRONMENT)
        self.timeout = 30
        self._write_bytes = bytearray()
        try:
            response, exit_code = self._invoke(command, request)
            require(response.get('command') == command and not response.get('dry_run'), 'invalid_public_response')
            if response.get('ok') is False:
                validate_readback(response, 'commandFailure')
                code = response['error']['code']
                require(re.fullmatch(r'[a-z][a-z0-9_.:-]{0,159}', code) is not None
                        and code in FAILURE_EXITS and exit_code == FAILURE_EXITS[code], 'invalid_write_failure')
                error = PlanError(ENVIRONMENT if exit_code in (1, 7) else 'spine_command_rejection', 'spine_write_rejected')
                error.facts = [{'name': 'spine_error_code', 'value': code}]
                raise error
            require(exit_code == 0 and response.get('ok') is True, 'spine_write_failed')
            validate(response, PUBLIC_SCHEMA, COMMANDS[command]['response'], category=ENVIRONMENT)
            require(bool(self._write_bytes), 'missing_write_wire_evidence')
            return bytes(self._write_bytes)
        finally:
            self._write_bytes = None
