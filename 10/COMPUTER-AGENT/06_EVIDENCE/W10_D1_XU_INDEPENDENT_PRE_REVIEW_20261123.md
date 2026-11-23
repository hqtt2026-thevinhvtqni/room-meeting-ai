# W10 D1 — Xu Independent Pre-Review (Internal)
- Document ID: W10-D1-XU-PRE-REVIEW-20261123
- Version: 0.1.0
- Status: INTERNAL PRE-REVIEW — NOT A SUBSTITUTE FOR KA/CLA/QW/NU REVIEWS
- Reviewer: Xu / AI-01
- Date: 2026-11-23 (UTC+07:00)
- Scope: Desktop Adapter Capability Contract Draft, Threat Model Draft, D1 Review Brief, PC Host Capability Contract, and the three LOCKED browser contracts.

## 1. Overall disposition
D1 is a sound conservative starting draft. It preserves the Browser Adapter boundary and the three LOCKED browser contracts, uses observation-bound references, denies S2/S3 in v0.1, requires post-condition verification, and prohibits raw CLI/shell exposure. However, it is NOT ready to lock yet. The following P0/P1 clarifications should be resolved before Owner approval. This is a document review only; no implementation or test has been performed.

## 2. Findings

### P0 — F01: Define authorization binding end-to-end
The draft says an approved ROOM-HOP identity/authorization route invokes the loopback W10 API, while W24 owns Core authorization and authenticated PC transport. It does not yet define the exact authorization artifact W10 verifies, issuer/audience/subject/Work binding, operation scope, expiry, nonce/replay protection, revocation behavior, or how the loopback caller identity is cryptographically bound to that grant.
Required: Specify a signed/task-scoped grant contract or explicitly reference the canonical W24/W112 contract by version and fields. W10 must reject missing, expired, replayed, wrong-Work, wrong-session, wrong-app, or wrong-operation grants. Do not duplicate ownership or implement a second auth system inside W10.

### P0 — F02: Prevent semantically destructive clicks before execution
The contract denies S2 external/irreversible actions, but the generic desktop.click operation can click a control whose effect is Send, Delete, Purchase, Submit, Publish, or permission change. Post-action verification is too late to prevent the side effect.
Required: Define a pre-action risk classification and deny rule based on target semantics, app/action context, and policy metadata. If classification is unknown or the target can trigger an external/irreversible effect, block before click. Explicit human confirmation must not be treated as blanket permission in v0.1; keep S2 denied.

### P1 — F03: Resolve the interactive-session policy
The capability contract leaves open whether a human may actively use the controlled session; the threat model says a dedicated test session is required for pilot. These statements should be reconciled.
Recommendation: Pilot uses a dedicated, non-personal, non-admin interactive test account/session with visible control indicator and immediate revoke/cancel. Human-active shared-session control remains unsupported until arbitration and focus safety are independently reviewed.

### P1 — F04: Specify observation-data retention and redaction
The draft requires minimization and bounded retention but does not state retention duration, deletion trigger, access roles, encryption-at-rest requirement, or redaction-failure behavior.
Required: Define default no-raw-tree persistence; ephemeral in-memory processing; explicit allow-list of fields; fail closed if secret/PII redaction cannot be assured; evidence retains hashes/metadata only. If raw snapshot capture is needed for debugging, require separate per-run authorization, private storage, short fixed TTL and access audit.

### P1 — F05: Pin candidate backend and provenance before D2
The draft remains backend-neutral but names vercel-labs/agent-desktop as candidate. No exact release/commit, binary/library digest, license/provenance verification result, supported OS/provider matrix, or maintenance/security review is attached to D1.
Required: D1 can remain backend-neutral, but D2 entry criteria must require exact immutable source/release pin, SHA-256, license and dependency inventory, provenance, and supported platform matrix. No install based on a floating branch/latest tag.

### P1 — F06: Define ProcessSupervisor integration contract
The draft says every worker is contained by ProcessSupervisor, but does not define process ownership, child process discovery, environment inheritance, desktop-session handle passing, cleanup confirmation, or the BLOCKED state when descendants survive.
Required: Reuse the existing W10 ProcessSupervisor and its verified lifecycle semantics. Desktop worker must not create an independent untracked process tree. Record PID/process-tree identity, bounded resources/output/time, cancellation, cleanup evidence, and do not release the session lease until cleanup is confirmed.

### P1 — F07: Clarify operation semantics and result mapping
desktop.focus is in the operation table but also listed as an open decision. desktop.close_session needs precise definition of a W10-owned session versus closing an application/window. The result envelope says action-level status is success/fail/blocked/unsupported/timeout/cancelled, while task-level PASS/FAIL/BLOCKED mapping is separate.
Required: Mark focus as excluded from v0.1 unless explicitly approved; define close_session as closing only the adapter-owned control session/worker, never app/window or OS user session; formalize action-level status versus task-level workflow state and ensure only Workflow Verification can set PASS.

### P1 — F08: Add negative test matrix traceability
Threat model lists T01–T15 and abuse cases, but no mapping from each threat to a named test, expected status, evidence artifact, and owner.
Required: Create a traceability matrix before D2: threat/control → test ID → fixture → expected outcome → evidence → responsible reviewer. Include stale/replayed refs, ambiguous controls, misleading labels, cross-window leakage, privilege mismatch, session race, malicious UI prompt, cancellation during side effect, package digest mismatch, redaction failure, and dashboard/log leakage.

### P2 — F09: Make UI content explicitly untrusted in the capability contract
Threat model T03 handles prompt injection, but the capability contract should explicitly state that labels, accessible names, help text, notifications and document contents are data only and cannot grant permission, alter policy, or expand scope.

### P2 — F10: Clarify cross-platform scope
The candidate agent-desktop backend uses OS-specific accessibility providers. D1 should state that the first pilot target is Windows only (if that is the intended scope), with macOS/Linux capability profiles unsupported until separate provider and security tests pass. Do not imply cross-platform parity from an abstract contract.

## 3. Consistency with existing W10 contracts
- ACTION_CONTRACT: additive logical desktop operations are acceptable if mapped through a separate adapter namespace; do not mutate browser action meanings or silently reinterpret browser selectors.
- WORKFLOW_CONTRACT: desktop action success is not task PASS; require VERIFYING and fresh post-condition evidence. The existing browser state machine remains LOCKED.
- SAFETY_POLICY: the desktop v0.1 deny-by-default policy is stricter than generic destructive-action approval and should remain stricter; do not inherit browser retry behavior for uncertain desktop side effects.
- PC_HOST_CAPABILITY_CONTRACT: reuse ProcessSupervisor and host security assumptions, but do not confuse allow-listed host file/pytest/PowerShell operations with desktop UI authorization. The host capability API is not permission to expose a desktop shell or raw OS APIs.

## 4. Recommended D1 decision
Return the draft for targeted revision on F01–F08 before lock. F09–F10 should be included as explicit clarifications. No code, dependency install, host operation, MCP registration, benchmark, or D2 pilot should start from this pre-review.

## 5. Review limitations
This is Xu's independent document-level pre-review based on the Sandbox contents read in this session. It is not an implementation review, host test, security penetration test, backend due diligence, or approval from Ka, Cla, Qw, Nu, or Vinh.

## 6. Required next step
Revise the D1 contract/threat model and review brief to include the findings and assign reviewer-specific questions. Obtain actual Ka/Cla/Qw/Nu feedback through a verified agent communication channel. Then update the canonical Biên bản and Nhật ký and submit the revised D1 package to Vinh for the lock decision.