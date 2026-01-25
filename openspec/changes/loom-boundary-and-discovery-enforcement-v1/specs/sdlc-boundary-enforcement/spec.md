## ADDED Requirements

### Requirement: Boundary enforcement and discovery policy
The lifecycle engine MUST evaluate changed files against the BoundaryRegistry and enforce boundary limits and discovery Policy A during lifecycle transitions, while recording the BoundaryRegistry hash in ExecutionRecord links.

#### Scenario: Boundary limits exceeded during verification
- **WHEN** a bead attempts to transition to `verified` and its changed files exceed max_files_touched or max_subsystems_touched
- **THEN** the engine rejects the transition and records the violation metrics in an ExecutionRecord

#### Scenario: Discovery bead touches production paths
- **WHEN** a discovery bead attempts to transition while changed files match production path prefixes from the BoundaryRegistry
- **THEN** the engine rejects the transition and records the policy violation in an ExecutionRecord

#### Scenario: Boundary registry is linked
- **WHEN** the engine evaluates boundary policy for a transition
- **THEN** the resulting ExecutionRecord links the BoundaryRegistry artifact hash used for evaluation
