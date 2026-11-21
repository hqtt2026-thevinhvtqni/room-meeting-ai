# WORK 10 — OWNER DELEGATION & IMPLEMENTATION AUTHORIZATION

- Document ID: W10-OWNER-DELEGATION-EXEC-AUTH-20261122-01
- Work: 10 — COMPUTER-AGENT
- Owner: Vinh — Project Owner / Final Acceptance Authority
- Implementer: Co — AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:10 (UTC+07:00)
- Status: OWNER AUTHORIZATION RECEIVED — IMPLEMENTATION MAY PROCEED
- Scope: Continue Work 10 autonomously through implementation, verification, Sandbox/GitHub reconciliation and handover package for Owner acceptance.

## 1. Owner direction

Owner explicitly delegates Co to continue Work 10 until the work is complete and ready for handover/acceptance. A separate An V8 design review/ACK is not a prerequisite and is removed from the critical path. Co owns the technical decisions, implementation sequence, evidence quality, regression work and handover preparation within this authorization.

This supersedes the V8 proposal's requirement to wait for An review before implementation. Historical V7/V8 documents and An's earlier findings remain immutable records; they are not rewritten or represented as reviewed.

## 2. Implementation authority and limits

Co is authorized to:
- implement the P0 acceptance validator, runtime/process isolation and supporting tests;
- reconcile Sandbox and the canonical branch `work/10-computer-agent-mirror` with explicit diffs and readback;
- use controlled GitHub Actions runners (Linux and Windows) as execution hosts for repeatable CI evidence;
- add evidence, manifests, handover notes and test automation;
- make conservative technical decisions within the locked contracts and record rationale.

Co must not:
- modify the three LOCKED contracts without a separately versioned contract-change decision;
- claim the user's physical PC/PowerShell/browser has been validated when only GitHub-hosted runners were used;
- treat a successful file write, syntax check, JSON parse or Ubuntu run as proof of Windows process containment;
- merge to main, deploy, or release to production without the Owner's separate acceptance/approval;
- report PASS without reproducible artifacts, hashes, logs and exact tested commit.

## 3. F-15 timeout semantics — conservative disposition

The locked Safety Policy §3 remains authoritative:
- a single-action timeout is recorded as an ActionResult failure;
- an entire-workflow deadline is BLOCKED;
- if a timed-out action may still be executing or its side-effect outcome cannot be proven, the enclosing TaskResult is BLOCKED and the execution lease remains held until containment/cleanup is independently confirmed;
- TaskResult may be FAIL only when the action has terminated and the failure outcome is known; it must never be PASS on an uncertain outcome.

This is an implementation interpretation of the existing locked policy, not a change to ACTION_CONTRACT, WORKFLOW_CONTRACT or SAFETY_POLICY. If runtime evidence exposes a contradiction with the locked text, stop and record BLOCKED rather than silently changing contract semantics.

## 4. Acceptance gates owned by Co

1. Source provenance and exact Sandbox/GitHub parity for all accepted source/test/config artifacts.
2. P0 manifest/schema validator with trusted provenance, category policy and negative tests.
3. Process isolation with OS-specific containment, parent-owned deadlines, cleanup and crash-recovery evidence.
4. P1 HTTP authentication/origin/body-boundary regression tests.
5. Real-browser E2E on Linux and Windows runners, with retained artifacts and tested commit hashes.
6. No regressions in the three LOCKED contracts; verify their exact hashes before/after.
7. Dashboard and API integration evidence, with sample-only data clearly separated from live verification.
8. Complete handover: architecture, operating instructions, test matrix, known limitations, evidence index, open risks and owner acceptance checklist.

A gate remains BLOCKED if its required execution environment or evidence is unavailable. Co may continue other independent work while preserving the blocker.

## 5. Current known limitations at authorization time

- Sandbox source is materially newer than GitHub branch source; five source/test files differ and `test_http.py` exists only in Sandbox.
- Current runtime uses a thread-owned adapter worker; it is not yet proof of OS process-tree isolation.
- Existing GitHub CI has passed on Ubuntu, but Windows Job Object/process containment is not yet verified.
- No direct local PC PowerShell/desktop executor is exposed in the current session.
- V8 semantic validator/schema implementation and its negative suite have not been run.

## 6. Decision

Proceed without waiting for An's V8 review. Co is accountable for completing the engineering work and preparing an evidence-backed handover. Work 10 remains ACTIVE until every acceptance gate is either evidenced PASS or explicitly accepted as a documented limitation by the Owner. No false completion status is permitted.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
