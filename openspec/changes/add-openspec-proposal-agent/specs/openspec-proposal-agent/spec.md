## ADDED Requirements

### Requirement: OpenSpec proposal authoring via agent
The system SHALL provide an agent-driven workflow that drafts OpenSpec change artifacts from a bead, optionally running an interactive interview loop to gather clarifications.

#### Scenario: Interactive interview produces OpenSpec artifacts
- **WHEN** a human runs `sdlc agent openspec-propose <bead_id> --change-id <change-id>` in interactive mode
- **THEN** the system SHALL ask clarifying questions (up to a configured maximum round count)
- **AND THEN** the system SHALL write `proposal.md`, `tasks.md`, and at least one delta `spec.md` under `openspec/changes/<change-id>/`

#### Scenario: Non-interactive mode records assumptions
- **WHEN** a human or automation runs `sdlc agent openspec-propose <bead_id> --change-id <change-id> --no-interactive`
- **THEN** the system SHALL produce OpenSpec artifacts without prompting for answers
- **AND THEN** the generated proposal SHALL record any key assumptions the agent made due to missing context

### Requirement: OpenSpecRef creation in proposal state
The system SHALL create an OpenSpecRef JSON artifact under `openspec/refs/` in `proposal` state for agent-authored OpenSpec change proposals.

#### Scenario: Runner creates a proposal-state OpenSpecRef
- **WHEN** the OpenSpec proposal agent completes drafting a change
- **THEN** the system SHALL write `openspec/refs/<openspec_ref_id>.json`
- **AND THEN** the OpenSpecRef SHALL have `state == proposal` and `created_by.kind == agent`

### Requirement: Human-driven approval helper for OpenSpecRef
The system SHALL provide a human-invoked helper command to mark an OpenSpecRef approved, and the agent workflow MUST NOT auto-approve.

#### Scenario: Human approves an OpenSpecRef
- **WHEN** a human runs `sdlc openspec approve-ref <openspec_ref_id>`
- **THEN** the system SHALL require the current OpenSpecRef state is `proposal`
- **AND THEN** the system SHALL transition it to `approved` and set `approved_by.kind == human`

### Requirement: Optional council drafting mode
The system SHOULD support an optional council mode where multiple models draft independently and a synth step produces the final OpenSpec artifacts.

#### Scenario: Council mode synthesizes a single final change
- **WHEN** the OpenSpec proposal command runs with council mode enabled
- **THEN** the system SHALL produce exactly one final set of OpenSpec artifacts in `openspec/changes/<change-id>/`
