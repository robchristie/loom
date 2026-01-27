# Tasks: loom-decision-journaling-and-abort-hardening-v1

## 1. Canonicalize abort decision semantics
- [x] Document in loom-specification.md that aborts use decision_type=scope_change
- [x] Ensure all abort paths create DecisionLedgerEntry(decision_type=scope_change)

## 2. Journal decision actions
- [x] Add helper: record_decision_action(...)
- [x] Helper emits ExecutionRecord with:
  - requested_transition = null
  - applied_transition = null
  - exit_code = 0
  - link to DecisionLedgerEntry
- [x] Choose phase correctly (plan vs verify)

## 3. Explicit abort command hardening
- [x] Ensure `sdlc abort` always:
  - creates DecisionLedgerEntry
  - journals decision action
  - then attempts abort transition
- [x] Ensure behavior is correct even if bead is terminal

## 4. Automatic abort hardening
- [x] For engine-enforced aborts (boundary / anti-stall):
  - journal decision action
  - then apply transition
  - clearly annotate notes_md as engine-applied abort

## 5. Tests
- [x] Abort produces both decision-action and transition ExecutionRecords
- [x] Abort decision recorded even if transition is rejected
- [x] decision_type for abort is always scope_change
- [x] Engine-applied aborts annotate notes_md correctly

## 6. Spec update
- [x] Update docs/loom-specification.md with:
  - abort == scope_change clarification
  - explicit “decision actions are journaled” rule
