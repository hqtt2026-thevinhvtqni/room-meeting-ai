# DOC-060 — Đề xuất chuẩn hóa mã cổng / Gate Namespace and Identifier Separation
- **Document ID:** DOC-060
- **Priority:** P0
- **Status:** PROPOSAL ONLY — NOT APPROVED / NOT IMPLEMENTED
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Version:** 1.0-draft
- **Date:** 2026-10-31

## 1. Vấn đề
DOC-004 dùng G0–G9 cho cổng thoát phase của vòng đời Work. DOC-057 dùng G0–G5 cho cổng xác minh participant/assignment. DOC-054 dùng G0–G4 cho cổng tích hợp kỹ thuật. Cùng một mã ngắn đang chỉ ba điều kiện khác nhau, tạo nguy cơ hiểu sai trạng thái trong API, event, evidence, log và Dashboard.

## 2. Đề xuất định danh
- **Lifecycle Gate:** LC-G0 đến LC-G9 — định nghĩa tại DOC-004.
- **Work Entry Gate:** WE-G0 đến WE-G5 — định nghĩa tại DOC-057.
- **Integration Gate:** INT-G0 đến INT-G4 — định nghĩa tại DOC-054.

Tên namespace là định danh máy đọc được; tên tiếng Việt tương ứng lần lượt là Cổng vòng đời, Cổng đầu vào người tham gia và Cổng tích hợp.

## 3. Tương thích ngược
1. Giữ nguyên thứ tự, tiêu chí, evidence tối thiểu và authority hiện tại; đề xuất này chỉ chuẩn hóa định danh.
2. Mã G0… chỉ được hiểu trong phạm vi tài liệu đã định nghĩa nó; không dùng mã trần trong record/API/event/evidence mới.
3. Bản ghi lịch sử giữ nguyên mã gốc, không sửa ngược hoặc diễn giải lại.
4. Mọi alias cũ phải được ánh xạ tường minh trong migration mapping.
5. Không tự động chuyển trạng thái PASS/FAIL/WAIVED trong quá trình đổi mã.

## 4. Phạm vi tài liệu phải cập nhật sau khi được duyệt
- DOC-004: LC-G0…LC-G9.
- DOC-057: WE-G0…WE-G5.
- DOC-054: INT-G0…INT-G4.
- DOC-001: đổi pointer G0/G1 hiện tại thành LC-G0/LC-G1.
- DOC-042, DOC-044, DOC-045…DOC-053: rà soát và thay tham chiếu đúng namespace.
- DOC-005: không đổi Gate state enum; bổ sung ràng buộc định danh gate nếu cần.
- API/schema/event/evidence/Dashboard/test: dùng namespace đầy đủ và giữ alias mapping cho dữ liệu cũ.

## 5. Kế hoạch migration
1. Vinh phê duyệt hoặc yêu cầu chỉnh sửa đề xuất.
2. Lập inventory toàn bộ tham chiếu G0… trong tài liệu, source, test, schema và dữ liệu.
3. Chốt mapping cũ → mới theo từng nguồn; không suy luận chỉ dựa vào số G.
4. Cập nhật tài liệu chuẩn và Document Register.
5. Thêm validator ngăn mã gate trần trong record mới; cho phép đọc dữ liệu lịch sử qua alias mapping.
6. Chạy link check, schema validation, unit/contract tests, migration tests và Dashboard regression.
7. Đối soát Sandbox/GitHub exact readback; ghi evidence và DOC-035.
8. Chỉ bật enforcement sau khi QE độc lập xác nhận.

## 6. Ngoài phạm vi
Không thay đổi tiêu chí gate, authority, state machine, lifecycle, policy bảo mật, quyền thực thi, release condition hoặc trạng thái hiện tại của Work.

## 7. Quyết định cần có
Vinh quyết định APPROVE / REJECT / REVISE. Trước khi có quyết định, tài liệu hiện hành tiếp tục có hiệu lực; các mã LC-G*, WE-G*, INT-G* chỉ là đề xuất, không được dùng để cấp quyền hoặc đánh giá PASS.
