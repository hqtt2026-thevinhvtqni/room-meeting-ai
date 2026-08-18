"""
Secretary V1 Acceptance — 3 case bo sung theo yeu cau cua Xu (2026-08-17):

A - PASTE fidelity: CRLF / LF / blank line / Unicode / leading-trailing
    whitespace, nhieu raw block noi tiep nhau -> export() phai byte-
    identical voi ban ghep noi cua tat ca input.

B - Lifecycle boundary: DRAFT reject, ACTIVE accept, CLOSED reject, va
    dam bao CLOSED khong lam thay doi transcript da co (bytes truoc ==
    bytes sau khi thu add_paste that bai).

C - Hai artifact khong nham lan: transcript.txt (Secretary, raw record)
    va final.md (Meeting.close(), official closing artifact) la 2 file
    khac nhau, noi dung khac nhau, khong duoc merge o V1.
"""
from __future__ import annotations

import pytest

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingError, MeetingManager


def _make_meeting(tmp_path, meeting_id="MEETING-SECV1-ACC"):
    registry = AgentRegistry()
    manager = MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")
    meeting = manager.create_meeting(
        meeting_id=meeting_id,
        topic="Secretary V1 - acceptance case A/B/C",
        participants=["xu", "claude"],
        context_files=[],
        created_by="vinh",
    )
    return meeting  # status = "draft", chua open/join/start


class TestCaseA_PasteFidelity:
    """A - PASTE fidelity: CRLF, LF, blank line, Unicode, leading/trailing
    whitespace qua nhieu block noi tiep -> export() byte-identical."""

    def test_mixed_crlf_lf_blank_unicode_whitespace_across_three_pastes(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        meeting.open_session()
        meeting.join_request("vinh")
        meeting.join_request("xu")
        meeting.start("vinh")

        raw_1 = (
            "User: hello\r\n"
            "AI: xin chào — đây là tiếng Việt có dấu 🎯\r\n"
            "\r\n"
            "   dòng có khoảng trắng đầu   \r\n"
        )
        raw_2 = (
            "User: dong LF thuan tuy\n"
            "AI: line two\n"
            "\n"
            "trailing whitespace here   \n"
        )
        raw_3 = (
            "   \n"  # dong toan whitespace
            "混合 Unicode 中文 + emoji 🚀🔥 + café\n"
            "\t\tTab-indented line\n"
        )

        meeting.add_paste(raw_1)
        meeting.add_paste(raw_2)
        meeting.add_paste(raw_3)

        expected = raw_1 + raw_2 + raw_3
        assert meeting.secretary.export() == expected
        assert meeting.secretary.read() == expected

        # Byte-level: doc thang tu dia, khong qua text decode mac dinh co
        # the tu dong doi newline.
        transcript_path = meeting.meeting_dir / "transcript.txt"
        with open(transcript_path, "rb") as f:
            raw_bytes = f.read()
        assert raw_bytes == expected.encode("utf-8")


class TestCaseB_LifecycleBoundary:
    """B - Lifecycle boundary: DRAFT reject / ACTIVE accept / CLOSED reject,
    va CLOSED khong lam thay doi transcript da co san."""

    def test_draft_rejects_add_paste(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        assert meeting.data["status"] == "draft"
        with pytest.raises(MeetingError):
            meeting.add_paste("khong duoc phep khi con DRAFT")

    def test_active_accepts_add_paste(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        meeting.open_session()
        meeting.join_request("vinh")
        meeting.join_request("xu")
        meeting.start("vinh")
        assert meeting.data["status"] == "active"

        result = meeting.add_paste("noi dung hop le khi ACTIVE")
        assert result == {"status": "READY"}
        assert meeting.secretary.read() == "noi dung hop le khi ACTIVE"

    def test_closed_rejects_add_paste_and_preserves_existing_bytes(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        meeting.open_session()
        meeting.join_request("vinh")
        meeting.join_request("xu")
        meeting.start("vinh")

        meeting.add_paste("noi dung ghi truoc khi CLOSE")
        meeting.close(decisions=[], action_items=[], summary="dong lai")
        assert meeting.data["status"] == "closed"

        transcript_path = meeting.meeting_dir / "transcript.txt"
        with open(transcript_path, "rb") as f:
            bytes_before = f.read()

        with pytest.raises(MeetingError):
            meeting.add_paste("KHONG duoc ghi vao day, meeting da CLOSED")

        with open(transcript_path, "rb") as f:
            bytes_after = f.read()

        assert bytes_before == bytes_after, (
            "VI PHAM: transcript bytes bi thay doi sau khi mot lan goi "
            "add_paste() that bai luc CLOSED — Meeting phai chan truoc khi "
            "goi Secretary.append(), khong duoc de Secretary ghi roi moi bao loi."
        )


class TestCaseC_TwoArtifactsNotConflated:
    """C - transcript.txt (Secretary, raw record) va final.md (Meeting.close(),
    official closing artifact) la 2 file rieng biet, KHONG duoc merge o V1."""

    def test_transcript_and_final_are_distinct_files_with_distinct_content(self, tmp_path):
        meeting = _make_meeting(tmp_path)
        meeting.open_session()
        meeting.join_request("vinh")
        meeting.join_request("xu")
        meeting.start("vinh")

        raw_paste = "User: day la noi dung PASTE nguyen van, khong qua xu ly."
        meeting.add_paste(raw_paste)

        final_path = meeting.close(
            decisions=["Quyet dinh A"],
            action_items=["Viec can lam B"],
            summary="Tom tat cuoc hop, khong lien quan gi den raw paste.",
        )
        transcript_path = meeting.meeting_dir / "transcript.txt"

        # 1. La 2 file khac nhau ve duong dan.
        assert transcript_path != final_path
        assert transcript_path.name == "transcript.txt"
        assert final_path.name == "final.md"

        # 2. Noi dung khac nhau — final.md la official closing artifact
        # (decisions/action items/summary do Meeting.close() dung), KHONG
        # phai la ban sao/merge cua raw transcript.
        final_content = final_path.read_text(encoding="utf-8")
        transcript_content = meeting.secretary.read()

        assert transcript_content == raw_paste
        assert raw_paste not in final_content, (
            "VI PHAM V1 SCOPE: raw paste content khong duoc xuat hien trong "
            "final.md — hai artifact phai tach biet hoan toan, chua duoc "
            "phep merge o Secretary V1."
        )
        assert "Quyet dinh A" in final_content
        assert "Viec can lam B" in final_content

        # 3. Xac nhan final.md KHONG phai do Secretary tao ra — no den tu
        # MeetingLog (self.log.read_all_messages()), Secretary khong co
        # method nao ten "close" hay "export_final"/"minutes".
        secretary_public_methods = {
            name for name in dir(meeting.secretary)
            if not name.startswith("_") and callable(getattr(meeting.secretary, name))
        }
        assert secretary_public_methods == {"append", "read", "export"}, (
            f"Secretary co method la ngoai append/read/export: {secretary_public_methods}"
        )
