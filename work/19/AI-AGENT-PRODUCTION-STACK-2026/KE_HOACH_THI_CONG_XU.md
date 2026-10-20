# KẾ HOẠCH THI CÔNG — XU — WORK 19

- Work ID: 19
- Owner/decision maker: Vinh
- Plan owner/coordinator: Xu (AI-01)
- Updated: 2026-10-20 UTC+07:00
- Status: PLAN RECORDED — not accepted

## Sequence
1. G0 READ: inventory Sandbox, GitHub, governance, code, tests and evidence. Record sources and unknowns.
2. G1 TRACE: choose one approved request path and trace AI/MCP :8020 → Core :8000 → runtime/service → artifact.
3. G2 ANALYZE & DECIDE: compare actual evidence against the six stack layers and six readiness properties; record decisions and risks.
4. G3 BUILD: implement only approved gaps, in the designated Work/branch, with contracts and tests.
5. G4 VERIFY: run unit, contract, integration and applicable E2E tests; capture commands, exit codes, logs and artifacts.
6. G5 OBSERVE & EVALUATE: inspect logs/correlation, define evaluation cases and measure latency, reliability, resource use and cost when data exists.
7. G6 DATA & RECOVERY: document data ownership, backup, retention and restore requirements; distinguish plan from tested restore.
8. G7 HANDOFF: report outcomes, evidence, unresolved risks, blocked gates and next decision.

## Gate rules
- No PASS without evidence that directly supports the acceptance criterion.
- No change to protected Core or frozen baseline without required authorization.
- No merge/push to protected branch as part of this synchronization task.
- Do not add RAG/vector DB, Kubernetes, A2A or multi-provider complexity without a concrete use case.
- Update this canonical plan rather than creating competing plan files.
- All timestamps use Vietnam time UTC+07:00.

## Immediate next action
G0 READ: reconcile the Sandbox source documents with this GitHub mirror and record any content differences before proceeding to architecture or code changes.

## Work log pointer
Record all activity in NHAT_KY_HOP_THI_CONG.md.
