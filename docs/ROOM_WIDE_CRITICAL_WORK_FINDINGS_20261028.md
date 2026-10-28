# ROOM HOP — Critical Work Findings, Evidence Bounded
Date: 2026-10-28
Reviewer: Ka — CSA / Architecture & Backend
Status: ACTIVE / NOT RELEASED

## Work 28 — MCP-8020 Tooling Platform
Status: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.
- Sandbox Work manifest: MCP-8020-TOOLING-PLATFORM/00_ROOT/WORK_MANIFEST.md.
- Work-specific evidence at MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_SANDBOX_READ_PATH_DIVERGENCE_20261028.md reports same-target discrepancy: sandbox_read returned {} while sandbox_read_probe returned full content.
- Work-specific evidence at MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/KA_FOLLOWUP_CONTRACT_TRACE_E2E_GAPS_20261027.md says the inspected entrypoint showed 16 registration decorators and no evidenced V54 execution/grant/authorization path in the searched file; that scan alone cannot exclude imported/dynamic dispatch.
- Do not claim ordinary sandbox_read is healthy. Do not call the 8031 execution endpoint directly or bypass Core. Reconcile the actual loaded 8020 entrypoint and fingerprint before proposing integration. Integrated live E2E remains NOT PROVEN.

## Work 102 — AI Agent Loop Production Readiness
- Sandbox manifest is under AI-AGENT-LOOP-PRODUCTION-READINESS/00_ROOT/WORK_MANIFEST.md.
- Manifest status says READY_FOR_PC_ACCEPTANCE (updated 2026-10-24), but its own remaining items require authorized PC pytest/demo, live Gate A, closed-loop Gate C, and recovery/concurrency evidence.
- Gate A source audit explicitly says PARTIAL / NOT PASS and describes the inspected Core scope as meeting lifecycle, not proven generic task dispatcher. It also says connected MCP 8030 does not expose Core source/API inspection or authorized runtime probes.
- Reconcile status wording with actual acceptance evidence. Do not add a second dispatcher; identify canonical task authority and live API owner first.

## Work 200 — Crypto Trading Bot
- Manifest: CRYPTO-TRADING-BOT/00_ROOT/WORK_MANIFEST.md; status ACTIVE, research/backtest/paper only; no live trading.
- WORK200_RECOVERY_TRIAGE_20261028.md reports GitHub/Sandbox divergence, additional Sandbox-only files, unverified reads, unresolved ADR-001/ADR-002/WP0 freeze package, and required independent risk regression tests.
- Keep PAPER ONLY / NOT RELEASED. Do not merge or overwrite variants until canonical source/tree and ADR gates are reconciled.

## Work 15 — Website Builder
- Inventory marks manifest missing.
- Existing WORK.md says PHASE 0 workspace/architecture bootstrap; docs/WORK_STRUCTURE_STANDARD.md explicitly says preserve project-specific layout and do not invent canonical repo/branch/commit metadata before reconciliation.
- Do not create a manifest until canonical GitHub branch and source metadata are established.

## Work 98 — ONT Care / e2e
- Inventory marks manifest missing.
- Existing WORK_98_README.md and WORK_STRUCTURE_STANDARD.md explicitly require reconciling canonical source/GitHub before creating a manifest and preserving current root, ont-platform, preview, e2e, workflows, legacy archive, and dashboard artifacts.
- GitHub API query for numbered paths 15 and 98 on main returned 404. This is not proof the Work has no GitHub source; locate its actual branch/path before any mutation.

## Cross-room structural finding
- Sandbox inventory has 53 Works and 39 branch names were returned in the current branch query; branch-name heuristics are candidate hints only.
- Work 99 and Work 28 store WORK_MANIFEST.md under their Work-specific 00_ROOT paths, while Work 15 and Work 98 have custom layouts and explicit no-inference policies. Therefore, no global manifest path or mass folder migration should be imposed.
- Work 99 readback succeeded via sandbox_read_probe for both audit checkpoint and 53-Work matrix.

## Required next steps
1. Locate authoritative GitHub refs/paths for Works 15 and 98.
2. Build per-Work SHA/content reconciliation for 53 Works, not just branch-name matching.
3. Inspect PR #27 common standard CI/review before considering merge; PR #29 is draft audit documentation only.
4. Resolve ordinary Sandbox read result-shape issue in its owning backend with a focused regression test.
5. Obtain authorized PC/Core/runtime access for Work 28 and Work 102 live gates; report any access blocker to Xu.
6. Keep Work 200 paper-only until source/ADR/risk tests are resolved.

Signature: [KÝ: KA | CSA]
