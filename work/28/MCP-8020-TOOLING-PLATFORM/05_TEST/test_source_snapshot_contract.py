"""Regression tests for source snapshot contract, including KAST findings."""
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))
from source_snapshot_contract import HARD_MAX_FILES, SnapshotLimits, SnapshotValidationError, canonical_manifest_bytes, sha256_bytes, validate_manifest, validate_relative_path
ALLOW = ("room_hop_mcp", "core", "integration", "tests", "pyproject.toml", "requirements.txt")
GOOD = {"schema_version": "0.1.1", "collector_version": "pc-readonly-collector/0.3.0", "provenance_status": "UNAUTHENTICATED_LOCAL_OBSERVATION", "created_at_utc": "2026-10-15T00:00:00Z", "repo_root": "D:/ROOM-HOP-CLEAN/room-meeting-ai", "branch": "work-branch", "head": "d7c90d9d31062d389810808e43dfdd19d7711b75", "dirty": False, "status_short": [], "included_files": [{"path": "room_hop_mcp/mcp_http_main.py", "size_bytes": 100, "sha256": "a" * 64}, {"path": "core/auth.py", "size_bytes": 50, "sha256": "b" * 64}], "excluded_paths": [".env", ".git/"], "file_count": 2, "total_bytes": 150, "archive_sha256": "c" * 64}
class SourceSnapshotContractTests(unittest.TestCase):
    def test_valid_manifest(self): self.assertEqual(validate_manifest(GOOD, allowlist=ALLOW)["file_count"], 2)
    def test_missing_unknown_and_authenticated_provenance_rejected(self):
        bad = dict(GOOD); bad.pop("head")
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
        bad = dict(GOOD, extra=True)
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
        bad = dict(GOOD, provenance_status="AUTHENTICATED")
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
    def test_case_fold_path_collision_rejected_kast01(self):
        bad = dict(GOOD, included_files=[dict(GOOD["included_files"][0], path="core/A.py"), dict(GOOD["included_files"][1], path="core/a.py")], file_count=2)
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
    def test_path_controls_and_secrets_rejected(self):
        for path in ("secrets/token.txt", "../room_hop_mcp/x.py", "/etc/passwd", "C:/repo/x.py", "core/../secrets.txt", "room_hop_mcp/.env", "core/id_rsa", "core/private.pem", "core/runtime.db", "core/.git/config"):
            with self.subTest(path=path), self.assertRaises(SnapshotValidationError): validate_relative_path(path, allowlist=ALLOW)
    def test_duplicate_bad_hash_boolean_and_dirty_mismatch_rejected(self):
        bad = dict(GOOD, included_files=GOOD["included_files"] * 2, file_count=4, total_bytes=300)
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
        bad = dict(GOOD, included_files=[dict(GOOD["included_files"][0], sha256="bad")], file_count=1, total_bytes=100)
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
        bad = dict(GOOD, included_files=[dict(GOOD["included_files"][0], size_bytes=True)], file_count=1, total_bytes=True)
        with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
        with self.assertRaises(SnapshotValidationError): validate_manifest(dict(GOOD, dirty=True, status_short=[]), allowlist=ALLOW)
    def test_limits_empty_and_metadata_bounds_rejected(self):
        for kwargs in ({"max_files": True}, {"max_files": 0}, {"max_files": -1}, {"max_files": HARD_MAX_FILES + 1}, {"max_file_bytes": 8 * 1024 * 1024 + 1}, {"max_total_bytes": 128 * 1024 * 1024 + 1}, {"max_path_chars": 513}):
            with self.subTest(kwargs=kwargs), self.assertRaises(SnapshotValidationError): SnapshotLimits(**kwargs)
        for bad in (dict(GOOD, included_files=[], file_count=0, total_bytes=0), dict(GOOD, excluded_paths=["bad\nentry"]), dict(GOOD, excluded_paths=["x" * 1025])):
            with self.assertRaises(SnapshotValidationError): validate_manifest(bad, allowlist=ALLOW)
    def test_canonical_json_and_sha256(self):
        self.assertEqual(canonical_manifest_bytes({"b": 2, "a": 1}), canonical_manifest_bytes({"a": 1, "b": 2}))
        self.assertEqual(sha256_bytes(b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
if __name__ == "__main__": unittest.main()
