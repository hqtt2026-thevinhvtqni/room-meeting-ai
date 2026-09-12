"""
Tests for room_hop_mcp/adapter/http_server.py — lifecycle + identity routes.

These tests exercise the HTTP layer in isolation with a fake
MeetingService (no real filesystem meetings), because the thing being
verified here is route wiring / request validation / response mapping /
error-status mapping, not MeetingManager business logic (already covered
in test_meeting_manager_allocator.py) or MeetingService pass-through
(trivial, one line each).

/identities is tested against real PrincipalRegistry/AgentRegistry
pointed at a temp dir, since that route reads them directly.
"""

from __future__ import annotations

import pytest
import yaml
from fastapi.testclient import TestClient

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError
from core.principal_registry import PrincipalRegistry
from room_hop_mcp.adapter.http_server import create_http_app


class FakeMeetingService:
    """Minimal stand-in for MeetingService, records calls and returns
    canned responses so route wiring can be asserted without touching
    real Meeting/MeetingManager state."""

    def __init__(self):
        self.calls = []

    def list_meetings(self, status=None):
        self.calls.append(("list_meetings", status))
        return [{"id": "MEETING-2026-001", "title": "x", "status": status or "draft"}]

    def get_meeting(self, meeting_id):
        self.calls.append(("get_meeting", meeting_id))
        return {"id": meeting_id, "title": "x", "status": "open"}

    def get_transcript(self, meeting_id):
        self.calls.append(("get_transcript", meeting_id))
        return []

    def add_paste(self, meeting_id, text):
        self.calls.append(("add_paste", meeting_id, text))
        return {"status": "READY"}

    def create_meeting(self, topic, participants, context_files, created_by, meeting_id=None):
        self.calls.append(("create_meeting", topic, participants, context_files, created_by, meeting_id))
        return {"id": meeting_id or "MEETING-2026-999", "status": "draft"}

    def open_meeting(self, meeting_id):
        self.calls.append(("open_meeting", meeting_id))
        if meeting_id == "ALREADY-CLOSED":
            raise MeetingError("Meeting 'ALREADY-CLOSED' đang ở 'closed', cần 'draft'.")
        return {"id": meeting_id, "status": "open"}

    def join_meeting(self, meeting_id, identity_id):
        self.calls.append(("join_meeting", meeting_id, identity_id))
        return {"id": meeting_id, "status": "open"}

    def start_meeting(self, meeting_id, starter):
        self.calls.append(("start_meeting", meeting_id, starter))
        return {"id": meeting_id, "status": "active"}

    def close_meeting(self, meeting_id, decisions, action_items, summary, closer):
        self.calls.append(("close_meeting", meeting_id, decisions, action_items, summary, closer))
        return f"/fake/meetings/{meeting_id}/final.md"


@pytest.fixture
def principals_dir(tmp_path):
    d = tmp_path / "principals"
    d.mkdir()
    (d / "vinh.yaml").write_text(
        yaml.safe_dump({"id": "vinh", "name": "Vinh", "type": "human_principal"}),
        encoding="utf-8",
    )
    return d


@pytest.fixture
def agents_dir(tmp_path):
    d = tmp_path / "agents"
    d.mkdir()
    (d / "claude.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "claude",
                "name": "Claude",
                "role": "assistant",
                "provider": "anthropic",
                "capabilities": ["notes"],
            }
        ),
        encoding="utf-8",
    )
    return d


@pytest.fixture
def client(principals_dir, agents_dir):
    service = FakeMeetingService()
    app = create_http_app(
        service,
        principal_registry=PrincipalRegistry(principals_dir),
        agent_registry=AgentRegistry(agents_dir),
    )
    test_client = TestClient(app)
    test_client.fake_service = service  # type: ignore[attr-defined]
    return test_client


# ---------------------------------------------------------------------------
# /identities
# ---------------------------------------------------------------------------

def test_identities_returns_both_registries(client):
    response = client.get("/identities")
    assert response.status_code == 200

    body = response.json()
    assert body["principals"] == [{"id": "vinh", "name": "Vinh", "type": "human_principal"}]
    assert body["agents"] == [
        {"id": "claude", "name": "Claude", "role": "assistant", "type": "ai_agent"}
    ]


# ---------------------------------------------------------------------------
# GET /meetings?status=
# ---------------------------------------------------------------------------

def test_list_meetings_forwards_status_query_param(client):
    response = client.get("/meetings?status=closed")
    assert response.status_code == 200
    assert ("list_meetings", "closed") in client.fake_service.calls


def test_list_meetings_without_status_passes_none(client):
    response = client.get("/meetings")
    assert response.status_code == 200
    assert ("list_meetings", None) in client.fake_service.calls


# ---------------------------------------------------------------------------
# POST /meetings — allocator wiring
# ---------------------------------------------------------------------------

def test_create_meeting_without_id(client):
    response = client.post(
        "/meetings",
        json={"topic": "T", "participants": ["vinh"], "created_by": "vinh"},
    )
    assert response.status_code == 200
    call = [c for c in client.fake_service.calls if c[0] == "create_meeting"][0]
    assert call[5] is None  # meeting_id arg


def test_create_meeting_with_explicit_id(client):
    response = client.post(
        "/meetings",
        json={
            "topic": "T",
            "participants": ["vinh"],
            "created_by": "vinh",
            "meeting_id": "MEETING-CUSTOM",
        },
    )
    assert response.status_code == 200
    call = [c for c in client.fake_service.calls if c[0] == "create_meeting"][0]
    assert call[5] == "MEETING-CUSTOM"


# ---------------------------------------------------------------------------
# Lifecycle routes — happy path wiring
# ---------------------------------------------------------------------------

def test_open_join_start_close_happy_path(client):
    assert client.post("/meetings/M1/open").status_code == 200

    r = client.post("/meetings/M1/join", json={"identity_id": "vinh"})
    assert r.status_code == 200
    assert ("join_meeting", "M1", "vinh") in client.fake_service.calls

    r = client.post("/meetings/M1/start", json={"starter": "vinh"})
    assert r.status_code == 200
    assert ("start_meeting", "M1", "vinh") in client.fake_service.calls

    r = client.post(
        "/meetings/M1/close",
        json={
            "decisions": ["d1"],
            "action_items": ["a1 — phụ trách: vinh — hạn: mai — trạng thái: OPEN"],
            "summary": "s",
            "closer": "vinh",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["final_md_path"] == "/fake/meetings/M1/final.md"
    assert body["meeting"]["id"] == "M1"


# ---------------------------------------------------------------------------
# MeetingError -> HTTP 400 mapping
# ---------------------------------------------------------------------------

def test_meeting_error_maps_to_http_400(client):
    response = client.post("/meetings/ALREADY-CLOSED/open")
    assert response.status_code == 400
    assert "closed" in response.json()["detail"]
