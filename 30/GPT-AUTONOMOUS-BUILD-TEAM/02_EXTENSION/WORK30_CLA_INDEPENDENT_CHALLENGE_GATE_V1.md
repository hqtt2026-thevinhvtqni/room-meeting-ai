# WORK 30 — CLA INDEPENDENT CHALLENGE GATE V1

Status: DECISION RECORDED / IMPLEMENTATION AND RECEIPT NOT VERIFIED
Work: 30 — GPT-AUTONOMOUS-BUILD-TEAM

## 1. Purpose
Add an independent adversarial review gate when the product is near completion, after Nu/Vi defect handling and An's independent testing, but before Ka's final review.

## 2. Agreed workflow
1. Xu consolidates independent planning proposals from Claude (Cla), Grok (Go), Qwen (Qe), and Vibe into one Plan. Vinh must approve the Plan before implementation.
2. Nu performs end-to-end implementation and records reproducible evidence.
3. Vi repairs scoped defects assigned with defect IDs and evidence.
4. Nu reruns end-to-end checks after repairs.
5. An performs independent testing against acceptance criteria and records results.
6. Cla performs an independent adversarial challenge on the near-complete product, test results, code/configuration changes, security boundaries, and evidence.
7. Nu/Vi address confirmed findings; Nu reruns affected regression and end-to-end tests. An retests relevant acceptance criteria. Cla verifies closure of its findings or explicitly records unresolved risk.
8. Ka performs independent final review using the approved Plan, acceptance criteria, An's evidence, Cla's findings/closure matrix, and Nu's final E2E evidence.
9. Xu produces the evidence-based handoff for Vinh's decision.

## 3. Cla's mandate
Cla must challenge, not rubber-stamp:
- requirements coverage and mismatches against the approved Plan;
- untested paths, edge cases, failure/recovery paths, and misleading success states;
- security boundaries, permissions, input validation, secrets exposure, and unsafe defaults;
- architectural assumptions, hidden coupling, maintainability, and regression risk;
- test quality, reproducibility, evidence freshness, and claims unsupported by artifacts.

Cla must prioritize findings by severity (Critical/High/Medium/Low), include finding ID, evidence/location, reproduction steps where possible, impact, expected versus actual behavior, and a concrete verification condition. Separate confirmed defects from hypotheses and unknowns. Do not make changes to code or approve own findings as fixed.

## 4. Exit criteria for the Cla gate
- A written challenge report exists and is linked to the exact product revision/build under review.
- Every finding has an owner and status: OPEN, FIXED_PENDING_RETEST, VERIFIED_CLOSED, ACCEPTED_RISK_BY_VINH, or NOT_REPRODUCED_WITH_EVIDENCE.
- Critical/High findings must not be silently waived. Any unresolved Critical/High issue blocks routine handoff and must be escalated to Vinh with evidence.
- Fixes are verified by tests independent of the edit itself; Nu reruns E2E and An retests affected acceptance criteria.
- Ka receives the report and evidence package before review.
- Missing evidence is BLOCKED/NOT VERIFIED, never PASS.

## 5. Independence and loop control
- Cla challenges the artifact and evidence; Cla is not the implementation coder, An tester, or Ka reviewer.
- Ka makes its own review decision and must not treat Cla's opinion as a substitute for review.
- After two unsuccessful repair attempts on the same finding, stop patch repetition and return to root-cause/Plan decision.
- Scope or architecture changes require Vinh's approval through the Plan decision path.
- Every dispatch requires a real task ID, recipient identity, timestamp, and explicit ACK. A file write or message append is not proof that Cla received/read the task.

## 6. Required handoff package
Approved Plan and revision; build/commit identifier; E2E commands and outputs; An test report; Cla challenge report and finding-closure matrix; Vi repair evidence; Nu retest evidence; Ka review decision; remaining risks; named actors and timestamps.

## 7. Current evidence status
This protocol is documented here. Actual dispatch to Cla, identity-bound ACK, completed challenge report, finding closure, and successful end-to-end gate execution are PENDING / NOT VERIFIED until supported by runtime evidence.
