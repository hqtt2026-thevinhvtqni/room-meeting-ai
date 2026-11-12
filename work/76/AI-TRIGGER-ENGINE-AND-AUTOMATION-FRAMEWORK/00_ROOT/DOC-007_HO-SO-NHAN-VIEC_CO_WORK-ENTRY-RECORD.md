# DOC-007 — HỒ SƠ NHẬN VIỆC VÀ PHẠM VI QUYỀN CO / CO WORK ENTRY RECORD

- Document ID: DOC-007 | Priority: P0 | Read order: 7
- Work: 76 — AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK
- Participant: Co / AI-07 — ROOM implementation coder
- Authority: Vinh (Product Owner); Xu / AI-01 (Lifecycle Orchestrator)
- Assignment ID: ASG-W76-CO-20261113-01
- Assessment time: 2026-11-13 05:23 +07:00
- Status: WORK ENTRY BLOCKED FOR BUILD MUTATION; PREPARATION ALLOWED
- Governing policy: Work 70 DOC-057 Work Entry Gate Standard
- Canonical source: GitHub main / work/76/AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK/

## 1. Delegation and assignment scope

This record formalizes Vinh's explicit delegation that Co has received authority to carry out Work 76 implementation autonomously (AUTO–E2E), without asking Vinh to repeat the authorization.

**Intended scope after Work Entry G0–G5 PASS:**
- Co owns implementation preparation and, after the entry gate is passed, assigned engineering packages WP-76-01 through WP-76-08.
- Co may work on a dedicated Git branch, implement within approved Work 76 scope, run unit/contract/integration/E2E tests, fix defects, capture evidence, and hand off results.
- Co must record every actual action, command/method, timestamp, source revision, output and PASS/FAIL/BLOCKED result in the canonical Work 76 execution log/evidence register.
- Co must synchronize only approved Work 76 artifacts to the appropriate Sandbox/GitHub locations and perform read-back verification.
- Co must not merge to main, release, or claim acceptance; final acceptance remains with Vinh.
- WP-76-07 AI dispatch remains blocked until a real dispatch transport, identity binding, receipt/ACK contract and evidence are verified.
- No use of the retired/disallowed MCP 8020 path. No fabricated dispatch, PC access, Sandbox write, test or E2E evidence.

**Scope exclusions / reserved authority:**
- Xu retains lifecycle coordination, gate reconciliation, cross-Work architecture and approval of architecture/contract changes.
- Core identity, authorization, audit, production configuration and shared runtime contracts are not to be changed unilaterally by Co; prepare a proposal and obtain the required decision first.
- Co cannot grant permissions to itself or other agents, mark its own independent QE as PASS, merge, release or accept the Work.

## 2. Work Package ownership and reviewer nominations

| WP | Scope | Accountable owner | Reviewer | Current status |
|---|---|---|---|---|
| WP-76-01 | Trigger Registry and schema | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-02 | Event Gateway and source validation | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-03 | Scheduler and TIME triggers | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-04 | Typed Condition Evaluator | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-05 | Policy adapter and approval | Co (delegated; entry blocked) | Ka architecture review; Qw QE (both nominations only) | PLANNED |
| WP-76-06 | Orchestration, dedupe and retry | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-07 | Verified AI dispatch adapter | Co for discovery/adapter design only | Xu + Qw (nomination only) | BLOCKED — transport unverified |
| WP-76-08 | Audit and evidence store | Co (delegated; entry blocked) | Qw (nomination; ACK/entry not verified) | PLANNED |
| WP-76-09 | Read-only Dashboard | Xu | An / Qw (nomination; ACK/entry not verified) | IN_REVIEW |

No agent other than Co is recorded as having accepted a Work 76 assignment in the evidence inspected for this assessment. Ka, Qw and An are reviewer nominations, not confirmed ACKs or Work Entry PASS records. Each participant must pass its own G0–G5.

## 3. Work Entry Gate assessment (Work 70 DOC-057)

These are participant-specific Work Entry gates WE-G0…WE-G5. They are not the Work 76 lifecycle gates or implementation/release gates.

| Gate | Assessment | Evidence / reason |
|---|---|---|
| WE-G0 — Work identity | PASS | Work 76 Manifest, Work ID/name, canonical GitHub main path and Sandbox Work ID 76 inspected. Sandbox list and GitHub exact-path reads succeeded. |
| WE-G1 — Applicable procedures | PASS | Read Work 76 Manifest, Discover Brief, architecture, roadmap, Build Register, Evidence Register and verification plan; read Work 70 DOC-057 plus DOC-033, DOC-038, DOC-039, DOC-040, DOC-055 and DOC-056. |
| WE-G2 — Document standards/register | PASS after DOC-008 creation and read-back | Work 70 naming/type-code/storage standards applied; this Work's canonical Document Register is established at DOC-008. |
| WE-G3 — Current state/history | PASS | Read Work 76 execution log, evidence register, build register, manifest and dashboard source status. Current lifecycle remains 01_DISCOVER; runtime not implemented; CI/browser E2E/QE not run; NOT_RELEASED. |
| WE-G4 — Assignment, permissions and dependencies | BLOCKED | Vinh's delegation and the scope/owner boundaries are documented here. However, Co's live runtime identity binding and tool permissions have not been observed from Co's own execution session. Xu's current tool inventory has no Windows Terminal/VS Code Bridge. PC state is therefore NOT VERIFIED, not declared faulty. Sandbox read/list are observed; Co-specific Sandbox write and PC bridge remain unverified. Reviewer ACKs are not evidenced. |
| WE-G5 — Ready to execute | BLOCKED | DOC-057 requires WE-G0–WE-G4 PASS and no unresolved entry blocker. WE-G4 remains BLOCKED; therefore source/code/build mutation is not authorized by this entry record. |

**Work Entry decision:** BLOCKED for code/build mutation. This does not revoke or ask Vinh to repeat the AUTO–E2E delegation. It records that technical entry prerequisites and participant-bound permissions are not yet evidenced. Co may continue READ, TRACE, ANALYZE, PLAN, contract discovery and connection diagnostics that do not mutate protected Work artifacts or runtime state.

## 4. Connection diagnostics and remediation ownership

### PC / VS Code Bridge
- Observed: no local terminal, filesystem, VS Code or PC bridge action is exposed in Xu's current tool inventory.
- Not established: whether Co's separate session has a working bridge; whether Windows/VS Code on Vinh's PC is faulty.
- Owner: Co to report exact bridge tool name, session identity, target repo path, and one read-only proof (for example repository root + current branch + HEAD). Do not ask Vinh to perform broad manual diagnostics.
- Verification: Xu compares reported path/branch/HEAD with the declared repository baseline. No write/test/E2E claim until actual command output is captured.

### Sandbox MCP 8030
- Observed in Xu's session on 2026-11-13: sandbox_list(work_id=76) returned status=ok; sandbox_read_probe on the canonical execution log returned status=ok and the complete log content.
- Not established at assessment start: sandbox_write/append reliability and Co-specific access.
- Owner: Xu verifies the shared service write/read-back path; Co separately verifies access under its own runtime identity before relying on it.
- Verification: append a uniquely timestamped diagnostic entry to the canonical journal, read it back with sandbox_read_probe, and record exact result. Do not use the ordinary sandbox_read result alone as proof when it returns an empty payload.

### Core identity / authorization / audit / AI dispatch
- Core remains the authoritative owner. MCP 8030 is a Work artifact service, not the production dispatcher or authority service.
- No live Core Work-scoped authorization contract or private-session AI dispatch/ACK contract is established by the Work 76 baseline.
- Owner: Xu to trace Core contracts and prepare an architecture decision/adapter gap. WP-76-07 stays BLOCKED until actual transport + receipt/ACK evidence exists.

## 5. Entry exit criteria

WE-G4 may move to PASS only when:
1. Co's runtime identity is resolved to AI-07 in the trusted roster for this Work session.
2. The assignment ID, branch/ref, WP scope, permitted tools/actions, exclusions and expiry/revocation conditions are visible and consistent.
3. Co can demonstrate the actual required GitHub and Sandbox capabilities under its own session; any PC bridge is proven with a read-only command/output if PC execution is required.
4. Required dependencies and reviewer ownership are confirmed; reviewers provide explicit ACK and their own Work Entry records before review/QE tasks.
5. No unresolved conflict exists between Vinh's delegation, Work 70 DOC-057, Work 76 architecture and tool-enforced authorization.

WE-G5 may move to PASS only after WE-G0–WE-G4 PASS, the execution plan and acceptance criteria are explicit, and rollback/risk controls are appropriate for the first implementation slice.

## 6. Non-claims

This record does not claim:
- Co has connected to Vinh's PC or VS Code.
- Co has written to Sandbox or run tests/E2E.
- A Core authorization or dispatch API is live.
- Ka/Qw/An have accepted their nominations or passed Work Entry.
- Any Work 76 lifecycle gate, Build gate, QE gate, acceptance or release has passed.

Recorded by: Xu / AI-01.
