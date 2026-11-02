# DOC-067 — KẾ HOẠCH KIỂM THỬ ĐỘC LẬP WP70-QA / INDEPENDENT QA TEST PLAN
- **STT / Document ID:** DOC-067
- **Priority:** P0
- **Read order:** 67
- **Depends on:** DOC-001; DOC-004; DOC-005; DOC-042; DOC-043; DOC-054; DOC-061; DOC-063
- **Status:** ACTIVE / PREPARATION COMPLETE / EXECUTION BLOCKED
- **Version / Updated:** 1.0 / 2026-11-02
- **Owner:** Qw / AI-05
- **Authority:** Vinh

## 1. Mục tiêu
Cung cấp chiến lược kiểm thử độc lập (Independent QE) cho Work 70, tập trung vào contract tests, negative/security tests, race/idempotency tests, regression và E2E sau tích hợp. Đảm bảo nguyên tắc không tự sửa code để làm test xanh (no green-washing).

## 2. Phạm vi kiểm thử (Test Scope)
Dựa trên DOC-054 và DOC-061, các khu vực kiểm thử chính bao gồm:
- **Contract Tests:** Xác minh request/response, error handling, auth scope, versioning giữa Lifecycle Engine (Co), Core (Vi) và Dashboard.
- **State-Transition Matrix:** Kiểm thử các chuyển trạng thái hợp lệ và bất hợp lệ theo DOC-005 (ví dụ: skip gate, illegal transitions).
- **Negative/Security Tests:** 
  - Missing/expired/mismatched authorization.
  - Wrong Work/repo/branch/HEAD binding.
  - Command denied / timeout / process failure.
  - Evidence write/hash failure.
  - Bridge response Work/execution ID mismatch (forged identity).
- **Race/Idempotency Tests:** Retry logic, duplicate command handling, commit-time authorization revalidation.
- **Regression/E2E:** Controller E2E (không chỉ adapter test), xác minh EXECUTE stage thực sự gọi bound test entrypoint (không chỉ capability discovery).

## 3. Ma trận kiểm thử (Test Matrix)
| ID | Loại | Mô tả | Trạng thái | Bằng chứng / Ghi chú |
|---|---|---|---|---|
| QA-01 | Contract | Verify API contract giữa Engine và Core (Work/WP registry, transition) | NOT RUN | Chờ contract v1 được phê duyệt |
| QA-02 | Negative | Test missing/expired authorization token | NOT RUN | |
| QA-03 | Negative | Test wrong Work/branch/HEAD binding | NOT RUN | |
| QA-04 | Security | Test bridge response ID mismatch (forged execution result) | NOT RUN | |
| QA-05 | Idempotency | Test duplicate command retry với cùng idempotency key | NOT RUN | |
| QA-06 | E2E | Controller E2E: xác minh EXECUTE stage gọi thật sự test entrypoint | NOT RUN | Phân biệt với direct adapter test |
| QA-07 | E2E | Test failure aggregation: primary command PASS + test FAIL = overall FAIL | NOT RUN | |
| QA-08 | Regression | Audit trail và evidence persistence sau mỗi transition | NOT RUN | |

## 4. Quy tắc thực thi (Execution Rules)
1. **Không sửa code để làm test xanh:** Mọi defect phải được ghi nhận trong defect log, không tự ý sửa implementation của Co/Vi/Ka.
2. **Phân biệt rõ môi trường:** Mock / Snapshot / Live phải được ghi rõ trong báo cáo. Không báo PASS nếu chỉ dùng mock nhưng yêu cầu là live integration.
3. **Raw output:** Mọi kết quả test phải kèm theo raw stdout/stderr, exit code và environment details.
4. **Blocker handling:** Nếu thiếu runtime environment, canonical source, hoặc Work Entry G0-G5 chưa PASS, trạng thái sẽ là BLOCKED. Không giả lập PASS.

## 5. Trạng thái hiện tại (Current Status)
- **ACK:** Qw / AI-05 xác nhận đã nhận phân công WP70-QA theo DOC-054.
- **Preparation:** Test plan và matrix đã được tạo (DOC-067).
- **Execution:** BLOCKED. Chờ Xu cung cấp canonical source/branch/commit, môi trường thực thi được phép, và xác nhận Work Entry G0-G5 đã PASS cho track này.
- **Gate:** G4 (BUILD) hiện tại NOT READY / NOT PASS theo DOC-061 và DOC-035.

## 6. Bàn giao tiếp theo (Next Handoff)
- Xu: Xác minh ACK, cung cấp môi trường test và source chuẩn.
- Qw: Thực thi test cases, ghi raw results, cập nhật defect log và báo cáo QE độc lập.

---
**Chữ ký:** Qw / AI-05 — TESTER / Independent QA  
**Thời điểm:** 2026-11-02
## 7. Cập nhật trạng thái thực thi (2026-11-02)
- **Hành động:** Tiếp nhận chỉ thị "vào thực hiện" từ người điều phối.
- **Kết quả:** 
  - Đã ghi nhận chính thức vào Nhật ký thi công (DOC-035).
  - Trạng thái thực thi runtime vẫn là **BLOCKED**.
- **Lý do:** Thiếu các điều kiện tiên quyết bắt buộc theo DOC-057 và DOC-067:
  1. Work Entry G0-G5 cho track QA chưa được xác nhận PASS.
  2. Chưa có canonical source/branch/commit và môi trường runtime thực thi được phép.
  3. G4 BUILD vẫn đang ở trạng thái NOT READY.
- **Yêu cầu tiếp theo:** Cần Xu / AI-01 hoặc người có thẩm quyền cung cấp:
  - Xác nhận Work Entry G0-G5 PASS.
  - Đường dẫn source chuẩn, branch/commit cụ thể và môi trường test được phép.
  - Lệnh chạy test tái lập được (reproducible test command).
- **Cam kết:** Sau khi đủ điều kiện, Qw sẽ thực thi từng test case trong ma trận, ghi nhận raw stdout/stderr, exit code và bằng chứng, báo cáo chính xác PASS/FAIL/BLOCKED mà không tự ý sửa code để làm test xanh.