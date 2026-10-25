"""Regression tests for the staged Work 28 -> canonical W13 boundary."""
from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from execution_host.work28_contract import (
    Work28ContractError,
    create_source_snapshot,
    validate_request,
)


def payload(source: bytes, **overrides):
    value = {
        "work_id": "W28",
        "entry_path": "scripts/check.py",
        "operation": "RUN_SCRIPT",
        "expected_source_sha256": hashlib.sha256(source).hexdigest(),
        "timeout_seconds": 30,
    }
    value.update(overrides)
    return value


class Work13ContractBoundaryTests(unittest.TestCase):
    def test_valid_request_normalizes_contract(self):
        request = validate_request(payload(b"print(1)"))
        self.assertEqual(request.work_id, "W28")
        self.assertEqual(request.entry_path, "scripts/check.py")
        self.assertEqual(request.operation, "RUN_SCRIPT")

    def test_arbitrary_command_and_authority_fields_rejected(self):
        for field in (
            {"command": ["python", "-c", "print(1)"]},
            {"authorized": True},
            {"principal": "admin"},
            {"cwd": "/tmp"},
            {"shell": True},
        ):
            with self.subTest(field=field), self.assertRaises(Work28ContractError):
                validate_request({**payload(b"x"), **field})

    def test_unsafe_paths_rejected(self):
        for entry in ("../outside.py", "/absolute.py", r"C:\\temp\\x.py",
                      "a//b.py", "a/./b.py", "a/../b.py", "script.py."):
            with self.subTest(entry=entry), self.assertRaises(Work28ContractError):
                validate_request(payload(b"x", entry_path=entry))

    def test_bad_operation_hash_and_timeout_rejected(self):
        cases = (
            {"operation": "RUN_COMMAND"},
            {"expected_source_sha256": "A" * 64},
            {"timeout_seconds": True},
            {"timeout_seconds": 0},
            {"timeout_seconds": 301},
            {"timeout_seconds": 1.5},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises(Work28ContractError):
                validate_request(payload(b"x", **overrides))

    def test_snapshot_binds_exact_bytes_and_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "work"
            source = root / "scripts" / "check.py"
            source.parent.mkdir(parents=True)
            data = b"print('snapshot')\n"
            source.write_bytes(data)
            request = validate_request(payload(data))
            snapshot = create_source_snapshot(
                request=request,
                authoritative_work_id="W28",
                work_root=root,
                snapshot_root=base / "snapshots",
            )
            self.assertEqual(snapshot.snapshot_path.read_bytes(), data)
            self.assertEqual(snapshot.source_sha256, hashlib.sha256(data).hexdigest())
            self.assertEqual(snapshot.snapshot_path.stat().st_mode & 0o222, 0)

    def test_snapshot_rejects_authoritative_work_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "work"
            (root / "scripts").mkdir(parents=True)
            (root / "scripts" / "check.py").write_bytes(b"x")
            request = validate_request(payload(b"x"))
            with self.assertRaises(PermissionError):
                create_source_snapshot(
                    request=request, authoritative_work_id="OTHER",
                    work_root=root, snapshot_root=base / "snapshots",
                )

    def test_snapshot_rejects_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "work"
            (root / "scripts").mkdir(parents=True)
            (root / "scripts" / "check.py").write_bytes(b"changed")
            request = validate_request(payload(b"expected"))
            with self.assertRaisesRegex(Work28ContractError, "source_hash_mismatch"):
                create_source_snapshot(
                    request=request, authoritative_work_id="W28",
                    work_root=root, snapshot_root=base / "snapshots",
                )

    def test_snapshot_rejects_symlink_component(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "work"
            root.mkdir()
            outside = base / "outside.py"
            outside.write_bytes(b"x")
            link = root / "check.py"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable on this runner")
            request = validate_request(payload(b"x", entry_path="check.py"))
            with self.assertRaisesRegex(Work28ContractError, "symlink_component_rejected"):
                create_source_snapshot(
                    request=request, authoritative_work_id="W28",
                    work_root=root, snapshot_root=base / "snapshots",
                )


if __name__ == "__main__":
    unittest.main()
