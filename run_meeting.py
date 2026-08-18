#!/usr/bin/env python3
"""
run_meeting.py — ROOM HOP v0.1

Chạy MỘT cuộc họp thật, xuyên suốt: Agent -> Context -> Meeting -> Message -> Log -> Final.

v0.1 CHƯA gọi API AI thật (Giai đoạn 3, deferred). Ở bước "Xu / Claude trao đổi",
nội dung message được nạp qua danh sách `SCRIPTED_EXCHANGE` bên dưới — đại diện
cho nội dung một AI thật SẼ nói. Khi Giai đoạn 3 (AI Connector) sẵn sàng, phần
này được thay bằng lệnh gọi API thật, phần còn lại của pipeline không đổi.

Chạy:
    python run_meeting.py
"""

from __future__ import annotations

from core.agent_registry import AgentRegistry
from core.context_loader import suggest_context
from core.meeting_manager import MeetingManager

MEETING_ID = "MEETING-2026-001"
TOPIC = "Kiểm thử ROOM HOP v0.1 — cuộc họp đầu tiên chạy thật trên PC"
PARTICIPANTS = ["xu", "claude"]
CONTEXT_FILES = [
    # Vinh chọn thủ công — đây là quyết định của người điều phối, không phải AI.
    "XU_CORE.md",
    "XU_SESSION.md",
    "PROJECT_STATE.md",
]

# Nội dung trao đổi mẫu cho E2E test v0.1 (thay bằng API thật ở Giai đoạn 3).
SCRIPTED_EXCHANGE = [
    ("vinh", "Mở cuộc họp đầu tiên. Mục tiêu: xác nhận ROOM HOP v0.1 chạy được xuyên suốt."),
    ("xu", "Đã nhận context: XU_CORE.md, XU_SESSION.md, PROJECT_STATE.md. "
           "Đề xuất: kiểm tra pipeline Agent -> Context -> Meeting -> Log trước khi mở rộng."),
    ("claude", "Đồng ý. Về mặt kỹ thuật, context đã được copy đúng (không sửa file gốc), "
               "meeting.yaml đang ở trạng thái 'open'. Sẵn sàng ghi nhận quyết định."),
    ("xu", "Vậy chốt: v0.1 PASS nếu final.md được tạo đầy đủ với decisions + action items."),
]

DECISIONS = [
    "ROOM HOP v0.1 (4 lõi: Meeting Manager, Agent Registry, Context Loader, Meeting Log) được xác nhận chạy end-to-end.",
]
ACTION_ITEMS = [
    "Vinh xem lại meetings/MEETING-2026-001/final.md để xác nhận evidence.",
    "Sau khi xác nhận, Xu + Claude ngồi lại quyết định phạm vi v0.2 dựa trên log thật.",
]
SUMMARY = (
    "Cuộc họp đầu tiên chạy thành công trên PC. Pipeline Agent -> Context -> "
    "Meeting -> Message -> Log -> Final đã được xác nhận hoạt động. Context gốc "
    "(XU_CORE.md, XU_SESSION.md, PROJECT_STATE.md) không bị chỉnh sửa trong quá trình này."
)


def main() -> None:
    print("=" * 60)
    print("ROOM HOP v0.1 — RUN MEETING")
    print("=" * 60)

    # 1. Agent Registry
    registry = AgentRegistry()
    print(f"\n[1/6] Agent Registry: {len(registry.list_agents())} agent đã nạp "
          f"-> {[a.id for a in registry.list_agents()]}")

    # 2. Gợi ý context (chỉ tham khảo — KHÔNG tự động áp dụng)
    suggestion = suggest_context(TOPIC)
    print(f"[2/6] Gợi ý context cho topic (rule-based, chỉ tham khảo): {suggestion}")
    print(f"       -> Vinh chọn thủ công: {CONTEXT_FILES}")

    # 3. Tạo Meeting (Meeting Manager gọi Context Loader bên trong, CHỈ ĐỌC context gốc)
    manager = MeetingManager(registry=registry)
    meeting = manager.create_meeting(
        meeting_id=MEETING_ID,
        topic=TOPIC,
        participants=PARTICIPANTS,
        context_files=CONTEXT_FILES,
        created_by="vinh",
    )
    print(f"[3/6] Meeting '{MEETING_ID}' đã tạo, trạng thái: {meeting.data['status']}")
    print(f"       -> Context đã đóng gói vào: {meeting.meeting_dir / 'context'}")

    # 4. Trao đổi (Message Log)
    print(f"[4/6] Ghi {len(SCRIPTED_EXCHANGE)} message vào Meeting Log...")
    for speaker, content in SCRIPTED_EXCHANGE:
        meeting.add_message(speaker, content)
    print("       -> Đã ghi xong.")

    # 5. Đóng cuộc họp -> final.md
    final_path = meeting.close(decisions=DECISIONS, action_items=ACTION_ITEMS, summary=SUMMARY)
    print(f"[5/6] Meeting đã đóng. Final summary: {final_path}")

    # 6. Xác nhận log đầy đủ
    events = meeting.log.read_all_events()
    print(f"[6/6] Audit log có {len(events)} sự kiện (log.jsonl).")

    print("\n" + "=" * 60)
    print(f"ROOM HOP v0.1 STATUS: READY")
    print(f"Xem kết quả tại: {meeting.meeting_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
