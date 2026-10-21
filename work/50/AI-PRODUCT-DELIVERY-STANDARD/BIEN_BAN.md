# BIÊN BẢN — WORK 50

## Thông tin
- Work ID: 50
- Tên: HQTT AI Product Delivery Standard (APDS)
- Chủ sở hữu / người quyết định cuối cùng: Vinh
- Điều phối / quản lý kế hoạch: Xu (AI-01)
- Người thực hiện ghi hồ sơ: Xu (AI-01), CEO / AI Core của LAB
- Ngày ghi nhận: 2026-10-20 (UTC+07:00)
- Trạng thái: DECISION RECORDED — chờ nghiệm thu và phê duyệt tiêu chuẩn

## Bối cảnh
HQTT cần một chuẩn chung để quy hoạch và phát triển sản phẩm CNTT/AI theo vòng đời đầy đủ, tránh mỗi Work tự định nghĩa quy trình, vai trò, trạng thái và bằng chứng khác nhau.

## Phạm vi
APDS bao phủ: quản trị sản phẩm, khám phá bài toán, yêu cầu, kiến trúc, kỹ thuật AI, kế hoạch giao hàng, phát triển, QA/kiểm thử, bảo mật, phát hành, vận hành, bằng chứng và bàn giao.

APDS là tiêu chuẩn quản lý và tiêu chí; bản thân Work 50 không tự động triển khai code hoặc thay đổi các dịch vụ hiện hữu.

## Quyết định được ghi nhận
1. Tạo Work riêng mã 50: HQTT AI Product Delivery Standard (APDS).
2. Work 50 sở hữu tiêu chuẩn, phiên bản và quá trình đánh giá tiêu chuẩn.
3. Work 19, Work 21 và các Work sản phẩm khác là Work áp dụng tiêu chuẩn trong phạm vi phù hợp; không chuyển quyền sở hữu APDS sang các Work đó.
4. Không được coi APDS là tiêu chuẩn đã phê duyệt toàn HQTT cho đến khi Vinh ra quyết định rõ ràng.
5. Không ghi PASS nếu thiếu bằng chứng đáp ứng tiêu chí nghiệm thu.
6. Giữ thay đổi trên branch `work/50-ai-product-delivery-standard`; không sửa/merge vào `main` trong bước khởi tạo này.
7. Phải duy trì đúng ba hồ sơ điều hành chính thức: biên bản, kế hoạch thi công và nhật ký chung; không tạo các bản cạnh tranh.
8. Phải tạo/đối chiếu Sandbox khi dịch vụ sẵn sàng. Tại thời điểm ghi biên bản, lệnh liệt kê Work Sandbox trả lỗi kết nối nên trạng thái Sandbox là CHƯA XÁC MINH.

## Quyết định chưa đưa ra
- Chưa phê duyệt APDS v1.0 làm quy định bắt buộc toàn HQTT.
- Chưa chốt ngưỡng định lượng chung cho độ chính xác AI, độ trễ, chi phí hoặc độ tin cậy. Các ngưỡng phải được xác định theo rủi ro, use case và dữ liệu đánh giá của từng sản phẩm.
- Chưa xác nhận Work 50 đã đồng bộ với Sandbox.
- Chưa xác nhận sản phẩm mẫu nào sẽ dùng để thử nghiệm.

## Bước tiếp theo
Khôi phục kết nối Sandbox → đối chiếu hồ sơ → đánh giá checklist → chạy thử trên sản phẩm mẫu → trình Vinh phê duyệt.

## Bổ sung quyết định — 2026-10-21 (UTC+07:00)

### Thống nhất nguyên tắc dự phòng MCP
- Khi MCP lỗi nhưng GitHub hoạt động, Xu tiếp tục các đầu việc có thể thực hiện an toàn trực tiếp trên branch Work; ghi nhận commit, bằng chứng và phần bị chặn bởi Sandbox.
- Khi MCP phục hồi, phải đọc và đối chiếu trạng thái GitHub/Sandbox trước khi đồng bộ; phát hiện và xử lý xung đột trước khi ghi; đọc lại hai phía sau đồng bộ.
- Không coi MCP lỗi là bằng chứng rằng mọi dịch vụ ROOM-HOP đều lỗi; xác định phạm vi ảnh hưởng theo bằng chứng.
- Không tuyên bố Sandbox đã đồng bộ cho đến khi có bằng chứng đọc lại và so sánh thành công.

### Danh mục vai trò AI
- Đã tạo đề xuất 01_STANDARD/AI_ROLE_CATALOG_v1.0.md với 17 vai trò chuẩn.
- APDS được bổ sung tham chiếu tới danh mục, ma trận phân công và quy trình dự phòng MCP.
- Trạng thái vẫn PROPOSED; chưa áp dụng bắt buộc toàn HQTT cho đến khi Vinh phê duyệt.


## Bổ sung quyết định — Điều phối tự động và danh bạ AI tập trung — 2026-10-21 (UTC+07:00)

### 1. Yêu cầu của Vinh
- Mọi quyết định, mô hình, lưu đồ điều phối và quy tắc được thống nhất trong phiên làm việc phải được ghi vào hồ sơ biên bản của Work 50; không để chỉ tồn tại trong hội thoại.
- Khi khởi động dự án, AI phải tự đọc định danh, vai trò, nhiệm vụ, Project Manifest, phụ thuộc và tiêu chí nghiệm thu; tự nhận và thực hiện nhiệm vụ trong phạm vi quyền được giao, không cần Vinh gọi từng AI hoặc nhắc từng bước nhỏ.
- Cần một danh bạ AI tập trung, duy nhất làm nguồn tham chiếu chung cho các Work. Không để từng Work tự tạo danh bạ mâu thuẫn.
- Quy tắc “không hỏi, không chờ” chỉ áp dụng khi đã đủ dữ liệu và quyền hạn. Nếu thiếu đầu vào thiết yếu, có xung đột, hết giới hạn thử lại hoặc cần phê duyệt bắt buộc, AI phải tự tra cứu/xử lý trong phạm vi cho phép; nếu không giải quyết được thì ghi BLOCKED, nêu nguyên nhân, bằng chứng và người cần quyết định. Không tự đoán và không vượt quyền.

### 2. Lưu đồ điều phối tự động đã thống nhất về định hướng
`START PROJECT → Load Project Manifest + AI Registry → Build Task Graph → Assign owner/output/acceptance criteria/dependencies → Run independent tasks in parallel → Integrate & review PLAN → Required approval gate → BUILD → VERIFY → HANDOFF → Update Dashboard and trigger next eligible task`

Cơ chế cần có:
- Identity/Role Loader: nạp đúng AI ID, nền tảng, chức danh, Skills, quyền và năng lực thực thi.
- Task Graph/Scheduler: quản lý phụ thuộc và tự kích hoạt nhiệm vụ đủ điều kiện.
- Bounded Retry: tự thử lại có giới hạn; không lặp vô hạn.
- Policy/Approval Gate: giữ nguyên quyền hạn, ngân sách và các cổng phê duyệt.
- Evidence/Event Log: lưu đầu ra, sự kiện, trạng thái và bằng chứng truy vết.
- Dashboard: hiển thị trạng thái từ nguồn dữ liệu chuẩn; không tự suy diễn PASS.

### 3. Quyền hạn và bàn giao
- Vinh là chủ sở hữu và người quyết định cuối cùng; các cổng bắt buộc dành cho Vinh không được tự động bỏ qua.
- Xu (AI-01) điều phối, phân rã, phân công, tích hợp kế hoạch, theo dõi phụ thuộc và chuyển cấp ngoại lệ; không thay Vinh phê duyệt.
- Ka phản biện kiến trúc; Cla phụ trách tính khả thi và kỹ thuật; các AI chuyên môn chịu trách nhiệm về đầu ra thuộc lĩnh vực được giao.
- AI thực thi chỉ nhận nhiệm vụ đủ điều kiện; kiểm thử độc lập phải có kết quả và bằng chứng riêng. Người viết mã không tự thay thế vai trò QA độc lập.
- Mỗi Task phải có ít nhất: Task ID, Project/Work ID, owner AI ID, mục tiêu, đầu vào/tham chiếu, đầu ra, phụ thuộc, tiêu chí nghiệm thu, phạm vi quyền, giới hạn thử lại, quy tắc chuyển cấp, trạng thái, bằng chứng và bên nhận bàn giao.

### 4. Danh bạ AI tập trung — trạng thái đối chiếu
- Work 99 Sandbox có các hồ sơ: `WORK-INDEX/08_AI_TEAM/AI_IDENTITY_REGISTER_PROPOSED.md`, `AI_TEAM_DIRECTORY.md`, `AI_INTRO_CHAT.md`, và bản đề xuất mới `AI_IDENTITY_REGISTER_V1_20261021.md`.
- Bản V1 mới được tạo thành công và đã xác minh sự hiện diện qua danh sách tệp; nó vẫn là PROPOSED, chưa phải danh bạ được phê duyệt. Các tệp cũ chưa bị ghi đè hoặc xóa.
- Trong lần đọc hồ sơ qua Sandbox, công cụ trả về đối tượng rỗng; vì vậy chưa thể so sánh nội dung các tệp cũ. Trạng thái đối chiếu: BLOCKED/UNVERIFIED, không được suy luận rằng các tệp cũ rỗng.
- Danh bạ chuẩn cần có: AI ID, tên ngắn, nhà cung cấp/nền tảng, chức danh, trách nhiệm, quyền hạn, Skills/công cụ, người/AI điều phối, trạng thái, ngày xác minh và bằng chứng. Trường chưa xác minh phải ghi UNVERIFIED; không tự suy đoán.
- Không đổi/xóa/hợp nhất tệp danh bạ cũ cho đến khi đọc được và so sánh nội dung, xác định provenance (nguồn gốc), giải quyết xung đột và có quyết định phê duyệt.

### 5. Vị trí Work 50 và ranh giới đồng bộ
- Đã xác minh Work 50 tồn tại trên GitHub branch `work/50-ai-product-delivery-standard`, tại `work/50/AI-PRODUCT-DELIVERY-STANDARD/`.
- Hồ sơ biên bản chính thức là `work/50/AI-PRODUCT-DELIVERY-STANDARD/BIEN_BAN.md`; bản bổ sung này được ghi trực tiếp vào tệp đó trên branch Work 50, không ghi vào `main`.
- Work 50 không xuất hiện trong danh sách Work Sandbox ở lần kiểm tra hiện tại. Điều này chỉ xác nhận chưa có Work 50 trong danh sách Sandbox được trả về; không có nghĩa Work 50 không tồn tại trên GitHub.
- Work 99: bản V1 danh bạ và báo cáo đối chiếu đã được tạo trên Sandbox. Chưa có bằng chứng đồng bộ nội dung các hồ sơ giữa Sandbox và GitHub.

### 6. Các Work cần đối chiếu trước khi triển khai
- Work 21: Skills theo vai trò.
- Work 27: Runtime Orchestrator và năng lực thực thi.
- Work 28: công cụ MCP cho đọc ngữ cảnh, giao việc và ghi bằng chứng.
- Work 03: dashboard tiến độ dựa trên nguồn dữ liệu chuẩn.
- Work 99: danh bạ AI và cổng vào ROOM.
Không tạo bộ điều phối trùng lặp; phải đọc hồ sơ và hợp đồng hiện có trước khi phân công thi công.

### 7. Tiêu chí nghiệm thu tự động hóa
Chỉ xem xét PASS khi có kiểm thử đầu-cuối chứng minh: một lệnh khởi động tạo Project/Task Graph; registry được nạp; AI được giao đúng nhiệm vụ; task độc lập chạy song song; phụ thuộc tự kích hoạt đúng; cổng phê duyệt không bị bỏ qua; lỗi được thử lại có giới hạn hoặc chuyển BLOCKED; bằng chứng được lưu; dashboard phản ánh trạng thái thực tế. Tệp đề xuất hoặc sơ đồ riêng lẻ không chứng minh runtime đã vận hành.

### 8. Trạng thái hiện tại
- DONE: ghi nhận quyết định và lưu đồ điều phối tự động trong biên bản GitHub của Work 50.
- DONE: tạo bản đề xuất danh bạ AI V1 và báo cáo đối chiếu trong Work 99 Sandbox.
- BLOCKED: đọc/đối chiếu nội dung các danh bạ Sandbox do công cụ đọc trả về đối tượng rỗng trong lần kiểm tra.
- UNVERIFIED: đồng bộ Work 50 giữa GitHub và Sandbox; tích hợp registry vào runtime; tự động hóa end-to-end; dashboard phản ánh sự kiện runtime.
- NEXT: phục hồi đường đọc nội dung Sandbox hoặc dùng phương thức đọc được hỗ trợ; hợp nhất danh bạ sau khi đối chiếu; sau đó kiểm tra hợp đồng Work 21/27/28/03 trước khi thi công.


## Bổ sung trạng thái đồng bộ Work 50 — 2026-10-21 (UTC+07:00)

### Kết quả thực hiện
- Đã xác minh Work 50 canonical trên GitHub: branch `work/50-ai-product-delivery-standard`, thư mục `work/50/AI-PRODUCT-DELIVERY-STANDARD/`.
- Đã tạo Work 50 trong ROOM-HOP Sandbox bằng identity runtime đã đăng ký `xu`. Identity HQTT `AI-01` không phải runtime identity của ROOM-HOP; lần gọi đầu với `AI-01` bị từ chối `UNKNOWN_IDENTITY`, sau đó tạo thành công với `xu`.
- Đã chép 10 hồ sơ chuẩn từ GitHub branch sang Sandbox Work 50 bằng thao tác write thành công: BIEN_BAN.md, README.md, KE_HOACH_THI_CONG_XU.md, NHAT_KY_HOP_THI_CONG.md, APDS_STANDARD_v1.0.md, AI_ROLE_CATALOG_v1.0.md, WORK_AI_DASHBOARD_MODEL_v1.0.md, PRODUCT_CHARTER_TEMPLATE.md, WORK_AI_DASHBOARD_TEMPLATE.md, APDS_ACCEPTANCE_CHECKLIST.md.
- Danh sách Sandbox đã xác nhận các đường dẫn trên xuất hiện. GitHub BIEN_BAN.md đã được đọc lại và xác nhận chứa phần điều phối tự động/danh bạ AI.

### Giới hạn xác minh
- `sandbox_read` tiếp tục trả về đối tượng rỗng kể cả sau khi ghi thành công. Do đó đã xác minh thao tác write và sự hiện diện qua listing, nhưng chưa thể xác nhận byte-for-byte/content readback giữa GitHub và Sandbox.
- Trạng thái đồng bộ: PARTIAL — 10 tệp đã ghi và có mặt trong listing; content readback chưa xác minh.
- Không tuyên bố E2E runtime orchestration đã triển khai hoặc PASS. Việc đồng bộ tài liệu không chứng minh khả năng tự khởi động và điều phối agent đã hoạt động.

### Bước tiếp theo
1. Khắc phục hoặc dùng một đường đọc được hỗ trợ để kiểm chứng nội dung Sandbox mà không lặp lại kiểm tra encoding đã được xác nhận OK trước đây.
2. Tiếp tục đối chiếu nội dung danh bạ AI trong Work 99 sau khi đường đọc hoạt động; không ghi đè hồ sơ cũ trước khi so sánh.
3. Thiết kế và kiểm thử hợp đồng Automatic Project Execution với Work 21/27/28/03 trước khi triển khai runtime.
