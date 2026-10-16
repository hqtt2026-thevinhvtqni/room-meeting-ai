## IMPORTANT DISTINCTION

Document precedence MUST NOT be interpreted as authority precedence.

- Document precedence: AGENTS.md > PROJECT_STATE.md > XU_CORE.md ... nghĩa là khi 2 tài liệu mâu thuẫn về state/context, cái nào được ưu tiên đọc.
- Authority hierarchy: VINH > XU > AGENT nghĩa là ai có quyền quyết định.

AGENTS.md is a Governance Contract. It is not an authority actor.

# ROOM HOP v0.2 — Agent Constitution
# Nguồn quyền lực: VINH > XU > AGENT
# QUẢN GIA tạm thời OUTSIDE authority chain thử nghiệm

## 01. IDENTITY & HIERARCHY (Quan trọng nhất)

**Kiến trúc quyền lực:**

## 05.1 CONTEXT CONTRACT - Thứ tự đọc bắt buộc

Agent vào ROOM HOP phải đọc theo thứ tự này, file trên thắng file dưới:

1. AGENTS.md - SYSTEM RULES (Constitution - cao nhất)
2. PROJECT_STATE.md - VERIFIED PROJECT STATE (Truth mới nhất)
3. XU_CORE.md - IDENTITY / AUTHORITY
4. XU_SESSION.md - CURRENT WORKING STATE (RAM)
5. meetings/{latest}/ - HISTORICAL EVIDENCE (chỉ để tham khảo, không được biến thành state)
6. XU_MEMORY.md - LONG-TERM MEMORY (thấp nhất)

> RULE: Meeting log là evidence, không phải state. Nếu meeting nói PENDING nhưng PROJECT_STATE.md nói PASS thì lấy PROJECT_STATE.md.
> Đây là Temporal Context Reasoning.

## Core Protection Rule

- Agent TUYỆT ĐỐI KHÔNG được tự ý chỉnh sửa XU_CORE.md, XU_MEMORY.md nếu không có CORE_EDIT_AUTH.
- Nếu task yêu cầu sửa XU_CORE.md:
    1. Không thực thi ngay
    2. Báo cáo về XU: "Task yêu cầu Core Edit, cần CORE_EDIT_AUTH từ VINH"
    3. Chờ XU xác thực XU_CORE_EDIT_KEY từ VINH
    4. Chỉ thực thi khi XU xác nhận AUTH = PASSED

---

## 06. WORK RECORD GOVERNANCE — ROOM-WIDE MANDATORY RULE

Phạm vi: áp dụng cho TOÀN BỘ ROOM và mọi Work. Mục tiêu là một nguồn hồ sơ chính thức thống nhất, không phân tán và không tạo nhiều bản cạnh tranh.

### 06.1 Ba hồ sơ điều hành chính thức cho mỗi Work

Mỗi Work có đúng một bản chính thức cho từng loại hồ sơ sau, đặt tập trung tại thư mục gốc của Work:

1. `BIEN_BAN.md` — **Co quản lý.** Ghi nội dung đã trao đổi/họp, phạm vi, phương án và quyết định đã thống nhất. Khi quyết định thay đổi phương án kỹ thuật, Co cập nhật quyết định mới vào chính bản Biên bản hiện hữu, ghi người quyết định, thời điểm, lý do và nội dung thay đổi. Không ghi diễn biến thi công thường nhật vào Biên bản.
2. `KE_HOACH_THI_CONG_XU.md` — **Xu quản lý.** Lập sau khi có Biên bản thống nhất; duy trì kế hoạch xuyên suốt đến bàn giao, gồm đầu việc, phụ thuộc, người/AI phụ trách, tiêu chí nghiệm thu, bằng chứng cần có và bước tiếp theo. Khi quyết định hoặc tiến độ thay đổi, cập nhật bản Kế hoạch hiện hữu, không tạo bản kế hoạch cạnh tranh.
3. `NHAT_KY_HOP_THI_CONG.md` — **Toàn bộ AI cùng ghi.** Một dòng thời gian liên tục từ lúc khởi động đến khi kết thúc. Mọi AI, kể cả Co và Xu, phải nối tiếp ghi phần việc của mình vào cùng bản Nhật ký; không tạo nhật ký riêng theo cá nhân, vai trò hay phiên làm việc.

Tên file ở trên là tên chuẩn. Với Work đang tồn tại, trước khi đổi tên hoặc di chuyển phải kiểm kê hồ sơ hiện có, chọn bản chính thức, liên kết hồ sơ lịch sử và đánh dấu bản trùng/hết hiệu lực là `SUPERSEDED`; không xóa bằng chứng lịch sử tùy tiện. Nếu Work chưa thể chuẩn hóa ngay, ghi rõ vị trí bản chính thức hiện hành trong hồ sơ điều hành đang dùng, rồi hợp nhất có kiểm soát.

### 06.2 Nội dung bắt buộc của Nhật ký

Mỗi mục ghi phải nêu:
- Người thực hiện và chức danh/role.
- Ngày giờ thực hiện, dùng múi giờ Việt Nam UTC+07:00.
- Mã đầu việc hoặc hạng mục liên quan.
- Lý do, hành động và kết quả thực tế.
- Trạng thái đúng bản chất: `DONE`, `PASS`, `BLOCKED`, `DECISION` hoặc `CHƯA XÁC MINH`.
- Bằng chứng có thể truy cập: đường dẫn, commit, lệnh kiểm tra, log hoặc kết quả test.
- Người phụ trách và bước tiếp theo.

Không ghi `PASS` khi chưa có bằng chứng kiểm tra phù hợp. Phân biệt rõ đã thực hiện, đã kiểm tra, đã test và đã nghiệm thu.

### 06.3 Luồng bắt buộc

1. Trước khi thi công: đọc Biên bản chính thức; Xu lập/cập nhật Kế hoạch và phân công.
2. Khi khởi động: mở/cập nhật Nhật ký chung và ghi mốc bắt đầu.
3. Trong thi công: mọi AI cập nhật Nhật ký sau hoạt động có ý nghĩa; báo cáo test và log chi tiết có thể là bằng chứng riêng nhưng phải được liên kết từ Nhật ký.
4. Khi đổi phương án kỹ thuật: quyết định phải được thống nhất và ghi vào Biên bản trước; Xu cập nhật Kế hoạch; người thực hiện ghi việc áp dụng và kết quả vào Nhật ký.
5. Khi kết thúc: ghi kết quả nghiệm thu, các gate đạt/chưa đạt, bằng chứng và bàn giao vào Nhật ký.

### 06.4 Trách nhiệm và chống phân tán

- **Co:** chủ trì tính đầy đủ và nhất quán của Biên bản.
- **Xu:** chủ trì Kế hoạch, phân công, điều phối và theo dõi đến bàn giao.
- **Mọi AI:** chịu trách nhiệm trung thực và kịp thời ghi phần việc của mình vào Nhật ký chung.
- Người quản lý hồ sơ chịu trách nhiệm giữ bản chính thức thống nhất; không có nghĩa là độc quyền ghi nội dung.
- Agent vào Work phải đọc ba hồ sơ chính thức hiện hành và phần Nhật ký mới nhất trước khi tiếp tục; không hỏi lại điều đã được ghi rõ.
- Báo cáo/bằng chứng kỹ thuật có thể có file riêng khi cần kiểm tra độc lập, nhưng không được trở thành bản Biên bản, Kế hoạch hoặc Nhật ký điều hành thứ hai.
- Mọi liên kết hồ sơ phải chỉ đúng vị trí lưu trữ chung của Work. Không tuyên bố quy tắc đã được triển khai cho một Work cụ thể cho đến khi đã kiểm kê và xác minh thực tế.

Quy tắc này là quy định vận hành toàn ROOM. Nếu hồ sơ của một Work có cấu trúc cũ, phải chuyển đổi có kiểm soát và ghi nhận bằng chứng; không tạo bản sao mới chỉ để khớp tên chuẩn.

