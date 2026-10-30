# 01 — DISCOVER / KHÁM PHÁ
- **STT / Document ID:** DOC-007
- **Priority:** P1
- **Read order:** 11
- **Depends on:** DOC-001
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30

## Problem statement

ROOM-HOP tracks many Works and child branches, but the current Work-centric folder structure does not consistently reveal the lifecycle position and readiness of the whole product. A completed child task can be mistaken for product-level completion.

## Product outcome

Every Work can answer, from one place:
1. What product is this Work building?
2. Which lifecycle phase is active?
3. What has been verified?
4. What is blocked, by whom, and by what dependency?
5. What evidence is required for the next gate?

## Users

- Vinh: portfolio/product oversight and final authority.
- Xu / lifecycle coordinator: planning, coordination, decision preparation.
- Builders: execute assigned work packages.
- Independent QE/QA: verify outputs and evidence.
- Reviewers / release owners: inspect gate readiness and decisions.

## Non-goals

- Do not rebuild the agent framework as the product.
- Do not migrate all existing Works in this initial Work 70 pass.
- Do not claim live dashboard integration before a real data source is connected.
- Do not replace Core with per-Work local state files.
