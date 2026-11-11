# W1111 — THREE-AGENT END-TO-END RE-ASSIGNMENT
**Assignment date:** 2026-11-10 (UTC+7)
**Coordinator / integrator:** Xu (ROOM-HOP identity: xu)
**Priority:** P0 — prove and close the Core → Gateway/Execution Host → Sandbox → durable result/GitHub path
**Execution mode:** END_TO_END_DELEGATED_OUTCOME; no routine progress pings.

## 0. Mandatory common instructions — all three agents
Before acting, READ the complete relevant canonical Work 1111 documents and the full execution journal, including the latest addenda. At minimum:
- `00_ROOT/WORK_MANIFEST.md`
- `00_ROOT/AI_WORKING_RULES.md`
- `00_ROOT/AUTONOMOUS_E2E_EXECUTION_MODE.md`
- `00_ROOT/NHAT_KY_THI_CONG.md`
- `02_EXTENSION/TECHNICAL_BASELINE_AND_OPEN_BLOCKERS.md`
- `02_EXTENSION/CLA_TASK_ASSIGNMENT_TO_CO_20261109.md`
- `02_EXTENSION/APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md`
- `02_EXTENSION/DOC-010_REVISION-LEDGER_SOURCE-OF-TRUTH.md`
- latest C02/C07 evidence and PR #48 self-review / source-trace records in `03_ARCHITECTURE` and `06_EVIDENCE`.
If a named path is absent, locate the canonical equivalent from the Work listing/document register and record the exact result; do not silently skip it.

Then independently reconcile the current GitHub repository, PR #48, branch HEAD, exact file/blob SHAs, CI run status and Sandbox evidence. Earlier SHAs and CI results in historical notes are anchors only; do not assume they remain current. Keep GitHub branch, Sandbox mirror, PC/live runtime and CI evidence as separate evidence classes.

Each agent owns its assigned outcome from READ through TRACE → PLAN → EXECUTE → VERIFY → RECORD → HANDOFF. Self-correct and rerun relevant checks within scope and permissions. Do not stop after proposing a plan. Do not send routine chat progress reports. Record each meaningful command/method, timestamp, scope, exact revision, output/evidence, PASS/FAIL/BLOCKED and next action in the canonical Work 1111 journal and linked evidence file. Preserve history by appending corrections/addenda.

## 1. Co — Core authorization / policy / durable authority record
**Ownership:** Core authority and authorization path.
- Trace the exact current Core source and all call sites that issue/validate Work-scoped execution authority.
- Determine whether authenticated principal, exact Work + Task/Assignment, owner/ACK/state/revocation, canonical resource/path, action allow-list, source commit/blob SHA, environment, expiry, replay/idempotency, policy/gates and correlation are bound together and revalidated immediately before effect.
- Trace Core → downstream grant/authorization handoff; prove deny-by-default for missing, stale, mismatched, revoked or unverifiable claims.
- Prove durable Core decision/result recording and failure behavior. A failed durable record must not be represented as successful execution.
- Build/extend positive and negative tests for authorized request, wrong Work, wrong source SHA, unauthorized action/resource, expired/revoked/replayed grant, malformed/missing claims and Core record failure.
- Resolve implementation defects only on the currently authorized dedicated branch/PR scope. If required authority approval is absent, do not infer it from a draft or historic statement; complete read-only trace, tests that do not bypass the gate, and precise blocker evidence.
**Handoff:** exact source revision, changed paths, test names/results, CI evidence tied to exact SHA, grant/record contract, remaining blocker.

## 2. Xuco — Gateway / MCP / Sandbox enforcement
**Ownership:** Gateway request identity, tool authorization and Sandbox boundary.
- Trace the real request path from authenticated caller through Gateway to MCP tool dispatch and Sandbox mutation/read operations.
- Establish whether identity is cryptographically/trustworthily bound to the caller; caller-supplied headers or arbitrary `work_id`/authorization booleans are not trusted identity.
- Verify every protected operation is bound to Work, Task/Assignment, exact resource/path, action allow-list, source revision and current authorization; fail closed on missing or inconsistent context.
- Trace policy enforcement at the actual mutation call sites, not merely policy prototypes or disconnected helper modules.
- Test positive and negative cases: wrong Work, wrong path/resource, forged identity/header, unauthorized action, stale/revoked grant, path traversal/symlink/reparse boundary where applicable, audit failure and direct tool invocation bypass.
- Confirm durable audit evidence is written before/with protected effect according to the contract; audit failure must prevent the effect.
- Do not use the Meeting MCP endpoint or assume that a file-only MCP capability can execute pytest/processes. Discover actual available execution capabilities and record limits.
**Handoff:** exact request sequence/call sites, enforcement map, tests and evidence, bypasses closed/open, current tool/runtime capability and blocker.

## 3. Vi — Execution Host / execution integrity / result artifact
**Ownership:** Execution Host validation, process execution and result integrity.
- Trace exact current Execution Host source, startup/entrypoint, bridge caller, host configuration and all execution/result call sites.
- Verify authorization/grant validation occurs before process creation and is bound to the exact Work workspace, source SHA, allowed command, timeout and execution environment.
- Verify workspace containment, symlink/reparse/path traversal defense, executable allow-list, environment/secret handling, timeout and child-process cleanup.
- Verify nested test failures/timeouts/BLOCKED and execution errors propagate to the top-level result; a primary command PASS must never mask a failing nested test.
- Verify `FINAL_RESULT.json` (or the canonical current result artifact) and evidence hashes/metadata are complete, tamper-evident and consistent with the durable Core record.
- Add/run regression tests for positive execution, unauthorized execution, wrong Work/SHA, timeout, child cleanup, nested FAIL/TIMEOUT/BLOCKED, missing result artifact and Core-record failure.
- Distinguish source/unit/CI success from live PC/runtime proof. Do not claim a live :8031 or cloud execution PASS without current process identity, build/source hash, authorization and end-to-end evidence.
**Handoff:** exact source/build revision, execution/result state machine, regression tests and exact-SHA CI evidence, runtime proof or precise missing condition.

## 4. Integration and dependency protocol
- Xu maintains one integration view and maps dependencies among the three deliverables. Each agent must expose interface/contract changes to the other two through the canonical journal/evidence, not private chat alone.
- Parallelize independent source tracing and tests. Do not wait idle on another agent when safe, in-scope work remains.
- Integrate only after all three handoffs are read and cross-checked. Resolve contradictions by exact source/call-site evidence, not role seniority or assumptions.
- End-to-end acceptance requires a single traceable correlation chain: trusted caller → Core policy/grant → Gateway/MCP enforcement → Execution Host validation → correct isolated Work execution → result artifact + durable Core record → GitHub branch/commit remote readback.
- Include negative authorization tests and exact source SHA. CI must be tied to the exact tested SHA. Sandbox parity and live runtime are separate gates.
- No false PASS: if any required link cannot be evidenced, report the overall chain BLOCKED/NOT VERIFIED and identify the exact missing condition.

## 5. Authority and safety boundary — applies to all agents
This assignment does NOT override DOC-117 or any stricter existing authorization/gate. Until the exact task-scoped authorization is verified:
- No protected source mutation, CI dispatch, PC/runner operation, service restart, PR merge, deploy, release, secret access/disclosure, destructive cleanup or privilege escalation.
- Do not treat a draft approval record, old branch, old SHA, old CI run, source-level test or file readback as live authorization/runtime evidence.
- Work may proceed autonomously on read-only trace, architecture, test design, non-protected documentation and other explicitly permitted actions.
- If the required authorization is missing, record the exact tuple element / authority / evidence missing, what was attempted, why it cannot be safely bypassed, options, and safe work that continues.
- Never ask the user for information already present in Work or retrievable through connected tools. Escalate only a genuine human-reserved approval or irreducible PC/live-runtime action, consolidated into one request.

## 6. Definition of done for each agent
A complete handoff contains: task outcome; files/paths; before/after revision; source/call-site trace; commands/methods; test inventory and exact results; CI run/job evidence tied to exact SHA where available; evidence paths/hashes; security boundary; unresolved risks; next owner/dependency. Mark DONE only when the assigned acceptance criteria are evidenced. Otherwise use BLOCKED_WITH_EXACT_MISSING_CONDITION or PARTIAL with explicit evidence.

---

## 2026-11-10 — Xu authority reconciliation addendum (supersedes stale PENDING checkpoint)

The canonical approval record `02_EXTENSION/APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md` has been reconciled against Anh Vinh's explicit prior decisions:
- DR-1..DR-4 = APPROVED (original owner decision 2026-10-25).
- Gate 1 = PASS / APPROVED.
- Gate 2 = OPEN / AUTHORIZED for Co's Core implementation and tests within existing task/repository/branch/security boundaries.
- Gates 3–5 remain NOT OPEN pending their independent prerequisites and task-scoped authorization.

**Co: resume the authorized Core implementation/remediation and tests. Do not ask Anh Vinh to re-confirm DR-1..DR-4.** Start by reading the corrected approval record and current journal, then continue the C-CORE-01 source-hash mismatch, C-CORE-02 task/assignment binding gap and C-CORE-03 revoke/run race findings through permitted implementation, regression tests, exact-SHA CI evidence and handoff. Preserve dirty working trees and unrelated changes. Do not assume this approval authorizes PC/runner, service restart, secret access, live /execute, merge, main mutation, deploy or release; DOC-117 remains binding.

Xuco and Vi continue their own assigned end-to-end work without waiting on Co where safe. Xu integrates their evidence. This addendum is an instruction to use the corrected canonical decision state, not a new request for owner approval.
