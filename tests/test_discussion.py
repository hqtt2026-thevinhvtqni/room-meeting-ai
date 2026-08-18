import pytest

from core.agent_registry import AgentRegistry
from core.connectors import AgentResponse, MockConnector, TurnStatus
from core.discussion import run_discussion
from core.meeting_manager import MeetingManager


@pytest.fixture
def manager(tmp_path):
    registry = AgentRegistry()
    return MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")


def _make_meeting(manager, meeting_id):
    meeting = manager.create_meeting(
        meeting_id=meeting_id,
        topic="Test discussion",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    # Lifecycle v0.2.1: Discussion chỉ chạy khi Meeting ACTIVE.
    meeting.open_session()
    meeting.join_request("xu")
    meeting.join_request("claude")
    meeting.start("xu")
    return meeting


def test_stops_on_final(manager):
    meeting = _make_meeting(manager, "DISC-FINAL")

    xu_conn = MockConnector(
        manager.registry.get("xu"),
        [AgentResponse(TurnStatus.REPLY, "Xu nói lượt 1")],
    )
    claude_conn = MockConnector(
        manager.registry.get("claude"),
        [AgentResponse(TurnStatus.FINAL, "Claude cho là đã đủ, chốt luôn")],
    )

    result = run_discussion(meeting, {"xu": xu_conn, "claude": claude_conn})

    assert result.stop_reason == "final"
    assert result.rounds_used == 2  # xu nói 1 lượt, claude nói 1 lượt rồi FINAL
    messages = meeting.log.read_all_messages()
    assert len(messages) == 2
    assert messages[-1]["content"] == "Claude cho là đã đủ, chốt luôn"


def test_stops_on_consecutive_pass(manager):
    meeting = _make_meeting(manager, "DISC-PASS")

    # xu REPLY rồi PASS, claude PASS rồi PASS -> 2 PASS liên tiếp (claude, xu) phải dừng
    xu_conn = MockConnector(
        manager.registry.get("xu"),
        [
            AgentResponse(TurnStatus.REPLY, "Xu mở đầu"),
            AgentResponse(TurnStatus.PASS, ""),
        ],
    )
    claude_conn = MockConnector(
        manager.registry.get("claude"),
        [
            AgentResponse(TurnStatus.PASS, ""),
            AgentResponse(TurnStatus.PASS, ""),
        ],
    )

    result = run_discussion(
        meeting,
        {"xu": xu_conn, "claude": claude_conn},
        max_consecutive_pass=2,
    )

    assert result.stop_reason == "consecutive_pass"
    messages = meeting.log.read_all_messages()
    # chỉ có 1 message thật (Xu mở đầu), các PASS không tạo message
    assert len(messages) == 1

    events = meeting.log.read_all_events()
    pass_events = [e for e in events if e["type"] == "event" and e["action"] == "agent_pass"]
    assert len(pass_events) == 2


def test_stops_on_max_rounds(manager):
    meeting = _make_meeting(manager, "DISC-MAXROUND")

    # Cả 2 agent luôn REPLY -> không bao giờ tự dừng -> phải bị Room chặn ở max_rounds
    xu_conn = MockConnector(
        manager.registry.get("xu"),
        [AgentResponse(TurnStatus.REPLY, f"Xu vòng {i}") for i in range(10)],
    )
    claude_conn = MockConnector(
        manager.registry.get("claude"),
        [AgentResponse(TurnStatus.REPLY, f"Claude vòng {i}") for i in range(10)],
    )

    result = run_discussion(
        meeting,
        {"xu": xu_conn, "claude": claude_conn},
        max_rounds=4,
        max_consecutive_pass=2,
    )

    assert result.stop_reason == "max_rounds"
    assert result.rounds_used == 4
    messages = meeting.log.read_all_messages()
    assert len(messages) == 4


def test_missing_connector_raises(manager):
    meeting = _make_meeting(manager, "DISC-MISSING")
    xu_conn = MockConnector(manager.registry.get("xu"), [])
    with pytest.raises(ValueError):
        run_discussion(meeting, {"xu": xu_conn})  # thiếu connector cho claude


def test_history_grows_across_turns(manager):
    """Xác nhận agent lượt sau nhận được đầy đủ history của lượt trước (qua context truyền vào)."""
    meeting = _make_meeting(manager, "DISC-HISTORY")

    captured_histories = []

    class RecordingConnector(MockConnector):
        def send_turn(self, context):
            captured_histories.append([h["content"] for h in context.history])
            return super().send_turn(context)

    xu_conn = RecordingConnector(
        manager.registry.get("xu"),
        [AgentResponse(TurnStatus.REPLY, "Xu: mở đầu")],
    )
    claude_conn = RecordingConnector(
        manager.registry.get("claude"),
        [AgentResponse(TurnStatus.FINAL, "Claude: chốt")],
    )

    run_discussion(meeting, {"xu": xu_conn, "claude": claude_conn})

    # Lượt đầu tiên (Xu) chưa có history
    assert captured_histories[0] == []
    # Lượt thứ hai (Claude) phải thấy được message của Xu trước đó
    assert captured_histories[1] == ["Xu: mở đầu"]
