"""
End-to-End Test — ROOM HOP v0.1

Đây là test quan trọng nhất: chứng minh Agent -> Context -> Meeting ->
Message -> Log -> Final chạy xuyên suốt, đúng như luồng run_meeting.py,
và context gốc không hề bị đụng tới.
"""

import hashlib

from core.agent_registry import AgentRegistry
from core.context_loader import CONTEXT_DIR
from core.meeting_manager import MeetingManager


def _md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def test_full_meeting_lifecycle_end_to_end(tmp_path):
    context_files = ["XU_CORE.md", "XU_SESSION.md", "PROJECT_STATE.md"]
    source_hashes_before = {f: _md5(CONTEXT_DIR / f) for f in context_files}

    # 1. Agent Registry
    registry = AgentRegistry()
    assert registry.exists("xu")
    assert registry.exists("claude")

    # 2. Meeting Manager tạo meeting (bên trong gọi Context Loader)
    manager = MeetingManager(registry=registry, meetings_dir=tmp_path / "meetings")
    meeting = manager.create_meeting(
        meeting_id="MEETING-E2E-001",
        topic="Kiểm thử end-to-end",
        participants=["xu", "claude"],
        context_files=context_files,
        created_by="vinh",
    )
    assert meeting.data["status"] == "draft"

    # 2b. Lifecycle v0.2.1: mở phiên, 3 người JOIN (vinh là creator nên
    # được join dù không nằm trong invited_participants), rồi START.
    meeting.open_session()
    meeting.join_request("vinh")
    meeting.join_request("xu")
    meeting.join_request("claude")
    meeting.start("vinh")
    assert meeting.data["status"] == "active"

    # 3. Context đã được đóng gói (copy) đúng vào thư mục meeting
    for f in context_files:
        assert (meeting.meeting_dir / "context" / f).exists()

    # 4. Trao đổi nhiều lượt giữa các participant
    meeting.add_message("vinh", "Mở cuộc họp kiểm thử end-to-end.")
    meeting.add_message("xu", "Đã nhận context, sẵn sàng thảo luận.")
    meeting.add_message("claude", "Xác nhận pipeline hoạt động đúng.")
    meeting.add_message("xu", "Chốt: v0.1 PASS.")

    messages = meeting.log.read_all_messages()
    assert len(messages) == 4
    assert [m["speaker"] for m in messages] == ["vinh", "xu", "claude", "xu"]

    # 5. Đóng cuộc họp -> final.md
    final_path = meeting.close(
        decisions=["ROOM HOP v0.1 chạy end-to-end thành công."],
        action_items=["Vinh xác nhận evidence.", "Xu + Claude bàn v0.2."],
        summary="Pipeline đầy đủ đã chạy thật, có log, có final summary.",
    )
    assert final_path.exists()
    final_content = final_path.read_text(encoding="utf-8")
    assert "MEETING-E2E-001" in final_content
    assert "ROOM HOP v0.1 chạy end-to-end thành công." in final_content

    # 6. Audit log (log.jsonl) phải ghi đủ event quan trọng
    events = meeting.log.read_all_events()
    event_types = [e["type"] for e in events]
    assert "event" in event_types  # meeting_created, meeting_closed
    assert "context_loaded" in event_types
    assert event_types.count("message") == 4

    # 7. 🔒 Nguyên tắc khóa quan trọng nhất: context GỐC không bị sửa
    source_hashes_after = {f: _md5(CONTEXT_DIR / f) for f in context_files}
    assert source_hashes_after == source_hashes_before, (
        "VI PHẠM NGUYÊN TẮC KHÓA: context gốc đã bị thay đổi trong quá trình chạy meeting!"
    )

    # 8. Meeting có thể tra cứu lại qua MeetingManager
    reloaded = manager.get_meeting("MEETING-E2E-001")
    assert reloaded.data["status"] == "closed"
    assert len(reloaded.data["decisions"]) == 1
