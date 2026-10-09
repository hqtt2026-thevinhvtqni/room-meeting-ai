# WORK INDEX — 99

## 1. Mục đích

Work 99 là **WORK INDEX (sổ đăng ký Work)** của ROOM-HOP Sandbox.

Đây là registry runtime trung tâm để theo dõi toàn bộ Work hiện có.

## 2. Quy tắc quản lý

- Work ID do VINH cấp và không bao giờ tái sử dụng.
- Mỗi Work tồn tại trong runtime phải có đúng một dòng trong registry.
- Khi Work mới được tạo thành công, registry phải được bổ sung.
- Khi Work đạt trạng thái hoàn thành thực sự (DONE/PASS theo acceptance của Work), registry phải chuyển: **COMPLETED + LOCKED**.
- Work còn ACTIVE/TEST/BLOCKED/IN_PROGRESS không được tự động LOCK.
- LOCKED nghĩa là Work đã hoàn thành và source/evidence của Work không được sửa ngoài quy trình được VINH cho phép.
- Không tự ý đổi Work ID hoặc đổi tên Work đã tồn tại.
- Nếu runtime và registry lệch nhau: **BLOCKED — WORK_REGISTRY_DRIFT**.

## 3. Runtime Work Registry — RECONCILED 2026-10-10

| Work ID | Work Name | Display Name | Trạng thái | Lock | Mô tả |
|---|---|---|---|---|---|
| 01 | AI-BUILD-GATEWAY | 01 - Xây Gateway ROOM | ACTIVE | NO | Gateway AI, Sandbox và ranh giới phát triển |
| 02 | MCP-UNIFIED-AUTHORIZATION | 02 - MCP-UNIFIED-AUTHORIZATION | ACTIVE | NO | Phân quyền thống nhất cho MCP |
| 03 | GO-DATA-TRANSFER | 03 - GO-DATA-TRANSFER | ACTIVE | NO | Luồng truyền dữ liệu cho Go |
| 04 | 04 - BH Alert 5P Analysis | 04 - BH Alert 5P (Mobile Rescue Alert) | ACTIVE | NO | BH Alert 5P và preview/dashboard |
| 05 | GOOGLE-WORKSPACE-DOCS-DRIVE | 05 - GOOGLE-WORKSPACE-DOCS-DRIVE | ACTIVE | NO | Google Workspace Docs/Drive |
| 06 | REMOTE-LAB-MOBILE-PC | 06 - REMOTE-LAB-MOBILE-PC | ACTIVE | NO | Remote Lab Mobile-PC |
| 07 | App TV | 07 - App TV | ACTIVE | NO | Ứng dụng TV/nội dung giải trí |
| 08 | VSCode-Web | 08 - VSCode trên Web | ACTIVE | NO | VSCode Web/editor/workspace |
| 09 | ROOM-HOP-BROWSER-AGENT-ADAPTER | 09 - ROOM-HOP-BROWSER-AGENT-ADAPTER | ACTIVE | NO | Browser Agent Adapter |
| 091 | BROWSER-WORKFLOW-ENGINE | 091 - BROWSER-WORKFLOW-ENGINE | ACTIVE | NO | Browser Workflow Engine |
| 092 | 00_ROOT | 092 - 00_ROOT | ACTIVE | NO | Runtime Work hiện có; metadata cần chuẩn hóa |
| 10 | COMPUTER-AGENT | 10 - COMPUTER-AGENT | ACTIVE | NO | Computer Agent |
| 11 | AI-MEMBER-ADAPTER | 11 - AI-MEMBER-ADAPTER | ACTIVE | NO | Adapter cho AI member |
| 111 | 00_ROOT | 111 - 00_ROOT | ACTIVE | NO | Runtime Work hiện có; metadata cần chuẩn hóa |
| 12 | WORK-EXECUTION-ENVIRONMENT | 12 - WORK-EXECUTION-ENVIRONMENT | BLOCKED | NO | WEE foundation; real E2E còn BLOCKED vì thiếu canonical execution/runtime bindings |
| 13 | EXECUTION-HOST-INFRASTRUCTURE | 13 - EXECUTION-HOST-INFRASTRUCTURE | ACTIVE | NO | Execution Host infrastructure; chưa có acceptance evidence hoàn tất |
| 14 | AUTONOMOUS-E2E-BUILDER | 14 - AUTONOMOUS-E2E-BUILDER | COMPLETED | LOCKED | W14 Browser + Autonomous Execution UI via W13 canonical host; release d6ce49e268ab |
| 15 | WEBSITE-BUILDER | 15 - WEBSITE-BUILDER | ACTIVE | NO | Autonomous website creation/execution workflow; PHASE 0 bootstrap |
| 20 | CREATE-AGENT | 20 - CREATE-AGENT | ACTIVE | NO | Agent creation, architecture và agent brain/cost work |
| 21 | AI-SKILLS | 21 - AI-SKILLS | ACTIVE | NO | AI Skills schema, stack, multi-agent và Browser E2E Skill |
| 22 | SECURITY-AND-SAFETY | 22 - SECURITY-AND-SAFETY | ACTIVE | NO | Message Security, threat model, security architecture và safety |
| 89 | XI-MANG-NGHI-SON-SALES-CUSTOMER-EXPERIENCE | 89 - XI-MANG-NGHI-SON-SALES-CUSTOMER-EXPERIENCE | ACTIVE | NO | Hai dashboard Xi măng Nghi Sơn; đặc tả MVP và kế hoạch E2E; chưa triển khai ứng dụng |
| 802001 | 00_ROOT | 802001 - 00_ROOT | TEST | NO | Runtime test Work |
| 91 | 00_ROOT | 91 - 00_ROOT | ACTIVE | NO | Work 91 — Harness Engineering Audit |
| 96 | 00_ROOT | 96 - 00_ROOT | ACTIVE | NO | Runtime Work hiện có; metadata cần chuẩn hóa |
| 97 | SANDBOX-97 | 97 - SANDBOX-97 | TEST | NO | Sandbox test Work / voice biên bản experiment |
| 98 | ONT-CARE | 98 - ONT-CARE | ACTIVE | NO | ONT Care; khảo sát, kiến trúc và biên bản nghiên cứu |
| 99 | WORK-INDEX | 99 - WORK-INDEX | SYSTEM | N/A | Registry quản lý toàn bộ Work |

**Runtime count:** 28 Works.

### Metadata drift cần theo dõi

- Work 13 runtime metadata hiện vẫn trả work_name=06_EVIDENCE; nội dung/evidence của Work xác định mục tiêu là EXECUTION-HOST-INFRASTRUCTURE.
- Work 15 chưa có WORK_MANIFEST.md, nhưng có WEBSITE-BUILDER/WORK.md với trạng thái IN_PROGRESS; registry giữ ACTIVE và ghi rõ phase.
- Work 98 runtime metadata hiện trả work_name=e2e, nhưng BIEN_BAN_W98.md xác nhận Work 98 là ONT care; registry dùng tên canonical theo biên bản.
- Work 092, 111 và 96 vẫn tồn tại trong runtime nhưng metadata còn 00_ROOT; chưa tự ý đổi Work ID hoặc tên runtime.

Các metadata drift trên không phải lý do để xóa Work hoặc tái sử dụng Work ID. Chúng cần được chuẩn hóa tại nguồn khi có authority phù hợp.

## 4. Quy trình lifecycle

CREATE
  ↓
RUNTIME CREATE OK
  ↓
REGISTER IN WORK INDEX
  ↓
ACTIVE / TEST
  ↓
WORK ACCEPTANCE PASS
  ↓
COMPLETED
  ↓
LOCKED

**BLOCKED không đồng nghĩa COMPLETED và không được LOCK.**

Đặc biệt:
- Work 12 hiện BLOCKED / NOT LOCKED vì real E2E vẫn thiếu canonical runtime/execution bindings.
- Work 14 hiện BLOCKED / DO_NOT_LOCK theo evidence W14.
- Work 13 vẫn ACTIVE / NOT LOCKED.
- Work 89 mới tạo, đang ở SPECIFICATION / BOOTSTRAP; không được đánh dấu COMPLETED hoặc LOCKED.

## 5. Reconciliation rule

Nguồn kiểm tra runtime:
sandbox_list_works

Mỗi lần reconcile phải so sánh:
Runtime Works == WORK INDEX

Nếu runtime có Work chưa có trong Index → bổ sung entry.

Nếu Index có Work không tồn tại trong runtime → báo:
WORK_REGISTRY_DRIFT

Không tự ý xóa Work khỏi registry hoặc tái sử dụng Work ID.

## 6. Current reconciliation — 2026-10-10

Runtime hiện có **28 Work** theo kết quả sandbox_list_works sau khi tạo Work 89.

Work mới:
- 89 — XI-MANG-NGHI-SON-SALES-CUSTOMER-EXPERIENCE — ACTIVE / NOT LOCKED.

Đã cập nhật:
- Work 89 được bổ sung vào registry.
- Work 89 vẫn ACTIVE vì hiện mới có đặc tả, mô hình dữ liệu, phân quyền và kế hoạch E2E.
- Không có Work nào được chuyển COMPLETED + LOCKED trong lần cập nhật này.

## 7. Automation status

Quy tắc lifecycle đã được chốt tại Work Index.

Tuy nhiên, auto-update trực tiếp từ runtime create_work → WORK_INDEX.md chưa được chứng minh là đang chạy trong MAIN SOURCE.

Sandbox hiện cho phép cập nhật file Work 99 nhưng chưa expose execution hook để sửa MAIN SOURCE.

Vì vậy không claim rằng cơ chế auto-register/auto-lock runtime đã được implement live.

**STATUS: REGISTRY FILE UPDATED VIA MCP / AUTO-HOOK NOT YET VERIFIED**

## 8. Authority

Authority: **VINH**

Work Index: **Work 99**

Last reconciled: **2026-10-10**
