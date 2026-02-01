## ADDED Requirements

### Requirement: Atomic JSON artifacts
The system SHALL write JSON artifacts atomically so that readers never observe partially-written JSON content.

#### Scenario: Atomic write prevents truncated reads
- **WHEN** the system writes a JSON artifact consumed by the web UI or validation gates
- **AND WHEN** a reader attempts to read the artifact concurrently
- **THEN** the reader SHALL observe either the previous complete JSON document or the new complete JSON document
- **AND THEN** the reader SHALL NOT observe a truncated or partially-written JSON document

### Requirement: UI-safe errors are observable
The system SHALL remain resilient to malformed or transiently invalid artifacts in UI-facing reads, but SHALL record errors with enough context to debug.

#### Scenario: Server swallows exception but records context
- **WHEN** the server encounters an exception while reading/parsing a UI-facing artifact
- **THEN** the server SHALL NOT crash
- **AND THEN** the server SHALL record the exception (type/message) and relevant context (operation and path)

### Requirement: Formatting is enforced as a quality gate
The repository SHALL provide a quality gate that enforces deterministic formatting via `ruff format`.

#### Scenario: Format check rejects drift
- **WHEN** a developer or CI runs the project quality gates
- **THEN** `uv run ruff format --check .` SHALL pass

### Requirement: Transition phase mapping is centralized
The system SHALL define transition-to-phase mapping in a single shared implementation to prevent lifecycle drift between CLI, engine, and server.

#### Scenario: Server and engine use the same mapping
- **WHEN** the system journals an execution record for a transition request
- **THEN** the phase determination SHALL use the shared mapping implementation

