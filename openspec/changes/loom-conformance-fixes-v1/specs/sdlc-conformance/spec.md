## ADDED Requirements

### Requirement: Conformance fixes for approvals, evidence, and OpenSpec sync
The lifecycle engine and CLI MUST conform to approval, evidence, and OpenSpecRef workflows described in the Loom specification.

#### Scenario: Approval summaries are accepted with warnings
- **WHEN** an approval is recorded without the recommended `APPROVAL:` prefix
- **THEN** the CLI warns but still records the approval DecisionLedgerEntry

#### Scenario: Evidence validation anchors git state
- **WHEN** evidence is validated
- **THEN** the ExecutionRecord includes the git head and produced_artifacts pointing to the evidence bundle

#### Scenario: OpenSpecRef sync writes bead artifact
- **WHEN** `sdlc openspec sync` is invoked for a bead
- **THEN** the tool writes `runs/<bead_id>/openspec_ref.json` that validates as an OpenSpecRef
