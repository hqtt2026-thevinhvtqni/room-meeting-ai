/**
 * Live service boundary for ROOM-HOP / W300 MCP gateway.
 * NOT CONNECTED: no endpoint is called until VITE_W300_GATEWAY_URL is configured AND
 * a verified backend contract exists. Credentials must never be placed in browser code;
 * authenticated calls must go through a server function holding secrets.
 */
import type { Integration, Job } from "./types";

export interface W300Service {
  readonly connected: boolean;
  listJobs(): Promise<Job[]>;
  submitJob(input: unknown): Promise<Job>;
  checkIntegrations(): Promise<Integration[]>;
}

export class NotConnectedError extends Error {
  constructor() { super("W300 backend/MCP chưa kết nối (not connected)"); this.name = "NotConnectedError"; }
}

export function gatewayUrl(): string | undefined {
  const v = import.meta.env?.VITE_W300_GATEWAY_URL;
  return v && v.length > 0 ? v : undefined;
}

/** Disconnected adapter: every live call rejects safely. */
export const liveService: W300Service = {
  connected: false,
  async listJobs() { throw new NotConnectedError(); },
  async submitJob() { throw new NotConnectedError(); },
  async checkIntegrations() { throw new NotConnectedError(); },
};