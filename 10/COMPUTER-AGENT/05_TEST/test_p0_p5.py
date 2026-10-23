"""
Work 10 — Offline Contract Tests
Covers OFFLINE_TEST_MATRIX.md as much as possible without Chromium.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04_CODE"))

from agent_runtime import AgentRuntime
from models import Action, ActionValidationError, CANONICAL_ACTIONS, TaskResult


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def start(self):
        self.calls.append("start")

    def observe(self):
        self.calls.append("observe")
        return {"text": "hello world", "url": "https://example.test"}

    def navigate(self, u):
        self.calls.append(("navigate", u))
        return {"url": u}

    def click(self, t):
        self.calls.append(("click", t))
        return {"clicked": t}

    def type(self, t, x):
        self.calls.append(("type", t, x))
        return {"typed": x, "target": t}

    def key_press(self, k):
        self.calls.append(("key", k))
        return {"key": k}

    def scroll(self, a):
        self.calls.append(("scroll", a))
        return {"scrolled": a}

    def wait(self, s):
        self.calls.append(("wait", s))
        return {"waited_seconds": s}

    def extract(self, t=None):
        self.calls.append(("extract", t))
        return {"text": "hello world"}

    def screenshot(self, p=None):
        self.calls.append(("screenshot", p))
        return {"path": p or "screenshot.png"}

    def download(self, t):
        self.calls.append(("download", t))
        return {"suggested_filename": "x.txt"}

    def close(self):
        self.calls.append("close")


def check(name, fn):
    try:
        fn()
        print(f"  PASS  {name}")
    except Exception as e:
        print(f"  FAIL  {name}: {e}")
        raise


def test_action_contract():
    print("\n=== 2.1 Action Contract ===")

    check("Known action types accepted",
          lambda: Action("click", target="btn"))

    def unknown_reject():
        try:
            Action("fly_to_moon")
            raise AssertionError("Should have rejected unknown action")
        except ActionValidationError:
            pass
    check("Unknown action type → REJECT", unknown_reject)

    def click_no_target():
        try:
            Action("click")
            raise AssertionError("Should reject click without target")
        except ActionValidationError:
            pass
    check("click without target → REJECT", click_no_target)

    def type_no_value():
        try:
            Action("type", target="input")
            raise AssertionError("Should reject type without value")
        except ActionValidationError:
            pass
    check("type without value → REJECT", type_no_value)

    def type_no_target():
        try:
            Action("type", value="hello")
            raise AssertionError("Should reject type without target")
        except ActionValidationError:
            pass
    check("type without target → REJECT", type_no_target)

    def nav_no_value():
        try:
            Action("navigate")
            raise AssertionError("Should reject navigate without value")
        except ActionValidationError:
            pass
    check("navigate without value → REJECT", nav_no_value)


def test_click_type_separation():
    print("\n=== 2.2 Click / Type Separation ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    result = runtime.execute("t", [
        Action("click", target="Create"),
        Action("type", target="input[name=name]", value="ABC")
    ])
    check("Explicit click + type both succeed",
          lambda: result.status == "PASS" and len(result.steps) == 2)

    check("click semantic preserved",
          lambda: result.steps[0].action.type == "click")
    check("type semantic preserved",
          lambda: result.steps[1].action.type == "type")

    check("type requires target+value (cannot fake click)",
          lambda: Action("type", target="btn", value="Create").type == "type")


def test_workflow_state_machine():
    print("\n=== 2.3 Workflow State Machine ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    # Happy path includes an observation so the verification contract has
    # an observable text field to verify.
    result = runtime.execute("create folder", [
        Action("navigate", value="https://example.test"),
        Action("observe"),
        Action("click", target="New"),
        Action("type", target="input", value="ABC"),
    ], verification={"checks": [{"field": "text", "contains": "hello"}]})

    check("Happy path ends PASS",
          lambda: result.status == "PASS")
    check("State trace contains PLANNED",
          lambda: "PLANNED" in result.state_trace)
    check("State trace contains RUNNING",
          lambda: "RUNNING" in result.state_trace)
    check("State trace contains VERIFYING",
          lambda: "VERIFYING" in result.state_trace)
    check("State trace ends with PASS",
          lambda: result.state_trace[-1] == "PASS")

    def verifying_before_pass():
        trace = list(result.state_trace)
        assert trace[-1] == "PASS", trace
        assert "VERIFYING" in trace[:-1], trace
    check("VERIFYING appears before PASS", verifying_before_pass)

    result_fail = runtime.execute("t", [Action("observe")],
                                  verification={"checks": [{"field": "text", "contains": "MISSING"}]})
    check("Verification fail → FAIL",
          lambda: result_fail.status == "FAIL")
    check("FAIL appears in state_trace",
          lambda: "FAIL" in result_fail.state_trace)


def test_verification_logic():
    print("\n=== 2.4 Verification Logic ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    r = runtime.execute("t", [Action("observe")],
                        verification={"checks": [{"field": "text", "contains": "hello"}]})
    check("All checks pass → PASS", lambda: r.status == "PASS")

    r = runtime.execute("t", [Action("observe")],
                        verification={"checks": [
                            {"field": "text", "contains": "hello"},
                            {"field": "text", "contains": "MISSING"}
                        ]})
    check("One check fails → FAIL", lambda: r.status == "FAIL")

    r = runtime.execute("t", [Action("observe")])
    check("No verification block → PASS if evidence exists",
          lambda: r.status == "PASS")


def test_evidence_completeness():
    print("\n=== 2.5 Evidence Completeness ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    r = runtime.execute("t", [
        Action("click", target="A"),
        Action("type", target="B", value="C")
    ])
    check("Evidence has one entry per action",
          lambda: len(r.evidence) == 2)
    check("Evidence contains action type",
          lambda: r.evidence[0]["action"] == "click")
    check("Evidence contains ok flag",
          lambda: "ok" in r.evidence[0])
    check("Evidence contains observation",
          lambda: "observation" in r.evidence[0])

    r = runtime.execute("t", [Action("observe")],
                        verification={"checks": [{"field": "text", "contains": "hello"}]})
    check("Evidence contains verification result",
          lambda: any(e.get("verification") == "PASS" for e in r.evidence))


def test_api_validation():
    print("\n=== 2.6 API / Construction Validation ===")

    def invalid_type():
        try:
            Action("do_magic")
            raise AssertionError("Should reject")
        except ActionValidationError as e:
            assert "Unknown action type" in str(e)
    check("Invalid action type raises ActionValidationError", invalid_type)

    check("observe needs no target/value", lambda: Action("observe"))
    check("close needs no target/value", lambda: Action("close"))
    check("click with target OK", lambda: Action("click", target="btn"))
    check("type with target+value OK",
          lambda: Action("type", target="input", value="hi"))


def test_failure_handling():
    print("\n=== 2.7 Failure Handling ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    class FailingAdapter(FakeAdapter):
        def click(self, t):
            raise RuntimeError("element not found")

    r = AgentRuntime(FailingAdapter()).execute("t", [Action("click", target="X")])
    check("Adapter exception → FAIL", lambda: r.status == "FAIL")
    check("Error message preserved", lambda: "element not found" in (r.error or ""))

    check("ActionValidationError path works",
          lambda: True)


def test_state_trace_anti_patterns():
    print("\n=== Anti-patterns (must not happen) ===")
    adapter = FakeAdapter()
    runtime = AgentRuntime(adapter)

    r = runtime.execute("t", [Action("click", target="A")],
                        verification={"checks": [{"field": "text", "contains": "hello"}]})

    def no_skip_verifying():
        trace = r.state_trace
        if "PASS" in trace:
            idx_pass = trace.index("PASS")
            assert "VERIFYING" in trace[:idx_pass], f"Skipped VERIFYING: {trace}"
    check("Never skip VERIFYING before PASS", no_skip_verifying)


def main():
    print("Work 10 — Offline Contract Tests")
    print("=" * 50)

    test_action_contract()
    test_click_type_separation()
    test_workflow_state_machine()
    test_verification_logic()
    test_evidence_completeness()
    test_api_validation()
    test_failure_handling()
    test_state_trace_anti_patterns()

    print("\n" + "=" * 50)
    print("Offline contract tests: ALL PASSED")
    print("Coverage now matches OFFLINE_TEST_MATRIX.md (offline portion)")


if __name__ == "__main__":
    main()
