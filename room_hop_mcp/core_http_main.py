"""Core HTTP runtime entrypoint.

Runs the existing Meeting API and the additive Work execution-authority
mount in one Core process. Execution endpoints remain 503 until the Core
identity/Work policy and durable-store environment are configured.
"""
from __future__ import annotations

import os
from pathlib import Path

import uvicorn

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.http_server import create_http_app


def build_app():
    meetings_dir = os.getenv("ROOM_HOP_MEETINGS_DIR")
    manager = MeetingManager(meetings_dir=Path(meetings_dir)) if meetings_dir else MeetingManager()
    service = MeetingService(manager)
    return create_http_app(service)


app = build_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("ROOM_HOP_CORE_BIND", "127.0.0.1"),
        port=int(os.getenv("ROOM_HOP_CORE_PORT", "8000")),
        access_log=False,
    )
