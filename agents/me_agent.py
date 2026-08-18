"""
MeAgent — CXO-ME (Mê)

Agent nội bộ, không gọi API bên ngoài. Chạy local trong tiến trình Python
(không phải Meta AI API thật — đây là 1 rule-based/local agent đại diện
cho vai trò CXO/UX trong meeting, tương tự MockConnector nhưng logic nằm
trong chính agent thay vì kịch bản cứng).

Output tuân theo giao thức STATUS: REPLY/PASS/FINAL giống mọi agent khác,
để tương thích với Discussion Engine qua InternalConnector (core/connectors.py).
"""

from __future__ import annotations


class MeAgent:
    ROLE = "CXO-ME"
    NAME = "Mê"

    def execute(self, task: str, history: list[dict] | None = None) -> str:
        """
        Nhận task + lịch sử hội thoại, trả về raw text có dòng STATUS đầu tiên.
        Logic v0.1: agent luôn REPLY một lần góp ý theo góc nhìn UX/CXO,
        sau đó FINAL ở lượt kế tiếp nếu đã có ý kiến trước đó trong history.
        (Đây là behavior giữ chỗ — thay bằng logic/luật thật khi cần.)
        """
        already_spoke = any(
            m.get("speaker") == "me_meta" for m in (history or [])
        )
        if already_spoke:
            return f"STATUS: FINAL\n[{self.NAME}] Đã góp ý xong, đề xuất chốt: {task}"
        return f"STATUS: REPLY\n[{self.NAME}] Góc nhìn CXO/UX về: {task}"
