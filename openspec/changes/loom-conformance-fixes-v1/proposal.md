# OpenSpec Change: loom-conformance-fixes-v1

## Summary
Bring Loom MVP into closer conformance with Agentic SDLC v1 by:
- Aligning approval CLI behavior with the Approval Recording Rule (non-empty summary; prefix recommended, not required).
- Adding an OpenSpecRef sync command so spec gating is workable in normal flows.
- Making evidence invalidation correctly track repo changes after evidence validation (git ref recorded at validation time).
- Documenting canonical filenames for SDLC-managed bead artifacts used by the engine.

## Motivation
Current behavior has three sharp edges:
1) `sdlc approve` rejects approvals that are valid per spec.
2) `runs/<bead_id>/openspec_ref.json` is required by the engine but not conveniently produced.
3) Evidence invalidation is not anchored to the moment evidence becomes validated (no git ref captured on validation), so “code changed since evidence” is unreliable.

## Scope
In scope:
- CLI + engine/io changes needed to support:
  - Approval summary rule: non-empty required; `APPROVAL:` prefix warning only.
  - `sdlc openspec sync <bead_id>`: copies canonical OpenSpecRef to `runs/<bead_id>/openspec_ref.json`.
  - Evidence validate writes an ExecutionRecord that includes git ref + produced_artifacts referencing the evidence bundle path.
  - Evidence invalidation compares current git state to the git state recorded at evidence validation.
- Update `docs/loom-specification.md` to reflect canonical filenames for bead artifacts and the non-required approval prefix.

Out of scope:
- Full boundary registry enforcement, discovery policies, intervention counters, or container sandbox enforcement.
- Any changes to schema_version.

## Acceptance Criteria
- `uv run pytest -q` passes.
- Approvals:
  - `sdlc approve <bead_id> --summary "ok"` succeeds and appends a DecisionLedgerEntry with decision_type=approval.
  - If summary does not start with `APPROVAL:`, command prints a warning but still succeeds.
- OpenSpec sync:
  - `sdlc openspec sync <bead_id>` writes `runs/<bead_id>/openspec_ref.json` that validates as `sdlc.openspec_ref`.
- Evidence git anchoring:
  - `sdlc evidence validate <bead_id>` writes an ExecutionRecord containing a non-null `git.head_before` (when git is available) and includes `runs/<bead_id>/evidence.json` in produced_artifacts.
  - `sdlc evidence invalidate-if-stale <bead_id>` invalidates validated evidence when HEAD differs from the git ref recorded at validation time, and records an ExecutionRecord describing the staleness signal.
- Docs:
  - `docs/loom-specification.md` explicitly lists:
    - `runs/<bead_id>/bead_review.json` as BeadReview location
    - `runs/<bead_id>/bead.json` as Bead location (when Loom-managed)
    - Approval prefix as recommended (not required)

## Notes
This change intentionally keeps the MVP small and avoids adding new schema fields; git anchoring is recorded via ExecutionRecord.
