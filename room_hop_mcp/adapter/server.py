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
from core.secretary import MAX_TEXT_BYTES


# F4 boundary declaration: JSON Schema maxLength is character-based,
# while the F4 runtime policy (core.secretary) is UTF-8 byte-based.
# Declaring maxLength == MAX_TEXT_BYTES keeps the public schema limit
# aligned with the runtime policy ceiling (see test_f4_resource_limits).
ADD_PASTE_MAX_LENGTH = MAX_TEXT_BYTES

LIST_MEETINGS = "list_meetings"
GET_MEETING = "get_meeting"
GET_TRANSCRIPT = "get_transcript"
ADD_PASTE_TO_MEETING = "add_paste_to_meeting"
JOIN_MEETING = "join_meeting"
START_MEETING = "start_meeting"


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
                            # F4 resource limit declaration (public schema).
                            "maxLength": ADD_PASTE_MAX_LENGTH,
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
            Tool(
                name=JOIN_MEETING,
                description=(
                    "Join an active ROOM HOP meeting as a resolved identity "
                    "(JOIN_ACCEPTED or policy-rejected)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "meeting_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                        "identity_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                    },
                    "required": ["meeting_id", "identity_id"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name=START_MEETING,
                description=(
                    "Start an open ROOM HOP meeting (lifecycle transition "
                    "open -> active) initiated by the given identity."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "meeting_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                        "starter": {
                            "type": "string",
                            "minLength": 1,
                        },
                    },
                    "required": ["meeting_id"],
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

        if name == JOIN_MEETING:
            join_record = service.join_meeting(
                arguments["meeting_id"],
                arguments["identity_id"],
            )
            return {"join_record": join_record}

        if name == START_MEETING:
            meeting = service.start_meeting(
                arguments["meeting_id"],
                starter=arguments.get("starter", "vinh"),
            )
            return {"meeting": meeting}

        raise ValueError(f"Unknown ROOM HOP MCP tool: {name}")

    return server
