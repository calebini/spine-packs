"""Emit an apply_patch for one FR-2 pinned artifact; never modify a checkout.

Usage: python scripts/build_fr2_contracts.py EXACT_EXPORT schema|inventory|wire|map
The caller must establish export provenance before invoking this offline tool.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PIN = '8f3c50b6fd1b4aa534e50925b7417a7a80d19122'


def generate(upstream):
    old = json.loads((ROOT / 'contracts/installer-spine-0.9.1-inventory.json').read_text())
    inv = json.loads(json.dumps(old))
    inv.update(spine_commit=PIN, runtime_version='0.10.0')
    # Assert unchanged upstream dependencies, rather than trusting the new version.
    for path, expected in old['source_sha256'].items():
        path = path.removeprefix('upstream/')
        if path.startswith('contracts/'):
            assert hashlib.sha256((upstream / path).read_bytes()).hexdigest() == expected, path
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
              '$id': 'https://spine-packs.local/contracts/schemas/spine-readback-0.10.0.schema.json',
              '$comment': 'Exact Spine ' + PIN + '. Unchanged public closure reuses the immutable 0.9.1 sibling; no network resolution.',
              '$defs': {name: {'$ref': 'spine-readback-0.9.1.schema.json#/$defs/' + name}
                        for name in json.loads((ROOT / 'contracts/schemas/spine-readback-0.9.1.schema.json').read_text())['$defs']}}
    def reference(file, pointer=''):
        key = 'upstream/' + file + '#' + pointer
        if key in inv['source_pointers']:
            return {'$ref': '#/$defs/' + inv['source_pointers'][key]}
        name = 'revision_readback_' + str(len(inv['source_pointers']))
        inv['source_pointers'][key] = name
        raw = (upstream / file).read_bytes()
        inv['source_sha256']['upstream/' + file] = hashlib.sha256(raw).hexdigest()
        obj = json.loads(raw)
        for part in pointer.lstrip('/').split('/') if pointer else []:
            obj = obj[part.replace('~1', '/').replace('~0', '~')]
        def rewrite(value):
            if isinstance(value, list):
                return [rewrite(x) for x in value]
            if not isinstance(value, dict):
                return value
            result = {}
            for k, v in value.items():
                if k in ('$id', '$schema'):
                    continue
                if k == '$ref':
                    f, _, p = v.partition('#')
                    result.update(reference(str(Path(file).parent / f) if f else file, p))
                else:
                    result[k] = rewrite(v)
            return result
        schema['$defs'][name] = rewrite(obj)
        return {'$ref': '#/$defs/' + name}
    shapes = {kind: reference('contracts/schemas/facet-schema-revision-show-' + kind + '.schema.json')['$ref'].split('/')[-1]
              for kind in ('request', 'response', 'failure')}
    inv['commands']['facet_schema.revision.show'] = dict(shapes, family='facet_revision',
        selector='spine.facet-schema-revision-readback.v1', phase=None, outputs={})
    inv['required_execution_contracts'] = sorted(old['required_execution_contracts'] + ['spine.facet-schema-revision-readback.v1'])
    # Copy only public fixtures; no live ledger facts or upstream Python imports.
    index = json.loads((upstream / 'contracts/facet-schema-revision-readback-fixture-manifest.json').read_text())
    vectors = []
    for row in index['fixtures']:
        raw = (upstream / row['fixture']).read_bytes()
        vectors.append(dict(row, value=json.loads(raw), sha256=hashlib.sha256(raw).hexdigest()))
    authority_paths = ['contracts/facet-schema-revision-readback.v1.json',
        'contracts/facet-schema-revision-readback-fixture-manifest.json',
        'specs/facet-schema-revision-readback.md', 'src/spine/commands/registry.py']
    package = 'src/spine/contracts/revision_readback/'
    pins = json.loads((upstream / package / 'pins.v1.json').read_text())
    for file, digest in pins['files'].items():
        assert hashlib.sha256((upstream / package / file).read_bytes()).hexdigest() == digest
        authority_paths.append(package + file)
    authority_paths.append(package + 'pins.v1.json')
    inv['revision_readback_authority_sha256'] = {file: hashlib.sha256((upstream / file).read_bytes()).hexdigest()
                                               for file in sorted(authority_paths)}
    registry = json.loads((upstream / authority_paths[0]).read_text())
    inv['revision_readback_prerequisites'] = registry['commands']['facet_schema.revision.show']['required_contract_versions']
    inv['revision_readback_limits'] = registry['limits']
    return inv, schema, {'spine_commit': PIN, 'vectors': vectors}


if __name__ == '__main__':
    inv, schema, wire = generate(Path(sys.argv[1]))
    outputs = {
        'schema': ('contracts/schemas/spine-readback-0.10.0.schema.json', json.dumps(schema, indent=2)),
        'inventory': ('contracts/installer-spine-0.10.0-inventory.json', json.dumps(inv, indent=2)),
        'wire': ('tests/fixtures/installer-v2/revision-readback-0.10.0.json', json.dumps(wire, indent=2)),
        'map': ('src/spine_packs/facet_inventory.py',
                '"""Pinned FR-2 public map; generated from the exact inventory, not Spine code."""\n'
                + 'BASELINE = ' + repr(dict(commit=PIN, runtime='0.10.0', schema='19')) + '\n'
                + 'COMMANDS = ' + repr(inv['commands']) + '\n'
                + 'CONTRACTS = ' + repr(inv['required_execution_contracts']) + '\n'
                + 'READ_COMMANDS = frozenset(k for k, v in COMMANDS.items() if v["phase"] is None)\n')}
    path, content = outputs[sys.argv[2]]
    print('*** Begin Patch\n*** Add File: ' + path)
    print('\n'.join('+' + line for line in content.splitlines()))
    print('*** End Patch')
