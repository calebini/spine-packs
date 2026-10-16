"""Independent official-schema and FR-1-oracle checks of FR-2 runtime evidence."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
import facet_artifact_oracle as oracle
from spine_packs import artifacts as a
from spine_packs.facet_contracts import check, KEYWORDS
from spine_packs.facet_inventory import COMMANDS, CONTRACTS, BASELINE, READ_COMMANDS
from spine_packs.facet_planning import build_plan
from spine_packs.facet_manifest import digest as manifest_digest, validate as validate_manifest
from spine_packs.planning import PlanError, PACK_INVALID


def registry():
    return oracle.Registry().with_resources((schema['$id'], oracle.Resource.from_contents(schema))
        for schema in (oracle.load(path) for path in a.SCHEMA_ROOT.glob('*.schema.json')))


@unittest.skipIf(oracle.Draft202012Validator is None, 'official Draft 2020-12 development gate required')
class FR2ContractTests(unittest.TestCase):
    def test_inventory_exact_union_and_map(self):
        inventory = oracle.load(ROOT / 'contracts/installer-spine-0.10.0-inventory.json')
        self.assertEqual(COMMANDS, inventory['commands'])
        self.assertEqual(CONTRACTS, inventory['required_execution_contracts'])
        self.assertEqual(BASELINE['commit'], inventory['spine_commit'])
        self.assertEqual(len(COMMANDS), 23); self.assertEqual(len(READ_COMMANDS), 12)
        self.assertEqual(len(CONTRACTS), 18)
        old = oracle.load(ROOT / 'contracts/installer-spine-0.9.1-inventory.json')
        self.assertEqual({k: v for k, v in COMMANDS.items() if k != 'facet_schema.revision.show'}, old['commands'])
        self.assertEqual(set(CONTRACTS) - set(old['required_execution_contracts']), {'spine.facet-schema-revision-readback.v1'})

    def test_official_meta_closure_and_supported_runtime_vocabulary(self):
        schema_keys = {'properties', '$defs'}
        def walk(value):
            if isinstance(value, bool): return
            self.assertLessEqual(set(value), KEYWORDS)
            for k, v in value.items():
                if k in schema_keys:
                    for item in v.values(): walk(item)
                elif k in ('items', 'additionalProperties', 'unevaluatedProperties', 'not', 'if', 'then', 'else', 'contains'): walk(v)
                elif k in ('allOf', 'anyOf', 'oneOf'):
                    for item in v: walk(item)
                elif k == '$ref':
                    file, _, pointer = v.partition('#')
                    self.assertNotIn('://', file)
                    self.assertTrue(not file or (a.SCHEMA_ROOT / file).is_file())
        for name in ('spine-readback-0.10.0.schema.json', 'spine-readback-0.9.1.schema.json',
                     'spine-pack-manifest.v2.schema.json', 'spine-pack-installer-types.v2.schema.json'):
            schema = oracle.load(a.SCHEMA_ROOT / name)
            oracle.Draft202012Validator.check_schema(schema); walk(schema)

    def test_upstream_vectors_official_and_runtime_agree(self):
        path = a.SCHEMA_ROOT / 'spine-readback-0.10.0.schema.json'; root = oracle.load(path)
        for vector in oracle.load(ROOT / 'tests/fixtures/installer-v2/revision-readback-0.10.0.json')['vectors']:
            kind = Path(vector['schema']).name.removeprefix('facet-schema-revision-show-').removesuffix('.schema.json')
            schema = root['$defs'][COMMANDS['facet_schema.revision.show'][kind]]
            official = oracle.Draft202012Validator(dict(schema, **{'$id': root['$id'], '$defs': root['$defs']}), registry=registry())
            with self.subTest(vector=vector['fixture_id']):
                self.assertEqual(official.is_valid(vector['value']), vector['valid'])
                self.assertEqual(check(vector['value'], schema, path, root)[0], vector['valid'])

    def test_rendering_utf8_byte_bound_supplements_official_character_limits(self):
        manifest = oracle.load(ROOT / 'tests/fixtures/installer-v2/fr2-cross-root.json')['manifest']
        revision = manifest['rendering_definitions'][0]['revision']
        revision.update(display_name='\U0001f680' * 160, description='\U0001f680' * 2000)
        manifest['content_identity']['digest'] = manifest_digest(manifest)
        oracle.validator('spine-pack-manifest.v2.schema.json').validate(manifest)
        # Even the text alone exceeds the byte ceiling; valid character counts
        # are not evidence that a request fits after reference resolution.
        self.assertGreater(len((revision['display_name'] + revision['description']).encode('utf-8')), 8192)
        with self.assertRaises(PlanError) as caught: validate_manifest(manifest)
        self.assertEqual(caught.exception.category, PACK_INVALID)
        public = oracle.load(a.SCHEMA_ROOT / 'spine-readback-0.10.0.schema.json')
        identity = oracle.Draft202012Validator(
            {'$ref': public['$id'] + '#/$defs/public_0056'}, registry=registry())
        self.assertFalse(identity.is_valid(''))
        self.assertTrue(identity.is_valid('x'))  # One-byte floor, not a generated-ID prediction.

    def test_actual_public_reads_and_plan_against_independent_oracle(self):
        f = oracle.load(ROOT / 'tests/fixtures/installer-v2/fr2-cross-root.json')
        inventory = oracle.load(ROOT / 'contracts/installer-spine-0.10.0-inventory.json')
        with patch.object(oracle, 'INVENTORY', inventory):
            oracle.plan_check(f['manifest'], f['request'], f['plan'])
        actual = build_plan(f['manifest'], f['request'], f['plan']['environment'], f['plan']['observation'])
        self.assertEqual(actual, f['plan'])
        root = oracle.load(a.SCHEMA_ROOT / 'spine-readback-0.10.0.schema.json')
        for row in f['reads']:
            for field, shape in [('request', 'request'), ('response', 'response')]:
                fragment = {'$ref': root['$id'] + '#/$defs/' + COMMANDS[row['command']][shape]}
                oracle.Draft202012Validator(fragment, registry=registry()).validate(row[field])

    def test_ref_siblings_unevaluated_and_conditionals_crosscheck(self):
        path = a.SCHEMA_ROOT / 'spine-readback-0.10.0.schema.json'
        schema = {'$defs': {'base': {'type': 'object', 'properties': {'a': {'type': 'string'}}}},
                  '$ref': '#/$defs/base', 'required': ['a'], 'unevaluatedProperties': False}
        for value in ({'a': 'x'}, {}, {'a': 1}, {'a': 'x', 'b': 'y'}):
            self.assertEqual(check(value, schema, path, schema)[0], oracle.Draft202012Validator(schema).is_valid(value))
        with self.assertRaises(ValueError): check('x', {'inventedKeyword': True}, path, {})

    def test_baseline_union_cannot_be_mixed(self):
        f = oracle.load(ROOT / 'tests/fixtures/installer-v2/fr2-cross-root.json')
        valid = oracle.validator('spine-pack-install-plan.v2.schema.json')
        self.assertTrue(valid.is_valid(f['plan']))
        for fault in ('old_union', 'old_runtime', 'newer_runtime'):
            plan = deepcopy(f['plan'])
            if fault == 'old_union': plan['required_execution_contracts'].remove('spine.facet-schema-revision-readback.v1')
            else: plan['environment']['runtime_version'] = '0.9.1' if fault == 'old_runtime' else '0.10.1'
            self.assertFalse(valid.is_valid(plan))


if __name__ == '__main__': unittest.main()
