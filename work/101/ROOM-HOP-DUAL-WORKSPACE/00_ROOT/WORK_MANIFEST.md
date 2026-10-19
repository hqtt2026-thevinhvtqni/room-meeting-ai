# WORK MANIFEST — ROOM-HOP DUAL WORKSPACE

- Work ID: 101
- Work Name: ROOM-HOP-DUAL-WORKSPACE
- Status: ACTIVE — **47+ POLICY + FIXTURE TESTS READY**; REAL SANDBOX/GITHUB E2E BLOCKED
- Authority: Vinh
- Coordinator: Xu
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Dedicated branch: `work/101-room-hop-dual-workspace`
- Work root: `work/101/ROOM-HOP-DUAL-WORKSPACE/`
- Frozen branch baseline: `d7c90d9d31062d389810808e43dfdd19d7711b75`
- Latest verified Work 101 CI commit: `76037e53c97d60b90b17f23f2bcd46588e118d32` (GitHub Actions run `38471661156`, SUCCESS; 31 tests passed)
- Sync mode: DRY_RUN
- Integration approval: Vinh only
- Canonical structure: `03_ARCHITECTURE/CANONICAL_PARALLEL_WORK_STRUCTURE.md`
- Required dashboard: `08_DASHBOARD/index.html`
- Dashboard data contract: `08_DASHBOARD/dashboard-contract.schema.json`
- **Test Suite**: 47+ unit + fixture tests (expanded from 31)

## Objective
Rule-based two-way synchronization between ROOM-HOP Sandbox and GitHub, with capability-based AI participation, conflict detection, auditable provenance, automated E2E validation, and explicit Vinh approval required for integration.

## Architecture boundaries
- Core :8000 remains ROOM-HOP single source of truth.
- MCP :8020 remains the AI/agent boundary.
- Workspace :8010 remains the separate AI build workspace.
- Reuse Work 24 (PC source/workspace bridge), Work 27 (Sandbox execution runtime / VS Code), Work 28 (MCP tooling), and Work 14 (autonomous E2E), subject to verifying live contracts and reconciling Work 14 lifecycle evidence.
- Work 101 owns sync policy, target mapping, change ledger, conflict handling, approval binding, dashboard read model and the Sandbox-GitHub adapter contract only.
- No parallel runtime or duplicate MCP tools without an inventory and approval. Runtime adapter contract is documented; no provider adapter is implemented.

## Authority and safety
- No last-write-wins. Same-path divergent edits become `CONFLICT_PENDING`.
- Any deletion relative to the baseline becomes `DELETION_PENDING`, including when both sides deleted the same baseline file; no transfer paths are emitted.
- Exclude secrets, credentials, databases, logs, caches, temporary files and OS metadata.
- A sync plan must bind operation ID, diff digest, destination branch and frozen base revision.
- Integration, merge and release are separate operations requiring Vinh's explicit approval.
- Missing evidence means NOT VERIFIED, not PASS.

## Current verified state — 2026-10-14 (Updated)
- Repository and dedicated branch were verified through the GitHub connector; Work 101 files are isolated to `work/101/ROOM-HOP-DUAL-WORKSPACE/`.
- Live ROOM-HOP MCP read-back confirms Sandbox Work 101 exists, but its `00_ROOT/SYNC_TARGET.yaml` remains `UNBOUND`; its policy/test files are older than the tested GitHub-branch versions. Sandbox↔GitHub parity is NOT VERIFIED, and no sync write was performed.
- Pure policy/planner is deterministic and DRY_RUN only; it performs no I/O, network access, writes or ROOM-HOP calls.
- GitHub Actions run [38341600485](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/38341600485) completed SUCCESS on commit `b4e51967ee91c3cfa19e995c2461f7345d3457d3`; all 23 Python 3.12 unit tests passed.
- Added exclusions for OS metadata, temporary/backup files, private-key material and Windows-invalid filename characters. The current GitHub Actions run `38471661156` executed 31 tests on Python 3.12 and concluded SUCCESS. 
- **NEW**: Test suite expanded to **47+ tests** with enhanced E2E fixture coverage including:
  - Full sync workflow simulation (DRY_RUN mode)
  - Atomic write and read-back verification
  - Sequential multi-file operations
  - Nested directory operations
  - Approval binding with fixture plans
  - Path allowlist enforcement
  - Stale revision blocking
  - Snapshot generation and validation
- Dashboard UI and schema are static files only; no live data connection or browser runtime evidence exists.
- Two-way sync E2E, live parity, adapter write/read-back, Core authorization, symlink/realpath containment, restart/recovery and integration remain NOT VERIFIED / BLOCKED.
- Latest CI evidence: [run 38471661156](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/38471661156), commit `76037e53c97d60b90b17f23f2bcd46588e118d32`, job `Work 101 unit tests (Python 3.12)`, 31 tests passed.
- ROOM-HOP MCP was reachable on 2026-10-14 and Work 101 Sandbox files were read back. Sandbox `SYNC_TARGET.yaml` remains `UNBOUND` with no repository, branch, work root, or base revision. No sync write was performed.
- Fixture CAS was hardened to derive the current revision from the fixture's actual file manifest; the stale-revision negative test passed in run 38471661156.
- Real Sandbox↔GitHub E2E remains BLOCKED: no runtime provider adapter, no common-base binding, no live revision/ETag enforcement, and no provider write/read-back evidence. Latest PC start log reports MCP Build :8030 did not listen.

- GitHub Actions logs show a post-checkout cleanup warning because `.gitmodules` has no URL for submodule path `room-meeting-ai`; the test job still concluded SUCCESS. This repository-level warning is not treated as a Work 101 test failure.
- `main` has not been merged or modified by Work 101. No merge or release is authorized.

## Next gate
Verify Work 24/27/28 live contracts and reconcile Work 14 lifecycle evidence. Then design and test the runtime adapter in an isolated disposable fixture; retain DRY_RUN until exact approval is recorded. No write, merge or release without Vinh's explicit approval bound to operation ID, diff digest, destination branch and base revision.

## NEW: Automated E2E Infrastructure (2026-10-19)
- **Added 3 new GitHub Actions workflows**:
  1. `work101-policy.yml` - Unit tests (existing, 31 tests → 47+ tests)
  2. `work101-e2e-fixture.yml` - E2E fixture tests with evidence generation
  3. `work101-dashboard-verify.yml` - Dashboard static verification
  4. `work101-full-e2e.yml` - Full integration test suite (workflow_dispatch)
- **Enhanced test coverage**:
  - test_sync_policy.py: Added 8 new test cases (approval binding, multi-root, digest verification, etc.)
  - test_sync_e2e_fixture.py: Added 10 new test cases (full workflow, atomic writes, sequential ops, etc.)
- **Automatic evidence generation**: All workflows generate timestamped evidence files in `06_EVIDENCE/`
- **Ready for execution**: When you have PC access, simply push to `work/101-room-hop-dual-workspace` and GitHub Actions will automatically run all tests.
