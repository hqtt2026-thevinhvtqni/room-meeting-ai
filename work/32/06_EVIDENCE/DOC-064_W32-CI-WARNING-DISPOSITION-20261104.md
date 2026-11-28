# DOC-064 — CI WARNING DISPOSITION: NODE.JS 20 ACTION RUNTIME AND STARLETTE/HTTPX
- **Document Number:** DOC-064
- **Priority Order:** P1 — CI reliability and dependency compatibility
- **Name:** Ka
- **Title:** CSA / Delegated Work 32 Execution Owner
- **Date-Time:** 2026-11-04 15:48 Asia/Ho_Chi_Minh
- **Status:** COMPLETE — NODE.JS 24 AND STARLETTE/HTTPX2 WARNINGS RESOLVED (RUN #36 / RUN #39)
- **Evidence basis:** GitHub Actions run #26, ID 41792043382, exact SHA 14cb29a5228abe9b9195f2bee44c96b92f5c2a32; jobs 126447415173 and 126447415347; workflow blob 48c3a649e31f97285530fdedf730718ace5622a9; requirements blob 2fdc940632d880df954355878d4963c099677468; constraints blob 8f30ded0ff6a6e4ffdc8d690c494de161e7e2ab8.

## 1. Node.js 20 deprecation warning
- Run #26 reports: `actions/setup-python` pinned to immutable SHA `a26af69be951a213d495a4c3e4e4022e16d87065` (commented v5) and `actions/upload-artifact` pinned to immutable SHA `ea165f8d65b6e75b540449e92b4886f43607fa02` (commented v4) target Node.js 20; GitHub runner forces these actions to execute on Node.js 24.
- This is a GitHub Actions runtime deprecation warning, not a failed test or proof of current runtime malfunction. Run #26 completed all four jobs successfully.
- Both actions are pinned by full commit SHA. Do not replace pins by mutable tags or guess newer SHAs.
- Recommended next step: verify the official release/changelog for Node.js 24-compatible versions, inspect their immutable commit SHAs and inputs/behavior, then run a controlled exact-SHA validation before any pin update. No workflow change is made in this document.

## 2. Starlette/httpx deprecation warning
- Product Auto E2E completed **45 passed, 1 warning**. Warning emitted from installed `fastapi/testclient.py`: using `httpx` with `starlette.testclient` is deprecated; message recommends `httpx2`.
- Exact CI environment from run #26: FastAPI 0.162.0, Starlette 1.10.0, httpx 0.28.1, MCP 1.28.1. `constraints-ci.txt` pins these observed versions; `requirements.txt` declares broad lower bounds for FastAPI/httpx.
- The warning is a deprecation signal, not a test failure. It does not by itself prove that a dependency replacement is safe or required. In particular, do not add httpx2 or change the Starlette/FastAPI/httpx pins without checking dependency compatibility, test-client API behavior, MCP/HTTP usage, and the full CI matrix.
- Recommended next step: isolate the source/import path and verify supported dependency combinations in a separate controlled branch/run; preserve current known-good constraints until that evidence exists.

## 3. Disposition
- RUN #26: **PASS — 4/4 jobs**; unit 167 passed; tooling 20 tests OK; Product Auto E2E 45 passed / 1 deprecation warning; immutable artifact verification 1 passed.
- Warnings: **RECORDED / NON-BLOCKING FOR RUN #26**. They remain maintenance items; they do not invalidate the exact-SHA CI result.
- No action pin, dependency, workflow, product source, or test was changed. No tests were skipped or weakened.
- No merge/rebase/cherry-pick, strict coverage, CD, deployment, acceptance, or release authorization is implied.
- Work 32 remains **ACTIVE — NOT RELEASED**.

## BIÊN BẢN / MINUTES
- **Name:** Ka
- **Title:** CSA / Delegated Work 32 Execution Owner
- **Date-Time:** 2026-11-04 15:48 Asia/Ho_Chi_Minh
- **Decision:** Record exact warning evidence and recommend controlled compatibility verification only; no remediation applied.

## NHẬT KÝ / JOURNAL
- **Name:** Ka
- **Title:** CSA / Delegated Work 32 Execution Owner
- **Date-Time:** 2026-11-04 15:48 Asia/Ho_Chi_Minh
- **Action:** Audited run #26 logs, workflow action pins, requirements and constraints. Recorded warning origins, exact versions, non-blocking disposition and next verification gates.
- **Result:** Analysis recorded; remediation remains NOT AUTHORIZED.


## Node.js 24 remediation addendum — W32-LOG-44
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- Verified `actions/setup-python@v7.1.0` commit `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0` and `actions/upload-artifact@v7.0.1` commit `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`; both exact action.yml files declare `node24`.
- Updated four workflow references for each action, pinned by full commit SHA. Workflow semantics and permissions are unchanged.
- DOC-066 records official release references and exact runtime evidence. Exact-SHA CI verification is pending; Node 20 warning is not yet declared resolved.
- Starlette/httpx dependency remediation remains a separate change.


## Node.js 24 exact-SHA disposition — W32-LOG-45
- Name: Ka
- Title: CSA / Backend execution owner delegated by Xu
- Date-Time: 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- Run #36 / 41806199038, exact SHA 7984d167a1eec935f062dd17894d89ff90503619: COMPLETED / SUCCESS, 4/4 jobs.
- Raw logs of all four jobs inspected: zero Node.js 20 deprecation warnings.
- Node.js Actions warning is RESOLVED for this workflow revision. Evidence W32-EVIDENCE-022 / DOC-066.
- Starlette/httpx warning remains open and is the next independent dependency change.


## Starlette/httpx2 compatibility remediation — W32-LOG-46
- Name: Ka
- Title: CSA / Backend execution owner delegated by Xu
- Date-Time: 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- Raw run #36 confirms StarletteDeprecationWarning from FastAPI TestClient import. Official Starlette TestClient docs recommend httpx2; official Starlette release notes confirm TestClient support.
- Added httpx2 >=2.16.0 and exact CI constraint httpx2==2.16.0. Existing httpx 0.28.1 remains installed; no FastAPI/Starlette upgrade.
- DOC-067 records the compatibility basis. Exact-SHA CI, pip check, raw warning logs and transitive freeze inspection pending.


## Final CI warning disposition — W32-LOG-48
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- Node.js Actions warning: RESOLVED on run #36 / 41806199038, exact SHA 7984d167a1eec935f062dd17894d89ff90503619. Four jobs inspected; zero Node.js 20 deprecation warnings.
- Starlette/httpx TestClient warning: RESOLVED on run #39 / 41806906885, exact SHA 17d7d87c9e09b08026fd8bdda29578c04bd1aa35. httpx2 2.16.0, httpcore2 2.16.0 and truststore 0.10.5 pinned; pip check passed; zero StarletteDeprecationWarning in unit/E2E logs.
- Both warning remediations were separate changes with independent exact-SHA validation. No FastAPI/Starlette upgrade; original httpx retained.
- Remaining Work 32 gates are independent: Browser Adapter deferred, Track B blocked, branch governance pending, CD/release blocked.
