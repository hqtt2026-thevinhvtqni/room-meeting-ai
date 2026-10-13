# WORK MANIFEST — ROOM-HOP DUAL WORKSPACE

- Work ID: 101
- Work Name: ROOM-HOP-DUAL-WORKSPACE
- Status: ACTIVE — ARCHITECTURE BASELINED; IMPLEMENTATION / E2E NOT VERIFIED
- Authority: Vinh
- Coordinator: Xu
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Dedicated branch: `work/101-room-hop-dual-workspace`
- Work root: `work/101/ROOM-HOP-DUAL-WORKSPACE/`
- Frozen branch baseline: `d7c90d9d31062d389810808e43dfdd19d7711b75`
- Sync mode: DRY_RUN
- Integration approval: Vinh only
- Canonical structure: `03_ARCHITECTURE/CANONICAL_PARALLEL_WORK_STRUCTURE.md`
- Required dashboard: `08_DASHBOARD/index.html`
- Dashboard data contract: `08_DASHBOARD/dashboard-contract.schema.json`

## Objective
Rule-based two-way synchronization between ROOM-HOP Sandbox and GitHub, with capability-based AI participation, conflict detection, auditable provenance, automated E2E validation, and explicit Vinh approval required for integration.

## Architecture boundaries
- Core :8000 remains ROOM-HOP single source of truth.
- MCP :8020 remains the AI/agent boundary.
- Workspace :8010 remains the separate AI build workspace.
- Reuse Work 24 (PC source/workspace bridge), Work 27 (Sandbox execution runtime / VS Code), Work 28 (MCP tooling), and Work 14 (autonomous E2E), subject to verifying live contracts and reconciling Work 14 lifecycle evidence.
- Work 101 owns sync policy, target mapping, change ledger, conflict handling, approval binding, dashboard read model and the Sandbox-GitHub adapter contract only.
- No parallel runtime or duplicate MCP tools without an inventory and approval.

## Authority and safety
- No last-write-wins. Same-path divergent edits become `CONFLICT_PENDING`.
- Never silently delete destination-only files.
- Exclude secrets, credentials, databases, logs, caches, temporary files and OS metadata.
- A sync plan must bind operation ID, diff digest, destination branch and frozen base revision.
- Integration, merge and release are separate operations requiring Vinh's explicit approval.
- Missing evidence means NOT VERIFIED, not PASS.

## Current verified state — 2026-10-13
- Repository and dedicated branch were verified through GitHub connector.
- Branch was created from `main`; comparison showed the branch and main identical at baseline `d7c90d9d31062d389810808e43dfdd19d7711b75` before Work 101 files were added.
- Work 101 artifacts are being organized under `work/101/ROOM-HOP-DUAL-WORKSPACE/`; no Work files are placed at repository root.
- Sandbox source files were read before selecting artifacts for the initial branch scaffold. Windows `desktop.ini` files are intentionally excluded.
- Static policy and tests are ported for review; tests have NOT RUN in an approved runner.
- Dashboard files are static only; no live data connection or browser runtime evidence.
- Two-way sync E2E, live parity, and integration are NOT VERIFIED.
- `main` is not the destination for Work 101 commits; no merge or release is authorized.

## Next gate
Review source and target digest parity, execute tests through an approved runner, reconcile Work 14 lifecycle evidence, verify Work 24/27/28 live contracts, and only then design the runtime adapter. Keep sync in DRY_RUN until an exact operation is separately approved.
