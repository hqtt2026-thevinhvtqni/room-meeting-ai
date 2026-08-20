"""Tests for Governance.can_access_meeting() + protected READ fix."""
import pytest
from core.governance import Governance, MissionContext


@pytest.fixture
def gov():
    return Governance()


class TestCanAccessMeeting:
    def test_vinh_can_read_any_meeting(self, gov):
        assert gov.can_access_meeting("vinh", "m1", "READ") is True

    def test_agent_llama_cannot_read_meeting(self, gov):
        assert gov.can_access_meeting("agent_llama", "m1", "READ") is False

    def test_xu_can_read_meeting(self, gov):
        assert gov.can_access_meeting("xu", "m1", "READ") is True

    def test_default_capability_is_read(self, gov):
        assert gov.can_access_meeting("vinh", "m1") is True

    def test_returns_bool_not_tuple(self, gov):
        result = gov.can_access_meeting("vinh", "m1")
        assert isinstance(result, bool)


class TestProtectedReadAllowed:
    """Verify fix: only READ through protected paths is allowed."""

    def test_read_meeting_yaml_allowed(self, gov):
        mission = MissionContext(name="test")
        ok, _ = gov.check("vinh", "READ", "meetings/m1/meeting.yaml", mission)
        assert ok is True

    def test_create_meeting_yaml_denied_without_flag(self, gov):
        # CREATE on protected denied without allow_edit_protected
        mission = MissionContext(name="test", allow_edit_protected=False)
        ok, _ = gov.check("vinh", "CREATE", "meetings/m1/meeting.yaml", mission)
        assert ok is False

    def test_edit_meeting_yaml_denied_without_flag(self, gov):
        mission = MissionContext(name="test", allow_edit_protected=False)
        ok, _ = gov.check("vinh", "EDIT", "meetings/m1/meeting.yaml", mission)
        assert ok is False

    def test_edit_meeting_yaml_allowed_with_flag(self, gov):
        mission = MissionContext(name="test", allow_edit_protected=True)
        ok, _ = gov.check("vinh", "EDIT", "meetings/m1/meeting.yaml", mission)
        assert ok is True

    def test_delete_meeting_yaml_denied_without_flags(self, gov):
        mission = MissionContext(name="test", allow_delete=False, allow_edit_protected=False)
        ok, _ = gov.check("vinh", "DELETE", "meetings/m1/meeting.yaml", mission)
        assert ok is False
