import pytest

from core.agent_registry import AgentRegistry
from core.context_loader import ContextFileNotFoundError, validate_context_files
from core.meeting_manager import MeetingError, MeetingManager


def test_meeting_manager_rejects_traversal_id_before_creating_directory(tmp_path):
    meetings = tmp_path / "meetings"
    manager = MeetingManager(
        registry=AgentRegistry(),
        meetings_dir=meetings,
    )

    with pytest.raises(MeetingError, match="meeting_id"):
        manager.create_meeting(
            meeting_id="../outside",
            topic="unsafe",
            participants=[],
            context_files=[],
        )

    assert not (tmp_path / "outside").exists()


def test_meeting_manager_rejects_absolute_id(tmp_path):
    manager = MeetingManager(
        registry=AgentRegistry(),
        meetings_dir=tmp_path / "meetings",
    )

    with pytest.raises(MeetingError, match="meeting_id"):
        manager.get_meeting(str(tmp_path / "outside"))


@pytest.mark.parametrize(
    "filename",
    ["../XU_CORE.md", "/tmp/secret.md", r"..\\secret.md", ".", ".."],
)
def test_context_loader_rejects_paths_outside_context(filename):
    with pytest.raises(ContextFileNotFoundError, match="Context path"):
        validate_context_files([filename])
