# WORK 98 — ONT CARE: E2E AUTOMATIC BUILD PLAN
- TÊN: Xu
- CHỨC DANH: Work 98 technical lead
- NGÀY: 2026-10-13
- GIỜ-PHÚT: 15:02 UTC+7
- TRẠNG THÁI: PLAN DRAFT / CHƯA CÓ E2E PASS
- AUTHORITY: Vinh quyết định cuối cùng; kế hoạch không tự cấp quyền tích hợp/phát hành.

## 1. Quyết định nền tảng
1. Work 98 / ONT Care là dự án độc lập, không phụ thuộc ROOM-HOP Core :8000, MCP :8020 hoặc ROOM-HOP Dashboard để app chạy.
2. MCP :8020 chỉ là kênh quản lý Work Sandbox/đọc-ghi source và evidence theo tool contract; không phải dependency runtime của ONT Care.
3. Quy trình thi công trong Sandbox qua MCP: READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.
4. Có source sẵn: audit trước, tái sử dụng phần tốt, sửa theo evidence; không dựng lại từ đầu, không tuyên bố test khi chưa chạy.
5. Phải có hai mục DASH và PREVIEW. DASH là dashboard sản phẩm; PREVIEW là nơi xem build/test, không phải dashboard sản phẩm.
6. Sandbox và GitHub dùng cấu trúc logic song song. Sandbox là vùng thi công; GitHub là quản lý phiên bản/CI. Không tuyên bố đã sync/commit/push nếu chưa có evidence.
7. Chỉ lập kế hoạch và audit ở lượt này; không tự ý tích hợp ngoài Sandbox hay vượt quyền phê duyệt.

## 2. Source đã phát hiện qua MCP
- Có source ở Work root và thư mục ont-platform/.
- ont-platform/ là prototype React + TypeScript + TanStack Router/Start + Vite; có route dashboard (/), technician (/technician), customer (/customer), shared provider/mock data.
- Có ont-platform/.github/workflows/e2e.yml và e2e/deep_links_e2e.py.
- Có thư mục preview/ ở root, nhưng preview/data.json là snapshot danh sách file, ghi ngày 2026-10-04; preview hiện chỉ hiển thị cấu trúc Work/metadata, chưa phải product preview.
- Root README mô tả “Scaffold only”, trong khi ont-platform/roadmap.md ghi prototype dashboard/mobile/deep links/E2E/CI đã có. Đây là mâu thuẫn tài liệu cần hợp nhất, không xóa lịch sử.
- Đây mới là static source audit qua MCP. Chưa chạy build/lint/browser E2E, chưa kết nối ONT thật; chưa có runtime PASS.

## 3. Mục tiêu sản phẩm
### DASH — PC Operations Dashboard
- Tổng quan thuê bao, ONT, trạng thái WAN/Wi-Fi, cảnh báo, ticket, kỹ thuật viên và khu vực.
- Tra cứu khách hàng/ONT; trang chi tiết ONT; lịch sử diagnostic; quản lý ticket và phân công.
- Mọi dữ liệu phải gắn nguồn/trạng thái LIVE, CACHED, MOCK hoặc UNKNOWN; không giả dữ liệu thật.
- Quản lý tài khoản/role theo acc, audit log và cấu hình trong phạm vi được phép.

### APP — một app dùng chung cho kỹ thuật viên và khách hàng
- Đăng nhập bằng acc; quyền theo role được xác thực ở trusted service/local-agent boundary, không chỉ ẩn nút UI.
- Khách: trạng thái có bằng chứng, kiểm tra kết nối, thiết bị LAN, báo sự cố, theo dõi ticket.
- Thợ: nhận việc, xem dữ liệu được phân quyền, chạy diagnostic read-only, ghi kết quả, xác nhận và hoàn tất ticket.

### PREVIEW — build review
- Tab DASH / APP-KHÁCH / APP-KỸ THUẬT / E2E / BUILD & EVIDENCE.
- Hiển thị build ID, source revision nếu có, thời điểm tạo, data mode, kết quả build/test và evidence.
- Có DEMO/MOCK label rõ ràng; không trình bày mock như dữ liệu ONT thật.
- Preview dùng build artifact/source revision xác định, không dùng snapshot danh sách file cũ.

## 4. Kiến trúc độc lập
DASH + Mobile/PWA → ONT Care application services → Direct ONT Access adapters + local persistence/queue → optional sync.
- Không gọi ROOM-HOP Core :8000.
- Không yêu cầu MCP :8020 khi app chạy cho khách/thợ.
- Direct ONT Access: discovery/fingerprint, capability profile theo vendor/model/firmware, session an toàn, collector read-only, parser/normalizer, cache/queue local.
- Trường không được ONT hỗ trợ trả UNAVAILABLE/UNSUPPORTED; không tự suy ra.
- Lệnh có thể đổi cấu hình ONT bị chặn mặc định; chỉ thêm sau threat model, test và phê duyệt.
- Không ghi credential vào log, client bundle hoặc GitHub.

## 5. E2E Automatic — vòng khép kín
1. DISCOVER: liệt kê Work 98, source tree, manifests, scripts, tests, preview, CI.
2. TRACE: lập dependency graph DASH/APP/PREVIEW/data/adapters/tests; phân biệt prototype, mock và live capability.
3. BASELINE: đọc source liên quan; xác định test commands từ package/CI; ghi revision nếu tool hỗ trợ.
4. PLAN: task P0/P1/P2, file dự kiến sửa, rủi ro, test và rollback.
5. BUILD: sửa source trong Sandbox qua MCP, thay đổi nhỏ, giữ hồ sơ append-only.
6. VERIFY: chạy install/build/lint/unit/E2E nếu Sandbox có execution capability. Nếu MCP chỉ đọc/ghi file thì báo BLOCKED runtime verification, không giả lập kết quả.
7. REPAIR LOOP: đọc log, tìm nguyên nhân gốc, sửa và chạy lại test lỗi cùng regression suite; dừng khi thiếu quyền/thiết bị/credential/evidence.
8. PREVIEW: tạo preview từ source revision xác định; kiểm tra DASH và hai role mobile, loading/empty/error states và deep links.
9. EVIDENCE: lưu lệnh, exit code, logs, test report, screenshots nếu có, revision và timestamp trong 06_EVIDENCE/.
10. HANDOFF: báo DONE/PASS/BLOCKED/DECISION theo từng mục. Không tự merge/commit/push hoặc triển khai ngoài Sandbox.

## 6. P0 acceptance gates
- G0: xác định canonical source; không còn mâu thuẫn README/roadmap.
- G1: clean install + production build PASS.
- G2: lint/typecheck PASS theo scripts đã xác nhận.
- G3: role isolation; khách không gọi được thao tác thợ/admin qua deep link.
- G4: dữ liệu mock/demo có nhãn; không trình bày là live.
- G5: Direct ONT capability detection, read-only allowlist, timeout/retry, credential/session safety; ONT thật mới cho phép tuyên bố verified.
- G6: E2E DASH + khách + thợ + ticket + deep links có evidence.
- G7: preview hiển thị source revision/data mode/test state.
- G8: source audit chứng minh runtime không cần Core :8000 hoặc MCP :8020.
- G9: không có secrets trong source/log; authorization ở trusted boundary.

## 7. Cấu trúc song song
Xem GITHUB_PARALLEL_STRUCTURE_20261013.md. Dùng relative paths tương ứng; evidence/runtime artifacts không commit nếu chưa được duyệt.

## 8. Thứ tự thi công
P0-A source audit sâu + baseline + canonical source.
P0-B chuẩn hóa DASH, APP, PREVIEW và data mode.
P0-C build/lint/typecheck/E2E automation + evidence.
P0-D acc/role, ticket flow, data contracts và security gates.
P0-E Direct ONT adapters/capability profiles trên ONT thật.
P1 offline-first, local queue/sync, diagnostic history, notifications.
P2 AI diagnosis dựa trên evidence; không tự điều khiển cấu hình ONT.

## 9. Trạng thái trung thực
- DONE: source tree và tài liệu chính đã đọc qua MCP.
- FOUND: prototype hiện hữu và CI/E2E files; có ont-platform/ và root preview/.
- BLOCKED: chưa có bằng chứng runtime build/test từ MCP trong phiên này.
- DECISION: cần Vinh duyệt kế hoạch trước khi triển khai kiến trúc sản phẩm.
