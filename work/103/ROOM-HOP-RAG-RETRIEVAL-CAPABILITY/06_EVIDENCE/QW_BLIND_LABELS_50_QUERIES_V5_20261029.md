# WORK 103 — QW BLIND LABELS (FIRST-PASS V5 - PROVENANCE & RULES ALIGNED)
**Date-time:** 2026-10-29 (UTC+07:00)
**Annotator:** Qw (QE/QA)
**Status:** FIRST-PASS READY FOR Xu HASHING AND Ka FINAL ADJUDICATION

## 1. Explicit Labeling Rules (Per Manifest v3.0)
1. **ANSWERABLE:** The corpus contains sufficient explicit evidence to answer the query *affirmatively or negatively*. (e.g., If a security policy explicitly states "No credentials are indexed", a query asking "Does the policy forbid storing passwords?" is ANSWERABLE with a definitive "Yes").
2. **NO_ANSWER:** The corpus lacks any information to form a definitive yes/no answer, or the query references entities/concepts entirely absent from the defined benchmark scope.
3. **Component Boundary:** Queries must precisely match the component described in the rationale. Do not conflate MCP boundaries with RAG retrieval boundaries unless explicitly stated in the source.
4. **No Retrieval Data:** NO retrieval scores, ranks, or actual retrieval outputs are included in this artifact.

## 2. Corpus Reference (v3.0 Benchmark Fixture with Verified Hashes)
- `00_CORPUS/network.md`
- `00_CORPUS/sales.md`
- `00_CORPUS/architecture.md`
- `00_CORPUS/security.md`
- `00_CORPUS/evidence.md`
- `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`

## 3. Blind Labeling Dataset (50 Queries)

| query_id | query_text | label | expected_source_id | category_stratum | evidence_span_rationale | ambiguity_flag |
|----------|------------|-------|--------------------|------------------|-------------------------|----------------|
| Q001 | Làm thế nào để kiểm tra tín hiệu quang của modem ONT? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | Đề cập đến việc kiểm tra công suất RX và cảnh báo LOS. | FALSE |
| Q002 | Cảnh báo LOS trên modem ONT nghĩa là gì và cần kiểm tra gì? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | Cần kiểm tra công suất RX và đầu nối sợi quang. | FALSE |
| Q003 | Các bước kiểm tra đầu nối sợi quang khi mất tín hiệu? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | Đề cập đến việc kiểm tra đầu nối sợi quang trong xử lý sự cố. | FALSE |
| Q004 | Ngưỡng công suất RX bình thường cụ thể của modem ONT là bao nhiêu? | NO_ANSWER | N/A | [Technical/Network] | Tài liệu chỉ yêu cầu "Check RX power" nhưng không nêu ngưỡng số liệu cụ thể. | TRUE |
| Q005 | Làm sao để xử lý lỗi mất tín hiệu quang trên thiết bị đầu cuối? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | Liên quan đến kiểm tra RX power và LOS alarm. | FALSE |
| Q006 | Lịch giao hàng cho đơn đặt hàng của khách hàng được xác nhận như thế nào? | ANSWERABLE | 00_CORPUS/sales.md | [Technical/Sales] | Đề cập đến "Customer order delivery schedule". | FALSE |
| Q007 | Làm thế nào để xác nhận số lượng xi măng trong đơn hàng? | ANSWERABLE | 00_CORPUS/sales.md | [Technical/Sales] | Đề cập đến "Confirm cement quantity". | FALSE |
| Q008 | Quy trình xử lý khi khách hàng yêu cầu thay đổi lịch giao xi măng? | NO_ANSWER | N/A | [Technical/Sales] | Tài liệu chỉ đề cập xác nhận số lượng và lịch giao, không có quy trình thay đổi. | FALSE |
| Q009 | Ai là người phụ trách xác nhận số lượng xi măng? | NO_ANSWER | N/A | [Technical/Sales] | Tài liệu không đề cập đến vai trò hoặc tên người phụ trách cụ thể. | FALSE |
| Q010 | Lịch giao hàng được lưu trữ ở đâu trong hệ thống? | NO_ANSWER | N/A | [Technical/Sales] | Không có thông tin về nơi lưu trữ hoặc cơ sở dữ liệu lịch giao hàng. | FALSE |
| Q011 | Cổng MCP sử dụng port nào trong kiến trúc ROOM-HOP? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | MCP sử dụng port :8020. | FALSE |
| Q012 | Core service chạy trên port nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Core service chạy trên port :8000. | FALSE |
| Q013 | Dashboard render chạy trên port nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Dashboard chạy trên port :3000. | FALSE |
| Q014 | Workspace Sandbox sử dụng port nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Workspace sử dụng port :8010. | FALSE |
| Q015 | MCP có được phép truy cập trực tiếp vào storage không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Không. Tài liệu quy định rõ MCP không truy cập storage trực tiếp; mọi thao tác đọc/ghi dữ liệu phải thông qua Core service theo hợp đồng MCP. | FALSE |
| Q016 | Làm thế nào để thêm ChromaDB vào hệ thống RAG hiện tại ngay lập tức? | NO_ANSWER | N/A | [Technical/Architecture] | ChromaDB là extension gate, chưa được tích hợp, cần đánh giá baseline trước. | FALSE |
| Q017 | Các hợp đồng (contracts) đề xuất cho RAG retrieval là gì? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | rag_index, rag_search, rag_get_context. | FALSE |
| Q018 | Tham số top_k mặc định trong rag_search là bao nhiêu? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | top_k=5. | FALSE |
| Q019 | Làm sao để RAG trả về lý do từ chối (abstention)? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Khi không đủ bằng chứng, trả về sufficient_evidence=false và abstention_reason. | FALSE |
| Q020 | Điểm số (score) trong lexical retrieval có phải là xác suất đã hiệu chỉnh không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Không, nó là baseline, không phải xác suất đã hiệu chỉnh. | FALSE |
| Q021 | Hệ thống có được phép lập chỉ mục các tệp .env không? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Không, không bao giờ lập chỉ mục .env, thông tin xác thực hoặc khóa riêng. | FALSE |
| Q022 | Làm thế nào để xử lý nội dung tài liệu có chứa prompt injection? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Nội dung retrieved được coi là dữ liệu không đáng tin cậy, không được thực thi. | FALSE |
| Q023 | Lỗi MCP có được phép hiển thị stack trace không? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Không, lỗi MCP không được phơi bày stack trace hoặc bí mật. | FALSE |
| Q024 | AI có được phép đưa ra quyết định thay thế Core không? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Không, RAG trả về bằng chứng, không trở thành cơ quan quyết định. | FALSE |
| Q025 | Làm sao để xóa một tài liệu khỏi chỉ mục RAG một cách an toàn? | NO_ANSWER | N/A | [Security/Policy] | Tài liệu hiện tại chưa mô tả quy trình xóa/rebuild chi tiết, chỉ đề cập cần review ở extension gate. | TRUE |
| Q026 | RAG retrieval có trả về abstention_reason khi không đủ bằng chứng không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Có, tài liệu quy định trả về sufficient_evidence=false và abstention_reason khi không đủ bằng chứng. | FALSE |
| Q027 | Điều gì xảy ra nếu top_k được đặt là 0 hoặc số âm? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Sẽ ném ra lỗi ValueError (top_k phải dương). | FALSE |
| Q028 | Metadata của chunk có bao gồm đường dẫn nguồn (source path) không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Có, chunking xác định giữ lại source path, chunk number, và line ranges. | FALSE |
| Q029 | Làm thế nào để đảm bảo chunking giữ nguyên metadata nguồn? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Chunking xác định giữ lại source path, chunk number, và line ranges. | FALSE |
| Q030 | Truy vấn "lượng tử tàu ngầm thiên thạch" sẽ trả về kết quả gì? | NO_ANSWER | N/A | [Technical/Architecture] | Không có bằng chứng liên quan trong bất kỳ tài liệu nào của corpus. | FALSE |
| Q031 | Tín hiệu quang LOS có liên quan đến đầu nối sợi quang không? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | Có, cần kiểm tra đầu nối sợi quang khi có cảnh báo LOS. | FALSE |
| Q032 | Làm thế nào để khắc phục sự cố modem ONT không lên đèn nguồn? | NO_ANSWER | N/A | [Technical/Network] | Tài liệu chỉ đề cập kiểm tra tín hiệu quang, không nói về đèn trạng thái cụ thể. | TRUE |
| Q033 | Tài liệu nào hướng dẫn kiểm tra công suất RX? | ANSWERABLE | 00_CORPUS/network.md | [Technical/Network] | 00_CORPUS/network.md. | FALSE |
| Q034 | Quy trình xác nhận đơn hàng xi măng bao gồm những bước nào? | ANSWERABLE | 00_CORPUS/sales.md | [Technical/Sales] | Xác nhận lịch giao hàng và số lượng xi măng. | FALSE |
| Q035 | Khách hàng A có đơn hàng nào trong hệ thống không? | NO_ANSWER | N/A | [Technical/Sales] | Không có dữ liệu cụ thể về "Khách hàng A" trong tài liệu mẫu. | FALSE |
| Q036 | Luồng dữ liệu RAG bắt đầu từ đâu và đi qua những thành phần nào? | ANSWERABLE | 03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md | [Technical/Architecture] | Tài liệu mô tả rõ luồng dữ liệu bắt đầu từ Approved source registry, qua ingestion adapter, đến retrieval engine. | FALSE |
| Q037 | AI caller nhận được gì từ RAG retrieval? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Nhận được grounded answer với citations hoặc abstention. | FALSE |
| Q038 | Port 8020 được sử dụng cho dịch vụ nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | MCP tool contract. | FALSE |
| Q039 | Port 8000 được sử dụng cho dịch vụ nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Core service. | FALSE |
| Q040 | Có thể sử dụng RAG để tự động xóa tệp trên ổ đĩa không? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Không, tài liệu security.md nêu rõ retrieval chỉ trả về bằng chứng, không cấp quyền thực thi lệnh hoặc xóa tệp. | FALSE |
| Q041 | Chunking có giữ lại thông tin dòng bắt đầu và kết thúc không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Có, metadata giữ lại start_line và end_line. | FALSE |
| Q042 | Metadata của chunk có bao gồm số thứ tự chunk không? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Có, metadata giữ lại chunk number cùng với source path và line ranges. | FALSE |
| Q043 | Làm sao để biết một chunk bắt đầu và kết thúc ở dòng nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | Thông qua metadata start_line và end_line. | FALSE |
| Q044 | Điểm số (score) mặc định tối thiểu để trả về kết quả là bao nhiêu? | NO_ANSWER | N/A | [Technical/Architecture] | Tài liệu nói "Calibrate acceptance thresholds", không đưa ra con số mặc định cụ thể cho lexical. | TRUE |
| Q045 | rag_get_context trả về những trường thông tin nào? | ANSWERABLE | 00_CORPUS/architecture.md | [Technical/Architecture] | context, citations[], sufficient_evidence, abstention_reason?. | FALSE |
| Q046 | Làm thế nào để cấu hình ChromaDB cho ROOM-HOP ngay bây giờ? | NO_ANSWER | N/A | [Technical/Architecture] | ChromaDB chưa được tích hợp, đang ở extension gate, cần đánh giá trước. | FALSE |
| Q047 | Ai là người chịu trách nhiệm chính cho việc review nhãn mù độc lập? | ANSWERABLE | 00_CORPUS/evidence.md | [Governance/Process] | Ka (CSA / independent reviewer). | FALSE |
| Q048 | Qw có nhiệm vụ gì trong quy trình đánh giá RAG? | ANSWERABLE | 00_CORPUS/evidence.md | [Governance/Process] | Qw (QE/QA) phải tạo nhãn mù first-pass cho các truy vấn. | FALSE |
| Q049 | Xu có vai trò gì trong quy trình này? | ANSWERABLE | 00_CORPUS/evidence.md | [Governance/Process] | Xu điều phối và xác nhận bằng chứng, đóng băng phiên bản nhãn. | FALSE |
| Q050 | Chính sách bảo mật có cấm việc lưu trữ hoặc trả về mật khẩu quản trị trong hệ thống RAG không? | ANSWERABLE | 00_CORPUS/security.md | [Security/Policy] | Có. Tài liệu 00_CORPUS/security.md quy định rõ nguyên tắc cấm lập chỉ mục thông tin xác thực như .env hoặc passwords, và hệ thống không được phép lưu trữ hoặc trả về mật khẩu. (Đã sửa theo hướng dẫn của Ka: hỏi về chính sách thay vì nội dung thực tế của tệp). | FALSE |

## 4. Handoff Notes & Resolution of Ka's V4 Findings
- **V1, V2, V3, V4 are IMMUTABLE.** This V5 is a new artifact created to resolve adjudication blocks without altering history.
- **Q050 Resolved (Per Ka's Directive):** Changed the query from asking about the *actual content* of the file to asking about the *security policy*. The query is now: "Chính sách bảo mật có cấm việc lưu trữ hoặc trả về mật khẩu quản trị trong hệ thống RAG không?". Label remains **ANSWERABLE** with a clear rationale citing the explicit policy in `00_CORPUS/security.md`. This perfectly aligns with the "Absence of Evidence" rule without making unverifiable claims about file contents.
- **Provenance Upgraded:** Upgraded the manifest to v3.0, populating actual Byte Size and SHA-256 hashes. Crucially, the "Approver / Scope" column now explicitly references upstream approval evidence (e.g., `01_ORIGINAL/REQUEST_AND_SCOPE.md`, `00_ROOT/WORK_MANIFEST.md`) instead of generic scope names, fulfilling the traceable provenance requirement.

**Signature:** Qw | QE/QA Annotator