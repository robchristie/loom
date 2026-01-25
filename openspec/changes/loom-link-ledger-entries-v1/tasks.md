# Tasks: loom-link-ledger-entries-v1

## 1) Decision lookup helpers
- [x] Add helper(s) in engine.py (or io.py) to find:
  - active exception decision for bead (decision_type=exception, bead_id match, not expired, summary non-empty)
  - approval decision for bead (decision_type=approval, bead_id match, created_by.kind=human, summary non-empty)

Return the chosen entry (prefer most recent by created_at if multiple exist).

## 2) Link decisions in ExecutionRecord
- [x] Extend record_transition_attempt(...) to accept extra_links: list[ArtifactLink]
- [x] When journaling a *successful* transition:
  - If transition == "ready -> in_progress" and bead.execution_profile == exception:
    - include link to the chosen exception decision entry
  - If transition == "approval_pending -> done":
    - include link to the chosen approval decision entry

Use ArtifactLink:
- artifact_type: "decision_ledger_entry"
- artifact_id: entry.artifact_id
- schema_name: "sdlc.decision_ledger_entry"
- schema_version: 1

## 3) Tests
- [x] Add tests that:
  - create bead + decision ledger entry + perform transition via CLI request()
  - assert last journal record contains the link
- [x] Include both positive and negative tests:
  - negative: exception bead with no exception entry -> start transition rejected and journal record has no applied_transition.

## 4) Docs (optional but recommended)
- [x] Add a short paragraph in docs/loom-specification.md describing that ExecutionRecord.links will include approval/exception decision links. (tracked in work-xi2)
