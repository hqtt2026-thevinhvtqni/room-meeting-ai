import asyncio
import os

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

from integration.room_hop_integration import (
    RoomHopIntegration,
    RoomHopIntegrationConfig,
)


async def _test_integration_session_init():
    """TEST-INT-001: Verify Integration.session() establishes MCP connection."""
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=".")
    )

    async with integration.session() as mcp_session:
        await mcp_session.initialize()
        assert mcp_session is not None


def test_integration_smoke():
    """Wrapper for pytest."""
    asyncio.run(_test_integration_session_init())


async def _test_integration_list_meetings():
    """INT-LIST-001: list_meetings works through MCP stdio."""
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=".")
    )

    async with integration.session() as mcp_session:
        meetings = await integration.list_meetings(mcp_session)

        assert isinstance(meetings, list)
        print(meetings)


def test_integration_list_meetings():
    """Wrapper for pytest."""
    asyncio.run(_test_integration_list_meetings())

async def _test_integration_get_meeting():
    """INT-MEETING-001: get_meeting works through MCP stdio."""
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=".")
    )
    async with integration.session() as mcp_session:
        meetings = await integration.list_meetings(mcp_session)
        meeting_id = meetings[0]["id"]

        meeting = await integration.get_meeting(
            mcp_session,
            meeting_id,
        )

        assert meeting["id"] == meeting_id
        assert "title" in meeting
        assert "status" in meeting
        print(meeting)


def test_integration_get_meeting():
    """Wrapper for pytest."""
    asyncio.run(_test_integration_get_meeting())

async def _test_integration_get_transcript():
    """INT-TRANSCRIPT-001: get_transcript works through MCP stdio."""
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=".")
    )
    async with integration.session() as mcp_session:
        meetings = await integration.list_meetings(mcp_session)
        meeting_id = meetings[0]["id"]

        transcript = await integration.get_transcript(
            mcp_session,
            meeting_id,
        )

        print(transcript)
        assert isinstance(transcript, list)


def test_integration_get_transcript():
    """Wrapper for pytest."""
    asyncio.run(_test_integration_get_transcript())

async def _test_integration_add_paste(tmp_path):
    """INT-PASTE-001: recording works through MCP stdio."""
    meetings_dir = tmp_path / "meetings"

    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    meeting_id = "MEETING-INT-TEST-001"

    service.create_meeting(
        meeting_id=meeting_id,
        topic="Integration Recording Test",
        participants=["vinh", "xu", "claude"],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, "xu")
    service.join_meeting(meeting_id, "claude")
    service.start_meeting(meeting_id, "vinh")

    env = dict(os.environ)
    env["ROOM_HOP_MEETINGS_DIR"] = str(meetings_dir)

    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(
            cwd=".",
            env=env,
        )
    )

    async with integration.session() as mcp_session:
        result = await integration.add_paste_to_meeting(
            mcp_session,
            meeting_id,
            "Integration recording test.",
        )

        print(result)
        assert result == {"status": "READY"}


def test_integration_add_paste(tmp_path):
    """Wrapper for pytest."""
    asyncio.run(_test_integration_add_paste(tmp_path))
