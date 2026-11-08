# Work 103 — Evidence-Support Stage Interface Contract V3

- Author: Vibe (GLM 5.3 via Vibe Work agent)
- Date: 2026-11-08 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Supersedes: `06_EVIDENCE/KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V2_20261029.md` (V2 preserved; nothing deleted)
- Decision type: **INTERFACE CONTRACT V3 — closes the B1–B6 blocking gaps from `KA_EVIDENCE_SUPPORT_STAGE_V2_REVIEW_20261029.md`**
- Build authorization: Vinh, 2026-11-08, in the Work 103 coordination conversation ("xây tiếp" after review of the branch state).
- Status: **CONTRACT FROZEN FOR INDEPENDENT REVIEW; Gate B prototype implemented under build authorization; Gate A independent adjudication and Gate C/D remain OPEN.**
- Scope: Work 103 Sandbox prototype only. No Core :8000, MCP :8020, production corpus, or Dashboard changes. No changes to `rag_retrieval.py`, `rag_eval.py`, thresholds, fixtures, labels V3, or Qw V5.

## 1. Closures of the V2-review blocking findings

- **B1 (T4 oracle):** T4 is split into two deterministic rows. **T4a**: scope-limited output available — expected `EXPLICITLY_UNSPECIFIED` with `scope_limited=true` and exact citation. **T4b**: scope-limited output unavailable — expected `INSUFFICIENT_EVIDENCE`, reason `SCOPE_LIMITED_OUTPUT_UNAVAILABLE`. Each row has fixed inputs and one expected decision; the implementation never chooses its own oracle at runtime.
- **B2 (interface contract):** section 2 of this document freezes the normative request/response schema, reason codes, evidence cardinality, and aggregation rules.
- **B3 (conflict scope/authority):** sections 3–4 lock fact identity, scope matching, and value-conflict rules. No authority/recency resolution policy is approved; same-scope value differences fail closed as `CONFLICTING_EVIDENCE`, scoped differences are not conflicts.
- **B4 (independence verification):** section 5 locks the metamorphic test protocol; it is implemented in `05_TEST/test_rag_evidence_support.py`.
- **B5 (adjudication protocol):** section 6 locks the protocol; it is recorded in the dataset's `adjudication_record` and per-row `adjudication` objects.
- **B6 (coverage matrix):** section 7 locks the minimum coverage matrix; the runner enforces it structurally (`required_case_families` × `required_decisions`).

## 2. Normative interface (v1, frozen)

### Request (one fact per request)

```json
{
  "query": "string, non-empty",
  "candidates": [EvidenceCandidate],
  "fact": FactSpec,
  "scope_limited_answers_enabled": true
}
```

`EvidenceCandidate` (minimum evidence unit is the claim/span pair with exact provenance):

```json
{
  "source_id": "string, non-empty",
  "chunk_id": "string, non-empty",
  "start_line": "int >= 1",
  "end_line": "int >= start_line",
  "text": "string, non-empty",
  "scope": "declared value scope, default 'default'",
  "score": "optional; ORDERING ONLY — must never influence the decision"
}
```

`FactSpec` (declared, reviewed data — patterns are configuration, not hidden code):

```json
{
  "fact_id": "string",
  "query_scope": "string",
  "support_patterns":  [{"regex": "..."}],
  "absence_patterns":  [{"regex": "...", "source_scope": "..."}],
  "negation_patterns": [{"regex": "..."}],
  "value_patterns":    [{"regex": "... (with capture group 1)", "value_scope": "..."}]
}
```

### Response

```json
{
  "decision": "SUPPORTED | EXPLICITLY_UNSPECIFIED | CONTRADICTED | CONFLICTING_EVIDENCE | INSUFFICIENT_EVIDENCE",
  "reason_code": "NO_CANDIDATES | PROVENANCE_INVALID | ABSENCE_SCOPE_COVERED | ABSENCE_SCOPE_EXCEEDS_QUERY | SCOPE_LIMITED_OUTPUT_UNAVAILABLE | NEGATED_BY_SOURCE | CONFLICTING_VALUES | SUPPORTED_BY_SOURCE | NO_ADEQUATE_SUPPORT",
  "citations": [{"source_id", "chunk_id", "start_line", "end_line"}],
  "scope_limited": "bool",
  "dropped_candidates": ["source_id of every candidate rejected by the provenance gate"]
}
```

Evidence cardinality: `citations` is non-empty only for `EXPLICITLY_UNSPECIFIED`, `CONTRADICTED`, and `SUPPORTED`. `CONFLICTING_EVIDENCE` and all `INSUFFICIENT_EVIDENCE` variants return no answer citations (fail closed, nothing fabricated).

### Locked decision precedence

1. Provenance validation (drop invalid candidates; all-invalid or empty → fail closed).
2. Explicit absence statement (`EXPLICITLY_UNSPECIFIED` or `SCOPE_LIMITED_OUTPUT_UNAVAILABLE`).
3. Direct negation (`CONTRADICTED`).
4. Conflicting values (`CONFLICTING_EVIDENCE`).
5. Direct support (`SUPPORTED`).
6. Otherwise `INSUFFICIENT_EVIDENCE` / `NO_ADEQUATE_SUPPORT`.

Earlier stages short-circuit later ones. Negation beats support (fail closed). Multi-subquestion aggregation is out of scope for v1: one request carries one fact; callers issue separate requests and aggregate with the same precedence order (worst-case-first: any non-SUPPORTED member downgrades the aggregate).

## 3. Scope matching (locked)

A `source_scope` covers a `query_scope` iff the strings are equal or `source_scope == "*"`. There are no implicit scope hierarchies; any wider interpretation must be declared explicitly in a reviewed pattern row.

- `EXPLICITLY_UNSPECIFIED` with `scope_limited=false`: query scope is covered by the absence statement's source scope.
- `EXPLICITLY_UNSPECIFIED` with `scope_limited=true`: query scope exceeds the source scope, scope-limited output is available, and the answer may ONLY assert absence within the cited source, never the corpus.
- A statement "document A does not specify X" is never generalized beyond document A.

## 4. Fact identity and value conflict (locked)

Two usable spans conflict iff they extract **different casefolded values** with the **same `fact_id`** and the **same `value_scope`**. A candidate contributes a value only when its declared `scope` equals the pattern's `value_scope` (or the `value_scope` is `default`). Scoped differences (e.g. `legacy` vs `current` documents) are NOT conflicts. No authority/recency policy may silently resolve a same-scope conflict; adding one requires a new contract version and independent review.

## 5. Independence verification (locked, B4)

The support assessment consumes candidates as (source_id, chunk_id, line range, text, scope) only. The score may order candidates; it must never appear in, weight, or short-circuit the decision. Verification protocol, implemented as metamorphic tests:

1. Hold spans/provenance fixed; perturb scores (low, high, reversed order, absent) — the decision must be identical for every dataset row.
2. Changing the span text (e.g. adding the explicit absence statement) must be able to change the decision.
3. Per-case reporting shows both assertions.

## 6. Adjudication protocol (locked, B5)

- The dataset author may not be the sole adjudicator of any expected label.
- Per row, the record preserves: `author`, `independent_reviewer`, `status`, `initial_label`, `resolution`.
- Rows without independent adjudication are either `gate_counted: false` + `status: PENDING_INDEPENDENT_ADJUDICATION` (excluded from the gate), or `gate_counted: true` + `status: AUTHORED_PENDING_INDEPENDENT_ADJUDICATION` (CI build evidence only, explicitly NOT a release claim).
- If reviewers disagree, the row stays unresolved and Gate A stays BLOCKED for release use.

## 7. Coverage matrix (locked, B6)

Mandatory gate-counted case families: `T1, T2, T3, T4a, T4b, T5, T6, T7, C_SUPPORTED, C_NO_CANDIDATES, C_SCOPED_DIFFERENCE`. Every one of the five decisions must be produced by at least one gate-counted row. The runner (`rag_evidence_support.py --decision-set ...`) fails if any required family or decision lacks a gate-counted row; each case is reported pass/fail individually and a single failing case fails the gate. No aggregate score exists.

## 8. Gates

- **Gate A (dataset):** `05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json` authored 2026-11-08. Independent adjudication OPEN (see dataset `adjudication_record`); Q008/Q037 carried as pending, non-gate-counted rows per V2 section 6.
- **Gate B (component tests + runner):** `05_TEST/test_rag_evidence_support.py` + `04_CODE/rag_evidence_support.py`. CI executes them on every push.
- **Gate C (corpus-aligned five-state evaluation over the V3 query set): NOT BUILT.** Requires Gate A adjudication first; building it against an unadjudicated dataset would be circular.
- **Gate D (architecture integration review): OPEN. E2E MCP :8020 → Core :8000 remains CLOSED.**
- The existing strict retrieval gates, floors, and the failing corpus-aligned no-answer gate are unchanged. Work 103 remains ACTIVE with the corpus-aligned retrieval limitation recorded separately.

## 9. Non-goals

No vector DB, embeddings, external model APIs, or paid dependencies. No changes to retrieval code, thresholds, fixture freezes, labels V3, Qw V5. No merge, no release certification, no claim that lexical retrieval passes the corpus-aligned gate.

— Vibe (GLM 5.3 via Vibe Work agent), under Vinh's build authorization; independent review by Xu/Ka remains required and OPEN.
