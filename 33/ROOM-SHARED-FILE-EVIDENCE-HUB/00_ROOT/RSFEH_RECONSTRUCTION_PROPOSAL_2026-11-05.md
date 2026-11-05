# RSFEH Reconstruction Proposal — for Xu (AI-01) to read and execute

Written: 2026-11-05 (Asia/Ho_Chi_Minh), by the Vibe agent, per Vinh's instruction "đọc nhật ký và triển khai tiếp w33".
Precedent: Work 32 handoff pattern — proposal recorded in the Work log; implementation NOT performed from chat.

## Verified state (2026-11-05)
- Branch head: `11506ea0daaec7aa487651c69368bb7eff15c91b` ("Work 33: sync original RSFEH package from Sandbox", 2026-10-26).
- The "sync" commits delivered ONLY the `00_ROOT/` documents (README, WORK, BUILD_REPORT, DISCOVERY_REPORT, RECONCILIATION, SYNC_MANIFEST).
- MISSING vs SYNC_MANIFEST: `03_ARCHITECTURE/` (4 files), `04_CODE/src/rsfeh/` (4 files incl. cli.py 6317B, store.py 12368B), `05_TEST/` (2 files), `06_EVIDENCE/` (3 files), `07_RELEASE/` (2 files). Verified by direct directory reads on this branch.
- Original artifact search (per RECOVERY_SEARCH_2026-10-26) was already negative across Sandbox/GitHub/Library; an additional check of the current Vibe environment (uploads + filesystem) on 2026-11-05 also found no `WORK_33_ROOM`/`rsfeh` archive.
- Conclusion: Grok's original v0.1.0 bytes are NOT recoverable through any accessible channel. The claimed 17/17 PASS stays NOT VERIFIED. Do not reconstruct test logs from the summary (per RECONCILIATION rule).

## Decision requested from Vinh (DECISION status)
Authorize **RSFEH v0.2 reconstruction as a NEW artifact lineage** (Xu's RECOVERY_SEARCH path 2). Rules:
- v0.2 is a fresh implementation from the recorded spec; it must never be presented as Grok's original v0.1.0.
- No fabricated historical logs; all PASS claims must come from executed, inspectable test runs.
- Keep A10 (live Core/MCP integration) BLOCKED until a separate authorization.

## Reconstruction plan (for Xu)
**Spec sources:** `ACCEPTANCE.md` (W33-AC-04…08), `BUILD_REPORT.md` functional description, `SYNC_MANIFEST.md` inventory (structure reference only).

**P1 — Spec freeze (04_CODE/src planning)**
Functional floor (from BUILD_REPORT): content-addressable blob store (SHA-256); SQLite catalog; append-only audit JSONL; CLI: init, put, get, list, search, verify, link, audit, meta; path sanitization; soft-delete; work linkage; integrity verify. Python 3.10+, stdlib only.

**P2 — Implement v0.2** under `33/ROOM-SHARED-FILE-EVIDENCE-HUB/04_CODE/src/rsfeh/` on this branch.

**P3 — Tests** under `05_TEST/{unit,e2e}` covering the A1–A9 semantics (init, put/get byte-identical, meta/list, verify-tamper, bad id, audit events, search/link, consistency-after-error, full suite green).

**P4 — Independent CI verification** on this branch (GitHub Actions Python 3.11 runner, no Docker — reuse the Work 32 evidence pattern: G0 record → G1 compileall → G2 pytest → evidence posted to a tracking issue + artifacts). This satisfies "run the tests in an isolated clean environment" from RECONCILIATION.

**P5 — Evidence & sync**
- New `SYNC_MANIFEST_v0.2.md` with real sha256 of every file.
- Update WORK_LOG with run links; update BUILD/RELEASE docs as v0.2 lineage.
- Reviewer checks diff/risks; Vinh decides integration (A10 remains a separate future authorization).

**Out of scope:** live Core :8000 / MCP :8020 mutation, PC changes, auto-merge/push to main, any claim about v0.1.0 history.

**W33-AC mapping:** AC-04→P1; AC-05/06/08→P3/P4; AC-07 partial (multi-agent read testable at CLI identity level; full cross-agent auth stays with Core); AC-09→P5; AC-01/02/03 (sandbox_read root-cause trace) remain with Xu's READ/TRACE phase.
