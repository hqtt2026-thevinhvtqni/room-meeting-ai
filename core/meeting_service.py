"""
ROOM HOP Public Service Interface v0.1.

Facade for MCP (and future external interfaces).
- No business logic (pure delegation)
- No direct storage access
- Returns DTOs, not internal models
- Enforces governance via Governance.can_access_meeting()

Resolves: Architecture Block G3
"""
from __future__ import annotations

from typing import List, Optional

from core.governance import GOV
from core.meeting_manager import MeetingManager, MeetingError


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


class MeetingDTO:
    """Public DTO for meeting metadata. No internal model leakage."""
    def __init__(
        self,
        meeting_id: str,
        title: str,
        status: str,
        created_at: str,
    ):
        self.meeting_id = meeting_id
        self.title = title
        self.status = status
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "meeting_id": self.meeting_id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }


class TranscriptMessageDTO:
    """
    Public DTO for transcript message.

    Schema follows Core canonical format:
    index / type / speaker / timestamp / content / file

    Preserves provenance. No AI modification.
    """
    def __init__(
        self,
        index: int,
        type: str,
        speaker: str,
        timestamp: str,
        content: str,
        file: Optional[str] = None,
    ):
        self.index = index
        self.type = type
        self.speaker = speaker
        self.timestamp = timestamp
        self.content = content
        self.file = file

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "type": self.type,
            "speaker": self.speaker,
            "timestamp": self.timestamp,
            "content": self.content,
            "file": self.file,
        }


class MeetingService:
    """
    Public facade for ROOM HOP Core.

    Delegates to:
    - MeetingManager (meeting lifecycle + transcript)
    - Governance (access control)

    Returns DTOs. Raises semantic errors. No storage access.

    Identity propagation:
    - requester_identity là BẮT BUỘC, không có default
    - MCP server phải inject identity từ config/env
    - Nếu không có identity → raise ValueError
    """

    def __init__(
        self,
        manager: MeetingManager,
        governance=GOV,
        requester_identity: str | None = None,
    ):
        if not requester_identity:
            raise ValueError(
                "MeetingService requires requester_identity. "
                "MCP server must inject identity from config/env."
            )

        self.manager = manager
        self.governance = governance
        self.requester_identity = requester_identity

    def list_meetings(
        self,
        limit: Optional[int] = None,
        status: Optional[str] = None,
    ) -> List[MeetingDTO]:
        """
        List meetings with optional filters.
        Delegates to MeetingManager.list_meetings().
        """
        raw_meetings = self.manager.list_meetings(limit=limit, status=status)
        return [self._to_meeting_dto(data) for data in raw_meetings]

    def get_meeting(self, meeting_id: str) -> MeetingDTO:
        """
        Get meeting by ID.
        Checks governance, delegates to MeetingManager.get_meeting().
        """
        if not self.governance.can_access_meeting(
            self.requester_identity, meeting_id, "READ"
        ):
            raise GovernanceDeniedError(
                f"Identity '{self.requester_identity}' cannot read meeting '{meeting_id}'"
            )

        try:
            meeting = self.manager.get_meeting(meeting_id)
        except MeetingError as e:
            raise MeetingNotFoundError(meeting_id) from e

        return self._to_meeting_dto(meeting.data)

    def get_transcript(self, meeting_id: str) -> List[TranscriptMessageDTO]:
        """
        Get transcript for a meeting.
        Checks governance, delegates to Meeting.get_transcript().
        Preserves provenance (speaker, timestamp, content, file, type).
        """
        if not self.governance.can_access_meeting(
            self.requester_identity, meeting_id, "READ"
        ):
            raise GovernanceDeniedError(
                f"Identity '{self.requester_identity}' cannot read meeting '{meeting_id}'"
            )

        try:
            meeting = self.manager.get_meeting(meeting_id)
        except MeetingError as e:
            raise MeetingNotFoundError(meeting_id) from e

        raw_entries = meeting.get_transcript()
        return [self._to_transcript_dto(entry) for entry in raw_entries]

    def _to_meeting_dto(self, data: dict) -> MeetingDTO:
        """Map internal meeting dict to MeetingDTO."""
        return MeetingDTO(
            meeting_id=data["id"],
            title=data["topic"],
            status=data["status"],
            created_at=data["created_at"],
        )

    def _to_transcript_dto(self, entry: dict) -> TranscriptMessageDTO:
        """Map Core transcript entry to TranscriptMessageDTO. Preserves provenance."""
        return TranscriptMessageDTO(
            index=entry["index"],
            type=entry.get("type", "message"),
            speaker=entry["speaker"],
            timestamp=entry["timestamp"],
            content=entry["content"],
            file=entry.get("file"),
        )
