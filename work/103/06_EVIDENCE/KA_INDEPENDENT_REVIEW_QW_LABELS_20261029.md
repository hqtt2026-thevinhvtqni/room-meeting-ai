# WORK 103 — KA INDEPENDENT REVIEW OF QW BLIND LABELS
**Date-time:** 2026-10-29 (UTC+07:00)
**Reviewer:** Ka — CSA / Independent Reviewer
**Artifact reviewed:** `06_EVIDENCE/QW_BLIND_LABELS_50_QUERIES_20261029.md`
**Decision:** BLOCKED — artifact structurally valid as a first-pass table, but not eligible for corpus-grounded adjudication/freeze.

## 1. Structural checks
- Read directly from Work 103 Sandbox using ROOM-HOP read-probe.
- File size reported by Sandbox: 11,056 bytes.
- Exactly 50 query rows; IDs Q001–Q050; 50 unique IDs.
- Required six columns are present: query_id, query_text, label, expected_source_id, evidence_span_rationale, ambiguity_flag.
- Label values are valid: 39 ANSWERABLE, 11 NO_ANSWER.
- No score/rank/retrieval-output fields are present in the dataset table. Mentions of scores/ranks occur only in annotation rules/handoff text, not as per-query results.
- These checks confirm table structure only; they do not validate the labels or prove blind production.

## 2. Critical evidence gap: source corpus is not identifiable
The Work 103 Sandbox inventory contains architecture, prototype code, unit tests, acceptance plan, manifest, and evidence files. It does NOT contain the referenced source documents:
- docs/network.md
- docs/sales.md
- docs/architecture.md
- docs/security.md
- docs/evidence.md

The unit test contains synthetic fixtures named docs/network.md and docs/sales.md, but those fixtures are not an approved/versioned evaluation corpus. Work 103's manifest and architecture explicitly state that the implementation remains an isolated Sandbox prototype and is not integrated with Core/MCP. No corpus snapshot, query-pool version, manifest of source hashes, or approved source registry was available to bind the labels to a reproducible source state.

Therefore, expected_source_id and evidence_span_rationale cannot currently be independently verified against canonical source spans. The label file itself is not proof that Qw did not see retrieval outputs; that procedural assertion requires traceable attestation/evidence from the annotation process.

## 3. Row-level findings requiring correction or adjudication
1. **Q030 — definite label/rationale contradiction.** Query asks about an unrelated phrase (“lượng tử tàu ngầm thiên thạch”). Label is ANSWERABLE, while rationale says retrieval should return empty/no evidence. Under the stated ANSWERABLE / NO_ANSWER meaning, review this as NO_ANSWER unless an explicit source actually answers the query.
2. **Q040 — unsupported safety/authority claim.** Query asks whether RAG can automatically delete files. It is labeled ANSWERABLE against docs/security.md, which is absent from the approved corpus inventory. Work 103's architecture boundary says RAG is evidence retrieval, not execution authority, but that does not establish the requested behavior as a corpus-grounded answer unless the authoritative source is explicitly included and cited.
3. **Q041 — unsupported test-coverage claim.** Rationale claims Unicode/Vietnamese is covered by tests, but the inspected test file does not contain a Unicode/Vietnamese test case. Mark ambiguous or provide a real source/test artifact.
4. **Q050 — scope ambiguity.** “Tài liệu này” has no defined referent in the query pool, and absence of a password cannot be inferred from the current artifact inventory. Needs a fixed target document/source and evidence.
5. **Q001–Q005, Q031–Q033:** network claims point to docs/network.md, which is not present as an approved source. Similar source-identity issue applies to sales, security, architecture and evidence references.
6. **Q014:** Sandbox/workspace port claim requires an authoritative source span. Do not infer it solely from environment assumptions.
7. **Q047–Q049:** role/procedure questions cite docs/evidence.md, which is absent. The gate status document describes roles, but expected_source_id must identify the actual versioned source used.

These are actionable findings, not a final relabeling pass. Ka must not silently rewrite Qw's first-pass labels or fabricate missing source spans.

## 4. Gate decision
- Structural validation: PASS.
- Corpus identity and source-span verification: BLOCKED.
- Blind-process attestation and freeze/hash confirmation by Xu: BLOCKED / not evidenced.
- Independent adjudication of disagreements: NOT STARTED as a valid corpus-grounded adjudication; row-level contradictions are flagged above.
- Work 103 overall: remains ACTIVE / BLOCKED for blind-label gate and E2E acceptance.

## 5. Required next actions
1. Provide the exact approved corpus snapshot/path and query-pool version, with source inventory and hashes.
2. Confirm whether the referenced docs/*.md files are real approved corpus sources; if so, add/identify their exact versioned artifacts. Do not substitute unit-test fixtures for source documents.
3. Preserve Qw's first-pass artifact unchanged. After corpus identity is established, freeze/hash the exact file and record a traceable attestation that labels were produced without retrieval outputs.
4. Qw should resolve the explicit Q030 contradiction and clarify Q041/Q050; Ka will review changes as a new version and adjudicate disputed labels against source spans.
5. Keep all changes and review results in Work 103 evidence. Do not claim blind-label gate PASS or RAG E2E PASS until source-grounded checks and live E2E evidence pass.

**Signature:** Ka | CSA / Independent Reviewer
