"""Container-grade sandbox profile (D-04c in DECISION_REGISTER).

Same run(artifact_code, program, timeout_s) contract as sandbox.Sandbox,
but the runner executes inside a locked-down Docker container when Docker
is available:

  --network none                no network interfaces at all
  --memory 512m --cpus 1.0      kernel/cgroup-enforced resource caps
  --pids-limit 64               fork-bomb guard
  --cap-drop ALL                no Linux capabilities
  --security-opt no-new-privileges
  --security-opt seccomp=default  default Docker seccomp profile
  --read-only                   immutable container root filesystem

Env scrub and the 200 KB input caps are inherited from sandbox.Sandbox by
composition. This profile is OPTIONAL: call available() and fall back to
sandbox.Sandbox on hosts without Docker (e.g. developer laptops).

Known limits (documented in DECISION_REGISTER D-04c):
- no custom seccomp whitelist yet; image not pinned by digest yet.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import uuid

from .sandbox import Sandbox, SandboxInputError  # noqa: F401  (SandboxInputError re-exported)


class ContainerSandbox:
    """Docker-backed sandbox with the same run() result shape as Sandbox."""

    def __init__(self, image: str = "python:3.12-slim", python_bin: str = "python"):
        self.image = image
        self.python_bin = python_bin

    # -- availability ---------------------------------------------------------

    def available(self) -> bool:
        if not shutil.which("docker"):
            return False
        try:
            info = subprocess.run(["docker", "info"], capture_output=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return False
        if info.returncode != 0:
            return False
        if not self._image_present():
            # Pre-pull once so the first run() does not eat its own timeout.
            try:
                subprocess.run(["docker", "pull", self.image],
                               capture_output=True, timeout=600)
            except (OSError, subprocess.TimeoutExpired):
                return False
        return self._image_present()

    def _image_present(self) -> bool:
        try:
            q = subprocess.run(["docker", "images", "-q", self.image],
                               capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return False
        return q.returncode == 0 and bool(q.stdout.strip())

    # -- run -------------------------------------------------------------------

    def run(self, artifact_code: str, program: str, timeout_s: float = 60.0) -> dict:
        Sandbox._check_size("artifact_code", artifact_code)
        Sandbox._check_size("program", program)
        name = "a2a_ct_" + uuid.uuid4().hex[:12]
        with tempfile.TemporaryDirectory(prefix="a2a_ct_container_") as td:
            runner_path = os.path.join(td, "runner.py")
            runner = (
                artifact_code.rstrip()
                + "\n\n# ---- acceptance program (appended by tester sandbox) ----\n"
                + program.rstrip()
                + "\n"
            )
            with open(runner_path, "w", encoding="utf-8") as fh:
                fh.write(runner)
            cmd = [
                "docker", "run", "--rm", "--name", name,
                "--network", "none",
                "--memory", "512m", "--cpus", "1.0",
                "--pids-limit", "64",
                "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges",
                "--security-opt", "seccomp=default",
                "--read-only",
                "-e", "PYTHONDONTWRITEBYTECODE=1",
                "-v", td + ":/work:ro", "-w", "/work",
                self.image, self.python_bin, "-I", "runner.py",
            ]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=timeout_s)
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", name],
                               capture_output=True, timeout=30)
                return {
                    "ok": False, "returncode": None, "stdout": "",
                    "stderr": f"container sandbox timeout after {timeout_s}s",
                    "timeout": True, "network_isolated": True, "engine": "docker",
                }
            except FileNotFoundError:
                return {
                    "ok": False, "returncode": None, "stdout": "",
                    "stderr": "docker not available",
                    "timeout": False, "network_isolated": False, "engine": "docker",
                }
            # Best-effort cleanup in case --rm did not fire (killed client).
            subprocess.run(["docker", "rm", "-f", name],
                           capture_output=True, timeout=30)
            return {
                "ok": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": proc.stdout[-2000:],
                "stderr": proc.stderr[-2000:],
                "timeout": False,
                "network_isolated": True,
                "engine": "docker",
            }
