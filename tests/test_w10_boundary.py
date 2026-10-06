"""Regression tests for Work 10 public boundary hardening."""
import os
import subprocess
import sys
from unittest.mock import Mock

import pytest

from core.meeting_service import MeetingService, GovernanceDeniedError


def _service(identity="agent_llama"):
    manager = Mock()
    manager.list_meetings.return_value = [
        {"id": "m1", "topic": "T1", "status": "active", "created_at": "t1"},
        {"id": "m2", "topic": "T2", "status": "closed", "created_at": "t2"},
    ]
    governance = Mock()
    governance.can_access_meeting.side_effect = (
        lambda who, meeting_id, capability: who == "vinh" or meeting_id == "m1"
    )
    return MeetingService(manager, governance, identity), manager, governance


def test_list_meetings_filters_unauthorized_metadata():
    service, _, governance = _service("agent_llama")
    result = service.list_meetings()
    assert [item.meeting_id for item in result] == ["m1"]
    assert governance.can_access_meeting.call_count == 2


def test_list_meetings_denies_all_for_unauthorized_identity():
    service, _, governance = _service("blocked")
    governance.can_access_meeting.side_effect = lambda *_: False
    assert service.list_meetings() == []


@pytest.mark.parametrize("meeting_id", ["../secret", "m1/../../x", r"m1\\x", "", "."])
def test_public_boundary_rejects_path_like_meeting_ids(meeting_id):
    service, _, _ = _service("vinh")
    with pytest.raises(ValueError, match="Invalid meeting_id"):
        service.get_meeting(meeting_id)


def test_mcp_server_refuses_missing_identity():
    env = os.environ.copy()
    env.pop("MCP_REQUESTER_IDENTITY", None)
    result = subprocess.run(
        [sys.executable, "-c", "import mcp.server"],
        cwd=os.getcwd(),
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "MCP_REQUESTER_IDENTITY is required" in (result.stdout + result.stderr)


def test_mcp_server_starts_with_explicit_identity():
    env = os.environ.copy()
    env["MCP_REQUESTER_IDENTITY"] = "xu"
    result = subprocess.run(
        [sys.executable, "-c", "import mcp.server"],
        cwd=os.getcwd(),
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
