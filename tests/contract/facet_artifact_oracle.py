"""Independent FR-1 artifact oracle. No transport, filesystem writes or Spine imports.

This is executable contract evidence, not the successor installer implementation.
"""
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import re

from test_facet_manifest_contract import ROOT, canonical, load, require, ordered, validate as validate_manifest

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    Draft202012Validator = None

SCHEMAS = ROOT / 'contracts/schemas'
INVENTORY = load(ROOT / 'contracts/installer-spine-0.9.1-inventory.json')
COMMANDS = INVENTORY['commands']
LIMITS = dict(zip(('install-request', 'install-plan', 'install-approval', 'apply-checkpoint',
                   'apply-result', 'verification-result', 'installer-result'),
                  (65536, 8388608, 262144, 16777216, 16777216, 16777216, 1048576)))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def hash_value(value):
    return sha(canonical(value))


def blob(value):
    text = canonical(value).decode()
    return {'canonical_json': text, 'digest': sha(text.encode())}


def parse(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON member')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON number')
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)
    def unicode_check(v):
        if isinstance(v, str):
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in v), 'invalid Unicode')
        elif isinstance(v, dict):
            for k, x in v.items():
                unicode_check(k)
                unicode_check(x)
        elif isinstance(v, list):
            for x in v:
                unicode_check(x)
    unicode_check(value)
    return value


def unblob(value, public=False):
    text = value['json_text' if public else 'canonical_json']
    require(sha(text.encode()) == value['digest'], 'embedded digest')
    decoded = parse(text)
    if not public:
        require(canonical(decoded).decode() == text, 'noncanonical embedded value')
    return decoded


def seal(value):
    value = deepcopy(value)
    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
    value['content_identity'] = {'algorithm': 'sha256', 'canonical_json_version': 'spine.canonical-json.v1',
                                 'derivation_version': 'spine.pack-' + kind + '-digest.v2'}
    value['content_identity']['digest'] = hash_value(value)
    return value


@lru_cache(maxsize=None)
def validator(filename, definition=None):
    resources = [(s['$id'], Resource.from_contents(s)) for p in SCHEMAS.glob('*.json')
                 if '$id' in (s := load(p))]
    registry = Registry().with_resources(resources)
    schema = load(SCHEMAS / filename)
    if definition:
        schema = {'$ref': schema['$id'] + '#/$defs/' + definition}
    return Draft202012Validator(schema, registry=registry)


def public_schema(command, direction, value):
    validator('spine-readback-0.9.1.schema.json', COMMANDS[command][direction]).validate(value)


def artifact(value):
    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
    require(kind in LIMITS and value['artifact_schema'].endswith('.v2'), 'artifact version')
    require(len(canonical(value)) <= LIMITS[kind], 'artifact size')
    validator('spine-pack-' + kind + '.v2.schema.json').validate(value)
    if kind != 'installer-result':
        require(value == seal(value), 'artifact digest')
    else:
        mapping={'0':('success',None),'2':('failed','invalid_cli_or_artifact_input'),
                 '3':('failed','invalid_pack_contract_or_digest'),'4':('failed','incompatible_spine_runtime_or_contracts'),
                 '5':('decision_required','decision_required_for_drift'),'6':('blocked','blocked_desired_state'),
                 '7':('failed','stale_plan_or_target_mismatch'),'8':('failed','spine_command_rejection'),
                 '9':('partial','partial_apply'),'10':('mismatch','verification_mismatch'),
                 '11':('failed','transport_or_environment_failure')}
        status,category=mapping[value['exit_code']]
        require(value['status']==status and (value['error']['category'] if value['error'] else None)==category,'exit/category correlation')
        if value['exit_code'] in ('0','5','6','9','10'): require(value['artifact'] is not None,'required output artifact')


def pointer(value, path, replacement=None, write=False):
    parts = path.split('/')[1:]
    for p in parts[:-1]:
        value = value[int(p)] if isinstance(value, list) else value[p]
    p = int(parts[-1]) if isinstance(value, list) else parts[-1]
    if write:
        value[p] = replacement
    else:
        return value[p]


def command_id(plan, approval, action):
    return 'spack_' + hash_value({'action_id': action['action_id'], 'derivation_version': 'spine.pack-command-id.v2',
                                 'execution_id': approval['execution']['execution_id'],
                                 'plan_digest': plan['content_identity']['digest']})


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


def observation_digest(view):
    return hash_value({'derivation_version': 'spine.pack-observation.v2',
                       'view': {k: v for k, v in view.items() if k != 'digest'}})


def public_snapshots(entries):
    """Only the three pinned legacy public fingerprints; no new-catalog hash."""
    rows = {'archetypes': [], 'profiles': [], 'bindings': []}
    for r in entries:
        family, key = r['object_key'].split(':',1)
        if family in ('archetype','profile'):
            row = {'id':r['root_id'],'key':key,'status':r['status'],'current_revision_id':r['revision_id']}
            if family=='profile': row.update(unblob(r['value'])['metadata'])
            rows['archetypes' if family=='archetype' else 'profiles'].append(row)
        elif family=='binding' and r['status']=='active':
            rows['bindings'].append(dict(unblob(r['value']), notification_profile_binding_id=r['binding_id'],status='active'))
    for key in ('archetypes','profiles'): rows[key].sort(key=lambda r:(r['key'],r['id']))
    rows['bindings'].sort(key=lambda r:(r['item_archetype_id'],r['notification_profile_binding_id']))
    return [{'catalog':k,'digest':hash_value(rows[k])} for k in ('archetypes','profiles','bindings')]


def validate_state(row, owner):
    validator('spine-pack-installer-types.v2.schema.json', 'state').validate(row)
    require(row['owner'] == owner, 'foreign owner')
    family = row['object_key'].split(':')[0]
    require(row['root_id'] is not None, 'missing root identity')
    binding = family in ('binding', 'facet_binding')
    require((row['binding_id'] is not None) == binding, 'binding identity')
    require((row['revision_id'] is None) == binding, 'revision identity')
    require((row['revision_contract'] is None) == binding, 'revision decoder')
    if family == 'profile':
        require(row['revision_contract'] in ('spine.notification-profiles.v1', 'spine.notification-profiles.v2'), 'profile decoder')
        if row['revision_contract'].endswith('.v1'):
            family = 'profile_v1'
    elif not binding:
        require(row['revision_contract']=={'archetype':'spine.item-archetypes.v1',
                    'schema':'spine.facet-schemas.v1','rendering':'spine.notification-rendering-definitions.v1'}[family], 'wrong revision contract')
    validator('spine-pack-embedded-values.v2.schema.json', family).validate(unblob(row['value']))
    if binding:
        require(row['root_id']==unblob(row['value'])['item_archetype_id'], 'binding archetype identity')


def observation(view, owner):
    validator('spine-pack-installer-types.v2.schema.json', 'observation').validate(view)
    require(view['owner'] == owner, 'observation owner')
    require(view['digest'] == observation_digest(view), 'observation digest')
    require(len(view['entries']) + len(view['historical_revisions']) <= 4096, 'aggregate entries')
    ordered([r['object_key'] for r in view['entries']])
    ordered([(r['object_key'], r['revision_id']) for r in view['historical_revisions']])
    require([x['catalog'] for x in view['public_catalog_snapshots']] == ['archetypes', 'profiles', 'bindings'], 'public snapshots')
    require(view['public_catalog_snapshots'] == public_snapshots(view['entries']), 'public fingerprint mismatch')
    for row in view['entries'] + view['historical_revisions']:
        validate_state(row, owner)
    current={r['object_key']:r for r in view['entries']}
    for row in view['historical_revisions']:
        require(row['object_key'] in current and row['root_id']==current[row['object_key']]['root_id'] and
                row['revision_id']!=current[row['object_key']]['revision_id'],'historical root/revision membership')
    roots = [r['root_id'] for r in view['entries'] if r['binding_id'] is None]
    require(len(roots) == len(set(roots)), 'duplicate root identity')


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
        return source['value'] if source['kind'] == 'observed' else '@pending/' + source['action_id'] + source['output_pointer']
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


def plan_check(manifest, request, plan):
    validate_manifest(manifest); artifact(request); artifact(plan)
    require(plan['request'] == request['request'] and plan['request_digest'] == request['content_identity']['digest'], 'request correlation')
    require(plan['pack'] == dict(manifest_schema=manifest['manifest_schema'], **manifest['pack'], manifest_digest=manifest['content_identity']['digest']), 'pack correlation')
    selection = plan['request']['selection']
    if selection['mode'] == 'archetypes':
        ordered(selection['archetype_keys'])
    require(plan['closure'] == closure(manifest, selection), 'selection closure')
    ordered(plan['environment']['advertised_contracts'])
    require(set(INVENTORY['required_execution_contracts']) <= set(plan['environment']['advertised_contracts']), 'missing execution contracts')
    require(set(manifest['compatibility']['spine_content_contracts']) <= set(plan['environment']['advertised_contracts']), 'missing content contracts')
    observation(plan['observation'], plan['request']['owner'])
    rows = {r['object_key']: r for r in plan['observation']['entries']}
    require([c['object_key'] for c in plan['classifications']] == plan['closure'], 'classification coverage')
    require([r['object_key'] for r in plan['resolutions']] == plan['closure'], 'resolution coverage')
    objects = manifest_objects(manifest)
    for c in plan['classifications']:
        require(unblob(c['desired']) == objects[c['object_key']], 'desired content')
        require(c['observed'] == rows.get(c['object_key']), 'observed preimage')
        require(c['classification'] == 'blocked' or (c['classification'] == 'missing') == (c['observed'] is None), 'missing classification')
        require((c['blocked_reason'] is not None) == (c['classification'] == 'blocked'), 'blocked classification')
        if c['observed'] and c['observed']['status'] == 'retired':
            require(c['classification'] == 'blocked', 'retired object')
    actions = {a['action_id']: a for a in plan['actions']}
    require(len(actions) == len(plan['actions']), 'duplicate actions')
    phases = []
    for i, a in enumerate(plan['actions']):
        require(a['ordinal'] == str(i) and a['action_id'] == f'action-{i:06d}', 'action ordinal')
        require(a['object_key'] in plan['closure'], 'unselected action')
        require(unblob(a['desired']) == objects[a['object_key']], 'action desired')
        require(a['expected'] == rows.get(a['object_key']), 'action preimage')
        require((a['change_kind'] == 'create') == (a['expected'] is None), 'change kind')
        phases.append((COMMANDS[a['command']]['phase'], a['object_key']))
        require(unblob(a['request_template']) == expected_template(a, plan['request']['owner']), 'request template mapping')
        require('${' not in a['request_template']['canonical_json'], 'interpolation forbidden')
        slots = allowed_slots(a, objects[a['object_key']])
        require(a['slots'] == [dict(request_pointer=p, object_key=k, field=f) for p, (k, f) in sorted(slots.items())], 'typed slots')
        resolutions = {r['object_key']: r for r in plan['resolutions']}
        for k, f in slots.values():
            source = resolutions[k][f]
            require(source is not None, 'unresolved dependency')
            if source['kind'] == 'action_result':
                require(int(actions[source['action_id']]['ordinal']) < i, 'forward/self reference')
    require(phases == sorted(set(phases)), 'action phase order or duplicate')
    for row in plan['resolutions']:
        for field in ('root', 'revision', 'binding'):
            source = row[field]
            if source is None:
                continue
            if source['kind'] == 'observed':
                key = ('archetype:' + row['object_key'].split(':')[1]
                       if field == 'root' and row['object_key'].split(':')[0] in ('binding', 'facet_binding') else row['object_key'])
                require(source['object_key'] == key and source['field'] == field, 'observed source kind')
                require(source['value'] == rows[key][field + '_id'], 'observed source identity')
            else:
                producer = actions[source['action_id']]
                key = ('archetype:' + row['object_key'].split(':')[1]
                       if field == 'root' and row['object_key'].split(':')[0] in ('binding', 'facet_binding') else row['object_key'])
                require(producer['object_key'] == key, 'wrong producer object')
                require(COMMANDS[producer['command']]['outputs'].get(field) == source['output_pointer'], 'wrong producer output')
    require(plan['decision_action_ids'] == [a['action_id'] for a in plan['actions'] if a['change_kind'] == 'update'], 'update coverage')
    require(plan['blocked_object_keys'] == [c['object_key'] for c in plan['classifications'] if c['classification'] == 'blocked'], 'blocked coverage')
    require(plan['apply_eligible'] == (manifest['pack']['status'] == 'released' and not plan['blocked_object_keys']), 'draft or blocked eligibility')
    resolutions = {r['object_key']:r for r in plan['resolutions']}
    expected_commands = []
    for c in plan['classifications']:
        key=c['object_key']; family=key.split(':')[0]; old=c['observed']; resolution=resolutions[key]
        if c['classification'] == 'blocked':
            require(all(resolution[f] is None for f in ('root','revision','binding')), 'blocked resolution')
            continue
        require(resolution['root'] is not None, 'missing root source')
        binding=family in ('binding','facet_binding')
        require((resolution['revision'] is None) == binding and (resolution['binding'] is not None) == binding, 'resolution identity shape')
        desired=desired_semantics(key,objects[key],resolutions)
        observed=unblob(old['value']) if old else None
        if family=='profile' and old and old['revision_contract']=='spine.notification-profiles.v1':
            for t in observed['revision']['templates']:t['rendering']={'kind':'ordinary'}
        classification='missing' if old is None else 'equivalent' if desired==observed else 'drifted'
        require(c['classification']==classification, 'semantic classification')
        if classification=='equivalent':continue
        cmd={'archetype':'item_archetype','schema':'facet_schema','rendering':'notification_rendering_definition','facet_binding':'item_archetype.facet_binding','binding':'notification_profile.binding','profile':'notification_profile'}[family]
        if classification=='missing':
            expected_commands.append((key,cmd+('.set' if binding else '.create')))
        elif family=='profile':
            if desired['metadata']!=observed['metadata']:expected_commands.append((key,cmd+'.metadata.update'))
            if desired['revision']!=observed['revision']:expected_commands.append((key,cmd+'.revise'))
        else:
            expected_commands.append((key,cmd+('.set' if binding else '.revise' if family=='archetype' else '.publish')))
    require(sorted(expected_commands)==sorted((a['object_key'],a['command']) for a in plan['actions']), 'complete action coverage')


def approval_check(plan, approval):
    artifact(approval)
    require(approval['plan_digest'] == plan['content_identity']['digest'], 'stale approval')
    require(approval['authorized_update_action_ids'] == plan['decision_action_ids'], 'update authorization')
    require(plan['apply_eligible'], 'ineligible apply')


def materialize(plan, approval, action, prefix):
    request = unblob(action['request_template'])
    rows = {r['object_key']: r for r in plan['resolutions']}
    for slot in action['slots']:
        source = rows[slot['object_key']][slot['field']]
        if source['kind'] == 'observed':
            value = source['value']
        else:
            evidence = next((e for e in prefix if e['action_id'] == source['action_id']), None)
            require(evidence is not None, 'consumer before accepted producer')
            value = pointer(unblob(evidence['response'], True), source['output_pointer'])
        require(pointer(request, slot['request_pointer']) is None, 'non-null slot')
        pointer(request, slot['request_pointer'], value, True)
    request.update({k: approval['execution'][k] for k in ('actor_subject_id', 'action_timestamp_utc')},
                   command_id=command_id(plan, approval, action))
    public_schema(action['command'], 'request', request)
    if action['command'].startswith('notification_rendering_definition.'):
        require(len(canonical(request['revision'])) <= 8192, 'resolved rendering byte limit')
    if action['command'].startswith('facet_schema.'):
        require(len(canonical(request['definition'])) <= 32768, 'facet byte limit')
    if action['command'] in ('notification_profile.create', 'notification_profile.revise'):
        require(len(canonical(request)) <= 32768, 'resolved profile request byte limit')
    return request


def receipt_projection(command, response):
    family = COMMANDS[command]['family']
    if family == 'catalog':
        return dict(family=family, **{k: response['receipt'][k] for k in ('command_receipt_id', 'effect', 'semantic_facts_hash', 'created_at_utc')})
    return dict(family=family, **{k: response[k] for k in ('command_receipt_id', 'effect', 'changed', 'replayed')}, audit_id=response.get('audit_id'))


def evidence_check(plan, approval, action, evidence, prefix):
    req = materialize(plan, approval, action, prefix)
    require(evidence['action_id'] == action['action_id'] and evidence['command'] == action['command'], 'evidence prefix')
    require(evidence['command_id'] == req['command_id'] and unblob(evidence['request']) == req, 'exact submitted request')
    response = unblob(evidence['response'], True)
    public_schema(action['command'], 'response', response)
    require(not response.get('dry_run'), 'dry-run evidence')
    require(evidence['receipt'] == receipt_projection(action['command'], response), 'receipt projection')
    receipt = response.get('receipt', response)
    require(receipt['command_id'] == req['command_id'], 'receipt command identity')
    if evidence['receipt']['family'] == 'catalog':
        require(receipt['semantic_facts_hash'] == hash_value(req), 'receipt request hash')
        require(receipt['created_at_utc'] == req['action_timestamp_utc'], 'receipt timestamp')
        require(receipt['effect'] == response['effect'], 'receipt effect')
    post = evidence['post_observation']; validate_state(post, plan['request']['owner'])
    require(post['object_key'] == action['object_key'], 'post object')
    for field, path in COMMANDS[action['command']]['outputs'].items():
        require(post[field + '_id'] == pointer(response, path), 'response output/readback mismatch')
    for field in ('item_archetype_id', 'notification_profile_id', 'facet_schema_id', 'notification_rendering_definition_id'):
        if field in req and field in response:
            require(req[field] == response[field], 'response target')
    for field in ('archetype_key', 'profile_key'):
        if field in req:
            require(response[field] == req[field], 'create key')
    if 'prior_revision_id' in response:
        require(response['prior_revision_id'] == req.get('expected_current_revision_id'), 'prior revision')
    if 'prior_binding_id' in response:
        require(response['prior_binding_id'] == req['expected_binding_id'], 'prior binding')
    body = unblob(post['value']); cmd = action['command']
    if cmd.startswith('item_archetype.') and cmd != 'item_archetype.facet_binding.set':
        require(body == req['revision'], 'archetype readback semantics')
    elif cmd.startswith('facet_schema.'):
        require(body == req['definition'], 'facet readback semantics')
    elif cmd.startswith('notification_rendering_definition.'):
        record = response['record']
        require(body == req['revision'] == record['revision'], 'rendering readback semantics')
        require(record['owner'] == plan['request']['owner'], 'rendering owner')
        require(record['status']=='active', 'rendering status')
        require(record['definition_key'] == action['object_key'].split(':')[1], 'rendering key')
        require(record['current_revision_id'] == post['revision_id'] and record['notification_rendering_definition_id'] == post['root_id'], 'rendering current/root')
        require(record['definition_hash'] == hash_value({'contract_version':'spine.notification-rendering-definitions.v1','canonical_json_version':'spine.canonical-json.v1','revision':req['revision']}), 'rendering hash')
        require(record['published'] == {k:req[k] for k in ('command_id','actor_subject_id','action_timestamp_utc')}, 'rendering provenance')
        if cmd.endswith('.create'):require(record['created']==record['published'],'rendering create provenance')
    elif cmd == 'item_archetype.facet_binding.set':
        require(body == {k:req[k] for k in ('item_archetype_id','facet_key','facet_schema_revision_id')}, 'facet binding semantics')
    elif cmd == 'notification_profile.binding.set':
        require(body == {k:req[k] for k in ('item_archetype_id','notification_profile_id')}, 'default binding semantics')
    elif cmd == 'notification_profile.metadata.update':
        require(body['metadata'] == req['metadata'], 'metadata semantics')
        require(body['revision'] == unblob(action['expected']['value'])['revision'], 'metadata changed revision')
    else:
        require(body['revision'] == req['revision'], 'profile readback semantics')
        desired = unblob(action['desired'])
        require(body['metadata'] == {k:desired[k] for k in ('display_name','description')}, 'profile metadata')
        templates=[]
        for template in req['revision']['templates']:
            templates.append(dict(template, normalized_template_hash=hash_value({
                'derivation_version':'spine.notification-profile-template-hash.v2',
                'canonical_json_version':'spine.canonical-json.v1','template':template})))
        require(response['normalized_revision_hash']==hash_value({
            'derivation_version':'spine.notification-profile-revision-hash.v2',
            'canonical_json_version':'spine.canonical-json.v1',
            'revision':dict(req['revision'],templates=templates)}), 'profile revision hash')
    if action['expected']:
        require(post['root_id'] == action['expected']['root_id'], 'changed root')
    if response['effect'].endswith('noop'):
        require(action['expected'] == post, 'no-op cannot explain change')


def checkpoint_check(plan, approval, checkpoint):
    artifact(checkpoint); approval_check(plan, approval)
    require(checkpoint['plan_digest'] == plan['content_identity']['digest'], 'checkpoint plan')
    require(checkpoint['approval_digest'] == approval['content_identity']['digest'] and checkpoint['execution'] == approval['execution'], 'checkpoint execution')
    prefix = checkpoint['accepted_responses']; actions = plan['actions']
    require(len(prefix) <= len(actions), 'prefix overflow')
    for i, evidence in enumerate(prefix):
        evidence_check(plan, approval, actions[i], evidence, prefix[:i])
    next_id = actions[len(prefix)]['action_id'] if len(prefix) < len(actions) else None
    require(checkpoint['next_action_id'] == next_id, 'next action')
    pending = checkpoint['unresolved_submission']
    if pending:
        require(pending['action_id'] == next_id, 'uncertain gap')
        request = materialize(plan, approval, actions[len(prefix)], prefix)
        require(pending['command_id'] == request['command_id'] and unblob(pending['request']) == request, 'changed replay bytes')


def forward(view, evidence):
    result = deepcopy(view)
    entries = {r['object_key']: r for r in result['entries']}
    history = {(r['object_key'], r['revision_id']): r for r in result['historical_revisions']}
    for e in evidence:
        post = e['post_observation']; old = entries.get(post['object_key'])
        if old and old['revision_id'] and old['revision_id'] != post['revision_id']:
            history[(old['object_key'], old['revision_id'])] = old
        entries[post['object_key']] = post
    result['entries'] = [entries[k] for k in sorted(entries)]
    result['historical_revisions'] = [history[k] for k in sorted(history)]
    # Old fingerprints are independently validated by the observer; they cannot
    # be invented from this reduced semantic view. Recovery compares the full
    # semantic/identity projection, not unknown future public hash strings.
    result.pop('public_catalog_snapshots'); result.pop('digest')
    return result


def recovery_check(plan, approval, checkpoint, fresh, provisional=None, replay=None):
    checkpoint_check(plan, approval, checkpoint)
    observation(fresh, plan['request']['owner'])
    prefix = checkpoint['accepted_responses']
    baseline = forward(plan['observation'], prefix)
    actual = forward(fresh, [])
    if actual == baseline:
        require(provisional is None, 'unexplained provisional candidate')
        return 'prefix'
    require(checkpoint['unresolved_submission'] is not None and provisional is not None, 'unexplained catalog change')
    require(provisional['object_key'] == plan['actions'][len(prefix)]['object_key'], 'uncertain suffix')
    validate_state(provisional, plan['request']['owner'])
    candidate = forward(plan['observation'], prefix + [{'post_observation': provisional}])
    require(actual == candidate, 'unrelated catalog change')
    require(replay is not None, 'candidate is not acceptance evidence')
    evidence_check(plan, approval, plan['actions'][len(prefix)], replay, prefix)
    require(replay['post_observation'] == provisional, 'replay candidate identity mismatch')
    return 'prefix_plus_one'


def result_check(plan, approval, result):
    artifact(result); checkpoint_check(plan, approval, result['checkpoint'])
    cp = result['checkpoint']; n = len(cp['accepted_responses']); actions = plan['actions']
    if result['state'] == 'applied':
        require(n == len(actions) and not cp['unresolved_submission'] and result['failure'] is None and result['unattempted_action_ids'] == [], 'applied coverage')
    elif result['state'] == 'partial':
        require(n < len(actions) and result['failure']['action_id'] == actions[n]['action_id'], 'partial failure')
        require(result['unattempted_action_ids'] == [a['action_id'] for a in actions[n+1:]], 'partial suffix')
    else:
        require(n == 0 and cp['unresolved_submission'] is None and result['failure'] is not None, 'not-applied evidence')
        require(result['unattempted_action_ids'] == [a['action_id'] for a in actions], 'not-applied suffix')


def verification_check(plan, approval, result, verification):
    artifact(verification)
    require(verification['plan_digest'] == plan['content_identity']['digest'], 'verification plan')
    for field in ('pack', 'environment', 'closure'):
        require(verification[field] == plan[field], 'verification ' + field)
    require(verification['target'] == plan['request']['target'], 'verification target')
    observation(verification['observation'], plan['request']['owner'])
    require([r['object_key'] for r in verification['object_results']] == plan['closure'], 'verification coverage')
    fresh = {r['object_key']: r for r in verification['observation']['entries']}
    expected = {r['object_key']: r for r in plan['observation']['entries']}
    if result is not None:
        result_check(plan, approval, result)
        expected.update({e['post_observation']['object_key']: e['post_observation'] for e in result['checkpoint']['accepted_responses']})
    complete = bool(result and result['state'] == 'applied')
    coverage = ('complete' if complete else 'missing') if plan['actions'] else 'not_required'
    require(verification['response_evidence'] == coverage, 'verification evidence coverage')
    require(verification['apply_result_digest'] == (result['content_identity']['digest'] if result and plan['actions'] else None), 'verification result correlation')
    for r in verification['object_results']:
        require(r['observed'] == fresh.get(r['object_key']), 'verification observation')
        if r['state'] == 'equivalent':
            actual=deepcopy(r['observed']); desired=deepcopy(expected.get(r['object_key']))
            if actual and desired and (r['object_key'].startswith('archetype:') or
                    r['object_key'].startswith('profile:') and actual['revision_contract']==desired['revision_contract']=='spine.notification-profiles.v1'):
                actual['revision_id']=desired['revision_id']
            require(actual is not None and actual == desired and actual['status'] == 'active', 'exact current pin/identity')
    success = coverage in ('complete','not_required') and all(r['state'] == 'equivalent' for r in verification['object_results'])
    require((verification['state'] == 'verified') == success, 'verification outcome')
