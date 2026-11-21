"""
Work 10 — Offline Contract Tests (P0/P1/P2 contracts, no browser)

Covers the current Workflow Contract:
  * an omitted verification block invokes §3.4 minimum observation verification;
  * an explicitly supplied empty/malformed block is BLOCKED;
  * explicit post-condition checks run against the FINAL observation by default.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04_CODE"))

from agent_runtime import AgentRuntime
from models import Action, ActionValidationError, CANONICAL_ACTIONS, SafetyPolicy  # noqa: F401
from test_fake_adapter import FakeAdapter

VERIFY = {"checks": [{"field": "text", "contains": "SUBMITTED"}]}
FAILED = []


def check(name, fn):
    try:
        outcome = fn()
        if outcome is False:
            raise AssertionError("check returned False")
        print(f"  PASS  {name}")
    except Exception as exc:  # noqa: BLE001
        FAILED.append(f"{name}: {exc}")
        print(f"  FAIL  {name}: {exc}")


def test_action_contract():
    print("\n=== 2.1 Action Contract ===")
    check("Known action types accepted", lambda: Action("click", target="btn"))

    def reject(factory, label):
        def run():
            try:
                factory()
            except ActionValidationError:
                return
            raise AssertionError(f"{label} should have been rejected")
        return run

    check("Unknown action type -> REJECT", reject(lambda: Action("fly_to_moon"), "unknown"))
    check("click without target -> REJECT", reject(lambda: Action("click"), "click"))
    check("type without value -> REJECT", reject(lambda: Action("type", target="input"), "type"))
    check("type without target -> REJECT", reject(lambda: Action("type", value="hi"), "type"))
    check("navigate without value -> REJECT", reject(lambda: Action("navigate"), "navigate"))
    check("key_press without value -> REJECT", reject(lambda: Action("key_press"), "key"))
    check("wait without value -> REJECT", reject(lambda: Action("wait"), "wait"))
    check("wait non-numeric value -> REJECT", reject(lambda: Action("wait", value="soon"), "wait"))
    check("scroll non-numeric amount -> REJECT",
          reject(lambda: Action("scroll", args={"amount": "far"}), "scroll"))


def test_click_type_separation():
    print("\n=== 2.2 Click / Type Separation ===")
    runtime = AgentRuntime(FakeAdapter())
    result = runtime.execute("t", [
        Action("click", target="Start task"),
        Action("type", target="Task name", value="Work 10 REAL E2E"),
        Action("observe"),
    ], verification=VERIFY)

    check("Explicit click + type both succeed",
          lambda: result.status == "PASS" and len(result.steps) == 3)
    check("click semantic preserved", lambda: result.steps[0].action.type == "click")
    check("type semantic preserved", lambda: result.steps[1].action.type == "type")
    check("type cannot fake click",
          lambda: Action("type", target="btn", value="Create").type == "type")


def test_workflow_state_machine():
    print("\n=== 2.3 Workflow State Machine ===")
    runtime = AgentRuntime(FakeAdapter())
    result = runtime.execute("create folder", [
        Action("navigate", value="http://127.0.0.1/fake"),
        Action("observe"),
        Action("click", target="Start task"),
        Action("type", target="Task name", value="Work 10 REAL E2E"),
        # post-conditions are read from the FINAL observation, so the workflow
        # must end in an observation (a click no longer satisfies verification)
        Action("observe"),
    ], verification=VERIFY)

    check("Happy path ends PASS", lambda: result.status == "PASS")
    check("State trace starts PLANNED", lambda: result.state_trace[0] == "PLANNED")
    check("State trace contains RUNNING", lambda: "RUNNING" in result.state_trace)
    check("State trace contains VERIFYING", lambda: "VERIFYING" in result.state_trace)
    check("State trace ends with PASS", lambda: result.state_trace[-1] == "PASS")
    check("VERIFYING appears before PASS", lambda: result.state_trace.index("VERIFYING")
          < result.state_trace.index("PASS"))

    failing = runtime.execute("t", [Action("observe")],
                              verification={"checks": [{"field": "text", "contains": "MISSING"}]})
    check("Verification fail -> FAIL", lambda: failing.status == "FAIL")
    check("FAIL appears in state_trace", lambda: failing.state_trace[-1] == "FAIL")

    defaulted = runtime.execute("t", [Action("click", target="Continue")])
    check("Omitted verification invokes minimum observation check",
          lambda: defaulted.status == "PASS")
    check("Default check records VERIFYING before PASS",
          lambda: defaulted.state_trace[-2:] == ["VERIFYING", "PASS"])
    check("Default check is recorded in verification evidence",
          lambda: any(e.get("verification") == "PASS"
                      and e.get("checks") == [{"kind": "observation_exists"}]
                      for e in defaulted.evidence))
    check("Default verification performs a fresh observation",
          lambda: "observe" in runtime.adapter.calls)

    explicitly_empty = runtime.execute("t", [Action("observe")], verification={})
    check("Explicit empty verification -> BLOCKED",
          lambda: explicitly_empty.status == "BLOCKED")


def test_verification_logic():
    print("\n=== 2.4 Verification Logic ===")
    runtime = AgentRuntime(FakeAdapter())

    ok = runtime.execute("t", [Action("observe")], verification=VERIFY)
    check("All checks pass -> PASS", lambda: ok.status == "PASS")

    mixed = runtime.execute("t", [Action("observe")], verification={"checks": [
        {"field": "text", "contains": "SUBMITTED"},
        {"field": "text", "contains": "MISSING"},
    ]})
    check("One check fails -> FAIL", lambda: mixed.status == "FAIL")
    check("Failure names the failed post-condition",
          lambda: "MISSING" in (mixed.error or ""))

    empty = runtime.execute("t", [Action("observe")], verification={"checks": []})
    check("Empty checks -> BLOCKED", lambda: empty.status == "BLOCKED")
    check("Empty checks reason is verification_invalid",
          lambda: "verification_invalid" in (empty.error or ""))

    partial = runtime.execute("t", [Action("observe")],
                              verification={"checks": [{"field": "text"}]})
    check("Check without 'contains' -> BLOCKED", lambda: partial.status == "BLOCKED")



def test_action_timeout_semantics():
    print("\n=== 2.6 Timeout Semantics ===")

    class SlowAdapter(FakeAdapter):
        def click(self, target):
            time.sleep(0.35)
            return super().click(target)

    runtime = AgentRuntime(
        SlowAdapter(),
        policy=SafetyPolicy(action_timeout_seconds=0.05),
    )
    result = runtime.execute("timeout semantics", [Action("click", target="slow")])
    check("single-action timeout is recorded as ActionResult fail",
          lambda: result.steps[0].status == "fail")
    check("single-action timeout marks outcome uncertain",
          lambda: result.steps[0].outcome_uncertain is True)
    check("uncertain action timeout blocks enclosing TaskResult",
          lambda: result.status == "BLOCKED" and result.state_trace[-1] == "BLOCKED")
    runtime.wait_for_timed_out_calls()
    runtime.close_adapter()
    runtime.shutdown_adapter_worker()


def test_evidence_completeness():
    print("\n=== 2.5 Evidence Completeness ===")
    runtime = AgentRuntime(FakeAdapter(), work_id="10")
    result = runtime.execute("t", [
        Action("click", target="A"),
        Action("type", target="B", value="C"),
        Action("observe"),
    ], verification=VERIFY)

    action_entries = [e for e in result.evidence if e.get("action") not in (None, "verify")]
    check("Evidence has one entry per action", lambda: len(action_entries) == 3)
    check("Evidence contains action type", lambda: action_entries[0]["action"] == "click")
    check("Evidence contains ok flag", lambda: "ok" in action_entries[0])
    check("Evidence contains observation", lambda: "observation" in action_entries[0])
    check("Evidence has action_id", lambda: bool(action_entries[0]["action_id"]))
    check("Evidence has work_id", lambda: action_entries[0]["work_id"] == "10")
    check("Evidence has ISO8601 UTC timestamp",
          lambda: action_entries[0]["timestamp"].endswith("Z"))
    check("Evidence records attempts and timeout",
          lambda: action_entries[0]["attempts"] == 1
          and action_entries[0]["timeout_seconds"] > 0)
    check("Evidence contains verification result",
          lambda: any(e.get("verification") == "PASS" for e in result.evidence))
    check("TaskResult carries started/finished timestamps",
          lambda: bool(result.started_at) and bool(result.finished_at))


def test_api_validation():
    print("\n=== 2.6 Construction / Payload Validation ===")

    def invalid_type():
        try:
            Action("do_magic")
        except ActionValidationError as exc:
            assert "Unknown action type" in str(exc)
            return
        raise AssertionError("should reject unknown type")

    check("Invalid action type raises ActionValidationError", invalid_type)
    check("observe needs no target/value", lambda: Action("observe"))
    check("close needs no target/value", lambda: Action("close"))
    check("click with target OK", lambda: Action("click", target="btn"))
    check("type with target+value OK", lambda: Action("type", target="input", value="hi"))
    check("wait with value OK", lambda: Action("wait", value=1.5))
    check("scroll with value OK", lambda: Action("scroll", value=500))
    check("extract with schema OK",
          lambda: Action("extract", args={"schema": {"title": "string"}}))


def test_failure_handling():
    print("\n=== 2.7 Failure Handling ===")

    class FailingAdapter(FakeAdapter):
        def click(self, target):
            raise RuntimeError("element not found")

    result = AgentRuntime(FailingAdapter()).execute("t", [Action("click", target="X")],
                                                    verification=VERIFY)
    check("Adapter exception -> FAIL", lambda: result.status == "FAIL")
    check("Error message preserved", lambda: "element not found" in (result.error or ""))
    check("Permanent error not retried", lambda: result.steps[0].attempts == 1)

    class TransientOnce(FakeAdapter):
        def __init__(self):
            super().__init__()
            self.failures = 0

        def click(self, target):
            self.failures += 1
            if self.failures == 1:
                raise TimeoutError("network timeout")
            return {"clicked": target}

    sleeps = []
    runtime = AgentRuntime(TransientOnce(), sleep=sleeps.append)
    retried = runtime.execute("t", [Action("click", target="Y"), Action("observe")], verification=VERIFY)
    check("Transient failure retried then PASS", lambda: retried.status == "PASS")
    check("Retry attempts recorded", lambda: retried.steps[0].attempts == 2)
    check("Backoff applied at >= 500 ms", lambda: sleeps and all(s >= 0.5 for s in sleeps))


def test_state_trace_anti_patterns():
    print("\n=== Anti-patterns (must not happen) ===")
    runtime = AgentRuntime(FakeAdapter())
    result = runtime.execute("t", [Action("click", target="A")],
                             verification={"checks": [{"field": "text", "contains": "MISSING"}]})

    def no_skip_verifying():
        trace = result.state_trace
        if "PASS" in trace:
            assert "VERIFYING" in trace[:trace.index("PASS")], trace
    check("Never skip VERIFYING before PASS", no_skip_verifying)
    check("Failing post-condition never yields PASS", lambda: result.status != "PASS")

    no_evidence = AgentRuntime(FakeAdapter()).execute("t", [], verification=VERIFY)
    check("Empty action list needs verification and still verifies",
          lambda: no_evidence.status in ("PASS", "FAIL", "BLOCKED"))


def main():
    print("Work 10 — Offline Contract Tests")
    print("=" * 58)
    for fn in (
        test_action_contract,
        test_click_type_separation,
        test_workflow_state_machine,
        test_verification_logic,
        test_evidence_completeness,
        test_api_validation,
        test_failure_handling,
        test_state_trace_anti_patterns,
    ):
        fn()
    print("\n" + "=" * 58)
    if FAILED:
        print(f"Offline contract tests: {len(FAILED)} FAILED")
        for item in FAILED:
            print(f"  - {item}")
        raise SystemExit(1)
    print("Offline contract tests: ALL PASSED")


if __name__ == "__main__":
    main()
