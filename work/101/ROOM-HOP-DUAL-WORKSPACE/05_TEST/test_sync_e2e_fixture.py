"""Disposable filesystem-fixture E2E tests for Work 101.

These tests exercise policy-to-provider-shaped read/write/read-back behavior only
inside TemporaryDirectory. They do NOT claim Sandbox, GitHub, Core, or MCP E2E.
The production integration remains blocked until provider contracts and authorization
routes are verified.
"""
from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
import sys
sys.path.insert(0, str(CODE_DIR))

from sync_policy import (
    ApprovalBinding,
    ChangeState,
    PolicyError,
    Snapshot,
    bind_approval,
    build_sync_plan,
    canonical_relative_path,
    sha256_text,
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FixtureProvider:
    """Minimal CAS-like provider constrained to an isolated temporary root."""

    def __init__(self, root: Path, allowed_roots: tuple[str, ...]):
        self.root = root.resolve()
        self.allowed_roots = allowed_roots
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, relative: str) -> Path:
        canonical = canonical_relative_path(relative)
        if not any(canonical == r.rstrip("/") or canonical.startswith(r.rstrip("/") + "/")
                   for r in self.allowed_roots):
            raise PolicyError("PATH_OUTSIDE_ALLOWLIST")
        candidate = self.root.joinpath(*canonical.split("/"))
        # Reject symlink components, including a symlink that resolves inside root.
        cursor = self.root
        for part in canonical.split("/"):
            cursor = cursor / part
            if cursor.is_symlink():
                raise PolicyError("SYMLINK_PATH_BLOCKED")
        resolved = candidate.resolve(strict=False)
        if resolved != self.root and self.root not in resolved.parents:
            raise PolicyError("PATH_OUTSIDE_ROOT")
        return candidate

    def read(self, relative: str) -> bytes:
        path = self._path(relative)
        return path.read_bytes()

    def snapshot(self, revision: str, base_revision: str) -> Snapshot:
        files: dict[str, str] = {}
        for root_name in self.allowed_roots:
            root = self.root / root_name.rstrip("/")
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if path.is_symlink():
                    raise PolicyError("SYMLINK_PATH_BLOCKED")
                if not path.is_file():
                    continue
                relative = path.relative_to(self.root).as_posix()
                canonical_relative_path(relative)
                files[relative] = digest_bytes(path.read_bytes())
        return Snapshot(revision, files, base_revision)

    def write_cas(self, relative: str, content: bytes, expected_revision: str,
                  current_revision: str) -> str:
        if current_revision != expected_revision:
            raise PolicyError("STALE_DESTINATION_REVISION")
        path = self._path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Temporary file + atomic replace; this fixture never touches a real repo.
        fd, temp_name = tempfile.mkstemp(prefix=".work101-", dir=str(path.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        return digest_bytes(path.read_bytes())


class Work101FixtureE2ETests(unittest.TestCase):
    ROOTS = ("04_CODE/", "05_TEST/")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="work101-e2e-")
        self.addCleanup(self.temp.cleanup)
        self.base_root = Path(self.temp.name) / "base"
        self.source_root = Path(self.temp.name) / "source"
        self.destination_root = Path(self.temp.name) / "destination"
        for root in (self.base_root, self.source_root, self.destination_root):
            root.mkdir()
        self.base = FixtureProvider(self.base_root, self.ROOTS)
        self.source = FixtureProvider(self.source_root, self.ROOTS)
        self.destination = FixtureProvider(self.destination_root, self.ROOTS)
        for provider in (self.base, self.source, self.destination):
            path = provider._path("04_CODE/sample.txt")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("baseline", encoding="utf-8")

    def _snapshot(self, provider, revision, base_revision="base-r1"):
        return provider.snapshot(revision, base_revision)

    def _plan(self, operation_id="fixture-op-1"):
        return build_sync_plan(
            operation_id=operation_id,
            work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="base-r1",
            base=self._snapshot(self.base, "base-r1", "base-r1"),
            source=self._snapshot(self.source, "source-r2"),
            destination=self._snapshot(self.destination, "destination-r2"),
            permitted_path_roots=self.ROOTS,
        )

    def test_source_only_change_plan_then_digest_readback(self):
        self.source._path("04_CODE/sample.txt").write_text("source edit", encoding="utf-8")
        plan = self._plan()
        self.assertEqual(plan.state, ChangeState.SOURCE_ONLY)
        self.assertEqual(plan.source_to_destination, ("04_CODE/sample.txt",))
        self.assertEqual(plan.mode, "DRY_RUN")
        # Planner is read-only: destination remains unchanged until a fixture write.
        self.assertEqual(self.destination.read("04_CODE/sample.txt"), b"baseline")
        source_bytes = self.source.read("04_CODE/sample.txt")
        expected = digest_bytes(source_bytes)
        observed = self.destination.write_cas(
            "04_CODE/sample.txt", source_bytes, "destination-r2", "destination-r2"
        )
        self.assertEqual(observed, expected)
        self.assertEqual(digest_bytes(self.destination.read("04_CODE/sample.txt")), expected)

    def test_destination_only_change_is_planned_back_to_source(self):
        self.destination._path("05_TEST").mkdir(parents=True, exist_ok=True)
        self.destination._path("05_TEST/remote.txt").write_text("remote edit", encoding="utf-8")
        plan = self._plan()
        self.assertEqual(plan.state, ChangeState.DESTINATION_ONLY)
        self.assertEqual(plan.destination_to_source, ("05_TEST/remote.txt",))

    def test_divergent_same_path_conflicts_and_never_plans_transfer(self):
        self.source._path("04_CODE/sample.txt").write_text("source edit", encoding="utf-8")
        self.destination._path("04_CODE/sample.txt").write_text("remote edit", encoding="utf-8")
        plan = self._plan()
        self.assertEqual(plan.state, ChangeState.CONFLICT_PENDING)
        self.assertEqual(plan.conflict_paths, ("04_CODE/sample.txt",))
        self.assertEqual(plan.source_to_destination, ())
        self.assertEqual(plan.destination_to_source, ())

    def test_baseline_deletion_is_pending_and_emits_no_transfer(self):
        self.source._path("04_CODE/sample.txt").unlink()
        plan = self._plan()
        self.assertEqual(plan.state, ChangeState.DELETION_PENDING)
        self.assertEqual(plan.source_to_destination, ())
        self.assertEqual(plan.destination_to_source, ())

    def test_exact_approval_binding_rejects_changed_branch_or_digest(self):
        approved = ApprovalBinding("op-1", "a" * 64,
                                   "work/101-room-hop-dual-workspace", "base-r1")
        bind_approval(approved, approved)
        changed = ApprovalBinding("op-1", "b" * 64,
                                  "work/101-room-hop-dual-workspace", "base-r1")
        with self.assertRaises(PolicyError):
            bind_approval(approved, changed)

    def test_stale_destination_revision_blocks_fixture_write(self):
        with self.assertRaises(PolicyError):
            self.destination.write_cas(
                "04_CODE/sample.txt", b"unapproved overwrite",
                "destination-r2", "destination-r3"
            )
        self.assertEqual(self.destination.read("04_CODE/sample.txt"), b"baseline")

    def test_path_escape_and_secret_are_rejected(self):
        for path in ("../outside.txt", "C:/outside.txt", ".env", "data/app_workspace.db"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                self.destination._path(path)

    def test_symlink_escape_is_rejected_when_platform_supports_symlinks(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        link = self.destination_root / "04_CODE" / "escape"
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable for this runner identity/platform")
        with self.assertRaises(PolicyError):
            self.destination._path("04_CODE/escape/payload.txt")


if __name__ == "__main__":
    unittest.main()
