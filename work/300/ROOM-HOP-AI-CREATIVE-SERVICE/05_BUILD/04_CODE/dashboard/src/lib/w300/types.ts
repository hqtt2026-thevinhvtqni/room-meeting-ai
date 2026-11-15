export type Role = "guest" | "customer" | "internal";
export type WorkStatus = "PLANNED" | "IN_PROGRESS" | "BLOCKED" | "DONE";
export type Priority = "P0" | "P1" | "P2" | "P3";
export type JobStatus = "QUEUED" | "RUNNING" | "NEEDS_REVIEW" | "COMPLETED" | "FAILED" | "CANCELLED";
export type JobType = "IMAGE_GEN" | "IMAGE_EDIT" | "VIDEO_GEN" | "IMAGE_TO_VIDEO" | "STORYBOARD";
export type ReviewStatus = "NOT_REQUESTED" | "IN_REVIEW" | "APPROVE" | "CONDITIONAL" | "REJECT";
export type IntegrationState = "NOT_CONNECTED" | "UNVERIFIED" | "CONNECTED" | "ERROR";
export type JournalResult = "PASS" | "FAIL" | "BLOCKED";
export type GateStatus = "PENDING" | "IN_REVIEW" | "PASSED" | "FAILED";

export interface WorkPackage { id: string; title: string; owner: string; status: WorkStatus; priority: Priority; due: string; evidence?: string; nextStep: string; isDemo: true }
export interface Gate { id: string; name: string; description: string; status: GateStatus; isDemo: true }
export interface Review { reviewer: "Xu" | "Ka" | "Cla" | "Kha" | "Go" | "QE"; scope: string; status: ReviewStatus; note?: string; updatedAt?: string }
export interface Decision { id: string; date: string; title: string; outcome: string; by: string }
export interface Risk { id: string; title: string; severity: "P0" | "P1"; owner: string; mitigation: string }
export interface Job {
  id: string; ref: string; projectId: string; type: JobType; title: string; prompt: string;
  status: JobStatus; progress: number; createdAt: string; updatedAt: string;
  providerStatus: IntegrationState; durationSec?: number; retries: number;
  costEstimate?: number; costActual?: number; costSource?: string;
  etaConfirmed: boolean; error?: string; format: string; quantity: number; intendedUse: string;
  isDemo: boolean;
}
export interface Project { id: string; name: string; createdAt: string; isDemo: boolean }
export interface Asset { id: string; jobId: string; kind: "image" | "video"; label: string; url?: string; thumbnail?: string; isDemo: boolean }
export interface Integration { id: string; name: string; kind: string; state: IntegrationState; envVar: string; lastChecked?: string; evidence?: string; note: string }
export interface JournalEntry { id: string; ts: string; actor: string; scope: string; action: string; evidence?: string; result: JournalResult; nextStep: string }

export const JOB_TYPE_LABEL: Record<JobType, { vi: string; en: string; kind: "image" | "video" }> = {
  IMAGE_GEN: { vi: "Tạo ảnh", en: "Image generation", kind: "image" },
  IMAGE_EDIT: { vi: "Chỉnh sửa / ghép ảnh", en: "Image edit & compositing", kind: "image" },
  VIDEO_GEN: { vi: "Tạo video", en: "Video generation", kind: "video" },
  IMAGE_TO_VIDEO: { vi: "Ảnh thành video", en: "Image-to-video", kind: "video" },
  STORYBOARD: { vi: "Storyboard", en: "Storyboard", kind: "image" },
};