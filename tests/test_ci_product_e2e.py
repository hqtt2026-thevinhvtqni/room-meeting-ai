"""Product-level ROOM HOP E2E through real HTTP + MCP + persisted evidence.

This test follows one complete user-visible Core product journey:
identity discovery -> create -> open -> join -> start -> record through MCP
-> transcript readback -> close -> final artifact -> post-close readback.

It intentionally crosses the live HTTP server and a real MCP stdio subprocess.
No mocks/fake services are used for the product path.
"""

from __future__ import annotations

import asyncio
import os
import threading
import time
from pathlib import Path

import pytest
import requests
import uvicorn

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from core.principal_registry import PrincipalRegistry
from integration.room_hop_integration import (
    RoomHopIntegration,
    RoomHopIntegrationConfig,
)
from room_hop_mcp.adapter.http_server import create_http_app


@pytest.fixture()
def product_runtime(tmp_path):
    meetings_dir = tmp_path / "meetings"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    app = create_http_app(
        service,
        principal_registry=PrincipalRegistry(),
        agent_registry=AgentRegistry(),
    )

    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=0,
        log_level="warning",
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 15
    while time.time() < deadline and not server.started:
        time.sleep(0.05)
    if not server.started:
        server.should_exit = True
        thread.join(timeout=5)
        pytest.fail("ROOM HOP product HTTP server did not start within 15s")

    port = server.servers[0].sockets[0].getsockname()[1]
    yield f"http://127.0.0.1:{port}", meetings_dir

    server.should_exit = True
    thread.join(timeout=5)
    assert not thread.is_alive(), "ROOM HOP HTTP server did not shut down cleanly"


def test_complete_room_hop_product_journey_http_mcp_storage_and_close(
    product_runtime,
):
    base_url, meetings_dir = product_runtime
    timeout = 8

    # 1. Identity discovery is read-only and preserves the two registry types.
    identities_response = requests.get(base_url + "/identities", timeout=timeout)
    assert identities_response.status_code == 200
    identities = identities_response.json()
    assert any(
        item["id"] == "vinh" and item["type"] == "human_principal"
        for item in identities["principals"]
    )
    assert any(
        item["id"] == "xu" and item["type"] == "ai_agent"
        for item in identities["agents"]
    )

    # 2. Create using Core's ID allocator; no client-generated meeting ID.
    create_response = requests.post(
        base_url + "/meetings",
        json={
            "topic": "ROOM HOP product-level Auto E2E",
            "participants": ["xu"],
            "context_files": [],
            "created_by": "vinh",
        },
        timeout=timeout,
    )
    assert create_response.status_code == 200, create_response.text
    created = create_response.json()
    meeting_id = created["id"]
    assert meeting_id.startswith("MEETING-")
    assert created["status"] == "draft"

    listed_draft = requests.get(
        base_url + "/meetings",
        params={"status": "draft"},
        timeout=timeout,
    )
    assert listed_draft.status_code == 200
    assert any(item["id"] == meeting_id for item in listed_draft.json()["meetings"])

    # 3. Open and exercise policy/quorum guards before the valid path.
    opened = requests.post(base_url + f"/meetings/{meeting_id}/open", timeout=timeout)
    assert opened.status_code == 200
    assert opened.json()["status"] == "open"

    denied_join = requests.post(
        base_url + f"/meetings/{meeting_id}/join",
        json={"identity_id": "claude"},
        timeout=timeout,
    )
    assert denied_join.status_code == 400

    creator_join = requests.post(
        base_url + f"/meetings/{meeting_id}/join",
        json={"identity_id": "vinh"},
        timeout=timeout,
    )
    assert creator_join.status_code == 200

    denied_start = requests.post(
        base_url + f"/meetings/{meeting_id}/start",
        json={"starter": "vinh"},
        timeout=timeout,
    )
    assert denied_start.status_code == 400

    participant_join = requests.post(
        base_url + f"/meetings/{meeting_id}/join",
        json={"identity_id": "xu"},
        timeout=timeout,
    )
    assert participant_join.status_code == 200

    started = requests.post(
        base_url + f"/meetings/{meeting_id}/start",
        json={"starter": "vinh"},
        timeout=timeout,
    )
    assert started.status_code == 200
    assert started.json()["status"] == "active"

    # 4. Cross the real MCP stdio boundary and record identified + legacy paste.
    env = dict(os.environ)
    env["ROOM_HOP_MEETINGS_DIR"] = str(meetings_dir)
    repo_root = Path(__file__).resolve().parents[1]
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(cwd=str(repo_root), env=env)
    )

    raw_identified = (
        "Vinh: Xác nhận nội dung họp product E2E.\r\n"
        "Xu: Đã ghi nhận đúng identity và transcript.\r\n"
    )
    raw_legacy = "Nguồn legacy: giữ nguyên văn bản, không tự gán danh tính.\n"

    async def record_and_verify_active():
        async with integration.session() as session:
            tools_result = await session.list_tools()
            names = {tool.name for tool in tools_result.tools}
            assert names == {
                "list_meetings",
                "get_meeting",
                "get_transcript",
                "add_paste_to_meeting",
            }
            await integration.verify_capabilities(session)

            meetings = await integration.list_meetings(session)
            assert any(item["id"] == meeting_id for item in meetings)

            meeting = await integration.get_meeting(session, meeting_id)
            assert meeting["status"] == "active"

            first = await integration.add_paste_to_meeting(
                session,
                meeting_id,
                raw_identified,
                identity_id="xu",
            )
            assert first == {"status": "READY"}

            second = await integration.add_paste_to_meeting(
                session,
                meeting_id,
                raw_legacy,
            )
            assert second == {"status": "READY"}

            transcript = await integration.get_transcript(session, meeting_id)
            entries = [
                item for item in transcript
                if item["source"] == {"type": "ai_chat_paste"}
            ]
            assert len(entries) == 2

            identified = next(item for item in entries if item["content"] == raw_identified)
            legacy = next(item for item in entries if item["content"] == raw_legacy)
            assert identified["speaker"] == "xu"
            assert identified["header"]["name"] == AgentRegistry().get("xu").name
            assert identified["header"]["role"] == AgentRegistry().get("xu").role
            assert legacy["speaker"] is None
            assert legacy["header"] is None

    asyncio.run(record_and_verify_active())

    # 5. Verify raw Secretary transcript is byte-identical before closing.
    transcript_path = meetings_dir / meeting_id / "transcript.txt"
    expected_raw = raw_identified + raw_legacy
    assert transcript_path.read_bytes() == expected_raw.encode("utf-8")

    # 6. Close through the public HTTP lifecycle endpoint and verify final artifact.
    close_response = requests.post(
        base_url + f"/meetings/{meeting_id}/close",
        json={
            "decisions": ["Giữ Transcript là bằng chứng append-only."],
            "action_items": ["Vibe thực hiện independent review."],
            "summary": "ROOM HOP product-level journey completed through HTTP and MCP.",
            "closer": "xu",
        },
        timeout=timeout,
    )
    assert close_response.status_code == 200, close_response.text
    closed = close_response.json()
    assert closed["meeting"]["status"] == "closed"

    final_path = Path(closed["final_md_path"])
    assert final_path.is_file()
    final_content = final_path.read_text(encoding="utf-8")
    assert "ROOM HOP product-level journey completed" in final_content
    assert "Giữ Transcript là bằng chứng append-only." in final_content
    assert "Vibe thực hiện independent review." in final_content
    assert raw_identified not in final_content
    assert raw_legacy not in final_content

    # 7. Closed-state readback through public HTTP and MCP; evidence stays intact.
    listed_closed = requests.get(
        base_url + "/meetings",
        params={"status": "closed"},
        timeout=timeout,
    )
    assert listed_closed.status_code == 200
    assert any(item["id"] == meeting_id for item in listed_closed.json()["meetings"])

    async def read_back_closed():
        async with integration.session() as session:
            meeting = await integration.get_meeting(session, meeting_id)
            assert meeting["status"] == "closed"
            transcript = await integration.get_transcript(session, meeting_id)
            entries = [
                item for item in transcript
                if item["source"] == {"type": "ai_chat_paste"}
            ]
            assert [item["content"] for item in entries] == [
                raw_identified,
                raw_legacy,
            ]

    asyncio.run(read_back_closed())
    assert transcript_path.read_bytes() == expected_raw.encode("utf-8")
