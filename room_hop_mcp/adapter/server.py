"""ROOM HOP MCP Public Boundary V1."""

from __future__ import annotations

from typing import Any

from mcp.server import Server
from mcp.types import (
    CallToolResult,
    TextContent,
    Tool,
)

from core.meeting_service import MeetingService


LIST_MEETINGS = "list_meetings"
GET_MEETING = "get_meeting"
GET_TRANSCRIPT = "get_transcript"
ADD_PASTE_TO_MEETING = "add_paste_to_meeting"
MAX_TEXT_BYTES = 1 * 1024 * 1024


def create_server(service: MeetingService) -> Server:
    """Create the ROOM HOP MCP server over the public MeetingService."""

    server = Server(
        "room-hop",
        version="1.0.0",
        instructions="ROOM HOP MCP Public Boundary V1",
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=LIST_MEETINGS,
                description="List meetings available through ROOM HOP.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            ),
            Tool(
                name=GET_MEETING,
                description="Get a detached ROOM HOP meeting DTO.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "meeting_id": {"type": "string", "minLength": 1},
                    },
                    "required": ["meeting_id"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name=GET_TRANSCRIPT,
                description="Get the transcript evidence for a ROOM HOP meeting.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "meeting_id": {"type": "string", "minLength": 1},
                    },
                    "required": ["meeting_id"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name=ADD_PASTE_TO_MEETING,
                description="Append raw text to an active ROOM HOP meeting.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "meeting_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                        "text": {
                            "type": "string",
                            # JSON Schema counts Unicode characters, whereas
                            # F4 runtime enforcement must count UTF-8 bytes.
                            # This declared cap is an early protocol boundary;
                            # MeetingService remains responsible for byte safety.
                            "maxLength": MAX_TEXT_BYTES,
                        },
                        # MESSAGE v1.0 — OPTIONAL. Không có trong
                        # "required" -> mọi caller cũ (Gate 2, test F1-F3)
                        # không kèm identity_id vẫn tiếp tục hoạt động
                        # nguyên trạng (legacy compatibility path).
                        "identity_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                    },
                    "required": [
                        "meeting_id",
                        "text",
                    ],
                    "additionalProperties": False,
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if name == LIST_MEETINGS:
            return {
                "meetings": service.list_meetings(),
            }

        if name == GET_MEETING:
            return {
                "meeting": service.get_meeting(arguments["meeting_id"]),
            }

        if name == GET_TRANSCRIPT:
            return {
                "transcript": service.get_transcript(arguments["meeting_id"]),
            }

        if name == ADD_PASTE_TO_MEETING:
            meeting_id = arguments["meeting_id"]
            text = arguments["text"]

            result = service.add_paste(meeting_id, text)

            return {
                "paste": result,
            }

        raise ValueError(f"Unknown ROOM HOP MCP tool: {name}")

    return server
