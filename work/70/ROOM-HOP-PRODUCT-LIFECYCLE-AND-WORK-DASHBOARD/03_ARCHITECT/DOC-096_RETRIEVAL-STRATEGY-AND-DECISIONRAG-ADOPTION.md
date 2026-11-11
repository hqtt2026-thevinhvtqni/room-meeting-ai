# DOC-096 — CHIẾN LƯỢC RETRIEVAL ĐA PHƯƠNG PHÁP VÀ TIẾP NHẬN DECISIONRAG
- Document ID: DOC-096
- Priority: P1
- Status: DESIGN ADDENDUM — RESEARCH ONLY; PRODUCTION IMPLEMENTATION NOT AUTHORIZED
- Owner: Xu / xu
- Authority: Vinh
- Date: 2026-11-11
- Canonical path: 03_ARCHITECT/DOC-096_RETRIEVAL-STRATEGY-AND-DECISIONRAG-ADOPTION.md
- Governing architecture: DOC-095

## 1. Mục đích
Chuẩn hóa Retrieval thành năng lực dùng chung, có thể thay đổi chiến lược tìm kiếm mà không tạo Core thứ hai hoặc khóa ROOM-HOP vào một thuật toán duy nhất. DecisionRAG được tiếp nhận làm phương án nghiên cứu bổ sung, chưa thay baseline và chưa được phép triển khai production.

## 2. Quyết định kiến trúc
1. ROOM-HOP giữ một Core authority duy nhất tại ranh giới kiến trúc đã được xác lập; Retrieval là capability/subsystem, không phải control plane mới.
2. Các chiến lược retrieval được triển khai sau một interface/contract thống nhất:
   - lexical retrieval (BM25/keyword);
   - dense vector retrieval;
   - hybrid retrieval;
   - reranking;
   - hierarchical / decision-based retrieval (DecisionRAG);
   - graph retrieval khi có use case và evidence.
3. Các strategy phải trả về cùng Evidence Result Contract: query_id, strategy_id/version, source_id, document_revision, chunk_id, exact source locator, content/span, rank, score (nếu có), retrieval trace, access decision, timestamp và abstention metadata.
4. Generation chỉ nhận evidence đã qua kiểm tra quyền truy cập và provenance. Không có evidence đủ căn cứ thì abstain; không được bịa nguồn.
5. Strategy selection có thể cấu hình theo loại câu hỏi/tài liệu, nhưng mọi lựa chọn phải đo được, tái lập và có fallback rõ ràng.

## 3. DecisionRAG — phạm vi tiếp thu
DecisionRAG tổ chức tài liệu theo cây phân cấp và dùng Decision Model điều hướng các nhánh để tìm passages. Cách đánh giá nhiều ứng viên trong cùng context là giả thuyết nghiên cứu đáng kiểm chứng.
- Không mặc định xóa vector index khỏi toàn hệ thống; paper mô tả một retrieval path không cần first-stage retriever/vector index trong lúc truy vấn.
- Không suy rộng kết quả benchmark thành cam kết hiệu năng trên corpus ROOM-HOP.
- Cần kiểm tra tree construction, node summaries/metadata, decision accuracy, pruning loss, context/token cost, latency, throughput, permission filtering và source traceability.
- Shared-context decision phải được so sánh với candidate-wise decision trên cùng dữ liệu, cùng model, cùng ngân sách token và cùng điều kiện chạy.

## 4. Ranh giới và nguyên tắc an toàn
- Core vẫn là authority cho identity, authorization, source access và audit.
- Retrieval không được đọc trực tiếp kho dữ liệu ngoài contract được Core cho phép.
- Permission filtering phải diễn ra trước khi nội dung nhạy cảm được đưa vào Decision Model/context.
- Mọi node/chunk phải giữ document revision và đường dẫn truy nguyên tới nguồn.
- Pruning là quyết định có thể làm mất bằng chứng; phải log nhánh được mở rộng, loại bỏ và lý do.
- Không thay đổi API, DB, runtime, model provider, threshold production hoặc flow hiện hành bằng tài liệu này.

## 5. Đánh giá và điều kiện so sánh
So sánh trên cùng query set, corpus snapshot, permission context và generation policy:
- Retrieval: Precision@5, Recall@5, MRR, R@1/Hit@1.
- Answerability: answer rate, no-answer accuracy, false abstention, unsupported-answer/leak rate.
- Evidence: source coverage, citation/locator correctness, pruning miss rate.
- Operations: p50/p95 latency, token usage, cost/query, throughput, tree build/update cost.
- Reproducibility: model/version, prompt/version, corpus hash, tree snapshot/hash, code commit, run ID và raw output.

Không dùng duy nhất R@1 để chọn phương án; không đánh đổi leak/security/provenance để tăng retrieval score.

## 6. Lộ trình tiếp nhận
A. W70: duy trì chiến lược đa phương pháp và contract chung làm baseline kiến trúc.
B. W103: xây DecisionRAG thành nhánh thí nghiệm riêng; giữ baseline hiện hành bất biến trong phép so sánh.
C. Chỉ sau khi có kết quả tái lập, independent review và quyết định của Vinh mới xem xét thay đổi kiến trúc/production.
D. Các Work khác tham chiếu DOC-095 và DOC-096; không tự tạo retrieval service/Core trùng lặp.

## 7. Trạng thái và giới hạn
- Architecture direction: RECORDED.
- DecisionRAG implementation: NOT AUTHORIZED.
- Corpus-specific benchmark: NOT RUN / NOT VERIFIED.
- Production adoption: NOT APPROVED.
- Paper-reported benchmark numbers are research claims, not ROOM-HOP evidence.

## 8. Lịch sử cập nhật
- 2026-11-11: tiếp nhận DecisionRAG làm nhánh nghiên cứu và chuẩn hóa retrieval đa phương pháp; giữ nguyên baseline và quyền phê duyệt production của Vinh.
