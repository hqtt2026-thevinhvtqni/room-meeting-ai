# WORK 98 — SOURCE AUDIT UPDATE
- TÊN: Xu
- CHỨC DANH: Technical Lead / E2E Owner
- NGÀY: 2026-10-13
- GIỜ-PHÚT: 16:27 UTC+7
- PHẠM VI: static read-only audit via MCP + one targeted DASH label fix
- RUNTIME: NOT RUN

## Evidence-based findings

### P0 — data provenance / authorization
1. `ont-platform/src/lib/ont-data.ts` generates customers, ONTs, technicians, LAN devices and tickets using `Array.from` and synthetic IDs/values. Treat as MOCK fixtures, not ONT telemetry.
2. `ont-platform/src/components/platform-context.tsx` keeps tickets/customers/ONTs in React state and updates them in memory. No persistent store was found in the inspected provider; reload durability is not established.
3. `ont-platform/src/routes/customer.tsx` binds the customer view to `customers[0]` (`you`) instead of an authenticated identity. This is a prototype, not production access control.
4. `ont-platform/src/routes/technician.tsx` binds technician identity to `technicians[0]`. The inspected routes do not demonstrate server-side authorization. Hiding links or validating deep links is not enough to secure ticket/ONT data.
5. `ont-platform/src/lib/deep-links.ts` normalizes IDs and bounds strings, but this is input validation, not authentication/authorization.

### P1 — canonical root / build workflow
6. Root `package.json` identifies a scaffold and has no scripts/dependencies. The actual application manifest is `ont-platform/package.json`.
7. `ont-platform/.github/workflows/e2e.yml` runs `bun install` and `bun run dev` without an explicit `working-directory: ont-platform`. If the workflow runs from the repository root as currently laid out, the commands likely target the root scaffold rather than the app. This is a static risk, not a confirmed CI failure; verify after repository root/CI path is decided.
8. E2E test `ont-platform/e2e/deep_links_e2e.py` expects server at port 8080 and exercises valid/invalid links and customer ticket isolation. Test existence is not test PASS; the suite has not run in this session.
9. The existing root `preview/` was a file-tree snapshot, not an app build preview. It has now been replaced with a product-oriented preview and explicit MOCK/BLOCKED state.

### P1 — UI honesty
10. Fixed the DASH topbar status in `ont-platform/src/routes/index.tsx` from “Hệ thống hoạt động” to “DEMO · DỮ LIỆU MẪU (MOCK)”. MCP write returned ok and read-back confirmed the replacement. Build/browser rendering has not been verified.

## Changes this session
- `preview/index.html`: product preview shell with navigation for DASH, APP Khách, APP Kỹ thuật, E2E Journey, BUILD & EVIDENCE.
- `preview/preview.config.json`: preview sections and explicit build BLOCKED state.
- `preview/data.json`: deterministic demo fixtures and explicit MOCK/NOT RUN metadata.
- `preview/product-render.js`: renderers for product-oriented views and honest test/build status.
- `ont-platform/src/routes/index.tsx`: dashboard topbar label corrected to MOCK.
- `XU_EXECUTION_MANDATE_20261013.md` and `NEXT_ACTIONS_AI_WORK98_20261013.md`: execution mandate and ordered worklist.

## Verification status
- DONE: MCP write + read-back for the files listed above.
- NOT RUN: TypeScript compile, Vite build, ESLint, browser rendering, Playwright E2E.
- BLOCKED: no tool in the available MCP tool contract was found that executes shell/build commands inside Work 98 Sandbox.
- NOT CONNECTED: no real ONT session/device was tested.
- NOT CREATED/IDENTIFIED: GitHub repository.
