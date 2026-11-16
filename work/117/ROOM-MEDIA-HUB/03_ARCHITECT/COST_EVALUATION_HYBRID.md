# COST EVALUATION — HYBRID STORAGE MODEL (ROOM MEDIA HUB)
- Work: 117
- Author: Go / CFO (AI-06)
- Date: 2026-11-16 21:20 +07
- Status: INITIAL COST MODEL — ASSUMPTION-BASED / NOT BASELINED
- Related: ODR-002, ODR-003, ODR-008, ODR-014, ARCHITECTURE_PROPOSAL.md, ARCHITECTURE_CONSULTATION_BRIEF.md

## 1. Purpose & Scope
Đánh giá chi phí mô hình Hybrid (Internal primary + Cloud replica encrypted, asynchronous) theo candidate H1 được đề xuất trong Architecture Proposal.

Mục tiêu:
- Cung cấp khung chi phí minh bạch cho quyết định kiến trúc.
- Làm rõ các giả định và độ nhạy (sensitivity).
- Không bịa số liệu chính xác khi volume, provider, retention, file-size chưa được quyết định.
- Hỗ trợ so sánh H1 vs H2 và các phương án thay thế.

## 2. Cost Structure (Hybrid H1 — Preferred Candidate)

| Hạng mục | Mô tả | Tính chất | Ghi chú |
|----------|-------|-----------|---------|
| **A. Internal Storage** | Disk / NAS / object store nội bộ (primary) | CapEx hoặc OpEx cố định | Amortized hardware + điện + chỗ | 
| **B. Cloud Object Storage** | Replica encrypted (Standard / IA / Archive) | OpEx biến đổi theo dung lượng | Phụ thuộc class & region |
| **C. Egress / Data Transfer** | Internal → Cloud (replication) + Cloud → user (preview/download) | OpEx biến đổi cao | Thường là rủi ro chi phí lớn nhất |
| **D. Processing Workers** | Thumbnail, proxy, transcode, malware scan | OpEx / compute hours | CPU/GPU; có thể burst |
| **E. Metadata & Catalog** | SQLite / DB + search index | Thấp | Có thể reuse W33 + mở rộng |
| **F. Operations & Observability** | Monitoring, backup verification, restore drill, support | OpEx cố định + biến | Bắt buộc cho production |
| **G. One-time / Setup** | Adapter development, encryption key setup, migration, testing | CapEx / one-time | Phụ thuộc độ phức tạp W33 extension |

## 3. Key Assumptions (Explicit & Conservative)

Vì các NFR số lượng chưa được chốt (RMH-NF-004, ODR-008), Go áp dụng **ba kịch bản** dựa trên quy mô Room nhỏ–trung bình:

| Tham số | Low | Base | High | Ghi chú |
|---------|-----|------|------|---------|
| Tổng dung lượng media gốc (sau 12 tháng) | 2 TB | 8 TB | 30 TB | Ảnh + video; dedup SHA-256 giúp giảm |
| Tỷ lệ growth / tháng | 10% | 15% | 25% | Sau khi ổn định |
| Tỷ lệ video (dung lượng lớn) | 40% | 55% | 70% | Video chiếm phần lớn byte |
| Retention (soft-delete + legal hold) | 18 tháng | 36 tháng | 60 tháng | Ảnh hưởng Cloud Archive |
| Tỷ lệ preview/download / tháng so với tổng store | 5% | 15% | 40% | Egress driver |
| Replication lag target (RPO) | ≤ 24h | ≤ 4h | ≤ 1h | Ảnh hưởng tần suất job & chi phí |
| Cloud storage class chính | Standard | Standard + IA | Standard + IA + Archive | IA/Archive giảm $/GB nhưng tăng restore cost |

**Giả định khác:**
- Deduplication hiệu quả nhờ SHA-256 (W33 đã có unique hash) → tiết kiệm 15–40% so với không dedup.
- Không public bucket; mọi access qua short-lived authorized URL → egress chỉ khi user thực sự xem/tải.
- Internal storage đủ capacity cho primary + working set thumbnails/proxies.
- Không tính chi phí nhân sự full-time; chỉ tính infrastructure + biến đổi.

## 4. Unit Cost Reference Ranges (2026, indicative USD)

| Thành phần | Đơn giá tham chiếu (USD) | Nguồn / Ghi chú |
|------------|--------------------------|-----------------|
| Cloud Object Storage — Standard | 0.020 – 0.026 / GB-month | AWS S3 / GCS / Azure tương đương |
| Cloud Object Storage — Infrequent Access | 0.010 – 0.015 / GB-month | + retrieval fee |
| Cloud Object Storage — Archive / Glacier | 0.001 – 0.004 / GB-month | + retrieval latency & fee cao |
| Egress (Cloud → Internet) | 0.05 – 0.12 / GB | Vùng & volume discount |
| Internal → Cloud transfer | 0.00 – 0.02 / GB | Thường rẻ hơn hoặc free trong cùng provider |
| Transcode / proxy (CPU) | 0.02 – 0.08 / minute video | Phụ thuộc resolution & codec |
| Thumbnail generation | Rất thấp (cents / 1000 ảnh) | |
| Internal storage amortized | 0.008 – 0.025 / GB-month | Disk + điện + chỗ (tùy scale) |

> Các số trên là **khoảng tham chiếu thị trường 2025–2026**, không phải quote chính thức. Provider & region cụ thể sẽ thay đổi đáng kể.

## 5. Scenario Cost Model (12 tháng đầu + steady state)

### 5.1 Storage Cost (năm 1, sau khi đạt volume cuối năm)

| Kịch bản | Internal (primary) | Cloud Replica (Standard/IA mix) | Tổng Storage / năm |
|----------|--------------------|---------------------------------|---------------------|
| Low (2 TB) | ~$200 – $400 | ~$400 – $650 | **$600 – $1,050** |
| Base (8 TB) | ~$800 – $1,600 | ~$1,600 – $2,600 | **$2,400 – $4,200** |
| High (30 TB) | ~$3,000 – $6,000 | ~$6,000 – $10,000 | **$9,000 – $16,000** |

*Giả định: Cloud dùng mix Standard (hot) + IA (warm). Archive chỉ áp dụng cho phần retention dài nếu có policy.*

### 5.2 Egress Cost (rủi ro lớn nhất)

| Kịch bản | Egress volume / tháng (ước) | Chi phí egress / năm |
|----------|-----------------------------|----------------------|
| Low (5% of store) | ~100 – 150 GB | **$60 – $200** |
| Base (15%) | ~1.0 – 1.5 TB | **$600 – $2,000** |
| High (40%) | ~8 – 12 TB | **$5,000 – $15,000+** |

**Cảnh báo CFO:** Egress là biến số nhạy cảm nhất. Nếu Media Hub trở thành nơi xem/tải thường xuyên (đặc biệt video), chi phí Cloud egress có thể vượt storage. Cần policy cache internal thumbnail/proxy mạnh và short-lived URL.

### 5.3 Processing Cost (thumbnail + proxy)

| Kịch bản | Ước tính năm 1 |
|----------|----------------|
| Low | $100 – $400 |
| Base | $400 – $1,500 |
| High | $1,500 – $5,000+ |

Phụ thuộc mạnh vào tỷ lệ video và độ phức tạp transcode (1080p vs 4K, multiple proxies).

### 5.4 Tổng hợp chi phí vận hành năm 1 (OpEx ước tính)

| Kịch bản | Storage | Egress | Processing | Ops/Monitoring | **Tổng OpEx năm 1** |
|----------|---------|--------|------------|----------------|---------------------|
| Low | $0.6–1.1k | $0.06–0.2k | $0.1–0.4k | $0.3–0.8k | **~$1.1k – $2.5k** |
| Base | $2.4–4.2k | $0.6–2.0k | $0.4–1.5k | $0.5–1.2k | **~$4.0k – $9.0k** |
| High | $9–16k | $5–15k | $1.5–5k | $1–2.5k | **~$16.5k – $38.5k** |

### 5.5 One-time / Setup Cost (CapEx / Project)

| Hạng mục | Ước tính | Ghi chú |
|----------|----------|---------|
| Mở rộng W33 (many-to-many, storage port, replication state) | Trung bình–Cao | Phụ thuộc review Cla |
| Cloud adapter + encryption + key management | Trung bình | |
| Worker pipeline (thumbnail/proxy) | Trung bình | Có thể reuse một phần W29 |
| Testing & restore rehearsal | Bắt buộc | |
| **Tổng one-time ước tính** | **$3,000 – $12,000** (effort equivalent) | Không tính full-time headcount |

## 6. So sánh nhanh các phương án

| Phương án | Ưu điểm chi phí | Nhược điểm chi phí | Rủi ro chính |
|-----------|-----------------|--------------------|--------------|
| **H1 Internal-primary + Cloud replica** | Egress thấp hơn nếu hầu hết access nội bộ; offline capacity tốt | Phải duy trì 2 lớp storage | Replication lag, dual consistency |
| **H2 Cloud-primary + Internal cache** | Đơn giản hơn về primary | Egress cao hơn khi user xem nhiều; phụ thuộc Cloud | Connectivity, egress bill shock |
| **B. W117 cloud riêng (không reuse W33)** | — | Duplicate storage + metadata → chi phí cao hơn rõ | Split brain, audit phức tạp |
| **D. Managed media platform** | Ít ops nội bộ | Vendor lock-in + premium pricing (thường 2–5x raw storage) | Data control, exit cost |

**Khuyến nghị sơ bộ của Go (CFO):**  
H1 vẫn là phương án có kiểm soát chi phí tốt nhất trong dài hạn **nếu** Room chủ yếu truy cập nội bộ và có capacity internal ổn định. H2 chỉ nên xem xét nếu đa số người dùng ở xa và internal bandwidth/storage bị hạn chế.

## 7. Risk & Sensitivity Highlights (ODR-014)

1. **Egress là killer variable** — cần theo dõi và đặt soft/hard limit + alert.
2. **Video ratio** quyết định mạnh processing + storage growth.
3. **Retention policy** (ODR-007) ảnh hưởng trực tiếp Cloud bill sau năm 2–3.
4. **Deduplication** từ SHA-256 của W33 là lợi thế chi phí thực sự; không được phá khi thiết kế many-to-many.
5. Chưa có số liệu thực tế về volume hiện tại của Room → model chỉ mang tính định hướng.

## 8. Recommended Next Actions (Go)

1. **Thu thập số liệu thực tế** (ưu tiên cao):
   - Dung lượng media hiện có trên các Work liên quan (W01, W32, W29, W33…).
   - Tần suất upload / xem / tải trong 30–90 ngày gần nhất (nếu có log).
2. **Chốt Cloud provider shortlist** cùng Ka (cost + privacy + residency).
3. **Đề xuất NFR số** cho RMH-NF-004 / ODR-008 (max file size, capacity target năm 1, RPO/RTO, budget ceiling).
4. Sau khi có feedback Cla (architecture) và Ka (security), Go sẽ cập nhật model với số liệu chặt hơn và đề xuất budget ceiling chính thức.

## 9. Disposition

- Đây là **cost model ban đầu**, không phải ngân sách đã duyệt.
- Không authorize bất kỳ chi tiêu Cloud nào.
- Không claim chính xác đến từng dollar.
- Sẵn sàng refine khi có thêm evidence từ Cla / Ka / Platform hoặc số liệu thực tế từ anh Vinh.

---
*Go / CFO — 2026-11-16*


---

## 10. Egress Sensitivity Analysis (Added 2026-11-16 21:25)

Chi tiết đầy đủ xem file riêng: `03_ARCHITECT/EGRESS_SENSITIVITY_ANALYSIS.md`

**Tóm tắt nhanh kết quả sensitivity:**

- **Egress Ratio** và **Internal Cache Hit Rate** là hai biến số nhạy cảm nhất.
- Tăng Cache Hit Rate từ 30% → 80% có thể giảm Egress cost xuống còn khoảng 1/3 – 1/4.
- Ở volume Base (8 TB), Egress Ratio chỉ cần ~25–30% là Egress đã ngang bằng storage cost.
- Stress case (30 TB + 40% ratio + cache thấp + video heavy) có thể đẩy Egress lên $15k–$25k+/năm.

**Khuyến nghị ưu tiên cao:**
1. Internal thumbnail + proxy cache mạnh (P0)
2. Short-lived authorized URL (đã có trong proposal)
3. Proxy bắt buộc cho video trước khi cho phép full download
4. Soft/hard Egress limit + alert ngay từ đầu

Go đề xuất đưa các target sau vào NFR:
- Cache Hit Rate ≥ 70% cho thumbnail/preview
- Egress monthly soft limit + alert
- Proxy quality là requirement có ảnh hưởng tài chính trực tiếp
