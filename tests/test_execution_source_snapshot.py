from __future__ import annotations

import os
from pathlib import Path

import pytest

from execution_host.source_snapshot import workspace_source_sha256


def test_workspace_source_hash_is_deterministic_and_content_sensitive(tmp_path):
    root = tmp_path / "workspace"
    root.mkdir()
    (root / "b.py").write_text("print('b')\n", encoding="utf-8")
    (root / "a.py").write_text("print('a')\n", encoding="utf-8")

    first = workspace_source_sha256(root)
    assert first == workspace_source_sha256(root)

    (root / "a.py").write_text("print('changed')\n", encoding="utf-8")
    assert workspace_source_sha256(root) != first


def test_workspace_source_hash_ignores_git_and_python_cache(tmp_path):
    root = tmp_path / "workspace"
    (root / ".git").mkdir(parents=True)
    (root / "__pycache__").mkdir()
    root.mkdir(exist_ok=True)
    (root / "app.py").write_text("value = 1\n", encoding="utf-8")
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (root / "__pycache__" / "app.pyc").write_bytes(b"cache")
    first = workspace_source_sha256(root)

    (root / ".git" / "HEAD").write_text("ref: refs/heads/other\n", encoding="utf-8")
    (root / "__pycache__" / "app.pyc").write_bytes(b"new cache")
    assert workspace_source_sha256(root) == first


def test_workspace_source_hash_rejects_symlinks(tmp_path):
    root = tmp_path / "workspace"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    try:
        (root / "escape.txt").symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable on this runner")
    with pytest.raises(ValueError, match="execution_workspace_symlink_rejected"):
        workspace_source_sha256(root)
