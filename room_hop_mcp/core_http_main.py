"""Core HTTP runtime entrypoint.

Runs the existing Meeting API and the additive Core-owned Work execution
authority in one Core process. Execution remains fail-closed unless the
identity, Work policy and durable journal are configured.
"""
from __future__ import annotations

import ipaddress
import os
from pathlib import Path

import uvicorn

from core.agent_registry import AgentRegistry
from core.execution_authority import ExecutionAuthority
from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.execution_authority_http import (
    create_execution_authority_router,
)
from room_hop_mcp.adapter.http_server import create_http_app


def build_app():
    meetings_dir = os.getenv("ROOM_HOP_MEETINGS_DIR")
    manager = MeetingManager(
        meetings_dir=Path(meetings_dir) if meetings_dir else None,
    ) if meetings_dir else MeetingManager()
    service = MeetingService(manager)
    app = create_http_app(service)

    # Agent identity is resolved from the server-side Agent Registry.
    # Service credentials map to this principal; request bodies cannot
    # nominate or override the principal.
    authority = ExecutionAuthority.from_env(agent_registry=AgentRegistry())
    app.include_router(create_execution_authority_router(authority))
    return app


app = build_app()


def resolve_loopback_bind_host(value: str | None = None) -> str:
    """Remote HTTP exposure is disabled until authenticated transport ships."""
    host = (value or os.getenv("ROOM_HOP_CORE_BIND", "127.0.0.1")).strip()
    if host.lower() == "localhost":
        return "127.0.0.1"
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        raise RuntimeError(
            "ROOM HOP Core HTTP must bind to a loopback address."
        ) from None
    if not address.is_loopback:
        raise RuntimeError(
            "ROOM HOP Core HTTP remote bind is disabled pending authenticated transport."
        )
    return host


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=resolve_loopback_bind_host(),
        port=int(os.getenv("ROOM_HOP_CORE_PORT", "8000")),
        access_log=False,
    )
