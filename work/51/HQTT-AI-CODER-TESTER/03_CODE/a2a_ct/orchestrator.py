"""Orchestrator — the A2A consumer that drives the Coder-Tester loop.

Pipeline (PLAN_WORK51 §4 P2):
  1. send contract brief to Coder            -> artifact (versioned, hashed)
  2. send artifact + acceptance to Tester    -> verdict with evidence
  3. PASS with evidence        -> status PASS, stop
  4. FAIL and rounds remaining -> actionable feedback to Coder, re-verify
  5. FAIL beyond max rounds    -> BLOCKED with evidence (no infinite loop)

Rules honored here:
- A2A task `completed` is NOT test PASS (only the Tester verdict + evidence count).
- PASS without evidence -> BLOCKED (D-06).
- max_fix_rounds is a hard cap (default 2, charter §5).
- Transport failures -> BLOCKED with reason, never a silent hang.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .a2a import artifact_text
from .contract import WorkContract
from .evidence import EvidenceLog, sha256_text


@dataclass
class RunReport:
    contract_id: str
    status: str            # PASS | FAIL | BLOCKED
    reason: str
    rounds_used: int       # feedback rounds consumed (0 = passed first try)
    artifact_sha256: str | None
    verdict: dict | None
    evidence_path: str

    def summary(self) -> str:
        return (
            f"[{self.status}] contract={self.contract_id} "
            f"rounds={self.rounds_used} reason={self.reason} "
            f"artifact={(self.artifact_sha256 or 'n/a')[:12]} evidence={self.evidence_path}"
        )


def _artifact_from_task(task: dict | None) -> dict | None:
    """Extract the first artifact of a completed task, else None."""
    if not isinstance(task, dict):
        return None
    if task.get("state") != "completed":
        return None
    artifacts = task.get("artifacts") or []
    return artifacts[0] if artifacts else None


def _verdict_from_task(task: dict) -> dict | None:
    artifact = _artifact_from_task(task)
    if artifact is None:
        return None
    try:
        verdict = json.loads(artifact_text(artifact))
    except ValueError:
        return None
    return verdict if isinstance(verdict, dict) else None


def run_pipeline(contract: WorkContract, coder, tester, evidence: EvidenceLog) -> RunReport:
    """coder/tester: any client with .send(payload, task_id=None) -> task dict
    (A2AClient over HTTP, or LocalClient in-process)."""
    evidence.log("run_start", contract_id=contract.contract_id,
                 coder_mode=contract.coder_mode, tester_mode=contract.tester_mode,
                 max_fix_rounds=contract.max_fix_rounds)

    brief = contract.coder_brief()

    # -- 1. brief -> Coder -------------------------------------------------
    try:
        coder_task = coder.send(brief)
    except Exception as exc:  # TransportError and friends
        return _finish(evidence, contract, "BLOCKED", f"coder_transport_error: {exc}",
                       0, None, None)
    evidence.log("coder_task", task_id=coder_task.get("id"),
                state=coder_task.get("state"))
    artifact = _artifact_from_task(coder_task)
    if artifact is None:
        return _finish(evidence, contract, "BLOCKED", "coder_produced_no_artifact",
                       0, None, None)
    content = artifact_text(artifact)
    sha = artifact.get("metadata", {}).get("sha256") or sha256_text(content)
    evidence.log("coder_artifact", filename=artifact.get("name"),
                 sha256=sha, version=artifact.get("metadata", {}).get("version"))

    # -- 2..5 verify / feedback loop -----------------------------------------
    fix_rounds = 0
    verdict: dict | None = None
    status = "BLOCKED"
    reason = "unknown"

    while True:
        verify_payload = contract.tester_brief() | {
            "artifact": {"filename": artifact.get("name"), "content": content, "sha256": sha},
        }
        try:
            tester_task = tester.send(verify_payload)
        except Exception as exc:
            status, reason = "BLOCKED", f"tester_transport_error: {exc}"
            break

        verdict = _verdict_from_task(tester_task)
        if verdict is None:
            status, reason = "BLOCKED", "tester_produced_no_verdict"
            break
        evidence.log("tester_verdict", contract_id=contract.contract_id,
                     verdict=verdict.get("verdict"),
                     has_results=bool(verdict.get("results")),
                     artifact_sha=verdict.get("artifact_sha256"))

        if verdict.get("verdict") == "PASS":
            has_evidence = bool(verdict.get("results")) and verdict.get("artifact_sha256")
            if has_evidence and verdict.get("artifact_sha256") == sha:
                status, reason = "PASS", "all_acceptance_programs_passed"
            else:
                # PASS without evidence does NOT count (charter §6, D-06).
                status, reason = "BLOCKED", "pass_without_evidence"
            break

        # FAIL path: bounded feedback loop.
        if fix_rounds >= contract.max_fix_rounds:
            status = "BLOCKED"
            reason = f"max_fix_rounds_exceeded ({contract.max_fix_rounds})"
            break
        fix_rounds += 1
        feedback = brief | {
            "kind": "feedback",
            "round": fix_rounds,
            "feedback": {
                "verdict": verdict.get("verdict"),
                "results": verdict.get("results", []),
                "instruction": "Fix the artifact so all acceptance checks pass.",
            },
        }
        try:
            coder_task = coder.send(feedback, task_id=coder_task.get("id"))
        except Exception as exc:
            status, reason = "BLOCKED", f"coder_transport_error_on_fix: {exc}"
            break
        artifact = _artifact_from_task(coder_task)
        if artifact is None:
            status, reason = "BLOCKED", "coder_produced_no_artifact_on_fix"
            break
        content = artifact_text(artifact)
        sha = artifact.get("metadata", {}).get("sha256") or sha256_text(content)
        evidence.log("coder_artifact", filename=artifact.get("name"),
                     sha256=sha, version=artifact.get("metadata", {}).get("version"),
                     round=fix_rounds)

    return _finish(evidence, contract, status, reason, fix_rounds, sha, verdict)


def _finish(evidence: EvidenceLog, contract: WorkContract, status: str, reason: str,
            rounds: int, sha: str | None, verdict: dict | None) -> RunReport:
    evidence.log("run_end", contract_id=contract.contract_id, status=status,
                 reason=reason, rounds=rounds, artifact_sha256=sha)
    return RunReport(
        contract_id=contract.contract_id,
        status=status,
        reason=reason,
        rounds_used=rounds,
        artifact_sha256=sha,
        verdict=verdict,
        evidence_path=str(evidence.path),
    )
