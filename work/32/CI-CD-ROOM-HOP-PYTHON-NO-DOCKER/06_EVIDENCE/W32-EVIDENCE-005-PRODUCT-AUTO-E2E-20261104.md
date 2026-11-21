# W32-EVIDENCE-005 — Product-level Auto E2E

- **Document Number:** W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104
- **Priority order:** P0 — Product journey / cross-boundary verification
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** work/32-ci-cd-python-ci-v2
- **Source SHA:** `a39438caa694549a7918d3a86878ee5ff95338de`
- **GitHub Actions:** run #64 — `41722337882` — SUCCESS
- **Runtime:** GitHub-hosted Ubuntu, Python 3.12
- **Evidence date:** 2026-11-04 (project date; GitHub runner logs timestamped 2026-11-03 21:30 UTC)

## 1. Purpose

This evidence upgrades the Work 32 E2E gate from isolated component/adapter roundtrips to one complete ROOM HOP Core product journey, crossing the real HTTP adapter, real MCP stdio subprocess, Core lifecycle, identity registries, persisted transcript and final meeting artifact.

No fake MeetingService, mocked transport, in-memory replacement service or skipped test is used for this scenario.

## 2. Product journey exercised

1. Read-only identity discovery via live HTTP `GET /identities`; assert Vinh remains `human_principal` and Xu remains `ai_agent`.
2. Create a meeting through live HTTP without client-supplied meeting ID; assert Core allocator returns a `MEETING-YYYY-NNN` identifier and state `draft`.
3. Read back the draft meeting through the public list/status filter.
4. Open the meeting through HTTP.
5. Negative policy case: registered but uninvited Claude is rejected from JOIN (HTTP 400).
6. Negative quorum case: START with only the creator joined is rejected (HTTP 400).
7. Valid JOIN by creator Vinh and invited agent Xu; START succeeds only after the two accepted participants exist.
8. Start the actual MCP stdio subprocess and verify the exact four-tool Public V1 inventory.
9. Record an identity-aware paste as Xu and a legacy unidentified paste through MCP; assert correct identity header on the identified paste and no fabricated speaker/header on the legacy paste.
10. Read transcript through MCP; assert both raw records and ordering.
11. Verify `transcript.txt` byte-for-byte against the exact CRLF/LF input payload.
12. Close through the live HTTP lifecycle endpoint using the authorized Xu identity.
13. Verify closed state, closed-list filter, and persisted `final.md`.
14. Verify final artifact contains approved decision/action/summary but does not leak raw AI paste content.
15. Reopen MCP stdio and read the closed meeting/transcript again; verify post-close evidence remains unchanged.

## 3. Exact results

- Unit job — PASS: **157 passed in 2.49s**.
- Product Auto E2E job — PASS: **39 passed, 1 warning in 4.39s**.
- Both jobs completed exact triggering-SHA checkout, Python 3.12 setup, dependency installation, `pip check`, application `compileall`, test execution and JUnit artifact upload.
- New product-level test: `tests/test_ci_product_e2e.py`.
- Existing component, HTTP, MCP and execution-host tests remain enabled; no test was removed or marked skipped to obtain PASS.

## 4. Artifact provenance

- Unit artifact ID: `13271603230`
- Unit artifact SHA-256: `d53fefde32748e5c8bc5cbb44090d041c402b6faeb076fb8bf8533fd274dee18`
- E2E artifact ID: `13273077743`
- E2E artifact SHA-256: `ff7c5cc0e63d39dedd83031cebe6c1a4aa501f153a98cf32eb137b819ceaa729`
- Retention expiry: 2026-11-17 (14 days after upload).

## 5. Coverage boundary — do not overclaim

**PASS:** Complete ROOM HOP Core product workflow through the public HTTP + MCP interfaces and persisted evidence, within the exact scope above.

**NOT RUN / BLOCKED:** HQTT Dashboard browser-to-Core integrated journey. The independently inspected Dashboard source remains on a separate repository/branch:
- Repository: `hqtt2026-thevinhvtqni/hqtt-Dashboard-note`
- Branch: `hqtt-ai-project-structure-082c9`
- Inspected HEAD: `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`
- `src/App.tsx` still defaults to `createMockBridge()`.
- `src/room-hop/bridge/RoomHOPBridge.ts` explicitly labels the bridge as MOCK/client-side.
- The documented `httpBridge.ts` is described as not yet written.
- Its proposed `/api/meetings/{id}/hqtt-bridge` resource is not present in the locked Core HTTP contract. The Core contract separately assigns Workspace working-state to its own authority.
- Therefore, a browser test against the current mock UI would not prove Dashboard→Core semantic integration. No false cross-layer PASS is claimed.

**CD / production:** NOT RUN. No attested staging target, protected deployment approval, deployment credentials/host trust, real health-check target or tested rollback is available in this Work evidence.

## 6. Disposition

- Unit: PASS.
- Core product-level Auto E2E: PASS.
- Dashboard→Core integrated product E2E: BLOCKED / NOT RUN pending architecture/contract reconciliation and an implemented, authorized bridge.
- CD: BLOCKED / NOT RUN.
- Release: NOT RELEASED.
- Work 32: ACTIVE — NOT RELEASED.

This evidence supports a complete automated E2E of the ROOM HOP Core product path, not acceptance of the separate Dashboard integration or production release.


## Final branch SHA revalidation — PASS

The final evidence/documentation commit was independently rerun on its exact SHA:

- Final branch SHA: `ecb263a2d53786e71bdca8eed336b303506c06b4`.
- GitHub Actions run #65: `41722744353` — SUCCESS.
- Unit: 157 passed in 2.07s.
- Product Auto E2E: 39 passed, 1 warning in 3.89s.
- Unit artifact ID `13272412907`; SHA-256 `b80f706f8f91833ccdf69c0102b201957645c77ff346837c4cbdc0dc698f648b`.
- E2E artifact ID `13272817780`; SHA-256 `ae028bf6c2a5c95247fd950ee70ad7a51e69c0801ff5cf2aad5dd9729b3140f3`.
- Artifact retention: 14 days.


## Artifact-level validation extension

Run #67 adds a dependent product-artifact job after the Unit and Product Auto E2E gates. The exact source commit was archived, its SHA-256 checksum generated and verified, the archive extracted into a clean directory, dependencies installed and checked, packages compiled, and the complete product E2E rerun against the extracted artifact.

- Source SHA: `0069157d24d6748cff69f162147b892242d9726f`.
- Run #67: `41723138912` — SUCCESS.
- Artifact-level product E2E: 1 passed in 1.76s.
- Immutable release-candidate artifact ID `13272918198`; uploaded ZIP digest `fa059d00b74fe7e884c98ca95dc9ec283dcb940ffaa0b3b6eec4c25761a299f6`.
- Separate unit and source E2E: 157 passed; 39 passed, 1 warning.
- The release-candidate artifact is not deployed. CD remains BLOCKED / NOT RUN.


## Exact-SHA immutable artifact verification — PASS

- Final tested source SHA: `e451764d4bc900a98f4d0b2d00a1e863ea86b22c`; Actions run #68 `41723597131` SUCCESS.
- Unit: 157 passed; Product Auto E2E: 39 passed, 1 warning; extracted artifact E2E: 1 passed in 2.15s.
- Source archive SHA-256: `76d77939c43b33727a534cbccd06e4240eb106458659b9186f9fb125ca59f0ae`.
- Artifact ID `13271449355`; uploaded ZIP digest `9a688cc80b97e428a2d1b9c39a3c4bc97aa854e7b0715b64e8a7d39aa98c6062`.
- Retention: 14 days. Artifact is a release candidate, not deployed.
