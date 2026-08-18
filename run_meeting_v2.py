#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

from core.agent_registry import AgentRegistry
from core.connectors import AgentResponse, InternalConnector, MockConnector, TurnStatus
from core.discussion import request_synthesis, run_discussion
from core.meeting_manager import MeetingManager, MeetingError

PARTICIPANTS_DEFAULT = ["xu", "claude"]
CONTEXT_FILES = ["XU_CORE.md", "XU_SESSION.md", "PROJECT_STATE.md"]

INTERNAL_AGENTS = {}
try:
    from agents.me_agent import MeAgent
    INTERNAL_AGENTS["me_meta"] = MeAgent
except ImportError:
    pass

def build_mock_connectors(registry, participants):
    connectors = {}
    for pid in participants:
        agent_def = registry.get(pid)

        if pid in INTERNAL_AGENTS:
            connectors[pid] = InternalConnector(agent_def, INTERNAL_AGENTS[pid]())
            continue

        if pid == "xu":
            script = [
                AgentResponse(TurnStatus.REPLY, f"{pid}: Mở đầu - test full council 8 người"),
                AgentResponse(TurnStatus.REPLY, f"{pid}: Đồng ý với council"),
                AgentResponse(TurnStatus.REPLY, f"TỔNG HỢP: Full council {participants} PASS"),
            ]
        else:
            script = [
                AgentResponse(TurnStatus.REPLY, f"{pid}: Đã đọc transcript, đồng ý theo vai {pid}"),
                AgentResponse(TurnStatus.FINAL, f"{pid}: Đề xuất chốt PASS"),
            ]
        connectors[pid] = MockConnector(agent_def, script)
    return connectors

def inject_culture_wall(meeting_path: Path):
    """Mê - Tự động dán ảnh văn hóa vào phòng họp XU CORE"""
    try:
        src_html = Path("meetings/xu_core_culture_wall.html")
        src_img = Path("assets/images/hq-tt-lab-culture-team.jpg")

        if src_html.exists():
            shutil.copy(src_html, meeting_path / "xu_core_culture_wall.html")

        if src_img.exists():
            assets_dir = meeting_path / "assets"
            assets_dir.mkdir(exist_ok=True)
            shutil.copy(src_img, assets_dir / "hq-tt-lab-culture-team.jpg")

        wall_md = meeting_path / "CULTURE_WALL.md"
        wall_md.write_text(
            "# TT Lab Culture Team - Hình ảnh văn hóa LAB\n\n"
            "![TT Lab Culture Team](assets/hq-tt-lab-culture-team.jpg)\n\n"
            "Đây là hình ảnh chính thức được treo trong phòng họp XU CORE.\n"
            "Mọi AI khi vào họp đều nhìn thấy.\n\n"
            "**Authority: VINH > XU > AGENT**\n",
            encoding="utf-8"
        )
        print(f"[Culture Wall] ✅ Đã dán ảnh vào phòng {meeting_path.name}")
    except Exception as e:
        print(f"[Culture Wall] ⚠️ Lỗi: {e}")

def main():
    parser = argparse.ArgumentParser(description="ROOM HOP v0.2 - Full Council")
    parser.add_argument('--meeting-id', type=str, required=True, help='VD: MEETING-2026-003 hoặc 003')
    parser.add_argument('--participants', type=str, default=",".join(PARTICIPANTS_DEFAULT), help='Comma separated')
    args = parser.parse_args()

    meeting_id = args.meeting_id.strip()
    if not meeting_id.startswith("MEETING-"):
        meeting_id = f"MEETING-2026-{meeting_id.zfill(3)}"

    participants = [p.strip() for p in args.participants.split(",") if p.strip()]
    registry = AgentRegistry()
    manager = MeetingManager(registry=registry)
    meeting_path = Path(manager.meetings_dir) / meeting_id

    if meeting_path.exists():
        yaml_path = meeting_path / "meeting.yaml"
        if not yaml_path.exists():
            print(f"⛔ CORRUPTED: {meeting_id} tồn tại nhưng thiếu meeting.yaml")
            print(f" Đây là thư mục ghi tay fake. Hãy xóa hoặc đổi tên:")
            print(f" Rename-Item meetings/{meeting_id} meetings/{meeting_id}_FAKE_BACKUP")
            return
        try:
            meeting = manager.get_meeting(meeting_id)
            print(f"Meeting {meeting_id} đã CLOSED -> không chạy lại được. Hãy dùng ID mới như 004.")
            return
        except MeetingError as e:
            if "đã tồn tại" in str(e) or "CLOSED" in str(e):
                print(f"⛔ {e}")
                print(f"Gợi ý: Dùng MEETING-2026-004 hoặc xóa folder cũ")
                return
            meeting = manager.get_meeting(meeting_id)
    else:
        meeting = manager.create_meeting(
            meeting_id=meeting_id,
            topic=f"ROOM HOP v0.2 Full Council {meeting_id}",
            participants=participants,
            context_files=CONTEXT_FILES,
            created_by="vinh",
        )
        # === Mê inject ảnh văn hóa vào phòng mới ===
        inject_culture_wall(meeting_path)

    print(f"[1/4] Meeting {meeting_id} OK - participants: {participants}")
    connectors = build_mock_connectors(registry, participants)
    print(f"[2/4] Connectors sẵn sàng cho {len(participants)} agents")

    result = run_discussion(meeting, connectors, max_rounds=15, max_consecutive_pass=2)
    print(f"[3/4] Discussion dừng: {result.stop_reason} sau {result.rounds_used} lượt")

    synthesis = request_synthesis(meeting, synthesizer_id="xu", connectors=connectors)
    final_path = meeting.close(
        decisions=[synthesis],
        action_items=["Full council test PASS"],
        summary=synthesis,
    )
    print(f"[4/4] Final: {final_path}")

if __name__ == "__main__":
    main()