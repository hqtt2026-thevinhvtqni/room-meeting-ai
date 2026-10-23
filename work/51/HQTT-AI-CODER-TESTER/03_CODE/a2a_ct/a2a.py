"""Minimal A2A-compatible protocol binding (D-01 in DECISION_REGISTER).

Chosen binding: JSON-RPC 2.0 over HTTP, single text part carrying a JSON
payload. A2A concepts exposed:
  - Agent Card:   GET /.well-known/agent-card.json
  - message/send: create or continue a Task; payload travels in a text part
  - tasks/get:    read task state (idempotent read path)
  - Task:         {id, kind:"task", state, artifacts[], status{}, metadata{}}
  - Artifact:     {artifactId, name, parts[{type:"text", text}], metadata{sha256, version}}

This module is the ONLY file that knows the wire format. Swapping to the
official A2A SDK later means re-implementing A2AServer/A2AClient here and
leaving every other module untouched.
"""

from __future__ import annotations

import json
import threading
import uuid
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib import request as urllib_request
from urllib.error import URLError

AGENT_CARD_PATH = "/.well-known/agent-card.json"

JSONRPC_PARSE_ERROR = -32700
JSONRPC_INVALID_REQUEST = -32600
JSONRPC_METHOD_NOT_FOUND = -32601
JSONRPC_INVALID_PARAMS = -32602
JSONRPC_INTERNAL_ERROR = -32603
JSONRPC_AGENT_ERROR = -32000  # task-level application error

TERMINAL_STATES = ("completed", "failed", "canceled")


class TransportError(Exception):
    """Network-level failure: agent unavailable, timeout, bad HTTP."""


class AgentError(Exception):
    """Agent returned a JSON-RPC error response."""


class RpcParamError(Exception):
    """Invalid message/task parameters."""


class MethodNotFound(Exception):
    pass


def new_id(prefix: str = "t") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------------------------------
# Backend contract — implement this to get an A2A server for free.
# ---------------------------------------------------------------------------

class AgentBackend(ABC):
    """In-memory task store + agent logic. Thread-safety: tasks dict is
    guarded by a lock because ThreadingHTTPServer serves concurrently."""

    def __init__(self) -> None:
        self.tasks: dict[str, dict] = {}
        self._lock = threading.Lock()

    # -- storage --------------------------------------------------------

    def store(self, task: dict) -> dict:
        with self._lock:
            self.tasks[task["id"]] = task
        return task

    def get_task(self, task_id: str) -> dict | None:
        with self._lock:
            return self.tasks.get(task_id)

    # -- logic -------------------------------------------------------------

    @abstractmethod
    def agent_card(self) -> dict: ...

    @abstractmethod
    def handle_task(self, task_id: str, payload: dict, existing: dict | None) -> dict:
        """Process one message. Return the new (or unchanged) task dict.

        payload: decoded JSON from the message's first text part.
        existing: current task dict when this message continues a task.
        """


# ---------------------------------------------------------------------------
# Task / artifact helpers
# ---------------------------------------------------------------------------

def make_task(task_id: str, state: str, artifacts: list[dict] | None = None,
              status_message: str | None = None, metadata: dict | None = None) -> dict:
    return {
        "id": task_id,
        "kind": "task",
        "state": state,
        "artifacts": artifacts or [],
        "status": {"state": state, "message": status_message},
        "metadata": metadata or {},
    }


def make_text_artifact(name: str, text: str, sha256: str, version: int = 1,
                       description: str = "") -> dict:
    return {
        "artifactId": new_id("a"),
        "name": name,
        "description": description,
        "parts": [{"type": "text", "text": text}],
        "metadata": {"sha256": sha256, "version": version},
    }


def artifact_text(artifact: dict) -> str:
    parts = artifact.get("parts") or []
    for part in parts:
        if part.get("type") == "text":
            return part.get("text", "")
    return ""


def payload_from_message(message: Any) -> dict:
    """Extract the JSON payload from the first text part of a message."""
    if not isinstance(message, dict):
        raise RpcParamError("params.message must be an object")
    parts = message.get("parts")
    if not isinstance(parts, list) or not parts:
        raise RpcParamError("params.message.parts must be a non-empty list")
    for part in parts:
        if isinstance(part, dict) and part.get("type") == "text":
            try:
                return json.loads(part.get("text", ""))
            except (ValueError, TypeError) as exc:
                raise RpcParamError(f"text part is not valid JSON: {exc}") from exc
    raise RpcParamError("message must contain at least one text part")


# ---------------------------------------------------------------------------
# HTTP server (A2A producer side)
# ---------------------------------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    server_version = "a2a-ct/1.0"

    def log_message(self, *args) -> None:  # silence request logging
        return

    def _respond_json(self, status: int, body: dict) -> None:
        raw = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == AGENT_CARD_PATH:
            self._respond_json(200, self.server.backend.agent_card())
        else:
            self._respond_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length else b""
        try:
            req = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._respond_json(200, self._rpc_error(None, JSONRPC_PARSE_ERROR, "parse error"))
            return
        if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" \
                or not isinstance(req.get("method"), str):
            self._respond_json(
                200,
                self._rpc_error(
                    req.get("id") if isinstance(req, dict) else None,
                    JSONRPC_INVALID_REQUEST,
                    "invalid JSON-RPC 2.0 request",
                ),
            )
            return
        req_id = req.get("id")
        params = req.get("params") if isinstance(req.get("params"), dict) else {}
        try:
            result = self._dispatch(req["method"], params)
        except MethodNotFound as exc:
            self._respond_json(200, self._rpc_error(req_id, JSONRPC_METHOD_NOT_FOUND, str(exc)))
            return
        except RpcParamError as exc:
            self._respond_json(200, self._rpc_error(req_id, JSONRPC_INVALID_PARAMS, str(exc)))
            return
        except TransportError as exc:
            self._respond_json(200, self._rpc_error(req_id, JSONRPC_AGENT_ERROR, str(exc)))
            return
        except Exception as exc:  # pragma: no cover - defensive
            self._respond_json(
                200,
                self._rpc_error(req_id, JSONRPC_INTERNAL_ERROR, f"{type(exc).__name__}: {exc}"),
            )
            return
        self._respond_json(200, {"jsonrpc": "2.0", "id": req_id, "result": result})

    def _dispatch(self, method: str, params: dict) -> dict:
        backend = self.server.backend
        if method == "message/send":
            payload = payload_from_message(params.get("message"))
            message = params.get("message") or {}
            cont_id = message.get("taskId")
            if cont_id:
                existing = backend.get_task(cont_id)
                if existing is None:
                    raise RpcParamError(f"unknown taskId: {cont_id}")
                task = backend.handle_task(cont_id, payload, existing)
            else:
                suggested = params.get("taskId")
                if suggested and backend.get_task(suggested) is not None:
                    # Idempotent replay: caller reuses an allocated task id.
                    return backend.get_task(suggested)
                task = backend.handle_task(suggested or new_id(), payload, None)
            if not isinstance(task, dict) or "id" not in task or "state" not in task:
                raise RpcParamError("backend produced a malformed task")
            return backend.store(task)
        if method == "tasks/get":
            task = backend.get_task(params.get("id") or "")
            if task is None:
                raise RpcParamError(f"unknown task: {params.get('id')!r}")
            return task
        raise MethodNotFound(f"method not supported: {method}")

    @staticmethod
    def _rpc_error(req_id: Any, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }


class A2AServer:
    """Runs an AgentBackend behind the minimal A2A HTTP binding."""

    def __init__(self, backend: AgentBackend, host: str = "127.0.0.1", port: int = 0):
        self.backend = backend
        self._httpd = ThreadingHTTPServer((host, port), _Handler)
        self._httpd.backend = backend
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        host, bound_port = self._httpd.server_address[:2]
        return f"http://{host}:{bound_port}/"

    def start(self) -> str:
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self.base_url

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()


# ---------------------------------------------------------------------------
# HTTP client (A2A consumer side)
# ---------------------------------------------------------------------------

class A2AClient:
    def __init__(self, base_url: str, timeout_s: float = 60.0):
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout_s = timeout_s
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def agent_card(self) -> dict:
        try:
            with urllib_request.urlopen(
                self.base_url.rstrip("/") + AGENT_CARD_PATH, timeout=self.timeout_s
            ) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, OSError) as exc:
            raise TransportError(f"agent_card failed: {exc}") from exc

    def send(self, payload: dict, task_id: str | None = None) -> dict:
        """message/send with JSON payload in a single text part."""
        message: dict = {
            "messageId": new_id("m"),
            "role": "user",
            "parts": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
        }
        if task_id:
            message["taskId"] = task_id
        return self._rpc("message/send", {"message": message})

    def send_raw_text(self, text: str, task_id: str | None = None) -> dict:
        """Fault-injection helper: send arbitrary text as the payload part."""
        message: dict = {"messageId": new_id("m"), "role": "user",
                        "parts": [{"type": "text", "text": text}]}
        if task_id:
            message["taskId"] = task_id
        return self._rpc("message/send", {"message": message})

    def get_task(self, task_id: str) -> dict:
        return self._rpc("tasks/get", {"id": task_id})

    def _rpc(self, method: str, params: dict) -> dict:
        body = json.dumps(
            {"jsonrpc": "2.0", "id": self._next_id(), "method": method, "params": params}
        ).encode("utf-8")
        req = urllib_request.Request(
            self.base_url, data=body,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib_request.urlopen(req, timeout=self.timeout_s) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, OSError) as exc:
            raise TransportError(f"{method} failed: {exc}") from exc
        if not isinstance(data, dict):
            raise TransportError(f"{method}: non-object response")
        if "error" in data:
            raise AgentError(str(data["error"].get("message") or data["error"]))
        return data.get("result") or {}


class LocalClient:
    """In-process client: same wire semantics as A2AClient without HTTP.

    Used by the test suite for fast pipeline coverage; the HTTP binding is
    covered separately in test_http.py.
    """

    def __init__(self, backend: AgentBackend):
        self.backend = backend

    def send(self, payload: dict, task_id: str | None = None) -> dict:
        if task_id:
            existing = self.backend.get_task(task_id)
            if existing is None:
                raise TransportError(f"unknown taskId: {task_id}")
            task = self.backend.handle_task(task_id, payload, existing)
        else:
            task = self.backend.handle_task(new_id(), payload, None)
        return self.backend.store(task)

    def get_task(self, task_id: str) -> dict:
        task = self.backend.get_task(task_id)
        if task is None:
            raise TransportError(f"unknown task: {task_id}")
        return task
