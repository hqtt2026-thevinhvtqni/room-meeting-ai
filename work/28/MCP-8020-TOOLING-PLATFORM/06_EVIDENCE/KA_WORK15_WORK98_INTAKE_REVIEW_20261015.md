# KA — Work 15 / Work 98 Intake Review for Work 28
Date: 2026-10-15
Role: Ka / CSA — Work 28 coordinator
Scope: Read-only Sandbox intake; no source edits, manifest creation, GitHub mutation, PC access, or runtime execution.

## Evidence collected
- `sandbox_list_works`: status=ok, 39 records; Work 15 and Work 98 report `manifest_exists=false`.
- `sandbox_list(work_id="15")`: status=ok; Work 15 source tree is present under `WEBSITE-BUILDER/`, including README.md, WORK.md, docs/ARCHITECTURE.md, docs/REQUIREMENTS.md, docs/E2E.md, scripts/e2e.ps1, scripts/start.ps1, scripts/test.ps1, frontend source and test directories.
- Read Work 15 README.md, WORK.md, docs/ARCHITECTURE.md. These state PHASE 0 / IN_PROGRESS, require real runtime and E2E evidence, and mandate the ROOM-HOP execution architecture rather than an independent execution path. No execution was run in this intake.
- `sandbox_list(work_id="98")`: status=ok; source tree is present, including handoff/audit/mandate files, `ont-platform/`, `preview/`, and E2E/CI material.
- Read Work 98 HANDOFF_TO_NEXT_AI_20261014.md, WORK_98_README.md, BIEN_BAN_W98.md, AGENTS.md. The handoff explicitly says build, lint, typecheck, browser render, E2E/CI and real ONT are NOT RUN; source is staged to a separate GitHub branch, but that does not prove build/test success. Work 98 instructions say do not implement product architecture without Xu/Vinh approval.

## Intake conclusions
### Work 15 — WEBSITE-BUILDER
- Source presence: OBSERVED.
- Manifest: MISSING according to Sandbox inventory.
- Product/runtime verification: NOT RUN / NOT VERIFIED.
- Work 28 relevance: consumer/orchestrator candidate; it must consume the canonical Core -> Work 12 -> Work 13 execution route and Work 27 isolation. Do not expose a new execution tool or create an alternate host based only on Work 15 docs.
- Next action: keep source untouched; prepare a manifest proposal only after checking the canonical Work manifest schema and existing Work 15 metadata. No manifest was created by this review.

### Work 98 — ONT Care
- Source presence: OBSERVED.
- Manifest: MISSING according to Sandbox inventory.
- Build/runtime/E2E/real ONT verification: NOT RUN per handoff evidence.
- Work 28 relevance: typed product capabilities are future integration candidates only. ONT actions require explicit authorization and trusted server boundary; read-only is default. Product source/API is not automatically an MCP tool.
- Next action: no product architecture/code change. Resolve manifest intake separately against the canonical manifest schema; runtime/product work requires its own authorized owner and test environment.

## Effect on Work 28 capability matrix
- These two Works are no longer “source not discoverable”; their Sandbox trees and key documents were read.
- Their missing manifests remain an intake/metadata gap, not proof that source is absent.
- Neither Work provides evidence that additional Work 28 MCP tools are already registered in the live PC :8020 runtime.
- No P0 tool implementation decision changes. Continue source/API trace before building `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, or `capability_discover`.

## Gate
Work 28: ACTIVE / NOT LOCKED.
Work 15/98 intake: PARTIAL READ-ONLY REVIEW COMPLETE.
Manifest remediation: NOT PERFORMED.
Build/tests/E2E: NOT RUN.
Live PC MCP :8020 registry: UNVERIFIED.
Release: NO-GO.
