from __future__ import annotations

import json
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


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    # Serve the deterministic test target from 05_TEST.
    import os
    os.chdir(ROOT)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main():
    server = start_server()
    port = server.server_address[1]
    evidence_dir = PROJECT / "06_EVIDENCE"
    evidence_dir.mkdir(parents=True, exist_ok=True)

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
        Action("screenshot", args={"path": str(evidence_dir / "real-browser-e2e.png")}),
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

    result = runtime.execute("Real browser end-to-end verification", actions, verification)
    payload = {
        "status": result.status,
        "state_trace": result.state_trace,
        "error": result.error,
        "steps": [s.__dict__ for s in result.steps],
        "evidence": result.evidence,
    }
    (evidence_dir / "real-browser-e2e-result.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    server.shutdown()

    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    if result.status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
