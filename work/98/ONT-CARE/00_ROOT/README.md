# ONT CARE - AI EXECUTION DOCUMENTATION
## TÀI LIỆU HƯỚNG DẪN THỰC HIỆN CHO CÁC AI

---

## 📚 **DANH MỤC TÀI LIỆU**

| STT | Tài liệu | Mô tả | Ưu tiên |
|-----|----------|------|--------|
| 1 | [📋 AI_EXECUTION_PLAN.md](./AI_EXECUTION_PLAN.md) | Kế hoạch thực hiện chi tiết cho các AI | ⭐⭐⭐ |
| 2 | [🔴 P0_CRITICAL_TASKS.md](./P0_CRITICAL_TASKS.md) | Danh sách tasks ưu tiên cao nhất | ⭐⭐⭐ |
| 3 | [🏗️ ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md) | Phân tích kiến trúc & đề xuất cải tiến | ⭐⭐⭐ |
| 4 | [📄 WORK_MANIFEST.md](./WORK_MANIFEST.md) | Thông tin cơ bản về Work 98 | ⭐⭐ |
| 5 | [📄 WORK_CONTEXT.yaml](./WORK_CONTEXT.yaml) | Context của Work 98 (YAML) | ⭐⭐ |
| 6 | [🎯 SYNC_TARGET.yaml](./SYNC_TARGET.yaml) | Cấu hình sync target | ⭐ |

---

## 🎯 **QUY TRÌNH THỰC HIỆN**

### **1. ĐỌC TÀI LIỆU**
Trước khi bắt đầu bất kỳ task nào, **BẮT BUỘC** phải đọc:
- ✅ [AI_EXECUTION_PLAN.md](./AI_EXECUTION_PLAN.md) - Toàn bộ kế hoạch
- ✅ [P0_CRITICAL_TASKS.md](./P0_CRITICAL_TASKS.md) - Tasks ưu tiên
- ✅ [ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md) - Kiến trúc

### **2. CHỌN TASK**
Lựa chọn task theo thứ tự ưu tiên:
```
P0 (CRITICAL) → P1 (HIGH) → P2 (MEDIUM)
```

**P0 Tasks (Làm ngay):**
- [ ] P0-A: Fix CI/CD Workflow Path
- [ ] P0-B: Thêm MOCK DATA Labels
- [ ] P0-C: Triển khai Authentication
- [ ] P0-D: Verify Build/Lint/TypeCheck
- [ ] P0-E: Verify E2E Test Suite

### **3. THỰC HIỆN TASK**
1. **Đọc mô tả task** trong [P0_CRITICAL_TASKS.md](./P0_CRITICAL_TASKS.md)
2. **Thực hiện theo hướng dẫn** chi tiết
3. **Test kĩ** trước khi commit
4. **Ghi evidence** sau khi hoàn thành

### **4. GHI EVIDENCE**
Sau khi hoàn thành mỗi task:
```bash
# Tạo file evidence
mkdir -p ../../06_EVIDENCE/
touch ../../06_EVIDENCE/<task_name>_<date>.md
```

**Nội dung evidence phải bao gồm:**
- ✅ Mô tả task
- ✅ Thay đổi đã thực hiện
- ✅ Kết quả verification
- ✅ Logs/screenshots/videos
- ✅ Thời gian hoàn thành

### **5. COMMIT & PUSH**
```bash
# Add changes
git add .

# Commit với message rõ ràng
git commit -m "[P0-A] Fix CI/CD workflow path - working-directory added"

# Push lên branch
git push origin work/98-ont-care
```

---

## 🚀 **BẮT ĐẦU NGAY**

### **Option 1: Làm theo P0 Tasks**
```bash
# Đọc tài liệu
cat 00_ROOT/AI_EXECUTION_PLAN.md
cat 00_ROOT/P0_CRITICAL_TASKS.md

# Bắt đầu với P0-A
cd 04_CODE/ont-platform
# Thực hiện theo hướng dẫn trong P0_CRITICAL_TASKS.md
```

### **Option 2: Làm theo Architecture Analysis**
```bash
# Đọc phân tích kiến trúc
cat 00_ROOT/ARCHITECTURE_ANALYSIS.md

# Triển khai theo đề xuất
cd 04_CODE/ont-platform
# Thực hiện cải tiến kiến trúc
```

---

## 📊 **TÓM TẮT TRẠNG THÁI**

### **✅ Đã hoàn thành:**
- Cấu trúc thư mục canonical
- Prototype React + TypeScript
- 3 apps (Dashboard, Technician, Customer)
- Mock data đầy đủ
- Deep links system
- E2E tests (Playwright)
- CI/CD workflow

### **❌ Chưa hoàn thành:**
- ❌ Authentication (P0-C)
- ❌ CI/CD path fix (P0-A)
- ❌ MOCK labels (P0-B)
- ❌ Build verify (P0-D)
- ❌ E2E verify (P0-E)
- ❌ Backend service
- ❌ Data persistence
- ❌ Direct ONT access
- ❌ Offline mode

### **📈 Acceptance Gates:**
- [ ] G0: Canonical source structure
- [ ] G1: Build success
- [ ] G2: Lint/typecheck success
- [ ] G3: Role isolation
- [ ] G4: Mock data honesty
- [ ] G5: Direct ONT access
- [ ] G6: E2E test coverage
- [ ] G7: Preview functionality
- [ ] G8: No core dependency
- [ ] G9: Security

---

## 📞 **HỖ TRỢ & LIÊN HỆ**

### **Câu hỏi thường gặp:**

**Q: Tôi nên bắt đầu từ đâu?**
A: Đọc [AI_EXECUTION_PLAN.md](./AI_EXECUTION_PLAN.md) → Làm P0-A → P0-B → P0-D → P0-E → P0-C

**Q: Làm sao để verify task?**
A: Xem mục "Verification" trong mỗi task ở [P0_CRITICAL_TASKS.md](./P0_CRITICAL_TASKS.md)

**Q: Evidence ghi như thế nào?**
A: Xem ví dụ trong [SOURCE_AUDIT_20261013.md](../06_EVIDENCE/SOURCE_AUDIT_20261013.md)

**Q: Có thể thay đổi tech stack không?**
A: **KHÔNG** - Phải theo tech stack đã định trong [AI_EXECUTION_PLAN.md](./AI_EXECUTION_PLAN.md)

---

## 🔗 **LINKS QUAN TRỌNG**

- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Branch:** `work/98-ont-care`
- **Canonical Root:** `work/98/ONT-CARE/`
- **App Source:** `work/98/ONT-CARE/04_CODE/ont-platform/`
- **Tests:** `work/98/ONT-CARE/05_TEST/`
- **Evidence:** `work/98/ONT-CARE/06_EVIDENCE/`

---

## 📝 **CHANGELOG**

| Ngày | Thay đổi | Tác giả |
|------|----------|---------|
| 2026-10-15 | Tạo tài liệu AI Execution | Vibe Code (Mistral AI) |
| 2026-10-15 | Thêm P0 Critical Tasks | Vibe Code |
| 2026-10-15 | Thêm Architecture Analysis | Vibe Code |

---

## 🎓 **BEST PRACTICES**

### **1. Code Quality**
- ✅ Sử dụng TypeScript strict mode
- ✅ Follow ESLint/Prettier rules
- ✅ No console.log in production
- ✅ Meaningful variable names
- ✅ Comments cho logic phức tạp

### **2. Testing**
- ✅ Test trước khi commit
- ✅ Run lint/typecheck
- ✅ Verify deep links
- ✅ Test trên mobile/desktop

### **3. Documentation**
- ✅ Ghi evidence sau mỗi task
- ✅ Commit message rõ ràng
- ✅ Update roadmap nếu có thay đổi

### **4. Security**
- ✅ Không hardcode credentials
- ✅ Không commit secrets
- ✅ Input validation
- ✅ Role-based access control

---

## 🏆 **SUCCESS METRICS**

### **P0 Success (1 tuần):**
- ✅ 100% P0 tasks hoàn thành
- ✅ Tất cả acceptance gates (G0-G9) PASS
- ✅ CI/CD pipeline hoạt động
- ✅ E2E tests PASS

### **P1 Success (2 tuần):**
- ✅ Backend service deployed
- ✅ Direct ONT access hoạt động
- ✅ Data persistence implemented
- ✅ Offline mode hoạt động

### **P2 Success (2 tuần):**
- ✅ AI diagnosis integrated
- ✅ Analytics dashboard hoạt động
- ✅ Multi-language support
- ✅ Production deployment

---

## 💡 **TIPS CHO CÁC AI**

1. **Đọc kĩ trước khi code** - Tránh làm sai hoặc thiếu
2. **Test thường xuyên** - Đừng đợi đến cuối mới test
3. **Ghi evidence ngay** - Đừng quên ghi lại kết quả
4. **Follow canonical structure** - Đừng tạo files ngoài cấu trúc
5. **Ask for clarification** - Nếu không chắc, hỏi trước khi làm

---

**📌 GHI CHÚ:** Tất cả các AI làm việc trên dự án này **BẮT BUỘC** phải tuân thủ các tài liệu trong thư mục này. Việc không tuân thủ có thể dẫn đến conflicts, errors, hoặc work bị reject.

---

*Last updated: 2026-10-15 by Vibe Code (Mistral AI)*
