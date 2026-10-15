# WORK 28 — LỆNH GIAO TRỌN GÓI E2E-AUTOMATIC
Order ID: KA-W28-E2E-AUTO-FULL-20261015
Ngày: 15/10/2026 UTC+07
Work: 28 — MCP-8020-TOOLING-PLATFORM
Thẩm quyền cuối: Vinh — Project Owner
Người ký/điều phối: Ka — Chief System Architect (CSA), Work 28 Coordinator
Trạng thái lúc giao: ACTIVE / NOT LOCKED; LIVE E2E BLOCKED; SECURITY NO-GO.

## LỆNH DUY NHẤT
Go là Delivery Owner, chịu trách nhiệm đầu-cuối từ source/runtime inventory, implementation, regression tests, runner tự động, sửa và chạy lại, evidence, phối hợp Cla, live E2E độc lập và báo cáo bàn giao cuối. Không dừng ở việc viết kế hoạch hoặc báo blocker rồi chờ giao việc tiếp. Các mục bên dưới là checklist nội bộ của cùng nhiệm vụ, không phải các đợt giao việc rời.

Cla chịu trách nhiệm review bảo mật độc lập trên implementation cuối và có quyền kết luận SECURITY NO-GO. Ka giữ kiến trúc, audit evidence và tổng hợp gate. Vinh giữ quyền cuối cùng đối với đăng ký tool, thay đổi runtime/registry, sync, merge, release và đóng Work.

## KẾT QUẢ ĐẦU-CUỐI CẦN CHỨNG MINH
Authenticated request → MCP :8020 → Core :8000 authorization và Core-derived principal/WorkContext → capability/runtime canonical đã phê duyệt (W12/W13/Work 27) → immutable source snapshot + manifest/digest → isolated execution với giới hạn tài nguyên/mạng/thời gian → kết quả được xác minh độc lập → protected evidence → authorized readback → Cla security verdict → Go live E2E acceptance → Ka tổng hợp trình Vinh.

## CHECKLIST TRONG CÙNG MỘT PIPELINE
1. Ràng buộc deployed source/runtime: listener PID, executable, working directory, loaded entrypoint/adapter, cấu hình không bí mật, source revision/hash và raw MCP initialize/tools/list. Không quan sát được thì ghi rõ.
2. Hoàn thiện contract/adapter và test: xử lý KA-AUDIT-28-07 (chỉ nhận string mapping keys, từ chối NaN/±Infinity, định nghĩa serialization của result Any), cùng identity/WorkContext, ownership, error/status, path containment/symlink, replay/idempotency và evidence binding.
3. Bảo vệ kết quả test: không tin summary do test code tự khai; phát hiện forged PASS, zero/all-skipped, thiếu counters, bool counters, sai inventory, non-zero exit, thiếu/tampered evidence và replay.
4. Tạo/hoàn thiện runner xác định, chạy từ root đã tài liệu hóa, giữ stdout/stderr, command, exit code, Python/runtime version, test counters/inventory, request_id/run_id, source/snapshot digest, timestamps và evidence_ref. Exit khác 0 nếu bất kỳ yêu cầu bắt buộc nào fail.
5. Chứng minh Core-derived principal + WorkContext; xác minh rủi ro alternate execution listener N08; OS isolation, không host secrets/network/loopback, least privilege, quotas, timeout/tree cleanup, evidence writer được bảo vệ.
6. Thực hiện positive và negative E2E: smoke, intentional failure, forged principal, cross-Work, traversal/symlink race, mutation sau snapshot, forged test summary, zero/all-skipped, timeout/tree cleanup, replay, evidence tamper/delete/overwrite, alternate-host/Core/MCP reachability, resource exhaustion, patch → digest mới → rerun nhưng giữ evidence cũ. Đối chiếu A01–A30; case chưa chạy phải ghi NOT RUN và dependency cụ thể.
7. Tự sửa lỗi trong Sandbox, review diff/scope, thêm regression test, rerun; không xóa evidence cũ, không tự mở quyền hay tự phê duyệt.
8. Cla review độc lập; Go chạy live E2E độc lập trên listener/runtime thật khi prerequisites đã được chứng minh. Nộp MỘT báo cáo cuối: GO_WORK28_E2E_AUTOMATIC_FINAL_20261015.md, một ma trận G0–G7/A01–A30, changed files, logs, exact commands, exit codes, counters, digests/readback và một danh sách blockers.

## BẰNG CHỨNG VÀ RANH GIỚI
Mỗi claim cần artifact path, command/request, endpoint, timestamp UTC+07, process/runtime/source revision, hash (hoặc NOT AVAILABLE với lý do), logs, exit code, counters, request_id/run_id, snapshot digest, runtime profile, evidence hash/readback và người review. Phân biệt SOURCE REVIEW, LOCAL TEST, APPROVED RUNNER, LIVE E2E, READBACK.
MAIN SOURCE read-only; Sandbox là BUILD ZONE. Core :8000 là authority duy nhất; MCP :8020 là adapter. Không tạo Core/runtime thay thế hoặc bypass. Không bật/đăng ký python_run, không live registry mutation, không PC/GitHub writes, sync/merge/release nếu chưa được Vinh duyệt riêng. Không tuyên bố PASS nếu không có log thực thi. Nếu thiếu PC/runtime/tool, tiếp tục phần an toàn có thể làm và gom dependency vào báo cáo cuối; chỉ báo ngay blocker Critical/High hoặc quyết định kiến trúc/quyền hạn.

## TÌNH TRẠNG ĐIỂM XUẤT PHÁT
Contract được báo cáo ở v1.2.1; Ka đã đóng hai phát hiện trước ở mức source review nhưng chưa có test run được xác nhận. KA-AUDIT-28-07 còn mở. Báo cáo Cla 2026-10-12 là SECURITY NO-GO; phải review lại source/runtime cuối. Các báo cáo gần nhất ghi 0 test trên runner được duyệt; live listener/source binding, principal/WorkContext, OS isolation, protected evidence và live E2E còn BLOCKED.

## XÁC NHẬN GIAO VIỆC
Go và Cla phản hồi bằng một gói trạng thái tổng hợp: DONE/BLOCKED, artifact paths, commands, logs, exit codes, hashes (nếu có), gate matrix, blockers. Inbox query gần nhất của go và cla đều rỗng. Chưa có action dispatch task được xác minh trong phiên này, nên tài liệu này không được mô tả là đã xuất hiện trong inbox cá nhân; phải đọc lại artifact trong Work Sandbox.

---
KÝ LỆNH: Ka — Chief System Architect (CSA) / Work 28 Coordinator
Agent ID: ka-csa
Ngày ký: 15/10/2026 UTC+07
Phạm vi chữ ký: chữ ký văn bản điều phối; không phải chữ ký mật mã, không chứng minh runtime/test và không thay quyền phê duyệt cuối của Vinh.
QUYẾT ĐỊNH HIỆN TẠI: BUILD CONTINUES; LIVE E2E BLOCKED; SECURITY NO-GO; RELEASE NO-GO.
