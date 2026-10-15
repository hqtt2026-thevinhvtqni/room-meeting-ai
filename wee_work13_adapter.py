from pathlib import Path
import json
import os
import shutil
import sys

from wee.bridge.real_host import RealExecutionHost
from wee.models import WorkContext as W12Context
from wee.bridge.contracts import ExecutionResult


def _normalize_command(command):
    """
    Platform-portability shim (Windows -> Linux/macOS).

    Authority contract test data tren PC Vinh dung 'python.exe' (Windows).
    Tren cac platform khac, executable do khong ton tai -> subprocess tra
    OSError -> host BLOCKED. Ta thay the bang interpreter dang chay
    (sys.executable) de giu nguyen y nghia test ma khong doi authority
    data duoc dong bang trong tests/.
    """
    normalized = []
    for token in command:
        if isinstance(token, str) and Path(token).name.lower() in (
            "python.exe",
            "pythonw.exe",
        ):
            normalized.append(sys.executable)
        else:
            normalized.append(token)
    return normalized


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
        r = self.host.execute(_normalize_command(command), w12)

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
