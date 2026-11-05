import importlib
import sys
import types
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

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
    browser_adapter = importlib.import_module("room_hop_mcp.browser_agent_adapter.adapter")


EXPECTED_TOOLS = {
    "list_meetings",
    "get_meeting",
    "get_transcript",
    "add_paste_to_meeting",
}
RESULT = {
    "execution_id": "exec-test-001",
    "evidence_id": "evidence-test-001",
    "work_id": "work-32-test",
    "evidence_json": "/tmp/workflow-evidence.json",
    "final_url": "https://example.com/",
    "page_title": "Example Domain",
}


class FakeIntegration:
    def __init__(self, config, *, tools=None, meetings=None, meeting=None):
        self.config = config
        self.tools = EXPECTED_TOOLS if tools is None else set(tools)
        self.meetings = (
            [{"id": "MEETING-W32-DISPOSABLE", "status": "active"}]
            if meetings is None else meetings
        )
        self.meeting = (
            {"id": "MEETING-W32-DISPOSABLE", "status": "active"}
            if meeting is None else meeting
        )
        self.transcript = []
        self.calls = []
        self.session_opened = False
        self.session_closed = False

    @asynccontextmanager
    async def session(self):
        self.session_opened = True
        try:
            yield SimpleNamespace(
                list_tools=lambda: self._list_tools()
            )
        finally:
            self.session_closed = True

    async def _list_tools(self):
        return SimpleNamespace(
            tools=[SimpleNamespace(name=name) for name in sorted(self.tools)]
        )

    async def list_meetings(self, session):
        self.calls.append(("list_meetings", None))
        return self.meetings

    async def get_meeting(self, session, meeting_id):
        self.calls.append(("get_meeting", meeting_id))
        return self.meeting

    async def add_paste_to_meeting(self, session, meeting_id, text, identity_id=None):
        self.calls.append(("add_paste_to_meeting", meeting_id, identity_id))
        self.transcript.append({"content": text, "speaker": identity_id})
        return {"status": "READY"}

    async def get_transcript(self, session, meeting_id):
        self.calls.append(("get_transcript", meeting_id))
        return self.transcript


def _configure_test_target(monkeypatch, tmp_path):
    meetings_dir = tmp_path / "disposable-meetings"
    meetings_dir.mkdir()
    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_TEST_MEETING_ID", "MEETING-W32-DISPOSABLE")
    monkeypatch.setenv("ROOMHOP_TEST_IDENTITY_ID", "identity-w32-e2e")
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(meetings_dir))
    return meetings_dir


def _install_fake(monkeypatch, **kwargs):
    instances = []

    def factory(config):
        instance = FakeIntegration(config, **kwargs)
        instances.append(instance)
        return instance

    monkeypatch.setattr(browser_adapter, "RoomHopIntegration", factory)
    return instances


def test_submission_is_blocked_without_explicit_test_mode(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.delenv("ROOMHOP_TEST_MODE")
    monkeypatch.setattr(
        browser_adapter,
        "RoomHopIntegration",
        lambda config: (_ for _ in ()).throw(AssertionError("must not start MCP")),
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_MODE=1" in result["reason"]


def test_submission_requires_explicit_disposable_store_and_identity(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.delenv("ROOMHOP_TEST_MEETINGS_DIR")
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_MEETINGS_DIR" in result["reason"]


def test_submission_rejects_nonexistent_disposable_store(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    missing = tmp_path / "missing-store"
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(missing))
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "does not exist" in result["reason"]


def test_submission_rejects_extra_or_missing_public_tools(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(monkeypatch, tools=EXPECTED_TOOLS | {"join_meeting"})
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert result["expected_tools"] == sorted(EXPECTED_TOOLS)
    assert "join_meeting" in result["actual_tools"]
    assert instances[0].calls == []
    assert instances[0].session_closed is True


def test_submission_does_not_fall_back_when_explicit_test_meeting_missing(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(
        monkeypatch,
        meetings=[{"id": "REAL-MEETING", "status": "active"}],
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "no fallback" in result["reason"]
    assert instances[0].calls == [("list_meetings", None)]
    assert instances[0].session_closed is True


def test_submission_rejects_inactive_disposable_meeting(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(
        monkeypatch,
        meeting={"id": "MEETING-W32-DISPOSABLE", "status": "closed"},
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "not active" in result["reason"]
    assert [call[0] for call in instances[0].calls] == [
        "list_meetings", "get_meeting"
    ]
    assert instances[0].session_closed is True


def test_submission_uses_exact_target_stdio_and_verifies_readback(monkeypatch, tmp_path):
    meetings_dir = _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(monkeypatch)
    result = browser_adapter.submit_to_roomhop(RESULT)

    assert result["status"] == "pass"
    assert result["read_back"] is True
    assert result["transport"] == "stdio"
    assert result["meeting_id"] == "MEETING-W32-DISPOSABLE"
    assert result["identity_id"] == "identity-w32-e2e"
    assert result["meetings_dir"] == str(meetings_dir.resolve())
    assert instances[0].session_opened is True
    assert instances[0].session_closed is True
    assert instances[0].config.cwd == str(Path(browser_adapter.__file__).resolve().parents[2])
    assert instances[0].config.env["ROOM_HOP_MEETINGS_DIR"] == str(meetings_dir.resolve())
    assert [call[0] for call in instances[0].calls] == [
        "list_meetings",
        "get_meeting",
        "add_paste_to_meeting",
        "get_transcript",
    ]
    assert instances[0].calls[2] == (
        "add_paste_to_meeting",
        "MEETING-W32-DISPOSABLE",
        "identity-w32-e2e",
    )
