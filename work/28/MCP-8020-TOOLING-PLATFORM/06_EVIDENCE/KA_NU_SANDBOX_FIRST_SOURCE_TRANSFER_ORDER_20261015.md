# NU EXECUTION ORDER — WORK 28 SANDBOX-FIRST SOURCE INTAKE AND DELIVERY
Date: 2026-10-15
Issued by: Ka — CSA
Authority: Vinh
Work: 28 / MCP-8020-TOOLING-PLATFORM
Priority: P0 — START NOW
Mode: E2E-Automatic; source-of-truth and provenance first

## Objective
Move the actual existing ROOM-HOP implementation source needed for Work 28 into Work 28 Sandbox, audit it there, implement and test the Work 28 changes there, and only prepare a final reviewed export for the PC operator when the work is complete. Do NOT copy Work 28 implementation into the PC now, and do NOT modify/restart the PC listener, Core, registry or source during this task.

## Non-negotiable rule
Do not invent or hand-write replacement files for the existing MCP/Core/Sandbox implementation. Work 28 must contain a provenance-traceable snapshot of existing source before implementation work begins. Contract files in 04_CODE are not the real implementation.

## Step A — Locate and collect source into Work 28
1. Use an authorized, read-only source channel available to Nu (PC read-only collector, connected repository, or approved source transfer). Do not assume public GitHub HEAD equals the PC working tree.
2. Canonical PC source reference supplied so far: repo path D:\ROOM-HOP-CLEAN\room-meeting-ai; reported HEAD d7c90d9d31062d389810808e43dfdd19d7711b75 — recheck at collection time.
3. Collect the full relevant source tree and dependencies, preserving relative paths:
   - room_hop_mcp/mcp_http_main.py
   - room_hop_mcp/sandbox_service.py
   - room_hop_mcp/sandbox_identity.py
   - remaining room_hop_mcp/ source needed for tool registration and handlers
   - Core :8000 route/authz/policy modules actually called by these handlers
   - relevant tests and safe dependency/config manifests
4. Exclude secrets, .env, access tokens, private keys, private user data and runtime state.
5. Place snapshot under MCP-8020-TOOLING-PLATFORM/04_CODE/source_snapshot/. Include a manifest with source origin, timestamp, branch/HEAD, dirty/untracked status, included/excluded files, per-file SHA-256, and archive SHA-256. If PC working tree is dirty, report that explicitly; do not call it clean HEAD.
6. If no authorized read-only source path is available, STOP and report the exact access gap. Do not fabricate source, do not substitute a different revision silently, and do not write anything to PC.

## Step B — Verify and audit
1. Verify archive hash and per-file hashes after import.
2. Trace actual registered tools -> handlers -> service -> Core authorization -> filesystem operation -> tests.
3. Identify duplicates and missing P0 capabilities (sandbox_search, sandbox_stat, sandbox_read_range; capability_discover only if it queries the actual runtime registry).
4. Keep proposed/static registry separate from live registered MCP tools.
5. Record precise source paths and callable names; do not infer from filenames or contract models.

## Step C — Implement only in Work 28
After source audit, make changes only inside Work 28 Sandbox and only in the imported implementation snapshot:
- Core authorization remains authoritative; server-derived principal only.
- Work-scoped path containment, traversal/drive/UNC/ADS and symlink/reparse-point safety.
- Enforced byte/entry limits at actual adapter/service boundary.
- Bounded outputs/timeouts and safe errors.
- Negative tests: forged identity, cross-Work, denied operation, malformed path, symlink/race where testable, exact-limit, over-limit, multibyte byte count, no partial writes on rejection.
- No unrestricted Python, shell, generic process launch or alternate execution host.
- No second bridge/runner or duplicate Core.

## Step D — E2E-Automatic evidence
Run deterministic tests within the sandbox/approved runner. Capture exact command, environment, stdout, stderr, exit code, discovered/run counts, per-file hashes and immutable evidence reference. A green contract-only test is not source integration E2E.
Separate results into contract/unit, service/adapter, connector, and live PC E2E. Live PC E2E remains untested unless an authorized test path exists; do not change the live PC merely to obtain a PASS.

## Step E — Final delivery
Prepare a self-contained reviewed export bundle and manifest inside Work 28. Nu cannot self-certify. Go checks reproducibility, Cla performs independent security review/veto, Ka adjudicates gates, and Vinh decides release. Only after explicit approval may an operator transfer the final artifact to PC. No PC import or runtime change now.

## Required immediate reply from Nu
Return one of:
- SOURCE_TRANSFER_STARTED with source channel and planned manifest; or
- BLOCKED_SOURCE_ACCESS with exact unavailable path/permission and the smallest needed access; or
- SOURCE_SNAPSHOT_IMPORTED with manifest path, HEAD, file count, archive SHA-256, and hash verification result.

## Status at issue time
Work 28 ACTIVE / NOT LOCKED. Canonical implementation source not yet present in Work 28. Existing 31 contract tests are PASS AS REPORTED only, not independently rerun and not live E2E. python_run, live registry mutation, PC source edits, service restart, deployment and release remain NO-GO.