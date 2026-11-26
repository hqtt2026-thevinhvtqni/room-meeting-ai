"""E2E CLI tests for RSFEH — acceptance A1–A9 core path."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_CODE" / "src"
PYTHON = sys.executable


def run_cli(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    env["RSFEH_ROOT"] = str(root)
    cmd = [PYTHON, "-m", "rsfeh", "--root", str(root), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        check=check,
    )


@pytest.fixture
def rsfeh_root(tmp_path: Path) -> Path:
    r = tmp_path / "data"
    return r


def test_a1_init(rsfeh_root: Path):
    cp = run_cli(rsfeh_root, "init")
    assert cp.returncode == 0
    assert (rsfeh_root / "blobs").is_dir()
    assert (rsfeh_root / "meta.db").is_file()


def test_a2_a3_put_get_meta(rsfeh_root: Path, tmp_path: Path):
    run_cli(rsfeh_root, "init")
    src = tmp_path / "payload.bin"
    payload = b"E2E-payload-" + os.urandom(64)
    src.write_bytes(payload)
    cp = run_cli(
        rsfeh_root,
        "put",
        str(src),
        "--agent",
        "e2e",
        "--work-id",
        "33",
        "--notes",
        "e2e-test",
    )
    assert cp.returncode == 0
    meta = json.loads(cp.stdout)
    assert meta["sha256"] == hashlib.sha256(payload).hexdigest()
    assert meta["size_bytes"] == len(payload)
    assert meta["work_id"] == "33"

    out = tmp_path / "out.bin"
    cp2 = run_cli(rsfeh_root, "get", meta["file_id"], "--out", str(out), "--agent", "e2e")
    assert cp2.returncode == 0
    assert out.read_bytes() == payload

    cp3 = run_cli(rsfeh_root, "meta", meta["file_id"])
    m2 = json.loads(cp3.stdout)
    assert m2["file_id"] == meta["file_id"]
    assert m2["status"] == "active"


def test_a4_verify_tamper(rsfeh_root: Path, tmp_path: Path):
    run_cli(rsfeh_root, "init")
    src = tmp_path / "v.bin"
    src.write_bytes(b"integrity")
    meta = json.loads(run_cli(rsfeh_root, "put", str(src)).stdout)
    assert run_cli(rsfeh_root, "verify", meta["file_id"]).returncode == 0
    blob = rsfeh_root / "blobs" / meta["sha256"]
    blob.write_bytes(b"broken")
    cp = run_cli(rsfeh_root, "verify", meta["file_id"], check=False)
    assert cp.returncode != 0
    assert "INTEGRITY_FAIL" in cp.stderr


def test_a5_bad_id(rsfeh_root: Path):
    run_cli(rsfeh_root, "init")
    cp = run_cli(rsfeh_root, "get", "not-a-uuid", check=False)
    assert cp.returncode != 0
    assert "NOT_FOUND" in cp.stderr or "not found" in cp.stderr.lower()


def test_a6_a7_audit_search_link(rsfeh_root: Path, tmp_path: Path):
    run_cli(rsfeh_root, "init")
    src = tmp_path / "s.txt"
    src.write_bytes(b"searchable-content")
    meta = json.loads(
        run_cli(rsfeh_root, "put", str(src), "--agent", "searcher", "--name", "findme.txt").stdout
    )
    run_cli(rsfeh_root, "link", meta["file_id"], "33", "--evidence-ref", "AC-A7")
    found = json.loads(run_cli(rsfeh_root, "search", "findme").stdout)
    assert any(f["file_id"] == meta["file_id"] for f in found)
    listed = json.loads(run_cli(rsfeh_root, "list", "--work-id", "33").stdout)
    assert any(f["file_id"] == meta["file_id"] for f in listed)
    audit = json.loads(run_cli(rsfeh_root, "audit", "--limit", "30").stdout)
    actions = {e["action"] for e in audit}
    assert "put" in actions
    assert "link" in actions
    assert any(e["agent"] == "searcher" for e in audit)


def test_a8_consistent_after_error(rsfeh_root: Path):
    run_cli(rsfeh_root, "init")
    cp = run_cli(rsfeh_root, "put", "/nonexistent/path/xyz", check=False)
    assert cp.returncode != 0
    assert run_cli(rsfeh_root, "list").returncode == 0
