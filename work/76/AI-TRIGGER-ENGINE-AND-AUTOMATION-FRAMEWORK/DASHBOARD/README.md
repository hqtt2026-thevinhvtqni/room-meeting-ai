# DASHBOARD — WORK 76 / BẢNG ĐIỀU KHIỂN WORK 76

- Document ID: DOC-076-DASHBOARD
- Version: 0.2
- Updated: 2026-11-06
- Reference: Work 70 / Dashboard DOC-032
- Status: ACTIVE — SOURCE SYNC VERIFIED; BROWSER/MOBILE QE NOT RUN

## 1. Mục đích
Bảng điều khiển theo dõi vòng đời Work 76, phase/gate, Work Package, AI assignment, blocker, risk, decision, activity log, evidence và freshness. Dashboard là read-only projection, không thay thế Core và không có quyền thực thi Trigger.

## 2. Thành phần
- `index.html`: giao diện responsive cho PC và điện thoại; lọc/tìm WP; làm mới dữ liệu.
- `PRODUCT_STATUS.json`: nguồn trạng thái local snapshot.
- `PRODUCT_STATUS.schema.json`: hợp đồng cấu trúc dữ liệu.
- `../00_ROOT/DOC-035_NHAT-KY-THI-CONG_EXECUTION-LOG.md`: nhật ký thi công.
- `../06_EVIDENCE/EVIDENCE_REGISTER.md`: sổ bằng chứng chính thức.

## 3. Các vùng hiển thị
1. Tổng quan Work status, current phase, WP count và blocker count.
2. 9 phase lifecycle cùng owner và gate status.
3. Danh sách WP có tìm kiếm và lọc trạng thái.
4. AI roster/assignment; trạng thái PLANNED không có nghĩa AI đã nhận việc.
5. Blocker, risk và decision cần phê duyệt.
6. Hoạt động gần đây và evidence status.
7. Data source, timestamp, revision và freshness.

## 4. Nguồn dữ liệu và quy tắc tin cậy
- `core_live`: chỉ dùng khi dữ liệu đến từ Core thật, xác thực và kiểm tra quyền.
- `core_cached`: cache do Core phát hành, phải có revision/generated_at/freshness.
- `local_snapshot`: dữ liệu tĩnh trong repository/Sandbox; không phải Core live.
- `sample`: dữ liệu minh họa, phải gắn nhãn rõ ràng.
- Không tải được JSON: hiển thị UNKNOWN, không dùng dữ liệu cũ để giả lập.
- Không có evidence: không nâng trạng thái thành PASS/DONE.
- Dashboard chỉ đọc; không cập nhật manifest, gate, quyền hoặc trạng thái Work.

## 5. Chạy Dashboard
Mở terminal tại thư mục `DASHBOARD`, chạy:
```bash
python -m http.server 8080
```
Sau đó mở `http://localhost:8080`. Không dùng `file://` nếu trình duyệt chặn fetch JSON.

## 6. Kiểm thử thủ công
- [ ] PC: bố cục không tràn ngang, các panel hiển thị đủ.
- [ ] Mobile: bố cục một cột, nút và bộ lọc thao tác được.
- [ ] WP search: lọc đúng theo ID, title, owner, reviewer.
- [ ] WP status: lọc đúng trạng thái.
- [ ] Refresh: tải lại PRODUCT_STATUS.json với cache-busting.
- [ ] JSON missing/HTTP error/invalid JSON: hiển thị UNKNOWN.
- [ ] Không có blocker/evidence: hiển thị empty state, không tạo dữ liệu giả.
- [ ] Xác nhận Dashboard không có action thay đổi trạng thái hoặc thực thi Trigger.

## 7. Giới hạn hiện tại
Dashboard v0.2 đọc JSON tĩnh từ repository. Chưa có Core API, authentication/authorization, live push, backend persistence, upload/export backend, browser E2E hoặc independent QE. Source sync không đồng nghĩa browser test PASS. Work 76 vẫn ở 01_DISCOVER; G0/G1 chưa xác minh; NOT RELEASED.


## 8. Snapshot refresh — 2026-11-13
- PRODUCT_STATUS.json revision: W76-DASHBOARD-0.3.3.
- Snapshot includes evidence EV-76-001…EV-76-018 and recent discovery/review activity from the canonical Work journal.
- Source mode remains local_snapshot; this is not Core live data.
- GitHub/Sandbox data-file synchronization is not browser rendering or interaction evidence. PC/mobile browser checks and independent QE remain NOT RUN; EV-76-007 remains NOT_AVAILABLE.
