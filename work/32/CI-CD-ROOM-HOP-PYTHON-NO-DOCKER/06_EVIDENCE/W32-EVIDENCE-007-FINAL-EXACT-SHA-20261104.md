# W32-EVIDENCE-007 — Final Exact-SHA Product Pipeline

- **Document Number:** W32-EVIDENCE-007-FINAL-EXACT-SHA-20261104
- **Priority order:** P0 — Final product Auto E2E and artifact provenance
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** work/32-ci-cd-python-ci-v2
- **Exact source SHA:** `4a931a351432a1ce6a06b84f05ed6fa3c788a1eb`
- **GitHub Actions:** run #70 — `41724182414` — SUCCESS
- **Runtime:** GitHub-hosted Ubuntu, Python 3.12

## 1. End-to-end gates

| Gate | Result | Raw result |
|---|---|---|
| Compile + dependency consistency | PASS | `compileall`, `pip check` completed |
| Bounded Unit | PASS | 157 passed in 1.90s |
| Core Product Auto E2E | PASS | 39 passed, 1 warning in 2.74s |
| Immutable artifact build | PASS | exact-SHA archive + SHA-256 checksum |
| Artifact extraction + dependency check | PASS | `pip check` + `compileall` |
| Product E2E against extracted artifact | PASS | 1 passed in 2.52s |

## 2. Immutable product artifact

- Archive: `room-hop-4a931a351432a1ce6a06b84f05ed6fa3c788a1eb.tar.gz`
- SHA-256: `0b14943b1a85201fa0dc02ba0f823b5fa15440ed0935d7da5a020aa29c3861a2`
- Product artifact bundle ID: `13272004526`
- Uploaded ZIP digest: `24221ef509286698cc73ce3edbe0fd20650cbf5cdd89745e86b3f728996f4d21`
- Unit artifact ID `13272199414`, ZIP digest `878c286f3e84b392560c917715d5bf5b5e7c7979fac63d7d5c0c7345795b5e87`.
- Product E2E artifact ID `13273940178`, ZIP digest `543b2e0a0641e6de9d205aaa278e5f038132ffdc7fb54e9add6e971b2d52cf0a`.
- Retention: 14 days.

## 3. Branch and release boundary

- Main HEAD: `157e88e2cd821a0b53bdcabd6483956e6bc2074a`.
- Work branch: 70 ahead / 32 behind.
- Merge base: `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No merge, rebase, cherry-pick, production deployment or secrets mutation.

## 4. Product boundary — honest status

- Complete Core product workflow through live HTTP, actual MCP stdio subprocess, persistent transcript and final artifact: PASS.
- Dashboard→Core browser journey: BLOCKED / NOT RUN. The separate Dashboard repo still defaults to `createMockBridge()`; its proposed bridge contract is not implemented and conflicts with the locked Core/Workspace ownership boundary.
- CD/staging/production: BLOCKED / NOT RUN. No attested staging target, protected approval, deployment credentials/host trust, health-check target or tested rollback.
- Independent Vibe review and safe branch reconciliation remain pending.

**Disposition:** Core product CI + Auto E2E + immutable artifact verification PASS; Dashboard integration BLOCKED; CD BLOCKED; NOT RELEASED.
