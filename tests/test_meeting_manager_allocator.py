"""
Tests for MeetingManager._allocate_meeting_id() and the create_meeting()
wiring around it.

Scope note: _allocate_meeting_id() itself never calls resolve_identity()
(it only scans meetings_dir), so it is unit-tested directly, with zero
dependency on PrincipalRegistry/AgentRegistry file layout.

For the two tests that go through create_meeting() end-to-end
(test_create_meeting_without_id_uses_allocator,
test_create_meeting_with_explicit_id_bypasses_allocator), resolve_identity
is monkeypatched to always resolve. core/identity_resolution.py was not
part of the evidence read for this task, so its real behavior is not
exercised here — this stub only isolates the allocator wiring under test.
Replace/remove the monkeypatch once identity_resolution.py is reviewed
and a proper fixture (real principals/agents yaml) is set up, ideally
shared with existing identity/join tests elsewhere in the suite.

Adjust the import path below if the project's real test layout differs;
this file was written standalone since existing conftest/fixture
conventions were not part of the evidence provided.
"""

from __future__ import annotations

import pytest

from core.meeting_manager import MeetingError, MeetingManager


@pytest.fixture
def manager(tmp_path):
    return MeetingManager(meetings_dir=tmp_path / "meetings")


class _AlwaysResolved:
    is_resolved = True
    identity_type = "human_principal"
    registry_check = "PASS"


@pytest.fixture(autouse=True)
def _stub_identity_resolution(monkeypatch):
    monkeypatch.setattr(
        "core.meeting_manager.resolve_identity",
        lambda identity_id, principal_registry, agent_registry: _AlwaysResolved(),
    )


# ---------------------------------------------------------------------------
# _allocate_meeting_id() — pure unit tests, no identity resolution involved
# ---------------------------------------------------------------------------

def test_allocate_first_id_for_empty_dir(manager):
    meeting_id = manager._allocate_meeting_id()
    year = meeting_id.split("-")[1]
    assert meeting_id == f"MEETING-{year}-001"


def test_allocate_uses_max_plus_one_not_len(manager):
    # Simulate a gap: 001 exists, 003 exists, 002 was deleted by hand.
    # len(existing) would wrongly give 003 (2 dirs + 1); max(seq)+1 must
    # give 004.
    manager.meetings_dir.mkdir(parents=True, exist_ok=True)
    year = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).year
    (manager.meetings_dir / f"MEETING-{year}-001").mkdir()
    (manager.meetings_dir / f"MEETING-{year}-003").mkdir()

    meeting_id = manager._allocate_meeting_id()

    assert meeting_id == f"MEETING-{year}-004"


def test_allocate_ignores_other_years(manager):
    manager.meetings_dir.mkdir(parents=True, exist_ok=True)
    (manager.meetings_dir / "MEETING-2020-099").mkdir()

    meeting_id = manager._allocate_meeting_id()
    year = meeting_id.split("-")[1]

    assert year != "2020"
    assert meeting_id.endswith("-001")


def test_allocate_ignores_malformed_directory_names(manager):
    manager.meetings_dir.mkdir(parents=True, exist_ok=True)
    (manager.meetings_dir / "not-a-meeting-dir").mkdir()
    (manager.meetings_dir / "MEETING-broken").mkdir()

    # Should not raise, should not be influenced by junk dirs.
    meeting_id = manager._allocate_meeting_id()
    assert meeting_id.endswith("-001")


# ---------------------------------------------------------------------------
# create_meeting() wiring
# ---------------------------------------------------------------------------

def test_create_meeting_without_id_uses_allocator(manager):
    meeting = manager.create_meeting(
        meeting_id=None,
        topic="Test topic",
        participants=[],
        context_files=[],
        created_by="vinh",
    )

    assert meeting.data["id"].startswith("MEETING-")
    assert meeting.data["status"] == "draft"


def test_create_meeting_with_explicit_id_bypasses_allocator(manager):
    meeting = manager.create_meeting(
        meeting_id="MEETING-CUSTOM-ID",
        topic="Test topic",
        participants=[],
        context_files=[],
        created_by="vinh",
    )

    assert meeting.data["id"] == "MEETING-CUSTOM-ID"


def test_create_meeting_positional_args_backward_compatible(manager):
    """
    Locks the exact calling convention used by the pre-existing
    tests/test_meeting_lifecycle_v021.py: meeting_id passed as the
    first POSITIONAL argument (not keyword-only). This is the
    regression that a first draft of the allocator patch introduced
    by making create_meeting keyword-only — guarding against it
    recurring.
    """
    meeting = manager.create_meeting(
        "MEETING-LIFE-001", "Secretary integration", ["xu"], [], created_by="vinh"
    )
    assert meeting.data["id"] == "MEETING-LIFE-001"
    assert meeting.data["status"] == "draft"


def test_create_meeting_collision_raises_meeting_error(manager):
    manager.create_meeting(
        meeting_id="MEETING-DUP-ID",
        topic="First",
        participants=[],
        context_files=[],
        created_by="vinh",
    )

    with pytest.raises(MeetingError):
        manager.create_meeting(
            meeting_id="MEETING-DUP-ID",
            topic="Second",
            participants=[],
            context_files=[],
            created_by="vinh",
        )