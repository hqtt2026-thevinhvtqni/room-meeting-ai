# WORK 104 — AI Usage & Evidence Tracking

- Work ID: 104
- Name: AI-USAGE-EVIDENCE-TRACKING
- Status: ACTIVE — PLAN / INITIALIZATION
- Owner: Vinh (business authority); Xu (AI-01 GPT CEO / coordination)
- Technical lead: Cla (AI-03 CTO), implementation assignment pending
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/104-ai-usage-evidence-tracking
- Created: 2026-10-24
- Principle: Evidence First + Necessary and Sufficient Conditions

## Purpose
Build a shared ROOM-HOP capability to record AI identity, Work/task attribution, provider/model usage, cost, tool activity, outputs, and verifiable acceptance evidence across heterogeneous AI providers.

## Scope
1. Inventory current AI invocation paths, provider adapters, ROOM/MCP 8030 tools, Core :8000 boundaries, and existing usage/evidence storage.
2. Define a provider-neutral event schema and usage ledger with explicit provenance and confidence.
3. Capture task lifecycle, tool calls, provider-reported token usage, cost calculation inputs, errors/retries, artifacts, tests, and acceptance evidence.
4. Provide query/report APIs and a dashboard-ready data contract.
5. Verify with deterministic tests and end-to-end evidence before declaring PASS.

## Hard boundaries / non-goals
- Never create a second Core or place Core :8000 inside Sandbox.
- Do not force every provider through one proxy unless discovery justifies it.
- Never claim exact tokens/costs when data is unavailable; label estimates and missing data explicitly.
- Token volume, activity count, and AI self-report are not proof of completion.
- Fine-tuning from raw logs is excluded; it requires curation, privacy review, and evaluation.
- File creation or a dashboard alone is not implementation PASS.

## Delivery sequence
READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.

## Acceptance gates
- G0 Discovery: invocation paths and data sources inventoried with evidence.
- G1 Design: schema, identity, task correlation, pricing provenance, privacy and failure policy approved.
- G2 Implementation: instrumentation and persistence work with fail-safe behavior.
- G3 Verification: unit/integration/retry/idempotency/missing-usage/reconciliation tests pass.
- G4 E2E: trace AI identity and Work/task to usage, cost, artifact, and independent acceptance evidence.
- G5 Handoff: docs, operations, limitations and residual blockers recorded.

## Current decision
Start with architecture and discovery, reusing ROOM-HOP/MCP 8030 and existing provider adapters. LiteLLM or custom FastAPI proxy is an option only if evidence shows it is needed.
