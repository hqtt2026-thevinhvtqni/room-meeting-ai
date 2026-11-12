# KẾ HOẠCH KIỂM CHỨNG WORK 115 / VERIFICATION PLAN
- **STT / Document ID:** DOC-010
- **Priority:** P1
- **Read order:** 10
- **Depends on:** DOC-007; DOC-008; DOC-009
- **Status:** DRAFT — TESTS NOT RUN
- **Version / Updated:** 0.1 / 2026-11-12

## Verification streams — planned, not executed
1. Functional: create project, define work, assign worker, submit report, attach photos, manager review and correction.
2. Authorization: role boundaries, project isolation, worker assignment scope, unauthorized direct API access and session handling.
3. Data integrity: duplicate submissions, retries, concurrent edits, timestamp handling and audit history.
4. Upload: file type/size validation, interrupted upload, retry, access control and orphan cleanup.
5. Mobile usability: common Android browsers, small screens, low bandwidth and accessibility.
6. Reliability: backup/restore, export, failure recovery and service availability.
7. Privacy: retention, deletion, data export, least privilege and secret handling.
8. End-to-end: worker-to-manager report flow using test data, with traceable source commit and test run.

## Evidence requirements
Every test record must identify requirement/test ID, exact source commit/version, environment, method/command, timestamp, raw result, pass/fail and evidence path. Independent QE remains separate from implementation. No test has been run in this initialization.
