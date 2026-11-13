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


## 9. Architecture decision register — 2026-11-13
- PRODUCT_STATUS.json revision: W76-DASHBOARD-0.3.4.
- Eight architecture decisions ADR-76-001…008 are listed as OPEN / NOT APPROVED; they are decision tracking items, not approved designs.
- Snapshot remains local_snapshot; Core live integration is not available/verified.
- Trigger implementation, CI/tests and browser/mobile QE remain NOT RUN.


## Static review finding — Work Entry gates are not rendered (2026-11-13)
- Reviewed artifact: DASHBOARD/index.html, GitHub main blob c53b084a5a9bedbafef2d74af5701dc0c4f0149d (16,248 chars).
- Exact behavior found: the UI calculates gateSummary only from phases.filter(p => p.gate_status === "PASS") and renders each lifecycle phase's gate_status.
- No G0, G1, WE-G4 or Work Entry gate fields/rendering were found in the inspected HTML.
- Impact: the displayed “Gate đạt x/9” is a lifecycle phase-gate summary only. It does not communicate DOC-007 participant-specific Work Entry WE-G0…WE-G5; a viewer may miss that Co WE-G4/G5 are BLOCKED even while looking at the gate summary.
- Required correction for WP-76-09 owner Xu: add a distinct Work Entry panel/summary sourced from canonical DOC-007 or an explicitly versioned snapshot field; show lifecycle G0/G1 separately from participant WE-G0…WE-G5; label unknown/stale data UNKNOWN; do not combine counts or infer PASS.
- Boundary: static HTML inspection only. No browser/mobile rendering, interaction or accessibility test was run. This is a review finding, not a source-code defect reproduction.
- Disposition: WP-76-09 remains IN_REVIEW; owner Xu to assess and implement within its assignment; An/Qw independent QE ACK/entry still pending.


### 2026-11-13 12:06 +07:00 — Snapshot revision W76-DASHBOARD-0.3.7
- Added EV-76-022 for the DOC-006 observable FR/NFR acceptance criteria matrix.
- The matrix is a specification only; tests remain NOT RUN and no approval or gate transition is implied.
- Sandbox capability evidence EV-76-021 is limited to the current OChat tool session; trusted AI-07 identity binding and PC/VS Code Bridge remain NOT VERIFIED.
- Current source remains LOCAL_SNAPSHOT, not Core live. Dashboard browser/mobile QE remains NOT RUN.
