# WORK 28 — LỆNH GIAO NHIỆM VỤ XÂY DỰNG E2E-AUTOMATIC
Ngày: 15/10/2026 (UTC+07)
Người giao việc: Ka — CSA / Work 28 Coordinator
Thẩm quyền cuối cùng: Vinh
Trạng thái: BUILD ACTIVE; LIVE E2E / python_run / registry mutation / release vẫn NO-GO cho đến khi được phê duyệt riêng.

## 1. Quyết định
Work 28 chuyển trọng tâm sang BUILD. Không để công việc xây dựng đứng chờ vòng nghiệm thu độc lập. Kiểm thử được thực hiện như một phần của quá trình phát triển; Go không chỉ làm reviewer mà được giao vai trò implementer/builder. Cla không chỉ viết review mà trực tiếp xây dựng và khắc phục lớp bảo mật. Ka chịu trách nhiệm điều phối, thiết kế hợp đồng, phân rã công việc và tích hợp trong phạm vi sandbox. Go vẫn phải đưa ra kết luận E2E độc lập ở giai đoạn acceptance cuối, tách biệt với việc tự kiểm thử code do Go triển khai.

## 2. Go — BUILDER / IMPLEMENTER (chủ trì xây dựng)
Mục tiêu: biến hợp đồng và blueprint hiện có thành implementation có thể kiểm thử trong Work 28.
Thực hiện theo thứ tự:
1. Đọc MCP-8020-TOOLING-PLATFORM/00_ROOT/WORK_MANIFEST.md, 01_ORIGINAL/WORK_28_REQUIREMENT.md, 03_ARCHITECTURE/WORK_28_ARCHITECTURE_PLAN.md, 03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md, 03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md, 03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md, 04_CODE/tool_contracts.py, 05_TEST/WORK_28_TEST_PLAN.md và evidence liên quan.
2. Audit implementation hiện hữu; không viết lại từ đầu khi có thể mở rộng an toàn. Ghi rõ file thiếu, contract mismatch và dependency.
3. Xây các thành phần Work 28 theo boundary hiện hành: validation/contract; request schema; server-side authorization interface; WorkContext/principal binding interface; digest/revision preconditions; DRY_RUN plan; structured result; evidence record/readback interface; timeout/size/resource limits; failure handling.
4. Bổ sung unit tests và negative tests cho forged PASS, missing/tampered evidence, digest mismatch, replay/idempotency reuse, forged principal, cross-Work access, caller spoofing, timeout và lỗi adapter.
5. Chỉ thực thi các test local/sandbox an toàn, không kích hoạt python_run trên PC, không sửa live registry, không ghi PC/GitHub, không sync/merge/release.
6. Ghi kết quả thực tế bằng command, exit code, số tests/failures/errors/skipped, log path, SHA-256 và readback. Không ghi PASS nếu chưa chạy.
7. Nộp checkpoint và blocker cụ thể; không tự ký thay Cla hoặc tự cấp quyền mở gate.
Đầu ra: implementation + tests trong phạm vi Work 28 sandbox, checkpoint kỹ thuật và nhật ký thi công cập nhật.

## 3. Cla — SECURITY ENGINEER / HARDENING OWNER
Mục tiêu: xây và khắc phục security controls ngay trong implementation, không dừng ở review.
Thực hiện song song với Go:
1. Đọc security review 12/10 và danh sách red tests; chuyển từng Critical/High finding thành security requirement, regression test và remediation.
2. Xây/hoàn thiện các guardrails phía server: principal phải lấy từ Core/authenticated caller context; caller không được tự khai authorized, operation_kind hoặc principal để vượt quyền; ràng buộc WorkContext; từ chối cross-Work read/cancel; kiểm tra digest/revision trước khi lập plan.
3. Xây/hoàn thiện kiểm soát chống replay/idempotency misuse, tampering/missing evidence, forged PASS và lỗi readback.
4. Xây/hoàn thiện timeout, giới hạn payload/resource/network, OS/process isolation và process-tree cleanup ở mức mà runtime/host hiện có hỗ trợ. Nếu cần quyền PC/OS hoặc bằng chứng runtime chưa có, tạo interface + testable contract và ghi rõ dependency; không giả lập thành production PASS.
5. Tạo regression tests cho từng finding và ghi mapping finding → remediation → test → evidence.
6. Nộp security engineering checkpoint. Chỉ sau khi remediation và bằng chứng chạy được cung cấp, lập Security Review mới với từng mục PASS/BLOCKED và command/log/exit code/SHA.
7. Không tự bật tool/registry, không cho phép python_run, không thực hiện PC/GitHub writes, sync, merge hoặc release.
Đầu ra: security controls/remediation trong phạm vi được phép, red/regression tests, mapping phát hiện và checkpoint. Security Review mới là đầu ra sau khi có bằng chứng; không thay thế việc xây dựng.

## 4. Ka — CSA / WORK 28 COORDINATOR
1. Điều phối Go và Cla theo workstream song song, xử lý xung đột contract và dependency.
2. Duy trì source-audit-first, Evidence First và không tạo Core/bridge/runtime thứ hai.
3. Giữ Core :8000 là authority; MCP :8020 là adapter. Không vượt boundary sang Work 12/13/27 hoặc Work 101 nếu chưa có handoff/authorization phù hợp.
4. Duyệt contract, tích hợp các checkpoint vào build plan và cập nhật biên bản/nhật ký trong Work 28 sandbox.
5. Yêu cầu PC/runtime evidence riêng cho những phần không thể chứng minh bằng sandbox.
6. Không tự tuyên bố live E2E PASS hoặc security PASS khi chưa có bằng chứng runtime.
7. Trình Vinh các quyết định cần quyền quản trị; không tự mở gate.

## 5. Phân tách BUILD và ACCEPTANCE
- BUILD: Go implementer; Cla security engineer; Ka điều phối/tích hợp.
- Component tests: người xây dựng chạy và lưu log trong quá trình làm.
- Security acceptance: Cla cung cấp đánh giá dựa trên remediation và evidence, nhưng không được bỏ qua các finding chưa giải quyết.
- Independent live E2E acceptance: Go thực hiện ở giai đoạn cuối khi runtime inputs đã sẵn sàng; kết luận phải dựa trên live evidence, không dựa vào sandbox-only success.
- Final gate: Vinh quyết định. Không ai tự cấp quyền đăng ký tool hoặc mutation.

## 6. Phạm vi cấm vẫn giữ nguyên
Cho đến khi có phê duyệt riêng: python_run NO-GO; live registry change NO-GO; PC/GitHub write NO-GO; sync/merge/release NO-GO. Việc xây dựng code và tests trong sandbox không đồng nghĩa được phép kích hoạt tool trên PC.

## 7. Báo cáo tiến độ bắt buộc
Mỗi người cập nhật theo mẫu:
TÊN — VAI TRÒ — ngày/giờ UTC+07 — BUILD STATUS — files changed — tests run — exit code — test counters — evidence path — SHA-256 — blockers/dependencies — next action.
Không chấp nhận báo cáo chỉ có “xong” hoặc “PASS” mà thiếu bằng chứng có thể đọc lại.

## 8. Lệnh điều phối
Go bắt đầu BUILD theo Mục 2 ngay; Cla bắt đầu SECURITY ENGINEERING/HARDENING theo Mục 3 song song; Ka điều phối và tích hợp theo Mục 4. Không chờ Xu. Xu chỉ được yêu cầu khi có dependency kiến trúc cụ thể và không được biến thành điều kiện chờ chung.

---
Ka — CSA / Work 28 Coordinator
15/10/2026 UTC+07
Ghi chú: đây là lệnh phân công được ghi vào Work 28 Sandbox; chưa phải commit vào repository PC/GitHub và không tự mở bất kỳ gate runtime nào.