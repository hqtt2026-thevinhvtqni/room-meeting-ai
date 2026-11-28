# DOC-106 — Work32 Security Remediation Build Plan

- **Document Number:** DOC-106
- **Priority:** P0 — security remediation execution
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Base:** work/32-main-integration-20261109 at 2ae2011504aa91156f869813104b9cc29edaafe4
- **Status:** ISOLATED REMEDIATION BRANCH — IMPLEMENTATION IN PROGRESS

## 1. Authority
Execute Xu W32-LOG-20261109-XU-03 and Cla W32-EVIDENCE-017 on an isolated Work32 branch. No main merge, staging, production, or release. Preserve Public MCP V1 exact four-tool contract and F4 limits.

## 2. Implementation order
1. S4: fail-closed paste membership — require non-empty identity and active JOIN_ACCEPTED participant.
2. S5: short committed SQLite reservation, transcript append outside lock, exact reservation compensation on append failure; controlled busy/lock response.
3. S6: structured MCP rate-limit tool error with retry seconds; keep HTTP 429 + Retry-After.
4. S9: redact URL query and fragment before transcript/evidence persistence.
5. S1/S2/S2b: browser URL/redirect/IP controls, path confinement, Chromium sandbox configuration, tests; coordinate with Cla's review.
6. S3/S7/S8: authenticated actor boundary and path validation; keep external exposure loopback-only.
7. auth_verified: trace consumers and replace misleading semantics only with security-reviewed contract.

## 3. Verification
- Add focused positive/negative tests for each security boundary.
- Run focused tests and complete CI on exact SHA.
- Request independent Qw retest and Cla security re-review.
- No PASS based only on source inspection.

## 4. Qw source
The only Qw QE report currently retrieved is for Work70 Dashboard, not W32. W32 Qw report remains pending retrieval; this build plan does not claim Qw approval.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Record:** Isolated remediation plan created; no source changes in this document commit.

## NHẬT KÝ
- **W32-LOG-20261109-95**
- Created isolated branch work/32-security-remediation-20261109 from the clean integration branch.
- Recorded Xu/Cla-directed remediation sequence and evidence requirements.
