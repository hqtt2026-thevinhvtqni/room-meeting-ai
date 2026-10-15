# Security Review - Work 98 ONT Care

**Date:** 2026-10-15  
**Scope:** Identity management, access control, deep links, data isolation  
**Status:** ANALYZED (No fixes implemented - awaiting Vinh's approval)

---

## Executive Summary

The ONT Care application is a **frontend-only prototype** using hardcoded mock data. The security review identified **CRITICAL** and **HIGH** severity issues related to identity management and access control. **No authentication mechanism exists**, and the application relies on hardcoded array indices for user identity.

**Key Finding:** The system uses `customers[0]` and `technicians[0]` as default identities, meaning ALL users access the same hardcoded accounts (KH-001, KT-001). There is NO user differentiation, NO login flow, and NO session management.

---

## Findings

### F-001: Hardcoded Identity (CRITICAL)

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Status** | CONFIRMED |
| **Evidence** | Code inspection |
| **Impact** | All users share same identity; no user differentiation |
| **Affected Files** | `src/routes/customer.tsx:59`, `src/routes/technician.tsx:58`, `src/routes/index.tsx:1548` |

**Description:**
```typescript
// customer.tsx line 59
const you = customers[0] ?? { id: "KH-001", ... };

// technician.tsx line 58
const technician = technicians[0] ?? { id: "KT-001", ... };

// index.tsx line 1548
{t.customerId === customers[0]?.id && ...}
```

All users accessing the Customer App are treated as `KH-001` (Nguyen Minh An). All users accessing the Technician App are treated as `KT-001`. There is no way to switch users or authenticate as a different user.

**Risk:** Complete lack of identity isolation. Any user can access any customer's data by manipulating deep links.

**Recommendation:** Implement proper authentication with JWT/OAuth2. Store user identity in secure session. **REQUIRES VINH'S APPROVAL** before implementation.

---

### F-002: No Access Control - Cross-Customer Data Access (CRITICAL)

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Status** | CONFIRMED |
| **Evidence** | Code inspection, E2E test case |
| **Impact** | Users can access other customers' tickets |
| **Affected Files** | `src/routes/customer.tsx:78` |

**Description:**
```typescript
// customer.tsx line 78
const myTickets = tickets.filter((t) => t.customerId === you.id);
```

The filter uses `you.id` which is hardcoded to `KH-001`. However, the deep link validation in `parseDeepLink` does NOT validate that the ticket belongs to the current user. The E2E test explicitly checks:

```python
# From deep_links_e2e.py
("customer: other customer's ticket blocked", "/customer?ticket=TK-2401", [NF, "không thuộc tài khoản"], ["Kỹ thuật viên:"]),
```

This test expects the system to BLOCK access to TK-2401 (which belongs to a different customer), but the current implementation only filters the ticket list - it does NOT prevent direct access via deep link.

**Evidence from code:** In `index.tsx` line 1548, there's a conditional render:
```typescript
{t.customerId === customers[0]?.id && (
  <Link to="/customer" search={{ ticket: t.id }}>
    <Users size={16} /> Mở trong App Khách
  </Link>
)}
```

This link is only shown for tickets belonging to KH-001, but users can still manually navigate to `/customer?ticket=TK-2401` and the customer app will display it (since it only filters the list, not the direct access).

**Risk:** Complete data isolation failure. Any user can access any ticket by knowing its ID.

**Recommendation:** Add access control check in customer route: `if (openTicket && openTicket.customerId !== you.id) return <NotAuthorized />`. **REQUIRES VINH'S APPROVAL**.

---

### F-003: Deep Link Validation Bypass (HIGH)

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Status** | CONFIRMED |
| **Evidence** | Code inspection |
| **Impact** | Malicious deep links can access any resource |
| **Affected Files** | `src/lib/deep-links.ts` |

**Description:**
```typescript
// deep-links.ts
const clean = (value: unknown) =>
  typeof value === "string" && value.trim() ? value.trim().toUpperCase().slice(0, 32) : undefined;

export function parseDeepLink(raw: Record<string, unknown>): DeepLinkSearch {
  const out: DeepLinkSearch = {};
  const ont = clean(raw["ont"]);
  const ticket = clean(raw["ticket"]);
  if (ont) out.ont = ont;
  if (ticket) out.ticket = ticket;
  if (typeof raw["tab"] === "string" && raw["tab"].trim()) out.tab = raw["tab"].trim().slice(0, 32);
  return out;
}
```

The `parseDeepLink` function only sanitizes input (uppercase, trim, length limit). It does NOT validate:
- Whether the ONT exists
- Whether the ticket exists
- Whether the user has permission to access the resource
- Whether the resource belongs to the user

**Risk:** Any user can access any ONT or ticket by ID, regardless of ownership.

**Recommendation:** Add validation layer that checks resource existence and user permissions. **REQUIRES VINH'S APPROVAL**.

---

### F-004: No Authentication Flow (HIGH)

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Status** | CONFIRMED |
| **Evidence** | Code inspection |
| **Impact** | No user authentication; all users are anonymous |
| **Affected Files** | Entire application |

**Description:**
There is NO authentication mechanism in the application:
- No login page
- No login form
- No JWT token handling
- No session storage
- No OAuth2 integration
- No backend authentication API

The application assumes identity based on which app is being used (customer, technician, dashboard).

**Risk:** No way to identify or authenticate users. All access is anonymous and shared.

**Recommendation:** Implement authentication flow. **REQUIRES VINH'S APPROVAL** for architecture decision.

---

### F-005: Mock Data Honesty - MOCK Labels Present (INFO)

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **Status** | VERIFIED |
| **Evidence** | Code inspection |
| **Impact** | Positive - users are informed data is mock |
| **Affected Files** | `src/routes/customer.tsx`, `src/routes/technician.tsx`, `src/routes/index.tsx` |

**Description:**
The application correctly displays MOCK labels in multiple locations:

**Customer App:**
- Line 178: `DEMO · Đang hoạt động (MOCK)`
- Line 183: `TRẠNG THÁI KẾT NỐI (DEMO)`
- Line 184: `Đã kết nối` + `Dữ liệu mẫu (MOCK)`
- Line 280: `Đường truyền ổn định (DEMO)`
- Line 281: `ONT và Wi-Fi đang hoạt động (MOCK)`
- Line 295: `Internet` + `Đang hoạt động (MOCK)`
- Line 297: `Wi-Fi` + `Đang hoạt động (MOCK)`

**Technician App:** Status and activity labels include MOCK indicators.

**Dashboard:** MOCK labels present in status displays.

**Status:** ✅ COMPLIANT with mock data honesty requirement.

---

### F-006: Hardcoded Ticket Assignment (MEDIUM)

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Status** | CONFIRMED |
| **Evidence** | Code inspection |
| **Impact** | Tickets can be assigned to wrong technicians |
| **Affected Files** | `src/routes/index.tsx:1119-1122` |

**Description:**
```typescript
// index.tsx lines 1119-1122
technicianId: technicians[0]?.id ?? "KT-001",
`Đã phân công ${t.id} cho ${technicians[0]?.name ?? "Kỹ thuật viên"}`
```

When assigning tickets from the dashboard, it always assigns to `KT-001` (the first technician) regardless of which technician should handle it.

**Risk:** Incorrect ticket routing; no way to assign to specific technicians.

**Recommendation:** Add technician selection dropdown or implement intelligent assignment logic. **Can be fixed without architecture approval** (frontend-only change).

---

## Access Control Matrix

| User Type | App | Identity | Can Access | Cannot Access (Expected) | Vulnerability |
|-----------|-----|----------|------------|--------------------------|--------------|
| Customer | /customer | Hardcoded KH-001 | All tickets via deep link | Other customers' tickets | ✅ F-002 |
| Technician | /technician | Hardcoded KT-001 | All tickets | Tickets not assigned to them | ❌ Not implemented |
| Admin/Dashboard | / | All data (no identity) | All ONTs, all tickets | None | ❌ Not implemented |

**Current State:** No access control exists. All apps can access all data.

---

## Deep Link Security Analysis

### Current Deep Link Patterns
- `/?ont=ONT-001` - View ONT details
- `/?ticket=TK-2401` - View ticket details
- `/?ont=ONT-001&tab=LAN` - View ONT with specific tab
- `/technician?ticket=TK-2401` - Technician view of ticket
- `/customer?ticket=TK-2401` - Customer view of ticket

### Validation Flow
1. URL search params parsed by `parseDeepLink()`
2. Values sanitized (uppercase, trim, max 32 chars)
3. NO existence check
4. NO ownership check
5. NO permission check

### Attack Vectors
1. **Direct Object Reference:** `/customer?ticket=TK-2401` (TK-2401 belongs to KH-002, but KH-001 can access it)
2. **Invalid IDs:** `/customer?ticket=TK-9999` (Shows "not found" but doesn't distinguish between "doesn't exist" and "not yours")
3. **Injection:** `/customer?ticket=<script>alert(1)</script>` (Sanitized by uppercase conversion, but still risky)

---

## Recommendations Summary

### Immediate (Can implement without approval)
1. **F-006:** Fix hardcoded technician assignment to allow selection
2. **Enhance deep link validation:** Add existence checks for ONT and ticket IDs

### Requires Vinh's Approval
1. **F-001, F-004:** Implement authentication mechanism (JWT/OAuth2)
2. **F-002, F-003:** Implement proper access control and authorization
3. **Backend integration:** Connect to real authentication backend

### Architecture Decisions Needed
1. **Authentication method:** JWT vs OAuth2 vs Session-based
2. **Backend API:** REST vs GraphQL vs other
3. **Database:** For storing user accounts and permissions
4. **ONT adapter:** For real ONT data access

---

## Evidence Commands

```bash
# Verify hardcoded identities
grep -n "customers\[0\]" work/98/ONT-CARE/04_CODE/ont-platform/src/routes/*.tsx
grep -n "technicians\[0\]" work/98/ONT-CARE/04_CODE/ont-platform/src/routes/*.tsx

# Verify deep link parsing
cat work/98/ONT-CARE/04_CODE/ont-platform/src/lib/deep-links.ts

# Verify E2E test expectations
cat work/98/ONT-CARE/05_TEST/e2e/deep_links_e2e.py | grep -A2 "other customer"
```

---

## Status

| Finding | Severity | Status | Action Required |
|---------|----------|--------|-----------------|
| F-001 | CRITICAL | CONFIRMED | Await Vinh's approval |
| F-002 | CRITICAL | CONFIRMED | Await Vinh's approval |
| F-003 | HIGH | CONFIRMED | Await Vinh's approval |
| F-004 | HIGH | CONFIRMED | Await Vinh's approval |
| F-005 | INFO | VERIFIED | ✅ Compliant |
| F-006 | MEDIUM | CONFIRMED | Can fix without approval |

**Overall Security Status:** 🔴 **CRITICAL** - Not suitable for production without major security improvements.

**Prototype Status:** ✅ Acceptable for demonstration purposes with MOCK labels clearly displayed.

---

*This document is part of Work 98 evidence. Do not implement security fixes without explicit approval from Vinh.*
