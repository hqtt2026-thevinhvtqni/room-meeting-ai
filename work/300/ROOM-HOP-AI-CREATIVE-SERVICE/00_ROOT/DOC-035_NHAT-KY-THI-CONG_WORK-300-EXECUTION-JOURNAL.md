# DOC-035 — NHẬT KÝ THI CÔNG / W300 EXECUTION JOURNAL

## 2026-11-15 — Entry 001 — Xu / AI-01 — Discovery and Git preflight
- Scope: W300 Lovable prototype, existing ROOM-HOP GitHub repository and branch main.
- Method: inspected Lovable project metadata/files and GitHub repository metadata/current main ref.
- Evidence: Lovable project ID 8cadd295-5da9-4325-89db-fc0355d2d3a3; Lovable latest commit 036a25ba6ece55df5e84c93d8422bbe7675f7ad1; preview https://id-preview--8cadd295-5da9-4325-89db-fc0355d2d3a3.lovable.app. GitHub repo exists, default branch main, push permission true; preflight main HEAD 355311f787a06b10be64f6df394aae06cf1e7d91.
- Findings: Lovable agent reported unresolved TypeScript/build errors and tests/browser checks NOT RUN. Workspace has no remaining Lovable credits, so another build/fix turn could not be started.
- Status: PASS — repository/project discovery only. Product build/test status remains NOT VERIFIED.
- Next: place the isolated UI source snapshot and W300 canonical work records in the Work folder; do not overwrite repository root.

## 2026-11-15 — Entry 002 — Xu / AI-01 — Git source synchronization
- Scope: copy the existing Lovable UI prototype into W300's isolated GitHub main directory and create canonical Work records.
- Method: GitHub Git Database API via connected GitHub tools; create blobs/tree/commit and move main with expected-SHA protection. Exact readback is required after commit.
- Source: Lovable project 8cadd295-5da9-4325-89db-fc0355d2d3a3, initial UI snapshot commit 036a25ba6ece55df5e84c93d8422bbe7675f7ad1.
- Status: PASS — GitHub main commit created; sampled exact readback passed. Full build/test verification remains NOT RUN.
- Restrictions: no production provider/backend/MCP/payment integration; no publish/deploy; no fake PASS.


## 2026-11-15 — Entry 002 — Xu / AI-01 — GitHub main synchronization and exact readback
- Scope: W300 canonical Work records and isolated dashboard source snapshot.
- Method: created a Git tree based on preflight main tree; created commit and advanced main using expected-SHA protection (force=false, expected_sha=355311f787a06b10be64f6df394aae06cf1e7d91).
- GitHub commit: 3a3f8ec43b85c67553e11dca92ee150aa231e697 — feat(w300): import isolated creative studio UI prototype and work records.
- Exact readback: Source synchronization commit: 3a3f8ec43b85c67553e11dca92ee150aa231e697. A follow-up README path correction was committed as f54a6954963e965caec8aa0e667b4ee6a4122b13. Before this journal amendment, main ref readback returned f54a6954963e965caec8aa0e667b4ee6a4122b13. Read back DOC-001, DOC-035, dashboard package.json, demo-data.ts and adapter.ts successfully. Confirmed package name, isolated paths, SVG demo assets, and patched Gate tuple typing are present.
- Scope of synchronization: UI prototype source and Work documentation only. Original binary JPG assets were not copied; replaced with three SVG demo placeholders. Lovable native bidirectional GitHub connection has NOT been configured. This is a source snapshot commit into ROOM-HOP main.
- Verification: exact file fetch PASS for 5/5 sampled canonical/source files; Git ref readback PASS. Full tree audit, install, typecheck, unit tests, production build and browser E2E NOT RUN.
- Build issues: original Lovable agent had reported build/type errors. A local source patch was applied to demo gate tuple typing and Vite env typing; these fixes are NOT build-verified.
- Status: PASS — GitHub write and sampled exact readback. BLOCKED/NOT RUN — build/test/runtime verification because Lovable workspace is out of credits and no local execution has yet been performed.
- Next: correct relative README links; inspect all files and import paths; run npm install, tests, typecheck, lint and build in a controlled runtime; then record each result here. Native Lovable GitHub sync requires linking the project in Lovable's GitHub settings, which cannot safely target this nested Work subdirectory.


## 2026-11-15 — Entry 003 — Xu / AI-01 — Final Git ref and directory verification
- Scope: W300 GitHub main synchronization verification after the README correction.
- Method: fetched GitHub main ref; fetched Work 00_ROOT and dashboard directory listings; exact-fetched canonical journal and representative app source files.
- Evidence: immediately before this journal amendment, main ref = f54a6954963e965caec8aa0e667b4ee6a4122b13; W300 00_ROOT contains DOC-001, DOC-002, DOC-003, DOC-034 and DOC-035; dashboard root contains .gitignore, .lovable, formatting/config files, AGENTS.md, README.md, bun.lock, package.json, public/, src/, tsconfig.json, vite.config.ts and vitest.config.ts.
- Exact readback: DOC-001, DOC-035, package.json, demo-data.ts and adapter.ts fetched successfully; demo-data imports SVG placeholders and uses an explicit Gate tuple type. Git ref and directory listings returned expected W300 paths.
- Status: PASS — GitHub main write and structural/readback verification. NOT RUN — npm/bun install, typecheck, lint, unit tests, production build and browser E2E. No deployment or public release.
- Next: use a controlled local/CI runtime to run the test/build suite and fix any remaining errors. Native Lovable bidirectional GitHub connection remains unconfigured; source of truth for this Work is the nested W300 directory on ROOM-HOP main.
