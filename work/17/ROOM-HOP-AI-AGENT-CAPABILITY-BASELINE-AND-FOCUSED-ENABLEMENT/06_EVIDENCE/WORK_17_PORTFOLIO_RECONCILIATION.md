# ĐỐI SOÁT DANH MỤC WORK: GITHUB MAIN MIRROR — WORK 17 (G0/G1)

- Work ID: 17 · Kỳ quét: 2026-11-19 · Phương pháp: liệt kê thư mục `work/` trên GitHub main (hqtt2026-thevinhvtqni/room-meeting-ai), đọc commit mới nhất của từng workfolder; sau đó so với danh mục Sandbox 71 Work (Journal Entry 002).
- Giới hạn: GitHub là MIRROR, Sandbox là nguồn registry; thiếu trên GitHub không có nghĩa Work không tồn tại → trạng thái mặc định của Work không thấy là MIRROR_MISSING, không phải NOT_FOUND.

## 1. Số liệu tổng

| Chỉ tiêu | Giá trị | Kết luận |
|----------|---------|----------|
| Work đăng ký trong Sandbox (sandbox_list_works, 2026-11-19) | 71 | Nguồn chuẩn danh mục |
| Snapshot DOC-018 (2026-11-03) | 56 | Chênh lệch +15 → GAP-06 |
| Workfolder mirror trên GitHub main | 17 | MVSR (Mirror Coverage) = 17/71 ≈ 24% → GAP-07 |
| Workfolder có tên đúng chuẩn `work/<ID>/<WORK-NAME>/` | 16/17 | W802001 và 0001/1111 tổ chức khác chuẩn → NAME_ANOMALY cần phân loại |

## 2. Bảng đối soát Workfolder mirror (dữ liệu thật)

| Work ID | Tên (mirror) | Commit mới nhất trên GitHub | Trạng thái đọc kỳ này |
|---------|--------------|------------------------------|------------------------|
| 0001 | TRADING-DECISION-LAB-REBUILD | "Work 0001: journal source extraction and transfer blocker" | TRACE — có blocker chuyển nguồn journal |
| 103 | (DecisionRAG experiment) | "docs(w103): add isolated DecisionRAG experiment plan" | TRACE |
| 1111 | ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB | "record Co read-only T07 authorization audit" | TRACE |
| 112 | ROOM-HOP-INTEGRATION-CONTRACTS-AND-EVIDENCE-ORCHESTRATION | "record framework ownership and work sync audit" | TRACE — liên quan trực tiếp GAP-07 |
| 113 | ROOM-HOP-UNIVERSAL-DASHBOARD | "finalize verified GitHub main sync checkpoint" | TRACE |
| 115 | CONSTRUCTION-SITE-MANAGEMENT | "journal logical model parity verification" | TRACE |
| 116 | ROOM-HOP-RESOURCE-LIBRARY | "journal — runtime reachability batch results" | TRACE — có runtime evidence mảng reachability |
| 117 | ROOM-MEDIA-HUB | "DASH-010 Vibe support pass — snapshot refresh + Xu audit fixes" | TRACE |
| 17 | ROOM-HOP-AI-AGENT-...-ENABLEMENT (Work này) | "docs(work-17): record final journal commit SHA" | ACTIVE |
| 28 | MCP-8020-TOOLING-PLATFORM | "define automatic E2E operating runbook v2" | TRACE — liên quan GAP-03 |
| 300 | ROOM-HOP-AI-CREATIVE-SERVICE | "add QE fatal gates and circuit breaker requirements" | TRACE |
| 501 | HQTT-UNIVERSAL-LLM-HUB | "record GitHub sync evidence and verification" | TRACE — liên quan GAP-02 |
| 502 | ME-AUTONOMOUS-AI-BUILDER | "Record final Work 502 MÊ journal verification" | TRACE |
| 70 | ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD | "record AI capability registry periodic audit" | TRACE — control plane |
| 75 | AI-NETWORK-GUARDIAN | "record GitHub bootstrap verification" | TRACE |
| 76 | AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK | "record Co execution handoff in canonical journal" | TRACE |
| 802001 | (architecture package self-audit) | "record architecture package consistency self-audit" | NAME_ANOMALY — số 6 chữ số, không khớp dãy ID chuẩn |

## 3. Phân loại chênh lệch (bổ sung GAP-06)

1. Nhật ký Entry 001 ghi 70 Work, Entry 002 ghi 71 Work cùng ngày → xác định Work mới xuất hiện giữa hai lần list là Work 17 (chính Work này tạo ra). Khuyến nghị: ghi chú chênh lệch 70→71 là ĐÃ GIẢI THÍCH.
2. Chênh lệch 56 (DOC-018, 2026-11-03) → 71 (2026-11-19): chưa giải thích; các Work tạo trong tháng 11 cần truy vết theo registry Sandbox, không suy đoán.
3. Mirror GitHub là lưới hẹp nhưng MINH BỊ CHẮC không đồng bộ theo thời gian thực (Entry 004 cũng ghi giới hạn này) → GAP-07 đề xuất nâng MVSR.

## 4. Điều kiện của bảng này

- Bảng 2 chỉ là KIỂM KÊ về mirror, không kết luận năng lực của các Work đó (chúng giữ trạng thái của tài liệu canonical trong Sandbox).
- Để chốt G1, cần bổ sung 54 Work còn lại từ danh mục Sandbox, mỗi mục: ID, tên chuẩn, trạng thái, owner, canonical path.


## 5. G1 — Sandbox intake for the 54 Works without GitHub workfolder mirror (2026-11-19)

- Method: refreshed `sandbox_list_works` (71 records); calculated the set difference against the 17 IDs listed in Section 2; called `sandbox_list(work_id)` for each of the 54 missing IDs; located and read the canonical/root `WORK_MANIFEST.md` or its DOC-001 pointer target using `sandbox_read_probe` where `sandbox_read` returned an empty object. No files were changed in those 54 Works.
- Inventory result: **54/54 IDs inspected; 54/54 manifest_exists=true; 54/54 canonical/root manifest content read or pointer target read**. This is an intake/readback result, not a full Work audit, source execution, runtime verification, or status endorsement.
- Every row below is `MIRROR_MISSING` on GitHub main relative to the 17-workfolder snapshot in Section 2. Work names are from Sandbox registry; status/owner are copied only where stated in the read manifest. `Không ghi rõ` means the manifest did not state it; it is not an inferred assignment.

| Work ID | Sandbox registry name | Manifest status (verbatim/normalized) | Owner / role stated | Canonical manifest path relative to Work Sandbox |
|---|---|---|---|---|
| 0000 | HQTT COMPANY — MASTER GOVERNANCE & WORK INDEX | ACTIVE | Vinh | HQTT COMPANY — MASTER GOVERNANCE & WORK INDEX/00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md |
| 01 | AI-BUILD-GATEWAY | ACTIVE | Vinh; Lead AI Xu | AI-BUILD-GATEWAY/00_ROOT/WORK_MANIFEST.md |
| 02 | MCP-UNIFIED-AUTHORIZATION | ACTIVE | Vinh; Lead AI Xu | MCP-UNIFIED-AUTHORIZATION/00_ROOT/WORK_MANIFEST.md |
| 03 | GO-DATA-TRANSFER | ACTIVE | Không ghi rõ | GO-DATA-TRANSFER/00_ROOT/WORK_MANIFEST.md |
| 04 | 04 - BH Alert 5P Analysis | ACTIVE | Không ghi rõ | 00_ROOT/WORK_MANIFEST.md |
| 05 | GOOGLE-WORKSPACE-DOCS-DRIVE | ACTIVE | Không ghi rõ | GOOGLE-WORKSPACE-DOCS-DRIVE/00_ROOT/WORK_MANIFEST.md |
| 06 | REMOTE-LAB-MOBILE-PC | ACTIVE | Không ghi rõ | REMOTE-LAB-MOBILE-PC/00_ROOT/WORK_MANIFEST.md |
| 07 | App TV | ACTIVE | Không ghi rõ | App TV/00_ROOT/WORK_MANIFEST.md |
| 08 | VSCode-Web | ACTIVE | Không ghi rõ | VSCode-Web/00_ROOT/WORK_MANIFEST.md |
| 09 | ROOM-HOP-BROWSER-AGENT-ADAPTER | ACTIVE | Không ghi rõ | ROOM-HOP-BROWSER-AGENT-ADAPTER/00_ROOT/WORK_MANIFEST.md |
| 091 | BROWSER-WORKFLOW-ENGINE | ACTIVE | Không ghi rõ | BROWSER-WORKFLOW-ENGINE/00_ROOT/WORK_MANIFEST.md |
| 092 | ROOM-HOP-BROWSER-PRODUCT-UX-V2 | DONE / PASS T1–T17 (theo Manifest) | Không ghi rõ | 00_ROOT/WORK_MANIFEST.md |
| 10 | COMPUTER-AGENT | ACTIVE — NOT RELEASED; gates partly BLOCKED | Không ghi rõ | COMPUTER-AGENT/00_ROOT/WORK_MANIFEST.md |
| 100 | ROOM-HOP-TECHNICAL-INCIDENTS-ROOT-CAUSE-AND-LESSONS | ACTIVE | Không ghi rõ | ROOM-HOP-TECHNICAL-INCIDENTS-ROOT-CAUSE-AND-LESSONS/00_ROOT/WORK_MANIFEST.md |
| 101 | ROOM-HOP-DUAL-WORKSPACE | ACTIVE — DRY_RUN; runtime adapter/E2E BLOCKED | Vinh | ROOM-HOP-DUAL-WORKSPACE/00_ROOT/WORK_MANIFEST.md |
| 102 | AI-AGENT-LOOP-PRODUCTION-READINESS | READY_FOR_PC_ACCEPTANCE; PC gates open | Vinh | AI-AGENT-LOOP-PRODUCTION-READINESS/00_ROOT/WORK_MANIFEST.md |
| 104 | AI-USAGE-EVIDENCE-TRACKING | ACTIVE — PLAN / INITIALIZATION | Vinh; Xu điều phối | 00_ROOT/WORK_MANIFEST.md |
| 11 | AI-MEMBER-ADAPTER | ACTIVE | Không ghi rõ | AI-MEMBER-ADAPTER/00_ROOT/WORK_MANIFEST.md |
| 111 | E2E SOURCE SNAPSHOT PROCESS | ACTIVE | Vinh; Xu điều phối; Cla thực thi | 00_ROOT/WORK_MANIFEST.md |
| 114 | ROOM-HOP-GRAPH-INTELLIGENCE-ARCHITECTURE | ACTIVE / DESIGN BASELINE; discovery PLANNED | Vinh; Xu điều phối | ROOM-HOP-GRAPH-INTELLIGENCE-ARCHITECTURE/00_ROOT/WORK_MANIFEST.md |
| 12 | WORK-EXECUTION-ENVIRONMENT | COMPLETED / LOCKED; future ownership W14 | Vinh | WORK-EXECUTION-ENVIRONMENT/00_ROOT/WORK_MANIFEST.md |
| 13 | EXECUTION-HOST-INFRASTRUCTURE | COMPLETED / LOCKED; absorbed by W14 | Không ghi rõ | EXECUTION-HOST-INFRASTRUCTURE/00_ROOT/WORK_MANIFEST.md |
| 14 | AUTONOMOUS-E2E-BUILDER | ACTIVE / UNLOCKED; NOT ACCEPTED / NOT RELEASED | Vinh; Xu điều phối | AUTONOMOUS-E2E-BUILDER/00_ROOT/DOC-001_W14_WORK_MANIFEST.md |
| 15 | WEBSITE-BUILDER | ACTIVE — PHASE 0 / bootstrap | Vinh | WEBSITE-BUILDER/WORK_MANIFEST.md |
| 16 | ROOM-HOP-WORKFLOW-ENGINE | ACTIVE — SPECIFICATION / EXPERIMENT-FIRST | Vinh | ROOM-HOP-WORKFLOW-ENGINE/00_ROOT/WORK_MANIFEST.md |
| 19 | CẤU TRÚC HỌC TẬP - AI AGENT PRODUCTION STACK 2026 | ACTIVE | Không ghi rõ | CẤU TRÚC HỌC TẬP - AI AGENT PRODUCTION STACK 2026/00_ROOT/WORK_MANIFEST.md |
| 20 | CREATE-AGENT | ACTIVE | Không ghi rõ | CREATE-AGENT/00_ROOT/WORK_MANIFEST.md |
| 200 | CRYPTO-TRADING-BOT | ACTIVE — PLAN / BUILD / VERIFY chưa hoàn tất | Vinh | CRYPTO-TRADING-BOT/00_ROOT/WORK_MANIFEST.md |
| 21 | AI-SKILLS | ACTIVE / NORMALIZATION IN PROGRESS; NOT ACCEPTED | Vinh; Xu điều phối | AI-SKILLS/00_ROOT/WORK_MANIFEST.md |
| 22 | SECURITY-AND-SAFETY | ACTIVE; NO-GO / NOT PASS | Không ghi rõ | SECURITY-AND-SAFETY/00_ROOT/WORK_MANIFEST.md |
| 23 | GEMINI-API-PROVIDER-INTEGRATION | ACTIVE; implementation/E2E NOT VERIFIED | Không ghi rõ | GEMINI-API-PROVIDER-INTEGRATION/00_ROOT/WORK_MANIFEST.md |
| 24 | PC-SOURCE-AND-WORKSPACE-BRIDGE | ACTIVE | Không ghi rõ | PC-SOURCE-AND-WORKSPACE-BRIDGE/00_ROOT/WORK_MANIFEST.md |
| 26 | MULTIMODAL-CAMERA-VOICE-PLATFORM | ACTIVE | Không ghi rõ | MULTIMODAL-CAMERA-VOICE-PLATFORM/00_ROOT/WORK_MANIFEST.md |
| 27 | SANDBOX-EXECUTION-RUNTIME-VSCODE | ACTIVE | Vinh; Xu điều phối | SANDBOX-EXECUTION-RUNTIME-VSCODE/00_ROOT/WORK_MANIFEST.md |
| 29 | HQTT-AI-VIDEO-STUDIO | ACTIVE | Không ghi rõ | HQTT-AI-VIDEO-STUDIO/00_ROOT/WORK_MANIFEST.md |
| 30 | GPT-AUTONOMOUS-BUILD-TEAM | ACTIVE / NOT LOCKED | Vinh; Xu điều phối | GPT-AUTONOMOUS-BUILD-TEAM/00_ROOT/WORK_MANIFEST.md |
| 31 | AUTOMATIC-E2E-PLAN | ACTIVE | Không ghi rõ | AUTOMATIC-E2E-PLAN/00_ROOT/WORK_MANIFEST.md |
| 32 | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER | ACTIVE — core CI/E2E PASS; Dashboard→Core/CD BLOCKED; NOT RELEASED | Vinh; Xu điều phối; Ka thực thi trong phạm vi | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md |
| 33 | ROOM-SHARED-FILE-EVIDENCE-HUB | ACTIVE | Không ghi rõ | ROOM-SHARED-FILE-EVIDENCE-HUB/00_ROOT/WORK_MANIFEST.md |
| 37 | ROOM-HOP-8000-CORE-SOURCE-OF-TRUTH | OPEN | Vinh; Xu điều phối | WORK_MANIFEST.md |
| 38 | ROOM-HOP-8040-GATEWAY-SERVICES | CREATED; technical audit NOT STARTED | Vinh; Xu khởi tạo | WORK_MANIFEST.md |
| 39 | MCP-8030-BUILD-TOOLS-AND-SERVICE | OPEN | Vinh; Xu điều phối | WORK_MANIFEST.md |
| 40 | MCP-8020-LIVE-TOOLS-AND-GATEWAY-OBSERVABILITY | ACTIVE — INITIALIZED; live verification NOT VERIFIED | Vinh; Xu điều phối | 00_ROOT/WORK_MANIFEST.md |
| 50 | HQTT AI Product Delivery Standard (APDS) | ACTIVE | Không ghi rõ | HQTT AI Product Delivery Standard (APDS)/00_ROOT/WORK_MANIFEST.md |
| 500 | PRODUCT-DEMO-AND-HANDS-ON-TEST-LAB | ACTIVE | Vinh; Xu điều phối | PRODUCT-DEMO-AND-HANDS-ON-TEST-LAB/00_ROOT/WORK_MANIFEST.md |
| 51 | CODER-TESTER-HQTT-AI | ACTIVE | Không ghi rõ | CODER-TESTER-HQTT-AI/00_ROOT/WORK_MANIFEST.md |
| 52 | ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION | ACTIVE / DESIGN-FIRST / NOT RELEASED | Không ghi rõ | ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION/00_ROOT/WORK_MANIFEST.md |
| 71 | ROOM-MEETING-NEXT-GENERATION | ACTIVE — INTAKE BASELINE; NOT_STARTED; G0/G1 NOT_READY | Vinh; Xu điều phối | ROOM-MEETING-NEXT-GENERATION/00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md |
| 89 | XI-MANG-NGHI-SON-SALES-CUSTOMER-EXPERIENCE | ACTIVE | Không ghi rõ | XI-MANG-NGHI-SON-SALES-CUSTOMER-EXPERIENCE/00_ROOT/WORK_MANIFEST.md |
| 91 | HARNESS-ENGINEERING-AUDIT | Không ghi rõ trong Manifest root | Không ghi rõ | 00_ROOT/WORK_MANIFEST.md |
| 96 | ROOM-STRUCTURE-COMPLETION | Không ghi rõ trong Manifest root | Vinh; Builder Co | 00_ROOT/WORK_MANIFEST.md |
| 97 | SANDBOX-97 | ACTIVE | Không ghi rõ | SANDBOX-97/00_ROOT/WORK_MANIFEST.md |
| 98 | ONT-CARE | ACTIVE — SOURCE TRANSFER STAGED; BUILD/E2E/LIVE NOT VERIFIED | Vinh; Xu điều phối | 00_ROOT/WORK_MANIFEST.md |
| 99 | WORK-INDEX | ACTIVE | Không ghi rõ | WORK-INDEX/00_ROOT/WORK_MANIFEST.md |

### G1 disposition and exceptions
1. **Inventory intake: DONE for the 54 IDs.** The 71-ID Sandbox registry and the 17-ID GitHub mirror list reconcile arithmetically: 17 + 54 = 71.
2. **Mirror status: MIRROR_MISSING** for all 54 at the checked snapshot; no missing Work is to be treated as deleted or nonexistent.
3. **Owner/status completeness: PARTIAL.** Where a manifest omitted owner or status, the table says so. Do not assign owners or infer lifecycle states from directory names.
4. **Canonical-path anomalies / duplicate manifests:** W03 has both `WORK_MANIFEST.md` and `DASHBOARD_WORK_MANIFEST.md`; W14 has a legacy `WORK_MANIFEST.md` and DOC-001 manifest; W30 has a nested GitHub mirror copy in Sandbox; W32 root `WORK_MANIFEST.md` is a compatibility pointer to DOC-001; W37/W38/W39 have root-level manifests plus nested same-ID Work folders; W40/W91/W96/W104/W092 contain additional nested same-ID or subproject manifests. These are retained as lineage/structure exceptions; no file was renamed, deleted, or silently chosen as a replacement.
5. **W0000, W32, W71:** root compatibility pointers were followed to their DOC-001 canonical targets. W92, W91, W96 and W104 were read at the Work root; nested same-ID records remain a reconciliation issue, not an additional Work count.
6. The 54 manifests are intake evidence E0 (document/registry) only. This does not close GAP-06's historical 56→71 explanation, does not prove GitHub parity, and does not promote G1 to full PASS. Per-Work ownership/dependency/evidence audits remain pending.
