# WORK 28 — AUTO E2E RUNBOOK V2.0

**Document ID:** A2E-W28-20261104-001  
**Execution time:** 2026-11-04 06:18:00 UTC+07:00  
**Authority:** Vinh  
**Coordinator:** Xu  
**Implementation / automation owner:** Vi  
**Independent QA:** An  
**Independent architecture/security review:** Ka  
**Branch:** `work/28-mcp-tooling-platform`  
**Status:** AUTOMATION PRECONDITIONS IMPLEMENTED / DEPLOYED E2E BLOCKED

## 1. Purpose

Make Work 28 execution repeatable from a single GitHub Actions pipeline. Vi continues implementation without waiting for conversational checkpoints. Every push/PR affecting Work 28, Execution Host, Core execution authority, MCP adapter or tests triggers the same automated preflight and regression path. A workflow-dispatch run is available for an explicit rerun.

This runbook supersedes the obsolete participant/owner references in `03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`. The blueprint's technical stages and A01–A18 acceptance cases remain the contract, interpreted under the current Work Manifest and Master Execution Plan V2.0.

## 2. Canonical pipeline

`DISCOVER → AUTHORIZE → SNAPSHOT → HASH → DISPATCH → COLLECT → VERIFY → PERSIST → READBACK → REPORT`

| Stage | Required operation | Automatic evidence | Fail-closed behavior |
|---|---|---|---|
| DISCOVER | Capture branch, commit, source files, build/process identity and registered MCP tool/schema inventory | Git SHA, source/test/workflow artifact, deployed identity and tools/list evidence | Unknown deployed identity or source provenance = BLOCKED |
| AUTHORIZE | Derive principal from trusted server transport; Core resolves WorkContext and capability | Core build identity, principal reference, canonical Work ID, authorization decision | Missing/forged principal, wrong Work or Core denial = DENIED before side effects |
| SNAPSHOT | Resolve only Work-relative source and copy to immutable per-run snapshot | Snapshot reference, Work binding, immutable attestation | Path/symlink/race failure = BLOCKED; no process spawn |
| HASH | Hash exact snapshot bytes and compare with requested expected SHA-256 | Source/snapshot SHA-256 | Mismatch = FAIL/BLOCKED; no dispatch |
| DISPATCH | Send only to the one approved canonical Runtime behind Core and Execution Host :8031 | Request/run IDs, runtime and host identities | Unknown runtime, absent isolation attestation or no approved route = BLOCKED; never fallback |
| COLLECT | Capture actual exit code, test discovery summary, bounded output refs and process-tree cleanup | Exit code, test counts, output refs, cleanup evidence | Missing exit/summary or incomplete cleanup = non-PASS |
| VERIFY | Evaluate the complete evidence record with `work28_auto_e2e_gate_v1.py` | Machine-calculated PASS/FAIL/DENIED/BLOCKED | Caller-supplied status text is ignored |
| PERSIST | Store integrity-protected, append-only evidence | Protected evidence reference and SHA-256 | Missing writer, mutable/unprotected evidence or write error = BLOCKED |
| READBACK | Re-read through the authorized readback API and verify exact checksum/reference | Readback reference and SHA-256 | Missing/mismatched readback = FAIL/BLOCKED |
| REPORT | Publish JSON artifact and GitHub Actions summary bound to source commit/run | CI job outcomes, gate result, blockers, artifact link | CI success alone never promotes deployed E2E or release |

## 3. What is automated now

Workflow: `.github/workflows/work28-mcp-tooling.yml` (display name: **Work 28 Automatic E2E Gate**).

Triggers:
- Push to `work/28-mcp-tooling-platform` when Work 28, `execution_host/**`, `core/execution_authority/**`, `room_hop_mcp/**`, tests or this workflow change.
- Pull request affecting those paths.
- Manual `workflow_dispatch`.

Jobs:
1. `unit-regression-tests` — complete Work 28 contract/unit regression discovery, including the Core execution-authority boot boundary test (real subprocess + local socket on the CI runner).
2. `execution-host-lifecycle-linux` — process lifecycle, suspended spawn, Core/dispatch/evidence/readback/bounds/audit/HTTP contract suites.
3. `execution-host-lifecycle-windows` — the same Windows-relevant suites on a native Windows runner. Every Python command propagates its own nonzero exit code.
4. `automatic-e2e-gate-report` — runs even when an upstream job fails; emits `work28-auto-e2e-report.json` as a 30-day artifact and a GitHub Actions summary. It reports CI preconditions PASS/FAIL independently from deployed E2E.

The evidence evaluator is `04_CODE/work28_auto_e2e_gate_v1.py`. Its contract requires exact source commit, MCP/Core/runtime/Execution Host identities, registered tool-list digest, trusted principal and Core authorization reference, canonical Work ID, immutable snapshot, equality of expected/snapshot/runtime SHA-256, approved runtime identity, OS-isolation attestation, actual integer exit code, process cleanup, non-empty test summary for RUN_TESTS, protected evidence, explicit readback verification and matching readback SHA-256. It also requires an HMAC-SHA256 attestation signed by a deployment-held key and pinned key ID; the key is supplied out-of-band through `WORK28_E2E_ATTESTATION_HMAC_KEY` and never stored in the evidence record. Secret material is rejected. A string such as `reported_status: PASS` cannot grant PASS.

## 4. Current boundary — do not mislabel CI as live E2E

The automated workflow deliberately reports:

- `CI_PRECONDITIONS=PASS` only when all three test jobs succeed.
- `DEPLOYED_MCP_CORE_RUNTIME_E2E=BLOCKED` until live MCP :8030 build/process identity and tools/list parity, trusted deployed Core principal/WorkContext, approved Runtime MCP identity, Execution Host :8031 identity/isolation attestation and a complete protected evidence/readback chain are connected to the runner.
- `EXECUTION_GATE=CLOSED`.
- `RELEASE=NOT_RELEASED`.

Current source inspection shows `mcp8020_core_execution_session_v1.py` and `mcp8020_authorized_execution_adapter_v1.py` are staged and not wired into MCP registration/v54 dispatch. Their tests use injected test doubles for snapshot/runtime. The Core authority boot test proves a local CI process/socket boundary, not deployed Core integration. Therefore no automatic workflow may call an unverified endpoint or historical MCP :8020 listener.

## 5. Gate calculation rules

- RUN_TESTS PASS: exit code 0; tests_run >= 1; failures/errors = 0; exact source/snapshot hash; approved runtime identity; process-tree cleanup verified; protected evidence and successful readback with identical SHA-256.
- RUN_SCRIPT PASS: exit code 0; exact source/snapshot hash; approved runtime identity; process-tree cleanup verified; protected evidence and successful readback.
- Missing identity, authorization, immutable snapshot, isolation, cleanup, evidence or readback => BLOCKED.
- Authorization denial => DENIED.
- Hash mismatch, runtime identity mismatch, nonzero exit, zero tests, test failure/error, secret leakage or checksum mismatch => FAIL.
- Never use stdout/printed JSON/caller status as an authoritative result.
- CI, mocks, source writes, a green test job or a successful Sandbox file read do not equal deployed E2E acceptance.

## 6. Team operating model

- **Vi:** continuously reconcile GitHub HEAD; implement the next safe dependency-ready slice; run the automated CI; fix failures; sync exact committed artifacts to MCP 8030 Sandbox; read back and compare; append the canonical journal. Do not wait for a conversational checkpoint.
- **An:** independent QA, native Linux/Windows reproduction and A01–A18 verification; record exact command, runner, output, exit code, commit and uncovered cases.
- **Ka:** independent architecture/security review, threat model, authorization/path/process/evidence boundary and explicit NO-GO findings.
- **Xu:** coordinate dependencies, resolve delegated technical decisions and maintain gate state.
- An and Ka remain independent; Vi must not convert self-tests into their PASS/review result. Vinh may route their review/test assignments directly.
- Only the four approved participants Xu, Vi, An and Ka. Co is excluded.

## 7. GitHub → Sandbox synchronization

For every completed implementation/evidence slice:
1. Fetch current canonical branch HEAD and exact file blob SHA.
2. Make the smallest reviewable GitHub branch change; do not overwrite a concurrent update.
3. Wait for the relevant Actions run and inspect job-level results/logs.
4. Copy exact committed file content to Work 28 Sandbox through MCP 8030.
5. Run diagnostic readback; require `status=ok` and exact content equality. Record source blob/commit and Sandbox path.
6. If a binary artifact is involved, require byte-preserving upload and SHA-256 parity; text-only `sandbox_write` is not binary transfer.
7. Keep GitHub canonical. Never publish Sandbox state back to GitHub automatically.

## 8. Remaining implementation sequence

1. Complete WP2 race/repeated-cleanup tests and structured `start_service()` BLOCKED mapping; An/Ka independently verify.
2. Complete WP3 Core trusted-context injection and explicit Core Work ID `W28` → Sandbox key `28` mapping; do not expose binary upload before authorization is real.
3. Implement bounded binary upload sessions, staging, quotas, SHA-256, atomic promotion, readback and audit; then An/Ka verify.
4. Reconcile MCP :8030 source/build/process identity and runtime `tools/list` schema parity through approved read-only diagnostics.
5. Build the new Runtime MCP independently; do not touch historical :8020.
6. Wire authenticated Core → Runtime MCP → Execution Host :8031 and protected evidence/readback.
7. Enable the live E2E job only after the exact deployed contracts and identity sources are verified; then run A01–A18 and the disposable-Work mutation loop.
8. Xu consolidates evidence; release remains closed pending required reviews and Vinh's explicit approval.

## 9. Current state

**AUTOMATED CI PRECONDITIONS:** first full pipeline run PASS — run `41722405589`, source commit `952f85bb29e5c67b89d32109cc2c3cf59fa6eae7`.  
**LIVE DEPLOYED AUTO E2E:** BLOCKED — trusted deployed identity/route/isolation/evidence integration not yet wired.  
**WP2:** focused suspended-spawn Linux/Windows CI verified; concurrency and service error mapping remain open.  
**WP3:** binary upload source gap confirmed; secure Core authorization contract proposal exists; implementation pending.  
**Execution Gate:** CLOSED. **Work:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

### First automated pipeline evidence
- Run: `41722405589` — all four jobs SUCCESS (`unit-regression-tests`, Linux lifecycle, Windows lifecycle, `automatic-e2e-gate-report`).
- Unit/regression discovery: **341 tests, OK**. The live Core authority boot test launched a real local subprocess/socket on the CI runner; this is not the deployed Core service.
- Linux suspended-spawn: **13 passed, 4 skipped** (native-Windows-only cases).
- Windows suspended-spawn: **17 passed**.
- Machine report artifact: `work28-auto-e2e-report-41722405589`, artifact ID `13273471450`.
- Report correctly keeps deployed MCP → Core → Runtime E2E **BLOCKED**, Execution Gate **CLOSED**, Release **NOT RELEASED**.
- Windows/Linux job logs include a post-checkout cleanup warning about `.gitmodules` (`No url found for submodule path 'room-meeting-ai'`); it did not change job conclusions, but remains a repository maintenance item.


---
**Record owner:** Vi | CODER  
**Signature:** [KÝ: VI | CODER]
