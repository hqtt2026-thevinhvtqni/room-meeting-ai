"""Opt-in Windows E2E against a per-run disposable Core meeting and local page."""
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
    "ROOMHOP_BROWSER_ADAPTER_URL",
    "ROOMHOP_BROWSER_ADAPTER_PORT",
)

pytestmark = pytest.mark.skipif(
    os.getenv("ROOMHOP_TEST_MODE") != "1"
    or any(not os.getenv(name) for name in REQUIRED_ENV),
    reason="requires an explicitly provisioned per-run disposable ROOM-HOP fixture",
)


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (
            "<!doctype html><html><head><title>W32 Browser Adapter Fixture</title></head>"
            "<body><h1>Work32 deterministic browser fixture</h1>"
            "<h2>Exact-SHA runner-owned process</h2>"
            "<p>Local-only page used to verify browser navigation and extraction.</p>"
            "</body></html>"
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format, *_args):
        return


def test_browser_workflow_handoff_and_readback():
    """Run only when the workflow has created the exact disposable fixture."""
    fixture_server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
    thread = threading.Thread(target=fixture_server.serve_forever, daemon=True)
    thread.start()
    fixture_url = f"http://127.0.0.1:{fixture_server.server_address[1]}/fixture"
    adapter_url = os.environ["ROOMHOP_BROWSER_ADAPTER_URL"].rstrip("/")
    expected_port = int(os.environ["ROOMHOP_BROWSER_ADAPTER_PORT"])

    try:
        health = requests.get(adapter_url + "/health", timeout=5)
        assert health.ok, health.text
        assert health.json()["ok"] is True
        assert health.json()["port"] == expected_port

        req = {
            "url": fixture_url,
            "work_id": "w32-windows-browser-e2e",
            "steps": [
                {"op": "inspect"},
                {
                    "op": "extract",
                    "selectors": {
                        "headings": "h1,h2",
                        "summary": "body p",
                    },
                },
                {"op": "wait", "ms": 100},
                {"op": "screenshot", "name": "w32-windows-browser-e2e.png"},
            ],
        }
        response = requests.post(
            adapter_url + "/browser/execute_workflow",
            json=req,
            timeout=60,
        )
        assert response.ok, response.text
        data = response.json()
        assert data["ok"] is True
        assert data["final_url"] == fixture_url
        assert data["page_title"] == "W32 Browser Adapter Fixture"

        submission = data["roomhop_submission"]
        assert submission["status"] == "pass", submission
        assert submission["read_back"] is True
        assert submission["transport"] == "stdio"
        assert submission["meeting_id"] == os.environ["ROOMHOP_TEST_MEETING_ID"]
        assert submission["identity_id"] == os.environ["ROOMHOP_TEST_IDENTITY_ID"]
    finally:
        fixture_server.shutdown()
        fixture_server.server_close()
        thread.join(timeout=5)
