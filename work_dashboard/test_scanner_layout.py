"""Regression tests for scanner layout detection."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import scanner

class ScannerLayoutTests(unittest.TestCase):
    def test_single_root_ignores_partial_mirror(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "00_ROOT").mkdir()
            (root / "00_ROOT" / "WORK_MANIFEST.md").write_text("Status: ACTIVE", encoding="utf-8")
            for phase in ("01_DISCOVER", "02_DEFINE", "03_ARCHITECT", "06_EVIDENCE"):
                (root / phase).mkdir()
            (root / "00_ROOT" / "BIEN_BAN.md").write_text("Minutes", encoding="utf-8")
            mirror = root / "work" / "32"
            (mirror / "00_ROOT").mkdir(parents=True)
            (mirror / "05_BUILD").mkdir()
            (mirror / "06_EVIDENCE").mkdir()
            with patch.object(scanner, "REPO_ROOT", root), patch.object(scanner, "WORK_ROOT", root / "work"):
                result = scanner.scan_all()
            self.assertEqual(result["discovery_mode"], "single-work-root")
            self.assertEqual(len(result["works"]), 1)
            self.assertEqual(result["works"][0]["path"], ".")
            self.assertEqual(result["works"][0]["records"]["BIEN_BAN"]["path"], "00_ROOT/BIEN_BAN.md")
            self.assertFalse(any(x["name"] == "work" for x in result["works"][0]["folders"]))

    def test_multi_work_ignores_incomplete_mirror(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            work = root / "work" / "SBX-A" / "Work-A"
            (work / "00_ROOT").mkdir(parents=True)
            (work / "00_ROOT" / "WORK_MANIFEST.md").write_text("Status: ACTIVE", encoding="utf-8")
            for phase in ("01_DISCOVER", "02_DEFINE", "03_ARCHITECT", "06_EVIDENCE"):
                (work / phase).mkdir()
            partial = root / "work" / "SBX-A" / "partial-mirror"
            (partial / "00_ROOT").mkdir(parents=True)
            (partial / "00_ROOT" / "WORK_MANIFEST.md").write_text("Status: ACTIVE", encoding="utf-8")
            (partial / "05_BUILD").mkdir()
            (partial / "06_EVIDENCE").mkdir()
            with patch.object(scanner, "REPO_ROOT", root), patch.object(scanner, "WORK_ROOT", root / "work"):
                result = scanner.scan_all()
            self.assertEqual(result["discovery_mode"], "multi-work")
            self.assertEqual(len(result["works"]), 1)
            self.assertEqual(result["works"][0]["work_name"], "Work-A")

if __name__ == "__main__":
    unittest.main()
