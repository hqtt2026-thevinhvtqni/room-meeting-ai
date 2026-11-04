# DOC-066 — NODE.JS 24 GITHUB ACTIONS PIN UPDATE

- **Document Number:** DOC-066
- **Priority Order:** P1 — CI runner compatibility / warning remediation
- **Work:** 32
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Status:** IMPLEMENTED ON WORK BRANCH — EXACT-SHA VALIDATION PENDING

## 1. Verified release evidence
- `actions/setup-python` v7.1.0 official release is immutable and points to commit `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`. Its exact `action.yml` blob is `645de4f5108b28bcc7ed043ee171770b0754cc35` and declares `runs.using: node24`.
- `actions/upload-artifact` v7.0.1 tag points to commit `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`. Its exact `action.yml` blob is `7cb4d1e81db55320b41217e1a78a1a46e3d2baef` and declares `runs.using: node24`.
- Official references: https://github.com/actions/setup-python/releases/tag/v7.1.0 ; https://github.com/actions/upload-artifact/releases/tag/v7.0.1
- setup-python v6+ requires Actions Runner 2.327.1 or later; Work 32 uses GitHub-hosted `ubuntu-latest`, and exact-SHA CI is the compatibility check.

## 2. Change
- Replace all four old setup-python v5 pins with immutable v7.1.0 commit SHA.
- Replace all four old upload-artifact v4 pins with v7.0.1 commit SHA.
- Keep workflow inputs, job boundaries, artifact names/retention, triggers and read-only permissions unchanged.
- No mutable action tags are used.

## 3. Validation gate
- Exact branch SHA and Actions run ID will be appended after completion.
- Verify all four jobs, artifacts and raw logs; confirm the GitHub Actions Node.js 20 deprecation warning is absent.
- This is separate from F4 and from the Starlette/httpx dependency update.

## BIÊN BẢN / MINUTES
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Decision:** Use verified immutable Node 24 action commits; retain workflow semantics.

## NHẬT KÝ / JOURNAL
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Action:** Verified official release refs and exact action.yml runtime declarations, then updated only action SHA pins in the Work 32 workflow.
- **Result:** Change committed to Work branch; exact-SHA CI validation pending.
