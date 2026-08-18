"""
Secretary V1 Acceptance — SECRETARY x MEETING LIFECYCLE.

Contract (Xu, 2026-08-17):
    INPUT:  raw text pasted by Vinh (vd: copy tu AI chat)
    OUTPUT: raw transcript + meeting record/minutes artifact
    MUST:   preserve exact content
    MUST NOT: interpret, summarize, call AI, control lifecycle

Acceptance flow 1 (roundtrip byte-identical):
    COPY FROM AI CHAT -> SECRETARY.append() -> TRANSCRIPT -> READ -> EXPORT
    -> BYTE IDENTICAL

    (Da co coverage day du trong tests/test_secretary.py - file nay chi
    xac nhan lai qua duong Meeting thay vi Secretary doc lap, de dam bao
    khong bi lech khi di qua Meeting.add_paste()).

Acceptance flow 2 (full lifecycle):
    CREATE ROOM -> JOIN -> START -> PASTE CONVERSATION ->
    PASTE ANOTHER AI CONVERSATION -> CLOSE
    -> transcript ton tai
    -> minutes/record (final.md) ton tai
    -> raw content van nguyen (byte-identical, khong bi Meeting/Secretary
       parse/sua doi)
"""
from __future__ import annotations

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError, MeetingManager


def _make_meeting(tmp_path, meeting_id="MEETING-SECV1-001"):
    registry = AgentRegistry()
    manager = MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")
    meeting = manager.create_meeting(
        meeting_id=meeting_id,
        topic="Secretary V1 acceptance",
        participants=["xu", "claude"],
        context_files=[],
        created_by="vinh",
    )
    meeting.open_session()
    meeting.join_request("vinh")
    meeting.join_request("xu")
    meeting.start("vinh")
    return meeting


class TestSecretaryReceiveViaMeetingIsByteIdentical:
    """Acceptance flow 1: COPY -> append -> TRANSCRIPT -> read -> export ->
    BYTE IDENTICAL, di qua Meeting.add_paste() thay vi Secretary doc lap."""

    def test_single_paste_roundtrip_byte_identical(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        pasted = (
            "User: giai thich ho toi ve gradient descent\r\n"
            "AI: Gradient descent la mot thuat toan toi uu...\r\n"
            "    (indent giu nguyen)\r\n"
        )
        meeting.add_paste(pasted)

        assert meeting.secretary.read() == pasted
        assert meeting.secretary.export() == pasted

    def test_append_return_status_unchanged_via_add_paste(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        result = meeting.add_paste("noi dung bat ky")
        assert result == {"status": "READY"}


class TestSecretaryDoesNotControlLifecycle:
    """MUST NOT control lifecycle: Meeting - khong phai Secretary - la noi
    quyet dinh co cho ghi hay khong, dua tren trang thai meeting."""

    def test_paste_rejected_before_start(self, tmp_path):
        registry = AgentRegistry()
        manager = MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")
        meeting = manager.create_meeting(
            meeting_id="MEETING-SECV1-002",
            topic="Secretary V1 - chua start",
            participants=["xu"],
            context_files=[],
            created_by="vinh",
        )
        # Chua open_session/join/start -> van con "draft"
        import pytest
        with pytest.raises(MeetingError):
            meeting.add_paste("khong duoc phep ghi khi chua active")

    def test_paste_rejected_after_close(self, tmp_path):
        import pytest

        meeting = _make_meeting(tmp_path)
        meeting.add_paste("noi dung truoc khi dong")
        meeting.close(decisions=[], action_items=[], summary="dong meeting")

        with pytest.raises(MeetingError):
            meeting.add_paste("khong duoc phep ghi sau khi da CLOSE")


class TestSecretaryFullLifecycleAcceptance:
    """Acceptance flow 2 (dung y so do cua Xu):
    CREATE ROOM -> JOIN -> START -> PASTE CONVERSATION ->
    PASTE ANOTHER AI CONVERSATION -> CLOSE
    -> transcript ton tai, minutes/record ton tai, raw content van nguyen.
    """

    def test_create_join_start_paste_paste_close(self, tmp_path):
        meeting = _make_meeting(tmp_path, meeting_id="MEETING-SECV1-003")

        conversation_1 = (
            "User: Toi can phan tich VN-Index tuan nay.\n"
            "AI: VN-Index dong cua tai 1,250 diem, tang 0.8%...\n"
        )
        conversation_2 = (
            "User: Con crypto BTC thi sao?\r\n"
            "AI: BTC dang giao dich quanh vung $95,000...\r\n"
        )

        meeting.add_paste(conversation_1)
        meeting.add_paste(conversation_2)

        final_path = meeting.close(
            decisions=["Ghi nhan 2 doan hoi thoai AI vao transcript."],
            action_items=["Doc lai transcript truoc khi phan tich sau."],
            summary="Secretary V1 acceptance - 2 lan PASTE thanh cong.",
        )

        # 1. transcript ton tai
        transcript_path = meeting.meeting_dir / "transcript.txt"
        assert transcript_path.exists()

        # 2. minutes/record (final.md) ton tai
        assert final_path.exists()
        assert final_path.name == "final.md"

        # 3. raw content van nguyen - byte-identical, ghep dung thu tu,
        # khong bi Secretary hay Meeting parse/sua doi noi dung.
        expected_raw = conversation_1 + conversation_2
        assert meeting.secretary.read() == expected_raw
        with open(transcript_path, "r", encoding="utf-8", newline="") as f:
            assert f.read() == expected_raw

        # 4. Sau CLOSE, transcript immutable qua duong Meeting (guard o
        # add_paste, khong phai o Secretary - dung dinh huong kien truc).
        try:
            meeting.add_paste("khong duoc ghi them sau CLOSE")
            assert False, "add_paste sau CLOSE phai raise MeetingError"
        except MeetingError:
            pass

        # 5. Noi dung transcript khong bi lam thay doi sau khi CLOSE.
        assert meeting.secretary.read() == expected_raw
