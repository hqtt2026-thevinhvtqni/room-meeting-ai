from __future__ import annotations

import json
import os
import secrets
import sys
from dataclasses import asdict, is_dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent_runtime import AgentRuntime
from browser_adapter import PlaywrightBrowserAdapter
from execution_coordinator import ExecutionCoordinator
from models import Action, ActionValidationError

PORT = int(os.getenv("COMPUTER_AGENT_PORT", "8787"))
HEADLESS = os.getenv("COMPUTER_AGENT_HEADLESS", "0") == "1"
MAX_BODY_BYTES = int(os.getenv("COMPUTER_AGENT_MAX_BODY_BYTES", str(1024 * 1024)))
MAX_ACTIONS = int(os.getenv("COMPUTER_AGENT_MAX_ACTIONS", "100"))
EXECUTION_COORDINATOR = ExecutionCoordinator()


def build_adapter():
    return PlaywrightBrowserAdapter(HEADLESS)


def _allowed_origins() -> set[str]:
    return {
        value.strip()
        for value in os.getenv("COMPUTER_AGENT_ALLOWED_ORIGINS", "").split(",")
        if value.strip()
    }


def _configured_token() -> str:
    return os.getenv("COMPUTER_AGENT_TOKEN", "")


def _json_default(value):
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "__dict__"):
        return value.__dict__
    return str(value)


class Handler(BaseHTTPRequestHandler):
    server_version = "computer-agent/1.2.0"

    def _send(self, status: int, payload: dict, origin: str | None = None) -> None:
        raw = b"" if status == 204 else json.dumps(
            payload, ensure_ascii=False, default=_json_default
        ).encode("utf-8")
        self.send_response(status)
        if status != 204:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        if origin and origin in _allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def log_message(self, format, *args):
        if os.getenv("COMPUTER_AGENT_VERBOSE") == "1":
            super().log_message(format, *args)

    def _origin_check(self) -> bool:
        origin = self.headers.get("Origin")
        # Non-browser clients may omit Origin, but must still authenticate.
        return origin is None or origin in _allowed_origins()

    def _authorized(self) -> bool:
        expected = _configured_token()
        supplied = self.headers.get("Authorization", "")
        if not expected or not supplied.startswith("Bearer "):
            return False
        candidate = supplied[7:]
        return bool(candidate) and secrets.compare_digest(candidate, expected)

    def _reject_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not self._origin_check():
            self._send(403, {"status": "BLOCKED", "error": "origin_not_allowed"})
            return True
        return False

    def do_OPTIONS(self):
        origin = self.headers.get("Origin")
        if not origin or origin not in _allowed_origins():
            return self._send(403, {"status": "BLOCKED", "error": "origin_not_allowed"})
        method = self.headers.get("Access-Control-Request-Method", "").upper()
        requested_headers = {
            item.strip().lower()
            for item in self.headers.get("Access-Control-Request-Headers", "").split(",")
            if item.strip()
        }
        if method != "POST" or not requested_headers.issubset({"authorization", "content-type"}):
            return self._send(403, {"status": "BLOCKED", "error": "preflight_not_allowed"})
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Max-Age", "300")
        self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self):
        if self.path != "/health":
            return self._send(404, {"status": "FAIL", "error": "not_found"})
        if self._reject_origin():
            return
        return self._send(200, {
            "status": "ok",
            "service": "computer-agent",
            "version": self.server_version.rsplit("/", 1)[-1],
            "port": PORT,
            "execution_busy": EXECUTION_COORDINATOR.busy,
        }, self.headers.get("Origin"))

    def _read_request(self):
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            raise ValueError("content_type_must_be_application_json")
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("content_length_required")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("invalid_content_length") from exc
        if length <= 0:
            raise ValueError("empty_body")
        if length > MAX_BODY_BYTES:
            raise OverflowError("request_body_too_large")
        raw = self.rfile.read(length)
        if len(raw) != length:
            raise ValueError("incomplete_request_body")
        try:
            body = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid_json") from exc
        if not isinstance(body, dict):
            raise ValueError("request_body_must_be_object")
        if set(body) - {"task", "actions", "verification"}:
            raise ValueError("unknown_request_fields")
        task = body.get("task")
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task_must_be_non_empty_string")
        raw_actions = body.get("actions")
        if not isinstance(raw_actions, list):
            raise ValueError("actions_must_be_list")
        if len(raw_actions) > MAX_ACTIONS:
            raise OverflowError("too_many_actions")
        if any(not isinstance(item, dict) for item in raw_actions):
            raise ValueError("each_action_must_be_object")
        verification = body.get("verification")
        if verification is not None:
            if not isinstance(verification, dict):
                raise ValueError("verification_must_be_object")
            checks = verification.get("checks")
            if not isinstance(checks, list) or not checks:
                raise ValueError("verification_checks_must_be_non_empty_list")
            for check in checks:
                if not isinstance(check, dict):
                    raise ValueError("each_verification_check_must_be_object")
                if not isinstance(check.get("field"), str) or not check["field"].strip():
                    raise ValueError("verification_check_field_required")
                if check.get("contains") in (None, ""):
                    raise ValueError("verification_check_contains_required")
        actions = [Action(**item) for item in raw_actions]
        return task, actions, verification

    def do_POST(self):
        if self.path != "/agent/execute":
            return self._send(404, {"status": "FAIL", "error": "not_found"})
        if self._reject_origin():
            return
        if not self._authorized():
            return self._send(401, {"status": "BLOCKED", "error": "unauthorized"})
        try:
            task, actions, verification = self._read_request()
        except OverflowError as exc:
            return self._send(413, {"status": "BLOCKED", "error": str(exc)}, self.headers.get("Origin"))
        except (ValueError, TypeError, ActionValidationError) as exc:
            return self._send(400, {"status": "FAIL", "error": str(exc)}, self.headers.get("Origin"))

        # Acquire before constructing an adapter. A busy service never starts a
        # second browser/session and never dispatches a second action concurrently.
        if not EXECUTION_COORDINATOR.try_acquire():
            return self._send(409, {
                "status": "BLOCKED",
                "error": "execution_busy",
                "message": "Another execution still owns the process-wide browser lease",
            }, self.headers.get("Origin"))

        adapter = None
        result = None
        failure = None
        try:
            adapter = build_adapter()
            result = AgentRuntime(adapter).execute(task, actions, verification)
        except Exception as exc:
            failure = f"{type(exc).__name__}: {exc}"
        finally:
            try:
                if adapter is not None:
                    adapter.close()
            except Exception as exc:
                failure = f"adapter_close_failed: {type(exc).__name__}: {exc}"
            finally:
                EXECUTION_COORDINATOR.release()

        # Do not report PASS until adapter shutdown has also completed.
        if failure:
            return self._send(500, {
                "status": "FAIL",
                "error": failure,
            }, self.headers.get("Origin"))
        code = 200 if result.status == "PASS" else 409
        return self._send(code, result.__dict__, self.headers.get("Origin"))


def serve(port: int = PORT, host: str = "127.0.0.1") -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = serve()
    actual_port = server.server_address[1]
    print(f"Computer Agent API listening on 127.0.0.1:{actual_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        sys.exit(0)
