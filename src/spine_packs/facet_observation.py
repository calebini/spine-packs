"""Bounded, two-pass public catalog observation for FR-2. No writes or SQL."""
from copy import deepcopy
import re
import unicodedata

from . import artifacts as a
from .facet_contracts import blob, body, validate
from .facet_inventory import COMMANDS, CONTRACTS
from .facet_transport import ObservationBudget
from .planning import require, ENVIRONMENT, INCOMPATIBLE, owner_matches, validate_entry

FAMILIES = {
    'archetype': ('item_archetype', 'archetype_key', 'item_archetype_id', 'entries'),
    'profile': ('notification_profile', 'profile_key', 'notification_profile_id', 'entries'),
    'schema': ('facet_schema', 'schema_key', 'facet_schema_id', 'schemas'),
    'rendering': ('notification_rendering_definition', 'definition_key', 'notification_rendering_definition_id', 'records'),
}


def canonical_order(values):
    require(values == sorted(set(values)), 'noncanonical_public_order')


def canonical_key(value):
    require(re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', value) is not None, 'noncanonical_catalog_key')


def schema_semantics(definition):
    validate(definition, 'spine-readback-0.10.0.schema.json', 'semantic_schema', category=ENVIRONMENT)
    require(len(a.canonical_text(definition).encode()) <= 32768, 'facet_definition_capacity')
    def inspect(v):
        if isinstance(v, str):
            require(v == unicodedata.normalize('NFC', v), 'noncanonical_facet_text')
        elif isinstance(v, dict):
            for x in v.values(): inspect(x)
        elif isinstance(v, list):
            for x in v: inspect(x)
    inspect(definition)
    canonical_order(definition['compatible_item_types'])
    canonical_order([f['key'] for f in definition['fields']])
    for f in definition['fields']:
        canonical_key(f['key'])
        if f['type'] == 'enum': canonical_order(f['choices'])
        if f['type'] == 'integer':
            require(-(2**63) <= int(f['min']) <= int(f['max']) < 2**63, 'invalid_facet_range')


def rendering_semantics(revision):
    validate(revision, 'spine-readback-0.10.0.schema.json', 'semantic_rendering', category=ENVIRONMENT)
    require(len(a.canonical_text(revision).encode()) <= 8192, 'rendering_capacity')
    canonical_order(revision['compatible_item_types'])
    for text in [revision['display_name'], revision['description'], *[s['label'] for s in revision['selections']]]:
        if text is not None:
            require(bool(text) and text == ' '.join(text.split())
                    and not any(unicodedata.category(c).startswith('C') for c in text), 'noncanonical_rendering_text')
    require(len({s['selection_key'] for s in revision['selections']}) == len(revision['selections'])
            and len({(s['facet_key'], s['facet_schema_revision_id'], s['field_key']) for s in revision['selections']})
            == len(revision['selections']), 'duplicate_rendering_selection')
    for selection in revision['selections']:
        for field in ('selection_key', 'facet_key', 'field_key'): canonical_key(selection[field])


def profile_content(revision):
    content = deepcopy(revision['content'])
    canonical_order(content['compatible_item_types'])
    canonical_order([t['template_key'] for t in content['templates']])
    v2 = revision['revision_contract'] == 'spine.notification-profiles.v2'
    for t in content['templates']:
        canonical_key(t['template_key'])
        original_hash = t.pop('normalized_template_hash')
        preimage = dict(derivation_version='spine.notification-profile-template-hash.v2',
                        canonical_json_version='spine.canonical-json.v1', template=t) if v2 else t
        require(original_hash == a.digest(preimage), 'profile_template_hash_mismatch')
    stored = revision['content']
    preimage = (dict(derivation_version='spine.notification-profile-revision-hash.v2',
                     canonical_json_version='spine.canonical-json.v1', revision=stored) if v2 else
                dict(contract_version='spine.notification-profiles.v1', **stored))
    require(revision['normalized_revision_hash'] == a.digest(preimage), 'profile_revision_hash_mismatch')
    return content


def state(family, value, owner, *, historical=False):
    """Project only after wire shape, owner, identity, normalization and hashes."""
    prefix, key_field, id_field, _ = FAMILIES[family]
    row = value['root'] if family == 'schema' else value
    canonical_key(row[key_field])
    if family == 'archetype':
        require(owner_matches(row, owner), 'catalog_owner_mismatch')
        if not historical: validate_entry(row, owner, family)
    else:
        require(row['owner'] == owner, 'catalog_owner_mismatch')
    revision = value['revision']
    number = row['revision_number'] if family == 'rendering' else revision['revision_number']
    require(str(int(number)) == str(number) and int(number) > 0, 'invalid_revision_number')
    if family == 'schema':
        rev_id = revision['facet_schema_revision_id']
        require(revision['facet_schema_id'] == row[id_field], 'revision_root_mismatch')
        semantic = revision['definition']; schema_semantics(semantic)
        require(revision['definition_hash'] == a.digest(dict(derivation_version='spine.facet-definition.v1', definition=semantic)),
                'facet_definition_hash_mismatch')
        decoder = 'spine.facet-schemas.v1'
    elif family == 'rendering':
        rev_id = row['notification_rendering_definition_revision_id']
        semantic = revision; rendering_semantics(semantic)
        decoder = 'spine.notification-rendering-definitions.v1'
        require(row['definition_hash'] == a.digest(dict(contract_version=decoder,
                canonical_json_version='spine.canonical-json.v1', revision=semantic)), 'rendering_hash_mismatch')
        require((row['retired'] is not None) == (row['status'] == 'retired'), 'retirement_mismatch')
    elif family == 'profile':
        rev_id = revision['notification_profile_revision_id']; decoder = revision['revision_contract']
        semantic = dict(metadata={k: row[k] for k in ('display_name', 'description')}, revision=profile_content(revision))
    else:
        rev_id = revision['item_archetype_revision_id']; decoder = 'spine.item-archetypes.v1'
        require(revision['item_archetype_id'] == row[id_field], 'revision_root_mismatch')
        semantic = {k: revision[k] for k in ('display_name', 'description', 'compatible_item_types')}
        require(revision['normalized_content_hash'] == a.digest(semantic), 'archetype_hash_mismatch')
    require(historical or rev_id == row['current_revision_id'], 'current_revision_mismatch')
    result = dict(object_key=family + ':' + row[key_field], owner=deepcopy(owner), status=row['status'],
        root_id=row[id_field], revision_id=rev_id, binding_id=None, revision_contract=decoder, value=blob(semantic))
    validate(result, 'spine-pack-installer-types.v2.schema.json', 'state', category=ENVIRONMENT)
    return result


def snapshots(entries):
    rows = {'archetypes': [], 'profiles': [], 'bindings': []}
    for row in entries:
        family, key = row['object_key'].split(':', 1)
        if family in ('archetype', 'profile'):
            value = dict(id=row['root_id'], key=key, status=row['status'], current_revision_id=row['revision_id'])
            if family == 'profile': value.update(body(row['value'])['metadata'])
            rows['archetypes' if family == 'archetype' else 'profiles'].append(value)
        elif family == 'binding':
            rows['bindings'].append(dict(body(row['value']), notification_profile_binding_id=row['binding_id'], status='active'))
    for family, values in rows.items():
        values.sort(key=(lambda r: (r['item_archetype_id'], r['notification_profile_binding_id']))
                    if family == 'bindings' else (lambda r: (r['key'], r['id'])))
    return [{'catalog': k, 'digest': a.digest(v)} for k, v in rows.items()]


class Observer:
    def __init__(self, transport, owner, selection, page_size=100):
        require(type(page_size) is int and 1 <= page_size <= 100, 'invalid_page_size')
        self.transport, self.owner, self.selection, self.limit = transport, owner, set(selection), page_size
        self.entries, self.history, self.raw, self.exact = {}, {}, {}, {}
        self.fingerprints = {}

    def read(self, command, **fields):
        request = dict(contract_version=COMMANDS[command]['selector'], **fields)
        result = self.transport.read(command, request)
        validate(result, 'spine-readback-0.10.0.schema.json', COMMANDS[command]['response'], category=ENVIRONMENT)
        require(not result.get('dry_run'), 'dry_run_readback')
        return result

    def add(self, row, historical=False):
        key = (row['object_key'], row['revision_id']) if historical else row['object_key']
        target = self.history if historical else self.entries
        require(key not in target or target[key] == row, 'conflicting_observation')
        target[key] = row
        require(len(self.entries) + len(self.history) <= 4096, 'observation_entry_capacity')

    def pages(self, command, collection, order, **scope):
        query = dict(scope, limit=str(self.limit)); seen, ids, result = set(), set(), []
        previous = None; fingerprint = None
        while True:
            page = self.read(command, **query)
            values = page[collection]
            require(len(values) <= self.limit, 'invalid_page_count')
            if 'limit' in page: require(page['limit'] == str(self.limit), 'page_limit_mismatch')
            if 'owner' in page: require(page['owner'] == self.owner, 'page_owner_mismatch')
            if 'item_archetype_id' in page:
                require(page['item_archetype_id'] == scope['item_archetype_id'], 'page_archetype_mismatch')
            if 'count' in page: require(page['count'] == str(len(values)), 'invalid_page_count')
            if 'catalog_snapshot_hash' in page:
                require(fingerprint is None or fingerprint == page['catalog_snapshot_hash'], 'catalog_changed')
                fingerprint = page['catalog_snapshot_hash']
            for value in values:
                key = order(value)
                require(key not in ids and (previous is None or previous < key), 'duplicate_or_unordered_page')
                if 'status' in scope: require(value['status'] == scope['status'], 'wrong_status_page')
                ids.add(key); previous = key; result.append(value)
                require(len(result) <= 4096, 'observation_entry_capacity')
            cursor = page['next_cursor']
            require(page['has_more'] == (cursor is not None), 'cursor_presence_mismatch')
            if not page['has_more']: break
            require(bool(values) and cursor not in seen, 'cursor_cycle_or_empty_page')
            seen.add(cursor); query['cursor'] = cursor
        return result, fingerprint

    def schema_revision(self, identity):
        if identity in self.exact: return self.exact[identity]
        result = self.read('facet_schema.revision.show', facet_schema_revision_id=identity)
        require(result['revision']['facet_schema_revision_id'] == identity, 'requested_revision_mismatch')
        row = state('schema', result, self.owner, historical=True)
        current = self.entries.get(row['object_key'])
        require(current is not None and current['root_id'] == row['root_id'], 'revision_root_not_in_catalog')
        require(result['root'] == self.raw[row['object_key']]['root'], 'revision_root_changed')
        if identity != current['revision_id']: self.add(row, True)
        else:
            require(row == current and result['revision'] == self.raw[row['object_key']]['revision'], 'current_revision_changed')
        self.exact[identity] = row
        return row

    def rendering_revision(self, root_id, revision_id):
        cache = (root_id, revision_id)
        if cache in self.exact: return self.exact[cache]
        rows = [r for r in self.entries.values() if r['object_key'].startswith('rendering:') and r['root_id'] == root_id]
        require(len(rows) == 1, 'rendering_root_not_in_catalog')
        current = rows[0]
        record = self.read('notification_rendering_definition.show', notification_rendering_definition_id=root_id,
            notification_rendering_definition_revision_id=revision_id)['record']
        row = state('rendering', record, self.owner, historical=True)
        require(row['root_id'] == root_id and row['revision_id'] == revision_id
                and row['object_key'] == current['object_key'], 'rendering_pin_mismatch')
        original = self.raw[current['object_key']]
        require(all(record[k] == original[k] for k in ('current_revision_id', 'created', 'retired', 'status', 'owner', 'definition_key')),
                'rendering_root_changed')
        if revision_id != current['revision_id']: self.add(row, True)
        else: require(row == current, 'current_revision_changed')
        self.inspect_rendering(row)
        self.exact[cache] = row
        return row

    def inspect_rendering(self, row):
        revision = body(row['value'])
        for selection in revision['selections']:
            schema = self.schema_revision(selection['facet_schema_revision_id'])
            definition = body(schema['value'])
            fields = {f['key']: f for f in definition['fields']}
            require(selection['field_key'] in fields and set(revision['compatible_item_types']) <= set(definition['compatible_item_types']),
                    'rendering_schema_mismatch')
            field = fields[selection['field_key']]
            require((selection['projection'] == 'location_label' and field['type'] == 'reference' and field['target_kind'] == 'location')
                    or (selection['projection'] == 'value' and field['type'] != 'reference'), 'rendering_projection_mismatch')

    def collect(self):
        for family, (prefix, key_field, id_field, collection) in FAMILIES.items():
            all_rows = []
            # Legacy unfiltered lists supply the exact full public fingerprint.
            for status_filter in (('active', 'retired') if family in ('schema', 'rendering') else (None,)):
                scope = dict(owner=self.owner)
                if status_filter: scope['status'] = status_filter
                ordering = (lambda r: r[id_field]) if family in ('schema', 'rendering') else (lambda r: (r[key_field], r[id_field]))
                rows, fingerprint = self.pages(prefix + '.list', collection, ordering, **scope)
                if fingerprint: self.fingerprints['archetypes' if family == 'archetype' else 'profiles'] = fingerprint
                all_rows.extend(rows)
            require(len({r[key_field] for r in all_rows}) == len(all_rows)
                    and len({r[id_field] for r in all_rows}) == len(all_rows), 'duplicate_catalog_root')
            if family == 'schema': require(len(all_rows) <= 100, 'facet_catalog_capacity')
            for listed in all_rows:
                shown = self.read(prefix + '.show', **{id_field: listed[id_field]})
                value = shown if family == 'schema' else shown['record' if family == 'rendering' else prefix]
                require((value['root'] if family == 'schema' else value) == listed, 'list_show_mismatch')
                row = state(family, value, self.owner)
                self.add(row); self.raw[row['object_key']] = value
        roots = [r['root_id'] for r in self.entries.values()]
        require(len(set(roots)) == len(roots), 'duplicate_root_identity')
        archetypes = {r['root_id']: r for r in self.entries.values() if r['object_key'].startswith('archetype:')}
        profiles = {r['root_id']: r for r in self.entries.values() if r['object_key'].startswith('profile:')}
        for identity, archetype in archetypes.items():
            bindings, _ = self.pages('item_archetype.facet_binding.list', 'bindings', lambda r: r['facet_key'], item_archetype_id=identity)
            require(len(bindings) <= 100, 'facet_binding_capacity')
            for b in bindings:
                canonical_key(b['facet_key'])
                require(b['item_archetype_id'] == identity and b['status'] == 'active', 'facet_binding_mismatch')
                key = 'facet_binding:' + archetype['object_key'].split(':', 1)[1] + ':' + b['facet_key']
                self.add(dict(object_key=key, owner=self.owner, status='active', root_id=identity, revision_id=None,
                    binding_id=b['facet_binding_id'], revision_contract=None,
                    value=blob({k: b[k] for k in ('item_archetype_id', 'facet_key', 'facet_schema_revision_id')})))
        bindings, fingerprint = self.pages('notification_profile.binding.list', 'entries',
            lambda r: (r['item_archetype_id'], r['notification_profile_binding_id']), owner=self.owner, status='active')
        self.fingerprints['bindings'] = fingerprint
        require(len({b['item_archetype_id'] for b in bindings}) == len(bindings), 'duplicate_default_binding')
        for b in bindings:
            validate_entry(b, self.owner, 'binding')
            require(b['item_archetype_id'] in archetypes and b['notification_profile_id'] in profiles, 'foreign_binding_root')
            key = 'binding:' + archetypes[b['item_archetype_id']]['object_key'].split(':', 1)[1]
            self.add(dict(object_key=key, owner=self.owner, status='active', root_id=b['item_archetype_id'], revision_id=None,
                binding_id=b['notification_profile_binding_id'], revision_contract=None,
                value=blob({k: b[k] for k in ('item_archetype_id', 'notification_profile_id')})))
        binding_ids = [r['binding_id'] for r in self.entries.values() if r['binding_id'] is not None]
        require(len(binding_ids) == len(set(binding_ids)), 'duplicate_binding_identity')
        for key in sorted(self.selection):
            row = self.entries.get(key)
            if row is None: continue
            if key.startswith('facet_binding:'):
                self.schema_revision(body(row['value'])['facet_schema_revision_id'])
            elif key.startswith('rendering:'): self.inspect_rendering(row)
            elif key.startswith('profile:') and row['revision_contract'].endswith('.v2'):
                for template in body(row['value'])['revision']['templates']:
                    rendering = template['rendering']
                    if rendering['kind'] == 'definition':
                        ref = rendering['definition']
                        definition = self.rendering_revision(ref['notification_rendering_definition_id'], ref['notification_rendering_definition_revision_id'])
                        require(set(body(row['value'])['revision']['compatible_item_types'])
                                <= set(body(definition['value'])['compatible_item_types']), 'profile_rendering_type_mismatch')
        entries = [self.entries[k] for k in sorted(self.entries)]
        public = snapshots(entries)
        require(all(self.fingerprints[r['catalog']] == r['digest'] for r in public), 'public_fingerprint_mismatch')
        view = dict(owner=self.owner, entries=entries, historical_revisions=[self.history[k] for k in sorted(self.history)],
                    public_catalog_snapshots=public)
        view['digest'] = a.digest(dict(derivation_version='spine.pack-observation.v2', view=view))
        validate(view, 'spine-pack-installer-types.v2.schema.json', 'observation', category=ENVIRONMENT)
        return view


def observe(transport, owner, selection, *, page_size=100, content_contracts=()):
    budget = ObservationBudget()
    transport.begin_observation(budget)
    transport.check_target()
    def environment():
        info = transport.read('system.info', {})
        require(info.get('runtime_version') == '0.10.0', 'incompatible_runtime', INCOMPATIBLE)
        validate(info, 'spine-readback-0.10.0.schema.json', COMMANDS['system.info']['response'], category=ENVIRONMENT)
        canonical_order(info['implemented_contract_versions'])
        require(info['ledger_schema_version'] == info['implemented_ledger_schema_version'] == '19'
                and set(CONTRACTS) | set(content_contracts) <= set(info['implemented_contract_versions']), 'incompatible_contracts_or_schema', INCOMPATIBLE)
        return dict(runtime_version='0.10.0', ledger_schema_current='19', ledger_schema_implemented='19',
                    ledger_instance_id=info['ledger_instance_id'], advertised_contracts=info['implemented_contract_versions'])
    env = environment()
    first = Observer(transport, owner, selection, page_size).collect()
    second = Observer(transport, owner, selection, page_size).collect()
    require(first == second and env == environment(), 'catalog_changed_between_passes')
    require(budget.clock() < budget.deadline, 'observation_capacity')
    transport.check_target()
    return env, first
