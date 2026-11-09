# WORK MANIFEST
- Work ID: 112
- Work Name: ROOM-HOP-INTEGRATION-CONTRACTS-AND-EVIDENCE-ORCHESTRATION
- Status: ACTIVE — DISCOVER / DEFINE
- Authority: Vinh
- Executive Coordinator: Xu / xu
- Created: 2026-11-09
- Canonical source: hqtt2026-thevinhvtqni/room-meeting-ai; GitHub main is source of code truth; Sandbox is working/verification zone.
- Purpose: Define and verify cross-Work integration contracts for the unified ROOM-HOP machine under W70.
- Non-goals: Do not rebuild W70 lifecycle engine, W32 CI engine, W33 evidence hub, W52 communication orchestration, W16 workflow engine, W37 Core, W38 Gateway, W39 Build MCP, W14 execution-host ownership, or W0000 governance registry.
- Required reading: W70 governing documents and relevant source Work manifests, decisions, journals and contracts before every task.
- State rule: No PASS/DONE without reproducible evidence. Journal every measurement, test, decision and blocker.


## 2026-11-09 — W70 lifecycle structure alignment (structural baseline)
- W112 adopts the canonical top-level lifecycle set from W70 DOC-001: 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE and DASHBOARD.
- 05_BUILD uses the W70 child set: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE and 10_AI_DEBUG_HANDOFF.
- Canonical architecture documents are stored under 03_ARCHITECT. W112 DOC-001 is placed there.
- Initial scaffold folders at Work root (01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE) are legacy paths, not canonical lifecycle phases. Their intended mapping is respectively 05_BUILD/01_ORIGINAL, 05_BUILD/02_EXTENSION, 03_ARCHITECT, 05_BUILD/04_CODE, 05_BUILD/05_TEST, 05_BUILD/06_EVIDENCE and 05_BUILD/07_RELEASE.
- Existing legacy folders are preserved; no files were moved or deleted. Their contents must be inventoried and inbound links mapped before any retirement. The empty/duplicate 03_ARCHITECTURE root is not a second architecture source.
- Standard directories and .gitkeep placeholders have been created in Sandbox. This is STRUCTURAL SCAFFOLDING ONLY; it does not mean any lifecycle phase has started, passed a gate, or completed.
- Physical legacy-path retirement and full DOC-055-equivalent register/link audit remain OPEN.
