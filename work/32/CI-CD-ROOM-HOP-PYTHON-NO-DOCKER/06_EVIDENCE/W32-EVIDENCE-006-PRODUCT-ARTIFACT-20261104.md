# W32-EVIDENCE-006 — Immutable Product Artifact

- **Document Number:** W32-EVIDENCE-006-PRODUCT-ARTIFACT-20261104
- **Priority order:** P0 — Product artifact provenance / release-candidate verification
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** work/32-ci-cd-python-ci-v2
- **Artifact source SHA:** `0069157d24d6748cff69f162147b892242d9726f`
- **GitHub Actions run:** #67 — `41723138912` — SUCCESS
- **Runtime:** GitHub-hosted Ubuntu, Python 3.12

## 1. Build provenance

- Built immutable source archive using `git archive` from the exact triggering commit SHA.
- Archive: `room-hop-0069157d24d6748cff69f162147b892242d9726f.tar.gz`.
- Generated SHA-256 sidecar and verified it with `sha256sum --check`.
- Extracted the archive into a clean directory; the test did not run against the original checkout.

## 2. Artifact execution

- Installed declared dependencies from the extracted artifact.
- `pip check`: PASS.
- `compileall` over `core`, `agents`, `execution_host`, `room_hop_mcp`: PASS.
- Ran `tests/test_ci_product_e2e.py` from the extracted artifact.
- Result: **1 passed in 1.76s**.
- This repeats the complete HTTP → MCP stdio → persisted transcript → close → final artifact → post-close readback journey using the packaged product source.

## 3. Pipeline results

- Unit job: **157 passed in 2.72s**.
- Product Auto E2E job: **39 passed, 1 warning in 3.39s**.
- Product artifact job: archive/checksum/extract/dependency/compile/product E2E all PASS.
- All three jobs: SUCCESS.
- Product release-candidate artifact ID: `13272918198`.
- Uploaded artifact ZIP SHA-256: `fa059d00b74fe7e884c98ca95dc9ec283dcb940ffaa0b3b6eec4c25761a299f6`.
- Retention: 14 days; expires 2026-11-17.

## 4. Disposition and boundary

- Core product functional Auto E2E: PASS.
- Immutable product artifact + artifact-level E2E: PASS.
- Dashboard→Core browser E2E: BLOCKED / NOT RUN; the separately maintained Dashboard source still defaults to `createMockBridge()`, and its proposed bridge endpoint is not part of the locked Core/Workspace contract.
- CD/staging/production deployment: NOT RUN; no attested staging target, protected approval, deployment credentials/host trust, health check or tested rollback.
- No main merge, rebase, cherry-pick, secrets mutation or production deployment.

**Status:** Core product CI + Auto E2E + immutable artifact verification PASS; Dashboard integration and CD remain BLOCKED; NOT RELEASED.
