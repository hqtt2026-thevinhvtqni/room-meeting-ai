from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import (
    WorkContext,
    ExecutionRequest,
    ExecutionResult,
    new_execution_id,
)
from .security import (
    HostError,
    redact,
    validate_context,
    validate_command,
    validate_cwd,
    safe_env,
    executable_capabilities,
)
from .adapters import unavailable
from .git_adapter import GitAdapter
from .identity import RuntimeIdentity


class ExecutionHost:
    provider_type = "SANDBOX_REAL_PROCESS"

    def __init__(
        self,
        *,
        browser=None,
        github=None,
        ci=None,
        runtime_identity: RuntimeIdentity | None = None,
    ):
        self.browser = browser
        self.github = github
        self.ci = ci
        self.runtime_identity = runtime_identity or RuntimeIdentity()
        self.processes: dict[str, subprocess.Popen] = {}

    def identity(self) -> dict[str, Any]:
        return self.runtime_identity.as_dict()

    def _evidence(
        self,
        evidence_root: Path,
        execution_id: str,
        payload: dict[str, Any],
    ) -> str:
        target = (
            evidence_root
            / execution_id
            / "FINAL_RESULT.json"
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

        return str(target)

    def discover(
        self,
        ctx: WorkContext,
    ) -> dict[str, Any]:
        validate_context(ctx)

        return {
            "status": "PASS",
            "provider": self.provider_type,
            "execution_id": ctx.execution_id,
            "work_id": ctx.work_id,
            "capabilities": executable_capabilities(),
            "browser": (
                "AVAILABLE"
                if self.browser
                else "NOT_CONFIGURED"
            ),
            "github": (
                "AVAILABLE"
                if self.github
                else "NOT_CONFIGURED"
            ),
            "ci": (
                "AVAILABLE"
                if self.ci
                else "NOT_CONFIGURED"
            ),
            **self.identity(),
        }

    def _artifact(
        self,
        source: str,
        workspace: Path,
        evidence: Path,
        execution_id: str,
    ) -> str:
        src = Path(source)

        if not src.is_absolute():
            src = workspace / src

        src = src.resolve()

        validate_cwd(src.parent, workspace)

        if not src.exists() or not src.is_file():
            return ""

        dest = (
            evidence
            / execution_id
            / "artifacts"
            / src.name
        ).resolve()

        dest.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(src, dest)

        return str(dest)

    @staticmethod
    def _cleanup_process(
        process: subprocess.Popen,
        *,
        terminate_first: bool = False,
    ) -> tuple[str, str]:
        """
        Windows-safe process cleanup.

        Returns:
            stdout, stderr
        """

        if process.poll() is None:
            try:
                if terminate_first:
                    process.terminate()
                else:
                    process.kill()

                process.wait(timeout=5)

            except (subprocess.TimeoutExpired, OSError):
                try:
                    process.kill()
                except OSError:
                    pass

                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass

        try:
            out, err = process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass

            out, err = process.communicate()

        return out or "", err or ""

    def execute_command(
        self,
        ctx: WorkContext,
        command: list[str],
        timeout_seconds: float = 30.0,
    ) -> dict[str, Any]:

        root, workspace, evidence = validate_context(ctx)

        args = validate_command(command)

        validate_cwd(workspace, workspace)

        if timeout_seconds <= 0 or timeout_seconds > 3600:
            raise HostError("invalid_timeout")

        started = datetime.now(timezone.utc).isoformat()

        out_path = (
            evidence
            / ctx.execution_id
            / "runtime"
            / "stdout.log"
        )

        err_path = (
            evidence
            / ctx.execution_id
            / "runtime"
            / "stderr.log"
        )

        out_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        env = safe_env()

        env.update(
            {
                "ROOM_HOP_EXECUTION_ID": ctx.execution_id,
                "ROOM_HOP_WORK_ID": ctx.work_id,
            }
        )

        process = None

        status = "FAILED"
        exit_code = None
        stdout = ""
        stderr = ""
        blocker = None

        try:
            process = subprocess.Popen(
                args,
                cwd=workspace,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )

            stdout, stderr = process.communicate(
                timeout=timeout_seconds
            )

            exit_code = process.returncode

            stdout = redact(stdout or "")
            stderr = redact(stderr or "")

            status = (
                "PASS"
                if exit_code == 0
                else "FAILED"
            )

        except subprocess.TimeoutExpired:
            blocker = "timeout"
            status = "TIMEOUT"

            if process is not None:
                stdout, stderr = self._cleanup_process(
                    process,
                    terminate_first=False,
                )

                stdout = redact(stdout)
                stderr = redact(stderr)

                exit_code = process.returncode

        except OSError as exc:
            blocker = redact(str(exc))
            status = "BLOCKED"

        out_path.write_text(
            stdout,
            encoding="utf-8",
        )

        err_path.write_text(
            stderr,
            encoding="utf-8",
        )

        result = {
            "execution_id": ctx.execution_id,
            "work_id": ctx.work_id,
            "workspace_root": str(root),
            "execution_workspace": str(workspace),
            "command": args,
            "started_at": started,
            "finished_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "exit_code": exit_code,
            "stdout_summary": stdout[-4000:],
            "stderr_summary": stderr[-4000:],
            "status": status,
            "blocker": blocker,
            "isolation": "PASS",
            "authorization": ctx.authorized,
            "artifacts": [],
            "cleanup": {
                "process_reaped": (
                    process is None
                    or process.poll() is not None
                )
            },
            "runtime_instance_id": (
                self.runtime_identity.instance_id
            ),
            "runtime_build_hash": (
                self.runtime_identity.build_hash
            ),
            "runtime_started_at": (
                self.runtime_identity.started_at
            ),
            "runtime_pid": self.runtime_identity.pid,
            "runtime_platform": self.runtime_identity.platform,
            "runtime_bind_address": (
                self.runtime_identity.bind_address
            ),
        }

        result["stdout_ref"] = str(out_path)
        result["stderr_ref"] = str(err_path)

        result["evidence_ref"] = self._evidence(
            evidence,
            ctx.execution_id,
            result,
        )

        return result

    def execute_work(
        self,
        ctx: WorkContext,
        request: ExecutionRequest,
    ) -> ExecutionResult:

        execution_id = (
            ctx.execution_id
            or new_execution_id()
        )

        execution_ctx = replace(
            ctx,
            execution_id=execution_id,
        )

        result = self.execute_command(
            execution_ctx,
            list(request.command or ()),
            request.timeout_seconds,
        )

        if request.run_test:
            if not execution_ctx.test_entrypoint:
                result["test"] = {
                    "status": "BLOCKED",
                    "reason": "test_entrypoint_not_bound",
                }
            else:
                result["test"] = (
                    self.execute_command(
                        execution_ctx,
                        list(
                            execution_ctx.test_entrypoint
                        ),
                        request.timeout_seconds,
                    )
                )

        _, workspace, evidence = validate_context(
            execution_ctx
        )

        result["artifacts"] = [
            artifact
            for artifact in (
                self._artifact(
                    source,
                    workspace,
                    evidence,
                    execution_id,
                )
                for source in request.collect_artifacts
            )
            if artifact
        ]

        result["evidence_ref"] = self._evidence(
            evidence,
            execution_id,
            result,
        )

        return ExecutionResult(
            execution_id=execution_id,
            work_id=ctx.work_id,
            status=result["status"],
            exit_code=result["exit_code"],
            stdout=result.get(
                "stdout_summary",
                "",
            ),
            stderr=result.get(
                "stderr_summary",
                "",
            ),
            artifacts=result["artifacts"],
            evidence_ref=result["evidence_ref"],
            blocker=result.get("blocker"),
            cleanup=result["cleanup"],
            runtime_instance_id=(
                self.runtime_identity.instance_id
            ),
            runtime_build_hash=(
                self.runtime_identity.build_hash
            ),
            runtime_started_at=(
                self.runtime_identity.started_at
            ),
            runtime_pid=self.runtime_identity.pid,
            runtime_platform=self.runtime_identity.platform,
            runtime_bind_address=(
                self.runtime_identity.bind_address
            ),
        )

    def start_service(
        self,
        name: str,
        command: list[str],
        ctx: WorkContext,
    ) -> dict[str, Any]:

        _, workspace, _ = validate_context(ctx)

        args = validate_command(command)

        existing = self.processes.get(name)

        if existing and existing.poll() is None:
            return {
                "status": "PASS",
                "name": name,
                "pid": existing.pid,
                "already_running": True,
                "execution_id": ctx.execution_id,
                **self.identity(),
            }

        env = safe_env()

        env.update(
            {
                "ROOM_HOP_EXECUTION_ID": ctx.execution_id,
                "ROOM_HOP_WORK_ID": ctx.work_id,
            }
        )

        process = subprocess.Popen(
            args,
            cwd=workspace,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )

        self.processes[name] = process

        return {
            "status": "PASS",
            "name": name,
            "pid": process.pid,
            "execution_id": ctx.execution_id,
            **self.identity(),
        }

    def service_status(
        self,
        name: str,
        ctx: WorkContext,
    ) -> dict[str, Any]:

        process = self.processes.get(name)

        return {
            "status": (
                "PASS"
                if process
                and process.poll() is None
                else "STOPPED"
            ),
            "name": name,
            "pid": process.pid if process else None,
            "returncode": (
                process.poll()
                if process
                else None
            ),
            "execution_id": ctx.execution_id,
            **self.identity(),
        }

    def stop_service(
        self,
        name: str,
        ctx: WorkContext,
    ) -> dict[str, Any]:

        process = self.processes.pop(name, None)

        if not process:
            return {
                "status": "STOPPED",
                "name": name,
                "execution_id": ctx.execution_id,
                **self.identity(),
            }

        if process.poll() is None:
            stdout, stderr = self._cleanup_process(
                process,
                terminate_first=True,
            )

        return {
            "status": "PASS",
            "name": name,
            "returncode": process.returncode,
            "execution_id": ctx.execution_id,
            "process_reaped": process.poll() is not None,
            **self.identity(),
        }

    def git_validate(self, ctx):
        return GitAdapter(ctx).validate()

    def git_status(self, ctx):
        return GitAdapter(ctx).status()

    def git_push(self, ctx, authorized=False):
        return GitAdapter(ctx).push(authorized)

    def browser_execute(
        self,
        ctx,
        action,
        timeout_seconds=30,
    ):
        return (
            self.browser.execute(
                ctx.execution_id,
                ctx,
                action,
                timeout_seconds,
            )
            if self.browser
            else unavailable(
                "browser",
                ctx.execution_id,
            )
        )

    def verify_head(
        self,
        ctx,
        expected_head,
    ):
        return (
            self.github.verify_head(
                ctx.execution_id,
                ctx,
                expected_head,
            )
            if self.github
            else unavailable(
                "github",
                ctx.execution_id,
            )
        )

    def verify_ci(
        self,
        ctx,
        commit_sha,
    ):
        return (
            self.ci.verify(
                ctx.execution_id,
                ctx,
                commit_sha,
            )
            if self.ci
            else unavailable(
                "ci",
                ctx.execution_id,
            )
        )