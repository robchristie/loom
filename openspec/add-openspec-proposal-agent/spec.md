## ADDED Requirements

### Requirement: OpenSpec proposal agent command
The system SHALL provide a CLI command that drafts OpenSpec change artifacts from a bead via an agent-driven interview and drafting workflow.

#### Scenario: Interactive interview produces OpenSpec artifacts
- **WHEN** a human runs `sdlc agent openspec-propose <bead_id> --change-id <id>` in interactive mode
- **THEN** the system SHALL ask clarifying questions (up to a configured max round count)
- **AND THEN** the system SHALL write `proposal.md`, `tasks.md`, and at least one delta `spec.md` under `openspec/changes/<id>/`

#### Scenario: Non-interactive mode produces OpenSpec artifacts
- **WHEN** a human or automation runs the command with `--no-interactive`
- **THEN** the system SHALL produce OpenSpec artifacts without prompting for answers
- **AND THEN** the generated proposal SHALL record any key assumptions the agent had to make

### Requirement: OpenSpecRef generation and human approval gate
The system SHALL generate an OpenSpecRef in `proposal` state for agent-authored OpenSpec changes, and SHALL provide a human-driven mechanism to mark it approved.

#### Scenario: Agent creates a proposal-state OpenSpecRef
- **WHEN** the OpenSpec proposal agent completes drafting a change
- **THEN** the system SHALL write an `OpenSpecRef` JSON file under `openspec/refs/` with `state == proposal`

#### Scenario: Human approves an OpenSpecRef
- **WHEN** a human runs `sdlc openspec approve-ref <openspec_ref_id>`
- **THEN** the system SHALL transition the referenced OpenSpecRef to `state == approved`
- **AND THEN** the system SHALL set `approved_by.kind == human`

### Requirement: Optional council drafting
The system SHOULD support an optional council mode where multiple models draft independently and a synth step produces the final OpenSpec artifacts.

#### Scenario: Council mode synthesizes a single final change
- **WHEN** the OpenSpec proposal command runs with council mode enabled
- **THEN** the system SHALL produce exactly one final set of OpenSpec artifacts in `openspec/changes/<change-id>/`
