# Work 29 — Acceptance Criteria

## Design gate
- [x] Typed project and shot schemas documented. (`src/video_studio/models.py`)
- [x] Provider adapter contract documented. (`src/video_studio/provider.py`)
- [x] Core/MCP/Workspace boundary documented. (`ARCHITECTURE.md`)
- [x] Job lifecycle, retries, idempotency, and cost limits documented.
- [x] No credentials or real paid provider calls in unit tests.

## MVP runtime gate
- [x] Unit tests cover valid/invalid briefs, lifecycle, provider errors, cost ceiling.
- [x] Mock provider generates deterministic fixture assets.
- [x] Renderer creates a playable MP4 from fixtures (FFmpeg).
- [x] FFprobe confirms duration/streams in QC.
- [x] QC failure produces BLOCKED/FAILED with evidence, not false PASS.
- [x] Offline E2E: brief → plan → mock → render → QC → READY_FOR_REVIEW.
- [x] Evidence records commands/results/checksums via validation entrypoint.
- [x] Provider integration disabled unless explicitly configured (mock refuses paid).
- [ ] Real-provider opt-in with consent + spend ceiling — **NOT RUN** (no credentials).

## Integration gate
- [ ] Core application service owns project state — **BLOCKED** (no Core :8000).
- [ ] MCP tools call Core services — **BLOCKED**.
- [ ] Workspace artifacts path — Sandbox path used for offline only.
- [ ] Dashboard server-backed state — **NOT RUN**.
- [ ] Human approval before public posting — policy documented, not productized.
- [ ] Real-provider test with consent — **NOT RUN**.

## Governance
**Status:** OFFLINE_VALIDATION_PASS · INTEGRATION_BLOCKED · **NOT COMPLETED/LOCKED** · **NO_RELEASE**
Do not set COMPLETED/LOCKED until integration + real-provider gates have evidence.
