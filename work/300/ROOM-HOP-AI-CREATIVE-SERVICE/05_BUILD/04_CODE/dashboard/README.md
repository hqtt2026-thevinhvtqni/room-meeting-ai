# W300 — ROOM-HOP Creative Studio

Isolated frontend prototype for W300, stored inside the ROOM-HOP monorepo.

## Status

- UI prototype imported from Lovable project 8cadd295-5da9-4325-89db-fc0355d2d3a3.
- Demo-only data and request simulation. No real AI generation is executed.
- Public MCP gateway, auth, tenant persistence, providers, storage, queue, billing and deployment are NOT CONNECTED / NOT VERIFIED.
- The original Lovable build agent reported TypeScript/build issues; Git source snapshot has not yet passed local build, tests or browser verification.

## Run locally

Requires Node.js 20+ and npm.

```sh
npm install
npm run dev
npm test
npm run build
```

Run commands from this directory. Do not run production deployment before Work approval.

## Routes

- / — landing
- /signin — demo role selection
- /ops — internal progress dashboard (demo data)
- /app — customer portal (demo only)
- /docs — planned MCP tool documentation

## Demo/live boundary

- Submitting a request creates a DEMO job in client-side state only.
- Demo thumbnails are illustrative SVGs and are not customer deliverables.
- Live adapter deliberately rejects calls while the gateway is unconfigured.
- No credentials or provider keys belong in browser code or Git.

## Backend contract TODOs

See W300 canonical docs at ../../../00_ROOT and roadmap at ../../../04_PLAN. Backend work is gated by architecture and security review.

## Build & verify (W300 CI)

CI workflow: `.github/workflows/w300-dashboard-ci.yml` (Bun install → tsc --noEmit → ESLint → Vitest → production build). All current data remains demo-only; no provider, storage or billing is connected.

CI status: typecheck/lint/tests/build verified by w300-dashboard-ci run evidence (see DOC-035 Entry 009).
