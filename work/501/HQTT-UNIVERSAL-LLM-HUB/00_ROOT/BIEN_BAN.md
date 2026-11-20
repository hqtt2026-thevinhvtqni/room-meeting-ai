# BIÊN BẢN THIẾT KẾ — WORK 501: HQTT UNIVERSAL LLM HUB
- Ngày: 2026-11-17 | Phiên bản: 0.1 | Trạng thái: PROVISIONAL — CHỜ PHẢN BIỆN ĐỘC LẬP
- Chủ trì/quyết định: Vinh | Điều phối: Xu / AI-01
## 1. Mục tiêu
Xây dựng trung tâm quản lý và khai thác nhiều provider/model cho ROOM-HOP; giữ nguyên danh tính, vai trò, quyền và phiên làm việc của Agent; định tuyến theo năng lực và chính sách; hỗ trợ Model Arena và truy vết đầy đủ.
## 2. Quyết định đã chốt
1. LOCAL FIRST: ưu tiên model chạy trên PC/server do ROOM-HOP kiểm soát; cloud miễn phí chỉ là dự phòng được kiểm soát.
2. GLOBAL CONTROL: Vinh có quyền điều khiển toàn cục; Xu điều phối; Agent chỉ được dùng provider/model đã được cấp quyền.
3. MODEL ARENA = YES: nhiều model có thể xử lý độc lập cùng nhiệm vụ, sau đó phản biện chéo và đánh giá theo rubric.
4. ZERO-COST FIRST: không tự ý phát sinh chi phí. Paid API, subscription, billing, payment setup, cloud resource có khả năng tính phí và mọi cam kết tài chính đều bị cấm nếu chưa có phê duyệt riêng của Vinh.
5. Hết quota hoặc lỗi dịch vụ miễn phí không được âm thầm fallback sang paid. Nếu không có lựa chọn miễn phí đủ điều kiện thì trả BLOCKED.
## 3. Phạm vi chức năng dự kiến
- Provider Registry và Model Registry: danh mục, model ID/version, capability, license, nguồn xác minh, trạng thái.
- Global Policy và Agent-Model Grant: allow/deny theo Agent, task, model, provider, loại dữ liệu và chi phí.
- Model Router: local-first, capability matching, health/capacity check, fallback có lý do.
- Provider Adapters: runtime local và API cloud qua hợp đồng chuẩn hóa.
- Quota/Cost Guard: paid mặc định DENY ở server-side; theo dõi quota và ngăn overage.
- Secret integration: dùng kho bí mật hiện hữu nếu có; không lưu khóa trong Git, tài liệu, source hoặc log.
- Call Log/Audit: model/provider/version, Agent/task/session ref, policy decision, thời gian, latency, usage nếu provider trả về, fallback và lỗi.
- Model Arena: independent first pass, sealed submissions, challenge round, rubric scoring, evidence provenance và báo cáo.
- Dashboard: trạng thái thật từ API chuẩn; dữ liệu chưa xác minh phải hiển thị NOT VERIFIED, không giả lập thành live.
## 4. Ranh giới hệ thống
ROOM-HOP Core là nguồn thẩm quyền cho identity/authorization. Gateway và Agent Runtime hiện hữu phải được khảo sát và ưu tiên tái sử dụng. LLM Hub không tạo Agent, không tự cấp quyền, không sở hữu session và không thay Core/Gateway/Runtime. Hợp đồng thực tế phải được đọc từ source trước khi chốt.
Work 23 là ứng viên tái sử dụng adapter Gemini, chưa chứng minh API/runtime readiness. Work 01/11/52/70/22/50 là nguồn cần đối soát để tránh trùng chức năng.
## 5. Routing và fallback
Thứ tự: (1) local model đủ năng lực và được phép; (2) free cloud model đã qua policy và privacy review; (3) paid chỉ khi Vinh phê duyệt riêng bằng thay đổi có kiểm soát. Không hạ cấp capability hoặc bảo mật âm thầm. Mọi fallback phải được ghi log.
## 6. Model Arena
- Đóng băng input, context, model version, tham số và rubric.
- Mỗi model chạy độc lập vòng đầu, không xem kết quả model khác.
- Lưu submission và provenance bất biến; phản biện chéo là vòng riêng.
- Chấm theo tiêu chí task-specific: factual accuracy, completeness, instruction compliance, safety, reasoning quality, latency, resource use và cost.
- Kết luận quan trọng cần kiểm chứng độc lập; đồng thuận đa số không phải chân lý.
- Nếu chỉ một model chạy được, ghi SINGLE-MODEL / NOT COMPARABLE; không gọi là Arena comparison.
- Không gửi dữ liệu nhạy cảm tới nhiều cloud provider nếu chưa được phê duyệt.
## 7. Bảo mật và chi phí
Paid provider mặc định DISABLED/DENY ở server-side. Secret chỉ tham chiếu qua secret store được duyệt. Không log prompt/response nhạy cảm mặc định; redaction, retention và access control phải được thiết kế. Local inference vẫn cần sandbox, egress control, resource limits và kiểm tra nguồn/license model.
## 8. Phản biện trước BUILD
Cla/AI-03: technical/runtime; Ka/AI-02: security/privacy/CSA; Go/AI-06: default QE/QA/testability under D70-026; Go/AI-06: local feasibility/cost; Vibe: adversarial architecture; Kha: provider/Gemini và Work 23; Qc: adapter feasibility không code; Gem: Agent operating model. Phân công là kế hoạch, chưa chứng minh đã dispatch hoặc reviewer đã nhận.
## 9. Vấn đề còn mở
Phần cứng thực tế; runtime local; lựa chọn LiteLLM hay adapter hiện hữu; Core/Gateway/Runtime contract; provider free-tier đủ điều kiện; secret store/database/log retention; Arena rubric/dataset; Dashboard ownership; data classification; deployment topology.
## 10. Điều kiện thoát thiết kế
Hoàn tất READ/TRACE các Work liên quan; kiểm kê phần cứng có bằng chứng; nhận hoặc ghi rõ unavailable cho phản biện; hoàn thiện sơ đồ, API contract, trust boundary, threat model, cost model, Arena rubric, test strategy và ADR; xử lý ý kiến trái chiều; Vinh phê duyệt rõ ràng trước BUILD.
## 11. Trạng thái xác nhận
Work Sandbox đã tạo. Chưa xác nhận GitHub/PC sync trước lần đồng bộ này. Chưa có reviewer response/ACK. Chưa chọn công nghệ cuối cùng. Chưa cài đặt, tải model, gọi API, tạo key, bật billing, triển khai hoặc chạy test. Không có PASS cho sản phẩm/runtime.