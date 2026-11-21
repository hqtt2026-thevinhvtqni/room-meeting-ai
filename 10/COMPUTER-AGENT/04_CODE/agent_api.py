from __future__ import annotations

import importlib
import hmac
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent_runtime import AgentRuntime
from models import Action, ActionValidationError, SafetyPolicy

PORT = int(os.getenv("COMPUTER_AGENT_PORT", "8787"))
HEADLESS = os.getenv("COMPUTER_AGENT_HEADLESS", "0") == "1"
WORK_ID = os.getenv("COMPUTER_AGENT_WORK_ID", "10")
SERVICE_VERSION = "1.3.0"

# One process-wide browser lease. ThreadingHTTPServer can receive concurrent
# requests; never allow a second request to dispatch while a timed-out worker
# from the first request may still touch the shared browser/adapter lifecycle.
_EXECUTION_LOCK = threading.Lock()


def allowed_origins() -> set[str]:
    raw = os.getenv("COMPUTER_AGENT_ALLOWED_ORIGINS", "http://127.0.0.1:3000")
    return {item.strip() for item in raw.split(",") if item.strip()}


def request_token() -> str:
    return os.getenv("COMPUTER_AGENT_API_TOKEN", "")


def build_policy() -> SafetyPolicy:
    """Server-side policy. A client can never grant itself destructive rights:
    only this process environment can, per SAFETY_POLICY §4."""
    prefix_raw = os.getenv("COMPUTER_AGENT_ALLOWED_PATHS", "06_EVIDENCE")
    domain_raw = os.getenv("COMPUTER_AGENT_ALLOWED_DOMAINS", "").strip()
    return SafetyPolicy(
        allow_destructive=os.getenv("COMPUTER_AGENT_ALLOW_DESTRUCTIVE", "0") == "1",
        action_timeout_seconds=float(os.getenv("COMPUTER_AGENT_ACTION_TIMEOUT_SECONDS", "30")),
        observation_timeout_seconds=float(os.getenv("COMPUTER_AGENT_OBSERVATION_TIMEOUT_SECONDS", "15")),
        workflow_timeout_seconds=float(os.getenv("COMPUTER_AGENT_WORKFLOW_TIMEOUT_SECONDS", "600")),
        allowed_path_prefixes=tuple(p.strip() for p in prefix_raw.split(",") if p.strip()),
        allowed_domains=tuple(d.strip() for d in domain_raw.split(",") if d.strip()) or None,
        work_root=os.getenv("COMPUTER_AGENT_WORK_ROOT") or None,
    )


def build_adapter():
    """Adapter factory — keeps the HTTP layer testable without Chromium."""
    target = os.getenv("COMPUTER_AGENT_ADAPTER_MODULE", "").strip()
    if target:
        module_name, _, class_name = target.partition(":")
        module = importlib.import_module(module_name)
        return getattr(module, class_name)()
    from browser_adapter import PlaywrightBrowserAdapter
    return PlaywrightBrowserAdapter(HEADLESS)


class Handler(BaseHTTPRequestHandler):
    server_version = f"computer-agent/{SERVICE_VERSION}"

    def _send(self, status: int, payload: dict, origin: str | None = None) -> None:
        raw = b"" if status == 204 else json.dumps(payload, ensure_ascii=False, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        if origin and origin in allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, format, *args):  # keep test output readable
        if os.getenv("COMPUTER_AGENT_VERBOSE") == "1":
            super().log_message(format, *args)

    def do_OPTIONS(self):
        origin = self.headers.get("Origin", "")
        if self.path != "/agent/execute":
            return self._send(404, {"status": "FAIL", "error": "not_found"})
        requested_method = self.headers.get("Access-Control-Request-Method", "").upper()
        requested_headers = {h.strip().lower() for h in self.headers.get("Access-Control-Request-Headers", "").split(",") if h.strip()}
        if origin not in allowed_origins():
            return self._send(403, {"status": "BLOCKED", "error": "origin_not_allowed"})
        if requested_method != "POST" or not {"authorization", "content-type"}.issubset(requested_headers) or not requested_headers.issubset({"authorization", "content-type"}):
            return self._send(403, {"status": "BLOCKED", "error": "preflight_not_allowed"})
        self._send(204, {}, origin=origin)

    def do_GET(self):
        origin = self.headers.get("Origin", "")
        if origin and origin not in allowed_origins():
            return self._send(403, {"status": "BLOCKED", "error": "origin_not_allowed"})
        if self.path == "/health":
            policy = build_policy()
            return self._send(200, {
                "status": "ok",
                "service": "computer-agent",
                "version": SERVICE_VERSION,
                "port": PORT,
                "work_id": WORK_ID,
                "execution_busy": _EXECUTION_LOCK.locked(),
                "policy": {
                    "allow_destructive": policy.allow_destructive,
                    "max_action_retries": policy.max_action_retries,
                    "action_timeout_seconds": policy.action_timeout_seconds,
                    "workflow_timeout_seconds": policy.workflow_timeout_seconds,
                },
            }, origin=origin if origin else None)
        self._send(404, {"status": "FAIL", "error": "not_found"}, origin=origin if origin else None)

    def do_POST(self):
        origin = self.headers.get("Origin", "")
        if origin not in allowed_origins():
            return self._send(403, {"status": "BLOCKED", "error": "origin_not_allowed"})
        configured_token = request_token()
        supplied_auth = self.headers.get("Authorization", "")
        supplied_token = supplied_auth[7:] if supplied_auth.startswith("Bearer ") else ""
        if not configured_token or not hmac.compare_digest(supplied_token, configured_token):
            return self._send(401, {"status": "BLOCKED", "error": "unauthorized"}, origin=origin)
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            return self._send(415, {"status": "BLOCKED", "error": "content_type_must_be_application_json"}, origin=origin)
        if self.path != "/agent/execute":
            return self._send(404, {"status": "FAIL", "error": "not_found"}, origin=origin)
        if self.headers.get("Transfer-Encoding"):
            return self._send(400, {"status": "FAIL", "error": "transfer_encoding_not_supported"}, origin=origin)

        adapter = None
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0:
                return self._send(400, {"status": "FAIL", "error": "invalid_content_length"}, origin=origin)
            if length > 1024 * 1024:
                return self._send(413, {"status": "BLOCKED", "error": "request_body_too_large"}, origin=origin)
            body = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError) as exc:
            return self._send(400, {"status": "FAIL", "error": f"invalid_json: {exc}"}, origin=origin)

        if not isinstance(body, dict):
            return self._send(400, {"status": "FAIL", "error": "request_body_must_be_object"}, origin=origin)

        task = body.get("task")
        if not isinstance(task, str) or not task.strip():
            return self._send(400, {"status": "FAIL", "error": "task must be a non-empty string"}, origin=origin)
        raw_actions = body.get("actions")
        if not isinstance(raw_actions, list):
            return self._send(400, {"status": "FAIL", "error": "actions must be a list"}, origin=origin)

        try:
            actions = [Action(**a) for a in raw_actions]
        except (TypeError, ActionValidationError) as exc:
            return self._send(400, {"status": "FAIL",
                                    "error": f"invalid_action: {exc}"}, origin=origin)

        invalid_verification = AgentRuntime._validate_verification(body.get("verification"))
        if invalid_verification:
            return self._send(409, {
                "status": "BLOCKED",
                "error": f"policy_violation[{invalid_verification['rule']}]: {invalid_verification['detail']}",
            }, origin=origin)

        if not _EXECUTION_LOCK.acquire(blocking=False):
            return self._send(409, {
                "status": "BLOCKED",
                "error": "execution_busy",
                "detail": "another workflow is active or a timed-out adapter worker has not terminated",
            }, origin=origin)

        adapter = None
        runtime = None
        result = None
        try:
            adapter = build_adapter()
            runtime = AgentRuntime(adapter, policy=build_policy(), work_id=WORK_ID)
            result = runtime.execute(task, actions, body.get("verification"))
        except Exception as exc:  # adapter construction / unexpected runtime failure
            return self._send(500, {"status": "FAIL",
                                    "error": f"{type(exc).__name__}: {exc}"}, origin=origin)
        finally:
            has_active_worker = (
                runtime is not None and runtime.has_active_timed_out_calls()
            )
            if runtime is not None and has_active_worker:
                # Wait for the timed-out call, then close on the same adapter-owner
                # thread. Keep the global lease throughout this deferred cleanup.
                def deferred_cleanup():
                    try:
                        runtime.wait_for_timed_out_calls()
                        try:
                            runtime.close_adapter()
                        except Exception as cleanup_error:
                            print(
                                f"Work10 deferred adapter cleanup failed: {type(cleanup_error).__name__}: {cleanup_error}",
                                file=sys.stderr, flush=True,
                            )
                        runtime.shutdown_adapter_worker()
                    finally:
                        _EXECUTION_LOCK.release()

                try:
                    threading.Thread(
                        target=deferred_cleanup,
                        name="work10-deferred-adapter-cleanup",
                        daemon=True,
                    ).start()
                except Exception as start_error:
                    # Fail closed: retain the lease rather than close an adapter
                    # concurrently with a possibly active worker. /health stays busy.
                    print(
                        f"Work10 deferred cleanup thread could not start: {type(start_error).__name__}: {start_error}",
                        file=sys.stderr, flush=True,
                    )
            else:
                try:
                    if runtime is not None:
                        try:
                            runtime.close_adapter()
                        except Exception as cleanup_error:
                            print(
                                f"Work10 adapter cleanup failed: {type(cleanup_error).__name__}: {cleanup_error}",
                                file=sys.stderr, flush=True,
                            )
                        finally:
                            runtime.shutdown_adapter_worker()
                    elif adapter is not None:
                        adapter.close()
                finally:
                    _EXECUTION_LOCK.release()


        if result is None:
            return self._send(500, {"status": "FAIL", "error": "execution_failed"}, origin=origin)
        code = 200 if result.status == "PASS" else 409
        return self._send(code, result.__dict__, origin=origin)


def serve(port: int = PORT, host: str = "127.0.0.1") -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = serve()
    actual_port = server.server_address[1]
    print(f"Computer Agent API listening on 127.0.0.1:{actual_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
