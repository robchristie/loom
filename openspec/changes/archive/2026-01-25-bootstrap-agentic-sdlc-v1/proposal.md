# Proposal: bootstrap-agentic-sdlc-v1

## Intent
Implement a minimal SDLC lifecycle engine ("sdlc") that enforces Agentic SDLC v1 semantics via:
- Pydantic v2 normative schemas
- artifact validation + schema export
- canonical hashing (SHA-256 over canonical JSON)
- append-only JSONL journals (ExecutionRecord, DecisionLedgerEntry)
- bead state transition enforcement (+ rejection recording)
- evidence validate + invalidate-if-stale
- grounding bundle generation (heuristic, best-effort)

This bootstrap targets solo usage and integrates with existing Beads (`bd`) and OpenSpec tooling.
Execution is "safe enough" via containerization and conservative defaults.

## Why
Prevent LLM-driven drift by separating intent, plan, implement, verify, approve through enforceable artifacts + gates.

## Assumptions (v1)
- The repo uses `uv` for Python tooling (`uv run`, `uv sync`).
- The container environment has `codex`, `bd`, and `openspec` on PATH.
- Beads may remain owned by `bd` (e.g. `issues.jsonl`), but the engine can optionally store bead artifacts in `runs/<bead_id>/bead.json` if configured.

## Scope (v1 bootstrap)
Included:
- Python package `sdlc/` with CLI entrypoint
- schema validation + JSON schema export
- transition engine + ExecutionRecord journaling
- evidence validation + staleness invalidation
- approval command (DecisionLedgerEntry)
- tests for core semantics

Excluded:
- hard sandbox mediation of repo access
- multi-agent orchestration
- UI
- replacing bd/OpenSpec tools

## Success Criteria
- `uv run sdlc validate <artifact>` validates artifacts strictly (extra=forbid).
- `uv run sdlc request <bead_id> <transition>` enforces transition table, emits ExecutionRecord for success/rejection, and updates Bead.status only through the engine.
- `uv run sdlc evidence validate <bead_id>` enforces Evidence Validation Rule and updates EvidenceBundle.status to validated only if rules pass.
- `uv run sdlc evidence invalidate-if-stale <bead_id>` invalidates evidence on git change signals.
- Journals are append-only JSONL and are never rewritten.
