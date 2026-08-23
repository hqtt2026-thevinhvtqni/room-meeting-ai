"""Entrypoint for running the ROOM HOP MCP server over stdio.

Wires: MeetingManager -> MeetingService -> MCP adapter (server.py)
Run with:  python -m room_hop_mcp   (from the room-meeting-ai project root)
"""

from __future__ import annotations

import asyncio

import mcp.server.stdio

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.server import create_server


async def main() -> None:
    manager = MeetingManager()
    service = MeetingService(manager)
    server = create_server(service)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())