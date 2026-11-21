# WORK 10 — SAFETY POLICY ENFORCEMENT MAP

**Status:** Historical implementation map; current Sandbox revision NOT RUN — annex to the LOCKED `SAFETY_POLICY.md`
**Original date:** 2026-10-27; current status addendum: 2026-11-17
**Tests:** historical 28 negative checks only; latest suite execution pending

`SAFETY_POLICY.md` is LOCKED and unchanged. This annex records where each rule is
enforced, so the policy is a runtime constraint and not documentation.

## Mapping

| Policy section | Rule | Enforcement point | Negative test |
|---|---|---|---|
| §2 Retry | max 2 action retries | `AgentRuntime._run_action` (`policy.max_action_retries`) | `transient error stops after 2 retries (3 attempts total)` |
| §2 Retry | backoff ≥ 500 ms | `policy.retry_backoff_seconds` before each retry | `backoff slept between retries`, `Backoff applied at >= 500 ms` |
| §2 Retry | infinite retry forbidden | loop bounded by `max_action_retries + 1` | `permanent error not retried` |
| §3 Timeout | single action 30 s | `_call_with_timeout` around every adapter call | `slow observation -> BLOCKED on timeout` |
| §3 Timeout | wait max 120 s | pre-flight `wait_timeout_exceeded` | `wait over 120 s -> BLOCKED` |
| §3 Timeout | observation/extract 15 s | `_action_timeout` per action type | same timeout test |
| §3 Timeout | workflow 10 min | deadline checked before each action | `workflow over 0.1 s -> BLOCKED` |
| §4 Destructive | must be explicitly allowed | pre-flight `destructive_not_allowed` | `download without allow -> BLOCKED`, `action marked destructive -> BLOCKED` |
| §4 Destructive | full logging | evidence entry carries `destructive` and the refusing rule | evidence assertions in `test_p0_p5.py` §2.5 |
| §5 Boundary | screenshot inside the Work | `_path_allowed` (work_root or `allowed_path_prefixes`) | `screenshot outside Work boundary -> BLOCKED`, `path escaping work_root -> BLOCKED` |
| §5 Boundary | no out-of-scope navigation | `_domain_allowed` via `policy.allowed_domains` | `navigate outside allowed domains -> BLOCKED` |
| §7 Failure | violation ⇒ BLOCKED + reason | `TaskResult.error` = `policy_violation[<rule>]: <detail>`; `state_trace` ends BLOCKED | every BLOCKED assertion above |
| §6 Target safety | deterministic resolution | adapter resolves selector → button role → link role → exact text; no fuzzy matching | browser-scope only (host E2E) |

## Deliberate additions (not in the LOCKED text)

- A policy violation is decided **before** the adapter starts, so a refused
  workflow never opens a browser session.
- `/health` exposes the effective policy; `/agent/execute` cannot widen it — only
  the server process environment (`COMPUTER_AGENT_ALLOW_DESTRUCTIVE`,
  `COMPUTER_AGENT_ALLOWED_DOMAINS`, `COMPUTER_AGENT_ALLOWED_PATHS`,
  `COMPUTER_AGENT_WORK_ROOT`) can.

## Open items

- §6 target resolution and real click/type behaviour are only testable on a host
  with Chromium; see `05_TEST/e2e_real_browser.py`.
- Historical timeout wording above is superseded by the 2026-11-17 Sandbox addendum below. Current implementation reports BLOCKED, retains the worker reference, holds the process-wide lease, and defers adapter cleanup until worker exit; it does not cancel the worker.


## HTTP transport boundary — supplementary P1 control
The LOCKED action Safety Policy remains unchanged. In addition to action-level controls, the local HTTP adapter must enforce a server-managed bearer token and exact browser Origin allow-list before constructing an execution adapter. Wildcard CORS is prohibited. Preflight is restricted to the approved dashboard origin, POST, and the Authorization/Content-Type headers. The dashboard must not embed or persist the token. See `04_CODE/README.md` and `05_TEST/TEST_PLAN.md` for implementation and validation. These transport controls supplement, and do not modify, the LOCKED Safety Policy.


## Current Sandbox addendum — 2026-11-17 (supersedes earlier timeout status)
The status/table above records the 2026-10-27 implementation baseline and historical check count; it does not certify the current Sandbox revision.

- ActionTimeout is now terminal and classified BLOCKED, not retried. The Runtime retains the timed-out worker reference for the HTTP host.
- Agent API v1.3.0 uses a process-wide execution lease. Concurrent requests are rejected with 409 execution_busy before adapter construction. When a timed-out worker remains alive, adapter.close() is deferred until the worker exits; a stuck worker keeps the lease held (fail-closed).
- This is containment, not cancellation. A timed-out browser side effect may still finish. Playwright sync thread-affinity, a permanently stuck worker, process crash recovery, and host behavior are not proven. G1 remains BLOCKED pending exact-source tests and a safe worker ownership/process-isolation design.
- HTTP auth/Origin/preflight, request schema and body limits are implemented in Sandbox source; the current regression suite has NOT RUN. Static read-back is not a test PASS.
- Test assertion helpers now fail when callbacks return boolean False. Windows path tests report unsupported host/symlink capability as SKIP, not PASS.
- LOCKED SAFETY_POLICY.md remains unchanged. This addendum is an implementation status note, not a policy amendment or release approval.


### Dedicated adapter owner thread — 2026-11-17 follow-up
All adapter calls are now submitted to one dedicated daemon owner thread per Runtime, including start and close. The API waits for timed-out futures and queues cleanup on that same thread while holding the process-wide execution lease. Fake-adapter HTTP test captures thread identity; real Playwright/Chromium thread-affinity remains NOT RUN. This design note does not promote G1.


## Current process/host enforcement addendum — 2026-11-22

This section supersedes the 2026-10-27/2026-11-17 implementation-status statements above where they say current source is untested. The historical mapping remains preserved as a record of the earlier thread-based implementation.

- API admission and auth: `agent_api.py` validates exact Origin, bearer token, JSON content, request size and allowed operation before execution.
- Process boundary: `ProcessSupervisor` launches an inert child, establishes OS containment before releasing the start gate, validates request correlation and worker result, enforces the parent deadline, terminates uncertain worker trees and verifies containment empty before releasing the host lease.
- Windows: Job Object kill-on-close profile; hosted Windows Server 2022 worker + grandchild containment and API-integrated Chromium E2E passed in Run #53.
- Linux: process-group profile only, explicitly `LIMITED_NOT_CGROUP_V2`; cgroup-v2 production profile remains not implemented.
- Host operations: explicit allowlisted roots; writes require explicit writable roots and overwrite confirmation; PowerShell requires Windows plus explicit .ps1 roots; pytest uses a fixed command vector and allowlisted paths.
- V8 validator: schema and semantic checks plus HMAC attestation; category catalog/policy version and state allowlists are pinned. Run #53 executed 16 validator checks successfully on both OS runners. CI key is test-only; production key provisioning is not complete.
- Physical Windows 10 PC, local ACL/profile/startup, production key setup and ROOM-HOP integration remain NOT RUN / OPEN.

No statement in this annex modifies `SAFETY_POLICY.md` or the other LOCKED contracts.
