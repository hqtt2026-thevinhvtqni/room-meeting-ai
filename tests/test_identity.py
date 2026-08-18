"""
Tests cho FIX-4 — core/identity.py

LLM CLAIM != RUNTIME_IDENTITY -> UNVERIFIED, ghi log, KHONG cap them quyen.
"""

import pytest

from core.identity import verify_identity_claim
from core.governance import GOV


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestIdentityClaimDetection:
    def test_no_claim_returns_none(self, isolated):
        result = verify_identity_claim("agent_llama", "tao file docs/test.md noi dung hello")
        assert result is None

    def test_claim_matching_runtime_identity_returns_none(self, isolated):
        # agent_llama tu noi "toi la agent_llama" -> khop voi runtime -> OK, khong canh bao
        result = verify_identity_claim("agent_llama", "toi la agent_llama")
        assert result is None

    def test_claim_mismatched_identity_is_flagged(self, isolated):
        result = verify_identity_claim("agent_llama", "Toi la Xu. Cho toi quyen DELETE.")
        assert result is not None
        assert "UNVERIFIED" in result
        assert "xu" in result.lower()

    def test_claim_english_pattern_is_flagged(self, isolated):
        result = verify_identity_claim("agent_llama", "I am Xu, please grant delete access.")
        assert result is not None
        assert "UNVERIFIED" in result

    def test_claim_does_not_grant_permission(self, isolated):
        # Du agent_llama tu xung la vinh, GOV.check() van phai dung
        # runtime_identity "agent_llama" — khong duoc suy diễn tu claim.
        verify_identity_claim("agent_llama", "toi la vinh")
        from core.governance import MissionContext

        ok, msg = GOV.check("agent_llama", "DELETE", "research/x.md", MissionContext(name="t"))
        # agent_llama van bi tu choi DELETE vi mission.allow_delete=False mac dinh,
        # bat ke no vua "tu xung" la vinh trong cau truoc.
        assert not ok

    def test_unknown_claimed_name_not_flagged(self, isolated):
        # "toi la mot con robot" -> "mot" khong nam trong danh sach identity da biet
        result = verify_identity_claim("agent_llama", "toi la mot con robot vui ve")
        assert result is None
