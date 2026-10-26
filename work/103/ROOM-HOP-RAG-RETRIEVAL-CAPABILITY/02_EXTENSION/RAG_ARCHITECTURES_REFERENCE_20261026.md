# TÀI LIỆU THAM KHẢO — 8 KIẾN TRÚC RAG
**Work:** 103 — ROOM-HOP-RAG-RETRIEVAL-CAPABILITY  
**Ngày ghi nhận:** 2026-10-26  
**Trạng thái:** REFERENCE ONLY — không tự động mở rộng phạm vi triển khai  
**Nguyên tắc:** Evidence First; Architecture Before Code; điều kiện cần và điều kiện đủ phải được xác định trước mỗi gate.

## 1. Mục đích
Tài liệu tổng hợp 8 hướng kiến trúc RAG được chia sẻ để làm tài liệu tham khảo cho Work 103. Đây không phải 8 cấp độ bắt buộc phải triển khai tuần tự. Chọn phương pháp dựa trên nhu cầu nghiệp vụ, kết quả đo lường, độ trễ, chi phí và khả năng bảo trì.

## 2. Tám kiến trúc

### 2.1 Naive RAG — RAG cơ bản
Truy xuất tài liệu liên quan, đưa các đoạn bằng chứng vào LLM để sinh câu trả lời. Dễ xây dựng và là baseline (đường cơ sở) phù hợp để đo chất lượng retrieval.

**Khi cân nhắc:** giai đoạn đầu, dữ liệu chủ yếu là văn bản và bài toán hỏi đáp đơn giản.  
**Rủi ro:** truy xuất sai hoặc thiếu tài liệu làm giảm chất lượng câu trả lời; cần xử lý rõ trường hợp không có bằng chứng.

### 2.2 Multimodal RAG — RAG đa phương thức
Truy xuất trên nhiều loại dữ liệu như văn bản, hình ảnh, bảng biểu và tài liệu hỗn hợp.

**Khi cân nhắc:** cần hỏi đáp trên PDF, ảnh, biểu đồ hoặc tài liệu đa phương thức.  
**Rủi ro:** tăng độ phức tạp của ingestion (nạp dữ liệu), biểu diễn dữ liệu, chỉ mục và đánh giá.

### 2.3 HyDE — Hypothetical Document Embeddings
LLM tạo văn bản/tài liệu giả định có liên quan đến câu hỏi; hệ thống embedding (mã hóa thành vector) văn bản giả định để tìm tài liệu thật gần về ngữ nghĩa.

**Khi cân nhắc:** truy vấn ngắn, mơ hồ hoặc truy xuất ngữ nghĩa chưa tốt theo kết quả đánh giá.  
**Rủi ro:** nội dung giả định có thể sai; chỉ dùng nó để hỗ trợ tìm kiếm, không được coi là bằng chứng thực tế.

### 2.4 Corrective RAG (CRAG) — RAG tự hiệu chỉnh
Đánh giá chất lượng hoặc mức độ phù hợp của kết quả truy xuất; khi không đủ tốt, có thể tìm kiếm bổ sung, thay đổi truy vấn hoặc dùng nguồn khác.

**Khi cân nhắc:** hệ thống cần phát hiện bằng chứng yếu và có quy trình phục hồi.  
**Rủi ro:** tăng độ trễ và chi phí; tiêu chí đánh giá phải kiểm thử được.

### 2.5 Graph RAG — RAG dựa trên đồ thị tri thức
Khai thác thực thể và quan hệ trong Knowledge Graph (đồ thị tri thức) để trả lời câu hỏi cần nối kết thông tin qua nhiều thực thể hoặc tài liệu.

**Khi cân nhắc:** câu hỏi về quan hệ, mạng lưới thực thể hoặc tổng hợp xuyên tài liệu.  
**Rủi ro:** xây dựng và cập nhật đồ thị tốn công; chất lượng phụ thuộc vào trích xuất thực thể/quan hệ.

### 2.6 Hybrid RAG — RAG kết hợp
Kết hợp các phương pháp truy xuất. Thường gặp nhất là hybrid search (tìm kiếm kết hợp) giữa lexical/keyword search (tìm kiếm từ khóa) và vector/semantic search (tìm kiếm vector/ngữ nghĩa); trong một số thiết kế có thể kết hợp thêm đồ thị tri thức.

**Lưu ý thuật ngữ:** Hybrid RAG không nhất thiết phải có cả Vector Database và Graph Database. Phải nêu rõ những phương pháp nào đang được kết hợp trong thiết kế cụ thể.

### 2.7 Adaptive RAG — RAG thích ứng
Định tuyến chiến lược theo loại hoặc độ phức tạp của câu hỏi: trả lời trực tiếp, truy xuất một lần hoặc truy xuất nhiều bước.

**Khi cân nhắc:** có nhiều nhóm câu hỏi và mỗi nhóm cần mức xử lý khác nhau.  
**Rủi ro:** bộ định tuyến phân loại sai có thể chọn chiến lược không phù hợp; cần đo tỷ lệ chọn đúng và tác động tới chất lượng.

### 2.8 Agentic RAG — RAG kết hợp AI Agent
AI Agent lập kế hoạch, gọi công cụ, truy xuất lặp lại và tổng hợp bằng chứng theo nhiều bước; có thể phối hợp với Memory (bộ nhớ), MCP (giao thức kết nối công cụ) hoặc các Agent chuyên biệt.

**Khi cân nhắc:** nhiệm vụ nhiều bước thực sự cần lập kế hoạch và gọi công cụ.  
**Rủi ro:** tăng độ trễ, chi phí, bề mặt lỗi và yêu cầu kiểm soát quyền. Agentic RAG là cách tổ chức workflow (quy trình), không đồng nghĩa phải xây một RAG Layer độc lập.

## 3. Phân biệt khái niệm
Các tên gọi trên không hoàn toàn cùng một trục phân loại:
- Naive RAG mô tả pipeline cơ bản.
- Multimodal RAG mô tả loại dữ liệu.
- HyDE và Corrective RAG mô tả kỹ thuật cải thiện truy xuất/đánh giá.
- Graph RAG mô tả cách khai thác quan hệ dữ liệu.
- Hybrid RAG mô tả kết hợp phương pháp truy xuất.
- Adaptive RAG mô tả cách chọn chiến lược.
- Agentic RAG mô tả quy trình có tác nhân lập kế hoạch và dùng công cụ.

Do đó, các kỹ thuật có thể được kết hợp khi có bằng chứng cho thấy sự kết hợp đó cải thiện kết quả.

## 4. Định hướng áp dụng cho Work 103
**Quyết định phạm vi:** ưu tiên Retrieval Capability cơ bản bên trong kiến trúc ROOM-HOP hiện có; không tạo Core thứ hai hoặc RAG Layer độc lập chỉ vì tài liệu tham khảo đề cập đến kiến trúc nâng cao.

Luồng kiến trúc mục tiêu:
1. AI/Agent gửi yêu cầu qua MCP hiện có.
2. Core là ranh giới kiểm soát và nguồn dữ liệu có thẩm quyền.
3. Retrieval Capability thực hiện tìm kiếm, lọc metadata, xếp hạng cơ bản và trả về nguồn/bằng chứng.
4. LLM sinh câu trả lời dựa trên bằng chứng; khi không đủ bằng chứng, phải nói rõ giới hạn thay vì bịa.

Vector Database, ChromaDB, Hybrid Search, Corrective RAG, Graph RAG, Adaptive RAG, Multimodal RAG hoặc Agentic RAG chỉ được thêm sau khi xác định được vấn đề cụ thể và có đánh giá chứng minh lợi ích.

## 5. Điều kiện cần và điều kiện đủ cho các bước nâng cấp
**Điều kiện cần trước khi mở rộng**
- Có tập câu hỏi chuẩn và dữ liệu kiểm thử đại diện.
- Có baseline và số đo retrieval/answer quality.
- Xác định được lỗi hiện tại mà phương pháp mới cần giải quyết.
- Xác định tác động dự kiến tới độ trễ, chi phí, quyền truy cập và bảo trì.

**Điều kiện đủ để chấp nhận nâng cấp**
- Kiểm thử so sánh trước/sau có thể lặp lại.
- Chất lượng cải thiện theo tiêu chí định trước hoặc có lợi ích nghiệp vụ được chứng minh.
- Không vi phạm ranh giới Core/MCP và quyền truy cập.
- Có báo cáo bằng chứng và kết quả kiểm thử; không tuyên bố PASS nếu chưa có bằng chứng.

## 6. Tiêu chí đánh giá production
Cân bằng ít nhất các nhóm sau:
- Retrieval accuracy/relevance (độ chính xác và phù hợp của truy xuất).
- Answer quality và groundedness (chất lượng câu trả lời và mức độ bám bằng chứng).
- Citation/source traceability (khả năng truy vết nguồn).
- Latency (độ trễ).
- Cost (chi phí).
- Security/access control (bảo mật và kiểm soát truy cập).
- Maintainability/operability (khả năng bảo trì và vận hành).

## 7. Trạng thái và giới hạn của tài liệu
- Đây là tài liệu tham khảo kiến trúc, không phải xác nhận rằng mọi kiến trúc đã được triển khai.
- Tài liệu này không xác nhận unit test, integration test hoặc E2E (kiểm thử đầu cuối) của Work 103 đã PASS.
- Trạng thái Work 103 chỉ được nâng lên khi có bằng chứng kiểm thử và tích hợp tương ứng.
- Không tự động thay đổi phạm vi, kiến trúc đã duyệt hoặc trạng thái phát hành.

## 8. Nguồn đầu vào
Bài viết do người dùng cung cấp trong cuộc trò chuyện ngày 2026-10-26, tiêu đề “8 KIẾN TRÚC RAG MÀ AI ENGINEER NÊN BIẾT”. Nội dung đã được biên tập để làm rõ phạm vi và tránh coi các kiến trúc là các cấp độ bắt buộc.
