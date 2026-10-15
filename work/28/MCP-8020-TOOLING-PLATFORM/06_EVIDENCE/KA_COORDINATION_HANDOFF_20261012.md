# KA COORDINATION HANDOFF — WORK 28 — 2026-10-12
Status: ACTIVE / NOT LOCKED
Coordinator: Ka (CSA), delegated by Vinh
Repository policy: MAIN SOURCE remains read-only; Sandbox is the build zone. No commit/merge/push was made.

## Read this baseline first
1. `06_EVIDENCE/KA_WP0_SOURCE_BOUNDARY_MAP_20261012.md`
2. `03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md`
3. `03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`
4. `04_CODE/tool_contracts.py`
5. `05_TEST/test_tool_contracts.py`
6. `05_TEST/WORK_28_TEST_PLAN.md`
7. `06_EVIDENCE/KA_CONTRACT_HARDENING_CHECKPOINT_20261012.md`
8. `06_EVIDENCE/GO_E2E_REVIEW_REPORT_20261011.md`
9. `06_EVIDENCE/CLA_SECURITY_REVIEW_REPORT_20261011.md`

## Current technical decision
NO-GO registering/enabling live execution tools until deployed MCP/Core identity, authenticated principal, Core WorkContext authorization, canonical W12/W13 runtime, OS-level isolation, process-tree cleanup and protected evidence are proven. The alternate `execution_host/server.py` is not an approved shortcut.

## Cla — independent security review (action required)
1. Review contract and blueprint independently, especially `ExecutionOperation` and RUN_TESTS PASS evidence requirements.
2. Evaluate A02–A07, A11–A15, A17–A18 and the earlier S01–S15 findings. Prioritize principal spoofing, caller-supplied `authorized`, cross-Work reads, path race/symlink/reparse points, host secret/network isolation, resource limits, timeout/kill-tree, evidence overwrite/delete and malformed/zero-test summaries.
3. Write `06_EVIDENCE/CLA_AUTOMATIC_E2E_SECURITY_REVIEW_20261012.md`.
4. For each finding provide severity, source path/line if available, expected behavior, evidence and PASS/FAIL/BLOCKED. Distinguish static review from tests actually run; include exact command/output/exit code only when truly executed.
5. Do not overwrite Ka’s artifacts. Security NO-GO is valid without waiting for Ka if a blocker remains.

## Go — independent E2E acceptance (action required after prerequisites)
1. Read the E2E blueprint and Cla’s review.
2. Before executing, evidence deployed MCP/Core SHA, live registered tool list, authenticated principal, Core WorkContext route, canonical runtime identity, OS isolation and protected evidence.
3. When all prerequisites pass, exercise the real MCP entry point through Core and the canonical runtime; run applicable A01–A18 including authorization denial, path/snapshot integrity, zero tests, nonzero exit, timeout/process-tree cleanup, evidence immutability, and baseline → test-only mutation FAIL → patch → rerun PASS in a disposable test Work.
4. Write `06_EVIDENCE/GO_AUTOMATIC_E2E_ACCEPTANCE_20261012.md` with exact commands, run_id, source SHA, runtime build identity, exit codes, stdout/stderr refs, cleanup evidence, evidence readback and per-gate verdict.
5. No direct-runtime-only test, mock, unit test or local Sandbox readback may be called live E2E PASS. If prerequisites are missing, report BLOCKED with the missing proof.

## Ka — ongoing implementation
- Keep hardening contract and tests in Sandbox, perform static/readback checks and maintain honest gate states.
- Obtain read-only deployed PC metadata using `06_EVIDENCE/PC_READONLY_RUNTIME_EVIDENCE_REQUEST_20261012.md`.
- Do not invent route names or wire MCP directly to an alternate execution host.
- Integrate only after Cla security gate and runtime/Core evidence are sufficient; Go independently validates afterwards.

## Current gate state
- Source map: PARTIAL (GitHub snapshot inspected; deployed PC alignment unproven).
- Contract: written/readback verified; tests not executed by an approved runner.
- G3 approved-runner tests: BLOCKED.
- G4 authorization/path/OS isolation: BLOCKED.
- G5 live MCP → Core → canonical runtime → protected evidence: BLOCKED.
- G6 full automatic E2E: BLOCKED.
- Work 28 remains ACTIVE / NOT LOCKED; Vinh retains final authority.
