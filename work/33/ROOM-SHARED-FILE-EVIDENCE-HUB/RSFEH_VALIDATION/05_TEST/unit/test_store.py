"""Unit tests for RSFEH Store."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

# Allow import from src
SRC = Path(__file__).resolve().parents[2] / "04_CODE" / "src"
sys.path.insert(0, str(SRC))

from rsfeh.store import RSFEHError, Store  # noqa: E402


@pytest.fixture
def store(tmp_path: Path) -> Store:
    s = Store(tmp_path / "rsfeh")
    s.init()
    yield s
    s.close()


def test_init_creates_layout(tmp_path: Path):
    root = tmp_path / "rsfeh"
    s = Store(root)
    s.init()
    assert (root / "blobs").is_dir()
    assert (root / "meta.db").is_file()
    assert (root / "audit.jsonl").is_file()
    s.close()


def test_put_get_roundtrip(store: Store):
    data = b"hello evidence\x00\xff"
    meta = store.put(data, "hello.bin", agent="tester")
    assert meta["size_bytes"] == len(data)
    assert meta["sha256"] == hashlib.sha256(data).hexdigest()
    got = store.get_bytes(meta["file_id"], agent="tester")
    assert got == data


def test_dedup_same_hash(store: Store):
    data = b"same-bytes"
    m1 = store.put(data, "a.txt", agent="a")
    m2 = store.put(data, "b.txt", agent="b")
    assert m1["file_id"] == m2["file_id"]
    assert m1["sha256"] == m2["sha256"]


def test_verify_ok(store: Store):
    data = b"verify-me"
    meta = store.put(data, "v.bin")
    detail = store.verify(meta["file_id"])
    assert detail["match"] is True


def test_verify_detects_tamper(store: Store):
    data = b"original"
    meta = store.put(data, "t.bin")
    blob = store.blobs / meta["sha256"]
    blob.write_bytes(b"tampered!")
    with pytest.raises(RSFEHError) as ei:
        store.verify(meta["file_id"])
    assert ei.value.code == "INTEGRITY_FAIL"


def test_not_found(store: Store):
    with pytest.raises(RSFEHError) as ei:
        store.get_bytes("00000000-0000-0000-0000-000000000000")
    assert ei.value.code == "NOT_FOUND"


def test_invalid_name(store: Store):
    with pytest.raises(RSFEHError):
        store.put(b"x", "bad\x00name")
    with pytest.raises(RSFEHError):
        store.put(b"x", "")
    with pytest.raises(RSFEHError):
        store.put(b"x", ".")
    with pytest.raises(RSFEHError):
        store.put(b"x", "..")


def test_search_and_list(store: Store):
    store.put(b"one", "alpha.txt", work_id="33", agent="a")
    store.put(b"two", "beta.log", work_id="33", agent="a")
    store.put(b"three", "gamma.txt", work_id="99", agent="a")
    listed = store.list_files(work_id="33")
    assert len(listed) == 2
    found = store.search("alpha")
    assert len(found) == 1
    assert found[0]["original_name"] == "alpha.txt"


def test_link_work(store: Store):
    meta = store.put(b"linkme", "l.txt")
    updated = store.link_work(meta["file_id"], "33", evidence_ref="E2E-001")
    assert updated["work_id"] == "33"
    assert updated["evidence_ref"] == "E2E-001"


def test_soft_delete(store: Store):
    meta = store.put(b"del", "d.txt")
    store.soft_delete(meta["file_id"])
    with pytest.raises(RSFEHError) as ei:
        store.get_bytes(meta["file_id"])
    assert ei.value.code == "NOT_FOUND"


def test_audit_recorded(store: Store):
    store.put(b"aud", "a.txt", agent="auditor")
    events = store.audit_tail(20)
    assert any(e["action"] == "put" and e["agent"] == "auditor" for e in events)
