from dataclasses import dataclass, field
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

class ActionValidationError(ValueError):
    """Raised when an action violates the Action Contract."""
    pass


def validate_action_type(action_type: str) -> None:
    """Enforce Action Contract: unknown action → REJECT."""
    if action_type not in CANONICAL_ACTIONS:
        raise ActionValidationError(
            f"Unknown action type '{action_type}'. "
            f"Allowed: {sorted(CANONICAL_ACTIONS)}"
        )


def validate_action_fields(action_type: str, target: str | None, value: str | None) -> None:
    """Enforce required fields per Action Contract."""
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


@dataclass
class Action:
    type: str
    target: str | None = None
    value: str | None = None
    args: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Harden: reject unknown actions at construction time
        validate_action_type(self.type)
        validate_action_fields(self.type, self.target, self.value)


@dataclass
class ActionResult:
    ok: bool
    action: Action
    observation: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    status: str = "success"  # success | fail | blocked


@dataclass
class TaskResult:
    status: Literal["PASS", "FAIL", "BLOCKED"]
    task: str
    steps: list[ActionResult] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    state_trace: list[str] = field(default_factory=list)  # PLANNED → RUNNING → VERIFYING → ...
