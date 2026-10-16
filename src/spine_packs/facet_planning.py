"""FR-2 read-only plan compilation. Proposed write templates are data only."""
from copy import deepcopy

from . import artifacts as a
from .facet_contracts import artifact, blob, body, seal
from .facet_manifest import validate as validate_manifest, rendering_size_floor
from .facet_graph import manifest_objects, closure, desired_semantics, allowed_slots, expected_template
from .facet_inventory import COMMANDS, CONTRACTS
from .facet_observation import observe
from .planning import require, INVALID, PACK_INVALID, INCOMPATIBLE

PREFIX = {'archetype': 'item_archetype', 'schema': 'facet_schema', 'rendering': 'notification_rendering_definition',
          'profile': 'notification_profile', 'facet_binding': 'item_archetype.facet_binding', 'binding': 'notification_profile.binding'}
PHASE = {k: n for n, k in enumerate(('archetype', 'schema', 'facet_binding', 'rendering', 'profile', 'binding'))}


def dependencies(key, desired):
    family = key.split(':')[0]
    if family == 'facet_binding': return ['archetype:' + desired['archetype_key'], 'schema:' + desired['schema_ref']['schema_key']]
    if family == 'binding': return ['archetype:' + desired['archetype_key'], 'profile:' + desired['notification_profile_key']]
    if family == 'rendering': return ['schema:' + s['schema_ref']['schema_key'] for s in desired['revision']['selections']]
    if family == 'profile':
        return ['rendering:' + t['rendering']['definition_ref']['definition_key']
                for t in desired['revision']['templates'] if t['rendering']['kind'] == 'definition']
    return []


def build_plan(manifest, request, environment, observation):
    objects = manifest_objects(manifest)
    selected = closure(manifest, request['request']['selection'])
    existing = {r['object_key']: r for r in observation['entries']}
    resolutions, classifications, actions = {}, {}, []
    owner = request['request']['owner']

    def action(key, command, desired, old):
        index = str(len(actions))
        row = dict(ordinal=index, action_id='pending-' + index, command=command, object_key=key,
                   change_kind='create' if old is None else 'update', desired=blob(desired), expected=old)
        row['request_template'] = blob(expected_template(row, owner))
        row['slots'] = [dict(request_pointer=p, object_key=k, field=f) for p, (k, f) in sorted(allowed_slots(row, desired).items())]
        require('${' not in row['request_template']['canonical_json'], 'interpolation_forbidden', INVALID)
        actions.append(row)
        for field, pointer in COMMANDS[command]['outputs'].items():
            resolutions[key][field] = dict(kind='action_result', action_id=row['action_id'], output_pointer=pointer)

    for key in sorted(selected, key=lambda k: (PHASE[k.split(':')[0]], k)):
        desired, old = objects[key], existing.get(key)
        family = key.split(':')[0]; binding = family in ('binding', 'facet_binding')
        blocked = (old is not None and old['status'] == 'retired') or any(
            classifications[d]['classification'] == 'blocked' for d in dependencies(key, desired))
        resolution = dict(object_key=key, root=None, revision=None, binding=None)
        resolutions[key] = resolution
        if not blocked:
            if old:
                for field in ('root', 'revision', 'binding'):
                    if old[field + '_id'] is not None:
                        resolution[field] = dict(kind='observed', object_key=key, field=field, value=old[field + '_id'])
            if binding:
                resolution['root'] = deepcopy(resolutions['archetype:' + desired['archetype_key']]['root'])
            if family == 'rendering':
                known = {k.removeprefix('schema:'): r['revision']['value']
                         for k, r in resolutions.items() if k.startswith('schema:')
                         and r['revision'] and r['revision']['kind'] == 'observed'}
                require(rendering_size_floor(desired['revision'], known) <= 8192,
                        'rendering_definition_too_large', PACK_INVALID)
            semantic = desired_semantics(key, desired, resolutions)
            observed = body(old['value']) if old else None
            if family == 'profile' and old and old['revision_contract'].endswith('.v1'):
                for template in observed['revision']['templates']: template['rendering'] = {'kind': 'ordinary'}
            classification = 'missing' if old is None else 'equivalent' if semantic == observed else 'drifted'
        else:
            classification = 'blocked'
        classifications[key] = dict(object_key=key, classification=classification, desired=blob(desired), observed=old,
                                   blocked_reason='retired_definition_or_dependency' if blocked else None)
        if classification in ('blocked', 'equivalent'): continue
        prefix = PREFIX[family]
        if classification == 'missing':
            action(key, prefix + ('.set' if binding else '.create'), desired, old)
        elif family == 'profile':
            if semantic['metadata'] != observed['metadata']: action(key, prefix + '.metadata.update', desired, old)
            if semantic['revision'] != observed['revision']: action(key, prefix + '.revise', desired, old)
        else:
            action(key, prefix + ('.set' if binding else '.revise' if family == 'archetype' else '.publish'), desired, old)
    actions.sort(key=lambda row: (COMMANDS[row['command']]['phase'], row['object_key']))
    identities = {row['action_id']: f'action-{i:06d}' for i, row in enumerate(actions)}
    for i, row in enumerate(actions):
        row.update(ordinal=str(i), action_id=f'action-{i:06d}')
    for row in resolutions.values():
        for field in ('root', 'revision', 'binding'):
            source = row[field]
            if source and source['kind'] == 'action_result': source['action_id'] = identities[source['action_id']]
    blocked = sorted(k for k, c in classifications.items() if c['classification'] == 'blocked')
    plan = seal(dict(artifact_schema='spine.pack-install-plan.v2', request_digest=request['content_identity']['digest'],
        request=deepcopy(request['request']), pack=dict(manifest_schema=manifest['manifest_schema'], **manifest['pack'],
            manifest_digest=manifest['content_identity']['digest']), closure=selected, environment=environment,
        required_execution_contracts=CONTRACTS, observation=observation,
        classifications=[classifications[k] for k in selected], resolutions=[resolutions[k] for k in selected],
        actions=actions, decision_action_ids=[r['action_id'] for r in actions if r['change_kind'] == 'update'],
        blocked_object_keys=blocked, apply_eligible=manifest['pack']['status'] == 'released' and not blocked))
    artifact(plan, 'install-plan')
    return plan


def validate_inputs(manifest, request):
    validate_manifest(manifest)
    require(manifest['compatibility']['spine_runtime_versions'] == ['0.10.0'], 'successor_requires_exact_0100', INCOMPATIBLE)
    artifact(request, 'install-request')
    # Request-body semantics and target normalization are unchanged from v1.
    original = a.seal(dict(artifact_schema='spine.pack-install-request.v1', request=request['request']))
    require(not a.request_errors(original), 'invalid_request', INVALID)
    selection = request['request']['selection']
    if selection['mode'] == 'archetypes':
        require(set(selection['archetype_keys']) <= {x['archetype_key'] for x in manifest['archetypes']}, 'unknown_selection', INVALID)
    require(manifest['pack']['status'] != 'draft' or request['request']['draft_posture'] == 'inspect_only',
            'draft_inspection_not_allowed', PACK_INVALID)


def plan_installation(manifest, request, transport, *, page_size=100):
    validate_inputs(manifest, request)
    selected = closure(manifest, request['request']['selection'])
    environment, view = observe(transport, request['request']['owner'], selected, page_size=page_size,
                                content_contracts=manifest['compatibility']['spine_content_contracts'])
    require(set(manifest['compatibility']['spine_content_contracts']) <= set(environment['advertised_contracts']),
            'missing_content_contracts', INCOMPATIBLE)
    return build_plan(manifest, request, environment, view)
