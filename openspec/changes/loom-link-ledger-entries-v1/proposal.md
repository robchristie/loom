# Change Proposal: loom-link-ledger-entries-v1

## Summary
Improve auditability by ensuring ExecutionRecord entries link the relevant DecisionLedgerEntry artifacts for:
- execution_profile exceptions (start transition)
- approvals (done transition)

This implements the Loom spec’s requirement that the engine link these decisions from the canonical run journal.

## Motivation
The engine currently enforces the existence of required DecisionLedgerEntry records (exception, approval),
but does not link them in ExecutionRecord.links. This weakens traceability when reviewing why a bead was
allowed to start (exception) or considered complete (approval).

## Scope
In scope:
- Add helpers to locate the relevant DecisionLedgerEntry for:
  - exception entries for a bead (non-expired)
  - approval entries for a bead (human-created, non-empty summary)
- Update transition journaling so that:
  - `ready -> in_progress` records a link to the exception entry when `execution_profile == exception`
  - `approval_pending -> done` records a link to the approval entry
- Add tests to lock the behavior.

Out of scope:
- New schema fields
- Decision ledger policy enforcement beyond what exists (e.g., rationale required)

## Acceptance Criteria
- `uv run pytest -q` passes.
- Exception linking:
  - For a bead with `execution_profile == exception` and a valid exception decision entry,
    a successful `ready -> in_progress` transition appends an ExecutionRecord where:
    - `links` contains an ArtifactLink with `artifact_type == "decision_ledger_entry"`
    - linked `artifact_id` equals the decision entry’s artifact_id
- Approval linking:
  - For a bead with a valid approval decision entry,
    a successful `approval_pending -> done` transition appends an ExecutionRecord where:
    - `links` contains an ArtifactLink with `artifact_type == "decision_ledger_entry"`
    - linked `artifact_id` equals the approval entry’s artifact_id

## Notes
This change assumes ExecutionRecord already inherits SchemaBase.links (it does).
We avoid schema_version changes and keep linking as an additive audit improvement.
