from __future__ import annotations

import sys
import json
from pathlib import Path

W12_CODE = (
    Path(__file__).resolve().parents[4]
    / "12"
    / "WORK-EXECUTION-ENVIRONMENT"
    / "04_CODE"
)

if str(W12_CODE) not in sys.path:
    sys.path.insert(0, str(W12_CODE))

from wee.bridge.real_host import RealExecutionHost
from wee.models import WorkBinding, WorkContext as W12WorkContext

from .host import HostError, validate_context
from .security import validate_command
from .models import ExecutionRequest, ExecutionResult, WorkContext


class W12ExecutionAdapter:
    """W13 security/runtime boundary adapter over W12 canonical execution host."""

    provider_type = "W12_REAL_EXECUTION_HOST"

    def __init__(
        self,
        *,
        allow_processes: bool = True,
        runtime_identity=None,
    ) -> None:
        self.allow_processes = allow_processes
        self.runtime_identity = runtime_identity
        self.host: RealExecutionHost | None = None

    @staticmethod
    def _binding(ctx: WorkContext) -> WorkBinding:
        return WorkBinding(
            work_id=ctx.work_id,
            work_name=ctx.work_name,
            repository=ctx.repository,
            repository_root=ctx.repository_root,
            branch=ctx.branch,
            execution_workspace=ctx.execution_workspace,
            expected_head=ctx.expected_head,
            runtime=dict(ctx.runtime),
            browser=dict(ctx.browser),
            test_entrypoint=list(ctx.test_entrypoint)
            if ctx.test_entrypoint is not None
            else None,
            ci_target=ctx.ci_target,
            evidence_root=ctx.evidence_root,
        )

    @classmethod
    def _w12_context(cls, ctx: WorkContext) -> W12WorkContext:
        return W12WorkContext.from_binding(
            cls._binding(ctx),
            execution_id=ctx.execution_id,
        )

    @staticmethod
    def _unsupported_request(request: ExecutionRequest) -> str | None:
        if request.timeout_seconds != 30.0:
            return "w12_timeout_control_not_supported"
        if request.collect_artifacts:
            return "w12_collect_artifacts_not_supported"
        if request.run_test:
            return "w12_run_test_not_supported"
        return None

    def execute_work(
        self,
        ctx: WorkContext,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        try:
            validate_context(ctx)
        except HostError as exc:
            return ExecutionResult(
                execution_id=ctx.execution_id or "",
                work_id=ctx.work_id,
                status="BLOCKED",
                blocker=str(exc),
            )

        if not request.command:
            return ExecutionResult(
                execution_id=ctx.execution_id or "",
                work_id=ctx.work_id,
                status="BLOCKED",
                blocker="execution_command_missing",
            )

        try:
            validate_command(list(request.command))  # W13 executable allowlist / injection / absolute-arg rules
        except HostError as exc:
            return ExecutionResult(
                execution_id=ctx.execution_id or "",
                work_id=ctx.work_id,
                status="BLOCKED",
                blocker=str(exc),
            )

        unsupported = self._unsupported_request(request)
        if unsupported:
            return ExecutionResult(
                execution_id=ctx.execution_id or "",
                work_id=ctx.work_id,
                status="BLOCKED",
                blocker=unsupported,
            )

        self.host = RealExecutionHost(
            evidence_root=ctx.evidence_root,
            enabled=True,
            allow_processes=self.allow_processes,
        )

        w12_context = self._w12_context(ctx)

        result = self.host.execute(
            list(request.command),
            w12_context,
            timeout_seconds=request.timeout_seconds,
        )

        ident = (
            self.runtime_identity.as_dict()
            if self.runtime_identity is not None
            else {}
        )

        evidence_path = Path(ctx.evidence_root) / (ctx.execution_id or result.execution_id) / "FINAL_RESULT.json"
        evidence_payload = {
            "execution_id": result.execution_id,
            "work_id": result.work_id,
            "work_name": ctx.work_name,
            "status": result.status,
            "exit_code": result.exit_code,
            "source_sha256": dict(ctx.runtime).get("source_sha256"),
            "stdout_ref": result.stdout_ref,
            "stderr_ref": result.stderr_ref,
            "artifacts": list(result.artifacts),
            "runtime_identity": ident,
            "provider": self.provider_type,
            "blocker": getattr(result, "blocker", None),
            "timed_out": getattr(result, "timed_out", False),
            "process_tree_cleanup_verified": getattr(result, "process_tree_cleanup_verified", False),
        }
        try:
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(
                json.dumps(evidence_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError:
            return ExecutionResult(
                execution_id=result.execution_id,
                work_id=result.work_id,
                status="BLOCKED",
                exit_code=result.exit_code,
                stdout=result.stdout_ref or "",
                stderr=result.stderr_ref or "",
                artifacts=list(result.artifacts),
                blocker="w13_evidence_write_failed",
            )

        return ExecutionResult(
            execution_id=result.execution_id,
            work_id=result.work_id,
            status=result.status,
            exit_code=result.exit_code,
            stdout=result.stdout_ref or "",
            stderr=result.stderr_ref or "",
            artifacts=list(result.artifacts),
            evidence_ref=str(evidence_path),
            blocker=(
                None
                if result.status != "BLOCKED"
                else (getattr(result, "blocker", None) or "w12_execution_blocked")
            ),
            cleanup={
                "timed_out": getattr(result, "timed_out", False),
                "process_tree_cleanup_verified": getattr(result, "process_tree_cleanup_verified", False),
            },
            runtime_instance_id=ident.get("instance_id"),
            runtime_build_hash=ident.get("build_hash"),
            runtime_started_at=ident.get("started_at"),
            runtime_pid=ident.get("pid"),
            runtime_platform=ident.get("platform"),
            runtime_bind_address=ident.get("bind_address"),
        )

    def cleanup(self) -> None:
        if self.host is not None:
            self.host.cleanup()

