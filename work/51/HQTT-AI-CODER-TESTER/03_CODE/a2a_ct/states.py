"""Task state machine — aligned with A2A task lifecycle.

A2A task states used in this slice:
  submitted, working, input-required, completed, failed, canceled

Terminal states are immutable (matches ROOM-HOP "closed is immutable" rule).

Work-51 BLOCKED mapping (D-02 in DECISION_REGISTER):
  BLOCKED is a *pipeline* outcome, not an A2A task state.
  Orchestrator maps BLOCKED -> task state `failed` + metadata {"blocked": true}.
"""

from __future__ import annotations

TASK_STATES = (
    "submitted",
    "working",
    "input-required",
    "completed",
    "failed",
    "canceled",
)

_VALID_TRANSITIONS: dict[str, set[str]] = {
    "submitted": {"working", "input-required", "failed", "canceled"},
    "working": {"input-required", "completed", "failed", "canceled"},
    "input-required": {"working", "failed", "canceled"},
    # Terminal states are immutable.
    "completed": set(),
    "failed": set(),
    "canceled": set(),
}


class TaskStateError(Exception):
    """Raised when a task state transition is illegal."""


def assert_transition(current: str, next_state: str) -> str:
    """Return next_state if the transition is legal, else raise TaskStateError."""
    if current not in TASK_STATES:
        raise TaskStateError(f"unknown current state: {current!r}")
    if next_state not in TASK_STATES:
        raise TaskStateError(f"unknown next state: {next_state!r}")
    if next_state != current and next_state not in _VALID_TRANSITIONS[current]:
        raise TaskStateError(f"illegal transition: {current} -> {next_state}")
    return next_state


def is_terminal(state: str) -> bool:
    return state in ("completed", "failed", "canceled")
