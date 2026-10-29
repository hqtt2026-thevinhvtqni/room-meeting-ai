"""W12-oriented execution adapter: maps ManagedProcess cleanup into results.

Does not claim OS isolation PASS. Does not open network listeners.
Always attaches a real CleanupResult dict (never hard-coded {}).
"""
from __future__ import annotations

import subprocess
from typing import Any, Sequence

from .process_job import CleanupResult, ManagedProcess, spawn_managed
from .security import HostError, redact, safe_env, validate_command, validate_context, validate_cwd


class W12ExecutionAdapter:
    """Run one command under WorkContext; attach attested cleanup."""

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
        members_at_start: int | None = None
        cleanup: dict[str, Any] = CleanupResult(
            process_reaped=True, notes=("not_started",)
        ).as_dict()

        try:
            managed = spawn_managed(args, cwd=workspace, env=env)
            members_at_start = managed.members_count()
            try:
                stdout, stderr = managed.process.communicate(timeout=timeout_seconds)
                exit_code = managed.process.returncode
                status = "PASS" if exit_code == 0 else "FAILED"
            except subprocess.TimeoutExpired as exc:
                blocker = "timeout"
                status = "TIMEOUT"
                if getattr(exc, "output", None):
                    stdout = exc.output if isinstance(exc.output, str) else (stdout or "")
                if getattr(exc, "stderr", None):
                    stderr = exc.stderr if isinstance(exc.stderr, str) else (stderr or "")
            cleanup = managed.cleanup(terminate_first=(status == "TIMEOUT")).as_dict()
            if members_at_start is not None and cleanup.get("members_before") in (None, 0):
                cleanup["members_before"] = members_at_start
            exit_code = managed.process.returncode if exit_code is None else exit_code
        except OSError as exc:
            blocker = redact(str(exc))
            status = "BLOCKED"
            if managed is not None:
                cleanup = managed.cleanup(terminate_first=False).as_dict()
                if members_at_start is not None:
                    cleanup["members_before"] = members_at_start

        if not isinstance(cleanup, dict) or not cleanup:
            cleanup = CleanupResult(process_reaped=False, notes=("cleanup_missing",)).as_dict()

        return {
            "status": status,
            "exit_code": exit_code,
            "stdout": redact(stdout or ""),
            "stderr": redact(stderr or ""),
            "blocker": blocker,
            "cleanup": cleanup,
            "isolation": "NOT_VERIFIED",
            "provider_type": self.provider_type,
            "workspace_root": str(root),
            "execution_workspace": str(workspace),
            "evidence_root": str(evidence),
            "command": list(args),
        }


__all__ = ["W12ExecutionAdapter"]
