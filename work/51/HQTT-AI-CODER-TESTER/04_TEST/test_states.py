"""Task state machine: legal transitions pass, illegal ones raise."""

import pytest

from a2a_ct.states import TaskStateError, assert_transition, is_terminal


@pytest.mark.parametrize("current,next_state", [
    ("submitted", "working"),
    ("working", "completed"),
    ("working", "failed"),
    ("working", "canceled"),
    ("submitted", "canceled"),
])
def test_legal_transitions(current, next_state):
    assert assert_transition(current, next_state) == next_state


@pytest.mark.parametrize("current,next_state", [
    ("completed", "working"),   # terminal states are immutable
    ("failed", "working"),
    ("canceled", "submitted"),
    ("completed", "completed_bogus"),
])
def test_illegal_transitions_raise(current, next_state):
    with pytest.raises(TaskStateError):
        assert_transition(current, next_state)


def test_unknown_states_raise():
    with pytest.raises(TaskStateError):
        assert_transition("bogus", "working")


def test_terminal_detection():
    assert is_terminal("completed")
    assert is_terminal("failed")
    assert is_terminal("canceled")
    assert not is_terminal("working")
