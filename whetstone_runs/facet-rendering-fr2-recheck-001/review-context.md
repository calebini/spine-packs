# Exact-source supporting context

Staged 2026-10-17. These excerpts are supporting evidence, not new normative
requirements. Each names its exact Git source and full-source SHA-256. Only
these excerpts, not the omitted full source files, are proposed for transmission.
No client was invoked to prepare them.

## src/spine_packs/artifacts.py

Repository: spine-packs; commit: `be64a9c9c42ed7816caca7b78b68283149044be5`.
Full-source SHA-256: `6a3333f53f89f7fee00f2dafd0ede70ff112271c82b54d0045f11d358aec42d9`.

Lines 95–109:

```text
EXIT_MAP = {
    "success": ("0", None),
    "invalid_cli_or_artifact_input": ("2", "failed"),
    "invalid_pack_contract_or_digest": ("3", "failed"),
    "incompatible_spine_runtime_or_contracts": ("4", "failed"),
    "decision_required_for_drift": ("5", "decision_required"),
    "blocked_desired_state": ("6", "blocked"),
    "stale_plan_or_target_mismatch": ("7", "failed"),
    "spine_command_rejection": ("8", "failed"),
    "partial_apply": ("9", "partial"),
    "verification_mismatch": ("10", "mismatch"),
    "transport_or_environment_failure": ("11", "failed"),
}


```

Lines 128–164:

```text
def canonical_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        raise ValueError("numbers are not allowed")
    if isinstance(value, str):
        pieces = ['"']
        for char in value:
            codepoint = ord(char)
            if 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError("surrogates are not allowed")
            if char == '"':
                pieces.append('\\"')
            elif char == "\\":
                pieces.append("\\\\")
            elif codepoint <= 0x1F:
                pieces.append(f"\\u{codepoint:04x}")
            else:
                pieces.append(char)
        return "".join(pieces) + '"'
    if isinstance(value, list):
        return "[" + ",".join(canonical_text(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_text(key)}:{canonical_text(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise ValueError(f"unsupported canonical value: {type(value).__name__}")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_text(value).encode("utf-8")).hexdigest()

```

Lines 205–218:

```text
def _schema_document(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def _resolve_ref(
    reference: str, current_path: Path, current_schema: dict[str, Any]
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    file_part, marker, fragment = reference.partition("#")
    if file_part:
        target_path = (current_path.parent / file_part).resolve()
        root = _schema_document(target_path)
```

## src/spine_packs/planning.py

Repository: spine-packs; commit: `be64a9c9c42ed7816caca7b78b68283149044be5`.
Full-source SHA-256: `445493754591cb04953b235b6d8bb4ee3e6276d1fb4cf7eb348857a4a2e370ae`.

Lines 14–29:

```text
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
```

## src/spine_packs/__main__.py

Repository: spine-packs; commit: `be64a9c9c42ed7816caca7b78b68283149044be5`.
Full-source SHA-256: `6d9817dbb0b1e9ba7fd2ed1c4ece460e1aeb31ac995ccf20df15f02d9d5c297d`.

Lines 68–83:

```text


def envelope(category, code=None, artifact=None, operation="plan"):
    exit_code, status = a.EXIT_MAP[category]
    return {"artifact_schema": "spine.pack-installer-result.v1", "operation": operation,
            "status": "success" if category == "success" else status, "exit_code": exit_code,
            "artifact": artifact, "error": None if category == "success" else {
                "category": category, "code": code or category,
                "message": "Operation stopped: " + (code or category) + ".", "facts": [],
            }}


def main(argv=None, *, transport_factory=SpineCommand):
    successor = False
    try:
        parser = Parser(prog="spine-packs", description="Local Spine pack plan, approved apply, and read-only verify.")
```

Lines 173–186:

```text
                        if applied["state"] == "partial" else applied["failure"]["error"]["category"])
            result = envelope(category, artifact={"path": args.output,
                "digest": applied["content_identity"]["digest"]}, operation="apply")
    except PlanError as exc:
        result = envelope(exc.category, exc.code, operation=(args.operation if 'args' in locals() else "plan"))
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        # Do not echo arbitrary input, process output, paths, or environment data.
        result = envelope(INVALID, "invalid_contract_value", operation=(args.operation if 'args' in locals() else "plan"))
    except OSError:
        result = envelope(ENVIRONMENT, "local_environment_failure", operation=(args.operation if 'args' in locals() else "plan"))
    if successor:
        result['artifact_schema'] = 'spine.pack-installer-result.v2'
    print(a.canonical_text(result))
    return int(result["exit_code"])
```

## src/spine_packs/spine_command.py

Repository: spine-packs; commit: `be64a9c9c42ed7816caca7b78b68283149044be5`.
Full-source SHA-256: `00c0c445b82a25ba74d024fd2f75a13b5206c71bef4db8de38ba1e93a0ba1a24`.

Lines 94–169:

```text
                                       stderr=subprocess.DEVNULL, shell=False)
            output = bytearray()
            deadline = time.monotonic() + self.timeout
            os.set_blocking(process.stdin.fileno(), False)
            written = 0
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                selector.register(process.stdin, selectors.EVENT_WRITE)
                while selector.get_map():
                    remaining = deadline - time.monotonic()
                    require(remaining > 0, "spine_timeout")
                    for key, _ in selector.select(min(remaining, 0.2)):
                        if key.fileobj is process.stdin:
                            written += os.write(key.fd, data[written:written + 4096])
                            if written == len(data):
                                selector.unregister(process.stdin)
                                process.stdin.close()
                            continue
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                        else:
                            output.extend(chunk)
                            require(len(output) <= RESPONSE_LIMIT, "spine_response_too_large")
                            self._received(chunk)
            returncode = process.wait(timeout=max(0.01, deadline - time.monotonic()))
            response = a.parse_json(bytes(output), public_response=True)
            require(isinstance(response, dict), "invalid_public_response")
            return response, returncode
        except (OSError, ValueError, RecursionError, subprocess.TimeoutExpired) as exc:
            raise PlanError(ENVIRONMENT, "spine_transport_failed") from exc
        finally:
            if process is not None:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                if process.stdout is not None:
                    process.stdout.close()
                if process.stdin is not None and not process.stdin.closed:
                    process.stdin.close()

    def _command_arguments(self, command):
        return [command]

    def _received(self, chunk):
        """Optional stricter observation budget; v1 retains its existing ceiling."""
```

## specs/architecture.md

Repository: spine-packs; commit: `be64a9c9c42ed7816caca7b78b68283149044be5`.
Full-source SHA-256: `020ef8d0b7c0777e7177a1024f85927ed2aab158f1dd6c8a4d9909227e8fdf24`.

Lines 1–38:

```text
# Architecture

## Facet/rendering successor — FR-2 read-only planning

[facet-rendering-packs.md](facet-rendering-packs.md) proposes a separate manifest
and installer-artifact v2 path for exact Spine `0.10.0` / schema `19` at
`8f3c50b6fd1b4aa534e50925b7417a7a80d19122`. It adds a bounded configuration graph:
archetype and facet schema -> facet binding -> rendering definition -> profile
revision -> default binding. The proposal does not expand the runtime authority
or compatibility of the implemented slices below. No disclosure authorization,
item authoring, scheduling or sending belongs to that graph. Read its review
gates before successor work; old v1 behavior and released artifacts remain intact.

The draft successor machine layer is specified in
[installer-artifacts-v2.md](installer-artifacts-v2.md). Its pure test oracle lives
under `tests/contract/`, not `src/spine_packs/`. Saved synthetic execution and
recovery fixtures are not results from an implemented successor installer.

## Relationship

FR-2 adds `facet_manifest`, `facet_graph`, `facet_contracts`, `facet_inventory`,
`facet_observation`, `facet_transport` and `facet_planning` in the existing package.
They implement only manifest-v2/request-v2 read-only `plan`. The CLI uses the
same selection assertions and private no-clobber output publication; successor
apply/continuation/verify are rejected before target access. V1 dispatch and
supported-baseline allowlists are unchanged. Proposed write templates are data,
not executable authority; the successor transport rejects every write.

The bounded pinned-vocabulary validator is independent of the frozen v1 decoder
and cross-checked with official Draft 2020-12 in development. Unknown vocabulary
fails closed. Offline sibling schema references supply the complete transitive
closure without runtime dependencies or network schema resolution.

`scripts/qualify_fr2.py` is isolated test setup, not installer apply. It accepts
no existing ledger, attests exported/wheel/installed Spine bytes against the
exact Git tree, and exercises synthetic configuration through public CLIs only.
This narrow gate does not complete FR-5 or authorize release/installation.

```

## Minimum public ID shape

Source: `contracts/schemas/spine-readback-0.9.1.schema.json`, Spine Packs commit
`be64a9c9c42ed7816caca7b78b68283149044be5`; full-source SHA-256 `90471d1674233e7b3d47575adf085c4095ddfecc92f1f2e7833f4be56d7d4204`.
The supplied 0.10.0 closure aliases these unchanged definitions; this is not
permission to plan against runtime 0.9.1.

```json
{
  "public_0056": {
    "$ref": "#/$defs/public_0002"
  },
  "public_0002": {
    "type": "string",
    "minLength": 1
  }
}
```

## specs/facet-schema-revision-readback.md

Repository: spine; commit: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`.
Full-source SHA-256: `be263114ca40f397f392acabce7f5a8b1d10b32ab44692cd9275d67190a88ca6`.

Lines 128–170:

```text
Keep normal database/runtime preflight before handler execution. Handler ordering is
closed request shape, exact selector, ID validity, exact revision resolution,
root/invariant/definition validation, then complete result release. Capacity checks
may fail any stage; never reset budgets or retry through alternative roots.

For a parsed request object, shape validation MUST report exactly one error in
this order, independent of JSON member order or a validator's error iteration:

1. If any key is not an allowed request field, return `unsupported_field` for
   the lexicographically smallest extra field, **before** checking missing fields.
2. Otherwise, if a required key is absent, return `missing_required_field` for
   the lexicographically smallest missing field.
3. Only after both shape checks pass, check the exact `contract_version`, then
   the validity of `facet_schema_revision_id`, then perform revision resolution.

Field-name comparison is case-sensitive Unicode code-point lexicographic order;
do not normalize, case-fold or use locale ordering. Presence means key existence,
even if the value is null or the wrong type. Thus `{}` reports missing
`contract_version`; `{unexpected:null}` reports unsupported `unexpected`, not a
missing field. A missing revision key wins over an invalid selector, while an
invalid selector wins over an invalid revision ID when both keys are present.
These are command error-selection rules, not JSON Schema keyword-order semantics.

| Condition | error.code | error.field | CLI exit |
| --- | --- | --- | --- |
| Required request field absent | missing_required_field | Missing field | 2 |
| Extra request field | unsupported_field | Extra field | 2 |
| Selector not exactly supported | unsupported_contract_version | contract_version | 2 |
| Empty/non-string/invalid-Unicode revision ID | invalid_request | facet_schema_revision_id | 2 |
| Exact revision absent | referenced_row_not_found | facet_schema_revision_id | 4 |
| Broken root membership, missing stored root, corrupt hash/definition/declaration parity or unsupported historical decoder | environment_failure | facets | 7 |
| Resource, SQL-step, wall-clock, lock or handler byte budget exhausted | environment_failure | capacity | 7 |

Malformed transport JSON and routine preflight failures retain the existing owning
contracts; this leaf does not reclassify them as an absent revision. The
[failure schema](../contracts/schemas/facet-schema-revision-show-failure.schema.json)
covers normalized command handler outcomes, not all transport diagnostics.

Failure messages are safe explanatory prose, not byte-exact constants. Do not echo
revision/root IDs, owners or definition content in errors. No missing-revision
failure proves that a whole catalog lacks a desired schema. Capacity/corruption/
preflight failures are never not-found evidence. Existing `facet_schema.show`
membership-mismatch failures and missing/inaccessible protections stay unchanged.
```

## specs/agent-command-contract.md

Repository: spine; commit: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`.
Full-source SHA-256: `17d73f1c0292517711b10d4b25069912ad3c4f9270d395e44a274bc02de69afd`.

Lines 273–304:

```text

The trusted-local facet rows additionally require the exact owning family in
`contracts/archetype-facet-contract-registry.v1.json`. The three paginated reads
also require `spine.facet-cursor.v1`; `item.facets.update` additionally requires
`spine.facet-notification-continuity.v1`. Every row retains the common canonical-JSON
requirement. Their compiled mapping is `commands/registry.py`; none is a web allowlist entry.

The schema-19 registry retains the prior family requirements and adds:

| Commands | Additional exact local versions |
| --- | --- |
| Definition create/publish/retire/show | `spine.notification-rendering-definitions.v1` |
| Definition list | `spine.notification-rendering-definitions.v1`, `spine.notification-rendering-cursor.v1` |
| Disclosure provision/revoke/show | `spine.notification-rendering-disclosures.v1` |
| Disclosure list | `spine.notification-rendering-disclosures.v1`, `spine.notification-rendering-cursor.v1` |
| `notification_profile.create/revise/show/list` | `spine.notification-profiles.v2` |
| `schedule.create` | `spine.schedule-create.v3`, `spine.schedule-create-response.v3`, `spine.schedule-create-receipt.v3`, `spine.notification-profile-application.v2` |
| `schedule.update` | `spine.schedule-update.v3`, `spine.schedule-update-response.v3`, `spine.schedule-update-receipt.v3`, `spine.notification-profile-application.v2` |
| `schedule.show` | `spine.schedule-show.v2`, `spine.notification-profile-readback.v2`, `spine.notification-rendering.v2` |
| `reminder.create/edit` | `spine.notification-schedule-authoring.v2` |

Every compiled command row additionally requires `spine.notification-rendering-integration.v1`.
The registry's dependency union does not change an omitted selector or authorize a
new HTTP payload. Frozen web registries retain their exact pre-existing family pins;
only the enumerated local rendering additions are excluded when comparing those pins,
and runtime admission still requires the complete compiled union to be implemented.

### 5.3 Schema-Object Manifest

The authority for expected SQLite objects is one immutable compiled manifest with identity `spine.sqlite-schema-object-manifest.v1`, keyed by the exact decimal `ledger_schema` version. The current runtime contains exactly one entry for its implemented schema version. Each manifest object contains `object_type` (`table`, `index`, or `trigger`), exact case-sensitive `name`, and `definition_sha256`. `definition_sha256` is lowercase SHA-256 over the UTF-8 bytes of the non-null `sqlite_schema.sql` value exactly as stored by the canonical completed migration path, with no whitespace, case, comment, or quoting normalization. Objects whose SQLite definition is engine-generated with `sql IS NULL`, including `sqlite_autoindex_*`, MUST NOT appear as required manifest objects.

The manifest MUST be generated or reviewed from the same canonical schema and ordered migration corpus shipped by the runtime, checked in or compiled with that runtime, and covered by tests proving that both fresh initialization and every supported migration path produce the same manifest fingerprints on every supported SQLite runtime. It is not derived from the target ledger at startup. Routine preflight reads only the `sqlite_schema` rows for the constant-size required manifest and compares exact object type, name, and definition fingerprint. Required objects are ordered for comparison and diagnostics by `object_type`, then `name`.
```

## src/spine/commands/cli.py

Repository: spine; commit: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`.
Full-source SHA-256: `2fd9f80f36ac16d6b4d79a4263a8e243e0a3b24f82c843353f2084bc830815ab`.

Lines 21–42:

```text
EXIT_BY_ERROR = {
    "invalid_request": 2,
    "unsupported_command": 2,
    "unsupported_field": 2,
    "missing_required_field": 2,
    "invalid_timestamp": 2,
    "wrong_item_type": 2,
    "invalid_state_transition": 2,
    "referenced_row_not_found": 4,
    "stale_version": 5,
    "semantic_conflict": 6,
    "stale_cursor": 6,
    "environment_failure": 7,
    "facet_schema_invalid": 2,
    "facet_value_invalid": 2,
    "facet_binding_conflict": 6,
    "facet_archetype_conflict": 6,
    "facet_schema_retired": 2,
    "facet_reference_unavailable": 4,
    "unsupported_contract_version": 2,
    "rendering_definition_invalid": 2,
    "rendering_definition_retired": 2,
```

Lines 60–83:

```text
    if command not in MVP_COMMANDS:
        response = {"ok": False, "error": {"code": "unsupported_command", "message": f"unsupported command: {command}", "field": "command"}}
        if _is_dotted_command(command):
            response["command"] = command
        _dump(response, pretty=args.pretty)
        return 2
    missing_contracts = missing_runtime_contract_versions(command)
    if missing_contracts:
        _dump(
            {
                "ok": False,
                "command": command,
                "error": {
                    "code": "environment_failure",
                    "message": f"missing required runtime contracts: {', '.join(missing_contracts)}",
                    "field": "runtime_contracts",
                },
            },
            pretty=args.pretty,
        )
        return 7
    if args.if_absent and command != "reminder.create":
        _dump(
            {
```

Lines 182–238:

```text
    except SpineValidationError as exc:
        code, _, field = exc.code.partition(":")
        _dump(
            {
                "ok": False,
                "command": command,
                "error": {"code": code, "message": exc.message, "field": field or "request"},
                **({"dry_run": True} if args.dry_run and command in FACET_COMMANDS else {}),
            },
            pretty=args.pretty,
        )
        return EXIT_BY_ERROR.get(code, 2)
    except CliPreflightError as exc:
        _dump(
            {
                "ok": False,
                "command": command,
                "error": {"code": exc.code, "message": exc.message, "field": exc.field},
                **({"dry_run": True} if args.dry_run and command in FACET_COMMANDS else {}),
            },
            pretty=args.pretty,
        )
        return 3
    try:
        context = CommandContext(
            ledger=connection,
            ledger_path=str(Path(args.db).expanduser()),
            dry_run=args.dry_run,
            transport_metadata={"adapter": "cli"},
            adapter_bindings=_adapter_bindings(args),
            delivery_target_defaults=delivery_target_defaults,
            facet_cursor_config=cursor_config,
            rendering_cursor_config=rendering_cursor_config,
        )
        response = handle(command, request, context)
        if args.compact and response.get("ok") is True:
            response = compact_schedule_response(response)
    except Exception as exc:  # pragma: no cover - final transport fallback
        response = {"ok": False, "command": command, "error": {"code": "runtime_failure", "message": str(exc)}}
    finally:
        connection.close()
    _dump(response, pretty=args.pretty)
    if response.get("ok") is True:
        return 0
    error = response.get("error")
    code = error.get("code") if isinstance(error, Mapping) else "runtime_failure"
    return EXIT_BY_ERROR.get(str(code), 1)


class CliPreflightError(Exception):
    def __init__(self, code: str, message: str, field: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field


```

Lines 321–374:

```text
def _load_request(input_ref: str, *, facet: bool = False, rendering: bool = False) -> dict[str, Any]:
    try:
        if facet or rendering:
            maximum = 32768 if rendering else 1024 * 1024
            family = "rendering" if rendering else "facet"
            if input_ref == "-":
                text = sys.stdin.read(maximum + 1)
            else:
                with Path(input_ref).open(encoding="utf-8") as stream:
                    text = stream.read(maximum + 1)
            from spine.core.facets import parse_object

            if len(text.encode("utf-8")) > maximum:
                raise SpineValidationError("environment_failure:capacity", f"{family} request capacity exceeded")
            try:
                return parse_object(text or "{}", maximum=maximum)
            except SpineValidationError as exc:
                raise SpineValidationError("invalid_request:request", f"invalid {family} request JSON") from exc
        text = sys.stdin.read() if input_ref == "-" else Path(input_ref).read_text(encoding="utf-8")
    except OSError as exc:
        raise CliPreflightError("invalid_request", str(exc), "input") from exc
    try:
        value = json.loads(text or "{}")
    except json.JSONDecodeError as exc:
        raise CliPreflightError("invalid_request", str(exc), "input") from exc
    if not isinstance(value, dict):
        raise CliPreflightError("invalid_request", "input JSON must be an object", "input")
    return value


def _open_ledger(db: str, *, writable: bool):
    path = Path(db).expanduser()
    if not path.exists():
        raise CliPreflightError("invalid_request", "ledger database does not exist", "db")
    if writable:
        if not os.access(path, os.W_OK) or not os.access(path.parent, os.W_OK):
            raise CliPreflightError("invalid_request", "ledger database is not writable", "db")
    else:
        if not os.access(path, os.R_OK):
            raise CliPreflightError("invalid_request", "ledger database is not readable", "db")
    connection = connect(path)
    try:
        verify_runtime_schema(connection)
    except Exception as exc:
        connection.close()
        raise CliPreflightError("invalid_request", str(exc), "db") from exc
    return connection


def _adapter_bindings(args: argparse.Namespace) -> dict[str, object]:
    if not args.openclaw_whatsapp:
        return {}
    return {"openclaw": {"binding_name": "openclaw", "channel": "whatsapp", "configured": True}}

```

## src/spine/commands/core.py

Repository: spine; commit: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`.
Full-source SHA-256: `dc48336e009795ca070eef32a1a47b888c02eaf09d00b6d84cadd02965116c23`.

Lines 115–133:

```text
def handle(command: str, request: Mapping[str, Any], context: CommandContext) -> dict[str, Any]:
    """Dispatch the MVP command-core interface."""

    if command not in MVP_COMMANDS:
        return _error(command, "unsupported_command", f"unsupported command: {command}", "command")
    if not isinstance(request, Mapping):
        return _error(command, "invalid_request", "request must be a JSON object", "request")
    if context.ledger is None:
        return _error(command, "invalid_request", f"{command} requires CommandContext.ledger", "ledger")
    try:
        from spine.commands import rendering_candidate
        if rendering_candidate.accepts(command, request):
            return rendering_candidate.execute(command, request, context, cursor_config=context.rendering_cursor_config)
        from spine.commands.facets import CONTRACTS as FACET_COMMANDS
        from spine.commands.facets import execute as execute_facet
        if command in FACET_COMMANDS:
            return execute_facet(command, request, context)
        if context.dry_run and command in WRITE_COMMANDS:
            preview = sqlite3.connect(":memory:", factory=LedgerConnection)
```

Lines 174–196:

```text
    db = context.ledger
    # Web admission and provisioning already own their outer boundary. All ordinary
    # CLI writes now absorb helper contexts, including the receipt after item creation.
    # Owner discovery uses a nested read savepoint; give it an explicit outer
    # read transaction so RELEASE cannot become an unfinalized outer commit.
    if (command not in WRITE_COMMANDS and command != "owner_scope.list" or command == "web_access.apply"
            or isinstance(db, LedgerConnection) and db._command_transaction):
        return _dispatch(command, request, context)
    if not isinstance(db, LedgerConnection):
        raise SpineValidationError("environment_failure:ledger", "transaction-aware ledger connection required")
    if db.in_transaction:
        raise SpineValidationError("environment_failure:ledger", "command requires an idle connection or owned transaction")
    try:
        with db.atomic_command(write=command in WRITE_COMMANDS):
            result = _dispatch(command, request, context)
            if not result.get("ok"):
                raise _CommandRejected(result)
            return result
    except _CommandRejected as exc:
        return exc.result
    except sqlite3.OperationalError as exc:
        raise SpineValidationError("environment_failure:ledger", "ledger transaction could not complete") from exc

```

## src/spine/commands/facets.py

Repository: spine; commit: `8f3c50b6fd1b4aa534e50925b7417a7a80d19122`.
Full-source SHA-256: `7245a364ffdcd4f8334183b555b923fc11e15b5b2a52d531cda527fc958113d6`.

Lines 138–148:

```text
def execute(command: str, request: Mapping[str, Any], context: CommandContext) -> dict[str, Any]:
    if command == "facet_schema.revision.show":
        from spine.commands.facet_revision_readback import execute as revision_readback

        return revision_readback(request, context)
    db = context.ledger
    if not isinstance(db, LedgerConnection) or db.in_transaction or db._command_transaction:
        failure("environment_failure", "ledger", "facet commands require an idle transaction-aware ledger")
    assert isinstance(db, LedgerConnection)
    if context.transport_metadata.get("adapter") not in {None, "cli"}:
        failure("environment_failure", "admission", "use trusted-local admission or the dedicated facet web adapter")
```
