# W05 — GOOGLE DOCS / GOOGLE DRIVE MCP EVIDENCE

## Evidence date
2026-09-28 — test thực tế do Mê thực hiện.

## 1. MCP thực tế đã test
- Community MCP: `@modelcontextprotocol/server-gdrive`
- Kết nối remote: `mcp-remote`
- Đây KHÔNG phải Google Official Workspace MCP.
- Google official Workspace MCP/Toolbox tại thời điểm test vẫn ở trạng thái experimental.

## 2. Các khả năng đã test PASS
- OAuth authentication và refresh token.
- Tạo Google Doc.
- `documents.get`.
- `batchUpdate`.
- Append nội dung vào Google Doc.
- Formatting trên Google Doc.
- Luồng append phải xác định lại `endIndex` trước khi ghi tiếp; không được giả định index cũ.
- Markdown không thể đẩy nguyên văn để mong Docs tự hiểu formatting; cần parser Markdown → Google Docs requests.

## 3. Failure / limit evidence
### 3.1 Revision conflict
- Khi revision bị conflict, Google Docs trả:
  `400 FAILED_PRECONDITION`.
- Đây là evidence cho việc Core/Adapter cần xử lý concurrency/revision conflict.

### 3.2 Rate limit
- Test tạo 11 files trong khoảng 60 giây gặp:
  `429 RESOURCE_EXHAUSTED`.
- Đây là evidence cho nhu cầu throttle/rate-limit/retry/backoff ở lớp tích hợp.

## 4. Kiến trúc đã chốt từ evidence
```
AI → MCP :8020 → Core :8000 → Google Workspace Adapter → Drive/Docs API
```

MCP :8020 là translator/interface cho AI, không phải nơi chứa business logic Google Workspace.

Core :8000 là single truth. AI không được tự bypass Core để gọi Google Drive/Docs.

## 5. Provider direction
- Google Official MCP được xem là primary direction khi capability/runtime phù hợp.
- Direct Google Drive/Docs API được giữ như fallback/special capability thông qua `GoogleDocumentProvider`.
- Dù dùng provider nào, AI vẫn đi qua MCP → Core; không cho AI tự bypass Core.

## 6. Pipeline W05
```
raw transcript.md
    ↓
Structured Transcript
    ↓
Evidence / Messages / Decisions / Actions
    ↓
Document Composer
    ↓
Google Docs
```

## 7. Thiết kế cần mang vào W05
- Customer-owned OAuth là mặc định.
- Service Account chỉ là option.
- Auth Adapter cần quản lý OAuth/refresh.
- Adapter cần xử lý endIndex khi append.
- Markdown parser cần là một capability riêng.
- Batch/retry/throttle/concurrency conflict phải nằm ở lớp Core/Adapter, không đẩy trách nhiệm cho AI.

## 8. Trạng thái
EVIDENCE RECOVERED — đủ cơ sở để bước tiếp theo là chốt Adapter Contract/Auth Adapter trước khi code.
