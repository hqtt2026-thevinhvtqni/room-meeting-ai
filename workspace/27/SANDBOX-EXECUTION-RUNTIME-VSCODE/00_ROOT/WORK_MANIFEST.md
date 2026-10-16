# WORK 27 — SANDBOX EXECUTION RUNTIME (VS CODE)

- Work ID: 27
- Status: ACTIVE / NOT LOCKED (status to be reconciled with ROOM-HOP Core)
- Lead Work: Work 27 is the sole implementation owner for Sandbox Execution Runtime.
- Repository: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai
- Working branch: work/27-sandbox-execution-runtime
- Record date: 2026-10-16 (ICT)

## Mission
Build one coherent Sandbox execution runtime that enables an AI build loop to inspect authorized source, edit files in an isolated workspace, execute permitted commands and tests, capture evidence, repair failures within a bounded loop, rerun tests, and hand off an evidence-backed result.

## Work ownership
Work 27 owns architecture, implementation, integration, validation, and handoff for the runtime. Related Works are evidence/contract sources only, not parallel implementation owners:

- Work 28: MCP :8020 tool contract, read/write and readback evidence.
- Work 14: autonomous end-to-end execution and integration evidence.
- Work 12: Execution Host / Work Context contracts and isolation lifecycle evidence.

Reuse existing contracts only after reading and tracing them. Do not fork duplicate implementations merely because a related contract lives in another Work.

## Required operating sequence
READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.

## Initial gates
1. P0 — Read and trace Work 27 requirements, architecture, execution contract and test plan; record related-work dependencies and evidence provenance.
2. P1 — Verify MCP read/write and readback integrity before relying on it for runtime implementation.
3. P2 — Implement and verify Python runtime first. Do not add another runtime until Python has evidence-backed PASS.
4. P3 — Add browser E2E only after the prior runtime gate passes.
5. P4 — Update architecture and handoff documentation from the actual implementation and evidence.

## Safety and evidence requirements
- Runtime execution must remain inside the authorized Work workspace and must not bypass ROOM-HOP Core :8000.
- Use least privilege, non-root execution where supported, resource/time limits, restricted mounts and default-deny network policy where supported.
- Capture command, exit code, stdout/stderr, test reports, relevant diff and artifacts.
- Limit autonomous patch/rerun to at most five attempts. If still failing, stop, preserve evidence and mark ESCALATED_HUMAN.
- PASS requires independently readable evidence; a successful write response or file listing alone is insufficient.

## Current evidence status
This GitHub branch publishes the Work 27 tracking documents and agreed direction. It is not evidence that the runtime has been implemented or tested. The original Sandbox file inventory was visible, but prior MCP readback calls returned empty objects; source contents and P0 completion therefore remain unverified.
