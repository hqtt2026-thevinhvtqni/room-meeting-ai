# Work 28 — Authorized adapter staging evidence

- Date: 2026-10-25
- Reviewer/implementer: Xu (AI-01)
- Branch: `work/28-mcp-tooling-platform`
- Decision: **STAGED / NOT WIRED / NOT RELEASED**

## Changes

- `04_CODE/mcp8020_authorized_execution_adapter_v1.py`
  - Introduces a narrow policy seam around injected trusted Core authorization, immutable source snapshot provider, and pinned runtime.
  - Rejects missing/denied caller context before snapshot resolution.
  - Checks Work/path binding, immutable snapshot attestation, expected SHA-256, exact snapshot reference, pinned runtime identity, required request/run/evidence IDs, integer exit code, process-tree cleanup attestation, and non-empty clean test summary.
  - Does not authenticate callers itself, inspect/hash source bytes itself, launch processes, or provide trustworthy attestations; those are contracts for trusted injected components.
  - Not registered in MCP and not wired into v54 service or W13 HTTP route.

- `05_TEST/test_mcp8020_authorized_execution_adapter_v1.py`
  - Positive contract test and negative tests for forged public authority/command fields, absent caller context, authorization denial, hash mismatch, mutable snapshot, Work/path mismatch, runtime identity mismatch, wrong snapshot, missing evidence binding, failed cleanup, invalid/empty test summary, and missing pinned runtime identity.

## CI evidence

- Run: [Work 28 MCP Tooling Tests #104](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40150058368)
- Latest commit: `bb196eefdd1c459f4d26069e1d11aa1dd57cf727`
- Latest run: [CI #106](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40150157499)
- Result: **PASS** — 192 tests, 4 skipped.
- Added negative checks: non-PASS runtime status and nonzero, boolean, or missing exit code are rejected.
- The earlier run at `01f9269fafc12560cba088b88e5cf739a0c435b8` failed because its commit snapshot contained the pre-update test fixture; the subsequent test commit above ran the updated source and fixture successfully. No failure was concealed.

## Boundary / next gate

This CI run proves only staged unit/regression behavior with mocks. It does **not** prove live Core authorization, source bytes are actually snapshotted and hashed by a trusted resolver, W13 executes that exact snapshot, approved runtime identity is cryptographically/trustworthily pinned, process-tree cleanup is real, or live E2E works.

Keep all seven public execution/evidence tools `NOT_IMPLEMENTED`. Do not wire this adapter or enable tools until trusted implementations exist and W13 unit tests plus authorized live E2E prove the complete evidence chain. No second execution host is authorized.


## Follow-up: W13 contract-boundary regression (2026-10-25)

- Commit under test: `8d8514a87e3e39cf5fc69d2ff4e5b937bd678bea`
- CI run: [40150494323](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40150494323)
- Result: **PASS — 200 tests, 4 skipped** (`Ran 200 tests`, `OK (skipped=4)`).
- New coverage: reject caller-provided command/authority/cwd/shell fields; reject traversal, absolute and Windows-ambiguous paths; reject invalid operation/hash/timeout; bind snapshot bytes to SHA-256; reject mismatched authoritative Work, hash mismatch, and symlink components.
- Source staged for the canonical W13 host: `execution_host/work28_contract.py` on branch `work/13-execution-host-hardening`; mirrored into the Work 28 branch for regression execution.
- Important limitation: this is contract/snapshot unit coverage only. The module is **not wired to HTTP :8031**, does not authenticate the Core caller, does not execute scripts, does not attest runtime identity, and does not prove process-tree cleanup. No live host request was sent. All seven execution/evidence MCP tools remain `NOT_IMPLEMENTED`.
