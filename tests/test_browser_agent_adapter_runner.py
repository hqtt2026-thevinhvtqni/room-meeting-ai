"""Unit tests for the fail-closed Windows Browser Adapter runner bootstrap."""
from __future__ import annotations

from pathlib import Path

import pytest

from room_hop_mcp.browser_agent_adapter.runner import validate_runtime_config


SHA = "a" * 40


def _fixture_env(store: Path, port: int = 49152) -> dict[str, str]:
    workspace = store.parent.parent / "workspace"
    workspace.mkdir(exist_ok=True)
    return {
        "GITHUB_SHA": SHA,
        "RUNNER_TEMP": str(store.parent),
        "GITHUB_WORKSPACE": str(workspace),
        "ROOMHOP_TEST_MODE": "1",
        "ROOMHOP_TEST_MEETINGS_DIR": str(store),
        "ROOMHOP_TEST_MEETING_ID": "MEETING-W32-123-1",
        "ROOMHOP_TEST_IDENTITY_ID": "xu",
        "ROOMHOP_BROWSER_ADAPTER_PORT": str(port),
    }


def _store(tmp_path: Path) -> Path:
    runner_temp = tmp_path / "runner-temp"
    runner_temp.mkdir()
    store = runner_temp / "disposable"
    store.mkdir()
    (store / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE",
        encoding="utf-8",
    )
    return store


def test_runner_accepts_matching_sha_store_and_dynamic_port(tmp_path):
    store = _store(tmp_path)
    resolved = validate_runtime_config(SHA, store, 49152, _fixture_env(store))
    assert resolved == store.resolve()


@pytest.mark.parametrize("port", [0, -1, 65536])
def test_runner_rejects_invalid_port(tmp_path, port):
    store = _store(tmp_path)
    with pytest.raises(ValueError, match="port must be between"):
        validate_runtime_config(SHA, store, port, _fixture_env(store, port))


def test_runner_rejects_sha_not_equal_to_exact_github_sha(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(ValueError, match="does not match GITHUB_SHA"):
        validate_runtime_config("b" * 40, store, 49152, _fixture_env(store))


def test_runner_rejects_store_without_exact_sentinel(tmp_path):
    store = tmp_path / "disposable"
    store.mkdir()
    env = _fixture_env(store)
    with pytest.raises(ValueError, match="sentinel is missing"):
        validate_runtime_config(SHA, store, 49152, env)


def test_runner_rejects_store_mismatch(tmp_path):
    store = _store(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    env = _fixture_env(other)
    with pytest.raises(ValueError, match="does not match ROOMHOP_TEST_MEETINGS_DIR"):
        validate_runtime_config(SHA, store, 49152, env)


def test_runner_rejects_port_environment_mismatch(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(ValueError, match="does not match ROOMHOP_BROWSER_ADAPTER_PORT"):
        validate_runtime_config(SHA, store, 49152, _fixture_env(store, 49153))


def test_runner_rejects_store_outside_runner_temp(tmp_path):
    store = _store(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE",
        encoding="utf-8",
    )
    env = _fixture_env(store)
    env["ROOMHOP_TEST_MEETINGS_DIR"] = str(outside)
    with pytest.raises(ValueError, match="inside RUNNER_TEMP"):
        validate_runtime_config(SHA, outside, 49152, env)


def test_runner_rejects_unapproved_identity(tmp_path):
    store = _store(tmp_path)
    env = _fixture_env(store)
    env["ROOMHOP_TEST_IDENTITY_ID"] = "identity-w32-e2e"
    with pytest.raises(ValueError, match="approved test identity"):
        validate_runtime_config(SHA, store, 49152, env)
