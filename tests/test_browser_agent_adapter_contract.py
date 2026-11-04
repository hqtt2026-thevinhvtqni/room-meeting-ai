import json

from room_hop_mcp.browser_agent_adapter import adapter as browser_adapter

EXPECTED_TOOLS = {
    "list_meetings", "get_meeting", "get_transcript", "add_paste_to_meeting"
}
RESULT = {
    "execution_id": "exec-test-001",
    "evidence_id": "evidence-test-001",
    "work_id": "work-32-test",
    "evidence_json": "/tmp/workflow-evidence.json",
    "final_url": "https://example.com/",
    "page_title": "Example Domain",
}

def _rpc(value):
    return {"result": {"content": [{"type": "json", "json": value}]}}

def _configure_test_target(monkeypatch):
    monkeypatch.setenv("ROOMHOP_MCP_URL", "http://127.0.0.1:9999/mcp")
    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_TEST_MEETING_ID", "MEETING-W32-DISPOSABLE")
    monkeypatch.setenv("ROOMHOP_TEST_IDENTITY_ID", "identity-w32-e2e")

def test_submission_is_blocked_without_explicit_test_mode(monkeypatch):
    monkeypatch.setenv("ROOMHOP_MCP_URL", "http://127.0.0.1:9999/mcp")
    monkeypatch.delenv("ROOMHOP_TEST_MODE", raising=False)
    calls = []
    monkeypatch.setattr(browser_adapter, "roomhop_tools_list", lambda: calls.append("tools"))
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_MODE=1" in result["reason"]
    assert calls == []

def test_submission_rejects_extra_or_missing_public_tools(monkeypatch):
    _configure_test_target(monkeypatch)
    monkeypatch.setattr(
        browser_adapter, "roomhop_tools_list",
        lambda: [{"name": name} for name in EXPECTED_TOOLS | {"join_meeting"}],
    )
    calls = []
    monkeypatch.setattr(browser_adapter, "roomhop_tool_call", lambda *args, **kwargs: calls.append(args))
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert result["expected_tools"] == sorted(EXPECTED_TOOLS)
    assert "join_meeting" in result["actual_tools"]
    assert calls == []

def test_submission_does_not_fall_back_when_explicit_test_meeting_missing(monkeypatch):
    _configure_test_target(monkeypatch)
    monkeypatch.setattr(
        browser_adapter, "roomhop_tools_list",
        lambda: [{"name": name} for name in EXPECTED_TOOLS],
    )
    calls = []
    def fake_call(name, arguments=None):
        calls.append((name, arguments))
        return _rpc({"meetings": [{"id": "REAL-MEETING", "status": "active"}]})
    monkeypatch.setattr(browser_adapter, "roomhop_tool_call", fake_call)
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "no fallback" in result["reason"]
    assert [name for name, _ in calls] == ["list_meetings"]

def test_submission_requires_explicit_test_identity(monkeypatch):
    _configure_test_target(monkeypatch)
    monkeypatch.delenv("ROOMHOP_TEST_IDENTITY_ID")
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_IDENTITY_ID" in result["reason"]

def test_submission_uses_exact_test_target_and_verifies_readback(monkeypatch):
    _configure_test_target(monkeypatch)
    monkeypatch.setattr(
        browser_adapter, "roomhop_tools_list",
        lambda: [{"name": name} for name in EXPECTED_TOOLS],
    )
    transcript, calls = [], []
    def fake_call(name, arguments=None):
        calls.append((name, arguments))
        if name == "list_meetings":
            return _rpc({"meetings": [
                {"id": "REAL-MEETING", "status": "active"},
                {"id": "MEETING-W32-DISPOSABLE", "status": "active"},
            ]})
        if name == "add_paste_to_meeting":
            transcript.append(arguments["text"])
            return _rpc({"accepted": True})
        if name == "get_transcript":
            assert arguments == {"meeting_id": "MEETING-W32-DISPOSABLE"}
            return _rpc({"transcript": transcript})
        raise AssertionError(f"Unexpected MCP tool call: {name}")
    monkeypatch.setattr(browser_adapter, "roomhop_tool_call", fake_call)
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "pass"
    assert result["read_back"] is True
    assert result["meeting_id"] == "MEETING-W32-DISPOSABLE"
    assert result["identity_id"] == "identity-w32-e2e"
    assert [name for name, _ in calls] == [
        "list_meetings", "add_paste_to_meeting", "get_transcript"
    ]
    append_args = calls[1][1]
    assert append_args["meeting_id"] == "MEETING-W32-DISPOSABLE"
    assert append_args["identity_id"] == "identity-w32-e2e"
    artifact = json.loads(transcript[0].split(" ", 1)[1])
    assert artifact["execution_id"] == RESULT["execution_id"]
    assert artifact["evidence_id"] == RESULT["evidence_id"]
    assert artifact["work_id"] == RESULT["work_id"]
    assert artifact["evidence_json"] == "workflow-evidence.json"
