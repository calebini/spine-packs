"""FR-4 forward admission and replay correlation; no write or publication.

No acceptance, retry, checkpoint publication or CLI activation occurs here.
Fresh views must come from the bounded public observer, not an internal ledger.
"""
from copy import deepcopy

from .facet_contracts import artifact, blob, body, validate
from .facet_execution import ExecutionContext, guarded, immutable_lineage, observation, projected_state, public_body
from .facet_inventory import COMMANDS
from .facet_observation import observe, state
from .planning import ENVIRONMENT, INVALID, require

STALE = 'stale_plan_or_target_mismatch'


def forward_view(view, posts):
    """Private comparison projection, never a fabricated public snapshot.

    Callers validate the base observation and each explained post-state first.
    Original immutable revisions survive head changes even without consumers.
    """
    result = deepcopy(view)
    entries = {r['object_key']: r for r in result['entries']}
    history = {(r['object_key'], r['revision_id']): r for r in result['historical_revisions']}
    immutable_lineage([*entries.values(), *history.values(), *posts])
    for value in posts:
        post = deepcopy(value)
        old = entries.get(post['object_key'])
        if old and old['revision_id'] is not None and old['revision_id'] != post['revision_id']:
            history[(old['object_key'], old['revision_id'])] = old
        entries[post['object_key']] = post
        if post['object_key'].startswith('profile:'):
            # Historical show combines the immutable revision with the current
            # mutable root metadata. Forward only this explained root effect;
            # preserve every historical ID, decoder and revision body.
            metadata = body(post['value'])['metadata']
            for row in history.values():
                if row['object_key'] == post['object_key'] and row['root_id'] == post['root_id']:
                    value = body(row['value'])
                    value['metadata'] = deepcopy(metadata)
                    row['value'] = blob(value)
    result['entries'] = [entries[k] for k in sorted(entries)]
    result['historical_revisions'] = [history[k] for k in sorted(history)]
    require(len(entries) + len(history) <= 4096, 'observation_capacity', INVALID)
    # Fresh public fingerprints are checked by the observer. These fields may
    # not be presented as predictions or new Spine attestations.
    del result['public_catalog_snapshots']
    del result['digest']
    return result


class RecoveryPreimage(ExecutionContext):
    """Validate an approved checkpoint and derive its accepted-prefix view.

    Admission is private comparison, not acceptance or submission authority.
    """

    @guarded(INVALID)
    def __init__(self, manifest, plan, approval, checkpoint):
        super().__init__(manifest, plan, approval)
        self._content_contracts = tuple(manifest['compatibility']['spine_content_contracts'])
        require(isinstance(checkpoint, dict), 'invalid_recovery_checkpoint', INVALID)
        self._checkpoint = deepcopy(checkpoint)
        cp = self._checkpoint
        artifact(cp, 'apply-checkpoint')
        require(cp['plan_digest'] == self._plan['content_identity']['digest']
                and cp['approval_digest'] == self._approval['content_identity']['digest']
                and cp['execution'] == self._approval['execution'],
                'checkpoint_execution_mismatch', INVALID)
        self._prefix(cp['accepted_responses'])
        index = len(cp['accepted_responses'])
        actions = self._plan['actions']
        next_id = actions[index]['action_id'] if index < len(actions) else None
        require(cp['next_action_id'] == next_id, 'checkpoint_next_action_mismatch', INVALID)
        pending = cp['unresolved_submission']
        if pending is not None:
            require(next_id is not None, 'completed_checkpoint_has_submission', INVALID)
            request = self.materialize(cp['accepted_responses'])
            require(pending['action_id'] == next_id and pending['command_id'] == request['command_id']
                    and body(pending['request']) == request,
                    'checkpoint_request_mismatch', INVALID)
        self._expected = forward_view(self._plan['observation'],
            [e['post_observation'] for e in cp['accepted_responses']])

    def expected_view(self):
        return deepcopy(self._expected)

    def lineage(self, *, include_pending=False):
        """Exact non-current pins to freshly read, not to trust from disk."""
        rows = deepcopy(self._expected['historical_revisions'])
        cp = self._checkpoint
        if include_pending and cp['unresolved_submission'] is not None:
            action = self._plan['actions'][len(cp['accepted_responses'])]
            if ('revision' in COMMANDS[action['command']]['outputs'] and action['expected'] is not None):
                # A pending head advance needs its original revision freshly
                # retained even before a response has been accepted.
                rows.append(deepcopy(next(r for r in self._expected['entries']
                                         if r['object_key'] == action['object_key'])))
        return rows

    @guarded(INVALID)
    def compare_prefix(self, fresh, *, environment, target):
        require(environment == self._plan['environment']
                and target == self._plan['request']['target'], 'recovery_target_changed', STALE)
        observation(fresh, self._plan['request']['owner'])
        immutable_lineage([*self._expected['entries'], *self._expected['historical_revisions'],
                           *fresh['entries'], *fresh['historical_revisions']])
        require(forward_view(fresh, []) == self._expected, 'recovery_prefix_changed', STALE)
        # No returned IDs, accepted prefix mutation or request regeneration.
        return True

    @guarded(INVALID)
    def observe_prefix(self, transport, *, page_size=100):
        """Fresh bounded reads only; not admission, replay or verification.

        Construction validates saved inputs before any target access. History
        hints select public reads, never replace fresh evidence. The caller may
        not treat this comparison as authorization to continue an execution.
        """
        require(transport.target == self._plan['request']['target'], 'recovery_target_changed', STALE)
        environment, fresh = observe(transport, self._plan['request']['owner'], self._plan['closure'],
            page_size=page_size, content_contracts=self._content_contracts,
            lineage=self.lineage())
        self.compare_prefix(fresh, environment=environment, target=transport.target)
        return fresh

    def _candidate(self, row, record, archetype_record):
        """Validate only the first unresolved action, never a suffix producer."""
        cp, plan = self._checkpoint, self._plan
        require(cp['unresolved_submission'] is not None, 'uncertain_request_required', INVALID)
        index = len(cp['accepted_responses'])
        action = plan['actions'][index]
        request = self.materialize(cp['accepted_responses'])
        command = action['command']
        value = projected_state(row, plan['request']['owner'])
        require(row['object_key'] == action['object_key'] and row['status'] == 'active',
                'invalid_candidate_object', STALE)
        if action['expected'] is not None:
            require(row['root_id'] == action['expected']['root_id'], 'candidate_root_changed', STALE)
            if 'revision' in COMMANDS[command]['outputs']:
                require(row['revision_id'] != action['expected']['revision_id'],
                        'candidate_immutable_revision_reused', STALE)
        if command in ('item_archetype.create', 'item_archetype.revise'):
            require(archetype_record is not None, 'candidate_archetype_record_required', STALE)
            validate(dict(ok=True, command='item_archetype.show', response_contract='spine.item-archetypes.v1',
                item_archetype=archetype_record),
                'spine-readback-0.10.0.schema.json', COMMANDS['item_archetype.show']['response'], category=ENVIRONMENT)
            require(state('archetype', archetype_record, plan['request']['owner']) == row,
                    'candidate_archetype_record_mismatch', STALE)
            provenance = dict(created_by_command_id=request['command_id'],
                created_by_subject_id=request['actor_subject_id'], created_at_utc=request['action_timestamp_utc'])
            require(all(archetype_record['revision'][k] == v for k, v in provenance.items()),
                    'candidate_archetype_revision_provenance', STALE)
            if command.endswith('.create'):
                require(all(archetype_record[k] == v for k, v in provenance.items()),
                        'candidate_archetype_creation_provenance', STALE)
            desired = request['revision']
        elif command.startswith('facet_schema.'):
            desired = request['definition']
        elif command.startswith('notification_rendering_definition.'):
            require(record is not None, 'candidate_rendering_record_required', STALE)
            validate(dict(ok=True, command='notification_rendering_definition.show',
                contract_version=COMMANDS[command]['selector'], record=record),
                'spine-readback-0.10.0.schema.json',
                COMMANDS['notification_rendering_definition.show']['response'], category=ENVIRONMENT)
            require(state('rendering', record, plan['request']['owner']) == row,
                    'candidate_rendering_record_mismatch', STALE)
            provenance = {k: request[k] for k in ('command_id', 'actor_subject_id', 'action_timestamp_utc')}
            require(record['published'] == provenance, 'candidate_publication_mismatch', STALE)
            if command.endswith('.create'):
                require(record['created'] == provenance, 'candidate_creation_mismatch', STALE)
            desired = request['revision']
        elif command in ('item_archetype.facet_binding.set', 'notification_profile.binding.set'):
            fields = (('item_archetype_id', 'facet_key', 'facet_schema_revision_id')
                      if command.startswith('item_') else ('item_archetype_id', 'notification_profile_id'))
            desired = {k: request[k] for k in fields}
        elif command == 'notification_profile.metadata.update':
            expected = action['expected']
            require(row['revision_id'] == expected['revision_id']
                    and row['revision_contract'] == expected['revision_contract'],
                    'candidate_metadata_revision_changed', STALE)
            desired = dict(metadata=request['metadata'], revision=body(expected['value'])['revision'])
        else:
            authored = body(action['desired'])
            desired = dict(metadata={k: authored[k] for k in ('display_name', 'description')},
                           revision=request['revision'])
            require(row['revision_contract'] == 'spine.notification-profiles.v2', 'candidate_profile_decoder', STALE)
        require(value == desired, 'candidate_semantics_changed', STALE)
        immutable_lineage([*self._expected['entries'], *self._expected['historical_revisions'], row])

    @guarded(INVALID)
    def admit(self, fresh, *, environment, target, rendering_record=None, archetype_record=None):
        """Compare supplied fresh public evidence; perform no reads or writes.

        The result is a private comparison handle, not accepted response evidence
        or permission to submit. Transport collection and durability remain owned
        by their separate runtime boundaries.
        """
        fresh, rendering_record, archetype_record = deepcopy((fresh, rendering_record, archetype_record))
        require(environment == self._plan['environment'] and target == self._plan['request']['target'],
                'recovery_target_changed', STALE)
        observation(fresh, self._plan['request']['owner'])
        immutable_lineage([*self._expected['entries'], *self._expected['historical_revisions'],
                           *fresh['entries'], *fresh['historical_revisions']])
        actual = forward_view(fresh, [])
        candidate = None
        kind = 'prefix'
        if actual != self._expected:
            require(self._checkpoint['unresolved_submission'] is not None, 'unexplained_recovery_change', STALE)
            index = len(self._checkpoint['accepted_responses'])
            key = self._plan['actions'][index]['object_key']
            candidate = next((r for r in fresh['entries'] if r['object_key'] == key), None)
            require(candidate is not None, 'uncertain_candidate_missing', STALE)
            self._candidate(candidate, rendering_record, archetype_record)
            require(forward_view(self._plan['observation'],
                [e['post_observation'] for e in self._checkpoint['accepted_responses']] + [candidate]) == actual,
                'unexplained_recovery_change', STALE)
            kind = 'prefix_plus_one'
        retained_record = (rendering_record if candidate is not None
                           and candidate['object_key'].startswith('rendering:') else None)
        return RecoveryAdmission(self, kind, candidate, retained_record)


@guarded(INVALID)
def continuation_context(manifest, plan, approval, source):
    """Validate a checkpoint or terminal partial without editing its source."""
    require(isinstance(source, dict), 'invalid_continuation_source', INVALID)
    kind = source.get('artifact_schema')
    require(kind in ('spine.pack-apply-checkpoint.v2', 'spine.pack-apply-result.v2'),
            'invalid_continuation_source', INVALID)
    artifact(source, 'apply-result' if kind.endswith('result.v2') else 'apply-checkpoint')
    if kind == 'spine.pack-apply-result.v2':
        require(source['state'] == 'partial', 'continuation_requires_partial_result', INVALID)
        cp = source['checkpoint']
        context = RecoveryPreimage(manifest, plan, approval, cp)
        remaining = [a['action_id'] for a in context._plan['actions'][len(cp['accepted_responses']):]]
        require(bool(remaining) and source['failure']['action_id'] == remaining[0]
                and source['unattempted_action_ids'] == remaining[1:], 'partial_result_suffix_mismatch', INVALID)
        return context
    return RecoveryPreimage(manifest, plan, approval, source)


def preflight_continuation(manifest, plan, approval, source, transport, *, page_size=100):
    """Fresh bounded two-pass admission; never a replay or durability claim."""
    context = continuation_context(manifest, plan, approval, source)
    context.validate_known_requests()
    require(transport.target == context._plan['request']['target'], 'recovery_target_changed', STALE)
    cp = context._checkpoint
    record_key = None
    if cp['unresolved_submission'] is not None:
        action = context._plan['actions'][len(cp['accepted_responses'])]
        if action['object_key'].split(':')[0] in ('archetype', 'rendering'):
            record_key = action['object_key']
    observed = observe(transport, context._plan['request']['owner'], context._plan['closure'],
        page_size=page_size, content_contracts=context._content_contracts,
        lineage=context.lineage(include_pending=True), record_key=record_key)
    environment, fresh = observed[:2]
    record = observed[2] if record_key is not None else None
    return context.admit(fresh, environment=environment, target=transport.target,
        rendering_record=record if record_key and record_key.startswith('rendering:') else None,
        archetype_record=record if record_key and record_key.startswith('archetype:') else None)


class RecoveryAdmission:
    """Private correlation handle. No transport, publication or prefix advance."""

    def __init__(self, context, kind, candidate, rendering_record):
        self._context = deepcopy(context)
        self.kind = kind
        self._candidate = deepcopy(candidate)
        self._record = deepcopy(rendering_record)

    def checkpoint(self):
        return deepcopy(self._context._checkpoint)

    @guarded(INVALID)
    def retry_request(self):
        pending = self._context._checkpoint['unresolved_submission']
        require(pending is not None, 'uncertain_request_required', INVALID)
        return body(pending['request'])

    @guarded(ENVIRONMENT)
    def replay_evidence(self, raw_response, post_observation):
        self.retry_request()  # Complete/prefix-only checkpoints cannot infer a retry.
        context = self._context
        accepted = context._checkpoint['accepted_responses']
        evidence = context.response_evidence(accepted, raw_response, post_observation)
        if self._candidate is not None:
            require(evidence['post_observation'] == self._candidate, 'replay_candidate_mismatch')
        if self._record is not None:
            require(public_body(evidence['response'])['record'] == self._record, 'replay_rendering_record_mismatch')
        immutable_lineage([*context._expected['entries'], *context._expected['historical_revisions'],
                           evidence['post_observation']])
        return evidence

    @guarded(INVALID)
    def check_binding(self, current):
        context = self._context
        index = len(context._checkpoint['accepted_responses'])
        require(index < len(context._plan['actions']), 'binding_action_required', INVALID)
        action = context._plan['actions'][index]
        require(action['command'] in ('item_archetype.facet_binding.set', 'notification_profile.binding.set'),
                'binding_action_required', INVALID)
        expected = self._candidate if self._candidate is not None else action['expected']
        require(current == expected, 'binding_precondition_changed', STALE)
        return True
