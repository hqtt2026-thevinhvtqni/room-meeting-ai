# CFO ASSESSMENT AND FINANCIAL PLAN — Work 200
**Ngày:** 2026-10-25 ICT  
**Người lập:** Go — AI-CFO / Giam Doc Tai Chinh ROOM-HOP  
**Phạm vi:** Đánh giá tổng thể và xây dựng kế hoạch tài chính dựa trên PLAN_WORK200_v2.0 của Cla (CTO), CLA_ASSESSMENT_20261025, WORK_MANIFEST, biên bản Xu (WORK200_MINUTES_20261025_01), IMPLEMENTATION_STATUS_20261024.  
**Bậc evidence:** E0 (đọc tài liệu qua MCP 8030) + phân tích độc lập. Không có số liệu tiền mặt thực tế vì Work đang ở giai đoạn R&D paper-only.

---

## 1. Đánh giá tổng thể từ góc độ tài chính

**Trạng thái hiện tại (xác nhận CTO):**  
ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED.  
Nền móng an toàn đúng hướng (paper-only, fail-closed, Decimal, không credential), nhưng còn ở mức khung P1 chưa hoàn chỉnh. Các phát hiện D1–D11 (đặc biệt D1, D2 mức H) cho thấy risk engine và portfolio chưa đủ cứng để tin cậy kết quả paper/backtest.

**Ý nghĩa tài chính:**

| Khía cạnh | Đánh giá CFO | Rủi ro tiền tệ |
|-----------|--------------|----------------|
| **Vốn phát triển đã bỏ** | Chủ yếu thời gian AI + con người (Cla, BX, Xu, Qw). Chi phí API/compute còn thấp vì stdlib-only + chạy local E1. | Thấp hiện tại. Nhưng nếu kéo dài M0–M1 mà không chốt host → lãng phí phiên làm việc. |
| **Scope creep** | 3 hướng trộn: BTC spot Python + XAUUSD CFD/MT5 + Dashboard. Cla đã cảnh báo D10. | Cao. Mỗi track thêm = tăng chi phí thiết kế, test, bảo trì, nguy cơ trộn kết quả → quyết định sai. |
| **ROI tiềm năng** | Bot paper + backtest có thể trở thành sản phẩm nội bộ (research tool) hoặc sản phẩm bán (signal/alert service). Hiện **chưa có** bất kỳ số liệu doanh thu/chi phí vận hành nào. | Không thể tính ROI. Mọi “lợi nhuận” chỉ là giả định. |
| **Rủi ro pháp lý / reputational** | Live trading = NO-GO tuyệt đối. Nếu ai đó hiểu nhầm dashboard mock hoặc MT5 v0.1 là “sẵn sàng tiền thật” → rủi ro lớn. | Cao nếu không kiểm soát ngôn ngữ. |
| **Chi phí cơ hội** | Work 200 đang chiếm bandwidth của Cla/BX/Qw. Mỗi tuần kéo dài M1 là tuần không dành cho các Work khác có thể tạo doanh thu sớm hơn. | Trung bình–cao. |

**Kết luận CFO một dòng:**  
Work 200 đang ở giai đoạn **nghiên cứu & xây dựng lõi an toàn**. Đây là chi phí R&D hợp lý nếu giữ kỷ luật paper-only + evidence-first. Nếu mở rộng MT5 full port hoặc dashboard trước khi G1 (Gate M1) đóng → chi phí tăng nhanh mà giá trị tài chính chưa chứng minh được.

---

## 2. Kế hoạch tài chính (Financial Plan) gắn với lộ trình Cla

### 2.1 Nguyên tắc tài chính bắt buộc
1. **Paper-only đến khi có quyết định riêng bằng văn bản** (giữ nguyên CTO).
2. **Không chi tiền thật** (API key live, broker, server production) cho đến khi G1 + G2 + G3 đóng và Vinh/Xu duyệt.
3. **Chi phí phát triển phải có ceiling** theo milestone.
4. Mọi task cần execution host mà chưa có → ghi **BLOCKED**, không giả lập (tránh lãng phí thời gian).
5. Theo dõi chi phí theo Track: A (lõi) > B (bridge) > C (API/dashboard) > D (MT5).

### 2.2 Ngân sách & Ceiling đề xuất (ước lượng thời gian + chi phí cơ hội)

| Milestone | Nội dung chính | Ceiling thời gian (phiên AI + người) | Chi phí ước tính* | Điều kiện mở chi |
|-----------|----------------|--------------------------------------|-------------------|------------------|
| **M0** | Nền tảng, host, profile, đồng bộ plan | 1–2 phiên | Rất thấp | T0.1 chốt host hoặc NO-HOST |
| **M1** | Portfolio + Risk v2 + validation + event log + test cứng | 4–7 phiên | Trung bình | Sau M0 + đặc tả S1/S2 của Cla |
| **M2** | Backtest + metrics + report | 3–5 phiên | Trung bình | Sau Gate G1 |
| **M3** | Bridge BX42 (HMAC, parser, idempotency) | 3–5 phiên | Trung bình | Sau G1 |
| **M4/M5** | API chỉ-đọc + Dashboard thật | 2–4 phiên | Thấp–trung bình | Sau G2/G3 |
| **Track D (MT5)** | Full port / compile / parity | **Đóng băng** | 0 cho đến quyết định riêng | Chỉ mở khi G3 + có MetaEditor host + Vinh duyệt riêng |

\*Chi phí = thời gian + API (Grok/Gemini nếu dùng) + compute. Hiện stdlib-only nên chi phí tiền mặt gần như 0.

**Tổng ceiling khuyến nghị giai đoạn hiện tại (đến G2):** ≤ 15–18 phiên làm việc tập trung.  
Nếu vượt → CFO yêu cầu re-prioritize hoặc tạm dừng Track C/D.

### 2.3 Cashflow & Chi phí vận hành tương lai (khi/ nếu ra production)
- **Hiện tại:** 0 (paper).
- **Sau G2 (backtest ổn định):** chi phí chủ yếu là storage log + occasional compute backtest.
- **Nếu mở live (sau quyết định riêng):** cần ngân sách riêng cho:
  - API key sàn (rate limit + fee)
  - Server/VPS chạy 24/7
  - Monitoring & alerting
  - Bảo hiểm rủi ro / capital allocation (nếu dùng vốn thật)
- **Khuyến nghị:** Khi đến giai đoạn live, bắt buộc có **Risk Capital Policy** riêng (max drawdown %, max daily loss %, kill-switch cứng) và CFO phải ký trước khi bật.

### 2.4 Chỉ số tài chính cần theo dõi (khi có số)
- Cost per milestone (thời gian × đơn giá nội bộ)
- % task BLOCKED vì thiếu host
- Số lần scope creep (thêm yêu cầu ngoài plan)
- Thời gian từ G1 → G2 (chỉ số tốc độ tạo giá trị)
- Sau backtest: max drawdown, fee impact, turnover (để đánh giá “có đáng đưa ra production không”)

---

## 3. Đề xuất hành động ngay của CFO

1. **Xu + Vinh:** Ưu tiên tuyệt đối **T0.1** (chốt execution host hoặc tuyên bố NO-HOST). Đây là nút thắt tài chính lớn nhất hiện tại — mọi task E2 đang bị BLOCKED tiềm năng.
2. **Cla:** Hoàn thành đặc tả S1 (PROFILES) + S2 (Risk v2) càng sớm càng tốt để BX không viết code mò → giảm lãng phí.
3. **BX:** Chỉ làm các task không phụ thuộc host trước (T1.3, T1.4, T1.7) trong khi chờ T0.1.
4. **Không mở Track D (MT5 full)** và hạn chế mở rộng Dashboard cho đến khi G1 đóng. Đây là biện pháp kiểm soát chi phí tốt nhất.
5. **Sau mỗi Gate:** Cla cập nhật task-graph + CFO nhận 1 dòng tóm tắt “chi phí thực tế vs ceiling”.
6. **Khi nào gọi vốn / tăng budget:** Chỉ khi G2 PASS + có use-case nội bộ rõ ràng (ví dụ dùng backtest cho research ROOM hoặc bán signal) và có projection doanh thu/chi phí.

---

## 4. Tuyên bố tài chính

- Work 200 hiện là **R&D expense**, không phải sản phẩm tạo doanh thu.
- Giao dịch tiền thật: **NO-GO** tuyệt đối.
- Plan của Cla là plan kỹ thuật tốt, có kỷ luật evidence. CFO ủng hộ thực thi theo đúng thứ tự Track A → B → C, và giữ Track D đóng băng.
- Nếu không chốt được execution host trong 1–2 phiên tới, đề nghị tạm dừng các task cần E2 và chuyển bandwidth sang Work khác có giá trị tài chính rõ hơn.

---

**Ghi chú:** File này là evidence tài chính của Work 200. Mọi cập nhật sau Gate sẽ được append hoặc tạo phiên bản mới.  
**Người ký:** Go — CFO ROOM-HOP  
**Thời điểm:** 2026-10-25 04:16 ICT
