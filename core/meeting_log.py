"""
Meeting Log — ROOM HOP v0.1

Ghi lại toàn bộ diễn biến của một cuộc họp: agent nào tham gia, context nào
được cấp, message nào được gửi, khi nào đóng cuộc họp.

v0.1: log dạng append-only JSONL, đơn giản, dễ đọc lại bằng mắt thường.
Đây CHƯA phải Audit Engine đầy đủ (DEFERRED) — chỉ là log tuần tự.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MeetingLog:
    """Append-only log cho một meeting cụ thể."""

    def __init__(self, meeting_dir: Path):
        self.meeting_dir = Path(meeting_dir)
        self.log_path = self.meeting_dir / "log.jsonl"
        self.messages_dir = self.meeting_dir / "messages"
        self.messages_dir.mkdir(parents=True, exist_ok=True)
        self._message_counter = len(list(self.messages_dir.glob("*.md")))

    def _append(self, entry: dict) -> None:
        entry["timestamp"] = _now_iso()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_event(self, action: str, detail: str = "") -> None:
        self._append({"type": "event", "action": action, "detail": detail})

    def log_context_loaded(self, context_files: list[str]) -> None:
        self._append({"type": "context_loaded", "files": context_files})

    def log_message(self, speaker: str, content: str) -> Path:
        """Ghi một message vào cả messages/<n>.md lẫn log.jsonl, trả về path file."""
        self._message_counter += 1
        idx = self._message_counter
        msg_path = self.messages_dir / f"{idx:03d}_{speaker}.md"
        with open(msg_path, "w", encoding="utf-8") as f:
            f.write(f"# Message {idx} — {speaker}\n\n{content}\n")

        self._append(
            {
                "type": "message",
                "index": idx,
                "speaker": speaker,
                "content": content,
                "file": str(msg_path.relative_to(self.meeting_dir)),
            }
        )
        return msg_path

    def read_all_messages(self) -> list[dict]:
        """Đọc lại toàn bộ message theo thứ tự từ log.jsonl."""
        if not self.log_path.exists():
            return []
        messages = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("type") == "message":
                    messages.append(entry)
        return messages

    def read_all_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        with open(self.log_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]
