"""Tests for MeetingService — Public Core Boundary."""
import pytest
from unittest.mock import Mock
from pathlib import Path

from core.meeting_service import (
    MeetingService,
    MeetingNotFoundError,
    GovernanceDeniedError,
    MeetingDTO,
    TranscriptMessageDTO,
)
from core.meeting_manager import MeetingError


@pytest.fixture
def mock_manager():
    manager = Mock()
    manager.list_meetings.return_value = []
    manager.get_meeting.return_value = None
    return manager


@pytest.fixture
def mock_governance():
    governance = Mock()
    governance.can_access_meeting.return_value = True
    return governance


@pytest.fixture
def service(mock_manager, mock_governance):
    return MeetingService(
        manager=mock_manager,
        governance=mock_governance,
        requester_identity="vinh",
    )


# === Identity propagation ===

class TestIdentityPropagation:
    def test_service_requires_identity(self, mock_manager, mock_governance):
        """MeetingService must have requester_identity, no default."""
        with pytest.raises(ValueError, match="requires requester_identity"):
            MeetingService(manager=mock_manager, governance=mock_governance)

    def test_service_uses_provided_identity(self, mock_manager, mock_governance):
        """Service uses the identity provided, not hard-coded."""
        service = MeetingService(
            manager=mock_manager,
            governance=mock_governance,
            requester_identity="xu",
        )
        assert service.requester_identity == "xu"

    def test_get_meeting_checks_correct_identity(self, service, mock_manager, mock_governance):
        """Verify governance check uses the service's identity."""
        mock_meeting = Mock()
        mock_meeting.data = {"id": "m1", "topic": "T", "status": "active", "created_at": "t1"}
        mock_manager.get_meeting.return_value = mock_meeting
        mock_governance.can_access_meeting.return_value = True

        service.get_meeting("m1")

        mock_governance.can_access_meeting.assert_called_once_with("vinh", "m1", "READ")


# === list_meetings ===

class TestListMeetings:
    def test_empty_list(self, service, mock_manager):
        mock_manager.list_meetings.return_value = []
        result = service.list_meetings()
        assert result == []
        mock_manager.list_meetings.assert_called_once_with(limit=None, status=None)

    def test_one_meeting_returns_dto(self, service, mock_manager):
        mock_manager.list_meetings.return_value = [{
            "id": "m1",
            "topic": "Test Topic",
            "status": "active",
            "created_at": "2026-08-21T10:00:00",
        }]
        result = service.list_meetings()
        assert len(result) == 1
        assert isinstance(result[0], MeetingDTO)
        assert result[0].meeting_id == "m1"
        assert result[0].title == "Test Topic"

    def test_multiple_meetings(self, service, mock_manager):
        mock_manager.list_meetings.return_value = [
            {"id": "m1", "topic": "T1", "status": "active", "created_at": "t1"},
            {"id": "m2", "topic": "T2", "status": "closed", "created_at": "t2"},
        ]
        result = service.list_meetings()
        assert len(result) == 2

    def test_does_not_mutate_storage(self, service, mock_manager):
        original_data = [{"id": "m1", "topic": "T1", "status": "active", "created_at": "t1"}]
        mock_manager.list_meetings.return_value = original_data
        service.list_meetings()
        assert original_data[0] == {"id": "m1", "topic": "T1", "status": "active", "created_at": "t1"}


# === get_meeting ===

class TestGetMeeting:
    def test_success_returns_dto(self, service, mock_manager, mock_governance):
        mock_meeting = Mock()
        mock_meeting.data = {
            "id": "m1",
            "topic": "Test",
            "status": "active",
            "created_at": "2026-08-21",
        }
        mock_manager.get_meeting.return_value = mock_meeting
        mock_governance.can_access_meeting.return_value = True

        result = service.get_meeting("m1")

        assert isinstance(result, MeetingDTO)
        assert result.meeting_id == "m1"
        mock_governance.can_access_meeting.assert_called_once_with("vinh", "m1", "READ")

    def test_not_found_raises(self, service, mock_manager, mock_governance):
        mock_manager.get_meeting.side_effect = MeetingError("not found")
        mock_governance.can_access_meeting.return_value = True

        with pytest.raises(MeetingNotFoundError) as exc_info:
            service.get_meeting("nonexistent")
        assert exc_info.value.meeting_id == "nonexistent"

    def test_governance_denied_raises(self, service, mock_governance):
        mock_governance.can_access_meeting.return_value = False

        with pytest.raises(GovernanceDeniedError):
            service.get_meeting("m1")


# === get_transcript ===

class TestGetTranscript:
    def test_provenance_preserved(self, service, mock_manager, mock_governance):
        mock_meeting = Mock()
        mock_meeting.get_transcript.return_value = [
            {
                "index": 1,
                "type": "message",
                "speaker": "vinh",
                "timestamp": "2026-08-21T10:00:00",
                "content": "Raw content from source",
                "file": None,
            }
        ]
        mock_manager.get_meeting.return_value = mock_meeting
        mock_governance.can_access_meeting.return_value = True

        result = service.get_transcript("m1")

        assert len(result) == 1
        assert isinstance(result[0], TranscriptMessageDTO)
        assert result[0].content == "Raw content from source"
        assert result[0].speaker == "vinh"

    def test_not_found_raises(self, service, mock_manager, mock_governance):
        mock_manager.get_meeting.side_effect = MeetingError("not found")
        mock_governance.can_access_meeting.return_value = True

        with pytest.raises(MeetingNotFoundError):
            service.get_transcript("nonexistent")

    def test_governance_denied_raises(self, service, mock_governance):
        mock_governance.can_access_meeting.return_value = False

        with pytest.raises(GovernanceDeniedError):
            service.get_transcript("m1")


# === DTO Boundary ===

class TestDTOBoundary:
    def test_meeting_dto_does_not_leak_internal(self, service, mock_manager, mock_governance):
        mock_meeting = Mock()
        mock_meeting.data = {
            "id": "m1",
            "topic": "Test",
            "status": "active",
            "created_at": "t1",
            "participants": ["vinh"],
            "join_records": [],
        }
        mock_manager.get_meeting.return_value = mock_meeting
        mock_governance.can_access_meeting.return_value = True

        result = service.get_meeting("m1")
        result_dict = result.to_dict()

        assert set(result_dict.keys()) == {"meeting_id", "title", "status", "created_at"}
        assert "participants" not in result_dict

    def test_transcript_dto_preserves_canonical_schema(self, service, mock_manager, mock_governance):
        mock_meeting = Mock()
        mock_meeting.get_transcript.return_value = [
            {
                "index": 1,
                "type": "message",
                "speaker": "vinh",
                "timestamp": "t1",
                "content": "hello",
                "file": None,
            }
        ]
        mock_manager.get_meeting.return_value = mock_meeting
        mock_governance.can_access_meeting.return_value = True

        result = service.get_transcript("m1")
        result_dict = result[0].to_dict()

        assert set(result_dict.keys()) == {"index", "type", "speaker", "timestamp", "content", "file"}
