# Work 103 — No-Answer Leak Analysis

- Reviewer: Ka | CSA / Independent Reviewer
- Date: 2026-10-29 (UTC+07:00)
- Working-tree reproduction reported at: `5756a6e`
- GitHub branch at time of sync: `work/103-rag-retrieval-capability`
- Decision: **STRICT NO-ANSWER GATE FAILS; W103 ACTIVE / BLOCKED**
- This report records reproduced observations and does not change the fixture, thresholds, retrieval code, evaluator, or labels V3.

## 1. Reproduction evidence

The reported local rerun against the corpus-aligned V4/V3 fixture produced:
- Unit tests: 44 passed.
- Corpus-aligned gate at `min_score=0.35`: Hit@5=0.950, Precision@5=0.880, Recall@5=0.950, MRR=0.9375, answered rate=0.975, strict no-answer accuracy=0.300.
- The strict evaluator exits 1 because no-answer accuracy is below the required 0.800 floor.
- Grounded-abstention report-only result at 0.35: strict=0.300, grounded=0.600. No tested threshold satisfies both answerable-query and no-answer requirements.

These values are transcribed from the reported local reproduction; this document does not claim an independent rerun of the user's `/workspace`.

## 2. Seven no-answer leaks at threshold 0.35

| Query | Retrieved score | Reported source/collision | Analysis |
|---|---:|---|---|
| Q008 | 0.990 | `00_CORPUS/sales.md` | Persistent at 0.45. The source describes confirming an existing delivery schedule; it does not establish a procedure for changing the schedule. Grounded-absence mapping is borderline here. |
| Q035 | 0.736 | `00_CORPUS/sales.md` | Persistent at 0.45. Customer/order vocabulary overlaps with answerable sales queries; generic process text must not establish that a named customer has an order. |
| Q010 | 0.636 | `00_CORPUS/sales.md` | Persistent at 0.45. Schedule-related vocabulary does not establish where schedules are stored. |
| Q032 | 0.434 | See per-query CI diagnostics | Near-threshold terminology/process collision; not in the current documented-absence mapping. Do not expand the mapping solely to improve the supplemental metric. |
| Q044 | 0.429 | Architecture/retrieval terminology | Candidate documented-absence case, subject to exact-span and scope review. |
| Q025 | 0.367 | See per-query CI diagnostics | Near-threshold peripheral terminology collision; not in the current documented-absence mapping. Do not expand the mapping solely to improve the supplemental metric. |
| Q004 | 0.412 | `00_CORPUS/network.md` | Candidate documented-absence case if the retrieved exact span explicitly establishes that the requested RX threshold is unspecified. |

The table records the reported top scores and source-level analysis. For Q025/Q032, the exact source/chunk should be read from the saved per-query diagnostic output rather than inferred here.

## 3. Root cause: no single-threshold fix

Q008, Q035 and Q010 remain leaks even at threshold 0.45. These queries collide lexically with answerable queries whose expected source is the same document:
- `sales.md`: Q006, Q007, Q009 and Q034.
- `security.md`: Q021–Q024, Q040 and Q050.

Raising `min_score` enough to block these false matches harms answerable-query Hit@5, Recall@5 and MRR. The reproduced sweep therefore provides evidence that **no single threshold tested satisfies both sides of the gate**. This is a limitation of lexical relevance as a proxy for semantic answer support, not a reason to lower acceptance floors.

## 4. Grounded-abstention caution

The supplemental grounded-abstention mapping is not a replacement for the strict no-answer metric. Q004 and Q044 may qualify only if exact source spans and scope support an explicit “unspecified” interpretation. Q008 is borderline: the sales source's statement about confirming a delivery schedule is not itself evidence that a schedule-change process is unspecified.

Do not broaden the mapping to include Q025, Q032 or Q008 merely to improve the supplemental score. Require independent review of the exact source span and the scope of any absence statement.

## 5. Next remediation boundary

Close threshold-only tuning as the primary remediation path. A separately designed **evidence-support stage** should distinguish:
- direct supporting evidence;
- explicit contradiction;
- a scoped statement that the requested detail is unspecified;
- insufficient evidence; and
- conflicting evidence.

The stage must preserve exact source/chunk/line provenance, fail closed, and remain separately tested from ranking. This report does not authorize implementation, change labels V3, or approve any production integration.

See [Evidence-Support Stage Design Proposal V1](KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V1_20261029.md).

## 6. Status

- Retrieval metrics: five answerable-query metrics meet their floors at 0.35.
- Strict no-answer gate: **FAIL** (0.300 < 0.800).
- Labels V3, fixture, baseline floors and retrieval code: unchanged.
- Live MCP :8020 → Core :8000 → retrieval → source-readback E2E: **CLOSED / NOT RUN**.
- Work 103: **ACTIVE / BLOCKED**.

— Ka | CSA / Independent Reviewer
