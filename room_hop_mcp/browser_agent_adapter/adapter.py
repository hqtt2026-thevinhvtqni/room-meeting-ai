from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright, Browser, Page


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)
app = FastAPI(title="ROOM-HOP Browser Agent Adapter", version="1.1.0")


class WorkflowRequest(BaseModel):
    url: str
    steps: list[dict[str, Any]] = Field(default_factory=list)
    work_id: str = "browser-e2e"
    collect_screenshot: bool = True


class Adapter:
    def __init__(self):
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

    def start(self):
        if self.page:
            return {"status": "already_started"}

        self.pw = sync_playwright().start()
        executable = os.getenv("ROOMHOP_BROWSER_EXECUTABLE")
        launch_kwargs: dict[str, Any] = {
            "headless": True,
            "args": ["--no-sandbox"],
        }
        if executable:
            launch_kwargs["executable_path"] = executable

        self.browser = self.pw.chromium.launch(**launch_kwargs)
        self.context = self.browser.new_context(
            accept_downloads=True,
            viewport={"width": 1280, "height": 900},
        )
        self.page = self.context.new_page()
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

    def require(self) -> Page:
        if not self.page:
            self.start()
        assert self.page is not None
        return self.page

    def navigate(self, url: str):
        p = self.require()
        r = p.goto(url, wait_until="domcontentloaded", timeout=30000)
        p.wait_for_timeout(500)
        self.log("browser_navigate", url=p.url, status=r.status if r else None)
        return {"url": p.url, "status": r.status if r else None, "title": p.title()}

    def inspect(self):
        p = self.require()
        data = {
            "url": p.url,
            "title": p.title(),
            "headings": p.locator("h1,h2,h3").all_text_contents()[:20],
            "links": p.locator("a").all_text_contents()[:30],
            "inputs": p.locator("input").count(),
        }
        self.log("browser_inspect", **data)
        return data

    def click(self, selector: str):
        p = self.require()
        p.locator(selector).first.click(timeout=15000)
        p.wait_for_timeout(500)
        self.log("browser_click", selector=selector)
        return {"url": p.url, "title": p.title()}

    def type(self, selector: str, text: str):
        p = self.require()
        p.locator(selector).first.fill(text, timeout=15000)
        self.log("browser_type", selector=selector, chars=len(text))
        return {"selector": selector, "typed": len(text)}

    def wait(self, ms: int = 1000):
        self.require().wait_for_timeout(ms)
        self.log("browser_wait", ms=ms)
        return {"waited_ms": ms}

    def extract(self, selectors: dict[str, str]):
        p = self.require()
        out = {k: p.locator(v).all_text_contents()[:20] for k, v in selectors.items()}
        out["url"] = p.url
        out["title"] = p.title()
        self.log("browser_extract", fields=list(selectors))
        return out

    def screenshot(self, name: str = "page.png"):
        p = self.require()
        path = EVIDENCE / name
        p.screenshot(path=str(path), full_page=True)
        self.log("browser_screenshot", path=str(path))
        return {"path": str(path)}

    def download(self, selector: str, name: str | None = None):
        p = self.require()
        with p.expect_download(timeout=20000) as pending:
            p.locator(selector).first.click()
        download = pending.value
        path = EVIDENCE / (name or download.suggested_filename)
        download.save_as(str(path))
        self.log("browser_download", selector=selector, path=str(path))
        return {"path": str(path), "suggested_filename": download.suggested_filename}

    def close(self):
        if self.browser:
            self.browser.close()
            if self.pw:
                self.pw.stop()
            self.browser = None
            self.page = None
            self.log("browser_close")
        return {"status": "closed"}

    def workflow(self, req: WorkflowRequest):
        self.logs = []
        self.start()
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
            "work_id": req.work_id,
            "ok": True,
            "final_url": self.page.url,
            "page_title": self.page.title(),
            "results": results,
            "logs": self.logs,
            "started_at": self.started_at,
            "finished_at": time.time(),
        }

        out = EVIDENCE / f"{req.work_id}-{int(time.time())}.json"
        out.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
        final["evidence_json"] = str(out)
        final["roomhop_submission"] = submit_to_roomhop(final)
        return final


adapter = Adapter()


def _roomhop_endpoint() -> str:
    endpoint = os.getenv("ROOMHOP_MCP_URL")
    if not endpoint:
        raise RuntimeError("ROOMHOP_MCP_URL not configured")
    return endpoint.rstrip("/")


_ROOMHOP_SESSION_ID: str | None = None
_ROOMHOP_PROTOCOL_VERSION: str | None = None


def _parse_mcp_response(response: requests.Response) -> dict[str, Any]:
    content_type = response.headers.get("content-type", "").lower()
    raw = response.text

    if not raw.strip():
        raise RuntimeError(
            "ROOM-HOP MCP empty response: "
            f"status={response.status_code} content_type={content_type!r} "
            f"headers={{k: v for k, v in response.headers.items() if k.lower() in ['content-type', 'mcp-session-id', 'mcp-protocol-version']}}"
        )

    if "application/json" in content_type:
        data = response.json()
    elif "text/event-stream" in content_type:
        data = None
        for line in raw.splitlines():
            if line.startswith("data:"):
                event_data = line[5:].strip()
                if not event_data:
                    continue
                try:
                    candidate = json.loads(event_data)
                except json.JSONDecodeError:
                    continue
                if isinstance(candidate, dict) and ("result" in candidate or "error" in candidate):
                    data = candidate
        if data is None:
            raise RuntimeError(
                "ROOM-HOP MCP SSE contained no JSON-RPC result/error: "
                f"status={response.status_code} body={raw[:1000]!r}"
            )
    else:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "ROOM-HOP MCP unexpected response: "
                f"status={response.status_code} content_type={content_type!r} body={raw[:1000]!r}"
            ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"ROOM-HOP MCP returned non-object response: {data!r}")
    if "error" in data:
        raise RuntimeError(f"ROOM-HOP MCP error: {data['error']}")
    return data


def _roomhop_headers() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if _ROOMHOP_SESSION_ID:
        headers["Mcp-Session-Id"] = _ROOMHOP_SESSION_ID
    if _ROOMHOP_PROTOCOL_VERSION:
        headers["MCP-Protocol-Version"] = _ROOMHOP_PROTOCOL_VERSION
    return headers


def _roomhop_post(payload: dict[str, Any]) -> dict[str, Any]:
    global _ROOMHOP_SESSION_ID, _ROOMHOP_PROTOCOL_VERSION

    response = requests.post(
        _roomhop_endpoint(),
        json=payload,
        headers=_roomhop_headers(),
        timeout=float(os.getenv("ROOMHOP_MCP_TIMEOUT", "20")),
    )
    response.raise_for_status()

    session_id = response.headers.get("Mcp-Session-Id")
    if session_id:
        _ROOMHOP_SESSION_ID = session_id

    protocol_version = response.headers.get("MCP-Protocol-Version")
    if protocol_version:
        _ROOMHOP_PROTOCOL_VERSION = protocol_version

    return _parse_mcp_response(response)


def _roomhop_notification(payload: dict[str, Any]) -> None:
    global _ROOMHOP_SESSION_ID, _ROOMHOP_PROTOCOL_VERSION

    response = requests.post(
        _roomhop_endpoint(),
        json=payload,
        headers=_roomhop_headers(),
        timeout=float(os.getenv("ROOMHOP_MCP_TIMEOUT", "20")),
    )
    response.raise_for_status()

    session_id = response.headers.get("Mcp-Session-Id")
    if session_id:
        _ROOMHOP_SESSION_ID = session_id

    protocol_version = response.headers.get("MCP-Protocol-Version")
    if protocol_version:
        _ROOMHOP_PROTOCOL_VERSION = protocol_version


def _roomhop_initialize() -> None:
    global _ROOMHOP_SESSION_ID, _ROOMHOP_PROTOCOL_VERSION

    if _ROOMHOP_SESSION_ID:
        return

    versions = [
        os.getenv("ROOMHOP_MCP_PROTOCOL_VERSION", "2025-03-26"),
        "2025-06-18",
    ]
    last_error: Exception | None = None

    for version in versions:
        try:
            data = _roomhop_post(
                {
                    "jsonrpc": "2.0",
                    "id": str(uuid.uuid4()),
                    "method": "initialize",
                    "params": {
                        "protocolVersion": version,
                        "capabilities": {},
                        "clientInfo": {
                            "name": "room-hop-browser-agent-adapter",
                            "version": "1.1.0",
                        },
                    },
                }
            )
            negotiated = data.get("result", {}).get("protocolVersion")
            if negotiated:
                _ROOMHOP_PROTOCOL_VERSION = str(negotiated)
            _roomhop_notification(
                {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                }
            )
            return
        except Exception as exc:
            last_error = exc
            _ROOMHOP_SESSION_ID = None
            _ROOMHOP_PROTOCOL_VERSION = None

    raise RuntimeError(f"ROOM-HOP MCP initialize failed: {last_error}")


def roomhop_rpc(method: str, params: dict[str, Any] | None = None, request_id: str | None = None):
    if method not in {"initialize", "notifications/initialized"}:
        _roomhop_initialize()

    payload = {
        "jsonrpc": "2.0",
        "id": request_id or str(uuid.uuid4()),
        "method": method,
    }
    if params is not None:
        payload["params"] = params

    return _roomhop_post(payload)


def roomhop_tools_list() -> list[dict[str, Any]]:
    data = roomhop_rpc("tools/list")
    return data.get("result", {}).get("tools", [])


def roomhop_tool_call(name: str, arguments: dict[str, Any] | None = None):
    return roomhop_rpc(
        "tools/call",
        {"name": name, "arguments": arguments or {}},
    )


def _tool_names(tools: list[dict[str, Any]]) -> set[str]:
    return {str(tool.get("name")) for tool in tools}


def _extract_tool_result(data: dict[str, Any]) -> Any:
    result = data.get("result", {})
    content = result.get("content", [])
    for item in content:
        if item.get("type") in {"json", "application/json"}:
            if "json" in item:
                return item["json"]
        if "text" in item:
            raw = item["text"]
            try:
                return json.loads(raw)
            except Exception:
                return raw
    return result


def submit_to_roomhop(result: dict[str, Any]):
    endpoint = os.getenv("ROOMHOP_MCP_URL")
    if not endpoint:
        return {
            "status": "deferred",
            "reason": "ROOMHOP_MCP_URL not configured",
            "local_evidence": result["evidence_json"],
        }

    try:
        tools = roomhop_tools_list()
        names = _tool_names(tools)
        required = {"list_meetings", "add_paste_to_meeting", "get_transcript"}
        missing = sorted(required - names)
        if missing:
            return {
                "status": "blocked",
                "reason": "ROOM-HOP MCP public contract missing required recording/read tools",
                "missing_tools": missing,
                "endpoint": endpoint,
            }

        meetings = _extract_tool_result(roomhop_tool_call("list_meetings"))
        meeting_items = meetings.get("meetings", []) if isinstance(meetings, dict) else []
        preferred = os.getenv("ROOMHOP_MEETING_ID")
        meeting = next((m for m in meeting_items if m.get("id") == preferred), None) if preferred else None

        if meeting is None:
            meeting = next(
                (m for m in meeting_items if str(m.get("status", "")).lower() in {"active", "open", "started"}),
                None,
            )
        if meeting is None:
            return {
                "status": "blocked",
                "reason": "No active ROOM-HOP meeting available for recording",
                "endpoint": endpoint,
            }

        meeting_id = meeting["id"]
        artifact = {
            "artifact_type": "browser_workflow_execution",
            "execution_id": result["execution_id"],
            "work_id": result["work_id"],
            "evidence_json": Path(result["evidence_json"]).name,
            "final_url": result["final_url"],
            "page_title": result["page_title"],
        }
        marker = "ROOMHOP_BROWSER_AGENT_ARTIFACT " + json.dumps(
            artifact, ensure_ascii=False, sort_keys=True
        )

        handoff = _extract_tool_result(
            roomhop_tool_call(
                "add_paste_to_meeting",
                {
                    "meeting_id": meeting_id,
                    "text": marker,
                    "identity_id": os.getenv("ROOMHOP_IDENTITY_ID", "xu"),
                },
            )
        )

        transcript = _extract_tool_result(
            roomhop_tool_call("get_transcript", {"meeting_id": meeting_id})
        )
        transcript_text = json.dumps(transcript, ensure_ascii=False)
        read_back = all(
            token in transcript_text
            for token in [result["execution_id"], result["work_id"], Path(result["evidence_json"]).name]
        )

        return {
            "status": "pass" if read_back else "blocked",
            "endpoint": endpoint,
            "meeting_id": meeting_id,
            "handoff": handoff,
            "read_back": read_back,
            "artifact": artifact,
            "contract_tools": sorted(names),
        }
    except Exception as exc:
        return {
            "status": "blocked",
            "reason": str(exc),
            "endpoint": endpoint,
        }


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "room-hop-browser-agent-adapter",
        "browser_started": adapter.page is not None,
    }


@app.post("/browser/start")
def start():
    return adapter.start()


@app.post("/browser/navigate")
def navigate(body: dict):
    return adapter.navigate(body["url"])


@app.post("/browser/inspect")
def inspect():
    return adapter.inspect()


@app.post("/browser/click")
def click(body: dict):
    return adapter.click(body["selector"])


@app.post("/browser/type")
def type_text(body: dict):
    return adapter.type(body["selector"], body["text"])


@app.post("/browser/wait")
def wait(body: dict | None = None):
    return adapter.wait((body or {}).get("ms", 1000))


@app.post("/browser/extract")
def extract(body: dict):
    return adapter.extract(body["selectors"])


@app.post("/browser/screenshot")
def screenshot(body: dict | None = None):
    return adapter.screenshot((body or {}).get("name", "page.png"))


@app.post("/browser/download")
def download(body: dict):
    return adapter.download(body["selector"], body.get("name"))


@app.post("/browser/execute_workflow")
def execute(req: WorkflowRequest):
    try:
        return adapter.workflow(req)
    except Exception as exc:
        raise HTTPException(500, detail={"error": str(exc), "logs": adapter.logs})


@app.post("/browser/close")
def close():
    return adapter.close()


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
            "browser_start": lambda: adapter.start(),
            "browser_navigate": lambda: adapter.navigate(args["url"]),
            "browser_inspect": lambda: adapter.inspect(),
            "browser_click": lambda: adapter.click(args["selector"]),
            "browser_type": lambda: adapter.type(args["selector"], args["text"]),
            "browser_wait": lambda: adapter.wait(args.get("ms", 1000)),
            "browser_extract": lambda: adapter.extract(args["selectors"]),
            "browser_screenshot": lambda: adapter.screenshot(args.get("name", "page.png")),
            "browser_download": lambda: adapter.download(args["selector"], args.get("name")),
            "browser_execute_workflow": lambda: adapter.workflow(WorkflowRequest(**args)),
            "browser_close": lambda: adapter.close(),
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
