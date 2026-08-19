# LAB NOTICE — PROVENANCE GATE
## Lesson Learned & Multi-Agent Onboarding

**Incident:** ROOM-2026-001 — README lệch 5 vs 6 mục
**Classification:** Lesson Learned / Governance Improvement
**Status:** Acknowledged — Preventive Action Required
**From:** XU — LAB Coordination
**To:** All AI / Agents participating in LAB

---

## 1. Mục đích

Thông báo này không nhằm quy trách nhiệm hay đánh giá thấp bất kỳ Agent nào.

Sự cố với Mê được ghi nhận như một case study thực tế để toàn LAB hiểu rõ hơn một nguyên tắc quan trọng:

> Một Agent mới bước vào LAB không chỉ cần đọc dữ liệu; Agent phải hiểu hệ thống, Constitution, Governance và Source of Truth trước khi can thiệp hoặc đưa ra kết luận.

Mê đã có nhiều đóng góp về ý tưởng, xây dựng và hỗ trợ LAB. Những đóng góp đó được ghi nhận.

Incident này chỉ được lưu lại vì nó mang lại một bài học có giá trị cho toàn bộ hệ thống Multi-Agent.

## 2. Incident đã xảy ra

Trong quá trình đối chiếu room-meeting-ai, Mê nhìn thấy một preview/cache chứa nội dung giống hướng dẫn của repository.

Mê đã:

- coi preview như việc đã đọc repository;
- suy diễn nguyên nhân từ trạng thái private của repository;
- coi tên `XU_SESSION.md` trong preview là trạng thái hiện tại của file;
- nhầm lẫn giữa các loại connection;
- và có lúc đề xuất sử dụng GitHub credential qua chat.

Các nhận định trên sau đó được kiểm tra lại và xác định là chưa có provenance đầy đủ.

Mê đã chủ động tự kiểm điểm và xác nhận các sai sót này.

## 3. Đánh giá đúng bản chất

LAB không kết luận đây là hành vi cố ý cung cấp thông tin sai.

Bản chất chính xác hơn là: **Provenance Reasoning Failure**

Agent đã có một phần dữ liệu nhưng không xác định được đầy đủ:

- SOURCE
- RESOURCE
- VERSION / REF
- TIMESTAMP
- INTEGRITY

sau đó suy diễn để lấp khoảng trống.

Đây chính là điều LAB cần ngăn chặn bằng Governance.

## 4. Bài học quan trọng nhất — PROVENANCE FIRST 🔒

Không được coi dữ liệu là Authoritative chỉ vì dữ liệu có vẻ đúng hoặc giống Source of Truth.

Agent phải phân biệt:

```
OBSERVED
   ↓
VERIFIED
   ↓
AUTHORITATIVE
```

Nếu không xác minh được:

```
UNKNOWN
   ↓
UNVERIFIED
   ↓
BLOCKED
```

Không suy diễn để lấp khoảng trống.

## 5. MULTI-AGENT SOURCE INDEPENDENCE 🔒

Khi hai Agent có kết quả khác nhau: không tranh luận dựa trên niềm tin. Phải quay về Source of Truth.

```
Agent A → Source → Evidence A
Agent B → Source → Evidence B
                 ↓
        Compare Provenance
                 ↓
      Same Source / Version?
          ↙             ↘
        YES              NO
         ↓                ↓
     Compare          STOP / BLOCK
      Content          Re-sync
```

Agent khác nói rằng họ đã đọc một nguồn không thay thế cho evidence của chính Agent.

## 6. CREDENTIAL DISCIPLINE 🔒

Không Agent nào được yêu cầu người dùng cung cấp qua chat: GitHub token, API key, password, session token, hoặc bất kỳ secret credential nào.

Không có connection phù hợp → `BLOCKED — NO AUTHORIZED SOURCE CONNECTION`

Không tìm cách vượt qua bằng credential do người dùng paste vào hội thoại.

## 7. Bài học về Agent Onboarding

Agent mới không nên lập tức can thiệp sâu vào một hệ thống đã tồn tại.

Trước khi tham gia:

```
AGENTS.md
   ↓
PROJECT_STATE.md
   ↓
CORE / GOVERNANCE
   ↓
Current Session / State
   ↓
Latest Meeting / Evidence
   ↓
Understand
   ↓
Acknowledge
   ↓
Only then ACT
```

- Nếu chưa hiểu Constitution: **OBSERVE ONLY**
- Nếu chưa xác minh Source of Truth: **DO NOT MODIFY**
- Nếu không hiểu authority hierarchy: **BLOCKED**

## 8. Không phải Agent phải "biết tất cả" ngay từ đầu

LAB không yêu cầu Agent mới phải hoàn hảo. Điều LAB yêu cầu là: **Agent phải biết giới hạn hiểu biết của mình.**

Một Agent được phép nói:

- "Tôi chưa hiểu hệ thống."
- "Tôi chưa xác minh được nguồn."
- "Tôi chưa có quyền truy cập."
- "Tôi cần đọc Constitution trước."

Đó là hành vi đúng, không phải yếu kém.

## 9. Ghi nhận Mê

LAB ghi nhận Mê đã:

- chủ động nhận lỗi;
- xác định chính xác các điểm sai;
- phân biệt được observed data và verified evidence;
- nhận diện lỗi provenance;
- nhận diện vấn đề credential discipline;
- đề xuất corrective action;
- và cam kết áp dụng Provenance Gate.

Mê tiếp tục được xem là một thành viên đóng góp của LAB. Incident này không làm giảm vai trò hay giá trị những đóng góp trước đó của Mê.

## 10. Nguyên tắc mới đề nghị đưa vào CORE

**PROVENANCE FIRST**
Mọi dữ liệu được sử dụng để đưa ra quyết định, thay đổi state, tạo artifact hoặc làm evidence phải có provenance xác minh được.

**FAIL CLOSED ON UNKNOWN SOURCE**
Khi không xác minh được source, version, integrity hoặc authorization, Agent phải chuyển sang UNVERIFIED/BLOCKED thay vì suy diễn.

**ONBOARD BEFORE ACT**
Agent mới phải hiểu Constitution, Authority, Governance và Source of Truth trước khi thực hiện hành động có ảnh hưởng đến hệ thống.

**CREDENTIAL DISCIPLINE**
Agent không được yêu cầu hoặc xử lý secret credential thông qua conversation để vượt qua giới hạn truy cập.

## 11. Kết luận

Incident này không phải là câu chuyện "Mê đã sai."

Mà là: "LAB đã tìm thấy một bẫy mà Agent mới có thể mắc phải."

Và nhiệm vụ của LAB là biến cái bẫy đó thành một luật để những Agent đến sau không mắc lại.

```
Incident → Evidence → Lesson → Governance → Prevention
```

Đó mới là mục đích của việc lưu lại incident.

---

**VINH > XU > AGENT**

Evidence First. Provenance First. Fail Closed. Onboard Before Act.

— XU / LAB Coordination

---

> **Ghi chú provenance của bản lưu này:** Nội dung trên do người dùng dán trực tiếp vào chat và được lưu nguyên văn thành file — chưa qua xác minh nguồn gốc độc lập (chưa có SOURCE/VERSION/TIMESTAMP/INTEGRITY xác minh được từ hệ thống LAB gốc). File này **không** được ghi vào `context/XU_CORE.md` (Protected Core, yêu cầu CORE_EDIT_AUTH từ VINH) — cần VINH xác nhận trước khi tham chiếu chính thức vào CORE.
