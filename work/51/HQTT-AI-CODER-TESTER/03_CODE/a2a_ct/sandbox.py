"""Execution Sandbox — runs artifact + acceptance program in an isolated
subprocess with a hard timeout (charter §3.5).

Isolation in this slice (D-04 in DECISION_REGISTER):
- fresh temp dir per run, artifact written inside it
- `python -I` isolated mode: ignores PYTHONPATH, user site-packages and env vars
- hard wall-clock timeout via subprocess timeout

Documented limitations (production hardening deferred, needs approval):
- no container/namespace/seccomp isolation
- no CPU/memory cgroup limits
- no network egress blocking (untrusted code could attempt network calls)
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile


class Sandbox:
    def __init__(self, python_bin: str | None = None):
        self.python_bin = python_bin or sys.executable

    def run(self, artifact_code: str, program: str, timeout_s: float = 10.0) -> dict:
        """Run `program` appended to `artifact_code` in an isolated subprocess.

        Returns {"ok": bool, "returncode": int|None, "stdout": str,
                 "stderr": str, "timeout": bool}
        """
        with tempfile.TemporaryDirectory(prefix="a2a_ct_sandbox_") as td:
            runner_path = os.path.join(td, "runner.py")
            runner = (
                artifact_code.rstrip()
                + "\n\n# ---- acceptance program (appended by tester sandbox) ----\n"
                + program.rstrip()
                + "\n"
            )
            with open(runner_path, "w", encoding="utf-8") as fh:
                fh.write(runner)
            try:
                proc = subprocess.run(
                    [self.python_bin, "-I", runner_path],
                    capture_output=True,
                    text=True,
                    timeout=timeout_s,
                    cwd=td,
                )
            except subprocess.TimeoutExpired:
                return {
                    "ok": False,
                    "returncode": None,
                    "stdout": "",
                    "stderr": f"sandbox timeout after {timeout_s}s",
                    "timeout": True,
                }
            return {
                "ok": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": proc.stdout[-2000:],
                "stderr": proc.stderr[-2000:],
                "timeout": False,
            }
