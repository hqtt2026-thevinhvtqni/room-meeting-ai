"""Builder / Runtime ports (issue #34, part C).

The backend depends on two *abstract* boundaries, never on concrete agent
or execution machinery:

    BuilderPort  — "generate or edit the website artifacts for this job"
    RuntimePort  — "provision a sandboxed runtime and report its status"

Why ports: WORK.md forbids the Website Builder from creating an independent
execution path. The ROOM-HOP chain is AI -> MCP -> Core -> Workspace /
Execution Contract -> PC Execution Host -> Website Runtime. So the only
adapters allowed here are ones that delegate to that chain. This module
ships with:

* ``NullBuilderPort`` / ``RefusedRuntimePort`` — explicit not-wired stubs.
  They raise ``RuntimeBlockedError``/return empty results so an unwired
  system reports BLOCKED honestly instead of pretending to work.
* ``HttpBuilderAdapter`` / ``HttpRuntimeAdapter`` — thin HTTP clients that
  forward to the existing MCP adapter (:8000) and Execution Host (:8100).
  They contain no business logic; they translate.

Security rules baked into the adapters:
- No shell string is ever built or executed by this process.
- The runtime host must be one of the configured allow-listed origins.
- Responses larger than ``MAX_ARTIFACT_BYTES`` are rejected.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from .errors import RuntimeBlockedError, RuntimeFailedError

#: Guardrail: refuse absurdly large payloads coming back from a builder.
MAX_ARTIFACT_BYTES = 2 * 1024 * 1024


@dataclass
class BuildResult:
    """What a BuilderPort returns: generated files + a diff summary."""

    files: dict[str, str] = field(default_factory=dict)
    diff_summary: str = ""
    log: str = ""
    ok: bool = False
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "files": sorted(self.files),
            "diff_summary": self.diff_summary,
            "log": self.log,
            "detail": self.detail,
        }


@dataclass
class RuntimeStatus:
    """Observed state of a provisioned runtime — never asserted without a probe."""

    running: bool
    preview_url: Optional[str] = None
    pid: Optional[int] = None
    http_status: Optional[int] = None
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "running": self.running,
            "preview_url": self.preview_url,
            "pid": self.pid,
            "http_status": self.http_status,
            "detail": self.detail,
        }


class BuilderPort(ABC):
    @abstractmethod
    def build(self, job: Any) -> BuildResult:
        """Generate/edit artifacts for ``job``. Must not execute arbitrary commands."""

    @property
    @abstractmethod
    def name(self) -> str: ...


class RuntimePort(ABC):
    @abstractmethod
    def start(self, job: Any, artifacts: dict[str, str]) -> RuntimeStatus:
        """Provision a permitted sandbox for the artifacts."""

    @abstractmethod
    def status(self, handle: Any) -> RuntimeStatus:
        """Probe the live runtime. Reports facts, not intentions."""

    @abstractmethod
    def stop(self, handle: Any) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str: ...


# ---------------------------------------------------------------------------
# Explicit "not wired yet" implementations.
# ---------------------------------------------------------------------------


class NullBuilderPort(BuilderPort):
    """Placeholder used until the real builder is connected through MCP/Core."""

    @property
    def name(self) -> str:
        return "null-builder"

    def build(self, job: Any) -> BuildResult:
        return BuildResult(
            ok=False,
            diff_summary="",
            log="builder port not wired: request routed nowhere",
            detail={"reason": "BUILDER_NOT_WIRED"},
        )


class RefusedRuntimePort(RuntimePort):
    """Default runtime port: refuses to open any execution surface.

    Chosen deliberately as the default so a half-built backend cannot run
    commands. Wiring a real runtime requires an explicit, reviewed change.
    """

    @property
    def name(self) -> str:
        return "refused-runtime"

    def start(self, job: Any, artifacts: dict[str, str]) -> RuntimeStatus:
        raise RuntimeBlockedError(
            "runtime port not wired; refusing to start execution",
            details={"reason": "RUNTIME_NOT_WIRED", "artifacts": len(artifacts)},
        )

    def status(self, handle: Any) -> RuntimeStatus:
        return RuntimeStatus(running=False, detail={"reason": "RUNTIME_NOT_WIRED"})

    def stop(self, handle: Any) -> None:
        return None


# ---------------------------------------------------------------------------
# Thin HTTP adapters onto the existing ROOM-HOP infrastructure.
# ---------------------------------------------------------------------------


def _check_origin(origin: str, allowed: tuple[str, ...]) -> str:
    origin = origin.rstrip("/")
    if origin not in allowed:
        raise RuntimeBlockedError(
            f"origin {origin} is not in the allow-list",
            details={"allowed": list(allowed)},
        )
    return origin


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_ARTIFACT_BYTES + 1)
            if len(raw) > MAX_ARTIFACT_BYTES:
                raise RuntimeFailedError(
                    f"response from {url} exceeded {MAX_ARTIFACT_BYTES} bytes"
                )
            return json.loads(raw.decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        raise RuntimeFailedError(
            f"{url} returned HTTP {exc.code}", details={"url": url}
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeFailedError(
            f"{url} unreachable: {exc}", details={"url": url}
        ) from exc


class HttpBuilderAdapter(BuilderPort):
    """Calls the MCP/Core-facing builder endpoint. No local generation logic."""

    ALLOWED_ORIGINS = ("http://127.0.0.1:8000", "http://localhost:8000")

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 60.0) -> None:
        self.base_url = _check_origin(base_url, self.ALLOWED_ORIGINS)
        self.timeout = timeout

    @property
    def name(self) -> str:
        return "http-builder->core:8000"

    def build(self, job: Any) -> BuildResult:
        payload = {
            "job_id": job.id,
            "intent": job.intent,
            "site_name": job.site_name,
            "created_by": job.created_by,
        }
        data = _post_json(f"{self.base_url}/builder/build", payload, self.timeout)
        files = data.get("files") or {}
        if not isinstance(files, dict):
            raise RuntimeFailedError("builder response 'files' is not an object")
        return BuildResult(
            files={str(k): str(v) for k, v in files.items()},
            diff_summary=str(data.get("diff_summary", "")),
            log=str(data.get("log", "")),
            ok=bool(data.get("ok", False)),
            detail={"endpoint": "/builder/build", "raw_keys": sorted(data)},
        )


class HttpRuntimeAdapter(RuntimePort):
    """Delegates provisioning to the PC Execution Host (:8100).

    The Execution Host owns sandboxing/security policy (see
    ``execution_host/security.py``); this adapter only asks and reports.
    """

    ALLOWED_ORIGINS = ("http://127.0.0.1:8100", "http://localhost:8100")

    def __init__(self, base_url: str = "http://127.0.0.1:8100", timeout: float = 30.0) -> None:
        self.base_url = _check_origin(base_url, self.ALLOWED_ORIGINS)
        self.timeout = timeout

    @property
    def name(self) -> str:
        return "http-runtime->execution-host:8100"

    def start(self, job: Any, artifacts: dict[str, str]) -> RuntimeStatus:
        payload = {"job_id": job.id, "artifacts": artifacts, "sandbox": True}
        data = _post_json(f"{self.base_url}/runtime/start", payload, self.timeout)
        if not data.get("granted", False):
            raise RuntimeBlockedError(
                "execution host refused runtime",
                details={"host_response": {k: data.get(k) for k in ("granted", "reason")}},
            )
        return RuntimeStatus(
            running=bool(data.get("running", False)),
            preview_url=data.get("preview_url"),
            pid=data.get("pid"),
            http_status=data.get("http_status"),
            detail={"handle": data.get("handle"), "source": self.base_url},
        )

    def status(self, handle: Any) -> RuntimeStatus:
        data = _post_json(f"{self.base_url}/runtime/status", {"handle": handle}, self.timeout)
        return RuntimeStatus(
            running=bool(data.get("running", False)),
            preview_url=data.get("preview_url"),
            pid=data.get("pid"),
            http_status=data.get("http_status"),
            detail={"source": self.base_url},
        )

    def stop(self, handle: Any) -> None:
        _post_json(f"{self.base_url}/runtime/stop", {"handle": handle}, self.timeout)
