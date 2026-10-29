"""WP16–WP19 — Authenticated dispatch: grant → snapshot → execute + sealed evidence.

Server-side only. Client cannot inject grants. MCP execution tools remain closed.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .host import ExecutionHost
from .models import ExecutionRequest, WorkContext, new_execution_id
from .work28_contract import create_source_snapshot
from .work28_execute import run_verified_snapshot
from .work28_grant import ExecutionGrant, GrantError, bind_grant_to_request
from .work28_work_id import work_ids_equivalent
from .work28_evidence import seal_evidence


class DispatchError(ValueError):
    """Request shape or mode is invalid for the execution boundary."""


def dispatch_execute(
    host: ExecutionHost,
    *,
    work_context: dict[str, Any],
    body: dict[str, Any],
    grant_registry: dict[str, ExecutionGrant] | None,
    snapshot_only: bool = False,
) -> dict[str, Any]:
    if not isinstance(body, dict):
        raise DispatchError("body_must_be_object")

    mode = body.get("mode", "command")
    if mode == "work28_snapshot":
        return _dispatch_work28_snapshot(
            host,
            work_context=work_context,
            body=body,
            grant_registry=grant_registry or {},
        )
    if mode != "command":
        raise DispatchError("unsupported_mode:" + str(mode))

    if snapshot_only:
        raise DispatchError("command_mode_disabled_snapshot_only")

    if "work28_request" in body or "execution_grant_id" in body:
        raise DispatchError("work28_fields_require_mode_work28_snapshot")

    ctx = WorkContext(**work_context)
    if not ctx.execution_id:
        work_context = dict(work_context)
        work_context["execution_id"] = new_execution_id()
        ctx = WorkContext(**work_context)

    req = ExecutionRequest(**(body.get("execution_request") or {}))
    result = host.execute_work(ctx, req).as_dict()
    result["dispatch_mode"] = "command"
    return result


def _dispatch_work28_snapshot(
    host: ExecutionHost,
    *,
    work_context: dict[str, Any],
    body: dict[str, Any],
    grant_registry: dict[str, ExecutionGrant],
) -> dict[str, Any]:
    grant_id = body.get("execution_grant_id")
    if not isinstance(grant_id, str) or not grant_id:
        raise DispatchError("execution_grant_id_required")

    grant = grant_registry.get(grant_id)
    if grant is None:
        raise GrantError("grant_not_found")

    payload = body.get("work28_request")
    if not isinstance(payload, dict):
        raise DispatchError("work28_request_required")

    request = bind_grant_to_request(grant, payload)

    ctx_data = dict(work_context)
    if not work_ids_equivalent(ctx_data.get("work_id"), grant.work_id):
        raise GrantError("context_grant_work_mismatch")

    if not ctx_data.get("execution_id"):
        ctx_data["execution_id"] = new_execution_id()
    ctx_data["authorized"] = True
    ctx = WorkContext(**ctx_data)

    work_root = Path(ctx.workspace_root).resolve()
    snap_parent = Path(ctx.evidence_root).resolve() / "snapshots"
    snap_parent.mkdir(parents=True, exist_ok=True)

    snapshot = create_source_snapshot(
        request=request,
        authoritative_work_id=grant.work_id,
        work_root=work_root,
        snapshot_root=snap_parent,
    )
    result = run_verified_snapshot(host, ctx, request, snapshot)
    result["dispatch_mode"] = "work28_snapshot"
    result["grant_id"] = grant.grant_id
    result["snapshot_ref"] = snapshot.snapshot_ref
    result["source_sha256"] = snapshot.source_sha256
    sealed = seal_evidence(
        evidence_root=ctx.evidence_root,
        execution_id=ctx.execution_id or "unknown",
        payload={
            "grant_id": grant.grant_id,
            "work_id": grant.work_id,
            "snapshot_ref": snapshot.snapshot_ref,
            "source_sha256": snapshot.source_sha256,
            "dispatch_mode": "work28_snapshot",
            "status": result.get("status"),
            "exit_code": result.get("exit_code"),
            "execution_id": ctx.execution_id,
        },
    )
    result.update(sealed)
    return result


__all__ = ["DispatchError", "dispatch_execute"]
