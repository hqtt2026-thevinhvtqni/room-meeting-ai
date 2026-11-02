# WORK MANIFEST — WORK 28

- **Work ID:** 28
- **Work name:** MCP Tooling Platform
- **Canonical path:** `work/28/MCP-8020-TOOLING-PLATFORM/`
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Branch:** `work/28-mcp-tooling-platform`
- **Status:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED
- **Execution Gate:** CLOSED
- **Authority:** Vinh
- **Coordinator and technical decision owner:** Xu
- **Last governance update:** 2026-11-03

## Mission

Build and verify a secure, reusable MCP tooling platform for ROOM-HOP. The platform must support the complete controlled lifecycle from discovery and planning through implementation, tests, review, evidence, and release handoff. Core :8000 remains the sole authorization and application authority. The platform must not create a parallel authority or unrestricted execution path.

## Approved team — exactly four AI participants

| AI | Role | Accountability |
|---|---|---|
| Xu | Coordinator / architecture / technical decisions | Owns scope, architecture, prioritization, task coordination, decision log, integration and acceptance recommendation |
| Vi | Implementation lead | Implements and fixes approved Work 28 scope end-to-end; maintains code, tests and implementation evidence |
| Ka | Independent architecture and security reviewer | Reviews boundaries, contracts, threat model, implementation diffs and release risks independently |
| An | Independent QA / verification | Designs and runs tests, reproduces results, checks CI and verifies acceptance evidence |

**Co is excluded from Work 28**: no assignment, implementation, review, approval or coordination. No fifth AI may be added without Vinh's explicit decision. Historical documents authored by other agents remain evidence only and do not grant current participation.

## Source-of-truth and execution rules

1. GitHub branch `work/28-mcp-tooling-platform` is the canonical source for code, controlled documents and reviewable changes.
2. Reconcile the current branch HEAD and affected file SHAs before every write. Do not overwrite concurrent changes.
3. GitHub Actions is the reproducible CI evidence lane. Sandbox/MCP 8030 is a supporting build/verification environment; it is not a competing source of truth.
4. Record commit SHA, workflow run, exact test scope, exit/result, and any divergence. CI PASS is not runtime E2E PASS.
5. Do not claim an AI has received or executed an assignment unless there is an observable task acknowledgement or execution artifact. The role assignment in this manifest is governance, not proof of dispatch.
6. All work follows READ → TRACE → ANALYZE → DECIDE → BUILD → RUN → VERIFY → HANDOFF. Keep the canonical Work journal current.
7. Preserve historical reports. Classify them as evidence, review, test output, decision, handoff or archive; do not create competing official minutes or journals.

## Architecture boundaries

- **Core :8000:** sole source of authorization, Work identity/context and application policy.
- **MCP Build/Verification :8030:** remains the supported Build/Verification MCP lane.
- **Runtime MCP:** rebuild as a separate, new Runtime MCP target. The historical MCP :8020 listener is quarantined and DO NOT USE; never probe, restart, activate, modify or route traffic to it.
- **Execution Host :8031:** approved execution boundary only; it must enforce the Core-authorized contract and OS-level containment. No MCP-to-arbitrary-shell path.
- No direct Workspace/DB access, Core bypass, duplicate Core/runtime authority, fail-open execution, fake handlers or placeholder PASS responses.

## Canonical Work records

- Official minutes: `00_ROOT/BIEN_BAN.md`
- Master plan: `01_PLAN/WORK28_MASTER_EXECUTION_PLAN_V2.0.md`
- Architecture decision: `03_ARCHITECTURE/WORK28_ARCHITECTURE_DECISION_V2.md`
- Work-wide execution journal: `00_ROOT/NHAT_KY_THI_CONG.md`
- Document register and evidence classification: `00_ROOT/WORK_DOCUMENT_REGISTER.md`
- Technical evidence: `06_EVIDENCE/`
- AI review / patch / validation handoffs: `10_AI_DEBUG_HANDOFF/` (supporting artifacts only, not official minutes or journal)

## Acceptance and release

Work 28 remains NOT RELEASED until all required contracts, tool registration, security boundaries, Linux and Windows tests, Core-authorized end-to-end execution, independent review, evidence traceability, deployment/rollback and operational handoff are verified. The execution gate remains CLOSED until the release criteria are met and Vinh's approval is recorded where required.

**No document write, source edit, unit test, or CI run alone constitutes product acceptance.**
