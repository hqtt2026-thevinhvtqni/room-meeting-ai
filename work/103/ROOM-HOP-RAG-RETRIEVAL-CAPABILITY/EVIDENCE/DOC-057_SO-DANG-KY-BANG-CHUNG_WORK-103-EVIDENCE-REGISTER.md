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
| EVD-008 | Evidence-support Gate A/B CI runs 42467238385 and 42467375198 | GitHub Actions; heads b2bc26216754c637420ef47e6d3d7c3f2726919e and 35126909f343a1b0c6d7b6c2dcb67aa4526981e | 42467238385: initial build FAIL with 2 defects (32/34 tests passing), fixed in 3512690. 42467375198: py_compile, all unit suites, evidence-support Gate B decision-set step and EVAL_V2 baseline PASS on Python 3.11 and 3.12; corpus-aligned no-answer gate FAIL preserved (no_answer_accuracy=0.300 vs 0.8). Producer: Vibe; details in LOG-W103-20261108-005 and 06_EVIDENCE/VIBE_103_EVIDENCE_SUPPORT_GATEA_GATEB_20261108.md. |
| EVD-009 | Gate C seed corpus diagnostic (report-only, 50-query coverage) | 06_EVIDENCE/VIBE_103_GATE_C_SEED_CORPUS_DIAGNOSTIC_20261109.md; CI runs 42559743132 and 42559810631; heads d9635f4a and e66d3716 | Harness + fact specs V2 (AUTHORED_PENDING_INDEPENDENT_ADJUDICATION). CI-verified: specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 (Q040 retrieval miss). Unit suites, Gate B, baseline and diagnostic steps PASS on Python 3.11/3.12; independent corpus-aligned gate still FAIL 0.300 vs 0.8, preserved. Producer: Vibe; details in LOG-W103-20261109-001. |
| EVD-010 | Corpus diagnostic v2 metrics — citation-source alignment + relaxed-threshold retrieval probe | 06_EVIDENCE/VIBE_103_GATE_C_SEED_CORPUS_DIAGNOSTIC_20261109.md (section 7); CI run #96; head c14939a4eab69a6995fc6289cabc30042eab2014 | REPORT-ONLY, AUTHORED_PENDING_INDEPENDENT_ADJUDICATION. CI-verified: V2 specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 citation_misaligned=2 (Q037/Q045) expected_source_missed=2 (Q037/Q040; relaxed best 0.353077 / 0.19145 vs min_score 0.35). Unit suites PASS; independent corpus-aligned gate still FAIL 0.300 vs 0.8, preserved. Numeric Actions run ID not recorded (anonymous GitHub API quota exhausted from build environment); run number #96 + commit SHA binding. Producer: Vibe; details in LOG-W103-20261109-002. |
| EVD-011 | Retrieval-miss root-cause analysis (diagnostic v3) | 06_EVIDENCE/VIBE_103_RETRIEVAL_MISS_ROOT_CAUSE_20261109.md | REPORT-ONLY, AUTHORED_PENDING_INDEPENDENT_ADJUDICATION. TS port validated against CI anchors (Q040 0.191450, Q037 0.353077, gate 0.300). Key results: Q040 = rank-1 span rejected by threshold (zero-df query terms inflate IDF denominator ~3x; bridge is a 0.75-weight expansion alias); counterfactual matrix: any normalization recovering Q040 re-opens all 10 no-answer leaks; Q037/Q045 citation misalignment = duplicate-content ranking problem (DEBT-ES-08), not threshold. No code/threshold/gate changed. Producer: Vibe; details in LOG-W103-20261109-003. |
