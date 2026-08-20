"""
Tests for MeetingService (Public Service Interface).
Uses mocks for Core components to test delegation + DTO mapping + error handling.
"""
import pytest
from unittest.mock import Mock
from datetime import datetime

from core.meeting_service import MeetingService, MeetingNotFoundError, GovernanceDeniedError
from room_meeting_ai.mcp.dtos import MeetingDTO, TranscriptMessageDTO


@pytest.fixture
def mock_manager():
    manager = Mock()
    manager.list_meetings.return_value = []
    manager.get_meeting.return_value = None
    return manager


@pytest.fixture
def mock_secretary():
    secretary = Mock()
    secretary.get_transcript.return_value = []
    return secretary


@pytest.fixture
def mock_governance():
    governance = Mock()
    governance.can_access_meeting.return_value = True
    return governance


@pytest.fixture
def service(mock_manager, mock_secretary, mock_governance):
    return MeetingService(mock_manager, mock_secretary, mock_governance)


def test_list_meetings_returns_dtos(service, mock_manager):
    """Verify list_meetings delegates to manager and returns DTOs."""
    mock_meeting = Mock()
    mock_meeting.id = "m1"
    mock_meeting.title = "Test Meeting"
    mock_meeting.status = "active"
    mock_meeting.created_at = datetime(2026, 8, 21, 10, 0, 0)
    mock_manager.list_meetings.return_value = [mock_meeting]

    result = service.list_meetings(limit=10, status="active")

    assert len(result) == 1
    assert isinstance(result[0], MeetingDTO)
    assert result[0].meeting_id == "m1"
    assert result[0].title == "Test Meeting"
    assert result[0].status == "active"
    mock_manager.list_meetings.assert_called_once_with(limit=10, status="active")


def test_get_meeting_success(service, mock_manager, mock_governance):
    """Verify get_meeting checks governance and returns DTO."""
    mock_meeting = Mock()
    mock_meeting.id = "m1"
    mock_meeting.title = "Test"
    mock_meeting.status = "active"
    mock_meeting.created_at = datetime(2026, 8, 21)
    mock_manager.get_meeting.return_value = mock_meeting
    mock_governance.can_access_meeting.return_value = True

    result = service.get_meeting("m1")

    assert isinstance(result, MeetingDTO)
    assert result.meeting_id == "m1"
    mock_governance.can_access_meeting.assert_called_once_with("m1")


def test_get_meeting_not_found(service, mock_manager):
    """Verify get_meeting raises MeetingNotFoundError when not found."""
    mock_manager.get_meeting.return_value = None

    with pytest.raises(MeetingNotFoundError) as exc_info:
        service.get_meeting("nonexistent")

    assert exc_info.value.meeting_id == "nonexistent"


def test_get_meeting_governance_denied(service, mock_governance):
    """Verify get_meeting raises GovernanceDeniedError when access denied."""
    mock_governance.can_access_meeting.return_value = False

    with pytest.raises(GovernanceDeniedError):
        service.get_meeting("m1")


def test_get_transcript_provenance(service, mock_manager, mock_secretary):
    """Verify get_transcript preserves raw text and provenance (G9)."""
    mock_meeting = Mock()
    mock_manager.get_meeting.return_value = mock_meeting

    mock_message = Mock()
    mock_message.id = "msg1"
    mock_message.speaker = "User"
    mock_message.timestamp = datetime(2026, 8, 21, 10, 0, 0)
    mock_message.text = "Raw text from source"
    mock_message.source = "whisper_v1"
    mock_secretary.get_transcript.return_value = [mock_message]

    result = service.get_transcript("m1")

    assert len(result) == 1
    assert isinstance(result[0], TranscriptMessageDTO)
    assert result[0].text == "Raw text from source"  # Raw, not modified
    assert result[0].source == "whisper_v1"  # Provenance preserved
    assert result[0].speaker == "User"


def test_get_transcript_meeting_not_found(service, mock_manager):
    """Verify get_transcript raises MeetingNotFoundError if meeting doesn't exist."""
    mock_manager.get_meeting.return_value = None

    with pytest.raises(MeetingNotFoundError):
        service.get_transcript("nonexistent")


def test_get_transcript_governance_denied(service, mock_governance):
    """Verify get_transcript raises GovernanceDeniedError if access denied."""
    mock_governance.can_access_meeting.return_value = False

    with pytest.raises(GovernanceDeniedError):
        service.get_transcript("m1")
