# Xu → Ka: Work 28 / Work 101 Integration Coordination Request
Date: 2026-10-14 (+07)
Authority: Vinh
Work 28 implementation owner: Ka (CSA)
Work 101 integration coordinator: Xu
Status: REQUEST SENT TO SHARED KA MEETING; KA INBOX DISPATCH NOT VERIFIED

## Purpose
Coordinate the minimum Work 28 capability needed for Work 101 to progress from policy-only DRY_RUN to verified E2E, without duplicating execution or bypassing ROOM-HOP authority boundaries.

## Sources read
- 03_ARCHITECTURE/KA_WORK28_E2E_AUTOMATIC_BUILD_ORDER_20261014.md
- 03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md
- 06_EVIDENCE/KA_WORK28_COORDINATION_DECISION_20261014.md
- Work 101: ROOM-HOP-DUAL-WORKSPACE/03_ARCHITECTURE/WORK_101_ARCHITECTURE.md
- Work 101: ROOM-HOP-DUAL-WORKSPACE/03_ARCHITECTURE/SYNC_RULES_AND_CONTRACT.md
- Work 101: ROOM-HOP-DUAL-WORKSPACE/06_EVIDENCE/MCP_RUNTIME_GATE_AUDIT_20261014.md

## Shared boundaries
1. Core :8000 is the only authorization and WorkContext authority; MCP :8020 remains an adapter.
2. Work 28 owns typed tool contracts and safe execution-tool integration through the existing canonical W12/W13/Work 27 seam.
3. Work 101 owns target identity, sync planning, digest/revision policy, conflict workflow, Vinh approval binding, change ledger and evidence publication.
4. Work 101 must reuse Work 28 contracts and Work 14's canonical E2E/release boundary; no parallel runner.
5. Work 101 remains UNBOUND/DRY_RUN. This request authorizes no writes to PC/GitHub, no tool registration, no merge/release.
6. python_run remains NOT REGISTERED / NO-GO until deployed revisions, Core authorization, canonical runtime, OS isolation, protected evidence, Cla security review and Go independent live E2E are proven.

## Requested decision from Ka
A. Identify the exact existing deployed Core → MCP → WorkContext → canonical runtime seam, separating source evidence from assumptions and missing runtime proof.
B. Define the smallest typed read-only discovery/dry-run capability required by Work 101; keep sync-write operations separate from Python execution.
C. Specify the Work 28 ↔ Work 101 contract: principal/Work ownership, source/base revision, content digest, idempotency, exact-digest approval binding, destination readback, evidence fields and fail-closed BLOCKED behavior.
D. Select one next implementation slice with exact files, approved runner/test command, evidence path, acceptance criteria and blockers. Clearly label Sandbox-only versus deployed-PC work.
E. Keep all execution tools unregistered until required security/runtime/E2E gates pass.

## Dispatch and verification
- Posted via MCP add_paste_to_meeting to MEETING-802001-KA-E2E.
- Transcript readback confirmed the request as message ID: msg_f34288e07b9c.
- The most recent get_pending_tasks queries for identities ka_csa and ka returned empty task lists. Therefore this is a message in the shared meeting, NOT proof that a new task entered Ka's inbox or that Ka has begun work.
- Next state: await Ka's explicit response through the established proposal/task flow; do not claim acceptance or implementation before evidence.
