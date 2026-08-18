"""Human CLI for ROOM HOP lifecycle + Secretary integration."""
from __future__ import annotations
import argparse
from core.meeting_manager import MeetingError, MeetingManager

parser = argparse.ArgumentParser()
parser.add_argument("--meeting-id", required=True)
args = parser.parse_args()

meeting = MeetingManager().get_meeting(args.meeting_id)
# SECRETARY V1: meeting.secretary duoc Meeting tu wiring san (xem
# core/meeting_manager.py). Khong tu tao Secretary rieng o day nua de
# tranh 2 instance cung ghi vao 1 file theo 2 duong khac nhau.
print(f"=== ROOM HOP CHAT | Identity: vinh | Meeting: {args.meeting_id} ===")
print("Gõ: JOIN <identity> | START | Vinh:... | Xu:... | Me:... | REQUEST_CLOSE | ROOM CLOSE")
print("Hoặc: PASTE  (rồi dán nhiều dòng nguyên văn, kết thúc bằng dòng END)")
print("-" * 50)

while True:
    raw = input("\n> ").strip()
    if not raw:
        continue

    # Never persist the CLI prompt itself as meeting content.
    # This also makes copy/paste of a displayed prompt ("> START") safe.
    if raw.startswith(">"):
        raw = raw[1:].strip()
    if not raw:
        continue
    try:
        if raw.upper().startswith("JOIN "):
            identity = raw.split(None, 1)[1].strip()
            meeting.join_request(identity)
            print(f"JOIN_ACCEPTED: {identity}")
            continue
        if raw.upper() == "START":
            meeting.start("vinh")
            print("MEETING ACTIVE")
            continue
        if raw.upper() == "REQUEST_CLOSE":
            meeting.request_close("vinh")
            print("MEETING CLOSING")
            continue
        if raw.upper() == "ROOM CLOSE":
            meeting.close([], [], "Secretary integration test closed.", closer="vinh")
            print("MEETING CLOSED")
            break

        if raw.upper() == "PASTE":
            # Nhan nhieu dong nguyen van cho toi khi gap dong END. Secretary
            # ghi nguyen block, khong tach dong, khong nhan dien speaker,
            # khong parse noi dung.
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            block = "\n".join(lines)
            meeting.add_paste(block)
            print("RECORDED [PASTE BLOCK]")
            continue

        speaker = "vinh"
        content = raw
        if ":" in raw and raw.split(":", 1)[0].strip().lower() in {"vinh", "xu", "me", "claude"}:
            speaker, content = raw.split(":", 1)
            speaker, content = speaker.strip().lower(), content.strip()
        meeting.add_message(speaker, content)
        print(f"RECORDED [{speaker}]")
    except MeetingError as e:
        print(f"[MEETING BLOCKED] {e}")
