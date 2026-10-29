"""W12-oriented execution adapter: maps ManagedProcess cleanup into results.

Does not claim OS isolation PASS. Does not open network listeners.
"""
from __future__ import annotations

import subprocess
from typing import Any, Sequence

from .process_job import CleanupResult, ManagedProcess, spawn_managed
from .security import HostError, redact, safe_env, validate_command, validate_context, validate_cwd


class W12ExecutionAdapter:
    """Run one command under WorkContext; attach real cleanup attestation."""

    provider_type = "W12_MANAGED_PROCESS"

    def execute(
        self,
        ctx: Any,
        command: Sequence[str],
        *,
        timeout_seconds: float = 30.0,
    ) -> dict[str, Any]:
        root, workspace, evidence = validate_context(ctx)
        args = validate_command(list(command))
        validate_cwd(workspace, workspace)
        if timeout_seconds <= 0 or timeout_seconds > 3600:
            raise HostError("invalid_timeout")

        env = safe_env()
        env.update(
            {
                "ROOM_HOP_EXECUTION_ID": getattr(ctx, "execution_id", "") or "",
                "ROOM_HOP_WORK_ID": getattr(ctx, "work_id", "") or "",
            }
        )

        managed: ManagedProcess | None = None
        status = "FAILED"
        exit_code = None
        stdout = ""
        stderr = ""
        blocker = None
        cleanup: dict[str, Any] = CleanupResult(process_reaped=True).as_dict()

        try:
            managed = spawn_managed(args, cwd=workspace, env=env)
            try:
                stdout, stderr = managed.process.communicate(timeout=timeout_seconds)
                exit_code = managed.process.returncode
                status = "PASS" if exit_code == 0 else "FAILED"
                # Process already exited; still record attested cleanup snapshot.
                cleanup = managed.cleanup(terminate_first=False).as_dict()
            except subprocess.TimeoutExpired:
                blocker = "timeout"
                status = "TIMEOUT"
                cleanup = managed.cleanup(terminate_first=False).as_dict()
                exit_code = managed.process.returncode
                stdout = stdout or ""
                stderr = stderr or ""
        except OSError as exc:
            blocker = redact(str(exc))
            status = "BLOCKED"
            if managed is not None:
                cleanup = managed.cleanup(terminate_first=False).as_dict()

        return {
            "status": status,
            "exit_code": exit_code,
            "stdout": redact(stdout or ""),
            "stderr": redact(stderr or ""),
            "blocker": blocker,
            "cleanup": cleanup,  # never hard-coded {}
            "isolation": "NOT_VERIFIED",  # honest: process reaping ≠ OS sandbox
            "provider_type": self.provider_type,
            "workspace_root": str(root),
            "execution_workspace": str(workspace),
            "command": list(args),
        }


__all__ = ["W12ExecutionAdapter"]
