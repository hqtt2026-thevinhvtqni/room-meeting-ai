"""W12 adapter must propagate CleanupResult fields (never hard-coded {})."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

from execution_host.models import WorkContext, new_execution_id
from execution_host.w12_execution_adapter import W12ExecutionAdapter


def _ctx(tmp: Path, authorized: bool = True) -> WorkContext:
    root = tmp
    (root / "workspace").mkdir(parents=True, exist_ok=True)
    evidence = root / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    return WorkContext(
        work_id="28",
        work_name="t",
        workspace_root=str(root),
        execution_workspace=str(root / "workspace"),
        evidence_root=str(evidence),
        authorized=authorized,
        execution_id=new_execution_id(),
    )


class W12AdapterTests(unittest.TestCase):
    def test_cleanup_not_empty_on_pass(self):
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            result = W12ExecutionAdapter().execute(
                ctx, [sys.executable, "-c", "print(1)"], timeout_seconds=10
            )
            self.assertIn(result["status"], ("PASS", "FAILED"))
            self.assertIsInstance(result["cleanup"], dict)
            self.assertIn("process_reaped", result["cleanup"])
            self.assertNotEqual(result["cleanup"], {})
            self.assertEqual(result["isolation"], "NOT_VERIFIED")

    def test_cleanup_on_timeout(self):
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            result = W12ExecutionAdapter().execute(
                ctx,
                [sys.executable, "-c", "import time; time.sleep(30)"],
                timeout_seconds=0.05,
            )
            self.assertEqual(result["status"], "TIMEOUT")
            self.assertTrue(result["cleanup"].get("process_reaped"))


if __name__ == "__main__":
    unittest.main()
