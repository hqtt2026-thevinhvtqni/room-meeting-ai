# WORK 52 — ROOM Universal AI Communication & Orchestration

- **Work ID:** 52
- **Status:** ACTIVE / DESIGN-FIRST / NOT RELEASED
- **Authority:** Vinh > Xu > Agent
- **Coordinator:** Xu (AI-01, Planner)
- **Opened:** 2026-10-23 (UTC+07:00)

## Purpose
Design a provider-neutral communication and orchestration layer for all AI agents in ROOM-HOP. It must not depend on one model vendor, coding agent, UI, or transport protocol.

## Scope
1. Trace current ROOM-HOP architecture and reuse components before proposing new services.
2. Define a common A2A task contract: identity, capabilities, input/output schema, lifecycle, events, cancellation, timeout, retries, approvals, provenance and evidence.
3. Define provider/runtime adapters. Initial feasibility targets are Codex App Server/SDK and Qwen Code ACP or supported service interfaces. Other providers are capability-gated.
4. Integrate with existing Core/Gateway/Agent Runtime, MCP 8030 and Sandbox boundaries.
5. Support auditable Coder → Tester → Reviewer → Handoff.
6. Define security, reliability, conformance and E2E acceptance tests.

## Non-goals
- Do not replace or duplicate ROOM Core, MCP 8030, Work 28, Work 30 or Work 51.
- Do not make Codex, Qwen, ACP, MCP or any vendor API the universal internal contract.
- No automatic Git commit, push, merge or release by agents.
- No production-code changes before architecture tracing and design gates.

## Architecture constraints
- Core :8000 remains the source of truth and must never be created inside Sandbox.
- Dashboard :3000 remains render-only.
- Sandbox is the AI build zone; working source is read-only to build agents.
- Provider adapters translate between the common contract and provider-specific interfaces.
- The orchestrator owns task state, correlation IDs, policy checks, event normalization, observability and handoff—not model inference.
- Missing provider capability must be declared explicitly, not simulated.

## Acceptance gates
- **G0 Discovery:** existing services, Works and files traced; no duplicate architecture.
- **G1 Contract:** schemas, lifecycle, error model, cancellation and event ordering specified.
- **G2 Adapter:** at least two runtimes can be discovered and invoked through the same contract, or unsupported capability is evidenced as BLOCKED.
- **G3 Sandbox safety:** scoped execution, enforced permissions, no unauthorized source/Git mutation.
- **G4 E2E:** task dispatch, progress events, normalized completion/error, independent test and linked evidence.
- **G5 Handoff:** docs, logs, tests, limitations and next step verified.

Use READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF. Status vocabulary: DONE / PASS / DECISION / BLOCKED / CHƯA XÁC MINH. Design intent is not implementation evidence.
