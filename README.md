# ROOM HOP

ROOM HOP is an experimental multi-agent meeting engine. It coordinates agent turns, records meeting messages and decisions, and applies room-level stop guards so agent autonomy does not mean unlimited authority.

> **Project status:** the canonical state record currently marks the discussion mechanism and MockConnector as verified, while real-API integration remains pending verification. Do not treat the project as end-to-end complete until a real-API run produces reviewable evidence. See [project state](context/PROJECT_STATE.md).

## What it does

- Coordinates a meeting lifecycle and participant turns.
- Supports agent decisions such as `REPLY`, `PASS`, and `FINAL`, subject to room-level limits.
- Separates current project state from meeting logs and historical evidence.
- Defines a public service boundary and API expectations in [API_CONTRACT.md](API_CONTRACT.md).

## Quickstart

Requirements: Python 3.10+ recommended; use the Python version supported by the project's dependencies.

```bash
git clone https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai.git
cd room-meeting-ai
python -m venv .venv
# Activate the virtual environment:
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest -q
```

The repository includes scripted/demo meeting runners, but some are explicitly **not real-API runs**. For example, `python run_meeting.py` uses a scripted exchange; it must not be used as evidence that real model connectors work.

For API-backed experiments, copy `.env.example` to `.env` and supply valid credentials for the provider being tested. Never commit secrets or real `.env` files.

## Architecture at a glance

- `core/` — meeting and discussion domain logic.
- `agents/` and provider adapter modules — agent/provider integration.
- `room_hop_mcp/` — MCP integration surface.
- `tests/` — automated tests.
- `context/PROJECT_STATE.md` — canonical verified project state.
- `AGENTS.md` — governance and agent operating rules.
- `API_CONTRACT.md` — API boundary and contract decisions.
- `meetings/` — meeting records and supporting evidence.

This is a high-level orientation, not a claim that every integration path is complete.

## Development and verification

- Run tests with `pytest -q`.
- CI is configured to run the test suite on pushes and pull requests.
- Mark a result `PASS` only when the relevant test or real integration has run and its evidence is linked.
- Do not merge a Work branch solely because it is behind `main`; inspect divergence, conflicts, scope, and verification first.

## Governance and contribution

Start with [AGENTS.md](AGENTS.md), then [the verified project state](context/PROJECT_STATE.md), and [the API contract](API_CONTRACT.md). The detailed internal agent onboarding notes are in [docs/AGENT_ONBOARDING.md](docs/AGENT_ONBOARDING.md).

Contributions should be isolated on a named branch and reviewed through a pull request that states scope, tests run, evidence, and known blockers. Work-specific changes must remain within that Work's declared scope. Do not merge directly to `main` without the required review and verification.
