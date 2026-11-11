"""V2 initial and same-execution continued apply through public commands."""
from copy import deepcopy
import hashlib

from . import artifacts as a
from .apply import checkpoint_writer as durable_writer, failure
from .facet_contracts import artifact, blob, seal, validate
from .facet_execution import ExecutionContext, public_body
from .facet_inventory import COMMANDS
from .facet_observation import Observer, state
from .facet_planning import plan_installation
from .facet_transport import ObservationBudget
from .planning import ENVIRONMENT, PlanError, require, validate_entry

STALE = 'stale_plan_or_target_mismatch'


def checkpoint(plan, approval, accepted, unresolved=None):
    index = len(accepted)
    cp = seal(dict(artifact_schema='spine.pack-apply-checkpoint.v2',
        plan_digest=plan['content_identity']['digest'], approval_digest=approval['content_identity']['digest'],
        execution=deepcopy(approval['execution']), accepted_responses=deepcopy(accepted),
        unresolved_submission=deepcopy(unresolved),
        next_action_id=plan['actions'][index]['action_id'] if index < len(plan['actions']) else None))
    artifact(cp, 'apply-checkpoint')
    return cp


def result(plan, cp, outcome, exc=None, action_id=None):
    index = len(cp['accepted_responses'])
    remaining = [a['action_id'] for a in plan['actions'][index:]]
    value = seal(dict(artifact_schema='spine.pack-apply-result.v2', checkpoint=deepcopy(cp), state=outcome,
        failure=failure(exc, action_id) if exc else None,
        unattempted_action_ids=remaining[1:] if outcome == 'partial' else remaining))
    artifact(value, 'apply-result')
    return value


def checkpoint_writer(path):
    return durable_writer(path, validator=lambda value: artifact(value, 'apply-checkpoint'))


def reader(transport, plan, page_size):
    # Each bounded readback/recheck operation has its own global budget; writes
    # retain their independent 30-second/16-MiB subprocess ceiling.
    transport.begin_observation(ObservationBudget())
    transport.check_target()
    return Observer(transport, plan['request']['owner'], plan['closure'], page_size)


def binding_row(observer, action, request):
    owner = observer.owner
    if action['command'] == 'item_archetype.facet_binding.set':
        rows, _ = observer.pages('item_archetype.facet_binding.list', 'bindings', lambda r: r['facet_key'],
                                  item_archetype_id=request['item_archetype_id'])
        require(len(rows) <= 100, 'facet_binding_capacity')
        matches = [r for r in rows if r['facet_key'] == request['facet_key']]
        for row in rows:
            require(row['status'] == 'active' and row['item_archetype_id'] == request['item_archetype_id'],
                    'facet_binding_scope_mismatch')
        fields = ('item_archetype_id', 'facet_key', 'facet_schema_revision_id')
        id_field = 'facet_binding_id'
    else:
        rows, fingerprint = observer.pages('notification_profile.binding.list', 'entries',
            lambda r: (r['item_archetype_id'], r['notification_profile_binding_id']), owner=owner, status='active')
        for row in rows:
            validate_entry(row, owner, 'binding')
            require(row['status'] == 'active', 'default_binding_status_mismatch')
        require(len({r['item_archetype_id'] for r in rows}) == len(rows), 'duplicate_default_binding')
        require(fingerprint == a.digest([{k: r[k] for k in ('item_archetype_id', 'notification_profile_id',
                'notification_profile_binding_id', 'status')} for r in rows]), 'binding_fingerprint_mismatch')
        matches = [r for r in rows if r['item_archetype_id'] == request['item_archetype_id']]
        fields = ('item_archetype_id', 'notification_profile_id')
        id_field = 'notification_profile_binding_id'
    require(len(matches) <= 1, 'ambiguous_binding')
    if not matches:
        return None
    row = matches[0]
    return dict(object_key=action['object_key'], owner=deepcopy(owner), status='active', root_id=row['item_archetype_id'],
        revision_id=None, binding_id=row[id_field], revision_contract=None, value=blob({k: row[k] for k in fields}))


def binding_guard(transport, plan, action, request, page_size):
    observed = binding_row(reader(transport, plan, page_size), action, request)
    require(observed == action['expected'], 'binding_precondition_changed', STALE)


def readback(transport, plan, action, request, raw_response, page_size):
    # A response's IDs select public reads, but cannot become accepted evidence
    # until exact ownership, hashes, semantics and response identity all agree.
    require(isinstance(raw_response, bytes), 'invalid_write_wire_evidence')
    raw = raw_response[:-1] if raw_response.endswith(b'\n') else raw_response
    response = public_body(dict(json_text=raw.decode('utf-8'), digest=hashlib.sha256(raw).hexdigest()))
    validate(response, 'spine-readback-0.10.0.schema.json', COMMANDS[action['command']]['response'], category=ENVIRONMENT)
    obs = reader(transport, plan, page_size)
    family = action['object_key'].split(':')[0]
    if family in ('binding', 'facet_binding'):
        row = binding_row(obs, action, request)
        require(row is not None, 'binding_readback_missing')
        return row
    prefix, id_field, identity = {
        'archetype': ('item_archetype', 'item_archetype_id', response.get('item_archetype_id')),
        'profile': ('notification_profile', 'notification_profile_id', response.get('notification_profile_id')),
        'schema': ('facet_schema', 'facet_schema_id', response.get('facet_schema_id')),
        'rendering': ('notification_rendering_definition', 'notification_rendering_definition_id',
                      response.get('record', {}).get('notification_rendering_definition_id')),
    }[family]
    shown = obs.read(prefix + '.show', **{id_field: identity})
    value = shown if family == 'schema' else shown['record' if family == 'rendering' else prefix]
    if family == 'rendering':
        require(response['record'] == value, 'rendering_public_readback_mismatch')
    elif 'revision_number' in response:
        require(str(response['revision_number']) == str(value['revision']['revision_number']),
                'revision_number_readback_mismatch')
    return state(family, value, plan['request']['owner'])


def apply_initial(manifest, plan, approval, transport, writer, *, page_size=100):
    manifest, plan, approval = deepcopy((manifest, plan, approval))
    context = ExecutionContext(manifest, plan, approval)
    context.validate_known_requests()
    accepted = []
    cp = checkpoint(plan, approval, accepted)
    try:
        request = seal(dict(artifact_schema='spine.pack-install-request.v2', request=plan['request']))
        fresh = plan_installation(manifest, request, transport, page_size=page_size)
        require(fresh == plan, 'stale_plan', STALE)
    except PlanError as exc:
        return result(plan, cp, 'not_applied', exc)
    return _execute(context, plan, approval, transport, writer, cp, page_size=page_size)


def apply_continuation(manifest, plan, approval, source, transport, writer, *, page_size=100):
    """Same-execution boundary; the caller protects source/destination paths.

    Callers supply an operator-selected source and a new private checkpoint
    writer. Invalid/stale admission raises before publication or submission.
    """
    from .facet_recovery import preflight_continuation
    manifest, plan, approval, source = deepcopy((manifest, plan, approval, source))
    admission = preflight_continuation(manifest, plan, approval, source, transport, page_size=page_size)
    cp = admission.checkpoint()
    writer(deepcopy(cp))  # New destination durable before retry, even for a complete checkpoint.
    context = ExecutionContext(manifest, plan, approval)
    return _execute(context, plan, approval, transport, writer, cp, page_size=page_size,
                    continuing=True, admission=admission)


def _execute(context, plan, approval, transport, writer, cp, *, page_size, continuing=False, admission=None):
    accepted = deepcopy(cp['accepted_responses'])
    start = len(accepted)
    if start == len(plan['actions']):
        if not continuing: writer(deepcopy(cp))
        return result(plan, cp, 'applied')
    for index in range(start, len(plan['actions'])):
        action = plan['actions'][index]
        retry = admission if index == start and cp['unresolved_submission'] is not None else None
        try:
            request = retry.retry_request() if retry is not None else context.materialize(accepted)
            if action['command'] in ('item_archetype.facet_binding.set', 'notification_profile.binding.set'):
                if retry is not None:
                    current = binding_row(reader(transport, plan, page_size), action, request)
                    retry.check_binding(current)
                else:
                    binding_guard(transport, plan, action, request, page_size)
        except PlanError as exc:
            return result(plan, cp, 'partial' if accepted or continuing else 'not_applied', exc, action['action_id'])
        pending = dict(action_id=action['action_id'], command_id=request['command_id'],
            submission_state='prepared_or_submitted', request=blob(request))
        cp = checkpoint(plan, approval, accepted, pending)
        writer(deepcopy(cp))  # Failure propagates before any submission.
        try:
            raw_response = transport.write(action['command'], deepcopy(request))
            post = readback(transport, plan, action, request, raw_response, page_size)
            evidence = (retry.replay_evidence(raw_response, post) if retry is not None else
                        context.response_evidence(accepted, raw_response, post))
            advanced = checkpoint(plan, approval, [*accepted, evidence])
        except (PlanError, ValueError, TypeError, KeyError, RecursionError, OSError) as exc:
            if not isinstance(exc, PlanError):
                exc = PlanError(ENVIRONMENT, 'invalid_or_uncertain_write_response')
            return result(plan, cp, 'partial', exc, action['action_id'])
        writer(deepcopy(advanced))  # No consumer before durable acceptance.
        cp = advanced
        accepted.append(evidence)
    return result(plan, cp, 'applied')
