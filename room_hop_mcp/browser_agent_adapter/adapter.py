from __future__ import annotations

import asyncio
import ipaddress
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from functools import wraps
import json
import os
import socket
import sys
import time
from threading import RLock
import uuid
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright, Browser, Page

from integration.room_hop_integration import RoomHopIntegration, RoomHopIntegrationConfig


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
app = FastAPI(title="ROOM-HOP Browser Agent Adapter", version="1.1.0")

MAX_BROWSER_WAIT_MS = 5000
MAX_BROWSER_WORKFLOW_STEPS = 10
BROWSER_OPERATION_TIMEOUT_SECONDS = 120

def _redact_url(value: str) -> str:
    """Remove query strings and fragments before evidence/transcript persistence."""
    try:
        parts = urlsplit(str(value))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    except ValueError:
        return "[invalid-url]"


def _validate_navigation_url(value: str) -> None:
    """Fail closed for non-web schemes and non-public destinations."""
    try:
        parts = urlsplit(str(value))
        host = parts.hostname
        if parts.scheme.lower() not in {"http", "https"} or not host:
            raise ValueError("Browser navigation permits only http/https URLs.")
        if parts.username is not None or parts.password is not None:
            raise ValueError("Credentials embedded in browser URLs are not permitted.")
    except ValueError:
        raise

    allowed_test_hosts = {
        item.strip().lower()
        for item in os.getenv("ROOMHOP_BROWSER_ALLOWED_HOSTS", "").split(",")
        if item.strip()
    }
    if os.getenv("ROOMHOP_TEST_MODE") == "1" and host.lower() in allowed_test_hosts:
        return

    try:
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(host, parts.port, type=socket.SOCK_STREAM)
        }
    except OSError:
        raise ValueError("Browser destination DNS resolution failed.") from None
    if not addresses:
        raise ValueError("Browser destination did not resolve.")
    for address in addresses:
        try:
            parsed_ip = ipaddress.ip_address(address)
        except ValueError:
            raise ValueError("Browser destination resolved to an invalid IP.") from None
        if not parsed_ip.is_global:
            raise ValueError("Browser destination resolves to a non-public IP address.")


def _safe_evidence_path(name: str) -> Path:
    """Confine evidence filenames to the adapter evidence directory."""
    if not isinstance(name, str) or not name or name in {".", ".."}:
        raise ValueError("Evidence filename is required.")
    candidate = Path(name)
    if (
        candidate.is_absolute()
        or candidate.name != name
        or "/" in name
        or "\\" in name
        or any(character in name for character in '<>:"|?*')
        or any(ord(character) < 32 for character in name)
        or name.endswith((" ", "."))
    ):
        raise ValueError("Evidence filename must be a safe plain basename.")
    stem = name.split(".", 1)[0].upper()
    reserved_windows_names = {"CON", "PRN", "AUX", "NUL"}
    reserved_windows_names.update(f"{prefix}{index}" for prefix in ("COM", "LPT") for index in range(1, 10))
    reserved_windows_names.update(f"{prefix}{suffix}" for prefix in ("COM", "LPT") for suffix in ("¹", "²", "³"))
    if stem in reserved_windows_names:
        raise ValueError("Evidence filename uses a reserved Windows device name.")
    root = EVIDENCE.resolve()
    resolved = (root / name).resolve()
    if resolved.parent != root:
        raise ValueError("Evidence path escapes the evidence directory.")
    return resolved


class WorkflowRequest(BaseModel):
    url: str
    steps: list[dict[str, Any]] = Field(default_factory=list, max_length=MAX_BROWSER_WORKFLOW_STEPS)
    work_id: str = Field(default="browser-e2e", max_length=64)
    collect_screenshot: bool = True


def _serialized_operation(method):
    """Serialize access to the process-wide Playwright state; nested calls are re-entrant."""
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        with self._operation_lock:
            return method(self, *args, **kwargs)
    return wrapped


class Adapter:
    def __init__(self):
        self._operation_lock = RLock()
        self.pw = None
        self.browser: Browser | None = None
        self.context = None
        self.page: Page | None = None
        self.started_at = None
        self.logs: list[dict[str, Any]] = []

    def log(self, event: str, **data: Any):
        item = {"ts": time.time(), "event": event, **data}
        self.logs.append(item)
        return item

    @_serialized_operation
    def start(self):
        if self.page:
            return {"status": "already_started"}

        if self.browser is None:
            self.pw = sync_playwright().start()
            executable = os.getenv("ROOMHOP_BROWSER_EXECUTABLE")
            launch_kwargs: dict[str, Any] = {
                "headless": True,
                "args": [],
            }
            if executable:
                launch_kwargs["executable_path"] = executable
            self.browser = self.pw.chromium.launch(**launch_kwargs)

        self._create_context()
        self.started_at = time.time()
        self.log(
            "browser_start",
            backend="chromium",
            executable=executable or "playwright-managed",
        )
        return {
            "status": "started",
            "backend": "chromium",
            "executable": executable or "playwright-managed",
        }

    def _create_context(self):
        if self.browser is None:
            raise RuntimeError("Browser process is not started.")
        self.context = self.browser.new_context(
            accept_downloads=True,
            service_workers="block",
            viewport={"width": 1280, "height": 900},
        )
        self.context.route("**/*", self._guard_route)
        self.page = self.context.new_page()
        return self.context

    def _close_context(self) -> None:
        context = self.context
        self.context = None
        self.page = None
        if context is not None:
            context.close()

    def _replace_context(self):
        """Start a clean browser storage/session boundary for one workflow."""
        self._close_context()
        return self._create_context()

    def require(self) -> Page:
        if not self.page:
            self.start()
        assert self.page is not None
        return self.page

    @staticmethod
    def _guard_route(route) -> None:
        try:
            _validate_navigation_url(route.request.url)
        except ValueError:
            route.abort()
        else:
            route.continue_()

    @_serialized_operation
    def navigate(self, url: str):
        _validate_navigation_url(url)
        p = self.require()
        r = p.goto(url, wait_until="domcontentloaded", timeout=30000)
        _validate_navigation_url(p.url)
        p.wait_for_timeout(500)
        self.log("browser_navigate", url=_redact_url(p.url), status=r.status if r else None)
        return {"url": _redact_url(p.url), "status": r.status if r else None, "title": p.title()}

    @_serialized_operation
    def inspect(self):
        p = self.require()
        data = {
            "url": _redact_url(p.url),
            "title": p.title(),
            "headings": p.locator("h1,h2,h3").all_text_contents()[:20],
            "links": p.locator("a").all_text_contents()[:30],
            "inputs": p.locator("input").count(),
        }
        self.log("browser_inspect", **data)
        return data

    @_serialized_operation
    def click(self, selector: str):
        p = self.require()
        p.locator(selector).first.click(timeout=15000)
        p.wait_for_timeout(500)
        self.log("browser_click", selector=selector)
        return {"url": _redact_url(p.url), "title": p.title()}

    @_serialized_operation
    def type(self, selector: str, text: str):
        p = self.require()
        p.locator(selector).first.fill(text, timeout=15000)
        self.log("browser_type", selector=selector, chars=len(text))
        return {"selector": selector, "typed": len(text)}

    @_serialized_operation
    def wait(self, ms: int = 1000):
        if isinstance(ms, bool) or not isinstance(ms, int) or not 0 <= ms <= MAX_BROWSER_WAIT_MS:
            raise ValueError(f"wait ms must be an integer between 0 and {MAX_BROWSER_WAIT_MS}.")
        self.require().wait_for_timeout(ms)
        self.log("browser_wait", ms=ms)
        return {"waited_ms": ms}

    @_serialized_operation
    def extract(self, selectors: dict[str, str]):
        p = self.require()
        out = {k: p.locator(v).all_text_contents()[:20] for k, v in selectors.items()}
        out["url"] = _redact_url(p.url)
        out["title"] = p.title()
        self.log("browser_extract", fields=list(selectors))
        return out

    @_serialized_operation
    def screenshot(self, name: str = "page.png"):
        p = self.require()
        path = _safe_evidence_path(name)
        p.screenshot(path=str(path), full_page=True)
        self.log("browser_screenshot", path=str(path))
        return {"path": str(path)}

    @_serialized_operation
    def download(self, selector: str, name: str | None = None):
        p = self.require()
        with p.expect_download(timeout=20000) as pending:
            p.locator(selector).first.click()
        download = pending.value
        path = _safe_evidence_path(name or download.suggested_filename)
        download.save_as(str(path))
        self.log("browser_download", selector=selector, path=str(path))
        return {"path": str(path), "suggested_filename": download.suggested_filename}

    @_serialized_operation
    def close(self):
        if self.browser:
            self._close_context()
            self.browser.close()
            if self.pw:
                self.pw.stop()
            self.browser = None
            self.pw = None
            self.log("browser_close")
        return {"status": "closed"}

    @_serialized_operation
    def workflow(self, req: WorkflowRequest):
        self.logs = []
        self.start()
        isolated_context = self.browser is not None
        if isolated_context:
            self._replace_context()
        try:
            self.navigate(req.url)
            results = []

            for step in req.steps:
                op = step["op"]
                if op == "inspect":
                    results.append(self.inspect())
                elif op == "click":
                    results.append(self.click(step["selector"]))
                elif op == "type":
                    results.append(self.type(step["selector"], step["text"]))
                elif op == "wait":
                    results.append(self.wait(step.get("ms", 1000)))
                elif op == "extract":
                    results.append(self.extract(step["selectors"]))
                elif op == "screenshot":
                    results.append(self.screenshot(step.get("name", "page.png")))
                else:
                    raise ValueError(f"unsupported operation: {op}")

            final = {
                "execution_id": str(uuid.uuid4()),
                "evidence_id": str(uuid.uuid4()),
                "work_id": req.work_id,
                "ok": True,
                "final_url": _redact_url(self.page.url),
                "page_title": self.page.title(),
                "results": results,
                "logs": self.logs,
                "started_at": self.started_at,
                "finished_at": time.time(),
            }

            out = _safe_evidence_path(f"{req.work_id}-{int(time.time())}.json")
            out.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
            final["evidence_json"] = str(out)
            final["roomhop_submission"] = _submit_to_roomhop_from_worker(final)
            return final
        finally:
            if isolated_context:
                self._close_context()


adapter = Adapter()
# FastAPI sync endpoints may execute on different worker threads. Playwright's
# synchronous objects must remain owned by one thread, so all adapter calls are
# dispatched through this single-worker executor.
_BROWSER_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="roomhop-browser-adapter")


def _run_browser_operation(operation, *args, **kwargs):
    future = _BROWSER_EXECUTOR.submit(operation, *args, **kwargs)
    try:
        return future.result(timeout=BROWSER_OPERATION_TIMEOUT_SECONDS)
    except FutureTimeoutError:
        future.cancel()
        raise HTTPException(
            status_code=504,
            detail="Browser operation exceeded its bounded execution window; outcome may be uncertain; do not retry automatically.",
        ) from None


def _execute_workflow(req: WorkflowRequest):
    try:
        return {"ok": True, "value": adapter.workflow(req)}
    except Exception as exc:
        return {
            "ok": False,
            "detail": {"error": str(exc), "logs": list(adapter.logs)},
        }



def _contains_exact_marker(value: Any, marker: str) -> bool:
    if isinstance(value, str):
        return marker in value
    if isinstance(value, dict):
        return any(_contains_exact_marker(item, marker) for item in value.values())
    if isinstance(value, list):
        return any(_contains_exact_marker(item, marker) for item in value)
    return False


async def _submit_to_roomhop_stdio(
    result: dict[str, Any],
    meeting_id: str,
    identity_id: str,
    meetings_dir: Path,
) -> dict[str, Any]:
    """Use the canonical Work32 Public V1 stdio client for one isolated handoff."""
    repo_root = Path(__file__).resolve().parents[2]
    # Pass only the two required values; stdio_client adds its safe default
    # environment. Never forward the Browser Adapter's full environment.
    child_env = {
        "ROOM_HOP_MEETINGS_DIR": str(meetings_dir),
        "PYTHONPATH": str(repo_root),
    }
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(
            python_executable=sys.executable,
            cwd=str(repo_root),
            env=child_env,
            # The runner uses Python's embeddable distribution, which ignores
            # PYTHONPATH. Inject the exact checkout root before importing Public V1.
            python_args=[
                "-c",
                "import sys, runpy; "
                f"sys.path.insert(0, {str(repo_root)!r}); "
                "runpy.run_module('room_hop_mcp', run_name='__main__')",
            ],
        )
    )

    expected_tools = {
        "list_meetings",
        "get_meeting",
        "get_transcript",
        "add_paste_to_meeting",
    }

    async with integration.session() as session:
        tools_result = await session.list_tools()
        actual_tools = {tool.name for tool in tools_result.tools}
        if actual_tools != expected_tools:
            return {
                "status": "blocked",
                "reason": "ROOM-HOP MCP tool inventory does not exactly match ADR-002 Public V1",
                "expected_tools": sorted(expected_tools),
                "actual_tools": sorted(actual_tools),
                "meeting_id": meeting_id,
                "identity_id": identity_id,
            }

        meetings = await integration.list_meetings(session)
        target = next(
            (item for item in meetings if item.get("id") == meeting_id),
            None,
        )
        if target is None:
            return {
                "status": "blocked",
                "reason": "Configured disposable test meeting was not found; no fallback is permitted",
                "meeting_id": meeting_id,
                "identity_id": identity_id,
            }

        meeting = await integration.get_meeting(session, meeting_id)
        status = str(meeting.get("status", "")).lower()
        if status not in {"active", "open", "started"}:
            return {
                "status": "blocked",
                "reason": "Configured disposable test meeting is not active",
                "meeting_id": meeting_id,
                "meeting_status": meeting.get("status"),
                "identity_id": identity_id,
            }

        artifact = {
            "artifact_type": "browser_workflow_execution",
            "execution_id": result["execution_id"],
            "evidence_id": result["evidence_id"],
            "work_id": result["work_id"],
            "evidence_json": Path(result["evidence_json"]).name,
            "final_url": result["final_url"],
        }
        marker = "ROOMHOP_BROWSER_AGENT_ARTIFACT " + json.dumps(
            artifact, ensure_ascii=False, sort_keys=True
        )

        handoff = await integration.add_paste_to_meeting(
            session,
            meeting_id,
            marker,
            identity_id=identity_id,
        )
        transcript = await integration.get_transcript(session, meeting_id)
        transcript_text = json.dumps(transcript, ensure_ascii=False, sort_keys=True)
        read_back = _contains_exact_marker(transcript, marker) and all(
            token in transcript_text
            for token in (
                result["execution_id"],
                result["evidence_id"],
                result["work_id"],
                Path(result["evidence_json"]).name,
            )
        )

        return {
            "status": "pass" if read_back else "blocked",
            "reason": None if read_back else "Exact execution artifact was not found in transcript readback",
            "meeting_id": meeting_id,
            "identity_id": identity_id,
            "handoff": handoff,
            "read_back": read_back,
            "artifact": artifact,
            "contract_tools": sorted(actual_tools),
            "transport": "stdio",
            "meetings_dir": str(meetings_dir),
        }


DEFAULT_MCP_TIMEOUT_SECONDS = 30.0
MAX_MCP_TIMEOUT_SECONDS = 120.0


def _mcp_timeout_seconds() -> float:
    raw = os.getenv("ROOMHOP_MCP_TIMEOUT_SECONDS", str(DEFAULT_MCP_TIMEOUT_SECONDS))
    try:
        timeout = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("ROOMHOP_MCP_TIMEOUT_SECONDS must be numeric") from exc
    if not (0 < timeout <= MAX_MCP_TIMEOUT_SECONDS):
        raise ValueError(
            f"ROOMHOP_MCP_TIMEOUT_SECONDS must be greater than 0 and at most {MAX_MCP_TIMEOUT_SECONDS:g}"
        )
    return timeout


def submit_to_roomhop(result: dict[str, Any]):
    """Synchronous Browser Adapter boundary; each handoff owns one bounded stdio session."""
    if os.getenv("ROOMHOP_TEST_MODE") != "1":
        return {
            "status": "blocked",
            "reason": "ROOM-HOP transcript submission requires ROOMHOP_TEST_MODE=1",
        }

    meeting_id = os.getenv("ROOMHOP_TEST_MEETING_ID")
    identity_id = os.getenv("ROOMHOP_TEST_IDENTITY_ID")
    test_store = os.getenv("ROOMHOP_TEST_MEETINGS_DIR")
    if not meeting_id or not identity_id or not test_store:
        return {
            "status": "blocked",
            "reason": "Explicit ROOMHOP_TEST_MEETING_ID, ROOMHOP_TEST_IDENTITY_ID and ROOMHOP_TEST_MEETINGS_DIR are required",
        }

    meetings_dir = Path(test_store).expanduser()
    if not meetings_dir.is_absolute():
        return {
            "status": "blocked",
            "reason": "ROOMHOP_TEST_MEETINGS_DIR must be an absolute path",
        }
    meetings_dir = meetings_dir.resolve()
    if not meetings_dir.is_dir():
        return {
            "status": "blocked",
            "reason": "Configured disposable test meetings directory does not exist",
            "meetings_dir": str(meetings_dir),
        }
    store_marker = meetings_dir / ".roomhop-disposable-test-store"
    try:
        marker_value = store_marker.read_text(encoding="utf-8").strip()
    except OSError:
        marker_value = ""
    if marker_value != "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE":
        return {
            "status": "blocked",
            "reason": "Disposable test store marker is missing or invalid; no MCP subprocess was started",
            "meetings_dir": str(meetings_dir),
        }

    try:
        timeout_seconds = _mcp_timeout_seconds()
    except ValueError as exc:
        return {"status": "blocked", "reason": str(exc)}

    # Guard before constructing the coroutine: asyncio.run cannot be nested.
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        pass
    else:
        return {
            "status": "blocked",
            "reason": "Nested event loops are not allowed; call from the synchronous Browser Adapter worker",
        }

    try:
        return asyncio.run(
            asyncio.wait_for(
                _submit_to_roomhop_stdio(
                    result,
                    meeting_id=meeting_id,
                    identity_id=identity_id,
                    meetings_dir=meetings_dir,
                ),
                timeout=timeout_seconds,
            )
        )
    except asyncio.TimeoutError:
        # The append may have reached Core before timeout; never retry automatically.
        return {
            "status": "blocked",
            "reason": "MCP stdio submission timed out; append outcome is uncertain; do not retry automatically",
            "meeting_id": meeting_id,
            "identity_id": identity_id,
            "timeout_seconds": timeout_seconds,
            "transport": "stdio",
        }
    except Exception as exc:
        return {
            "status": "blocked",
            "reason": f"{type(exc).__name__}: {exc}",
            "meeting_id": meeting_id,
            "identity_id": identity_id,
            "transport": "stdio",
        }



def _submit_to_roomhop_from_worker(result: dict[str, Any]) -> dict[str, Any]:
    """Run MCP stdio outside Playwright's synchronous API event-loop thread."""
    with ThreadPoolExecutor(max_workers=1, thread_name_prefix="roomhop-mcp-submit") as executor:
        return executor.submit(submit_to_roomhop, result).result()


def _configured_port() -> int:
    raw = os.getenv("ROOMHOP_BROWSER_ADAPTER_PORT", "8787")
    try:
        port = int(raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError("ROOMHOP_BROWSER_ADAPTER_PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise RuntimeError("ROOMHOP_BROWSER_ADAPTER_PORT must be between 1 and 65535")
    return port


@app.get("/health")
def health():
    browser_started = _run_browser_operation(lambda: adapter.page is not None)
    return {
        "ok": True,
        "service": "room-hop-browser-agent-adapter",
        "browser_started": browser_started,
        "port": _configured_port(),
    }


@app.post("/browser/start")
def start():
    return _run_browser_operation(adapter.start)


@app.post("/browser/navigate")
def navigate(body: dict):
    return _run_browser_operation(adapter.navigate, body["url"])


@app.post("/browser/inspect")
def inspect():
    return _run_browser_operation(adapter.inspect)


@app.post("/browser/click")
def click(body: dict):
    return _run_browser_operation(adapter.click, body["selector"])


@app.post("/browser/type")
def type_text(body: dict):
    return _run_browser_operation(adapter.type, body["selector"], body["text"])


@app.post("/browser/wait")
def wait(body: dict | None = None):
    return _run_browser_operation(adapter.wait, (body or {}).get("ms", 1000))


@app.post("/browser/extract")
def extract(body: dict):
    return _run_browser_operation(adapter.extract, body["selectors"])


@app.post("/browser/screenshot")
def screenshot(body: dict | None = None):
    return _run_browser_operation(adapter.screenshot, (body or {}).get("name", "page.png"))


@app.post("/browser/download")
def download(body: dict):
    return _run_browser_operation(adapter.download, body["selector"], body.get("name"))


@app.post("/browser/execute_workflow")
def execute(req: WorkflowRequest):
    # Execute and snapshot failures on the same dedicated browser thread.
    result = _run_browser_operation(_execute_workflow, req)
    if not result["ok"]:
        raise HTTPException(500, detail=result["detail"])
    return result["value"]


@app.post("/browser/close")
def close():
    return _run_browser_operation(adapter.close)


TOOLS = [
    "browser_start",
    "browser_navigate",
    "browser_inspect",
    "browser_click",
    "browser_type",
    "browser_wait",
    "browser_extract",
    "browser_screenshot",
    "browser_download",
    "browser_execute_workflow",
    "browser_close",
]


@app.post("/mcp")
def mcp(payload: dict):
    method = payload.get("method")
    request_id = payload.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": name,
                        "description": f"ROOM-HOP Browser Agent Adapter {name}",
                    }
                    for name in TOOLS
                ]
            },
        }

    if method == "tools/call":
        name = payload.get("params", {}).get("name")
        args = payload.get("params", {}).get("arguments", {})
        routes = {
            "browser_start": lambda: _run_browser_operation(adapter.start),
            "browser_navigate": lambda: _run_browser_operation(adapter.navigate, args["url"]),
            "browser_inspect": lambda: _run_browser_operation(adapter.inspect),
            "browser_click": lambda: _run_browser_operation(adapter.click, args["selector"]),
            "browser_type": lambda: _run_browser_operation(adapter.type, args["selector"], args["text"]),
            "browser_wait": lambda: _run_browser_operation(adapter.wait, args.get("ms", 1000)),
            "browser_extract": lambda: _run_browser_operation(adapter.extract, args["selectors"]),
            "browser_screenshot": lambda: _run_browser_operation(adapter.screenshot, args.get("name", "page.png")),
            "browser_download": lambda: _run_browser_operation(adapter.download, args["selector"], args.get("name")),
            "browser_execute_workflow": lambda: _run_browser_operation(adapter.workflow, WorkflowRequest(**args)),
            "browser_close": lambda: _run_browser_operation(adapter.close),
        }

        if name not in routes:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": "Unknown tool"},
                },
                status_code=404,
            )

        try:
            value = routes[name]()
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"content": [{"type": "json", "json": value}]},
            }
        except Exception as exc:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": str(exc)},
                },
                status_code=500,
            )

    return JSONResponse(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "Unsupported method"},
        },
        status_code=400,
    )
