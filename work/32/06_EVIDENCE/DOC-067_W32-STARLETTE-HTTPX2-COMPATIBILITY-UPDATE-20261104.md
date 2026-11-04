# DOC-067 — STARLETTE TESTCLIENT HTTPX2 COMPATIBILITY UPDATE

- **Document Number:** DOC-067
- **Priority Order:** P1 — CI test-runtime deprecation remediation
- **Work:** 32
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Status:** IMPLEMENTED ON WORK BRANCH — EXACT-SHA VALIDATION PENDING

## 1. Confirmed warning and compatibility evidence
- Exact run #36 / `41806199038` logs report `StarletteDeprecationWarning` at `fastapi/testclient.py:1`: using plain `httpx` with `starlette.testclient` is deprecated; install `httpx2`.
- Official Starlette TestClient documentation states TestClient is built on httpx2; plain httpx remains supported but deprecated, and httpx2 is included in Starlette's `full` extra: https://www.starlette.io/testclient/
- Starlette release notes record httpx2 support in TestClient from 1.2.0 and addition to the full extra in 1.3.0: https://www.starlette.io/release-notes/
- PyPI lists `httpx2 2.16.0`, released 2026-10-21, requiring Python >=3.11; Work 32 CI uses Python 3.12: https://pypi.org/project/httpx2/2.16.0/

## 2. Narrow dependency change
- Add `httpx2>=2.16.0` to `requirements.txt`.
- Pin `httpx2==2.16.0` in `constraints-ci.txt`.
- Retain existing `httpx>=0.27.0` / `httpx==0.28.1`; the application/MCP stack may still use the original package. The new package supplies the Starlette TestClient implementation and does not require replacing runtime httpx.
- Do not bump FastAPI or Starlette; the current Starlette 1.10.0 supports httpx2. Avoid unrelated dependency upgrades.
- CI's existing pip check, unit, Product Auto E2E and immutable artifact checks validate the combined environment. The resulting pip freeze must be inspected for newly resolved transitive packages before finalizing constraints provenance.

## 3. Validation gate
- Exact-SHA CI must complete 4/4.
- Verify pip check succeeds and all TestClient-based tests pass.
- Inspect raw unit/E2E/artifact logs and confirm StarletteDeprecationWarning is absent.
- Record actual pip freeze additions and pin newly introduced transitive dependencies based on observed output, not guesses.
- This is separate from DOC-066 Node.js Actions remediation, already validated in run #36.

## BIÊN BẢN / MINUTES
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Decision:** Add the supported httpx2 client without removing the existing httpx dependency or upgrading FastAPI/Starlette.

## NHẬT KÝ / JOURNAL
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Action:** Matched raw warning to official Starlette TestClient documentation and PyPI httpx2 release; applied only the additive httpx2 dependency and exact direct pin.
- **Result:** Work branch commit and exact-SHA CI validation pending.
