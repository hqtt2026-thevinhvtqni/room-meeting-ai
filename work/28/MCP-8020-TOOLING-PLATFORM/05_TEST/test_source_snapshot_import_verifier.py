"""Pure in-memory archive verification tests for KAST-01..04."""
import hashlib, io, json, stat, sys, unittest, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))
from source_snapshot_contract import HARD_MAX_MANIFEST_BYTES, canonical_manifest_bytes
from source_snapshot_import_verifier import ImportVerificationError, verify_archive_in_memory
ALLOW = ("room_hop_mcp", "core", "integration", "tests"); WORK = "28"
def make_case():
    entries = [("core/a.py", b"print('a')\n"), ("room_hop_mcp/b.py", b"print('b')\n")]; buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path, data in entries:
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.create_system = 3; info.external_attr = (0o100644 & 0xFFFF) << 16; zf.writestr(info, data)
    archive = buffer.getvalue(); manifest = {"schema_version": "0.1.1", "collector_version": "pc-readonly-collector/0.3.0", "provenance_status": "UNAUTHENTICATED_LOCAL_OBSERVATION", "created_at_utc": "2026-10-15T00:00:00Z", "repo_root": "untrusted-local-observation", "branch": "branch", "head": "a" * 40, "dirty": False, "status_short": [], "included_files": [{"path": p, "size_bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()} for p, d in entries], "excluded_paths": [".env"], "file_count": 2, "total_bytes": sum(len(d) for _, d in entries), "archive_sha256": hashlib.sha256(archive).hexdigest()}
    return archive, canonical_manifest_bytes(manifest)
class ImportVerifierTests(unittest.TestCase):
    def test_valid_archive_is_only_verified_in_memory(self):
        archive, manifest = make_case(); result = verify_archive_in_memory(archive, manifest, allowlist=ALLOW, destination_work_id=WORK); self.assertEqual(result["status"], "VERIFIED_IN_MEMORY_NOT_IMPORTED"); self.assertFalse(result["imported"])
    def test_manifest_archive_hash_mismatch_rejected(self):
        archive, manifest = make_case(); data = json.loads(manifest); data["archive_sha256"] = "0" * 64
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive, canonical_manifest_bytes(data), allowlist=ALLOW, destination_work_id=WORK)
    def test_manifest_size_checked_before_parse_kast03(self):
        archive, _ = make_case(); oversized = b"{" + b" " * HARD_MAX_MANIFEST_BYTES
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive, oversized, allowlist=ALLOW, destination_work_id=WORK)
    def test_member_hash_mismatch_rejected(self):
        archive, manifest = make_case(); data = json.loads(manifest); data["included_files"][0]["sha256"] = "0" * 64
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive, canonical_manifest_bytes(data), allowlist=ALLOW, destination_work_id=WORK)
    def test_truncated_archive_rejected(self):
        archive, manifest = make_case()
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive[:-7], manifest, allowlist=ALLOW, destination_work_id=WORK)
    def test_zip_symlink_external_attribute_rejected_kast02(self):
        archive, manifest = make_case(); buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(archive), "r") as source, zipfile.ZipFile(buffer, "w") as target:
            for index, old in enumerate(source.infolist()):
                info = zipfile.ZipInfo(old.filename); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = ((stat.S_IFLNK | 0o777) if index == 0 else (0o100644)) << 16; target.writestr(info, source.read(old.filename))
        data = json.loads(manifest); data["archive_sha256"] = hashlib.sha256(buffer.getvalue()).hexdigest()
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(buffer.getvalue(), canonical_manifest_bytes(data), allowlist=ALLOW, destination_work_id=WORK)
    def test_zip_case_fold_collision_rejected_kast01(self):
        archive, manifest = make_case(); data = json.loads(manifest); data["included_files"][1]["path"] = "CORE/B.PY"
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive, canonical_manifest_bytes(data), allowlist=ALLOW, destination_work_id=WORK)
    def test_unexpected_entry_rejected(self):
        archive, manifest = make_case(); buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(archive), "r") as source, zipfile.ZipFile(buffer, "w") as target:
            for info in source.infolist(): target.writestr(info, source.read(info.filename))
            target.writestr("core/extra.py", b"extra")
        data = json.loads(manifest); data["archive_sha256"] = hashlib.sha256(buffer.getvalue()).hexdigest()
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(buffer.getvalue(), canonical_manifest_bytes(data), allowlist=ALLOW, destination_work_id=WORK)
    def test_receipt_work_mismatch_rejected(self):
        archive, manifest = make_case(); receipt = {"receipt_version": "0.1.0", "source_identity": "pc", "approved_channel": "pending", "archive_sha256": hashlib.sha256(archive).hexdigest(), "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "destination_work_id": "99", "transferred_at_utc": "2026-10-15T00:00:00Z", "nonce": "nonce-123456789012", "issuer": "pending", "issuer_signature": "pending", "verifier_result": "TRUSTED_RECEIPT_PENDING_EXTERNAL_AUTH"}
        with self.assertRaises(ImportVerificationError): verify_archive_in_memory(archive, manifest, allowlist=ALLOW, destination_work_id=WORK, receipt=receipt)
    def test_untrusted_receipt_never_imports(self):
        archive, manifest = make_case(); receipt = {"receipt_version": "0.1.0", "source_identity": "pc", "approved_channel": "pending", "archive_sha256": hashlib.sha256(archive).hexdigest(), "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "destination_work_id": WORK, "transferred_at_utc": "2026-10-15T00:00:00Z", "nonce": "nonce-123456789012", "issuer": "pending", "issuer_signature": "pending", "verifier_result": "TRUSTED_RECEIPT_PENDING_EXTERNAL_AUTH"}
        result = verify_archive_in_memory(archive, manifest, allowlist=ALLOW, destination_work_id=WORK, receipt=receipt); self.assertFalse(result["imported"]); self.assertEqual(result["receipt_authentication"], "NOT_PERFORMED_BY_PURE_VERIFIER")
if __name__ == "__main__": unittest.main()
