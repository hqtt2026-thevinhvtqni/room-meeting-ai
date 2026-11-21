import asyncio
import os

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

from integration.room_hop_integration import (
    RoomHopIntegration,
    RoomHopIntegrationConfig,
)


def _isolated_integration(tmp_path, *, seed_meeting=False):
    """Give each test its own meeting store; never depend on repo meetings/."""
    meetings_dir = tmp_path / "meetings"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    meeting_id = "MEETING-INT-ISOLATED-001"

    if seed_meeting:
        service.create_meeting(
            meeting_id=meeting_id,
            topic="Isolated MCP integration test",
            participants=[],
            context_files=[],
            created_by="vinh",
        )

    env = dict(os.environ)
    env["ROOM_HOP_MEETINGS_DIR"] = str(meetings_dir)
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=".", env=env)
    )
    return integration, meeting_id


async def _test_integration_session_init(tmp_path):
    """TEST-INT-001: Verify Integration.session() establishes MCP connection."""
    integration, _ = _isolated_integration(tmp_path)

    async with integration.session() as mcp_session:
        await integration.verify_capabilities(mcp_session)
        assert mcp_session is not None


def test_integration_smoke(tmp_path):
    asyncio.run(_test_integration_session_init(tmp_path))


async def _test_integration_list_meetings(tmp_path):
    """INT-LIST-001: list_meetings is deterministic against an empty test store."""
    integration, _ = _isolated_integration(tmp_path)

    async with integration.session() as mcp_session:
        meetings = await integration.list_meetings(mcp_session)
        assert meetings == []


def test_integration_list_meetings(tmp_path):
    asyncio.run(_test_integration_list_meetings(tmp_path))


async def _test_integration_get_meeting(tmp_path):
    """INT-MEETING-001: get_meeting reads the test-owned meeting."""
    integration, meeting_id = _isolated_integration(
        tmp_path, seed_meeting=True
    )

    async with integration.session() as mcp_session:
        meeting = await integration.get_meeting(mcp_session, meeting_id)
        assert meeting == {
            "id": meeting_id,
            "title": "Isolated MCP integration test",
            "status": "draft",
        }


def test_integration_get_meeting(tmp_path):
    asyncio.run(_test_integration_get_meeting(tmp_path))


async def _test_integration_get_transcript(tmp_path):
    """INT-TRANSCRIPT-001: transcript read is isolated and starts empty."""
    integration, meeting_id = _isolated_integration(
        tmp_path, seed_meeting=True
    )

    async with integration.session() as mcp_session:
        transcript = await integration.get_transcript(mcp_session, meeting_id)
        assert transcript == []


def test_integration_get_transcript(tmp_path):
    asyncio.run(_test_integration_get_transcript(tmp_path))


async def _test_integration_add_paste(tmp_path):
    """INT-PASTE-001: recording works through MCP stdio on test-owned state."""
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
        RoomHopIntegrationConfig(cwd=".", env=env)
    )

    async with integration.session() as mcp_session:
        result = await integration.add_paste_to_meeting(
            mcp_session,
            meeting_id,
            "Integration recording test.",
            identity_id="vinh",
        )
        assert result == {"status": "READY"}


def test_integration_add_paste(tmp_path):
    asyncio.run(_test_integration_add_paste(tmp_path))
