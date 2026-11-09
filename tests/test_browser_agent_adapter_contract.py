import asyncio
import importlib
import inspect
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import types
import pytest
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from integration import room_hop_integration as integration_module
from integration.room_hop_integration import RoomHopIntegration, RoomHopIntegrationConfig

try:
    from room_hop_mcp.browser_agent_adapter import adapter as browser_adapter
except ModuleNotFoundError as exc:
    if exc.name != "playwright":
        raise
    playwright = types.ModuleType("playwright")
    sync_api = types.ModuleType("playwright.sync_api")
    sync_api.sync_playwright = lambda: None
    sync_api.Browser = type("Browser", (), {})
    sync_api.Page = type("Page", (), {})
    playwright.sync_api = sync_api
    sys.modules["playwright"] = playwright
    sys.modules["playwright.sync_api"] = sync_api
    browser_adapter = importlib.import_module("room_hop_mcp.browser_agent_adapter.adapter")


EXPECTED_TOOLS = {
    "list_meetings",
    "get_meeting",
    "get_transcript",
    "add_paste_to_meeting",
}
RESULT = {
    "execution_id": "exec-test-001",
    "evidence_id": "evidence-test-001",
    "work_id": "work-32-test",
    "evidence_json": "/tmp/workflow-evidence.json",
    "final_url": "https://example.com/",
    "page_title": "Example Domain",
}


class FakeIntegration:
    def __init__(self, config, *, tools=None, meetings=None, meeting=None):
        self.config = config
        self.tools = EXPECTED_TOOLS if tools is None else set(tools)
        self.meetings = (
            [{"id": "MEETING-W32-DISPOSABLE", "status": "active"}]
            if meetings is None else meetings
        )
        self.meeting = (
            {"id": "MEETING-W32-DISPOSABLE", "status": "active"}
            if meeting is None else meeting
        )
        self.transcript = []
        self.calls = []
        self.session_opened = False
        self.session_closed = False

    @asynccontextmanager
    async def session(self):
        self.session_opened = True
        try:
            yield SimpleNamespace(
                list_tools=lambda: self._list_tools()
            )
        finally:
            self.session_closed = True

    async def _list_tools(self):
        return SimpleNamespace(
            tools=[SimpleNamespace(name=name) for name in sorted(self.tools)]
        )

    async def list_meetings(self, session):
        self.calls.append(("list_meetings", None))
        return self.meetings

    async def get_meeting(self, session, meeting_id):
        self.calls.append(("get_meeting", meeting_id))
        return self.meeting

    async def add_paste_to_meeting(self, session, meeting_id, text, identity_id=None):
        self.calls.append(("add_paste_to_meeting", meeting_id, identity_id))
        self.transcript.append({"content": text, "speaker": identity_id})
        return {"status": "READY"}

    async def get_transcript(self, session, meeting_id):
        self.calls.append(("get_transcript", meeting_id))
        return self.transcript


def _configure_test_target(monkeypatch, tmp_path):
    meetings_dir = tmp_path / "disposable-meetings"
    meetings_dir.mkdir()
    (meetings_dir / ".roomhop-disposable-test-store").write_text(
        "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE", encoding="utf-8"
    )
    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_TEST_MEETING_ID", "MEETING-W32-DISPOSABLE")
    monkeypatch.setenv("ROOMHOP_TEST_IDENTITY_ID", "identity-w32-e2e")
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(meetings_dir))
    return meetings_dir


def _install_fake(monkeypatch, **kwargs):
    instances = []

    def factory(config):
        instance = FakeIntegration(config, **kwargs)
        instances.append(instance)
        return instance

    monkeypatch.setattr(browser_adapter, "RoomHopIntegration", factory)
    return instances


def test_submission_is_blocked_without_explicit_test_mode(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.delenv("ROOMHOP_TEST_MODE")
    monkeypatch.setattr(
        browser_adapter,
        "RoomHopIntegration",
        lambda config: (_ for _ in ()).throw(AssertionError("must not start MCP")),
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_MODE=1" in result["reason"]


def test_submission_requires_explicit_disposable_store_and_identity(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.delenv("ROOMHOP_TEST_MEETINGS_DIR")
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "ROOMHOP_TEST_MEETINGS_DIR" in result["reason"]


def test_submission_rejects_nonexistent_disposable_store(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    missing = tmp_path / "missing-store"
    monkeypatch.setenv("ROOMHOP_TEST_MEETINGS_DIR", str(missing))
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "does not exist" in result["reason"]


def test_submission_rejects_store_without_disposable_sentinel(monkeypatch, tmp_path):
    meetings_dir = _configure_test_target(monkeypatch, tmp_path)
    (meetings_dir / ".roomhop-disposable-test-store").unlink()
    instances = _install_fake(monkeypatch)
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "marker is missing or invalid" in result["reason"]
    assert instances == []


def test_submission_rejects_extra_or_missing_public_tools(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(monkeypatch, tools=EXPECTED_TOOLS | {"join_meeting"})
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert result["expected_tools"] == sorted(EXPECTED_TOOLS)
    assert "join_meeting" in result["actual_tools"]
    assert instances[0].calls == []
    assert instances[0].session_closed is True


def test_submission_does_not_fall_back_when_explicit_test_meeting_missing(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(
        monkeypatch,
        meetings=[{"id": "REAL-MEETING", "status": "active"}],
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "no fallback" in result["reason"]
    assert instances[0].calls == [("list_meetings", None)]
    assert instances[0].session_closed is True


def test_submission_rejects_inactive_disposable_meeting(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(
        monkeypatch,
        meeting={"id": "MEETING-W32-DISPOSABLE", "status": "closed"},
    )
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "not active" in result["reason"]
    assert [call[0] for call in instances[0].calls] == [
        "list_meetings", "get_meeting"
    ]
    assert instances[0].session_closed is True


def test_submission_timeout_is_blocked_and_never_retried(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.setenv("ROOMHOP_MCP_TIMEOUT_SECONDS", "0.01")

    async def slow_submission(*args, **kwargs):
        await asyncio.sleep(0.1)
        return {"status": "pass"}

    monkeypatch.setattr(browser_adapter, "_submit_to_roomhop_stdio", slow_submission)
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "blocked"
    assert "outcome is uncertain" in result["reason"]
    assert "do not retry automatically" in result["reason"]


def test_submission_fails_closed_inside_running_event_loop(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)

    def must_not_start(*args, **kwargs):
        raise AssertionError("coroutine must not be created in a running loop")

    monkeypatch.setattr(browser_adapter, "_submit_to_roomhop_stdio", must_not_start)

    async def invoke():
        return browser_adapter.submit_to_roomhop(RESULT)

    result = asyncio.run(invoke())
    assert result["status"] == "blocked"
    assert "Nested event loops are not allowed" in result["reason"]



def test_browser_submission_worker_has_no_inherited_playwright_event_loop(monkeypatch):
    observed = {}

    def fake_submit(result):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            observed["running_loop"] = False
        else:
            observed["running_loop"] = True
        observed["result"] = result
        return {"status": "pass"}

    monkeypatch.setattr(browser_adapter, "submit_to_roomhop", fake_submit)

    async def invoke_from_playwright_loop():
        return browser_adapter._submit_to_roomhop_from_worker(RESULT)

    result = asyncio.run(invoke_from_playwright_loop())
    assert result == {"status": "pass"}
    assert observed == {"running_loop": False, "result": RESULT}


def test_stdio_session_preserves_cancellation_and_unwinds(monkeypatch):
    lifecycle = {"stdio_closed": False, "session_closed": False}

    @asynccontextmanager
    async def fake_stdio_client(params):
        try:
            yield object(), object()
        finally:
            lifecycle["stdio_closed"] = True

    class FakeClientSession:
        def __init__(self, read, write):
            self.read = read
            self.write = write

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            lifecycle["session_closed"] = True

        async def initialize(self):
            return None

    monkeypatch.setattr(integration_module, "stdio_client", fake_stdio_client)
    monkeypatch.setattr(integration_module, "ClientSession", FakeClientSession)
    integration = RoomHopIntegration(RoomHopIntegrationConfig())

    async def blocked_session():
        async with integration.session():
            await asyncio.sleep(5)

    async def exercise_timeout():
        try:
            await asyncio.wait_for(blocked_session(), timeout=0.01)
        except asyncio.TimeoutError:
            return
        raise AssertionError("session timeout was not propagated")

    asyncio.run(exercise_timeout())
    assert lifecycle == {"stdio_closed": True, "session_closed": True}


def test_submission_uses_exact_target_stdio_and_verifies_readback(monkeypatch, tmp_path):
    meetings_dir = _configure_test_target(monkeypatch, tmp_path)
    monkeypatch.setenv("ROOMHOP_PRIVATE_TEST_VALUE", "must-not-forward")
    instances = _install_fake(monkeypatch)
    result = browser_adapter.submit_to_roomhop(RESULT)

    assert result["status"] == "pass"
    assert result["read_back"] is True
    assert result["transport"] == "stdio"
    assert result["meeting_id"] == "MEETING-W32-DISPOSABLE"
    assert result["identity_id"] == "identity-w32-e2e"
    assert result["meetings_dir"] == str(meetings_dir.resolve())
    assert instances[0].session_opened is True
    assert instances[0].session_closed is True
    assert instances[0].config.cwd == str(Path(browser_adapter.__file__).resolve().parents[2])
    repo_root = str(Path(browser_adapter.__file__).resolve().parents[2])
    assert instances[0].config.python_args == [
        "-c",
        "import sys, runpy; "
        f"sys.path.insert(0, {repo_root!r}); "
        "runpy.run_module('room_hop_mcp', run_name='__main__')",
    ]
    assert instances[0].config.env["ROOM_HOP_MEETINGS_DIR"] == str(meetings_dir.resolve())
    assert instances[0].config.env == {
        "ROOM_HOP_MEETINGS_DIR": str(meetings_dir.resolve()),
        "PYTHONPATH": str(Path(browser_adapter.__file__).resolve().parents[2]),
    }
    assert "ROOMHOP_PRIVATE_TEST_VALUE" not in instances[0].config.env
    assert [call[0] for call in instances[0].calls] == [
        "list_meetings",
        "get_meeting",
        "add_paste_to_meeting",
        "get_transcript",
    ]
    assert instances[0].calls[2] == (
        "add_paste_to_meeting",
        "MEETING-W32-DISPOSABLE",
        "identity-w32-e2e",
    )



def test_adapter_workflows_are_serialized_and_keep_request_scoped_logs(monkeypatch, tmp_path):
    monkeypatch.setattr(browser_adapter, "EVIDENCE", tmp_path)
    instance = browser_adapter.Adapter()
    state = {"active": 0, "max_active": 0}
    state_lock = threading.Lock()
    instance.page = SimpleNamespace(url="", title=lambda: "serialized test")

    def fake_start():
        with state_lock:
            state["active"] += 1
            state["max_active"] = max(state["max_active"], state["active"])
        instance.started_at = time.time()
        instance.logs.append({"event": "start"})
        return {"status": "started"}

    def fake_navigate(url):
        time.sleep(0.04)
        instance.page.url = url
        instance.logs.append({"event": "navigate", "url": url})
        return {"url": url, "status": 200, "title": "serialized test"}

    def fake_submit(result):
        with state_lock:
            state["active"] -= 1
        return {"status": "pass"}

    monkeypatch.setattr(instance, "start", fake_start)
    monkeypatch.setattr(instance, "navigate", fake_navigate)
    monkeypatch.setattr(browser_adapter, "_submit_to_roomhop_from_worker", fake_submit)

    requests = [
        browser_adapter.WorkflowRequest(url="https://one.example/", work_id="parallel-one"),
        browser_adapter.WorkflowRequest(url="https://two.example/", work_id="parallel-two"),
    ]
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(instance.workflow, requests))

    assert state["max_active"] == 1
    assert state["active"] == 0
    by_url = {result["final_url"]: result for result in results}
    assert set(by_url) == {"https://one.example/", "https://two.example/"}
    assert by_url["https://one.example/"]["logs"] == [
        {"event": "start"},
        {"event": "navigate", "url": "https://one.example/"},
    ]
    assert by_url["https://two.example/"]["logs"] == [
        {"event": "start"},
        {"event": "navigate", "url": "https://two.example/"},
    ]



def test_browser_adapter_dispatch_uses_one_playwright_owner_thread():
    def read_thread_id():
        return threading.get_ident()

    with ThreadPoolExecutor(max_workers=4) as callers:
        thread_ids = list(
            callers.map(
                lambda _index: browser_adapter._run_browser_operation(read_thread_id),
                range(12),
            )
        )

    assert len(set(thread_ids)) == 1


def test_browser_evidence_redacts_url_query_and_fragment():
    assert browser_adapter._redact_url(
        "https://example.test/path?access_token=secret&x=1#private"
    ) == "https://example.test/path"


def test_browser_navigation_rejects_non_http_scheme():
    with pytest.raises(ValueError, match="http/https"):
        browser_adapter._validate_navigation_url("file:///etc/passwd")


def test_browser_navigation_blocks_private_destination(monkeypatch):
    monkeypatch.setattr(
        browser_adapter.socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(None, None, None, None, ("127.0.0.1", 0))],
    )
    with pytest.raises(ValueError, match="non-public"):
        browser_adapter._validate_navigation_url("http://internal.example/")


def test_browser_navigation_allows_explicit_loopback_test_host(monkeypatch):
    monkeypatch.setenv("ROOMHOP_TEST_MODE", "1")
    monkeypatch.setenv("ROOMHOP_BROWSER_ALLOWED_HOSTS", "127.0.0.1")
    browser_adapter._validate_navigation_url("http://127.0.0.1:8080/")


@pytest.mark.parametrize("name", ["../escape.txt", "/tmp/escape.txt", "subdir/file.txt", ".."])
def test_browser_evidence_path_rejects_traversal(name):
    with pytest.raises(ValueError):
        browser_adapter._safe_evidence_path(name)


def test_browser_evidence_path_is_confined():
    path = browser_adapter._safe_evidence_path("evidence.json")
    assert path.parent == browser_adapter.EVIDENCE.resolve()


@pytest.mark.parametrize("name", ["bad:name.png", "bad?.png", "trailing.", "CON", "nul.txt", "COM1.log", "LPT9", "AUX.data"])
def test_browser_evidence_path_rejects_platform_unsafe_names(name):
    with pytest.raises(ValueError):
        browser_adapter._safe_evidence_path(name)


def test_browser_chromium_launch_does_not_disable_sandbox():
    source = inspect.getsource(browser_adapter.Adapter.start)
    assert "--no-sandbox" not in source


def test_browser_request_guard_aborts_private_redirect_target(monkeypatch):
    calls = []
    monkeypatch.setattr(
        browser_adapter.socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(None, None, None, None, ("10.0.0.8", 0))],
    )
    route = SimpleNamespace(
        request=SimpleNamespace(url="https://internal.example/redirected"),
        abort=lambda: calls.append("abort"),
        continue_=lambda: calls.append("continue"),
    )

    browser_adapter.Adapter._guard_route(route)
    assert calls == ["abort"]


def test_browser_context_blocks_service_workers():
    captured = {}

    class FakeContext:
        def route(self, pattern, handler):
            captured["route"] = (pattern, handler)

        def new_page(self):
            return SimpleNamespace(url="about:blank")

    class FakeBrowser:
        def new_context(self, **kwargs):
            captured["kwargs"] = kwargs
            return FakeContext()

    instance = browser_adapter.Adapter()
    instance.browser = FakeBrowser()
    instance._create_context()
    assert captured["kwargs"]["service_workers"] == "block"
    assert instance.page is not None


def test_browser_wait_rejects_unbounded_or_invalid_values():
    instance = browser_adapter.Adapter()
    for value in (-1, browser_adapter.MAX_BROWSER_WAIT_MS + 1, "100", True):
        with pytest.raises(ValueError, match="wait ms must be an integer"):
            instance.wait(value)


def test_browser_workflow_rejects_excessive_step_count():
    with pytest.raises(Exception):
        browser_adapter.WorkflowRequest(
            url="https://example.com/",
            steps=[{"op": "wait"}] * (browser_adapter.MAX_BROWSER_WORKFLOW_STEPS + 1),
        )


def test_browser_operation_executor_has_a_bounded_wait(monkeypatch):
    class TimedOutFuture:
        def result(self, timeout=None):
            assert timeout == browser_adapter.BROWSER_OPERATION_TIMEOUT_SECONDS
            raise TimeoutError()

        def cancel(self):
            return False

    monkeypatch.setattr(
        browser_adapter._BROWSER_EXECUTOR,
        "submit",
        lambda *args, **kwargs: TimedOutFuture(),
    )
    with pytest.raises(Exception) as exc:
        browser_adapter._run_browser_operation(lambda: None)
    assert getattr(exc.value, "status_code", None) == 504


def test_roomhop_transcript_submission_omits_untrusted_page_title(monkeypatch, tmp_path):
    _configure_test_target(monkeypatch, tmp_path)
    instances = _install_fake(monkeypatch)
    result = browser_adapter.submit_to_roomhop(RESULT)
    assert result["status"] == "pass"
    assert len(instances[0].transcript) == 1
    marker = instances[0].transcript[0]["content"]
    assert "page_title" not in marker
    assert "Example Domain" not in marker
