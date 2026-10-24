# G2 Independent Static Review — Work 104 (bằng chứng đọc mã, KHÔNG phải kết quả chạy)

- Thời điểm: 2026-10-24 (UTC+7). Người review: Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh — vai trò review độc lập tĩnh).
- Đối tượng: commit đầu 710a5b1 trên nhánh `work/104-ai-usage-evidence-tracking` — core/usage_ledger.py, tests/test_usage_ledger.py, core/connectors.py, core/gemini_intent_router.py (đọc trực tiếp toàn văn).
- Phương pháp: đối chiếu từng mục G1 REV 6 với code. KHÔNG chạy được test (chưa có môi trường ủy quyền) → kết luận dưới đây chỉ có giá trị TĨNH, không thay G3.

## Đạt (đối chiếu G1 REV 6)

| Mục G1 | Bằng chứng code |
|---|---|
| §2 envelope v1 | `_FIELDS` allowlist đủ 33 trường đúng schema; thiếu = null, không bịa 0 |
| §2 redaction | allowlist + test `test_record_writes_one_jsonl_row_and_redacts_unapproved_fields` chèn prompt/api_key → không xuất hiện trong dòng JSONL |
| §4 lifecycle | `new_usage_event` cấp event_id TRƯỚC request; các connector/router ghi dòng hoàn chỉnh ở cả 2 nhánh có/không response |
| §3 lỗi 3 giai đoạn | connector: `except RequestException` → status="error" + error_class + latency; trích usage từ error body nếu có (giai đoạn 2), để null nếu không (giai đoạn 1); Internal/Mock = unavailable |
| §4.2 correlation | KHÔNG sinh mã giả — connector không có room_id → để null đúng quy tắc |
| §5b retention | xoay vòng 20MB `.partN` + index kèm sha256 đầu/cuối + event_count; quét index các tháng cũ khi sang tháng mới |
| §3 bộ đếm | `_fallback` ghi `{timestamp, count}` vào failures.log best-effort + stderr; module không bao giờ raise vào luồng chính |
| Gemini fallback | 1 event cho MỖI model thử (kể cả 404) — đúng tinh thần billed retry |

## Findings (không chặn G2 tiếp diễn, đưa vào danh sách chờ G3 xử lý)

- **F1 (thiếu test §7 mục 7):** test kép "hỏng cả ledger path VÀ failures.log path" chưa có trong test file — Vibe đã BỔ SUNG trong commit này (`test_dual_path_failure_no_counter_no_raise`).
- **F2 (concurrency):** module không khóa file; nhiều tiến trình ghi đồng thời JSONL có thể xen dòng (Linux append nhỏ thường an toàn, Windows không đảm bảo). G3 cần test/hạn chế: ghi rõ giả định single-writer hoặc thêm file lock.
- **F3 (race xoay vòng):** 2 tiến trình cùng vượt ngưỡng 20MB có thể race khi `path.replace()` — cùng giả định single-process với F2.
- **F4 (index nạp cả file vào bộ nhớ):** `_write_index_for_file` dùng `read_bytes()` toàn file (≤20MB theo ngưỡng — chấp nhận được, ghi nhận).
- **F5 (correlation chưa khai thác):** connector nhận `MeetingContextForAgent` không chứa room_id/meeting_id/turn_number nên event để null. Đúng quy tắc cấm-mã-giả, nhưng G4 nên truyền correlation từ tầng có sẵn mã (đầu việc G4).

## Kết luận review (tĩnh)

- Code implementation NHẤT QUÁN với G1 REV 6 ở mức đọc tĩnh; không phát hiện vi phạm ranh giới (không import MeetingManager/Governance, không đụng Protected Core).
- **KHÔNG tuyên bố G2 PASS**: tests chưa chạy trong môi trường ủy quyền (bằng chứng 0); findings F2–F5 chờ G3.
- Trạng thái: REVIEW DONE (static) — gửi Co/Xu xử lý findings; G3 giữ CHƯA BẮT ĐẦU.
