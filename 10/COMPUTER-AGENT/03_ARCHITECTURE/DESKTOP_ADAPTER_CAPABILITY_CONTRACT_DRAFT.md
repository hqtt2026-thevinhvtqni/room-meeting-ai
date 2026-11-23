# W10 DESKTOP ADAPTER CAPABILITY CONTRACT
- Document ID: W10-DESKTOP-CAPABILITY-CONTRACT-DRAFT-20261123
- Version: 0.1.0-draft
- Status: DRAFT — ARCHITECTURE REVIEW REQUIRED; NOT IMPLEMENTATION AUTHORIZATION
- Owner / final authority: Vinh
- Coordinator: Xu (AI-01)
- Date: 2026-11-23 (UTC+07:00)

## 1. Purpose and scope
Define a separate capability and action boundary for native desktop application automation behind Work 10. This is additive and does not alter the existing LOCKED browser ACTION_CONTRACT, WORKFLOW_CONTRACT or SAFETY_POLICY.

Candidate backend: vercel-labs/agent-desktop. The contract is backend-neutral; W10 must not expose upstream CLI/MCP commands directly to calling agents.

In scope: desktop application/window discovery, accessibility-tree observation, narrowly scoped semantic actions, post-action observation, evidence and fail-closed behavior.

Out of scope: browser-page DOM automation (existing Browser Adapter); unrestricted shell/terminal; general-purpose remote desktop; OS administration; arbitrary filesystem access; credential extraction; unattended financial or legally binding transactions.

## 2. Trust and execution boundary
Caller (authorized HQTT AI/workflow) → approved ROOM-HOP identity and authorization route → W10 Agent API (loopback-only) → W10 Agent Runtime policy → ProcessSupervisor-contained Desktop Adapter worker → pinned backend → OS accessibility API → fresh observation and post-condition verification → W10 evidence/journal.

Mandatory invariants:
1. W10 is the only policy and action boundary. The caller cannot invoke raw CLI, arbitrary shell or unrestricted MCP.
2. W10 API remains loopback-only. Remote access must use the approved ROOM-HOP/W24 authenticated route; no Core authorization bypass.
3. W24 owns PC Source Bridge, Core authorization and authenticated PC transport. W112 owns cross-Work contracts. W14 owns canonical autonomous E2E execution/delivery. W113 owns shared Dashboard ingress :3000. W10 standalone UI remains :3010.
4. Every worker is launched, monitored, timed out, cancelled and cleaned up through ProcessSupervisor.
5. Browser Adapter remains separate. Browser page tasks use Playwright/Chromium; native desktop tasks use this contract.
6. Desktop actions never inherit browser selectors or semantics implicitly.
7. No action is PASS until its explicit post-condition is independently observed and verified.

## 3. Capability negotiation
Before a task, W10 MUST return a capability profile:
- backend name, exact version and binary/library digest;
- OS, OS version, architecture, desktop session type and interactive user/session identity;
- application identity, window identity and supported accessibility provider;
- granted OS permissions and integrity/elevation level;
- supported observation/action capabilities and known unsupported classes;
- worker policy version and contract version.

Capabilities are explicit allow-lists, not inferred from the mere presence of a backend command. Unknown capability = UNSUPPORTED. Any mismatch in pinned identity, session, permission, policy or app/window scope = BLOCKED.

## 4. Canonical desktop operations
These are logical W10 operations, not a promise that every backend/platform implements them.

| Operation | Required inputs | Safety / expected behavior |
|---|---|---|
| desktop.capabilities | none | Return pinned runtime profile; read-only |
| desktop.observe | approved app/window scope | Return redacted accessibility snapshot and observation_id |
| desktop.resolve | observation_id + semantic locator | Resolve only within referenced snapshot and approved scope |
| desktop.click | fresh element_ref | Click only one enabled, visible, in-scope element |
| desktop.type | fresh element_ref + value | Target must be approved editable control; secrets prohibited unless separately approved |
| desktop.select | fresh element_ref + option | Only supported select/list controls |
| desktop.toggle | fresh element_ref + desired_state | Report actual state after re-observation |
| desktop.focus | approved window/control ref | Explicit and auditable; may be unsupported in background mode |
| desktop.wait | condition + bounded timeout | Bounded wait; condition must be observable |
| desktop.close_session | session_id | Close only W10-owned session/worker; never arbitrary user apps |

Not in v0.1 allow-list: arbitrary keyboard shortcuts, global hotkeys, drag/drop, free-coordinate mouse movement, arbitrary clipboard read/write, screenshots by default, file open/save dialogs, app install/uninstall/launch/terminate, shell/terminal, system settings, notification dismissal, credential managers, password/OTP entry, file transfer, payment/purchase, send/publish/submit actions.

A future operation requires a new contract revision, threat review, test cases and explicit Owner approval.

## 5. Reference and observation semantics
- Each observation has unique observation_id, timestamp, app/window identity, tree digest, backend/session identity and bounded lifetime.
- Element refs are opaque, short-lived capabilities scoped to exactly one observation and one app/window.
- Ref MUST be rejected if stale, reused across observations, from another app/window/session, ambiguous, disabled, hidden, detached or outside the allow-list.
- Resolve must return exactly one target. Zero or multiple matches = UNSUPPORTED/BLOCKED; no fuzzy guessing.
- Any state-changing operation invalidates the prior observation for subsequent actions. W10 MUST obtain a fresh observation before another state-changing operation.
- Ref freshness is checked immediately before execution, not only at planning time.
- No silent fallback to pixel coordinates, OCR guessing or global input injection when semantic resolution fails.

## 6. Action request and result envelope
Illustrative logical request:
{
  "contract": "W10-DESKTOP/0.1",
  "task_id": "opaque-id",
  "session_id": "w10-owned-session",
  "observation_id": "fresh-observation",
  "app_scope": {"app_id": "approved-app", "window_id": "approved-window"},
  "operation": "desktop.click",
  "target": {"element_ref": "opaque-ref"},
  "policy_context": {"work_id": "10", "authorization_id": "approved-grant"}
}

Illustrative result:
{
  "action_id": "opaque-id",
  "status": "success | fail | blocked | unsupported | timeout | cancelled",
  "observation_id_before": "opaque-id",
  "observation_id_after": "opaque-id-or-null",
  "target_identity": "redacted-semantic-identity",
  "error_code": "stable-code-or-null",
  "timestamp": "ISO8601",
  "evidence_id": "opaque-id"
}

success means only that the adapter reports the requested operation executed. It does not mean the task or post-condition passed. Missing post-action observation => task BLOCKED, not PASS.

## 7. Safety classes and approval
- S0 READ_ONLY: capabilities and scoped observations. Allowed only within approved app/window scope.
- S1 REVERSIBLE_UI: click/type/select/toggle/focus on explicitly allow-listed non-sensitive controls. Requires task-scoped grant and fresh ref.
- S2 EXTERNAL_OR_IRREVERSIBLE: submit, send, publish, delete, purchase, payment, account/security/permission changes, file transfer or other external side effects. Denied in v0.1. Future support requires separate operation-specific approval, human confirmation and idempotency/reconciliation design.
- S3 PRIVILEGED_SYSTEM: shell, admin/elevation, system settings, security controls, credential store, arbitrary filesystem or process control. Prohibited.

Human confirmation must bind to exact operation, target, app/window, data summary, consequence, expiry and one-time authorization ID. No reuse for another action.

## 8. Privacy and evidence
- Accessibility snapshots may contain names, email, messages, financial data and secrets. Treat all observations as sensitive.
- Default to local/private processing; minimize tree depth and fields; redact secrets and unrelated app content before model exposure.
- Never log raw passwords, OTPs, auth tokens, private message bodies or full clipboard contents.
- Evidence stores metadata, policy decision, action class, timestamps, app/window identity, observation digests, verification outcomes and private evidence references. Raw snapshots are retained only when necessary and under bounded retention/access controls.
- No screenshots by default. Separately authorized diagnostic screenshots are sensitive evidence and follow scope/redaction rules.
- Logs must not leak content to Dashboard, analytics, third-party services or another Work without an approved data flow.

## 9. Runtime reliability and fail-closed rules
- Worker process must be owned by ProcessSupervisor with bounded CPU/memory/output/time, cancellation and process-tree cleanup.
- One active desktop control lease per interactive session by default; concurrent controllers are denied unless a future arbitration protocol is approved.
- If session ownership, focus, app/window identity or user-presence state becomes uncertain, stop and return BLOCKED.
- Never elevate privileges to bypass OS permission or integrity boundaries.
- Timeout/cancellation/worker crash with uncertain side effects => BLOCKED and require fresh human reconciliation before retry.
- No automatic retry for non-idempotent actions. Any retry requires fresh observation and policy re-evaluation.
- Accessibility provider missing/incomplete, stale ref, ambiguous target, unexpected modal/dialog or unsupported control => UNSUPPORTED/BLOCKED; no coordinate fallback.
- Do not claim background/non-interference unless measured for the exact operation, OS and app.

## 10. Task verification and status mapping
Every state-changing action follows: OBSERVE → RESOLVE → POLICY CHECK → ACT → OBSERVE AGAIN → VERIFY POST-CONDITION.
- PASS: all declared post-conditions pass, evidence is complete, and no safety invariant was violated.
- FAIL: a post-condition is observed false or a deterministic operation failure is established.
- BLOCKED: permission/session/identity/observation/evidence/verification is unavailable or side effects are uncertain.
- UNSUPPORTED: requested operation/control is outside declared capability profile.
- TIMEOUT/CANCELLED: execution ended without sufficient evidence; task cannot be PASS.

This supplements the existing workflow verification principle; it does not modify the LOCKED browser workflow state machine.

## 11. Versioning and compatibility
- This document is DRAFT 0.1.0 and not a locked implementation contract.
- The three existing LOCKED contracts remain unchanged.
- Before lock: Owner review, security/threat review, implementation feasibility review, and test matrix approval are required.
- Any semantic change after lock requires a new version, migration notes, compatibility tests and Work Manifest update.
- Backend replacement must not change W10 public semantics without a contract version change.

## 12. Open decisions for review
1. Whether v0.1 should permit desktop.focus, given focus-stealing implications.
2. Whether one interactive user session may be controlled while a human is actively using it, or whether pilot requires a dedicated test session.
3. Whether raw accessibility snapshots may be retained temporarily, and the exact retention window.
4. Which non-sensitive Windows test application and controls form the acceptance fixture.
5. Whether W10 invokes candidate via a narrow CLI/library wrapper or internal MCP stdio. Direct exposure to callers is prohibited either way.

## 13. Current disposition
DRAFT FOR REVIEW. No dependency selection, install, source code, runtime, MCP registration, host operation, test, benchmark or release is authorized by this document. Work 10 remains ACTIVE — NOT RELEASED.
