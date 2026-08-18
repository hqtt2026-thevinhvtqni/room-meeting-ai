"""
Governance Tests — ROOM HOP v0.2 (bản V2: Governance/GOV/MissionContext)

Thay thế tests/test_authority.py cũ (test AuthorizationEngine đã bị xóa
khỏi core/governance.py khi module được viết lại thành bản V2 - Capability
+ Vùng + Authority). Cùng tinh thần: positive/negative/protected/edge case,
nhưng bám theo API thật đang chạy: GOV.check(identity, capability, path, mission).
"""

import pytest

from core.governance import GOV, MissionContext


def default_mission(**overrides) -> MissionContext:
    return MissionContext(name="test_mission", **overrides)


class TestPositiveCases:
    def test_vinh_can_do_anything_anywhere(self):
        mission = default_mission()
        for cap in ("READ", "CREATE", "EDIT"):
            ok, msg = GOV.check("vinh", cap, "anything/anywhere.md", mission)
            assert ok, f"vinh should {cap}: {msg}"

    def test_agent_llama_can_write_research(self):
        ok, msg = GOV.check("agent_llama", "CREATE", "research/notes.md", default_mission())
        assert ok, msg

    def test_agent_llama_can_write_docs(self):
        ok, msg = GOV.check("agent_llama", "EDIT", "docs/readme.md", default_mission())
        assert ok, msg

    def test_xu_can_edit_meetings(self):
        mission = default_mission(allow_edit_protected=True)
        ok, msg = GOV.check("xu", "EDIT", "meetings/MEETING-2026-001/meeting.yaml", mission)
        assert ok, msg

    def test_quan_gia_can_edit_meetings(self):
        mission = default_mission(allow_edit_protected=True)
        ok, msg = GOV.check("quan_gia", "EDIT", "meetings/MEETING-2026-001/meeting.yaml", mission)
        assert ok, msg

    def test_unknown_identity_falls_back_to_agent_llama_scope(self):
        ok, msg = GOV.check("agent_random_xyz", "CREATE", "research/x.md", default_mission())
        assert ok, msg


class TestNegativeCases:
    def test_agent_llama_cannot_write_core(self):
        ok, msg = GOV.check("agent_llama", "EDIT", "XU_CORE.md", default_mission())
        assert not ok, "agent_llama khong duoc sua XU_CORE.md"

    def test_agent_llama_cannot_write_governance(self):
        ok, msg = GOV.check("agent_llama", "EDIT", "core/governance.py", default_mission())
        assert not ok

    def test_claude_cannot_edit_meetings_without_capability(self):
        # "claude" khong co entry rieng trong CAPABILITIES -> fallback agent_llama,
        # khong co "meetings/*" trong scope EDIT -> DENY, ke ca khi mission mo protected.
        mission = default_mission(allow_edit_protected=True)
        ok, msg = GOV.check("claude", "EDIT", "meetings/MEETING-2026-001/meeting.yaml", mission)
        assert not ok, msg

    def test_agent_llama_cannot_edit_outside_scope(self):
        ok, msg = GOV.check("agent_llama", "EDIT", "some_other_zone/file.txt", default_mission())
        assert not ok

    def test_delete_denied_without_mission_allow_delete(self):
        ok, msg = GOV.check("agent_llama", "DELETE", "tmp/junk.txt", default_mission(allow_delete=False))
        assert not ok, "DELETE phai bi tu choi khi mission.allow_delete=False"


class TestProtectedResources:
    def test_core_governance_py_protected_from_agent_llama(self):
        ok, _ = GOV.check("agent_llama", "EDIT", "core/governance.py", default_mission())
        assert not ok

    def test_core_governance_py_protected_even_with_allow_edit_protected_but_no_scope(self):
        # Mo khoa "protected" khong tu dong cap scope - agent_llama van khong co
        # "core/*" trong EDIT scope cua no -> van DENY.
        mission = default_mission(allow_edit_protected=True)
        ok, _ = GOV.check("agent_llama", "EDIT", "core/governance.py", mission)
        assert not ok

    def test_vinh_can_edit_protected_paths(self):
        mission = default_mission(allow_edit_protected=True)
        ok, msg = GOV.check("vinh", "EDIT", "core/governance.py", mission)
        assert ok, msg

    def test_meetings_protected_by_default(self):
        mission = default_mission(allow_edit_protected=False)
        ok, msg = GOV.check("vinh", "EDIT", "meetings/MEETING-2026-001/meeting.yaml", mission)
        assert not ok, "meetings/ phai bi chan neu mission khong allow_edit_protected"


class TestMissionScopeOverride:
    def test_mission_allowed_scopes_extends_access(self):
        mission = MissionContext(name="special", allowed_scopes=["special_zone/*"])
        ok, msg = GOV.check("agent_llama", "EDIT", "special_zone/file.md", mission)
        assert ok, msg

    def test_mission_scope_does_not_bypass_protected_lock(self):
        # Mission scope mo rong pham vi EDIT thong thuong, nhung KHONG the
        # bypass protected-lock (can allow_edit_protected=True rieng).
        mission = MissionContext(name="special", allowed_scopes=["core/*"], allow_edit_protected=False)
        ok, msg = GOV.check("agent_llama", "EDIT", "core/governance.py", mission)
        assert not ok, "Mission scope khong duoc bypass protected lock"


class TestEdgeCases:
    def test_empty_identity_defaults_to_agent_llama(self):
        ok, msg = GOV.check("", "CREATE", "research/x.md", default_mission())
        assert ok, msg

    def test_reason_string_always_present(self):
        ok, msg = GOV.check("vinh", "READ", "anything.md", default_mission())
        assert msg
        ok, msg = GOV.check("agent_llama", "EDIT", "core/governance.py", default_mission())
        assert msg
