# Change: Add agentic runner (Pydantic-AI + OpenRouter + codex-cli)

## Why
Loom currently provides an SDLC kernel with artifacts, phase gates, and an audit trail, but it does not yet execute “agentic” work end-to-end.
This change adds a first-class agent runner that can:
- generate structured plans/prompts (planner agent),
- perform implementation via codex-cli (implementation agent),
- execute verification via acceptance checks + evidence validation (verification runner),
while preserving Loom’s enforcement guarantees (gates, authority rules, and append-only journaling).

## What Changes
- Add an **Agent Runner** subsystem that supports phase-specific runs:
  - **plan**: OpenRouter-backed planner agent produces a structured plan and a codex-ready prompt.
  - **implement**: codex-cli runs against the repo using the GroundingBundle as primary context; runner journals actions and flags out-of-grounding modifications (best-effort).
  - **verify**: runner executes Bead acceptance checks, writes an EvidenceBundle, validates it through the engine, and (optionally) requests the engine-authored verified transition as a system actor.

- Add configuration for agent models and tools:
  - OpenRouter API key + model names for planner/verifier
  - codex-cli executable path and default arguments
  - optional toggles for “auto-transition” behavior

- Extend the SDLC CLI and API surface:
  - `sdlc agent plan <bead_id>`
  - `sdlc agent implement <bead_id>`
  - `sdlc agent verify <bead_id>`
  - (optional) `sdlc agent run <bead_id> --phase {plan|implement|verify}`

- Add new run artifacts (non-breaking additions):
  - `runs/<bead_id>/agent_plan.json` (structured plan output)
  - `runs/<bead_id>/codex_prompt.md` (prompt for codex-cli)
  - `runs/<bead_id>/codex.log` (stdout/stderr capture)
  - `runs/<bead_id>/evidence/<check_name>.log` (per-check logs; optional)
  - `runs/<bead_id>/agent_verify.json` (optional structured verifier output)

- Ensure every agent action is journaled:
  - Append an `ExecutionRecord` for each agent run (phase, commands executed, git refs, produced artifacts, notes).

## Non-Goals
- Full autonomy (human approvals remain required).
- Streaming agent outputs over websockets/SSE (initial implementation is synchronous; logs are written to artifacts and shown via existing journal UI).
- Advanced sandboxing / syscall-level enforcement (initial out-of-grounding enforcement is best-effort via changed-file detection).
- Multi-agent parallelism or distributed execution.

## Impact
- Affected specs (OpenSpec deltas):
  - `agent-runner` (new capability): introduces normative behavior for phase execution and journaling.

- Affected code (high level):
  - `src/sdlc/` (new `agents/` package + runner)
  - `src/sdlc/cli.py` (new `agent` subcommands)
  - `src/sdlc/server.py` (optional endpoints for UI)
  - `ui/` (optional: add “Run agents” buttons)

- New configuration:
  - Environment variables for OpenRouter and codex-cli.

- Compatibility / breaking changes:
  - No breaking changes to existing artifact schemas.
  - Adds new optional artifacts and commands only.

- Security considerations:
  - Do not log API keys or request headers.
  - Record policy violations as notes, not secrets.
  - Prefer least-privilege command execution; default allowlist inherits from GroundingBundle.
