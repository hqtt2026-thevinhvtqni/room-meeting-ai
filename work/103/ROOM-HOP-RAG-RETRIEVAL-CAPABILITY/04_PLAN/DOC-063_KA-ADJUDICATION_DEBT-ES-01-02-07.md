# KA INDEPENDENT ADJUDICATION — DEBT-ES-01 / 02 / 07

- **Document ID:** DOC-063
- **Priority:** P0 — critical path
- **Date:** 2026-11-27 (UTC+07)
- **Reviewer:** Ka — independent adjudicator
- **Authority:** Vinh
- **Branch:** `work/103-rag-retrieval-capability`
- **Baseline handover:** DOC-062 / EVD-013 at `ba82151ef6ac563224f4371334029b81461e213a`
- **Review mode:** read-only source, contract, fixture, and test review. No source/test/label/fixture/threshold/CI/gate changes were made.
- **Disposition:** DEBT-ES-01 FAIL (contract corrections required); DEBT-ES-02 PARTIAL (semantic review recorded; freeze and dataset adjudication record remain open); DEBT-ES-07 FAIL (row corrections/source alignment required).
- **Gate boundary:** Gate A remains OPEN / BLOCKED; Gate C BLOCKED; independent retrieval gate remains FAIL 0.300 vs 0.800; Release NOT PASS.

## 1. Integrity anchors

All four files were fetched from the Work 103 GitHub branch. Git blob SHA values match DOC-062. SHA-256 below is computed over the exact UTF-8 text returned by GitHub's content API; it is not represented as raw on-disk byte hashing.

| Artifact | Git blob SHA | SHA-256 (UTF-8 content) |
|---|---|---|
| Interface Contract V3 | `4c19b678e9ff37062081c0420c9de96f2852adfd` | `d0397e435bd166fc64a400eb838ad12b30f6694f468faff66d8b8bcaae14f826` |
| Decision Set V1 | `4f782f2d37620937f054de4a9c3a1a476b4ad7d9` | `7865cf38f99b9de3fde487ed01a0c8ecfa8628482c86d167339c20122ad813d1` |
| Fact Specs V1 (historical) | `ed26f8f8ced43a4fcd631510f9882d2bd2d93301` | `9c2c86a24d26d0832318b7f6fde5c37f983fabce26df9bf12ad92fcaf21ab6c0` |
| Fact Specs V2 | `00bb8f89e7fe380ee5c8695a4d81002a62a688cb` | `e704b18adcd232fec0aef25cbc508a203cb08ee87e6b6830749bda3ee4804850` |

## 2. DEBT-ES-01 — Interface Contract V3

**Disposition: FAIL — P1 contract defects / corrections required.**

### F01 — Absence evidence is not bound to the candidate's actual source

Contract §3 defines absence by the source scope, but `assess_support()` checks the pattern's `source_scope` against `fact.query_scope` without checking that the candidate's `source_id` is that source (or that the pattern explicitly allows any source with `*`). A span from an unrelated document that happens to match the absence regex could therefore be cited as proof that another document does not specify a fact.

The schema/validator also does not require a non-empty `source_scope` on absence patterns. If it is missing, current code treats the absence as covered and can return `EXPLICITLY_UNSPECIFIED` with `scope_limited=false`.

**Required correction:** require `source_scope`; bind candidate provenance to it (exact source identity, or explicit wildcard); reject ambiguous/mismatched absence evidence; add negative tests for missing and mismatched source scopes.

### F02 — Scope-limited output flag disables even source-local absence

When `scope_limited_answers_enabled=false`, current code returns `INSUFFICIENT_EVIDENCE` for every matched absence pattern. That also suppresses a fully source-local absence where `source_scope == query_scope`, although Contract §3 permits `EXPLICITLY_UNSPECIFIED` with `scope_limited=false` for that case.

**Required correction:** apply the flag only when the query scope exceeds the source scope and a scope-limited answer would be required. Add a test proving a covered/source-local absence remains admissible when limited output is disabled, while T4b still fails closed.

### F03 — Support-source scope semantics need an explicit rule

Support patterns have no declared source scope and the implementation does not constrain a support candidate by `query_scope`. This is observable in V2/Q037: the expected source is `00_CORPUS/architecture.md`, while the phrase “grounded answer with citations / abstention” is in `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`, not in the named corpus fixture. This is a scope/citation ambiguity and overlaps DEBT-ES-08.

**Required correction:** explicitly define whether `query_scope` constrains support candidates. If yes, enforce it and add a test; if no, rename/document the field semantics and require an explicit expected-source/citation alignment policy in Gate C.

The existing score-independence design is sound by inspection: `score` is not read by the decision logic and B4 tests perturb/reorder/remove scores. T1–T7 and C1–C3 cover the stated contract families. However, current tests do not cover F01/F02, so the test suite does not close these defects.

## 3. DEBT-ES-02 — Decision Set V1

**Disposition: PARTIAL — row semantics reviewed; Gate A freeze/record remains OPEN.**

The actual Decision Set V1 contains **13 rows: 11 gate-counted rows and 2 pending rows**, not 15 as stated in DOC-062 §1. The 11 gate-counted cases T1, T2, T3, T4a, T4b, T5, T6, T7, C1, C2, C3 are consistent with the declared expected behavior on the supplied candidate spans by independent source/contract inspection:

- T1: source-local explicit RX-threshold absence — EXPLICITLY_UNSPECIFIED.
- T2/T3: no retrieved absence or direct support — INSUFFICIENT_EVIDENCE.
- T4a: sales.md absence with broader corpus query; scoped answer allowed — EXPLICITLY_UNSPECIFIED with scope_limited=true.
- T4b: same evidence, scope-limited output disabled — INSUFFICIENT_EVIDENCE.
- T5: empty chunk_id invalidates provenance — INSUFFICIENT_EVIDENCE.
- T6: two different values in the same `current` value scope — CONFLICTING_EVIDENCE.
- T7: security.md directly negates execution authority — CONTRADICTED.
- C1: exact top_k=5 support span — SUPPORTED.
- C2: no candidates — INSUFFICIENT_EVIDENCE.
- C3: current=8000 and legacy=9000 are scoped separately; current span supports — SUPPORTED, not a conflict.

Pending-row adjudication:

- **DecisionSet/Q008-PENDING:** accept EXPLICITLY_UNSPECIFIED only when the retrieved sales.md chunk contains the explicit statement that the change process is not specified. This does not contradict Qw's binary NO_ANSWER label: the process itself cannot be answered, while the five-state stage may report a cited, source-scoped explicit absence. Do not infer absence if that chunk is not retrieved (T2 discipline).
- **DecisionSet/Q037-PENDING:** accept SUPPORTED for the question asking which fields `rag_get_context` returns. The architecture fixture lists context, citations[], sufficient_evidence and optional abstention_reason. Preserve the optional nature of abstention_reason.

**Identifier collision warning:** DecisionSet/Q037-PENDING is the `rag_get_context` field-list case. It is NOT the same question as FactSpecsV2/Q037 (AI caller output / duplicate architecture content). Records must qualify Q037 with the dataset name.

Although the row meanings above are independently dispositioned, the JSON still records all 11 gate-counted rows as `AUTHORED_PENDING_INDEPENDENT_ADJUDICATION` and both pending rows as `PENDING_INDEPENDENT_ADJUDICATION`. This report does not mutate that dataset. Gate A cannot be declared closed until the independent reviewer/resolution fields and a valid frozen dataset snapshot are recorded under B5.

## 4. DEBT-ES-07 — Fact Specs V2 (50 rows)

**Disposition: FAIL — four semantic corrections and one source-alignment resolution required.**

### Confirmed row findings

| Dataset row | Current spec | Independent disposition | Reason |
|---|---|---|---|
| Q009 | SUPPORTED; Qw V5 says NO_ANSWER | **SUPPORTED** | sales.md explicitly says sales staff (`nhân viên kinh doanh`) perform both confirmation steps, including cement quantity. The Qw rationale that no role is named overlooks this role. |
| Q015 | SUPPORTED | **CONTRADICTED** | Query asks whether MCP may access storage directly; architecture.md explicitly says it does not. Move the matching negative proposition to `negation_patterns`. |
| Q020 | SUPPORTED | **CONTRADICTED** | Query asks whether lexical score is a calibrated probability; architecture.md says it is not. This is direct negation, not support. |
| Q023 | SUPPORTED | **CONTRADICTED** | Query asks whether MCP errors may expose stack traces; security.md says they must not. Use an explicit negation pattern, not the broad `stack trace` support regex. |
| Q037 | SUPPORTED, query_scope=00_CORPUS/architecture.md | **CONDITIONAL / SOURCE ALIGNMENT REQUIRED** | The “grounded answer with citations / abstention” statement is in RAG_RETRIEVAL_ARCHITECTURE.md, not the named architecture fixture. If scope is strictly architecture.md, the row lacks direct support; if the intended scope is the whole benchmark corpus, record the actual source and treat citation alignment under DEBT-ES-08. |

### Rows whose current interpretation is retained with explicit limits

- Q004 and Q008: EXPLICITLY_UNSPECIFIED only on retrieval of their exact, source-local absence statements.
- Q044: INSUFFICIENT_EVIDENCE; the corpus says to calibrate thresholds but does not explicitly state a default minimum score is unspecified.
- Q040: ideal ground-truth CONTRADICTED is correct from security.md, but the operating-point retrieval miss means the stage sees no candidate and returns INSUFFICIENT_EVIDENCE. Record as CONTRADICTION_MISSED / retrieval-side finding (DEBT-ES-06), not as a support-stage label defect.
- Q050: SUPPORTED is correct after Qw's V5 wording change to ask whether the security policy prohibits storing/returning administrator passwords.
- Q047–Q049 and Q011–Q014: support is limited to statements in the benchmark fixture. It does not establish external organizational authority or production runtime facts.

The remaining rows were checked against the V5 query table and the six fixture/architecture sources in this review pass; no additional semantic mismatch was identified. Fact Specs V1 remains historical and is superseded by V2.

## 5. Blind-label, corpus freeze, and authority constraints

- Qw V5 still declares “Per Manifest v3.0”; the branch contains Manifest v4.0. V5 therefore has a stale corpus-version reference.
- Manifest v4.0 states benchmark-fixture approval is PENDING and freeze is PENDING_XU_VERIFICATION. Its logical UTF-8/LF hashes are not raw stored-byte hashes.
- Ka's V5 sync review records that no Xu blind-process attestation, exact freeze attestation, or raw-byte SHA-256 verification was established. Absence of score columns is not proof of blinding.
- The four main-only historical blind-labeling files remain read-only context. Per Xu's recorded decision, keep them on main; do not copy them to this branch, delete them, or rewrite history without a separate authorized mapping.

Xu's five decisions are now recorded in DOC-035: Batch 1 closure approved (DEBT-ES-10 CLOSED); keep main evidence drift in place; DEBT-ES-05 CLOSED and DEBT-ES-09 OPEN / DOC-058 NOT VERIFIED; Gate C remains BLOCKED pending adjudication and citation alignment; Batch 3 register/mapping closure approved only.

## 6. Required next actions

1. Correct Contract V3 and implementation/tests for F01/F02; resolve support-source scope semantics with a versioned contract decision.
2. Prepare a versioned corrected Fact Specs V2 (or V3) and reconcile Q009/Q015/Q020/Q023/Q037 without rewriting the original V2 artifact.
3. Record Ka's row-level adjudication in the dataset's B5 fields and obtain Xu's corpus/blind-process/freeze attestation; verify raw-byte integrity through an approved byte-preserving path.
4. Keep Gate C blocked until DEBT-ES-08 citation-source alignment is resolved.
5. Do not change retrieval code, strict thresholds, fixtures, Qw V5 labels, CI workflows, or the independent retrieval gate as part of this report.

**Final status:** DEBT-ES-01 FAIL; DEBT-ES-02 PARTIAL / FREEZE BLOCKED; DEBT-ES-07 FAIL. Work 103 remains ACTIVE / BLOCKED. No Gate A/B/C/D PASS, no E2E PASS, no release claim.

— Ka | Independent adjudicator
