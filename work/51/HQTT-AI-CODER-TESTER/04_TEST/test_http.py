"""HTTP binding end-to-end: agent card, message/send, tasks/get, error codes.

Also proves the pipeline itself works over real HTTP (not only in-process).
"""

import json
from pathlib import Path

import pytest

from a2a_ct.a2a import A2AClient, A2AServer, AgentError, TransportError
from a2a_ct.coder_agent import CoderBackend
from a2a_ct.contract import make_demo_contract
from a2a_ct.evidence import EvidenceLog
from a2a_ct.orchestrator import run_pipeline
from a2a_ct.tester_agent import TesterBackend


@pytest.fixture()
def coder_server():
    server = A2AServer(CoderBackend())
    server.start()
    yield server
    server.stop()


@pytest.fixture()
def tester_server():
    server = A2AServer(TesterBackend())
    server.start()
    yield server
    server.stop()


def test_agent_card_served(coder_server):
    client = A2AClient(coder_server.base_url)
    card = client.agent_card()
    assert card["name"] == "work51-coder-agent"
    assert card["supportedInterfaces"][0]["protocolBinding"] == "JSONRPC"
    assert card["supportedInterfaces"][0]["protocolVersion"] == "1.0"
    assert card["skills"][0]["id"] == "work51-coder"
    assert card["signatures"]


def test_message_send_returns_completed_task_with_artifact(coder_server):
    client = A2AClient(coder_server.base_url)
    task = client.send(make_demo_contract().coder_brief())
    assert task["state"] == "completed"
    assert task["artifacts"]
    artifact = task["artifacts"][0]
    assert artifact["name"] == "artifact_sum_digits.py"
    assert artifact["metadata"]["sha256"]
    assert "def sum_digits" in artifact["parts"][0]["text"]


def test_tasks_get_read_path_is_idempotent(coder_server):
    client = A2AClient(coder_server.base_url)
    task = client.send(make_demo_contract().coder_brief())
    again = client.get_task(task["id"])
    assert again == task


def test_unknown_task_raises_agent_error(coder_server):
    client = A2AClient(coder_server.base_url)
    with pytest.raises(AgentError):
        client.get_task("t-does-not-exist")


def test_malformed_payload_rejected_as_invalid_params(coder_server):
    client = A2AClient(coder_server.base_url)
    with pytest.raises(AgentError):
        client.send_raw_text("this is not json")


def test_unsupported_kind_fails_task(coder_server):
    client = A2AClient(coder_server.base_url)
    task = client.send({"kind": "bogus"})
    assert task["state"] == "failed"
    assert "unsupported" in task["status"]["message"]


def test_continuation_message_must_reference_existing_task(coder_server):
    client = A2AClient(coder_server.base_url)
    with pytest.raises(AgentError, match="unknown taskId"):
        client.send({"kind": "feedback"}, task_id="t-never-created")


def test_feedback_continues_same_task(coder_server):
    client = A2AClient(coder_server.base_url)
    brief = make_demo_contract(coder_mode="seeded_bug").coder_brief()
    first = client.send(brief)
    feedback = dict(brief)
    feedback["kind"] = "feedback"
    feedback["round"] = 1
    feedback["feedback"] = {"verdict": "FAIL", "results": [], "instruction": "fix it"}
    second = client.send(feedback, task_id=first["id"])
    assert second["id"] == first["id"]
    assert second["artifacts"][0]["metadata"]["version"] == 2


def test_unreachable_agent_raises_transport_error():
    client = A2AClient("http://127.0.0.1:1", timeout_s=2)
    with pytest.raises(TransportError):
        client.send({"kind": "brief"})


def test_full_pipeline_over_http(tmp_path: Path, coder_server, tester_server):
    coder = A2AClient(coder_server.base_url)
    tester = A2AClient(tester_server.base_url)
    evidence = EvidenceLog(tmp_path / "http_evidence.jsonl")
    report = run_pipeline(make_demo_contract(coder_mode="seeded_bug"),
                          coder, tester, evidence)
    assert report.status == "PASS"
    assert report.rounds_used == 1
    events = [r["event"] for r in evidence.read_all()]
    assert events[-1] == "run_end"

# ---- Iteration 2: tasks/cancel + binding v1.2 fields -----------------------

from a2a_ct.a2a import make_task  # noqa: E402


class _WorkingBackend(CoderBackend):
    """Stays in "working" after a brief — gives cancel something to cancel."""

    __test__ = False

    def handle_task(self, task_id: str, payload: dict, existing: dict | None) -> dict:
        if payload.get("kind") == "brief" and existing is None:
            return make_task(task_id, "working",
                             status_message="accepted, working")
        return super().handle_task(task_id, payload, existing)


@pytest.fixture()
def working_server():
    server = A2AServer(_WorkingBackend())
    server.start()
    yield server
    server.stop()


def test_cancel_working_task(working_server):
    client = A2AClient(working_server.base_url)
    task = client.send({"kind": "brief"})
    assert task["state"] == "working"
    canceled = client.cancel_task(task["id"])
    assert canceled["state"] == "canceled"
    assert canceled["status"]["state"] == "canceled"
    assert canceled["updatedAt"] >= task["updatedAt"]


def test_cancel_unknown_task_raises_agent_error(working_server):
    client = A2AClient(working_server.base_url)
    with pytest.raises(AgentError):
        client.cancel_task("t-does-not-exist")


def test_cancel_terminal_task_is_noop(coder_server):
    client = A2AClient(coder_server.base_url)
    task = client.send(make_demo_contract().coder_brief())
    assert task["state"] == "completed"
    again = client.cancel_task(task["id"])
    assert again["state"] == "completed"
    assert again["status"]["state"] == "completed"


def test_agent_card_and_task_expose_binding_v12_fields(coder_server):
    client = A2AClient(coder_server.base_url)
    card = client.agent_card()
    assert card["protocolVersion"] == "1.0"
    assert card["version"] == "1.2.0"
    assert card["preferredTransport"] == "JSONRPC"
    task = client.send(make_demo_contract().coder_brief())
    assert task["contextId"]
    assert task["createdAt"] and task["updatedAt"]
    assert task["status"]["timestamp"]
