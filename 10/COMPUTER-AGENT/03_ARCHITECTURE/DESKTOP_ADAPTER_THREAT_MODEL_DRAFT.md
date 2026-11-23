# W10 DESKTOP ADAPTER — THREAT MODEL
- Document ID: W10-DESKTOP-THREAT-MODEL-DRAFT-20261123
- Version: 0.1.0-draft
- Status: DRAFT — REVIEW REQUIRED
- Date: 2026-11-23 (UTC+07:00)
- Owner / final authority: Vinh
- Coordinator: Xu (AI-01)

## 1. Assets to protect
A. OS user session, desktop focus and active applications.
B. Files, clipboard, credentials, messages, financial and personal data exposed by accessibility trees.
C. ROOM-HOP identity, authorization grants, Core credentials and Work boundaries.
D. W10 worker processes, logs, evidence, binaries and pinned dependency integrity.
E. Human intent and approval integrity; prevention of unintended external side effects.

## 2. Trust boundaries
TB-1: Remote AI caller ↔ ROOM-HOP authenticated route.
TB-2: ROOM-HOP authorization ↔ W10 loopback Agent API.
TB-3: W10 Runtime/Policy ↔ ProcessSupervisor worker.
TB-4: Desktop Adapter ↔ native OS accessibility provider and interactive session.
TB-5: Desktop observations/evidence ↔ model, journal, dashboard and storage.
TB-6: W10 ↔ other Works (W24, W112, W14, W113).

## 3. Threats and controls

| Threat | Example / impact | Required control |
|---|---|---|
| T01 Caller impersonation | Untrusted agent invokes desktop actions | Authenticated identity, task-scoped authorization, deny by default |
| T02 Privilege escalation | Worker inherits admin token or elevates | Dedicated least-privilege account; record integrity level; reject unexpected elevation |
| T03 Tool/prompt injection | Malicious UI text instructs AI to exfiltrate data or run commands | Treat UI content as untrusted data, never as policy; no shell capability |
| T04 Cross-app data exposure | Snapshot includes unrelated windows or sensitive fields | Exact app/window scope, minimal tree, redaction, no global desktop dump |
| T05 Stale/forged ref | Old ref clicks a different control | Observation-bound opaque refs, short TTL, immediate revalidation |
| T06 Ambiguous target | Multiple matching buttons or deceptive labels | Exactly-one resolution; ambiguity blocks; no fuzzy guessing |
| T07 Focus/session race | Human or another agent changes active window | Exclusive session lease, focus/window recheck before action, stop on uncertainty |
| T08 Unintended external action | Click sends email, submits order or deletes record | v0.1 deny external/irreversible actions; future operation-specific approval |
| T09 Data exfiltration | Clipboard/snapshot/log leaks credentials | No clipboard API in v0.1; redaction; private evidence; retention/access policy |
| T10 Dependency compromise | Tampered binary/package | Pin release and SHA-256; verify provenance/license; controlled update process |
| T11 Worker escape/resource exhaustion | Child process survives cancellation or floods output | ProcessSupervisor containment, bounded output/time/resources, process-tree cleanup |
| T12 OS/provider bypass | Unsupported API silently falls back to global input | Fail closed; no coordinate/OCR fallback |
| T13 Audit tampering | Missing or rewritten action evidence | Append-only journal/evidence, hashes, actor and timestamp, read-back verification |
| T14 Cross-Work privilege confusion | W10 bypasses W24/Core or leaks to W113 dashboard | Preserve ownership boundaries; no direct Core auth bypass; W113 receives approved summaries only |
| T15 Human safety/conflict | AI moves focus or types while person works | Dedicated test session for pilot; visible control indicator/lease; immediate cancel/revoke |

## 4. Abuse cases to test
- Malicious app content asks agent to reveal clipboard or open a terminal.
- Ref from one observation is replayed after a dialog/window change.
- Two AI callers race to control the same desktop session.
- Target label is duplicated or visually deceptive.
- Application shows an unexpected confirmation, authentication or permission dialog.
- Worker is cancelled during typing/clicking and leaves uncertain side effect.
- App runs at higher integrity than worker, or worker unexpectedly has administrator privileges.
- Accessibility tree includes private data from a neighboring/background window.
- Backend package/binary digest differs from approved pin.
- Dashboard/logging path accidentally receives raw snapshot or clipboard data.

## 5. Minimum security acceptance criteria
1. All T01–T15 controls have an implementation owner and test evidence before pilot PASS.
2. Caller cannot access raw CLI, shell, unrestricted MCP or OS APIs.
3. Least privilege and exact app/window scope are demonstrated.
4. Ref replay, stale ref, ambiguous target and session race all fail closed.
5. UI text cannot change authorization or policy.
6. External/irreversible and privileged-system operations are rejected in v0.1.
7. Raw sensitive data is redacted/minimized and not exposed to dashboard or unrelated Works.
8. Cancellation and worker cleanup are evidenced; uncertain effects remain BLOCKED.
9. Binary/version digest is pinned and verified.
10. Every action is auditable and every task outcome is backed by fresh post-condition evidence.

## 6. Residual risks / limitations
- Accessibility providers expose inconsistent or incomplete semantics across applications and OS versions.
- Some actions may affect focus or physical input even when no screenshot is used.
- UI text and accessibility labels can be adversarial or misleading.
- A dedicated test session reduces but does not eliminate OS/application side effects.
- This threat model must be reviewed against the actual Windows host, W10 worker design and ROOM-HOP authorization path before implementation.

## 7. Review disposition
DRAFT FOR REVIEW. Threat model does not authorize dependency installation, host access, runtime execution, code changes or release.
