# OpenSpec Change: loom-boundary-and-discovery-enforcement-v1

## Summary
Add BoundaryRegistry-based enforcement and discovery-bead production-path protection to Loom MVP, per Agentic SDLC v1.

## Motivation
The current Loom engine enforces core lifecycle gating (spec, evidence, approval), but does not yet enforce:
- Boundary computation and policy limits (files/subsystems), required by the Boundary Computation Rule and Boundary Violation Handling.
- Discovery bead restrictions against modifying production paths, required by Discovery beads policy (normative default Policy A).

These are major workflow-safety features: they prevent “scope creep” and prevent discovery work from landing production changes.

## Scope
In scope:
1) Boundary computation:
- Determine which subsystems are touched by a bead’s changes using BoundaryRegistry.subsystems[].paths prefix matching.
- If bead.boundary_registry_ref is absent, use project default boundary registry.
- Record the BoundaryRegistry hash and selected subsystems in ExecutionRecord.notes_md and/or ExecutionRecord.links.

2) Boundary enforcement:
- Enforce project defaults:
  - max_files_touched (recommended default 8)
  - max_subsystems_touched (recommended default 2)
- If limits are exceeded mid-run, block further transitions toward verified and force bead to `aborted:needs-discovery`
  OR require an explicit split plan via BeadReview (minimal v1: force abort).
- Record the violation and computed metrics in an ExecutionRecord.

3) Discovery bead protection (Policy A):
- Define "production paths" as the union of all BoundaryRegistry subsystem path prefixes used for the bead.
- For BeadType.discovery:
  - Reject transitions that would advance work if modified files include any production paths.
  - Allow modifications only under an allowlist (project-configurable; default: docs/, notes/, tools/, experiments/, runs/).
- Record the active policy in ExecutionRecord.notes_md.

Out of scope:
- Hard sandboxing (Policy B workspace isolation).
- Full automatic bead splitting / generating new beads (only force abort and require human follow-up).
- Any schema_version changes.

## Acceptance Criteria
- `uv run pytest -q` passes.
- Boundary computation:
  - Given a boundary registry with subsystems and paths, and a mocked set of changed files, the engine computes touched subsystems correctly.
  - ExecutionRecord includes a link to the BoundaryRegistry hash used for evaluation.
- Boundary enforcement:
  - If changed files exceed max_files_touched or max_subsystems_touched, a verify-ward transition is blocked and the event is recorded.
  - Minimal v1 behavior: transition attempt returns not-ok with a clear reason; optional CLI command can force `aborted:needs-discovery`.
- Discovery protection:
  - A discovery bead attempting to proceed when production paths were modified is rejected and recorded.
  - A discovery bead modifying only allowlisted paths is permitted (subject to existing gates).
