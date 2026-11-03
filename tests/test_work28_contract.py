import hashlib
import os
from pathlib import Path

import pytest

from execution_host.work28_contract import (
    Work28ContractError,
    create_source_snapshot,
    validate_request,
)


def request_for(source: bytes, **overrides):
    payload = {
        "work_id": "W28",
        "entry_path": "scripts/check.py",
        "operation": "RUN_SCRIPT",
        "expected_source_sha256": hashlib.sha256(source).hexdigest(),
        "timeout_seconds": 30,
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize("bad_path", [
    "../outside.py", "/absolute.py", r"C:\\temp\\x.py",
    "a//b.py", "a/./b.py", "a/../b.py", "script.py.",
])
def test_request_rejects_unsafe_paths(bad_path):
    with pytest.raises(Work28ContractError):
        validate_request(request_for(b"x", entry_path=bad_path))


@pytest.mark.parametrize("extra", [
    {"command": ["python", "-c", "print(1)"]},
    {"authorized": True},
    {"principal": "admin"},
    {"cwd": "/tmp"},
    {"shell": True},
])
def test_request_rejects_caller_command_and_authority_fields(extra):
    with pytest.raises(Work28ContractError):
        validate_request({**request_for(b"x"), **extra})


@pytest.mark.parametrize("timeout", [True, 0, -1, 301, 1.5, "30"])
def test_request_rejects_invalid_timeout(timeout):
    with pytest.raises(Work28ContractError):
        validate_request(request_for(b"x", timeout_seconds=timeout))


def test_request_rejects_invalid_operation_and_hash():
    with pytest.raises(Work28ContractError):
        validate_request(request_for(b"x", operation="RUN_COMMAND"))
    with pytest.raises(Work28ContractError):
        validate_request(request_for(b"x", expected_source_sha256="A" * 64))


def test_snapshot_binds_work_hash_and_exact_bytes(tmp_path):
    root = tmp_path / "work"
    source = root / "scripts" / "check.py"
    source.parent.mkdir(parents=True)
    data = b"print('immutable snapshot candidate')\n"
    source.write_bytes(data)
    request = validate_request(request_for(data))
    snapshot = create_source_snapshot(
        request=request,
        authoritative_work_id="W28",
        work_root=root,
        snapshot_root=tmp_path / "snapshots",
    )
    assert snapshot.source_sha256 == hashlib.sha256(data).hexdigest()
    assert snapshot.snapshot_path.read_bytes() == data
    assert snapshot.snapshot_path.stat().st_mode & 0o222 == 0
    assert snapshot.snapshot_ref.startswith("sha256:" + snapshot.source_sha256 + ":")


def test_snapshot_refuses_wrong_authoritative_work(tmp_path):
    root = tmp_path / "work"
    (root / "scripts").mkdir(parents=True)
    source = root / "scripts" / "check.py"
    source.write_bytes(b"x")
    request = validate_request(request_for(b"x"))
    with pytest.raises(PermissionError, match="work_binding_mismatch"):
        create_source_snapshot(
            request=request, authoritative_work_id="OTHER",
            work_root=root, snapshot_root=tmp_path / "snapshots",
        )


def test_snapshot_refuses_hash_mismatch(tmp_path):
    root = tmp_path / "work"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "check.py").write_bytes(b"changed")
    request = validate_request(request_for(b"expected"))
    with pytest.raises(Work28ContractError, match="source_hash_mismatch"):
        create_source_snapshot(
            request=request, authoritative_work_id="W28",
            work_root=root, snapshot_root=tmp_path / "snapshots",
        )


def test_snapshot_refuses_symlink_escape(tmp_path):
    root = tmp_path / "work"
    root.mkdir()
    outside = tmp_path / "outside.py"
    outside.write_bytes(b"x")
    link = root / "scripts.py"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable on this runner")
    request = validate_request(request_for(b"x", entry_path="scripts.py"))
    with pytest.raises(Work28ContractError, match="symlink_component_rejected"):
        create_source_snapshot(
            request=request, authoritative_work_id="W28",
            work_root=root, snapshot_root=tmp_path / "snapshots",
        )


def test_snapshot_refuses_work_root_escape_after_resolution(tmp_path):
    root = tmp_path / "work"
    root.mkdir()
    outside = tmp_path / "outside.py"
    outside.write_bytes(b"x")
    link = root / "escape.py"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable on this runner")
    request = validate_request(request_for(b"x", entry_path="escape.py"))
    with pytest.raises(Work28ContractError, match="symlink_component_rejected"):
        create_source_snapshot(
            request=request, authoritative_work_id="W28",
            work_root=root, snapshot_root=tmp_path / "snapshots",
        )
