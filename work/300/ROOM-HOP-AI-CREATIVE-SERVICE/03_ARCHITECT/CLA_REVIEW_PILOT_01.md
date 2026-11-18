# CLA-300 — PHẢN BIỆN ĐỘC LẬP PILOT-01 (API contract / kiến trúc kỹ thuật / xử lý cục bộ)

- Người thực hiện: Cla (Claude) / AI-03 — vai trò theo AI_REVIEW_HANDOFF.md: technical architecture, API contract, local processing.
- Ngày: 2026-11-19 (giờ cụ thể không được cung cấp).
- Đối tượng review: `REVIEW_PACKET_PILOT_01.md`, `AI_REVIEW_HANDOFF.md` (GitHub main, đọc raw, read-only), DOC-034, DOC-035 (đọc phần liên quan), `PILOT_01_ZERO_CASH_PLAN.md` + `REVIEW_REQUEST_PILOT_01.md` (Sandbox).
- Phương pháp: review tĩnh tài liệu + đối chiếu tài liệu chính thức Cloudflare Workers AI (schema model, pricing, changelog). KHÔNG chạy code, KHÔNG gọi API/provider, KHÔNG upload ảnh, KHÔNG đụng billing/credential, KHÔNG sửa DOC-001/002/003/034/035 trên GitHub.
- Nhãn bằng chứng: DOCUMENTED / ASSUMED / UNKNOWN / EXPERIMENTALLY VERIFIED. Không có mục nào đạt EXPERIMENTALLY VERIFIED vì chưa có phép thử.

## 0. Xác minh phần "đồng bộ GitHub" (đối chiếu độc lập)
- DOCUMENTED (đọc raw main, HTTP 200): `03_ARCHITECT/AI_REVIEW_HANDOFF.md` (1.223 byte), `03_ARCHITECT/REVIEW_PACKET_PILOT_01.md` (8.134 byte), `00_ROOT/DOC-034…MINUTES.md` (8.947 byte), `00_ROOT/DOC-035…JOURNAL.md` (35.767 byte). Nội dung khớp mô tả trong báo cáo đồng bộ (W300 chỉ ảnh/Photo AI; Work 29 giữ video; BUILD chưa mở).
- DOCUMENTED: trang commit `e74a5a944056` truy cập được (HTTP 200).
- UNKNOWN: chưa xác minh `e74a5a944056` là HEAD của main; chưa xác minh commit chỉ đổi tài liệu như báo cáo nói (API GitHub trả 403); chưa đối chiếu toàn bộ cây thư mục và việc mã Dashboard legacy giữ nguyên.
- Phát hiện: DOC-035 trên GitHub đã có Entry 014–015 của Ka. Cla không lặp lại các finding KAI-300-01…08; chỉ xác nhận/bổ sung khi có bằng chứng độc lập (xem mục 3).

## 1. Trả lời nhanh các câu hỏi review thuộc phạm vi Cla
- Q2 (FLUX.1 schnell, FLUX.2 klein 4B có phù hợp?): Phù hợp làm ứng viên để kiểm chứng đường ống (contract, chi phí, metadata, QC). KHÔNG phù hợp để kết luận về chất lượng sản phẩm hay "photo editing" theo nghĩa giữ nguyên ảnh gốc (xem CLA-300-02).
- Q3 (schema/kích thước/định dạng cần chốt): xem CLA-300-01, 02.
- Q4 (metadata tối thiểu): xem CLA-300-06.
- Q7 (3 request đủ chưa?): đủ cho smoke test; nhưng không phải cơ chế chứng minh zero-spend (đồng ý KAI-300-03). Xem CLA-300-03.
- Q9 (làm gì cục bộ trước): xem CLA-300-05.
- Q10 (thiếu failure mode/acceptance): xem CLA-300-04, 07, 08.

## 2. Phán quyết
**APPROVE WITH CONDITIONS — chỉ cho tài liệu/nghiên cứu/thiết kế tiếp tục. KHÔNG phê duyệt đóng băng kiến trúc, KHÔNG mở BUILD.**
Các điều kiện P1 cần giải quyết hoặc được Vinh chấp nhận rõ ràng trước cổng BUILD: CLA-300-01, 02, 03, 04, 05, 08.

## 3. Findings
Định dạng: finding / evidence / severity / recommendation / acceptance test.

### CLA-300-01 — P1 / API CONTRACT: FLUX.1 schnell chưa được ghim hợp đồng
- Finding: Packet nêu giá nhưng không ghim request/response contract; ví dụ "20 bước" là cấu hình không hợp lệ.
- Evidence (DOCUMENTED, schema trên trang model chính thức): `prompt` bắt buộc, độ dài 1–2048; `steps` mặc định 4, tối đa 8; output là JSON `{image: <base64>}`. Xác nhận độc lập KAI-300-02. Schema không liệt kê width/height → kích thước output UNKNOWN. Có phiên bản tài liệu ghi tên tham số khác (`num_steps` so với `steps`) và có trang ghi `seed` tuỳ chọn → tài liệu không nhất quán giữa các phiên bản. Ví dụ tài liệu dùng data URI `image/jpeg` nhưng đó là ví dụ, không phải cam kết định dạng (ASSUMED JPEG).
- Recommendation: ghim hợp đồng tại thời điểm test (model ID, ngày đọc, URL tài liệu, schema đã lưu bản sao); validate request phía client theo schema (từ chối field lạ, steps >8, prompt >2048); không suy định dạng/kích thước ảnh từ tài liệu mà đo từ file thật bằng magic bytes + decode; mặc định `steps=4`.
- Acceptance test: contract test chạy trên mock (không gọi mạng) với request hợp lệ/không hợp lệ; golden fixture response giả; test fail-closed khi response thiếu `image`, base64 hỏng, hoặc decode lỗi; test nhận diện định dạng bằng magic bytes không dựa vào Content-Type.

### CLA-300-02 — P1 / API CONTRACT & SCOPE: klein 4B là sinh ảnh có tham chiếu, không phải trình chỉnh sửa giữ nguyên ảnh
- Finding: P300-02 và AC-300-06 gọi là "image editing / subject-layout preservation", nhưng hợp đồng mô hình không có mask/inpaint và ảnh vào bị giới hạn nhỏ.
- Evidence (DOCUMENTED, changelog + trang model Cloudflare): input là multipart/form-data kể cả khi chỉ có prompt; `prompt` bắt buộc; tối đa 4 ảnh tham chiếu `input_image_0…3` (binary); `width`/`height` 256–1920 (mặc định 1024×768); `guidance`, `seed` tuỳ chọn; steps cố định 4 (mô hình chưng cất); output `{image: base64}`. Giới hạn ảnh vào dưới 512×512 được ghi cho FLUX.2 trên Workers AI (bài launch FLUX.2 dev); klein "giống dev" nên áp dụng tạm — ASSUMED cho klein cho tới khi trang model xác nhận. Trang model klein còn ví dụ có `steps=25` trái với changelog (steps cố định) → UNKNOWN, cần đo.
- Hệ quả: với ảnh thật độ phân giải cao, "edit" thực chất là tái tạo có điều kiện từ bản ảnh đã thu nhỏ ≤512 px; không bảo đảm giữ pixel/bố cục. Các thao tác cần trung thực pixel (crop, resize, chỉnh màu, tách nền…) phải là xử lý cục bộ xác định hoặc endpoint khác.
- Recommendation: đổi tên workflow thành "reference-conditioned image-to-image"; ghi rõ non-goal "không đảm bảo giữ nguyên ảnh gốc"; bước thu nhỏ tham chiếu là một biến đổi cục bộ có ghi lại; rubric "structure consistency" chấm so với bản tham chiếu đã thu nhỏ; không dùng kết quả klein để kết luận cho "photo editing" của sản phẩm.
- Acceptance test: test cục bộ chứng minh ảnh vào luôn bị ép về đúng giới hạn trước khi gửi (có assert kích thước + transform ghi trong manifest); test từ chối >4 ảnh, ảnh quá lớn/định dạng lạ; tài liệu AC-300-06 được đổi tên và có dòng non-goal.

### CLA-300-03 — P1 / COST ESTIMATOR & GATING
- Finding: ước lượng chi phí trong packet sai tham số và chưa có công thức/giả định tile; 3 request không phải kiểm soát zero-spend.
- Evidence (DOCUMENTED, pricing chính thức): schnell 4,80 neurons/tile 512×512 + 9,60 neurons/bước; klein-4b 5,37 neurons/tile ảnh vào + 26,05 neurons/tile ảnh ra; 10.000 neurons/ngày miễn phí; vượt hạn mức trên Workers Free thì thao tác lỗi, muốn dùng thêm phải lên Workers Paid ($0,011/1.000 neurons). Tính theo công thức giả định tile = số ô 512×512 (ASSUMED, làm tròn lên chưa xác minh):
  - schnell, 4 bước: 43,2 neurons (1 tile) đến 57,6 (4 tile, nếu ảnh 1024²); 8 bước: 81,6 đến 96,0. Gói 20 bước của packet không hợp lệ.
  - klein-4b: ảnh ra 1024×1024 = 4 tile → 104,2; 1024×768 = 3 tile → 78,15; cộng 5,37 cho mỗi ảnh vào 512×512 (1 tile) → khoảng 109,6 hoặc 83,5 neurons cho một lần edit.
  - Quy đổi: 3 request dùng vào khoảng 2–4% hạn mức ngày → giới hạn 3 request là rất bảo thủ về quota nhưng không chứng minh được "không phát sinh phí" (đồng ý KAI-300-03).
- UNKNOWN: có phải mô hình ảnh nào cũng dùng được trên Workers Free? Nguồn thứ cấp (bài dev.to) nói có lỗi 5035 "model requires Workers Paid plan" với một số mô hình tốn tài nguyên, đặc biệt mô hình ảnh. Chưa kiểm tra bằng trang errors chính thức hay tài khoản thật.
- Recommendation: (1) cổng điều kiện cứng: tài khoản đang ở Workers Free, không có phương thức thanh toán/Paid, model truy cập được — nếu một model đòi Paid thì BLOCKED, không nâng cấp; (2) hàm `estimate_neurons(model, w, h, n_inputs, steps)` thuần, làm tròn lên, fail-closed khi model/kích thước/steps lạ; (3) sổ cái ngân sách: trần pilot ví dụ ≤ 400 neurons ước tính và giữ ≥ 50% hạn mức ngày chưa dùng; (4) sau lần gọi đầu tiên đối chiếu mức tiêu thụ thực trên dashboard với ước lượng (đây mới là EXPERIMENTALLY VERIFIED).
- Acceptance test: unit test estimator cho các cặp (model, kích thước, steps) kể trên; test model/size lạ → từ chối; test vượt trần ngân sách → từ chối trước khi tạo request; bằng chứng dashboard (ảnh chụp/ghi chép) trước và sau lần gọi duy nhất đầu tiên.

### CLA-300-04 — P1 / ADAPTER, JOB LIFECYCLE & CHI TIÊU NGẦM
- Finding: thiết kế "Job Orchestrator + Provider Registry" chưa nói rõ vòng đời job, retry, idempotency, đồng thời; với dịch vụ tính theo neurons, mỗi retry là chi tiêu.
- Evidence: DOCUMENTED — Workers AI gọi đồng bộ trả base64 (không cần polling cho pilot); có tham số hàng đợi `queueRequest` ở endpoint REST (async/batch là ngoại lệ ZDR theo KAI-300-04). ASSUMED — mã lỗi cụ thể (4xx/5xx/hạn mức) lấy từ trang errors chính thức lúc build, chưa đọc đầy đủ ở lượt này.
- Recommendation: giữ pilot ở mức tối giản — hợp đồng adapter `describe / validate / estimate / submit` + kết quả chuẩn hoá; máy trạng thái CREATED → VALIDATED → APPROVED → SUBMITTED → SUCCEEDED | FAILED | BLOCKED; zero retry tự động (retry là quyết định của người, kèm ước lượng mới); idempotency key = băm job spec để chặn gửi trùng; single-flight (đồng thời tối đa 1) để admission control không bị race; tắt `queueRequest`; timeout rõ ràng và timeout không được hiểu là "chưa tốn" (coi như đã tốn trong sổ cái); mọi lỗi lạ → BLOCKED, không thử lại.
- Acceptance test: mock server: lỗi quota → BLOCKED, không retry; timeout → không gửi lại, sổ cái vẫn trừ; gửi trùng spec → bị chặn; hai job song song → chỉ một được admit.

### CLA-300-05 — P1 / XỬ LÝ CỤC BỘ LÀM TRƯỚC (Q7, Q9)
- Finding: packet liệt kê tiện ích cục bộ nhưng không nêu thứ tự, đặc tả an toàn giải mã ảnh hay chính sách metadata; đây là phần phải xong và qua test trước khi có adapter cloud.
- Evidence: DOCUMENTED (nhật ký Sandbox, mục đo phần cứng — thuộc nhóm entry bị đánh dấu MISROUTED nhưng thông số máy không riêng cho video, cần xác nhận lại): HP EliteBook 840 G3, i5-6300U (2C/4T), RAM 7,88 GB (trống 1,15 GB lúc đo), Intel HD 520, ổ trống tổng khoảng 7,9 GB. Ngôn ngữ/thư viện (Python, Pillow) là ASSUMED theo bối cảnh Python + VS Code.
- Recommendation — thứ tự triển khai khi BUILD được mở:
  1. Kiểm tra/giải mã an toàn: sniff magic bytes, giới hạn byte và số điểm ảnh (chống decompression bomb), từ chối ảnh nhiều khung/động, xử lý EXIF orientation, chỉ whitelist PNG/JPEG/WebP.
  2. SHA-256 trên byte chuẩn hoá + manifest.
  3. Chính sách metadata: mặc định gỡ EXIF/GPS ở đầu ra, ghi nhận trong manifest (hợp với KAI-300-04).
  4. Resize/crop/convert với bộ lấy mẫu cố định, chuyển hệ màu về sRGB, xử lý alpha khi xuất JPEG; không gọi "upscale" là "enhancement".
  5. Thu nhỏ tham chiếu ≤512 px cho klein (CLA-300-02) và thumbnail.
  6. Ghi file nguyên tử, thư mục tạm quyền hạn chế, xử lý từng ảnh một.
  Cấu hình máy hiện tại chỉ hợp thư viện nhẹ; không đưa framework nặng vào pilot.
- Acceptance test: bộ test file lỗi (cắt cụt, header kích thước khổng lồ, đa khung, CMYK, PNG alpha sang JPEG, EXIF xoay, 1×1); băm lặp lại cho cùng kết quả; test chặn mạng (module cục bộ không import/không mở socket); bộ test chạy được trong giới hạn RAM/ổ đĩa của máy mục tiêu.

### CLA-300-06 — P2 / METADATA & PROVENANCE TỐI THIỂU (Q4)
- Finding/Recommendation: manifest cho mỗi job gồm — `job_id`, `schema_version`, thời điểm UTC; ĐẦU VÀO: sha256, byte, w×h, định dạng đo được, nguồn tạo, tình trạng quyền, tham chiếu consent, danh sách biến đổi tiền xử lý; YÊU CẦU: provider, model ID, ngày đọc hợp đồng, tham số gửi (băm prompt; prompt lưu theo mức phân loại dữ liệu, steps, seed, width, height, guidance), ước lượng neurons, request ID/mã tương tự nếu API trả về (UNKNOWN có hay không), HTTP status, độ trễ, số lần thử (=0 retry); ĐẦU RA: sha256, byte, w×h, định dạng đo bằng magic bytes, cờ đã gỡ metadata; QC: điểm theo từng chiều, người chấm, lỗi chí tử; sổ cái ngân sách; tham chiếu bản chụp điều khoản + ngày. Không đưa token, base64, URL ảnh hay prompt thô vào log; log chỉ ghi kích thước/băm. ID tài khoản được coi là thông tin nhạy cảm và che trong đường dẫn ghi nhận.
- Acceptance test: JSON Schema cho manifest + test validate; quét bí mật trên repo/log; kiểm tra log không chứa base64.

### CLA-300-07 — P2 / ĐIỀU KIỆN NGHIỆM THU KỸ THUẬT BỔ SUNG (Q8)
- Finding: đồng ý KAI-300-07 (điểm trung bình dễ che lỗi chí tử). Bổ sung kiểm tra khách quan: kích thước đầu ra đúng yêu cầu; định dạng bằng magic bytes; decode thành công; phát hiện ảnh trống/đồng nhất (độ lệch chuẩn); khoảng cách băm tri giác giữa ảnh vào đã thu nhỏ và ảnh ra cho P300-02 như chỉ báo phụ, không phải tiêu chí PASS duy nhất; P300-05: kiểm tra xem `seed` có cho kết quả lặp lại hay không là một thí nghiệm riêng (UNKNOWN), so sánh bằng phân phối độ tương đồng và độ trễ, không đòi trùng pixel.
- Acceptance test: bộ kiểm tra khách quan chạy tự động trên ảnh mẫu; kết quả vào manifest; mọi fail chí tử → FAIL dù điểm trung bình đạt.

### CLA-300-08 — P1 / TÁCH ĐÔI NGUỒN SỰ THẬT: BA ĐỊNH DANH, HAI CÂY THƯ MỤC
- Finding: W300 hiện có ba tên và hai cấu trúc: Sandbox runtime `TRAO-DOI-VA-GIOI-THIEU` (cây `03_ARCHITECTURE`, `04_CODE`, `05_TEST`…), GitHub canonical `work/300/ROOM-HOP-AI-CREATIVE-SERVICE/` (`03_ARCHITECT`, `04_PLAN`, `05_BUILD/04_CODE/dashboard`…), và manifest Sandbox ghi `AI-IMAGE-AND-PHOTO-STUDIO`. Sandbox không có REVIEW_PACKET, HANDOFF, DOC-034/035; file review này và nhật ký bên dưới hiện nằm ở Sandbox. Work 99 chưa có Work ID 300 (theo nhật ký 2026-11-16) — chưa xác minh lại.
- Risk: nhật ký và biên bản bị tách đôi, mã build có thể rơi vào cây legacy/dashboard sai chỗ.
- Recommendation: theo HANDOFF, GitHub là canonical; Sandbox là bản làm việc/phản chiếu; Xu thêm một file PATH_MAP (tên ↔ ID ↔ đường dẫn); đăng ký W300 vào Work 99 không tái dùng ID; mã build vào đúng cây canonical, không ghi đè dashboard legacy.
- Acceptance test: người mới đọc PATH_MAP tìm đúng canonical DOC-034/035 trong một bước; không còn tài liệu active nào chỉ tồn tại ở một phía mà không có con trỏ.

## 4. Ranh giới bằng chứng
Đây là review tĩnh. Không có tài khoản, dashboard, phép thử runtime, kiểm thử bảo mật hay chất lượng ảnh nào được thực hiện; không phát sinh chi phí. Mọi con số neurons là suy ra từ giá công bố với giả định tile ghi ở CLA-300-03, chưa đối chiếu dashboard.

## 5. Bàn giao
Nộp cho Xu để hợp nhất vào DOC-034/DOC-035 canonical trên GitHub (Cla không có quyền ghi GitHub trong phiên này và không sửa các file đó). Review xong không phải cấp phép BUILD.
