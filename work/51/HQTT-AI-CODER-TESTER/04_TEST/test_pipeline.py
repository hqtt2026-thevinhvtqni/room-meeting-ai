"""P3 pipeline scenarios (in-process; HTTP covered in test_http.py).

- happy path PASS
- seeded failure -> feedback -> fix -> PASS
- persistent failure -> BLOCKED after max_fix_rounds (no infinite loop)
- PASS without evidence -> BLOCKED (evidence gate)
- transport error -> BLOCKED with reason
"""

import json
from pathlib import Path

import pytest

from a2a_ct.a2a import LocalClient
from a2a_ct.coder_agent import CoderBackend
from a2a_ct.contract import make_demo_contract
from a2a_ct.evidence import EvidenceLog
from a2a_ct.orchestrator import run_pipeline
from a2a_ct.tester_agent import TesterBackend


@pytest.fixture()
def evidence(tmp_path: Path) -> EvidenceLog:
    return EvidenceLog(tmp_path / "evidence.jsonl")


def run(contract, evidence):
    coder = LocalClient(CoderBackend())
    tester = LocalClient(TesterBackend())
    return run_pipeline(contract, coder, tester, evidence)


def test_happy_path_pass(evidence):
    report = run(make_demo_contract(coder_mode="correct"), evidence)
    assert report.status == "PASS"
    assert report.reason == "all_acceptance_programs_passed"
    assert report.rounds_used == 0
    assert report.artifact_sha256
    assert report.verdict["verdict"] == "PASS"
    assert all(r["ok"] for r in report.verdict["results"])


def test_seeded_bug_fixed_by_feedback(evidence):
    report = run(make_demo_contract(coder_mode="seeded_bug"), evidence)
    assert report.status == "PASS"
    assert report.rounds_used == 1


def test_always_bug_blocked_after_max_rounds(evidence):
    report = run(make_demo_contract(coder_mode="always_bug"), evidence)
    assert report.status == "BLOCKED"
    assert "max_fix_rounds_exceeded" in report.reason
    assert report.rounds_used == 2          # hard cap, no infinite loop


def test_zero_fix_rounds_blocks_immediately(evidence):
    contract = make_demo_contract(coder_mode="always_bug")
    contract.max_fix_rounds = 0
    report = run(contract, evidence)
    assert report.status == "BLOCKED"
    assert report.rounds_used == 0


def test_pass_without_evidence_is_blocked(evidence):
    report = run(make_demo_contract(coder_mode="correct",
                                     tester_mode="strip_evidence"), evidence)
    assert report.status == "BLOCKED"
    assert report.reason == "pass_without_evidence"


def test_transport_error_blocks_with_reason(evidence):
    class DeadClient:
        def send(self, payload, task_id=None):
            raise ConnectionError("agent down")

    contract = make_demo_contract()
    report = run_pipeline(contract, DeadClient(), DeadClient(), evidence)
    assert report.status == "BLOCKED"
    assert "transport_error" in report.reason


def test_evidence_log_records_full_run(evidence):
    report = run(make_demo_contract(coder_mode="seeded_bug"), evidence)
    records = evidence.read_all()
    events = [r["event"] for r in records]
    assert events[0] == "run_start"
    assert "coder_task" in events
    assert events.count("coder_artifact") == 2   # initial + fix
    assert "tester_verdict" in events
    assert events[-1] == "run_end"
    end = records[-1]
    assert end["status"] == report.status == "PASS"
    assert Path(str(end.get("artifact_sha256") and report.evidence_path)).exists()


def test_verdict_is_json_and_hashed(evidence):
    report = run(make_demo_contract(coder_mode="correct"), evidence)
    assert json.dumps(report.verdict)  # verdict must be JSON-serializable
    assert report.verdict["artifact_sha256"] == report.artifact_sha256
