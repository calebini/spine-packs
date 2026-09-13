"""Local process adapter for the pinned Spine 0.3.0 command surface."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import selectors
import socket
import subprocess
import time
import re

from . import artifacts as a
from .planning import CATALOGS, ENVIRONMENT, PlanError, require, validate_readback


READ_COMMANDS = frozenset({"system.info", "item_archetype.list", "item_archetype.show",
                           "notification_profile.list", "notification_profile.show",
                           "notification_profile.binding.list"})
WRITE_COMMANDS = frozenset(a.COMMAND_SHAPES)
RESPONSE_LIMIT = 16 * 1024 * 1024


class SpineCommand:
    """Only this adapter may spawn Spine. It never opens the ledger itself."""
    def __init__(self, target, *, timeout=30, host_resolver=socket.getfqdn):
        self.target = target
        self.timeout = timeout
        self.host_resolver = host_resolver

    def check_target(self):
        try:
            host = self.host_resolver().lower().removesuffix(".")
            require(host.isascii() and "." in host and ".." not in host,
                    "target_host_unresolved")
            executable = Path(self.target["spine_command"]["path"]).resolve(strict=True)
            ledger = Path(self.target["ledger"]["path"]).resolve(strict=True)
            require(executable.is_file() and ledger.is_file() and os.access(executable, os.X_OK),
                    "target_unavailable")
            with executable.open("rb") as handle:
                sha = hashlib.file_digest(handle, "sha256").hexdigest()
            observed = {"host_name": host, "spine_command": {"path": str(executable), "sha256": sha},
                        "ledger": {"kind": "path", "path": str(ledger)}}
            require(observed == self.target, "target_binding_mismatch", "stale_plan_or_target_mismatch")
        except OSError as exc:
            raise PlanError(ENVIRONMENT, "target_unavailable") from exc

    def read(self, command, request):
        # A write name is rejected before target inspection or process creation.
        require(command in READ_COMMANDS, "read_only_command_required")
        if command == "system.info":
            require(request == {}, "invalid_read_request")
        else:
            catalog = next(k for k, v in CATALOGS.items() if command.startswith(v[0] + ".")
                           and (k == "bindings") == command.startswith("notification_profile.binding."))
            validate_readback(request, catalog + ("ListRequest" if command.endswith(".list") else "ShowRequest"))
        response, returncode = self._invoke(command, request)
        if response.get("ok") is False:
            validate_readback(response, "commandFailure")
            require(response["command"] == command, "response_command_mismatch")
            raise PlanError("spine_command_rejection", "spine_read_rejected")
        # Read failure never becomes a missing/retained object or an applicable plan.
        require(returncode == 0 and response.get("ok") is True, "spine_read_failed")
        require(response.get("command") == command, "response_command_mismatch")
        return response

    def write(self, command, request):
        require(command in WRITE_COMMANDS, "write_command_not_allowed")
        prefix, contract = a.COMMAND_SHAPES[command]
        value = a.canonical_value(contract, request, prefix + "Request")
        require(not a.canonical_value_errors(value, prefix + "Request"), "invalid_write_request")
        response, returncode = self._invoke(command, request)
        if response.get("ok") is False:
            validate_readback(response, "commandFailure")
            require(response.get("command") == command, "response_command_mismatch")
            # Keep only the public machine error code, never its arbitrary message.
            code = response["error"]["code"]
            require(re.fullmatch(r"[a-z][a-z0-9_.:-]{0,159}", code) is not None, "invalid_spine_error_code")
            error = PlanError("spine_command_rejection", "spine_write_rejected")
            error.facts = [{"name": "spine_error_code", "value": code}]
            raise error
        require(returncode == 0 and response.get("ok") is True, "spine_write_failed", ENVIRONMENT)
        require(response.get("command") == command, "response_command_mismatch", ENVIRONMENT)
        return response

    def _invoke(self, command, request):
        self.check_target()
        argv = [self.target["spine_command"]["path"], "--db", self.target["ledger"]["path"],
                command, "--input", "-"]
        data = (a.canonical_text(request) + "\n").encode("utf-8")
        process = None
        try:
            process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
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
