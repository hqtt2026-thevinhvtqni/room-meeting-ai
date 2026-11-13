# WP3-F01 — HỒ SƠ QUYẾT ĐỊNH CHO XU (DECISION BRIEF)

**Work:** 28 — MCP Tooling Platform  
**Branch:** `work/28-wp3-xu-decision-brief` (nhánh làm việc riêng, tách từ canonical `work/28-mcp-tooling-platform` tại `563b03f`)  
**Ngày lập:** 2026-11-13  
**Người lập:** Vibe, theo ủy quyền tự chủ của Vinh  
**Người quyết:** XU (trong phạm vi ủy quyền điều phối); capability-grant bắt buộc qua KA review trước khi cấp  
**Tài liệu gốc:** `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md`  
**Nhật ký tham chiếu:** JRN-W28-013, JRN-W28-014 (canonical journal)

---

## BỐI CẢNH

Feature W28-WP3-F01 `sandbox_upload_file` (upload binary byte-preserving vào Sandbox, theo JRN-W28-005) đang **IMPLEMENTATION BLOCKED** vì 4 câu hỏi hợp đồng chưa được quyết. Trace nguồn (VI_WP3_BINARY_UPLOAD_SOURCE_TRACE_20261104.md) xác nhận: v54 chỉ có write/read text UTF-8, không có tool/schema/registration upload binary; Core authorizer đã staged nhưng CHƯA wire vào dispatch v54.

Vinh đã trả lời 4 câu hỏi trong phiên 2026-11-13 (ghi tại JRN-W28-014): **3 câu CHƯA QUYẾT, 1 câu CHƯA CHẤP THUẬN (yêu cầu Ka review trước)**. Hồ sơ này tổng hợp options + hệ quả để Xu quyết.

---

## CÂU HỎI 1 — TRUSTED CALLER CONTEXT (ai được server tin là đã xác thực?)

**Trạng thái Vinh: CHƯA QUYẾT.**

| Option | Mô tả | Ưu | Nhược |
|---|---|---|---|
| A. MCP/transport session đã xác thực | Server tin identity từ transport layer (stdio parent / HTTP session sau auth) | Ít mã mới; khớp mô hình MCP hiện tại | Phụ thuộc transport đúng cấu hình; HTTP phải bật auth trước khi lộ tool |
| B. Service credential pinned | Server xác thực riêng bằng credential cấp out-of-band (như HMAC key của E2E gate) | Không phụ thuộc transport; test được độc lập | Phải quản lý vòng đời credential; thêm bề mặt secret |

**Khuyến nghị kỹ thuật (không ràng buộc):** Option A cho môi trường hiện tại (stdio + Core wired trước), thêm B khi mở HTTP public. Điều kiện PASS: caller không xác thực được → mọi upload op trả lỗi trước khi đụng filesystem.

---

## CÂU HỎI 2 — MAPPING WORK ID (Core W28 ↔ Sandbox 28)

**Trạng thái Vinh: CHƯA QUYẾT.**

| Option | Mô tả | Ưu | Nhược |
|---|---|---|---|
| A. Mapping tĩnh cấu hình | Bảng tĩnh W{n} ↔ sandbox id trong cấu hình server | Đơn giản, dễ audit, đủ cho 1 Work | Phải cập nhật tay khi thêm Work; rủi ro lệch nếu cấu hình sai |
| B. Core cấp mapping động | Core trả sandbox id trong WorkContext/authorization response | Một nguồn sự thật là Core; tự động | Phải wire Core authorizer vào v54 dispatch trước (chưa làm) |

**Khuyến nghị kỹ thuật:** Option B là đích đúng (Core :8000 là authority duy nhất); Option A chỉ chấp nhận làm bước trung gian có ghi rõ trong evidence là tạm thời. Cấm hardcode mapping trong code tool.

---

## CÂU HỎI 3 — HÌNH THỨC TOOL (1 streaming vs 3 begin/chunk/finalize)

**Trạng thái Vinh: CHƯA QUYẾT.**

| Option | Mô tả | Ưu | Nhược |
|---|---|---|---|
| A. 1 tool streaming | `sandbox_upload_file` nhận toàn bộ nội dung trong 1 call | Contract đơn giản; ít state server-side | Giới hạn kích thước bởi giới hạn message; khó resume; khó quota theo chunk |
| B. 3 tool session (begin/chunk/finalize) | begin cấp session id; chunk ghi từng phần có index; finalize seal + checksum + atomic promote | Hỗ trợ file lớn, resume, quota, hủy giữa chừng; khớp acceptance trong JRN-W28-005 (chunked/interrupted) | Nhiều state (session TTL, idempotency); nhiều bề mặt kiểm tra bảo mật hơn |

**Khuyến nghị kỹ thuật:** Option B khớp yêu cầu acceptance đã duyệt (interrupted/chunked transfer, cancellation, concurrent uploads). Nếu chọn B: session phải TTL ngắn, bind session ↔ (caller, work_id, path), chunk index kiểm tra thứ tự, finalize mới promote; hủy/tiêu session phải dọn staging.

---

## CÂU HỎI 4 — CORE CAPABILITY-GRANT CHO UPLOAD

**Trạng thái Vinh: CHƯA CHẤP THUẬN — BẮT BUỘC KA REVIEW TRƯỚC KHI CẤP.**

Vấn đề: upload là side-effect ghi ra filesystem. Core phải cấp capability rõ ràng (work_id, op=upload, path scope, quota, TTL) và server phải kiểm tra grant TRƯỚC MỌI side effect. Không có grant → mọi op trả AUTHORIZATION DENIED, không tạo staging dir.

**Bước bắt buộc:** Ka review thiết kế grant trong proposal gốc trước khi Xu phê duyệt bất kỳ option nào của Câu 4. Xu không được cấp grant vượt đề xuất Ka đã review.

---

## QUY TẮC THI CÔNG SAU KHI XU QUYẾT

1. Code chỉ viết trên nhánh này (hoặc nhánh feature tách từ đây) cho đến khi 4 quyết định chốt; sau đó mới merge về canonical qua PR có CI xanh.
2. Không đụng MCP :8020; không đổi Core/Runtime/Execution Host.
3. Mọi commit phải kèm test + CI evidence; không khai PASS khi chưa có run xanh trên commit đó.
4. An (QA độc lập) và Ka (security review) phải xác nhận trước khi WP3-F01 rời trạng thái BLOCKED.
5. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

## TRẠNG THÁI HIỆN TẠI

- WP3-F01: IMPLEMENTATION BLOCKED (4 quyết định pending tại Xu; grant chờ Ka review).
- WP2: service BLOCKED mapping + race coverage đã commit (98d68a7, 31f21c3); CI run #327 trên 8c9ff9d đang chạy, chưa khai PASS.
- Không có code upload nào được viết trong commit này (tài liệu thuần).
