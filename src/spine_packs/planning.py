"""Read-only planning over a supplied public-command transport.

The transport owns process/filesystem interaction. This module never submits
the write templates it constructs, and never imports Spine internals.
"""
from __future__ import annotations

from copy import deepcopy

from . import artifacts as a
from .manifest import validate_pack


class PlanError(Exception):
    def __init__(self, category: str, code: str):
        super().__init__(code)
        self.category = category
        self.code = code


INVALID = "invalid_cli_or_artifact_input"
PACK_INVALID = "invalid_pack_contract_or_digest"
ENVIRONMENT = "transport_or_environment_failure"
INCOMPATIBLE = "incompatible_spine_runtime_or_contracts"


def require(condition, code, category=ENVIRONMENT):
    if not condition:
        raise PlanError(category, code)


CATALOGS = {
    "archetypes": ("item_archetype", "archetype_key", "item_archetype_id", "archetype"),
    "profiles": ("notification_profile", "profile_key", "notification_profile_id", "profile"),
    "bindings": ("notification_profile.binding", "item_archetype_id", "notification_profile_binding_id", "binding"),
}
FAMILIES = {
    "archetypes": "spine.item-archetypes.v1",
    "profiles": "spine.notification-profiles.v1",
    "bindings": "spine.notification-profile-bindings.v1",
}


def validate_readback(value, shape):
    path = a.SCHEMA_ROOT / "spine-readback-0.3.0.schema.json"
    schema = a._schema_document(path)
    require(not a.schema_errors(value, schema["$defs"][shape], path, schema),
            "invalid_public_response")


def owner_matches(entry, owner):
    return (entry["owner_kind"] == owner["owner_kind"]
            and entry["owner_subject_id"] == owner.get("owner_subject_id")
            and entry["owner_group_id"] == owner.get("owner_group_id"))


def semantics(entry, kind):
    revision = entry["revision"]
    if kind == "archetype":
        return {k: deepcopy(revision[k]) for k in
                ("display_name", "description", "compatible_item_types")}
    return {
        "metadata": {k: entry[k] for k in ("display_name", "description")},
        "revision": {
            "compatible_item_types": deepcopy(revision["compatible_item_types"]),
            "templates": [{k: deepcopy(t[k]) for k in ("template_key", "schedule", "late_handling")}
                          for t in revision["templates"]],
        },
    }


def validate_entry(entry, owner, kind):
    require(owner_matches(entry, owner), "catalog_owner_mismatch")
    retired = entry["status"] == "retired"
    require(all((entry[k] is not None) == retired for k in
                ("retired_by_subject_id", "retired_by_command_id", "retired_at_utc")),
            "catalog_retirement_mismatch")
    if kind == "binding":
        return
    prefix = "item_archetype" if kind == "archetype" else "notification_profile"
    revision = entry["revision"]
    require(revision[prefix + "_id"] == entry[prefix + "_id"]
            and revision[prefix + "_revision_id"] == entry["current_revision_id"],
            "revision_identity_mismatch")
    require(revision["compatible_item_types"] == sorted(set(revision["compatible_item_types"])),
            "readback_item_types_not_canonical")
    if kind == "profile":
        templates = revision["templates"]
        require([t["template_key"] for t in templates] == sorted({t["template_key"] for t in templates}),
                "readback_templates_not_canonical")
        require([t["template_index"] for t in templates] == list(range(len(templates))),
                "readback_template_indices_invalid")
        require(len({t["notification_profile_template_id"] for t in templates}) == len(templates)
                and all(t["notification_profile_revision_id"] == entry["current_revision_id"]
                        for t in templates), "template_identity_mismatch")


def observe_catalog(transport, catalog, owner, *, page_size=100):
    command, key_field, id_field, kind = CATALOGS[catalog]
    query = {"contract_version": FAMILIES[catalog], "owner": owner, "limit": str(page_size)}
    # Roots include active and retired definitions. Only active bindings affect defaults.
    if kind == "binding":
        query["status"] = "active"
    entries, ids, keys, cursors = [], set(), set(), set()
    snapshot, previous = None, None
    while True:
        page = transport.read(command + ".list", query)
        validate_readback(page, catalog + "Page")
        require(page["count"] == str(len(page["entries"])) and len(page["entries"]) <= page_size,
                "invalid_page_count")
        require(snapshot is None or snapshot == page["catalog_snapshot_hash"], "catalog_changed")
        snapshot = page["catalog_snapshot_hash"]
        for entry in page["entries"]:
            validate_entry(entry, owner, kind)
            ordering = (entry[key_field], entry[id_field])
            require(previous is None or ordering > previous, "catalog_order_invalid")
            require(entry[id_field] not in ids and entry[key_field] not in keys, "catalog_duplicate")
            if kind == "binding":
                require(entry["status"] == "active", "inactive_binding_readback")
            previous = ordering
            ids.add(entry[id_field])
            keys.add(entry[key_field])
            if kind != "binding":
                shown = transport.read(command + ".show", {
                    "contract_version": FAMILIES[catalog], id_field: entry[id_field],
                })
                validate_readback(shown, kind + "Show")
                require(shown[command] == entry, "catalog_show_changed")
            entries.append(entry)
        cursor = page["next_cursor"]
        require(page["has_more"] == (cursor is not None), "cursor_presence_invalid")
        if not page["has_more"]:
            break
        require(bool(page["entries"]) and cursor not in cursors, "cursor_cycle_or_empty_page")
        cursors.add(cursor)
        query = {**query, "cursor": cursor}
    return entries, snapshot


def selected_definitions(manifest, request):
    archetypes = {x["archetype_key"]: x for x in manifest["archetypes"]}
    profiles = {x["profile_key"]: x for x in manifest["notification_profiles"]}
    bindings = {x["archetype_key"]: x for x in manifest["binding_intents"]}
    selection = request["selection"]
    if selection["mode"] == "archetypes":
        keys = selection["archetype_keys"]
        require(set(keys) <= archetypes.keys(), "unknown_archetype_selection", INVALID)
        archetypes = {k: archetypes[k] for k in keys}
        bindings = {k: b for k, b in bindings.items() if k in archetypes}
        profile_keys = {b["notification_profile_key"] for b in bindings.values()}
        profiles = {k: p for k, p in profiles.items() if k in profile_keys}
    return archetypes, profiles, bindings


def build_plan(manifest, request_artifact, environment, catalogs, snapshots):
    """Compile validated, owner-scoped public observations to a sealed plan."""
    request = request_artifact["request"]
    archetypes, profiles, bindings = selected_definitions(manifest, request)
    classifications, pending = [], []
    roots = {}

    def value(kind, semantic):
        return a.canonical_value(a.SEMANTIC_CONTRACTS[kind + "Semantics"], semantic)

    def classify(kind, key, desired, observed, state, identity, reason=None):
        c = {"object_kind": kind, "object_key": kind + ":" + key,
             "classification": state, "desired": value(kind, desired),
             "observed": None if observed is None else value(kind, observed),
             "identity": identity, "blocked_reason": reason}
        classifications.append(c)
        return c

    def action(c, command, body, rank):
        pending.append((rank, c["object_key"], command, c, body))

    for kind, desired_by_key, catalog, prefix in (
        ("archetype", archetypes, "archetypes", "item_archetype"),
        ("profile", profiles, "profiles", "notification_profile"),
    ):
        by_key = {r["archetype_key" if kind == "archetype" else "profile_key"]: r
                  for r in catalogs[catalog]}
        for key in sorted(desired_by_key):
            definition = desired_by_key[key]
            desired = (deepcopy(definition["revision"]) if kind == "archetype" else {
                "metadata": {k: definition[k] for k in ("display_name", "description")},
                "revision": deepcopy(definition["revision"]),
            })
            existing = by_key.get(key)
            observed = None if existing is None else semantics(existing, kind)
            state = ("missing" if existing is None else "blocked" if existing["status"] == "retired"
                     else "equivalent" if desired == observed else "drifted")
            c = classify(kind, key, desired, observed, state,
                         None if existing is None else {"catalog_id": existing[prefix + "_id"]},
                         "retired_definition" if state == "blocked" else None)
            roots[(kind, key)] = c
            contract = FAMILIES[catalog]
            if state == "missing":
                body = {"contract_version": contract, "owner": deepcopy(request["owner"]),
                        "archetype_key" if kind == "archetype" else "profile_key": key,
                        "revision": deepcopy(definition["revision"])}
                if kind == "profile":
                    body.update(desired["metadata"])
                action(c, prefix + ".create", body, 0 if kind == "archetype" else 1)
            elif state == "drifted":
                if kind == "profile" and desired["metadata"] != observed["metadata"]:
                    action(c, "notification_profile.metadata.update", {
                        "contract_version": "spine.notification-profile-metadata-update.v1",
                        "notification_profile_id": existing["notification_profile_id"],
                        "expected_metadata": deepcopy(observed["metadata"]),
                        "metadata": deepcopy(desired["metadata"]),
                    }, 2)
                if kind == "archetype" or desired["revision"] != observed["revision"]:
                    action(c, prefix + ".revise", {
                        "contract_version": contract, prefix + "_id": existing[prefix + "_id"],
                        "expected_current_revision_id": existing["current_revision_id"],
                        "revision": deepcopy(definition["revision"]),
                    }, 0 if kind == "archetype" else 3)

    profiles_by_id = {p["notification_profile_id"]: p for p in catalogs["profiles"]}
    bindings_by_archetype = {b["item_archetype_id"]: b for b in catalogs["bindings"]}
    for key in sorted(bindings):
        profile_key = bindings[key]["notification_profile_key"]
        root_a, root_p = roots[("archetype", key)], roots[("profile", profile_key)]
        desired = {"binding_kind": "archetype_default", "notification_profile_key": profile_key}
        archetype_id = root_a["identity"]["catalog_id"] if root_a["identity"] else None
        profile_id = root_p["identity"]["catalog_id"] if root_p["identity"] else None
        binding = bindings_by_archetype.get(archetype_id)
        observed_profile = profiles_by_id.get(binding["notification_profile_id"]) if binding else None
        if ("blocked" in (root_a["classification"], root_p["classification"])
                or (binding is not None and observed_profile is None)):
            classify("binding", key, desired, None, "blocked", None, "unresolved_binding_dependency")
            continue
        observed = None if binding is None else {
            "binding_kind": "archetype_default", "notification_profile_key": observed_profile["profile_key"],
        }
        state = ("missing" if binding is None else "equivalent"
                 if binding["notification_profile_id"] == profile_id else "drifted")
        identity = {"item_archetype_id": archetype_id, "notification_profile_id": profile_id,
                    "observed_binding": None if binding is None else
                    {k: binding[k] for k in ("notification_profile_binding_id", "item_archetype_id", "notification_profile_id")}}
        c = classify("binding", key, desired, observed, state, identity)
        if state != "equivalent":
            action(c, "notification_profile.binding.set", {
                "contract_version": FAMILIES["bindings"], "owner": deepcopy(request["owner"]),
                "item_archetype_id": archetype_id, "notification_profile_id": profile_id,
            }, 4)

    actions, producers = [], {}
    for index, (_, key, command, c, body) in enumerate(sorted(pending, key=lambda p: (p[0], p[1]))):
        action_id = f"action-{index:06d}"
        if command.endswith(".create"):
            producers[key] = action_id
        if command == "notification_profile.binding.set":
            binding_key = key.split(":", 1)[1]
            for field, producer_key in (
                ("item_archetype_id", "archetype:" + binding_key),
                ("notification_profile_id", "profile:" + bindings[binding_key]["notification_profile_key"]),
            ):
                if body[field] is None:
                    body[field] = "${spine-pack.result:" + producers[producer_key] + ":" + field + "}"
        prefix, contract = a.COMMAND_SHAPES[command]
        actions.append({"ordinal": str(index), "action_id": action_id, "command": command,
                        "object_key": key, "change_kind": "create" if c["classification"] == "missing" else "update",
                        "desired": deepcopy(c["desired"]), "expected": deepcopy(c["observed"]),
                        "request_template": a.canonical_value(contract, body, prefix + "Template")})
    blocked = sorted(c["object_key"] for c in classifications if c["classification"] == "blocked")
    plan = a.seal({
        "artifact_schema": "spine.pack-install-plan.v1",
        "request_digest": request_artifact["content_identity"]["digest"],
        "request": deepcopy(request),
        "pack": {"manifest_schema": manifest["manifest_schema"], **manifest["pack"],
                 "manifest_digest": manifest["content_identity"]["digest"]},
        "closure": {"archetype_keys": sorted(archetypes), "profile_keys": sorted(profiles),
                    "binding_archetype_keys": sorted(bindings)},
        "environment": deepcopy(environment), "required_execution_contracts": a.REQUIRED_EXECUTION_CONTRACTS[:],
        "catalog_snapshots": [{"catalog": k, "digest": snapshots[k]} for k in CATALOGS],
        "classifications": classifications, "actions": actions,
        "decision_action_ids": [x["action_id"] for x in actions if x["change_kind"] == "update"],
        "blocked_object_keys": blocked,
        "apply_eligible": manifest["pack"]["status"] == "released" and not blocked,
    })
    require(not a.plan_errors(plan) and not a.artifact_size_errors(plan), "invalid_generated_plan", INVALID)
    return plan


def plan_outcome(plan):
    if plan["blocked_object_keys"]:
        return "blocked_desired_state"
    if plan["pack"]["status"] == "draft":
        return "success"
    if plan["decision_action_ids"]:
        return "decision_required_for_drift"
    return "success"


def observe_installation(manifest, request, transport, *, page_size=100):
    """Validate inputs and collect a complete, consistent public observation."""
    manifest_schema = a._schema_document(a.SCHEMA_ROOT / "spine-pack-manifest.v1.schema.json")
    require(not validate_pack(manifest, manifest_schema), "invalid_manifest", PACK_INVALID)
    require(not a.validate_schema(request), "invalid_request_shape", INVALID)
    require(not a.request_errors(request) and not a.artifact_size_errors(request), "invalid_request", INVALID)
    require(manifest["pack"]["status"] != "draft" or request["request"]["draft_posture"] == "inspect_only",
            "draft_inspection_not_allowed", PACK_INVALID)
    selected_definitions(manifest, request["request"])
    require(type(page_size) is int and 1 <= page_size <= 500, "invalid_page_size", INVALID)
    transport.check_target()
    info = transport.read("system.info", {})
    require(isinstance(info, dict) and isinstance(info.get("runtime_version"), str)
            and bool(info["runtime_version"]), "invalid_public_response")
    # Reject a different runtime before interpreting its version-specific payload.
    require(info["runtime_version"] == "0.3.0"
            and info["runtime_version"] in manifest["compatibility"]["spine_runtime_versions"],
            "incompatible_runtime_or_contracts", INCOMPATIBLE)
    validate_readback(info, "systemInfo")
    advertised = info["implemented_contract_versions"]
    require(advertised == sorted(set(advertised)), "contracts_not_canonical")
    require(set(a.REQUIRED_EXECUTION_CONTRACTS + manifest["compatibility"]["spine_content_contracts"]) <= set(advertised)
            and info["implemented_ledger_schema_version"] == info["ledger_schema_version"] == "12",
            "incompatible_runtime_or_contracts", INCOMPATIBLE)
    environment = {"runtime_version": info["runtime_version"],
                   "ledger_schema_implemented": info["implemented_ledger_schema_version"],
                   "ledger_schema_current": info["ledger_schema_version"], "advertised_contracts": advertised}
    owner = request["request"]["owner"]
    catalogs, snapshots = {}, {}
    for catalog in CATALOGS:
        catalogs[catalog], snapshots[catalog] = observe_catalog(transport, catalog, owner, page_size=page_size)
    # Detect changes across catalogs and show calls, including single-page scans.
    for catalog, (command, _, _, kind) in CATALOGS.items():
        query = {"contract_version": FAMILIES[catalog], "owner": owner, "limit": "1"}
        if kind == "binding":
            query["status"] = "active"
        page = transport.read(command + ".list", query)
        validate_readback(page, catalog + "Page")
        require(page["catalog_snapshot_hash"] == snapshots[catalog], "catalog_changed")
        require(page["entries"] == catalogs[catalog][:1]
                and page["count"] == str(len(page["entries"]))
                and page["has_more"] == (len(catalogs[catalog]) > 1)
                and page["has_more"] == (page["next_cursor"] is not None),
                "catalog_recheck_changed")
    transport.check_target()
    return environment, catalogs, snapshots


def plan_installation(manifest, request, transport, *, page_size=100):
    """Validate all inputs before any Spine observation; produce no writes."""
    observation = observe_installation(manifest, request, transport, page_size=page_size)
    return build_plan(manifest, request, *observation)
