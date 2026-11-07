# KẾ HOẠCH TRIỂN KHAI SỔ ĐĂNG KÝ NĂNG LỰC AI / AI CAPABILITY REGISTRY IMPLEMENTATION PLAN
- **STT / Document ID:** DOC-087
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 87
- **Depends on / Phụ thuộc:** DOC-001; DOC-006; DOC-035; DOC-043; DOC-055; DOC-086
- **Status / Trạng thái:** PHASE 1 DATA CONTRACT CREATED — RUNTIME/API/UI NOT STARTED
- **Version / Phiên bản:** 1.0
- **Updated / Cập nhật:** 2026-11-07
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh

## 1. Mục tiêu
Triển khai bước đầu AI Model Capability Registry dưới dạng dữ liệu có cấu trúc, có schema kiểm soát và quy trình cập nhật có thể kiểm tra. Phase 1 không tạo database, API, UI, scheduler, model integration hoặc chi phí API.

## 2. Phạm vi Phase 1
Các hiện vật:
- `05_BUILD/04_CODE/ai_capability_registry/README.md`: hướng dẫn vận hành và quy tắc ghi nhận.
- `05_BUILD/04_CODE/ai_capability_registry/schema/capability-registry.schema.json`: JSON Schema Draft 2020-12.
- `05_BUILD/04_CODE/ai_capability_registry/data/registry.json`: registry khởi tạo rỗng, chưa gán năng lực cho model nào.
- `05_BUILD/04_CODE/ai_capability_registry/templates/capability-record.template.json`: mẫu bản ghi chưa xác minh.

## 3. Trạng thái năng lực và quy tắc quyết định
- VERIFIED: có test case, phương pháp, model/provider/version cụ thể, kết quả, evidence có thể truy xuất và reviewer.
- PARTIAL: có bằng chứng nhưng chỉ đáp ứng một phần hoặc còn điều kiện/giới hạn rõ ràng.
- UNVERIFIED: chưa chạy test hoặc chưa đủ evidence; không được dùng làm căn cứ tự động phân công.
- UNSUPPORTED: đã kiểm tra hợp lệ và xác định không hỗ trợ tác vụ trong điều kiện đã nêu.
- STALE: trạng thái freshness của hồ sơ; bằng chứng/model/runtime đã cũ. STALE là cờ freshness riêng, không thay thế capability_status.
- UNKNOWN / NOT RUN không phải PASS. Không tự nâng trạng thái dựa trên mô tả nhà cung cấp hoặc tên model.

## 4. Quy trình cập nhật bản ghi
1. Tạo capability_id ổn định và mô tả một tác vụ có thể kiểm thử.
2. Xác định modality input/output, provider, model_id, model_version, deployment và tool/endpoint.
3. Định nghĩa test case, tiêu chí đạt, tập dữ liệu và giới hạn bảo mật/quyền riêng tư.
4. Chạy test trong môi trường được phép; lưu kết quả và evidence URI/hash.
5. Reviewer độc lập kiểm tra evidence và quyết định capability_status.
6. Cập nhật registry; ghi người sửa, thời gian, nguồn và ngày review kế tiếp.
7. Khi model/version/API thay đổi hoặc evidence hết hiệu lực, đánh dấu freshness STALE và yêu cầu test lại.

## 5. Quy tắc dữ liệu và an toàn
- Không lưu API key, token, mật khẩu, cookie, dữ liệu cá nhân nhạy cảm hoặc payload bí mật trong registry.
- Endpoint chỉ lưu tên/URI đã được phép công khai nội bộ; không lưu credential.
- Chi phí/latency chỉ ghi khi đã đo; nêu đơn vị, môi trường, thời điểm và phương pháp.
- Evidence phải là nguồn có thể truy xuất; không dùng câu trả lời tự xác nhận của chính model làm bằng chứng duy nhất.
- Không cấp quyền tool, identity, network action hay execution chỉ từ registry.
- Registry là nguồn tham khảo năng lực; Core/permission/policy vẫn là nguồn có thẩm quyền cho quyết định thực thi.

## 6. Kiểm thử Phase 1
| ID | Kiểm tra | Kỳ vọng |
|---|---|---|
| REG-001 | Parse schema JSON | JSON hợp lệ |
| REG-002 | Parse registry JSON | JSON hợp lệ |
| REG-003 | Kiểm tra schema version và registry ID | Đúng metadata bắt buộc |
| REG-004 | Kiểm tra registry khởi tạo | entries là mảng rỗng; không có capability giả lập |
| REG-005 | Kiểm tra template | trạng thái UNVERIFIED; trường chưa biết là UNKNOWN/NOT RUN |
| REG-006 | Kiểm tra status vocabulary | Chỉ chấp nhận enum đã quy định |
| REG-007 | Kiểm tra secret policy | Không có token/key/credential mẫu |
| REG-008 | GitHub readback | Nội dung đọc lại khớp các file vừa tạo |
| REG-009 | Document governance | DOC-087 được đăng ký; DOC-035 ghi đủ lệnh/phương pháp/evidence/kết quả/bước tiếp |
| REG-010 | Runtime/schema validator | BLOCKED/NOT RUN trong Phase 1 nếu chưa có validator được phê duyệt; không tuyên bố full schema validation |

## 7. Điều kiện mở rộng Phase 2
Chỉ đề xuất database/API/UI sau khi:
- Phase 1 data contract và readback đạt;
- xác định owner dữ liệu, versioning, audit trail và nguồn dữ liệu;
- có kiến trúc Core integration và authorization review;
- có kế hoạch test độc lập và chi phí/hạ tầng;
- có quyết định phê duyệt riêng nếu phát sinh database/API/UI, chi phí định kỳ, credential hoặc tích hợp model/provider.

## 8. Trạng thái thực hiện
Phase 1 tạo schema, registry rỗng, template và README. Không tạo model capability records vì chưa có evidence test model/version cụ thể. Không chạy benchmark model. Không có API/UI/database/runtime integration. Trạng thái hoàn tất Phase 1 chỉ được xác nhận sau khi JSON parse, kiểm tra cấu trúc, policy và GitHub readback có bằng chứng trong DOC-035.
