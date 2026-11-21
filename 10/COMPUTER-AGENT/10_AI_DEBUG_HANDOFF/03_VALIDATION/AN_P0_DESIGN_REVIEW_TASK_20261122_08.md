# WORK 10 — AN INDEPENDENT DESIGN REVIEW TASK — V8

- Document ID: W10-AN-P0-DESIGN-REVIEW-TASK-20261122-08
- Work: 10 — COMPUTER-AGENT | Priority: P0
- Reviewer: An — TESTER / Independent Reviewer
- Requested by: Co — AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 04:49 (UTC+07:00)
- Mode: STATIC / ADVERSARIAL ONLY
- Status: REVIEW REQUEST PREPARED — NOT YET ACKNOWLEDGED

## Inputs
1. 06_EVIDENCE/W10_P0_ACCEPTANCE_INTEGRITY_AMENDMENT_20261122_08.md
2. 06_EVIDENCE/W10_P0_ACCEPTANCE_MANIFEST_V7.schema.json
3. 10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261119_07.md
4. 06_EVIDENCE/W10_P0_IMPLEMENTATION_READINESS_GATE_20261118_01.md
5. 06_EVIDENCE/W10_P0_PROCESS_ISOLATION_REVIEW_20261117_01.md
6. Work Manifest, Sync Policy v1.2 and three LOCKED contracts.

## Review requirements
1. AN-V7-F01: determine whether the proposed validator attestation and trusted-runner provenance prevent caller-authored consistency flags from being treated as proof. Identify replay, stale-build, hash-substitution and provenance-forgery paths.
2. AN-V7-F02: verify that PASS excludes UNKNOWN lease/owner states while allowing only explicitly defined NOT_APPLICABLE semantics where justified by category.
3. AN-V7-F03: review the category/outcome policy model. Ensure negative tests can legitimately PASS when the observed outcome is REJECTED or TERMINATED, but only when the category's pinned acceptance policy allows it.
4. AN-V7-F04: assess whether the expanded negative catalogue is deterministic and complete; identify missing forged flags, outcome contradictions, artifact/fixture hash mismatches, and validator failure cases.
5. Verify the separation between JSON Schema validation, semantic validation, trusted-runner provenance and real host/process evidence.
6. Confirm that no V8 proposal silently changes F-15 timeout semantics or any of the three LOCKED contracts.
7. State explicitly that schema validation, semantic validator execution, host/runtime tests and process-tree tests are NOT RUN unless independently evidenced.

## Boundary
- Static adversarial review only.
- Do not edit runtime source, tests, configuration or the three LOCKED contracts.
- Do not implement the semantic validator.
- Do not run host/runtime/process tests.
- Do not authorize P0 implementation or release.
- Preserve V7 amendment, V7 schema and An's V7 report unchanged.

## Required report
Create a new result file:
10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261122_08.md

For each finding, use PASS (design only), FINDING, PARTIAL or BLOCKED with exact references. Explicitly state whether AN-V7-F01..F04 are ready to close, remain open, or need another revision. Record any additional AN-V8 findings with severity, evidence and required disposition.

KÝ: Co | AI-07
