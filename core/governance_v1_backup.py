"""
Governance — ROOM HOP v0.2

Central authorization mechanism for enforcing the authority hierarchy:
VINH > XU > AGENT

Principles:
- Filesystem access ≠ governance authority
- Agent having capability does NOT mean agent is authorized
- All protected operations must pass authorization check
- Authorization is centralized, testable, explainable
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Agent(str, Enum):
    """Agents in the authority hierarchy."""
    VINH = "vinh"          # Final Authority
    XU = "xu"              # CEO / AI Core
    QUAN_GIA = "quan_gia"  # Operations Manager (experimental, outside chain)
    CLAUDE = "claude"      # Generic agent
    OTHER = "other"        # Generic agent (default)


class ResourceType(str, Enum):
    """Resource classification for authorization."""
    CORE = "core"               # XU_CORE.md, XU_MEMORY.md (most protected)
    GOVERNANCE = "governance"   # AGENTS.md, governance rules
    PROJECT_STATE = "project_state"  # PROJECT_STATE.md
    SESSION = "session"         # XU_SESSION.md
    CONTEXT = "context"         # Context files (read-only)
    MEETING = "meeting"         # Meeting artifacts
    WORKSPACE = "workspace"     # General project files/folders (code, docs, tests...)


class Action(str, Enum):
    """Operations on resources."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"            # Modify governance rules


class AuthorizationResult:
    """Result of an authorization check."""
    
    def __init__(self, allowed: bool, reason: str = ""):
        self.allowed = allowed
        self.reason = reason
    
    def __bool__(self):
        return self.allowed
    
    def __repr__(self):
        status = "ALLOW" if self.allowed else "DENY"
        return f"AuthResult({status}: {self.reason})"


@dataclass
class PermissionPolicy:
    """
    Permission policy defines what actions each agent can perform on each resource type.
    
    Policy is defined as:
    resource_type → agent → action → allowed
    """
    
    # XU_CORE.md, XU_MEMORY.md — Only VINH can write
    CORE_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ},
        Agent.QUAN_GIA: {Action.READ},
        Agent.CLAUDE: {Action.READ},
        Agent.OTHER: {Action.READ},
    }
    
    # AGENTS.md, governance rules — Only VINH can modify
    GOVERNANCE_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ},
        Agent.QUAN_GIA: {Action.READ},
        Agent.CLAUDE: {Action.READ},
        Agent.OTHER: {Action.READ},
    }
    
    # PROJECT_STATE.md — Only Xu + QUAN_GIA can write
    PROJECT_STATE_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ, Action.WRITE},
        Agent.QUAN_GIA: {Action.READ, Action.WRITE},
        Agent.CLAUDE: {Action.READ},
        Agent.OTHER: {Action.READ},
    }
    
    # XU_SESSION.md — Working memory, can be modified by Xu
    SESSION_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ, Action.WRITE},
        Agent.QUAN_GIA: {Action.READ, Action.WRITE},
        Agent.CLAUDE: {Action.READ},
        Agent.OTHER: {Action.READ},
    }
    
    # Context files — Read-only for all
    CONTEXT_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ},
        Agent.QUAN_GIA: {Action.READ},
        Agent.CLAUDE: {Action.READ},
        Agent.OTHER: {Action.READ},
    }
    
    # Meeting lifecycle — Specific rules per action
    MEETING_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ, Action.WRITE},
        Agent.QUAN_GIA: {Action.READ, Action.WRITE},
        Agent.CLAUDE: {Action.READ, Action.WRITE},
        Agent.OTHER: {Action.READ, Action.WRITE},
    }
    
    # General project files/folders (code, docs, non-core content) —
    # named team roles can read/write; generic/unknown agents read-only.
    # WRITE ở đây KHÔNG bao giờ áp dụng cho path thuộc CORE/GOVERNANCE/
    # CONTEXT/PROJECT_STATE/SESSION/MEETING — những path đó được phân loại
    # vào đúng ResourceType của chúng TRƯỚC khi tới nhánh WORKSPACE
    # (xem classify_path trong core/file_ops_agent.py).
    WORKSPACE_PERMISSIONS = {
        Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN},
        Agent.XU: {Action.READ, Action.WRITE},
        Agent.QUAN_GIA: {Action.READ, Action.WRITE},
        Agent.CLAUDE: {Action.READ, Action.WRITE},
        Agent.OTHER: {Action.READ},
    }

    @classmethod
    def get_policy(cls, resource_type: ResourceType) -> dict:
        """Get permission policy for a resource type."""
        if resource_type == ResourceType.CORE:
            return cls.CORE_PERMISSIONS
        elif resource_type == ResourceType.GOVERNANCE:
            return cls.GOVERNANCE_PERMISSIONS
        elif resource_type == ResourceType.PROJECT_STATE:
            return cls.PROJECT_STATE_PERMISSIONS
        elif resource_type == ResourceType.SESSION:
            return cls.SESSION_PERMISSIONS
        elif resource_type == ResourceType.CONTEXT:
            return cls.CONTEXT_PERMISSIONS
        elif resource_type == ResourceType.MEETING:
            return cls.MEETING_PERMISSIONS
        elif resource_type == ResourceType.WORKSPACE:
            return cls.WORKSPACE_PERMISSIONS
        else:
            # Default: deny all for unknown resource types
            return {Agent.VINH: {Action.READ, Action.WRITE, Action.ADMIN}}


class AuthorizationEngine:
    """
    Central authorization engine that enforces the authority hierarchy.
    
    Responsibility:
    - Check agent identity
    - Evaluate against permission policy
    - Return deterministic ALLOW/DENY decision
    - Explain authorization result
    """
    
    def __init__(self):
        self.policy = PermissionPolicy()
    
    def _parse_agent(self, agent_id: str) -> Agent:
        """Convert agent_id string to Agent enum."""
        agent_id = agent_id.lower().strip()
        try:
            return Agent(agent_id)
        except ValueError:
            # Unknown agent defaults to OTHER
            if agent_id == "vinh":
                return Agent.VINH
            elif agent_id == "xu":
                return Agent.XU
            elif agent_id == "quan_gia":
                return Agent.QUAN_GIA
            elif agent_id == "claude":
                return Agent.CLAUDE
            else:
                return Agent.OTHER
    
    def check(
        self,
        agent_id: str,
        resource_type: ResourceType,
        action: Action,
    ) -> AuthorizationResult:
        """
        Check if agent is authorized to perform action on resource.
        
        Args:
            agent_id: Agent identifier (e.g., "xu", "claude")
            resource_type: Type of resource (e.g., CORE, GOVERNANCE)
            action: Action to perform (e.g., READ, WRITE)
        
        Returns:
            AuthorizationResult with ALLOW/DENY and explanation
        """
        agent = self._parse_agent(agent_id)
        policy = PermissionPolicy.get_policy(resource_type)
        
        # Get allowed actions for this agent on this resource
        allowed_actions = policy.get(agent, set())
        
        # Check if action is in allowed set
        if action in allowed_actions:
            reason = f"{agent.value} → {resource_type.value} :: {action.value} ALLOWED"
            return AuthorizationResult(True, reason)
        else:
            reason = (
                f"{agent.value} cannot {action.value} {resource_type.value} "
                f"(allowed: {', '.join(a.value for a in allowed_actions) or 'none'})"
            )
            return AuthorizationResult(False, reason)
    
    def check_meeting_transition(
        self,
        agent_id: str,
        current_status: str,
        target_status: str,
    ) -> AuthorizationResult:
        """
        Check if agent can transition meeting from current_status to target_status.
        
        Allowed transitions:
        - open → closed (requires WRITE permission on MEETING)
        - Any other transition is denied
        """
        agent = self._parse_agent(agent_id)
        
        # Define allowed transitions
        allowed_transitions = {
            ("open", "closed"): {Agent.VINH, Agent.XU, Agent.QUAN_GIA},
        }
        
        transition = (current_status, target_status)
        allowed_agents = allowed_transitions.get(transition, set())
        
        if agent in allowed_agents:
            reason = f"{agent.value} can transition {current_status} → {target_status}"
            return AuthorizationResult(True, reason)
        else:
            reason = (
                f"{agent.value} cannot transition {current_status} → {target_status} "
                f"(allowed: {', '.join(a.value for a in allowed_agents) or 'none'})"
            )
            return AuthorizationResult(False, reason)
    
    def can_escalate_authority(self, agent_id: str) -> bool:
        """
        Check if agent is attempting to escalate their own authority.
        For now, always deny self-escalation.
        """
        # An agent CANNOT modify their own authority
        # This would be an escalation attempt
        return False


# Singleton instance for use throughout the application
_auth_engine: Optional[AuthorizationEngine] = None


def get_authorization_engine() -> AuthorizationEngine:
    """Get the singleton authorization engine."""
    global _auth_engine
    if _auth_engine is None:
        _auth_engine = AuthorizationEngine()
    return _auth_engine
