# WORK 28 — LỆNH ĐIỀU PHỐI E2E-AUTOMATIC
Ngày: 2026-10-15
Giờ lập: 11:53 (UTC+07:00, Việt Nam)
Người lập: Ka — CSA / Independent Reviewer & Work 28 Coordinator
Thẩm quyền cuối cùng: Vinh — Project Owner / Final Authority
Trạng thái chung: ACTIVE / NOT LOCKED; live E2E BLOCKED; python_run NO-GO.

## Ka — CSA / Work 28 Coordinator
1. Tiếp tục audit source-first; không tuyên bố test PASS khi chưa có runner log.
2. Ưu tiên kế tiếp: lấy raw MCP tools/list từ listener thực tế :8020 và ràng buộc với PID, executable, source revision, runtime config. Nếu MCP không cung cấp được, ghi BLOCKED và phát lệnh PowerShell kiểm chứng tại PC.
3. Sau khi runner được phê duyệt: chạy từ root Work 28 `python -m unittest discover -s 05_TEST -t . -v`; lưu stdout/stderr, exit code, Python version, source SHA, tests/failures/errors/skipped, run ID và evidence readback.
4. Không bật/đăng ký `python_run`; không sửa registry; không ghi PC/GitHub; không sync/merge/release.

## Xu — CEO / Lead Architect; điều phối Work 101
1. Đọc và xác nhận dependency handoff `ROOM-HOP-DUAL-WORKSPACE/06_EVIDENCE/KA_WORK28_DEPENDENCY_HANDOFF_20261015.md`.
2. Chốt seam hiện hữu: Core :8000 là authority; MCP :8020 là adapter; chỉ dùng runtime W12/W13 / Work 27 đã phê duyệt. Không tạo Core/bridge/runtime thứ hai.
3. Giữ Work101 read-only + DRY_RUN; `SYNC_TARGET=UNBOUND`; không ghi đích, merge hoặc release.
4. Phản hồi meeting bằng evidence path/commit hoặc BLOCKED + lý do. Đọc handoff không đồng nghĩa xác nhận triển khai.

## Cla — CTO / Security Reviewer độc lập
1. Review boundary Core → MCP → runtime bằng bằng chứng thực thi.
2. Kiểm tra negative cases: forged PASS; thiếu/thay evidence; snapshot hash sai trước khi process tạo; replay/idempotency key reuse; giả principal; cross-Work read/cancel; caller spoof operation_kind/authorized.
3. Xác nhận Core-derived principal/WorkContext, server-side authorization, authenticated transport, OS isolation/process-tree cleanup, resource/network limits, protected immutable evidence và authorized readback.
4. Trả từng mục PASS/BLOCKED kèm path, command, log, exit code, SHA. Không tự cấp GO cho đăng ký tool.

## Go — Independent E2E Acceptance
1. Chỉ sau khi Ka cung cấp live tools/list + runner evidence và Cla cung cấp security result, chạy độc lập live E2E trên listener/runtime thật.
2. Chứng minh identity → WorkContext → read-only capability → digest/revision comparison → DRY_RUN plan → protected evidence write/readback; negative tests phải chứng minh không có write/sync ngoài phạm vi.
3. Ghi endpoint/process/source SHA, command, timestamp, log, exit code và evidence readback. Không dùng Ka's run thay bằng chứng độc lập.
4. Trả PASS chỉ khi toàn chuỗi được chứng minh; nếu thiếu bất kỳ thành phần nào, BLOCKED với blocker cụ thể.

## Vinh — Project Owner / Final Authority
Chỉ xem xét mở gate sau khi Ka có runner/registry evidence, Cla ký security review và Go xác nhận live E2E độc lập. Mọi đăng ký `python_run`, target binding, write/sync, merge/release phải có phê duyệt riêng, rõ phạm vi và digest đích.

## Gates
G0 live listener identity + raw tools/list ↔ PID/executable/source revision/config.
G1 canonical unit tests chạy trên runner được phê duyệt, log + exit code + readback.
G2 negative contract/adapter tests.
G3 Core-derived principal + WorkContext + authenticated transport.
G4 isolation, process cleanup, resource/network limits, runtime identity.
G5 immutable evidence + authorized readback.
G6 Cla security PASS + Go independent live E2E PASS.
G7 chỉ sau đó Vinh mới cân nhắc đăng ký tool và phê duyệt riêng mutation.

## Evidence hiện có lúc lập lệnh
- Work28 decision artifact và Work101 dependency handoff trước đó đã tạo/readback trong Sandbox.
- Proposal trước đó ACCEPTED là phản hồi task của Xu; không phải Cla/Go đã nhận hoặc hoàn tất.
- 11:53 +07: inbox Xu/Cla/Go/Ka không có pending task.
- Chưa có bằng chứng test runner đã chạy; chưa có live tools/list được ràng buộc với process PC.
- NO-GO: `python_run`, live registry changes, PC/GitHub writes, sync, merge, release.

## Báo cáo bắt buộc
Mỗi người trả lời trong meeting theo mẫu: TÊN — CHỨC DANH — ngày/giờ UTC+07 — DONE/BLOCKED — evidence path — command — exit code — SHA — blocker/next action.
