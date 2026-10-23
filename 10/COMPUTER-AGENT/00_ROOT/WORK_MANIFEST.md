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

## Current status
SOURCE: PASS  
SPECIFICATION: LOCKED  
RUNTIME: HARDENED (contract enforced in code)  
OFFLINE TEST FIX: APPLIED  
CI RE-VERIFY: PENDING  
HOST E2E: NOT YET VERIFIED  
RELEASE: NOT READY until host E2E evidence exists

## Next gate
CI offline tests PASS → real Chromium E2E → inspect runtime evidence → self-fix/retest if needed → Qe review → release decision
