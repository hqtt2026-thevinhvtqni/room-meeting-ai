"""Work 28 offline execution against a verified SourceSnapshot (WP14).

Rules (Xu):
- Run only bytes already hashed into SourceSnapshot — never re-read work_root entry.
- Stage a verified copy under the authorized execution workspace (relative path only;
  host security rejects absolute args).
- Use host.execute_command so lifecycle goes through spawn_managed / Job Object.
- Do NOT authorize callers here; Core supplies authoritative work binding upstream.
- Do NOT wire this module into HTTP / MCP registration in this slice.
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path
from typing import Any

from .host import ExecutionHost
from .models import WorkContext
from .security import validate_context
from .work28_contract import SourceSnapshot, Work28ContractError, Work28RunRequest


def run_verified_snapshot(
    host: ExecutionHost,
    ctx: WorkContext,
    request: Work28RunRequest,
    snapshot: SourceSnapshot,
) -> dict[str, Any]:
    """Execute Python against verified snapshot bytes only."""
    if ctx.work_id != request.work_id:
        raise Work28ContractError("context_work_binding_mismatch")
    if snapshot.work_id != request.work_id:
        raise Work28ContractError("snapshot_work_binding_mismatch")
    if snapshot.entry_path != request.entry_path:
        raise Work28ContractError("snapshot_entry_mismatch")
    if snapshot.source_sha256 != request.expected_source_sha256:
        raise Work28ContractError("snapshot_hash_binding_mismatch")

    path = Path(snapshot.snapshot_path)
    if not path.is_file():
        raise Work28ContractError("snapshot_path_missing")

    live = hashlib.sha256(path.read_bytes()).hexdigest()
    if live != snapshot.source_sha256:
        raise Work28ContractError("snapshot_tampered_or_mutated")

    _, workspace, _ = validate_context(ctx)
    staged_name = f"w28_snap_{snapshot.source_sha256[:16]}.py"
    staged = (workspace / staged_name).resolve()
    try:
        staged.relative_to(workspace.resolve())
    except ValueError as exc:
        raise Work28ContractError("stage_path_escape") from exc

    shutil.copy2(path, staged)
    staged_hash = hashlib.sha256(staged.read_bytes()).hexdigest()
    if staged_hash != snapshot.source_sha256:
        staged.unlink(missing_ok=True)
        raise Work28ContractError("staged_hash_mismatch")

    try:
        command = [sys.executable, staged_name]
        result = host.execute_command(
            ctx,
            command,
            timeout_seconds=float(request.timeout_seconds),
        )
    finally:
        try:
            staged.unlink(missing_ok=True)
        except OSError:
            pass

    result = dict(result)
    result["snapshot_ref"] = snapshot.snapshot_ref
    result["source_sha256"] = snapshot.source_sha256
    result["operation"] = request.operation
    result["wp14_path"] = "verified_snapshot_only"
    return result


__all__ = ["run_verified_snapshot"]
