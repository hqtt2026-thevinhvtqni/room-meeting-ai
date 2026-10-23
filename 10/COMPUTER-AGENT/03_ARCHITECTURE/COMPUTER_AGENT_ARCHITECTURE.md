# WORK 10 — COMPUTER AGENT ARCHITECTURE

## 1. Goal
Build a real browser/computer agent from specification. Existing HTML under 01_ORIGINAL and 04_CODE is reference/mock only.

## 2. Boundary
Dashboard is presentation/control UI. The Agent Runtime performs actions and verification.

User -> Dashboard -> Agent API -> Agent Runtime -> Browser/Computer -> Observation -> Agent Runtime -> Verification -> Evidence

## 3. Core capabilities
- observe: screenshot + structured page/UI inspection
- navigate
- click
- type
- key_press
- scroll
- wait
- extract
- screenshot
- download
- workflow execution
- close
- verify post-condition

## 4. Safety
- explicit action types; never infer that typing a button label means clicking it
- validate target before destructive actions
- bounded retries/timeouts
- record every action and observation
- no silent success: task is PASS only after verification

## 5. Implementation phases
P0: runnable Agent API + capability contracts
P1: browser session lifecycle
P2: observe/navigate/click/type/key/wait/extract
P3: workflow loop + verification + evidence
P4: Dashboard
P5: integrated E2E and release package
