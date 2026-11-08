"""Tests for ci_tools.check_workflow_mirror (stdlib unittest)."""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

from ci_tools import check_workflow_mirror as m

BASE = "name: CI\non: push\njobs:\n  a:\n    runs-on: ubuntu-latest\n"


class TestMirror(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.active = self.root / "active.yml"
        self.mirror = self.root / "mirror.yml"
        self._saved = {
            key: os.environ.pop(key, None)
            for key in ("CHECK_STRICT", "REPO_ROOT", "W32_DIR")
        }
        os.environ["REPO_ROOT"] = str(self.root)

    def tearDown(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.tmp.cleanup()

    def _run(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = m.main(["active.yml", "mirror.yml"])
        return code, output.getvalue()

    def test_identical_files_in_sync(self):
        self.active.write_text(BASE)
        self.mirror.write_text(BASE)
        code, output = self._run()
        self.assertEqual(code, 0)
        self.assertIn("IN_SYNC", output)

    def test_crlf_and_trailing_newline_are_ignored(self):
        self.active.write_bytes(BASE.encode())
        self.mirror.write_bytes(BASE.replace("\n", "\r\n").rstrip("\r\n").encode())
        code, output = self._run()
        self.assertEqual(code, 0)
        self.assertIn("IN_SYNC", output)

    def test_drift_reported_but_not_failing_by_default(self):
        self.active.write_text(BASE + "    # f4\n")
        self.mirror.write_text(BASE)
        code, output = self._run()
        self.assertEqual(code, 0)
        self.assertIn("DRIFT", output)
        self.assertIn("+++ mirror", output)

    def test_drift_fails_in_strict_mode(self):
        self.active.write_text(BASE + "    # f4\n")
        self.mirror.write_text(BASE)
        os.environ["CHECK_STRICT"] = "1"
        code, _ = self._run()
        self.assertEqual(code, 1)

    def test_pin_change_is_detected(self):
        self.active.write_text(BASE + "    uses: x/y@aaaa # v7\n")
        self.mirror.write_text(BASE + "    uses: x/y@bbbb # v5\n")
        self.assertTrue(m.diff_workflows(self.active, self.mirror))

    def test_missing_file_exits_2(self):
        self.active.write_text(BASE)
        code, output = self._run()
        self.assertEqual(code, 2)
        self.assertIn("MISSING", output)


if __name__ == "__main__":
    unittest.main()
