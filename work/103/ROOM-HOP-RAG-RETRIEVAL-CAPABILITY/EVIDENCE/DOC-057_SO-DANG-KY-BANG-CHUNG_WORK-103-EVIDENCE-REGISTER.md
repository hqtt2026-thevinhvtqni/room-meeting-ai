# SỔ ĐĂNG KÝ BẰNG CHỨNG WORK 103 / WORK 103 EVIDENCE REGISTER
- **STT / Document ID:** DOC-057
- **Priority:** P0
- **Read order:** 4
- **Depends on:** DOC-001; DOC-055; DOC-056
- **Status:** ACTIVE — INITIAL INDEX
- **Version / Updated:** 1.0 / 2026-11-08

## Canonical evidence policy
This register is the single cross-phase evidence index. Existing 06_EVIDENCE/ remains a legacy evidence location while CI paths and inbound links are audited. Historical files remain unchanged and are referenced, not silently copied or deleted.

| Evidence ID | Evidence / source | Location | Status / interpretation |
|---|---|---|---|
| EVD-001 | CI run 40668733280 | GitHub Actions run; head 5f91f3ea2143dafaa5af958dc2bb431399e93621 | SUCCESS confirmed by user; EVAL_V2 and both unit suites green at that head |
| EVD-002 | Blind retrieval challenge pool V1 | 05_TEST/BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json | 50 candidate queries; UNLABELED; not valid for metric reporting |
| EVD-003 | Controlled retrieval experiment V1 | 06_EVIDENCE/CONTROLLED_RETRIEVAL_EXPERIMENT_20261028.md | Historical experiment on prior labeled set; not blind-pool results |
| EVD-004 | Independent replication addendum | GitHub commit 730250d | Replication record; exact current path requires readback before future citation |
| EVD-005 | Vibe evidence-support Gate A/B report | 06_EVIDENCE/VIBE_103_EVIDENCE_SUPPORT_GATEA_GATEB_20261108.md | Newer technical evidence; requires mapping to lifecycle/gates |
| EVD-006 | Prior CI/evaluation/label audit reports | 06_EVIDENCE/ | Historical evidence; preserve original status and provenance |

## Evidence record minimum fields
Every new evidence entry must record evidence ID, purpose, producer, UTC+07 timestamp, exact branch and commit, command/method, scope, raw result or immutable artifact reference, PASS/FAIL/BLOCKED/NOT VERIFIED, limitations and next step.

Do not infer PASS from a file existing or from a different commit's CI. Never overwrite failed or superseded evidence.

| EVD-007 | Work 103 CI run 42467546737 (run #85) | GitHub Actions, head f56f86cb9c8ba2be8be990d8cebdb0a1068f0daa | FAILURE on Python 3.11 and 3.12 at independent Manifest V4 + Ka V3 corpus-aligned evaluation gate; no_answer_accuracy=0.300 vs required 0.8. Unit tests, syntax, Gate B and existing EVAL_V2 step succeeded. Controlled experiment steps skipped. Preserve as failure evidence; do not weaken gate. |
