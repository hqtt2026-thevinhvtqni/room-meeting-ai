# Work 29 — Architecture Baseline

## 1. End-to-end flow
User brief -> Project Planner -> Storyboard/Shot List -> Asset Registry -> Provider Router -> Shot Generation Jobs -> Voice/Audio -> Render/Compose -> Quality Gate -> Review/Approval -> Export + Evidence.

## 2. Components
- **Project API / orchestration:** validates briefs, owns lifecycle and job state.
- **Planner:** turns brief into typed project spec and shot list; deterministic schema validation.
- **Asset Registry:** versioned references to character sheets, brand assets, product images, voice settings, and rights/consent metadata.
- **Provider Router:** selects a capability-compatible adapter based on availability, cost ceiling, duration, ratio, and quality requirements.
- **Video Adapter:** text-to-video, image-to-video, reference/character control when supported.
- **Voice Adapter:** text-to-speech or provider-native audio.
- **Renderer:** FFmpeg-based composition for clips, narration, music, captions, logo, transitions, and output formats.
- **Quality Gate:** technical validation plus checklist for visual/brand/legal review.
- **Evidence Store:** project manifest, provider task IDs, sanitized logs, timings, cost estimate/actual, output checksums, test reports.

## 3. ROOM-HOP boundary
AI agent -> MCP :8020 -> Core :8000 (single source of truth) -> Workspace :8010. Dashboard :3000 is render-only. The Sandbox is the build zone, not canonical runtime. The video system must not write to Core storage or provider credentials directly. Any eventual MCP tools must call a Core application service through the existing authorized boundary.

## 4. Suggested MCP capability groups
- project_create
- project_get
- project_plan
- asset_register
- generation_submit
- generation_status
- render_submit
- quality_check
- artifact_list
- cost_estimate
All inputs must be schema-validated. Long-running jobs return job IDs and explicit states; do not hold a request open while a provider renders.

## 5. Job lifecycle
DRAFT -> PLANNED -> GENERATING -> RENDERING -> QC_PENDING -> READY_FOR_REVIEW -> APPROVED -> EXPORTED.
Failure states: BLOCKED, FAILED, CANCELED. Retry only transient failures, with bounded attempts and idempotency keys. A blocked job must preserve evidence and explain the missing dependency.

## 6. Provider adapter contract
Each adapter declares capabilities and constraints, validates inputs, submits a task, polls/receives status, normalizes output references, reports provider task IDs, and emits sanitized errors. Secrets are injected from environment/secret store and never serialized into project manifests.

## 7. Cost and safety controls
- Default tests use mock providers; no credits consumed.
- Require explicit project-level opt-in before real generation.
- Set max shots, max duration, resolution, and spend ceiling.
- Estimate before submission and stop if ceiling would be exceeded.
- Record source/consent metadata for real people, voices, logos, and copyrighted assets.
- Require human approval before publication or customer-facing use.

## 8. MVP sequence
A. Contract and project manifest.
B. Mock provider + deterministic planner.
C. Render pipeline and technical QC.
D. Automated tests and one self-contained E2E using generated fixtures.
E. Optional provider adapter (Runway first candidate) behind explicit configuration.
F. ROOM-HOP Core/MCP integration only after contracts and local E2E pass.

## 9. Provider research
Runway documents official MCP integration at https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP and developer APIs at https://docs.dev.runwayml.com/. Video generation consumes provider credits; verify current model availability, terms, pricing, and account access before enabling. Kling is a possible alternate provider via its developer API.
