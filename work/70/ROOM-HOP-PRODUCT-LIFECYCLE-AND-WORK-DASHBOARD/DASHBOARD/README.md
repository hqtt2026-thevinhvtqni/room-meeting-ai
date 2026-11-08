# DASHBOARD — BẢNG ĐIỀU KHIỂN RIÊNG CHO TỪNG WORK
- **STT / Document ID:** DOC-032
- **Priority:** P3
- **Read order:** 39
- **Depends on:** DOC-010
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30


## Mục đích
Mỗi Work có một Dashboard để theo dõi vòng đời, gate, WP, blockers, risks, decisions, evidence và độ mới dữ liệu.

## Thành phần
- index.html: giao diện chỉ đọc.
- PRODUCT_STATUS.json: bản dữ liệu trạng thái cục bộ hiện tại.
- PRODUCT_STATUS.schema.json: hợp đồng kiểm tra cấu trúc dữ liệu.

## Nguồn dữ liệu
- core_live: chỉ dùng khi response đến từ Core thật, đã xác thực và kiểm tra quyền.
- core_cached: cache do Core phát hành, kèm revision/generated_at/freshness.
- local_snapshot: bản chụp trong Sandbox/Work; không phải dữ liệu trực tiếp.
- sample: dữ liệu minh họa.
Nếu tải dữ liệu lỗi, Dashboard hiển thị UNKNOWN. Không fallback sang dữ liệu giả.

## Hiển thị
Dashboard trình bày giai đoạn hiện tại, 9 phase/gate, owner, WP owner/reviewer, blockers, risks, decisions, evidence references, source mode và freshness. Trạng thái tiến độ không thay thế gate.

## Chạy thử
Chạy static HTTP server trong thư mục DASHBOARD, ví dụ `python -m http.server 8080`, rồi mở `http://localhost:8080`. Không mở bằng file:// nếu trình duyệt chặn fetch JSON.

## Giới hạn hiện tại
Dashboard đang đọc PRODUCT_STATUS.json cục bộ. Core API, đăng nhập/phân quyền, live refresh, lưu trữ bền vững, upload và export backend chưa được xác minh/triển khai. Không có nút giả để tuyên bố lưu/xuất file. G0 và các gate lifecycle vẫn chờ kiểm chứng.


## 2026-11-06 — Clarification: Work Dashboard vs Product Dashboard

This directory is the **Work Dashboard** for the current Work. It is not the product-facing dashboard built by the product.

### Work Dashboard lifecycle
- Create a minimal W0 scaffold when the Work is instantiated.
- Evolve to W1 as folders, phases, documents, gates and WP records appear.
- Evolve to W2 as assignments, owners, blockers, risks, decisions and evidence references become available.
- Evolve to W3 as executed verification, independent QE, acceptance and release evidence become available.
- Evolve to W4 for operational monitoring and links to the delivered product interface.

W0–W4 are Dashboard maturity levels, not lifecycle phases or authorization gates. A maturity level must be supported by source evidence; file presence alone is insufficient.

### Product Dashboard boundary
The Product Dashboard belongs to the product source declared by this Work. It has its own product users, domain requirements, data/API contract, identity/permissions and acceptance tests. It is not stored or implemented here by default.

### Current Work 70 baseline
- `index.html`: Work Dashboard prototype / read-only entry point.
- `PRODUCT_STATUS.json`: legacy-named Work status local snapshot, not Product Dashboard data.
- `PRODUCT_STATUS.schema.json`: schema for the Work status projection.
- Core live integration, browser E2E, usability and independent QE: NOT VERIFIED / NOT RUN as applicable.
- Product Dashboard: NOT VERIFIED as a separate deliverable.

See DOC-085 for the governing two-dashboard architecture. This README update documents the boundary; it does not authorize code or production configuration changes.



## 2026-11-09 — Three-tier Product Progress view (DOC-094)
- Work Execution Dashboard adds a read-only Product Progress section.
- Tier 1 shows Product Tasks; Tier 2 shows Phase Tasks with primary/contributing/checking Agents; Tier 3 links existing shared Work-level Agent Task IDs from DOC-093.
- Data source: `execution/PRODUCT_PHASE_TASK_STATUS.json`, derived from DOC-094. No mock fallback; fetch failure displays UNKNOWN.
- DOC-094 is DRAFT_NOT_APPROVED. Assignment ACK, product progress calculation, browser E2E, QE and GitHub parity remain unverified/not run as applicable.
