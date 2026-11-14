"""Real Browser Adapter -> Work32 MCP stdio -> Core transcript E2E.

Uses a temporary disposable meetings store and the actual RoomHopIntegration
stdio subprocess. It does not contact a PC service or mutate a real meeting.
"""
from __future__ import annotations

import asyncio
import importlib
import sys
import types

try:
    from room_hop_mcp.browser_agent_adapter import adapter as browser_adapter
except ModuleNotFoundError as exc:
    if exc.name != "playwright":
        raise
    playwright = types.ModuleType("playwright")
    sync_api = types.ModuleType("playwright.sync_api")
    sync_api.sync_playwright = lambda: None
    sync_api.Browser = type("Browser", (), {})
    sync_api.Page = type("Page", (), {})
    playwright.sync_api = sync_api
    sys.modules["playwright"] = playwright
    sys.modules["playwright.sync_api"] = sync_api
    browser_adapter = importlib.import_module(
        "room_hop_mcp.browser_agent_adapter.adapter"
    )

import mcp.client.stdio as mcp_stdio

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService


def test_browser_adapter_real_stdio_submission_roundtrip(monkeypatch, tmp_path):
    meetings_dir = tmp_path / "disposable-meetings"
    meetings_dir.mkdir()
    (meetings_dir / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE",
        encoding="utf-8",
    )

    meeting_id = "MEETING-W32-BROWSER-STDIO-E2E"
    identity_id = "xu"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    service.create_meeting(
        meeting_id=meeting_id,
        topic="Work32 Browser Adapter real stdio E2E",
        participants=["vinh", identity_id],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, identity_id)
    service.start_meeting(meeting_id, "vinh")

    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_TEST_MEETING_ID", meeting_id)
    monkeypatch.setenv("ROOMHOP_TEST_IDENTITY_ID", identity_id)
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(meetings_dir.resolve()))
    monkeypatch.setenv("ROOMHOP_MCP_TIMEOUT_SECONDS", "30")

    result = {
        "execution_id": "w32-browser-stdio-exec-001",
        "evidence_id": "w32-browser-stdio-evidence-001",
        "work_id": "work-32-browser-stdio-e2e",
        "evidence_json": str(tmp_path / "browser-evidence.json"),
        "final_url": "https://example.com/",
        "page_title": "Example Domain",
    }

    submission = browser_adapter.submit_to_roomhop(result)

    assert submission["status"] == "pass", submission
    assert submission["transport"] == "stdio"
    assert submission["meeting_id"] == meeting_id
    assert submission["identity_id"] == identity_id
    assert submission["read_back"] is True
    assert set(submission["contract_tools"]) == {
        "list_meetings",
        "get_meeting",
        "get_transcript",
        "add_paste_to_meeting",
    }
    assert submission["artifact"]["execution_id"] == result["execution_id"]
    assert submission["artifact"]["evidence_id"] == result["evidence_id"]
    assert submission["artifact"]["work_id"] == result["work_id"]

    transcript = service.get_transcript(meeting_id)
    marker = "ROOMHOP_BROWSER_AGENT_ARTIFACT "
    matching = [item for item in transcript if marker in item["content"]]
    assert len(matching) == 1
    assert matching[0]["speaker"] == identity_id
    assert matching[0]["source"] == {"type": "ai_chat_paste"}
    assert result["execution_id"] in matching[0]["content"]
    assert result["evidence_id"] in matching[0]["content"]


def test_browser_adapter_timeout_closes_real_stdio_child(monkeypatch, tmp_path):
    meetings_dir = tmp_path / "disposable-timeout-store"
    meetings_dir.mkdir()
    (meetings_dir / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE",
        encoding="utf-8",
    )

    meeting_id = "MEETING-W32-BROWSER-STDIO-TIMEOUT"
    identity_id = "xu"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    service.create_meeting(
        meeting_id=meeting_id,
        topic="Work32 Browser Adapter stdio timeout cleanup",
        participants=["vinh", identity_id],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, identity_id)
    service.start_meeting(meeting_id, "vinh")

    captured_processes = []
    original_create = mcp_stdio._create_platform_compatible_process

    async def capture_process(*args, **kwargs):
        process = await original_create(*args, **kwargs)
        captured_processes.append(process)
        return process

    async def wait_before_append(self, session, meeting_id, text, identity_id=None):
        await asyncio.sleep(10)
        return {"status": "unreachable"}

    monkeypatch.setattr(
        mcp_stdio,
        "_create_platform_compatible_process",
        capture_process,
    )
    monkeypatch.setattr(
        browser_adapter.RoomHopIntegration,
        "add_paste_to_meeting",
        wait_before_append,
    )
    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_TEST_MEETING_ID", meeting_id)
    monkeypatch.setenv("ROOMHOP_TEST_IDENTITY_ID", identity_id)
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(meetings_dir.resolve()))
    monkeypatch.setenv("ROOMHOP_MCP_TIMEOUT_SECONDS", "2")

    result = {
        "execution_id": "w32-browser-stdio-timeout-exec",
        "evidence_id": "w32-browser-stdio-timeout-evidence",
        "work_id": "work-32-browser-stdio-timeout",
        "evidence_json": str(tmp_path / "timeout-evidence.json"),
        "final_url": "https://example.com/",
        "page_title": "Example Domain",
    }

    submission = browser_adapter.submit_to_roomhop(result)

    assert submission["status"] == "blocked", submission
    assert "outcome is uncertain" in submission["reason"]
    assert len(captured_processes) == 1
    assert captured_processes[0].returncode is not None
    transcript = service.get_transcript(meeting_id)
    assert not any(
        "ROOMHOP_BROWSER_AGENT_ARTIFACT " in item["content"]
        for item in transcript
    )
