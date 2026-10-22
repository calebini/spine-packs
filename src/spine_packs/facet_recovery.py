"""FR-4 read-only prefix comparison foundation, not a continuation executor.

No acceptance, retry, checkpoint publication or CLI activation occurs here.
Fresh views must come from the bounded public observer, not an internal ledger.
"""
from copy import deepcopy

from .facet_contracts import artifact, body
from .facet_execution import ExecutionContext, guarded, observation
from .facet_observation import observe
from .planning import INVALID, require

STALE = 'stale_plan_or_target_mismatch'


def immutable_lineage(rows):
    """A known immutable revision cannot change root, decoder or content.

    Mutable profile metadata and root status are not immutable revision facts.
    """
    known = {}
    for row in rows:
        revision = row['revision_id']
        if revision is None:
            continue
        value = body(row['value'])
        if row['object_key'].startswith('profile:'):
            value = value['revision']
        identity = (row['root_id'], row['revision_contract'], value)
        require(revision not in known or known[revision] == identity,
                'immutable_revision_contradiction', INVALID)
        known[revision] = identity


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

    This first increment deliberately admits only the exact prefix. The
    prefix-plus-one uncertain candidate and replay are separate work.
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

    def lineage(self):
        """Exact non-current pins to freshly read, not to trust from disk."""
        return deepcopy(self._expected['historical_revisions'])

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
