"""execute_command path: spawn_managed at process creation; isolation NOT_VERIFIED."""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from typing import Any

from .models import WorkContext
from .security import HostError, redact, safe_env, validate_command, validate_context, validate_cwd
from .host_cleanup_bridge import ISOLATION_STATUS, attested_cleanup, spawn_managed


def run_execute_command(host: Any, ctx: WorkContext, command: list[str], timeout_seconds: float = 30.0) -> dict[str, Any]:
    root, workspace, evidence = validate_context(ctx)
    args = validate_command(command)
    validate_cwd(workspace, workspace)
    if timeout_seconds <= 0 or timeout_seconds > 3600:
        raise HostError("invalid_timeout")

    started = datetime.now(timezone.utc).isoformat()
    out_path = evidence / ctx.execution_id / "runtime" / "stdout.log"
    err_path = evidence / ctx.execution_id / "runtime" / "stderr.log"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    env = safe_env()
    env.update({
        "ROOM_HOP_EXECUTION_ID": ctx.execution_id,
        "ROOM_HOP_WORK_ID": ctx.work_id,
    })

    managed = None
    process = None
    status = "FAILED"
    exit_code = None
    stdout = ""
    stderr = ""
    blocker = None

    try:
        managed = spawn_managed(args, cwd=workspace, env=env)
        process = managed.process
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        exit_code = process.returncode
        stdout = redact(stdout or "")
        stderr = redact(stderr or "")
        status = "PASS" if exit_code == 0 else "FAILED"
    except subprocess.TimeoutExpired:
        blocker = "timeout"
        status = "TIMEOUT"
        if managed is not None:
            managed.cleanup(terminate_first=True)
            try:
                out, err = process.communicate(timeout=1)
                stdout, stderr = out or "", err or ""
            except Exception:
                stdout, stderr = stdout or "", stderr or ""
            stdout = redact(stdout)
            stderr = redact(stderr)
            exit_code = process.returncode
    except OSError as exc:
        blocker = redact(str(exc))
        status = "BLOCKED"

    out_path.write_text(stdout, encoding="utf-8")
    err_path.write_text(stderr, encoding="utf-8")

    result = {
        "execution_id": ctx.execution_id,
        "work_id": ctx.work_id,
        "workspace_root": str(root),
        "execution_workspace": str(workspace),
        "command": args,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": exit_code,
        "stdout_summary": stdout[-4000:],
        "stderr_summary": stderr[-4000:],
        "status": status,
        "blocker": blocker,
        "isolation": ISOLATION_STATUS,
        "authorization": ctx.authorized,
        "artifacts": [],
        "cleanup": attested_cleanup(managed),
        "runtime_instance_id": host.runtime_identity.instance_id,
        "runtime_build_hash": host.runtime_identity.build_hash,
        "runtime_started_at": host.runtime_identity.started_at,
        "runtime_pid": host.runtime_identity.pid,
        "runtime_platform": host.runtime_identity.platform,
        "runtime_bind_address": host.runtime_identity.bind_address,
    }
    result["stdout_ref"] = str(out_path)
    result["stderr_ref"] = str(err_path)
    result["evidence_ref"] = host._evidence(evidence, ctx.execution_id, result)
    return result
