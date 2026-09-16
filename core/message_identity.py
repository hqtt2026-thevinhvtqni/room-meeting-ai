"""
Message v1.0 — Header resolution helper.

ROOM HOP MESSAGE v1.0 IMPLEMENTATION CONTRACT (LOCKED):

    role không được caller tự khai báo, phải resolve từ
    Identity / Principal Registry.

This module is purely additive: it does NOT modify
core/identity_resolution.py, core/principal_registry.py, or
core/agent_registry.py. It only reads their existing output to build
a Message Header.

    identity_id
        -> resolve_identity() (existing, unchanged)
        -> Principal/Agent Registry lookup (existing, unchanged)
        -> Header v1.0 {name, role, date, time}

If identity_id does not resolve in any Registry, this module raises
MessageIdentityError. It NEVER fabricates a name/role and NEVER falls
back to a default identity (e.g. "vinh", "claude") to fill the Header.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from core.agent_registry import AgentRegistry
from core.identity_resolution import resolve_identity
from core.principal_registry import PrincipalRegistry

# Allowed values for Message.source.type (LOCKED — Message v1.0 contract).
SOURCE_HUMAN = "human"
SOURCE_AI_MCP = "ai_mcp"
SOURCE_AI_CHAT_PASTE = "ai_chat_paste"


class MessageIdentityError(Exception):
    """Raised when a caller-supplied identity_id cannot be resolved.

    Per contract: "Nếu identity không resolve được: REJECT. Không
    fallback sang role do caller khai."
    """


def build_header(
    identity_id: str,
    principal_registry: Optional[PrincipalRegistry] = None,
    agent_registry: Optional[AgentRegistry] = None,
) -> tuple[dict, str]:
    """
    Resolve identity_id into (header, source_type).

    header = {
        "name": <from Registry>,
        "role": <from Registry>,
        "date": "YYYY-MM-DD",   # AI Message Header v1.0 (human-readable)
        "time": "HH:MM",        # AI Message Header v1.0 (human-readable)
    }
    source_type = "human" (Principal Registry) | "ai_mcp" (Agent Registry)

    Raises MessageIdentityError if identity_id resolves to neither
    registry. Never invents name/role.
    """
    principal_registry = principal_registry or PrincipalRegistry()
    agent_registry = agent_registry or AgentRegistry()

    resolution = resolve_identity(
        identity_id,
        principal_registry,
        agent_registry,
    )

    if not resolution.is_resolved:
        raise MessageIdentityError(
            f"Identity '{identity_id}' không resolve được qua "
            "Identity/Principal/Agent Registry."
        )

    if resolution.resolved_via == "principal_registry":
        principal = principal_registry.get(identity_id)
        name = principal.name
        role = principal.role
        source_type = SOURCE_HUMAN
    else:
        # resolved_via == "agent_registry"
        agent = agent_registry.get(identity_id)
        name = agent.name
        role = agent.role
        source_type = SOURCE_AI_MCP

    now = datetime.now(timezone.utc)
    header = {
        "name": name,
        "role": role,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
    }

    return header, source_type


__all__ = [
    "MessageIdentityError",
    "build_header",
    "SOURCE_HUMAN",
    "SOURCE_AI_MCP",
    "SOURCE_AI_CHAT_PASTE",
]
