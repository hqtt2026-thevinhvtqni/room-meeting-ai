# Quy trình đánh giá và vai trò trong Work 103

## Vai trò và trách nhiệm
- **Qw (QE/QA)**: Có nhiệm vụ tạo bộ nhãn mù (blind labels) first-pass cho các truy vấn đánh giá, đảm bảo không xem kết quả truy xuất thực tế.
- **Ka (CSA / Independent Reviewer)**: Tiến hành rà soát độc lập, đối chiếu nhãn với nguồn corpus chuẩn, phát hiện mâu thuẫn và ghi nhận biên bản mà không sửa đè trực tiếp lên bản gốc của Qw.
- **Xu (Coordinator)**: Điều phối quy trình, xác nhận snapshot corpus, đảm bảo tệp nhãn được tạo đúng quy trình, và thực hiện đóng băng (freeze/hash) phiên bản nhãn trước khi mở cổng đánh giá retrieval.

## Trạng thái cổng (Gate Status)
Cổng đánh giá retrieval (RAG E2E) chỉ được mở khi:
1. Corpus chuẩn đã được xác định, có phiên bản và hash rõ ràng.
2. Bộ nhãn first-pass đã được Ka rà soát và các bất đồng đã được giải quyết (adjudication).
3. Xu đã xác nhận và khóa (freeze) bộ nhãn cuối cùng.