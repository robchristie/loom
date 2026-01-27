## 1. Scaffolding
- [ ] 1.1 Create `src/sdlc/agents/` package with:
  - `config.py` (env-driven settings; uses pydantic-settings)
  - `openrouter.py` (OpenRouter model/client factory for Pydantic-AI)
  - `schemas.py` (Pydantic models for planner/verifier structured outputs)
  - `planner.py` (Pydantic-AI agent that produces `AgentPlan`)
  - `codex_runner.py` (subprocess wrapper to run codex-cli + capture logs)
  - `evidence_runner.py` (exec acceptance checks + write logs/exit codes)
  - `runner.py` (high-level orchestration for plan/implement/verify)

- [ ] 1.2 Add a small “public” API in `src/sdlc/agents/__init__.py`:
  - `run_plan(paths, bead_id, actor, *, options=...)`
  - `run_implement(paths, bead_id, actor, *, options=...)`
  - `run_verify(paths, bead_id, actor, *, options=...)`

## 2. Configuration (env vars)
- [ ] 2.1 Add agent settings via `pydantic-settings` (new file or integrate into existing config patterns):
  - `OPENROUTER_API_KEY` (required for planner/verifier)
  - `LOOM_OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`)
  - `LOOM_PLANNER_MODEL` (default sensible model string)
  - `LOOM_VERIFIER_MODEL` (default sensible model string)
  - `LOOM_CODEX_BIN` (default `codex`)
  - `LOOM_CODEX_ARGS` (default empty; parsed safely)
  - `LOOM_AGENT_AUTO_TRANSITION` (default false)

- [ ] 2.2 Ensure missing keys/tools fail with actionable errors (no stack traces by default).

## 3. OpenRouter + Pydantic-AI integration
- [ ] 3.1 Implement a Pydantic-AI model factory that targets OpenRouter (base_url override + API key).
- [ ] 3.2 Add a minimal wrapper so tests can swap the model for a fake/stub (no network in tests).

## 4. Planner agent (OpenRouter)
- [ ] 4.1 Implement `AgentPlan` output model (in `schemas.py`), e.g.:
  - `summary_md`
  - `step_plan` (list of steps)
  - `files_to_focus` (list of repo paths)
  - `codex_prompt_md` (final prompt body for codex-cli)

- [ ] 4.2 Implement `planner.py`:
  - Inputs: Bead, OpenSpecRef (if present), GroundingBundle summary/items
  - Output: `AgentPlan` (typed)

- [ ] 4.3 Persist outputs:
  - Write `runs/<bead_id>/agent_plan.json`
  - Write `runs/<bead_id>/codex_prompt.md`

- [ ] 4.4 Journal planner run:
  - Append `ExecutionRecord` with `phase=plan`, `commands=[]`, `produced_artifacts=[agent_plan.json, codex_prompt.md]`, and a brief `notes_md`.

## 5. Implementation runner (codex-cli)
- [ ] 5.1 Implement a prompt builder:
  - Always include: Bead requirements/context/acceptance criteria + acceptance checks
  - Include OpenSpecRef summary (change id + state)
  - Include GroundingBundle items (titles + snippets + file refs)
  - Include hard constraints:
    - allowed commands
    - disallowed commands
    - excluded paths
    - instruction to use `uv run` for tests

- [ ] 5.2 Implement `codex_runner.py`:
  - Run codex-cli via subprocess (configurable bin/args)
  - Write combined stdout/stderr to `runs/<bead_id>/codex.log`
  - Capture `git head_before/after` and `dirty_before/after` around the run

- [ ] 5.3 Best-effort “out-of-grounding” detection:
  - Compute changed files between `head_before` and working tree state after codex run (use existing git helpers if available)
  - If codex modifies paths not present in GroundingBundle file refs (excluding `runs/`), record a policy violation note in the `ExecutionRecord.notes_md`

- [ ] 5.4 Journal implement run:
  - Append `ExecutionRecord` with `phase=implement`, `commands=["codex ..."]`, `produced_artifacts=[codex.log]`, `git=...`, `exit_code=...`

- [ ] 5.5 (Optional, gated by config/flag) Auto-transition:
  - If bead is `ready`, request `ready -> in_progress` before running codex
  - If codex exits 0, request `in_progress -> verification_pending`

## 6. Verification runner (execute acceptance checks + evidence)
- [ ] 6.1 Implement `evidence_runner.py` that:
  - Reads Bead acceptance checks
  - Executes each command (subprocess) with timestamps
  - Writes per-check logs under `runs/<bead_id>/evidence/`
  - Produces an `EvidenceBundle` with items containing `command`, `exit_code`, `started_at`, `finished_at`, and attachments to logs

- [ ] 6.2 Call engine validation:
  - Use existing `validate_evidence_bundle(...)` to mark validated (engine-authored) when requirements are met
  - Ensure evidence status transitions respect the Evidence Authority Rule by only writing via engine functions

- [ ] 6.3 (Optional, gated by config/flag) Auto-transition:
  - If evidence validates successfully and bead is `verification_pending`, request `verification_pending -> verified` **as a system actor** (never as agent)

- [ ] 6.4 Journal verify run:
  - Append `ExecutionRecord` with `phase=verify`, commands executed, produced artifacts (evidence.json + logs), exit code, and summary notes.

## 7. CLI wiring
- [ ] 7.1 Add `agent_app = typer.Typer()` to `src/sdlc/cli.py` and register it under `app.add_typer(...)`.
- [ ] 7.2 Add commands:
  - `uv run sdlc agent plan <bead_id>`
  - `uv run sdlc agent implement <bead_id>`
  - `uv run sdlc agent verify <bead_id>`
  - Support `--auto-transition/--no-auto-transition` overrides per command

- [ ] 7.3 Update `docs/sdlc_quickstart.md` with an “Agent workflow” section.

## 8. API + UI wiring (recommended)
- [ ] 8.1 Add server endpoints (FastAPI) similar to grounding/evidence endpoints:
  - `POST /api/beads/{bead_id}/agent/plan`
  - `POST /api/beads/{bead_id}/agent/implement`
  - `POST /api/beads/{bead_id}/agent/verify`
  - Return `ActionResponse` and rely on existing `journal.jsonl` for UI updates

- [ ] 8.2 Update artifacts index to include:
  - agent plan + codex prompt + codex log (if present)

- [ ] 8.3 Update UI bead page to add buttons for:
  - Run Plan Agent
  - Run Implement (codex)
  - Run Verify
  - Show links to new artifacts when present

## 9. Tests + quality gates
- [ ] 9.1 Add unit tests for:
  - Planner output persistence + journaling (stub the LLM)
  - Codex runner logging + journaling (monkeypatch subprocess)
  - Evidence runner exit-code capture and validation (use a trivial command like `python -c "exit(0)"`)

- [ ] 9.2 Run:
  - `uv run pytest -q`
  - `uv run ruff check .`
  - `uv run mypy`

## 10. OpenSpec validation
- [ ] 10.1 Add at least one delta spec under `openspec/changes/add-agentic-runner/specs/`.
- [ ] 10.2 Run `openspec validate add-agentic-runner --strict --no-interactive` and fix any issues.
