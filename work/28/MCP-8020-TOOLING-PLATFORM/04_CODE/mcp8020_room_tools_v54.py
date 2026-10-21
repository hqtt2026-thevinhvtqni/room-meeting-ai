"""Work 28 v54 ROOM/meeting/task handlers. In-memory reference implementation.

These handlers perform real in-memory operations; they do not claim Core :8000
authorization. The service layer wraps results in the common envelope.
"""
from __future__ import annotations
from typing import Any
from mcp8020_catalog_v54 import ToolCallError

class RoomProvider:
    def __init__(self) -> None:
        self._meetings: dict[str, dict[str, Any]] = {}
        self._pending_tasks: list[dict[str, Any]] = []
        self._proposals: list[dict[str, Any]] = []
        self._meeting_counter = 0
        self._proposal_counter = 0

    def _require_meeting(self, meeting_id: str) -> dict[str, Any]:
        meeting = self._meetings.get(meeting_id)
        if meeting is None:
            raise ToolCallError("NOT_FOUND", "meeting not found: " + meeting_id)
        return meeting

    def room_get_context(self, selector: str | None = None) -> dict[str, Any]:
        active = sum(1 for m in self._meetings.values() if m["status"] == "active")
        return {"room": "ROOM-HOP", "core_authority": ":8000", "mcp_adapter": ":8020", "selector": selector, "active_meetings": active, "meetings_total": len(self._meetings)}

    def room_get_structure(self, scope: str | None = None) -> dict[str, Any]:
        return {"rooms": ["MAIN"], "works": ["work/28", "work/98"], "authorities": {"core": ":8000", "mcp_adapter": ":8020"}, "scope": scope}

    def room_list_meetings(self, status_filter: str | None = None, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        items = sorted(self._meetings.values(), key=lambda m: m["meeting_id"])
        if status_filter is not None:
            items = [m for m in items if m["status"] == status_filter]
        summaries = [{"meeting_id": m["meeting_id"], "title": m["title"], "status": m["status"], "participants": len(m["participants"])} for m in items]
        return {"meetings": summaries[offset:offset + limit], "total": len(summaries)}

    def room_get_meeting(self, meeting_id: str) -> dict[str, Any]:
        meeting = self._require_meeting(meeting_id)
        return {"meeting": dict(meeting), "messages": len(meeting["messages"])}

    def room_get_transcript(self, meeting_id: str, offset: int = 0, limit: int = 100) -> dict[str, Any]:
        meeting = self._require_meeting(meeting_id)
        segments = meeting["messages"]
        return {"meeting_id": meeting_id, "segments": segments[offset:offset + limit], "total": len(segments)}

    def room_start_meeting(self, title: str, identity_id: str, participants: list[str] | None = None) -> dict[str, Any]:
        if not title.strip():
            raise ToolCallError("INVALID_INPUT", "title must not be empty")
        self._meeting_counter += 1
        meeting_id = "MTG-%04d" % self._meeting_counter
        meeting = {"meeting_id": meeting_id, "title": title, "status": "active", "participants": list(participants or []), "messages": [], "started_by": identity_id}
        self._meetings[meeting_id] = meeting
        return {"meeting_id": meeting_id, "status": "active", "participants": list(meeting["participants"])}

    def room_join_meeting(self, meeting_id: str, identity_id: str) -> dict[str, Any]:
        meeting = self._require_meeting(meeting_id)
        if identity_id not in meeting["participants"]:
            meeting["participants"].append(identity_id)
        return {"meeting_id": meeting_id, "identity_id": identity_id, "participants": list(meeting["participants"])}

    def room_append_meeting_message(self, meeting_id: str, content: str, speaker: str | None = None) -> dict[str, Any]:
        meeting = self._require_meeting(meeting_id)
        if meeting["status"] != "active":
            raise ToolCallError("POLICY_REFUSED", "meeting is not active: " + meeting_id)
        message = {"index": len(meeting["messages"]) + 1, "speaker": speaker, "content": content}
        meeting["messages"].append(message)
        return {"meeting_id": meeting_id, "message_index": message["index"], "total_messages": len(meeting["messages"])}

    def room_get_pending_tasks(self, owner: str | None = None, status_filter: str | None = None, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        items = self._pending_tasks
        if owner is not None:
            items = [t for t in items if t["owner"] == owner]
        if status_filter is not None:
            items = [t for t in items if t["status"] == status_filter]
        return {"tasks": items[offset:offset + limit], "total": len(items)}

    def room_submit_proposal(self, identity_id: str, content: str, scope: str | None = None, evidence_refs: list[str] | None = None) -> dict[str, Any]:
        if not content.strip():
            raise ToolCallError("INVALID_INPUT", "proposal content must not be empty")
        self._proposal_counter += 1
        proposal_id = "PRP-%04d" % self._proposal_counter
        proposal = {"proposal_id": proposal_id, "identity_id": identity_id, "content": content, "scope": scope, "evidence_refs": list(evidence_refs or [])}
        self._proposals.append(proposal)
        task = {"task_id": "TSK-" + proposal_id, "owner": identity_id, "status": "PENDING", "proposal_id": proposal_id, "content": content, "scope": scope}
        self._pending_tasks.append(task)
        return {"proposal_id": proposal_id, "status": "SUBMITTED", "pending_task_id": task["task_id"]}
