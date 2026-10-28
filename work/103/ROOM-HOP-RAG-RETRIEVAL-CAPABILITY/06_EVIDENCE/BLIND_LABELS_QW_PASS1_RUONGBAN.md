# Work 103 — BẢN NHÃN MÙ LẦN 1 (QW / QE-QA) — 50 câu, có căn cứ từng câu

- **Người gán nhãn:** Qw (QE/QA — kiểm thử độc lập), `annotator_id = QW-QE-PASS1`
- **Ngày:** 2026-10-28 (UTC+07:00)
- **Đầu vào được dùng:** `05_TEST/BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json` (chỉ `id` + `query`) và corpus đã commit trong `05_TEST/EVAL_SET.json` → mảng `documents[]` (8 tài liệu).
- **Đầu vào KHÔNG dùng khi gán nhãn:** điểm retrieval, thứ hạng/xếp hạng, kết quả chạy hệ thống, metric baseline, và nhãn gốc của tác giả (`labeled_queries`, `no_answer_queries`).
- **Bản machine-readable:** `05_TEST/BLIND_LABELS_QW_PASS1.json` (= `06_EVIDENCE/BLIND_LABELS_QW_PASS1.json`), sha256 `19d2eb83ffe9abc759168a33a6606c1276d8a2ac339048d64928e48135e4b5bd`
- **Fingerprint corpus (sha256, source_id+text, theo thứ tự file):** `1becd8a1309854599afdc72ea5fac91510a37b17b7c640ca45c6f5c37d40bf92`
- **Pool file sha256:** `dd2a2a11a3e85b6066343b8c51c641154d1a200cbcb2d204ab0a3f7468a22f93` · **EVAL_SET file sha256:** `ab60cabdeee6254e11ee6889c20b6f2e68cd5072687bafcb314fb7c9a37c9f07` · **HEAD:** `5f91f3e`
- **Trạng thái:** `PASS1_INDEPENDENT_NOT_FROZEN_NOT_FOR_METRIC_REPORTING` — chưa đối chiếu với người nhãn thứ 2, chưa resolve bất đồng, chưa freeze; **không** dùng để báo cáo metric.

## Quy tắc diễn giải đã áp dụng (nhất quán cho cả 50 câu)

| Mã | Quy tắc |
|---|---|
| R1 | `answerable=true` chỉ khi một tài liệu trong corpus **nêu tường minh** dữ kiện được hỏi. Câu hỏi thêm đối tượng/thuộc tính không có trong corpus (khu C, khu A, chi nhánh Hà Nội/Đà Nẵng/miền Trung, marketing, người trực NOC, số giao thực tế, taxi, per diem Nhật Bản, Zalo, độ dài mật khẩu, chu kỳ đổi token, mức trần khách sạn, SLA/giờ, thay thiết bị, trạng thái khắc phục, số liệu/người ký/xếp hạng riêng của quý 4) → `false`. |
| R2 | Câu liệt kê/tổng hợp ("gồm những gì", "các bước nào") → `true` nếu đúng một tài liệu liệt kê nội dung đó. |
| R3 | Câu cần gộp nhiều nguồn → `true`, liệt kê đủ mọi `source_id` đóng góp vật chất. |
| R4 | Câu hỏi số nhiều nhưng corpus chỉ có **một** thể hiện duy nhất → `true` + `confidence=MEDIUM`, đánh dấu chờ tài phán. |
| R5 | Sai đơn vị/sai vai: "30 phút" là ngưỡng escalate của kỹ thuật viên, không phải SLA xử lý của NOC tính bằng giờ → Q027 `false`. |
| R6 | Kế hoạch ≠ thực tế: ngày/số lượng trong kế hoạch không chứng minh kết quả đã xảy ra → Q041 `false`. |
| R7 | Mọi câu `answerable=false` mang `expected_source_ids = []` (theo labeling_rules mục 3). |

**Tự kiểm tra sau khi gán nhãn (chỉ dùng text corpus, không dùng điểm/hạng):** đếm tỷ lệ token truy vấn xuất hiện trong từng tài liệu, để bắt (a) tài liệu bị bỏ sót khi nhãn `false`, (b) tài liệu khai quá tay khi nhãn `true`. Kết quả: không có câu `false` nào có tài liệu phủ ≥60% token mà vẫn trả lời được; các câu `true` có phủ thấp đều là câu liệt kê/tổng hợp (R2/R3/R4).

**Tổng phân phối nhãn:** answerable=true: **20** · answerable=false: **30** · confidence HIGH: 42 · MEDIUM: 8 (Q018, Q020, Q026, Q028, Q032, Q034, Q038, Q040).

Ký hiệu: ONT=`docs/bien-ban-hop-tuan-ont.md`, QT=`docs/quy-trinh-xu-ly-su-co-mang.md`, GH=`docs/ke-hoach-giao-hang.md`, DT=`docs/bao-cao-doanh-thu.md`, KL=`docs/ky-luat-hop.md`, BM=`docs/bao-mat-thong-tin.md`, NV=`docs/nhiem-vu-tuan-42.md`, CT=`docs/quy-dinh-cong-tac.md`.

## Bảng nhãn lần 1 — căn cứ theo từng câu

| ID | Query | answerable | expected_source_ids | Conf | Căn cứ |
|---|---|---|---|---|---|
| Q001 | doanh thu quý 4 của chi nhánh Hà Nội | false | — | H | Corpus chỉ có báo cáo doanh thu QUÝ 3 (120% kế hoạch); quý 4 chỉ là DỰ BÁO "tăng trưởng ổn định", không có số liệu và không cắt theo chi nhánh; "Hà Nội" không xuất hiện ở tài liệu nào. |
| Q002 | kỷ luật họp tuần gồm những gì | true | KL | H | ky-luat-hop.md ghi toàn bộ: phạt đi muộn 50 nghìn, điện thoại chế độ im lặng, vắng mặt báo trước 1 ngày, họp 8 giờ sáng thứ hai. |
| Q003 | tín hiệu quang ONT khu C mạnh bao nhiêu dBm | false | — | H | Biên bản ONT chỉ ghi tín hiệu yếu ở KHU B và không ghi giá trị dBm cho bất kỳ khu nào; "khu C" và đơn vị dBm đều không có. |
| Q004 | quy trình xử lý sự cố mạng gồm các bước nào | true | QT | H | quy-trinh-xu-ly-su-co-mang.md liệt kê đủ 5 bước (ticket → LOS/RX power → vệ sinh đầu nối → escalate NOC >30 phút → ghi biên bản). |
| Q005 | văn phòng chi nhánh Đà Nẵng đạt doanh thu quý 4 bao nhiêu | false | — | H | Không có số liệu doanh thu quý 4, không có "văn phòng chi nhánh Đà Nẵng"; báo cáo chỉ ở mức chung cho quý 3. |
| Q006 | quy định công tác xa gồm những nội dung gì | true | CT | H | quy-dinh-cong-tac.md: vé máy bay cần quản lý trực tiếp duyệt, per diem 500 nghìn/ngày, khách sạn hoàn qua kế toán, báo cáo công tác trong 3 ngày. |
| Q007 | LOS ở khu C xuất hiện lúc mấy giờ | false | — | H | Dòng "LOS alarm xuất hiện lúc 3 giờ sáng" gắn với sự cố KHU B; corpus không nhắc khu C nên không gán mốc giờ cho khu C. |
| Q008 | chính sách bảo mật thông tin có những quy định nào | true | BM | H | bao-mat-thong-tin.md: không chia sẻ mật khẩu qua email, token lưu vault, xóa dữ liệu khách hàng sau 30 ngày, rò rỉ phải báo ngay cho bảo mật. |
| Q009 | RX power của ONT khu A là bao nhiêu dBm | false | — | H | Corpus không chứa giá trị đo RX power/dBm nào; chỉ ghi người phụ trách kiểm tra RX power, không có "khu A". |
| Q010 | kế hoạch giao hàng xi măng gồm những mốc nào | true | GH | H | ke-hoach-giao-hang.md: quý 4, khách đặt 5000 tấn, lịch giao 5/11, 12/11 và 19/11. |
| Q011 | ai phê duyệt vé máy bay cho chuyến đi Hà Nội tuần sau | false | — | H | Có quy định chung "quản lý trực tiếp" duyệt vé, nhưng corpus không có chuyến đi Hà Nội tuần sau và không định danh người cụ thể. |
| Q012 | báo cáo doanh thu nêu những kết quả gì | true | DT | H | bao-cao-doanh-thu.md: quý 3 đạt 120% kế hoạch, sales dẫn đầu doanh số, dự báo quý 4 ổn định, kế toán xác nhận 5/10. |
| Q013 | doanh thu quý 4 của bộ phận marketing đạt bao nhiêu tiền | false | — | H | Không có số liệu quý 4; không tài liệu nào nhắc bộ phận marketing (chỉ có "sales"). |
| Q014 | nhiệm vụ tuần 42 gồm những việc nào | true | NV | H | nhiem-vu-tuan-42.md liệt kê 4 mục: báo cáo tín hiệu quang, hỗ trợ triển khai sales tại chi nhánh, cập nhật vault token trước thứ sáu, chuẩn bị biên bản. |
| Q015 | lịch giao xi măng cho khách hàng chi nhánh miền Trung tháng 12 | false | — | H | Lịch giao chỉ có 3 mốc tháng 11; không có "chi nhánh miền Trung" và không có mốc tháng 12. |
| Q016 | các bước cần làm khi nhận ticket khách hàng là gì | true | QT | H | Quy trình tuyến tính từ bước 1 (tiếp nhận ticket) đến bước 5 trong cùng tài liệu. |
| Q017 | ai chịu trách nhiệm xử lý sự cố ONT khu C trước 15/11 | false | — | H | Hạn chót trong corpus là 20/10 cho sự cố KHU B; không có khu C, không có mốc 15/11. |
| Q018 | các biện pháp xử lý tín hiệu quang yếu được nêu là gì | true | ONT, QT | M | Hai nguồn bổ sung nhau: biên bản nêu sự cố khu B + đề xuất vệ sinh đầu nối cáp quang; quy trình nêu kiểm tra LOS/do RX power và vệ sinh đầu nối quang. Không tài liệu nào gom thành một danh mục "biện pháp". |
| Q019 | mức phạt đi muộn họp của chi nhánh Hà Nội | false | — | H | Mức 50 nghìn thuộc "kỷ luật họp tuần của phòng"; corpus không gắn quy định nào với chi nhánh Hà Nội. |
| Q020 | những trường hợp nào cần báo cho bộ phận bảo mật | true | BM | M | Nghĩa vụ nêu rõ ("Rò rỉ thông tin phải báo ngay cho bảo mật"), nhưng corpus chỉ cung cấp ĐÚNG MỘT trường hợp cho câu hỏi số nhiều. |
| Q021 | token API phải đổi bao nhiêu ngày một lần | false | — | H | Corpus chỉ yêu cầu token lưu vault và "cập nhật vault token trước thứ sáu"; không định nghĩa chu kỳ đổi token theo ngày, không nói "token API". |
| Q022 | các khoản hỗ trợ trong chuyến công tác gồm những gì | true | CT | H | Vé máy bay (cần duyệt), per diem 500 nghìn/ngày, khách sạn hoàn qua kế toán. |
| Q023 | khách sạn công tác được hoàn tối đa bao nhiêu tiền mỗi đêm | false | — | H | Chỉ ghi "Khách sạn hoàn qua kế toán" (cách thức), không có mức trần hoàn mỗi đêm. |
| Q024 | các mốc giao hàng trong kế hoạch là ngày nào | true | GH | H | "Lịch giao: 5/11, 12/11 và 19/11". |
| Q025 | doanh thu quý 3 của chi nhánh Hà Nội bằng bao nhiêu phần trăm | false | — | H | Con số 120% là doanh thu quý 3 ở cấp báo cáo chung, không phải của chi nhánh Hà Nội; corpus không cắt theo chi nhánh. |
| Q026 | những việc nào cần hoàn thành trước thứ sáu | true | NV | M | Mục duy nhất có mốc "trước thứ sáu" là "Cập nhật vault token hệ thống trước thứ sáu". |
| Q027 | NOC phải xử lý LOS trong bao nhiêu giờ theo SLA | false | — | H | "30 PHÚT" là ngưỡng để kỹ thuật viên escalate, không phải SLA xử lý của NOC và không phải đơn vị giờ; corpus không có SLA cho NOC. |
| Q028 | các thông tin nào liên quan đến token được nhắc đến | true | BM, NV | M | Token truy cập phải lưu vault (BM) và cập nhật vault token hệ thống trước thứ sáu (NV). |
| Q029 | danh sách khách hàng nợ quá hạn quý 4 | false | — | H | Corpus không có danh sách công nợ/khách hàng nợ quá hạn. |
| Q030 | các quy định về tham gia họp tuần là gì | true | KL | H | Hop 8 giờ sáng thứ hai; vắng mặt báo trước 1 ngày; điện thoại im lặng; đi muộn phạt 50 nghìn. |
| Q031 | ai duyệt chi phí taxi đi công tác | false | — | H | Phạm vi phê duyệt chỉ lập cho "vé máy bay"; không tài liệu nào nhắc chi phí taxi. |
| Q032 | các thông tin nào được nêu về doanh thu và sales | true | DT, GH, NV | M | Doanh thu: quý 3 đạt 120%, sales dẫn đầu doanh số, dự báo quý 4, kế toán xác nhận 5/10 (DT). Sales còn ở vai phụ trách giao hàng (GH) và hỗ trợ triển khai sales tại chi nhánh (NV). |
| Q033 | ONT khu B được thay thiết bị vào ngày nào | false | — | H | Corpus không ghi việc THAY THIẾT BI cho khu nào; chỉ có đề xuất vệ sinh đầu nối và hạn chót 20/10. |
| Q034 | những công việc nào liên quan đến biên bản họp | true | QT, NV, ONT | M | Bước 5 quy trình: ghi kết quả vào biên bản; NV: chuẩn bị biên bản họp tuần tới; ONT là tài liệu biên bản họp được lập. |
| Q035 | lịch họp tuần của chi nhánh Hà Nội chiều thứ sáu | false | — | H | Kỳ luật ghi hop 8 GIỜ SÁNG THỨ HAI của phòng; không có lịch "chiều thứ sáu", không có thông tin theo chi nhánh. |
| Q036 | các bước cuối của quy trình xử lý sự cố là gì | true | QT | H | Bước 4 và bước 5: escalate NOC khi LOS >30 phút; ghi nhận kết quả vào biên bản. |
| Q037 | doanh thu từng nhân viên sales trong tháng 10 | false | — | H | Báo cáo chỉ ở cấp bộ phận; không có doanh thu theo nhân viên, không có số liệu tháng 10. |
| Q038 | những nghĩa vụ sau chuyến công tác gồm những gì | true | CT | M | Báo cáo công tác trong 3 ngày sau khi về; khách sạn hoàn qua kế toán (gắn với giai đoạn sau chuyến đi). |
| Q039 | mật khẩu vault phải có tối thiểu bao nhiêu ký tự | false | — | H | Chính sách chỉ cấm chia sẻ mật khẩu qua email và yêu cầu token lưu vault; không có yêu cầu độ dài tối thiểu. |
| Q040 | các thông tin nào về lịch họp và giờ họp được ghi lại | true | KL, ONT | M | KL: họp tuần của phòng 8 giờ sáng thứ hai; ONT: cuộc họp tuần ONT ngày 12/10. |
| Q041 | số lượng xi măng đã giao thực tế ngày 19/11 | false | — | H | Tài liệu là KẾ HOẠCH (5000 tấn được đặt, lịch có 19/11); không có số liệu giao THỰC TẾ. |
| Q042 | ai ký xác nhận doanh thu quý 4 | false | — | H | Xác nhận kế toán ngày 5/10 gắn với báo cáo QUY 3 và không nêu tên người ký; không có xác nhận cho quý 4. |
| Q043 | quy trình xử lý sự cố điện tại văn phòng | false | — | H | Quy trình trong corpus là sự cố MẠNG (LOS/RX power/đầu nối quang/NOC); không có quy trình sự cố điện. |
| Q044 | mức hỗ trợ per diem ở Nhật Bản | false | — | H | Per diem 500 nghìn/ngày là mức chung; corpus không phân theo quốc gia, không nhắc Nhật Bản. |
| Q045 | tín hiệu quang ONT khu C đã khắc phục xong chưa | false | — | H | Không có sự cố khu C và không có trạng thái "khắc phục xong" cho bất kỳ sự cố nào. |
| Q046 | ngày kế toán xác nhận doanh thu quý 4 | false | — | H | Ngày 5/10 là xác nhận số liệu cho báo cáo doanh thu QUY 3; không có ngày xác nhận cho quý 4. |
| Q047 | số ticket LOS khách hàng gửi tuần 42 | false | — | H | Corpus không có số lượng ticket LOS theo tuần; "tuần 42" chỉ gắn với danh sách nhiệm vụ. |
| Q048 | quy định bảo mật khi chia sẻ file qua Zalo | false | — | H | Chính sách nêu kênh bị cấm là EMAIL; không tài liệu nào nhắc Zalo. |
| Q049 | chi nhánh nào đạt doanh số cao nhất quý 4 | false | — | H | Doanh số dẫn đầu ghi ở cấp BỘ PHẬN (sales) cho quý 3; không có xếp hạng theo chi nhánh, không có số liệu quý 4. |
| Q050 | ai trực NOC lúc 3 giờ sáng ngày 12/10 | false | — | H | LOS alarm 3 giờ sáng và biên bản ngày 12/10 có tồn tại, nhưng corpus không ghi danh tính người trực ca/trực NOC. |

## Câu hỏi mở cần tài phán trước khi unblind/freeze

1. **Biên của câu liệt kê/tổng hợp (R2/R3/R4)** — Q018, Q020, Q026, Q028, Q032, Q034, Q038, Q040: chấp nhận danh sách partial/một thể hiện duy nhất là "hỗ trợ vật chất", hay yêu cầu corpus phải có phát biểu gộp tường minh? Nếu theo hướng chặt, Q020/Q026/Q038 có thể chuyển sang `false`.
2. **Q034** — có nên liệt kê `docs/bien-ban-hop-tuan-ont.md` không? Nó là *thể hiện* của biên bản họp, không phải phát biểu *về* công việc liên quan biên bản.
3. **Q032** — `bao-cao-doanh-thu.md` hỗ trợ rõ vế "doanh thu"; `ke-hoach-giao-hang.md` và `nhiem-vu-tuan-42.md` chỉ hỗ trợ vế "sales". Cần chốt việc khai 3 nguồn là bắt buộc hay chỉ chấp nhận 1 nguồn.
4. **Q027** — nếu dự án định nghĩa "SLA" lỏng = mọi ràng buộc thời gian trong quy trình, câu này lật sang `true` với QT. Bản nhãn lần 1 giữ `false` theo R5.
5. **Nhóm near-miss đổi thực thể** (Q003, Q007, Q009, Q017, Q045) — xác nhận giữ `false` thay vì tạo nhãn trung gian "partially answerable" (pool V1 không có giá trị này).
6. **Q001 vs Q046/Q042/Q049** — cả nhóm "quý 4 + phân vị/đối tượng mới" đều `false`; cần đảm bảo người nhãn lần 2 dùng cùng phép suy diễn R1 để tránh bất đồng giả tạo.

## Bước tiếp theo

- Người nhãn độc lập thứ 2 (KHÔNG xem tệp này) hoàn tất pass 2 trên cùng pool + cùng fingerprint corpus `1becd8a1…`.
- So khớp từng câu: đồng thuận → giữ; bất đồng → tài phán theo 6 câu hỏi mở trên, ghi quyết định và người quyết định.
- Sau khi resolve: đóng băng phiên bản bộ nhãn có nhãn độc lập (tính sha256 của tệp đã freeze, ghi vào Nhật ký) rồi mới unblind so với nhãn tác giả; chỉ khi đó bộ câu hỏi mới đủ điều kiện báo cáo metric.
