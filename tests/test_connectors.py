import pytest

from core.agent_registry import AgentRegistry
from core.connectors import (
    AnthropicConnector,
    ConnectorError,
    MockConnector,
    OpenAIConnector,
    TurnStatus,
    parse_agent_output,
)


def test_parse_reply_status():
    raw = "STATUS: REPLY\nĐây là nội dung phản hồi."
    result = parse_agent_output(raw)
    assert result.status == TurnStatus.REPLY
    assert result.content == "Đây là nội dung phản hồi."


def test_parse_pass_status_has_empty_content():
    raw = "STATUS: PASS\n(một số nội dung thừa không nên xuất hiện)"
    result = parse_agent_output(raw)
    assert result.status == TurnStatus.PASS
    assert result.content == ""


def test_parse_final_status():
    raw = "STATUS: FINAL\nChốt: chọn phương án A."
    result = parse_agent_output(raw)
    assert result.status == TurnStatus.FINAL
    assert "chọn phương án A" in result.content


def test_parse_status_case_insensitive():
    raw = "status: reply\nNội dung"
    result = parse_agent_output(raw)
    assert result.status == TurnStatus.REPLY


def test_parse_missing_status_falls_back_to_reply():
    """Model quên format -> KHÔNG được raise lỗi, phải fallback an toàn."""
    raw = "Model quên viết STATUS nhưng vẫn có nội dung hữu ích."
    result = parse_agent_output(raw)
    assert result.status == TurnStatus.REPLY
    assert result.content == raw.strip()


def test_mock_connector_cycles_through_script():
    registry = AgentRegistry()
    from core.connectors import AgentResponse

    conn = MockConnector(
        registry.get("xu"),
        [AgentResponse(TurnStatus.REPLY, "một"), AgentResponse(TurnStatus.PASS, "")],
    )
    from core.connectors import MeetingContextForAgent

    ctx = MeetingContextForAgent(topic="t", context_text="", history=[], agent=registry.get("xu"))
    r1 = conn.send_turn(ctx)
    r2 = conn.send_turn(ctx)
    assert r1.content == "một"
    assert r2.status == TurnStatus.PASS


def test_mock_connector_exhausted_script_returns_pass_not_crash():
    registry = AgentRegistry()
    conn = MockConnector(registry.get("xu"), [])
    from core.connectors import MeetingContextForAgent

    ctx = MeetingContextForAgent(topic="t", context_text="", history=[], agent=registry.get("xu"))
    result = conn.send_turn(ctx)
    assert result.status == TurnStatus.PASS


def test_anthropic_connector_requires_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    registry = AgentRegistry()
    with pytest.raises(ConnectorError):
        AnthropicConnector(registry.get("claude"), api_key=None)


def test_anthropic_connector_requires_model_field(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-test")
    registry = AgentRegistry()
    claude = registry.get("claude")
    assert claude.model == ""  # chưa điền model thật trong agents/claude.yaml
    with pytest.raises(ConnectorError):
        AnthropicConnector(claude)


def test_openai_connector_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    registry = AgentRegistry()
    with pytest.raises(ConnectorError):
        OpenAIConnector(registry.get("xu"), api_key=None)
