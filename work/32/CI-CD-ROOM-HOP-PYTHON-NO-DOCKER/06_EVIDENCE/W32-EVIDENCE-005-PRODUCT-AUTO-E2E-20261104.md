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
