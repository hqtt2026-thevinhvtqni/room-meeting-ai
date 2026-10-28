# Architecture

## Objective

Create a website-building system that can receive a natural-language request and autonomously produce a runnable website.

## Initial Components

1. Intent / command input
2. Planner
3. Project generator
4. File editor
5. Runtime manager
6. Browser preview
7. E2E verifier
8. Evidence collector

## Integration

Website Builder must use the ROOM-HOP execution architecture rather than creating an independent execution path.

Target:

AI
→ MCP
→ Core
→ Workspace / Execution Contract
→ PC Execution Host
→ Website Runtime

## UI Direction

The builder UI should eventually support:

- Command / prompt input
- DIFF
- LOG
- PREVIEW

The preview must represent the real running website.
