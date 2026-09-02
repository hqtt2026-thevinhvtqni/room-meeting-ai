import pytest

from fastapi.testclient import TestClient

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.http_server import create_http_app


def make_client(tmp_path):
    manager = MeetingManager(meetings_dir=tmp_path / "meetings")
    service = MeetingService(manager)
    app = create_http_app(service)
    return TestClient(app), manager, service


def test_post_paste_active_returns_ready(tmp_path):
    client, _, service = make_client(tmp_path)

    service.create_meeting(
        meeting_id="MEETING-HTTP-PASTE-001",
        topic="HTTP recording test",
        participants=["xu", "claude"],
        context_files=[],
    )

    service.open_meeting("MEETING-HTTP-PASTE-001")
    service.join_meeting("MEETING-HTTP-PASTE-001", "xu")
    service.join_meeting("MEETING-HTTP-PASTE-001", "claude")
    service.start_meeting("MEETING-HTTP-PASTE-001", starter="xu")

    response = client.post(
        "/meetings/MEETING-HTTP-PASTE-001/paste",
        json={"text": "Hello from HTTP"},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "READY"}


def test_post_paste_closed_propagates_domain_error(tmp_path):
    client, _, service = make_client(tmp_path)

    service.create_meeting(
        meeting_id="MEETING-HTTP-PASTE-002",
        topic="HTTP closed recording test",
        participants=["xu", "claude"],
        context_files=[],
    )

    service.open_meeting("MEETING-HTTP-PASTE-002")
    service.join_meeting("MEETING-HTTP-PASTE-002", "xu")
    service.join_meeting("MEETING-HTTP-PASTE-002", "claude")
    service.start_meeting("MEETING-HTTP-PASTE-002", starter="xu")

    service.request_close(
        "MEETING-HTTP-PASTE-002",
        requester="vinh",
    )

    service.close_meeting(
        "MEETING-HTTP-PASTE-002",
        decisions=["OK"],
        action_items=[],
        summary="Done",
        closer="xu",
    )

    with pytest.raises(Exception):
        client.post(
            "/meetings/MEETING-HTTP-PASTE-002/paste",
            json={"text": "Should be rejected"},
        )


def test_post_paste_unknown_meeting_propagates_domain_error(tmp_path):
    client, _, _ = make_client(tmp_path)

    with pytest.raises(Exception):
        client.post(
            "/meetings/MEETING-HTTP-UNKNOWN/paste",
            json={"text": "Should be rejected"},
        )

def test_post_paste_missing_text_is_rejected(tmp_path):
    client, _, _ = make_client(tmp_path)

    response = client.post(
        "/meetings/MEETING-HTTP-VALIDATION-001/paste",
        json={},
    )

    assert response.status_code == 422
