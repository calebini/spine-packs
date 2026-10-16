"""Pure reviewed v2 graph and command-template mappings; never executes commands.

Derived from FR-1 mappings; the original official-schema test oracle is retained.
"""
from copy import deepcopy
from .facet_contracts import body as unblob
from .facet_inventory import COMMANDS
from .planning import require

def manifest_objects(manifest):
    result = {}
    for family, array, key in [('archetype', 'archetypes', 'archetype_key'), ('schema', 'facet_schemas', 'schema_key'),
                                ('rendering', 'rendering_definitions', 'definition_key'),
                                ('profile', 'notification_profiles', 'profile_key'), ('binding', 'binding_intents', 'archetype_key')]:
        for item in manifest[array]:
            result[family + ':' + item[key]] = item
    for item in manifest['archetype_facet_bindings']:
        result['facet_binding:' + item['archetype_key'] + ':' + item['facet_key']] = item
    return result


def closure(manifest, selection):
    objects = manifest_objects(manifest)
    if selection['mode'] == 'all':
        return sorted(objects)
    selected = set()
    def visit(key):
        require(key in objects, 'missing local object')
        if key in selected:
            return
        selected.add(key)
        obj = objects[key]
        if key.startswith('archetype:'):
            default = 'binding:' + obj['archetype_key']
            if default in objects:
                visit(default)
            for k in objects:
                if k.startswith('facet_binding:' + obj['archetype_key'] + ':'):
                    visit(k)
        elif key.startswith('binding:'):
            visit('profile:' + obj['notification_profile_key'])
        elif key.startswith('facet_binding:'):
            visit('schema:' + obj['schema_ref']['schema_key'])
        elif key.startswith('profile:'):
            for t in obj['revision']['templates']:
                if t['rendering']['kind'] == 'definition':
                    visit('rendering:' + t['rendering']['definition_ref']['definition_key'])
        elif key.startswith('rendering:'):
            for s in obj['revision']['selections']:
                visit('schema:' + s['schema_ref']['schema_key'])
    for key in selection['archetype_keys']:
        visit('archetype:' + key)
    return sorted(selected)


def allowed_slots(action, desired):
    cmd = action['command']
    result = {}
    if cmd == 'item_archetype.facet_binding.set':
        result['/item_archetype_id'] = ('archetype:' + desired['archetype_key'], 'root')
        result['/facet_schema_revision_id'] = ('schema:' + desired['schema_ref']['schema_key'], 'revision')
    elif cmd.startswith('notification_rendering_definition.'):
        for i, s in enumerate(desired['revision']['selections']):
            result[f'/revision/selections/{i}/facet_schema_revision_id'] = ('schema:' + s['schema_ref']['schema_key'], 'revision')
    elif cmd in ('notification_profile.create', 'notification_profile.revise'):
        for i, t in enumerate(desired['revision']['templates']):
            r = t['rendering']
            if r['kind'] == 'definition':
                key = 'rendering:' + r['definition_ref']['definition_key']
                p = f'/revision/templates/{i}/rendering/definition/notification_rendering_definition'
                result[p + '_id'] = (key, 'root')
                result[p + '_revision_id'] = (key, 'revision')
    elif cmd == 'notification_profile.binding.set':
        result['/item_archetype_id'] = ('archetype:' + desired['archetype_key'], 'root')
        result['/notification_profile_id'] = ('profile:' + desired['notification_profile_key'], 'root')
    return result


def expected_template(action, owner):
    """Exact declarative mapping; nulls are typed holes, never predicted IDs."""
    d = unblob(action['desired']); cmd = action['command']; old = action['expected']
    req = {'contract_version': COMMANDS[cmd]['selector']}
    if cmd == 'item_archetype.create':
        req.update(owner=owner, archetype_key=d['archetype_key'], revision=d['revision'])
    elif cmd == 'item_archetype.revise':
        req.update(item_archetype_id=old['root_id'], expected_current_revision_id=old['revision_id'], revision=d['revision'])
    elif cmd.startswith('facet_schema.'):
        req['definition'] = d['definition']
        if cmd.endswith('.create'):
            req.update(owner=owner, schema_key=d['schema_key'])
        else:
            req.update(facet_schema_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'item_archetype.facet_binding.set':
        req.update(item_archetype_id=None, facet_key=d['facet_key'], facet_schema_revision_id=None,
                   expected_binding_id=old['binding_id'] if old else None)
    elif cmd.startswith('notification_rendering_definition.'):
        req['revision'] = deepcopy(d['revision'])
        for s in req['revision']['selections']:
            del s['schema_ref']; s['facet_schema_revision_id'] = None
        if cmd.endswith('.create'):
            req.update(owner=owner, definition_key=d['definition_key'])
        else:
            req.update(notification_rendering_definition_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'notification_profile.metadata.update':
        req.update(notification_profile_id=old['root_id'], expected_metadata=unblob(old['value'])['metadata'],
                   metadata={k: d[k] for k in ('display_name', 'description')})
    elif cmd in ('notification_profile.create', 'notification_profile.revise'):
        req['revision'] = deepcopy(d['revision'])
        for t in req['revision']['templates']:
            if t['rendering']['kind'] == 'definition':
                t['rendering'] = {'kind': 'definition', 'definition': {
                    'notification_rendering_definition_id': None, 'notification_rendering_definition_revision_id': None}}
        if cmd.endswith('.create'):
            req.update(owner=owner, profile_key=d['profile_key'], **{k: d[k] for k in ('display_name', 'description')})
        else:
            req.update(notification_profile_id=old['root_id'], expected_current_revision_id=old['revision_id'])
    elif cmd == 'notification_profile.binding.set':
        req.update(owner=owner, item_archetype_id=None, notification_profile_id=None)
    return req


def desired_semantics(key, desired, resolutions):
    def resolve(k, f):
        source = resolutions[k][f]
        require(source is not None, 'missing resolution')
        # A tagged comparison token, never a guessed ID or a submitted request.
        return source['value'] if source['kind'] == 'observed' else {'pending_action': source['action_id'], 'output': source['output_pointer']}
    family = key.split(':')[0]
    if family == 'archetype': return desired['revision']
    if family == 'schema': return desired['definition']
    if family == 'rendering':
        body = deepcopy(desired['revision'])
        for s in body['selections']:
            s['facet_schema_revision_id'] = resolve('schema:' + s.pop('schema_ref')['schema_key'], 'revision')
        return body
    if family == 'profile':
        revision = deepcopy(desired['revision'])
        for t in revision['templates']:
            r = t['rendering']
            if r['kind'] == 'definition':
                k = 'rendering:' + r.pop('definition_ref')['definition_key']
                r['definition'] = {'notification_rendering_definition_id': resolve(k,'root'),
                                   'notification_rendering_definition_revision_id': resolve(k,'revision')}
        return {'metadata': {k:desired[k] for k in ('display_name','description')}, 'revision':revision}
    body = {'item_archetype_id':resolve('archetype:' + desired['archetype_key'],'root')}
    if family == 'facet_binding':
        body.update(facet_key=desired['facet_key'],facet_schema_revision_id=resolve('schema:' + desired['schema_ref']['schema_key'],'revision'))
    else:
        body['notification_profile_id'] = resolve('profile:' + desired['notification_profile_key'],'root')
    return body
