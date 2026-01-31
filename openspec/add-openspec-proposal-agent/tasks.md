## 1. OpenSpec delta scaffold
- [ ] 1.1 Create `openspec/changes/add-openspec-proposal-agent/specs/openspec-proposal-agent/spec.md` with ADDED requirements and scenarios.
- [ ] 1.2 Ensure the delta spec follows OpenSpec formatting rules (`## ADDED Requirements`, `### Requirement:`, and `#### Scenario:`).
- [ ] 1.3 (If OpenSpec CLI is available) run: `openspec validate add-openspec-proposal-agent --strict --no-interactive`

## 2. Agent schemas + configuration
- [ ] 2.1 Extend `src/sdlc/agents/config.py`:
  - Add `openspec_model` (default to planner_model if unset)
  - Add optional council config: `openspec_council_models` and `openspec_synth_model`
  - Add `openspec_interview_rounds_max` and `openspec_interactive_default`
- [ ] 2.2 Extend `src/sdlc/agents/schemas.py` with structured outputs:
  - Interview output: list of clarifying questions
  - Draft output: change-id, proposal.md content, tasks.md content, optional design.md content, and a list of delta spec files (path + content)
  - Include enough structure to write files deterministically and test without network.

## 3. Implement the OpenSpec proposal agent
- [ ] 3.1 Add `src/sdlc/agents/openspec_proposer.py` (or similar name) implementing:
  - An “interview” agent (returns questions)
  - A “draft” agent (returns the OpenSpec artifacts to write)
  - Optional synth agent (merges council drafts)
- [ ] 3.2 Ensure the agent prompt enforces:
  - OpenSpec formatting conventions (proposal/tasks + delta specs with scenarios)
  - No auto-approval of OpenSpecRef
  - Council mode (if enabled) produces a single final artifact set

## 4. Runner integration + artifact persistence
- [ ] 4.1 Add `run_openspec_propose(...)` in `src/sdlc/agents/runner.py`:
  - Inputs: `bead_id`, `change_id`, `interactive`, `council`, optional `model_override`
  - Reads bead + optional grounding + (optional) openspec/project.md + openspec/AGENTS.md to build context
  - Interview loop (interactive mode): ask questions, collect answers, iterate up to max rounds
  - Non-interactive mode: skip questions; the agent must record assumptions in proposal output
- [ ] 4.2 Write generated OpenSpec files to:
  - `openspec/changes/<change_id>/proposal.md`
  - `openspec/changes/<change_id>/tasks.md`
  - `openspec/changes/<change_id>/specs/<capability>/spec.md` (at least one)
  - Optional: `openspec/changes/<change_id>/design.md`
  - Refuse to overwrite existing change dir unless `--overwrite` is explicitly provided
- [ ] 4.3 Create an OpenSpecRef in `proposal` state at:
  - `openspec/refs/<openspec_ref_id>.json`
  - Use `created_by.kind="agent"` for agent-created refs
- [ ] 4.4 Persist Loom run artifacts:
  - `runs/<bead_id>/agent_openspec.json` (structured output)
  - `runs/<bead_id>/agent_openspec.md` (Q&A transcript + summary)
  - Append an `ExecutionRecord` describing what was produced (paths, models used, council on/off)

## 5. CLI surface area
- [ ] 5.1 Add `sdlc agent openspec-propose` in `src/sdlc/cli.py`
  - Required args: `bead_id`, `--change-id`
  - Options:
    - `--interactive/--no-interactive`
    - `--council/--no-council`
    - `--openspec-ref-id` (optional override; otherwise derive from change-id)
    - `--overwrite` (off by default)
- [ ] 5.2 Add `sdlc openspec approve-ref <openspec_ref_id>` helper
  - Loads `openspec/refs/<id>.json`
  - Validates current state is `proposal`
  - Writes state `approved`, sets `approved_at`, sets `approved_by.kind="human"`
  - MUST require an explicit human invocation (no hidden approvals)

## 6. Server endpoint (non-interactive)
- [ ] 6.1 Add `POST /api/beads/{bead_id}/agent/openspec-propose` in `src/sdlc/server.py`
  - Accepts: change_id, optional council flag, and optional “answers” to interview questions
  - Produces the same outputs as the runner (without interactive prompts)
- [ ] 6.2 Extend bead artifact index so UI can discover:
  - `runs/<bead_id>/agent_openspec.json`
  - `runs/<bead_id>/agent_openspec.md`

## 7. Tests
- [ ] 7.1 Add tests for `run_openspec_propose` using `pydantic_ai.models.test.TestModel` (no network)
  - Asserts files are written to expected paths
  - Asserts at least one delta spec file is created
  - Asserts OpenSpecRef is created in `proposal` state
- [ ] 7.2 Add tests for `approve-ref`
  - Ensures it transitions `proposal -> approved`
  - Ensures `approved_by.kind == "human"`
- [ ] 7.3 Add a server test for the new endpoint (optional if current test harness supports API calls)

## 8. Docs
- [ ] 8.1 Update `docs/sdlc_quickstart.md` to include the new optional step:
  - “Draft OpenSpec proposal via agent” (before plan/implement)
  - Explain the human approval step for OpenSpecRef
- [ ] 8.2 Update `AGENTS.md` or a relevant doc to mention the new command and environment variables

## 9. Quality gates
- [ ] 9.1 Run `uv run pytest`
- [ ] 9.2 Run `uv run ruff check .`
- [ ] 9.3 Run `uv run mypy`
