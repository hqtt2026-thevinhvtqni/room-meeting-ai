import os
import sys
from pathlib import Path
import json
import shutil

from wee.bridge.real_host import RealExecutionHost
from wee.models import WorkContext as W12Context
from wee.bridge.contracts import ExecutionResult


def _normalize_entrypoint(command):
    """W30-DEF-001: resolve interpreter aliases portably.

    Work 13 authority files were authored on Windows and hard-code the
    test entrypoint as ["python.exe", ...]. On POSIX hosts that binary
    name does not exist, so RealExecutionHost fails with ENOENT and the
    E2E result degrades to BLOCKED even though the flow itself is sound.

    Smallest safe fix (repair-coder scope): map a leading python/python.exe
    token to the *currently running* interpreter on every platform. This
    keeps Windows behavior identical (sys.executable IS python.exe there)
    and makes the real-host E2E reproducible on Linux/macOS without
    touching the isolation/policy checks in RealExecutionHost.
    """
    cmd = list(command)
    if not cmd:
        return cmd
    exe = os.path.basename(str(cmd[0])).lower()
    if exe in ("python", "python.exe", "python3", "python3.exe"):
        cmd[0] = sys.executable
    return cmd


class Work13ExecutionHostAdapter:
    provider_type = "W12_REAL_EXECUTION_HOST"

    def __init__(self, context):
        self.host = RealExecutionHost(
            evidence_root=context.evidence_root,
            enabled=True,
            allow_processes=True,
        )

    def _ctx(self, c):
        return W12Context(
            work_id=c.work_id,
            work_name=c.work_name,
            repository=c.repository,
            repository_root=c.repository_root,
            branch=c.branch,
            execution_workspace=c.execution_workspace,
            expected_head=c.expected_head,
            runtime=c.runtime,
            browser=c.browser,
            test_entrypoint=c.test_entrypoint,
            ci_target=c.ci_target,
            evidence_root=c.evidence_root,
            execution_id=c.execution_id,
        )

    def discover(self, context):
        return self.host.discover(self._ctx(context))

    def execute(self, command, context):
        w12 = self._ctx(context)
        command = _normalize_entrypoint(command)
        r = self.host.execute(list(command), w12)

        final = (
            Path(context.evidence_root)
            / context.execution_id
            / "FINAL_RESULT.json"
        )
        final.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "execution_id": r.execution_id,
            "work_id": r.work_id,
            "status": r.status,
            "exit_code": r.exit_code,
            "workspace": r.workspace,
            "command": r.command,
            "stdout_ref": r.stdout_ref,
            "stderr_ref": r.stderr_ref,
            "artifacts": list(r.artifacts),
            "provider_type": self.provider_type,
        }

        final.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        return ExecutionResult(
            execution_id=r.execution_id,
            work_id=r.work_id,
            workspace=r.workspace,
            command=r.command,
            start_time=r.start_time,
            end_time=r.end_time,
            exit_code=r.exit_code,
            stdout_ref=r.stdout_ref,
            stderr_ref=r.stderr_ref,
            artifacts=list(r.artifacts) + [str(final)],
            status=r.status,
            provider_type=self.provider_type,
        )

    def runtime_info(self, context):
        return {
            "execution_id": context.execution_id,
            "provider_type": self.provider_type,
            "python": shutil.which("python.exe"),
            "node": shutil.which("node.exe"),
        }

    def browser_info(self, context):
        result = {
            "execution_id": context.execution_id,
            "provider_type": self.provider_type,
            "status": "NOT_CONFIGURED",
            "provider": "playwright",
            "browser": "chromium",
        }

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as playwright:
                executable_path = Path(
                    playwright.chromium.executable_path
                )

                result["playwright"] = "AVAILABLE"
                result["executable_path"] = str(executable_path)
                result["executable_exists"] = executable_path.exists()

                if executable_path.exists():
                    result["status"] = "AVAILABLE"
                else:
                    result["reason"] = (
                        "playwright_available_but_chromium_executable_missing"
                    )

        except Exception as exc:
            result["reason"] = "playwright_probe_failed"
            result["error"] = str(exc)

        return result

    def workspace_info(self, context):
        return self.host.workspace_info(self._ctx(context))

    def collect_artifact(self, path, execution_id):
        return self.host.collect_artifact(path, execution_id)

    def cleanup(self):
        self.host.cleanup()
