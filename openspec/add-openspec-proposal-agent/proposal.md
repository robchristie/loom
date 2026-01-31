# Change: Add agent-assisted OpenSpec proposal authoring

## Why
Today, Loom can:
- generate grounding bundles
- produce an agent plan
- hand off to codex-cli for implementation
- verify via evidence

But the "spec-first" principle means non-trivial work should be authorized by an approved OpenSpec change.
Right now, authoring OpenSpec change artifacts (proposal/tasks/spec deltas) and creating/approving an OpenSpecRef is a manual step.

This change adds an optional agent handoff to:
- discuss a feature/change (with clarification questions)
- generate OpenSpec change artifacts in OpenSpec format
- generate an OpenSpecRef in `proposal` state (and optionally provide a human-driven approval step)

This keeps Loom spec-first while reducing friction, and enables downstream steps (plan/implement/verify) to be automated once the spec is approved.

## What Changes
- Add a new agent action: **OpenSpec Proposal Authoring**
  - CLI: `sdlc agent openspec-propose <bead_id> --change-id <change-id> [options]`
  - The agent conducts an interview loop (clarifying questions) and then drafts OpenSpec artifacts.

- Generated OpenSpec artifacts (written to the repo):
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/tasks.md`
  - `openspec/changes/<change-id>/specs/<capability>/spec.md` (at least one delta spec; OpenSpec validate requires it)
  - Optional: `openspec/changes/<change-id>/design.md` if the agent determines it is required by the OpenSpec criteria.

- Create an `OpenSpecRef` JSON in `proposal` state:
  - `openspec/refs/<openspec_ref_id>.json`
  - The agent MUST NOT auto-approve the ref (OpenSpec approval remains a human gate).

- Add a human-driven approval helper (optional but recommended for a smoother workflow):
  - CLI: `sdlc openspec approve-ref <openspec_ref_id>`
  - This transitions the OpenSpecRef state `proposal -> approved` and records `approved_at` and `approved_by` as a human actor.

- Optional “LLM council” drafting:
  - If enabled, multiple models each draft a proposal/tasks/spec delta set.
  - A synth step merges them into one final set of artifacts (still emitted as a single OpenSpec change directory).

- Persist agent output as Loom artifacts for traceability:
  - `runs/<bead_id>/agent_openspec.json` (structured representation of what was generated)
  - `runs/<bead_id>/agent_openspec.md` (human-readable transcript/summary, including Q&A)

- Add a non-interactive API endpoint (for UI + automation):
  - `POST /api/beads/{bead_id}/agent/openspec-propose`
  - This endpoint is non-interactive by design; it accepts user-supplied context/answers and produces artifacts.

## Impact
- Affected specs (OpenSpec):
  - New capability spec delta: `openspec-proposal-agent`

- Affected code (Loom):
  - `src/sdlc/agents/` (new agent + schemas)
  - `src/sdlc/agents/config.py` (model settings / council config)
  - `src/sdlc/agents/runner.py` (new runner function)
  - `src/sdlc/cli.py` (new commands)
  - `src/sdlc/server.py` (new endpoint + artifact index)
  - `tests/` (new tests for OpenSpec proposal agent and approval helper)

- Security / governance:
  - The agent MUST NOT author decision ledger entries of types that are reserved for humans/engine policy.
  - The agent MUST NOT mark an OpenSpecRef as approved without explicit human action.
  - File writes must be constrained to `openspec/changes/...`, `openspec/refs/...`, and `runs/<bead_id>/...`.

- Out of scope (for this change):
  - A full web chat UI for the interview loop.
  - Automatic modification of Bead.status or any engine-owned transitions.
  - Automatic OpenSpec approval without a human action.
