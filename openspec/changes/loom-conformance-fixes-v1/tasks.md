# Tasks: loom-conformance-fixes-v1

## 1) Approval CLI loosening
- Modify `sdlc approve`:
  - Require summary is non-empty.
  - If summary does not start with `APPROVAL:`, print a warning to stderr/stdout but do not fail.
  - Keep decision_type=approval, created_by.kind=human.

## 2) Canonical OpenSpecRef store + sync
- Define canonical store for OpenSpecRef artifacts:
  - `openspec/refs/<artifact_id>.json`
- Add `sdlc openspec sync <bead_id>`:
  - Load bead
  - Require bead.openspec_ref present
  - Read `openspec/refs/<bead.openspec_ref.artifact_id>.json`
  - Validate as OpenSpecRef
  - Write to `runs/<bead_id>/openspec_ref.json`
  - Optionally print path written

## 3) Evidence validate records git + produced_artifacts
- In `sdlc evidence validate`:
  - Write an ExecutionRecord that includes:
    - git.head_before + git.dirty_before (best effort)
    - produced_artifacts includes `runs/<bead_id>/evidence.json`
    - notes_md includes validation errors when present

## 4) Evidence invalidation compares against evidence-validation record
- Update `invalidate_evidence_if_stale`:
  - Find the most recent ExecutionRecord for the bead where:
    - phase == verify
    - produced_artifacts contains `runs/<bead_id>/evidence.json`
    - exit_code == 0 (validated)
  - Compare current git head/dirty to that record.git.head_before/dirty_before
  - If changed: invalidate evidence and record ExecutionRecord with explicit reason(s)

## 5) Tests
Add/extend tests to cover:
- approval summary without prefix succeeds (warns)
- openspec sync writes runs/<bead_id>/openspec_ref.json
- evidence validate writes execution record with produced_artifacts and git info (can be monkeypatched if needed)
- evidence invalidation triggers when git head changes relative to the validation record

## 6) Docs update
Update `docs/loom-specification.md` to include canonical bead/bead_review filenames and approval prefix guidance.
