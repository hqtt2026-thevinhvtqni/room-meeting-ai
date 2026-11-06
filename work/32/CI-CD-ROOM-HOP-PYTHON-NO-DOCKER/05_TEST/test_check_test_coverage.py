"""Tests for recursive ci_tools.check_test_coverage accounting."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

from ci_tools import check_test_coverage as c


class TestCoverage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "tests").mkdir()
        for n in ("test_a.py", "test_b.py", "test_c.py"):
            (self.root / "tests" / n).write_text("")
        self._saved = {
            k: os.environ.pop(k, None)
            for k in (
                "UNIT_TESTS", "E2E_TESTS", "WINDOWS_LANE_TESTS",
                "EXCLUDED_TESTS", "REPO_ROOT", "CHECK_STRICT",
            )
        }

    def tearDown(self):
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v
            else:
                os.environ.pop(k, None)
        self.tmp.cleanup()

    def test_reports_unlisted_root_file(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py"
        os.environ["E2E_TESTS"] = "tests/test_b.py"
        self.assertEqual(c.find_unaccounted(self.root), ["tests/test_c.py"])

    def test_excluded_counts_as_accounted(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py"
        os.environ["E2E_TESTS"] = "tests/test_b.py"
        os.environ["EXCLUDED_TESTS"] = "tests/test_c.py"
        self.assertEqual(c.find_unaccounted(self.root), [])

    def test_windows_lane_is_accounted_but_reported_separately(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py tests/test_b.py"
        os.environ["WINDOWS_LANE_TESTS"] = "tests/test_c.py"
        self.assertEqual(c.find_unaccounted(self.root), [])
        self.assertEqual(c.find_missing(self.root), [])

    def test_recursive_discovery_finds_eligible_nested_test(self):
        nested = self.root / "tests" / "browser"
        nested.mkdir()
        (nested / "test_nested.py").write_text("")
        os.environ["UNIT_TESTS"] = "tests/test_a.py"
        self.assertEqual(
            c.find_unaccounted(self.root),
            ["tests/browser/test_nested.py", "tests/test_b.py", "tests/test_c.py"],
        )

    def test_pytest_norecursedirs_are_respected(self):
        legacy = self.root / "tests" / "legacy"
        legacy.mkdir()
        (legacy / "test_legacy.py").write_text("")
        (self.root / "pytest.ini").write_text(
            "[pytest]\nnorecursedirs = .* build dist tests/legacy\n"
        )
        os.environ["UNIT_TESTS"] = "tests/test_a.py tests/test_b.py tests/test_c.py"
        self.assertEqual(c.find_unaccounted(self.root), [])

    def test_multiline_folded_value(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py\n tests/test_b.py tests/test_c.py"
        self.assertEqual(c.find_unaccounted(self.root), [])

    def test_missing_whitelisted_file_detected(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py tests/test_typo.py"
        self.assertEqual(c.find_missing(self.root), ["tests/test_typo.py"])

    def test_main_modes(self):
        os.environ["UNIT_TESTS"] = "tests/test_a.py"
        os.environ["REPO_ROOT"] = str(self.root)
        self.assertEqual(c.main(), 0)
        os.environ["CHECK_STRICT"] = "1"
        self.assertEqual(c.main(), 1)
        os.environ.pop("CHECK_STRICT")
        os.environ["UNIT_TESTS"] = "tests/test_a.py tests/nope.py"
        self.assertEqual(c.main(), 1)


if __name__ == "__main__":
    unittest.main()
