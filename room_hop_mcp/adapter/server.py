"""ROOM HOP MCP Public Boundary V1."""

from __future__ import annotations

from typing import Any

from mcp.server import Server
from mcp.types import (
    CallToolResult,
    TextContent,
    Tool,
)

from core.meeting_manager import MeetingRateLimitError, MeetingRateStoreUnavailable
from core.meeting_service import MeetingService


LIST_MEETINGS = "list_meetings"
GET_MEETING = "get_meeting"
GET_TRANSCRIPT = "get_transcript"
ADD_PASTE_TO_MEETING = "add_paste_to_meeting"


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
                            "maxLength": 1048576,
                            "description": (
                                "Maximum 1 MiB UTF-8 at Core runtime. "
                                "JSON Schema maxLength counts characters; "
                                "Core enforces the authoritative byte limit."
                            ),
                        },
                        # Xu D-102-04: required participant identity.
                        "identity_id": {
                            "type": "string",
                            "minLength": 1,
                        },
                    },
                    "required": [
                        "meeting_id",
                        "text",
                        "identity_id",
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

            try:
                result = service.add_paste(
                    meeting_id,
                    text,
                    identity_id=arguments["identity_id"],
                )
            except MeetingRateLimitError as exc:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="RATE_LIMIT_EXCEEDED",
                        )
                    ],
                    structuredContent={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "retry_after_seconds": exc.retry_after_seconds,
                        }
                    },
                    isError=True,
                )
            except MeetingRateStoreUnavailable as exc:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="PASTE_RATE_STORE_UNAVAILABLE",
                        )
                    ],
                    structuredContent={
                        "error": {
                            "code": "PASTE_RATE_STORE_UNAVAILABLE",
                            "retry_after_seconds": exc.retry_after_seconds,
                        }
                    },
                    isError=True,
                )

            return {
                "paste": result,
            }

        raise ValueError(f"Unknown ROOM HOP MCP tool: {name}")

    return server
