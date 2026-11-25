import tempfile
import unittest
from pathlib import Path
from tools.room_drive_guard import find_desktop_ini, make_report

class DesktopIniDetectionTests(unittest.TestCase):
    def test_root_and_nested_case_insensitive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "desktop.ini").write_text("root", encoding="utf-8")
            nested = root / "docs" / "nested"
            nested.mkdir(parents=True)
            (nested / "DESKTOP.INI").write_text("nested", encoding="utf-8")
            self.assertEqual(find_desktop_ini(root), ["desktop.ini", "docs/nested/DESKTOP.INI"])

    def test_skips_git_internal_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".git").mkdir()
            (root / ".git" / "desktop.ini").write_text("internal", encoding="utf-8")
            self.assertEqual(find_desktop_ini(root), [])

    def test_does_not_follow_symlink_directories(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root, external = Path(temp), Path(outside)
            (external / "desktop.ini").write_text("outside", encoding="utf-8")
            try:
                (root / "linked").symlink_to(external, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("directory symlinks unavailable")
            self.assertEqual(find_desktop_ini(root), [])

    def test_report_never_changes_detected_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "desktop.ini"
            target.write_text("metadata", encoding="utf-8")
            report = make_report(root)
            self.assertEqual(report["desktop_ini_count"], 1)
            self.assertEqual(report["findings"][0]["action_taken"], "none")
            self.assertTrue(target.exists())

if __name__ == "__main__":
    unittest.main()
