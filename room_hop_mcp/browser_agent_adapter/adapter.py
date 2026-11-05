from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import uuid
from pathlib import Path
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
            "evidence_id": str(uuid.uuid4()),
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
    child_env = dict(os.environ)
    # Force the MCP child onto the explicitly selected disposable test store.
    child_env["ROOM_HOP_MEETINGS_DIR"] = str(meetings_dir)
    child_env["PYTHONPATH"] = str(repo_root)
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(
            python_executable=sys.executable,
            cwd=str(repo_root),
            env=child_env,
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
            "page_title": result["page_title"],
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


def submit_to_roomhop(result: dict[str, Any]):
    """Synchronous Browser Adapter boundary; each handoff owns one stdio session."""
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

    try:
        return asyncio.run(
            _submit_to_roomhop_stdio(
                result,
                meeting_id=meeting_id,
                identity_id=identity_id,
                meetings_dir=meetings_dir,
            )
        )
    except Exception as exc:
        return {
            "status": "blocked",
            "reason": f"{type(exc).__name__}: {exc}",
            "meeting_id": meeting_id,
            "identity_id": identity_id,
            "transport": "stdio",
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
