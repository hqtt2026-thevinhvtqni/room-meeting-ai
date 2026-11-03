"""Tests for Builder/Runtime port boundaries (issue #34, parts C + E).

Focus: the backend must fail *honestly* when nothing is wired, must never
reach an execution surface outside the allow-list, and must translate host
refusals into BLOCKED rather than success.
"""

from __future__ import annotations

import pytest

from roomhop_builder.errors import RuntimeBlockedError, RuntimeFailedError
from roomhop_builder.jobs import WebsiteJob
from roomhop_builder.ports import (
    HttpBuilderAdapter,
    HttpRuntimeAdapter,
    NullBuilderPort,
    RefusedRuntimePort,
    RuntimeStatus,
)


def sample_job() -> WebsiteJob:
    return WebsiteJob(intent="site", site_name="demo", created_by="vinh")


# -- default stubs ----------------------------------------------------------


def test_null_builder_reports_not_wired_instead_of_faking_output():
    result = NullBuilderPort().build(sample_job())
    assert result.ok is False
    assert result.files == {}
    assert result.detail["reason"] == "BUILDER_NOT_WIRED"


def test_refused_runtime_never_starts_execution():
    with pytest.raises(RuntimeBlockedError) as exc:
        RefusedRuntimePort().start(sample_job(), {"index.html": "<h1>hi</h1>"})
    assert exc.value.details["reason"] == "RUNTIME_NOT_WIRED"


def test_refused_runtime_status_is_observed_false_not_assumed_true():
    status = RefusedRuntimePort().status(handle=None)
    assert isinstance(status, RuntimeStatus)
    assert status.running is False


# -- origin allow-list ------------------------------------------------------


@pytest.mark.parametrize(
    "origin",
    [
        "http://evil.example.com",
        "http://192.168.1.50:8100",
        "http://[::1]:8100",
        "https://127.0.0.1:8100",  # scheme change not allowed either
    ],
)
def test_runtime_adapter_rejects_non_allowlisted_origins(origin):
    with pytest.raises(RuntimeBlockedError):
        HttpRuntimeAdapter(base_url=origin)


@pytest.mark.parametrize("origin", ["http://127.0.0.1:8100", "http://localhost:8100/"])
def test_runtime_adapter_accepts_loopback_origins(origin):
    adapter = HttpRuntimeAdapter(base_url=origin)
    assert adapter.base_url.rstrip("/") in HttpRuntimeAdapter.ALLOWED_ORIGINS


def test_builder_adapter_rejects_foreign_origin():
    with pytest.raises(RuntimeBlockedError):
        HttpBuilderAdapter(base_url="http://attacker.tld:8000")


# -- host refusal / transport failure translation ---------------------------


def test_runtime_start_requires_explicit_grant(monkeypatch):
    adapter = HttpRuntimeAdapter()
    monkeypatch.setattr("roomhop_builder.ports._post_json",
                        lambda url, payload, timeout: {"granted": False, "reason": "policy"})
    with pytest.raises(RuntimeBlockedError):
        adapter.start(sample_job(), {})


def test_runtime_running_flag_comes_from_host_not_from_us(monkeypatch):
    adapter = HttpRuntimeAdapter()
    monkeypatch.setattr(
        "roomhop_builder.ports._post_json",
        lambda url, payload, timeout: {"granted": True, "running": False,
                                       "preview_url": None, "handle": "H1"},
    )
    status = adapter.start(sample_job(), {})
    assert status.running is False  # granted but not yet serving -> honest False
    assert status.detail["handle"] == "H1"


def test_unreachable_host_raises_runtime_failed(monkeypatch):
    adapter = HttpRuntimeAdapter()

    def boom(url, payload, timeout):
        raise RuntimeFailedError(f"{url} unreachable: refused", details={"url": url})

    monkeypatch.setattr("roomhop_builder.ports._post_json", boom)
    with pytest.raises(RuntimeFailedError):
        adapter.start(sample_job(), {})


def test_builder_response_shape_is_validated(monkeypatch):
    adapter = HttpBuilderAdapter()
    monkeypatch.setattr("roomhop_builder.ports._post_json",
                        lambda url, payload, timeout: {"files": ["not-a-dict"], "ok": True})
    with pytest.raises(RuntimeFailedError):
        adapter.build(sample_job())


def test_builder_sends_only_contract_fields(monkeypatch):
    adapter = HttpBuilderAdapter()
    captured = {}

    def fake_post(url, payload, timeout):
        captured.update(payload)
        return {"ok": True, "files": {"index.html": "<html></html>"},
                "diff_summary": "added index.html", "log": "generated"}

    monkeypatch.setattr("roomhop_builder.ports._post_json", fake_post)
    job = sample_job()
    result = adapter.build(job)
    assert set(captured) == {"job_id", "intent", "site_name", "created_by"}
    assert result.ok and "index.html" in result.files
