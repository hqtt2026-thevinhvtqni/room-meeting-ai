from __future__ import annotations

from fastapi.testclient import TestClient


def test_core_http_entrypoint_keeps_meeting_api_and_fails_closed_without_authority(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("ROOM_HOP_MEETINGS_DIR", str(tmp_path / "meetings"))
    monkeypatch.delenv("ROOM_HOP_EXECUTION_IDENTITIES_JSON", raising=False)
    monkeypatch.delenv("ROOM_HOP_EXECUTION_WORKS_JSON", raising=False)
    monkeypatch.delenv("ROOM_HOP_EXECUTION_STORE_PATH", raising=False)

    from room_hop_mcp.core_http_main import build_app

    client = TestClient(build_app())
    meetings = client.get("/meetings")
    assert meetings.status_code == 200
    assert meetings.json() == {"meetings": []}

    execution = client.post(
        "/works/W28/execution-grants",
        json={"purpose": "pytest_run"},
    )
    assert execution.status_code == 503
    assert execution.json()["detail"] == "execution_authority_not_configured"
