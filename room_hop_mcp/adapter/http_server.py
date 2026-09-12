"""
room_hop_mcp/adapter/http_server.py

Core Lifecycle HTTP Contract v0.1.

Nguyên tắc (mục V trong CTO task):
- HTTP adapter chỉ validate request DTO, gọi MeetingService, map response.
- Không chứa lifecycle business logic.
- Không tự allocate ID (MeetingManager._allocate_meeting_id() làm việc đó).
- Không đọc filesystem trực tiếp.
- Không gọi MeetingManager trực tiếp — luôn qua MeetingService.

Ngoại lệ duy nhất: GET /identities đọc PrincipalRegistry/AgentRegistry
trực tiếp, vì đây là Identity Layer — tách biệt khỏi Meeting lifecycle
theo đúng ROOM_HOP_LIFECYCLE_v0.2.1.md, không đi qua MeetingService.
Route này read-only, không mutate registry nào.
"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError
from core.meeting_service import MeetingService
from core.principal_registry import PrincipalRegistry


# ---------------------------------------------------------------------------
# Request DTOs
# ---------------------------------------------------------------------------

class AddPasteRequest(BaseModel):
    text: str


class CreateMeetingRequest(BaseModel):
    topic: str
    participants: list[str] = []
    context_files: list[str] = []
    created_by: str = "vinh"
    # v0.1: optional. Không cung cấp -> Core allocate (MEETING-YYYY-XXX).
    # Cung cấp tường minh -> giữ backward compatibility với caller cũ.
    meeting_id: Optional[str] = None


class JoinMeetingRequest(BaseModel):
    identity_id: str


class StartMeetingRequest(BaseModel):
    starter: str


class CloseMeetingRequest(BaseModel):
    decisions: list[str] = []
    action_items: list[str] = []
    summary: str = ""
    closer: str = "vinh"


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_http_app(
    service: MeetingService,
    principal_registry: Optional[PrincipalRegistry] = None,
    agent_registry: Optional[AgentRegistry] = None,
) -> FastAPI:
    app = FastAPI(title="ROOM HOP HTTP Adapter")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------------------------------------------
    # MeetingError -> HTTP 400, scoped ONLY to the 5 new lifecycle
    # routes below (create/open/join/start/close).
    #
    # A global @app.exception_handler(MeetingError) was tried first and
    # reverted: it silently changed behavior of the pre-existing
    # POST /meetings/{id}/paste route too, which tests/test_http_recording.py
    # relies on raising an *unhandled* exception through TestClient
    # (pytest.raises(Exception) around client.post(...)). /paste is not
    # part of this task's scope, so its error behavior must stay exactly
    # as it was pre-patch. Hence: local try/except per new route instead
    # of a global handler.
    # -----------------------------------------------------------------
    def _raise_as_bad_request(exc: MeetingError) -> None:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # -----------------------------------------------------------------
    # Identity discovery — read-only, không đi qua MeetingService.
    # -----------------------------------------------------------------
    @app.get("/identities")
    def list_identities() -> dict:
        principals_source = principal_registry or PrincipalRegistry()
        agents_source = agent_registry or AgentRegistry()

        return {
            "principals": [
                {"id": p.id, "name": p.name, "type": p.type}
                for p in principals_source.list_principals()
            ],
            "agents": [
                {
                    "id": a.id,
                    "name": a.name,
                    "role": a.role,
                    "type": "ai_agent",
                }
                for a in agents_source.list_agents()
            ],
        }

    # -----------------------------------------------------------------
    # Existing routes — KHÔNG đổi behavior.
    # -----------------------------------------------------------------
    @app.get("/meetings")
    def list_meetings(status: Optional[str] = None) -> dict:
        return {"meetings": service.list_meetings(status=status)}

    @app.get("/meetings/{meeting_id}")
    def get_meeting(meeting_id: str) -> dict:
        return service.get_meeting(meeting_id)

    @app.get("/meetings/{meeting_id}/transcript")
    def get_transcript(meeting_id: str) -> dict:
        return {"transcript": service.get_transcript(meeting_id)}

    @app.post("/meetings/{meeting_id}/paste")
    def add_paste(meeting_id: str, body: AddPasteRequest) -> dict:
        return service.add_paste(meeting_id, body.text)

    # -----------------------------------------------------------------
    # Lifecycle routes — MỚI.
    # -----------------------------------------------------------------
    @app.post("/meetings")
    def create_meeting(body: CreateMeetingRequest) -> dict:
        try:
            return service.create_meeting(
                meeting_id=body.meeting_id,
                topic=body.topic,
                participants=body.participants,
                context_files=body.context_files,
                created_by=body.created_by,
            )
        except MeetingError as exc:
            _raise_as_bad_request(exc)

    @app.post("/meetings/{meeting_id}/open")
    def open_meeting(meeting_id: str) -> dict:
        try:
            return service.open_meeting(meeting_id)
        except MeetingError as exc:
            _raise_as_bad_request(exc)

    @app.post("/meetings/{meeting_id}/join")
    def join_meeting(meeting_id: str, body: JoinMeetingRequest) -> dict:
        try:
            return service.join_meeting(meeting_id, body.identity_id)
        except MeetingError as exc:
            _raise_as_bad_request(exc)

    @app.post("/meetings/{meeting_id}/start")
    def start_meeting(meeting_id: str, body: StartMeetingRequest) -> dict:
        try:
            return service.start_meeting(meeting_id, starter=body.starter)
        except MeetingError as exc:
            _raise_as_bad_request(exc)

    @app.post("/meetings/{meeting_id}/close")
    def close_meeting(meeting_id: str, body: CloseMeetingRequest) -> dict:
        # meeting_service.close_meeting trả về Path (str) của final.md,
        # KHÔNG phải snapshot — khác pattern với open/join/start.
        # Đây là behavior có sẵn trong MeetingService, giữ nguyên,
        # chỉ map thành response envelope rõ ràng cho client.
        try:
            final_path = service.close_meeting(
                meeting_id,
                decisions=body.decisions,
                action_items=body.action_items,
                summary=body.summary,
                closer=body.closer,
            )
        except MeetingError as exc:
            _raise_as_bad_request(exc)
            return  # unreachable, keeps type-checkers happy

        return {
            "meeting": service.get_meeting(meeting_id),
            "final_md_path": final_path,
        }

    return app