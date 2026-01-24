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
