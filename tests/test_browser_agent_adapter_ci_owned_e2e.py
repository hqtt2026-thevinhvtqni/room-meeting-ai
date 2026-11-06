"""CI-owned Browser Adapter E2E with a private fixture and disposable ROOM HOP store.

The test starts the adapter as a child of pytest on a dynamically allocated
127.0.0.1 port. It never attaches to a pre-existing service or uses port 8787.
"""
from __future__ import annotations

import asyncio
import functools
import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psutil
import pytest
import requests

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from integration.room_hop_integration import (
    RoomHopIntegration,
    RoomHopIntegrationConfig,
)


def _source_sha(repo_root: Path) -> str:
    supplied = os.environ.get("GITHUB_SHA")
    if supplied:
        assert len(supplied) == 40 and all(c in "0123456789abcdef" for c in supplied.lower())
        actual = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip()
        assert actual == supplied, f"checkout SHA {actual} != triggering SHA {supplied}"
        return supplied
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
    ).strip()


def _assert_ci_owned_listener(pid: int, port: int, source_sha: str) -> None:
    process = psutil.Process(pid)
    assert process.is_running()
    assert process.ppid() == os.getpid(), (
        f"adapter parent PID {process.ppid()} != CI test PID {os.getpid()}"
    )
    assert os.path.normcase(process.exe()) == os.path.normcase(sys.executable)
    command_line = " ".join(process.cmdline())
    assert source_sha in command_line, "adapter command line does not attest exact source SHA"
    assert process.environ().get("ROOMHOP_CI_SOURCE_SHA") == source_sha
    listeners = [
        connection
        for connection in process.net_connections(kind="tcp")
        if connection.status == psutil.CONN_LISTEN
        and connection.laddr
        and connection.laddr.ip == "127.0.0.1"
        and connection.laddr.port == port
    ]
    assert len(listeners) == 1, (
        f"CI-owned adapter PID {pid} does not own exactly one loopback listener on {port}"
    )


@pytest.fixture()
def ci_owned_browser_adapter(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    source_sha = _source_sha(repo_root)

    workspace = Path(os.environ.get("GITHUB_WORKSPACE", repo_root)).resolve()
    meetings_dir = (tmp_path / "disposable-meetings").resolve()
    assert not str(meetings_dir).casefold().startswith(str(workspace).casefold()), (
        "disposable meeting store must be outside GITHUB_WORKSPACE"
    )
    meetings_dir.mkdir(parents=True)
    (meetings_dir / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE", encoding="utf-8"
    )

    meeting_id = "CI-BROWSER-OWNED-001"
    manager = MeetingManager(meetings_dir=meetings_dir)
    service = MeetingService(manager)
    service.create_meeting(
        meeting_id=meeting_id,
        topic="Work 32 CI-owned Browser Adapter E2E",
        participants=["xu"],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, "xu")
    service.start_meeting(meeting_id, "vinh")

    fixture_dir = tmp_path / "html-fixture"
    fixture_dir.mkdir()
    fixture_marker = "W32-INTERNAL-HTML-FIXTURE-ONLY"
    (fixture_dir / "index.html").write_text(
        "<!doctype html><html><head><title>ROOM HOP CI Fixture</title></head>"
        "<body><h1>Work 32 local browser fixture</h1>"
        f'<p id="fixture-marker">{fixture_marker}</p></body></html>',
        encoding="utf-8",
    )
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(fixture_dir))
    fixture_server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    fixture_server.daemon_threads = True
    fixture_thread = threading.Thread(target=fixture_server.serve_forever, daemon=True)
    fixture_thread.start()
    fixture_url = f"http://127.0.0.1:{fixture_server.server_address[1]}/index.html"

    ready_file = tmp_path / "adapter-port.txt"
    process_log = (tmp_path / "adapter-process.log").open("w", encoding="utf-8")
    launcher = (
        "import socket,sys,uvicorn; "
        "from room_hop_mcp.browser_agent_adapter.adapter import app; "
        "source_sha=sys.argv[2]; "
        "sock=socket.socket(); "
        "sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); "
        "sock.bind(('127.0.0.1',0)); sock.listen(128); "
        "open(sys.argv[1],'w',encoding='utf-8').write(str(sock.getsockname()[1])); "
        "uvicorn.run(app,sockets=[sock],log_level='warning')"
    )
    child_env = os.environ.copy()
    child_env.update(
        {
            "PYTHONPATH": str(repo_root),
            "ROOMHOP_TEST_MODE": "1",
            "ROOMHOP_TEST_MEETINGS_DIR": str(meetings_dir),
            "ROOMHOP_TEST_MEETING_ID": meeting_id,
            "ROOMHOP_TEST_IDENTITY_ID": "xu",
            "ROOMHOP_CI_SOURCE_SHA": source_sha,
        }
    )
    process = subprocess.Popen(
        [sys.executable, "-c", launcher, str(ready_file), source_sha],
        cwd=repo_root,
        env=child_env,
        stdout=process_log,
        stderr=subprocess.STDOUT,
    )

    base_url = None
    try:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise AssertionError(
                    f"CI-owned adapter exited early ({process.returncode}); "
                    f"log: {Path(process_log.name).read_text(encoding='utf-8')}"
                )
            if ready_file.is_file():
                raw_port = ready_file.read_text(encoding="utf-8").strip()
                if raw_port:
                    port = int(raw_port)
                    if port != 8787:
                        candidate = f"http://127.0.0.1:{port}"
                        try:
                            health = requests.get(candidate + "/health", timeout=0.5)
                            if health.ok and health.json().get("ok") is True:
                                base_url = candidate
                                break
                        except requests.RequestException:
                            pass
            time.sleep(0.1)
        assert base_url is not None, "CI-owned Browser Adapter did not become healthy"
        port = int(base_url.rsplit(":", 1)[1])
        _assert_ci_owned_listener(process.pid, port, source_sha)

        yield {
            "base_url": base_url,
            "fixture_url": fixture_url,
            "fixture_marker": fixture_marker,
            "meetings_dir": meetings_dir,
            "meeting_id": meeting_id,
            "source_sha": source_sha,
            "process": process,
            "repo_root": repo_root,
        }
    finally:
        if process.poll() is None:
            try:
                requests.post(process_base_url(ready_file), timeout=2)
            except Exception:
                pass
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        fixture_server.shutdown()
        fixture_server.server_close()
        fixture_thread.join(timeout=5)
        process_log.close()


def process_base_url(ready_file: Path) -> str:
    if not ready_file.is_file():
        return "http://127.0.0.1:1"
    try:
        return f"http://127.0.0.1:{int(ready_file.read_text(encoding='utf-8').strip())}/browser/close"
    except (ValueError, OSError):
        return "http://127.0.0.1:1/browser/close"


def test_ci_owned_browser_fixture_and_mcp_transcript_readback(ci_owned_browser_adapter):
    runtime = ci_owned_browser_adapter
    response = requests.post(
        runtime["base_url"] + "/browser/execute_workflow",
        json={
            "url": runtime["fixture_url"],
            "work_id": "w32-ci-owned-browser",
            "collect_screenshot": False,
            "steps": [
                {"op": "inspect"},
                {
                    "op": "extract",
                    "selectors": {
                        "headline": "h1",
                        "fixture_marker": "#fixture-marker",
                    },
                },
            ],
        },
        timeout=60,
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["ok"] is True
    assert result["final_url"] == runtime["fixture_url"]
    assert result["page_title"] == "ROOM HOP CI Fixture"
    assert result["results"][1]["fixture_marker"] == [runtime["fixture_marker"]]

    submission = result["roomhop_submission"]
    assert submission["status"] == "pass", submission
    assert submission["read_back"] is True
    assert submission["transport"] == "stdio"
    assert submission["meeting_id"] == runtime["meeting_id"]
    assert submission["identity_id"] == "xu"
    assert Path(result["evidence_json"]).is_file()

    artifact = submission["artifact"]
    marker = "ROOMHOP_BROWSER_AGENT_ARTIFACT " + json.dumps(
        artifact, ensure_ascii=False, sort_keys=True
    )
    integration = RoomHopIntegration(
        RoomHopIntegrationConfig(
            cwd=str(runtime["repo_root"]),
            env={
                "ROOM_HOP_MEETINGS_DIR": str(runtime["meetings_dir"]),
                "PYTHONPATH": str(runtime["repo_root"]),
            },
        )
    )

    async def read_back_transcript():
        async with integration.session() as session:
            return await integration.get_transcript(session, runtime["meeting_id"])

    transcript = asyncio.run(read_back_transcript())
    transcript_text = json.dumps(transcript, ensure_ascii=False, sort_keys=True)
    assert marker in transcript_text
    assert result["execution_id"] in transcript_text
    assert result["evidence_id"] in transcript_text
    assert runtime["source_sha"] == os.environ.get("GITHUB_SHA", runtime["source_sha"])
