"""
Agent Registry — ROOM HOP v0.1

Nhiệm vụ DUY NHẤT: biết có những AI nào, đọc hồ sơ của chúng từ
room_hop/agents/*.yaml, và validate đúng theo schemas/agent.yaml.

Không xử lý permissions/authority (DEFERRED sang v0.2+).
Không gọi API thật (DEFERRED sang Giai đoạn 3).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

ROOM_HOP_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOM_HOP_ROOT / "agents"

REQUIRED_FIELDS = ["id", "name", "role", "provider", "capabilities"]


class AgentValidationError(Exception):
    """Raised khi một agent.yaml thiếu field bắt buộc hoặc sai kiểu."""


@dataclass
class Agent:
    id: str
    name: str
    role: str
    provider: str
    model: str = ""
    capabilities: list = field(default_factory=list)

    # Forward-compatible, không xử lý ở v0.1
    permissions: dict = field(default_factory=dict)
    authority: dict = field(default_factory=dict)
    priority: Optional[str] = None
    memory_scope: Optional[str] = None
    context_scope: Optional[str] = None

    # GOVERNANCE RULE (v0.2.1, ROOM_HOP_LIFECYCLE_v0.2.1.md — Identity Layer):
    # id của human_principal (trong Principal Registry, core/principal_registry.py)
    # chịu trách nhiệm/authority cho agent này. KHÔNG dùng "owner_principal_id" —
    # agent là một identity có trách nhiệm, không phải tài sản sở hữu. Optional,
    # không bắt buộc trong agents/*.yaml hiện có (backward-compatible, default None).
    responsible_principal_id: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "Agent":
        missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
        if missing:
            raise AgentValidationError(
                f"Agent thiếu field bắt buộc: {missing} — data={data}"
            )
        if not isinstance(data["capabilities"], list):
            raise AgentValidationError(
                f"'capabilities' phải là list, nhận: {type(data['capabilities'])}"
            )
        return Agent(
            id=data["id"],
            name=data["name"],
            role=data["role"],
            provider=data["provider"],
            model=data.get("model", "") or "",
            capabilities=data.get("capabilities", []),
            permissions=data.get("permissions") or {},
            authority=data.get("authority") or {},
            priority=data.get("priority"),
            memory_scope=data.get("memory_scope"),
            context_scope=data.get("context_scope"),
            responsible_principal_id=data.get("responsible_principal_id"),
        )


class AgentRegistry:
    """Đọc toàn bộ agents/*.yaml và cung cấp truy vấn theo id."""

    def __init__(self, agents_dir: Path = AGENTS_DIR):
        self.agents_dir = Path(agents_dir)
        self._agents: dict[str, Agent] = {}
        self._load()

    def _load(self) -> None:
        if not self.agents_dir.exists():
            raise FileNotFoundError(f"Không tìm thấy thư mục agents: {self.agents_dir}")

        for file in sorted(self.agents_dir.glob("*.yaml")):
            with open(file, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            try:
                agent = Agent.from_dict(raw)
            except AgentValidationError as e:
                raise AgentValidationError(f"Lỗi ở file {file.name}: {e}") from e

            if agent.id != file.stem:
                raise AgentValidationError(
                    f"id trong {file.name} ('{agent.id}') phải trùng tên file ('{file.stem}')"
                )
            if agent.id in self._agents:
                raise AgentValidationError(f"Trùng agent id: {agent.id}")
            self._agents[agent.id] = agent

    def list_agents(self) -> list[Agent]:
        return list(self._agents.values())

    def get(self, agent_id: str) -> Agent:
        if agent_id not in self._agents:
            raise KeyError(
                f"Không tìm thấy agent '{agent_id}'. "
                f"Các agent hiện có: {list(self._agents.keys())}"
            )
        return self._agents[agent_id]

    def exists(self, agent_id: str) -> bool:
        return agent_id in self._agents


if __name__ == "__main__":
    registry = AgentRegistry()
    print(f"Đã nạp {len(registry.list_agents())} agent:")
    for a in registry.list_agents():
        print(f"  - {a.id}: {a.name} ({a.role}, {a.provider})")
