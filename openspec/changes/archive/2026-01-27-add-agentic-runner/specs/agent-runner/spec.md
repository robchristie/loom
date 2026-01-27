## ADDED Requirements

### Requirement: Agent runner supports plan, implement, and verify phases
The system SHALL provide an agent runner that executes phase-specific actions for a bead and records each action as an ExecutionRecord.

#### Scenario: Plan run is journaled and persisted
- **WHEN** a plan run is executed for a bead
- **THEN** the system writes `runs/<bead_id>/agent_plan.json`
- **AND THEN** the system appends an `ExecutionRecord` with `phase == plan` and links/refs to produced artifacts

#### Scenario: Implement run is journaled and logs are persisted
- **WHEN** an implement run is executed for a bead
- **THEN** the system writes `runs/<bead_id>/codex.log`
- **AND THEN** the system appends an `ExecutionRecord` with `phase == implement` and includes git refs before/after when available

#### Scenario: Verify run produces evidence and is journaled
- **WHEN** a verify run is executed for a bead
- **THEN** the system writes `runs/<bead_id>/evidence.json`
- **AND THEN** the system appends an `ExecutionRecord` with `phase == verify`

### Requirement: OpenRouter-backed planner/verifier via Pydantic-AI
The system SHALL use Pydantic-AI to run planner and verifier agents, using OpenRouter as the LLM provider.

#### Scenario: Missing OpenRouter API key fails with actionable error
- **WHEN** a planner or verifier run is requested without OpenRouter credentials configured
- **THEN** the command fails with an actionable configuration error message
- **AND THEN** no partial artifacts are written except an ExecutionRecord describing the failure

### Requirement: GroundingBundle is the primary implementation context
The system SHALL provide the GroundingBundle as the primary repo context for the implementation agent and SHALL record best-effort policy violations for out-of-grounding modifications.

#### Scenario: Out-of-grounding modification is recorded
- **WHEN** the implementation agent modifies a file not present in the GroundingBundle file refs
- **THEN** the system appends an `ExecutionRecord` with `notes_md` describing the policy violation
