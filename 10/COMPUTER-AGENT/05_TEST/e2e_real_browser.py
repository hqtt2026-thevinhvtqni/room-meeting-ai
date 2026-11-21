"""
Work 10 — real Chromium/Playwright E2E (gate P3)

MUST run on a host with Chromium + Playwright installed. The ROOM-HOP Sandbox
cannot launch a local Chromium process, so this script never claims a result by
itself: it writes 06_EVIDENCE/real-browser-e2e-result.json + .png and exits
non-zero on anything but PASS.

It serves 05_TEST over an ephemeral localhost port and drives the deterministic
target page (browser_e2e_target.html), then verifies a post-condition on the
FINAL observation — a click alone can never satisfy it. Adapter cleanup occurs
in the finally block after verification; close is not a workflow action.

Usage:  python 05_TEST/e2e_real_browser.py
"""
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
from models import Action, SafetyPolicy


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def start_server():
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)  # noqa: E731
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main() -> int:
    server = start_server()
    port = server.server_address[1]
    evidence_dir = PROJECT / "06_EVIDENCE"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # SAFETY_POLICY §4: this workflow explicitly declares the one destructive
    # action it needs (download of a file inside the Work), and §5 confines
    # navigation to the local test server and artifacts to the Work root.
    policy = SafetyPolicy(
        allow_destructive=True,
        allowed_domains=("127.0.0.1",),
        work_root=str(PROJECT),
    )

    adapter = PlaywrightBrowserAdapter(headless=True)
    runtime = AgentRuntime(adapter, policy=policy, work_id="10")

    actions = [
        Action("navigate", value=f"http://127.0.0.1:{port}/browser_e2e_target.html"),
        Action("observe"),
        Action("click", target="Start task"),
        Action("type", target="Task name", value="Work 10 REAL E2E"),
        Action("key_press", value="TAB"),
        Action("scroll", value=500),
        Action("click", target="Submit task"),
        Action("wait", value=0.2),
        Action("observe"),
        Action("extract", target="#result"),
        Action("screenshot", args={"path": str(evidence_dir / "real-browser-e2e.png")}),
        Action("download", target="Download evidence"),
        Action("observe"),
    ]

    verification = {
        "checks": [
            {"field": "text", "contains": "SUBMITTED"},
            {"field": "text", "contains": "Work 10 REAL E2E"},
        ]
    }

    try:
        result = runtime.execute("Real browser end-to-end verification", actions, verification)
    finally:
        try:
            # Playwright sync objects are thread-affine. AgentRuntime owns the
            # adapter on its worker thread, so close it through that same owner.
            if runtime.has_active_timed_out_calls():
                runtime.wait_for_timed_out_calls()
            runtime.close_adapter()
        finally:
            runtime.shutdown_adapter_worker()
            server.shutdown()

    payload = {
        "work_id": "10",
        "gate": "P3 — real Chromium E2E",
        "host": {"platform": sys.platform, "python": sys.version.split()[0]},
        "status": result.status,
        "state_trace": result.state_trace,
        "error": result.error,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "policy": result.policy,
        "steps": [s.__dict__ for s in result.steps],
        "evidence": result.evidence,
    }
    (evidence_dir / "real-browser-e2e-result.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )

    print(json.dumps({k: payload[k] for k in ("status", "state_trace", "error")},
                     ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
