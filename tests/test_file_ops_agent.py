"""
FileOpsAgent Tests — ROOM HOP v0.2 (bản V2: Soft Delete + Audit)

Thay thế tests/test_file_ops_agent.py cũ (nhắm vào bản FileOpsAgent v1 —
AuthorizationEngine/ResourceType — đã bị Copilot viết đè). Test này bám
theo hành vi thật đang chạy: GOV-based permission, soft-delete vào trash/,
backup .bak khi edit.

Lưu ý: FileOpsAgent V2 thao tác qua path tương đối với current working
directory (os.makedirs/open trực tiếp, không tự ép về 1 project root cố
định) — test chạy trong tmp_path do pytest cấp + chdir để không đụng file
thật của dự án.
"""

import os
from pathlib import Path

import pytest

from core.file_ops_agent import FileOpsAgent
from core.governance import MissionContext


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Chạy mỗi test trong 1 thư mục tạm riêng, không đụng file thật của dự án."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def research_mission():
    # scope mac dinh cua MissionContext da bao gom "research/*","docs/*","tmp/*"
    return MissionContext(name="test_mission", allow_delete=True)


class TestCreateFile:
    def test_vinh_create_file(self, workdir):
        agent = FileOpsAgent("vinh")
        result = agent.create_file("notes.md", "hello")
        assert "OK" in result
        assert Path("notes.md").read_text(encoding="utf-8") == "hello"

    def test_agent_llama_create_in_research_scope(self, workdir, research_mission):
        agent = FileOpsAgent("agent_llama", research_mission)
        agent.create_file("research/idea.md", "content")
        assert Path("research/idea.md").exists()

    def test_agent_llama_denied_outside_scope(self, workdir, research_mission):
        agent = FileOpsAgent("agent_llama", research_mission)
        with pytest.raises(PermissionError):
            agent.create_file("outside_zone/file.md", "x")

    def test_create_existing_file_raises(self, workdir):
        agent = FileOpsAgent("vinh")
        agent.create_file("dup.md", "v1")
        with pytest.raises(FileExistsError):
            agent.create_file("dup.md", "v2")


class TestEditFile:
    def test_edit_creates_backup_in_trash(self, workdir):
        agent = FileOpsAgent("vinh")
        agent.create_file("doc.md", "v1")
        agent.edit_file("doc.md", "v2")
        assert Path("doc.md").read_text(encoding="utf-8") == "v2"
        backups = list(Path("trash").glob("*doc.md.bak"))
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "v1"


class TestReadAndList:
    def test_read_file(self, workdir):
        agent = FileOpsAgent("vinh")
        agent.create_file("readme.md", "xin chao")
        assert agent.read_file("readme.md") == "xin chao"

    def test_list_dir(self, workdir):
        agent = FileOpsAgent("vinh")
        agent.create_file("a.md", "1")
        agent.create_file("b.md", "2")
        names = agent.list_dir(".")
        assert "a.md" in names and "b.md" in names


class TestSoftDelete:
    def test_delete_moves_to_trash_not_removed(self, workdir, research_mission):
        agent = FileOpsAgent("agent_llama", research_mission)
        agent.create_file("tmp/junk.txt", "x")
        result = agent.delete_file("tmp/junk.txt")
        assert "Soft-Delete" in result
        assert not Path("tmp/junk.txt").exists()
        assert any(Path("trash").glob("*junk.txt"))

    def test_delete_denied_without_allow_delete(self, workdir):
        mission = MissionContext(name="no_delete", allow_delete=False)
        agent = FileOpsAgent("agent_llama", mission)
        agent.create_file("tmp/junk2.txt", "x")
        with pytest.raises(PermissionError):
            agent.delete_file("tmp/junk2.txt")

    def test_delete_nonexistent_file_returns_message_not_raise(self, workdir, research_mission):
        agent = FileOpsAgent("agent_llama", research_mission)
        result = agent.delete_file("tmp/ghost.txt")
        assert "khong ton tai" in result


class TestHardDelete:
    def test_hard_delete_requires_vinh_identity(self, workdir):
        agent = FileOpsAgent("agent_llama")
        with pytest.raises(PermissionError):
            agent.delete_file_hard("anything.txt")

    def test_vinh_hard_delete_removes_permanently(self, workdir):
        agent = FileOpsAgent("vinh")
        agent.create_file("gone.md", "x")
        agent.delete_file_hard("gone.md")
        assert not Path("gone.md").exists()
        # Hard delete khong di qua trash/
        assert not any(Path("trash").glob("*gone.md*"))


class TestProtectedPaths:
    def test_cannot_edit_governance_module_without_agent_llama_scope(self, workdir, research_mission):
        agent = FileOpsAgent("agent_llama", research_mission)
        # tao "core/governance.py" gia trong sandbox tmp de test hanh vi
        os.makedirs("core", exist_ok=True)
        Path("core/governance.py").write_text("placeholder", encoding="utf-8")
        with pytest.raises(PermissionError):
            agent.edit_file("core/governance.py", "hacked")
