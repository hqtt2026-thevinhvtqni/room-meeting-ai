# KA Assignment — Work 28 next execution step
Date: 2026-10-15
Owner: Ka CSA
Authority: Vinh
Coordinator: Xu
Work status: ACTIVE / NOT LOCKED
Purpose: Continue Work 28 from evidence, avoid repeated planning and avoid duplicate tools.

## Mission
Perform READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF for the next Work 28 milestone. Do not stop at a plan-only report.

## Step 1 — Establish the source of truth
1. Read the latest Work 28 decisions and evidence:
   - MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/CROSS_WORK_TOOL_CAPABILITY_AUDIT_20261015.md
   - MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/TOOL_GAP_DECISION_20261015.md
   - MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md
   - relevant Go/Cla/Ka checkpoints in 06_EVIDENCE.
2. Reconcile actual source files for Core :8000, Sandbox service, MCP :8020 registration, authorization path and existing tests. Do not infer implementation from a contract or filename.
3. Explicitly distinguish Sandbox connector capabilities from the live PC MCP :8020 tools/list. The PC live registry is currently UNVERIFIED; do not claim otherwise.

## Step 2 — Trace P0 gaps before implementation
Check whether Core/Sandbox already provides equivalents for:
- bounded authorized Work artifact search;
- metadata/stat for one authorized relative path;
- bounded line/byte-range read;
- discovery of actually registered MCP capabilities and schemas.
Record exact source paths, callable routes/functions, authorization flow, tests and evidence. Reuse existing functions where adequate.

## Step 3 — Build only the confirmed missing slice
If and only if a capability is truly missing, implement the smallest safe P0 slice in the canonical source:
- Work-root relative paths only; reject traversal, absolute paths, drive/UNC paths and alternate data streams;
- Core authorization remains authoritative;
- bounded outputs and timeouts; redact secrets;
- stable response envelope with request_id, status, message, typed result, evidence_ref where available, contract_version;
- negative tests for denied access and malformed paths;
- no unrestricted Python, shell, command strings or process launch;
- no duplicate runner, bridge, or per-Work wrappers.
If source/runtime access is insufficient, mark BLOCKED with exact missing evidence and a single actionable handoff; do not fabricate a PASS.

## Step 4 — Verify end to end
Run the available targeted tests, capture results, and verify registration/call/readback through MCP → Core → authorized capability. Clearly separate:
- source/unit-test PASS;
- connector-level PASS;
- live PC :8020 E2E PASS.
Never promote one level as proof of another. If PC endpoint is not accessible from this execution context, report that limitation and specify the exact evidence needed from the PC runtime.

## Step 5 — Handoff
Update Work 28 evidence and NHAT_KY_THI_CONG.md with:
- files changed;
- tests actually run and exact outcomes;
- security-negative results;
- registration and E2E evidence;
- remaining blockers;
- DONE / PASS / DECISION / BLOCKED status.
Do not lock Work 28 until live integration gates pass.

## Acceptance criteria
A. API/source inventory is evidence-based.
B. No duplicate capabilities are built.
C. Any new tool is actually registered and callable, not merely present in a proposal registry.
D. Core authorization and path confinement are tested.
E. End-to-end claims match collected evidence.
F. Work 28 remains ACTIVE / NOT LOCKED until release gates pass.

## Immediate priority
Start with source/API trace for the four P0 capabilities and live-registry evidence request. Do not spend another cycle re-writing plans; move to implementation only when the missing capability is demonstrated.
