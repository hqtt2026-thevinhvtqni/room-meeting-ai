# BIÊN BẢN TIẾP TỤC THI CÔNG WORK 28 — CO E2E-AUTOMATIC

- **Ngày:** 2026-10-16
- **Work:** 28 — MCP-8020-TOOLING-PLATFORM
- **Branch:** `work/28-mcp-tooling-platform`
- **Phạm vi:** Work 28 và Sandbox AI בלבד; không sửa Work 13.
- **Trạng thái:** ACTIVE / NOT RELEASED; E2E BLOCKED; release NO-GO.

## 1. Căn cứ ghi nhận

Co báo cáo đã xác nhận cấu trúc Sandbox Work 27/28 và ghi hồ sơ `CO_AUTOMATIC_E2E_CONTINUATION_BLOCKER_20261016.md`; lần liệt kê tiếp theo cho thấy file hiện diện. Co cũng báo cáo chưa đọc được source đầy đủ, chưa có thao tác chạy pytest/runtime, đọc GitHub source/Issue hoặc kiểm tra live MCP registry. Đây là báo cáo do Co cung cấp; Xu chưa có log chạy hoặc bằng chứng runtime độc lập mới để xác nhận E2E.

## 2. Quyết định

Không dừng ở kế hoạch và không viết thêm tài liệu thay cho thi công. Co tiếp tục tự chủ vòng:

`READ → TRACE → ANALYZE → DECIDE → BUILD → RUN → VERIFY → FIX → RETEST → READBACK EVIDENCE → HANDOFF`

Ka review không phải điều kiện để Co tiếp tục build/test trong phạm vi được phép.

## 3. Lệnh thi công cho Co

1. Thử và ghi nhận chính xác các capability thực có trong Sandbox: tên, schema, giới hạn quyền, request và response/lỗi nguyên văn. Không suy luận rằng có runner chỉ vì thấy file runner.
2. Nếu có Python/test runner được cấp phép: tạo và chạy runner E2E giới hạn Work 28, dùng allowlist; thu stdout, stderr, exit code, test inventory, revision SHA, log và SHA-256, cùng bằng chứng readback. Khi fail, phân loại, sửa trong phạm vi và chạy lại.
3. Nếu không có capability chạy test: hoàn thiện các phần code/test độc lập có thể kiểm chứng; tiếp tục truy tìm đường đọc source/capability được cấp phép; ghi lỗi/blocker có thể tái hiện. Không tạo mô phỏng giả thành E2E PASS.
4. Đối chiếu P0 readonly contract với adapter/registry hiện có; ưu tiên code, test bảo mật/negative cases và readback tests có thể thực hiện. Không lặp kiểm kê tổng quát và không tuyên bố PASS khi chưa chạy.
5. Chỉ tuyên bố live registration khi có snapshot `tools/list` của đúng MCP Sandbox/live endpoint; phân biệt rõ Sandbox MCP và PC MCP :8020.
6. Không sửa Work 13; không sửa PC/restart dịch vụ thật; không thay live registry; không mở quyền shell/Python tùy ý; không tin identity/quyền do caller tự khai; không commit/push nếu chưa xác minh quyền và đường thao tác.
7. Bàn giao bằng file/line, capability đã thử, request/response hoặc lỗi, command, exit code, số test, revision, log/hash, readback và blockers còn lại.

## 4. Tiêu chuẩn ghi trạng thái

- **DONE:** artifact đã tạo và đọc lại được; chỉ chứng minh persistence/readback.
- **PASS:** test hoặc luồng đã chạy thật, có kết quả và bằng chứng phù hợp.
- **BLOCKED:** nêu capability/quyền/endpoint thiếu và bằng chứng tái hiện.
- **NOT RUN:** chưa thực thi; không chuyển thành PASS theo suy luận.

## 5. Release gate

Chỉ xem xét bàn giao khi có E2E thật qua tool surface MCP Sandbox, bằng chứng đăng ký tool, xác thực/quyền đúng, kết quả thực thi, exit code, readback, regression/security tests và bằng chứng không làm hỏng tool cũ. Hiện tại các gate này chưa được chứng minh đầy đủ.

## 6. Liên kết và lịch sử

- Lệnh trực tiếp cho Co trên Issue #12: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/12#issuecomment-6208681664
- Nhật ký thi công: `NHAT_KY_THI_CONG.md`
- Kết luận hiện tại: **Work 28 ACTIVE / NOT RELEASED; E2E BLOCKED; RELEASE NO-GO; chưa merge main.**
