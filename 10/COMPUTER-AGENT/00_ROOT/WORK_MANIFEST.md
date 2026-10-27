# WORK 10 — COMPUTER AGENT

Work ID: 10  
Name: COMPUTER-AGENT

## Decision 2026-10-04
Build from specification instead of porting the original HTML. Existing HTML is retained as reference/mock only.

## Current implementation
- Work structure: PASS
- Architecture spec: PASS
- Agent contracts/runtime: IMPLEMENTED + HARDENED
- Real Playwright/Chromium adapter: IMPLEMENTED
- API verification: IMPLEMENTED
- P0-P2 executable contract tests: **FULL COVER (Offline Matrix)**
- P3 real-browser E2E: TEST SCRIPT READY / HOST RUN REQUIRED
- P4 Dashboard integration: IMPLEMENTED
- P5 release smoke test: READY / HOST RUN REQUIRED

## Specification Lock (2026-10-04)

1. **ACTION_CONTRACT.md** — LOCKED  
   click ≠ type | Unknown → REJECT | Observable result required

2. **WORKFLOW_CONTRACT.md** — LOCKED  
   PLANNED → RUNNING → VERIFYING → PASS/FAIL/BLOCKED  
   Cấm nhảy từ action success → PASS

3. **SAFETY_POLICY.md** — LOCKED  
   Retry/timeout limits | Destructive must allow | Boundary for screenshot/extract

4. **OFFLINE_TEST_MATRIX.md** — READY

## Offline Hardening (2026-10-04 evening)

Đã harden code để **enforcement thực sự**, không chỉ ghi trong tài liệu:

### models.py
- `CANONICAL_ACTIONS` set
- `ActionValidationError`
- `__post_init__` reject unknown action + missing required fields
- click bắt buộc target, type bắt buộc target+value, navigate bắt buộc value

### agent_runtime.py
- Explicit state_trace: PLANNED → RUNNING → VERIFYING → PASS/FAIL/BLOCKED
- Unknown action → BLOCKED
- Không bao giờ skip VERIFYING khi có verification
- Phân biệt FAIL vs BLOCKED
- Evidence entry chuẩn hóa

### test_p0_p5.py
- Mở rộng full cover Offline Test Matrix:
  - 2.1 Action Contract
  - 2.2 Click/Type Separation
  - 2.3 Workflow State Machine
  - 2.4 Verification Logic
  - 2.5 Evidence Completeness
  - 2.6 API Validation
  - 2.7 Failure Handling
  - Anti-pattern checks (không skip VERIFYING)
- 2026-10-06: corrected the workflow happy-path fixture to include an observation required by its verification contract; awaiting CI rerun.

## Evidence rule
No fake PASS. P3/P5 chỉ được ghi PASS sau khi chạy thật trên host có Chromium/Playwright và có evidence trong 06_EVIDENCE.

## Pre-host-run hardening (2026-10-27)

Fixed before the host E2E run (static review findings):

### agent_api.py
- **P5 blocker fix:** `/agent/execute` crashed with 500 because `TaskResult.steps`
  contains `ActionResult` dataclasses that `json.dumps` cannot serialize.
  Added `default=str` to the response encoder.

### browser_adapter.py
- `type()`: label-first resolution (`get_by_label` → `get_by_placeholder` →
  `get_by_role("textbox")`). Raw label text is never passed to `locator()` as CSS —
  labels with special characters (e.g. "Task #1") are invalid selectors and raised
  even when the label matched.
- `screenshot()`: relative paths and the default are now anchored to
  `06_EVIDENCE` regardless of current working directory (the E2E harness calls `os.chdir`).

### e2e_real_browser.py
- Preflight check: missing playwright/Chromium → status BLOCKED with actionable
  message + evidence file written (per Workflow Contract; never a fake PASS, and
  an environment gap is BLOCKED, not FAIL).
- Exit codes: 0 = PASS, 1 = FAIL, 2 = BLOCKED.
- Browser and local server are always cleaned up in `finally`.

### New
- `05_TEST/HOST_E2E_RUNBOOK.md`: exact host commands + evidence checklist
  required before recording PASS.

## Current status (2026-10-27)
SOURCE: PASS
SPECIFICATION: LOCKED
RUNTIME: HARDENED (contract enforced in code)
OFFLINE TEST FIX: APPLIED (awaiting CI rerun)
API SERIALIZATION FIX: APPLIED
HOST E2E: NOT YET VERIFIED — follow 05_TEST/HOST_E2E_RUNBOOK.md
RELEASE: NOT READY until host E2E evidence exists
