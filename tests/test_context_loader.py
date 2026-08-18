import hashlib

import pytest

from core.context_loader import (
    CONTEXT_DIR,
    ContextFileNotFoundError,
    package_context,
    suggest_context,
    validate_context_files,
)


def _md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def test_suggest_context_matches_keyword():
    suggestions = suggest_context("Thiết kế ROOM HOP Context Engine")
    assert "XU_CORE.md" in suggestions


def test_suggest_context_no_match_returns_empty():
    suggestions = suggest_context("Chủ đề không liên quan gì tới các keyword đã khai báo")
    assert suggestions == []


def test_validate_context_files_ok():
    # không raise
    validate_context_files(["XU_CORE.md", "XU_SESSION.md"])


def test_validate_context_files_missing_raises():
    with pytest.raises(ContextFileNotFoundError):
        validate_context_files(["FILE_KHONG_TON_TAI.md"])


def test_package_context_copies_without_modifying_source(tmp_path):
    files = ["XU_CORE.md", "PROJECT_STATE.md"]
    source_hashes_before = {f: _md5(CONTEXT_DIR / f) for f in files}

    dest = tmp_path / "meeting_context"
    copied = package_context(files, dest)

    # đã copy đúng số file, đúng nội dung
    assert len(copied) == 2
    for f in files:
        assert (dest / f).exists()
        assert _md5(dest / f) == source_hashes_before[f]

    # 🔒 nguyên tắc khóa: file GỐC không hề bị thay đổi
    source_hashes_after = {f: _md5(CONTEXT_DIR / f) for f in files}
    assert source_hashes_after == source_hashes_before
