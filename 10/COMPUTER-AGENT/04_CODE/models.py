from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Literal

# Canonical action types — single source of truth
CANONICAL_ACTIONS = {
    "observe", "navigate", "click", "type", "key_press",
    "scroll", "wait", "extract", "screenshot", "download", "close"
}

ActionType = Literal[
    "observe", "navigate", "click", "type", "key_press",
    "scroll", "wait", "extract", "screenshot", "download", "close"
]

# Actions that the LOCKED Safety Policy classifies as destructive.
# They are REJECTED unless the policy (server-side) explicitly allows them.
DESTRUCTIVE_ACTIONS = {"download"}

# Error text fragments that mark a *transient* failure eligible for retry.
TRANSIENT_ERROR_MARKERS = (
    "timeout", "timed out", "temporarily", "network",
    "connection reset", "econnreset", "resource temporarily unavailable",
)


class ActionValidationError(ValueError):
    """Raised when an action violates the Action Contract."""


@dataclass
class SafetyPolicy:
    """Executable form of 03_ARCHITECTURE/SAFETY_POLICY.md (LOCKED).

    Every field here is enforced by AgentRuntime, not just documented.
    """

    max_action_retries: int = 2                 # §2 action-level retry: max 2
    retry_backoff_seconds: float = 0.5          # §2 minimum 500 ms backoff
    action_timeout_seconds: float = 30.0        # §3 single action: 30 s
    wait_max_seconds: float = 120.0             # §3 wait: max 120 s
    observation_timeout_seconds: float = 15.0   # §3 observation/extract: 15 s
    workflow_timeout_seconds: float = 600.0     # §3 entire workflow: 10 min
    allow_destructive: bool = False             # §4 destructive must be explicit
    allowed_path_prefixes: tuple = ("06_EVIDENCE",)  # §5 boundary for artifacts
    allowed_domains: tuple | None = None        # §5 None = no domain restriction
    work_root: str | None = None                # §5 absolute Work root, when known

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_action_type(action_type: str) -> None:
    """Enforce Action Contract: unknown action → REJECT."""
    if action_type not in CANONICAL_ACTIONS:
        raise ActionValidationError(
            f"Unknown action type '{action_type}'. "
            f"Allowed: {sorted(CANONICAL_ACTIONS)}"
        )


def _numeric(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ActionValidationError(
            f"{field_name} must be numeric, got {value!r}"
        ) from None


def validate_action_fields(
    action_type: str,
    target: str | None,
    value: Any,
    args: dict[str, Any] | None = None,
) -> None:
    """Enforce required fields per Action Contract (03_ARCHITECTURE/ACTION_CONTRACT.md)."""
    args = args or {}
    if action_type == "click" and not target:
        raise ActionValidationError("click requires non-empty 'target'")
    if action_type == "type":
        if not target:
            raise ActionValidationError("type requires non-empty 'target'")
        if value is None:
            raise ActionValidationError("type requires 'value'")
    if action_type == "navigate" and not value:
        raise ActionValidationError("navigate requires non-empty 'value' (url)")
    if action_type == "key_press" and not value:
        raise ActionValidationError("key_press requires non-empty 'value' (key)")
    # Contract §3: wait requires `value` (seconds). Previously only args["seconds"]
    # was read, so a wait with no value slipped through — that mismatch is fixed.
    if action_type == "wait":
        if value is None and "seconds" not in args:
            raise ActionValidationError("wait requires 'value' (seconds)")
        seconds = _numeric(value if value is not None else args.get("seconds"), "wait value")
        if seconds < 0:
            raise ActionValidationError("wait value must be >= 0")
    # Contract §3: scroll accepts target? and value? (amount). args["amount"] kept
    # as an accepted alias so existing workflows keep working.
    if action_type == "scroll":
        raw = value if value is not None else args.get("amount")
        if raw is not None:
            _numeric(raw, "scroll amount")
    if action_type == "extract":
        schema = args.get("schema")
        if schema is not None and not isinstance(schema, dict):
            raise ActionValidationError("extract 'schema' must be an object when provided")


@dataclass
class Action:
    type: str
    target: str | None = None
    value: Any = None
    args: dict[str, Any] = field(default_factory=dict)
    destructive: bool = False

    def __post_init__(self):
        # Harden: reject unknown actions at construction time
        validate_action_type(self.type)
        validate_action_fields(self.type, self.target, self.value, self.args)

    @property
    def is_destructive(self) -> bool:
        return bool(self.destructive) or self.type in DESTRUCTIVE_ACTIONS


@dataclass
class ActionResult:
    ok: bool
    action: Action
    observation: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    status: str = "success"  # success | fail | blocked
    outcome_uncertain: bool = False
    attempts: int = 1
    timeout_seconds: float | None = None
    duration_ms: int | None = None


@dataclass
class TaskResult:
    status: Literal["PASS", "FAIL", "BLOCKED"]
    task: str
    steps: list[ActionResult] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    state_trace: list[str] = field(default_factory=list)
    work_id: str = "10"
    started_at: str | None = None
    finished_at: str | None = None
    policy: dict[str, Any] | None = None
