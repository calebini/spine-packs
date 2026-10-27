"""FR-3 request/evidence helpers; no transport or filesystem mutation authority.

The future executor must perform fresh public preflight/readback and durably
accept a producer before passing its evidence as a consumer's accepted prefix.
These checks prove internal consistency, not authenticity, freshness or durability.
"""
from copy import deepcopy
from functools import wraps
import hashlib

from . import artifacts as a
from .facet_contracts import artifact, blob, body, seal, validate
from .facet_graph import allowed_slots, expected_template
from .facet_inventory import BASELINE, COMMANDS, CONTRACTS
from .facet_observation import snapshots
from .facet_planning import build_plan, validate_inputs
from .planning import ENVIRONMENT, INVALID, PACK_INVALID, PlanError, require

PUBLIC_SCHEMA = 'spine-readback-0.10.0.schema.json'
TYPES = 'spine-pack-installer-types.v2.schema.json'
WRITE_COMMANDS = frozenset(k for k, v in COMMANDS.items() if v['phase'] is not None)


def guarded(category):
    """Never expose raw malformed evidence or Python parser diagnostics."""
    def decorate(fn):
        @wraps(fn)
        def call(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except PlanError:
                raise
            except (ValueError, KeyError, TypeError, IndexError, OverflowError, RecursionError):
                raise PlanError(category, 'invalid_execution_evidence') from None
        return call
    return decorate


def command_id(plan_digest, execution_id, action_id):
    return 'spack_' + a.digest(dict(derivation_version='spine.pack-command-id.v2',
        plan_digest=plan_digest, execution_id=execution_id, action_id=action_id))


def pointer(value, path, replacement=None, *, replace=False):
    # Only paths checked against the closed graph/inventory may reach here.
    parts = path.lstrip('/').split('/')
    for token in parts[:-1]:
        value = value[int(token)] if isinstance(value, list) else value[token]
    key = int(parts[-1]) if isinstance(value, list) else parts[-1]
    if replace:
        require(value[key] is None, 'non_null_reference_slot', INVALID)
        value[key] = replacement
    return value[key]


def projected_state(row, owner):
    validate(row, TYPES, 'state', category=ENVIRONMENT)
    require(row['owner'] == owner and row['root_id'] is not None, 'post_owner_or_root')
    family = row['object_key'].split(':')[0]
    binding = family in ('binding', 'facet_binding')
    require((row['binding_id'] is not None) == binding
            and (row['revision_id'] is None) == binding
            and (row['revision_contract'] is None) == binding, 'post_identity_shape')
    decoder = row['revision_contract']
    if family == 'profile':
        require(decoder in ('spine.notification-profiles.v1', 'spine.notification-profiles.v2'), 'post_decoder')
        if decoder.endswith('.v1'):
            family = 'profile_v1'
    elif not binding:
        require(decoder == {'archetype': 'spine.item-archetypes.v1',
            'schema': 'spine.facet-schemas.v1', 'rendering': 'spine.notification-rendering-definitions.v1'}[family],
            'post_decoder')
    value = body(row['value'])
    validate(value, 'spine-pack-embedded-values.v2.schema.json', family, category=ENVIRONMENT)
    if binding:
        require(value['item_archetype_id'] == row['root_id'], 'binding_root_mismatch')
    return value


def observation(view, owner):
    validate(view, TYPES, 'observation')
    require(view['owner'] == owner and view['digest'] == a.digest(dict(
        derivation_version='spine.pack-observation.v2', view={k: v for k, v in view.items() if k != 'digest'})),
        'invalid_observation_identity', INVALID)
    entries, history = view['entries'], view['historical_revisions']
    require(len(entries) + len(history) <= 4096, 'observation_capacity', INVALID)
    for keys in ([r['object_key'] for r in entries], [(r['object_key'], r['revision_id']) for r in history]):
        require(keys == sorted(set(keys)), 'observation_order', INVALID)
    for row in entries + history:
        projected_state(row, owner)
    current = {r['object_key']: r for r in entries}
    for row in history:
        parent = current.get(row['object_key'])
        require(parent is not None and row['root_id'] == parent['root_id']
                and row['revision_id'] != parent['revision_id'], 'historical_membership', INVALID)
    roots = [r['root_id'] for r in entries if r['binding_id'] is None]
    require(len(roots) == len(set(roots)), 'duplicate_root', INVALID)
    require(view['public_catalog_snapshots'] == snapshots(entries), 'observation_snapshots', INVALID)


def receipt(command, response):
    family = COMMANDS[command]['family']
    if family == 'catalog':
        return dict(family=family, **{k: response['receipt'][k] for k in
            ('command_receipt_id', 'effect', 'semantic_facts_hash', 'created_at_utc')})
    return dict(family=family, audit_id=response.get('audit_id'), **{k: response[k] for k in
        ('command_receipt_id', 'effect', 'changed', 'replayed')})


def public_body(value):
    validate(value, TYPES, 'publicResponse', category=ENVIRONMENT)
    raw = value['json_text'].encode('utf-8')
    require(len(raw) <= 16 * 1024 * 1024 and hashlib.sha256(raw).hexdigest() == value['digest'],
            'invalid_response_bytes')
    return a.parse_json(raw, public_response=True)


@guarded(INVALID)
def validate_saved_plan(manifest, plan):
    """Rebuild saved intent without requiring an applicable plan or approval."""
    require(isinstance(manifest, dict) and isinstance(plan, dict), 'invalid_execution_inputs', INVALID)
    artifact(plan, 'install-plan')
    req = seal(dict(artifact_schema='spine.pack-install-request.v2', request=plan['request']))
    validate_inputs(manifest, req)
    env = plan['environment']
    require(env['runtime_version'] == BASELINE['runtime']
            and env['ledger_schema_current'] == env['ledger_schema_implemented'] == BASELINE['schema'],
            'execution_baseline_mismatch', INVALID)
    advertised = env['advertised_contracts']
    require(advertised == sorted(set(advertised)) and set(CONTRACTS) <= set(advertised)
            and set(manifest['compatibility']['spine_content_contracts']) <= set(advertised)
            and plan['required_execution_contracts'] == CONTRACTS, 'execution_contracts_mismatch', INVALID)
    observation(plan['observation'], plan['request']['owner'])
    require(build_plan(manifest, req, env, plan['observation']) == plan, 'plan_rebuild_mismatch', INVALID)


def immutable_lineage(rows, *, category=INVALID):
    """Immutable revision identity excludes mutable profile root metadata."""
    known = {}
    for row in rows:
        revision = row['revision_id']
        if revision is None: continue
        value = body(row['value'])
        if row['object_key'].startswith('profile:'): value = value['revision']
        identity = (row['root_id'], row['revision_contract'], value)
        require(revision not in known or known[revision] == identity,
                'immutable_revision_contradiction', category)
        known[revision] = identity


class ExecutionContext:
    """Exact applicable approved graph; still no transport or write authority."""

    @guarded(INVALID)
    def __init__(self, manifest, plan, approval):
        require(all(isinstance(v, dict) for v in (manifest, plan, approval)), 'invalid_execution_inputs', INVALID)
        self._plan, self._approval = deepcopy(plan), deepcopy(approval)
        p, ap = self._plan, self._approval
        validate_saved_plan(manifest, p); artifact(ap, 'install-approval')
        require(p['pack']['status'] == 'released', 'draft_plan_not_applicable', PACK_INVALID)
        require(not p['blocked_object_keys'], 'blocked_plan_not_applicable', 'blocked_desired_state')
        require(p['apply_eligible'] and ap['plan_digest'] == p['content_identity']['digest']
                and ap['authorized_update_action_ids'] == p['decision_action_ids'], 'invalid_execution_approval', INVALID)

    def _request(self, index, decoded):
        p, ap = self._plan, self._approval
        require(type(index) is int and 0 <= index < len(p['actions']), 'invalid_action_index', INVALID)
        action = p['actions'][index]; cmd = action['command']
        require(cmd in WRITE_COMMANDS, 'configuration_write_required', INVALID)
        request = body(action['request_template'])
        require(request == expected_template(action, p['request']['owner']), 'invalid_command_template', INVALID)
        slots = allowed_slots(action, body(action['desired']))
        require(action['slots'] == [dict(request_pointer=k, object_key=v[0], field=v[1])
                for k, v in sorted(slots.items())], 'invalid_reference_slots', INVALID)
        resolutions = {r['object_key']: r for r in p['resolutions']}
        for path, (key, field) in slots.items():
            source = resolutions[key][field]
            if source['kind'] == 'observed':
                identity = source['value']
            else:
                require(source['action_id'] in decoded, 'producer_evidence_required', INVALID)
                identity = pointer(decoded[source['action_id']], source['output_pointer'])
            pointer(request, path, identity, replace=True)
        request.update({k: ap['execution'][k] for k in ('actor_subject_id', 'action_timestamp_utc')},
            command_id=command_id(p['content_identity']['digest'], ap['execution']['execution_id'], action['action_id']))
        validate(request, PUBLIC_SCHEMA, COMMANDS[cmd]['request'])
        if cmd.startswith('notification_rendering_definition.'):
            require(len(a.canonical_text(request['revision']).encode()) <= 8192, 'resolved_rendering_capacity', INVALID)
        if cmd.startswith('facet_schema.'):
            require(len(a.canonical_text(request['definition']).encode()) <= 32768, 'resolved_facet_capacity', INVALID)
        if cmd in ('notification_profile.create', 'notification_profile.revise'):
            require(len(a.canonical_text(request).encode()) <= 32768, 'resolved_profile_capacity', INVALID)
        return request

    def _check_response(self, action, request, response, post):
        cmd = action['command']; owner = self._plan['request']['owner']
        validate(response, PUBLIC_SCHEMA, COMMANDS[cmd]['response'], category=ENVIRONMENT)
        require(response.get('ok') is True and response.get('command') == cmd
                and not response.get('dry_run'), 'invalid_write_response')
        rec = response.get('receipt', response)
        require(rec['command_id'] == request['command_id'], 'response_command_id')
        if COMMANDS[cmd]['family'] == 'catalog':
            require(rec['semantic_facts_hash'] == a.digest(request)
                    and rec['created_at_utc'] == request['action_timestamp_utc']
                    and rec['effect'] == response['effect'], 'catalog_receipt_mismatch')
        value = projected_state(post, owner)
        require(post['object_key'] == action['object_key'] and post['status'] == 'active', 'post_object_or_status')
        if 'status' in response:
            require(response['status'] == post['status'], 'response_status_mismatch')
        for field, path in COMMANDS[cmd]['outputs'].items():
            require(post[field + '_id'] == pointer(response, path), 'response_output_mismatch')
        # A published/revised effect produces a new immutable revision even when
        # its receipt is replayed. Catalog responses do not have a changed flag.
        # Metadata-only writes have no revision output; no-ops are checked below.
        if (action['expected'] and 'revision' in COMMANDS[cmd]['outputs']
                and not response['effect'].endswith('noop')):
            require(post['revision_id'] != action['expected']['revision_id'], 'immutable_revision_id_reused')
        for field in ('item_archetype_id', 'notification_profile_id', 'facet_schema_id', 'notification_rendering_definition_id'):
            if field in request and field in response:
                require(response[field] == request[field], 'response_target_mismatch')
        for field in ('archetype_key', 'profile_key'):
            if field in request:
                require(response[field] == request[field], 'response_key_mismatch')
        if 'prior_revision_id' in response:
            require(response['prior_revision_id'] == request.get('expected_current_revision_id'), 'prior_revision_mismatch')
        if 'prior_binding_id' in response:
            require(response['prior_binding_id'] == request['expected_binding_id'], 'prior_binding_mismatch')
        if action['expected']:
            require(post['root_id'] == action['expected']['root_id'], 'changed_root')
        if cmd in ('item_archetype.create', 'item_archetype.revise'):
            require(value == request['revision'], 'archetype_readback_mismatch')
        elif cmd.startswith('facet_schema.'):
            require(value == request['definition'], 'schema_readback_mismatch')
        elif cmd.startswith('notification_rendering_definition.'):
            record = response['record']
            require(value == request['revision'] == record['revision'], 'rendering_readback_mismatch')
            require(record['owner'] == owner and record['status'] == 'active'
                    and record['definition_key'] == action['object_key'].split(':')[1]
                    and record['notification_rendering_definition_id'] == post['root_id']
                    and record['current_revision_id'] == post['revision_id'], 'rendering_identity_mismatch')
            require(record['definition_hash'] == a.digest(dict(contract_version=COMMANDS[cmd]['selector'],
                canonical_json_version='spine.canonical-json.v1', revision=value)), 'rendering_hash_mismatch')
            provenance = {k: request[k] for k in ('command_id', 'actor_subject_id', 'action_timestamp_utc')}
            require(record['published'] == provenance, 'rendering_provenance_mismatch')
            if cmd.endswith('.create'):
                require(record['created'] == provenance, 'rendering_create_provenance_mismatch')
        elif cmd in ('item_archetype.facet_binding.set', 'notification_profile.binding.set'):
            fields = (('item_archetype_id', 'facet_key', 'facet_schema_revision_id')
                      if cmd == 'item_archetype.facet_binding.set' else ('item_archetype_id', 'notification_profile_id'))
            require(value == {k: request[k] for k in fields}, 'binding_readback_mismatch')
            require(all(response[k] == request[k] == value[k] for k in fields), 'binding_response_mismatch')
        elif cmd == 'notification_profile.metadata.update':
            require(value['metadata'] == request['metadata']
                    and value['revision'] == body(action['expected']['value'])['revision']
                    and post['revision_id'] == action['expected']['revision_id']
                    and post['revision_contract'] == action['expected']['revision_contract'], 'metadata_readback_mismatch')
            require(response['notification_profile_revision_id'] == post['revision_id']
                    and all(response[k] == value['metadata'][k] for k in ('display_name', 'description')),
                    'metadata_response_mismatch')
        else:
            desired = body(action['desired'])
            require(value['revision'] == request['revision'] and post['revision_contract'] == 'spine.notification-profiles.v2'
                    and value['metadata'] == {k: desired[k] for k in ('display_name', 'description')}, 'profile_readback_mismatch')
            templates = [dict(t, normalized_template_hash=a.digest(dict(
                derivation_version='spine.notification-profile-template-hash.v2',
                canonical_json_version='spine.canonical-json.v1', template=t))) for t in request['revision']['templates']]
            require(response['normalized_revision_hash'] == a.digest(dict(
                derivation_version='spine.notification-profile-revision-hash.v2', canonical_json_version='spine.canonical-json.v1',
                revision=dict(request['revision'], templates=templates))), 'profile_hash_mismatch')
        if response['effect'].endswith('noop'):
            require(post == action['expected'], 'noop_cannot_explain_change')

    def _prefix(self, accepted):
        require(isinstance(accepted, list) and len(accepted) <= len(self._plan['actions']), 'invalid_prefix', INVALID)
        decoded = {}
        for i, evidence in enumerate(accepted):
            validate(evidence, TYPES, 'evidence')
            action = self._plan['actions'][i]; req = self._request(i, decoded)
            require(evidence['action_id'] == action['action_id'] and evidence['command'] == action['command']
                    and evidence['command_id'] == req['command_id'] and body(evidence['request']) == req,
                    'invalid_prefix_request', INVALID)
            response = public_body(evidence['response'])
            self._check_response(action, req, response, evidence['post_observation'])
            require(evidence['receipt'] == receipt(action['command'], response), 'invalid_receipt_projection', INVALID)
            decoded[action['action_id']] = response
        return decoded

    @guarded(INVALID)
    def validate_known_requests(self):
        """Preflight known IDs before any submission; never guess producer IDs."""
        resolutions = {r['object_key']: r for r in self._plan['resolutions']}
        for i, action in enumerate(self._plan['actions']):
            if all(resolutions[s['object_key']][s['field']]['kind'] == 'observed'
                   for s in action['slots']):
                self._request(i, {})

    @guarded(INVALID)
    def materialize(self, accepted):
        """Construct only the next action, using a completely validated prefix."""
        return self._request(len(accepted), self._prefix(accepted))

    @guarded(ENVIRONMENT)
    def response_evidence(self, accepted, raw_response, post_observation):
        """Validate supplied fresh readback; return evidence, never advance state.

        Preserve wire bytes except exactly one terminal CLI newline. Caller must
        durably publish this result before adding it to an accepted prefix.
        """
        require(isinstance(raw_response, bytes) and len(raw_response) <= 16 * 1024 * 1024, 'invalid_response_bytes')
        request = self.materialize(accepted)
        action = self._plan['actions'][len(accepted)]
        raw = raw_response[:-1] if raw_response.endswith(b'\n') else raw_response
        wire = dict(json_text=raw.decode('utf-8'), digest=hashlib.sha256(raw).hexdigest())
        response = public_body(wire)
        self._check_response(action, request, response, post_observation)
        evidence = dict(action_id=action['action_id'], command=action['command'], command_id=request['command_id'],
            request=blob(request), response=wire, receipt=receipt(action['command'], response),
            post_observation=deepcopy(post_observation))
        validate(evidence, TYPES, 'evidence', category=ENVIRONMENT)
        return evidence
