# WORK 98 - ONT care — BIÊN BẢN

## Khởi tạo
- Work ID: 98
- Tên: ONT care
- Mục tiêu: Khảo sát và thu thập ý kiến đóng góp của tất cả AI về công nghệ, kiến trúc, rủi ro và hướng phát triển ONT care.
- Trạng thái: OPEN / SURVEY
- Chủ trì tổng hợp: Xu
- Quyền quyết định cuối: Vinh

## Quy định ghi nhận
- Không ghi đè biên bản.
- Các đóng góp được append theo thời gian.
- Không biến ý kiến thành quyết định nếu chưa có bước tổng hợp và xác nhận.
- Phân biệt rõ FACT / EVIDENCE / OPINION / HYPOTHESIS / DECISION.
- Mọi AI đóng góp phải định danh bằng AI Message Header v1.0.

## 2026-09-30 — KHỞI TẠO
Vinh đặt Work 98 là "ONT care" và yêu cầu lấy ý kiến đóng góp của tất cả AI. Xu khởi tạo hồ sơ khảo sát và biên bản làm việc trong Sandbox Work 98.

### Việc tiếp theo
1. Gửi cùng một bộ câu hỏi cho các AI.
2. Mỗi AI khảo sát độc lập.
3. Thu evidence/test nếu AI có tuyên bố kỹ thuật cần kiểm chứng.
4. Xu tổng hợp thành các nhóm: kiến trúc, công nghệ, rủi ro, cơ hội, test cần làm.
5. Vinh chốt hướng trước khi implementation.


## 2026-09-30 — KHÓA MỤC TIÊU SẢN PHẨM CUỐI CÙNG
- Mục tiêu cuối cùng của Work 98: hệ thống ONT care có 3 bề mặt/chức năng chính.
- 01 — Dashboard PC: quản lý và vận hành toàn diện.
- 02 — App di động dùng chung cho thợ và khách hàng; dùng `acc` để định danh và phân vai, từ đó hiển thị chức năng phù hợp theo vai trò.
- 03 — Về mặt sản phẩm/role có 3 nhóm sử dụng: vận hành PC, thợ, khách hàng; không mặc định phải triển khai thành 3 ứng dụng độc lập.
- Hướng kiến trúc cần khảo sát: một mobile app dùng chung cho thợ + khách hàng với role-based access (phân quyền theo vai trò) bằng `acc`.
- Không khóa công nghệ trước khảo sát. Các AI phải đánh giá tính khả thi, ưu/nhược điểm, bảo mật, vận hành và evidence thực tế của mô hình này.
- Nguyên tắc: Evidence trước, Architecture Before Code; Vinh là quyết định cuối cùng, Xu tổng hợp ý kiến các AI.


## 2026-09-30 — CLA / AI SURVEY ROUND 01 — ONT CARE
- CLA cung cấp bộ khảo sát dùng chung cho tất cả AI trong Work 98.
- Phạm vi khảo sát gồm 10 nhóm: Architecture; ONT/TR-069/ACS; Network Diagnostics; PC Dashboard; Mobile App; `acc` + Role; AI/Agent/Automation; Security/Privacy; Reliability/Compatibility; Technology Radar.
- Luật vòng 01: không viết code, không tranh luận/phản biện AI khác; mỗi đề xuất phải nêu công nghệ, mục đích, lý do, evidence nếu có, rủi ro, test case + tiêu chí pass/fail và ưu tiên P0/P1/P2.
- Evidence phải gắn nhãn [Verified] / [Docs] / [Experience] / [Assumption]; không được bịa evidence.
- Cuối bài mỗi AI phải đưa Top 5 công nghệ cần test đầu tiên, Top 3 rủi ro và các điểm chưa chắc cần người/thiết bị thực tế xác nhận.
- Quy ước nộp bài: `SURVEY-R01_<tên AI>` để Xu đối chiếu.
- Khung tổng hợp của Xu: ma trận công nghệ × AI; phân loại đồng thuận/bất đồng/chỉ một AI nêu; ưu tiên evidence [Verified]/[Docs]; gộp danh sách test; xác định vùng mù cần xác nhận thực tế.
- Đây là bộ câu hỏi khảo sát, chưa phải quyết định kiến trúc hay công nghệ cuối cùng.


## 2026-10-02 — GÓP Ý VỀ CÁCH GHI NHẬN VÀ TỔNG HỢP
- **TÊN:** Co (ChatGPT)
- **CHỨC DANH:** Thư ký AI — ghi nhận Work 98
- **NGÀY:** 2026-10-02
- **GIỜ-PHÚT:** 06:15 (UTC+7; thời điểm ghi nhận theo thời gian hội thoại)
- **NỘI DUNG:** Góp ý của Xu: các ý kiến góp ý cũng là nội dung biên bản xây dựng Work 98; ghi trực tiếp vào biên bản chính, ghi chung để Xu tổng hợp. Không tạo bản ghi riêng cho từng AI hoặc tách góp ý ra khỏi biên bản chính.
- **TRẠNG THÁI:** Quy ước ghi nhận được Xu xác nhận; áp dụng cho các lần ghi tiếp theo.


## 2026-10-02 — OUT / AI: DIRECT ONT ACCESS SURVEY R01
- **TÊN:** Grok (xAI)
- **CHỨC DANH:** Senior Systems Engineer – Direct ONT Access Survey
- **NGÀY:** 2026-10-01
- **GIỜ-PHÚT:** 14:32 UTC
- **NỘI DUNG:** Grok đề xuất khảo sát truy cập ONT trực tiếp trong LAN, gồm: (1) phát hiện ONT qua DHCP, ARP, mDNS, SSDP/UPnP, ICMP/ARP scan và gateway detection; (2) nhận diện thiết bị bằng OUI/MAC, HTTP headers/title, HTML/JS fingerprint, hostname; (3) truy cập Web GUI/local API qua HTTP(S), WebSocket, REST/JSON, form POST và session; (4) khám phá API bằng DevTools, Burp/mitmproxy, Wireshark và phân tích JS; (5) xác thực Basic/Digest/form/cookie/CSRF/JWT và duy trì session; (6) thu thập Wi-Fi như SSID, channel, clients, RSSI, TX/RX; (7) thu thập LAN, DHCP lease, ARP/MAC table, bridge; (8) trạng thái WAN; (9) thông tin quang/GPON như RX/TX power, nhiệt độ, LOS/LOF; (10) system/event/log; (11) fingerprint firmware; (12) pipeline đề xuất Discovery → Fingerprint → Auth → Capability Detection → Collector → Parser → Normalizer → Local Cache; (13) môi trường collector: Android, Windows, Raspberry Pi, router, browser/PWA, thiết bị riêng hoặc hybrid; đề xuất thử Raspberry Pi/mini-PC Linux trước; (14) kiểm thử hoạt động khi Internet down nhưng LAN/ONT còn hoạt động; (15) schema dữ liệu ONT gồm identity, WAN, Wi-Fi, LAN, optical, system; (16) bảo mật: mã hóa credential, không gửi qua WAN, read-only, giới hạn tốc độ login; (17) adapter theo vendor/model/firmware; (18) retry/backoff, fallback endpoint, refresh session, phát hiện đổi IP; (19) đo hiệu năng discovery/login/collection/polling/CPU/RAM; (20) Technology Radar P0/P1/P2; (21) Top 5 test: DHCP/ARP discovery, HTTP fingerprint, login/session, Wi-Fi client list, offline scenario; (22) Top 3 rủi ro: firmware làm hỏng endpoint, rò rỉ credential, chứng chỉ self-signed/MITM trong LAN; (23) điểm chưa rõ: endpoint/schema của từng model, khả năng lộ optical/RSSI, giới hạn session/polling đồng thời; (24) kết luận của AI: ưu tiên khảo sát DevTools + HTTP fingerprint + capability probing + collector Linux; thử đầu tiên trên ONT thật trong cùng LAN, lấy Wi-Fi client list và optical stats nếu có khi Internet ngắt.
- **EVIDENCE / ĐỘ TIN CẬY:** Bài khảo sát gắn nhãn [Docs], [Experience] và [Assumption] theo từng mục; nhiều khả năng và tiêu chí PASS/FAIL cần xác nhận trên ONT thực tế. Đây là ý kiến khảo sát, chưa phải quyết định kiến trúc của Work 98.
- **TRẠNG THÁI:** Đã ghi nhận để Xu tổng hợp; chưa phê duyệt triển khai.


## 2026-10-02 — OUT / AI: GROK — DIRECT ONT ACCESS SURVEY R01
- **TÊN:** Grok (xAI)
- **CHỨC DANH:** Technology Researcher – Direct ONT Access
- **NGÀY:** 2026-10-02
- **GIỜ-PHÚT:** 06:04 (UTC+7; theo header nguồn)
- **NỘI DUNG:** Grok đề xuất phát hiện ONT bằng Default Gateway + ARP + MAC/OUI + HTTP probe, tùy chọn mDNS/SSDP; nhận diện đa tín hiệu qua OUI, HTTP title/header, favicon, model/serial và hostname. Khảo sát Web GUI/local API qua HTTP(S), XHR/JSON/XML; khám phá endpoint bằng DevTools, replay log, phân tích JS và so sánh trước/sau đăng nhập. Xác thực form/cookie/CSRF, session isolation; giữ credential trong memory hoặc vault mã hóa, không plaintext. Thu thập Wi-Fi (SSID/channel/band/client/RSSI tùy model), LAN/DHCP/port, WAN status, optical/GPON và system logs. Đề xuất Capability Profile + Adapter theo vendor/model/firmware; pipeline Discovery → Fingerprint/Capability Probe → Auth → Collector Workers → Raw Store → Parser → Normalizer → Local Cache/Change Detection → Sync khi có Internet. Collector ưu tiên thử Raspberry Pi/mini-PC hoặc Android box always-on; Android/Windows là lựa chọn khác. Khi mất Internet, chuỗi đọc và lưu local cần tiếp tục hoạt động. Schema linh hoạt, ghi capability/field thiếu và completeness; giai đoạn đầu READ-only, timeout/rate limit, quyền tối thiểu. Reliability gồm retry/backoff, re-auth, phát hiện đổi IP, cache last-known-good và health check.
- **ƯU TIÊN / KIỂM THỬ:** P0 gồm fingerprint đa tín hiệu, capability profile/adapter, offline full-chain, optical reading, session isolation và bảo vệ credential. Năm test: offline full chain; cùng model khác firmware; credential safety; optical + Wi-Fi client quality; rediscovery sau đổi IP/reboot (mục tiêu lấy lại dữ liệu trong ≤2 phút). Các ngưỡng là tiêu chí đề xuất của AI, chưa được xác minh thực nghiệm.
- **RỦI RO / ĐIỂM CHƯA RÕ:** Parser hỏng do firmware/GUI thay đổi; credential lộ hoặc collector bị chiếm; nhận diện nhầm thiết bị. Chưa rõ tỷ lệ ONT expose optical/RSSI, độ ổn định endpoint, hành vi Android background trên thiết bị/ISP tại Việt Nam, session timeout và concurrent login; cần thử trên ONT thật.
- **KẾT LUẬN CỦA AI:** Thử collector adapter-based trên Raspberry Pi/mini-PC hoặc Android box; test thực tế đầu tiên là Offline Full Chain trên ONT thật, xác nhận DISCOVER → IDENTIFY → AUTHENTICATE → READ → PARSE → NORMALIZE → STORE vẫn lấy được Wi-Fi, WAN và Optical nếu thiết bị hỗ trợ.
- **EVIDENCE / TRẠNG THÁI:** Nội dung nguồn phân biệt [Experience] và [Assumption]; các nhận định chưa có kiểm thử thực tế được nêu rõ là cần xác nhận. Đây là ý kiến khảo sát, chưa phải quyết định kiến trúc/triển khai của Work 98; ghi chung để Xu tổng hợp.


## 2026-10-02 — OUT / AI: META AI — DIRECT ONT ACCESS SURVEY R01

- **TÊN:** Meta AI – Muse Spark
- **CHỨC DANH:** Network / Embedded / Security Researcher – Direct LAN Access
- **NGÀY:** 2026-05-13
- **GIỜ:** 10:30 ICT (theo tài liệu nguồn)
- **NGƯỜI GHI NHẬN:** Co (ChatGPT) — Thư ký AI, Work 98
- **NGÀY/GIỜ GHI BIÊN BẢN:** 2026-10-02, giờ hệ thống hiện tại khoảng 06:xx UTC+7

### Nội dung đóng góp

Meta đề xuất discovery theo gateway/default route, ARP, OUI, DHCP server identifier, port 80/443; mDNS và SSDP là các nhánh bổ sung. Nhận diện ONT bằng fingerprint nhiều lớp (IP, OUI, HTTP title/header, body signature) và scoring, có bước user confirm khi tín hiệu không đủ.

Đề xuất truy cập GUI/API nội bộ bằng quan sát XHR/Fetch, phân tích JS/HTML, xử lý cookie/SID/CSRF; hỗ trợ HTML scraping fallback và runtime capability detection để giảm phụ thuộc endpoint cố định. Đề xuất collector kiến trúc 7 tầng: NetEnv → Discover → Fingerprint → AuthManager → Capability Probe → Collectors → Parser/Normalizer → LocalStore/Uploader; adapter theo vendor/model, schema linh hoạt với field optional và capabilities map.

Nguồn nêu các nhóm dữ liệu có thể thu thập: Wi-Fi/client RSSI và rate, LAN/DHCP/ARP, WAN, optical/GPON, system/log; đề xuất offline local collection, SQLite queue và mô hình Hybrid Android cho PoC/mass + Raspberry Pi cho lab/24-7.

### Ưu tiên và kiểm thử được đề xuất

- **P0:** gateway/ARP/port scan, OUI và HTTP fingerprint; auth/session; hidden API và HTML fallback; read-only allowlist; local offline queue.
- **P1:** SSDP, DHCP identifier, mDNS, cert pinning, runtime capability probe, adapter pattern.
- **P2:** WebSocket, USP Local Agent, browser extension, AI HTML parser.
- 5 test chính: discover-identify; auth/session; offline collection; đối chiếu Wi-Fi client quality; read-only guarantee.

### Rủi ro và điểm chưa xác minh

Rủi ro được nêu: phân mảnh firmware/API, credential và double NAT, ONT stability khi polling. Các điểm cần test ONT thật gồm endpoint theo model/firmware, CSRF, concurrent session, độ chính xác optical, truy cập khi bridge mode, credential trên tem, lockout, giới hạn polling và đổi IP LAN.

### Trạng thái

Đây là **ý kiến/đề xuất khảo sát của Meta AI**, chưa phải quyết định kiến trúc hay phê duyệt triển khai. Các tỷ lệ, mức độ phổ biến, ngưỡng và tuyên bố [Verified]/[Experience]/[Assumption] được giữ là phát biểu của nguồn, cần kiểm chứng bằng thử nghiệm thực tế trước khi dùng làm baseline. Ghi trực tiếp vào biên bản chính để Xu tổng hợp.


## 2026-10-02 — OUT / AI: DEEPSEEK — DIRECT ONT ACCESS SURVEY R01

- **TÊN:** DeepSeek
- **CHỨC DANH:** AI Research Assistant — Direct ONT Access Survey; vai trò gửi: CRO (theo chỉ định của Xu)
- **NGÀY:** 2025-06-17
- **GIỜ:** UTC+7 (nguồn không ghi giờ cụ thể)
- **NGƯỜI GHI NHẬN:** Co (ChatGPT) — Thư ký AI, Work 98
- **NGÀY/GIỜ GHI BIÊN BẢN:** 2026-10-02, giờ hiện tại không xác định chính xác

### Nội dung đóng góp

DeepSeek đề xuất chuỗi discovery gồm default gateway, ARP/neighbour table, DHCP fingerprint, mDNS/SSDP, subnet/port scan và OUI; ưu tiên gateway/ARP/OUI P0, DHCP và scan P1, mDNS/SSDP P2. Nhận diện ONT bằng kết hợp IP/MAC/OUI, HTTP title/headers, firmware/model và serial khi GUI cung cấp; nguồn nhấn mạnh không thể fingerprint chính xác nếu thiếu credential hoặc dữ liệu thiết bị không expose.

Về GUI/API, đề xuất HTTP(S), quan sát AJAX/XHR qua DevTools hoặc proxy, phân tích JavaScript, HTML scraping và endpoint discovery; cần xử lý session/cookie/CSRF, self-signed certificate và khác biệt firmware. Kiến trúc đề xuất: Discovery → Fingerprint → Authentication → Capability Detection → Data Collector → Parser → Normalizer → Local Cache → Sync tùy chọn. Multi-vendor theo plugin/common interface, capability profile, feature detection, normalizer và fallback.

Các nhóm dữ liệu dự kiến nếu ONT expose: Wi-Fi/client, LAN/DHCP/ARP, WAN, optical/GPON, system/event/log. Schema dùng optional fields, null/not_available khi thiếu; không giả định mọi ONT có cùng field. Đề xuất Raspberry Pi + Python Collector, requests/BeautifulSoup, SQLite local cho PoC; offline LAN operation là test quan trọng.

### Bảo mật, kiểm thử và rủi ro

Nguồn đề xuất mã hóa credential, không ghi password vào log, hạn chế credential trong LAN, ưu tiên HTTPS/certificate pinning, kiểm soát session, thử nghiệm lab và thiết kế read-only. Cần phân biệt request đọc với form/action có thể thay đổi cấu hình; nguồn đề nghị audit request.

5 test chính: ONT discovery; identification; authentication; data extraction; offline operation. 3 rủi ro: firmware update làm hỏng collector; credential leakage; ONT không expose đủ dữ liệu. Các unknown cần test ONT thật gồm endpoint/API, offline behavior, credential, firmware compatibility, optical data, concurrent session, rate limit và account lockout.

### Kết luận của nguồn

PoC tối thiểu được đề xuất: Default Gateway Identification + HTTP/HTTPS Access + HTML Scraping + Session/Cookie Handling + Local Cache; test đầu tiên: Discovery → Identification → Login → Extract Wi-Fi SSID. Nguyên tắc kết luận: chỉ xác nhận khả năng sau khi có ONT thật, số liệu và evidence cho toàn chuỗi DISCOVER → IDENTIFY → AUTHENTICATE → READ → PARSE → NORMALIZE → STORE → VERIFY.

### Trạng thái

Đây là **đóng góp/đề xuất của DeepSeek**, chưa phải quyết định kiến trúc hay phê duyệt triển khai. Các khẳng định [Docs]/[Experience]/[Assumption] và ngưỡng kiểm thử trong nguồn được giữ là nội dung do nguồn nêu, cần kiểm chứng thực tế; không xem là kết quả đã xác minh của Work 98. Ghi vào biên bản chính để Xu tổng hợp.


## GHI NHẬN ĐÓNG GÓP — DIRECT ONT ACCESS SURVEY R01

- TÊN: AI DIRECT-ACCESS-RESEARCHER
- CHỨC DANH: INDEPENDENT TECHNOLOGY SURVEY
- NGÀY: 2026-10-02
- GIỜ: 05:59:10 UTC+7
- NGƯỜI GHI NHẬN: Co
- PHÂN LOẠI: OPINION / HYPOTHESIS / TEST PROPOSAL; chưa phê duyệt, chưa triển khai.

### Nội dung khảo sát
Nguồn đề xuất khảo sát discovery bằng DHCP, ARP/neighbor, default gateway, mDNS, SSDP/UPnP, subnet/port scan và OUI; fingerprint tổ hợp IP/MAC-OUI/hostname/HTTP title/headers/login page, với serial/firmware chỉ xác minh sau xác thực. Nguồn ước lượng nhận diện ứng viên 80–90% nhưng chưa đưa dữ liệu thử nghiệm hỗ trợ con số này.

Khảo sát các đường truy cập HTTP/HTTPS, form login, HTML scraping, API/AJAX nội bộ và WebSocket; nhấn mạnh endpoint, token, phiên và parser có thể thay đổi theo firmware. Đề xuất profile năng lực theo model-firmware kết hợp feature detection, parser/plugin theo hãng và schema chuẩn có completeness/missing_fields.

Các nhóm dữ liệu dự kiến: Wi-Fi/clients, LAN/DHCP/ARP, WAN, optical/GPON, logs/events; mức sẵn có thay đổi theo model và firmware. Collector được so sánh trên Android, Windows, Pi/Mini PC, router, PWA, thiết bị chuyên dụng và hybrid; nguồn đề xuất Pi/Mini PC cho PoC. Yêu cầu offline: discovery, đăng nhập, đọc và lưu cục bộ khi WAN/Internet mất; đồng bộ trung tâm chỉ khi kết nối lại.

Nguyên tắc bảo mật đề xuất: read-only, allowlist đường dẫn, quản lý thông tin xác thực cục bộ, kiểm tra chứng chỉ, hạn chế phiên/đăng nhập và tránh thay đổi cấu hình. Nêu rủi ro firmware drift, chiếm phiên khách hàng, lộ credential và Collector bị xâm nhập. Đề xuất 5 test thực tế: discovery/fingerprint, login/read, offline, read-only 1 giờ, phục hồi sau đổi IP/reboot; thông số hiệu năng đều là ước tính cần đo trên ONT thật.

### Giới hạn nguồn
Phần cuối văn bản bị cắt tại rủi ro thứ hai (gây nhiễu hoạt động khách hàng); không có đầy đủ TOP 3 rủi ro và chữ ký kết thúc. Các tuyên bố [Verified], mức độ phổ biến, tỷ lệ 80–90%, giá và thời gian vẫn là nội dung do nguồn khảo sát nêu, chưa được xác minh độc lập. Giữ nguyên khác biệt và yêu cầu chứng cứ trên thiết bị thật trước mọi kết luận triển khai.

STATUS: Ghi nhận khảo sát để Xu tổng hợp; không phải quyết định kiến trúc hay phê duyệt triển khai.


## GHI NHẬN — CHỈ THỊ KHẢO SÁT ĐỘC LẬP DIRECT ONT ACCESS R01 (PI - PĨEL AI)

- TÊN NGUỒN: Pi - Pĩel AI
- CHỨC DANH: Chưa nêu trong nội dung gửi
- NGÀY/GIỜ: Không có timestamp riêng cho phản hồi; tài liệu mẫu yêu cầu AI điền DATE/TIME.
- NGƯỜI GHI NHẬN: Co
- PHÂN LOẠI: DECISION / RESEARCH INSTRUCTION — quy định phạm vi và format khảo sát, không phải quyết định kiến trúc hoặc triển khai.

### Nội dung chỉ thị
Nguồn cung cấp bộ khảo sát độc lập Direct ONT Access Survey R01, yêu cầu không viết code, không dựa vào khảo sát AI khác, không giả định kiến trúc/công nghệ đã chọn, không xếp hạng AI; phân loại chứng cứ thành [Verified], [Docs], [Experience], [Assumption], [UNKNOWN], không biến giả định thành fact, mọi đề xuất có test PASS/FAIL, không tự đặt số liệu hiệu năng thiếu evidence.

Phạm vi gồm: discovery; xác định đúng ONT/fingerprint; Web GUI và Local API; authentication/session; Wi-Fi; LAN/home network; WAN; optical/GPON; system/event/log; firmware fingerprint; data extraction engine; runtime Collector; offline; data model; security; multi-vendor/firmware; reliability; performance; technology radar P0/P1/P2; top 5 tests; top 3 risks; UNKNOWN; kết luận ba câu về công nghệ PoC, Collector thử đầu tiên và test thực địa đầu tiên.

Nguyên tắc xác minh khóa: không kết luận khả thi chỉ từ việc mở GUI bằng Chrome. Cần evidence trên ONT thật cho chuỗi DISCOVER → IDENTIFY → AUTHENTICATE → READ → PARSE → NORMALIZE → STORE → VERIFY, gồm số liệu thật, request/response hoặc evidence tương ứng, parser, normalized data và kết quả verify.

Sau khi các AI khảo sát độc lập mới tổng hợp Technology × AI Matrix, Evidence Consolidation, Risk Ranking, Real-world Test Plan và PoC Scope. R01 chưa khóa kiến trúc, chưa chọn công nghệ cuối cùng, chưa coi giả định là fact.

STATUS: Ghi nhận chỉ thị khảo sát. Không phải phê duyệt kiến trúc/PoC. Không tự triển khai khảo sát thay AI được chỉ định.


---

## SURVEY CONTRIBUTION — GEMINI PRO — DIRECT ONT ACCESS R01

- **Nguồn:** Gemini Pro (Collaborative Persona)
- **Chức danh nguồn:** Senior Systems & Integration Architect
- **Ngày nguồn:** 04/10/2026
- **Giờ nguồn:** 06:00 (múi giờ không nêu)
- **Người ký/ghi nguồn:** Kha - Gemini - Giám đốc LAB
- **Loại:** SURVEY / OPINION / HYPOTHESIS / TEST PROPOSAL; chưa phải quyết định kiến trúc, chưa phê duyệt triển khai.
- **Phạm vi:** 24 mục khảo sát Direct ONT Access R01.

### Nội dung ghi nhận
1. Discovery: subnet scan và suy luận default gateway; cảnh báo router phụ; đề xuất thử HTTP/HTTPS trên gateway, P0.
2. Identification: HTTP title, favicon hash, HTML signature; nêu mục tiêu match vendor/model >90%; rủi ro firmware/ISP tùy biến, P0.
3. Web GUI/local API: kiểm tra Network DevTools và replay AJAX/XHR sau xác thực; khả năng endpoint/session/CSRF thay đổi; P0.
4. Local API discovery: phân tích JS bundle và dò endpoint có kiểm soát; cảnh báo rate limit/IP blocking; P1.
5. Authentication/session: cookie/token, tự động xác thực và duy trì phiên; rủi ro mật khẩu đổi, concurrent session và lockout; P0.
6. Wi-Fi: parser radio/client list, MAC/IP/RSSI nếu có; firmware có thể chỉ cung cấp số lượng; P0.
7. LAN: ARP/DHCP client và trạng thái cổng; giới hạn quan sát khi có router phụ/Double NAT; P0.
8. WAN: trạng thái, IP WAN/PPPoE; có thể bị ẩn hoặc khác theo bridge/router mode; P0.
9. Optical/GPON: RX/TX power, nhiệt độ; quyền user/admin có thể khác; P0.
10. System/event/log: polling snapshot, log vòng và giới hạn quyền/dung lượng; P2.
11. Firmware fingerprint: version adapter/profile; rủi ro parser drift và chi phí bảo trì; P0.
12. Extraction engine: pipeline Discovery → Fingerprint → Auth → Collector → Parser → Normalizer → Cache; P0.
13. Runtime: Raspberry Pi/Mini PC edge collector, polling 48 giờ; mục tiêu tài nguyên <5% CPU, <100MB RAM (đề xuất nguồn, chưa đo kiểm); P0.
14. Offline: LAN-only execution và SQLite/local cache khi WAN down; phụ thuộc cấu hình/profile local; P0.
15. Data model: unified JSON schema với nullable/dynamic fields; analytics có thể khó do không đồng nhất; P0.
16. Security: read-only, mã hóa credential, xử lý TLS self-signed; nguồn khẳng định chỉ GET/chặn POST loại bỏ hoàn toàn rủi ro — ghi nhận là claim của nguồn, chưa xác minh; P0.
17. Multi-vendor: modular driver/adapter và capability registry; P1.
18. Reliability: timeout, exponential backoff, circuit breaker, graceful degradation; P0.
19. Performance: HTTP pooling/polling cấu hình; nguồn nêu nguy cơ ONT quá tải và mốc quét >2 lần/giây nhưng chưa cung cấp chứng cứ đo; P0.
20. Radar: P0 discovery/auth/optical/offline/read-only; P1 JS analysis/adapters/Wi-Fi mapping; P2 logs/ML fingerprint.
21. Top 5 tests: gateway discovery; auth/session; optical + Wi-Fi extraction; offline execution; read-only safety; kèm PASS/FAIL và evidence dự kiến.
22. Top risks: firmware drift; resource exhaustion/DoS; credential/authorization; có đề xuất cách kiểm thử.
23. Unknowns: anti-bot/captcha/rate limit; API proprietary encoding; tác động thực lên CPU/VoIP/IPTV.
24. Kết luận của nguồn: HTTP/API local scraping + session cookie automation + modular adapter; edge collector; ưu tiên test gateway discovery và authentication trên ONT thật.

### Bảo toàn trạng thái bằng chứng
Các nhãn [Verified], [Experience], [Docs] và các mức độ chắc chắn trong bản khảo sát là tự khai báo của Gemini Pro, không được xem là xác minh độc lập của Work 98. Các tiêu chí định lượng (match >90%, coverage 80%, tài nguyên CPU/RAM, tần suất polling) được ghi như ngưỡng/giả thuyết kiểm thử do nguồn đề xuất, không phải kết quả thực nghiệm. Chưa có model ONT, firmware, log hoặc dữ liệu thử nghiệm đính kèm.

**Trạng thái:** Đã ghi nhận đóng góp khảo sát; chờ Xu tổng hợp/đánh giá. Không phê duyệt kiến trúc hay triển khai PoC.

---

## REVIEW CONTRIBUTION — PI AI — R01 DIRECT ONT ACCESS

- **Nguồn:** Pi AI
- **Chức danh:** Không nêu trong nội dung ký
- **Ngày/giờ nguồn:** Không nêu trong nội dung
- **Người ghi nhận:** Xu / Co ghi nhận nội dung do người dùng chuyển tiếp
- **Loại:** REVIEW / OPINION / PROPOSED TEST-PLAN REFINEMENTS; chưa phải quyết định phê duyệt.

### Nhận xét tích cực
Nguồn đánh giá R01 có tư duy khảo sát tốt: không khóa kiến trúc trước evidence; phân biệt các mức evidence; yêu cầu chứng minh chuỗi discovery → verify; ưu tiên ONT thật; có offline test; đã xét multi-vendor/firmware. Nguồn nhấn mạnh Web GUI truy cập được không đồng nghĩa Collector có thể tự động đọc dữ liệu.

### Các đề xuất cần xem xét
1. **Device classification:** tách ONT bridge, router, gateway, có/không Wi-Fi, operator-managed và third-party router behind ONT; mỗi kết luận ghi applicable device class / not applicable to.
2. **Network topology:** ghi vị trí Collector/ONT, subnet, broadcast domain, routing, VLAN, client isolation, management IP và data-plane IP; chưa rõ thì đánh dấu UNKNOWN, không mặc định cùng LAN có thể thấy nhau.
3. **Access capability:** phân biệt reachability, authentication và quyền đọc; lập capability matrix theo field/page/endpoint, user role, readable status và evidence.
4. **Read-only:** HTTP method không đủ chứng minh an toàn; phân loại endpoint READ_SAFE, READ_WITH_SIDE_EFFECT_RISK, WRITE, DESTRUCTIVE, UNKNOWN. Đề xuất snapshot cấu hình trước/sau, request log, so sánh cấu hình, uptime/Wi-Fi checks; loại reboot/reset/upgrade khỏi vòng đầu.
5. **Raw evidence:** mỗi normalized field truy ngược được về device identity, timestamp, request metadata, raw response/screenshot, parser/normalizer version, confidence và validation; ví dụ RSSI có raw field, unit conversion và validation.
6. **Evidence Ladder:** E0 lý thuyết; E1 tài liệu; E2 quan sát thủ công; E3 request/response; E4 Collector đọc tự động; E5 normalized và verified. Đề xuất dùng thay hoặc bổ sung nhãn certainty hiện tại.
7. **Top 5 tests:** local reachability; offline access; authentication + read-only; data coverage đối chiếu GUI; firmware variation.
8. **Go/No-Go:** GO khi phát hiện/nhận diện đúng, xác thực hợp lệ, đọc tập field tối thiểu, offline hoạt động, không đổi cấu hình, có raw evidence và xử lý ít nhất một biến thể firmware; CONDITIONAL GO cho giới hạn model/field/quyền/API; NO-GO nếu không nhận diện/truy cập local, chỉ thao tác tay, API không kiểm soát, credential không an toàn, không chứng minh read-only hoặc không truy nguyên evidence.
9. **Rút gọn cấu trúc:** ba lớp Discovery & Access; Data Capability; Productization để giảm trùng lặp.
10. **Thứ tự PoC đề xuất:** device class/topology → reachability → discovery → identification → authentication → read-only proof → evidence capture → minimum extraction → offline → firmware variation → normalization → reliability/security → scale/performance.

### Kết luận nguồn
Nguồn nhận định R01 phù hợp làm khung nghiên cứu; để thành Test Plan thực chiến cần khóa Device Classification, Network Topology, Evidence Ladder và Go/No-Go. Nhấn mạnh phải chứng minh Collector tiếp cận đúng ONT, đúng quyền, đọc được dữ liệu, không gây side effect, lưu raw evidence và tái xác minh.

### Trạng thái
Đã ghi nhận góp ý; chưa sửa R01, chưa phê duyệt Test Plan, chưa quyết định PoC. Các nguồn ngoài được Pi AI dẫn (Cisco, vendor manuals, NCCS và manuals.plus) là tài liệu tham chiếu do nguồn nêu; chưa được Work 98 kiểm tra độc lập trong mục ghi nhận này.

---

## QWEN3.7 — DIRECT ONT ACCESS TECHNOLOGY SURVEY R01

- **AI:** Qwen3.7
- **Chức danh nguồn:** Independent AI Technology Surveyor (Direct ONT Access Specialist)
- **Ngày nguồn:** Friday, October 02, 2026
- **Giờ nguồn:** 10:00 AM UTC+7
- **Người ghi nhận:** Co
- **Phân loại:** SURVEY / EVIDENCE CLAIMS / OPINION / PROPOSED TEST PLAN
- **Trạng thái:** Ghi nhận đóng góp khảo sát; chưa xác minh độc lập, chưa phê duyệt kiến trúc, PoC hoặc triển khai.

### Nội dung khảo sát được ghi nhận

Qwen3.7 trình bày Direct ONT Access Survey R01 gồm 24 mục:

1. **ONT Discovery (P0):** ARP/subnet scan, ICMP và port 80/443; đề xuất test phát hiện IP ONT trên /24 trong <5 giây. Nguồn khẳng định mức [Verified] và nêu nguy cơ ICMP bị tắt, quét subnet lớn gây tải.
2. **ONT Identification (P0):** Kết hợp MAC OUI, HTTP title/headers và HTML form ID; đề xuất confidence >90% khi 3/4 tiêu chí khớp. Mức certainty [Verified] do nguồn tự gán; chưa được xác minh.
3. **Web GUI / Local API (P0):** HTML scraping kết hợp phân tích Network Tab để tái tạo endpoint nội bộ; nêu rủi ro token/CSRF, obfuscation và thay đổi HTML.
4. **Local API Discovery (P1):** Endpoint probing/traffic interception trong môi trường test; mục tiêu tìm endpoint có dữ liệu JSON/XML sau authentication.
5. **Authentication & Session (P0):** Quản lý cookie/session và credential vault; test 5 request liên tiếp, theo dõi timeout, concurrent session và nguy cơ ảnh hưởng phiên người dùng.
6. **Wi-Fi (P0):** Parse trang trạng thái/client API để lấy SSID, channel, bandwidth, security, client MAC/IP, RSSI, TX/RX rate; RSSI có thể không được expose.
7. **LAN / Home Network (P1):** DHCP lease/ARP table; nguồn cho rằng ONT thường là DHCP server chính, đồng thời nêu tình huống router phụ/double NAT.
8. **WAN (P1):** Parse dashboard WAN state, IP, gateway, DNS, connection type và uptime; lưu ý WAN IP có thể là private.
9. **Optical / GPON (P0):** Parse RX/TX power, temperature, ONU state; test yêu cầu giá trị RX power dạng số, không chỉ nhãn trạng thái.
10. **System / Event / Log (P2):** Snapshot log reboot, LOS/LOF, DHCP/auth events; giới hạn dung lượng và định dạng timestamp là rủi ro.
11. **Firmware Fingerprint (P0):** Capability/feature detection và fallback parser khi endpoint/GUI thay đổi; cảnh báo probing quá mức có thể gây treo hoặc cảnh báo bảo mật.
12. **Data Extraction Engine:** Pipeline đề xuất Discovery → Fingerprint → Authentication → Capability Detection → Collector → Parser → Normalizer → Local Cache (SQLite/JSON); đây là đề xuất nguồn, chưa phải kiến trúc được duyệt.
13. **Collector Runtime:** Raspberry Pi/Mini PC Linux làm collector cố định P0; Android làm công cụ kỹ thuật viên P1; nguồn đánh giá Browser/PWA không phù hợp cho chủ động quét LAN/ARP.
14. **Offline:** Test rút WAN nhưng vẫn discovery, login, lấy Wi-Fi/LAN/Optical và lưu local; nguồn coi đây là yêu cầu P0.
15. **Data Model:** JSON linh hoạt, nullable fields, vendor extensions/raw data; ví dụ schema được giữ như đề xuất, chưa chuẩn hóa.
16. **Security:** Read-only enforcement, ephemeral sessions, OS Keychain/Keystore; nhấn mạnh POST có thể mang side effect và cần xác minh endpoint trước khi dùng.
17. **Multi-vendor/Firmware:** Plugin/Adapter và feature detection; đề xuất thêm model qua cấu hình/parser mà không sửa core.
18. **Reliability:** Exponential backoff/circuit breaker; ví dụ 2s, 4s, 8s, sau 3 lỗi ngừng thử 15 phút là thông số đề xuất, chưa đo thực nghiệm.
19. **Performance:** Đo discovery/auth/collection/CPU-RAM; ngưỡng <10 giây và CPU <10% là tiêu chí đề xuất của nguồn, không phải kết quả benchmark.
20. **Technology Radar:** P0 ARP scan, scraping, session cookies, offline LAN, modular plugins; P1 hidden API, DHCP table, numeric optical; P2 WebSocket, mDNS/UPnP.
21. **Top 5 tests:** Offline LAN discovery/read; auto-login/session persistence; Wi-Fi client mapping; firmware fallback; read-only safety. Bao gồm procedure, pass/fail và evidence artifacts theo nội dung nguồn.
22. **Top 3 risks:** Parser hỏng do firmware; POST gây thay đổi cấu hình ngoài ý muốn; rò rỉ credential trên collector. Nguồn đề xuất thử trong lab cô lập, kiểm tra cấu hình trước/sau và kiểm tra lưu trữ/memory.
23. **Unknowns:** Endpoint/payload theo model ISP; rate limit; mức expose RSSI; tác động JS obfuscation và nhu cầu headless browser.
24. **AI Conclusion:** Đưa HTML scraping + capability probing, session management, plugin/adapter vào phạm vi PoC; thử đầu tiên trên Raspberry Pi/Mini PC Linux với Python/Go và SQLite; bài test đầu tiên là Offline LAN Discovery & Read-Only Extraction khi rút WAN.

### Ghi chú kiểm soát nguồn

Các nhãn [Verified], [Experience], [Docs], tỷ lệ 90%, ngưỡng thời gian/CPU và nhận định phổ quát trong bản khảo sát là phát biểu của Qwen3.7; biên bản chỉ ghi nhận xuất xứ, không xác nhận tính đúng đắn. Một số tiêu chí test (ví dụ port 80/443 hoặc OUI không khớp được xem là FAIL) cần được giữ là tiêu chí do nguồn đề xuất, không mặc định là điều kiện kỹ thuật đủ/đúng cho mọi ONT. Không có quyết định triển khai hoặc phê duyệt PoC trong nội dung gửi.


---

## BỔ SUNG XUẤT XỨ / CHỮ KÝ — QWEN3.7 DIRECT ONT ACCESS SURVEY R01

- **AI ghi trong nội dung:** Qwen3.7
- **Chức danh:** Independent AI Technology Surveyor (Direct ONT Access Specialist)
- **Ngày/giờ nguồn:** Friday, October 02, 2026, 10:00 AM UTC+7
- **Chữ ký cuối bản gửi lần này:** Cla - CTO
- **Người ghi nhận:** Co
- **Phân loại:** SOURCE ATTRIBUTION / DUPLICATE SUBMISSION
- **Trạng thái:** Nội dung 24 mục trùng với khảo sát Qwen3.7 R01 đã được append trước đó. Ghi nhận chữ ký/nhãn gửi bổ sung là “Cla - CTO”; không tạo bản khảo sát lặp lại và không diễn giải chữ ký này thành phê duyệt CTO. Nội dung khảo sát, các mức certainty, chỉ tiêu và đề xuất vẫn chưa được xác minh độc lập hoặc phê duyệt triển khai.


---

## CLAUDE (SONNET 5.5) — DIRECT ONT ACCESS SURVEY R01

- **AI:** Claude (Sonnet 5.5)
- **Chức danh nguồn:** Tham vấn kỹ thuật độc lập (khảo sát lý thuyết, không có ONT thật)
- **Ngày nguồn:** 02/10/2026
- **Giờ nguồn:** Không xác định
- **Chữ ký cuối bản:** Cla - CTO
- **Người ghi nhận:** Co
- **Phân loại:** SURVEY / DOCS / EXPERIENCE / ASSUMPTION / PROPOSED TEST PLAN
- **Trạng thái:** Đã ghi nhận; không có mục nào được nguồn gắn [Verified]. Chưa xác minh độc lập, chưa phê duyệt kiến trúc hoặc PoC.

### Nguyên tắc bằng chứng

Nguồn xác nhận không truy cập ONT thật trong phiên khảo sát; không đưa số liệu hiệu năng. Các nhận định được phân loại [Docs], [Experience] hoặc [Assumption], hoặc nêu là UNKNOWN. Kết luận nhấn mạnh phải chứng minh trọn chuỗi bằng evidence từ ONT thật; việc mở được Web GUI bằng Chrome chưa đủ chứng minh khả năng thu thập tự động.

### Tóm tắt 24 mục

1. **Discovery:** Ưu tiên gateway/DHCP và ARP/neighbor + OUI (P0); SSDP/UPnP P1, mDNS P2, subnet/port scan giới hạn là fallback P1. Gateway không mặc định là ONT trong bridge/cascade/double NAT. Đề xuất thử trên 5 topology; ngưỡng ≥80% do nhóm dự án chốt.
2. **Identification:** Fingerprint tổ hợp, confidence scoring; tín hiệu gồm hash tài nguyên trang login, HTML/title, headers/cookie/redirect, TLS cert, SSDP, OUI, hostname/DHCP vendor class. Model/firmware/serial có thể cần login. Chỉ gửi credential khi fingerprint đủ tin cậy; cần kiểm tra false positive.
3. **Web GUI/API:** Dùng DevTools/HAR khi thao tác thủ công, phân loại HTML nhúng, CGI/ASP, JSON/XML, XHR/AJAX, form POST; headless browser là fallback. Cần xác nhận quyền truy cập hợp pháp. Test tái hiện ít nhất một trường bằng HTTP client độc lập.
4. **Local API Discovery:** Phân biệt API có tài liệu với API nội bộ GUI; ghi method, headers, body, token/cookie, CSRF, WebSocket. Khi firmware đổi, fail an toàn thay vì âm thầm trả dữ liệu sai.
5. **Authentication/Session:** Phân loại form/cookie, token, challenge-response, client-side password transform, Basic/Digest, CSRF. Đề xuất OS credential vault, không log/gửi credential ra ngoài LAN, tài khoản read-only nếu có. Test session đồng thời, lockout và logout.
6. **Wi-Fi:** Phân loại từng trường là đọc được/không có/đọc lỗi; phân biệt RSSI phía ONT với phía client. UNKNOWN với ONT mục tiêu; đề xuất đối chiếu GUI và đo độc lập.
7. **LAN:** Có thể đọc port state, speed/duplex, DHCP lease, ARP/host tùy ONT; MAC table/VLAN/bridge thường không chắc có. Bản đồ chỉ từ ONT có thể không thấy thiết bị sau router/switch riêng.
8. **WAN:** Khảo sát state, IP, gateway, DNS, VLAN, connection type, uptime, counters, PPPoE, IPv6; WAN up không đồng nghĩa Internet thông.
9. **Optical/GPON:** RX/TX, nhiệt độ, voltage, bias, ONU state, LOS/LOF; có thể bị ẩn với user account. Health monitoring chỉ khả thi nếu credential được cấp đọc ổn định; đề xuất đối chiếu thiết bị đo/OLT.
10. **Logs:** Snapshot/polling phổ biến theo nhận định nguồn; polling có thể bỏ lỡ sự kiện ngắn. Test bằng sự kiện có chủ đích.
11. **Firmware fingerprint:** Khóa nhận dạng đề xuất vendor × model × hw_rev × fw_version × gui_version, kèm hash trang login; ưu tiên capability profile theo họ firmware thay vì chỉ theo model.
12. **Extraction engine:** Network Context → Candidate Finder → Fingerprinter → Session Manager → Read-only Capability Probe → Firmware Adapter Collector → Schema Validator/Normalizer → Local Store append-only → Health/Drift Monitor. Dữ liệu kèm source, confidence, collected_at. Chỉ là đề xuất, cần PoC.
13. **Runtime:** So sánh Android, Windows, Pi/mini PC, router-resident, PWA, thiết bị chuyên dụng và hybrid. Pi/mini PC là chuẩn tham chiếu; Android gần khách nhưng cần kiểm tra giới hạn nền; PWA được đánh dấu assumption cần test.
14. **Offline:** Kiểm tra phụ thuộc DNS/NTP/cloud/license, lưu local và sync sau; Android có thể đổi mạng khi Wi-Fi không có Internet (UNKNOWN). Test DISCOVER→STORE offline rồi sync không mất/trùng.
15. **Data model:** Core nhỏ + capability extensions; mỗi field có value, unit, status (ok/unavailable/unsupported/error), source, collected_at. Giữ raw snapshot đã che credential. Test ít nhất 3 ONT không sửa schema lõi.
16. **Security:** Rủi ro credential, cert tự ký/MITM, session hijack, rogue device, brute force, replay, collector compromise. Đề xuất TOFU + pin fingerprint; whitelist endpoint đọc đã duyệt, chặn POST ngoài login/logout, xác minh endpoint read không side effect; thử ONT giả để bảo đảm không gửi credential.
17. **Multi-vendor:** Ba lớp Adapter → Capability Profile → Canonical Schema; khai báo cấu hình cho ca đơn giản, code riêng cho ca đặc biệt. Test thêm ONT mới chỉ bằng adapter/profile.
18. **Reliability:** Bao gồm timeout, login fail, reboot, IP change, GUI/response lỗi, firmware drift, thiếu dữ liệu, crash, network change. Retry bounded/backoff, idempotent, không giả dữ liệu; phục hồi không mất dữ liệu/khóa tài khoản.
19. **Performance:** Không nêu số; đo discovery/login/domain collection, CPU/RAM/bandwidth, polling interval và ảnh hưởng GUI/ONT. Chưa có benchmark.
20. **Technology Radar:** P0 gateway/DHCP, ARP/OUI, composite fingerprint, HAR, HTTP session, capability profile, offline-first, field status, read-only whitelist. P1 SSDP, scan giới hạn, headless fallback, so sánh Android/Pi, snapshot logs. P2 mDNS, WebSocket, syslog, PWA, router-resident.
21. **Top 5 tests:** Full DISCOVER→VERIFY trên ≥3 ONT/firmware; offline; read-only/session safety; Wi-Fi/LAN accuracy; firmware drift. Từng test yêu cầu evidence và đối chiếu thực tế.
22. **Top 3 risks:** GUI/API nội bộ bị ISP tùy biến; thiếu credential/quyền hoặc trường bị ẩn; runtime nền tảng và side effects do polling/session. Nêu cách xác nhận qua test thực tế.
23. **Unknowns:** Model/firmware mục tiêu, fingerprint trước login, auth/session, trường Wi-Fi/optical/log khả dụng, Android local network/background, polling load, ISP/legal constraints, PWA.
24. **Conclusion:** Thử gateway/DHCP + ARP/OUI, fingerprint confidence, HAR rồi HTTP client, capability profile, read-only whitelist. Pi/mini PC làm baseline; Android so sánh sau. Test đầu tiên trên một ONT thật: DISCOVER→VERIFY read-only, đối chiếu từng field với GUI và snapshot cấu hình trước/sau.

### Ghi chú kiểm soát

Ngưỡng ≥80%, ≥95%, N thiết bị và mọi tiêu chí PASS/FAIL là đề xuất khảo sát, chưa phải kết quả đo hoặc quyết định dự án. Chữ ký “Cla - CTO” được ghi đúng như nguồn gửi, không suy diễn thành phê duyệt CTO. Không triển khai hay thay đổi R01 từ bản khảo sát này.


## AI CONTRIBUTION — Ka (ChatGPT), DIRECT ONT ACCESS — SURVEY R01

- **AI:** Ka — ChatGPT
- **Chức danh:** CSA / Technology Reviewer
- **Ngày nguồn:** 02/10/2026
- **Giờ nguồn:** 06:02, UTC+7
- **Phạm vi:** Direct ONT Access
- **Trạng thái nguồn:** Technical desk research và đề xuất PoC; độc lập; chưa kiểm chứng trên ONT thật; không có thiết bị thực nghiệm.
- **Nguồn/ký tên:** Ka - CSA. Nội dung tự nêu chưa ghi vào transcript.md của Work 802001 hay Work Sandbox trong phiên nguồn.
- **Phân loại:** OPINION / TECHNICAL SURVEY / PROPOSED TEST PLAN. Không phải quyết định kiến trúc hay phê duyệt PoC.

### Nội dung khảo sát (tóm tắt theo nguồn)
Ka trình bày 24 nhóm: (1) discovery bằng DHCP, ARP, gateway, subnet/TCP port scan, MAC/OUI, mDNS, SSDP, hostname, SNMP; (2) fingerprint nhiều tín hiệu, candidate/probable/confirmed; (3) GUI inspection qua HTTP(S), WebSocket, REST/JSON, XHR, JavaScript endpoint, form và HTML scraping; (4) phân biệt official API, internal GUI API và undocumented protocol; (5) authentication/session, credential protection và lifecycle; (6) Wi-Fi fields; (7) LAN/home-network sources và giới hạn; (8) WAN/Internet status; (9) optical/GPON metrics và cần xác minh đơn vị/ngưỡng; (10) logs/events và phân biệt snapshot/polling/stream; (11) firmware fingerprint; (12) pipeline Discovery → Identity/Fingerprint → Authentication → Capability Detection → Read-only Collectors → Parsers → Normalizer → Local Cache/Evidence → Verification; (13) so sánh Android, Windows, Pi/mini PC, router, PWA, chuyên dụng, hybrid; (14) offline/Internet-down test; (15) schema và trạng thái present/unsupported/unavailable/unknown/stale; (16) security, read-only enforcement và kiểm tra cấu hình trước/sau; (17) multi-vendor/firmware adapter; (18) reliability; (19) performance metrics cần đo, không công bố số liệu; (20) Technology Radar P0/P1/P2; (21) năm test ưu tiên; (22) ba rủi ro; (23) 15 unknowns; (24) kết luận và đề xuất test đầu tiên.

### Các điểm nhấn được nguồn đề xuất
- Ưu tiên PoC trên ONT thật: discovery và xác nhận đúng ONT, sau đó tái hiện một request đọc dữ liệu và đối chiếu GUI.
- Test trọng yếu: Internet mất nhưng ONT/LAN còn hoạt động; collector phải tiếp tục truy cập và lưu local theo nhóm dữ liệu đã hỗ trợ.
- Collector thử nghiệm local trên PC/mini PC; tách discovery, auth, adapter, parser, normalizer, local storage và verification.
- Read-only phải được kiểm chứng bằng danh sách request được duyệt và so sánh cấu hình ONT trước/sau; không mặc định GET luôn vô hại.
- Không công bố benchmark, khả năng endpoint hay kết quả PoC khi chưa có evidence thiết bị.

### Evidence / certainty / giới hạn
Nguồn phân biệt Docs, Experience, Assumption và UNKNOWN; chưa có ONT vật lý/runtime evidence, chưa chạy PoC, chưa chốt kiến trúc. Các công nghệ và PASS/FAIL nêu trong báo cáo là phương pháp/tiêu chí đề xuất, không phải kết quả đã đạt. Báo cáo chứa một số liên kết hình minh họa; chính nguồn xác nhận chúng không phải evidence PoC.

### Trạng thái biên bản
Ghi nhận đóng góp khảo sát độc lập; **chưa phê duyệt, chưa triển khai, không thay đổi baseline hoặc kiến trúc**. Bảo toàn các giới hạn và xuất xứ của nguồn.

## 2026-10-13 — XU: AUDIT SOURCE VÀ KẾ HOẠCH E2E
- TÊN: Xu
- CHỨC DANH: Work 98 technical lead
- NGÀY: 2026-10-13
- GIỜ-PHÚT: 15:02 UTC+7
- NỘI DUNG: Đã đọc source tree qua MCP. Có prototype tại ont-platform/, có dashboard, route kỹ thuật viên/khách hàng và file E2E/CI. Root preview/ đang hiển thị snapshot danh sách file/metadata, chưa phải preview sản phẩm. Root README và ont-platform/roadmap.md không đồng nhất. Kế hoạch yêu cầu ONT Care độc lập khi runtime, MCP chỉ dùng cho thao tác Sandbox/source/evidence; cần có DASH và PREVIEW riêng, cấu trúc Sandbox/GitHub song song.
- EVIDENCE: MCP sandbox_list/read. Chưa chạy build, lint, browser E2E/CI hoặc kiểm thử ONT thật.
- TRẠNG THÁI: Audit tĩnh DONE; runtime verification NOT RUN; chưa đồng bộ GitHub.