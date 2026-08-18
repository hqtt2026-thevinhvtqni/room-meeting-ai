"""
Context Loader — ROOM HOP v0.1

Nguyên tắc đã chốt:
  - Vinh CHỌN THỦ CÔNG context_files khi tạo Meeting.
  - Rule-based keyword matching CHỈ dùng để GỢI Ý (suggest_context),
    KHÔNG được tự động áp dụng, KHÔNG gọi AI để chấm relevance.
  - Loader CHỈ ĐỌC từ room_hop/context/. KHÔNG BAO GIỜ ghi/sửa file gốc.
    Nội dung được COPY (đóng gói) vào meetings/<id>/context/.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOM_HOP_ROOT = Path(__file__).resolve().parent.parent
CONTEXT_DIR = ROOM_HOP_ROOT / "context"

# Rule-based gợi ý đơn giản: keyword trong topic -> file liên quan.
# Đây KHÔNG phải engine tự động chọn, chỉ để hiển thị gợi ý cho Vinh.
SUGGESTION_RULES: dict[str, list[str]] = {
    "context": ["XU_CORE.md", "XU_SESSION.md", "PROJECT_STATE.md"],
    "memory": ["XU_MEMORY.md", "XU_CORE.md"],
    "session": ["XU_SESSION.md"],
    "dự án": ["PROJECT_STATE.md"],
    "project": ["PROJECT_STATE.md"],
}


class ContextFileNotFoundError(Exception):
    """Raised khi context_files yêu cầu không tồn tại trong context/."""


def suggest_context(topic: str) -> list[str]:
    """
    Trả về danh sách file GỢI Ý dựa trên keyword đơn giản trong topic.
    Đây chỉ là gợi ý hiển thị cho Vinh — không tự động áp dụng vào Meeting.
    """
    topic_lower = topic.lower()
    suggested: list[str] = []
    for keyword, files in SUGGESTION_RULES.items():
        if keyword in topic_lower:
            for f in files:
                if f not in suggested:
                    suggested.append(f)
    return suggested


def validate_context_files(context_files: list[str]) -> None:
    """Kiểm tra mọi file trong context_files thực sự tồn tại trong context/."""
    missing = [f for f in context_files if not (CONTEXT_DIR / f).exists()]
    if missing:
        available = [p.name for p in CONTEXT_DIR.glob("*.md")]
        raise ContextFileNotFoundError(
            f"Các file context không tồn tại: {missing}. "
            f"File hiện có trong context/: {available}"
        )


def package_context(context_files: list[str], destination_dir: Path) -> list[Path]:
    """
    Copy các file context_files (do Vinh chọn thủ công) từ room_hop/context/
    vào thư mục context/ riêng của meeting. KHÔNG BAO GIỜ sửa file gốc.

    Trả về danh sách đường dẫn các file đã copy.
    """
    validate_context_files(context_files)
    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for filename in context_files:
        src = CONTEXT_DIR / filename
        dst = destination_dir / filename
        shutil.copy2(src, dst)  # copy2 giữ nguyên metadata, không sửa src
        copied.append(dst)
    return copied


if __name__ == "__main__":
    demo_topic = "Thiết kế ROOM HOP Context Engine"
    print(f"Topic: {demo_topic}")
    print(f"Gợi ý (chỉ tham khảo, Vinh vẫn phải tự chọn): {suggest_context(demo_topic)}")
