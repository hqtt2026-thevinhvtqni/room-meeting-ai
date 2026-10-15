# ONT CARE - ARCHITECTURE ANALYSIS
## PHÂN TÍCH KIẾN TRÚC VÀ ĐỀ XUẤT CẢI TIẾN

---

## 📊 **TÓM TẮT DỰ ÁN**

- **Tên dự án:** ONT Care - Hệ thống quản lý và chăm sóc thiết bị ONT
- **Work ID:** 98
- **Trạng thái:** Prototype hoàn thiện, chưa sẵn sàng production
- **Ngôn ngữ:** React + TypeScript + TanStack Router
- **Build tool:** Vite 8 + Bun
- **UI Framework:** ShadCN UI + Radix UI + Tailwind CSS v4

---

## 🏗️ **KIẾN TRÚC HIỆN TẠI (AS-IS)**

### **1. Cấu trúc thư mục (Canonical Structure)**
```
work/98/ONT-CARE/
├── 00_ROOT/                    # Work manifest, context, sync target
│   ├── WORK_MANIFEST.md       # Thông tin work
│   ├── WORK_CONTEXT.yaml      # Context YAML
│   └── SYNC_TARGET.yaml       # Sync configuration
│
├── 01_ORIGINAL/               # Original notes & source records
│   ├── legacy_archive/
│   │   ├── README.md
│   │   └── AI_SURVEY_ONCARE.md
│   ├── BIEN_BAN_W98.md
│   └── WORK_98_README.md
│
├── 02_EXTENSION/              # Reserved for approved extensions
│
├── 03_ARCHITECTURE/           # Architecture & plans
│   ├── ROOT_ROADMAP.md
│   ├── PLAN_ONT_CARE_E2E_AUTOMATIC_20261013.md
│   ├── CANONICAL_PARALLEL_WORK_STRUCTURE.md
│   └── GITHUB_PARALLEL_STRUCTURE_20261013.md
│
├── 04_CODE/                   # Application source
│   ├── root-scaffold/         # Root scaffold (empty)
│   │   ├── .gitignore
│   │   ├── bun.lock
│   │   ├── bunfig.toml
│   │   ├── eslint.config.js
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   │
│   └── ont-platform/          # Main application
│       ├── .github/
│       │   └── workflows/
│       │       └── e2e.yml  # CI/CD workflow
│       ├── .prettierignore
│       ├── .prettierrc
│       ├── AGENTS.md         # AI development guidelines
│       ├── package.json      # Dependencies
│       ├── roadmap.md        # Prototype roadmap
│       ├── tsconfig.json
│       ├── vite.config.ts
│       └── src/
│           ├── components/
│           │   └── ui/        # ShadCN UI components
│           │       ├── button.tsx
│           │       └── input.tsx
│           ├── lib/
│           │   ├── deep-links.ts    # Deep link parsing
│           │   ├── error-capture.ts
│           │   ├── error-page.ts
│           │   ├── lovable-error-reporting.ts
│           │   ├── ont-data.ts       # Mock data (100 ONT, 100 customers, etc.)
│           │   └── utils.ts
│           ├── routes/
│           │   ├── __root.tsx       # Root route with providers
│           │   ├── customer.tsx     # Customer mobile app
│           │   ├── index.tsx        # Main dashboard
│           │   └── technician.tsx   # Technician mobile app
│           ├── server.ts
│           └── start.ts
│
├── 05_TEST/                   # Tests & acceptance
│   ├── e2e/
│   │   ├── README.md
│   │   ├── deep_links_e2e.py  # Playwright E2E tests
│   │   └── README.md (duplicate)
│   └── ONT_CARE_E2E_ACCEPTANCE.md
│
├── 06_EVIDENCE/               # Audit & transfer evidence
│   ├── GITHUB_SOURCE_TRANSFER_20261014.md
│   └── SOURCE_AUDIT_20261013.md
│
├── 07_RELEASE/               # Release gate (empty)
│
├── 08_DASHBOARD/             # DASH contract (empty)
│
└── 09_DASHBOARD_PREVIEW/     # Separate preview
    ├── data.json
    ├── index.html
    ├── preview.config.json
    └── product-render.js
```

### **2. Kiến trúc ứng dụng**

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    React Application                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │ │
│  │  │  Dashboard   │  │  Technician  │  │    Customer       │  │ │
│  │  │   (PC)      │  │   (Mobile)   │  │     (Mobile)      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │ │
│  │                                                      │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                Shared Components                       │ │ │
│  │  │  - PlatformContext (State Management)               │ │ │
│  │  │  - Deep Links Parser                               │ │ │
│  │  │  - UI Components (ShadCN)                          │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Data Layer                             │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                Mock Data (In-Memory)                 │ │ │
│  │  │  - 100 ONTs with status, optical, speed, ping        │ │ │
│  │  │  - 100 Customers with address, phone                 │ │ │
│  │  │  - 15 Technicians with area, status                 │ │ │
│  │  │  - 30 Tickets with priority, status                 │ │ │
│  │  │  - 200 LAN Devices                                  │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                    ↓ No Backend Connection ↓
┌─────────────────────────────────────────────────────────────┐
│                      NO BACKEND LAYER                         │
│                    (All data is mocked)                        │
└─────────────────────────────────────────────────────────────┘
```

### **3. Data Flow**

```
User Request
     ↓
┌─────────────────┐
│   React Router   │  (TanStack Router)
└────────┬────────┘
         ↓
┌─────────────────┐
│   Platform       │  (Context Provider)
│   Context        │  - State: tickets, customers, onts
│                  │  - Actions: createTicket, updateTicket, etc.
└────────┬────────┘
         ↓
┌─────────────────┐
│   Mock Data      │  (ont-data.ts)
│   Module         │  - Array.from() generates deterministic data
│                  │  - No persistence
│                  │  - No API calls
└────────┬────────┘
         ↓
┌─────────────────┐
│   UI Components  │  (ShadCN + Radix)
│                  │  - Tables, Cards, Modals
│                  │  - Status indicators
│                  │  - Deep link buttons
└─────────────────┘
```

### **4. Deep Links System**

```typescript
// deep-links.ts
┌─────────────────────────────────────────┐
│  Deep Link Format:                        │
│  - /?ont=ONT-001                          │  → ONT Detail
│  - /?ont=ONT-001&tab=LAN                  │  → ONT Detail + LAN Tab
│  - /?ticket=TK-2401                       │  → Ticket Detail
│  - /technician?ticket=TK-2401             │  → Technician App + Ticket
│  - /customer?ticket=TK-2401              │  → Customer App + Ticket
└─────────────────────────────────────────┘

// Validation:
- Normalize IDs (toUpperCase())
- Bounded string length (max 32 chars)
- Check against valid ONT/ticket IDs
- Return 404 if not found
```

---

## 🔍 **PHÂN TÍCH ĐIỂM MẠNH & ĐIỂM YẾU**

### ✅ **Điểm mạnh (Strengths)**

| STT | Điểm mạnh | Mô tả | Lợi ích |
|-----|-----------|------|---------|
| 1 | **Canonical Structure** | Cấu trúc thư mục theo Work 101 | Dễ quản lý, nhất quán |
| 2 | **Modern Tech Stack** | React 19 + TypeScript + Vite 8 | Hiệu năng cao, developer experience tốt |
| 3 | **Component Library** | ShadCN UI + Radix UI | UI nhất quán, accessible |
| 4 | **Deep Links** | Hệ thống deep links hoàn thiện | Navigation liền mạch giữa apps |
| 5 | **Mock Data** | Dữ liệu mock đầy đủ | Demo hoàn chỉnh |
| 6 | **E2E Tests** | Playwright tests sẵn có | Verify chức năng |
| 7 | **CI/CD Pipeline** | GitHub Actions workflow | Automated testing |
| 8 | **Multi-App** | 3 apps (Dashboard, Technician, Customer) | Phủ đầy nhu cầu |
| 9 | **Responsive Design** | Mobile + Desktop | Tương thích đa thiết bị |
| 10 | **Error Handling** | Error boundaries, error pages | Trải nghiệm người dùng tốt |

### ❌ **Điểm yếu (Weaknesses)**

| STT | Điểm yếu | Mô tả | Rủi ro | Khắc phục |
|-----|----------|------|--------|-----------|
| 1 | **No Authentication** | Không có login/auth | Bất kỳ ai cũng truy cập | P0-C: JWT Auth |
| 2 | **No Persistence** | Dữ liệu chỉ in-memory | Reload mất data | P1-A: LocalStorage/Backend |
| 3 | **No Backend** | Chỉ frontend | Không thể live ONT | P1-B: Backend Service |
| 4 | **CI Path Issue** | Workflow chạy sai path | CI fail | P0-A: Fix working-directory |
| 5 | **Mock Data Honesty** | UI hiển thị live data | Nhầm lẫn | P0-B: Thêm MOCK labels |
| 6 | **Hardcoded Users** | Customer/Technician hardcode | Không multi-user | P0-C: Auth + User DB |
| 7 | **No Role Validation** | Không check role | Access control yếu | P0-C: RBAC |
| 8 | **No Data Sync** | Không đồng bộ | Offline không hoạt động | P1-C: Queue/Sync |
| 9 | **No Real ONT Access** | Chỉ mock | Không thể monitoring | P1-B: ONT Adapters |
| 10 | **No Notifications** | Không thông báo | User không biết trạng thái | P1-D: Notifications |

### ⚠️ **Rủi ro (Risks)**

| STT | Rủi ro | Xác suất | Tác động | Giảm thiểu |
|-----|--------|----------|----------|-------------|
| 1 | **Security Vulnerabilities** | Cao | Cao | Auth + Input Validation |
| 2 | **Data Loss** | Cao | Cao | Persistence + Backup |
| 3 | **Performance Issues** | Trung bình | Cao | Optimize + Caching |
| 4 | **Browser Compatibility** | Trung bình | Trung bình | Test đa trình duyệt |
| 5 | **ONT Protocol Incompatibility** | Cao | Cao | Test đa vendor |
| 6 | **Scalability** | Thấp | Cao | Backend + Database |

---

## 🎯 **ĐỀ XUẤT KIẾN TRÚC MỚI (TO-BE)**

### **1. Kiến trúc mục tiêu**

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    React Application                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │ │
│  │  │  Dashboard   │  │  Technician  │  │    Customer       │  │ │
│  │  │   (PC)      │  │   (Mobile)   │  │     (Mobile)      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │ │
│  │                                                      │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                Shared Components                       │ │ │
│  │  │  - AuthProvider (Authentication)                     │ │ │
│  │  │  - PlatformContext (State Management)               │ │ │
│  │  │  - ONT Adapters (Direct ONT Access)                  │ │ │
│  │  │  - Deep Links Parser                               │ │ │
│  │  │  - UI Components (ShadCN)                          │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    API Layer                              │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                Axios/Fetch                            │ │ │
│  │  │  - Request/Response Interceptors                     │ │ │
│  │  │  - Error Handling                                  │ │ │
│  │  │  - Retry Mechanism                                 │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────────────┘
               ↓ HTTPS/REST
┌──────────────┴──────────────────────────────────────────────┐
│                        Backend Layer                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    NestJS Application                    │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │ │
│  │  │   Auth      │  │  ONT         │  │   Ticket        │  │ │
│  │  │  Module     │  │  Module      │  │   Module        │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │ │
│  │                                                      │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                ONT Access Service                      │ │ │
│  │  │  - TR-069 Adapter                                   │ │ │
│  │  │  - SNMP Adapter                                    │ │ │
│  │  │  - SSH Adapter                                     │ │ │
│  │  │  - Parser/Normalizer                               │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Data Layer                             │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                PostgreSQL Database                     │ │ │
│  │  │  - Users, ONTs, Customers, Tickets, Technicians       │ │ │
│  │  │  - Audit Logs, Notifications                         │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **2. Data Flow mới**

```
User Request
     ↓
┌─────────────────┐
│   React Router   │  (TanStack Router)
└────────┬────────┘
         ↓
┌─────────────────┐
│   AuthProvider   │  (JWT-based Authentication)
└────────┬────────┘
         ↓
┌─────────────────┐
│   API Service    │  (Axios with interceptors)
└────────┬────────┘
         ↓ HTTPS
┌─────────────────┐
│   Backend API    │  (NestJS REST API)
│  - POST /api/auth/login
│  - GET /api/onts
│  - GET /api/tickets
│  - POST /api/onts/{id}/diagnose
└────────┬────────┘
         ↓
┌─────────────────┐
│   Database       │  (PostgreSQL)
│  - Users table
│  - ONTs table
│  - Tickets table
│  - Audit logs
└────────┬────────┘
         ↓
┌─────────────────┐
│   ONT Devices    │  (Real ONT devices)
│  - TR-069
│  - SNMP
│  - SSH
└─────────────────┘
```

---

## 📋 **CHI TIẾT CẢI TIẾN**

### **1. Authentication Layer**

#### **Current:**
```typescript
// customer.tsx
const you = customers[0]  // Hardcoded!

// technician.tsx  
const technician = technicians[0]  // Hardcoded!
```

#### **Proposed:**
```typescript
// auth.ts
interface User {
  id: string;
  name: string;
  email: string;
  role: 'customer' | 'technician' | 'admin';
  ontId?: string;  // For customers
  area?: string;   // For technicians
}

// AuthProvider
const AuthContext = createContext<{
  user: User | null;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
  isAuthenticated: boolean;
}>();

// JWT Storage
const TOKEN_KEY = 'ont-care-token';
const USER_KEY = 'ont-care-user';

// Backend Auth API
POST /api/auth/login
Body: { email, password }
Response: { token, user }

GET /api/auth/me
Headers: { Authorization: 'Bearer <token>' }
Response: { user }
```

#### **Route Protection:**
```typescript
// __root.tsx
function RootComponent() {
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <PlatformProvider>
          <Outlet />
        </PlatformProvider>
      </QueryClientProvider>
    </AuthProvider>
  );
}

// Protected Route Component
function ProtectedRoute({ children, roles }: { children: ReactNode; roles: UserRole[] }) {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (!roles.includes(user.role)) {
    return <Navigate to="/unauthorized" />;
  }
  
  return <>{children}</>;
}

// Usage
<Route path="/" element={
  <ProtectedRoute roles={['admin', 'technician']}>
    <Dashboard />
  </ProtectedRoute>
} />
```

### **2. Backend Service (NestJS)**

#### **File Structure:**
```
backend/
├── src/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.module.ts
│   │   ├── auth.service.ts
│   │   ├── dto/
│   │   │   ├── login.dto.ts
│   │   │   └── register.dto.ts
│   │   └── strategies/
│   │       └── jwt.strategy.ts
│   │
│   ├── ont/
│   │   ├── ont.controller.ts
│   │   ├── ont.module.ts
│   │   ├── ont.service.ts
│   │   ├── dto/
│   │   │   └── ont-filter.dto.ts
│   │   └── entities/
│   │       └── ont.entity.ts
│   │
│   ├── ticket/
│   │   ├── ticket.controller.ts
│   │   ├── ticket.module.ts
│   │   ├── ticket.service.ts
│   │   └── entities/
│   │       └── ticket.entity.ts
│   │
│   ├── ont-access/
│   │   ├── adapters/
│   │   │   ├── tr069.adapter.ts
│   │   │   ├── snmp.adapter.ts
│   │   │   └── ssh.adapter.ts
│   │   ├── ont-access.module.ts
│   │   └── ont-access.service.ts
│   │
│   ├── common/
│   │   ├── filters/
│   │   │   └── http-exception.filter.ts
│   │   └── guards/
│   │       └── roles.guard.ts
│   │
│   └── main.ts
│
├── prisma/
│   └── schema.prisma
│
├── .env
└── package.json
```

#### **Database Schema (Prisma):**
```prisma
// User
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  password  String    // Hashed
  name      String
  role      UserRole  @default(CUSTOMER)
  phone     String?
  address   String?
  ontId     String?   // For customers
  area      String?   // For technicians
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt
}

// ONT
model Ont {
  id          String     @id @default(cuid())
  serial      String     @unique
  model       String
  firmware    String
  customerId  String
  customer    User      @relation(fields: [customerId], references: [id])
  status      OntStatus  @default(ONLINE)
  optical     Float
  uptime      String?
  lastSeen    DateTime?
  wan         String?
  wifi        String?
  speed       Float?
  ping        Float?
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt
}

// Ticket
model Ticket {
  id           String        @id @default(cuid())
  customerId   String
  customer     User         @relation(fields: [customerId], references: [id])
  ontId        String
  ont          Ont          @relation(fields: [ontId], references: [id])
  technicianId String?
  technician   User?        @relation(fields: [technicianId], references: [id])
  issue        String
  priority     Priority
  status       TicketStatus @default(OPEN)
  diagnosis    String?
  action       String?
  testResult   String?
  confirmed    Boolean       @default(false)
  createdAt    DateTime      @default(now())
  updatedAt    DateTime      @updatedAt
}

// LAN Device
model LanDevice {
  id          String   @id @default(cuid())
  ontId       String
  ont         Ont      @relation(fields: [ontId], references: [id])
  name        String
  ip          String
  mac         String
  connection  String
  online      Boolean  @default(true)
  lastSeen    DateTime?
}

// Audit Log
model AuditLog {
  id        String   @id @default(cuid())
  userId    String
  action    String
  entity    String
  entityId  String
  oldValue  Json?
  newValue  Json?
  ip        String?
  userAgent String?
  createdAt DateTime @default(now())
}
```

### **3. ONT Access Adapters**

#### **TR-069 Adapter:**
```typescript
// tr069.adapter.ts
interface TR069Device {
  ip: string;
  username: string;
  password: string;
}

interface ONTInfo {
  serial: string;
  model: string;
  firmware: string;
  status: string;
  optical: number;
  uptime: string;
  wan: string;
  wifi: string;
  speed: number;
  ping: number;
}

class TR069Adapter {
  private client: TR069Client;
  
  constructor(device: TR069Device) {
    this.client = new TR069Client(device);
  }
  
  async getDeviceInfo(): Promise<ONTInfo> {
    const params = await this.client.getParameterValues([
      'DeviceInfo.SerialNumber',
      'DeviceInfo.ModelName',
      'DeviceInfo.SoftwareVersion',
      // ... other params
    ]);
    
    return {
      serial: params['DeviceInfo.SerialNumber'],
      model: params['DeviceInfo.ModelName'],
      firmware: params['DeviceInfo.SoftwareVersion'],
      // ... parse other values
    };
  }
  
  async getSignalInfo(): Promise<{ optical: number }> {
    const params = await this.client.getParameterValues([
      'DeviceInfo.X_ZTE-COM_PONOpticalSignal',
    ]);
    
    return {
      optical: parseFloat(params['DeviceInfo.X_ZTE-COM_PONOpticalSignal']),
    };
  }
}
```

#### **SNMP Adapter:**
```typescript
// snmp.adapter.ts
import { Session } from 'net-snmp';

interface SNMPDevice {
  ip: string;
  community: string;
}

class SNMPAdapter {
  private session: Session;
  
  constructor(device: SNMPDevice) {
    this.session = new Session({ host: device.ip, community: device.community });
  }
  
  async getONTStatus(): Promise<{ status: string; uptime: string }> {
    const result = await this.session.get([
      '1.3.6.1.2.1.1.3.0',  // sysUpTime
      '1.3.6.1.2.1.1.1.0',  // sysDescr
    ]);
    
    return {
      status: 'ONLINE',
      uptime: this.parseUptime(result[0].value),
    };
  }
}
```

### **4. Data Persistence**

#### **Option 1: LocalStorage (Quick Fix - P1-A)**
```typescript
// platform-context.tsx
import { useLocalStorage } from './use-localstorage';

function PlatformProvider({ children }) {
  const [tickets, setTickets] = useLocalStorage('ont-care-tickets', initialTickets);
  const [customers, setCustomers] = useLocalStorage('ont-care-customers', initialCustomers);
  const [onts, setOnts] = useLocalStorage('ont-care-onts', initialOnts);
  
  // ... rest of the code
}

// use-localstorage.ts
export function useLocalStorage<T>(key: string, initialValue: T): [T, Dispatch<SetStateAction<T>>] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });
  
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch {
      // Ignore errors
    }
  };
  
  return [storedValue, setValue];
}
```

#### **Option 2: Backend API (Long-term - P1)**
```typescript
// ont.service.ts (Backend)
@Injectable()
class OntService {
  constructor(@InjectRepository(Ont) private ontRepo: Repository<Ont>) {}
  
  async findAll(filter?: OntFilterDto): Promise<Ont[]> {
    return this.ontRepo.find({ where: filter });
  }
  
  async findOne(id: string): Promise<Ont> {
    return this.ontRepo.findOne({ where: { id } });
  }
  
  async update(id: string, data: Partial<Ont>): Promise<Ont> {
    await this.ontRepo.update(id, data);
    return this.findOne(id);
  }
}

// ont.controller.ts
@Controller('onts')
class OntController {
  constructor(private ontService: OntService) {}
  
  @Get()
  async findAll(@Query() filter?: OntFilterDto) {
    return this.ontService.findAll(filter);
  }
  
  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.ontService.findOne(id);
  }
  
  @Patch(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Ont>) {
    return this.ontService.update(id, data);
  }
}
```

---

## 📈 **LỘ TRÌNH TRIỂN KHAI**

### **Phase 1: P0 - Critical Fixes (1 tuần)**
```
Ngày 1-2: P0-A (CI Fix) + P0-B (Mock Labels)
Ngày 3: P0-D (Build Verify) + P0-E (E2E Verify)
Ngày 4-7: P0-C (Authentication)
```

### **Phase 2: P1 - Core Features (2 tuần)**
```
Tuần 1: P1-A (Persistence) + P1-B (ONT Access)
Tuần 2: P1-C (Offline Sync) + P1-D (Notifications)
```

### **Phase 3: P2 - Enhancements (2 tuần)**
```
Tuần 1: P2-A (AI Diagnosis)
Tuần 2: P2-B (Analytics) + P2-C (Multi-language)
```

---

## 🎯 **KẾT LUẬN & KHUYẾN NGHỊ**

### **Khuyến nghị ưu tiên:**

1. **🔴 P0 Tasks (CRITICAL) - LÀM NGAY:**
   - P0-A: Fix CI/CD Path
   - P0-B: Thêm MOCK Labels
   - P0-D: Verify Build/Lint
   - P0-E: Verify E2E Tests
   - P0-C: Authentication

2. **🟡 P1 Tasks (HIGH) - LÀM SAU P0:**
   - P1-A: LocalStorage Persistence (Quick win)
   - P1-B: Backend Service + ONT Adapters
   - P1-C: Offline-First
   - P1-D: Notifications

3. **🟢 P2 Tasks (MEDIUM) - LÀM SAU P1:**
   - P2-A: AI Diagnosis
   - P2-B: Analytics & Charts
   - P2-C: Multi-language

### **Tech Stack khuyến nghị:**
- **Frontend:** React 19 + TypeScript + Vite 8 + TanStack Router
- **UI:** ShadCN UI + Radix UI + Tailwind CSS v4
- **Backend:** NestJS + PostgreSQL + Prisma
- **Auth:** JWT + Passport.js
- **ONT Access:** TR-069 + SNMP + SSH
- **Testing:** Playwright (E2E) + Vitest (Unit)

### **Tài liệu tham khảo:**
- [AI Execution Plan](./AI_EXECUTION_PLAN.md)
- [P0 Critical Tasks](./P0_CRITICAL_TASKS.md)
- [Source Audit](../06_EVIDENCE/SOURCE_AUDIT_20261013.md)
