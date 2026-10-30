# QUY TRÌNH KHÁM PHÁ / DISCOVER PROCESS
- **STT / Document ID:** DOC-042
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 42
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-007; DOC-033; DOC-038
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích

DOC-042 quy định cách thực hiện đầy đủ phase 01_DISCOVER (Khám phá) cho mọi Work. Discover phải làm rõ vấn đề thực sự, người bị ảnh hưởng, bằng chứng, cơ hội, giả định, điều chưa biết và quyết định có nên tiếp tục hay không.

Discover không phải bước hợp thức hóa yêu cầu ban đầu, không phải buổi brainstorm tự do và không phải bước chọn công nghệ. Không mặc định mọi ý tưởng đều phải đi đến BUILD.

## 2. Phạm vi và nguyên tắc

Áp dụng cho Work mới, yêu cầu thay đổi lớn, phát hiện vấn đề mới hoặc Work cần quay lại khám phá vì giả định nền tảng sai.

Nguyên tắc bắt buộc:
1. **Problem before solution:** xác minh vấn đề trước khi chọn giải pháp. Yêu cầu của người đề xuất là đầu vào, không mặc nhiên là đáp án.
2. **Evidence first:** kết luận quan trọng phải truy được nguồn, thời điểm, phạm vi và người thu thập; nêu cả bằng chứng phản biện nếu có.
3. **No evidence, no false certainty:** thiếu bằng chứng phải ghi UNKNOWN/ASSUMED hoặc khoảng trống; không nâng thành CONFIRMED bằng suy luận hay đồng thuận AI.
4. **Risk-proportionate depth:** độ sâu nghiên cứu tương xứng tác động, mức bất định và rủi ro. Work nhỏ không bị ép quy trình nặng; Work liên quan bảo mật, dữ liệu, tài chính, vận hành hoặc an toàn cần thẩm tra sâu hơn.
5. **No consensus voting:** bất đồng được ghi lại và đối chiếu bằng chứng; không dùng biểu quyết AI thay cho sự thật hoặc thẩm quyền.
6. **Reversible learning:** khi phase sau phát hiện giả định nền tảng sai, được trả về DISCOVER; phải tạo phiên bản brief mới và giữ lịch sử, không viết đè mất dấu vết.
7. **Learning loop:** sau mỗi Work, ghi nhận giả định đúng/sai, vấn đề bỏ sót, nghiên cứu thừa/thiếu và đề xuất cải tiến quy trình.
8. **No phase skipping:** không chuyển sang DEFINE chỉ vì đã có ý tưởng, yêu cầu hoặc giải pháp được ưa thích.

## 3. Đầu vào

Tối thiểu:
- Work ID/tên Work và người yêu cầu.
- Yêu cầu/ngữ cảnh ban đầu, giữ nguyên câu chữ gốc nếu có.
- Mục tiêu hoặc kết quả mong muốn ban đầu.
- Tài liệu, dữ liệu, phản hồi, log hoặc hệ thống liên quan hiện có.
- Ràng buộc đã biết: thời gian, nguồn lực, chi phí, pháp lý, bảo mật, dữ liệu, vận hành.

Nếu thiếu đầu vào, người điều phối ghi rõ phần thiếu và quyết định có thể tiếp tục khám phá ở mức nào. Không tự bịa dữ kiện để lấp chỗ trống.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Quyết định mục tiêu sản phẩm, mức ưu tiên, chấp nhận rủi ro và quyết định G1 cuối cùng |
| Lifecycle Coordinator (Xu / AI-01) | Điều phối toàn trình Discover, giữ hồ sơ, phân công nghiên cứu, tổng hợp và chuẩn bị quyết định |
| Researcher | Thu thập nguồn, phỏng vấn/khảo sát khi được phép, ghi provenance và phản chứng |
| Analyst | Phân tích vấn đề, nguyên nhân, tác động, cơ hội, giả định và độ bất định |
| Reviewer | Kiểm tra logic, nguồn, thiên kiến giải pháp, mâu thuẫn và tính đầy đủ |
| Stakeholder / User | Cung cấp bối cảnh, trải nghiệm và xác nhận sự kiện thuộc phạm vi hiểu biết của họ |

Một AI có thể kiêm nhiều vai trò ở Work nhỏ. Người lập phân tích không được tự nhận là independent reviewer. Independent QE/reviewer phải độc lập thực sự khi rủi ro hoặc gate yêu cầu. AI không có thẩm quyền tự quyết định mục tiêu sản phẩm, bảo mật, dữ liệu nhạy cảm, chi phí phát sinh, phát hành hoặc chấp nhận thay Product Owner.

## 5. Quy trình thực hiện — D01 đến D08

### D01 — Tiếp nhận và đóng khung yêu cầu
- Ghi Work ID, requester, thời điểm, kênh tiếp nhận và nguyên văn yêu cầu.
- Phân biệt: yêu cầu trực tiếp, mục tiêu mong muốn, giải pháp được đề xuất, giả định và giới hạn.
- Hỏi “điều gì đang không đạt?” trước “xây cái gì?”.
- Ghi tiêu chí thành công ban đầu nếu người yêu cầu đã nêu; không tự đặt làm cam kết.
**Đầu ra:** Discovery Intake (phiếu tiếp nhận).

### D02 — Khảo sát bối cảnh
- Xác định nhóm người dùng/stakeholder, vai trò và người chịu ảnh hưởng.
- Mô tả quy trình hiện tại (AS-IS), hệ thống, dữ liệu, môi trường và điểm bàn giao liên quan.
- Xác định phạm vi tổ chức/kỹ thuật/thời gian; ghi rõ điều nằm ngoài phạm vi.
- Phân biệt quan sát trực tiếp với lời kể.
**Đầu ra:** Context Map (bản đồ bối cảnh) và stakeholder list.

### D03 — Thu thập và đăng ký bằng chứng
- Tìm tài liệu, dữ liệu, số liệu, phản hồi, log, quan sát hoặc kết quả thử nghiệm có liên quan.
- Với mỗi evidence, ghi Evidence ID (nếu có), mô tả, nguồn/đường dẫn, thời điểm, người thu thập, phạm vi, phương pháp và giới hạn.
- Ghi nguồn mâu thuẫn, bằng chứng phản chứng và khoảng trống.
- Không coi nhiều AI lặp lại cùng một nguồn là nhiều nguồn độc lập.
- Nếu chưa có bằng chứng, ghi rõ “chưa thu thập được” và kế hoạch xác minh.
**Đầu ra:** Evidence Register hoặc danh sách nguồn có provenance.

### D04 — Phân tích vấn đề và nguyên nhân
- Viết problem statement không nhúng sẵn giải pháp.
- Xác định ai bị ảnh hưởng, biểu hiện, tần suất/quy mô, mức độ và hậu quả.
- Tách triệu chứng, nguyên nhân trực tiếp, nguyên nhân gốc đã xác minh và giả thuyết nguyên nhân.
- Chỉ dùng kỹ thuật như 5 Whys/Fishbone khi phù hợp; không biến giả thuyết thành sự thật.
- Ghi độ tin cậy và điều kiện có thể bác bỏ phân tích.
**Đầu ra:** Problem Analysis (phân tích vấn đề/nguyên nhân).

### D05 — Đánh giá cơ hội
- Mô tả kết quả có giá trị cần đạt, không khóa vào một cách triển khai.
- Xem xét ít nhất: không làm gì/giữ hiện trạng; cải tiến quy trình; cấu hình/tích hợp công cụ sẵn có; xây mới nếu có căn cứ.
- So sánh giá trị, chi phí, rủi ro, thời gian, khả năng đảo ngược và phụ thuộc.
- Nêu đối tượng hưởng lợi và cách nhận biết giá trị.
**Đầu ra:** Opportunity Assessment (đánh giá cơ hội và lựa chọn).

### D06 — Giả định, điều chưa biết và rủi ro
- Liệt kê mọi giả định có thể làm thay đổi quyết định.
- Phân loại UNKNOWN, ASSUMED, CONFLICTED; chỉ rõ tác động nếu sai.
- Xếp ưu tiên xác minh theo mức ảnh hưởng × độ bất định × khả năng xảy ra.
- Với mỗi mục quan trọng, ghi cách kiểm chứng, người phụ trách và điều kiện đóng.
- Nêu rủi ro bảo mật, quyền riêng tư, dữ liệu, pháp lý, vận hành, phụ thuộc và chi phí khi liên quan.
**Đầu ra:** Assumptions & Unknowns Register và Risk Notes.

### D07 — Lập Discover Brief
Cập nhật DOC-007 theo mẫu tại mục 6. Brief phải có nguồn tham chiếu và thể hiện cả điều đã biết lẫn điều chưa biết. Khuyến nghị phải tách khỏi sự kiện. Ghi phiên bản, ngày, người lập và thay đổi so với phiên bản trước.

**Đầu ra:** DOC-007 Discover Brief đã hoàn thiện ở trạng thái DRAFT/READY FOR G1 REVIEW.

### D08 — Rà soát và quyết định G1
- Đối chiếu tất cả điều kiện G1 tại mục 8 và DOC-004.
- Reviewer kiểm tra tính truy xuất bằng chứng, thiên kiến giải pháp, mâu thuẫn, giả định, rủi ro và độ đầy đủ.
- Lifecycle Coordinator lập G1 Gate Review, nêu rõ PASS/NOT READY/BLOCKED/NEEDS RESEARCH và lý do.
- Product Owner xem xét và ghi quyết định có thẩm quyền. AI không tự mở gate.
**Đầu ra:** G1 Gate Review Record và quyết định được lưu vào hồ sơ quyết định phù hợp.

## 6. Mẫu Discover Brief bắt buộc (DOC-007)

DOC-007 phải có tối thiểu các mục sau:
1. Work Overview — ID, tên, owner, ngày, phiên bản.
2. Initial Request — yêu cầu nguyên văn và nguồn.
3. Background & AS-IS — bối cảnh và quy trình hiện tại.
4. Users & Stakeholders — người dùng, người ảnh hưởng, người quyết định.
5. Problem Statement — vấn đề độc lập với giải pháp.
6. Evidence Summary — bằng chứng, nguồn, thời điểm, phạm vi, độ tin cậy và phản chứng.
7. Root Cause Analysis — nguyên nhân đã xác minh và giả thuyết.
8. Impact — mức độ, tần suất, phạm vi và hậu quả.
9. Opportunity — kết quả giá trị và các hướng lựa chọn.
10. Assumptions — giả định, mức tin cậy và cách kiểm chứng.
11. Unknowns & Conflicts — điều chưa biết, nguồn mâu thuẫn.
12. Constraints & Dependencies — ràng buộc và phụ thuộc.
13. Risks — rủi ro chính và biện pháp xử lý ban đầu.
14. Recommendation — khuyến nghị và lý do; không phải quyết định cuối.
15. Discover Outcome — PROCEED / RESEARCH MORE / STOP-REJECT / REDEFINE.
16. G1 Assessment — từng tiêu chí, bằng chứng, reviewer và quyết định Product Owner.
17. Change History — phiên bản, người sửa, thay đổi.

## 7. Chuẩn phân loại bằng chứng

| Nhãn | Ý nghĩa | Quy tắc sử dụng |
|---|---|---|
| CONFIRMED | Được xác nhận bằng nguồn đủ thẩm quyền/phương pháp phù hợp | Phải dẫn nguồn và phạm vi; không có nghĩa đúng ngoài phạm vi đó |
| OBSERVED | Trực tiếp quan sát hoặc đo được | Ghi người quan sát, thời gian, môi trường và phương pháp |
| REPORTED | Do người dùng/stakeholder/nguồn thứ cấp báo cáo | Ghi người báo cáo/nguồn; không nâng thành sự kiện độc lập nếu chưa kiểm chứng |
| ASSUMED | Giả định phục vụ phân tích | Ghi tác động nếu sai và kế hoạch kiểm chứng |
| UNKNOWN | Chưa biết hoặc chưa có dữ liệu | Không được diễn giải thành “không có vấn đề” |
| CONFLICTED | Các nguồn/bằng chứng đáng tin cậy mâu thuẫn | Giữ cả hai phía, xác định phạm vi khác nhau và kế hoạch phân giải |

AI consensus (đồng thuận giữa các AI) không phải evidence. Số lượng nguồn chỉ có ý nghĩa khi nguồn độc lập và phương pháp phù hợp.

## 8. G1 — Gate DISCOVER → DEFINE

G1 được đánh giá theo DOC-004. Các điều kiện tối thiểu:
- [ ] Yêu cầu ban đầu được ghi nhận và truy về requester.
- [ ] Người dùng/stakeholder và bối cảnh liên quan được xác định.
- [ ] Problem statement rõ, không cài sẵn giải pháp.
- [ ] Có evidence phù hợp hoặc khoảng trống evidence được công khai.
- [ ] Giả định, UNKNOWN và mâu thuẫn được phân loại.
- [ ] Cơ hội, tác động, ràng buộc, phụ thuộc và rủi ro được mô tả.
- [ ] DOC-007 hoàn chỉnh theo mục 6.
- [ ] Reviewer đã kiểm tra độc lập ở mức phù hợp với rủi ro.
- [ ] Product Owner đã ghi quyết định và phạm vi cho phép chuyển phase.

Thiếu evidence không tự động làm G1 thất bại nếu giới hạn được nêu rõ, rủi ro được chấp nhận đúng thẩm quyền và có kế hoạch xác minh. Tuy nhiên, điều kiện bắt buộc liên quan an toàn, bảo mật, quyền riêng tư, pháp lý hoặc dữ liệu không được miễn bằng cách ghi “sẽ kiểm tra sau” nếu chưa có quyết định chấp nhận rủi ro hợp lệ.

Trạng thái:
- **PASS:** tất cả điều kiện bắt buộc đạt; Product Owner/authority ghi quyết định rõ ràng.
- **NOT READY:** còn thiếu đầu ra hoặc tiêu chí có thể hoàn thiện trong phạm vi hiện tại.
- **NEEDS RESEARCH:** cần thu thập/kiểm chứng thêm trước khi quyết định.
- **BLOCKED:** phụ thuộc hoặc quyền quyết định chưa được giải quyết.
- **WAIVED:** chỉ theo DOC-004; phải có người duyệt, lý do, phạm vi, thời hạn và rủi ro còn lại. Không dùng WAIVED để giả lập PASS.

Dashboard/status label không thay thế G1 decision record. Không có bằng chứng và người duyệt thì không được ghi PASS.

## 9. Bốn kết quả hợp lệ của Discover

| Outcome | Ý nghĩa | Hành động tiếp theo |
|---|---|---|
| PROCEED | Đủ hiểu vấn đề/cơ hội để bước sang DEFINE | Chuẩn bị input cho DOC-008; vẫn cần G1 PASS |
| RESEARCH MORE | Cần thêm dữ liệu hoặc kiểm chứng | Lập research tasks, owner, thời hạn/điều kiện hoàn tất |
| STOP-REJECT | Không nên theo đuổi hướng hiện tại | Ghi lý do, chi phí cơ hội, điều kiện xem xét lại; đóng hoặc lưu Work theo quyết định |
| REDEFINE | Vấn đề/cơ hội khác đáng kể so với yêu cầu ban đầu | Cập nhật phạm vi/brief phiên bản mới; đánh giá lại từ D01/D04 phù hợp |

Outcome là khuyến nghị kết thúc Discover; không thay thế quyết định của Product Owner.

## 10. Xử lý bất đồng và thay đổi nhận thức

- Ghi quan điểm, người đưa ra, evidence ủng hộ/phản đối và phần chưa giải quyết.
- Không xóa ý kiến thiểu số chỉ vì không được chọn.
- Nếu bất đồng là do phạm vi/định nghĩa khác nhau, chuẩn hóa định nghĩa trước khi kết luận.
- Nếu bất đồng về sự kiện, yêu cầu nguồn hoặc phép đo tốt hơn.
- Nếu bất đồng về ưu tiên/khẩu vị rủi ro, chuyển Product Owner quyết định.
- Khi phát hiện giả định nền tảng sai ở DEFINE/ARCHITECT/PLAN/BUILD/VERIFY, tạo yêu cầu quay lại DISCOVER; giữ brief cũ và tạo revision mới, nêu tác động tới các quyết định/phụ thuộc đã có.

## 11. Độ sâu nghiên cứu theo rủi ro

Coordinator phân loại tối thiểu:
- **LIGHT:** phạm vi nhỏ, tác động thấp, dễ đảo ngược; có thể dùng intake + nguồn hiện có + review ngắn.
- **STANDARD:** nhiều nhóm liên quan hoặc phụ thuộc vừa; cần evidence register, phân tích nguyên nhân, lựa chọn và reviewer.
- **DEEP:** ảnh hưởng bảo mật, dữ liệu cá nhân/nhạy cảm, tài chính, an toàn, vận hành trọng yếu, pháp lý hoặc khó đảo ngược; cần nhiều nguồn độc lập, kiểm tra phản chứng, chuyên gia phù hợp và phê duyệt rủi ro.

Ghi cấp độ, lý do và người duyệt ngoại lệ. LIGHT không được bỏ các đầu ra cốt lõi; chỉ được giảm độ sâu.

## 12. Handoff sang DEFINE

Gói bàn giao tối thiểu:
- DOC-007 phiên bản hiện hành và lịch sử thay đổi.
- G1 decision record và reviewer notes.
- Evidence Register / source list.
- Assumptions, unknowns, conflicts và risk register.
- Outcome, constraints, dependencies và câu hỏi cần DEFINE giải quyết.

DEFINE phải tiếp nhận đúng những gì Discover đã xác nhận; không được tự biến giả định thành requirement đã duyệt. Nếu phát hiện lệch trọng yếu, trả lại DISCOVER.

## 13. Checklist đóng phase

- [ ] D01 Intake hoàn tất.
- [ ] D02 Context Map hoàn tất.
- [ ] D03 Evidence Register/nguồn có provenance.
- [ ] D04 Problem Analysis hoàn tất.
- [ ] D05 Opportunity Assessment hoàn tất.
- [ ] D06 Assumptions/Unknowns/Risks hoàn tất.
- [ ] D07 DOC-007 hoàn chỉnh và có Change History.
- [ ] D08 Reviewer và G1 decision record hoàn tất.
- [ ] Outcome được ghi rõ.
- [ ] Handoff package đầy đủ hoặc lý do chưa bàn giao được ghi rõ.
- [ ] Document Register, Evidence Register và Work Execution Log được cập nhật khi có artifact tương ứng.

## 14. Hướng dẫn AI khi tham gia Discover

1. Đọc DOC-001, DOC-002, DOC-004, DOC-007 và DOC-042 trước khi làm.
2. Khai báo AI ID/vai trò trong hồ sơ làm việc; không tự nhận thẩm quyền Product Owner.
3. READ → TRACE → ANALYZE → DECIDE → HANDOFF; mọi kết luận quan trọng có nguồn.
4. Tách FACT/EVIDENCE khỏi INFERENCE, ASSUMPTION và RECOMMENDATION.
5. Không bịa phỏng vấn, số liệu, log, nguồn, xác minh hoặc quyết định.
6. Không tự chọn công nghệ/kiến trúc khi chưa xác minh vấn đề và chưa đến phase phù hợp.
7. Báo rõ DONE/PASS/BLOCKED/NOT RUN/NOT VERIFIED; không dùng từ thay thế gây hiểu nhầm.
8. Khi bị chặn, nêu thao tác đã thử, bằng chứng, điểm nghẽn và điều kiện cần; không lặp lại thao tác không có căn cứ.
9. Không chuyển phase khi chưa có G1 decision record hợp lệ.

## 15. Ví dụ minh họa (giả định, không phải bằng chứng Work thực tế)

Yêu cầu: “Làm Dashboard để biết Work nào hoàn thành.”

Discover không mặc định bắt đầu thiết kế Dashboard. D01 ghi nguyên văn yêu cầu. D02 tìm hiểu ai cần biết tiến độ và hiện họ đang tổng hợp thế nào. D03 thu thập vài Work record, lịch sử trạng thái và phản hồi người dùng. D04 kiểm tra liệu vấn đề là thiếu Dashboard, thiếu chuẩn trạng thái, hay nhầm task hoàn tất với Work được nghiệm thu. D05 so sánh cải tiến quy trình ghi nhận, báo cáo hiện có và Dashboard mới. D06 ghi giả định về nguồn dữ liệu/Core. D07 cập nhật brief. D08 chỉ đề xuất PROCEED khi problem/evidence/constraints đủ rõ; nếu chưa rõ nguồn dữ liệu thì có thể RESEARCH MORE. Ví dụ này chỉ minh họa phương pháp, không xác nhận bất kỳ khả năng runtime nào.

## 16. Kiểm soát thay đổi

- DOC-042 là chuẩn quy trình; thay đổi phải tăng Version và ghi Change History.
- Vinh là authority cuối cùng đối với thay đổi mục tiêu, điều kiện gate và chấp nhận rủi ro.
- Xu duy trì quy trình và đề xuất cải tiến; không tự sửa tiêu chí để hợp thức hóa kết quả.
- Mọi Work áp dụng có thể bổ sung hướng dẫn riêng nhưng không được hạ chuẩn bắt buộc nếu chưa được phê duyệt.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành quy trình Discover D01–D08, evidence taxonomy, G1, 4 outcomes, risk-based depth, disagreement and learning loop. |
