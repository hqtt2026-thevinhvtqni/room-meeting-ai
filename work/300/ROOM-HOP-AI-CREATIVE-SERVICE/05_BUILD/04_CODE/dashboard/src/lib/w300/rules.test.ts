import { describe, expect, it } from "vitest";
import { canAccessOps, canDownload, createDemoJob, validateRequest } from "./rules";

const base = { type: "IMAGE_GEN" as const, title: "t", prompt: "a long enough prompt", format: "1:1", quantity: 1, intendedUse: "social", rightsConfirmed: true, hasReference: false };

describe("W300 rules", () => {
  it("customer cannot access /ops", () => { expect(canAccessOps("customer")).toBe(false); expect(canAccessOps("guest")).toBe(false); });
  it("internal can access /ops", () => expect(canAccessOps("internal")).toBe(true));
  it("demo assets are never downloadable", () => expect(canDownload({ url: "https://x/y.png", isDemo: true })).toBe(false));
  it("asset without url is not downloadable", () => expect(canDownload({ isDemo: false })).toBe(false));
  it("submitted request creates a QUEUED demo job with no confirmed ETA", () => {
    const j = createDemoJob(base);
    expect(j.isDemo).toBe(true); expect(j.status).toBe("QUEUED"); expect(j.etaConfirmed).toBe(false); expect(j.providerStatus).toBe("NOT_CONNECTED"); expect(j.ref.startsWith("W300-DEMO-")).toBe(true);
  });
  it("reference upload requires rights confirmation", () => expect(validateRequest({ ...base, hasReference: true, rightsConfirmed: false })).not.toBeNull());
});