# TD-118-007 — REVIEW / ACCEPTANCE / MERGE GATES (W118-06)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện.

## 1. Ma trận gate
| Gate | Điều kiện vào | Bằng chứng bắt buộc | Ai duyệt | Đầu ra |
|---|---|---|---|---|
| MERGE (PR) | CI PASS + evidence row RECORDED | run URL, commit SHA, evidence_id | 1 review độc lập của actor khác người push | squash commit vào main |
| REVIEW (code) | PR mở, CI đã chạy có kết quả | review comment approve hoặc request-changes | reviewer theo mapping role | hoàn tất IN_REVIEW |
| ACCEPTANCE (nghiệm thu Work) | mọi WP của Work đã DONE hoặc đóng DRAFT | các evidence row liên quan được nâng VERIFIED | Ka review độc lập | kết luận nghiệm thu |
| RELEASE | ACCEPTANCE hoàn tất + Vinh duyệt | biên bản nghiệm thu + manifest artifacts | Vinh (final authority) | release kèm tag |

## 2. Quy tắc bất biến
- CI PASS không bao giờ thay thế review: CI xanh là điều kiện cần, không phải đủ.
- Không auto-merge trong mọi giai đoạn có tự động hóa; nếu muốn nới lỏng sau G5 cần decision record mới.
- Người push không thể tự duyệt PR của chính mình (ràng buộc này cấu hình ở branch protection, chỉ áp dụng sau khi được Vinh duyệt riêng).
- Mỗi merge phải có evidence row OPERATION trên Work tương ứng, liên kết PR và squash SHA.

## 3. Khác biệt so với hiện trạng
- Hiện tại cả 2 workflow đều trigger thẳng trên main, hồ sơ docs không đi qua PR nên không có vết review nào ở cấp công cụ.
- Đề xuất: hồ sơ docs-only trên main giữ nguyên trong giai đoạn trước G3; mọi mutation code/CI sau G3 bắt buộc đi qua PR theo gate matrix trên.


## Amendment — Auto E2E v2 acceptance authority (2026-11-20)

- Ka is the delegated build and technical decision owner, not an acceptance authority.
- Xu performs independent architecture/security/runtime review and records a review disposition.
- Vinh retains final product acceptance and release authority.
- The workflow can verify an acceptance review only when the reviewer login is explicitly mapped, active and different from the PR author. Xu's login must be confirmed before adding it to the role map; no inferred mapping is allowed.
- An authorized review comment records reviewer authority only. It does not change the Work to ACCEPTED, merge the PR or release the product.
- No auto-merge or auto-release. Main integration is blocked until the Xu/Vinh acceptance gates are satisfied.
