# WORK 70 — EVIDENCE REGISTER
- **STT / Document ID:** DOC-014
- **Priority:** P1
- **Read order:** 19
- **Depends on:** DOC-004; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.1 / 2026-10-30

Machine-readable source: `EVIDENCE_REGISTER.json` (schema_version 1.1), validated by `EVIDENCE_REGISTER.schema.json` v1.1. This Markdown file is the human-readable index and must remain consistent with the JSON source.

Schema v1.1 adds optional claim/requirement/test/decision references, artifact version/source commit, verifier and verification metadata, limitations, counter-evidence, supersession, access classification and retention. Existing v1.0 records remain compatible. A record in state VERIFIED now requires verifier, verified_at, verification_method and verification_scope. Existing records remain RECORDED until independently verified.

Version: 1.0
Status: ACTIVE INDEX / EVIDENCE MUST BE VERIFIED
Purpose: Cross-phase index of inspectable evidence. This file indexes artifacts; it does not itself prove their claims.

## Evidence rules
- Every evidence item has a unique evidence_id and stable Work ID.
- Record artifact path/URI, SHA-256 when available, media type, producer, timestamp, environment/source, related requirement/WP/gate, reviewer and verification state.
- Verification states: MISSING, RECORDED, VERIFIED, REJECTED.
- A file write or a contributor statement is RECORDED at most; independent inspection/test is required for VERIFIED.
- Do not store credentials, API keys, passwords, private prompts or unnecessary personal data.
- Preserve historical records. Corrections create a new record/version; do not silently rewrite the past.

## Work 70 evidence index
| Evidence ID | Artifact | Related WP/Gate | Producer | Timestamp | Integrity | Reviewer | State |
|---|---|---|---|---|---|---|---|
| E70-DOC-001 | README.md / Work standard v1.1 | WP-70-01 / G0-G3 | Xu AI-01 | 2026-10-30 | Sandbox readback available; hash not recorded | Pending | RECORDED |
| E70-DOC-002 | 00_ROOT/WORK_MANIFEST.md | WP-70-01 / G0 | Xu AI-01 | 2026-10-30 | Sandbox readback available; hash not recorded | Pending | RECORDED |
| E70-ARCH-001 | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | WP-70-01 / G3 | Xu AI-01 | 2026-10-30 | Sandbox readback available; hash not recorded | Pending | RECORDED |
| E70-DASH-001 | DASHBOARD/index.html + PRODUCT_STATUS.json + schema | WP-70-03 / G3-G5 | Xu AI-01 | 2026-10-30 | Pending runtime/schema validation | Qw pending | RECORDED |
| E70-STOR-001 | 05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | WP-70-05 | Xu AI-01 | 2026-10-30 | GitHub/Sandbox readback matched | Qw pending | RECORDED |
| E70-STOR-002 | 05_BUILD/05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | WP-70-05 | Xu AI-01 | 2026-10-30 | GitHub/Sandbox readback matched | Qw pending | RECORDED |
| E70-CORE-001 | 05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | WP-70-04 | Xu AI-01 | 2026-10-30 | Source review captured; no runtime verification | Qw pending | RECORDED |

No evidence item is marked VERIFIED until its artifact is independently checked against the claim it supports.
| E70-CONSOL-001 | 06_EVIDENCE/WORK70_CONSOLIDATION_CHECK_20261030.md | WP-70-01..06 | Xu AI-01 | 2026-10-30 | GitHub/Sandbox readback pending | Qw pending | RECORDED |
