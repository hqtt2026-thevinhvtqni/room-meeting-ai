# WORK 103 — Evidence-Support Stage Proposal V2 Technical Review

- Reviewer: Ka | CSA — technical pre-review
- Date: 2026-10-29 (UTC+07:00)
- Target branch: `work/103-rag-retrieval-capability`
- Reviewed artifact: `06_EVIDENCE/KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V2_20261029.md`
- Review type: **TECHNICAL PRE-REVIEW — NOT INDEPENDENT SIGN-OFF**
- Decision: **BLOCKED FOR GATE A / IMPLEMENTATION**
- Scope: Contract only. No code, fixture, threshold, V3 label, Core, or MCP changes.

## 1. Evidence inspected

The V2 proposal was fetched from the Work 103 GitHub branch. Its blob SHA is `88496ca8fccd80dac7ba2a440896b502e5b1c7f4`.

The proposal preserves the declared immutables and states that the Evidence-Support Stage is not implemented or tested. This review does not rerun tests or independently reproduce the corpus baseline.

## 2. Findings that pass this technical review

1. The distinction between `EXPLICITLY_UNSPECIFIED` and `INSUFFICIENT_EVIDENCE` is materially clearer and correctly rejects absence-of-retrieval as proof of unspecified information.
2. Lexical retrieval score is limited to candidate ordering and is forbidden as a support signal.
3. T1–T7 are individually gated; aggregate metrics cannot hide a failing case.
4. `CONTRADICTED` and `CONFLICTING_EVIDENCE` have distinct expected behavior.
5. The proposal correctly requires a new expected-support-decision dataset and explicitly prohibits reusing or modifying V3's `ANSWERABLE`/`NO_ANSWER` labels.
6. The offline-only scope and CLOSED state of MCP :8020 → Core :8000 E2E are preserved.

## 3. Blocking contract gaps

### B1 — T4 is not a single deterministic test oracle

T4 currently permits `EXPLICITLY_UNSPECIFIED` when the implementation can produce a scope-limited answer, but requires `INSUFFICIENT_EVIDENCE` otherwise. This is a valid policy boundary but not a single expected decision unless the capability/input condition is pinned in the test fixture.

**Required closure:** split T4 into two explicit test rows (for example, T4a: scope-limited output supported; T4b: scope-limited output unavailable), each with fixed inputs, one expected decision, and per-case assertions. Do not let the implementation choose its own oracle at runtime.

### B2 — The output/interface contract remains underspecified

V2 locks decision behavior but does not freeze a normative schema for the support-stage request/response, allowed reason codes, evidence cardinality, claim-level results, or aggregation when a query has multiple material subquestions. V1 explicitly left evidence-unit and component-boundary questions for review.

**Required closure:** before Gate A is approved, publish a versioned interface contract that defines the minimum evidence unit (claim/span pair with exact provenance is the safer default), required fields, enum values, and deterministic query-level aggregation rules. Keep this as design work; do not modify implementation code yet.

### B3 — Conflict handling needs scope and authority rules

T6 says different values for the same fact produce `CONFLICTING_EVIDENCE`, but does not define when two spans concern the same fact and compatible scope, or how different time periods, entities, versions, and source authority are treated. Without these rules, valid scoped differences can be mislabeled as conflicts.

**Required closure:** define fact identity and scope matching, and specify that source authority/recency may resolve a conflict only when an approved deterministic policy explicitly permits it. Otherwise fail closed as `CONFLICTING_EVIDENCE`.

### B4 — Independence is stated but its verification protocol is not testable yet

T3 forbids reuse of the lexical score, but the document does not prescribe an observable test that proves the decision is invariant to score changes when candidate content/provenance is held constant.

**Required closure:** add a metamorphic test: hold candidate spans and provenance fixed while changing/reordering scores; the support decision must remain identical. Separately test that changing the span text can change the decision. Per-case reporting must show both assertions.

### B5 — “Independent reviewer” is required but the adjudication protocol is incomplete

Gate A requires a reviewer per row and independent adjudication for Q008/Q037, but does not define separation from the dataset author, disagreement handling, or the immutable record of adjudication.

**Required closure:** specify that the adjudicator cannot be the sole author of the expected label being adjudicated; preserve initial label, independent decision, rationale, resolution, reviewer identity/role, and dataset hash. If reviewers disagree, the row remains unresolved and Gate A is blocked.

### B6 — Per-case minimum coverage can be too weak for approval

One example for each decision and T1–T7 satisfies the stated minimum but does not establish robustness across negation, scope, multi-subquestion aggregation, malformed provenance, and score perturbations.

**Required closure:** retain T1–T7 as mandatory named cases, add a minimum coverage matrix across decision × failure mode, and keep each case family individually gated. Do not weaken existing retrieval or no-answer floors.

## 4. Independence and approval boundary

This is a technical pre-review in a separate review pass, but the V2 artifact is also authored by Ka. Therefore this review **cannot satisfy the proposal's required independent architecture review** and must not be represented as independent sign-off. Xu or another designated reviewer who did not author V2 must decide whether the blocking findings are accepted and close the architecture review.

## 5. Gate decision

- Contract clarity: **PARTIAL PASS**
- T1–T7 coverage as written: **PARTIAL PASS; T4 oracle and score-independence test need closure**
- Dataset V3 separation: **PASS as a design constraint**
- Gate A authorization: **BLOCKED**
- Implementation authorization: **BLOCKED**
- Core/MCP integration and E2E: **CLOSED**
- Work 103: **ACTIVE / BLOCKED**

## 6. Required next actions

1. Xu/designated independent reviewer reviews V2 and this pre-review; record accepted/rejected findings with rationale.
2. Revise the contract only after that review decision; split T4 into deterministic cases and close B2–B6.
3. Freeze the new expected-support-decision dataset separately from V3, with immutable hashes and independent adjudication evidence.
4. Run Gate A review before any implementation. Keep all current code, fixture, V3 labels, thresholds, and E2E state unchanged until authorization.

— Ka | CSA — technical pre-review, not independent sign-off
