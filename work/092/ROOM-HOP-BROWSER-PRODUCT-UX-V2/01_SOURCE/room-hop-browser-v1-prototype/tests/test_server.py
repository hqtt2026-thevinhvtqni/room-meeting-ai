"""Deterministic tests for the Work 092 mock-only HTTP server."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

import pytest

import server


@pytest.fixture(scope="module")
def live_server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        yield base_url
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def test_health_endpoint_is_mock_only(live_server):
    with urlopen(f"{live_server}/api/health", timeout=3) as response:
        payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
    assert payload == {
        "status": "ok",
        "service": "room-hop-browser-v1-prototype",
        "mode": "MOCK ONLY",
        "external_api": False,
        "real_chromium": False,
    }


def test_root_serves_browser_ui(live_server):
    with urlopen(f"{live_server}/", timeout=3) as response:
        body = response.read().decode("utf-8")
        assert response.status == 200
        assert "ROOM-HOP Browser" in body
        assert response.headers.get_content_type() == "text/html"


def test_routes_manifest_is_valid_and_served(live_server):
    with urlopen(f"{live_server}/manus-routes.json", timeout=3) as response:
        manifest = json.loads(response.read().decode("utf-8"))
    assert manifest["routes"] == [
        {"path": "/", "title": "ROOM-HOP Browser V1 Prototype"}
    ]


def test_internal_assets_are_served(live_server):
    for path, marker in (("/styles.css", ":root"), ("/app.js", "const Workflow"),
                         ("/workflow.js", "resolveTask")):
        with urlopen(f"{live_server}{path}", timeout=3) as response:
            body = response.read().decode("utf-8")
            assert response.status == 200
            assert marker in body


def test_canonical_source_assets_exist():
    root = Path(server.ROOT)
    for name in ("index.html", "styles.css", "app.js", "workflow.js", "manus-routes.json"):
        assert (root / name).is_file(), f"Missing canonical asset: {name}"
