# W10 — TECHNICAL ASSESSMENT: agent-desktop

- Record ID: W10-TECH-ASSESSMENT-AGENT-DESKTOP-20261123
- Date: 2026-11-23 (UTC+07:00)
- Status: DOCUMENTED — DESIGN CANDIDATE ONLY
- Scope: Evaluate agent-desktop as a possible native Desktop Adapter for Work 10.
- Decision authority: Vinh — Project Owner / Final Acceptance Authority.
- Prepared by: Xu — AI-01 / Architecture Coordination.

## 1. Executive conclusion

agent-desktop is technically relevant to W10 and is a candidate implementation engine for a future native Desktop Adapter. It is not a replacement for W10, the existing Playwright Browser Adapter, W14 Execution Host, W24 PC Source Bridge, W112 cross-Work contracts, or W113 shared Dashboard.

No installation, dependency addition, source-code change, runtime invocation, MCP registration, GitHub write, or release action was performed as part of this assessment.

## 2. Facts verified from the upstream project

Sources: official vercel-labs/agent-desktop GitHub repository and documentation, reviewed 2026-11-23.

- It is a CLI and C library for AI agents to inspect and operate desktop applications through native OS accessibility APIs.
- It returns structured JSON snapshots and element refs; the calling agent owns the observe → act → observe/verify loop. It does not contain an LLM.
- Platform APIs documented upstream: macOS AX API; Windows UI Automation (UIA); Linux AT-SPI.
- It can expose commands as MCP tools over stdio.
- It is for desktop applications, not browser-page automation; upstream directs browser automation users to agent-browser.
- A successful action does not itself prove the UI changed. The caller must take a fresh observation and verify the post-condition.
- Screenshots are a separate command; the normal semantic-ref workflow does not require pixel matching. This does not establish zero token use by an AI caller.
- Platform/session constraints exist. For example, Windows operates in the signed-in interactive desktop and has integrity/elevation limits; Linux requires a supported graphical session and AT-SPI bus; macOS requires Accessibility permission.

Primary references:
- https://github.com/vercel-labs/agent-desktop
- https://github.com/vercel-labs/agent-desktop/blob/main/README.md
- https://github.com/vercel-labs/agent-desktop/blob/main/docs/faq.md
- https://github.com/vercel-labs/agent-desktop/blob/main/docs/install.md
- https://github.com/vercel-labs/agent-desktop/blob/main/skills/agent-desktop/SKILL.md

## 3. Claims not accepted as proven

The following marketing/social claims are NOT accepted as W10 requirements or verified facts:
- “zero token” — the native tool avoids sending screenshots as the default observation representation, but the AI still consumes tokens to interpret JSON and decide actions.
- “100% accuracy” — refs reduce coordinate/pixel ambiguity, but UIA/AX/AT-SPI coverage, stale refs, application behavior, focus, permissions and platform limitations remain.
- “90% cost reduction” — no controlled benchmark, workload definition, model/token accounting or comparison evidence was supplied.
- “runs in background without taking the mouse” — must be measured per operation/platform; some input actions require an interactive/headed session and may affect focus or input state.
- “25,800+ stars” and a specific package version — not used as acceptance evidence; verify live upstream release metadata before any dependency decision.

## 4. W10 architecture disposition

Retain W10 as the single Computer Agent / Computer Provider boundary.

- Browser Adapter: existing Playwright/Chromium path remains the browser-page automation path.
- Desktop Adapter: proposed optional adapter for native desktop application automation; agent-desktop is a candidate backend, not yet selected or integrated.
- Agent Runtime: owns policy checks, action lifecycle, deadlines, observation, post-condition verification and evidence.
- ProcessSupervisor: owns worker/process containment for W10; an external desktop process must not bypass it or gain broader privileges.
- W10 API: remains loopback-only. No remote exposure and no direct Core authorization bypass.
- W24: owns PC Source Bridge, Core authorization and authenticated PC transport.
- W112: owns cross-Work integration contracts.
- W14: remains canonical autonomous E2E execution/delivery owner.
- W113: owns shared Dashboard ingress :3000. W10 standalone development/acceptance UI remains :3010.

## 5. Integration shape — proposed, not implemented

HQTT AI / caller
→ approved ROOM-HOP route and authorization boundary
→ W10 Agent API / Agent Runtime
→ adapter capability selection
   - Browser Adapter → Playwright / Chromium page
   - Desktop Adapter (future) → narrow W10 wrapper → agent-desktop CLI or library
→ fresh observation
→ post-condition verification
→ W10 evidence and journal

The calling AI must not receive unrestricted shell/desktop privileges. Do not expose an unrestricted agent-desktop MCP stdio server directly to remote agents. If MCP is used internally, it must be wrapped by W10 policy, identity, allow-list, process supervision and evidence handling.

Do not force native desktop operations into the existing LOCKED browser ACTION_CONTRACT. Any new desktop action vocabulary/capability contract requires a separate design review and explicit Owner approval before implementation.

## 6. Security, privacy and reliability requirements

- Default deny; explicit application/window/surface scope and action allow-list.
- No arbitrary shell, arbitrary command, unrestricted clipboard, notification dismissal, app launch/close, file access or system settings by default.
- Treat snapshots, clipboard, screenshots, traces and command output as sensitive desktop data; redact secrets and keep evidence local/private by default.
- Validate ref freshness and target identity; refresh snapshot after every state-changing action.
- Require explicit post-condition checks; action success alone is never task PASS.
- Destructive, financial, credential, security, permission and system-level actions require a separate approval gate.
- Respect OS permission and integrity boundaries; do not elevate privileges to make a test pass.
- Record command, adapter, app/window identity, action class, timestamps, result, observation digest and evidence location without leaking private content.
- Bound process time, output size, retries and cleanup; uncertain side effects or unconfirmed cleanup must fail closed.
- Accessibility tree absence or incomplete semantics must return UNSUPPORTED/BLOCKED; no silent coordinate fallback.

## 7. Evaluation plan

| ID | Test | Required evidence |
|---|---|---|
| AD-01 | Verify supported OS/session/permission and installed binary identity | status output, version, SHA-256, OS/session metadata |
| AD-02 | Snapshot representative Windows app and enumerate supported controls | redacted JSON, app/window identity, ref inventory |
| AD-03 | Click/type/select/toggle using refs | command envelopes and fresh post-action snapshots |
| AD-04 | Stale ref, missing accessibility node, wrong window and unsupported control | fail-closed outcomes; no unintended action |
| AD-05 | Headed/headless and focus/input impact | measured focus, cursor/input effects per operation |
| AD-06 | Process timeout, cancellation and worker cleanup | process-tree/lease cleanup evidence |
| AD-07 | Sensitive data handling | redaction and local-only evidence review |
| AD-08 | W10 policy/runtime wrapper integration | API-level tests; no direct unrestricted CLI path |
| AD-09 | Regression against existing Browser Adapter | browser E2E remains green and isolated |
| AD-10 | Comparative cost/latency benchmark | same tasks, same model, token counts, wall-clock, failure rate and retries |

Initial pilot should be Windows on the Owner's actual interactive PC, because W10's current owner-host acceptance gap is physical Windows validation. This is a proposed sequence, not permission to install or execute.

## 8. Entry and exit gates

Entry prerequisites:
1. Read-only review of upstream license, release, security and platform docs.
2. Desktop capability contract and threat model reviewed.
3. Explicit Owner authorization to install/run the dependency on a designated host.
4. Test app and non-sensitive test account prepared.
5. Exact package/release checksum pinned.

Exit criteria for a pilot:
- All mandatory safety and fail-closed tests pass.
- Ref freshness and post-condition verification demonstrated.
- No bypass of W10 ProcessSupervisor, W24 authorization boundary or W112 contract.
- Existing Browser Adapter regression passes.
- Benchmarks include token usage and wall-clock time; no unsupported percentage claims.
- Evidence is read back and recorded in the W10 journal.
- Owner reviews pilot report before integration authorization.

## 9. Current disposition

- Architecture candidate: ACCEPTED FOR FURTHER EVALUATION.
- Dependency selection: NOT DECIDED.
- Installation: NOT AUTHORIZED / NOT PERFORMED.
- Desktop Adapter implementation: NOT AUTHORIZED / NOT STARTED.
- Runtime tests: NOT RUN.
- GitHub synchronization for this assessment: NOT PERFORMED.
- Work 10: ACTIVE — NOT RELEASED.

No existing LOCKED contract was changed.
