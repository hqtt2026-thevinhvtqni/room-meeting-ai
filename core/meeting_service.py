"""
Public Service Interface for ROOM HOP Core.

This is the facade that MCP (and other external interfaces) must use.
- No direct storage access
- No business logic (pure delegation)
- Returns DTOs, not internal models
- Enforces governance checks

Resolves: Architecture Block G3
"""
from typing import List, Optional
from datetime import datetime

# Core DTOs (import từ MCP hoặc định nghĩa riêng trong core)
from room_meeting_ai.mcp.dtos import MeetingDTO, TranscriptMessageDTO


class MeetingNotFoundError(Exception):
    """Raised when a meeting does not exist."""
    def __init__(self, meeting_id: str):
        super().__init__(f"Meeting not found: {meeting_id}")
        self.meeting_id = meeting_id


class GovernanceDeniedError(Exception):
    """Raised when governance policy denies access."""
    def __init__(self, reason: str):
        super().__init__(f"Governance denied: {reason}")
        self.reason = reason


class MeetingService:
    """
    Public facade for ROOM HOP Core.

    Delegates to:
    - MeetingManager (meeting lifecycle)
    - Secretary (transcript/messages)
    - Governance (access control)

    Returns DTOs. Raises semantic errors. No storage access.
    """
    def __init__(self, meeting_manager, secretary, governance):
        self.manager = meeting_manager
        self.secretary = secretary
        self.governance = governance

    def list_meetings(self, limit: int = 10, status: Optional[str] = None) -> List[MeetingDTO]:
        """
        List meetings with optional status filter.
        Delegates to MeetingManager.
        """
        meetings = self.manager.list_meetings(limit=limit, status=status)
        return [self._to_meeting_dto(m) for m in meetings]

    def get_meeting(self, meeting_id: str) -> MeetingDTO:
        """
        Get meeting by ID.
        Checks governance, delegates to MeetingManager.
        Raises MeetingNotFoundError if not found.
        Raises GovernanceDeniedError if access denied.
        """
        if not self.governance.can_access_meeting(meeting_id):
            raise GovernanceDeniedError("Access denied by governance policy")

        meeting = self.manager.get_meeting(meeting_id)
        if not meeting:
            raise MeetingNotFoundError(meeting_id)

        return self._to_meeting_dto(meeting)

    def get_transcript(self, meeting_id: str) -> List[TranscriptMessageDTO]:
        """
        Get transcript for a meeting.
        Checks governance, delegates to Secretary.
        Preserves provenance (speaker, timestamp, source, raw text).
        Raises MeetingNotFoundError if meeting not found.
        Raises GovernanceDeniedError if access denied.
        """
        if not self.governance.can_access_meeting(meeting_id):
            raise GovernanceDeniedError("Access denied by governance policy")

        # Check meeting exists (delegate to manager)
        if not self.manager.get_meeting(meeting_id):
            raise MeetingNotFoundError(meeting_id)

        # Delegate to secretary (raw transcript, no AI modification — G9)
        messages = self.secretary.get_transcript(meeting_id)
        return [self._to_transcript_dto(m) for m in messages]

    def _to_meeting_dto(self, meeting) -> MeetingDTO:
        """Map internal meeting model to MeetingDTO."""
        created_at = meeting.created_at
        if hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        else:
            created_at = str(created_at)

        return MeetingDTO(
            meeting_id=meeting.id,
            title=meeting.title,
            status=meeting.status,
            created_at=created_at
        )

    def _to_transcript_dto(self, message) -> TranscriptMessageDTO:
        """Map internal message model to TranscriptMessageDTO with provenance."""
        timestamp = message.timestamp
        if hasattr(timestamp, 'isoformat'):
            timestamp = timestamp.isoformat()
        else:
            timestamp = str(timestamp)

        return TranscriptMessageDTO(
            message_id=message.id,
            speaker=message.speaker,
            timestamp=timestamp,
            text=message.text,  # Raw text, no AI modification (G9)
            source=getattr(message, 'source', 'unknown')  # Provenance
        )
