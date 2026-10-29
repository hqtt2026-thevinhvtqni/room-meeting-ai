# Kiến trúc RAG Retrieval ROOM-HOP

## Phân bổ Port và Dịch vụ
- Core service: chạy trên port 8000, sở hữu ngữ nghĩa ứng dụng và truy cập dữ liệu chính tắc.
- MCP tool contract: expose trên port 8020, không truy cập storage trực tiếp, mọi thứ phải qua Core.
- Workspace Sandbox: chạy trên port 8010, dùng cho build artifacts và evidence, không phải canonical production corpus.
- Dashboard: render-only trên port 3000.

## Hợp đồng RAG (Initial contracts)
- `rag_index`: lập chỉ mục tài liệu.
- `rag_search(query, top_k=5)`: trả về kết quả tìm kiếm. Tham số `top_k` mặc định là 5 và phải là số dương (ném lỗi ValueError nếu <= 0).
- `rag_get_context`: trả về `context`, `citations[]`, `sufficient_evidence`, và `abstention_reason?` khi không đủ bằng chứng.

## Nguyên tắc xử lý
- Query rỗng hoặc chỉ có khoảng trắng sẽ bị từ chối (fail safely).
- Từ chối lập chỉ mục nếu phát hiện `duplicate source_ids`.
- Chunking phải giữ lại metadata nguồn: `source path`, `chunk number`, `start_line`, và `end_line`.
- Điểm số (score) trong lexical retrieval là baseline, không phải xác suất đã hiệu chỉnh. Cần hiệu chuẩn ngưỡng chấp nhận trên bộ đánh giá được gán nhãn.