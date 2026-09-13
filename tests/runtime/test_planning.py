"""Planner tests use synthetic public responses; never a live Spine ledger."""
from copy import deepcopy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/contract"))
import test_installer_artifact_contract as independent
import test_pack_manifest_contract as pack_contract
from spine_packs import artifacts as a, manifest as m, planning as p
from spine_packs.__main__ import main, publish
from spine_packs.spine_command import SpineCommand, READ_COMMANDS


def manifest(name="medical_vertical_slice", released=False):
    value = a.load_json(ROOT / f"tests/fixtures/pack-manifest/positive/{name}.json")
    if released:
        value["pack"].update(status="released", version="1.0.0")
        value["content_identity"]["digest"] = m.content_digest(value)
    return value


def request(selection=None):
    value = a.load_json(ROOT / "tests/fixtures/installer/positive/granular_request.json")
    value["request"]["selection"] = selection or {"mode": "all"}
    value["request"]["draft_posture"] = "inspect_only"
    return a.seal(value)


def info():
    return {"ok": True, "command": "system.info", "response_contract": "spine.system-info.v2",
            "runtime_version": "0.3.0", "implemented_ledger_schema_version": "12",
            "ledger_schema_version": "12", "timezone_database_version": "2026a",
            "implemented_contract_versions": a.REQUIRED_EXECUTION_CONTRACTS[:],
            "runtime_dependencies": [{"name": "tickerd", "package_version": "0.2.0",
                "capability_id": "tickerd.runtime-capabilities.v1",
                "descriptor_sha256": "215f9aa6b54e6c0e6186796a55d78e1c5a270adc9b3ccefb433df5a3bb87b58b",
                "compatibility_contract": "spine.tickerd-compatibility.v1", "status": "compatible"}]}


def catalog(pack, owner=None):
    owner = owner or request()["request"]["owner"]
    audit = {"created_by_subject_id": "actor_test", "created_by_command_id": "command_test",
             "created_at_utc": "2026-08-01T00:00:00Z"}
    common = {**owner, **audit, "owner_subject_id": owner.get("owner_subject_id"),
              "owner_group_id": owner.get("owner_group_id"), "status": "active",
              "retired_by_subject_id": None, "retired_by_command_id": None, "retired_at_utc": None}
    result = {k: [] for k in p.CATALOGS}
    for name, definitions, prefix, key_field in (
        ("archetypes", pack["archetypes"], "item_archetype", "archetype_key"),
        ("profiles", pack["notification_profiles"], "notification_profile", "profile_key"),
    ):
        for definition in definitions:
            key = definition[key_field]
            root_id, revision_id = prefix + "_" + key, prefix + "_revision_" + key
            revision = {**deepcopy(definition["revision"]), **audit, prefix + "_id": root_id,
                        prefix + "_revision_id": revision_id, "revision_number": 1}
            revision["normalized_content_hash" if name == "archetypes" else "normalized_revision_hash"] = "a" * 64
            if name == "profiles":
                for index, template in enumerate(revision["templates"]):
                    template.update(notification_profile_template_id=revision_id + str(index),
                                    notification_profile_revision_id=revision_id, template_index=index,
                                    normalized_template_hash="b" * 64)
            entry = {**common, prefix + "_id": root_id, key_field: key, "current_revision_id": revision_id,
                     "retirement_reason": None, "revision": revision}
            if name == "profiles":
                entry.update(display_name=definition["display_name"], description=definition["description"])
            result[name].append(entry)
    for binding in pack["binding_intents"]:
        result["bindings"].append({**common,
            "notification_profile_binding_id": "binding_" + binding["archetype_key"],
            "item_archetype_id": "item_archetype_" + binding["archetype_key"],
            "notification_profile_id": "notification_profile_" + binding["notification_profile_key"]})
    return result


class FakeSpine:
    def __init__(self, entries=None, mutate=None):
        self.entries = deepcopy(entries or {k: [] for k in p.CATALOGS})
        self.mutate = mutate
        self.calls = []
        self.checks = 0
        self.info = info()

    def check_target(self):
        self.checks += 1

    def read(self, command, query):
        assert command in READ_COMMANDS, command
        self.calls.append((command, deepcopy(query)))
        if command == "system.info":
            response = deepcopy(self.info)
        else:
            name = next(k for k, v in p.CATALOGS.items() if command in (v[0] + ".list", v[0] + ".show"))
            p.validate_readback(query, name + ("ListRequest" if command.endswith(".list") else "ShowRequest"))
            prefix, key_field, id_field, _ = p.CATALOGS[name]
            response = {"ok": True, "command": command, "response_contract": p.FAMILIES[name]}
            entries = sorted(self.entries[name], key=lambda e: (e[key_field], e[id_field]))
            if command.endswith(".show"):
                response[prefix] = deepcopy(next(e for e in entries if e[id_field] == query[id_field]))
            else:
                start, limit = int(query.get("cursor", "0")), int(query["limit"])
                page = entries[start:start + limit]
                more = start + limit < len(entries)
                response.update(entries=deepcopy(page), count=str(len(page)), has_more=more,
                                next_cursor=str(start + limit) if more else None,
                                catalog_snapshot_hash=hashlib.sha256(name.encode()).hexdigest())
        if self.mutate:
            self.mutate(command, query, response, self.calls)
        return response


class PlanningTests(unittest.TestCase):
    def plan(self, pack=None, req=None, transport=None, **kwargs):
        plan = p.plan_installation(pack or manifest(), req or request(), transport or FakeSpine(), **kwargs)
        self.assertEqual(independent.plan_errors(plan), [])
        self.assertEqual(independent.artifact_size_errors(plan), [])
        return plan

    def fails(self, transport, code, pack=None, req=None, **kwargs):
        with self.assertRaises(p.PlanError) as caught:
            self.plan(pack, req, transport, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_missing_plan_create_order_and_future_binding_references(self):
        plan = self.plan()
        self.assertEqual([x["command"] for x in plan["actions"]],
                         ["item_archetype.create", "notification_profile.create", "notification_profile.binding.set"])
        body = json.loads(plan["actions"][-1]["request_template"]["canonical_json"])
        self.assertEqual(body["item_archetype_id"], "${spine-pack.result:action-000000:item_archetype_id}")
        self.assertEqual(body["notification_profile_id"], "${spine-pack.result:action-000001:notification_profile_id}")
        self.assertFalse(plan["apply_eligible"])

    def test_equivalent_keeps_definitions_and_no_write_actions(self):
        pack = manifest(released=True)
        transport = FakeSpine(catalog(pack))
        before = deepcopy(transport.entries)
        plan = self.plan(pack, transport=transport)
        self.assertEqual(plan["actions"], [])
        self.assertTrue(plan["apply_eligible"])
        self.assertEqual(transport.entries, before)
        self.assertEqual({x["classification"] for x in plan["classifications"]}, {"equivalent"})

    def test_profile_metadata_revision_and_both_drift(self):
        pack = manifest(released=True)
        for metadata, revision in ((True, False), (False, True), (True, True)):
            with self.subTest(metadata=metadata, revision=revision):
                entries = catalog(pack)
                profile = entries["profiles"][0]
                if metadata:
                    profile["display_name"] = "Old name"
                if revision:
                    profile["revision"]["templates"][0]["late_handling"]["grace_seconds"] = "1"
                plan = self.plan(pack, transport=FakeSpine(entries))
                expected = (["notification_profile.metadata.update"] if metadata else []) + (["notification_profile.revise"] if revision else [])
                self.assertEqual([a["command"] for a in plan["actions"]], expected)
                self.assertTrue(plan["apply_eligible"])
                self.assertEqual(p.plan_outcome(plan), "decision_required_for_drift")
                for action in plan["actions"]:
                    self.assertEqual(action["expected"], plan["classifications"][1]["observed"])

    def test_archetype_revision_and_binding_drift(self):
        pack = manifest("medical_and_lesson", released=True)
        entries = catalog(pack)
        entries["archetypes"][0]["revision"]["description"] = "Earlier description"
        entries["bindings"][0]["notification_profile_id"] = entries["profiles"][1]["notification_profile_id"]
        plan = self.plan(pack, transport=FakeSpine(entries))
        self.assertEqual([a["command"] for a in plan["actions"]], ["item_archetype.revise", "notification_profile.binding.set"])

    def test_approved_outcome_precedence(self):
        for draft in (True, False):
            for blocked in (True, False):
                for drift in (True, False):
                    with self.subTest(draft=draft, blocked=blocked, drift=drift):
                        pack = manifest(released=not draft)
                        entries = catalog(pack)
                        if drift:
                            entries["profiles"][0]["display_name"] = "Old"
                        if blocked:
                            root = entries["archetypes"][0]
                            root.update(status="retired", retirement_reason="Retired",
                                        retired_by_subject_id="actor", retired_by_command_id="cmd",
                                        retired_at_utc="2026-08-02T00:00:00Z")
                        plan = self.plan(pack, transport=FakeSpine(entries))
                        self.assertEqual(plan["apply_eligible"], not draft and not blocked)
                        expected = "blocked_desired_state" if blocked else "success" if draft or not drift else "decision_required_for_drift"
                        self.assertEqual(p.plan_outcome(plan), expected)

    def test_granular_closure_and_page_size_independent_digest(self):
        pack = manifest("medical_and_lesson")
        req = request({"mode": "archetypes", "archetype_keys": ["lesson"]})
        small = self.plan(pack, req, FakeSpine(catalog(pack)), page_size=1)
        large = self.plan(pack, req, FakeSpine(catalog(pack)), page_size=100)
        self.assertEqual(small, large)
        self.assertEqual(small["closure"], {"archetype_keys": ["lesson"], "profile_keys": ["lesson_standard"], "binding_archetype_keys": ["lesson"]})

    def test_latest_draft_all_content(self):
        plan = self.plan(manifest("kinflow_starter_draft_9"))
        self.assertEqual(len(plan["closure"]["archetype_keys"]), 52)
        self.assertEqual(len(plan["actions"]), 156)

    def test_shared_profile_unbound_archetype_and_orphan_profile_selection(self):
        pack = manifest("medical_and_lesson")
        pack["binding_intents"][0]["notification_profile_key"] = pack["binding_intents"][1]["notification_profile_key"]
        pack["content_identity"]["digest"] = m.content_digest(pack)
        req = request({"mode": "archetypes", "archetype_keys": ["lesson", "medical_appointment"]})
        self.assertEqual(len(self.plan(pack, req)["closure"]["profile_keys"]), 1)
        self.assertEqual(len(self.plan(pack)["closure"]["profile_keys"]), 2)
        pack["binding_intents"] = pack["binding_intents"][1:]
        pack["content_identity"]["digest"] = m.content_digest(pack)
        req = request({"mode": "archetypes", "archetype_keys": ["lesson"]})
        self.assertEqual(self.plan(pack, req)["closure"]["profile_keys"], [])

    def test_invalid_unselected_manifest_rejected_before_transport(self):
        pack = manifest("medical_and_lesson")
        pack["archetypes"][1]["owner"] = "forbidden"
        pack["content_identity"]["digest"] = m.content_digest(pack)
        transport = FakeSpine()
        self.fails(transport, "invalid_manifest", pack=pack,
                   req=request({"mode": "archetypes", "archetype_keys": ["lesson"]}))
        self.assertEqual(transport.calls, [])
        self.assertEqual(transport.checks, 0)

    def test_bad_digest_draft_rejection_and_unknown_selection_before_reads(self):
        bad = request()
        bad["content_identity"]["digest"] = "0" * 64
        reject = request()
        reject["request"]["draft_posture"] = "reject"
        cases = [(bad, "invalid_request"), (a.seal(reject), "draft_inspection_not_allowed"),
                 (request({"mode": "archetypes", "archetype_keys": ["missing"]}), "unknown_archetype_selection")]
        for req, code in cases:
            transport = FakeSpine()
            self.fails(transport, code, req=req)
            self.assertEqual(transport.calls, [])

    def test_incompatible_runtime_and_execution_contract_fail_before_catalog(self):
        for field, value in (("runtime_version", "0.4.0"), ("ledger_schema_version", "13"),
                             ("implemented_contract_versions", a.REQUIRED_EXECUTION_CONTRACTS[1:])):
            transport = FakeSpine()
            transport.info[field] = value
            self.fails(transport, "incompatible_runtime_or_contracts")
            self.assertEqual(len(transport.calls), 1)

    def test_owner_scope_group(self):
        req = request()
        req["request"]["owner"] = {"owner_kind": "subject_group", "owner_group_id": "family_test"}
        req = a.seal(req)
        pack = manifest()
        self.assertEqual(self.plan(pack, req, FakeSpine(catalog(pack, req["request"]["owner"])))["actions"], [])

    def test_malformed_or_unstable_readback_fails_closed(self):
        cases = [
            ("owner", "catalog_owner_mismatch"), ("count", "invalid_page_count"),
            ("contract", "invalid_public_response"), ("show", "catalog_show_changed"),
            ("snapshot", "catalog_changed"), ("cursor", "cursor_presence_invalid"),
            ("index", "readback_template_indices_invalid"), ("revision", "revision_identity_mismatch"),
        ]
        for defect, expected in cases:
            with self.subTest(defect=defect):
                def mutate(command, query, response, calls):
                    if defect == "show" and command.endswith(".show"):
                        response[command.removesuffix(".show")]["revision"]["description"] = "Changed"
                    if command == "item_archetype.list":
                        if defect == "owner": response["entries"][0]["owner_subject_id"] = "wrong"
                        if defect == "count": response["count"] = "2"
                        if defect == "contract": response["response_contract"] = "unknown"
                        if defect == "cursor": response["next_cursor"] = "bad"
                        if defect == "revision": response["entries"][0]["current_revision_id"] = "wrong"
                        if defect == "snapshot" and len(calls) > 5: response["catalog_snapshot_hash"] = "0" * 64
                    if defect == "index" and command == "notification_profile.list":
                        response["entries"][0]["revision"]["templates"][0]["template_index"] = 9
                self.fails(FakeSpine(catalog(manifest()), mutate), expected)

    def test_unresolvable_binding_blocks_not_missing(self):
        entries = catalog(manifest())
        entries["bindings"][0]["notification_profile_id"] = "unknown_root"
        plan = self.plan(transport=FakeSpine(entries))
        self.assertEqual(plan["blocked_object_keys"], ["binding:medical_appointment"])
        self.assertEqual(plan["actions"], [])

    def test_duplicate_and_repeated_pages_rejected(self):
        pack = manifest("medical_and_lesson")
        def mutate(command, query, response, calls):
            if command == "item_archetype.list" and "cursor" in query:
                response["entries"][0] = deepcopy(catalog(pack)["archetypes"][0])
        self.fails(FakeSpine(catalog(pack), mutate), "catalog_order_invalid", pack=pack, page_size=1)

    def test_empty_continuation_and_cursor_cycle_fail_closed(self):
        for empty, code in ((True, "cursor_cycle_or_empty_page"), (False, "cursor_cycle_or_empty_page")):
            def mutate(command, query, response, calls):
                if command == "item_archetype.list":
                    response.update(has_more=True, next_cursor="1")
                    if empty:
                        response.update(entries=[], count="0")
            pack = manifest("medical_and_lesson")
            self.fails(FakeSpine(catalog(pack), mutate), code, pack=pack, page_size=1)

    def test_changed_target_and_snapshot_never_yield_partial_plan(self):
        transport = FakeSpine()
        def changed_target():
            transport.checks += 1
            if transport.checks > 1:
                raise p.PlanError("stale_plan_or_target_mismatch", "target_binding_mismatch")
        transport.check_target = changed_target
        self.fails(transport, "target_binding_mismatch")

    def test_runtime_manifest_validator_matches_all_contract_vectors(self):
        schema = a.load_json(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")
        for path in (ROOT / "tests/fixtures/pack-manifest").rglob("*.json"):
            with self.subTest(path=path.name):
                try:
                    value = a.parse_json(path.read_bytes())
                except ValueError:
                    self.assertEqual(path.parent.name, "negative")
                    continue
                actual = m.validate_pack(value, schema)
                self.assertEqual(actual, pack_contract.validate_pack(value, schema))
                self.assertEqual(bool(actual), path.parent.name == "negative")

    def test_pinned_schema_vocabulary_is_supported(self):
        supported = {"$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
                     "type", "const", "enum", "properties", "required", "additionalProperties",
                     "minLength", "maxLength", "pattern", "items", "minItems", "maxItems", "uniqueItems",
                     "oneOf", "anyOf", "allOf", "not", "if", "then", "else", "contains", "minContains",
                     "maxContains", "minimum"}
        def inspect(schema):
            self.assertEqual(set(schema) - supported, set())
            for key in ("$defs", "properties"):
                for child in schema.get(key, {}).values(): inspect(child)
            for key in ("items", "not", "if", "then", "else", "contains"):
                if isinstance(schema.get(key), dict): inspect(schema[key])
            for key in ("oneOf", "anyOf", "allOf"):
                for child in schema.get(key, []): inspect(child)
        for path in a.SCHEMA_ROOT.glob("*.json"):
            with self.subTest(schema=path.name): inspect(a.load_json(path))

    def test_public_boolean_is_not_a_json_integer(self):
        response = info()
        response["ok"] = 1
        with self.assertRaises(p.PlanError):
            p.validate_readback(response, "systemInfo")


class CliAndAdapterTests(unittest.TestCase):
    def invoke(self, directory, *, pack=None, req=None, flags=(), transport=None):
        directory = Path(directory)
        (directory / "pack.json").write_text(a.canonical_text(pack or manifest()), encoding="utf-8")
        (directory / "request.json").write_text(a.canonical_text(req or request()), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["plan", "--manifest", str(directory / "pack.json"), "--request", str(directory / "request.json"),
                         "--output", str(directory / "plan.json"), *flags], transport_factory=lambda target: transport or FakeSpine())
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        result = json.loads(lines[0])
        self.assertEqual(independent.validate_schema(result), [])
        self.assertEqual(str(code), result["exit_code"])
        return code, result

    def test_cli_publishes_private_artifact_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory)
            self.assertEqual(code, 0)
            output = Path(directory) / "plan.json"
            before = output.read_bytes()
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(a.load_json(output)["content_identity"]["digest"], result["artifact"]["digest"])
            code, result = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(result["error"]["code"], "output_already_exists")
            self.assertEqual(output.read_bytes(), before)
            self.assertFalse(list(Path(directory).glob(".spine-plan-*")))

    def test_cli_drift_and_blocked_results_keep_reviewable_artifact(self):
        pack = manifest(released=True)
        entries = catalog(pack)
        entries["profiles"][0]["display_name"] = "Old"
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, pack=pack, transport=FakeSpine(entries))
            self.assertEqual(code, 5)
            self.assertIsNotNone(result["artifact"])
        entries["bindings"][0]["notification_profile_id"] = "missing"
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, pack=pack, transport=FakeSpine(entries))
            self.assertEqual(code, 6)
            self.assertIsNotNone(result["artifact"])

    def test_cli_assertion_failure_and_missing_input_no_transport(self):
        transport = FakeSpine()
        with tempfile.TemporaryDirectory() as directory:
            code, result = self.invoke(directory, flags=["--archetype", "lesson"], transport=transport)
            self.assertEqual(code, 2)
            self.assertEqual(transport.calls, [])
            self.assertFalse((Path(directory) / "plan.json").exists())

    def test_unimplemented_operations_are_not_cli_commands(self):
        for command in ("verify", "recover"):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([command]), 2)
            self.assertEqual(json.loads(output.getvalue())["error"]["code"], "invalid_cli_arguments")

    def test_publication_race_and_symlink_never_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "existing"
            existing.write_bytes(b"preserve")
            with self.assertRaises(p.PlanError):
                publish(existing, {})
            self.assertEqual(existing.read_bytes(), b"preserve")
            (Path(directory) / "plan.json").symlink_to(existing)
            code, _ = self.invoke(directory)
            self.assertEqual(code, 2)
            self.assertEqual(existing.read_bytes(), b"preserve")
            self.assertEqual(list(Path(directory).glob(".spine-plan-*")), [])

    def test_invalid_read_request_rejected_before_spawn(self):
        transport = SpineCommand({})
        with patch.object(transport, "check_target") as check, patch("subprocess.Popen") as spawn:
            for body in ({}, {"contract_version": p.FAMILIES["archetypes"], "owner": request()["request"]["owner"], "limit": "501"}):
                with self.assertRaises(p.PlanError):
                    transport.read("item_archetype.list", body)
            check.assert_not_called()
            spawn.assert_not_called()

    def test_strict_json_boundary(self):
        for raw in (b'{"x":1}', b'{"x":1.5}', b'{"x":NaN}', b'{"x":null,"x":true}',
                    b'\xef\xbb\xbf{}', b'{"x":"\\ud800"}', b'{} trailing'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                a.parse_json(raw)
        self.assertEqual(a.parse_json(b'{"revision_number":1}', public_response=True), {"revision_number": 1})
        with self.assertRaises(ValueError):
            a.parse_json(b'{"revision_number":1.5}', public_response=True)

    def test_adapter_rejects_write_before_target_or_spawn(self):
        transport = SpineCommand({})
        with patch.object(transport, "check_target") as check, patch("subprocess.Popen") as spawn:
            for command in a.COMMAND_SHAPES:
                with self.assertRaises(p.PlanError):
                    transport.read(command, {})
            check.assert_not_called()
            spawn.assert_not_called()

    def test_adapter_target_identity_without_opening_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            exe, ledger = Path(directory) / "fake-command", Path(directory) / "ledger"
            exe.write_bytes(b"#!/bin/sh\nexit 0\n")
            exe.chmod(0o700)
            ledger.write_bytes(b"not a database")
            target = {"host_name": "test.local", "spine_command": {"path": str(exe.resolve()),
                      "sha256": hashlib.sha256(exe.read_bytes()).hexdigest()},
                      "ledger": {"kind": "path", "path": str(ledger.resolve())}}
            transport = SpineCommand(target, host_resolver=lambda: "TEST.LOCAL.")
            original = Path.open
            def safe_open(path, *args, **kwargs):
                self.assertNotEqual(path, ledger.resolve(), "adapter must never open ledger")
                return original(path, *args, **kwargs)
            with patch.object(Path, "open", safe_open):
                transport.check_target()
            target["spine_command"]["sha256"] = "0" * 64
            with self.assertRaises(p.PlanError) as caught:
                transport.check_target()
            self.assertEqual(caught.exception.category, "stale_plan_or_target_mismatch")

    def test_real_subprocess_argv_stdin_and_bounded_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            exe = Path(directory) / "fake command"
            target = request()["request"]["target"]
            target["spine_command"]["path"] = str(exe)
            programs = [
                ("import json,sys\nassert sys.argv[1:]==['--db','/var/lib/spine/ledger.sqlite3','system.info','--input','-']\nassert sys.stdin.read()=='{}\\n'\nprint(json.dumps({'ok':True,'command':'system.info'}))\n", None),
                ("print('not json')\n", "spine_transport_failed"),
                ("import json\nprint(json.dumps({'ok':True,'command':'wrong'}))\n", "response_command_mismatch"),
                ("import json,sys\nprint(json.dumps({'ok':False,'command':'system.info','error':{'code':'invalid_request','message':'private detail','field':None}}))\nsys.exit(3)\n", "spine_read_rejected"),
                ("import time\ntime.sleep(2)\n", "spine_timeout"),
                ("print('x'*2048)\n", "spine_response_too_large"),
            ]
            for program, error in programs:
                with self.subTest(error=error):
                    exe.write_text("#!" + sys.executable + "\n" + program, encoding="utf-8")
                    exe.chmod(0o700)
                    transport = SpineCommand(target, timeout=0.5)
                    with patch.object(transport, "check_target"), patch("spine_packs.spine_command.RESPONSE_LIMIT", 1024):
                        if error:
                            with self.assertRaises(p.PlanError) as caught:
                                transport.read("system.info", {})
                            self.assertEqual(caught.exception.code, error)
                        else:
                            self.assertTrue(transport.read("system.info", {})["ok"])


if __name__ == "__main__":
    unittest.main()
