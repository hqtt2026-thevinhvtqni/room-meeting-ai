import pytest

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError, MeetingManager
from core.meeting_service import MeetingService


@pytest.fixture
def service(tmp_path):
    registry = AgentRegistry()
    manager = MeetingManager(
        registry=registry,
        meetings_dir=tmp_path / "meetings",
    )
    return MeetingService(manager)


def _activate(
    service,
    meeting_id,
    joiners=("xu", "claude"),
    starter=None,
):
    service.open_meeting(meeting_id)

    for identity_id in joiners:
        service.join_meeting(
            meeting_id,
            identity_id,
        )

    service.start_meeting(
        meeting_id,
        starter=starter or joiners[0],
    )


def test_create_returns_state_snapshot(service):
    result = service.create_meeting(
        meeting_id="SERVICE-001",
        topic="Service boundary",
        participants=["xu", "claude"],
        context_files=["XU_CORE.md"],
    )

    assert isinstance(result, dict)
    assert result["id"] == "SERVICE-001"
    assert result["status"] == "draft"
    assert result["participants"] == []


def test_get_returns_state_snapshot_not_meeting_object(service):
    service.create_meeting(
        meeting_id="SERVICE-002",
        topic="Get",
        participants=["xu", "claude"],
        context_files=[],
    )

    result = service.get_meeting("SERVICE-002")

    assert isinstance(result, dict)
    assert result["status"] == "draft"
    assert not hasattr(result, "open_session")


def test_service_delegates_lifecycle(service):
    service.create_meeting(
        meeting_id="SERVICE-003",
        topic="Lifecycle",
        participants=["xu", "claude"],
        context_files=[],
    )

    assert service.get_meeting("SERVICE-003")["status"] == "draft"

    service.open_meeting("SERVICE-003")

    assert service.get_meeting("SERVICE-003")["status"] == "open"

    service.join_meeting("SERVICE-003", "xu")
    service.join_meeting("SERVICE-003", "claude")

    service.start_meeting(
        "SERVICE-003",
        starter="xu",
    )

    assert service.get_meeting("SERVICE-003")["status"] == "active"


def test_add_message_through_service(service):
    service.create_meeting(
        meeting_id="SERVICE-004",
        topic="Message",
        participants=["xu", "claude"],
        context_files=[],
    )

    _activate(service, "SERVICE-004")

    path = service.add_message(
        "SERVICE-004",
        "xu",
        "Xin chào",
    )

    assert isinstance(path, str)
    assert path.endswith(".md")
    assert "messages" in path


def test_add_paste_through_service(service):
    service.create_meeting(
        meeting_id="SERVICE-005",
        topic="Paste",
        participants=["xu", "claude"],
        context_files=[],
    )

    _activate(service, "SERVICE-005")

    result = service.add_paste(
        "SERVICE-005",
        "RAW TRANSCRIPT",
    )

    assert isinstance(result, dict)


def test_request_close_and_close_through_service(service):
    service.create_meeting(
        meeting_id="SERVICE-006",
        topic="Close",
        participants=["xu", "claude"],
        context_files=[],
    )

    _activate(service, "SERVICE-006")

    state = service.request_close(
        "SERVICE-006",
        requester="vinh",
    )

    assert state["status"] == "closing"

    final_path = service.close_meeting(
        "SERVICE-006",
        decisions=["OK"],
        action_items=[],
        summary="Done",
        closer="xu",
    )

    assert isinstance(final_path, str)
    assert final_path.endswith("final.md")
    assert service.get_meeting("SERVICE-006")["status"] == "closed"


def test_missing_meeting_preserves_core_error(service):
    with pytest.raises(MeetingError):
        service.get_meeting("NOT-EXIST")


def test_list_meetings_returns_snapshots(service):
    service.create_meeting(
        meeting_id="SERVICE-LIST-001",
        topic="First",
        participants=["xu", "claude"],
        context_files=[],
    )

    service.create_meeting(
        meeting_id="SERVICE-LIST-002",
        topic="Second",
        participants=["xu", "claude"],
        context_files=[],
    )

    result = service.list_meetings()

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)

    ids = {item["id"] for item in result}

    assert ids == {
        "SERVICE-LIST-001",
        "SERVICE-LIST-002",
    }


def test_list_meetings_filters_status(service):
    service.create_meeting(
        meeting_id="SERVICE-LIST-003",
        topic="Draft",
        participants=["xu", "claude"],
        context_files=[],
    )

    service.create_meeting(
        meeting_id="SERVICE-LIST-004",
        topic="Active",
        participants=["xu", "claude"],
        context_files=[],
    )

    _activate(
        service,
        "SERVICE-LIST-004",
    )

    result = service.list_meetings(
        status="active",
    )

    assert len(result) == 1
    assert result[0]["id"] == "SERVICE-LIST-004"
    assert result[0]["status"] == "active"


def test_list_meetings_respects_limit(service):
    for index in range(3):
        service.create_meeting(
            meeting_id=f"SERVICE-LIMIT-{index}",
            topic=f"Meeting {index}",
            participants=["xu", "claude"],
            context_files=[],
        )

    result = service.list_meetings(limit=2)

    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)


def test_get_transcript_through_service(service):
    service.create_meeting(
        meeting_id="SERVICE-TRANSCRIPT-001",
        topic="Transcript",
        participants=["xu", "claude"],
        context_files=[],
    )

    _activate(
        service,
        "SERVICE-TRANSCRIPT-001",
    )

    service.add_message(
        "SERVICE-TRANSCRIPT-001",
        "xu",
        "Nội dung thứ nhất.",
    )

    service.add_message(
        "SERVICE-TRANSCRIPT-001",
        "claude",
        "Nội dung thứ hai.",
    )

    result = service.get_transcript(
        "SERVICE-TRANSCRIPT-001",
    )

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0]["speaker"] == "xu"
    assert result[0]["content"] == "Nội dung thứ nhất."
    assert result[0]["type"] == "message"
    assert "timestamp" in result[0]
    assert "index" in result[0]
    assert "file" in result[0]

    assert result[1]["speaker"] == "claude"
    assert result[1]["content"] == "Nội dung thứ hai."