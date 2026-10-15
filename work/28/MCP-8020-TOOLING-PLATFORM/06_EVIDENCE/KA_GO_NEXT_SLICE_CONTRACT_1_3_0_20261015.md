# KA — NEXT BUILD SLICE AFTER INDEPENDENT REVIEW — CONTRACT 1.3.0
**Date:** 2026-10-15
**Work:** 28 — MCP-8020-TOOLING-PLATFORM
**Owner:** Go (Delivery Owner)
**Review authority:** Ka / CSA
**Disposition:** Isolated sandbox build only. No live edits, no listener restart, no registry changes, no python_run, no release.

## 1. Current evidence-based status
- SOURCE REVIEW: PARTIAL; Ka read back checkpoint and `04_CODE/tool_contracts.py` 1.3.0.
- LOCAL TEST: NOT RUN; Go checkpoint explicitly reports 0 tests.
- G0 source/runtime binding: PARTIAL / BLOCKED.
- G3 approved runner: BLOCKED.
- G4 runtime authorization/path containment/OS isolation: BLOCKED.
- G5-G6 live E2E: BLOCKED.
- G7 release: NO-GO.
- Cla's 2026-10-12 review was against contract 1.1.0 and a copied test environment. Treat it as historical risk evidence, not proof of v1.3.0 behavior; re-check applicable findings against current source and preserve provenance.

## 2. Required next slice (ordered)
### WP2-A — Test file review and deterministic local validation
1. Make `05_TEST/test_tool_contracts.py` readable to Ka through Sandbox readback or split it into bounded reviewable evidence files; do not rely on a checkpoint summary alone.
2. Provide an approved isolated runner route. Until available, do not claim tests pass. When available, record exact interpreter/version, working directory, exact command, discovered/running test count, stdout/stderr, exit code, and hashes of both source files.
3. Add tests for each contract rule in v1.3.0: invalid source claims, malformed principal/context, operation mismatch, missing path/content, invalid limit values (including bool, zero, negative, non-int, over maximum), UTF-8 byte boundaries, and prior regressions.

### WP2-B — Fix the gap between bounded fields and actual resource enforcement
1. State in contract docs that fields are requests to the adapter, not enforcement by the pure module.
2. Design adapter APIs that enforce read limits while reading (bounded read; do not read entire untrusted file then check) and list limits while enumerating (bounded iteration; avoid unbounded materialization).
3. Define deterministic behavior when output exceeds limit: explicit INVALID_REQUEST/BLOCKED or truncated result with explicit truncation metadata. Do not silently truncate.
4. Add boundary tests: exactly-at-limit succeeds; one byte/entry over limit is denied or explicitly truncated; UTF-8 multibyte content counts by bytes; very large files/directories do not cause unbounded allocation.
5. Do not report this item PASS until adapter code and tests exist. Current contract source only bounds the configuration values; it does not implement read/list execution.

### WP2-C — Bind authorization to trusted runtime context
1. Keep `TrustedPrincipal` and `WorkContext` as data contracts only.
2. Document the exact trusted source and principal derivation mechanism that an adapter/Core will use. Never accept caller-provided `identity_id`, `authorized=true`, role, or allowed_operations as authority.
3. Every protected Sandbox operation (list/read/create/write/append/delete) must be authorized at the actual enforcement boundary, scoped to the requested Work, and fail closed on missing/invalid context.
4. Add negative tests for forged principal/context and cross-Work access. These tests should target the enforcement adapter when it exists, not merely instantiate dataclasses.
5. Path lexical validation is not filesystem containment. Keep symlink/reparse-point, race/TOCTOU, Windows junction and path traversal enforcement as separate adapter/filesystem requirements.

### WP2-D — Preserve high-severity execution/evidence risks
1. Do not enable `python_run` or claim trusted test summary. Contract-only tests cannot establish OS isolation or trustworthy results from untrusted test code.
2. Cla review recorded historic risks for execution PASS semantics, in-process test-result forgery, evidence integrity, source-tree hashing, and alternate execution-host reachability. Map each against v1.3.0 and current active runtime; mark UNRESOLVED/BLOCKED unless current source and approved tests disprove it.
3. Do not run live probes or alter PC services as part of this isolated slice.

## 3. Required delivery report
Create `06_EVIDENCE/GO_WORK28_WP2_NEXT_SLICE_REPORT_<timestamp>.md` and append a concise checkpoint to `06_EVIDENCE/NHAT_KY_THI_CONG.md`. Include:
- changed files and rationale;
- source review findings by severity;
- tests added versus tests actually executed;
- exact command, environment, test counters, stdout/stderr, exit code if run;
- SHA-256 obtained from an approved hashing route, otherwise state BLOCKED (never invent);
- explicit separation: SOURCE REVIEW / LOCAL TEST / APPROVED RUNNER / LIVE E2E;
- remaining blockers and next dependency.

## 4. Acceptance / gates
- No gate moves to PASS on documentation or unexecuted tests.
- G0 stays PARTIAL/BLOCKED until live inventory is bound to exact source/build.
- G3 stays BLOCKED until approved runner evidence exists.
- G4 stays BLOCKED until real adapter/Core authorization, filesystem containment, resource enforcement and OS isolation evidence exist.
- G5-G6 stay BLOCKED until approved end-to-end path and Cla review.
- G7 remains NO-GO.

**Ka authorization:** Continue only the isolated contract/test/adapter design slice in Work 28 Sandbox. No live implementation or deployment authorization is granted.
