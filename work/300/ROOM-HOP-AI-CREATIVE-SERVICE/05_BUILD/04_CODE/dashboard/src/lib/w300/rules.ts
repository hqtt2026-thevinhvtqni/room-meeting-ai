import type { Job, JobType, Role } from "./types";

/** Only internal ROOM-HOP role may see /ops. */
export function canAccessOps(role: Role): boolean { return role === "internal"; }
export function canAccessPortal(role: Role): boolean { return role === "customer" || role === "internal"; }

/** Download only when a real asset URL exists and it is not demo. */
export function canDownload(asset: { url?: string; isDemo: boolean }): boolean {
  return !!asset.url && !asset.isDemo;
}

export interface DemoRequestInput { type: JobType; title: string; prompt: string; format: string; quantity: number; intendedUse: string; rightsConfirmed: boolean; hasReference: boolean }

export function validateRequest(i: DemoRequestInput): string | null {
  if (i.prompt.trim().length < 10) return "Mô tả (prompt) cần ít nhất 10 ký tự.";
  if (i.hasReference && !i.rightsConfirmed) return "Bạn cần xác nhận quyền sử dụng tài liệu tải lên.";
  if (!i.rightsConfirmed) return "Bạn cần xác nhận điều khoản sử dụng.";
  if (i.quantity < 1) return "Số lượng / thời lượng không hợp lệ.";
  return null;
}

/** Creates a DEMO job only — never calls a provider. */
export function createDemoJob(i: DemoRequestInput, now = new Date()): Job {
  const n = Math.floor(now.getTime() / 1000) % 100000;
  const iso = now.toISOString();
  return {
    id: `demo-${now.getTime()}`, ref: `W300-DEMO-${String(n).padStart(5, "0")}`, projectId: "demo-p-new",
    type: i.type, title: i.title || "Yêu cầu mới", prompt: i.prompt, status: "QUEUED", progress: 0,
    createdAt: iso, updatedAt: iso, providerStatus: "NOT_CONNECTED", retries: 0, etaConfirmed: false,
    format: i.format, quantity: i.quantity, intendedUse: i.intendedUse, isDemo: true,
  };
}