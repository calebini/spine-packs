"""FR-2 offline validation of the pinned schema vocabulary (not a general validator).

Kept separate from the frozen v1 decoder. Unknown vocabulary fails closed.
Independent Draft 2020-12 cross-checks live in tests/contract/.
"""
from copy import deepcopy
import json
import re

from . import artifacts as a
from .planning import require, INVALID, PACK_INVALID

KEYWORDS = frozenset(('$schema', '$id', '$comment', '$defs', '$ref', 'title', 'description',
    'default', 'format', 'type', 'const', 'enum', 'properties', 'required', 'additionalProperties',
    'unevaluatedProperties', 'items', 'minItems', 'maxItems', 'uniqueItems', 'minLength', 'maxLength',
    'pattern', 'minimum', 'maximum', 'oneOf', 'anyOf', 'allOf', 'not', 'if', 'then', 'else',
    'contains', 'minContains', 'maxContains'))


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def check(value, schema, path, root):
    """Return validity and evaluated object keys, including successful applicators."""
    if isinstance(schema, bool):
        return schema, set()
    if not set(schema) <= KEYWORDS:
        raise ValueError('unsupported pinned schema vocabulary')
    valid, evaluated = True, set()
    def merge(result):
        nonlocal valid
        ok, keys = result
        valid = valid and ok
        if ok:
            evaluated.update(keys)
    if '$ref' in schema:
        reference = schema['$ref']
        f, _, fragment = reference.partition('#')
        if f:
            if '/' in f or ':' in f or not f.endswith('.schema.json'):
                raise ValueError('nonlocal schema reference')
            target = path.parent / f
            document = a._schema_document(target)
        else:
            target, document = path, root
        part = document
        for token in fragment.lstrip('/').split('/') if fragment else []:
            part = part[token.replace('~1', '/').replace('~0', '~')]
        merge(check(value, part, target, document))
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(a._is_type(value, t) for t in types):
            return False, set()
    if 'const' in schema:
        valid &= encoded(value) == encoded(schema['const'])
    if 'enum' in schema:
        valid &= encoded(value) in [encoded(x) for x in schema['enum']]
    for branch in schema.get('allOf', []):
        merge(check(value, branch, path, root))
    for mode in ('oneOf', 'anyOf'):
        if mode in schema:
            matches = [r for branch in schema[mode] if (r := check(value, branch, path, root))[0]]
            valid &= len(matches) == 1 if mode == 'oneOf' else bool(matches)
            for _, keys in matches:
                evaluated.update(keys)
    if 'not' in schema:
        valid &= not check(value, schema['not'], path, root)[0]
    if 'if' in schema:
        condition = check(value, schema['if'], path, root)
        if condition[0]:
            evaluated.update(condition[1])
        merge(check(value, schema.get('then' if condition[0] else 'else', {}), path, root))
    if isinstance(value, str):
        valid &= schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value))
        if 'pattern' in schema:
            valid &= re.search(schema['pattern'], value) is not None
    if type(value) is int:
        valid &= schema.get('minimum', value) <= value <= schema.get('maximum', value)
    if isinstance(value, list):
        valid &= schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value))
        if schema.get('uniqueItems'):
            valid &= len({encoded(x) for x in value}) == len(value)
        if 'items' in schema:
            valid &= all(check(x, schema['items'], path, root)[0] for x in value)
        if 'contains' in schema:
            n = sum(check(x, schema['contains'], path, root)[0] for x in value)
            valid &= schema.get('minContains', 1) <= n <= schema.get('maxContains', len(value))
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        valid &= set(schema.get('required', [])) <= value.keys()
        for key in value.keys() & properties.keys():
            valid &= check(value[key], properties[key], path, root)[0]
            evaluated.add(key)
        extras = value.keys() - properties.keys()
        if 'additionalProperties' in schema:
            valid &= all(check(value[k], schema['additionalProperties'], path, root)[0] for k in extras)
            evaluated.update(extras)
        if 'unevaluatedProperties' in schema:
            valid &= all(check(value[k], schema['unevaluatedProperties'], path, root)[0]
                         for k in value.keys() - evaluated)
    return bool(valid), evaluated


def validate(value, filename, definition=None, *, category=INVALID):
    path = a.SCHEMA_ROOT / filename
    root = a._schema_document(path)
    schema = root if definition is None else root['$defs'][definition]
    require(check(value, schema, path, root)[0], 'invalid_v2_contract', category)


def blob(value):
    return {'canonical_json': a.canonical_text(value), 'digest': a.digest(value)}


def body(value):
    decoded = a.parse_json(value['canonical_json'].encode())
    require(blob(decoded) == value, 'invalid_embedded_value')
    return decoded


def seal(value):
    result = deepcopy(value)
    kind = value['artifact_schema'].removeprefix('spine.pack-').removesuffix('.v2')
    result['content_identity'] = dict(algorithm='sha256', canonical_json_version='spine.canonical-json.v1',
        derivation_version='spine.pack-' + kind + '-digest.v2')
    result['content_identity']['digest'] = a.digest(result)
    return result


def artifact(value, kind):
    require(value.get('artifact_schema') == 'spine.pack-' + kind + '.v2', 'mixed_artifact_version', INVALID)
    validate(value, 'spine-pack-' + kind + '.v2.schema.json')
    limit = a.SIZE_LIMITS['spine.pack-' + kind + '.v1']
    require(len(a.canonical_text(value).encode()) <= limit, 'artifact_too_large', INVALID)
    require(value == seal(value), 'artifact_digest_mismatch', INVALID)


def ordered(values):
    require(values == sorted(set(values)), 'noncanonical_order', PACK_INVALID)
