# LỆNH ĐIỀU PHỐI TOÀN LỰC — WORK 28
Ngày: 2026-10-16 (+07)
Chỉ huy mục tiêu: Vinh; điều phối: Xu.
Trạng thái: ACTIVE / NOT LOCKED.

## Mệnh lệnh
Ưu tiên duy nhất hiện tại là hoàn thành Work 28 — MCP-8020-TOOLING-PLATFORM. Không mở rộng phạm vi sang Work khác, không khởi động lại Work đã khóa, không biến việc điều tra phụ thuộc thành dự án riêng. Chỉ đọc phụ thuộc bên ngoài khi có bằng chứng rằng một gate của Work 28 cần nó; mọi thay đổi giữ trong phạm vi Work 28.

## Bảo toàn và giới hạn
1. Không checkout/reset/stash/ghi đè working tree PC; không sửa source ngoài Work 28.
2. Không tự ý mở lại Work 13. Nếu hợp đồng phụ thuộc không đủ, ghi BLOCKED với bằng chứng và phương án tối thiểu; không sửa Work 13.
3. Không unrestricted shell/Python tùy ý, không tạo Core 2/runtime/bridge trùng lặp, không bypass Core :8000.
4. Không ghi PASS chỉ từ tài liệu, static review, readback hoặc unit tests chưa chạy qua runtime được duyệt.
5. Mỗi thay đổi có regression test; lưu lệnh chạy, exit code, số test, log, revision/hash và evidence path khi khả dụng.
6. Giữ VS Code/local repository song song GitHub trên branch work/28-mcp-tooling-platform; không merge main trước khi release gates đạt.

## Trình tự READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF
A. Đối chiếu source/test/evidence của Work 28 trên Sandbox và GitHub; xác định sai lệch, không đoán.
B. Chạy canonical unit/regression suite trên checkout hiện tại. Giữ riêng kết quả 26 targeted tests ngày 16/10 và CI 56 tests trước đó; không gọi là full-suite PASS.
C. Sửa lỗi thuộc Work 28 trên nhánh Work 28; thêm regression tests và rerun.
D. Đóng security/contract gates: identity/principal binding, Core authorization, Work-relative path containment, bounded output/timeouts, secret redaction, audit, readback/evidence integrity.
E. Xác minh live MCP :8020 tools/list và gọi tool thật qua đường được hỗ trợ. Ghi nguồn/thời điểm; không suy ra PC registry từ connector inventory.
F. Kiểm chứng Python/execution chỉ qua capability được Core cho phép và runtime canonical đã có. Nếu thiếu bằng chứng, đánh dấu gate cụ thể BLOCKED; tiếp tục các phần Work 28 độc lập, không tạo runtime thay thế.
G. Chạy acceptance E2E gồm success, intentional failure, timeout/limits, unauthorized, path traversal, mutation + readback, evidence completeness. Lưu run ID, exit code, output/log và hash nếu công cụ hỗ trợ.
H. Kiểm tra GitHub Actions trên commit cuối và xử lý/cô lập cảnh báo cleanup submodule trong phạm vi Work 28.

## Review lanes
- Go: review acceptance/E2E và khả năng tái lập bằng chứng.
- Cla: security review độc lập về identity/Core boundary, path containment, execution isolation, evidence trust.
- Ka: đối chiếu gates, kết luận PASS/FAIL/BLOCKED theo evidence.
- Xu: điều phối liên tục trong Work 28. Tài liệu giao việc không chứng minh agent đã nhận việc; nếu inbox/acknowledgement không khả dụng, tiếp tục việc làm được và ghi giới hạn.

## Điều kiện nghiệm thu
- Live MCP :8020 registry được quan sát và đối chiếu contract.
- Identity/principal gắn với phiên gọi; Core authorization được chứng minh; không tin caller-supplied identity/authorized flag.
- Contract/path/security tests chạy với log/exit code; không làm yếu test để né lỗi.
- Execution chỉ qua runtime/capability canonical được phê duyệt; không unrestricted shell/bypass.
- E2E success và negative cases có output/readback/evidence đầy đủ.
- GitHub Actions pass trên commit cuối; cảnh báo còn lại được xử lý hoặc giải thích.
- Biên bản, nhật ký, README cập nhật đúng thực tế. Chỉ đề xuất release/merge khi mọi gate bắt buộc PASS.

## Trạng thái tại lúc ban hành
- CI trước đó: 56 tests PASS trên commit trước; không đại diện live E2E.
- Người dùng cung cấp kết quả 26 targeted tests PASS, exit code 0, log và SHA-256; chưa tự xác minh file log hoặc checkout nguồn.
- Live PC MCP :8020 registry, identity/Core-auth E2E và canonical execution E2E chưa được xác nhận PASS.
- Work 28 ACTIVE / NOT LOCKED; chưa merge/release.
