"""Isolated MCP stdio end-to-end test for the CI runner."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from integration.room_hop_integration import (
    RoomHopIntegration,
    RoomHopIntegrationConfig,
)


def test_mcp_stdio_public_boundary_roundtrip(tmp_path):
    meetings_dir = tmp_path / "meetings"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    meeting_id = "CI-MCP-E2E-001"

    service.create_meeting(
        meeting_id=meeting_id,
        topic="CI MCP stdio E2E",
        participants=["vinh", "xu"],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, "xu")
    service.start_meeting(meeting_id, "vinh")

    env = dict(os.environ)
    env["ROOM_HOP_MEETINGS_DIR"] = str(meetings_dir)
    repo_root = Path(__file__).resolve().parents[1]
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=str(repo_root), env=env)
    )

    async def exercise_public_boundary():
        async with integration.session() as session:
            tools_result = await session.list_tools()
            tool_names = {tool.name for tool in tools_result.tools}
            expected_tools = {
                "list_meetings",
                "get_meeting",
                "get_transcript",
                "add_paste_to_meeting",
            }
            assert tool_names == expected_tools
            await integration.verify_capabilities(session)

            meetings = await integration.list_meetings(session)
            assert any(item["id"] == meeting_id for item in meetings)

            meeting = await integration.get_meeting(session, meeting_id)
            assert meeting["id"] == meeting_id
            assert meeting["status"] == "active"

            vinh_result = await integration.add_paste_to_meeting(
                session, meeting_id, "Vinh stdio paste", identity_id="vinh"
            )
            assert vinh_result == {"status": "READY"}

            identified_result = await integration.add_paste_to_meeting(
                session,
                meeting_id,
                "identified stdio paste",
                identity_id="xu",
            )
            assert identified_result == {"status": "READY"}

            transcript = await integration.get_transcript(session, meeting_id)
            paste_entries = [
                message for message in transcript
                if message["source"] == {"type": "ai_chat_paste"}
            ]
            legacy = next(
                message for message in paste_entries
                if message["content"] == "Vinh stdio paste"
            )
            identified = next(
                message for message in paste_entries
                if message["content"] == "identified stdio paste"
            )
            assert legacy["speaker"] == "vinh"
            assert legacy["header"]["name"] == "Vinh"
            assert identified["speaker"] == "xu"
            assert identified["header"]["name"] == "Xu"
            assert identified["header"]["role"]

    asyncio.run(exercise_public_boundary())
