"""Follow-up regression tests for Ka's KAST static-review findings.

Pure tests only; no collector main invocation, PC access, transfer or import.
"""
import stat
import sys
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))
import source_snapshot_contract as contract
import source_snapshot_import_verifier as verifier
from pc_readonly_source_collector import append_excluded

class KastFollowupTests(unittest.TestCase):
    def test_manifest_cap_is_shared_by_contract_and_verifier(self):
        self.assertEqual(verifier.HARD_MAX_MANIFEST_BYTES, contract.HARD_MAX_MANIFEST_BYTES)

    def test_dos_normal_member_mode_zero_is_accepted(self):
        info = zipfile.ZipInfo("core/a.py")
        info.create_system = 0
        info.external_attr = 0x20  # DOS archive bit; no Unix mode
        verifier.validate_zip_member_type(info)

    def test_dos_ambiguous_unix_mode_is_rejected(self):
        info = zipfile.ZipInfo("core/a.py")
        info.create_system = 0
        info.external_attr = (0o100644 << 16) | 0x20
        with self.assertRaises(verifier.ImportVerificationError):
            verifier.validate_zip_member_type(info)

    def test_dos_reparse_like_attribute_is_rejected(self):
        info = zipfile.ZipInfo("core/a.py")
        info.create_system = 0
        info.external_attr = 0x400
        with self.assertRaises(verifier.ImportVerificationError):
            verifier.validate_zip_member_type(info)

    def test_unix_special_modes_are_rejected(self):
        for special in (stat.S_IFLNK, stat.S_IFIFO, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFSOCK):
            info = zipfile.ZipInfo("core/a.py")
            info.create_system = 3
            info.external_attr = (special | 0o644) << 16
            with self.subTest(special=special), self.assertRaises(verifier.ImportVerificationError):
                verifier.validate_zip_member_type(info)

    def test_unknown_creator_platform_is_rejected(self):
        info = zipfile.ZipInfo("core/a.py")
        info.create_system = 7
        info.external_attr = (0o100644 << 16)
        with self.assertRaises(verifier.ImportVerificationError):
            verifier.validate_zip_member_type(info)

    def test_excluded_metadata_fails_incrementally_at_count_cap(self):
        values = ["x"] * contract.HARD_MAX_EXCLUDED_ITEMS
        with self.assertRaises(SystemExit):
            append_excluded(values, "one-more/")

    def test_excluded_metadata_fails_incrementally_at_item_length_cap(self):
        with self.assertRaises(SystemExit):
            append_excluded([], "x" * (contract.HARD_MAX_EXCLUDED_ITEM_CHARS + 1))

if __name__ == "__main__":
    unittest.main()
