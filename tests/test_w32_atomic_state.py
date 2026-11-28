from concurrent.futures import ThreadPoolExecutor

import yaml

from core.agent_registry import AgentRegistry
from core.meeting_manager import MeetingManager


def _manager(tmp_path):
    return MeetingManager(
        registry=AgentRegistry(),
        meetings_dir=tmp_path / "meetings",
    )


def test_generated_meeting_ids_are_unique_under_concurrent_creation(tmp_path):
    manager = _manager(tmp_path)

    def create_one(_):
        meeting = manager.create_meeting(
            meeting_id=None,
            topic="concurrent ID allocation",
            participants=[],
            context_files=[],
        )
        return meeting.data["id"]

    with ThreadPoolExecutor(max_workers=8) as executor:
        ids = list(executor.map(create_one, range(8)))

    assert len(ids) == 8
    assert len(set(ids)) == 8


def test_concurrent_join_updates_from_separate_meeting_objects_are_not_lost(tmp_path):
    manager = _manager(tmp_path)
    created = manager.create_meeting(
        meeting_id="STATE-CONCURRENT-001",
        topic="serialized meeting state",
        participants=["xu", "claude"],
        context_files=[],
    )
    created.open_session()

    first = manager.get_meeting("STATE-CONCURRENT-001")
    second = manager.get_meeting("STATE-CONCURRENT-001")

    with ThreadPoolExecutor(max_workers=2) as executor:
        a = executor.submit(first.join_request, "xu")
        b = executor.submit(second.join_request, "claude")
        a.result()
        b.result()

    saved = manager.get_meeting("STATE-CONCURRENT-001").data
    assert {"xu", "claude"}.issubset(set(saved["participants"]))


def test_meeting_yaml_save_uses_atomic_replace(tmp_path):
    manager = _manager(tmp_path)
    meeting = manager.create_meeting(
        meeting_id="STATE-ATOMIC-001",
        topic="atomic save",
        participants=[],
        context_files=[],
    )

    updated = meeting.data
    updated["topic"] = "updated atomically"
    meeting._save(updated)

    reread = yaml.safe_load((meeting.meeting_dir / "meeting.yaml").read_text(encoding="utf-8"))
    assert reread["topic"] == "updated atomically"
    assert not list(meeting.meeting_dir.glob(".meeting.yaml.*.tmp"))
