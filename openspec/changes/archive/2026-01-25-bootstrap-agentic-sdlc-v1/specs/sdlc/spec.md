## ADDED Requirements
### Requirement: SDLC CLI
The system SHALL provide an `sdlc` CLI with commands to validate artifacts, manage transitions, collect/validate evidence, generate grounding, and record approvals.

#### Scenario: CLI commands available
- **WHEN** a user invokes `uv run sdlc --help`
- **THEN** the CLI lists validate, request, evidence, grounding, and approve subcommands

### Requirement: Artifact validation
The system SHALL validate SDLC artifacts using Pydantic v2 models with `schema_version=1` and `extra=forbid`.

#### Scenario: Unknown fields rejected
- **WHEN** an artifact includes an unexpected field
- **THEN** validation fails with a schema error

### Requirement: Canonical hashing
The system SHALL compute SHA-256 hashes over canonical JSON with recursively sorted object keys and preserved array order.

#### Scenario: Deterministic hash
- **WHEN** the same logical JSON content is hashed multiple times
- **THEN** the resulting hash is identical

### Requirement: Transition enforcement
The system SHALL enforce a transition table and gate checks for bead status changes, recording all outcomes to an append-only execution journal.

#### Scenario: Rejected transition
- **WHEN** a transition request fails gate checks
- **THEN** an ExecutionRecord is appended with a non-zero exit code and notes describing missing preconditions

### Requirement: Evidence lifecycle
The system SHALL collect, validate, and invalidate evidence bundles and update EvidenceBundle.status only through the SDLC engine.

#### Scenario: Evidence validation
- **WHEN** evidence fails the validation rules
- **THEN** the bundle remains unvalidated and the result is recorded

### Requirement: Grounding bundle
The system SHALL generate a best-effort grounding bundle for a bead in `runs/<bead_id>/grounding.json`.

#### Scenario: Grounding generated
- **WHEN** grounding generation runs for a bead
- **THEN** the grounding file is written under the bead run directory

### Requirement: Approval recording
The system SHALL append approval decisions to `decision_ledger.jsonl` and link them to the target bead.

#### Scenario: Approval entry appended
- **WHEN** an approval is issued with a summary
- **THEN** a DecisionLedgerEntry is appended with decision_type=approval
