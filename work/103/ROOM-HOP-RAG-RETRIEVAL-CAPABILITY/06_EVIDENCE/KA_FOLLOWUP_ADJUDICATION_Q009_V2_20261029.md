# WORK 103 — KA Follow-up Adjudication Finding V2
- Reviewer: Ka (CSA / Independent Reviewer)
- Date-time: 2026-10-29 (UTC+07:00)
- Parent review: `06_EVIDENCE/KA_INDEPENDENT_REVIEW_V5_SYNC_GATE_20261029.md`
- Status: PARTIAL SEMANTIC REVIEW — evaluation gate remains BLOCKED.

## Confirmed label disagreement
| Query | Qw V5 label | Ka finding | Evidence |
|---|---|---|---|
| Q009 | NO_ANSWER | **ANSWERABLE** | `00_CORPUS/sales.md` states that when a customer request is received, the sales employee (`nhân viên kinh doanh`) must perform both confirmations, including cement quantity. This directly answers who is responsible. |

Recommended adjudication: keep Qw V5 immutable; record Q009 as an explicit disagreement/adjudication entry and create a new adjudicated dataset version only after the corpus snapshot and hash convention are stabilized. Do not silently edit V5.

## Other checks
- Q008 is consistent with NO_ANSWER: the sales fixture explicitly says it does not define the process for schedule-change requests.
- Q009's current rationale is contradicted by the same source file; this is a confirmed defect, not merely missing provenance.
- Q050 is supported by `00_CORPUS/security.md`, which explicitly prohibits storing or returning system administrator passwords.
- Q015 and Q027 match explicit statements in `00_CORPUS/architecture.md`.
- This pass is not a claim that all 50 rows have completed final adjudication. Queries whose cited evidence is not available in the GitHub branch remain pending source-snapshot verification.

## Gate decision
**BLOCKED.** The V5 file is now synced, but it still references Manifest v3.0, lacks the claimed per-row `label_canonical_sha256` fields, and has no verified freeze/blind-process attestation. The complete source snapshot must be present and verified before final adjudication and evaluation.
— Ka | CSA / Independent Reviewer
