# WORK 28 — PHÂN CÔNG CỤ THỂ
Ngày: 2026-10-15
Work ID: 28 — MCP-8020-TOOLING-PLATFORM

## Trạng thái ràng buộc
- SANDBOX-ONLY POLICY: ACTIVE
- MCP CONNECTION: CONNECTED
- SOURCE SNAPSHOT: NOT IMPORTED
- E2E-AUTOMATIC: BLOCKED
- PC DEVELOPMENT/TRANSFER: PROHIBITED
- WORK 28: ACTIVE / NOT LOCKED
- RELEASE: NO-GO

## 1. Ka — CSA / Điều phối và kiểm soát bằng chứng
Nhiệm vụ:
1. Duy trì source-audit checklist và ma trận E2E-Automatic trong Sandbox.
2. Đánh dấu từng gate PASS/BLOCKED/NOT RUN; không chuyển kết quả contract test thành bằng chứng runtime.
3. Đối chiếu báo cáo Nu/Go/Cla; cập nhật nhật ký và trạng thái.
4. Không tạo bản thay thế cho MCP/Core canonical source.
Điều kiện hoàn thành: artefact đọc lại được trong Work 28, có bằng chứng và giới hạn rõ ràng.

## 2. Nu — Kỹ thuật / chuẩn bị nguồn và đường chuyển
Nhiệm vụ:
1. Review tĩnh candidate `04_CODE/pc_readonly_source_collector.py`; KHÔNG chạy trên PC.
2. Review `04_CODE/source_snapshot_contract.py` và `05_TEST/test_source_snapshot_contract.py`.
3. Đánh giá allowlist, secret exclusion, symlink/reparse point, TOCTOU, giới hạn file/kích thước, manifest, archive determinism, output path guard.
4. Đề xuất một đường chuyển source được cho phép và có thể kiểm chứng; nếu MCP không hỗ trợ upload/import thì ghi rõ BLOCKED, không giả lập thành công.
Bằng chứng cần nộp: báo cáo review, các finding theo mức độ, đề xuất sửa trong Sandbox, và danh sách kiểm tra trước khi xin phép hành động trên PC.
Ranh giới: không chạy collector, không đọc/ghi sửa PC source, không tạo ZIP trên PC, không restart service, không đổi live registry khi chưa được duyệt.

## 3. Go — Kiểm thử / khả năng tái lập độc lập
Nhiệm vụ:
1. Review contract v1.3.0, snapshot contract và test suite hiện có.
2. Phân loại mỗi test: đã chạy có log, mới đọc mã, hoặc chưa chạy.
3. Nếu có thể chạy trong môi trường Sandbox được cấp phép, chạy isolated tests và lưu lệnh, phiên bản Python, stdout/stderr, exit code, hash artefact.
4. Kiểm tra test âm: path traversal, allowlist bypass, malformed manifest/hash, limit boundary, dirty/untracked source, secret/runtime exclusion.
Bằng chứng cần nộp: báo cáo tái lập được và kết luận chỉ cho đúng artefact/môi trường đã kiểm tra.
Ranh giới: không gọi test contract là E2E MCP/Core; không sửa live PC.

## 4. Cla — Security reviewer độc lập
Nhiệm vụ:
1. Review trusted principal/authentication/authorization boundary; phân biệt caller claim với principal đã xác thực.
2. Review Sandbox handlers/service, path containment, resource limits, error leakage và nguy cơ thực thi code.
3. Xem xét các finding lịch sử của security review nhưng xác minh lại trên đúng revision khi canonical source có mặt; không giả định finding đã được sửa hoặc còn nguyên.
4. Đặt gate bảo mật trước khi bắt đầu E2E.
Bằng chứng cần nộp: security review với PASS/BLOCKED, severity, exploitability assumptions, bằng chứng cụ thể và điều kiện đóng từng finding.
Ranh giới: không tự duyệt phần do mình trực tiếp sửa; không thử trên PC/live service nếu chưa có phê duyệt.

## 5. Vinh — Final authority
Nhiệm vụ:
1. Quyết định có cho phép thu thập snapshot chỉ đọc trên PC hay không sau khi nhận review của Nu/Go/Cla.
2. Quyết định đường chuyển/import khi có đề xuất và kiểm soát hash.
3. Chỉ duyệt chuyển sang PC sau independent review, E2E evidence và quyết định rõ ràng của Vinh.

## Thứ tự phụ thuộc
A. Nu review collector + snapshot contract (static only).
B. Go review/test contract và xác định bằng chứng tái lập.
C. Cla review security gates, nêu điều kiện tối thiểu.
D. Ka tổng hợp findings, chọn blocker và cập nhật journal.
E. Chỉ sau các review mới trình Vinh xin phép thực hiện source collection/transfer.
F. Khi source snapshot được nhập và hash xác minh: mới audit canonical source, chốt runner, rồi bắt đầu E2E-Automatic.

## Trạng thái giao việc
Đây là phân công được ghi vào Work 28 Sandbox. Việc ghi tài liệu KHÔNG chứng minh agent đã nhận nhiệm vụ. Chưa có task-dispatch/acknowledgement evidence; trạng thái Nu/Go/Cla: ASSIGNED IN WORK DOCUMENT / ACKNOWLEDGEMENT PENDING.
