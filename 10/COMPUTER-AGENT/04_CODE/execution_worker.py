"""Isolated Work 10 execution worker.

The worker starts in an inert state and reads exactly one JSON request from
stdin. The parent must establish OS containment before releasing that request.
Stdout is reserved for one JSON response; diagnostics go to stderr.
"""
from __future__ import annotations

import dataclasses
import importlib
import json
import os
import sys
import traceback

MAX_REQUEST_BYTES = 1024 * 1024


def _build_adapter():
    target = os.getenv("COMPUTER_AGENT_ADAPTER_MODULE", "").strip()
    if target:
        module_name, _, class_name = target.partition(":")
        module = importlib.import_module(module_name)
        return getattr(module, class_name)()
    from browser_adapter import PlaywrightBrowserAdapter
    return PlaywrightBrowserAdapter(os.getenv("COMPUTER_AGENT_HEADLESS", "0") == "1")


def _error_result(request, message):
    now = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return {
        "status": "BLOCKED",
        "task": request.get("task", ""),
        "steps": [],
        "evidence": [{
            "action": "execution_worker",
            "status": "blocked",
            "ok": False,
            "error": message,
            "timestamp": now,
        }],
        "error": message,
        "state_trace": ["PLANNED", "RUNNING", "VERIFYING", "BLOCKED"],
        "work_id": request.get("work_id", "10"),
        "started_at": now,
        "finished_at": now,
        "policy": request.get("policy"),
    }


def main() -> int:
    raw = sys.stdin.readline(MAX_REQUEST_BYTES + 1)
    if not raw:
        print(json.dumps({"request_id": None, "error": "request_missing",
                          "cleanup_pending": False}), flush=True)
        return 2
    if len(raw.encode("utf-8")) > MAX_REQUEST_BYTES:
        print(json.dumps({"request_id": None, "error": "request_too_large",
                          "cleanup_pending": False}), flush=True)
        return 2

    request_id = None
    request = {}
    adapter = None
    runtime = None
    cleanup_pending = False
    cleanup_error = None
    try:
        request = json.loads(raw)
        if not isinstance(request, dict):
            raise ValueError("request must be a JSON object")
        request_id = request.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            raise ValueError("request_id is required")

        # Import application modules only after the parent has released the
        # start gate, proving containment has already been assigned.
        from models import SafetyPolicy

        policy_data = dict(request.get("policy") or {})
        if "allowed_path_prefixes" in policy_data:
            policy_data["allowed_path_prefixes"] = tuple(policy_data["allowed_path_prefixes"])
        if policy_data.get("allowed_domains") is not None:
            policy_data["allowed_domains"] = tuple(policy_data["allowed_domains"])
        policy = SafetyPolicy(**policy_data)

        if request.get("mode", "browser") == "host":
            from host_operations import HostOperations
            result = HostOperations(policy).execute(
                request.get("operation"), request.get("arguments")
            )
            cleanup_pending = bool(result.pop("cleanup_pending", False))
            payload = {
                "request_id": request_id,
                "result": result,
                "cleanup_pending": cleanup_pending,
                "worker_pid": os.getpid(),
            }
            print(json.dumps(payload, ensure_ascii=False, default=str), flush=True)
            return 0

        from agent_runtime import AgentRuntime
        from models import Action
        actions = [Action(**item) for item in request.get("actions", [])]

        runtime = AgentRuntime(None, policy=policy, work_id=str(request.get("work_id", "10")))
        violation = runtime._preflight(actions, request.get("verification"))
        if violation:
            # Policy/path/domain checks happen before adapter construction.
            result = runtime.execute(
                str(request.get("task", "")), actions, request.get("verification")
            )
        else:
            adapter = _build_adapter()
            runtime.adapter = adapter
            result = runtime.execute(
                str(request.get("task", "")),
                actions,
                request.get("verification"),
            )

            # A timed-out adapter call may still be executing. Do not close it
            # from another thread and do not claim cleanup. Parent terminates
            # the entire OS containment after receiving this flag.
            cleanup_pending = runtime.has_active_timed_out_calls()
            if not cleanup_pending:
                try:
                    runtime.close_adapter()
                except Exception as exc:
                    cleanup_pending = True
                    cleanup_error = f"{type(exc).__name__}: {exc}"
                finally:
                    runtime.shutdown_adapter_worker()

        payload = {
            "request_id": request_id,
            "result": dataclasses.asdict(result),
            "cleanup_pending": cleanup_pending,
            "cleanup_error": cleanup_error,
            "worker_pid": os.getpid(),
        }
        print(json.dumps(payload, ensure_ascii=False, default=str), flush=True)
        return 0
    except BaseException as exc:
        message = f"{type(exc).__name__}: {exc}"
        traceback.print_exc(file=sys.stderr)
        payload = {
            "request_id": request_id,
            "result": _error_result(request, message),
            "cleanup_pending": True,
            "cleanup_error": message,
            "worker_pid": os.getpid(),
        }
        print(json.dumps(payload, ensure_ascii=False, default=str), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
