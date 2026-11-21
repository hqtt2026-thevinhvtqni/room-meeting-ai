from __future__ import annotations

import os
import queue
import threading
from concurrent.futures import Future, TimeoutError as FutureTimeoutError
from pathlib import Path
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse

from models import (
    CANONICAL_ACTIONS,
    DESTRUCTIVE_ACTIONS,
    TRANSIENT_ERROR_MARKERS,
    Action,
    ActionResult,
    ActionValidationError,
    SafetyPolicy,
    TaskResult,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class _AdapterWorker:
    """Single daemon owner thread for every adapter call in one Runtime.

    Playwright's synchronous API is thread-affine. Start, actions, verification,
    and close must therefore execute serially on the same thread. A timed-out
    Future is not cancelled; the HTTP host waits for it before queuing close.
    """

    def __init__(self):
        self._queue = queue.Queue()
        self._thread = threading.Thread(
            target=self._run, name="work10-adapter-owner", daemon=True
        )
        self._thread.start()

    def submit(self, fn):
        future = Future()
        self._queue.put((future, fn))
        return future

    def _run(self):
        while True:
            item = self._queue.get()
            if item is None:
                return
            future, fn = item
            if not future.set_running_or_notify_cancel():
                continue
            try:
                future.set_result(fn())
            except BaseException as exc:  # preserve adapter exceptions for caller
                future.set_exception(exc)

    def shutdown(self):
        self._queue.put(None)
        if threading.current_thread() is not self._thread:
            self._thread.join()


class ActionTimeout(Exception):
    """A single action exceeded its Safety Policy timeout."""


class WorkflowTimeout(Exception):
    """The whole workflow exceeded its Safety Policy timeout."""


class AgentRuntime:
    """Computer Agent Runtime — enforces Action Contract + Workflow Contract + Safety Policy.

    State machine (Workflow Contract):
        PLANNED → RUNNING → VERIFYING → PASS
                                      → FAIL
                                      → BLOCKED

    Safety Policy (LOCKED, 03_ARCHITECTURE/SAFETY_POLICY.md) is enforced here:
      §2 retry: max 2 action retries, >=500 ms backoff, transient failures only; timed-out calls are terminal because the worker cannot be cancelled
      §3 timeout: per-action, wait, observation and whole-workflow limits
      §4 destructive: refused unless the policy explicitly allows it
      §5 boundary: screenshot/extract/download confined to the Work boundary
      §7 failure: policy violation => BLOCKED with the reason recorded in evidence

    No PASS is possible without a completed post-condition verification.
    """

    def __init__(self, adapter, policy: SafetyPolicy | None = None, work_id="10",
                 sleep=None, clock=None):
        self.adapter = adapter
        self.policy = policy or SafetyPolicy()
        self.work_id = str(work_id)
        self._sleep = sleep or time.sleep
        self._clock = clock or time.monotonic
        self._current_url: str | None = None
        # Timed-out adapter calls may still be executing on the owner thread.
        # The HTTP host retains the process-wide lease until these Futures finish.
        self._timed_out_futures: list[Future] = []
        self._adapter_worker: _AdapterWorker | None = None

    # ------------------------------------------------------------------ public

    def _worker(self) -> _AdapterWorker:
        if self._adapter_worker is None:
            self._adapter_worker = _AdapterWorker()
        return self._adapter_worker

    def has_active_timed_out_calls(self) -> bool:
        return any(not future.done() for future in self._timed_out_futures)

    def wait_for_timed_out_calls(self) -> None:
        """Wait until every timed-out adapter call has actually completed."""
        for future in self._timed_out_futures:
            try:
                future.result()
            except BaseException:
                # Completion, not successful action outcome, is the cleanup gate.
                pass

    def close_adapter(self) -> None:
        """Close on the same owner thread that started and used the adapter."""
        if self._adapter_worker is None:
            self.adapter.close()
            return
        self._adapter_worker.submit(self.adapter.close).result()

    def shutdown_adapter_worker(self) -> None:
        worker, self._adapter_worker = self._adapter_worker, None
        if worker is not None:
            worker.shutdown()

    def execute(self, task: str, actions: list, verification: dict | None = None) -> TaskResult:
        started_at = utc_now()
        clock_start = self._clock()
        state_trace = ["PLANNED"]
        steps: list[ActionResult] = []
        evidence: list[dict] = []

        def finish(status, error=None, extra_evidence=None):
            if extra_evidence:
                evidence.append(extra_evidence)
            state_trace.append(status)
            return TaskResult(
                status, task, steps, evidence, error=error, state_trace=state_trace,
                work_id=self.work_id, started_at=started_at, finished_at=utc_now(),
                policy=self.policy.as_dict(),
            )

        # --- PRE-FLIGHT: policy + contract review BEFORE the browser is touched ---
        violation = self._preflight(actions, verification)
        if violation:
            return finish(
                "BLOCKED",
                f"policy_violation[{violation['rule']}]: {violation['detail']}",
                {
                    "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                    "timestamp": utc_now(), "action": None, "ok": False,
                    "status": "blocked", "observation": {},
                    "error": violation["detail"],
                    "policy_violation": violation["rule"],
                },
            )

        deadline = clock_start + float(self.policy.workflow_timeout_seconds)

        try:
            # --- RUNNING ---
            state_trace.append("RUNNING")
            self._call_with_timeout(self.adapter.start, float(self.policy.action_timeout_seconds))

            for action in actions:
                if self._clock() > deadline:
                    return finish(
                        "BLOCKED",
                        f"policy_violation[workflow_timeout]: workflow exceeded "
                        f"{self.policy.workflow_timeout_seconds}s",
                        {
                            "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                            "timestamp": utc_now(), "action": getattr(action, "type", None),
                            "ok": False, "status": "blocked", "observation": {},
                            "error": "workflow timeout", "policy_violation": "workflow_timeout",
                        },
                    )

                result = self._run_action(action)
                steps.append(result)
                evidence.append(self._evidence_entry(action, result))

                if not result.ok:
                    final_status = "BLOCKED" if result.status == "blocked" else "FAIL"
                    return finish(final_status, result.error)

            # --- VERIFYING ---
            state_trace.append("VERIFYING")
            provisional = TaskResult(
                "PASS", task, steps, evidence, state_trace=state_trace,
                work_id=self.work_id, started_at=started_at, policy=self.policy.as_dict(),
            )
            verification_spec = verification
            if verification is None:
                # Workflow Contract §3.4: omission invokes a real minimum check.
                # This is not equivalent to PASS merely because action evidence exists.
                verification_spec = {
                    "checks": [{"kind": "observation_exists"}],
                    "_generated_default": True,
                }
            return self.verify(provisional, verification_spec)

        except ActionTimeout as exc:
            return finish(
                "BLOCKED",
                f"ActionTimeout: {exc}; adapter worker may still be active",
                {
                    "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                    "timestamp": utc_now(), "action": "start",
                    "ok": False, "status": "blocked", "observation": {},
                    "error": str(exc), "policy_violation": "action_timeout",
                },
            )
        except ActionValidationError as exc:
            return finish("BLOCKED", str(exc))
        except Exception as exc:
            return finish("FAIL", f"{type(exc).__name__}: {exc}")

    def verify(self, result: TaskResult, spec: dict) -> TaskResult:
        """VERIFYING stage. PASS only when every declared post-condition holds.

        Checks run against the FINAL observation by default, so an early page state
        cannot satisfy a post-condition. `scope: "any"` is available when a check
        is intentionally about any step.
        """
        spec = spec or {}
        checks = spec.get("checks") or []  # pre-flight guarantees non-empty
        final_observation = result.steps[-1].observation if result.steps else {}
        failures = []

        if spec.get("_generated_default"):
            # Closing the adapter is terminal for this workflow. Do not call
            # observe() afterwards: the browser adapter's lazy _ensure() would
            # silently create a second browser session.
            last_action = getattr(result.steps[-1].action, "type", None) if result.steps else None
            if last_action == "close":
                block_reason = "minimum verification unavailable: adapter was closed by the final action"
                result.finished_at = utc_now()
                result.status = "BLOCKED"
                result.error = block_reason
                result.state_trace.append("BLOCKED")
                result.evidence.append({
                    "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                    "timestamp": utc_now(), "action": "verify",
                    "verification": "BLOCKED", "checks": checks,
                    "failures": [block_reason], "observation": {},
                    "ok": False, "status": "blocked",
                })
                return result
            try:
                # Obtain a fresh post-action observation; do not mistake action/evidence
                # metadata for a verified post-condition.
                final_observation = self._call_with_timeout(
                    self.adapter.observe,
                    float(self.policy.observation_timeout_seconds),
                )
                if not isinstance(final_observation, dict) or not any(
                    value is not None and str(value).strip()
                    for value in final_observation.values()
                ):
                    block_reason = "minimum verification unavailable: final observation is empty"
                    result.finished_at = utc_now()
                    result.status = "BLOCKED"
                    result.error = block_reason
                    result.state_trace.append("BLOCKED")
                    result.evidence.append({
                        "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                        "timestamp": utc_now(), "action": "verify",
                        "verification": "BLOCKED", "checks": checks,
                        "failures": [block_reason], "observation": {},
                        "ok": False, "status": "blocked",
                    })
                    return result
            except Exception as exc:  # verification unavailable is an external block
                result.finished_at = utc_now()
                result.status = "BLOCKED"
                result.error = f"minimum verification unavailable: {type(exc).__name__}: {exc}"
                result.state_trace.append("BLOCKED")
                result.evidence.append({
                    "action_id": str(uuid.uuid4()), "work_id": self.work_id,
                    "timestamp": utc_now(), "action": "verify",
                    "verification": "BLOCKED", "checks": checks,
                    "failures": [result.error], "observation": {},
                    "ok": False, "status": "blocked",
                })
                return result

        for check in ([] if spec.get("_generated_default") else checks):
            field = check.get("field")
            expected = check.get("contains")
            scope = check.get("scope", "final")
            if scope == "any":
                candidates = [s.observation or {} for s in result.steps]
            else:
                candidates = [final_observation or {}]
            found = False
            for observation in candidates:
                value = observation.get(field)
                if value is not None and str(expected) in str(value):
                    found = True
                    break
            if not found:
                failures.append(f"post-condition failed: {field} does not contain {expected!r} (scope={scope})")

        result.finished_at = utc_now()
        result.state_trace.append("PASS" if not failures else "FAIL")
        result.evidence.append({
            "action_id": str(uuid.uuid4()), "work_id": self.work_id,
            "timestamp": utc_now(), "action": "verify",
            "verification": "PASS" if not failures else "FAIL",
            "checks": checks, "failures": failures,
            "observation": final_observation, "ok": not failures,
            "status": "success" if not failures else "fail",
        })
        if failures:
            result.status = "FAIL"
            result.error = "; ".join(failures)
        else:
            result.status = "PASS"
        return result

    # ------------------------------------------------------------- pre-flight

    def _preflight(self, actions, verification):
        if not isinstance(actions, (list, tuple)):
            return {"rule": "actions_invalid", "detail": "actions must be a list"}

        invalid = self._validate_verification(verification)
        if invalid:
            return invalid

        for action in actions:
            action_type = getattr(action, "type", None)
            if action_type not in CANONICAL_ACTIONS:
                return {"rule": "unknown_action",
                        "detail": f"Unsupported action type: {action_type!r}"}

            if getattr(action, "destructive", False) or action_type in DESTRUCTIVE_ACTIONS:
                if not self.policy.allow_destructive:
                    return {"rule": "destructive_not_allowed",
                            "detail": f"destructive action '{action_type}' requires "
                                      f"explicit policy allow (SAFETY_POLICY §4)"}

            if action_type == "wait":
                seconds = float(action.value if action.value is not None
                                else (action.args or {}).get("seconds", 0))
                if seconds > self.policy.wait_max_seconds:
                    return {"rule": "wait_timeout_exceeded",
                            "detail": f"wait {seconds}s exceeds max {self.policy.wait_max_seconds}s "
                                      f"(SAFETY_POLICY §3)"}

            if action_type == "screenshot":
                path = (action.args or {}).get("path") or action.value
                if not self._path_allowed(path):
                    return {"rule": "boundary_path",
                            "detail": f"screenshot path outside Work boundary: {path!r} "
                                      f"(SAFETY_POLICY §5)"}

            if action_type == "navigate" and not self._domain_allowed(action.value):
                return {"rule": "boundary_domain",
                        "detail": f"navigate target outside allowed domains: {action.value!r} "
                                  f"(SAFETY_POLICY §5)"}
        return None

    @staticmethod
    def _validate_verification(verification):
        """Validate a verification block without constructing or starting an adapter."""
        if verification is None:
            # Workflow Contract §3.4 defines the omitted-block default.
            return None
        if not isinstance(verification, dict) or not verification:
            return {"rule": "verification_invalid",
                    "detail": "an explicitly supplied verification block must be a non-empty object"}
        checks = verification.get("checks") if isinstance(verification, dict) else None
        if not isinstance(checks, list) or not checks:
            return {"rule": "verification_invalid",
                    "detail": "verification.checks must be a non-empty list"}
        for check in checks:
            if not isinstance(check, dict):
                return {"rule": "verification_invalid", "detail": f"check is not an object: {check!r}"}
            if not check.get("field"):
                return {"rule": "verification_invalid", "detail": f"check missing 'field': {check!r}"}
            if check.get("contains") in (None, ""):
                return {"rule": "verification_invalid",
                        "detail": f"check missing 'contains': {check!r}"}
            if check.get("scope", "final") not in ("final", "any"):
                return {"rule": "verification_invalid",
                        "detail": f"check scope must be 'final' or 'any': {check!r}"}
        return None

    def _path_allowed(self, path) -> bool:
        """Allow screenshots only inside this Work's 06_EVIDENCE directory.

        Resolve the destination (including existing symlink parents) before
        checking containment. Prefix/substring matches are deliberately not
        accepted because they permit traversal and look-alike path escapes.
        """
        root = Path(self.policy.work_root).expanduser() if self.policy.work_root else Path(__file__).resolve().parents[1]
        work_root = root.resolve()
        evidence_root = (work_root / "06_EVIDENCE").resolve()
        if path is None:
            return True  # adapter's default is 06_EVIDENCE/latest.png
        raw = Path(str(path)).expanduser()
        if raw.is_absolute():
            candidate = raw.resolve()
        else:
            # Preserve the documented Work-relative form while treating bare
            # filenames as relative to the evidence directory.
            if raw.parts and raw.parts[0].casefold() == "06_evidence":
                candidate = (work_root / raw).resolve()
            elif len(raw.parts) == 1:
                # A bare filename is Evidence-relative; nested relative paths
                # must be explicitly Work-relative under 06_EVIDENCE/.
                candidate = (evidence_root / raw).resolve()
            else:
                candidate = (work_root / raw).resolve()
        try:
            candidate.relative_to(evidence_root)
            return candidate != evidence_root
        except ValueError:
            return False

    def _domain_allowed(self, url) -> bool:
        if self.policy.allowed_domains is None:
            return True
        host = (urlparse(str(url)).hostname or "").lower()
        return host in {d.lower() for d in self.policy.allowed_domains}

    # --------------------------------------------------------------- running

    def _action_timeout(self, action) -> float:
        if action.type in ("observe", "extract"):
            return float(self.policy.observation_timeout_seconds)
        if action.type == "wait":
            seconds = float(action.value if action.value is not None
                            else (action.args or {}).get("seconds", 0))
            return max(float(self.policy.action_timeout_seconds), seconds + 5.0)
        return float(self.policy.action_timeout_seconds)

    def _call_with_timeout(self, fn, timeout: float):
        """Run an adapter call on its dedicated owner thread with bounded wait.

        Python cannot safely cancel a running call. On timeout we retain the
        Future; the HTTP host keeps the global execution lease and defers close
        until this Future has completed. All adapter calls remain on one thread.
        """
        def invoke():
            try:
                return True, fn()
            except BaseException as exc:  # transport adapter exception to caller
                return False, exc

        future = self._worker().submit(invoke)
        try:
            succeeded, value = future.result(timeout=timeout)
        except FutureTimeoutError:
            # Even if the call completes immediately after this timeout edge,
            # the caller's deadline has expired. Retain it for ordered cleanup.
            self._timed_out_futures.append(future)
            raise ActionTimeout(f"action exceeded {timeout}s (SAFETY_POLICY §3)")
        if not succeeded:
            raise value
        return value

    def _run_action(self, action) -> ActionResult:
        max_attempts = int(self.policy.max_action_retries) + 1
        attempts = 0
        last: ActionResult | None = None
        timeout = self._action_timeout(action)

        while attempts < max_attempts:
            attempts += 1
            started = self._clock()
            try:
                data = self._call_with_timeout(lambda: self._dispatch(action), timeout)
                return ActionResult(
                    True, action, observation=data or {}, status="success",
                    attempts=attempts, timeout_seconds=timeout,
                    duration_ms=int((self._clock() - started) * 1000),
                )
            except ActionTimeout as exc:
                # A timed-out worker may still be executing the side effect.
                # Retrying could dispatch a duplicate click/type/download while
                # the first call is alive; timeout is therefore terminal here.
                return ActionResult(
                    False, action, error=f"ActionTimeout: {exc}; worker may still be active", status="blocked",
                    attempts=attempts, timeout_seconds=timeout,
                    duration_ms=int((self._clock() - started) * 1000),
                )
            except Exception as exc:  # noqa: BLE001
                message = f"{type(exc).__name__}: {exc}"
                last = ActionResult(
                    False, action, error=message, status="fail",
                    attempts=attempts, timeout_seconds=timeout,
                    duration_ms=int((self._clock() - started) * 1000),
                )
                transient = any(m in message.lower() for m in TRANSIENT_ERROR_MARKERS)
                if not transient or attempts >= max_attempts:
                    return last
                self._sleep(float(self.policy.retry_backoff_seconds))

        return last

    def _dispatch(self, action):
        action_type = action.type
        if action_type not in CANONICAL_ACTIONS:
            raise ActionValidationError(f"Unknown action type '{action_type}'")

        if action_type == "observe":
            data = self.adapter.observe()
        elif action_type == "navigate":
            data = self.adapter.navigate(action.value or "")
        elif action_type == "click":
            data = self.adapter.click(action.target)
        elif action_type == "type":
            data = self.adapter.type(action.target, action.value or "")
        elif action_type == "key_press":
            data = self.adapter.key_press(action.value or "")
        elif action_type == "scroll":
            amount = action.value if action.value is not None else (action.args or {}).get("amount", 700)
            data = self.adapter.scroll(int(amount))
        elif action_type == "wait":
            seconds = float(action.value if action.value is not None
                            else (action.args or {}).get("seconds", 1))
            data = self.adapter.wait(seconds)
        elif action_type == "extract":
            data = self.adapter.extract(action.target)
            schema = (action.args or {}).get("schema")
            if schema is not None:
                data = {"schema": schema, "data": data}
        elif action_type == "screenshot":
            data = self.adapter.screenshot((action.args or {}).get("path") or action.value)
        elif action_type == "download":
            data = self.adapter.download(action.target or "")
        elif action_type == "close":
            self.adapter.close()
            data = {"closed": True}
        else:  # pragma: no cover - guarded above
            raise ActionValidationError(f"Unsupported action: {action_type}")

        if isinstance(data, dict) and data.get("url"):
            self._current_url = data["url"]
        return data

    def _evidence_entry(self, action, result: ActionResult) -> dict:
        return {
            "action_id": str(uuid.uuid4()),
            "work_id": self.work_id,
            "timestamp": utc_now(),
            "action": action.type,
            "target": action.target,
            "value": action.value,
            "destructive": bool(getattr(action, "destructive", False)
                                or action.type in DESTRUCTIVE_ACTIONS),
            "ok": result.ok,
            "status": result.status,
            "attempts": result.attempts,
            "timeout_seconds": result.timeout_seconds,
            "duration_ms": result.duration_ms,
            "observation": result.observation,
            "error": result.error,
        }
