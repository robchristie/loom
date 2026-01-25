## ADDED Requirements

### Requirement: Decision ledger linking
The lifecycle engine MUST link relevant DecisionLedgerEntry artifacts in ExecutionRecord links for exception-profile starts and approvals.

#### Scenario: Exception decision linked on start
- **WHEN** a bead with execution_profile exception transitions from `ready` to `in_progress`
- **THEN** the transition ExecutionRecord links the active exception DecisionLedgerEntry

#### Scenario: Approval decision linked on done
- **WHEN** a bead transitions from `approval_pending` to `done`
- **THEN** the transition ExecutionRecord links the approval DecisionLedgerEntry
