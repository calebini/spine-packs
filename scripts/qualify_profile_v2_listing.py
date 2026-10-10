"""Bounded public-CLI listing gate; always allocates a new disposable ledger.

This is test tooling, not installer behavior or full installer qualification.
Run with an isolated installed Spine 0.9.1 bin directory. Retains the private
temporary run directory and transcripts on success or failure. No ledger input,
Spine imports, SQL, item authoring, disclosure, or delivery commands are allowed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

V1 = "spine.notification-profiles.v1"
V2 = "spine.notification-profiles.v2"
NOW = "2035-02-01T12:00:00Z"
OWNER = {"owner_kind": "subject", "owner_subject_id": "listing_gate_owner"}
COMMANDS = frozenset({
    "system.info", "subject.upsert", "notification_profile.create",
    "notification_profile.show", "notification_profile.list",
    "facet_schema.create", "notification_rendering_definition.create",
})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def qualify(bin_dir: Path, schemas_dir: Path):
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource

    schemas = [json.loads(p.read_text()) for p in schemas_dir.glob("*.schema.json")]
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas)
    run = Path(tempfile.mkdtemp(prefix="spine-packs-profile-v2-gate-"))
    ledger = run / "new.sqlite"
    command = bin_dir / "spine-command"
    migrate = bin_dir / "spine-ledger-migrate"
    # Deliberately do not inherit PYTHONPATH or operator Spine configuration.
    env = {"PATH": str(bin_dir) + ":/usr/bin:/bin", "PYTHONNOUSERSITE": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"}
    transcript, checks = [], []

    def invoke(argv, request=None, expected=0):
        require(len(transcript) < 100, "command budget exhausted")
        result = subprocess.run(argv, input=json.dumps(request) if request is not None else None,
                                text=True, capture_output=True, cwd=run, env=env, timeout=30)
        require(len(result.stdout.encode()) <= 4 * 1024 * 1024, "response too large")
        response = json.loads(result.stdout)
        transcript.append({"argv": argv, "request": request, "exit_code": result.returncode,
                           "response": response})
        require(result.returncode == expected, f"unexpected exit for {argv[-2:]}: {response}")
        return response

    def cli(name, request, expected=0):
        require(name in COMMANDS, "command outside qualification allowlist")
        response = invoke([str(command), "--db", str(ledger), "--input", "-", *name.split(".")], request, expected)
        require(response["ok"] == (expected == 0), "inconsistent success envelope")
        if expected == 0:
            require(response["command"] == name, "wrong response command")
            if name.startswith("notification_profile."):
                require(response["response_contract"] == request["contract_version"], "wrong profile decoder")
                if request["contract_version"] == V2:
                    uri = "https://cortext.local/spine/contracts/schemas/notification-profile-responses-v2.schema.json"
                    Draft202012Validator({"$ref": uri + "#/$defs/" + name.rsplit(".", 1)[1]},
                                         registry=registry, format_checker=FormatChecker()).validate(response)
        return response

    def write(name, contract, **fields):
        return cli(name, {"contract_version": contract, "command_id": f"listing-gate-{len(transcript)}",
                          "actor_subject_id": OWNER["owner_subject_id"], "action_timestamp_utc": NOW, **fields})

    def create(key, version=V2, rendering=None):
        template = {"template_key": "one_hour_before",
                    "schedule": {"kind": "once", "at": {"kind": "target_offset", "offset_basis": "elapsed", "offset_seconds": "-3600"}},
                    "late_handling": {"kind": "deliver_within", "grace_seconds": "900"}}
        if version == V2:
            template["rendering"] = rendering or {"kind": "ordinary"}
        return write("notification_profile.create", version, owner=OWNER, profile_key=key,
                     display_name=key, description=None,
                     revision={"compatible_item_types": ["event"], "templates": [template]})

    def show(created):
        return cli("notification_profile.show", {"contract_version": V2,
                   "notification_profile_id": created["notification_profile_id"],
                   "notification_profile_revision_id": created["notification_profile_revision_id"]})["notification_profile"]

    def listing(limit="500", cursor=None, version=V2, expected=0):
        request = {"contract_version": version, "owner": OWNER, "status": "active", "limit": limit}
        if cursor is not None:
            request["cursor"] = cursor
        return cli("notification_profile.list", request, expected)

    try:
        require(not ledger.exists(), "refusing existing ledger")
        invoke([str(migrate), "--db", str(ledger), "--initialize-if-empty"])
        info = cli("system.info", {})
        require(info["runtime_version"] == "0.9.1", "wrong runtime")
        require(str(info["ledger_schema_version"]) == "19", "wrong current schema")
        require(info["implemented_ledger_schema_version"] == "19", "wrong implemented schema")
        Draft202012Validator(json.loads((schemas_dir / "system-info-response-v3.schema.json").read_text()),
                             registry=registry).validate(info)
        cli("subject.upsert", {"command_id": "listing-gate-owner", "actor_subject_id": OWNER["owner_subject_id"],
            "subject_id": OWNER["owner_subject_id"], "subject_kind": "person", "display_name": "Synthetic listing gate owner",
            "updated_at_utc": NOW})
        require(listing()["entries"] == [], "new owner catalog is not empty")
        ordinary = create("b_ordinary")
        ordinary_show = show(ordinary)
        require(listing()["entries"] == [ordinary_show], "ordinary create/show/list mismatch")
        checks.append("ordinary_v2_create_show_list")
        profiles = [create("a_legacy", V1), ordinary, create("c_legacy", V1), create("d_ordinary")]
        schema = write("facet_schema.create", "spine.facet-schemas.v1", owner=OWNER, schema_key="gate_flight",
            definition={"display_name": "Synthetic flight", "description": None, "compatible_item_types": ["event"],
                        "fields": [{"key": "flight_number", "type": "text", "max_length": "32", "required": False, "queryable": False}]})
        definition = write("notification_rendering_definition.create", "spine.notification-rendering-definitions.v1",
            owner=OWNER, definition_key="gate_flight", revision={"display_name": "Synthetic details", "description": None,
                "compatible_item_types": ["event"], "base_rendering_contract": "spine.notification-rendering.v1",
                "base_rendering_profile": "spine.notification-rendering.concise-en-ca.v1",
                "selections": [{"selection_key": "flight", "facet_key": "flight", "facet_schema_revision_id": schema["facet_schema_revision_id"],
                                "field_key": "flight_number", "label": "Flight", "projection": "value"}]})["record"]
        rendering = {"kind": "definition", "definition": {
            "notification_rendering_definition_id": definition["notification_rendering_definition_id"],
            "notification_rendering_definition_revision_id": definition["current_revision_id"]}}
        profiles.append(create("e_pinned", rendering=rendering))
        expected = [show(p) for p in profiles]
        require(expected[-1]["revision"]["content"]["templates"][0]["rendering"] == rendering, "lost definition pin")
        snapshots = set()
        for limit in ("1", "2", "500"):
            entries, seen, cursor = [], set(), None
            for _ in range(len(profiles) + 1):
                page = listing(limit, cursor)
                require(page["count"] == str(len(page["entries"])), "wrong count")
                require(len(page["entries"]) <= int(limit), "page exceeds requested limit")
                entries.extend(page["entries"])
                snapshots.add(page["catalog_snapshot_hash"])
                if not page["has_more"]:
                    require(page["next_cursor"] is None, "terminal cursor not null")
                    break
                cursor = page["next_cursor"]
                require(isinstance(cursor, str) and cursor and cursor not in seen, "repeated or missing cursor")
                seen.add(cursor)
            else:
                raise RuntimeError("pagination did not terminate")
            require(entries == expected, "pagination lost, duplicated, reordered or changed profiles")
            checks.append(f"mixed_v1_v2_complete_pagination_limit_{limit}")
        require(len(snapshots) == 1, "snapshot changed between page sizes")
        require([e["revision"]["revision_contract"] for e in expected] == [V1, V2, V1, V2, V2], "historical decoder lost")
        checks.append("definition_pins_and_decoder_identity_preserved")
        guard = listing(version=V1, expected=2)
        require(guard["error"]["code"] == "unsupported_contract_version", "v1 guard changed")
        checks.append("v1_guard_preserved")
        return {"status": "passed", "runtime": "0.9.1", "schema": "19", "checks": checks,
                "command_count": len(transcript), "run_directory": str(run), "installer_qualification": False}
    finally:
        # Generated test evidence only; no database reads, even for diagnostics.
        evidence = json.dumps(transcript, indent=2) + "\n"
        (run / "public-cli-transcript.json").write_text(evidence)
        print(json.dumps({"transcript": str(run / "public-cli-transcript.json"),
                          "sha256": hashlib.sha256(evidence.encode()).hexdigest()}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin-dir", required=True, type=Path)
    parser.add_argument("--schemas-dir", required=True, type=Path,
                        help="Public schemas from the exact repaired Git export")
    args = parser.parse_args()
    print(json.dumps(qualify(args.bin_dir.resolve(), args.schemas_dir.resolve()), sort_keys=True))
