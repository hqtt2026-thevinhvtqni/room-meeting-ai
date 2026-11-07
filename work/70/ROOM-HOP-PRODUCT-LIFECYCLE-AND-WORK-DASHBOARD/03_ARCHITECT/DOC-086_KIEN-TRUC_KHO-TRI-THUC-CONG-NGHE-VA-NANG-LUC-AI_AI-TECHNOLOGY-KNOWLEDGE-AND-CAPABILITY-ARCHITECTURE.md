# KIẾN TRÚC KHO TRI THỨC CÔNG NGHỆ VÀ NĂNG LỰC AI / AI TECHNOLOGY KNOWLEDGE & CAPABILITY ARCHITECTURE
- **STT / Document ID:** DOC-086
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 86
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-006; DOC-028; DOC-033; DOC-043; DOC-055
- **Status / Trạng thái:** BASELINE APPROVED FOR KNOWLEDGE GOVERNANCE — IMPLEMENTATION NOT STARTED
- **Version / Phiên bản:** 1.0
- **Updated / Cập nhật:** 2026-11-07
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh

## 1. Mục đích
Thiết lập một kho tri thức dùng chung trong Work 70 để phân loại công nghệ AI, mô tả năng lực thực tế của mô hình/nhà cung cấp, liên kết công nghệ với các Work có thể ứng dụng và lưu bằng chứng kiểm chứng. Đây là lớp tri thức/quản trị dùng chung; không phải một Work sản phẩm mới, không phải danh sách quảng cáo mô hình và không tự cấp quyền thực thi cho AI.

## 2. Phạm vi và nguyên tắc
- Work 70 quản lý taxonomy (hệ phân loại), định nghĩa, quan hệ phụ thuộc, tiêu chí đánh giá, capability registry (sổ đăng ký năng lực) và quy tắc tham chiếu.
- Mỗi Work ứng dụng công nghệ tại phạm vi của chính Work đó; Work 70 không thay thế yêu cầu, kiến trúc, kế hoạch, kiểm thử hoặc quyền phê duyệt của Work sử dụng.
- Phân biệt **technology family** (họ công nghệ), **model/provider** (mô hình/nhà cung cấp), **capability** (năng lực đã xác minh), **tool/interface** (công cụ/giao diện), và **deployment/runtime** (cách triển khai/vận hành).
- Không suy luận một mô hình có năng lực chỉ từ tên thương hiệu, quảng cáo hoặc khả năng chung của một họ mô hình. Mọi capability phải có model/version, điều kiện sử dụng, ngày kiểm tra, phương pháp, kết quả và nguồn bằng chứng.
- Không đồng nhất khả năng hiểu ảnh với khả năng sinh ảnh; không đồng nhất LLM với Agent; không đồng nhất RAG với huấn luyện mô hình.
- Công nghệ thay đổi nhanh: bản ghi phải có ngày xác minh và trạng thái CURRENT / STALE / UNVERIFIED / DEPRECATED.

## 3. Bản đồ phân loại công nghệ AI
Các nhóm dưới đây là taxonomy thực dụng để điều hướng tri thức, không phải một cây phân cấp toán học tuyệt đối; các nhóm có thể giao nhau.

| Nhóm | Nội dung | Ví dụ năng lực / đầu ra |
|---|---|---|
| AI Fundamentals | Khái niệm AI, biểu diễn tri thức, suy luận, tìm kiếm và tối ưu | Phân loại vấn đề, chọn phương pháp |
| Machine Learning | Học từ dữ liệu; supervised, unsupervised, self-supervised và reinforcement learning | Dự đoán, phân cụm, chính sách hành động |
| Deep Learning | Mạng nơ-ron nhiều lớp và kiến trúc học biểu diễn | Nhận dạng, trích xuất đặc trưng |
| LLM | Mô hình ngôn ngữ lớn | Hiểu/sinh ngôn ngữ, tóm tắt, lập luận có giới hạn |
| Generative AI | Họ phương pháp tạo nội dung mới | Văn bản, hình ảnh, âm thanh, video, mã |
| Multimodal AI | Tiếp nhận, liên kết hoặc sinh nhiều phương thức dữ liệu | Văn bản + ảnh, âm thanh + văn bản, video |
| Diffusion Models | Mô hình sinh học quá trình khử nhiễu lặp từ phân phối nhiễu, thường có điều kiện | Text-to-image, image editing, một số tác vụ video/audio |
| RAG | Kết hợp truy xuất nguồn ngoài với mô hình sinh | Trả lời có căn cứ từ kho tài liệu/dữ liệu |
| AI Agents | Hệ thống dùng mô hình, trạng thái, công cụ và vòng lặp điều phối để hoàn thành mục tiêu | Lập kế hoạch, gọi công cụ, quan sát và bàn giao |
| Speech & Audio AI | Nhận dạng tiếng nói, tổng hợp tiếng nói, hiểu âm thanh | ASR, TTS, phân loại âm thanh |
| Computer Vision | Phân tích nội dung ảnh/video | Phát hiện vật thể, OCR, phân đoạn, theo dõi |
| Robotics & Embodied AI | AI tương tác với môi trường/vật lý | Điều khiển, định vị, thao tác |
| Evaluation, Safety & Governance | Đánh giá chất lượng, an toàn, quyền, provenance và giám sát | Benchmark, red-team, audit, policy |

### 3.1 Ghi chú kỹ thuật về Diffusion Model
Trong huấn luyện điển hình, quy trình thuận thêm nhiễu vào dữ liệu theo các mức thời gian; mạng học dự đoán nhiễu hoặc một đại lượng tương đương để tối ưu mục tiêu khử nhiễu. Đây thường là mục tiêu học self-supervised trên dữ liệu ảnh, có thể kết hợp điều kiện văn bản/nhãn. Khi suy luận, mô hình bắt đầu từ nhiễu (thường trong latent space ở các hệ latent diffusion) và lặp bước khử nhiễu theo điều kiện prompt để tạo mẫu. Vì vậy, mô tả “AI lọc nhiễu ảnh” chỉ là phép so sánh trực quan, không phải mô tả đầy đủ cơ chế toán học. Không khẳng định mọi hệ tạo ảnh đều dùng diffusion; có các họ phương pháp sinh khác.

## 4. Chuỗi quan hệ công nghệ → năng lực → mô hình → ứng dụng
Mọi đề xuất ứng dụng cần truy vết theo chuỗi:
**Vấn đề / nhiệm vụ → họ công nghệ phù hợp → capability cần có → model/provider + version → tool/API/runtime → Work sử dụng → test case → evidence → quyết định sử dụng.**

Một technology family không tự chứng minh một model cụ thể có capability. Một model có capability cũng không chứng minh môi trường triển khai có quyền, kết nối, hiệu năng, bảo mật hoặc chi phí phù hợp.

## 5. AI Model Capability Registry — trường dữ liệu tối thiểu
Mỗi bản ghi năng lực cần tối thiểu:
- capability_id; technology_family; task; modality_in / modality_out;
- provider; model_id; model_version; deployment_mode; tool_or_endpoint;
- capability_status (VERIFIED / PARTIAL / UNVERIFIED / UNSUPPORTED);
- verification_date; test_method; test_dataset_or_case; result; limitations;
- latency/cost/resource notes nếu đã đo; security/privacy constraints;
- evidence_uri; evidence_hash nếu có; reviewer; next_review_date.
Không điền giá trị suy đoán. Trường chưa biết phải để UNKNOWN / NOT VERIFIED, không tự chuyển thành VERIFIED.

## 6. Liên kết ứng dụng ban đầu trong hệ sinh thái ROOM-HOP
| Work | Vai trò liên kết ban đầu | Công nghệ có thể xem xét | Ranh giới |
|---|---|---|---|
| Work 70 | Quản trị taxonomy, capability registry, chuẩn đánh giá và liên kết | Toàn bộ nhóm trong DOC-086 | Không triển khai thay các Work |
| Work 75 — AI Network Guardian | Phân tích ảnh thiết bị/sơ đồ, truy vấn tri thức vận hành, hỗ trợ Agent | Computer Vision, Multimodal AI, RAG, AI Agents, LLM | Mọi hành động mạng phải qua quyền, policy và xác nhận theo thiết kế Work 75 |
| Work 76 — AI Trigger Engine | Kích hoạt theo sự kiện/điều kiện, định tuyến nhiệm vụ | AI Agents, LLM, event processing, policy engine | Trigger không đồng nghĩa được phép thực thi; kiểm tra identity/permission |
| Work 103 — ROOM-HOP RAG | Truy xuất và đánh giá tri thức | RAG, embeddings, reranking, evaluation | Không biến dữ liệu truy xuất thành sự thật nếu nguồn yếu hoặc lỗi thời |
| Work 26 — Multimodal Camera Voice Platform | Tích hợp camera/voice và xử lý đa phương thức | Multimodal AI, Computer Vision, Speech & Audio AI | Capability phụ thuộc model/provider/runtime thực tế |
| Work 29 — HQTT AI Video Studio | Tạo và xử lý nội dung hình ảnh/video | Generative AI, Diffusion/Video models, multimodal | Kiểm soát bản quyền, nguồn dữ liệu và quyền sử dụng đầu ra |

Các liên kết là định hướng khám phá, không phải phê duyệt thay đổi phạm vi hoặc tích hợp. Mỗi Work phải tự lập yêu cầu, kiến trúc, đánh giá rủi ro, kế hoạch và kiểm thử.

## 7. Quy trình bổ sung công nghệ hoặc năng lực mới
1. Intake: nêu vấn đề, người dùng, đầu ra và ràng buộc.
2. Classify: gán technology family và mô tả quan hệ với nhóm khác.
3. Identify: ghi đúng provider/model/version/tool/deployment.
4. Verify: thiết kế test đại diện, đo chất lượng, giới hạn, chi phí và an toàn.
5. Record: cập nhật registry kèm evidence URI/hash và ngày kiểm tra.
6. Map: liên kết Work sử dụng và chủ sở hữu.
7. Review: đặt lịch đánh giá lại; chuyển STALE khi model/API thay đổi hoặc evidence hết hiệu lực.

## 8. Tiêu chí chấp nhận cho kho tri thức
- Mỗi mục có định nghĩa, phạm vi, trường hợp sử dụng và giới hạn.
- Không trộn lẫn taxonomy với registry model/capability.
- Mọi capability VERIFIED có bằng chứng tái kiểm tra được.
- Các Work liên kết có owner và ranh giới trách nhiệm.
- Bản ghi không rõ nguồn hoặc chưa test phải mang trạng thái UNVERIFIED.
- Có kiểm tra liên kết, schema và lịch rà soát; không tuyên bố hoàn tất chỉ vì tạo tài liệu.

## 9. Trạng thái triển khai
- DOC-086 là kiến trúc baseline cho kho tri thức AI tại Work 70.
- Taxonomy và liên kết Work ban đầu đã được mô tả.
- Phase 1 AI Capability Registry đã có data contract tĩnh: DOC-087, JSON Schema, registry rỗng, record template và README trong `05_BUILD/04_CODE/ai_capability_registry/`.
- Chưa tạo database/API/UI; chưa tích hợp model/provider; chưa chạy benchmark; chưa xác minh capability của bất kỳ provider/model nào.
- Trạng thái: **KNOWLEDGE BASELINE + STATIC REGISTRY DATA CONTRACT CREATED — RUNTIME/API/UI NOT STARTED — NO MODEL CAPABILITY VERIFIED**.
