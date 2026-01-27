# SDLC Quickstart

## Prereqs
- Python tooling via `uv`
- Run from repo root

## Validate an artifact
```bash
uv run sdlc validate runs/<bead_id>/evidence.json
```

## Export schemas
```bash
uv run sdlc schema-export
```

## Transition request
```bash
uv run sdlc request <bead_id> "draft -> sized"
```

## Evidence workflow
```bash
uv run sdlc evidence collect <bead_id>
uv run sdlc evidence validate <bead_id>
uv run sdlc evidence invalidate-if-stale <bead_id>
```

Note:
- `sdlc evidence validate` uses `expect_exit_code`
- `ready -> in_progress` enforces dependencies
- Spec gate requires `runs/<bead_id>/openspec_ref.json` for implementation work

## Grounding
```bash
uv run sdlc grounding generate <bead_id>
```

## Approvals
```bash
uv run sdlc approve <bead_id> --summary "APPROVAL: looks good"
```

## Example flow
```bash
# 1) Validate bead
uv run sdlc validate runs/<bead_id>/bead.json

# 2) Generate grounding
uv run sdlc grounding generate <bead_id>

# 3) Request start
uv run sdlc request <bead_id> "ready -> in_progress"

# 4) Collect and validate evidence
uv run sdlc evidence collect <bead_id>
uv run sdlc evidence validate <bead_id>

# 5) Mark verified -> approval -> done
uv run sdlc request <bead_id> "verification_pending -> verified"
uv run sdlc approve <bead_id> --summary "APPROVAL: shipped"
uv run sdlc request <bead_id> "approval_pending -> done"
```

## Agent workflow

These commands run the planner, implementation (codex-cli), and verification runner.

```bash
# 0) Ensure grounding + OpenSpecRef are present (recommended)
uv run sdlc grounding generate <bead_id>
uv run sdlc openspec sync <bead_id>

# 1) Plan
uv run sdlc agent plan <bead_id>

# 2) Implement (codex-cli)
uv run sdlc agent implement <bead_id>

# 3) Verify (runs acceptance checks + writes evidence)
uv run sdlc agent verify <bead_id>
```

Artifacts written:
- `runs/<bead_id>/agent_plan.json`
- `runs/<bead_id>/codex_prompt.md`
- `runs/<bead_id>/codex.log`
- `runs/<bead_id>/evidence.json`
- `runs/<bead_id>/evidence/*.log`
