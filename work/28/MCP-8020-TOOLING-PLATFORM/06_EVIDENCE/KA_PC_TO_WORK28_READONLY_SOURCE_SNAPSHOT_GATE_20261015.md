## KA SOURCE SNAPSHOT GATE — PC → WORK 28 — 2026-10-15

### Decision
Accepted the source-of-truth correction: Work 28 currently contains contract/validator code and tests plus architecture/evidence documents, but not the canonical implementation tree required for source-level audit. The reported 31 tests validate only the reconstructed contract snapshot; they do not validate the live MCP/Core/Sandbox implementation.

Do NOT create substitute `room_hop_mcp` implementation files in Work 28. That would create a second implementation and could diverge from the PC listener on :8020.

### Required read-only source bundle from PC repo
Canonical repo: `D:\ROOM-HOP-CLEAN\room-meeting-ai`
Reported HEAD: `d7c90d9d31062d389810808e43dfdd19d7711b75` (must be rechecked at bundle creation time).

Include, if present:
- `room_hop_mcp/mcp_http_main.py`
- `room_hop_mcp/sandbox_service.py`
- `room_hop_mcp/sandbox_identity.py`
- the complete `room_hop_mcp/` Python source tree and tests relevant to MCP tool registration/handlers
- canonical Core :8000 authorization/policy modules and route handlers actually called by these handlers
- the tests that cover those modules and the relevant dependency/config manifests (no secrets, `.env`, tokens, private keys, user data, or runtime state)
- a manifest with Git HEAD, branch, `git status --short`, file list, per-file SHA-256, bundle SHA-256, and creation time

### Integrity and provenance requirements
1. Create a read-only snapshot from the canonical PC repo; do not edit source, restart services, change registry, or alter the listener.
2. Preserve relative paths in the archive under `MCP-8020-TOOLING-PLATFORM/04_CODE/source_snapshot/` when imported into Work 28; keep the manifest beside the snapshot.
3. Compare bundle HEAD and per-file hashes against the source on PC at collection time. If the working tree is modified, record each modified/untracked file and include only explicitly approved implementation/test/config files; never silently label the bundle as clean HEAD.
4. Record the live :8020 process identity/command line and listener endpoint as separate runtime metadata. Source snapshot hashes alone do not prove the running process loaded those files.
5. After import, verify archive hash and a sample of extracted per-file hashes. Then trace handlers → service → Core authz → registered tools → tests before any code changes.

### Gate state
- Canonical implementation source imported into Work 28: BLOCKED — PC-generated bundle not yet present.
- Contract snapshot test result: PASS AS REPORTED only; not source E2E.
- No substitute implementation authorized.
- Next action owner: PC-side collector/authorized operator must create and transfer the read-only bundle. Ka can then audit the imported source, define targeted regressions and coordinate Nu/Go/Cla review.

### Safety
No credentials or secrets in the bundle. No PC writes, no service restart, no live registry mutation, no `python_run`, no deployment/release. Work 28 remains ACTIVE / NOT LOCKED.
