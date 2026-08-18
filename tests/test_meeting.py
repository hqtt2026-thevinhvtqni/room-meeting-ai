import pytest

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError, MeetingManager


@pytest.fixture
def manager(tmp_path):
    registry = AgentRegistry()  # dùng agents/ thật (xu, claude, cto...) — read-only
    return MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")


def _activate(meeting, joiners=("xu", "claude"), starter=None):
    """
    Đưa meeting từ draft -> active theo đúng lifecycle v0.2.1:
    create (draft) -> open_session (open) -> join_request mỗi joiner
    (JOIN_ACCEPTED) -> start (active).
    """
    meeting.open_session()
    for identity_id in joiners:
        meeting.join_request(identity_id)
    meeting.start(starter or joiners[0])
    return meeting


def test_create_meeting_with_valid_participants(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-001",
        topic="Test meeting",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    # Lifecycle v0.2.1: create_meeting() chỉ tạo DRAFT + danh sách INVITE.
    # participants thật (đã JOIN_ACCEPTED) còn rỗng cho tới khi join_request().
    assert meeting.data["status"] == "draft"
    assert meeting.data["invited_participants"] == ["xu", "claude"]
    assert meeting.data["participants"] == []


def test_create_meeting_with_unknown_participant_raises(manager):
    with pytest.raises(MeetingError):
        manager.create_meeting(
            meeting_id="TEST-002",
            topic="Test meeting",
            participants=["xu", "ma_khong_ton_tai"],
            context_files=["XU_CORE.md"],
        )


def test_create_duplicate_meeting_id_raises(manager):
    manager.create_meeting(
        meeting_id="TEST-003",
        topic="First",
        participants=["xu"],
        context_files=["XU_CORE.md"],
    )
    with pytest.raises(MeetingError):
        manager.create_meeting(
            meeting_id="TEST-003",
            topic="Duplicate",
            participants=["xu"],
            context_files=["XU_CORE.md"],
        )


def test_join_request_before_open_session_raises(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-004b",
        topic="Test",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    with pytest.raises(MeetingError):
        meeting.join_request("xu")  # còn draft, chưa open_session()


def test_start_requires_at_least_two_join_accepted(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-004c",
        topic="Test",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    meeting.open_session()
    meeting.join_request("xu")  # chỉ 1 người join
    with pytest.raises(MeetingError):
        meeting.start("xu")


def test_add_message_from_participant(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-004",
        topic="Test",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    _activate(meeting)
    meeting.add_message("xu", "Xin chào")
    messages = meeting.log.read_all_messages()
    assert len(messages) == 1
    assert messages[0]["speaker"] == "xu"


def test_add_message_from_non_participant_raises(manager):
    # claude được MỜI nhưng không join — chỉ xu và cto join (đủ 2 để start()).
    meeting = manager.create_meeting(
        meeting_id="TEST-005",
        topic="Test",
        participants=["xu", "claude", "cto"],
        context_files=["XU_CORE.md"],
    )
    _activate(meeting, joiners=("xu", "cto"), starter="xu")
    with pytest.raises(MeetingError):
        meeting.add_message("claude", "Tôi không được mời tham gia thật")


def test_cannot_add_message_after_close(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-006",
        topic="Test",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )
    _activate(meeting)
    meeting.add_message("xu", "Một tin nhắn")
    meeting.close(decisions=["ok"], action_items=[], summary="done")
    with pytest.raises(MeetingError):
        meeting.add_message("xu", "Quá muộn")


def test_close_generates_final_md(manager):
    meeting = manager.create_meeting(
        meeting_id="TEST-007",
        topic="Test",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md", "XU_SESSION.md"],
    )
    _activate(meeting)
    meeting.add_message("xu", "Đề xuất A")
    meeting.add_message("claude", "Đồng ý A")
    final_path = meeting.close(
        decisions=["Chọn phương án A"],
        action_items=["Claude triển khai"],
        summary="Đã thống nhất phương án A",
    )
    assert final_path.exists()
    content = final_path.read_text(encoding="utf-8")
    assert "Chọn phương án A" in content
    assert "Claude triển khai" in content
    assert meeting.data["status"] == "closed"


def test_get_meeting_not_found_raises(manager):
    with pytest.raises(MeetingError):
        manager.get_meeting("KHONG_TON_TAI")
