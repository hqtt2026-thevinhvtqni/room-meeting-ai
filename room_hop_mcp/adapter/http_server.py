"""
HTTP adapter — Slice #2 (Recording).

Scope, per BC-01 Contract v0.1 (LOCKED):
    GET /meetings
        -> MeetingService.list_meetings()
        -> {"meetings": [...]}

    POST /meetings/{meeting_id}/paste
        -> MeetingService.add_paste(meeting_id, text)
        -> {"status": "READY"}

This module is a SEPARATE transport from room_hop_mcp/adapter/server.py
(the stdio MCP adapter). It does NOT go through the MCP protocol and does
NOT import anything from mcp.*. It calls MeetingService directly.

BC-01 constraints:
    - Recording endpoint only.
    - No Bridge/Dashboard concern.
    - No Core changes.
    - No Public V1 changes.
    - No retry logic.
    - HTTP error status mapping remains TBD.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from core.meeting_service import MeetingService


class AddPasteRequest(BaseModel):
    """Request body for the BC-01 recording endpoint."""

    text: str


def create_http_app(service: MeetingService) -> FastAPI:
    """Create the ROOM HOP HTTP adapter over MeetingService."""

    app = FastAPI(title="ROOM HOP HTTP Adapter (Slice #2)")

    @app.get("/meetings")
    def list_meetings() -> dict:
        return {"meetings": service.list_meetings()}

    @app.post("/meetings/{meeting_id}/paste")
    def add_paste(meeting_id: str, body: AddPasteRequest) -> dict:
        return service.add_paste(meeting_id, body.text)

    return app