"""Auto E2E (Work 32 CI/CD) — live HTTP roundtrip qua TCP.

Khac voi cac test TestClient in-process: test nay boot server uvicorn that
tren port tam (127.0.0.1), roi goi HTTP that bang requests, chung minh
adapter stack khoi dong va wire route dung trong moi truong gan production.
Offline hoan toan: khong dich vu ngoai, khong network ra internet.
"""

from __future__ import annotations

import threading
import time

import pytest
import requests
import uvicorn

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.http_server import create_http_app


@pytest.fixture()
def live_base_url(tmp_path):
    registry = AgentRegistry()
    manager = MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")
    service = MeetingService(manager)
    app = create_http_app(service, agent_registry=registry)

    config = uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 15
    while time.time() < deadline and not server.started:
        time.sleep(0.05)
    if not server.started:
        pytest.fail("uvicorn server did not start within 15s")

    port = server.servers[0].sockets[0].getsockname()[1]
    yield "http://127.0.0.1:%d" % port

    server.should_exit = True
    thread.join(timeout=5)


def test_live_http_meetings_roundtrip(live_base_url):
    response = requests.get(live_base_url + "/meetings", timeout=5)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    assert isinstance(body, (list, dict)), body


def test_live_http_unknown_route_returns_404(live_base_url):
    response = requests.get(live_base_url + "/definitely-not-a-route", timeout=5)
    assert response.status_code == 404
