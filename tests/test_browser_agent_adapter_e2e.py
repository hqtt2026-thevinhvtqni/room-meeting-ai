"""Opt-in Windows integration test against a per-run disposable ROOM-HOP fixture."""
from __future__ import annotations

import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import requests


REQUIRED_ENV = (
    "ROOMHOP_TEST_MEETINGS_DIR",
    "ROOMHOP_TEST_MODE",
    "ROOMHOP_TEST_MEETING_ID",
    "ROOMHOP_TEST_IDENTITY_ID",
    "ROOMHOP_BROWSER_ADAPTER_PORT",
)

pytestmark = pytest.mark.skipif(
    os.getenv("ROOMHOP_TEST_MODE") != "1"
    or any(not os.getenv(name) for name in REQUIRED_ENV),
    reason="requires an explicitly configured runner-owned disposable ROOM-HOP fixture",
)


def _adapter_base_url() -> str:
    port = int(os.environ["ROOMHOP_BROWSER_ADAPTER_PORT"])
    if not 1 <= port <= 65535:
        raise ValueError("ROOMHOP_BROWSER_ADAPTER_PORT must be between 1 and 65535")
    return f"http://127.0.0.1:{port}"


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"""<!doctype html>
<html><head><title>Work32 Browser Adapter Fixture</title></head>
<body>
<h1>Work32 Browser Adapter E2E</h1>
<h2>Deterministic local page</h2>
<p id="summary">This page is served inside the Windows E2E job.</p>
</body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def test_browser_workflow_handoff_and_readback():
    """Exercise Chromium, the adapter, MCP stdio and transcript readback locally."""
    with ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler) as fixture:
        thread = threading.Thread(target=fixture.serve_forever, daemon=True)
        thread.start()
        try:
            fixture_url = f"http://127.0.0.1:{fixture.server_port}/"
            req = {
                "url": fixture_url,
                "work_id": "w32-local-browser-e2e",
                "steps": [
                    {"op": "inspect"},
                    {
                        "op": "extract",
                        "selectors": {
                            "headings": "h1,h2",
                            "summary": "#summary",
                        },
                    },
                    {"op": "wait", "ms": 100},
                    {"op": "screenshot", "name": "w32-local-browser-e2e.png"},
                ],
            }

            response = requests.post(
                _adapter_base_url() + "/browser/execute_workflow",
                json=req,
                timeout=60,
            )
            assert response.ok, response.text
            data = response.json()
            assert data["ok"] is True
            assert data["final_url"] == fixture_url
            assert data["page_title"] == "Work32 Browser Adapter Fixture"

            submission = data["roomhop_submission"]
            assert submission["status"] == "pass", submission
            assert submission["read_back"] is True
            assert submission["transport"] == "stdio"
            assert submission["meeting_id"] == os.environ["ROOMHOP_TEST_MEETING_ID"]
            assert submission["identity_id"] == os.environ["ROOMHOP_TEST_IDENTITY_ID"]
        finally:
            fixture.shutdown()
            thread.join(timeout=5)
