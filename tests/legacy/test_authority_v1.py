"""
Authorization & Permission Tests -- ROOM HOP v0.2 [LEGACY - Governance V1]

LEGACY: file nay test core/governance_v1_backup.py (AuthorizationEngine --
ResourceType + Action + Authority hierarchy), KHONG PHAI core/governance.py
hien hanh (Governance V2 -- Capability + Scope + Mission; xem
tests/test_governance.py cho bo test tuong ung ban dang chay).

Giu lai (Evidence First, khong xoa, khong @pytest.mark.skip):
governance_v1_backup.py van la reference/bang chung cho thiet ke
AuthorizationEngine cu. Dat trong tests/legacy/ de KHONG chan regression
suite chinh (`pytest -q` o root bo qua thu muc nay -- xem pytest.ini),
nhung van chay duoc khi can doi chieu:

    pytest -q tests/legacy/test_authority_v1.py
"""

import pytest

from core.governance_v1_backup import (
    Agent,
    Action,
    AuthorizationEngine,
    AuthorizationResult,
    ResourceType,
    get_authorization_engine,
)


@pytest.fixture
def auth_engine() -> AuthorizationEngine:
    """Provide authorization engine for tests."""
    return get_authorization_engine()


# ============================================================================
# POSITIVE TESTS - ALLOW CASES
# ============================================================================


class TestPositiveAuthorizationCases:
    """Tests that authorized operations SHOULD succeed."""

    def test_vinh_can_read_core(self, auth_engine):
        """VINH can read XU_CORE.md."""
        result = auth_engine.check("vinh", ResourceType.CORE, Action.READ)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_vinh_can_write_core(self, auth_engine):
        """VINH can write to XU_CORE.md."""
        result = auth_engine.check("vinh", ResourceType.CORE, Action.WRITE)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_vinh_can_admin_governance(self, auth_engine):
        """VINH can administer governance rules."""
        result = auth_engine.check("vinh", ResourceType.GOVERNANCE, Action.ADMIN)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_xu_can_read_core(self, auth_engine):
        """XU can read XU_CORE.md."""
        result = auth_engine.check("xu", ResourceType.CORE, Action.READ)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_xu_can_write_project_state(self, auth_engine):
        """XU can write to PROJECT_STATE.md."""
        result = auth_engine.check("xu", ResourceType.PROJECT_STATE, Action.WRITE)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_xu_can_write_session(self, auth_engine):
        """XU can write to XU_SESSION.md."""
        result = auth_engine.check("xu", ResourceType.SESSION, Action.WRITE)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_quan_gia_can_write_project_state(self, auth_engine):
        """QUáº¢N GIA can write to PROJECT_STATE.md."""
        result = auth_engine.check("quan_gia", ResourceType.PROJECT_STATE, Action.WRITE)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_claude_can_read_context(self, auth_engine):
        """CLAUDE can read context files."""
        result = auth_engine.check("claude", ResourceType.CONTEXT, Action.READ)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_agent_can_read_meeting(self, auth_engine):
        """Generic agents can read meeting info."""
        result = auth_engine.check("agent_1", ResourceType.MEETING, Action.READ)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_agent_can_write_meeting(self, auth_engine):
        """Generic agents can write to meetings (add messages)."""
        result = auth_engine.check("claude", ResourceType.MEETING, Action.WRITE)
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_vinh_can_transition_meeting_open_to_closed(self, auth_engine):
        """VINH can transition meeting from open to closed."""
        result = auth_engine.check_meeting_transition("vinh", "open", "closed")
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_xu_can_transition_meeting_open_to_closed(self, auth_engine):
        """XU can transition meeting from open to closed."""
        result = auth_engine.check_meeting_transition("xu", "open", "closed")
        assert result.allowed, f"Expected ALLOW: {result.reason}"

    def test_quan_gia_can_transition_meeting_open_to_closed(self, auth_engine):
        """QUáº¢N GIA can transition meeting from open to closed."""
        result = auth_engine.check_meeting_transition("quan_gia", "open", "closed")
        assert result.allowed, f"Expected ALLOW: {result.reason}"


# ============================================================================
# NEGATIVE TESTS - DENY CASES
# ============================================================================


class TestNegativeAuthorizationCases:
    """Tests that unauthorized operations MUST be denied."""

    def test_xu_cannot_write_core(self, auth_engine):
        """XU cannot write to XU_CORE.md."""
        result = auth_engine.check("xu", ResourceType.CORE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_claude_cannot_write_core(self, auth_engine):
        """CLAUDE cannot write to XU_CORE.md."""
        result = auth_engine.check("claude", ResourceType.CORE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_agent_cannot_admin_core(self, auth_engine):
        """Generic agents cannot administer core."""
        result = auth_engine.check("agent_1", ResourceType.CORE, Action.ADMIN)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_xu_cannot_write_governance(self, auth_engine):
        """XU cannot modify governance rules."""
        result = auth_engine.check("xu", ResourceType.GOVERNANCE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_claude_cannot_write_governance(self, auth_engine):
        """CLAUDE cannot modify governance rules."""
        result = auth_engine.check("claude", ResourceType.GOVERNANCE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_agent_cannot_write_project_state(self, auth_engine):
        """Generic agents cannot write to PROJECT_STATE.md."""
        result = auth_engine.check("agent_1", ResourceType.PROJECT_STATE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_claude_cannot_write_project_state(self, auth_engine):
        """CLAUDE cannot write to PROJECT_STATE.md."""
        result = auth_engine.check("claude", ResourceType.PROJECT_STATE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_agent_cannot_write_session(self, auth_engine):
        """Generic agents cannot write to XU_SESSION.md."""
        result = auth_engine.check("agent_1", ResourceType.SESSION, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_claude_cannot_write_context(self, auth_engine):
        """CLAUDE cannot write to context files (read-only)."""
        result = auth_engine.check("claude", ResourceType.CONTEXT, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_agent_cannot_transition_closed_meeting(self, auth_engine):
        """Agents cannot transition meetings (only VINH, XU, QUáº¢N GIA)."""
        result = auth_engine.check_meeting_transition("claude", "open", "closed")
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_unknown_agent_cannot_write_core(self, auth_engine):
        """Unknown agents cannot write to core."""
        result = auth_engine.check("unknown_agent", ResourceType.CORE, Action.WRITE)
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_cannot_transition_closed_to_open(self, auth_engine):
        """Cannot re-open a closed meeting (invalid transition)."""
        result = auth_engine.check_meeting_transition("vinh", "closed", "open")
        assert not result.allowed, f"Expected DENY: {result.reason}"

    def test_cannot_transition_open_to_open(self, auth_engine):
        """Cannot transition meeting from open to open (no-op)."""
        result = auth_engine.check_meeting_transition("vinh", "open", "open")
        assert not result.allowed, f"Expected DENY: {result.reason}"


# ============================================================================
# PROTECTED RESOURCE TESTS
# ============================================================================


class TestProtectedResources:
    """Tests for protection of core/governance resources."""

    def test_core_protected_from_all_except_vinh(self, auth_engine):
        """Only VINH can write to CORE resources."""
        agents_should_be_denied = ["xu", "claude", "quan_gia", "agent_1", "unknown"]
        for agent in agents_should_be_denied:
            result = auth_engine.check(agent, ResourceType.CORE, Action.WRITE)
            assert not result.allowed, f"Agent {agent} should not write CORE"

    def test_governance_protected_from_all_except_vinh(self, auth_engine):
        """Only VINH can write to GOVERNANCE resources."""
        agents_should_be_denied = ["xu", "claude", "quan_gia", "agent_1", "unknown"]
        for agent in agents_should_be_denied:
            result = auth_engine.check(agent, ResourceType.GOVERNANCE, Action.WRITE)
            assert not result.allowed, f"Agent {agent} should not write GOVERNANCE"

    def test_core_readable_by_all(self, auth_engine):
        """All agents can READ core resources."""
        agents_should_be_allowed = ["vinh", "xu", "claude", "quan_gia", "agent_1"]
        for agent in agents_should_be_allowed:
            result = auth_engine.check(agent, ResourceType.CORE, Action.READ)
            assert result.allowed, f"Agent {agent} should read CORE"

    def test_context_readonly_for_non_vinh(self, auth_engine):
        """Context files are read-only except for VINH."""
        agents_should_be_denied = ["xu", "claude", "quan_gia", "agent_1"]
        for agent in agents_should_be_denied:
            result = auth_engine.check(agent, ResourceType.CONTEXT, Action.WRITE)
            assert not result.allowed, f"Agent {agent} should not write CONTEXT"


# ============================================================================
# AUTHORITY ESCALATION PREVENTION
# ============================================================================


class TestAuthorityEscalationPrevention:
    """Tests to prevent agents from escalating their own authority."""

    def test_cannot_escalate_authority(self, auth_engine):
        """No agent can escalate their own authority."""
        for agent_id in ["xu", "claude", "quan_gia", "agent_1"]:
            can_escalate = auth_engine.can_escalate_authority(agent_id)
            assert not can_escalate, f"Agent {agent_id} should not be able to escalate"

    def test_vinh_cannot_self_escalate(self, auth_engine):
        """Even VINH cannot escalate beyond VINH (logical consistency)."""
        can_escalate = auth_engine.can_escalate_authority("vinh")
        assert not can_escalate, "No one should escalate authority"

    def test_agent_cannot_change_own_permissions(self, auth_engine):
        """Agents cannot modify their own permission dict."""
        # This is implicitly tested by permission checks, but make it explicit
        result = auth_engine.check("claude", ResourceType.GOVERNANCE, Action.ADMIN)
        assert not result.allowed, "Agent should not admin governance"


# ============================================================================
# AUTHORIZATION RESULT TESTS
# ============================================================================


class TestAuthorizationResult:
    """Tests for AuthorizationResult class."""

    def test_result_bool_allowed(self):
        """AuthorizationResult with allowed=True evaluates to True."""
        result = AuthorizationResult(True, "ALLOW")
        assert bool(result) is True

    def test_result_bool_denied(self):
        """AuthorizationResult with allowed=False evaluates to False."""
        result = AuthorizationResult(False, "DENY")
        assert bool(result) is False

    def test_result_repr_allowed(self):
        """AuthorizationResult repr shows ALLOW status."""
        result = AuthorizationResult(True, "Test allow reason")
        repr_str = repr(result)
        assert "ALLOW" in repr_str

    def test_result_repr_denied(self):
        """AuthorizationResult repr shows DENY status."""
        result = AuthorizationResult(False, "Test deny reason")
        repr_str = repr(result)
        assert "DENY" in repr_str


# ============================================================================
# EDGE CASES & ROBUSTNESS
# ============================================================================


class TestAuthorizationEdgeCases:
    """Edge cases and robustness tests."""

    def test_case_insensitive_agent_id(self, auth_engine):
        """Agent IDs should be case-insensitive."""
        result1 = auth_engine.check("XU", ResourceType.CORE, Action.READ)
        result2 = auth_engine.check("xu", ResourceType.CORE, Action.READ)
        assert result1.allowed == result2.allowed

    def test_unknown_agent_defaults_to_other(self, auth_engine):
        """Unknown agents default to OTHER role with limited permissions."""
        result = auth_engine.check("unknown_agent_xyz", ResourceType.CORE, Action.WRITE)
        assert not result.allowed, "Unknown agent should not write CORE"

    def test_whitespace_trimmed_from_agent_id(self, auth_engine):
        """Agent ID whitespace should be trimmed."""
        result = auth_engine.check("  xu  ", ResourceType.CORE, Action.READ)
        assert result.allowed, "Whitespace should be trimmed from agent ID"

    def test_empty_agent_id_treated_as_other(self, auth_engine):
        """Empty agent ID should default to OTHER."""
        result = auth_engine.check("", ResourceType.CORE, Action.WRITE)
        assert not result.allowed, "Empty agent ID should default to OTHER (no write)"

    def test_permission_result_reason_explains_decision(self, auth_engine):
        """Authorization result should explain the decision."""
        result_allow = auth_engine.check("vinh", ResourceType.CORE, Action.WRITE)
        assert result_allow.reason, "ALLOW result should have explanation"
        assert len(result_allow.reason) > 0

        result_deny = auth_engine.check("claude", ResourceType.CORE, Action.WRITE)
        assert result_deny.reason, "DENY result should have explanation"
        assert len(result_deny.reason) > 0


# ============================================================================
# POLICY CONSISTENCY TESTS
# ============================================================================


class TestPolicyConsistency:
    """Tests to verify permission policy is internally consistent."""

    def test_vinh_has_all_permissions(self, auth_engine):
        """VINH should have READ, WRITE, ADMIN on all resource types."""
        for resource_type in ResourceType:
            for action in Action:
                result = auth_engine.check("vinh", resource_type, action)
                assert result.allowed, f"VINH should have {action} on {resource_type}"

    def test_agents_never_have_admin(self, auth_engine):
        """Generic agents should never have ADMIN permission."""
        for agent_id in ["claude", "agent_1", "unknown"]:
            for resource_type in ResourceType:
                result = auth_engine.check(agent_id, resource_type, Action.ADMIN)
                assert not result.allowed, f"Agent {agent_id} should not have ADMIN on {resource_type}"

    def test_xu_cannot_admin(self, auth_engine):
        """XU should not have ADMIN permission on any resource."""
        for resource_type in ResourceType:
            result = auth_engine.check("xu", resource_type, Action.ADMIN)
            assert not result.allowed, f"XU should not have ADMIN on {resource_type}"

