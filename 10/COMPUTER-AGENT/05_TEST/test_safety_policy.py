"""
Work 10 — Safety Policy negative tests (Gate 1)

Every test here proves a dangerous workflow is actually REFUSED by the runtime,
not merely documented. SAFETY_POLICY.md is LOCKED; these tests are its
executable contract.
"""
import os
import sys
import time
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04_CODE"))

from agent_runtime import AgentRuntime
from browser_adapter import PlaywrightBrowserAdapter
from models import Action, SafetyPolicy
from test_fake_adapter import FakeAdapter

VERIFY = {"checks": [{"field": "text", "contains": "SUBMITTED"}]}
FAILED = []
SKIPPED = []


def check(name, fn):
    try:
        outcome = fn()
        if outcome is False:
            raise AssertionError("check returned False")
        print(f"  PASS  {name}")
    except Exception as exc:  # noqa: BLE001
        FAILED.append(f"{name}: {exc}")
        print(f"  FAIL  {name}: {exc}")


def blocked_with(result, rule):
    assert result.status == "BLOCKED", f"expected BLOCKED, got {result.status}"
    assert rule in (result.error or ""), f"expected rule {rule!r}, got {result.error!r}"


def test_unknown_action_blocked():
    print("\n=== SAFETY 1: unknown action ===")
    adapter = FakeAdapter()
    fake = types.SimpleNamespace(type="fly_to_moon", target=None, value=None, args={},
                                 destructive=False)
    result = AgentRuntime(adapter).execute("t", [fake], verification=VERIFY)
    check("unknown action -> BLOCKED", lambda: blocked_with(result, "unknown_action"))
    check("browser never started for a rejected workflow",
          lambda: "start" not in adapter.calls)


def test_destructive_requires_allow():
    print("\n=== SAFETY 2: destructive actions (§4) ===")
    adapter = FakeAdapter()
    result = AgentRuntime(adapter).execute(
        "download evidence", [Action("download", target="Download evidence"), Action("observe")],
        verification=VERIFY)
    check("download without allow -> BLOCKED",
          lambda: blocked_with(result, "destructive_not_allowed"))
    check("no adapter call when destructive refused", lambda: adapter.calls == [])

    allowed = FakeAdapter()
    ok = AgentRuntime(allowed, policy=SafetyPolicy(allow_destructive=True)).execute(
        "download evidence", [Action("download", target="Download evidence"), Action("observe")],
        verification=VERIFY)
    check("download with explicit allow -> PASS", lambda: ok.status == "PASS")

    flagged = FakeAdapter()
    marked = AgentRuntime(flagged).execute(
        "delete file", [Action("click", target="Delete", destructive=True)],
        verification=VERIFY)
    check("action marked destructive -> BLOCKED",
          lambda: blocked_with(marked, "destructive_not_allowed"))


def test_boundary_path():
    print("\n=== SAFETY 3: artifact boundary (§5) ===")
    outside = AgentRuntime(FakeAdapter()).execute(
        "shot", [Action("screenshot", args={"path": "/tmp/evil.png"})], verification=VERIFY)
    check("screenshot outside Work boundary -> BLOCKED",
          lambda: blocked_with(outside, "boundary_path"))

    inside = AgentRuntime(FakeAdapter()).execute(
        "shot", [Action("screenshot", args={"path": "06_EVIDENCE/real.png"}), Action("observe")],
        verification=VERIFY)
    check("screenshot inside 06_EVIDENCE -> PASS", lambda: inside.status == "PASS")

    bare = AgentRuntime(FakeAdapter()).execute(
        "shot", [Action("screenshot", args={"path": "bare.png"}), Action("observe")],
        verification=VERIFY)
    check("bare screenshot filename defaults into Evidence -> PASS",
          lambda: bare.status == "PASS")

    root = AgentRuntime(FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))).execute(
        "shot", [Action("screenshot", args={"path": str(ROOT / "06_EVIDENCE" / "a.png")}), Action("observe")],
        verification=VERIFY)
    check("absolute path inside work_root -> PASS", lambda: root.status == "PASS")

    escape = AgentRuntime(FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))).execute(
        "shot", [Action("screenshot", args={"path": str(ROOT.parent / "escape.png")})],
        verification=VERIFY)
    check("path escaping work_root -> BLOCKED",
          lambda: blocked_with(escape, "boundary_path"))

    traversal = AgentRuntime(FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))).execute(
        "shot", [Action("screenshot", args={"path": "06_EVIDENCE/../../outside.png"})],
        verification=VERIFY)
    check("parent traversal from Evidence -> BLOCKED",
          lambda: blocked_with(traversal, "boundary_path"))

    lookalike = AgentRuntime(FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))).execute(
        "shot", [Action("screenshot", args={"path": "not-06_EVIDENCE/evil.png"})],
        verification=VERIFY)
    check("look-alike Evidence path prefix -> BLOCKED",
          lambda: blocked_with(lookalike, "boundary_path"))

    if os.name == "nt":
        windows_runtime = AgentRuntime(
            FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))
        )
        check("Windows drive path outside Work root -> rejected",
              lambda: not windows_runtime._path_allowed(r"C:\outside.png"))
        check("Windows UNC path outside Work root -> rejected",
              lambda: not windows_runtime._path_allowed(r"\\server\share\outside.png"))
        check("Windows backslash traversal -> rejected",
              lambda: not windows_runtime._path_allowed(r"06_EVIDENCE\..\..\outside.png"))
    else:
        SKIPPED.extend([
            "Windows drive path test requires Windows",
            "Windows UNC path test requires Windows",
            "Windows backslash traversal test requires Windows",
        ])
        print("  SKIP  Windows drive/UNC/backslash path tests require Windows")

    link = ROOT / "06_EVIDENCE" / "_w10_symlink_escape"
    try:
        link.unlink(missing_ok=True)
    except OSError:
        pass
    try:
        link.symlink_to(ROOT.parent, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        SKIPPED.append(f"symlink escape test unavailable: {type(exc).__name__}")
        print(f"  SKIP  symlink escape test unavailable: {type(exc).__name__}")
    else:
        try:
            symlink_escape = AgentRuntime(
                FakeAdapter(), policy=SafetyPolicy(work_root=str(ROOT))
            ).execute("shot", [Action("screenshot",
                args={"path": str(link / "outside.png")})], verification=VERIFY)
            check("symlink escape from Evidence -> BLOCKED",
                  lambda: blocked_with(symlink_escape, "boundary_path"))
        finally:
            link.unlink(missing_ok=True)


def test_adapter_screenshot_path_boundary():
    print("\\n=== SAFETY 3B: adapter write-time screenshot containment ===")
    adapter = PlaywrightBrowserAdapter(headless=True)
    inside = adapter._evidence_path("06_EVIDENCE/adapter-test.png")
    check("adapter resolves Work-relative Evidence path",
          lambda: inside == (ROOT / "06_EVIDENCE" / "adapter-test.png").resolve())
    bare = adapter._evidence_path("adapter-bare.png")
    check("adapter resolves bare filename inside Evidence",
          lambda: bare == (ROOT / "06_EVIDENCE" / "adapter-bare.png").resolve())

    rejected = []
    for candidate in (
        str(ROOT.parent / "outside.png"),
        "06_EVIDENCE/../../outside.png",
        "not-06_EVIDENCE/evil.png",
    ):
        try:
            adapter._evidence_path(candidate)
        except ValueError:
            rejected.append(candidate)
    check("adapter rejects absolute, traversal and look-alike escapes",
          lambda: len(rejected) == 3)

    if os.name == "nt":
        direct_windows_rejected = []
        for candidate in (
            r"C:\outside.png",
            r"\\server\share\outside.png",
            r"06_EVIDENCE\..\..\outside.png",
        ):
            try:
                adapter._evidence_path(candidate)
            except ValueError:
                direct_windows_rejected.append(candidate)
        check("adapter rejects Windows drive, UNC and backslash traversal",
              lambda: len(direct_windows_rejected) == 3)

    adapter_link = ROOT / "06_EVIDENCE" / "_w10_adapter_symlink_escape"
    try:
        adapter_link.unlink(missing_ok=True)
        adapter_link.symlink_to(ROOT.parent, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        SKIPPED.append(f"direct-adapter symlink test unavailable: {type(exc).__name__}")
        print(f"  SKIP  direct-adapter symlink test unavailable: {type(exc).__name__}")
    else:
        try:
            direct_link_rejected = False
            try:
                adapter._evidence_path(str(adapter_link / "escape.png"))
            except ValueError:
                direct_link_rejected = True
            check("adapter rejects symlink/junction escape",
                  lambda: direct_link_rejected)
        finally:
            adapter_link.unlink(missing_ok=True)

    downloaded = adapter._download_destination("../../payload.txt")
    check("download filename traversal is reduced to a safe Evidence basename",
          lambda: downloaded.parent == (ROOT / "06_EVIDENCE").resolve()
          and downloaded.name.endswith("_payload.txt"))
    bad_name_rejected = False
    try:
        adapter._download_destination("bad:stream.txt")
    except ValueError:
        bad_name_rejected = True
    check("download filename alternate-stream syntax rejected",
          lambda: bad_name_rejected)


def test_boundary_domain():
    print("\n=== SAFETY 4: domain boundary (§5) ===")
    policy = SafetyPolicy(allowed_domains=("127.0.0.1", "localhost"))
    bad = AgentRuntime(FakeAdapter(), policy=policy).execute(
        "go", [Action("navigate", value="https://evil.test/x")], verification=VERIFY)
    check("navigate outside allowed domains -> BLOCKED",
          lambda: blocked_with(bad, "boundary_domain"))

    good = AgentRuntime(FakeAdapter(), policy=policy).execute(
        "go", [Action("navigate", value="http://127.0.0.1:8080/x")], verification=VERIFY)
    check("navigate inside allowed domains -> PASS", lambda: good.status == "PASS")


def test_wait_limit():
    print("\n=== SAFETY 5: wait limit (§3) ===")
    adapter = FakeAdapter()
    result = AgentRuntime(adapter).execute(
        "wait", [Action("wait", value=500)], verification=VERIFY)
    check("wait over 120 s -> BLOCKED", lambda: blocked_with(result, "wait_timeout_exceeded"))
    check("over-long wait never reaches the adapter", lambda: adapter.calls == [])


def test_action_timeout():
    print("\n=== SAFETY 6: action timeout is enforced, not just configured ===")

    class SlowAdapter(FakeAdapter):
        def observe(self):
            time.sleep(0.25)
            return {"url": "http://127.0.0.1/fake", "text": "SUBMITTED"}

    sleeps = []
    policy = SafetyPolicy(observation_timeout_seconds=0.05, max_action_retries=2)
    started = time.monotonic()
    result = AgentRuntime(SlowAdapter(), policy=policy, sleep=sleeps.append).execute(
        "t", [Action("observe")], verification=VERIFY)
    elapsed = time.monotonic() - started

    check("slow observation -> BLOCKED on timeout",
          lambda: result.status == "BLOCKED" and "ActionTimeout" in (result.error or ""))
    check("timed-out action is not retried while the first worker may still be alive",
          lambda: result.steps[0].attempts == 1)
    check("timeout path does not start duplicate workers", lambda: sleeps == [])
    check("runtime gave up before the blocking call finished", lambda: elapsed < 0.25 * 1.5)


def test_workflow_timeout():
    print("\n=== SAFETY 7: workflow timeout (§3) ===")

    class SlowWaitAdapter(FakeAdapter):
        def wait(self, seconds=1):
            time.sleep(float(seconds))
            return {"waited_seconds": seconds}

    policy = SafetyPolicy(workflow_timeout_seconds=0.1)
    actions = [Action("wait", value=0.06) for _ in range(4)]
    result = AgentRuntime(SlowWaitAdapter(), policy=policy).execute(
        "t", actions, verification=VERIFY)
    check("workflow over 0.1 s -> BLOCKED",
          lambda: blocked_with(result, "workflow_timeout"))


def test_retry_policy():
    print("\n=== SAFETY 8: retry policy (§2) ===")

    class AlwaysTransient(FakeAdapter):
        def click(self, target):
            raise TimeoutError("network timeout")

    sleeps = []
    result = AgentRuntime(AlwaysTransient(), sleep=sleeps.append).execute(
        "t", [Action("click", target="X")], verification=VERIFY)
    check("transient error stops after 2 retries (3 attempts total)",
          lambda: result.steps[0].attempts == 3 and sleeps == [0.5, 0.5])
    check("exhausted retries -> FAIL", lambda: result.status == "FAIL")

    class AlwaysPermanent(FakeAdapter):
        def click(self, target):
            raise RuntimeError("element not found")

    sleeps2 = []
    permanent = AgentRuntime(AlwaysPermanent(), sleep=sleeps2.append).execute(
        "t", [Action("click", target="X")], verification=VERIFY)
    check("permanent error not retried (no infinite retry)",
          lambda: permanent.steps[0].attempts == 1 and sleeps2 == [])


def test_no_false_pass():
    print("\n=== SAFETY 9: no false PASS (review principle #2) ===")
    plain = AgentRuntime(FakeAdapter()).execute("t", [Action("click", target="Continue")])
    check("omitted verification runs minimum observation -> PASS",
          lambda: plain.status == "PASS"
          and any(e.get("verification") == "PASS"
                  and e.get("checks") == [{"kind": "observation_exists"}]
                  for e in plain.evidence))

    class Unobservable(FakeAdapter):
        def observe(self):
            raise RuntimeError("observation unavailable")

    unavailable = AgentRuntime(Unobservable()).execute(
        "t", [Action("click", target="Continue")])
    check("unavailable minimum verification -> BLOCKED",
          lambda: blocked_with(unavailable, "minimum verification unavailable"))

    class EmptyObservation(FakeAdapter):
        def observe(self):
            self.calls.append("observe")
            return {}

    empty_observation = AgentRuntime(EmptyObservation()).execute(
        "t", [Action("click", target="Continue")])
    check("empty final observation -> BLOCKED, never FAIL/PASS",
          lambda: blocked_with(empty_observation, "final observation is empty"))

    closing = FakeAdapter()
    closed = AgentRuntime(closing).execute("close", [Action("close")])
    check("final close action -> BLOCKED without reopening browser",
          lambda: blocked_with(closed, "adapter was closed")
          and closing.calls == ["start", "close"])

    empty = AgentRuntime(FakeAdapter()).execute(
        "t", [Action("observe")], verification={"checks": []})
    check("empty checks -> BLOCKED", lambda: blocked_with(empty, "verification_invalid"))

    bogus = AgentRuntime(FakeAdapter()).execute(
        "t", [Action("observe")], verification={"checks": [{"field": "", "contains": "x"}]})
    check("check without field -> BLOCKED", lambda: blocked_with(bogus, "verification_invalid"))

    bad_scope = AgentRuntime(FakeAdapter()).execute(
        "t", [Action("observe")],
        verification={"checks": [{"field": "text", "contains": "x", "scope": "somewhere"}]})
    check("invalid scope -> BLOCKED", lambda: blocked_with(bad_scope, "verification_invalid"))


def test_post_condition_uses_final_observation():
    print("\n=== SAFETY 10: post-condition must hold at the END ===")

    class TwoStateAdapter(FakeAdapter):
        def __init__(self):
            super().__init__()
            self.n = 0

        def observe(self):
            self.n += 1
            text = "READY" if self.n == 1 else "DONE"
            return {"url": "http://127.0.0.1/fake", "text": text}

    runtime = AgentRuntime(TwoStateAdapter())
    early = runtime.execute("t", [Action("observe"), Action("observe")],
                            verification={"checks": [{"field": "text", "contains": "READY"}]})
    check("early observation cannot satisfy the final post-condition",
          lambda: early.status == "FAIL")

    any_scope = AgentRuntime(TwoStateAdapter()).execute(
        "t", [Action("observe"), Action("observe")],
        verification={"checks": [{"field": "text", "contains": "READY", "scope": "any"}]})
    check("explicit scope=any still works", lambda: any_scope.status == "PASS")


def main():
    print("Work 10 — Safety Policy Tests (negative cases)")
    print("=" * 58)
    for fn in (
        test_unknown_action_blocked,
        test_destructive_requires_allow,
        test_boundary_path,
        test_adapter_screenshot_path_boundary,
        test_boundary_domain,
        test_wait_limit,
        test_action_timeout,
        test_workflow_timeout,
        test_retry_policy,
        test_no_false_pass,
        test_post_condition_uses_final_observation,
    ):
        fn()
    print("\n" + "=" * 58)
    if SKIPPED:
        print(f"Safety Policy tests: {len(SKIPPED)} SKIPPED")
        for item in SKIPPED:
            print(f"  - {item}")
    if FAILED:
        print(f"Safety Policy tests: {len(FAILED)} FAILED")
        for item in FAILED:
            print(f"  - {item}")
        raise SystemExit(1)
    print("Safety Policy tests: ALL PASSED")


if __name__ == "__main__":
    main()
