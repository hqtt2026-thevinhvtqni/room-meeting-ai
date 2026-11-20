# MA TRẬN NĂNG LỰC AI MEMBER — WORK 17 (G2)

- Work ID: 17 · Ngày lập: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Nguồn khai báo: DOC-010 AI Identity Register v1.1 (W0000/.../AI_TEAM_AND_TOKEN_USAGE.md) — chỉ đạt cấp E0, không phải bằng chứng runtime (theo tiêu chí ở 02_DEFINE).
- Thông tin trạng thái ban đầu được lấy từ Journal Entry 002 (ngày 2026-11-19).

## Ma trận — roster đầy đủ và trạng thái bằng chứng hiện tại

| Member | Roster / role declared | Identity & session | Dispatch / ACK | Quyền & policy | Tool/provider / execution | Evidence hiện có | Token telemetry | Conflict / disposition |
|---|---|---|---|---|---|---|---|---|
| AI-01 Xu | CEO / Orchestrator — GPT | NOT_VERIFIED độc lập; có hoạt động điều phối được ghi trong W17 journal, chưa có session-auth artifact | NOT_PROVEN | UNASSESSED theo task scope | Provider/model exact theo session NOT_VERIFIED | W17 Journal Entry 008–011 (E0/E1) | NOT_AVAILABLE | — |
| AI-02 Ka | CSA / Architecture Reviewer — GPT | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Exact model/session/source access NOT_VERIFIED | DOC-010 roster E0; DOC-054 assignment records are not receipt proof | NOT_AVAILABLE | — |
| AI-03 Cla | CTO / Code-Debug Lead — Claude | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Exact model/session/repository access NOT_VERIFIED | DOC-010 roster E0; no attributable ACK found in inspected dispatch records | NOT_AVAILABLE | — |
| AI-04 Kha | Strategy & Product Architect — Gemini | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Exact model/session/provider invocation NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | — |
| AI-05 Qw | QE / Independent QA; Qween role label | NOT_VERIFIED | NOT_PROVEN | QE scope/independence must be checked per assignment | Exact provider/model/session NOT_VERIFIED | DOC-010 roster E0; DOC-043 defines QE role | NOT_AVAILABLE | DOC-025 legacy text labels provider “Qwen”; distinguish Qween QA role from Qc Qwen Coder |
| AI-06 | CONFLICT: DOC-010 v1.1 says Qc / Qwen Coder; DOC-043 + DOC-096 say Go / CFO | CONFLICT — do not authenticate by ID | NOT_PROVEN | BLOCKED for ID-based authorization until reconciled | Provider/session binding NOT_VERIFIED | DOC-010, DOC-025, DOC-043, DOC-096 (E0) | NOT_AVAILABLE | Stable ID conflict; Xu recommends AI-06 = Go, pending Vinh decision |
| AI-07 | CONFLICT: DOC-010 v1.1 says Go / CFO; DOC-043 + DOC-096 say Co / Coder Assistant | CONFLICT — do not authenticate by ID | NOT_PROVEN | BLOCKED for ID-based authorization until reconciled | Provider/session binding NOT_VERIFIED | DOC-010, DOC-025, DOC-043, DOC-096 (E0) | NOT_AVAILABLE | Stable ID conflict; Xu recommends AI-07 = Co, pending Vinh decision |
| AI-08 | DOC-010 v1.1 says Co / GPT Coder Assistant; no numeric assignment for Qc in newer DOC-043 / DOC-096 mapping | CONFLICT / UNMAPPED | NOT_PROVEN | BLOCKED for ID-based authorization until reconciled | Qc provider/model/session NOT_VERIFIED | DOC-010, DOC-025, DOC-043, DOC-096 (E0) | NOT_AVAILABLE | Xu recommends AI-08 = Qc / Qwen Coder, pending Vinh decision |
| AI-09 Vi | Coder / Implementation Engineer — GPT | NOT_VERIFIED | NOT_PROVEN | Repository/path/branch grant must be verified per task | Exact model/session and access NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | — |
| AI-10 An | Tester / Test Engineer — GPT | NOT_VERIFIED | NOT_PROVEN | Test-environment access must be verified per task | Test execution identity NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | Independent QE status is assignment-specific; not assumed |
| AI-11 Mê | CXO / Customer Experience — Meta AI | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Provider/backend/session NOT_VERIFIED | DOC-010 roster E0; historical local MeAgent source is not Meta AI identity proof | NOT_AVAILABLE | Separate local placeholder from external Meta AI participant |
| AI-12 La | COO / PMO — Dola AI | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Backend model/provider/session NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | Do not infer foundation model from product label |
| AI-13 De | CRO / Evidence & Risk Control — DeepSeek | NOT_VERIFIED | NOT_PROVEN | UNASSESSED | Exact model/session NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | — |
| AI-14 Xuco Coder | Coder / Implementation Engineer — separate ChatGPT conversation | NOT_VERIFIED | NOT_PROVEN | Assignment-specific repository/path/branch grant NOT_VERIFIED | Separate session from Xu/Co; exact model NOT_VERIFIED | DOC-010 roster E0 | NOT_AVAILABLE | Do not merge with AI-01 Xu or AI-07 Co |
| Support: Vibe | External Coding Support — Mistral/Vibe Code on Web; not a numbered ROOM-HOP AI member | Provider/session identity NOT_VERIFIED from available commit metadata | No private-session dispatch/ACK evidence | GitHub-only scope must be verified per assignment | GitHub artifacts exist; provider runtime identity not independently authenticated | W17 Entry 007 and commits 6d1f3df / da6c9ba; artifact attribution recorded, runtime identity E0/E1 only | NOT_AVAILABLE | External support; do not add to AI-01…AI-14 without a separate decision |

## Quy tắc điền bổ sung

1. Mỗi ô phải điền bằng trạng thái taxonomy (RUNTIME_VERIFIED / NOT_VERIFIED / CONFLICT ...) + cấp evidence (E0–E4) + đường dẫn bằng chứng; cấm điền "Có".
2. Điền xong phải đọc lại ngược về nguồn (DOC-010, DOC-043 AI-ROLE-PERMISSION-MATRIX, journal các Work dispatch).
3. Ma trận này là điều kiện bắt buộc để chốt G2; ô nào thiếu evidence câm giữ NOT_VERIFIED.
4. Khi có dispatch/ACK thật lần đầu tiên (GAP-01), cập nhật cả DOC-010 version mới, ghi Decision Log (DOC-006), không ghi đè nhật ký cũ.

## Định nghĩa chấp nhận bảng này (G2 exit criteria)

- 100% member có trạng thái identity/session + dispatch/ACK reconciliation rõ ràng.
- 100% ô mang link evidence hoặc nhãn NOT_VERIFIED/UNASSESSED.
- Mọi xung đột (GAP-05, GAP-09) được chốt quyết định của Vinh trước khi xây GAP khác lên trên.


## Roster source reconciliation — 2026-11-19

- Sources read from Sandbox: Work 0000 `AI_TEAM_AND_TOKEN_USAGE.md` (DOC-010 v1.1, updated 2026-11-03); Work 70 `AI_PARTICIPANTS_AND_TOKEN_USAGE.md` (DOC-025 v1.3, explicitly marked LEGACY / REFERENCE); Work 70 DOC-043 v1.0 with 2026-11-11 addenda; Work 70 DOC-096 v1.0; DOC-054 assignment/ACK rules; DOC-072 dispatch architecture reconciliation.
- DOC-010 and legacy DOC-025 both declare AI-06=Qc, AI-07=Go, AI-08=Co. Newer DOC-043 and DOC-096 state AI-06=Go and AI-07=Co; they do not assign a numeric ID to Qc. This is a real source conflict, not a spelling-only issue.
- Proposed mapping for Vinh's decision: **AI-06 Go (CFO), AI-07 Co (Coder Assistant), AI-08 Qc (Qwen Coder)**. This proposal is NOT applied to the canonical roster and must not be used for automated authorization until Vinh approves and the roster owner updates DOC-010 / Work 70 authoritative register with a Decision Log entry.
- Qw remains AI-05 QE/QA by role. DOC-025's historical “Qwen” provider text is ambiguous against the Qween QA label and Qc Qwen Coder; exact provider/model identity must be established from session evidence, not the role label.
- DOC-054 explicitly separates assignment readiness from AI receipt/ACK. DOC-072 says private-session dispatch, delivery and ACK were not executed/proven by the inspected toolset. Therefore all member dispatch/ACK cells remain NOT_PROVEN; this does not deny documented artifact contributions, but it prevents treating them as verified private-session delivery.
- DOC-010 and DOC-025 contain no verified provider usage ledger; all token/cost fields remain NOT_AVAILABLE. No zero or estimate is substituted.
- The local `agents/me_agent.py` source is a rule-based placeholder; it is not evidence that external AI-11 Mê / Meta AI has connected or participated.
- No identity IDs, permissions, provider sessions or token records were changed by this reconciliation.


## W300 demand-to-member capability mapping — proposal only (2026-11-20)

This section links W300 image/photo demand to existing roster roles for focused assessment. It does not change canonical identity/session, dispatch/ACK, permission, runtime or token status. All those fields retain existing NOT_VERIFIED / NOT_PROVEN / UNASSESSED values until independent evidence is recorded.

| Member | Candidate capability area to assess | Proposed evidence required | Current verdict |
|---|---|---|---|
| Xu / AI-01 | Coordination, traceability, evidence reconciliation | Reproducible plan, source links, journal, decision and handoff trace | NOT_ASSESSED |
| Ka / AI-02 | Architecture, privacy, security, trust boundaries | Independent threat/data-flow review, permission and failure-mode findings | NOT_ASSESSED |
| Cla / AI-03 | Image-processing design, API/provider contracts, technical debugging | Exact schema/source review, bounded tests when authorized, error-path analysis | NOT_ASSESSED |
| Kha / AI-04 | Model/provider research and product trade-offs | Official model/version/pricing/eligibility evidence, source date and unknowns register | NOT_ASSESSED |
| Qw / AI-05 | Independent image QA and acceptance design | Rubric, hard-fail taxonomy, repeatability/negative-test plan and independent results | NOT_ASSESSED |
| Go / AI-06 | Cost, quota and budget safety | Pricing arithmetic separated from measured usage; preflight and budget-control review | NOT_ASSESSED |
| Nu / Manus | Independent source research and candidate workflow execution | Identity/session proof, exact source/version, reproducible evidence and permission boundary | NOT_VERIFIED; runtime capability not inferred |
| Vi / AI-09 | Implementation candidate for approved image processing/adapter tasks | Task-specific repo/path/branch grant, patch, tests and review evidence | NOT_ASSESSED; role is not availability proof |
| An / AI-10 | Test execution candidate | Exact test environment, identity, commands, results and artifact hashes | NOT_ASSESSED; independent status is task-specific |
| Qc / Qwen Coder | UI/backend implementation candidate if explicitly assigned | Resolve roster-ID conflict first; task-specific grant, patch, CI and review evidence | ID/identity conflict OPEN; no authorization inferred |

### W300 capability demand taxonomy for G2 evidence planning
1. Safe local image processing and bounded decoding.
2. Provider/model research and exact compatibility/pricing verification.
3. Image generation vs reference-conditioned editing vs deterministic transformations.
4. Image output QA, integrity, dimensions and content acceptance.
5. Cost/quota gates, persistent circuit breaker and safe timeout handling.
6. Image privacy/security, rights/consent, metadata and deletion.
7. Versioned artifact provenance, storage-neutral URI and SHA-256 integrity.
8. Evidence-first multi-agent workflow and honest handoff/ACK semantics.

### Controls
- This is demand mapping, not evidence of capability. No row becomes E2/E3/E4 from this proposal.
- Do not alter canonical roster identity, numeric IDs, provider/session identity, permissions or token ledger; existing roster conflicts remain unresolved.
- W21 supplies Skill research/specification; W17 retains canonical member-capability verdicts; W300 retains product acceptance and build authority.
- Independent review and Vinh decision are required before any canonical matrix promotion or implementation assignment.
