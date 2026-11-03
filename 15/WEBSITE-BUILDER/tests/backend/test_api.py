"""HTTP contract tests (issue #34, parts A + E).

Runs the FastAPI app in-process via TestClient — no port is opened, no
runtime is executed. Asserts status codes, the single error envelope, and
that the API surface never lets a caller claim success without evidence.
"""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from roomhop_builder.api import create_app  # noqa: E402
from roomhop_builder.evidence import EvidenceStore  # noqa: E402
from roomhop_builder.jobs import JobState  # noqa: E402
from roomhop_builder.service import BuilderService  # noqa: E402

PAYLOAD = {"intent": "landing page cafe", "site_name": "cafe-demo", "created_by": "vinh"}


@pytest.fixture()
def client() -> TestClient:
    evidence = EvidenceStore()
    service = BuilderService(evidence=evidence, code_version="git:testsha")
    return TestClient(create_app(service))


def create_job(client: TestClient) -> str:
    response = client.post("/v1/websites/jobs", json=PAYLOAD)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["state"] == "QUEUED"
    return body["id"]


# -- health -----------------------------------------------------------------


def test_health_admits_ports_are_not_wired(client):
    body = client.get("/health").json()
    assert body["builder_port"] == "null-builder"
    assert body["runtime_port"] == "refused-runtime"
    assert body["wired_for_execution"] is False


# -- validation / error envelope -------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {"intent": "", "site_name": "s", "created_by": "u"},
        {"intent": "i", "site_name": "s"},
        {"intent": "i", "site_name": "s", "created_by": "u", "cmd": "del /q C:\\\\"},
        {"intent": 42, "site_name": "s", "created_by": "u"},
    ],
)
def test_bad_create_requests_get_422_with_single_error_shape(client, bad):
    response = client.post("/v1/websites/jobs", json=bad)
    assert response.status_code == 422
    err = response.json()["error"]
    assert err["code"] == "VALIDATION_ERROR"
    assert isinstance(err["details"]["problems"], list)


def test_unknown_job_returns_404_envelope(client):
    response = client.get("/v1/websites/jobs/W15-nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "UNKNOWN_JOB"


def test_illegal_transition_returns_409_with_allowed_set(client):
    job_id = create_job(client)
    response = client.post(
        f"/v1/websites/jobs/{job_id}/transitions",
        json={"to": "SUCCEEDED", "reason": "because I say so"},
    )
    assert response.status_code == 409
    err = response.json()["error"]
    assert err["code"] in ("INVALID_TRANSITION", "EVIDENCE_MISSING")
    if err["code"] == "INVALID_TRANSITION":
        assert "RUNNING" in err["details"]["allowed"]


def test_success_transition_blocked_by_evidence_gate(client):
    job_id = create_job(client)
    assert client.post(f"/v1/websites/jobs/{job_id}/transitions",
                       json={"to": "RUNNING", "reason": "worker start"}).status_code == 200
    response = client.post(f"/v1/websites/jobs/{job_id}/transitions",
                           json={"to": "SUCCEEDED", "reason": "claims done"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "EVIDENCE_MISSING"
    assert client.get(f"/v1/websites/jobs/{job_id}").json()["state"] == "RUNNING"


def test_blank_reason_rejected(client):
    job_id = create_job(client)
    response = client.post(f"/v1/websites/jobs/{job_id}/transitions",
                           json={"to": "RUNNING", "reason": "   "})
    assert response.status_code == 422


# -- listing / filters ------------------------------------------------------


def test_list_and_state_filter(client):
    a = create_job(client)
    create_job(client)
    client.post(f"/v1/websites/jobs/{a}/transitions", json={"to": "RUNNING", "reason": "go"})
    assert client.get("/v1/websites/jobs").json()["count"] == 2
    running = client.get("/v1/websites/jobs", params={"state": "running"}).json()
    assert running["count"] == 1 and running["jobs"][0]["id"] == a
    assert client.get("/v1/websites/jobs", params={"state": "nope"}).status_code == 422


# -- evidence endpoints -----------------------------------------------------


def test_evidence_append_then_manifest(client):
    job_id = create_job(client)
    for kind in ("diff", "log", "preview", "e2e", "runtime_status"):
        r = client.post(f"/v1/websites/jobs/{job_id}/evidence",
                        json={"kind": kind, "summary": f"{kind} proof"})
        assert r.status_code == 201
        assert r.json()["code_version"] == "git:testsha"
    manifest = client.get(f"/v1/websites/jobs/{job_id}/evidence").json()
    assert manifest["complete"] is True
    # now success is legitimately reachable
    client.post(f"/v1/websites/jobs/{job_id}/transitions",
                json={"to": "RUNNING", "reason": "worker start"})
    ok = client.post(f"/v1/websites/jobs/{job_id}/transitions",
                     json={"to": "SUCCEEDED", "reason": "all five artifacts recorded"})
    assert ok.status_code == 200
    assert ok.json()["state"] == "SUCCEEDED"


def test_unknown_evidence_kind_is_422(client):
    job_id = create_job(client)
    response = client.post(f"/v1/websites/jobs/{job_id}/evidence",
                           json={"kind": "screenshot-of-success", "summary": "trust me"})
    assert response.status_code == 422


def test_evidence_on_unknown_job_is_404(client):
    response = client.post("/v1/websites/jobs/W15-missing/evidence",
                           json={"kind": "log", "summary": "x"})
    assert response.status_code == 404


# -- run orchestration over HTTP -------------------------------------------


def test_run_without_wiring_blocks_and_reports_honestly(client):
    job_id = create_job(client)
    body = client.post(f"/v1/websites/jobs/{job_id}/run", json={}).json()
    assert body["note"] == "BUILDER_NOT_WIRED"
    assert body["job"]["state"] == "BLOCKED"
    # the (empty) build result is still reported — it must show zero files
    assert body["build"]["ok"] is False and body["build"]["files"] == []
    assert body["runtime"] == {}


def test_runtime_probe_without_handle_reports_no_handle(client):
    job_id = create_job(client)
    body = client.get(f"/v1/websites/jobs/{job_id}/runtime").json()
    assert body["running"] is False
    assert body["reason"] == "NO_HANDLE"
