# P0 CRITICAL TASKS - PRIORITY LIST
## DANH SÁCH CÁC TASK ƯU TIÊN CAO NHẤT CẦN THỰC HIỆN NGAY

---

## 📌 **HƯỚNG DẪN THỰC HIỆN**

### ✅ **Quy tắc chung:**
1. **Đọc kĩ** file `AI_EXECUTION_PLAN.md` trước khi bắt đầu
2. **Ghi evidence** sau khi hoàn thành mỗi task
3. **Không merge** nếu chưa có evidence
4. **Test kĩ** trước khi commit
5. **Tuân thủ** các acceptance gates (G0-G9)

### 📁 **Vị trí lưu evidence:**
```
work/98/ONT-CARE/06_EVIDENCE/
├── p0_a_ci_fix_20261015.md          # P0-A evidence
├── p0_b_mock_labels_fix_20261015.md # P0-B evidence
├── p0_c_auth_20261015.md           # P0-C evidence
├── p0_d_build_verify_20261015.md    # P0-D evidence
└── p0_e_e2e_verify_20261015.md     # P0-E evidence
```

---

## 🔴 **P0-A: FIX CI/CD WORKFLOW PATH**

### 📋 **Mô tả:**
CI workflow hiện tại chạy `bun install` từ repository root, nhưng `package.json` nằm ở `work/98/ONT-CARE/04_CODE/ont-platform/`. Cần fix path.

### 🎯 **Mục tiêu:**
- CI/CD pipeline chạy đúng thư mục
- Build thành công trên GitHub Actions

### 📝 **Tasks:**

#### Task P0-A-1: Sửa file e2e.yml
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/.github/workflows/e2e.yml`

**Thay đổi:**
```yaml
# BEFORE (line 26-27):
- name: Install app dependencies
  run: bun install

# AFTER:
- name: Install app dependencies
  working-directory: work/98/ONT-CARE/04_CODE/ont-platform
  run: bun install
```

**Thay đổi thêm:**
```yaml
# BEFORE (line 30-31):
- name: Start dev server
  run: |
    nohup bun run dev > dev-server.log 2>&1 &

# AFTER:
- name: Start dev server
  working-directory: work/98/ONT-CARE/04_CODE/ont-platform
  run: |
    nohup bun run dev > dev-server.log 2>&1 &
```

**Thay đổi thêm:**
```yaml
# BEFORE (line 35):
- name: Run deep link E2E suite
  run: python3 e2e/deep_links_e2e.py | tee e2e-output.txt

# AFTER:
- name: Run deep link E2E suite
  working-directory: work/98/ONT-CARE/04_CODE/ont-platform
  run: python3 e2e/deep_links_e2e.py | tee e2e-output.txt
```

### ✅ **Verification:**
1. Chạy locally:
   ```bash
   cd work/98/ONT-CARE/04_CODE/ont-platform
   bun install
   bun run build
   ```
2. Push lên GitHub và check CI chạy thành công

### 📊 **Evidence:**
- [ ] File `e2e.yml` đã được sửa
- [ ] Local build thành công
- [ ] CI trên GitHub chạy PASS
- [ ] Logs lưu tại `06_EVIDENCE/p0_a_ci_fix_20261015.md`

### ⏱️ **Thời gian ước tính:** 1-2 giờ

### 🏷️ **Priority:** CRITICAL

---

## 🔴 **P0-B: THÊM MOCK DATA LABELS (UI HONESTY)**

### 📋 **Mô tả:**
Dashboard hiện thị "Hệ thống hoạt động" thay vì "DEMO · DỮ LIỆU MẪU (MOCK)". Cần thêm label rõ ràng để người dùng biết đây là mock data.

### 🎯 **Mục tiêu:**
- UI hiển thị rõ ràng đây là DEMO mode
- Người dùng không bị nhầm lẫn với live data

### 📝 **Tasks:**

#### Task P0-B-1: Sửa label trên Dashboard
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/index.tsx`

**Tìm dòng:** (khoảng line 150)
```tsx
<span className="system-live"><span/> HỆ THỐNG HOẠT ĐỘNG</span>
```

**Thay bằng:**
```tsx
<span className="system-live"><span/> DEMO · DỮ LIỆU MẪU (MOCK)</span>
```

#### Task P0-B-2: Sửa label trên Technician App
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/technician.tsx`

**Tìm và thay:** Tất cả chỗ hiển thị trạng thái hệ thống
```tsx
# BEFORE:
<span>Hệ thống hoạt động</span>

# AFTER:
<span>DEMO · DỮ LIỆU MẪU (MOCK)</span>
```

#### Task P0-B-3: Sửa label trên Customer App
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/customer.tsx`

**Tìm và thay:** Tất cả chỗ hiển thị trạng thái kết nối
```tsx
# BEFORE:
<small>Đang hoạt động</small>

# AFTER:
<small>DEMO · Đang hoạt động (MOCK)</small>
```

### ✅ **Verification:**
1. Chạy dev server:
   ```bash
   cd work/98/ONT-CARE/04_CODE/ont-platform
   bun run dev
   ```
2. Mở browser tại `http://localhost:8080`
3. Kiểm tra các app (Dashboard, Technician, Customer) hiển thị label MOCK

### 📊 **Evidence:**
- [ ] Screenshots của Dashboard, Technician, Customer app
- [ ] Code changes đã commit
- [ ] Logs lưu tại `06_EVIDENCE/p0_b_mock_labels_fix_20261015.md`

### ⏱️ **Thời gian ước tính:** 30 phút

### 🏷️ **Priority:** CRITICAL

---

## 🔴 **P0-C: TRIỂN KHAI AUTHENTICATION CƠ BẢN**

### 📋 **Mô tả:**
Hiện tại không có authentication. Customer/Technician được xác định bằng hardcode ID. Cần triển khai JWT-based authentication.

### 🎯 **Mục tiêu:**
- Mỗi user phải đăng nhập
- Role-based access control
- Server-side validation

### 📝 **Tasks:**

#### Task P0-C-1: Tạo Auth Context
**File mới:** `work/98/ONT-CARE/04_CODE/ont-platform/src/lib/auth.ts`

**Nội dung:**
```typescript
import { createContext, useContext } from 'react';

type UserRole = 'customer' | 'technician' | 'admin';
type User = {
  id: string;
  name: string;
  role: UserRole;
  token: string;
};

type AuthContextType = {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
  role: UserRole | null;
};

export const AuthContext = createContext<AuthContextType>({
  user: null,
  login: async () => false,
  logout: () => {},
  isAuthenticated: false,
  role: null,
});

export function useAuth() {
  return useContext(AuthContext);
}
```

#### Task P0-C-2: Tạo Login Page
**File mới:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/login.tsx`

**Nội dung:** Basic login form với email/password

#### Task P0-C-3: Sửa Route Protection
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/__root.tsx`

**Thay đổi:**
```tsx
// BEFORE:
function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <PlatformProvider><Outlet /></PlatformProvider>
    </QueryClientProvider>
  );
}

// AFTER:
function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <PlatformProvider><Outlet /></PlatformProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

#### Task P0-C-4: Protect Routes
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/index.tsx`

**Thay đổi:** Thêm check authentication
```tsx
// Thêm ở đầu component Dashboard()
const { isAuthenticated, role } = useAuth();

if (!isAuthenticated) {
  return <Navigate to="/login" />;
}

// Chỉ admin mới thấy full dashboard
if (role !== 'admin' && role !== 'technician') {
  return <Navigate to="/customer" />;
}
```

#### Task P0-C-5: Sửa Customer Route
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/customer.tsx`

**Thay đổi:**
```typescript
// BEFORE:
const you = customers[0] ?? {id:'KH-001',name:'Nguyễn Minh An',...};

// AFTER:
const { user } = useAuth();
const you = customers.find(c => c.id === user?.id) ?? user;

// Nếu không phải customer, redirect
if (user?.role !== 'customer') {
  return <Navigate to="/login" />;
}
```

#### Task P0-C-6: Sửa Technician Route
**File:** `work/98/ONT-CARE/04_CODE/ont-platform/src/routes/technician.tsx`

**Thay đổi:**
```typescript
// BEFORE:
const technician = technicians[0] ?? {id:'KT-001',name:'Kỹ thuật viên',...};

// AFTER:
const { user } = useAuth();
const technician = technicians.find(t => t.id === user?.id) ?? user;

// Nếu không phải technician, redirect
if (user?.role !== 'technician') {
  return <Navigate to="/login" />;
}
```

### ✅ **Verification:**
1. Chạy dev server
2. Truy cập `/` → redirect đến `/login`
3. Đăng nhập với role customer → chỉ thấy Customer App
4. Đăng nhập với role technician → chỉ thấy Technician App
5. Đăng nhập với role admin → thấy full Dashboard

### 📊 **Evidence:**
- [ ] Auth context đã tạo
- [ ] Login page hoạt động
- [ ] Route protection hoạt động
- [ ] Role-based access working
- [ ] Logs lưu tại `06_EVIDENCE/p0_c_auth_20261015.md`

### ⏱️ **Thời gian ước tính:** 2-3 ngày

### 🏷️ **Priority:** CRITICAL

---

## 🔴 **P0-D: VERIFY BUILD/LINT/TYPECHECK**

### 📋 **Mô tả:**
Chạy verify build, lint, typecheck để đảm bảo code chất lượng.

### 🎯 **Mục tiêu:**
- Build production thành công
- Lint không errors
- TypeScript compile không errors

### 📝 **Tasks:**

#### Task P0-D-1: Chạy bun install
```bash
cd work/98/ONT-CARE/04_CODE/ont-platform
bun install
```

#### Task P0-D-2: Chạy build
```bash
bun run build
```

**Expected:**
- Build thành công
- Output trong `dist/` folder
- Không có errors

#### Task P0-D-3: Chạy lint
```bash
bun run lint
```

**Expected:**
- Exit code 0
- Không có errors
- Có thể có warnings (ghi lại để fix sau)

#### Task P0-D-4: Chạy typecheck
```bash
bun run build  # Vite sẽ chạy typecheck
# Hoặc:
tsc --noEmit
```

**Expected:**
- Không có type errors
- Exit code 0

### ✅ **Verification:**
- [ ] `bun install` thành công
- [ ] `bun run build` thành công
- [ ] `bun run lint` PASS
- [ ] TypeScript compile PASS

### 📊 **Evidence:**
- [ ] `build_log_20261015.txt`
- [ ] `lint_log_20261015.txt`
- [ ] `typecheck_log_20261015.txt`
- [ ] Logs lưu tại `06_EVIDENCE/p0_d_build_verify_20261015.md`

### ⏱️ **Thời gian ước tính:** 1-2 giờ

### 🏷️ **Priority:** CRITICAL

---

## 🔴 **P0-E: VERIFY E2E TEST SUITE**

### 📋 **Mô tả:**
Chạy E2E test suite để verify deep links và chức năng cơ bản.

### 🎯 **Mục tiêu:**
- Tất cả test cases PASS
- Deep links hoạt động
- Cross-app navigation hoạt động

### 📝 **Tasks:**

#### Task P0-E-1: Setup Playwright
```bash
cd work/98/ONT-CARE/04_CODE/ont-platform
pip install playwright
playwright install --with-deps chromium
```

#### Task P0-E-2: Chạy dev server
```bash
bun run dev
```

#### Task P0-E-3: Chạy E2E tests
```bash
python3 e2e/deep_links_e2e.py | tee e2e-output.txt
```

**Expected:**
- Exit code 0
- Tất cả test cases PASS
- Không có failing cases

#### Task P0-E-4: Fix failing tests (nếu có)
- Phân tích failing cases
- Fix code
- Re-run tests

### ✅ **Verification:**
- [ ] Playwright installed
- [ ] Dev server chạy
- [ ] E2E tests PASS
- [ ] Exit code 0

### 📊 **Evidence:**
- [ ] `e2e-output.txt`
- [ ] Screenshots của failing cases (nếu có)
- [ ] Logs lưu tại `06_EVIDENCE/p0_e_e2e_verify_20261015.md`

### ⏱️ **Thời gian ước tính:** 2-3 giờ

### 🏷️ **Priority:** CRITICAL

---

## 📊 **TÓM TẮT P0 TASKS**

| Task | Mô tả | Thời gian | Priority | Status |
|------|-------|-----------|----------|--------|
| P0-A | Fix CI/CD Path | 1-2 giờ | CRITICAL | ⬜ Pending |
| P0-B | Thêm MOCK Labels | 30 phút | CRITICAL | ⬜ Pending |
| P0-C | Authentication | 2-3 ngày | CRITICAL | ⬜ Pending |
| P0-D | Build/Lint Verify | 1-2 giờ | CRITICAL | ⬜ Pending |
| P0-E | E2E Verify | 2-3 giờ | CRITICAL | ⬜ Pending |

---

## 🚀 **BẮT ĐẦU THỰC HIỆN**

### **Bước 1: Chuẩn bị môi trường**
```bash
cd work/98/ONT-CARE/04_CODE/ont-platform
git checkout work/98-ont-care
git pull origin work/98-ont-care
bun install
```

### **Bước 2: Thực hiện theo thứ tự**
1. **P0-A** → Fix CI/CD Path
2. **P0-B** → Thêm MOCK Labels
3. **P0-D** → Verify Build/Lint
4. **P0-E** → Verify E2E Tests
5. **P0-C** → Authentication (mất thời gian nhất)

### **Bước 3: Ghi evidence sau mỗi task**
- Tạo file evidence trong `06_EVIDENCE/`
- Ghi logs, screenshots, videos
- Commit và push

---

## 📞 **LIÊN HỆ**

Nếu có câu hỏi hoặc blocker, hãy:
1. Tạo issue trên GitHub
2. Comment trực tiếp trên file
3. Liên hệ Vinh (Project Owner)

---

**Tài liệu tham khảo:**
- [AI Execution Plan](./AI_EXECUTION_PLAN.md)
- [Work Manifest](./WORK_MANIFEST.md)
- [Work Context](./WORK_CONTEXT.yaml)
