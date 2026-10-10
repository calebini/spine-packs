# Exact-baseline profile-list source conflict

Pinned source: `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`.
This is a source inspection inference, not an executed public-CLI regression.
The v2 profile list calls the shared legacy list; that list rejects stored v2
revisions before the caller can project them to v2. A separate disposable
public-CLI reproduction is a gate; no source repair or baseline change is authorized.

The snippets also show v2 request normalization before receipt-producing dispatch.
They are supplied for review only, not an installer internal-API interface.

## src/spine/commands/rendering_candidate.py

Full source SHA-256: `14363914ea733ec9ef9b9b1377b34d1573742050198f8ecfa807aaf4589e400e`

Lines 22–49:

```text
22: def accepts(command, request):
23:     if command.startswith(("notification_rendering_definition.", "notification_rendering_disclosure.")):
24:         return True
25:     selector = request.get("contract_version")
26:     if command in {"notification_profile.create", "notification_profile.revise", "notification_profile.show", "notification_profile.list"}:
27:         return selector == codec.PROFILE_V2
28:     if command in {"schedule.create", "schedule.update"}:
29:         return selector == ("spine.schedule-create.v3" if command.endswith("create") else "spine.schedule-update.v3")
30:     if command in {"reminder.create", "reminder.edit"}:
31:         patch = request.get("patch")
32:         notification = (
33:             request.get("notification") if command.endswith("create") else (patch.get("notification") if isinstance(patch, dict) else None)
34:         )
35:         return isinstance(notification, dict) and notification.get("authoring_contract") == "spine.notification-schedule-authoring.v2"
36:     return False
37:
38:
39: def normalized_request(command, request):
40:     value = copy.deepcopy(dict(request))
41:     codec.bounded(value, 32768, "request")
42:     if command in {"notification_profile.create", "notification_profile.revise"}:
43:         revision = codec.normalize_profile_v2(value.get("revision"))
44:         value["revision"] = {
45:             "compatible_item_types": list(revision.compatible_item_types),
46:             "templates": [{k: v for k, v in template.items() if k != "normalized_template_hash"} for template in revision.templates],
47:         }
48:     patch = value.get("patch", {})
49:     if not isinstance(patch, dict):
```

Lines 72–89:

```text
72: def execute(command, request, context, *, admission=None, cursor_config=None, now=None):
73:     db = context.ledger
74:     admission = admission or RenderingAdmission()
75:     timestamp = now or wire_time(utc_now())
76:     try:
77:         invariant(getattr(db, "_renderings_enabled", False) and not db.in_transaction, "candidate storage is required")
78:         if command.startswith(("notification_rendering_definition.", "notification_rendering_disclosure.")):
79:             return rendering_catalog.execute(command, request, context, admission=admission, cursor_config=cursor_config, now=timestamp)
80:         value = normalized_request(command, request)
81:         if command.startswith("notification_profile."):
82:             budget = FacetBudget()
83:             old_timeout = install_budget(db, budget)
84:             try:
85:                 return rendering_profiles.execute(command, value, context, admission=admission, now=timestamp, budget=budget)
86:             finally:
87:                 db.set_progress_handler(None, 0)
88:                 db.execute(f"PRAGMA busy_timeout={old_timeout}")
89:         handlers = {
```

## src/spine/commands/rendering_profiles.py

Full source SHA-256: `9facbbac4fc237d7eb8344c97c622a48be97e5d7ff099eae7d0e8179c605b53d`

Lines 118–133:

```text
118:                 "notification_profile": project(
119:                     load_profile(db, request["notification_profile_id"], revision_id=request.get("notification_profile_revision_id"))
120:                 ),
121:             }
122:         elif command == "notification_profile.list":
123:             # Preserve the profile family's fixed 1..500, snapshot/key cursor semantics.
124:             old = dict(request, contract_version="spine.notification-profiles.v1")
125:             if permissions and not permissions.scope(codec.owner(request["owner"])):
126:                 codec.fail("permission_denied", "owner")
127:             result = shared._list_roots(old, context, kind="notification_profile")
128:             result["response_contract"] = codec.PROFILE_V2
129:             result["entries"] = [project(load_profile(db, r["notification_profile_id"])) for r in result["entries"]]
130:         else:
131:             codec.fail("invalid_request", "command")
132:         codec.bounded(result, 4 * 1024 * 1024, "capacity")
133:     return result | ({"dry_run": True} if context.dry_run else {})
```

## src/spine/commands/notification_profiles.py

Full source SHA-256: `d33c9b0d51e6c1758a311551d2695cfe6d63cf246a5bce373b86ebd1293797a4`

Lines 818–825:

```text
818: def _legacy_profile(entry):
819:     """A frozen v1 full projection cannot label successor content as v1."""
820:     revision = entry["revision"]
821:     if revision.get("revision_contract") == "spine.notification-profiles.v2":
822:         raise SpineValidationError("unsupported_contract_version:contract_version", "use spine.notification-profiles.v2 for this revision")
823:     revision.pop("revision_contract", None)
824:     return entry
825:
```

Lines 912–932:

```text
912:             row
913:             for row in rows
914:             if (str(row[key_field]), str(row[id_field])) > last
915:         ]
916:     has_more = len(rows) > limit
917:     page = rows[:limit]
918:     loader = load_archetype if kind == "item_archetype" else load_profile
919:     entries = [
920:         loader(connection, str(row[id_field]))
921:         for row in page
922:     ]
923:     if kind == "notification_profile":
924:         entries = [_legacy_profile(entry) for entry in entries]
925:     next_cursor = None
926:     if has_more and page:
927:         final = page[-1]
928:         next_cursor = _encode_catalog_cursor(
929:             {
930:                 "cursor_version": "spine.notification-profile-catalog-cursor.v1",
931:                 "query": query_facts,
932:                 "snapshot_hash": snapshot_hash,
```

