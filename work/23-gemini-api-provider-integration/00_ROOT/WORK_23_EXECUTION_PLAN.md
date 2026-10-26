# WORK 23 — AUTONOMOUS E2E PRODUCT DELIVERY
Ngày cập nhật: 2026-10-10
Trạng thái: ACTIVE / CHƯA TRIỂN KHAI / CHƯA NGHIỆM THU
Chủ trì xây dựng: Kha (Gemini)
Điều phối kiến trúc và kiểm chứng: Xu
Chủ sở hữu sản phẩm: Vinh

## 1. Mục tiêu sản phẩm
Xây Gemini API Provider Adapter để ROOM-HOP và các Agent được phép sử dụng Gemini qua đúng luồng hệ thống, có kiểm soát dữ liệu, bảo mật khóa, usage/quota/chi phí, lỗi, audit và bằng chứng vận hành.

Đây là nhiệm vụ xây sản phẩm theo một chu trình Autonomous E2E (End-to-End — xuyên suốt tự động), không phải dự án mà người dùng phải theo dõi hay phê duyệt từng giai đoạn.

## 2. Quy tắc vận hành thống nhất
- Một yêu cầu triển khai -> một chu trình tự động từ khảo sát đến sản phẩm chạy thử -> một báo cáo cuối cùng.
- Kha tự thực hiện các bước nội bộ: đọc yêu cầu, khảo sát nguồn, lập kế hoạch, thiết kế, triển khai, chạy test, khởi động dependency cần thiết trong phạm vi được cấp, chạy E2E, thu thập evidence, phân loại lỗi, sửa lỗi, chạy lại regression/E2E và đóng gói kết quả.
- Các kiểm tra kiến trúc, bảo mật, contract và chất lượng vẫn bắt buộc nhưng là automated/internal gates trong cùng chu trình, không phải các giai đoạn chờ người dùng xác nhận.
- Không dừng để hỏi Vinh các quyết định kỹ thuật thông thường thuộc phạm vi đã thống nhất. Chọn phương án an toàn, tương thích ngược và ít thay đổi nhất; ghi lại lý do.
- Khi lỗi nằm trong phạm vi, tự sửa và chạy lại. Gom các lỗi có thể khắc phục trong một vòng tự chủ; không bắt Vinh chạy terminal từng lệnh nhỏ nếu có thể tự động hóa trong môi trường được cấp.
- Không tuyên bố PASS nếu thiếu bằng chứng runtime có thể kiểm tra lại.
- Nếu không thể truy cập nguồn/host/credential cần thiết, không giả vờ đã chạy. Hoàn thành tối đa phần độc lập có thể thực hiện, ghi BLOCKED cho phần phụ thuộc, nêu rõ đúng một gói thông tin cần được cấp để tiếp tục.
- Chỉ dừng toàn chu trình vì ranh giới an toàn/thẩm quyền: cần credential hoặc quyền truy cập chưa được cấp; cần phát sinh chi phí/billing ngoài giới hạn được phép; định gửi dữ liệu khách hàng/thật chưa được phê duyệt; cần sửa kiến trúc hoặc Work ngoài scope; hoặc có nguy cơ gây tác động không thể đảo ngược. Không cần xin duyệt cho các bước code/test nội bộ an toàn.
- Không tự ý tạo chi phí, đổi billing, nâng quota, dùng dữ liệu thật hoặc deploy production khi chưa có thẩm quyền.
- Sandbox/branch là nơi xây dựng; không sửa MAIN_SOURCE trực tiếp. Chỉ tích hợp sang nguồn chính qua quy trình được cho phép.

## 3. Ranh giới kiến trúc bắt buộc
Luồng gọi mô hình:
Agent/AI -> MCP :8020 -> Core :8000 -> Gemini Provider Adapter -> Gemini API.

Luồng lưu tài liệu (nếu yêu cầu sản phẩm có chức năng này):
Gemini response -> Core/MCP-controlled workflow -> Work 05 Google Workspace Docs/Drive Adapter -> Google Docs/Drive.

- Core :8000 tiếp tục là single source of truth.
- Không tạo Core 2, không để agent/frontend gọi Gemini trực tiếp để bỏ qua policy, audit hoặc metering.
- Work 05 giữ trách nhiệm Google Docs/Drive qua OAuth; Work 23 giữ trách nhiệm Gemini API qua provider credential. Không trộn hai adapter hoặc credential.
- Không tạo abstraction/provider client trùng lặp nếu repository đã có contract phù hợp.
- Nếu khảo sát thấy hiện trạng khác sơ đồ này, ghi evidence, chọn giải pháp tương thích trong phạm vi nếu có thể; chỉ dừng khi cần thay đổi ngoài thẩm quyền. Không lặng lẽ đổi kiến trúc nền.

## 4. Autonomous E2E — chu trình duy nhất
Kha phải tự chạy toàn bộ chu trình dưới đây như một pipeline, không chờ người dùng duyệt từng bước:

1. **Discover & Baseline:** đọc Work 23/Work 99 và repo/branch thực tế được cấp; xác định commit/version, cấu trúc, contract MCP/Core/provider, test baseline và dependency.
2. **Plan internally:** xác định scope/diff, luồng dữ liệu, rủi ro, test matrix, secret/config strategy, timeout/retry/error contract, usage/quota/cost controls. Ghi lại thiết kế nhưng không gửi yêu cầu duyệt theo từng phase.
3. **Implement:** code trong Work 23 Sandbox/branch được cấp; tái sử dụng interface hiện có; giữ thay đổi nhỏ, tương thích ngược, có thể rollback.
4. **Automated quality/security gates:** chạy lint/type/compile phù hợp repo, unit, contract, integration, regression, policy gate, secret leakage scan, dependency/security checks khả dụng. Gate nào không áp dụng phải nêu lý do.
5. **Start & verify runtime:** tự khởi động các service/dependency được phép, kiểm tra health/readiness/ports và ghi log; không coi service giả hoặc stub là runtime thật.
6. **Run end-to-end:** chạy từ entry point được hỗ trợ qua MCP :8020 -> Core :8000 -> adapter -> Gemini API khi có credential/quyền cho phép. Nếu thiếu real credential, chạy mock E2E tách biệt và đánh dấu real provider NOT VERIFIED/BLOCKED.
7. **Collect evidence:** lưu run ID, timestamp, source hash, commands/scripts, exit codes, pass/fail/skip counts, logs đã redacted, correlation IDs, HTTP/request outcomes, usage/quota/chi phí nếu có. Không lưu secret hay payload nhạy cảm.
8. **Diagnose & repair:** gom lỗi theo code/contract/config/auth/quota/network/runtime/architecture; tự sửa lỗi trong scope và không phá vỡ kiến trúc.
9. **Retest loop:** sau mỗi sửa đổi chạy test liên quan, sau đó chạy full regression và E2E lại. Lặp trong giới hạn thực tế của môi trường; nếu phụ thuộc ngoài quyền hạn, ghi BLOCKED và tiếp tục những kiểm tra độc lập.
10. **Package & final report:** đóng gói artifact, hướng dẫn chạy/test/rotate key/rollback, ma trận kiểm thử và evidence; đối chiếu Work 99. Trả một báo cáo tổng hợp cuối cùng với DONE/PASS/FAIL/BLOCKED/DECISION, không đẩy nhật ký từng bước cho người dùng trừ khi được yêu cầu.

## 5. Tiêu chuẩn sản phẩm
### Provider contract
- Request xác định caller/agent, mục đích, model được phép, input, tham số generation, data classification và correlation ID.
- Response chuẩn hóa output, provider/model, finish status, latency, correlation ID và usage metadata khi provider cung cấp.
- Chuẩn hóa lỗi: config/auth, policy denied, quota/rate limit, timeout, provider unavailable, invalid request, safety refusal và malformed response.
- Timeout và retry có giới hạn/backoff; không retry vô hạn hoặc retry mù lỗi không phục hồi.
- Model registry/config phải rõ ràng; không chọn model ngoài policy.

### Security & data policy
- API key chỉ ở server-side secret store hoặc cơ chế bảo vệ phù hợp môi trường; không nằm trong frontend, Git, prompt, logs, exception hoặc evidence.
- Mặc định dùng dữ liệu synthetic; chỉ gửi dữ liệu tối thiểu cần thiết.
- Policy không rõ hoặc không tải được thì fail closed.
- Không log prompt/response nhạy cảm mặc định; log actor/purpose/model/time/outcome/correlation ID và usage cần thiết.
- Không fallback tự động sang provider khác cho dữ liệu nhạy cảm nếu chưa có policy cho phép.
- Kiểm tra điều khoản hiện hành theo đúng dịch vụ, loại project và trạng thái billing; ghi ngày kiểm tra, không giả định điều khoản/retention.
- Tách mock tests khỏi real API tests.

### Usage, quota and cost
- Xử lý rate limit/quota/timeout với lỗi chuẩn hóa và retry có giới hạn.
- Theo dõi usage/latency và chi phí khi có dữ liệu đáng tin cậy; phân biệt số thực tế với ước tính.
- Có giới hạn lượt gọi, timeout và đường dừng. Không phát sinh chi phí ngoài thẩm quyền.
- Không khai báo real API PASS khi chỉ có mock.

## 6. Evidence contract — bằng chứng đầu ra bắt buộc
Mỗi chu trình cần có:
- Run ID, timestamp, source/commit hash, môi trường.
- Danh sách file thay đổi và diff summary.
- Commands/scripts đã chạy và exit code.
- Test matrix: expected/actual/status, pass/fail/skip counts.
- Runtime flow evidence: service health, request/correlation ID, kết quả qua từng boundary có thể quan sát.
- Logs đã redacted; secret scan result.
- Tách rõ MOCK E2E và REAL GEMINI API E2E.
- Usage/quota/cost thực tế, ước tính hoặc NOT AVAILABLE.
- Known limitations, residual risks, rollback instructions.
- Verdict cuối: PASS / FAIL / BLOCKED / PARTIAL; không dùng PASS chung nếu một hạng mục cốt lõi còn NOT VERIFIED.

Các tài liệu evidence nên nằm trong:
- 01_ORIGINAL/BASELINE_AND_SCOPE.md
- 03_ARCHITECTURE/CURRENT_VS_TARGET_FLOW.md
- 03_ARCHITECTURE/GEMINI_PROVIDER_CONTRACT.md
- 03_ARCHITECTURE/DATA_POLICY_AND_THREAT_MODEL.md
- 05_TEST/TEST_RESULTS.md
- 06_EVIDENCE/E2E_RESULT.md
- 06_EVIDENCE/FINAL_GATE_REPORT.md
- 07_RELEASE/OPERATIONS_AND_ROLLBACK.md
Có thể điều chỉnh tên/vị trí nếu repo có quy ước hiện hữu tốt hơn; cập nhật index tài liệu cho khớp.

## 7. Định nghĩa kết quả
- **PASS:** tất cả kiểm tra bắt buộc cho phạm vi đã tuyên bố đều có evidence đạt; real-provider PASS chỉ khi đã thực sự gọi API qua đường tích hợp được yêu cầu.
- **PARTIAL:** các phần độc lập đã hoàn thành nhưng một phần quan trọng chưa kiểm chứng; phải chỉ rõ.
- **FAIL:** đã chạy và phát hiện không đạt; kèm bằng chứng.
- **BLOCKED:** không thể tiếp tục phần cụ thể do thiếu quyền/credential/host/quota/decision hoặc dependency ngoài quyền kiểm soát.
- **NOT VERIFIED:** chưa có bằng chứng thực thi.
Không để compile/mock success che lấp real runtime failure.

## 8. Quyền tự chủ và điểm cần người quyết định
Kha được tự quyết các chi tiết kỹ thuật nội bộ, lựa chọn implementation tương thích, sửa lỗi trong scope, bổ sung test và chạy lại. Không cần yêu cầu Vinh xác nhận từng phase.

Chỉ yêu cầu quyết định khi:
1. Cần credential/quyền truy cập mà chưa được cấp.
2. Có chi phí/billing hoặc quota vượt giới hạn được cho phép.
3. Muốn gửi dữ liệu thật/nhạy cảm ra provider.
4. Cần sửa Core/MCP, Work 05/08 hoặc kiến trúc nền ngoài scope.
5. Cần deploy production, thay đổi có tác động không thể đảo ngược, hoặc chốt trạng thái COMPLETED/LOCKED.

Khi cần quyết định, tiếp tục hoàn thành phần độc lập an toàn và gửi một gói duy nhất: vấn đề, evidence, lựa chọn, chi phí/rủi ro, khuyến nghị và quyết định tối thiểu cần có.

## 9. Báo cáo cuối — hướng tới người dùng sản phẩm
Không gửi người dùng qua từng phase. Báo cáo tổng kết một lần:
- Sản phẩm/luồng nào đã chạy được.
- Cách khởi động và dùng.
- Kết quả E2E và bằng chứng.
- Test pass/fail/skip.
- Bảo mật, quota/chi phí và giới hạn đã biết.
- Việc nào còn BLOCKED/NOT VERIFIED và đúng nguyên nhân.
- Artifact/đường dẫn evidence và hướng rollback.
- Quyết định còn cần chủ sở hữu (nếu có).

## 10. Điều kiện hoàn tất Work
Work 23 chỉ được đề xuất COMPLETED khi scope sản phẩm đã đạt tiêu chí nghiệm thu, evidence đầy đủ, tài liệu vận hành/rollback sẵn sàng, Work 99 được cập nhật đúng thực tế và Xu review. Vinh giữ quyền phê duyệt trạng thái cuối và production release. Không tự đánh dấu LOCKED.

## 11. Tài liệu chính thức
- https://ai.google.dev/gemini-api/terms
- https://ai.google.dev/gemini-api/docs/usage-policies
- https://ai.google.dev/gemini-api/docs/api-key
- https://ai.google.dev/gemini-api/docs/pricing
Rà soát lại trước khi dùng API thật; ghi rõ thời điểm và điều khoản áp dụng.

## 12. Trạng thái khởi tạo
Tài liệu này thống nhất cách vận hành E2E tự động, không phải bằng chứng sản phẩm đã được triển khai. Work 23 vẫn ACTIVE. Chưa có implementation hoặc real API E2E nào được tuyên bố PASS.
