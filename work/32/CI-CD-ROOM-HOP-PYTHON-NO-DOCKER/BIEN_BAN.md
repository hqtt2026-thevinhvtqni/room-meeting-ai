# BIÊN BẢN — WORK 32
## CI-CD-ROOM-HOP-PYTHON-NO-DOCKER

- Người quyết định cuối cùng: Vinh
- Điều phối: Xu (AI-01)
- Reviewer độc lập: Ka (CSA)
- Thời điểm ghi: 2026-10-21, Asia/Ho_Chi_Minh (UTC+07:00)
- Trạng thái quyết định: SURVEY EVIDENCE RECORDED; IMPLEMENTATION CANDIDATE AUTHORIZED; CI ACTIVATION / MERGE / DEPLOY NOT AUTHORIZED BY THIS RECORD

### 1. Phạm vi
Xây dựng CI cho ROOM HOP bằng Python runner, không Docker. Chỉ khảo sát read-only và chuẩn bị patch trên Work branch. Không thay đổi MAIN SOURCE, không sửa dịch vụ đang chạy, không tạo secrets, không auto-merge, không deploy.

### 2. Bằng chứng khảo sát
- Repository: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai
- Branch Work 32: work/32-ci-cd-room-hop-python-no-docker
- Compare main...Work 32: 12 commits ahead, 0 behind; các thay đổi là 12 tài liệu Work 32.
- Branch HEAD được quan sát qua compare; merge base/main SHA: cc3100c835ad87ac9670a2ba38dc2c2dfae63755.
- requirements.txt SHA: 59e0a4c07842154d82784eff85a9b412c6b33263; dependencies khai báo pyyaml, pytest, python-dotenv, groq.
- pytest.ini SHA: b48b6676b85e30970e00a04a58fad3277be8c3e2; pythonpath=.; mặc định loại tests/legacy khỏi collection.
- ROOM-2026-001-BASELINE-FROZEN-v0.2.1.md SHA: c5014f27edfa3bf79dd5250c3a2a818a22462405; ghi baseline lịch sử 104 passed và yêu cầu patch mới phải chạy pytest -q.
- pytest_output.txt SHA: 076d05c4cf541ce3f79263dd1ae4b281616b9e2f; log lưu sẵn thể hiện 35 passed trong 2.17s trên một đường dẫn Windows cũ. Đây là historical artifact, không phải test run hiện tại và không tương đương baseline 104.
- Git tree recursive trên nhánh Work 32 không liệt kê .github/workflows; API đọc thư mục workflow trả NOT_FOUND. Đây là bằng chứng không có workflow ở đường dẫn đã kiểm tra trên nhánh, không suy rộng sang các ref khác.
- Các workflow run gần nhất quan sát được thuộc Work 28, không phải Work 32; không có bằng chứng run CI Work 32 trong tập 100 run trả về.

### 3. Đánh giá độc lập
- Thiết kế CI: PARTIAL / READY FOR IMPLEMENTATION CANDIDATE.
- Baseline tests hiện hành: BLOCKED — chưa chạy trực tiếp trên SHA Work 32.
- CI Work 32 execution: NOT RUN / NO EVIDENCE.
- Sandbox write: các tệp thiết kế đã được ghi; sandbox_read trả rỗng trước đó nên không dùng read-back làm điều kiện dừng. Dùng nguồn GitHub, SHA, sandbox_list và kết quả write làm bằng chứng hiện có; không tuyên bố nội dung Sandbox đã được đọc lại.
- Acceptance/closure: NOT PASS / NOT CLOSED.

### 4. Quyết định kỹ thuật
Cho phép chuẩn bị implementation candidate trong Sandbox để Qcoder triển khai/review: workflow validation-only, Python runner, không Docker, không deploy, không secrets, không auto-merge. Phải có manual workflow_dispatch và pull_request/push scope giới hạn rõ. Không kích hoạt CI trên GitHub, commit/push/merge hoặc deploy khi chưa có patch + baseline/test evidence được review.

### 5. Chữ ký
Ka — CSA / Independent Reviewer
Ngày giờ: 2026-10-21, Asia/Ho_Chi_Minh (UTC+07:00)


## W32-DECISION-20261103-01 — P1 — Quyết định kiến trúc CI/CD

- Người quyết định: Ka — CSA / phụ trách kiến trúc theo ủy quyền trực tiếp của Vinh.
- Thời điểm: 2026-11-03 08:43 UTC+07:00.
- Quyết định: CI-first trên GitHub Actions, Python 3.12, runner hosted, quyền contents:read; CD là pha riêng, chỉ sau exact-SHA review, protected approval, health check và rollback đã thử; Docker không bắt buộc, chỉ xem xét như lớp đóng gói VPS tùy chọn sau khảo sát runtime.
- Không merge/rebase/force-push nhánh Work 32 cũ vì compare với main là diverged (12 ahead / 530 behind); giữ nhánh cũ làm lịch sử; nhánh triển khai mới phải bắt đầu từ main SHA được xác minh lại.
- Ranh giới hiện tại: không bật workflow, không commit/push/merge, không deploy, không truy cập secrets hoặc live services. CI workflow draft chỉ lưu trong Sandbox.
- Bằng chứng chi tiết: `03_ARCHITECTURE/W32-ADR-001-ARCHITECTURE-DECISION.md`; workflow draft: `04_CODE/ci-validation.yml.draft`.
- Trạng thái: DECISION / CI DRAFT NOT ACTIVATED / CURRENT BASELINE NOT RUN / CD NOT RUN.


## W32-DECISION-20261103-02 — P1 — Nhánh triển khai sạch

- Người quyết định/thực hiện: Ka — CSA / architecture.
- Thời điểm: 2026-11-03 08:43 UTC+07:00.
- Tạo nhánh GitHub `work/32-ci-cd-python-ci-v2` từ main SHA `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- Xác minh compare main...nhánh mới: `identical`, ahead=0, behind=0; merge-base bằng chính SHA nguồn — PASS.
- Nhánh cũ `work/32-ci-cd-room-hop-python-no-docker` được giữ nguyên, không merge/rebase/cherry-pick.
- Chưa có commit code, chưa đưa workflow draft lên GitHub, chưa bật Actions, chưa deploy.


## W32-DECISION-20261103-03 — P1 — Kết luận CI pilot thực tế

- Người quyết định: Ka — CSA / architecture được Vinh ủy quyền.
- Ngày giờ: 2026-11-03 09:20 UTC+07:00.
- Quyết định: công nhận GitHub Actions workflow hoạt động và runner/dependency/compile đều PASS; KHÔNG công nhận CI gate PASS do regression suite còn 1 lỗi.
- Bằng chứng: run `41565286414`, SHA `b7e683dc5fa5ee165c9c12d9a7ee64a34a115550`, 201 passed / 1 failed; artifact `13197759403`.
- Lỗi: `test_t8_existing_mcp_tools_no_regression` kỳ vọng join_meeting/start_meeting nhưng MCP server hiện tại chỉ expose 4 tools. Giữ nguyên test làm gate; không chỉnh Core/MCP để hợp thức hóa CI.
- Phạm vi không triển khai: không merge vào main, không bật branch protection trong lượt này, không cấu hình SSH/secrets, không CD/VPS.
- Trạng thái: CI WORKFLOW OPERATIONAL / CI GATE BLOCKED / CD NOT STARTED / NOT RELEASED.
- Chi tiết: `06_EVIDENCE/W32-EVIDENCE-001-CI-PILOT-RESULTS-20261103.md`.
