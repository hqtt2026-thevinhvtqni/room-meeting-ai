"""Minimal A2A-compatible protocol binding (D-01 in DECISION_REGISTER).

Chosen binding: JSON-RPC 2.0 over HTTP, single text part carrying a JSON
payload. A2A concepts exposed:
  - Official A2A 1.0 JSON-RPC methods: SendMessage, GetTask, CancelTask.
  - Legacy aliases message/send, tasks/get, tasks/cancel retained for existing clients.
  - Agent Card: /.well-known/agent-card.json with supportedInterfaces and skills.
  - Official Task/Artifact shapes are serialized at the HTTP boundary; internal task
    dictionaries retain the simpler state field used by the pipeline.

Task state can be persisted across restarts via PersistentTaskStore
(task_store.py) — plug one into the backend constructor.

The wire adapter stays isolated in this module; official SDK interoperability
is tested independently in test_official_a2a_sdk.py.
"""

from __future__ import annotations

import json
import threading
import time
import uuid

from cryptography.hazmat.primitives.asymmetric import ec
from google.protobuf.json_format import MessageToDict
from jwt.algorithms import ECAlgorithm

from a2a.client.card_resolver import parse_agent_card
from a2a.utils.signing import create_agent_card_signer
from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib import request as urllib_request
from urllib.error import URLError

from .states import TaskStateError, assert_transition, is_terminal
from .task_store import TaskStore

AGENT_CARD_PATH = "/.well-known/agent-card.json"
JWKS_PATH = "/.well-known/jwks.json"
AGENT_CARD_KEY_ID = "work51-ephemeral-card-key-1"

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


def _utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# Backend contract — implement this to get an A2A server for free.
# ---------------------------------------------------------------------------

class AgentBackend(ABC):
    """Task store + agent logic. Thread-safety: the store guards its own
    state because ThreadingHTTPServer serves concurrently."""

    def __init__(self, store: TaskStore | None = None) -> None:
        self._store = store or TaskStore()

    # -- storage --------------------------------------------------------

    def store(self, task: dict) -> dict:
        return self._store.set(task)

    def get_task(self, task_id: str) -> dict | None:
        return self._store.get(task_id)

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
              status_message: str | None = None, metadata: dict | None = None,
              context_id: str | None = None) -> dict:
    now = _utc_now_iso()
    return {
        "id": task_id,
        "contextId": context_id or new_id("ctx"),
        "kind": "task",
        "state": state,
        "artifacts": artifacts or [],
        "status": {"state": state, "message": status_message,
                   "timestamp": now},
        "metadata": metadata or {},
        "createdAt": now,
        "updatedAt": now,
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
    """Extract the JSON payload from either legacy or A2A 1.0 text Parts."""
    if not isinstance(message, dict):
        raise RpcParamError("params.message must be an object")
    parts = message.get("parts")
    if not isinstance(parts, list) or not parts:
        raise RpcParamError("params.message.parts must be a non-empty list")
    for part in parts:
        if not isinstance(part, dict):
            continue
        # A2A 1.0 represents the Part union as {"text": "..."}; the legacy
        # local binding used {"type": "text", "text": "..."}.
        if part.get("type") == "text" or isinstance(part.get("text"), str):
            try:
                return json.loads(part.get("text", ""))
            except (ValueError, TypeError) as exc:
                raise RpcParamError(f"text part is not valid JSON: {exc}") from exc
    raise RpcParamError("message must contain at least one text part")


def _to_official_task(task: dict) -> dict:
    """Serialize an internal task to the official A2A 1.0 Task JSON shape."""
    state_map = {
        "submitted": "TASK_STATE_SUBMITTED",
        "working": "TASK_STATE_WORKING",
        "input-required": "TASK_STATE_INPUT_REQUIRED",
        "completed": "TASK_STATE_COMPLETED",
        "failed": "TASK_STATE_FAILED",
        "canceled": "TASK_STATE_CANCELED",
    }
    internal_status = task.get("status") or {}
    status = {
        "state": state_map.get(task.get("state", ""), "TASK_STATE_UNSPECIFIED"),
        "timestamp": internal_status.get("timestamp") or _utc_now_iso(),
    }
    status_message = internal_status.get("message")
    if status_message:
        status["message"] = {
            "messageId": new_id("m"),
            "role": "ROLE_AGENT",
            "parts": [{"text": str(status_message)}],
        }
    artifacts = []
    for artifact in task.get("artifacts") or []:
        parts = []
        for part in artifact.get("parts") or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                parts.append({"text": part["text"]})
        artifacts.append({
            "artifactId": artifact.get("artifactId") or new_id("a"),
            "name": artifact.get("name", ""),
            "description": artifact.get("description", ""),
            "parts": parts,
            "metadata": artifact.get("metadata") or {},
        })
    return {
        "id": task["id"],
        "contextId": task.get("contextId") or new_id("ctx"),
        "status": status,
        "artifacts": artifacts,
        "metadata": task.get("metadata") or {},
    }


# ---------------------------------------------------------------------------
# HTTP server (A2A producer side)
# ---------------------------------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    server_version = "a2a-ct/1.2"

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
            self._respond_json(200, self.server.signed_agent_card())
        elif self.path == JWKS_PATH:
            self._respond_json(200, self.server.jwks())
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
        except TaskStateError as exc:
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
        if method in ("message/send", "SendMessage"):
            official = method == "SendMessage"
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
                    task = backend.get_task(suggested)
                    return {"task": _to_official_task(task)} if official else task
                task = backend.handle_task(suggested or new_id(), payload, None)
            if not isinstance(task, dict) or "id" not in task or "state" not in task:
                raise RpcParamError("backend produced a malformed task")
            stored = backend.store(task)
            return {"task": _to_official_task(stored)} if official else stored
        if method in ("tasks/get", "GetTask"):
            official = method == "GetTask"
            task = backend.get_task(params.get("id") or "")
            if task is None:
                raise RpcParamError(f"unknown task: {params.get('id')!r}")
            return _to_official_task(task) if official else task
        if method in ("tasks/cancel", "CancelTask"):
            official = method == "CancelTask"
            task = backend.get_task(params.get("id") or "")
            if task is None:
                raise RpcParamError(f"unknown task: {params.get('id')!r}")
            if not is_terminal(task.get("state", "")):
                canceled = dict(task)
                canceled["state"] = assert_transition(task["state"], "canceled")
                canceled["status"] = {"state": "canceled",
                                      "message": "canceled by client",
                                      "timestamp": _utc_now_iso()}
                canceled["updatedAt"] = _utc_now_iso()
                task = backend.store(canceled)
            return _to_official_task(task) if official else task
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
        # Ephemeral signing key is suitable for CI/demo conformance only.
        # Production deployments must load a stable key from a secret manager.
        self._card_private_key = ec.generate_private_key(ec.SECP256R1())
        public_jwk = ECAlgorithm.to_jwk(self._card_private_key.public_key(), as_dict=True)
        self._jwks = {"keys": [{
            **public_jwk,
            "kid": AGENT_CARD_KEY_ID,
            "alg": "ES256",
            "use": "sig",
        }]}
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        host, bound_port = self._httpd.server_address[:2]
        return f"http://{host}:{bound_port}/"

    def signed_agent_card(self) -> dict:
        """Build and sign a standards-shaped Agent Card for this server endpoint."""
        card = dict(self.backend.agent_card())
        endpoint = self.base_url
        card["url"] = endpoint  # legacy field accepted by older clients
        card["supportedInterfaces"] = [{
            "url": endpoint,
            "protocolBinding": "JSONRPC",
            "protocolVersion": "1.0",
        }]
        # Non-standard metadata is deliberately not included in the signed card.
        card.pop("metadata", None)
        proto_card = parse_agent_card(card)
        signer = create_agent_card_signer(
            signing_key=self._card_private_key,
            protected_header={
                "alg": "ES256",
                "kid": AGENT_CARD_KEY_ID,
                "jku": endpoint.rstrip("/") + JWKS_PATH,
                "typ": "JOSE",
            },
        )
        return MessageToDict(signer(proto_card))

    def jwks(self) -> dict:
        """Publish the public key only; the private key is never serialized."""
        return self._jwks

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

    def cancel_task(self, task_id: str) -> dict:
        return self._rpc("tasks/cancel", {"id": task_id})

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

    def cancel_task(self, task_id: str) -> dict:
        task = self.backend.get_task(task_id)
        if task is None:
            raise TransportError(f"unknown task: {task_id}")
        if not is_terminal(task.get("state", "")):
            canceled = dict(task)
            canceled["state"] = assert_transition(task["state"], "canceled")
            canceled["status"] = {"state": "canceled",
                                  "message": "canceled by client",
                                  "timestamp": _utc_now_iso()}
            canceled["updatedAt"] = _utc_now_iso()
            return self.backend.store(canceled)
        return task
