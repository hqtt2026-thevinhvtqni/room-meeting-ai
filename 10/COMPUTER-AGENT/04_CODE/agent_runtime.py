from models import Action, ActionResult, TaskResult, ActionValidationError, CANONICAL_ACTIONS

class AgentRuntime:
    """
    Computer Agent Runtime — enforces Action Contract + Workflow Contract + Safety Policy.

    State machine (Workflow Contract):
        PLANNED → RUNNING → VERIFYING → PASS
                                      → FAIL
                                      → BLOCKED
    """

    def __init__(self, adapter):
        self.adapter = adapter

    def execute(self, task: str, actions: list[Action], verification: dict | None = None) -> TaskResult:
        state_trace = ["PLANNED"]
        steps: list[ActionResult] = []
        evidence: list[dict] = []

        try:
            # --- RUNNING ---
            state_trace.append("RUNNING")
            self.adapter.start()

            for action in actions:
                # Extra safety: re-validate even if Action was constructed elsewhere
                if action.type not in CANONICAL_ACTIONS:
                    result = ActionResult(
                        ok=False,
                        action=action,
                        error=f"Unsupported action: {action.type}",
                        status="blocked"
                    )
                    steps.append(result)
                    evidence.append(self._evidence_entry(action, result))
                    state_trace.append("BLOCKED")
                    return TaskResult("BLOCKED", task, steps, evidence,
                                      error=result.error, state_trace=state_trace)

                result = self._execute_action(action)
                steps.append(result)
                evidence.append(self._evidence_entry(action, result))

                if not result.ok:
                    # Distinguish FAIL vs BLOCKED
                    final_status = "BLOCKED" if result.status == "blocked" else "FAIL"
                    state_trace.append(final_status)
                    return TaskResult(final_status, task, steps, evidence,
                                      error=result.error, state_trace=state_trace)

            # --- VERIFYING ---
            state_trace.append("VERIFYING")
            result = TaskResult("PASS", task, steps, evidence, state_trace=state_trace)

            if verification:
                return self.verify(result, verification)

            # No verification block → still require minimal check (evidence exists)
            if not evidence:
                result.status = "FAIL"
                result.error = "No evidence produced"
                state_trace.append("FAIL")
                result.state_trace = state_trace
                return result

            state_trace.append("PASS")
            result.state_trace = state_trace
            return result

        except ActionValidationError as exc:
            state_trace.append("BLOCKED")
            return TaskResult("BLOCKED", task, steps, evidence,
                              error=str(exc), state_trace=state_trace)
        except Exception as exc:
            state_trace.append("FAIL")
            return TaskResult("FAIL", task, steps, evidence,
                              error=f"{type(exc).__name__}: {exc}", state_trace=state_trace)

    def _execute_action(self, action: Action) -> ActionResult:
        t = action.type
        try:
            if t == "observe":
                data = self.adapter.observe()
            elif t == "navigate":
                data = self.adapter.navigate(action.value or "")
            elif t == "click":
                if not action.target:
                    return ActionResult(False, action, error="click requires target", status="blocked")
                data = self.adapter.click(action.target)
            elif t == "type":
                if not action.target:
                    return ActionResult(False, action, error="type requires target", status="blocked")
                data = self.adapter.type(action.target, action.value or "")
            elif t == "key_press":
                data = self.adapter.key_press(action.value or "")
            elif t == "scroll":
                data = self.adapter.scroll(int(action.args.get("amount", 700)))
            elif t == "wait":
                data = self.adapter.wait(float(action.args.get("seconds", 1)))
            elif t == "extract":
                data = self.adapter.extract(action.target)
            elif t == "screenshot":
                data = self.adapter.screenshot(action.args.get("path"))
            elif t == "download":
                data = self.adapter.download(action.target or "")
            elif t == "close":
                self.adapter.close()
                data = {"closed": True}
            else:
                # Should never reach here if models.py validation works
                return ActionResult(False, action,
                                    error=f"Unsupported action: {t}", status="blocked")

            return ActionResult(True, action, observation=data, status="success")

        except Exception as exc:
            return ActionResult(False, action,
                                error=f"{type(exc).__name__}: {exc}", status="fail")

    def verify(self, result: TaskResult, spec: dict) -> TaskResult:
        """
        VERIFYING stage.
        PASS only when all checks pass.
        Never skip this stage when verification is provided.
        """
        if result.status not in ("PASS",):
            return result

        checks = spec.get("checks", [])
        failures = []

        for check in checks:
            field = check.get("field")
            expected = check.get("contains")
            found = any(
                expected in str(e.get("observation", {}).get(field, ""))
                for e in result.evidence
            )
            if not found:
                failures.append(f"{field} does not contain {expected!r}")

        if failures:
            result.status = "FAIL"
            result.error = "Post-condition verification failed: " + "; ".join(failures)
            result.state_trace.append("FAIL")
            result.evidence.append({
                "verification": "FAIL",
                "checks": checks,
                "failures": failures
            })
        else:
            result.state_trace.append("PASS")
            result.evidence.append({
                "verification": "PASS",
                "checks": checks
            })

        return result

    def _evidence_entry(self, action: Action, result: ActionResult) -> dict:
        return {
            "action": action.type,
            "target": action.target,
            "value": action.value,
            "ok": result.ok,
            "status": result.status,
            "observation": result.observation,
            "error": result.error,
        }
