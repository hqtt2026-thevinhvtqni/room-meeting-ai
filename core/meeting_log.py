"""
Meeting Log — ROOM HOP v0.1

Ghi lại toàn bộ diễn biến của một cuộc họp: agent nào tham gia, context nào
được cấp, message nào được gửi, khi nào đóng cuộc họp.

v0.1: log dạng append-only JSONL, đơn giản, dễ đọc lại bằng mắt thường.
Đây CHƯA phải Audit Engine đầy đủ (DEFERRED) — chỉ là log tuần tự.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_message_id() -> str:
    """MESSAGE v1.0 — mỗi Message có ID riêng, độc lập với `index`."""
    return f"msg_{uuid.uuid4().hex[:12]}"


class MeetingLog:
    """Append-only log cho một meeting cụ thể."""

    def __init__(self, meeting_dir: Path):
        self.meeting_dir = Path(meeting_dir)
        self.log_path = self.meeting_dir / "log.jsonl"
        self.messages_dir = self.meeting_dir / "messages"
        self.messages_dir.mkdir(parents=True, exist_ok=True)

        # MESSAGE v1.0 FIX: đếm dựa trên log.jsonl (bao gồm cả message
        # không có file .md riêng, vd. AI Chat Paste), KHÔNG đếm theo số
        # file .md nữa. Trước v1.0, mọi message đều có đúng 1 file .md nên
        # 2 cách đếm cho cùng kết quả — sau v1.0, AI Chat Paste tạo Message
        # nhưng KHÔNG tạo file .md, nên đếm theo .md sẽ bị lệch và làm
        # `index` bị trùng (collision) giữa các lần Meeting được nạp lại.
        # Đây là fix bắt buộc để giữ đúng backward-compat của `index`
        # (Message v1.0 Contract §6), không phải mở rộng scope.
        self._message_counter = len(self.read_all_messages())

    def _append(self, entry: dict) -> None:
        now = _now_iso()
        entry["timestamp"] = now
        if entry.get("type") == "message":
            # MESSAGE v1.0: created_at là technical metadata, tách biệt
            # với header.date/header.time (human-readable). Ghi cùng thời
            # điểm với `timestamp` (legacy field, giữ nguyên không đổi).
            entry.setdefault("created_at", now)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_event(self, action: str, detail: str = "") -> None:
        self._append({"type": "event", "action": action, "detail": detail})

    def log_context_loaded(self, context_files: list[str]) -> None:
        self._append({"type": "context_loaded", "files": context_files})

    def log_message(
        self,
        speaker: str,
        content: str,
        *,
        message_id: Optional[str] = None,
        header: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> Path:
        """Ghi một message vào cả messages/<n>.md lẫn log.jsonl, trả về path file.

        `header`/`source` là field MESSAGE v1.0, HOÀN TOÀN optional (mặc
        định None) để không phá bất kỳ caller cũ nào đang gọi
        log_message(speaker, content) như trước. `message_id`: nếu
        không truyền, tự sinh (mỗi Message luôn có `id` riêng — Contract
        T6), không có caller nào cần tự quản lý việc sinh id này.
        """
        self._message_counter += 1
        idx = self._message_counter
        msg_path = self.messages_dir / f"{idx:03d}_{speaker}.md"
        with open(msg_path, "w", encoding="utf-8") as f:
            f.write(f"# Message {idx} — {speaker}\n\n{content}\n")

        entry = {
            "type": "message",
            "index": idx,
            "id": message_id or _new_message_id(),
            "speaker": speaker,
            "content": content,
            "file": str(msg_path.relative_to(self.meeting_dir)),
        }

        if header is not None:
            entry["header"] = header
        if source is not None:
            entry["source"] = source

        self._append(entry)
        return msg_path

    def log_paste_message(
        self,
        content: str,
        *,
        identity_id: Optional[str] = None,
        header: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> str:
        """MESSAGE v1.0 — ghi một AI Chat Paste như MỘT Message logic.

        KHÔNG tạo file .md riêng (khác log_message()): paste có thể
        không có identity xác định, nên không có cơ sở đặt tên file theo
        speaker. `content` vẫn được ghi RAW nguyên văn vào log.jsonl —
        bản RAW đầy đủ (byte-identical) tiếp tục nằm ở Secretary
        (transcript.txt), KHÔNG đổi bởi hàm này.

        `identity_id`: string caller cung cấp nếu có (có thể None —
        legacy compatibility path, KHÔNG được bịa identity mặc định).
        `header`/`source`: do caller (Meeting.add_paste) build sẵn từ
        Registry, hàm này chỉ ghi lại nguyên trạng, không tự suy diễn.

        Trả về message_id đã sinh, để caller có thể trace/audit.
        """
        self._message_counter += 1
        idx = self._message_counter
        message_id = _new_message_id()

        entry = {
            "type": "message",
            "index": idx,
            "id": message_id,
            # `speaker` giữ nguyên tên field legacy cho backward-compat
            # đọc transcript, nhưng phản ánh ĐÚNG trạng thái: identity_id
            # nếu có, None nếu không — không giả danh.
            "speaker": identity_id,
            "content": content,
            "file": None,
            "header": header,
            "source": source,
        }

        self._append(entry)
        return message_id

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
