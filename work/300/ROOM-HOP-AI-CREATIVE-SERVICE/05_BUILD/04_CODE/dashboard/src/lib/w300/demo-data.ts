/** DỮ LIỆU MINH HỌA / DEMO DATA — not real ROOM-HOP data. Keep separate from live adapters. */
import perfume from "@/assets/demo-perfume.svg";
import city from "@/assets/demo-city.svg";
import abstractImg from "@/assets/demo-abstract.svg";
import type { Asset, Decision, Gate, Integration, Job, JournalEntry, Project, Review, Risk, WorkPackage } from "./types";

export const DEMO_PHASE = { name: "Phase 1 — Product shell & contracts", status: "IN_PROGRESS", percent: 32 };

export const demoWorkPackages: WorkPackage[] = [
  { id: "WP-01", title: "UI shell & design system", owner: "Cla", status: "IN_PROGRESS", priority: "P1", due: "2026-11-22", nextStep: "Hoàn thiện portal khách hàng", isDemo: true },
  { id: "WP-02", title: "MCP gateway contract (tools schema)", owner: "Xu", status: "PLANNED", priority: "P0", due: "2026-11-29", nextStep: "Draft OpenAPI/MCP tool spec", isDemo: true },
  { id: "WP-03", title: "Image provider evaluation", owner: "Ka", status: "BLOCKED", priority: "P0", due: "2026-11-25", nextStep: "Chờ quyết định license/provider", isDemo: true },
  { id: "WP-04", title: "Storage & delivery design", owner: "Kha", status: "PLANNED", priority: "P1", due: "2026-12-06", nextStep: "Signed URL policy", isDemo: true },
  { id: "WP-05", title: "Auth model (customer vs internal)", owner: "Go", status: "IN_PROGRESS", priority: "P0", due: "2026-11-27", nextStep: "Review role boundary", isDemo: true },
  { id: "WP-06", title: "QA test plan G0–G8", owner: "QE", status: "DONE", priority: "P2", due: "2026-11-12", evidence: "docs/qa-plan (demo)", nextStep: "—", isDemo: true },
  { id: "WP-07", title: "Billing/quota placeholder", owner: "Kha", status: "PLANNED", priority: "P3", due: "2026-12-20", nextStep: "Không triển khai thanh toán thật", isDemo: true },
];

const gateRows: Array<[string, string, Gate["status"]]> = [
  ["G0", "Scope locked", "PASSED"], ["G1", "Architecture draft", "IN_REVIEW"], ["G2", "Security & auth model", "PENDING"],
  ["G3", "MCP contract", "PENDING"], ["G4", "Provider integration", "PENDING"], ["G5", "Storage & delivery", "PENDING"],
  ["G6", "QA end-to-end", "PENDING"], ["G7", "Billing readiness", "PENDING"], ["G8", "Public launch", "PENDING"],
];
export const demoGates: Gate[] = gateRows.map(([id, name, status]) => ({ id, name, description: name, status, isDemo: true }));

export const demoReviews: Review[] = [
  { reviewer: "Xu", scope: "Architecture", status: "CONDITIONAL", note: "Cần tách adapter live/demo", updatedAt: "2026-11-13" },
  { reviewer: "Ka", scope: "Providers", status: "IN_REVIEW", updatedAt: "2026-11-14" },
  { reviewer: "Cla", scope: "UX/UI", status: "APPROVE", updatedAt: "2026-11-14" },
  { reviewer: "Kha", scope: "Data & storage", status: "NOT_REQUESTED" },
  { reviewer: "Go", scope: "Security", status: "IN_REVIEW", updatedAt: "2026-11-12" },
  { reviewer: "QE", scope: "Quality", status: "NOT_REQUESTED" },
];

export const demoDecisions: Decision[] = [
  { id: "D-001", date: "2026-11-10", title: "UI shell trước, backend sau", outcome: "Approved", by: "Xu" },
  { id: "D-002", date: "2026-11-12", title: "Không gọi MCP endpoint chưa xác minh", outcome: "Approved", by: "Go" },
  { id: "D-003", date: "2026-11-14", title: "Chọn provider ảnh", outcome: "Deferred", by: "Ka" },
];

export const demoRisks: Risk[] = [
  { id: "R-01", title: "Chưa có hợp đồng MCP gateway", severity: "P0", owner: "Xu", mitigation: "Ưu tiên WP-02" },
  { id: "R-02", title: "Quyền sử dụng tài liệu khách tải lên", severity: "P0", owner: "Go", mitigation: "Bắt buộc xác nhận quyền + ToS" },
  { id: "R-03", title: "Chi phí video provider chưa xác định", severity: "P1", owner: "Kha", mitigation: "Chỉ hiển thị chi phí khi có nguồn" },
];

const t = (d: string) => `2026-11-${d}`;
export const demoProjects: Project[] = [
  { id: "demo-p1", name: "Chiến dịch nước hoa Tết", createdAt: t("08T09:00:00Z"), isDemo: true },
  { id: "demo-p2", name: "Teaser đô thị đêm", createdAt: t("10T14:00:00Z"), isDemo: true },
  { id: "demo-p-new", name: "Yêu cầu mới (demo)", createdAt: t("15T00:00:00Z"), isDemo: true },
];

export const demoJobs: Job[] = [
  { id: "dj1", ref: "W300-DEMO-00101", projectId: "demo-p1", type: "IMAGE_GEN", title: "Key visual nước hoa", prompt: "Perfume bottle, navy, violet rim light", status: "COMPLETED", progress: 100, createdAt: t("08T09:10:00Z"), updatedAt: t("08T09:14:00Z"), providerStatus: "NOT_CONNECTED", durationSec: 240, retries: 0, etaConfirmed: false, format: "4:3", quantity: 4, intendedUse: "Social ads", isDemo: true },
  { id: "dj2", ref: "W300-DEMO-00102", projectId: "demo-p1", type: "IMAGE_EDIT", title: "Ghép logo lên nền", prompt: "Composite logo on abstract glass", status: "NEEDS_REVIEW", progress: 90, createdAt: t("09T10:00:00Z"), updatedAt: t("09T10:30:00Z"), providerStatus: "NOT_CONNECTED", durationSec: 1800, retries: 1, etaConfirmed: false, format: "1:1", quantity: 2, intendedUse: "Website", isDemo: true },
  { id: "dj3", ref: "W300-DEMO-00103", projectId: "demo-p2", type: "IMAGE_TO_VIDEO", title: "Mưa Sài Gòn 8s", prompt: "Animate rainy neon street", status: "RUNNING", progress: 45, createdAt: t("14T08:00:00Z"), updatedAt: t("14T08:05:00Z"), providerStatus: "NOT_CONNECTED", retries: 0, etaConfirmed: false, format: "16:9", quantity: 8, intendedUse: "Teaser", isDemo: true },
  { id: "dj4", ref: "W300-DEMO-00104", projectId: "demo-p2", type: "VIDEO_GEN", title: "Intro logo", prompt: "Liquid glass logo reveal", status: "FAILED", progress: 20, createdAt: t("13T11:00:00Z"), updatedAt: t("13T11:02:00Z"), providerStatus: "NOT_CONNECTED", retries: 2, etaConfirmed: false, error: "Provider chưa kết nối (demo)", format: "9:16", quantity: 6, intendedUse: "Reels", isDemo: true },
  { id: "dj5", ref: "W300-DEMO-00105", projectId: "demo-p2", type: "STORYBOARD", title: "Storyboard 6 khung", prompt: "Night city story, 6 frames", status: "QUEUED", progress: 0, createdAt: t("15T01:00:00Z"), updatedAt: t("15T01:00:00Z"), providerStatus: "NOT_CONNECTED", retries: 0, etaConfirmed: false, format: "16:9", quantity: 6, intendedUse: "Pitch", isDemo: true },
];

export const demoAssets: Asset[] = [
  { id: "da1", jobId: "dj1", kind: "image", label: "Key visual #1", thumbnail: perfume, isDemo: true },
  { id: "da2", jobId: "dj2", kind: "image", label: "Composite draft", thumbnail: abstractImg, isDemo: true },
  { id: "da3", jobId: "dj3", kind: "video", label: "Frame tham chiếu", thumbnail: city, isDemo: true },
];

export const defaultIntegrations: Integration[] = [
  { id: "mcp", name: "MCP Gateway", kind: "Gateway", state: "NOT_CONNECTED", envVar: "VITE_W300_GATEWAY_URL", note: "Endpoint chưa cấu hình / chưa xác minh" },
  { id: "img", name: "Image provider", kind: "AI", state: "NOT_CONNECTED", envVar: "W300_IMAGE_PROVIDER_KEY", note: "Chưa chọn provider" },
  { id: "vid", name: "Video provider", kind: "AI", state: "NOT_CONNECTED", envVar: "W300_VIDEO_PROVIDER_KEY", note: "Chưa chọn provider" },
  { id: "sto", name: "Storage", kind: "Infra", state: "NOT_CONNECTED", envVar: "W300_STORAGE_BUCKET", note: "Chưa có signed URL" },
  { id: "que", name: "Job queue", kind: "Infra", state: "NOT_CONNECTED", envVar: "W300_QUEUE_URL", note: "Chưa có worker" },
  { id: "bil", name: "Billing", kind: "Payments", state: "NOT_CONNECTED", envVar: "W300_BILLING_KEY", note: "Không xử lý thanh toán" },
];

export const demoJournal: JournalEntry[] = [
  { id: "J1", ts: "2026-11-15T02:10:00Z", actor: "Cla", scope: "WP-01", action: "UI review (manual)", evidence: "screenshot (demo)", result: "PASS", nextStep: "Portal flows" },
  { id: "J2", ts: "2026-11-14T16:00:00Z", actor: "Ka", scope: "WP-03", action: "Provider trial (paper)", result: "BLOCKED", nextStep: "Chờ license" },
  { id: "J3", ts: "2026-11-14T09:30:00Z", actor: "Go", scope: "G2", action: "Threat model draft", result: "PASS", nextStep: "Review với Xu" },
  { id: "J4", ts: "2026-11-13T11:00:00Z", actor: "QE", scope: "MCP", action: "Ping gateway", evidence: "no endpoint", result: "FAIL", nextStep: "Cấu hình endpoint" },
];