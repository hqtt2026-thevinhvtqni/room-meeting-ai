from __future__ import annotations

import json
import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
sys.path.insert(0, str(PROJECT / "04_CODE"))

from agent_runtime import AgentRuntime
from browser_adapter import PlaywrightBrowserAdapter
from models import Action

EVIDENCE_DIR = PROJECT / "06_EVIDENCE"
RESULT_PATH = EVIDENCE_DIR / "real-browser-e2e-result.json"

# Exit codes: distinguish env problems (BLOCKED) from genuine test failures (FAIL).
EXIT_PASS, EXIT_FAIL, EXIT_BLOCKED = 0, 1, 2

TASK = "Real browser end-to-end verification"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def write_evidence(payload):
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def preflight() -> str | None:
    """Return None when the host environment is ready, else a BLOCKED reason.

    Per the Workflow Contract: a missing environment is BLOCKED, not FAIL,
    and must never be reported as PASS.
    """
    try:
        import playwright  # noqa: F401
    except ImportError:
        return (
            "BLOCKED: playwright is not installed. "
            "Run: pip install -r 10/COMPUTER-AGENT/requirements.txt"
        )
    try:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        try:
            pw.chromium.launch(headless=True).close()
        finally:
            pw.stop()
    except Exception as exc:
        return (
            f"BLOCKED: Chromium is not available for Playwright ({type(exc).__name__}: {exc}). "
            "Run: playwright install chromium"
        )
    return None


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    # Serve the deterministic test target from 05_TEST.
    os.chdir(ROOT)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main():
    reason = preflight()
    if reason:
        payload = {
            "task": TASK,
            "status": "BLOCKED",
            "state_trace": ["PLANNED", "BLOCKED"],
            "error": reason,
            "steps": [],
            "evidence": [],
        }
        write_evidence(payload)
        print(reason)
        raise SystemExit(EXIT_BLOCKED)

    server = start_server()
    port = server.server_address[1]

    adapter = PlaywrightBrowserAdapter(headless=True)
    runtime = AgentRuntime(adapter)

    actions = [
        Action("navigate", value=f"http://127.0.0.1:{port}/browser_e2e_target.html"),
        Action("observe"),
        Action("click", target="Start task"),
        Action("type", target="Task name", value="Work 10 REAL E2E"),
        Action("key_press", value="TAB"),
        Action("scroll", args={"amount": 500}),
        Action("wait", args={"seconds": 0.2}),
        Action("click", target="Submit task"),
        Action("observe"),
        Action("extract", target="#result"),
        Action("screenshot", args={"path": str(EVIDENCE_DIR / "real-browser-e2e.png")}),
        Action("download", target="Download evidence"),
        Action("observe"),
        Action("close"),
    ]

    verification = {
        "checks": [
            {"field": "text", "contains": "Work 10 REAL E2E"},
            {"field": "text", "contains": "SUBMITTED"},
        ]
    }

    try:
        result = runtime.execute(TASK, actions, verification)
    finally:
        # Never leak the browser or the local server, even on unexpected errors.
        if adapter.browser:
            adapter.close()
        server.shutdown()

    payload = {
        "status": result.status,
        "state_trace": result.state_trace,
        "error": result.error,
        "steps": [s.__dict__ for s in result.steps],
        "evidence": result.evidence,
    }
    write_evidence(payload)

    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    if result.status == "PASS":
        raise SystemExit(EXIT_PASS)
    raise SystemExit(EXIT_BLOCKED if result.status == "BLOCKED" else EXIT_FAIL)


if __name__ == "__main__":
    main()
