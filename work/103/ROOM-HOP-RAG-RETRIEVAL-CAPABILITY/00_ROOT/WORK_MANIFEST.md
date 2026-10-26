# WORK MANIFEST — 103

Work ID: 103
Work Name: ROOM-HOP-RAG-RETRIEVAL-CAPABILITY
Display Name: 103 - ROOM-HOP-RAG-RETRIEVAL-CAPABILITY
Status: ACTIVE
Lock: NO
Created: 2026-10-15 (UTC+07:00)
Authority: Vinh
Coordinator: Xu
Technical execution: Sandbox-first; do not claim MAIN SOURCE integration without approved source changes and live evidence.

## Purpose
Build an evidence-grounded Retrieval-Augmented Generation (RAG) capability for ROOM-HOP, reusable by Work 91 Harness and other authorized Core capabilities.

## Relationship to existing Works
- Work 91: Harness Engineering Audit owns the broader harness contract; Work 103 owns the focused retrieval capability and its acceptance evidence.
- Work 28: MCP :8020 tooling platform owns MCP tool schemas/adapters.
- Core :8000 remains the single source of truth.
- Work 99: registry and entry gate.

## Non-negotiable architecture
AI/Agent -> MCP :8020 -> Core :8000 -> approved retrieval service/repository.
No direct AI -> filesystem/database access; no Core 2; no independent RAG port; Dashboard :3000 remains render-only.
Start with source-aware metadata/lexical retrieval. Add embeddings/vector DB only when evaluation shows a measurable need and the decision is recorded.

## Current status
ACTIVE / INITIAL BUILD IN SANDBOX. Work creation is confirmed. Initial artifacts are not yet runtime-tested or integrated with MAIN SOURCE. No E2E PASS is claimed.

## Build loop
READ -> TRACE -> ANALYZE -> DECIDE -> BUILD -> VERIFY -> FIX -> RETEST -> HANDOFF.
Every implementation/test result must be recorded in 06_EVIDENCE. Never claim PASS without execution evidence.
