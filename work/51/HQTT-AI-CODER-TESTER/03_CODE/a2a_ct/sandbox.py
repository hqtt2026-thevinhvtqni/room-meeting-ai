"""Execution Sandbox — hardened v1.2 (D-04 in DECISION_REGISTER).

Layers in this slice:
- fresh temp dir per run, artifact written inside it
- `python -I` isolated mode: ignores PYTHONPATH, user site-packages, env vars
- **environment scrubbing**: child gets a minimal env only — parent secrets
  (API keys etc.) are NOT inherited
- **resource limits (POSIX)**: RLIMIT_CPU, RLIMIT_AS (memory), RLIMIT_FSIZE,
  RLIMIT_NPROC applied via preexec_fn
- **network isolation (best effort)**: on Linux with `unshare -n` available,
  the runner is executed in a network namespace with no interfaces; result
  field `network_isolated` reports whether it applied
- hard wall-clock timeout via subprocess timeout
- input size caps (artifact/program must fit MAX_INPUT_BYTES)

Documented remaining limitations (deferred, need approval — D-04):
- no container/seccomp; unshare -n requires privileges on some systems
- no cgroup-based CPU/memory accounting beyond rlimits
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import tempfile

MAX_INPUT_BYTES = 200_000        # 200 KB cap per artifact/program
RLIMIT_CPU_SECONDS = 10
RLIMIT_AS_BYTES = 1 * 1024 * 1024 * 1024   # 1 GB
RLIMIT_FSIZE_BYTES = 4 * 1024 * 1024       # 4 MB writes cap
RLIMIT_NPROC = 64


class SandboxInputError(Exception):
    """Raised when artifact/program input exceeds the sandbox caps."""


def _posix_limits():  # pragma: no cover - executed in child process
    import resource
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (RLIMIT_CPU_SECONDS, RLIMIT_CPU_SECONDS))
        resource.setrlimit(resource.RLIMIT_AS, (RLIMIT_AS_BYTES, RLIMIT_AS_BYTES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (RLIMIT_FSIZE_BYTES, RLIMIT_FSIZE_BYTES))
        resource.setrlimit(resource.RLIMIT_NPROC, (RLIMIT_NPROC, RLIMIT_NPROC))
    except (ValueError, OSError, AttributeError):
        # Best effort: a limit the platform refuses is skipped, not fatal.
        pass


class Sandbox:
    def __init__(self, python_bin: str | None = None,
                 network_isolation: str = "auto"):
        """network_isolation: "auto" (use unshare -n when available),
        "off" (never — for sandboxes that already run inside a container)."""
        self.python_bin = python_bin or sys.executable
        self.network_isolation = network_isolation
        self._net_prefix = self._detect_net_prefix()

    def _detect_net_prefix(self) -> list[str]:
        if self.network_isolation != "auto":
            return []
        if platform.system() != "Linux":
            return []
        unshare = shutil.which("unshare")
        if not unshare:
            return []
        # Probe: only use unshare -n if the platform actually permits it,
        # otherwise every sandbox run would fail at exec time.
        try:
            probe = subprocess.run([unshare, "-n", "true"],
                                    capture_output=True, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            return []
        return [unshare, "-n"] if probe.returncode == 0 else []

    @staticmethod
    def _scrub_env() -> dict[str, str]:
        env: dict[str, str] = {
            "PATH": os.environ.get("PATH", ""),
            "LC_ALL": "C",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        if platform.system() == "Windows":
            env["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")
        return env

    @staticmethod
    def _check_size(name: str, text: str) -> None:
        if len(text.encode("utf-8", errors="replace")) > MAX_INPUT_BYTES:
            raise SandboxInputError(f"{name} exceeds {MAX_INPUT_BYTES} bytes")

    def run(self, artifact_code: str, program: str, timeout_s: float = 10.0) -> dict:
        """Run `program` appended to `artifact_code` in an isolated subprocess.

        Returns {"ok": bool, "returncode": int|None, "stdout": str,
                 "stderr": str, "timeout": bool, "network_isolated": bool}
        """
        self._check_size("artifact_code", artifact_code)
        self._check_size("program", program)

        is_posix = platform.system() != "Windows"
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
            cmd = self._net_prefix + [self.python_bin, "-I", runner_path]
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout_s,
                    cwd=td,
                    env=self._scrub_env(),
                    preexec_fn=_posix_limits if is_posix else None,
                )
            except subprocess.TimeoutExpired:
                return {
                    "ok": False,
                    "returncode": None,
                    "stdout": "",
                    "stderr": f"sandbox timeout after {timeout_s}s",
                    "timeout": True,
                    "network_isolated": bool(self._net_prefix),
                }
            return {
                "ok": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": proc.stdout[-2000:],
                "stderr": proc.stderr[-2000:],
                "timeout": False,
                "network_isolated": bool(self._net_prefix),
            }
