"""Tester Agent backend (charter §3, An role).

Independent verification: the Tester receives the original acceptance
programs and the ACTUAL artifact (code text), re-verifies its hash, runs
each program in the Sandbox, and returns PASS/FAIL with evidence.

The Tester never modifies the artifact and never sees the Coder's
reasoning. Verdict without evidence is rejected by the orchestrator
(D-06 evidence gate). `tester_mode="strip_evidence"` is a fault-injection
mode used only by the test suite to prove the gate works.
"""

from __future__ import annotations

import json

from .a2a import AgentBackend, artifact_text, make_task, make_text_artifact
from .evidence import sha256_text
from .sandbox import Sandbox
from .sandbox_container import ContainerSandbox


class TesterBackend(AgentBackend):
    # Prevent pytest from mistaking this imported backend for a test class.
    __test__ = False

    def __init__(self, sandbox: Sandbox | ContainerSandbox | None = None):
        super().__init__()
        if sandbox is not None:
            # Explicit dependency injection wins, keeping tests and deployments deterministic.
            self.sandbox = sandbox
        else:
            # Prefer the container profile when Docker and its image are available;
            # otherwise retain the portable subprocess sandbox.
            container_sandbox = ContainerSandbox()
            self.sandbox = container_sandbox if container_sandbox.available() else Sandbox()

    def agent_card(self) -> dict:
        return {
            "protocolVersion": "1.0",
            "version": "1.2.0",
            "preferredTransport": "JSONRPC",
            "name": "work51-tester-agent",
            "description": "Independently verifies artifact against Work Contract acceptance programs.",
            "url": "in-process://work51/tester",
            "capabilities": {"pushNotifications": False, "streaming": False},
            "defaultInputModes": ["application/json"],
            "defaultOutputModes": ["application/json", "text/plain"],
            "skills": [{"id": "work51-tester", "name": "Artifact verification", "description": "Verifies an artifact against acceptance programs and returns a verdict with evidence.", "tags": ["testing", "verification"], "examples": ["Verify a Python artifact against acceptance checks."]}],
            "metadata": {"role": "tester", "can_modify_artifact": False},
        }

    def handle_task(self, task_id: str, payload: dict, existing: dict | None) -> dict:
        kind = payload.get("kind")
        if kind != "verify":
            return make_task(
                task_id, "failed",
                status_message=f"unsupported payload kind: {kind!r}",
                metadata={"error": "unsupported_kind"},
            )

        contract_id = payload.get("contract_id", "")
        programs = payload.get("acceptance_programs") or []
        timeout_s = float(payload.get("sandbox_timeout_s", 10.0))
        artifact = payload.get("artifact") or {}
        content = artifact.get("content", "")
        claimed_sha = artifact.get("sha256", "")
        filename = artifact.get("filename", "artifact.py")

        results: list[dict] = []
        # Integrity check: hash must match the content actually tested.
        actual_sha = sha256_text(content)
        if not content or actual_sha != claimed_sha:
            results.append({
                "program_index": None,
                "ok": False,
                "reason": "artifact hash mismatch or empty artifact",
                "claimed_sha256": claimed_sha,
                "actual_sha256": actual_sha,
            })
        else:
            for i, program in enumerate(programs):
                run = self.sandbox.run(content, program, timeout_s=timeout_s)
                results.append({
                    "program_index": i,
                    "ok": run["ok"],
                    "returncode": run["returncode"],
                    "timeout": run["timeout"],
                    "stderr": run["stderr"][-500:],
                    "stdout": run["stdout"][-500:],
                })

        verdict = "PASS" if results and all(r["ok"] for r in results) else "FAIL"

        verdict_obj = {
            "contract_id": contract_id,
            "verdict": verdict,
            "artifact_sha256": actual_sha,
            "artifact_filename": filename,
            "results": results,
            "tester": "work51-tester-agent/1.0",
        }
        if payload.get("tester_mode") == "strip_evidence":
            # Fault injection: no results, no sha — the evidence gate must reject this.
            verdict_obj = {
                "contract_id": contract_id,
                "verdict": verdict,
                "tester": "work51-tester-agent/1.0",
            }

        text = json.dumps(verdict_obj, ensure_ascii=False, indent=2)
        artifact_out = make_text_artifact(
            name=
"verdict.json",
            text=text,
            sha256=sha256_text(text),
            version=1,
            description=f"tester verdict for {contract_id} (artifact {claimed_sha[:12]})",
        )
        return make_task(
            task_id,
            "completed",
            artifacts=[artifact_out],
            status_message=f"verdict {verdict}",
            metadata={"tester": {"contract_id": contract_id, "verdict": verdict}},
        )
