from core.meeting_manager import MeetingManager, MeetingError
from core.secretary import Secretary


def test_lifecycle_join_start_and_secretary(tmp_path):
    manager = MeetingManager(meetings_dir=tmp_path / "meetings")
    meeting = manager.create_meeting(
        "MEETING-LIFE-001", "Secretary integration", ["xu"], [], created_by="vinh"
    )
    assert meeting.data["status"] == "draft"

    meeting.open_session()
    assert meeting.data["status"] == "open"

    xu_evidence = meeting.join_request("xu")
    vinh_evidence = meeting.join_request("vinh")
    assert xu_evidence["authorization"]["registry_check"] == "REQUIRED_PASS"
    assert vinh_evidence["authorization"]["registry_check"] == "NOT_APPLICABLE"

    meeting.start("vinh")
    assert meeting.data["status"] == "active"

    meeting.add_message("vinh", "SECRETARY_INTEGRATION_TEST_001")
    secretary = Secretary(tmp_path / "transcript.txt")
    result = secretary.append("vinh: SECRETARY_INTEGRATION_TEST_001")
    assert result == {"status": "READY"}
    assert "SECRETARY_INTEGRATION_TEST_001" in (tmp_path / "transcript.txt").read_text(encoding="utf-8")


def test_start_requires_two_accepted_participants(tmp_path):
    manager = MeetingManager(meetings_dir=tmp_path / "meetings")
    meeting = manager.create_meeting("MEETING-LIFE-002", "quorum", ["xu"], [], created_by="vinh")
    meeting.open_session()
    meeting.join_request("xu")
    try:
        meeting.start("xu")
    except MeetingError as exc:
        assert "2 participants" in str(exc)
    else:
        raise AssertionError("START phải bị chặn khi chưa đủ 2 participants")
