# WORK 103 — Evidence-Support Stage: Contract V3 + Gate A Dataset + Gate B Build (2026-11-08)

- Author: Vibe (GLM 5.3 via Vibe Work agent)
- Date: 2026-11-08 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Build authorization: Vinh, in the Work 103 coordination conversation, after reviewing the branch state (V2 proposal + V2 pre-review, both ending BLOCKED with gaps B1–B6).
- Status: **GATE B PROTOTYPE BUILT AND CI-WIRED; GATE A INDEPENDENT ADJUDICATION OPEN; GATE C/D OPEN; E2E CLOSED.**

## 1. What was built (single commit)

1. `03_ARCHITECTURE/EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md` — interface contract V3 closing the six blocking findings B1–B6 of `KA_EVIDENCE_SUPPORT_STAGE_V2_REVIEW_20261029.md`: T4a/T4b deterministic split (B1), frozen request/response schema with 9 reason codes and locked precedence (B2), fact-identity/scope/value-conflict rules with fail-closed same-scope conflicts and no authority-resolution policy (B3), metamorphic score-independence protocol (B4), adjudication protocol (B5), coverage matrix enforced structurally by the runner (B6).
2. `05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json` — Gate A expected-support-decision dataset, SEPARATE from labels V3 (untouched): 11 gate-counted rows covering T1–T7 (+T4a/T4b split) plus 3 coverage rows (C_SUPPORTED, C_NO_CANDIDATES, C_SCOPED_DIFFERENCE), and 2 pending non-gate-counted rows for the borderline cases Q008/Q037 required by V2 section 6. Every row carries exact spans, rationale, and an adjudication record.
3. `04_CODE/rag_evidence_support.py` — deterministic five-stage decision engine (provenance → absence → negation → conflict → support → insufficient). The retrieval score is accepted for ordering and NEVER read by the decision logic (B4 independence by construction). Strict schema validation with a structural coverage check; per-case gate runner, exit 1 on any single row mismatch or coverage gap; pending rows reported but excluded.
4. `05_TEST/test_rag_evidence_support.py` — Gate B suite: committed-set validation, per-case expected decisions and reason codes, the B4 metamorphic protocol (score perturbation/reorder/removal invariance + span-text sensitivity), provenance fail-closed unit cases (including bool/string line-number forgery), locked-rule behaviour tests, 12 schema-rejection mutations, and a runner mismatch test. No aggregate score; every case reported individually.
5. `.github/workflows/work-103-rag-ci.yml` — CI extended: py_compile and unittest now include the new files; a new Gate B step (`python rag_evidence_support.py`) runs BEFORE the labeled retrieval evaluation so its verdict is observable even though the corpus-aligned no-answer gate below it is still expected to FAIL (known, preserved baseline per `KA_CORPUS_V4_V3_EVALUATION_FAILURE_REPORT_20261029.md`). No existing step was weakened, reordered, or removed.

## 2. Pre-commit verification (honest method note)

The build environment available to Vibe at authoring time executes TypeScript, not Python. Before writing the Python, the decision algorithm and all 13 dataset rows were ported to TypeScript and executed: all 11 gate-counted rows produced their expected decisions with the expected reason codes and scope flags, and the metamorphic score-perturbation battery (uniform-low, reversed-with-high, absurd-magnitude, removed scores) produced zero decision changes. The Python implementation mirrors that verified logic line-for-line. **CI is the binding verification; if CI disagrees, CI wins and this document must be corrected.**

## 3. What is NOT claimed

- **Gate A independent adjudication is OPEN.** The dataset was authored by Vibe under Vinh's build authorization; the author is not an independent adjudicator (contract section 6). Ka/Xu (or a designated reviewer) must adjudicate before any release use. CI green on this dataset is build evidence, NOT a release claim.
- **Gate C (corpus-aligned five-state evaluation over the V3 query set) is NOT BUILT**, deliberately: building it against an unadjudicated dataset would be circular.
- **Gate D and E2E MCP :8020 → Core :8000 remain CLOSED.** No Core/MCP changes were made.
- The corpus-aligned strict no-answer retrieval gate is still expected to FAIL (Q008/Q035/Q010 lexical leaks persist). The evidence-support stage is the separately scoped remediation path; it does not change the retrieval floors or claim lexical retrieval PASS.
- Immutables preserved: labels V3, fixture freezes V1/V2, baseline thresholds, Qw V5, `rag_retrieval.py`, `rag_eval.py`, existing eval sets.

## 4. Required next actions

1. CI run on this commit: verify py_compile, the three unit suites, and the Gate B decision-set step; record the run ID here.
2. Independent architecture review of Contract V3 (Xu or a reviewer who did not author V2/V3), with accepted/rejected findings recorded.
3. Independent adjudication of the Gate A dataset rows (including pending Q008/Q037); freeze with hashes per the adjudication protocol.
4. Only then: Gate C corpus-aligned five-state evaluation design, and the separately recorded integration decision for MCP :8020 → Core :8000.

— Vibe (GLM 5.3 via Vibe Work agent)
