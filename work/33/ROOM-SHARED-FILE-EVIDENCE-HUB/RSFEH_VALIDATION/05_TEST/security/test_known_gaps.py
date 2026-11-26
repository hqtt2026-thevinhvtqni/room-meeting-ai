"""Security/data-isolation regression probes for known RSFEH gaps.

These tests are strict xfails until the implementation is repaired.
An XPASS is treated as a failure so the marker must be removed after repair.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "04_CODE" / "src"
sys.path.insert(0, str(SRC))

from rsfeh.store import RSFEHError, Store  # noqa: E402


@pytest.fixture
def store(tmp_path: Path):
    instance = Store(tmp_path / "rsfeh")
    instance.init()
    yield instance
    instance.close()


@pytest.mark.xfail(
    strict=True,
    reason="Known gap: global SHA-256 dedup returns metadata from another Work scope",
)
def test_same_content_in_different_work_scopes_is_not_cross_linked(store: Store):
    payload = b"same private evidence"
    work_a = store.put(payload, "private-a.bin", work_id="WORK-A")
    work_b = store.put(payload, "private-b.bin", work_id="WORK-B")

    assert work_b["work_id"] == "WORK-B"
    assert work_b["file_id"] != work_a["file_id"]


@pytest.mark.xfail(
    strict=True,
    reason="Known gap: get_bytes returns altered blob bytes without verifying SHA-256",
)
def test_get_bytes_rejects_tampered_blob(store: Store):
    payload = b"immutable evidence"
    meta = store.put(payload, "evidence.bin")
    blob = store.blobs / meta["sha256"]
    blob.write_bytes(b"tampered evidence")

    with pytest.raises(RSFEHError) as error:
        store.get_bytes(meta["file_id"])

    assert error.value.code == "INTEGRITY_FAIL"
