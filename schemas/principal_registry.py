"""
Principal Registry — ROOM HOP v0.2.1 (GOVERNANCE RULE)

Nhiệm vụ DUY NHẤT: biết có những human_principal nào, đọc hồ sơ của họ từ
room_hop/principals/*.yaml, và validate đúng theo schemas/principal.yaml.

Đây là Registry TÁCH BIỆT với AgentRegistry (core/agent_registry.py), đúng
ROOM_HOP_LIFECYCLE_v0.2.1.md — Identity Layer:

    human_principal  -> Principal Registry
    ai_agent         -> Agent Registry

Không trộn chung 2 registry. Không dùng cái này thay cho cái kia.
Không xử lý authorization/JOIN — đó là việc của Identity Resolution
(core/identity_resolution.py) và Meeting Policy (bước MeetingManager kế
tiếp, CHƯA làm ở bước này).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

ROOM_HOP_ROOT = Path(__file__).resolve().parent.parent
PRINCIPALS_DIR = ROOM_HOP_ROOT / "principals"

REQUIRED_FIELDS = ["id", "name", "type"]


class PrincipalValidationError(Exception):
    """Raised khi một principal.yaml thiếu field bắt buộc hoặc sai kiểu."""


@dataclass
class Principal:
    id: str
    name: str
    type: str = "human_principal"

    # Forward-compatible, chưa có engine xử lý ở v0.2.1
    role: Optional[str] = None
    contact: Optional[str] = None
    authority: dict = field(default_factory=dict)

    @staticmethod
    def from_dict(data: dict) -> "Principal":
        missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
        if missing:
            raise PrincipalValidationError(
                f"Principal thiếu field bắt buộc: {missing} — data={data}"
            )
        if data["type"] != "human_principal":
            raise PrincipalValidationError(
                f"Principal Registry chỉ chứa human_principal, nhận type='{data['type']}' "
                f"(id={data.get('id')}). Nếu đây là AI, khai báo trong agents/*.yaml thay vào đó."
            )
        return Principal(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            role=data.get("role"),
            contact=data.get("contact"),
            authority=data.get("authority") or {},
        )


class PrincipalRegistry:
    """Đọc toàn bộ principals/*.yaml và cung cấp truy vấn theo id."""

    def __init__(self, principals_dir: Path = PRINCIPALS_DIR):
        self.principals_dir = Path(principals_dir)
        self._principals: dict[str, Principal] = {}
        self._load()

    def _load(self) -> None:
        if not self.principals_dir.exists():
            # Không bắt buộc phải tồn tại (khác AgentRegistry) — 1 project có
            # thể chưa đăng ký human_principal nào. Registry rỗng, không lỗi.
            return

        for file in sorted(self.principals_dir.glob("*.yaml")):
            with open(file, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            try:
                principal = Principal.from_dict(raw)
            except PrincipalValidationError as e:
                raise PrincipalValidationError(f"Lỗi ở file {file.name}: {e}") from e

            if principal.id != file.stem:
                raise PrincipalValidationError(
                    f"id trong {file.name} ('{principal.id}') phải trùng tên file ('{file.stem}')"
                )
            if principal.id in self._principals:
                raise PrincipalValidationError(f"Trùng principal id: {principal.id}")
            self._principals[principal.id] = principal

    def list_principals(self) -> list[Principal]:
        return list(self._principals.values())

    def get(self, principal_id: str) -> Principal:
        if principal_id not in self._principals:
            raise KeyError(
                f"Không tìm thấy principal '{principal_id}'. "
                f"Các principal hiện có: {list(self._principals.keys())}"
            )
        return self._principals[principal_id]

    def exists(self, principal_id: str) -> bool:
        return principal_id in self._principals


if __name__ == "__main__":
    registry = PrincipalRegistry()
    print(f"Đã nạp {len(registry.list_principals())} principal:")
    for p in registry.list_principals():
        print(f"  - {p.id}: {p.name} ({p.type})")
