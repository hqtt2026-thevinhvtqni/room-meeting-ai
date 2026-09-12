"""Public application boundary for ROOM HOP meetings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.meeting_manager import MeetingError, MeetingManager


class MeetingService:
    """
    Public application/service boundary for Meeting operations.

    External callers must use this service instead of directly depending on
    MeetingManager/Meeting internals.

    V1/V2 deliberately delegates lifecycle and read operations to the
    existing Core. No lifecycle logic is duplicated here.
    """

    def __init__(self, manager: MeetingManager):
        self._manager = manager

    @staticmethod
    def _snapshot(meeting) -> dict[str, Any]:
        """Return a detached Meeting state snapshot."""
        return dict(meeting.data)

    @staticmethod
    def _public_meeting_list_item(
        meeting: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Return the stable public DTO for a meeting list item.

        This mapper prevents internal meeting metadata from leaking through
        the public application boundary.
        """
        return {
            "id": meeting["id"],
            "title": meeting.get(
                "title",
                meeting.get("topic", ""),
            ),
            "status": meeting["status"],
        }

    @staticmethod
    def _public_meeting(
        meeting: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Return the stable public DTO for a single meeting.

        Internal meeting metadata is intentionally excluded from the
        public application boundary.
        """
        return {
            "id": meeting["id"],
            "title": meeting.get(
                "title",
                meeting.get("topic", ""),
            ),
            "status": meeting["status"],
        }

    def create_meeting(
        self,
        meeting_id: str | None,
        topic: str,
        participants: list[str],
        context_files: list[str],
        created_by: str = "vinh",
    ) -> dict[str, Any]:
        # meeting_id=None -> MeetingManager allocates MEETING-YYYY-NNN.
        # meeting_id tường minh -> giữ backward compatibility với caller cũ.
        meeting = self._manager.create_meeting(
            meeting_id=meeting_id,
            topic=topic,
            participants=participants,
            context_files=context_files,
            created_by=created_by,
        )
        return self._snapshot(meeting)

    def get_meeting(
        self,
        meeting_id: str,
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        return self._public_meeting(meeting.data)

    def list_meetings(
        self,
        limit: int | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return public meeting list DTOs.

        Internal MeetingManager metadata is not exposed to callers.
        """
        meetings = self._manager.list_meetings(
            limit=limit,
            status=status,
        )

        return [
            self._public_meeting_list_item(meeting)
            for meeting in meetings
        ]

    def get_transcript(
        self,
        meeting_id: str,
    ) -> list[dict[str, Any]]:
        """
        Return the existing Core transcript evidence.

        No filesystem access is exposed to callers.
        """
        meeting = self._manager.get_meeting(meeting_id)
        return [
            dict(message)
            for message in meeting.get_transcript()
        ]

    def open_meeting(
        self,
        meeting_id: str,
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        meeting.open_session()
        return self._snapshot(meeting)

    def join_meeting(
        self,
        meeting_id: str,
        identity_id: str,
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        meeting.join_request(identity_id)
        return self._snapshot(meeting)

    def start_meeting(
        self,
        meeting_id: str,
        starter: str = "vinh",
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        meeting.start(starter)
        return self._snapshot(meeting)

    def add_message(
        self,
        meeting_id: str,
        speaker: str,
        content: str,
    ) -> str:
        meeting = self._manager.get_meeting(meeting_id)
        path: Path = meeting.add_message(
            speaker,
            content,
        )
        return str(path)

    def add_paste(
        self,
        meeting_id: str,
        raw_text: str,
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        return meeting.add_paste(raw_text)

    def request_close(
        self,
        meeting_id: str,
        requester: str = "vinh",
    ) -> dict[str, Any]:
        meeting = self._manager.get_meeting(meeting_id)
        meeting.request_close(requester)
        return self._snapshot(meeting)

    def close_meeting(
        self,
        meeting_id: str,
        decisions: list[str],
        action_items: list[str],
        summary: str,
        closer: str = "xu",
    ) -> str:
        meeting = self._manager.get_meeting(meeting_id)
        path: Path = meeting.close(
            decisions=decisions,
            action_items=action_items,
            summary=summary,
            closer=closer,
        )
        return str(path)

    def save_artifact(
        self,
        meeting_id: str,
        artifact_name: str = "final.md",
    ) -> str:
        meeting = self._manager.get_meeting(meeting_id)
        path: Path = meeting.save_artifact(
            artifact_name,
        )
        return str(path)


__all__ = [
    "MeetingService",
    "MeetingError",
]