# EGRESS SENSITIVITY ANALYSIS — ROOM MEDIA HUB (W117)
- Author: Go / CFO (AI-06)
- Date: 2026-11-16 21:25 +07
- Status: SENSITIVITY ANALYSIS — ASSUMPTION-BASED
- Parent: COST_EVALUATION_HYBRID.md
- Related: ODR-014 (Cloud egress and storage cost growth risk)

## 1. Mục tiêu
Phân tích độ nhạy (sensitivity) của chi phí Egress — yếu tố rủi ro chi phí lớn nhất trong mô hình Hybrid H1.

Câu hỏi chính:
- Egress thay đổi như thế nào khi volume, tỷ lệ xem/tải, đơn giá, cache hit rate và tỷ lệ video thay đổi?
- Điểm nào khiến Egress vượt storage cost?
- Biện pháp kiểm soát nào có ROI cao nhất?

## 2. Công thức cơ bản

```
Egress Cost / năm ≈ 
  (Total Store Size GB × Egress Ratio × 12) × Unit Egress Price ($/GB)
  × (1 − Internal Cache Hit Rate)
  × Video Multiplier (nếu video bị tải full thay vì proxy)
```

Trong đó:
- **Egress Ratio** = tỷ lệ dung lượng bị tải/xem từ Cloud mỗi tháng so với tổng store
- **Internal Cache Hit Rate** = tỷ lệ request được phục vụ từ thumbnail/proxy nội bộ (không egress)
- **Unit Egress Price** = 0.05 – 0.12 USD/GB (thị trường 2026)

## 3. Biến số chính & Phạm vi phân tích

| Biến số | Low | Base | High | Extreme |
|---------|-----|------|------|---------|
| Total Store Size (cuối năm 1) | 2 TB | 8 TB | 30 TB | 50 TB |
| Egress Ratio (% store / tháng) | 5% | 15% | 40% | 70% |
| Unit Egress Price ($/GB) | 0.05 | 0.08 | 0.12 | 0.15 |
| Internal Cache Hit Rate | 80% | 60% | 30% | 10% |
| Video Ratio (byte) | 40% | 55% | 70% | 85% |

## 4. Sensitivity Matrix 1 — Egress Ratio × Store Size
(Giả định: Unit price = $0.08/GB, Cache Hit = 60%)

| Store Size \ Egress Ratio | 5% | 15% | 40% | 70% |
|---------------------------|----|-----|-----|-----|
| **2 TB** | $48 | $144 | $384 | $672 |
| **8 TB** | $192 | $576 | $1,536 | $2,688 |
| **30 TB** | $720 | $2,160 | $5,760 | $10,080 |
| **50 TB** | $1,200 | $3,600 | $9,600 | $16,800 |

**Nhận xét:** Ở Base volume (8 TB), khi Egress Ratio tăng từ 15% → 40%, chi phí tăng gần **2.7 lần**. Đây là đòn bẩy mạnh.

## 5. Sensitivity Matrix 2 — Unit Price × Cache Hit Rate
(Giả định: Store = 8 TB Base, Egress Ratio = 15%)

| Unit Price \ Cache Hit | 80% | 60% | 30% | 10% |
|------------------------|-----|-----|-----|-----|
| **$0.05/GB** | $144 | $288 | $504 | $648 |
| **$0.08/GB** | $230 | $461 | $806 | $1,037 |
| **$0.12/GB** | $346 | $691 | $1,210 | $1,555 |
| **$0.15/GB** | $432 | $864 | $1,512 | $1,944 |

**Nhận xét quan trọng:**  
Tăng Cache Hit Rate từ 30% → 80% có thể **giảm Egress cost xuống còn ~1/3 đến 1/4**. Đây là đòn bẩy kiểm soát chi phí hiệu quả nhất về mặt kỹ thuật (không phụ thuộc đàm phán giá Cloud).

## 6. Sensitivity Matrix 3 — Video Ratio impact (proxy vs full download)

Giả định:
- Ảnh + thumbnail hầu như luôn được phục vụ internal (cache hit cao).
- Video nếu không có proxy/transcode tốt → user tải full original → Egress cao.

| Video Ratio | % request video dùng proxy | Effective Egress multiplier | Impact ở Base 8TB / 15% ratio |
|-------------|----------------------------|-----------------------------|--------------------------------|
| 40% | 90% | ~1.1× | Thấp |
| 55% | 70% | ~1.4× | Trung bình |
| 70% | 40% | ~2.0× | Cao |
| 85% | 20% | ~2.8× | Rất cao |

**Kết luận:** Nếu không đầu tư proxy/transcode tốt, tỷ lệ video cao sẽ nhân đôi hoặc nhân ba chi phí Egress thực tế.

## 7. Break-even Analysis: Khi nào Egress vượt Storage?

Giả định Storage cost năm 1 (Cloud + Internal) khoảng:
- Base 8 TB: ~$3,000 – $4,200
- High 30 TB: ~$9,000 – $16,000

| Store Size | Storage cost (mid) | Egress Ratio cần để Egress ≈ Storage | Ghi chú |
|------------|--------------------|--------------------------------------|---------|
| 8 TB | ~$3,500 | ~25–30% (với cache 60%, $0.08/GB) | Dễ đạt nếu video xem nhiều |
| 30 TB | ~$12,000 | ~20–25% | Nguy hiểm hơn |

**Cảnh báo:** Ở volume cao, chỉ cần Egress Ratio ~20–25% là Egress đã ngang bằng toàn bộ storage cost. Đây là ngưỡng cần đặt alert.

## 8. Tornado Chart (Ranking độ nhạy)

Thứ tự ảnh hưởng đến chi phí Egress (từ mạnh → yếu) trong phạm vi phân tích:

1. **Egress Ratio** (tỷ lệ xem/tải) — ảnh hưởng mạnh nhất
2. **Internal Cache Hit Rate** — đòn bẩy kiểm soát kỹ thuật tốt nhất
3. **Store Size** (volume) — tuyến tính
4. **Unit Egress Price** — phụ thuộc provider & đàm phán
5. **Video Ratio + Proxy quality** — ảnh hưởng gián tiếp nhưng rất lớn nếu không kiểm soát

## 9. Khuyến nghị kiểm soát chi phí Egress (theo ROI)

| Hạng mục | Mức độ ưu tiên | Ước tính ROI | Ghi chú |
|----------|----------------|--------------|---------|
| **Internal thumbnail + proxy cache mạnh** | P0 | Rất cao | Giảm Egress 50–70% nếu làm tốt |
| Short-lived authorized URL (không public bucket) | P0 | Cao | Đã có trong proposal |
| Transcode/proxy chất lượng đủ dùng (không bắt user tải original) | P0 | Cao | Đặc biệt với video |
| Soft/hard limit + alert trên Egress | P1 | Trung bình–Cao | Ngăn bill shock |
| Chọn region + provider có egress rẻ / volume discount | P1 | Trung bình | Cần Ka + Go cùng làm |
| Archive tier cho media ít truy cập | P2 | Trung bình | Giảm storage nhưng không giảm egress nếu vẫn xem |
| CDN (nếu có user phân tán địa lý) | P2 | Tùy workload | Cân nhắc khi High scenario |

## 10. Scenario Stress Test (Worst reasonable case)

| Tham số | Giá trị stress |
|---------|----------------|
| Store Size | 30 TB |
| Egress Ratio | 40% |
| Cache Hit Rate | 30% |
| Unit Price | $0.12/GB |
| Video heavy + weak proxy | ×1.8 multiplier |

**Kết quả stress:** Egress năm 1 có thể đạt **$15,000 – $25,000+**.  
Đây là mức cần tránh bằng thiết kế (cache + proxy) chứ không chỉ bằng đàm phán giá.

## 11. Kết luận của Go (CFO)

1. **Egress là rủi ro chi phí số 1** của mô hình Hybrid — độ nhạy cao hơn storage.
2. Đòn bẩy kiểm soát mạnh nhất và rẻ nhất là **Internal Cache Hit Rate** (thumbnail + proxy).
3. Cần đặt **hard/soft Egress budget** và alert ngay từ giai (ví dụ: cảnh báo khi tháng vượt $300–500 ở Base).
4. Khi thiết kế kiến trúc, Cla & Qw cần coi **cache hit rate và proxy quality** là non-functional requirement có ảnh hưởng tài chính trực tiếp.
5. Go đề xuất đưa vào NFR:
   - Target Cache Hit Rate ≥ 70% cho thumbnail/preview
   - Egress monthly soft limit + alert
   - Proxy bắt buộc cho video trước khi cho phép full original download (trừ trường hợp đặc biệt)

## 12. Disposition

- Phân tích này là assumption-based, chưa có số liệu thực tế về traffic.
- Sẵn sàng cập nhật khi có log thực tế hoặc quyết định volume/provider.
- Không authorize chi tiêu.

---
*Go / CFO — 2026-11-16*
