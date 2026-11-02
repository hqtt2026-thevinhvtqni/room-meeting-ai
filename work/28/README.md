# Work 28 — MCP Tooling Platform

**Current authority:** Vinh  
**Coordinator / technical decision owner:** Xu  
**Approved team:** Xu, Vi, Ka, An only  
**Status:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED  
**Execution Gate:** CLOSED

## Canonical location

- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/28-mcp-tooling-platform`
- Work path: `work/28/MCP-8020-TOOLING-PLATFORM/`
- Manifest: `00_ROOT/WORK_MANIFEST.md`
- Official minutes: `00_ROOT/BIEN_BAN.md`
- Master plan: `01_PLAN/WORK28_MASTER_EXECUTION_PLAN_V2.0.md`
- Architecture decision: `03_ARCHITECTURE/WORK28_ARCHITECTURE_DECISION_V2.md`
- Work-wide journal: `00_ROOT/NHAT_KY_THI_CONG.md`
- Document register: `00_ROOT/WORK_DOCUMENT_REGISTER.md`

## Product mission

Deliver a secure, typed and auditable MCP tooling platform across discovery, tool registry/contracts, Build/Verification, a clean Runtime MCP rebuild, Core-authorized execution through Execution Host :8031, evidence and end-to-end verification.

## Architecture guardrails

- Core :8000 is the sole authorization and application authority.
- MCP Build/Verification :8030 remains the supported build lane.
- Historical MCP :8020 listener is quarantined and **DO NOT USE**. Do not probe, restart, activate, modify or route traffic to it.
- Runtime MCP is a separate clean rebuild; no reuse of the historical listener/process/state.
- Execution Host :8031 is the approved execution boundary. No arbitrary shell, direct Workspace/DB access or Core bypass.
- Job Object process-tree containment and OS sandbox isolation are separate controls; neither may be claimed without its own evidence.

## Delivery workflow

READ → TRACE → ANALYZE → DECIDE → BUILD → RUN → VERIFY → HANDOFF.

GitHub is the canonical source and document store. GitHub Actions is the primary CI evidence lane. Sandbox/MCP 8030 is supporting verification only. Preserve legacy evidence; do not treat old AI handoffs as current assignments. Co is excluded.

See the manifest and master plan for roles, work packages, acceptance gates and release requirements. Work 28 is not released until all required gates pass.
