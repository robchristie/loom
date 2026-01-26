This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
docs/
  loom-specification.md
  pydantic-ai-llms.txt
  sdlc_quickstart.md
openspec/
  changes/
    archive/
      2026-01-25-bootstrap-agentic-sdlc-v1/
        specs/
          sdlc/
            spec.md
        proposal.md
        tasks.md
      2026-01-25-loom-boundary-and-discovery-enforcement-v1/
        specs/
          sdlc-boundary-enforcement/
            spec.md
        proposal.md
        tasks.md
      2026-01-25-loom-conformance-fixes-v1/
        specs/
          sdlc-conformance/
            spec.md
        proposal.md
        tasks.md
      2026-01-25-loom-link-ledger-entries-v1/
        specs/
          sdlc-decision-linking/
            spec.md
        proposal.md
        tasks.md
    loom-decision-journaling-and-abort-hardening-v1/
      proposal.md
      tasks.md
  AGENTS.md
  project.md
sdlc/
  boundary_registry.json
src/
  sdlc/
    __init__.py
    cli.py
    codec.py
    engine.py
    io.py
    models.py
tests/
  test_sdlc.py
.gitattributes
.gitignore
.python-version
.repomixignore
AGENTS.md
pyproject.toml
README.md
repomix.config.json
```

# Files

## File: .repomixignore
````
# Add patterns to ignore here, one per line
# Example:
# *.log
# tmp/
.beads
oopenspec/
````

## File: repomix.config.json
````json
{
  "$schema": "https://repomix.com/schemas/latest/schema.json",
  "input": {
    "maxFileSize": 52428800
  },
  "output": {
    "filePath": "repomix-loom.md",
    "style": "markdown",
    "parsableStyle": false,
    "fileSummary": true,
    "directoryStructure": true,
    "files": true,
    "removeComments": false,
    "removeEmptyLines": false,
    "compress": false,
    "topFilesLength": 5,
    "showLineNumbers": false,
    "truncateBase64": false,
    "copyToClipboard": false,
    "includeFullDirectoryStructure": false,
    "tokenCountTree": false,
    "git": {
      "sortByChanges": true,
      "sortByChangesMaxCommits": 100,
      "includeDiffs": false,
      "includeLogs": false,
      "includeLogsCount": 50
    }
  },
  "include": [],
  "ignore": {
    "useGitignore": true,
    "useDotIgnore": true,
    "useDefaultPatterns": true,
    "customPatterns": []
  },
  "security": {
    "enableSecurityCheck": true
  },
  "tokenCount": {
    "encoding": "o200k_base"
  }
}
````

## File: docs/pydantic-ai-llms.txt
````
# Pydantic AI

> GenAI Agent Framework, the Pydantic way

Pydantic AI is a Python agent framework designed to make it less painful to build production grade
applications with Generative AI.

## Introduction

- [Pydantic AI](https://ai.pydantic.dev/index.md)
- [Installation](https://ai.pydantic.dev/install/index.md)
- [Getting Help](https://ai.pydantic.dev/help/index.md)
- [Troubleshooting](https://ai.pydantic.dev/troubleshooting/index.md)

## Concepts documentation

- [Agent2Agent (A2A)](https://ai.pydantic.dev/a2a/index.md)
- [Agents](https://ai.pydantic.dev/agents/index.md)
- [Built-in Tools](https://ai.pydantic.dev/builtin-tools/index.md)
- [Dependencies](https://ai.pydantic.dev/dependencies/index.md)
- [Deferred Tools](https://ai.pydantic.dev/deferred-tools/index.md)
- [Direct Model Requests](https://ai.pydantic.dev/direct/index.md)
- [Embeddings](https://ai.pydantic.dev/embeddings/index.md)
- [Image, Audio, Video &amp; Document Input](https://ai.pydantic.dev/input/index.md)
- [Function Tools](https://ai.pydantic.dev/tools/index.md)
- [Common Tools](https://ai.pydantic.dev/common-tools/index.md)
- [Output](https://ai.pydantic.dev/output/index.md)
- [HTTP Request Retries](https://ai.pydantic.dev/retries/index.md)
- [Messages and chat history](https://ai.pydantic.dev/message-history/index.md)
- [Multi-Agent Patterns](https://ai.pydantic.dev/multi-agent-applications/index.md)
- [Thinking](https://ai.pydantic.dev/thinking/index.md)
- [Third-Party Tools](https://ai.pydantic.dev/third-party-tools/index.md)
- [Advanced Tool Features](https://ai.pydantic.dev/tools-advanced/index.md)
- [Toolsets](https://ai.pydantic.dev/toolsets/index.md)

## Models

- [Anthropic](https://ai.pydantic.dev/models/anthropic/index.md)
- [Bedrock](https://ai.pydantic.dev/models/bedrock/index.md)
- [Cerebras](https://ai.pydantic.dev/models/cerebras/index.md)
- [Cohere](https://ai.pydantic.dev/models/cohere/index.md)
- [Google](https://ai.pydantic.dev/models/google/index.md)
- [Groq](https://ai.pydantic.dev/models/groq/index.md)
- [Hugging Face](https://ai.pydantic.dev/models/huggingface/index.md)
- [Mistral](https://ai.pydantic.dev/models/mistral/index.md)
- [OpenAI](https://ai.pydantic.dev/models/openai/index.md)
- [OpenRouter](https://ai.pydantic.dev/models/openrouter/index.md)
- [Outlines](https://ai.pydantic.dev/models/outlines/index.md)
- [Overview](https://ai.pydantic.dev/models/overview/index.md)
- [xAI](https://ai.pydantic.dev/models/xai/index.md)

## Graphs

- [Overview](https://ai.pydantic.dev/graph/index.md)

## API Reference

- [pydantic_ai.ag_ui](https://ai.pydantic.dev/api/ag_ui/index.md)
- [pydantic_ai.agent](https://ai.pydantic.dev/api/agent/index.md)
- [pydantic_ai.builtin_tools](https://ai.pydantic.dev/api/builtin_tools/index.md)
- [pydantic_ai.common_tools](https://ai.pydantic.dev/api/common_tools/index.md)
- [pydantic_ai.direct](https://ai.pydantic.dev/api/direct/index.md)
- [pydantic_ai.durable_exec](https://ai.pydantic.dev/api/durable_exec/index.md)
- [pydantic_ai.embeddings](https://ai.pydantic.dev/api/embeddings/index.md)
- [pydantic_ai.exceptions](https://ai.pydantic.dev/api/exceptions/index.md)
- [pydantic_ai.ext](https://ai.pydantic.dev/api/ext/index.md)
- [fasta2a](https://ai.pydantic.dev/api/fasta2a/index.md)
- [pydantic_ai.format_prompt](https://ai.pydantic.dev/api/format_prompt/index.md)
- [pydantic_ai.mcp](https://ai.pydantic.dev/api/mcp/index.md)
- [pydantic_ai.messages](https://ai.pydantic.dev/api/messages/index.md)
- [pydantic_ai.output](https://ai.pydantic.dev/api/output/index.md)
- [pydantic_ai.profiles](https://ai.pydantic.dev/api/profiles/index.md)
- [pydantic_ai.providers](https://ai.pydantic.dev/api/providers/index.md)
- [pydantic_ai.result](https://ai.pydantic.dev/api/result/index.md)
- [pydantic_ai.retries](https://ai.pydantic.dev/api/retries/index.md)
- [pydantic_ai.run](https://ai.pydantic.dev/api/run/index.md)
- [pydantic_ai.settings](https://ai.pydantic.dev/api/settings/index.md)
- [pydantic_ai.tools](https://ai.pydantic.dev/api/tools/index.md)
- [pydantic_ai.toolsets](https://ai.pydantic.dev/api/toolsets/index.md)
- [pydantic_ai.usage](https://ai.pydantic.dev/api/usage/index.md)
- [pydantic_ai.models.anthropic](https://ai.pydantic.dev/api/models/anthropic/index.md)
- [pydantic_ai.models](https://ai.pydantic.dev/api/models/base/index.md)
- [pydantic_ai.models.bedrock](https://ai.pydantic.dev/api/models/bedrock/index.md)
- [pydantic_ai.models.cerebras](https://ai.pydantic.dev/api/models/cerebras/index.md)
- [pydantic_ai.models.cohere](https://ai.pydantic.dev/api/models/cohere/index.md)
- [pydantic_ai.models.fallback](https://ai.pydantic.dev/api/models/fallback/index.md)
- [pydantic_ai.models.function](https://ai.pydantic.dev/api/models/function/index.md)
- [pydantic_ai.models.google](https://ai.pydantic.dev/api/models/google/index.md)
- [pydantic_ai.models.groq](https://ai.pydantic.dev/api/models/groq/index.md)
- [pydantic_ai.models.huggingface](https://ai.pydantic.dev/api/models/huggingface/index.md)
- [pydantic_ai.models.instrumented](https://ai.pydantic.dev/api/models/instrumented/index.md)
- [pydantic_ai.models.mcp_sampling](https://ai.pydantic.dev/api/models/mcp-sampling/index.md)
- [pydantic_ai.models.mistral](https://ai.pydantic.dev/api/models/mistral/index.md)
- [pydantic_ai.models.openai](https://ai.pydantic.dev/api/models/openai/index.md)
- [pydantic_ai.models.openrouter](https://ai.pydantic.dev/api/models/openrouter/index.md)
- [pydantic_ai.models.outlines](https://ai.pydantic.dev/api/models/outlines/index.md)
- [pydantic_ai.models.test](https://ai.pydantic.dev/api/models/test/index.md)
- [pydantic_ai.models.wrapper](https://ai.pydantic.dev/api/models/wrapper/index.md)
- [pydantic_ai.models.xai](https://ai.pydantic.dev/api/models/xai/index.md)
- [pydantic_evals.dataset](https://ai.pydantic.dev/api/pydantic_evals/dataset/index.md)
- [pydantic_evals.evaluators](https://ai.pydantic.dev/api/pydantic_evals/evaluators/index.md)
- [pydantic_evals.generation](https://ai.pydantic.dev/api/pydantic_evals/generation/index.md)
- [pydantic_evals.otel](https://ai.pydantic.dev/api/pydantic_evals/otel/index.md)
- [pydantic_evals.reporting](https://ai.pydantic.dev/api/pydantic_evals/reporting/index.md)
- [pydantic_graph.beta](https://ai.pydantic.dev/api/pydantic_graph/beta/index.md)
- [pydantic_graph.beta.decision](https://ai.pydantic.dev/api/pydantic_graph/beta_decision/index.md)
- [pydantic_graph.beta.graph](https://ai.pydantic.dev/api/pydantic_graph/beta_graph/index.md)
- [pydantic_graph.beta.graph_builder](https://ai.pydantic.dev/api/pydantic_graph/beta_graph_builder/index.md)
- [pydantic_graph.beta.join](https://ai.pydantic.dev/api/pydantic_graph/beta_join/index.md)
- [pydantic_graph.beta.node](https://ai.pydantic.dev/api/pydantic_graph/beta_node/index.md)
- [pydantic_graph.beta.step](https://ai.pydantic.dev/api/pydantic_graph/beta_step/index.md)
- [pydantic_graph.exceptions](https://ai.pydantic.dev/api/pydantic_graph/exceptions/index.md)
- [pydantic_graph](https://ai.pydantic.dev/api/pydantic_graph/graph/index.md)
- [pydantic_graph.mermaid](https://ai.pydantic.dev/api/pydantic_graph/mermaid/index.md)
- [pydantic_graph.nodes](https://ai.pydantic.dev/api/pydantic_graph/nodes/index.md)
- [pydantic_graph.persistence](https://ai.pydantic.dev/api/pydantic_graph/persistence/index.md)
- [pydantic_ai.ui.ag_ui](https://ai.pydantic.dev/api/ui/ag_ui/index.md)
- [pydantic_ai.ui](https://ai.pydantic.dev/api/ui/base/index.md)
- [pydantic_ai.ui.vercel_ai](https://ai.pydantic.dev/api/ui/vercel_ai/index.md)

## Evals

- [Overview](https://ai.pydantic.dev/evals/index.md)

## Durable Execution

- [DBOS](https://ai.pydantic.dev/durable_execution/dbos/index.md)
- [Overview](https://ai.pydantic.dev/durable_execution/overview/index.md)
- [Prefect](https://ai.pydantic.dev/durable_execution/prefect/index.md)
- [Temporal](https://ai.pydantic.dev/durable_execution/temporal/index.md)

## MCP

- [Client](https://ai.pydantic.dev/mcp/client/index.md)
- [FastMCP Client](https://ai.pydantic.dev/mcp/fastmcp-client/index.md)
- [Overview](https://ai.pydantic.dev/mcp/overview/index.md)
- [Server](https://ai.pydantic.dev/mcp/server/index.md)

## UI Event Streams

- [AG-UI](https://ai.pydantic.dev/ui/ag-ui/index.md)
- [Overview](https://ai.pydantic.dev/ui/overview/index.md)
- [Vercel AI](https://ai.pydantic.dev/ui/vercel-ai/index.md)

## Optional

- [Testing](https://ai.pydantic.dev/testing/index.md)
- [Clai](https://ai.pydantic.dev/cli/index.md)
- [Debugging & Monitoring with Pydantic Logfire](https://ai.pydantic.dev/logfire/index.md)
- [Contributing](https://ai.pydantic.dev/contributing/index.md)
- [Upgrade Guide](https://ai.pydantic.dev/changelog/index.md)
- [Version policy](https://ai.pydantic.dev/version-policy/index.md)

## Examples

- [Agent User Interaction (AG-UI)](https://ai.pydantic.dev/examples/ag-ui/index.md)
- [Bank support](https://ai.pydantic.dev/examples/bank-support/index.md)
- [Chat App with FastAPI](https://ai.pydantic.dev/examples/chat-app/index.md)
- [Data Analyst](https://ai.pydantic.dev/examples/data-analyst/index.md)
- [Flight booking](https://ai.pydantic.dev/examples/flight-booking/index.md)
- [Pydantic Model](https://ai.pydantic.dev/examples/pydantic-model/index.md)
- [Question Graph](https://ai.pydantic.dev/examples/question-graph/index.md)
- [RAG](https://ai.pydantic.dev/examples/rag/index.md)
- [Setup](https://ai.pydantic.dev/examples/setup/index.md)
- [Slack Lead Qualifier with Modal](https://ai.pydantic.dev/examples/slack-lead-qualifier/index.md)
- [SQL Generation](https://ai.pydantic.dev/examples/sql-gen/index.md)
- [Stream markdown](https://ai.pydantic.dev/examples/stream-markdown/index.md)
- [Stream whales](https://ai.pydantic.dev/examples/stream-whales/index.md)
- [Weather agent](https://ai.pydantic.dev/examples/weather-agent/index.md)
````

## File: openspec/changes/archive/2026-01-25-bootstrap-agentic-sdlc-v1/specs/sdlc/spec.md
````markdown
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
````

## File: openspec/changes/archive/2026-01-25-bootstrap-agentic-sdlc-v1/proposal.md
````markdown
# Proposal: bootstrap-agentic-sdlc-v1

## Intent
Implement a minimal SDLC lifecycle engine ("sdlc") that enforces Agentic SDLC v1 semantics via:
- Pydantic v2 normative schemas
- artifact validation + schema export
- canonical hashing (SHA-256 over canonical JSON)
- append-only JSONL journals (ExecutionRecord, DecisionLedgerEntry)
- bead state transition enforcement (+ rejection recording)
- evidence validate + invalidate-if-stale
- grounding bundle generation (heuristic, best-effort)

This bootstrap targets solo usage and integrates with existing Beads (`bd`) and OpenSpec tooling.
Execution is "safe enough" via containerization and conservative defaults.

## Why
Prevent LLM-driven drift by separating intent, plan, implement, verify, approve through enforceable artifacts + gates.

## Assumptions (v1)
- The repo uses `uv` for Python tooling (`uv run`, `uv sync`).
- The container environment has `codex`, `bd`, and `openspec` on PATH.
- Beads may remain owned by `bd` (e.g. `issues.jsonl`), but the engine can optionally store bead artifacts in `runs/<bead_id>/bead.json` if configured.

## Scope (v1 bootstrap)
Included:
- Python package `sdlc/` with CLI entrypoint
- schema validation + JSON schema export
- transition engine + ExecutionRecord journaling
- evidence validation + staleness invalidation
- approval command (DecisionLedgerEntry)
- tests for core semantics

Excluded:
- hard sandbox mediation of repo access
- multi-agent orchestration
- UI
- replacing bd/OpenSpec tools

## Success Criteria
- `uv run sdlc validate <artifact>` validates artifacts strictly (extra=forbid).
- `uv run sdlc request <bead_id> <transition>` enforces transition table, emits ExecutionRecord for success/rejection, and updates Bead.status only through the engine.
- `uv run sdlc evidence validate <bead_id>` enforces Evidence Validation Rule and updates EvidenceBundle.status to validated only if rules pass.
- `uv run sdlc evidence invalidate-if-stale <bead_id>` invalidates evidence on git change signals.
- Journals are append-only JSONL and are never rewritten.
````

## File: openspec/changes/archive/2026-01-25-bootstrap-agentic-sdlc-v1/tasks.md
````markdown
# Tasks: bootstrap-agentic-sdlc-v1

- [x] 1. Add Python project skeleton for SDLC engine (uv)
  - [x] add `pyproject.toml` (or extend existing) with Pydantic v2 + Typer
  - [x] add `src/sdlc/` package and `sdlc` console entry
- [x] 2. Implement normative Pydantic v2 models for v1 artifacts (exactly as spec)
- [x] 3. Implement `sdlc schema export --out sdlc/schemas/` (JSON Schema export)
- [x] 4. Implement canonical JSON hashing (sorted keys, SHA-256)
- [x] 5. Implement `sdlc validate <path>` (strict validation; extra=forbid)
- [x] 6. Implement append-only journal writer:
  - [x] `runs/journal.jsonl` (ExecutionRecord)
  - [x] `decision_ledger.jsonl` (DecisionLedgerEntry)
- [x] 7. Implement transition engine:
  - [x] enforce transition table + gates
  - [x] success and rejection both emit ExecutionRecord
  - [x] enforce "Bead artifact_id == bead_id"
  - [x] enforce acceptance check freeze after ready
- [x] 8. Implement evidence commands:
  - [x] `sdlc evidence collect <bead_id>` (skeleton from acceptance checks)
  - [x] `sdlc evidence validate <bead_id>` (Evidence Validation Rule)
  - [x] `sdlc evidence invalidate-if-stale <bead_id>`
- [x] 9. Implement `sdlc grounding generate <bead_id>` (heuristic; best-effort)
- [x] 10. Implement `sdlc approve <bead_id> --summary ...` writes approval DecisionLedgerEntry
- [x] 11. Tests (pytest):
  - [x] schema validation
  - [x] hashing determinism
  - [x] illegal transition rejection recording fields
  - [x] manual_check constraints
  - [x] acceptance coverage rule
- [x] 12. Docs: `docs/sdlc_quickstart.md`
  - [x] commands using `uv run sdlc ...`
  - [x] example flow for one bead end-to-end
````

## File: openspec/changes/archive/2026-01-25-loom-boundary-and-discovery-enforcement-v1/specs/sdlc-boundary-enforcement/spec.md
````markdown
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
````

## File: openspec/changes/archive/2026-01-25-loom-boundary-and-discovery-enforcement-v1/proposal.md
````markdown
# OpenSpec Change: loom-boundary-and-discovery-enforcement-v1

## Summary
Add BoundaryRegistry-based enforcement and discovery-bead production-path protection to Loom MVP, per Agentic SDLC v1.

## Motivation
The current Loom engine enforces core lifecycle gating (spec, evidence, approval), but does not yet enforce:
- Boundary computation and policy limits (files/subsystems), required by the Boundary Computation Rule and Boundary Violation Handling.
- Discovery bead restrictions against modifying production paths, required by Discovery beads policy (normative default Policy A).

These are major workflow-safety features: they prevent “scope creep” and prevent discovery work from landing production changes.

## Scope
In scope:
1) Boundary computation:
- Determine which subsystems are touched by a bead’s changes using BoundaryRegistry.subsystems[].paths prefix matching.
- If bead.boundary_registry_ref is absent, use project default boundary registry.
- Record the BoundaryRegistry hash and selected subsystems in ExecutionRecord.notes_md and/or ExecutionRecord.links.

2) Boundary enforcement:
- Enforce project defaults:
  - max_files_touched (recommended default 8)
  - max_subsystems_touched (recommended default 2)
- If limits are exceeded mid-run, block further transitions toward verified and force bead to `aborted:needs-discovery`
  OR require an explicit split plan via BeadReview (minimal v1: force abort).
- Record the violation and computed metrics in an ExecutionRecord.

3) Discovery bead protection (Policy A):
- Define "production paths" as the union of all BoundaryRegistry subsystem path prefixes used for the bead.
- For BeadType.discovery:
  - Reject transitions that would advance work if modified files include any production paths.
  - Allow modifications only under an allowlist (project-configurable; default: docs/, notes/, tools/, experiments/, runs/).
- Record the active policy in ExecutionRecord.notes_md.

Out of scope:
- Hard sandboxing (Policy B workspace isolation).
- Full automatic bead splitting / generating new beads (only force abort and require human follow-up).
- Any schema_version changes.

## Acceptance Criteria
- `uv run pytest -q` passes.
- Boundary computation:
  - Given a boundary registry with subsystems and paths, and a mocked set of changed files, the engine computes touched subsystems correctly.
  - ExecutionRecord includes a link to the BoundaryRegistry hash used for evaluation.
- Boundary enforcement:
  - If changed files exceed max_files_touched or max_subsystems_touched, a verify-ward transition is blocked and the event is recorded.
  - Minimal v1 behavior: transition attempt returns not-ok with a clear reason; optional CLI command can force `aborted:needs-discovery`.
- Discovery protection:
  - A discovery bead attempting to proceed when production paths were modified is rejected and recorded.
  - A discovery bead modifying only allowlisted paths is permitted (subject to existing gates).
````

## File: openspec/changes/archive/2026-01-25-loom-boundary-and-discovery-enforcement-v1/tasks.md
````markdown
# Tasks: loom-boundary-and-discovery-enforcement-v1

## 0) Project defaults
- [x] Add a minimal project config (can be env vars at first):
  - [x] SDLC_MAX_FILES_TOUCHED (default 8)
  - [x] SDLC_MAX_SUBSYSTEMS_TOUCHED (default 2)
  - [x] SDLC_DISCOVERY_ALLOWLIST (default "docs/,notes/,tools/,experiments/,runs/")

## 1) Boundary registry loading
- Define default boundary registry location:
- [x] `sdlc/boundary_registry.json` (as hinted by the canonical dirs section)
- Implement:
  - [x] load_boundary_registry(paths, bead) -> BoundaryRegistry
    - [x] If bead.boundary_registry_ref exists: resolve it (minimal v1: only support local file ref by convention)
    - [x] Else: load sdlc/boundary_registry.json
  - [x] hash_boundary_registry(registry) -> HashRef

## 2) Change detection (minimal v1)
- Implement best-effort changed-files discovery:
  - [x] Prefer: `git diff --name-only HEAD` or `git diff --name-only <head_before>..HEAD`
  - [x] Fallback: empty list if git unavailable
- [x] NOTE: keep it simple; unit tests can monkeypatch the function that returns changed files.

## 3) Subsystem computation
- Given changed files, compute touched subsystems by prefix matching against BoundaryRegistry.subsystems[].paths.
- Produce:
  - [x] touched_subsystems: list[str]
  - [x] files_touched: int

## 4) Enforcement gates
- Enforce on transitions toward verification (at minimum: when requesting `verification_pending -> verified`):
  - [x] If files_touched > max_files_touched or len(touched_subsystems) > max_subsystems_touched:
    - [x] reject transition with message requiring abort/split
    - [x] write an ExecutionRecord describing metrics + policy thresholds
    - [x] (optional minimal helper) `sdlc abort <bead_id> --reason ...` that appends a DecisionLedgerEntry and requests the abort transition

## 5) Discovery bead Policy A gate
- For BeadType.discovery:
  - [x] Determine production paths = union of boundary registry subsystem prefixes
  - [x] If any changed file begins with any production path prefix:
    - [x] reject start/verify transitions
    - [x] record policy violation in ExecutionRecord
  - [x] If changed files are only inside allowlist prefixes:
    - [x] allow (subject to existing gates)

## 6) Linking BoundaryRegistry in ExecutionRecord.links
- When boundary evaluation occurs, add an ArtifactLink:
  - [x] artifact_type: "boundary_registry"
  - [x] artifact_id: registry.artifact_id
  - [x] schema_name: "sdlc.boundary_registry"
  - [x] schema_version: 1
- [x] Also record the boundary registry hash used (notes_md is fine if you don’t want new fields).

## 7) Tests
Add tests to cover:
- [x] subsystem computation from prefixes
- [x] enforcement triggers on too many files / too many subsystems
- [x] discovery policy rejects production path modifications
- [x] boundary registry link present in the generated ExecutionRecord

## 8) Docs (small)
Add a short section to docs/loom-specification.md describing:
- [x] default boundary registry location
- [x] how discovery allowlist works in v1 (Policy A)
````

## File: openspec/changes/archive/2026-01-25-loom-conformance-fixes-v1/specs/sdlc-conformance/spec.md
````markdown
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
````

## File: openspec/changes/archive/2026-01-25-loom-conformance-fixes-v1/proposal.md
````markdown
# OpenSpec Change: loom-conformance-fixes-v1

## Summary
Bring Loom MVP into closer conformance with Agentic SDLC v1 by:
- Aligning approval CLI behavior with the Approval Recording Rule (non-empty summary; prefix recommended, not required).
- Adding an OpenSpecRef sync command so spec gating is workable in normal flows.
- Making evidence invalidation correctly track repo changes after evidence validation (git ref recorded at validation time).
- Documenting canonical filenames for SDLC-managed bead artifacts used by the engine.

## Motivation
Current behavior has three sharp edges:
1) `sdlc approve` rejects approvals that are valid per spec.
2) `runs/<bead_id>/openspec_ref.json` is required by the engine but not conveniently produced.
3) Evidence invalidation is not anchored to the moment evidence becomes validated (no git ref captured on validation), so “code changed since evidence” is unreliable.

## Scope
In scope:
- CLI + engine/io changes needed to support:
  - Approval summary rule: non-empty required; `APPROVAL:` prefix warning only.
  - `sdlc openspec sync <bead_id>`: copies canonical OpenSpecRef to `runs/<bead_id>/openspec_ref.json`.
  - Evidence validate writes an ExecutionRecord that includes git ref + produced_artifacts referencing the evidence bundle path.
  - Evidence invalidation compares current git state to the git state recorded at evidence validation.
- Update `docs/loom-specification.md` to reflect canonical filenames for bead artifacts and the non-required approval prefix.

Out of scope:
- Full boundary registry enforcement, discovery policies, intervention counters, or container sandbox enforcement.
- Any changes to schema_version.

## Acceptance Criteria
- `uv run pytest -q` passes.
- Approvals:
  - `sdlc approve <bead_id> --summary "ok"` succeeds and appends a DecisionLedgerEntry with decision_type=approval.
  - If summary does not start with `APPROVAL:`, command prints a warning but still succeeds.
- OpenSpec sync:
  - `sdlc openspec sync <bead_id>` writes `runs/<bead_id>/openspec_ref.json` that validates as `sdlc.openspec_ref`.
- Evidence git anchoring:
  - `sdlc evidence validate <bead_id>` writes an ExecutionRecord containing a non-null `git.head_before` (when git is available) and includes `runs/<bead_id>/evidence.json` in produced_artifacts.
  - `sdlc evidence invalidate-if-stale <bead_id>` invalidates validated evidence when HEAD differs from the git ref recorded at validation time, and records an ExecutionRecord describing the staleness signal.
- Docs:
  - `docs/loom-specification.md` explicitly lists:
    - `runs/<bead_id>/bead_review.json` as BeadReview location
    - `runs/<bead_id>/bead.json` as Bead location (when Loom-managed)
    - Approval prefix as recommended (not required)

## Notes
This change intentionally keeps the MVP small and avoids adding new schema fields; git anchoring is recorded via ExecutionRecord.
````

## File: openspec/changes/archive/2026-01-25-loom-conformance-fixes-v1/tasks.md
````markdown
# Tasks: loom-conformance-fixes-v1

## 1) Approval CLI loosening
- Modify `sdlc approve`:
  - Require summary is non-empty.
  - If summary does not start with `APPROVAL:`, print a warning to stderr/stdout but do not fail.
  - Keep decision_type=approval, created_by.kind=human.

## 2) Canonical OpenSpecRef store + sync
- Define canonical store for OpenSpecRef artifacts:
  - `openspec/refs/<artifact_id>.json`
- Add `sdlc openspec sync <bead_id>`:
  - Load bead
  - Require bead.openspec_ref present
  - Read `openspec/refs/<bead.openspec_ref.artifact_id>.json`
  - Validate as OpenSpecRef
  - Write to `runs/<bead_id>/openspec_ref.json`
  - Optionally print path written

## 3) Evidence validate records git + produced_artifacts
- In `sdlc evidence validate`:
  - Write an ExecutionRecord that includes:
    - git.head_before + git.dirty_before (best effort)
    - produced_artifacts includes `runs/<bead_id>/evidence.json`
    - notes_md includes validation errors when present

## 4) Evidence invalidation compares against evidence-validation record
- Update `invalidate_evidence_if_stale`:
  - Find the most recent ExecutionRecord for the bead where:
    - phase == verify
    - produced_artifacts contains `runs/<bead_id>/evidence.json`
    - exit_code == 0 (validated)
  - Compare current git head/dirty to that record.git.head_before/dirty_before
  - If changed: invalidate evidence and record ExecutionRecord with explicit reason(s)

## 5) Tests
Add/extend tests to cover:
- approval summary without prefix succeeds (warns)
- openspec sync writes runs/<bead_id>/openspec_ref.json
- evidence validate writes execution record with produced_artifacts and git info (can be monkeypatched if needed)
- evidence invalidation triggers when git head changes relative to the validation record

## 6) Docs update
Update `docs/loom-specification.md` to include canonical bead/bead_review filenames and approval prefix guidance.
````

## File: openspec/changes/archive/2026-01-25-loom-link-ledger-entries-v1/specs/sdlc-decision-linking/spec.md
````markdown
## ADDED Requirements

### Requirement: Decision ledger linking
The lifecycle engine MUST link relevant DecisionLedgerEntry artifacts in ExecutionRecord links for exception-profile starts and approvals.

#### Scenario: Exception decision linked on start
- **WHEN** a bead with execution_profile exception transitions from `ready` to `in_progress`
- **THEN** the transition ExecutionRecord links the active exception DecisionLedgerEntry

#### Scenario: Approval decision linked on done
- **WHEN** a bead transitions from `approval_pending` to `done`
- **THEN** the transition ExecutionRecord links the approval DecisionLedgerEntry
````

## File: openspec/changes/archive/2026-01-25-loom-link-ledger-entries-v1/proposal.md
````markdown
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
````

## File: openspec/changes/archive/2026-01-25-loom-link-ledger-entries-v1/tasks.md
````markdown
# Tasks: loom-link-ledger-entries-v1

## 1) Decision lookup helpers
- [x] Add helper(s) in engine.py (or io.py) to find:
  - active exception decision for bead (decision_type=exception, bead_id match, not expired, summary non-empty)
  - approval decision for bead (decision_type=approval, bead_id match, created_by.kind=human, summary non-empty)

Return the chosen entry (prefer most recent by created_at if multiple exist).

## 2) Link decisions in ExecutionRecord
- [x] Extend record_transition_attempt(...) to accept extra_links: list[ArtifactLink]
- [x] When journaling a *successful* transition:
  - If transition == "ready -> in_progress" and bead.execution_profile == exception:
    - include link to the chosen exception decision entry
  - If transition == "approval_pending -> done":
    - include link to the chosen approval decision entry

Use ArtifactLink:
- artifact_type: "decision_ledger_entry"
- artifact_id: entry.artifact_id
- schema_name: "sdlc.decision_ledger_entry"
- schema_version: 1

## 3) Tests
- [x] Add tests that:
  - create bead + decision ledger entry + perform transition via CLI request()
  - assert last journal record contains the link
- [x] Include both positive and negative tests:
  - negative: exception bead with no exception entry -> start transition rejected and journal record has no applied_transition.

## 4) Docs (optional but recommended)
- [x] Add a short paragraph in docs/loom-specification.md describing that ExecutionRecord.links will include approval/exception decision links. (tracked in work-xi2)
````

## File: openspec/changes/loom-decision-journaling-and-abort-hardening-v1/proposal.md
````markdown
# OpenSpec Change: loom-decision-journaling-and-abort-hardening-v1

## Summary

Harden Loom’s abort and decision semantics to fully satisfy Agentic SDLC v1
audit and traceability guarantees by:

1. Explicitly journaling *decision actions* (not just transitions),
2. Making abort semantics unambiguous and consistent,
3. Ensuring abort decisions are recorded even when transitions fail or are terminal.

This change does **not** introduce new lifecycle states, artifacts, or policies.
It strictly improves correctness, auditability, and spec conformance.

---

## Motivation

The Loom spec makes a clear distinction between:

- **Decisions** (human or system intent, recorded in DecisionLedgerEntry), and
- **State transitions** (engine-authored lifecycle changes, recorded in ExecutionRecord).

Currently:
- Abort decisions are recorded in the decision ledger (good),
- Abort transitions are recorded in the execution journal (good),
- But the *decision action itself* is only implicitly visible via the transition record.

This makes audits harder and slightly weakens the “append-only causal trail”
guarantee the spec is aiming for.

Additionally, abort semantics need to be made fully explicit and consistent:
- Which `DecisionType` represents an abort?
- Is a decision recorded even if the abort transition cannot be applied?

This change resolves those ambiguities.

---

## Normative requirements

### R1 — Decision actions MUST be journaled

When the lifecycle engine creates a `DecisionLedgerEntry` as part of enforcing
a gate or policy (including aborts), it MUST also emit a corresponding
`ExecutionRecord` representing the *decision action itself*.

That ExecutionRecord MUST:

- Have `requested_transition == null`
- Have `applied_transition == null`
- Have `exit_code == 0`
- Link the created `DecisionLedgerEntry` via `ExecutionRecord.links`
- Use an appropriate `phase`:
  - `plan` if decision is made pre-execution,
  - `verify` if decision is made during verification or enforcement.

This record represents “a decision was made”, not “a transition occurred”.

---

### R2 — Abort decision type is canonical and fixed

All aborts to `aborted:needs-discovery` MUST be accompanied by a
`DecisionLedgerEntry` with:

- `decision_type == scope_change`
- `bead_id` set to the affected bead
- `summary` describing *why* the bead was aborted

This applies to:
- Explicit human aborts (`sdlc abort …`)
- Automatic engine-enforced aborts (anti-stall, boundary violation, etc.)

The spec MUST explicitly state that **abort == scope_change** in v1.

---

### R3 — Abort decisions MUST be recorded even if the transition cannot be applied

If an abort is requested or enforced, the engine MUST:

1. Create and append the `DecisionLedgerEntry`,
2. Emit a decision-action `ExecutionRecord` (per R1),
3. Attempt the lifecycle transition to `aborted:needs-discovery`,
4. Emit a transition-attempt `ExecutionRecord` (success or failure).

If the bead is already in a terminal state and the transition is rejected,
steps (1) and (2) MUST still occur.

---

### R4 — ExecutionRecord notes MUST explain engine-applied aborts

When the engine *automatically* aborts a bead (e.g. boundary violation,
anti-stall), the transition attempt ExecutionRecord MUST clearly state
in `notes_md` that:

- The abort was engine-applied, and
- Which rule triggered it (boundary violation, time limit, etc.).

---

## Out of scope

- Changing lifecycle states or adding new ones
- Introducing new DecisionType values
- Modifying BoundaryRegistry or anti-stall policy definitions
- Adding UI/UX affordances beyond journaling

---

## Acceptance criteria

- Every abort produces:
  - one DecisionLedgerEntry,
  - one decision-action ExecutionRecord,
  - one transition-attempt ExecutionRecord.
- Abort uses `decision_type == scope_change` consistently.
- Aborts are auditable even when transitions fail.
- `uv run pytest -q` passes with new coverage.
````

## File: openspec/changes/loom-decision-journaling-and-abort-hardening-v1/tasks.md
````markdown
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
````

## File: openspec/AGENTS.md
````markdown
# OpenSpec Instructions

Instructions for AI coding assistants using OpenSpec for spec-driven development.

## TL;DR Quick Checklist

- Search existing work: `openspec spec list --long`, `openspec list` (use `rg` only for full-text search)
- Decide scope: new capability vs modify existing capability
- Pick a unique `change-id`: kebab-case, verb-led (`add-`, `update-`, `remove-`, `refactor-`)
- Scaffold: `proposal.md`, `tasks.md`, `design.md` (only if needed), and delta specs per affected capability
- Write deltas: use `## ADDED|MODIFIED|REMOVED|RENAMED Requirements`; include at least one `#### Scenario:` per requirement
- Validate: `openspec validate [change-id] --strict --no-interactive` and fix issues
- Request approval: Do not start implementation until proposal is approved

## Three-Stage Workflow

### Stage 1: Creating Changes
Create proposal when you need to:
- Add features or functionality
- Make breaking changes (API, schema)
- Change architecture or patterns  
- Optimize performance (changes behavior)
- Update security patterns

Triggers (examples):
- "Help me create a change proposal"
- "Help me plan a change"
- "Help me create a proposal"
- "I want to create a spec proposal"
- "I want to create a spec"

Loose matching guidance:
- Contains one of: `proposal`, `change`, `spec`
- With one of: `create`, `plan`, `make`, `start`, `help`

Skip proposal for:
- Bug fixes (restore intended behavior)
- Typos, formatting, comments
- Dependency updates (non-breaking)
- Configuration changes
- Tests for existing behavior

**Workflow**
1. Review `openspec/project.md`, `openspec list`, and `openspec list --specs` to understand current context.
2. Choose a unique verb-led `change-id` and scaffold `proposal.md`, `tasks.md`, optional `design.md`, and spec deltas under `openspec/changes/<id>/`.
3. Draft spec deltas using `## ADDED|MODIFIED|REMOVED Requirements` with at least one `#### Scenario:` per requirement.
4. Run `openspec validate <id> --strict --no-interactive` and resolve any issues before sharing the proposal.

### Stage 2: Implementing Changes
Track these steps as TODOs and complete them one by one.
1. **Read proposal.md** - Understand what's being built
2. **Read design.md** (if exists) - Review technical decisions
3. **Read tasks.md** - Get implementation checklist
4. **Implement tasks sequentially** - Complete in order
5. **Confirm completion** - Ensure every item in `tasks.md` is finished before updating statuses
6. **Update checklist** - After all work is done, set every task to `- [x]` so the list reflects reality
7. **Approval gate** - Do not start implementation until the proposal is reviewed and approved

### Stage 3: Archiving Changes
After deployment, create separate PR to:
- Move `changes/[name]/` → `changes/archive/YYYY-MM-DD-[name]/`
- Update `specs/` if capabilities changed
- Use `openspec archive <change-id> --skip-specs --yes` for tooling-only changes (always pass the change ID explicitly)
- Run `openspec validate --strict --no-interactive` to confirm the archived change passes checks

## Before Any Task

**Context Checklist:**
- [ ] Read relevant specs in `specs/[capability]/spec.md`
- [ ] Check pending changes in `changes/` for conflicts
- [ ] Read `openspec/project.md` for conventions
- [ ] Run `openspec list` to see active changes
- [ ] Run `openspec list --specs` to see existing capabilities

**Before Creating Specs:**
- Always check if capability already exists
- Prefer modifying existing specs over creating duplicates
- Use `openspec show [spec]` to review current state
- If request is ambiguous, ask 1–2 clarifying questions before scaffolding

### Search Guidance
- Enumerate specs: `openspec spec list --long` (or `--json` for scripts)
- Enumerate changes: `openspec list` (or `openspec change list --json` - deprecated but available)
- Show details:
  - Spec: `openspec show <spec-id> --type spec` (use `--json` for filters)
  - Change: `openspec show <change-id> --json --deltas-only`
- Full-text search (use ripgrep): `rg -n "Requirement:|Scenario:" openspec/specs`

## Quick Start

### CLI Commands

```bash
# Essential commands
openspec list                  # List active changes
openspec list --specs          # List specifications
openspec show [item]           # Display change or spec
openspec validate [item]       # Validate changes or specs
openspec archive <change-id> [--yes|-y]   # Archive after deployment (add --yes for non-interactive runs)

# Project management
openspec init [path]           # Initialize OpenSpec
openspec update [path]         # Update instruction files

# Interactive mode
openspec show                  # Prompts for selection
openspec validate              # Bulk validation mode

# Debugging
openspec show [change] --json --deltas-only
openspec validate [change] --strict --no-interactive
```

### Command Flags

- `--json` - Machine-readable output
- `--type change|spec` - Disambiguate items
- `--strict` - Comprehensive validation
- `--no-interactive` - Disable prompts
- `--skip-specs` - Archive without spec updates
- `--yes`/`-y` - Skip confirmation prompts (non-interactive archive)

## Directory Structure

```
openspec/
├── project.md              # Project conventions
├── specs/                  # Current truth - what IS built
│   └── [capability]/       # Single focused capability
│       ├── spec.md         # Requirements and scenarios
│       └── design.md       # Technical patterns
├── changes/                # Proposals - what SHOULD change
│   ├── [change-name]/
│   │   ├── proposal.md     # Why, what, impact
│   │   ├── tasks.md        # Implementation checklist
│   │   ├── design.md       # Technical decisions (optional; see criteria)
│   │   └── specs/          # Delta changes
│   │       └── [capability]/
│   │           └── spec.md # ADDED/MODIFIED/REMOVED
│   └── archive/            # Completed changes
```

## Creating Change Proposals

### Decision Tree

```
New request?
├─ Bug fix restoring spec behavior? → Fix directly
├─ Typo/format/comment? → Fix directly  
├─ New feature/capability? → Create proposal
├─ Breaking change? → Create proposal
├─ Architecture change? → Create proposal
└─ Unclear? → Create proposal (safer)
```

### Proposal Structure

1. **Create directory:** `changes/[change-id]/` (kebab-case, verb-led, unique)

2. **Write proposal.md:**
```markdown
# Change: [Brief description of change]

## Why
[1-2 sentences on problem/opportunity]

## What Changes
- [Bullet list of changes]
- [Mark breaking changes with **BREAKING**]

## Impact
- Affected specs: [list capabilities]
- Affected code: [key files/systems]
```

3. **Create spec deltas:** `specs/[capability]/spec.md`
```markdown
## ADDED Requirements
### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result

## MODIFIED Requirements
### Requirement: Existing Feature
[Complete modified requirement]

## REMOVED Requirements
### Requirement: Old Feature
**Reason**: [Why removing]
**Migration**: [How to handle]
```
If multiple capabilities are affected, create multiple delta files under `changes/[change-id]/specs/<capability>/spec.md`—one per capability.

4. **Create tasks.md:**
```markdown
## 1. Implementation
- [ ] 1.1 Create database schema
- [ ] 1.2 Implement API endpoint
- [ ] 1.3 Add frontend component
- [ ] 1.4 Write tests
```

5. **Create design.md when needed:**
Create `design.md` if any of the following apply; otherwise omit it:
- Cross-cutting change (multiple services/modules) or a new architectural pattern
- New external dependency or significant data model changes
- Security, performance, or migration complexity
- Ambiguity that benefits from technical decisions before coding

Minimal `design.md` skeleton:
```markdown
## Context
[Background, constraints, stakeholders]

## Goals / Non-Goals
- Goals: [...]
- Non-Goals: [...]

## Decisions
- Decision: [What and why]
- Alternatives considered: [Options + rationale]

## Risks / Trade-offs
- [Risk] → Mitigation

## Migration Plan
[Steps, rollback]

## Open Questions
- [...]
```

## Spec File Format

### Critical: Scenario Formatting

**CORRECT** (use #### headers):
```markdown
#### Scenario: User login success
- **WHEN** valid credentials provided
- **THEN** return JWT token
```

**WRONG** (don't use bullets or bold):
```markdown
- **Scenario: User login**  ❌
**Scenario**: User login     ❌
### Scenario: User login      ❌
```

Every requirement MUST have at least one scenario.

### Requirement Wording
- Use SHALL/MUST for normative requirements (avoid should/may unless intentionally non-normative)

### Delta Operations

- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

Headers matched with `trim(header)` - whitespace ignored.

#### When to use ADDED vs MODIFIED
- ADDED: Introduces a new capability or sub-capability that can stand alone as a requirement. Prefer ADDED when the change is orthogonal (e.g., adding "Slash Command Configuration") rather than altering the semantics of an existing requirement.
- MODIFIED: Changes the behavior, scope, or acceptance criteria of an existing requirement. Always paste the full, updated requirement content (header + all scenarios). The archiver will replace the entire requirement with what you provide here; partial deltas will drop previous details.
- RENAMED: Use when only the name changes. If you also change behavior, use RENAMED (name) plus MODIFIED (content) referencing the new name.

Common pitfall: Using MODIFIED to add a new concern without including the previous text. This causes loss of detail at archive time. If you aren’t explicitly changing the existing requirement, add a new requirement under ADDED instead.

Authoring a MODIFIED requirement correctly:
1) Locate the existing requirement in `openspec/specs/<capability>/spec.md`.
2) Copy the entire requirement block (from `### Requirement: ...` through its scenarios).
3) Paste it under `## MODIFIED Requirements` and edit to reflect the new behavior.
4) Ensure the header text matches exactly (whitespace-insensitive) and keep at least one `#### Scenario:`.

Example for RENAMED:
```markdown
## RENAMED Requirements
- FROM: `### Requirement: Login`
- TO: `### Requirement: User Authentication`
```

## Troubleshooting

### Common Errors

**"Change must have at least one delta"**
- Check `changes/[name]/specs/` exists with .md files
- Verify files have operation prefixes (## ADDED Requirements)

**"Requirement must have at least one scenario"**
- Check scenarios use `#### Scenario:` format (4 hashtags)
- Don't use bullet points or bold for scenario headers

**Silent scenario parsing failures**
- Exact format required: `#### Scenario: Name`
- Debug with: `openspec show [change] --json --deltas-only`

### Validation Tips

```bash
# Always use strict mode for comprehensive checks
openspec validate [change] --strict --no-interactive

# Debug delta parsing
openspec show [change] --json | jq '.deltas'

# Check specific requirement
openspec show [spec] --json -r 1
```

## Happy Path Script

```bash
# 1) Explore current state
openspec spec list --long
openspec list
# Optional full-text search:
# rg -n "Requirement:|Scenario:" openspec/specs
# rg -n "^#|Requirement:" openspec/changes

# 2) Choose change id and scaffold
CHANGE=add-two-factor-auth
mkdir -p openspec/changes/$CHANGE/{specs/auth}
printf "## Why\n...\n\n## What Changes\n- ...\n\n## Impact\n- ...\n" > openspec/changes/$CHANGE/proposal.md
printf "## 1. Implementation\n- [ ] 1.1 ...\n" > openspec/changes/$CHANGE/tasks.md

# 3) Add deltas (example)
cat > openspec/changes/$CHANGE/specs/auth/spec.md << 'EOF'
## ADDED Requirements
### Requirement: Two-Factor Authentication
Users MUST provide a second factor during login.

#### Scenario: OTP required
- **WHEN** valid credentials are provided
- **THEN** an OTP challenge is required
EOF

# 4) Validate
openspec validate $CHANGE --strict --no-interactive
```

## Multi-Capability Example

```
openspec/changes/add-2fa-notify/
├── proposal.md
├── tasks.md
└── specs/
    ├── auth/
    │   └── spec.md   # ADDED: Two-Factor Authentication
    └── notifications/
        └── spec.md   # ADDED: OTP email notification
```

auth/spec.md
```markdown
## ADDED Requirements
### Requirement: Two-Factor Authentication
...
```

notifications/spec.md
```markdown
## ADDED Requirements
### Requirement: OTP Email Notification
...
```

## Best Practices

### Simplicity First
- Default to <100 lines of new code
- Single-file implementations until proven insufficient
- Avoid frameworks without clear justification
- Choose boring, proven patterns

### Complexity Triggers
Only add complexity with:
- Performance data showing current solution too slow
- Concrete scale requirements (>1000 users, >100MB data)
- Multiple proven use cases requiring abstraction

### Clear References
- Use `file.ts:42` format for code locations
- Reference specs as `specs/auth/spec.md`
- Link related changes and PRs

### Capability Naming
- Use verb-noun: `user-auth`, `payment-capture`
- Single purpose per capability
- 10-minute understandability rule
- Split if description needs "AND"

### Change ID Naming
- Use kebab-case, short and descriptive: `add-two-factor-auth`
- Prefer verb-led prefixes: `add-`, `update-`, `remove-`, `refactor-`
- Ensure uniqueness; if taken, append `-2`, `-3`, etc.

## Tool Selection Guide

| Task | Tool | Why |
|------|------|-----|
| Find files by pattern | Glob | Fast pattern matching |
| Search code content | Grep | Optimized regex search |
| Read specific files | Read | Direct file access |
| Explore unknown scope | Task | Multi-step investigation |

## Error Recovery

### Change Conflicts
1. Run `openspec list` to see active changes
2. Check for overlapping specs
3. Coordinate with change owners
4. Consider combining proposals

### Validation Failures
1. Run with `--strict` flag
2. Check JSON output for details
3. Verify spec file format
4. Ensure scenarios properly formatted

### Missing Context
1. Read project.md first
2. Check related specs
3. Review recent archives
4. Ask for clarification

## Quick Reference

### Stage Indicators
- `changes/` - Proposed, not yet built
- `specs/` - Built and deployed
- `archive/` - Completed changes

### File Purposes
- `proposal.md` - Why and what
- `tasks.md` - Implementation steps
- `design.md` - Technical decisions
- `spec.md` - Requirements and behavior

### CLI Essentials
```bash
openspec list              # What's in progress?
openspec show [item]       # View details
openspec validate --strict --no-interactive  # Is it correct?
openspec archive <change-id> [--yes|-y]  # Mark complete (add --yes for automation)
```

Remember: Specs are truth. Changes are proposals. Keep them in sync.
````

## File: openspec/project.md
````markdown
# Project Context

## Purpose
[Describe your project's purpose and goals]

## Tech Stack
- [List your primary technologies]
- [e.g., TypeScript, React, Node.js]

## Project Conventions

### Code Style
[Describe your code style preferences, formatting rules, and naming conventions]

### Architecture Patterns
[Document your architectural decisions and patterns]

### Testing Strategy
[Explain your testing approach and requirements]

### Git Workflow
[Describe your branching strategy and commit conventions]

## Domain Context
[Add domain-specific knowledge that AI assistants need to understand]

## Important Constraints
[List any technical, business, or regulatory constraints]

## External Dependencies
[Document key external services, APIs, or systems]
````

## File: sdlc/boundary_registry.json
````json
{
  "schema_name": "sdlc.boundary_registry",
  "schema_version": 1,
  "artifact_id": "boundary-registry-default",
  "created_at": "2026-01-01T00:00:00Z",
  "created_by": {
    "kind": "system",
    "name": "loom-bootstrap"
  },
  "registry_name": "loom-default-boundaries",
  "subsystems": [
    {
      "name": "engine-core",
      "paths": [
        "src/sdlc/engine.py",
        "src/sdlc/io.py",
        "src/sdlc/codec.py"
      ],
      "invariants": [
        "Lifecycle transitions are engine-authored only",
        "ExecutionRecord and DecisionLedgerEntry are append-only",
        "Acceptance checks are frozen after ready"
      ]
    },
    {
      "name": "models-schema",
      "paths": [
        "src/sdlc/models.py"
      ],
      "invariants": [
        "Schema version is monotonic",
        "extra=forbid enforced on all models",
        "ArtifactId and BeadId constraints are preserved"
      ]
    },
    {
      "name": "cli-interface",
      "paths": [
        "src/sdlc/cli.py"
      ],
      "invariants": [
        "CLI must not mutate Bead.status directly",
        "All lifecycle changes go through engine"
      ]
    },
    {
      "name": "tests",
      "paths": [
        "tests/"
      ],
      "invariants": [
        "Tests may not modify production code at runtime",
        "Tests must assert journal behavior for failures"
      ]
    },
    {
      "name": "documentation",
      "paths": [
        "docs/",
        "README.md"
      ],
      "invariants": [
        "Docs changes do not alter runtime behavior"
      ]
    },
    {
      "name": "openspec",
      "paths": [
        "openspec/"
      ],
      "invariants": [
        "Approved OpenSpecRef required for implementation beads",
        "OpenSpecRef state transitions are human-authored"
      ]
    }
  ],
  "notes": "Default boundary registry for Loom MVP. Used for subsystem counting, discovery bead protection, and boundary enforcement."
}
````

## File: src/sdlc/__init__.py
````python
"""SDLC lifecycle engine."""

__all__ = ["__version__"]

__version__ = "0.1.0"
````

## File: src/sdlc/codec.py
````python
from __future__ import annotations

import json
from hashlib import sha256
from typing import Any


def canonicalize_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonicalize_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonicalize_json(item) for item in value]
    return value


def canonical_json_bytes(value: Any) -> bytes:
    canonical = canonicalize_json(value)
    return json.dumps(canonical, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_canonical_json(value: Any) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()
````

## File: src/sdlc/io.py
````python
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import subprocess

from pydantic import BaseModel

from .models import (
    Bead,
    BeadReview,
    DecisionLedgerEntry,
    EvidenceBundle,
    ExecutionRecord,
    GroundingBundle,
    OpenSpecRef,
)


@dataclass(frozen=True)
class Paths:
    repo_root: Path

    @property
    def runs_dir(self) -> Path:
        return self.repo_root / "runs"

    @property
    def journal_path(self) -> Path:
        return self.runs_dir / "journal.jsonl"

    @property
    def decision_ledger_path(self) -> Path:
        return self.repo_root / "decision_ledger.jsonl"

    def bead_dir(self, bead_id: str) -> Path:
        return self.runs_dir / bead_id

    def bead_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "bead.json"

    def grounding_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "grounding.json"

    def evidence_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "evidence.json"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n")


def load_bead(paths: Paths, bead_id: str) -> Bead:
    bead_path = paths.bead_path(bead_id)
    if bead_path.exists():
        return Bead.model_validate_json(bead_path.read_text(encoding="utf-8"))
    return _load_bead_from_bd(paths, bead_id)


def _load_bead_from_bd(paths: Paths, bead_id: str) -> Bead:
    issues_path = paths.repo_root / "beads" / "issues.jsonl"
    if not issues_path.exists():
        issues_path = paths.repo_root / "beads" / "issues.json"
    if not issues_path.exists():
        issues_path = paths.repo_root / ".beads" / "issues.jsonl"
    if not issues_path.exists():
        raise FileNotFoundError("No bead artifact or bd issues store found")

    bead_data: Optional[dict[str, Any]] = None
    with issues_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            data = json.loads(line)
            if data.get("id") == bead_id:
                bead_data = data
                break

    if bead_data is None:
        raise FileNotFoundError(f"Bead {bead_id} not found in bd store")

    created_at = bead_data.get("created_at") or bead_data.get("created")
    if created_at is None:
        created_at = now_utc().isoformat()

    acceptance = bead_data.get("acceptance") or bead_data.get("acceptance_criteria") or ""
    description = bead_data.get("description") or bead_data.get("body") or ""
    title = bead_data.get("title") or bead_id
    status = bead_data.get("status") or "draft"

    owner = bead_data.get("owner") or bead_data.get("assignee")
    priority = bead_data.get("priority")
    if isinstance(priority, str) and priority.upper().startswith("P"):
        try:
            priority = int(priority[1:]) + 1
        except ValueError:
            priority = 3
    if isinstance(priority, int):
        priority = max(1, min(5, priority))
    else:
        priority = 3

    bead_payload = {
        "schema_name": "sdlc.bead",
        "schema_version": 1,
        "artifact_id": bead_id,
        "created_at": created_at,
        "created_by": {
            "kind": "system",
            "name": "bd",
        },
        "bead_id": bead_id,
        "title": title,
        "bead_type": bead_data.get("bead_type", "implementation"),
        "status": status,
        "priority": priority,
        "owner": owner,
        "requirements_md": description,
        "acceptance_criteria_md": acceptance,
        "context_md": bead_data.get("notes") or bead_data.get("context") or "",
        "acceptance_checks": [],
    }

    return Bead.model_validate(bead_payload)


def load_bead_review(paths: Paths, bead_id: str) -> Optional[BeadReview]:
    review_path = paths.bead_dir(bead_id) / "bead_review.json"
    if not review_path.exists():
        return None
    return BeadReview.model_validate_json(review_path.read_text(encoding="utf-8"))


def load_grounding(paths: Paths, bead_id: str) -> Optional[GroundingBundle]:
    path = paths.grounding_path(bead_id)
    if not path.exists():
        return None
    return GroundingBundle.model_validate_json(path.read_text(encoding="utf-8"))


def load_evidence(paths: Paths, bead_id: str) -> Optional[EvidenceBundle]:
    path = paths.evidence_path(bead_id)
    if not path.exists():
        return None
    return EvidenceBundle.model_validate_json(path.read_text(encoding="utf-8"))


def write_model(path: Path, model: BaseModel) -> None:
    dump_json(path, model.model_dump(mode="json"))


def write_execution_record(paths: Paths, record: ExecutionRecord) -> None:
    append_jsonl(paths.journal_path, record.model_dump(mode="json"))


def write_decision_entry(paths: Paths, entry: DecisionLedgerEntry) -> None:
    append_jsonl(paths.decision_ledger_path, entry.model_dump(mode="json"))


def load_decision_ledger(paths: Paths) -> Iterable[DecisionLedgerEntry]:
    if not paths.decision_ledger_path.exists():
        return []
    entries: list[DecisionLedgerEntry] = []
    with paths.decision_ledger_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            entries.append(DecisionLedgerEntry.model_validate_json(line))
    return entries


def load_execution_records(paths: Paths) -> list[ExecutionRecord]:
    if not paths.journal_path.exists():
        return []
    records: list[ExecutionRecord] = []
    with paths.journal_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records.append(ExecutionRecord.model_validate_json(line))
    return records


def git_head(paths: Paths) -> Optional[str]:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=paths.repo_root)
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        return None


def git_is_dirty(paths: Paths) -> Optional[bool]:
    try:
        output = subprocess.check_output(["git", "status", "--porcelain"], cwd=paths.repo_root)
    except subprocess.CalledProcessError:
        return None
    return bool(output.strip())
````

## File: src/sdlc/models.py
````python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing_extensions import Annotated

ISO8601 = datetime

Sha256Hex = Annotated[
    str,
    StringConstraints(pattern=r"^[a-f0-9]{64}$", strip_whitespace=True),
]

ArtifactId = Annotated[
    str,
    StringConstraints(min_length=6, max_length=128, strip_whitespace=True),
]

BeadId = Annotated[
    str,
    StringConstraints(pattern=r"^work-[a-z0-9]+(\.[a-z0-9]+)?$", strip_whitespace=True),
]


class SDLCBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HashRef(SDLCBase):
    hash_alg: Literal["sha256"] = "sha256"
    hash: Sha256Hex


class FileRef(SDLCBase):
    path: str = Field(..., description="Repo-relative path")
    content_hash: Optional[HashRef] = None


class ArtifactLink(SDLCBase):
    artifact_type: str
    artifact_id: ArtifactId
    schema_name: Optional[str] = None
    schema_version: Optional[int] = None


class Actor(SDLCBase):
    kind: Literal["human", "agent", "system"]
    name: str
    email: Optional[str] = None


class SchemaBase(SDLCBase):
    schema_name: str
    schema_version: int
    artifact_id: ArtifactId
    created_at: ISO8601
    created_by: Actor
    links: List[ArtifactLink] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


class OpenSpecState(str, Enum):
    proposal = "proposal"
    approved = "approved"
    superseded = "superseded"


class OpenSpecRef(SchemaBase):
    schema_name: Literal["sdlc.openspec_ref"] = "sdlc.openspec_ref"
    schema_version: Literal[1] = 1

    change_id: str
    state: OpenSpecState
    path: str
    approved_at: Optional[ISO8601] = None
    approved_by: Optional[Actor] = None
    content_hash: Optional[HashRef] = None


class Subsystem(SDLCBase):
    name: str
    paths: List[str]
    invariants: List[str] = Field(default_factory=list)


class BoundaryRegistry(SchemaBase):
    schema_name: Literal["sdlc.boundary_registry"] = "sdlc.boundary_registry"
    schema_version: Literal[1] = 1

    registry_name: str
    subsystems: List[Subsystem]
    notes: Optional[str] = None


class BeadType(str, Enum):
    implementation = "implementation"
    discovery = "discovery"


class BeadStatus(str, Enum):
    draft = "draft"
    sized = "sized"
    ready = "ready"
    in_progress = "in_progress"
    verification_pending = "verification_pending"
    verified = "verified"
    approval_pending = "approval_pending"
    done = "done"
    blocked = "blocked"
    aborted_needs_discovery = "aborted:needs-discovery"
    failed = "failed"
    superseded = "superseded"


class ExecutionProfile(str, Enum):
    sandbox = "sandbox"
    ci_like = "ci-like"
    exception = "exception"


class AcceptanceCheck(SDLCBase):
    name: str
    command: str
    cwd: Optional[str] = None
    timeout_seconds: Optional[int] = None
    expect_exit_code: int = 0
    expected_outputs: List[FileRef] = Field(default_factory=list)


class Bead(SchemaBase):
    schema_name: Literal["sdlc.bead"] = "sdlc.bead"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    title: str
    bead_type: BeadType
    status: BeadStatus

    priority: int = Field(3, ge=1, le=5)
    owner: Optional[str] = None

    openspec_ref: Optional[ArtifactLink] = None

    boundary_registry_ref: Optional[ArtifactLink] = None

    requirements_md: str
    acceptance_criteria_md: str
    context_md: str

    acceptance_checks: List[AcceptanceCheck] = Field(default_factory=list)

    execution_profile: ExecutionProfile = ExecutionProfile.sandbox
    depends_on: List[BeadId] = Field(default_factory=list)

    max_elapsed_minutes: Optional[int] = None
    max_interventions: Optional[int] = None


class EffortBucket(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class RiskFlag(str, Enum):
    unknowns = "unknowns"
    dependency_hazard = "dependency_hazard"
    unclear_acceptance = "unclear_acceptance"
    cross_boundary_change = "cross_boundary_change"
    design_decision_missing = "design_decision_missing"
    too_many_files = "too_many_files"
    too_many_subsystems = "too_many_subsystems"
    multiple_primary_concerns = "multiple_primary_concerns"


class ProposedBeadDraft(SDLCBase):
    title: str
    bead_type: BeadType
    requirements_md: str
    acceptance_criteria_md: str
    context_md: str
    depends_on: List[str] = Field(default_factory=list)


class SplitProposal(SDLCBase):
    proposed_beads: List[ProposedBeadDraft]
    rationale: str


class BeadReview(SchemaBase):
    schema_name: Literal["sdlc.bead_review"] = "sdlc.bead_review"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    reviewed_bead_hash: Optional[HashRef] = None

    effort_bucket: EffortBucket
    risk_flags: List[RiskFlag] = Field(default_factory=list)

    estimated_files_touched: Optional[int] = None
    estimated_subsystems_touched: Optional[List[str]] = None

    tightened_acceptance_checks: List[AcceptanceCheck] = Field(default_factory=list)

    split_required: bool = False
    split_proposal: Optional[SplitProposal] = None

    notes: Optional[str] = None


class GroundingItem(SDLCBase):
    kind: Literal["file", "api", "pattern", "command", "note"]
    title: str
    content_md: str
    file_ref: Optional[FileRef] = None


class GroundingBundle(SchemaBase):
    schema_name: Literal["sdlc.grounding_bundle"] = "sdlc.grounding_bundle"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    generated_for_bead_hash: Optional[HashRef] = None

    items: List[GroundingItem] = Field(default_factory=list)

    allowed_commands: List[str] = Field(default_factory=list)
    disallowed_commands: List[str] = Field(default_factory=list)
    excluded_paths: List[str] = Field(default_factory=list)

    summary_md: Optional[str] = None


class EvidenceType(str, Enum):
    test_run = "test_run"
    lint = "lint"
    typecheck = "typecheck"
    benchmark = "benchmark"
    golden_compare = "golden_compare"
    manual_check = "manual_check"
    ci_run = "ci_run"


class EvidenceStatus(str, Enum):
    collected = "collected"
    validated = "validated"
    invalidated = "invalidated"


class EvidenceItem(SDLCBase):
    name: str
    evidence_type: EvidenceType
    command: Optional[str] = None
    exit_code: Optional[int] = None
    started_at: Optional[ISO8601] = None
    finished_at: Optional[ISO8601] = None
    attachments: List[FileRef] = Field(default_factory=list)
    summary_md: Optional[str] = None


class EvidenceBundle(SchemaBase):
    schema_name: Literal["sdlc.evidence_bundle"] = "sdlc.evidence_bundle"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    for_bead_hash: Optional[HashRef] = None
    status: EvidenceStatus = EvidenceStatus.collected
    items: List[EvidenceItem]
    invalidated_reason: Optional[str] = None


class RunPhase(str, Enum):
    plan = "plan"
    implement = "implement"
    verify = "verify"


class GitRef(SDLCBase):
    head_before: Optional[str] = None
    head_after: Optional[str] = None
    dirty_before: Optional[bool] = None
    dirty_after: Optional[bool] = None


class ExecutionRecord(SchemaBase):
    schema_name: Literal["sdlc.execution_record"] = "sdlc.execution_record"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    phase: RunPhase

    engine_version: Optional[str] = None
    policy_version: Optional[str] = None

    container_image: Optional[str] = None
    container_digest: Optional[str] = None
    commands: List[str] = Field(default_factory=list)
    exit_code: Optional[int] = None
    produced_artifacts: List[FileRef] = Field(default_factory=list)
    git: Optional[GitRef] = None
    notes_md: Optional[str] = None
    requested_transition: Optional[str] = None
    applied_transition: Optional[str] = None


class DecisionType(str, Enum):
    approval = "approval"
    assumption = "assumption"
    tradeoff = "tradeoff"
    exception = "exception"
    scope_change = "scope_change"


class DecisionLedgerEntry(SchemaBase):
    schema_name: Literal["sdlc.decision_ledger_entry"] = "sdlc.decision_ledger_entry"
    schema_version: Literal[1] = 1

    bead_id: Optional[BeadId] = None
    decision_type: DecisionType
    summary: str
    rationale_md: Optional[str] = None
    expires_at: Optional[ISO8601] = None
    waived_acceptance_checks: List[str] = Field(default_factory=list)


SCHEMA_MODELS = [
    OpenSpecRef,
    BoundaryRegistry,
    Bead,
    BeadReview,
    GroundingBundle,
    EvidenceBundle,
    ExecutionRecord,
    DecisionLedgerEntry,
]


def schema_registry() -> dict[str, type[SchemaBase]]:
    registry: dict[str, type[SchemaBase]] = {}
    for cls in SCHEMA_MODELS:
        default = cls.model_fields["schema_name"].default
        if isinstance(default, str):
            registry[default] = cls
    return registry
````

## File: .gitattributes
````
# Use bd merge for beads JSONL files
.beads/issues.jsonl merge=beads
````

## File: .python-version
````
3.13
````

## File: docs/sdlc_quickstart.md
````markdown
# SDLC Quickstart

## Prereqs
- Python tooling via `uv`
- Run from repo root

## Validate an artifact
```bash
uv run sdlc validate runs/<bead_id>/evidence.json
```

## Export schemas
```bash
uv run sdlc schema-export
```

## Transition request
```bash
uv run sdlc request <bead_id> "draft -> sized"
```

## Evidence workflow
```bash
uv run sdlc evidence collect <bead_id>
uv run sdlc evidence validate <bead_id>
uv run sdlc evidence invalidate-if-stale <bead_id>
```

Note:
- `sdlc evidence validate` uses `expect_exit_code`
- `ready -> in_progress` enforces dependencies
- Spec gate requires `runs/<bead_id>/openspec_ref.json` for implementation work

## Grounding
```bash
uv run sdlc grounding generate <bead_id>
```

## Approvals
```bash
uv run sdlc approve <bead_id> --summary "APPROVAL: looks good"
```

## Example flow
```bash
# 1) Validate bead
uv run sdlc validate runs/<bead_id>/bead.json

# 2) Generate grounding
uv run sdlc grounding generate <bead_id>

# 3) Request start
uv run sdlc request <bead_id> "ready -> in_progress"

# 4) Collect and validate evidence
uv run sdlc evidence collect <bead_id>
uv run sdlc evidence validate <bead_id>

# 5) Mark verified -> approval -> done
uv run sdlc request <bead_id> "verification_pending -> verified"
uv run sdlc approve <bead_id> --summary "APPROVAL: shipped"
uv run sdlc request <bead_id> "approval_pending -> done"
```
````

## File: .gitignore
````
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv

/reference
````

## File: README.md
````markdown
# LOOM

## Agentic Software Development Life Cycle (SDLC)
````

## File: AGENTS.md
````markdown
The master specification for this project (LOOM) is in docs/loom-specification.md
Pydantic-AI llms in docs/pydantic-ai-llms.txt
Python env is managed with `uv`. Use `uv run` for things like pytest.

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
````

## File: pyproject.toml
````toml
[project]
name = "loom"
version = "0.0.1"
description = "Agentic SDLC kernel: OpenSpec + Beads validator"
requires-python = ">=3.13"
readme = "README.md"
dependencies = [
    "pydantic-ai>=1.46.0",
    "pydantic-settings>=2.12.0",
    "pydantic>=2.12.0",
    "pyyaml>=6.0.3",
    "rich>=14.2.0",
    "typer>=0.21.1",
]

[project.scripts]
sdlc = "sdlc.cli:app"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[dependency-groups]
dev = [
    "mypy>=1.19.1",
    "pytest>=9.0.2",
    "ruff>=0.14.14",
]

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.13"
strict = true
mypy_path = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
````

## File: docs/loom-specification.md
````markdown
Agentic SDLC v1 Specification

Artifact-driven, spec-first, phase-gated SDLC for solo LLM-assisted development.

This system prioritizes correctness, auditability, and bounded execution over speed or autonomy.

1. Purpose

This specification defines a spec-first, artifact-driven SDLC intended to prevent LLM-driven drift by strictly separating:

 * intent (spec)
 * planning (bead + review)
 * execution (implementation agent)
 * verification (evidence)
 * approval (human gate)

The system targets solo usage and “safe enough” execution via containerization, with auditability focused on learning and workflow improvement.

2. Non-goals

The system is not:

 * fully autonomous
 * a replacement for CI/CD
 * a natural-language-only reasoning system
 * optimized for token minimization over correctness
 * a loose set of best practices without enforcement

3. Normative principles

1. Artifacts are authoritative: free-form chat is non-authoritative.
2. Spec-first: non-trivial work is authorized by an approved OpenSpec change.
3. Bounded execution: all work is decomposed into Beads.
4. Role separation: planning, implementation, verification, approval are distinct phases.
5. Evidence-based completion: “done” is determined only by Evidence bundles.
6. Closed-world semantics: all states/transitions are defined; illegal transitions are rejected and recorded.

---

4. Canonical artifacts

The SDLC defines the following typed artifacts:

 * `OpenSpecRef` (authorizing reference to OpenSpec change + approval status)
 * `BoundaryRegistry` (subsystems + invariants used for sizing/policy checks)
 * `Bead` (bounded work unit)
 * `BeadReview` (tractability sizing + split plan + tightened DoD)
 * `GroundingBundle` (curated repo context + command constraints)
 * `EvidenceBundle` (objective verification results)
 * `ExecutionRecord` (append-only run journal entries)
 * `DecisionLedgerEntry` (append-only decisions/exceptions)

Normative rule: Any automation MUST treat these artifacts as the only source of truth.

Status Authority Rule (Normative)

 * `Bead.status` MUST be treated as engine-authored state.
 * `Bead.status` transitions MAY ONLY be written by the lifecycle engine.
 * Agents (including the implementation agent) MAY request a transition, but the engine MUST validate preconditions and record the transition as an `ExecutionRecord`.
 * Humans MAY initiate a transition request through the engine UI/CLI, but MUST NOT mutate Bead state out-of-band.

Rationale (Non-normative): prevents self-mutating artifacts and keeps audit semantics consistent.

**OpenSpec Reference Rule (Normative)**
A `Bead` MUST reference its authorizing spec via `Bead.openspec_ref` (an `ArtifactLink` to an `OpenSpecRef`) and MUST NOT embed `OpenSpecRef` as a mutable inline structure.

Rationale (Non-normative): avoids duplicated spec state and drift.

Manual Check Evidence Rule (Normative)
If an `EvidenceBundle` contains any `EvidenceItem` with `evidence_type == manual_check`:

 * That `EvidenceItem.summary_md` MUST be present and non-empty.
 * The `EvidenceBundle.created_by.kind` MUST equal `"human"`.

**Illegal Transition Recording Rule (Normative, v1)**
Any rejected transition attempt MUST generate an `ExecutionRecord` with:

 * `exit_code != 0`
 * `requested_transition` set
 * `applied_transition` absent or empty
 * `phase` set to the phase in which the request was made (`plan|implement|verify`)
 * `notes_md` explaining rejection and missing preconditions

A DecisionLedgerEntry MAY additionally be emitted, but ExecutionRecord is canonical.

**Decision Action Journaling Rule (Normative, v1)**
When the engine creates a `DecisionLedgerEntry` as part of enforcing policy (including aborts),
it MUST also emit an `ExecutionRecord` that represents the decision action itself.

The decision-action `ExecutionRecord` MUST:

 * have `requested_transition` unset
 * have `applied_transition` unset
 * have `exit_code == 0`
 * link the DecisionLedgerEntry via `ExecutionRecord.links`
 * use `phase == plan` for pre-execution decisions or `phase == verify` for verification/enforcement decisions

**Acceptance Check Authority Rule (Normative, v1)**

* `BeadReview.tightened_acceptance_checks` is the authoritative set of acceptance checks for verification gating.
* Before a bead can transition `sized → ready`, the lifecycle engine MUST apply `BeadReview.tightened_acceptance_checks` to the bead by writing the resulting canonical `Bead.acceptance_checks`.
* After `ready`, `Bead.acceptance_checks` MUST NOT change except by creating a new bead (supersede) or transitioning to `aborted:needs-discovery` and re-reviewing.


**Split Proposal Structure Rule (Normative)**
`BeadReview.split_proposal` MUST contain lightweight proposed bead *drafts* (title/type/requirements/acceptance/context/dependencies). The lifecycle engine is responsible for creating real `Bead` artifacts from the proposal upon acceptance.

**Canonical ID Rule (Normative)**
For `Bead` artifacts, `artifact_id MUST equal bead_id`.
For non-Bead artifacts, `artifact_id` MUST be globally unique and stable.

Engine Validation Behavior (Normative)
1. **Bead artifact id rule**
   Reject Bead files where `artifact_id != bead_id`.

2. **Acceptance check freeze**
   After `ready`, reject any attempt to modify `Bead.acceptance_checks` in-place **except via abort+re-review or supersede**, per Acceptance Check Authority Rule.

---

5. Canonical serialization

5.1 File formats (normative)

JSON (single object per file)

Used for:

 * `Bead` (optionally; may be stored in existing Beads system)
 * `BeadReview`
 * `GroundingBundle`
 * `EvidenceBundle`
 * `BoundaryRegistry`
 * `OpenSpecRef`

Encoding rules:

 * UTF-8
 * no trailing commas
 * timestamps in RFC 3339 / ISO 8601
 * stable key ordering is not required by JSON, but writers SHOULD output deterministic ordering (for diffs)

JSONL (append-only)

Used for:

 * `ExecutionRecord` (`runs/journal.jsonl`)
 * `DecisionLedgerEntry` (`decision_ledger.jsonl`)

Normative rule: JSONL stores exactly one JSON object per line. Writers MUST only append; never edit prior lines.

Agents MUST NOT author `DecisionLedgerEntry` records with `decision_type` in {approval, exception, assumption, tradeoff, scope_change} unless explicitly permitted by project policy.

5.2 Canonical directories (recommended v1)

```
openspec/...
beads/ (bd tool owns this; may remain issues.jsonl)
sdlc/
  boundary_registry.json
runs/
  journal.jsonl
  <bead_id>/
    grounding.json
    evidence.json
    evidence/
      ...attachments...
decision_ledger.jsonl
```

5.3 Canonical filenames (normative for SDLC-managed outputs)

For bead `<bead_id>`:

 * `runs/<bead_id>/bead.json` → `Bead` (when Loom-managed)
 * `runs/<bead_id>/bead_review.json` → `BeadReview`
 * `runs/<bead_id>/grounding.json` → `GroundingBundle`
 * `runs/<bead_id>/evidence.json` → `EvidenceBundle`
 * `runs/journal.jsonl` → `ExecutionRecord` entries
 * `decision_ledger.jsonl` → `DecisionLedgerEntry` entries

5.4 Canonical Hashing -  Artifact Hash Rule (Normative)

When computing a `HashRef` for any artifact:

 * Serialize the artifact as canonical JSON:
   * UTF-8 encoding
   * no insignificant whitespace
   * keys sorted lexicographically at every object level
   * arrays preserved in their original order
 * Hash the resulting bytes using SHA-256

This makes `reviewed_bead_hash`, `generated_for_bead_hash`, etc. stable across implementations.


---

6. Lifecycle state machines

6.1 Bead lifecycle (normative)

States:

 * `draft`
 * `sized`
 * `ready`
 * `in_progress`
 * `verification_pending`
 * `verified`
 * `approval_pending`
 * `done`

Failure states:

 * `blocked`
 * `aborted:needs-discovery`
 * `failed`
 * `superseded`

Illegal transitions MUST be rejected and recorded per the Illegal Transition Recording Rule (Normative, v1).

Allowed transitions (Normative):

draft → sized
sized → ready
ready → in_progress
in_progress → verification_pending
verification_pending → verified
verified → approval_pending
approval_pending → done

Any state → blocked
Any non-terminal state → aborted:needs-discovery
Any non-terminal state → failed
Any state → superseded

6.1.1 Transition Table (Normative)

Normative rule: The lifecycle engine MUST enforce the transition table below. Any transition not listed is illegal and MUST be rejected and recorded per the Illegal Transition Recording Rule.

| From State | To State | Trigger (Request) | Authority (Who may request) | Engine Preconditions (non-exhaustive) | Notes |
| --- | --- | --- | --- | --- | --- |
| draft | sized | request_size | human, system | Bead exists; required fields present | “Sized” means ready for review/sizing checks. |
| sized | ready | request_ready | human, system | BeadReview exists; effort_bucket != XL; split policy satisfied; Engine applied tightened_acceptance_checks to Bead.acceptance_checks | Engine records computed sizing metrics. |
| ready | in_progress | request_start | human, agent, system | Spec gate satisfied (if implementation); execution_profile satisfied; dependencies satisfied; GroundingBundle present | Engine MUST open a run and record git.head_before/dirty state. |
| in_progress | verification_pending | request_verify | agent, system | Implementation phase completed; working tree in allowed condition (project policy) | Often used when implementation agent signals “ready for verification.” |
| verification_pending | verified | request_mark_verified | system | EvidenceBundle exists; status validated; acceptance coverage satisfied; evidence not stale | Verification is engine-authored; agents cannot directly mark verified. |
| verified | approval_pending | request_approval | system | Verified must be true; approval required by policy | Optional state; may be skipped if you later collapse it. |
| approval_pending | done | request_done | human, system | Approval Recording Rule satisfied; engine links approval entry | Engine writes final transition record. |


**Evidence Validation Rule (Normative)**
EvidenceBundle MAY be marked `validated` only if:

* All referenced commands completed with expected exit codes (or manual checks satisfy Manual Check Evidence Rule), and
* Acceptance Coverage Rule holds for the bead’s canonical acceptance checks, and
* EvidenceBundle.for_bead_hash matches the bead hash at time of validation.

That makes “validated” non-handwavy.


Failure / interruption transitions (Normative)

| From State | To State | Trigger (Request) | Authority | Engine Preconditions | Notes |
| --- | --- | --- | --- | --- | --- |
| any | blocked | request_block | human, agent, system | none | Engine SHOULD require notes_md describing blocker. |
| any non-terminal | aborted:needs-discovery | request_abort | human, system | Abort policy satisfied OR explicit human request | Engine MUST emit DecisionLedgerEntry describing why. |
| any non-terminal | failed | request_fail | human, system | Evidence failed OR execution failed OR policy violation | Use for “cannot proceed” without new spec/plan. |
| any | superseded | request_supersede | human, system | Replacement bead exists OR scope moved | Engine SHOULD link the superseding bead id in ExecutionRecord.links. |


Terminal states: done, failed, superseded (and optionally aborted:needs-discovery if you treat it as terminal).

FSM Global Rules (Normative)
	•	The lifecycle engine MUST be the only writer of Bead.status (per Status Authority Rule).
	•	verified MUST be engine-authored and MUST NOT be directly requested by agents.
	•	The engine MUST record requested_transition and applied_transition for every transition attempt (success or rejection).
	•	The engine MUST reject any transition that would bypass required gates (e.g., ready -> verified).


6.2 Artifact maturity (normative)

 * OpenSpec: `proposal → approved → superseded`
 * Evidence: `collected → validated → invalidated`

Normative rule: Evidence MUST be invalidated if code changes after evidence generation (detected by git HEAD change or file hash mismatch).

 * The lifecycle engine MUST invalidate evidence by updating `EvidenceBundle.status = invalidated` and setting invalidated_reason.

**Evidence Authority Rule (Normative)**
`EvidenceBundle` status transitions (`collected → validated → invalidated`) MAY ONLY be written by the lifecycle engine. Any invalidation MUST be accompanied by an `ExecutionRecord` describing the reason and the detected staleness signal (e.g. git head change).

---

7. Execution profiles (solo-safe)

ExecutionProfile Exception Rule (Normative)
If `Bead.execution_profile == exception`, the bead MUST NOT transition to `in_progress` unless there exists a non-expired `DecisionLedgerEntry` satisfying all of:

 * `decision_type == exception`
 * `bead_id` equals the bead
 * `expires_at` is either absent or in the future
 * `summary` includes a short description of the exception scope (e.g., “network enabled for dependency fetch”)

The engine MUST link the decision entry from the transition `ExecutionRecord`.

ExecutionRecord Decision Links (Normative)
When transitions rely on approval or exception decisions, the engine MUST include a
`decision_ledger_entry` link in the successful transition `ExecutionRecord` that references the
decision artifact.

---

8. Bead sizing + tractability (normative)

Each bead MUST have a `BeadReview` before it can enter `ready`.

Bead must be split if any are true:

 * touches > N files (project-defined; recommended N=8)
 * touches > 2 subsystems (as defined by BoundaryRegistry)
 * has > 1 primary concern (“and also…”)
 * acceptance requires manual judgment instead of a check
 * requires design decisions not already recorded

BeadReview MUST output:

 * effort bucket: `S|M|L|XL`
 * risk flags
 * tightened acceptance checks (explicit commands)
 * split proposal if required

`XL` is forbidden: a bead with `XL` MUST NOT transition to `ready`.

Boundary Computation Rule (Normative)

 * The lifecycle engine MUST compute “subsystems touched” by path-prefix matching changed files against the `BoundaryRegistry` referenced by the bead (`Bead.boundary_registry_ref`).
 * If `Bead.boundary_registry_ref` is absent, the engine MUST use the project’s default boundary registry (`sdlc/boundary_registry.json`) and record that choice in the `ExecutionRecord`.

Boundary Violation Handling (Normative)

 * If mid-execution the engine detects that a bead exceeds subsystem/file limits implied by policy (e.g., >2 subsystems, >N files), the engine MUST:

  1. block further transitions toward `verified`, and
  2. force the bead into `aborted:needs-discovery` OR require a split plan via `BeadReview`, and
  3. record the violation and computed metrics in an `ExecutionRecord`.

 Boundary Registry Integrity (Normative)

  * The engine MUST record the BoundaryRegistry artifact hash used for evaluation in ExecutionRecord.links.

---

9. Discovery beads (normative)

Discovery beads are timeboxed and MUST NOT land production code changes.

Discovery bead outputs:

 * findings (documented in bead context / notes)
 * updated plan (bead split proposal or updated OpenSpec)
 * tightened acceptance checks for follow-on implementation beads

Discovery Authorization (Normative)

  * Discovery beads MAY reference an OpenSpecRef in proposal state OR MAY omit OpenSpecRef.

Production Path Definition (Normative)

  * “Production paths” are defined as the union of all path prefixes listed in the active BoundaryRegistry.subsystems[].paths used for the bead.
  * If the bead does not reference a BoundaryRegistry, the engine MUST use the project default boundary registry (`sdlc/boundary_registry.json`) and record that choice in the ExecutionRecord.
 * The lifecycle engine MUST enforce one of the following controls (project-configurable), and MUST record which policy is active:

  Policy A (recommended):
  * Discovery beads MAY modify files only under a project-configured allowlist of non-production paths (default: docs/, notes/, tools/, experiments/, runs/).
  * Discovery beads MUST NOT modify files whose paths match any “production path” prefix as defined above.

  Policy B:

   * Discovery beads MUST run in a workspace that cannot write to the production repo mount.

Normative default: Policy A.


---

10. Anti-stall / abort policy (normative)

A bead MUST be aborted (`aborted:needs-discovery`) if:

 * time exceeds effort bucket expectation, OR
 * interventions exceed threshold, OR
 * unknown unknowns are detected

An “intervention” is any human action that alters the bead’s plan, acceptance, or execution constraints mid-run.
For v1 enforcement, interventions are counted as DecisionLedgerEntry types:
`assumption`, `tradeoff`, `exception`, or `scope_change` scoped to the bead.

On abort, the system MUST:

 * create a DecisionLedgerEntry describing why
 * use `decision_type == scope_change` for the abort decision
 * produce either:

   * a discovery bead, and/or
   * 2–6 smaller implementation beads + updated dependencies

---

11. Enforcement gates (normative)

The lifecycle engine MUST enforce:

1. Spec gate

    * **Implementation beads MUST have `Bead.openspec_ref` present and the referenced `OpenSpecRef.state == approved`.**

2. Plan gate

    * Bead must have a `BeadReview` with bucket != `XL`
    * If bucket == `L`, must have either split plan applied or explicit justification recorded.
      For v1 enforcement, “justification” is a DecisionLedgerEntry of type `assumption`, `tradeoff`,
      or `scope_change` with a non-empty summary for that bead.

3. Implement gate

    * Engine MUST provide the implementation agent with the GroundingBundle as the primary repo context.
    * Engine SHOULD restrict repo access to the GroundingBundle when technically feasible.
    * Engine MUST record detected accesses outside the GroundingBundle as a policy violation in ExecutionRecord.notes_md (best-effort).
    * Execution must occur under the bead’s `execution_profile`.

4. Verify gate

    * Bead cannot become `verified` without a `validated` `EvidenceBundle` that covers all acceptance checks.

5. Approval gate

   * A bead MUST NOT transition to done unless the Approval Recording Rule is satisfied.

Acceptance Coverage Rule (Normative)
To transition a bead to `verified`:

 * Every `AcceptanceCheck` applicable to the bead MUST be covered by at least one corresponding `EvidenceItem`, OR
 * The check MUST be explicitly waived by a `DecisionLedgerEntry` of type `exception` that:

   * references the bead,
   * names the waived check(s), and
   * provides rationale.

Correspondence Rule (Normative, v1)

Evidence covers an acceptance check if any of the following hold:
 1. Command match (preferred):
  * EvidenceItem.command equals AcceptanceCheck.command, and EvidenceItem.exit_code == AcceptanceCheck.expect_exit_code.
 2. Human-attested coverage:
  * EvidenceBundle.created_by.kind == "human", and
  * EvidenceItem.summary_md explicitly states that it covers AcceptanceCheck.name.
 3. Output-artifact match (optional, if used by project):
  * The acceptance check lists one or more expected_outputs, and
  * The evidence item attaches files with matching path and matching content_hash for those outputs.

Normative note: An EvidenceItem.summary_md statement authored by a non-human MUST NOT be used to establish acceptance coverage.

**Approval Recording Rule (Normative, v1)**
A bead MUST NOT transition to `done` unless there exists a `DecisionLedgerEntry` with:

* `decision_type == approval`
* `created_by.kind == "human"`
* `bead_id` set to the bead
* `summary` non-empty

The lifecycle engine MUST link this approval entry from the `done` transition `ExecutionRecord` via `ExecutionRecord.links`.

**Recommended convention (Non-normative)**
`summary` SHOULD start with `APPROVAL:` for grepability (recommended, not required).

---

12. Normative schemas (canonical source)

12.1 Schema source of truth

Normative rule: The canonical schema definitions for v1 are the Pydantic v2 models below.
JSON Schema exports MAY be generated from these models and used for validation, but Pydantic models are the normative reference.

Schema Version Update (Normative)

The schemas in this document define v1 of the SDLC artifact models.

 * All artifacts MUST set schema_version == 1.
 * Implementations MAY accept schema_version == 0 as a legacy format only if explicitly configured, and MUST treat it as deprecated.

Rationale (non-normative): v0 was pre-release; the addition of transition fields and waiver fields would otherwise break strict validators.

Then update all model literals from Literal[0] = 0 to Literal[1] = 1.

ArtifactLink Type Conventions (Normative)

When populating SchemaBase.links, implementations MUST use the following artifact_type values:

 * openspec_ref
 * boundary_registry
 * bead
 * bead_review
 * grounding_bundle
 * evidence_bundle
 * decision_ledger_entry
 * execution_record


12.2 Pydantic v2 schema definitions (v1)

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated
from pydantic import ConfigDict

ISO8601 = datetime

Sha256Hex = Annotated[
    str,
    StringConstraints(pattern=r"^[a-f0-9]{64}$", strip_whitespace=True),
]

ArtifactId = Annotated[
    str,
    StringConstraints(min_length=6, max_length=128, strip_whitespace=True),
]

BeadId = Annotated[
    str,
    StringConstraints(pattern=r"^work-[a-z0-9]+(\.[a-z0-9]+)?$", strip_whitespace=True),
]


class HashRef(BaseModel):
    hash_alg: Literal["sha256"] = "sha256"
    hash: Sha256Hex


class FileRef(BaseModel):
    path: str = Field(..., description="Repo-relative path")
    content_hash: Optional[HashRef] = None


class ArtifactLink(BaseModel):
    artifact_type: str
    artifact_id: ArtifactId
    schema_name: Optional[str] = None
    schema_version: Optional[int] = None


class Actor(BaseModel):
    kind: Literal["human", "agent", "system"]
    name: str
    email: Optional[str] = None


class SchemaBase(BaseModel):
    schema_name: str
    schema_version: int
    artifact_id: ArtifactId
    created_at: ISO8601
    created_by: Actor
    links: List[ArtifactLink] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")


# ---- OpenSpec reference (minimal authorizer) ----

class OpenSpecState(str, Enum):
    proposal = "proposal"
    approved = "approved"
    superseded = "superseded"


class OpenSpecRef(SchemaBase):
    schema_name: Literal["sdlc.openspec_ref"] = "sdlc.openspec_ref"
    schema_version: Literal[1] = 1

    change_id: str
    state: OpenSpecState
    path: str
    approved_at: Optional[ISO8601] = None
    approved_by: Optional[Actor] = None
    content_hash: Optional[HashRef] = None


# ---- Boundary registry ----

class Subsystem(BaseModel):
    name: str
    paths: List[str]
    invariants: List[str] = Field(default_factory=list)


class BoundaryRegistry(SchemaBase):
    schema_name: Literal["sdlc.boundary_registry"] = "sdlc.boundary_registry"
    schema_version: Literal[1] = 1

    registry_name: str
    subsystems: List[Subsystem]
    notes: Optional[str] = None


# ---- Beads ----

class BeadType(str, Enum):
    implementation = "implementation"
    discovery = "discovery"


class BeadStatus(str, Enum):
    draft = "draft"
    sized = "sized"
    ready = "ready"
    in_progress = "in_progress"
    verification_pending = "verification_pending"
    verified = "verified"
    approval_pending = "approval_pending"
    done = "done"
    blocked = "blocked"
    aborted_needs_discovery = "aborted:needs-discovery"
    failed = "failed"
    superseded = "superseded"


class ExecutionProfile(str, Enum):
    sandbox = "sandbox"
    ci_like = "ci-like"
    exception = "exception"


class AcceptanceCheck(BaseModel):
    name: str
    command: str
    cwd: Optional[str] = None
    timeout_seconds: Optional[int] = None
    expect_exit_code: int = 0
    expected_outputs: List[FileRef] = Field(default_factory=list)


class Bead(SchemaBase):
    schema_name: Literal["sdlc.bead"] = "sdlc.bead"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    title: str
    bead_type: BeadType
    status: BeadStatus

    priority: int = Field(3, ge=1, le=5)
    owner: Optional[str] = None

    # Canonical reference to OpenSpecRef (avoid inline drift)
    openspec_ref: Optional[ArtifactLink] = None

    boundary_registry_ref: Optional[ArtifactLink] = None

    requirements_md: str
    acceptance_criteria_md: str
    context_md: str

    # Canonical acceptance checks after review applied.
    acceptance_checks: List[AcceptanceCheck] = Field(default_factory=list)

    execution_profile: ExecutionProfile = ExecutionProfile.sandbox
    depends_on: List[BeadId] = Field(default_factory=list)

    max_elapsed_minutes: Optional[int] = None
    max_interventions: Optional[int] = None

    # Note: Spec rule (normative): for Bead, artifact_id MUST equal bead_id.
    # Enforced by engine/validator, not schema alone.


# ---- Bead review ----

class EffortBucket(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class RiskFlag(str, Enum):
    unknowns = "unknowns"
    dependency_hazard = "dependency_hazard"
    unclear_acceptance = "unclear_acceptance"
    cross_boundary_change = "cross_boundary_change"
    design_decision_missing = "design_decision_missing"
    too_many_files = "too_many_files"
    too_many_subsystems = "too_many_subsystems"
    multiple_primary_concerns = "multiple_primary_concerns"


class ProposedBeadDraft(BaseModel):
    """
    Lightweight bead draft used only inside a split proposal.
    The lifecycle engine materializes these into real Bead artifacts.
    """
    title: str
    bead_type: BeadType
    requirements_md: str
    acceptance_criteria_md: str
    context_md: str
    depends_on: List[str] = Field(default_factory=list)


class SplitProposal(BaseModel):
    proposed_beads: List[ProposedBeadDraft]
    rationale: str


class BeadReview(SchemaBase):
    schema_name: Literal["sdlc.bead_review"] = "sdlc.bead_review"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    reviewed_bead_hash: Optional[HashRef] = None

    effort_bucket: EffortBucket
    risk_flags: List[RiskFlag] = Field(default_factory=list)

    estimated_files_touched: Optional[int] = None
    estimated_subsystems_touched: Optional[List[str]] = None

    # Authoritative checks that the engine applies before sized->ready.
    tightened_acceptance_checks: List[AcceptanceCheck] = Field(default_factory=list)

    split_required: bool = False
    split_proposal: Optional[SplitProposal] = None

    notes: Optional[str] = None


# ---- Grounding bundle ----

class GroundingItem(BaseModel):
    kind: Literal["file", "api", "pattern", "command", "note"]
    title: str
    content_md: str
    file_ref: Optional[FileRef] = None


class GroundingBundle(SchemaBase):
    schema_name: Literal["sdlc.grounding_bundle"] = "sdlc.grounding_bundle"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    generated_for_bead_hash: Optional[HashRef] = None

    items: List[GroundingItem] = Field(default_factory=list)

    allowed_commands: List[str] = Field(default_factory=list)
    disallowed_commands: List[str] = Field(default_factory=list)
    excluded_paths: List[str] = Field(default_factory=list)

    summary_md: Optional[str] = None


# ---- Evidence ----

class EvidenceType(str, Enum):
    test_run = "test_run"
    lint = "lint"
    typecheck = "typecheck"
    benchmark = "benchmark"
    golden_compare = "golden_compare"
    manual_check = "manual_check"
    ci_run = "ci_run"


class EvidenceStatus(str, Enum):
    collected = "collected"
    validated = "validated"
    invalidated = "invalidated"


class EvidenceItem(BaseModel):
    name: str
    evidence_type: EvidenceType
    command: Optional[str] = None
    exit_code: Optional[int] = None
    started_at: Optional[ISO8601] = None
    finished_at: Optional[ISO8601] = None
    attachments: List[FileRef] = Field(default_factory=list)
    summary_md: Optional[str] = None


class EvidenceBundle(SchemaBase):
    schema_name: Literal["sdlc.evidence_bundle"] = "sdlc.evidence_bundle"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    for_bead_hash: Optional[HashRef] = None
    status: EvidenceStatus = EvidenceStatus.collected
    items: List[EvidenceItem]
    invalidated_reason: Optional[str] = None


# ---- Execution record (JSONL) ----

class RunPhase(str, Enum):
    plan = "plan"
    implement = "implement"
    verify = "verify"


class GitRef(BaseModel):
    head_before: Optional[str] = None
    head_after: Optional[str] = None
    dirty_before: Optional[bool] = None
    dirty_after: Optional[bool] = None


class ExecutionRecord(SchemaBase):
    schema_name: Literal["sdlc.execution_record"] = "sdlc.execution_record"
    schema_version: Literal[1] = 1

    bead_id: BeadId
    phase: RunPhase

    engine_version: Optional[str] = None
    policy_version: Optional[str] = None

    container_image: Optional[str] = None
    container_digest: Optional[str] = None
    commands: List[str] = Field(default_factory=list)
    exit_code: Optional[int] = None
    produced_artifacts: List[FileRef] = Field(default_factory=list)
    git: Optional[GitRef] = None
    notes_md: Optional[str] = None
    requested_transition: Optional[str] = None  # e.g. "ready -> in_progress"
    applied_transition: Optional[str] = None    # e.g. "ready -> in_progress"


# ---- Decision ledger (JSONL) ----

class DecisionType(str, Enum):
    approval = "approval"
    assumption = "assumption"
    tradeoff = "tradeoff"
    exception = "exception"
    scope_change = "scope_change"


class DecisionLedgerEntry(SchemaBase):
    schema_name: Literal["sdlc.decision_ledger_entry"] = "sdlc.decision_ledger_entry"
    schema_version: Literal[1] = 1

    bead_id: Optional[BeadId] = None
    decision_type: DecisionType
    summary: str
    rationale_md: Optional[str] = None
    expires_at: Optional[ISO8601] = None
    waived_acceptance_checks: List[str] = Field(default_factory=list)
```


---

13. Canonical JSON Schema export (non-normative but recommended)

Although the Pydantic models are normative, implementations SHOULD export JSON Schemas for tooling, validation outside Python, and editor support.

Recommended convention:

 * `sdlc/schemas/<schema_name>.v<schema_version>.json`

Example export approach:

 * `Bead.model_json_schema()` (Pydantic v2)

---

14. Compatibility and evolution

 * Backward-compatible changes: add optional fields.
 * Breaking changes: increment `schema_version` and provide a migration note.
 * Implementations SHOULD support validating at least the last two schema versions.

---

15. Minimal enforcement checklist (v1)

An implementation is “conformant” if it:

 * validates artifacts against the schemas above
 * enforces bead state transitions
 * enforces spec-first for implementation beads (approved OpenSpecRef)
 * requires BeadReview before ready
 * requires EvidenceBundle(validated) before verified
 * records execution events and decisions append-only (JSONL)

---
````

## File: src/sdlc/cli.py
````python
from __future__ import annotations

import json
import os
import re
from pathlib import Path
import typer
from pydantic import ValidationError

from .codec import sha256_canonical_json
from .engine import (
    append_decision_entry,
    build_execution_record,
    collect_evidence_skeleton,
    create_abort_entry,
    create_approval_entry,
    decision_ledger_link,
    generate_grounding_bundle,
    invalidate_evidence_if_stale,
    record_decision_action,
    record_transition_attempt,
    request_transition,
    validate_evidence_bundle,
)
from .io import Paths, git_head, git_is_dirty, load_bead, load_evidence, write_model
from .models import Actor, BeadStatus, FileRef, GitRef, OpenSpecRef, RunPhase, schema_registry


app = typer.Typer(add_completion=False)
schema_app = typer.Typer(add_completion=False)


def _phase_for_transition(transition: str) -> RunPhase:
    """
    Best-effort mapping from requested transition to RunPhase for journaling.
    Keeps journal compliant with the Loom spec rule that phase reflects where the
    request sits in the lifecycle (plan/implement/verify).
    """
    match = re.match(r"^\s*([^-\s>]+)\s*->\s*([^-\s>]+)\s*$", transition)
    if not match:
        return RunPhase.implement
    to_status = match.group(2).strip()

    if to_status in {"sized", "ready"}:
        return RunPhase.plan
    if to_status in {"in_progress", "verification_pending"}:
        return RunPhase.implement
    if to_status in {"verified", "approval_pending", "done"}:
        return RunPhase.verify

    return RunPhase.implement


def _decision_action_phase(paths: Paths, bead_id: str) -> RunPhase:
    bead = load_bead(paths, bead_id)
    if bead.status in {BeadStatus.draft, BeadStatus.sized, BeadStatus.ready}:
        return RunPhase.plan
    return RunPhase.verify


@app.command()
def validate(path: Path) -> None:
    """Validate an SDLC artifact."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema_name = payload.get("schema_name")
    if not schema_name:
        typer.echo("Missing schema_name")
        raise typer.Exit(code=2)
    registry = schema_registry()
    model = registry.get(schema_name)
    if model is None:
        typer.echo(f"Unknown schema_name: {schema_name}")
        raise typer.Exit(code=2)
    try:
        model.model_validate(payload)
    except ValidationError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2)


@app.command()
def hash(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    typer.echo(sha256_canonical_json(payload))


@app.command("schema-export")
def schema_export(out: Path = Path("sdlc/schemas")) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for schema_name, cls in schema_registry().items():
        schema_version = cls.model_fields["schema_version"].default
        if isinstance(schema_version, int):
            filename = f"{schema_name}.v{schema_version}.json"
            (out / filename).write_text(
                json.dumps(cls.model_json_schema(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )


@schema_app.command("export")
def schema_export_alias(out: Path = Path("sdlc/schemas")) -> None:
    schema_export(out)


@app.command()
def request(
    bead_id: str,
    transition: str,
    actor_kind: str = typer.Option("human", "--actor-kind"),
    actor_name: str = typer.Option(os.getenv("USER", "unknown"), "--actor-name"),
) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind=actor_kind, name=actor_name)
    result = request_transition(paths, bead_id, transition, actor)
    phase = _phase_for_transition(transition)
    record_transition_attempt(paths, bead_id, phase, actor, transition, result)
    if not result.ok:
        raise typer.Exit(code=1)


evidence_app = typer.Typer(add_completion=False)
app.add_typer(evidence_app, name="evidence")


app.add_typer(schema_app, name="schema")


grounding_app = typer.Typer(add_completion=False)
app.add_typer(grounding_app, name="grounding")
openspec_app = typer.Typer(add_completion=False)
app.add_typer(openspec_app, name="openspec")


@evidence_app.command("collect")
def evidence_collect(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    bead = load_bead(paths, bead_id)
    bundle = collect_evidence_skeleton(bead, actor)
    write_model(paths.evidence_path(bead_id), bundle)


@evidence_app.command("validate")
def evidence_validate(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    evidence = load_evidence(paths, bead_id)
    actor = Actor(kind="system", name="sdlc")
    if evidence and evidence.created_by.kind == "human":
        actor = evidence.created_by
    evidence, errors = validate_evidence_bundle(paths, bead_id, actor, mark_validated=True)
    git_ref = GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths))
    record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0 if not errors else 1,
        notes_md="; ".join(errors) if errors else None,
        git=git_ref,
        produced_artifacts=[FileRef(path=f"runs/{bead_id}/evidence.json")],
    )
    from .io import write_execution_record

    write_execution_record(paths, record)
    if errors:
        typer.echo("; ".join(errors))
        raise typer.Exit(code=1)


@evidence_app.command("invalidate-if-stale")
def evidence_invalidate_if_stale(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    reason = invalidate_evidence_if_stale(paths, bead_id, actor)
    if reason:
        typer.echo(reason)


@grounding_app.command("generate")
def grounding_generate(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    generate_grounding_bundle(paths, bead_id, actor)


@app.command()
def approve(bead_id: str, summary: str = typer.Option(..., "--summary")) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="human", name="sdlc")
    if not summary.strip():
        typer.echo("Summary must be non-empty")
        raise typer.Exit(code=2)
    if not summary.startswith("APPROVAL:"):
        typer.echo('Warning: summary should start with "APPROVAL:"', err=True)
    entry = create_approval_entry(bead_id, summary, actor)
    append_decision_entry(paths, entry)


@app.command()
def abort(
    bead_id: str,
    reason: str = typer.Option(..., "--reason"),
    actor_kind: str = typer.Option("human", "--actor-kind"),
    actor_name: str = typer.Option(os.getenv("USER", "unknown"), "--actor-name"),
) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind=actor_kind, name=actor_name)
    entry = create_abort_entry(bead_id, reason, actor)
    append_decision_entry(paths, entry)
    record_decision_action(
        paths,
        entry,
        _decision_action_phase(paths, bead_id),
        actor,
        notes_md="Abort requested",
    )
    bead = load_bead(paths, bead_id)
    requested = f"{bead.status.value} -> {BeadStatus.aborted_needs_discovery.value}"
    result = request_transition(paths, bead_id, requested, actor)
    record_transition_attempt(
        paths,
        bead_id,
        _phase_for_transition(requested),
        actor,
        requested,
        result,
        extra_links=[decision_ledger_link(entry)],
    )
    if not result.ok:
        raise typer.Exit(code=1)


@openspec_app.command("sync")
def openspec_sync(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    bead = load_bead(paths, bead_id)
    if bead.openspec_ref is None:
        typer.echo("Bead.openspec_ref missing")
        raise typer.Exit(code=2)
    artifact_id = bead.openspec_ref.artifact_id
    ref_path = paths.repo_root / "openspec" / "refs" / f"{artifact_id}.json"
    if not ref_path.exists():
        typer.echo(f"OpenSpecRef artifact not found: {ref_path}")
        raise typer.Exit(code=2)
    try:
        ref = OpenSpecRef.model_validate_json(ref_path.read_text(encoding="utf-8"))
    except ValidationError as exc:
        typer.echo(f"OpenSpecRef invalid: {exc}")
        raise typer.Exit(code=2)
    out_path = paths.bead_dir(bead_id) / "openspec_ref.json"
    write_model(out_path, ref)
    typer.echo(str(out_path))
````

## File: src/sdlc/engine.py
````python
from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import subprocess
from typing import Iterable, Optional

from .codec import sha256_canonical_json
from .io import (
    Paths,
    ensure_parent,
    git_head,
    git_is_dirty,
    load_bead,
    load_bead_review,
    load_decision_ledger,
    load_evidence,
    load_execution_records,
    load_grounding,
    now_utc,
    write_decision_entry,
    write_execution_record,
    write_model,
)
from .models import (
    AcceptanceCheck,
    Actor,
    ArtifactLink,
    BoundaryRegistry,
    Bead,
    BeadReview,
    BeadStatus,
    BeadType,
    DecisionLedgerEntry,
    DecisionType,
    EffortBucket,
    EvidenceBundle,
    EvidenceItem,
    EvidenceStatus,
    EvidenceType,
    ExecutionProfile,
    ExecutionRecord,
    FileRef,
    GitRef,
    GroundingBundle,
    HashRef,
    OpenSpecRef,
    OpenSpecState,
    RunPhase,
)


TRANSITIONS: dict[str, str] = {
    "draft": "sized",
    "sized": "ready",
    "ready": "in_progress",
    "in_progress": "verification_pending",
    "verification_pending": "verified",
    "verified": "approval_pending",
    "approval_pending": "done",
}

TERMINAL_STATES = {
    BeadStatus.done.value,
    BeadStatus.failed.value,
    BeadStatus.superseded.value,
}

FAILURE_TARGETS = {
    BeadStatus.blocked.value,
    BeadStatus.aborted_needs_discovery.value,
    BeadStatus.failed.value,
    BeadStatus.superseded.value,
}

TRANSITION_AUTHORITY: dict[tuple[str, str], set[str]] = {
    (BeadStatus.verification_pending.value, BeadStatus.verified.value): {"system"},
}


@dataclass
class TransitionResult:
    ok: bool
    notes: str
    applied_transition: Optional[str] = None
    phase: Optional[RunPhase] = None
    links: list[ArtifactLink] = field(default_factory=list)
    auto_abort: bool = False


@dataclass
class GateResult:
    ok: bool
    notes: str = ""


@dataclass(frozen=True)
class BoundaryEvaluation:
    registry: BoundaryRegistry
    registry_hash: HashRef
    touched_subsystems: list[str]
    files_touched: int
    production_prefixes: list[str]
    registry_path: Optional[Path]


def canonical_hash_for_model(model: Bead | BeadReview | EvidenceBundle) -> HashRef:
    payload = model.model_dump(mode="json")
    return HashRef(hash=sha256_canonical_json(payload))


def canonical_hash_for_acceptance_checks(checks: list[AcceptanceCheck]) -> HashRef:
    payload = [item.model_dump(mode="json") for item in checks]
    return HashRef(hash=sha256_canonical_json(payload))


def canonical_hash_for_boundary_registry(registry: BoundaryRegistry) -> HashRef:
    payload = registry.model_dump(mode="json")
    return HashRef(hash=sha256_canonical_json(payload))


def _default_boundary_registry_path(paths: Paths) -> Path:
    return paths.repo_root / "sdlc" / "boundary_registry.json"


def load_boundary_registry(paths: Paths, bead: Bead) -> tuple[BoundaryRegistry, Optional[Path]]:
    if bead.boundary_registry_ref is not None:
        ref = bead.boundary_registry_ref
        if ref.artifact_type != "boundary_registry":
            raise ValueError("Bead.boundary_registry_ref must reference boundary_registry artifact")
        candidate = paths.repo_root / "sdlc" / f"{ref.artifact_id}.json"
        if candidate.exists():
            return BoundaryRegistry.model_validate_json(
                candidate.read_text(encoding="utf-8")
            ), candidate
    default_path = _default_boundary_registry_path(paths)
    if not default_path.exists():
        raise FileNotFoundError(f"BoundaryRegistry not found: {default_path}")
    return BoundaryRegistry.model_validate_json(
        default_path.read_text(encoding="utf-8")
    ), default_path


def detect_changed_files(paths: Paths, head_before: Optional[str] = None) -> list[str]:
    try:
        if head_before:
            output = subprocess.check_output(
                ["git", "diff", "--name-only", f"{head_before}..HEAD"],
                cwd=paths.repo_root,
            )
        else:
            output = subprocess.check_output(
                ["git", "diff", "--name-only", "HEAD"],
                cwd=paths.repo_root,
            )
        return [line.strip() for line in output.decode("utf-8").splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def _normalize_prefix(prefix: str) -> str:
    return prefix.lstrip("./")


def compute_touched_subsystems(
    registry: BoundaryRegistry, changed_files: Iterable[str]
) -> tuple[list[str], int]:
    touched: set[str] = set()
    count = 0
    normalized_files = [_normalize_prefix(path) for path in changed_files]
    for path in normalized_files:
        count += 1
        for subsystem in registry.subsystems:
            for prefix in subsystem.paths:
                normalized_prefix = _normalize_prefix(prefix)
                if not normalized_prefix:
                    continue
                if path.startswith(normalized_prefix):
                    touched.add(subsystem.name)
                    break
    return sorted(touched), count


def _production_prefixes(registry: BoundaryRegistry) -> list[str]:
    prefixes: set[str] = set()
    for subsystem in registry.subsystems:
        for prefix in subsystem.paths:
            normalized = _normalize_prefix(prefix)
            if normalized:
                prefixes.add(normalized)
    return sorted(prefixes)


def evaluate_boundary(
    paths: Paths,
    bead: Bead,
    changed_files: Optional[list[str]] = None,
    changed_files_provider: Optional[callable] = None,
) -> BoundaryEvaluation:
    registry, registry_path = load_boundary_registry(paths, bead)
    registry_hash = canonical_hash_for_boundary_registry(registry)
    if changed_files is None:
        if changed_files_provider is None:
            changed_files = detect_changed_files(paths)
        else:
            changed_files = changed_files_provider(paths)
    touched_subsystems, files_touched = compute_touched_subsystems(registry, changed_files)
    return BoundaryEvaluation(
        registry=registry,
        registry_hash=registry_hash,
        touched_subsystems=touched_subsystems,
        files_touched=files_touched,
        production_prefixes=_production_prefixes(registry),
        registry_path=registry_path,
    )


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_optional_int(name: str) -> Optional[int]:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def _discovery_allowlist(default: str = "docs/,notes/,tools/,experiments/,runs/") -> list[str]:
    raw = os.getenv("SDLC_DISCOVERY_ALLOWLIST", default)
    items = []
    for item in raw.split(","):
        cleaned = _normalize_prefix(item.strip())
        if cleaned:
            items.append(cleaned)
    return items


def _boundary_link(registry: BoundaryRegistry) -> ArtifactLink:
    return ArtifactLink(
        artifact_type="boundary_registry",
        artifact_id=registry.artifact_id,
        schema_name="sdlc.boundary_registry",
        schema_version=1,
    )


def boundary_violation_notes(
    evaluation: BoundaryEvaluation, max_files: int, max_subsystems: int
) -> str:
    parts = [
        f"Boundary violation: files_touched={evaluation.files_touched} (limit {max_files})",
        f"subsystems_touched={len(evaluation.touched_subsystems)} (limit {max_subsystems})",
    ]
    if evaluation.touched_subsystems:
        parts.append("touched_subsystems=" + ", ".join(evaluation.touched_subsystems))
    parts.append(f"boundary_registry_hash={evaluation.registry_hash.hash}")
    return "; ".join(parts)


def discovery_policy_violation_notes(
    evaluation: BoundaryEvaluation,
    changed_files: list[str],
    allowlist: list[str],
    policy_name: str = "Policy A",
) -> str:
    normalized_files = [_normalize_prefix(path) for path in changed_files]
    production_hits = []
    for path in normalized_files:
        for prefix in evaluation.production_prefixes:
            if path.startswith(prefix):
                production_hits.append(path)
                break
    parts = [
        f"Discovery policy violation ({policy_name})",
        f"production_paths_hit={sorted(set(production_hits))}",
        f"allowlist={allowlist}",
        f"boundary_registry_hash={evaluation.registry_hash.hash}",
    ]
    return "; ".join(parts)


def _ready_acceptance_snapshot_path(paths: Paths, bead_id: str) -> Path:
    return paths.bead_dir(bead_id) / "ready_acceptance_hash.json"


def _write_ready_acceptance_snapshot(paths: Paths, bead: Bead) -> None:
    snapshot_path = _ready_acceptance_snapshot_path(paths, bead.bead_id)
    payload = {
        "bead_id": bead.bead_id,
        "acceptance_checks_hash": canonical_hash_for_acceptance_checks(bead.acceptance_checks).hash,
        "bead_hash": canonical_hash_for_model(bead).hash,
    }
    ensure_parent(snapshot_path)
    snapshot_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _load_ready_acceptance_snapshot(paths: Paths, bead_id: str) -> Optional[dict[str, str]]:
    snapshot_path = _ready_acceptance_snapshot_path(paths, bead_id)
    if not snapshot_path.exists():
        return None
    return json.loads(snapshot_path.read_text(encoding="utf-8"))


def ensure_bead_artifact_id(bead: Bead) -> Optional[str]:
    if bead.artifact_id != bead.bead_id:
        return "Bead artifact_id must equal bead_id"
    return None


def apply_acceptance_checks_from_review(bead: Bead, review: BeadReview) -> None:
    bead.acceptance_checks = list(review.tightened_acceptance_checks)


def acceptance_checks_equal(left: list[AcceptanceCheck], right: list[AcceptanceCheck]) -> bool:
    return [item.model_dump(mode="json") for item in left] == [
        item.model_dump(mode="json") for item in right
    ]


def allowed_transition(from_status: str, to_status: str) -> bool:
    if to_status in FAILURE_TARGETS:
        if to_status == BeadStatus.blocked.value:
            return True
        if to_status == BeadStatus.superseded.value:
            return True
        if from_status in TERMINAL_STATES:
            return False
        return True
    return TRANSITIONS.get(from_status) == to_status


def _require_review_for_ready(bead: Bead, review: Optional[BeadReview]) -> Optional[str]:
    if review is None:
        return "BeadReview missing"
    if review.effort_bucket.value == "XL":
        return "BeadReview effort bucket XL not allowed"
    return None


def _bucket_l_justification_decision(paths: Paths, bead_id: str) -> Optional[DecisionLedgerEntry]:
    for entry in load_decision_ledger(paths):
        if entry.bead_id != bead_id:
            continue
        if entry.decision_type not in {
            DecisionType.assumption,
            DecisionType.tradeoff,
            DecisionType.scope_change,
        }:
            continue
        if not entry.summary.strip():
            continue
        return entry
    return None


def _plan_gate_bucket_l(
    paths: Paths, bead_id: str, review: Optional[BeadReview]
) -> Optional[str]:
    if review is None:
        return None
    if review.effort_bucket != EffortBucket.L:
        return None
    if review.split_required and review.split_proposal is not None:
        return None
    if _bucket_l_justification_decision(paths, bead_id) is not None:
        return None
    if review.split_required and review.split_proposal is None:
        return "BeadReview split_required true but split_proposal missing for bucket L"
    return (
        "BeadReview effort bucket L requires split_required+split_proposal "
        "or justification DecisionLedgerEntry"
    )


def _intervention_decision_types() -> set[DecisionType]:
    return {
        DecisionType.assumption,
        DecisionType.tradeoff,
        DecisionType.exception,
        DecisionType.scope_change,
    }


def _count_interventions(paths: Paths, bead_id: str) -> int:
    return sum(
        1
        for entry in load_decision_ledger(paths)
        if entry.bead_id == bead_id and entry.decision_type in _intervention_decision_types()
    )


def _elapsed_minutes(bead: Bead) -> int:
    delta = now_utc() - bead.created_at
    seconds = max(0, int(delta.total_seconds()))
    return seconds // 60


def anti_stall_errors(paths: Paths, bead: Bead) -> list[str]:
    errors: list[str] = []
    max_elapsed = bead.max_elapsed_minutes
    if max_elapsed is None:
        max_elapsed = _env_optional_int("SDLC_MAX_ELAPSED_MINUTES_DEFAULT")
    if max_elapsed is not None:
        elapsed = _elapsed_minutes(bead)
        if elapsed > max_elapsed:
            errors.append(
                f"Anti-stall: elapsed_minutes={elapsed} exceeds limit {max_elapsed}"
            )
    max_interventions = bead.max_interventions
    if max_interventions is None:
        max_interventions = _env_optional_int("SDLC_MAX_INTERVENTIONS_DEFAULT")
    if max_interventions is not None:
        interventions = _count_interventions(paths, bead.bead_id)
        if interventions > max_interventions:
            types = ", ".join(sorted(t.value for t in _intervention_decision_types()))
            errors.append(
                "Anti-stall: interventions="
                f"{interventions} exceeds limit {max_interventions} "
                f"(types={types})"
            )
    return errors


def _phase_for_transition(from_status: str, to_status: str) -> RunPhase:
    if to_status in {"sized", "ready"}:
        return RunPhase.plan
    if to_status in {"in_progress", "verification_pending"}:
        return RunPhase.implement
    if to_status in {"verified", "approval_pending", "done"}:
        return RunPhase.verify
    return RunPhase.implement


def _spec_gate(paths: Paths, bead: Bead) -> Optional[str]:
    if bead.bead_type != BeadType.implementation:
        return None
    if bead.openspec_ref is None:
        return "Bead.openspec_ref missing"
    if bead.openspec_ref.artifact_type != "openspec_ref":
        return "Bead.openspec_ref must reference openspec_ref artifact"
    ref_path = paths.bead_dir(bead.bead_id) / "openspec_ref.json"
    if not ref_path.exists():
        return "OpenSpecRef artifact missing (runs/<bead_id>/openspec_ref.json); run grounding/spec sync"
    try:
        ref = OpenSpecRef.model_validate_json(ref_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return f"OpenSpecRef invalid: {exc}"
    if ref.state != OpenSpecState.approved:
        return "OpenSpecRef not approved"
    if ref.artifact_id != bead.openspec_ref.artifact_id:
        return (
            "OpenSpecRef mismatch: runs/"
            f"{bead.bead_id}/openspec_ref.json artifact_id='{ref.artifact_id}' "
            f"does not match bead.openspec_ref.artifact_id='{bead.openspec_ref.artifact_id}'"
        )
    return None


def _execution_profile_gate(paths: Paths, bead: Bead) -> Optional[str]:
    if bead.execution_profile != ExecutionProfile.exception:
        return None
    if find_active_exception_decision(paths, bead.bead_id) is not None:
        return None
    return "Execution profile exception requires DecisionLedgerEntry"


def _grounding_gate(paths: Paths, bead: Bead) -> Optional[str]:
    if load_grounding(paths, bead.bead_id) is None:
        return "GroundingBundle missing"
    return None


def _evidence_gate(paths: Paths, bead: Bead) -> Optional[str]:
    evidence = load_evidence(paths, bead.bead_id)
    if evidence is None:
        return "EvidenceBundle missing"
    if evidence.status != EvidenceStatus.validated:
        return "EvidenceBundle not validated"
    return None


def _approval_gate(paths: Paths, bead: Bead) -> Optional[str]:
    if find_approval_decision(paths, bead.bead_id) is not None:
        return None
    return "Approval DecisionLedgerEntry missing"


def _dependencies_gate(paths: Paths, bead: Bead) -> GateResult:
    if not bead.depends_on:
        return GateResult(True, "")
    blockers: list[str] = []
    for dependency_id in bead.depends_on:
        try:
            dependency = load_bead(paths, dependency_id)
        except FileNotFoundError:
            blockers.append(f"{dependency_id} (missing)")
            continue
        if dependency.status != BeadStatus.done:
            blockers.append(f"{dependency_id} ({dependency.status.value})")
    if blockers:
        return GateResult(False, "Dependencies not done: " + ", ".join(blockers))
    return GateResult(True, "")


def _apply_transition(bead: Bead, new_status: BeadStatus) -> None:
    bead.status = new_status


def request_transition(paths: Paths, bead_id: str, transition: str, actor: Actor) -> TransitionResult:
    bead = load_bead(paths, bead_id)
    phase_hint = RunPhase.plan if bead.status in {BeadStatus.draft, BeadStatus.sized} else RunPhase.implement
    if bead.status in {
        BeadStatus.verification_pending,
        BeadStatus.verified,
        BeadStatus.approval_pending,
        BeadStatus.done,
    }:
        phase_hint = RunPhase.verify

    from_status, _, to_status = transition.partition("->")
    from_status = from_status.strip()
    to_status = to_status.strip()
    if from_status != bead.status.value:
        return TransitionResult(
            False,
            (
                "Illegal transition: bead is "
                f"'{bead.status.value}', request was '{from_status} -> {to_status}'"
            ),
            phase=_phase_for_transition(from_status, to_status),
        )
    if not allowed_transition(from_status, to_status):
        return TransitionResult(
            False,
            f"Illegal transition: '{from_status} -> {to_status}' is not allowed",
            phase=_phase_for_transition(from_status, to_status),
        )

    authority = TRANSITION_AUTHORITY.get((from_status, to_status))
    if authority is not None and actor.kind not in authority:
        return TransitionResult(
            False,
            (
                f"Authority violation: {actor.kind} may not request '{from_status}->{to_status}' "
                f"(requires: {sorted(authority)})"
            ),
            phase=phase_hint,
        )

    errors: list[str] = []
    info_notes: list[str] = []
    links: list[ArtifactLink] = []
    boundary_eval: Optional[BoundaryEvaluation] = None
    changed_files: Optional[list[str]] = None
    force_abort = False

    def ensure_boundary_eval() -> BoundaryEvaluation:
        nonlocal boundary_eval, changed_files
        if boundary_eval is None:
            changed_files = detect_changed_files(paths)
            boundary_eval = evaluate_boundary(paths, bead, changed_files=changed_files)
            links.append(_boundary_link(boundary_eval.registry))
            if bead.boundary_registry_ref is None and boundary_eval.registry_path is not None:
                info_notes.append(
                    f"boundary_registry_default={boundary_eval.registry_path.as_posix()}"
                )
            info_notes.append(f"boundary_registry_hash={boundary_eval.registry_hash.hash}")
        return boundary_eval

    artifact_error = ensure_bead_artifact_id(bead)
    if artifact_error:
        errors.append(artifact_error)

    if bead.status == BeadStatus.draft and to_status == BeadStatus.sized.value:
        pass
    elif bead.status == BeadStatus.sized and to_status == BeadStatus.ready.value:
        review = load_bead_review(paths, bead_id)
        review_error = _require_review_for_ready(bead, review)
        if review_error:
            errors.append(review_error)
        plan_error = _plan_gate_bucket_l(paths, bead_id, review)
        if plan_error:
            errors.append(plan_error)
        if not errors:
            apply_acceptance_checks_from_review(bead, review)
            _write_ready_acceptance_snapshot(paths, bead)
    elif bead.status == BeadStatus.ready and to_status == BeadStatus.in_progress.value:
        review = load_bead_review(paths, bead_id)
        if review and not acceptance_checks_equal(
            bead.acceptance_checks, review.tightened_acceptance_checks
        ):
            errors.append("Acceptance checks changed after ready")
        snapshot = _load_ready_acceptance_snapshot(paths, bead_id)
        if snapshot is None:
            errors.append("Acceptance checks snapshot missing after ready")
        else:
            expected_hash = snapshot.get("acceptance_checks_hash")
            if expected_hash != canonical_hash_for_acceptance_checks(bead.acceptance_checks).hash:
                errors.append("Acceptance checks changed after ready")
        dependency_result = _dependencies_gate(paths, bead)
        if not dependency_result.ok:
            errors.append(dependency_result.notes)
        spec_error = _spec_gate(paths, bead)
        if spec_error:
            errors.append(spec_error)
        profile_error = _execution_profile_gate(paths, bead)
        if profile_error:
            errors.append(profile_error)
        grounding_error = _grounding_gate(paths, bead)
        if grounding_error:
            errors.append(grounding_error)
    elif bead.status == BeadStatus.in_progress and to_status == BeadStatus.verification_pending.value:
        pass
    elif bead.status == BeadStatus.verification_pending and to_status == BeadStatus.verified.value:
        evidence_error = _evidence_gate(paths, bead)
        if evidence_error:
            errors.append(evidence_error)
        try:
            evaluation = ensure_boundary_eval()
            max_files = _env_int("SDLC_MAX_FILES_TOUCHED", 8)
            max_subsystems = _env_int("SDLC_MAX_SUBSYSTEMS_TOUCHED", 2)
            info_notes.append(
                "boundary_evaluation="
                f"files_touched:{evaluation.files_touched},"
                f"subsystems_touched:{len(evaluation.touched_subsystems)}"
            )
            if (
                evaluation.files_touched > max_files
                or len(evaluation.touched_subsystems) > max_subsystems
            ):
                info_notes.append(
                    boundary_violation_notes(evaluation, max_files, max_subsystems)
                )
                info_notes.append(
                    "Boundary limit exceeded: forcing abort to aborted:needs-discovery"
                )
                force_abort = True
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
        anti_stall = anti_stall_errors(paths, bead)
        if anti_stall:
            errors.extend(anti_stall)
            errors.append("Anti-stall threshold exceeded: abort required")
    elif bead.status == BeadStatus.verified and to_status == BeadStatus.approval_pending.value:
        pass
    elif bead.status == BeadStatus.approval_pending and to_status == BeadStatus.done.value:
        approval_error = _approval_gate(paths, bead)
        if approval_error:
            errors.append(approval_error)
    elif to_status in FAILURE_TARGETS:
        pass

    if bead.bead_type == BeadType.discovery and to_status in {
        BeadStatus.in_progress.value,
        BeadStatus.verified.value,
    }:
        try:
            evaluation = ensure_boundary_eval()
            allowlist = _discovery_allowlist()
            info_notes.append(
                "discovery_policy=Policy A;"
                f"allowlist={allowlist};"
                f"production_prefixes={evaluation.production_prefixes}"
            )
            normalized_files = [_normalize_prefix(path) for path in (changed_files or [])]
            outside_allowlist = [
                path
                for path in normalized_files
                if not any(path.startswith(prefix) for prefix in allowlist)
            ]
            production_hits = [
                path
                for path in normalized_files
                if any(path.startswith(prefix) for prefix in evaluation.production_prefixes)
            ]
            if outside_allowlist or production_hits:
                parts = ["Discovery policy violation (Policy A)"]
                if production_hits:
                    parts.append(f"production_paths_hit={sorted(set(production_hits))}")
                if outside_allowlist:
                    parts.append(f"outside_allowlist={sorted(set(outside_allowlist))}")
                parts.append(f"allowlist={allowlist}")
                parts.append(f"boundary_registry_hash={evaluation.registry_hash.hash}")
                errors.append("; ".join(parts))
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))

    notes = "; ".join(errors) if errors else ""
    if info_notes:
        extra = "; ".join(info_notes)
        notes = f"{notes}; {extra}".strip("; ").strip()

    if force_abort:
        _apply_transition(bead, BeadStatus.aborted_needs_discovery)
        write_model(paths.bead_path(bead_id), bead)
        return TransitionResult(
            True,
            notes,
            applied_transition=f"{from_status} -> {BeadStatus.aborted_needs_discovery.value}",
            phase=phase_hint,
            links=links,
            auto_abort=True,
        )

    if errors:
        return TransitionResult(False, notes, phase=phase_hint, links=links)

    _apply_transition(bead, BeadStatus(to_status))
    write_model(paths.bead_path(bead_id), bead)
    return TransitionResult(
        True,
        notes,
        applied_transition=f"{from_status} -> {to_status}",
        phase=phase_hint,
        links=links,
    )


def build_execution_record(
    bead_id: str,
    phase: RunPhase,
    actor: Actor,
    requested_transition: Optional[str] = None,
    applied_transition: Optional[str] = None,
    exit_code: Optional[int] = None,
    notes_md: Optional[str] = None,
    git: Optional[GitRef] = None,
    produced_artifacts: Optional[list[FileRef]] = None,
    links: Optional[list[ArtifactLink]] = None,
) -> ExecutionRecord:
    return ExecutionRecord(
        artifact_id=f"exec-{bead_id}-{int(now_utc().timestamp())}",
        created_at=now_utc(),
        created_by=actor,
        bead_id=bead_id,
        phase=phase,
        exit_code=exit_code,
        notes_md=notes_md,
        requested_transition=requested_transition,
        applied_transition=applied_transition,
        git=git,
        produced_artifacts=produced_artifacts or [],
        links=links or [],
        schema_name="sdlc.execution_record",
        schema_version=1,
    )


def decision_ledger_link(entry: DecisionLedgerEntry) -> ArtifactLink:
    return ArtifactLink(
        artifact_type="decision_ledger_entry",
        artifact_id=entry.artifact_id,
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
    )


def _phase_for_abort_decision(from_status: str) -> RunPhase:
    if from_status in {
        BeadStatus.draft.value,
        BeadStatus.sized.value,
        BeadStatus.ready.value,
    }:
        return RunPhase.plan
    return RunPhase.verify


def record_decision_action(
    paths: Paths,
    decision: DecisionLedgerEntry,
    phase: RunPhase,
    actor: Actor,
    notes_md: Optional[str] = None,
) -> ExecutionRecord:
    if not decision.bead_id:
        raise ValueError("DecisionLedgerEntry.bead_id required for decision action record")
    record = build_execution_record(
        decision.bead_id,
        phase,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0,
        notes_md=notes_md,
        links=[decision_ledger_link(decision)],
    )
    write_execution_record(paths, record)
    return record


def _decision_action_phase_for_bead(paths: Paths, bead_id: str) -> RunPhase:
    bead = load_bead(paths, bead_id)
    return _phase_for_abort_decision(bead.status.value)


def collect_evidence_skeleton(bead: Bead, actor: Actor) -> EvidenceBundle:
    items = [
        EvidenceItem(
            name=check.name,
            evidence_type=EvidenceType.test_run,
            command=check.command,
        )
        for check in bead.acceptance_checks
    ]
    return EvidenceBundle(
        artifact_id=f"evidence-{bead.bead_id}",
        created_at=now_utc(),
        created_by=actor,
        bead_id=bead.bead_id,
        for_bead_hash=canonical_hash_for_model(bead),
        items=items,
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
    )


def evidence_validation_errors(
    bead: Bead,
    evidence: EvidenceBundle,
    decision_entries: Iterable[DecisionLedgerEntry],
) -> list[str]:
    errors: list[str] = []

    manual_items = [item for item in evidence.items if item.evidence_type == EvidenceType.manual_check]
    if manual_items:
        if evidence.created_by.kind != "human":
            errors.append("Manual check evidence requires human bundle creator")
        for item in manual_items:
            if not item.summary_md or not item.summary_md.strip():
                errors.append("Manual check evidence requires summary_md")

    bead_hash = canonical_hash_for_model(bead)
    if evidence.for_bead_hash is None:
        errors.append("EvidenceBundle.for_bead_hash missing")
    elif evidence.for_bead_hash.hash != bead_hash.hash:
        errors.append("EvidenceBundle.for_bead_hash does not match bead hash; evidence is stale")

    coverage_errors = acceptance_coverage_errors(bead, evidence, decision_entries)
    errors.extend(coverage_errors)

    for check in bead.acceptance_checks:
        if getattr(check, "kind", "command") != "command":
            continue
        item = _find_item_for_check(evidence, check)
        if item is None:
            errors.append(f"Missing evidence for command check '{check.name}'")
            continue
        if item.exit_code is None:
            errors.append(f"Evidence item {item.name} missing exit_code")
            continue
        if item.exit_code != check.expect_exit_code:
            errors.append(
                f"Evidence item {item.name} expected exit_code {check.expect_exit_code} "
                f"got {item.exit_code}"
            )

    return errors


def _find_item_for_check(evidence: EvidenceBundle, check: AcceptanceCheck) -> Optional[EvidenceItem]:
    for item in evidence.items:
        if item.name == check.name:
            return item
    if check.command:
        for item in evidence.items:
            if item.command == check.command:
                return item
    return None


def acceptance_coverage_errors(
    bead: Bead, evidence: EvidenceBundle, decision_entries: Iterable[DecisionLedgerEntry]
) -> list[str]:
    errors: list[str] = []
    waived: set[str] = set()
    for entry in decision_entries:
        if entry.decision_type == DecisionType.exception and entry.bead_id == bead.bead_id:
            waived.update(entry.waived_acceptance_checks)

    for check in bead.acceptance_checks:
        if check.name in waived:
            continue
        if _covered_by_command(check, evidence):
            continue
        if _covered_by_human_summary(check, evidence):
            continue
        if _covered_by_output(check, evidence):
            continue
        errors.append(f"Acceptance check '{check.name}' not covered")
    return errors


def _covered_by_command(check: AcceptanceCheck, evidence: EvidenceBundle) -> bool:
    for item in evidence.items:
        if item.command == check.command and item.exit_code == check.expect_exit_code:
            return True
    return False


def _covered_by_human_summary(check: AcceptanceCheck, evidence: EvidenceBundle) -> bool:
    if evidence.created_by.kind != "human":
        return False
    for item in evidence.items:
        if item.summary_md and check.name in item.summary_md:
            return True
    return False


def _covered_by_output(check: AcceptanceCheck, evidence: EvidenceBundle) -> bool:
    if not check.expected_outputs:
        return False
    expected = {(ref.path, ref.content_hash.hash if ref.content_hash else None) for ref in check.expected_outputs}
    for item in evidence.items:
        for attachment in item.attachments:
            key = (attachment.path, attachment.content_hash.hash if attachment.content_hash else None)
            if key in expected:
                return True
    return False


def validate_evidence_bundle(
    paths: Paths, bead_id: str, actor: Actor, mark_validated: bool = True
) -> tuple[Optional[EvidenceBundle], list[str]]:
    bead = load_bead(paths, bead_id)
    evidence = load_evidence(paths, bead_id)
    if evidence is None:
        return None, ["EvidenceBundle missing"]
    errors = evidence_validation_errors(bead, evidence, load_decision_ledger(paths))
    if errors:
        return evidence, errors
    if mark_validated:
        evidence.status = EvidenceStatus.validated
        evidence.for_bead_hash = canonical_hash_for_model(bead)
        write_model(paths.evidence_path(bead_id), evidence)
    return evidence, []


def invalidate_evidence_if_stale(paths: Paths, bead_id: str, actor: Actor) -> Optional[str]:
    evidence = load_evidence(paths, bead_id)
    if evidence is None:
        return None
    if evidence.status != EvidenceStatus.validated:
        return None

    reasons: list[str] = []
    bead = load_bead(paths, bead_id)
    bead_hash = canonical_hash_for_model(bead)
    if evidence.for_bead_hash is None or evidence.for_bead_hash.hash != bead_hash.hash:
        reasons.append("bead hash changed")

    head = git_head(paths)
    dirty = git_is_dirty(paths)
    validation_record = None
    expected_artifact_path = f"runs/{bead_id}/evidence.json"
    for record in reversed(load_execution_records(paths)):
        if record.bead_id != bead_id:
            continue
        if record.phase != RunPhase.verify:
            continue
        if record.exit_code != 0:
            continue
        if not any(ref.path == expected_artifact_path for ref in record.produced_artifacts):
            continue
        if record.git is None:
            continue
        validation_record = record
        break

    if validation_record and validation_record.git:
        if (
            head is not None
            and validation_record.git.head_before
            and validation_record.git.head_before != head
        ):
            reasons.append("git head changed")
        if (
            dirty is not None
            and validation_record.git.dirty_before is not None
            and validation_record.git.dirty_before != dirty
        ):
            reasons.append("git dirty state changed")

    if not reasons:
        return None

    evidence.status = EvidenceStatus.invalidated
    evidence.invalidated_reason = "; ".join(sorted(set(reasons)))
    write_model(paths.evidence_path(bead_id), evidence)
    record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=1,
        notes_md=f"Evidence invalidated: {evidence.invalidated_reason}",
        git=GitRef(head_before=head, dirty_before=dirty),
    )
    write_execution_record(paths, record)
    return evidence.invalidated_reason


def generate_grounding_bundle(paths: Paths, bead_id: str, actor: Actor) -> None:
    bead = load_bead(paths, bead_id)
    items = []
    for path in ["README.md", "docs/loom-specification.md", "openspec/changes/bootstrap-agentic-sdlc-v1/proposal.md"]:
        file_path = paths.repo_root / path
        if file_path.exists():
            items.append(
                {
                    "kind": "file",
                    "title": path,
                    "content_md": file_path.read_text(encoding="utf-8")[:2000],
                    "file_ref": {"path": path},
                }
            )
    payload = {
        "schema_name": "sdlc.grounding_bundle",
        "schema_version": 1,
        "artifact_id": f"grounding-{bead_id}",
        "created_at": now_utc(),
        "created_by": actor,
        "bead_id": bead_id,
        "generated_for_bead_hash": canonical_hash_for_model(bead),
        "items": items,
        "allowed_commands": ["uv run pytest -q"],
        "disallowed_commands": ["rm -rf /"],
        "excluded_paths": ["runs/"],
        "summary_md": "Auto-generated grounding bundle",
    }
    grounding = GroundingBundle.model_validate(payload)
    write_model(paths.grounding_path(bead_id), grounding)


def append_decision_entry(paths: Paths, entry: DecisionLedgerEntry) -> None:
    write_decision_entry(paths, entry)


def find_active_exception_decision(
    paths: Paths, bead_id: str
) -> Optional[DecisionLedgerEntry]:
    most_recent: Optional[DecisionLedgerEntry] = None
    now = now_utc()
    for entry in load_decision_ledger(paths):
        if entry.decision_type != DecisionType.exception:
            continue
        if entry.bead_id != bead_id:
            continue
        if entry.expires_at is not None and entry.expires_at <= now:
            continue
        if not entry.summary.strip():
            continue
        if most_recent is None or entry.created_at > most_recent.created_at:
            most_recent = entry
    return most_recent


def find_approval_decision(paths: Paths, bead_id: str) -> Optional[DecisionLedgerEntry]:
    most_recent: Optional[DecisionLedgerEntry] = None
    for entry in load_decision_ledger(paths):
        if entry.decision_type != DecisionType.approval:
            continue
        if entry.bead_id != bead_id:
            continue
        if entry.created_by.kind != "human":
            continue
        if not entry.summary.strip():
            continue
        if most_recent is None or entry.created_at > most_recent.created_at:
            most_recent = entry
    return most_recent


def record_transition_attempt(
    paths: Paths,
    bead_id: str,
    phase: RunPhase,
    actor: Actor,
    requested: str,
    result: TransitionResult,
    extra_links: Optional[list[ArtifactLink]] = None,
) -> ExecutionRecord:
    phase_value = result.phase or phase
    git_ref = GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths))
    links: list[ArtifactLink] = list(extra_links) if extra_links else []
    if result.links:
        links.extend(result.links)
    notes_md = result.notes or None
    if result.auto_abort:
        decision = create_abort_entry(
            bead_id, "ABORT: boundary or anti-stall enforcement", actor
        )
        write_decision_entry(paths, decision)
        if result.applied_transition:
            from_status = result.applied_transition.split("->", 1)[0].strip()
            decision_phase = _phase_for_abort_decision(from_status)
        else:
            decision_phase = RunPhase.verify
        record_decision_action(paths, decision, decision_phase, actor)
        links.append(decision_ledger_link(decision))
        engine_note = "Engine-applied abort"
        notes_md = f"{engine_note}; {notes_md}" if notes_md else engine_note
    if result.ok and result.applied_transition:
        transition = result.applied_transition.strip()
        if transition == "ready -> in_progress":
            bead = load_bead(paths, bead_id)
            if bead.execution_profile == ExecutionProfile.exception:
                entry = find_active_exception_decision(paths, bead_id)
                if entry is not None:
                    links.append(decision_ledger_link(entry))
        elif transition == "approval_pending -> done":
            entry = find_approval_decision(paths, bead_id)
            if entry is not None:
                links.append(decision_ledger_link(entry))
    record = build_execution_record(
        bead_id,
        phase_value,
        actor,
        requested_transition=requested,
        applied_transition=result.applied_transition if result.ok else None,
        exit_code=0 if result.ok else 1,
        notes_md=notes_md,
        git=git_ref,
        links=links,
    )
    write_execution_record(paths, record)
    return record


def create_approval_entry(bead_id: str, summary: str, actor: Actor) -> DecisionLedgerEntry:
    return DecisionLedgerEntry(
        artifact_id=f"decision-{bead_id}-{int(now_utc().timestamp())}",
        created_at=now_utc(),
        created_by=actor,
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        bead_id=bead_id,
        decision_type=DecisionType.approval,
        summary=summary,
    )


def create_abort_entry(bead_id: str, reason: str, actor: Actor) -> DecisionLedgerEntry:
    summary = reason.strip()
    if not summary.startswith("ABORT:"):
        summary = f"ABORT: {summary}"
    return DecisionLedgerEntry(
        artifact_id=f"decision-{bead_id}-{int(now_utc().timestamp())}",
        created_at=now_utc(),
        created_by=actor,
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        bead_id=bead_id,
        decision_type=DecisionType.scope_change,
        summary=summary,
    )


def policy_violation_record(
    bead_id: str, actor: Actor, note: str, links: Optional[list[ArtifactLink]] = None
) -> ExecutionRecord:
    return build_execution_record(
        bead_id,
        RunPhase.implement,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=1,
        notes_md=note,
        links=links,
    )
````

## File: tests/test_sdlc.py
````python
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest
import typer
from pydantic import ValidationError

from sdlc.codec import sha256_canonical_json
from sdlc.engine import acceptance_coverage_errors, build_execution_record, canonical_hash_for_model
from sdlc.cli import app
from sdlc.models import (
    Actor,
    AcceptanceCheck,
    ArtifactLink,
    Bead,
    RunPhase,
    BeadStatus,
    BeadType,
    DecisionLedgerEntry,
    DecisionType,
    EffortBucket,
    EvidenceBundle,
    EvidenceItem,
    EvidenceStatus,
    EvidenceType,
    BeadReview,
    BoundaryRegistry,
    GroundingBundle,
    HashRef,
    FileRef,
    GitRef,
    OpenSpecRef,
    OpenSpecState,
    Subsystem,
)
from sdlc.cli import abort, approve, evidence_validate, openspec_sync, request


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _write_boundary_registry(paths: "Paths") -> None:
    (paths.repo_root / "sdlc").mkdir(parents=True, exist_ok=True)
    (paths.repo_root / "sdlc" / "boundary_registry.json").write_text(
        json.dumps(
            {
                "schema_name": "sdlc.boundary_registry",
                "schema_version": 1,
                "artifact_id": "boundary-registry-test",
                "created_at": _now().isoformat(),
                "created_by": {"kind": "system", "name": "tester"},
                "registry_name": "test",
                "subsystems": [{"name": "docs", "paths": ["docs/"]}],
            }
        ),
        encoding="utf-8",
    )


def _write_boundary_registry_with(
    paths: "Paths",
    subsystems: list[dict[str, object]],
    artifact_id: str = "boundary-registry-test",
) -> None:
    (paths.repo_root / "sdlc").mkdir(parents=True, exist_ok=True)
    (paths.repo_root / "sdlc" / "boundary_registry.json").write_text(
        json.dumps(
            {
                "schema_name": "sdlc.boundary_registry",
                "schema_version": 1,
                "artifact_id": artifact_id,
                "created_at": _now().isoformat(),
                "created_by": {"kind": "system", "name": "tester"},
                "registry_name": "test",
                "subsystems": subsystems,
            }
        ),
        encoding="utf-8",
    )


def test_schema_extra_forbidden() -> None:
    payload = {
        "schema_name": "sdlc.bead",
        "schema_version": 1,
        "artifact_id": "work-abc123",
        "created_at": _now(),
        "created_by": {"kind": "system", "name": "tester"},
        "bead_id": "work-abc123",
        "title": "Test",
        "bead_type": "implementation",
        "status": "draft",
        "requirements_md": "req",
        "acceptance_criteria_md": "acc",
        "context_md": "ctx",
        "extra_field": "nope",
    }
    with pytest.raises(ValidationError):
        Bead.model_validate(payload)


def test_hash_deterministic() -> None:
    content = {"b": 2, "a": 1, "nested": {"z": 9, "y": 8}}
    first = sha256_canonical_json(content)
    second = sha256_canonical_json({"nested": {"y": 8, "z": 9}, "a": 1, "b": 2})
    assert first == second


def test_compute_touched_subsystems_by_prefix() -> None:
    from sdlc.engine import compute_touched_subsystems

    registry = BoundaryRegistry(
        schema_name="sdlc.boundary_registry",
        schema_version=1,
        artifact_id="boundary-registry-test",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        registry_name="test",
        subsystems=[
            Subsystem(name="core", paths=["src/"]),
            Subsystem(name="docs", paths=["docs/", "README.md"]),
        ],
    )
    touched, files_touched = compute_touched_subsystems(
        registry,
        ["src/sdlc/engine.py", "docs/guide.md", "README.md", "scripts/tool.sh"],
    )
    assert files_touched == 4
    assert touched == ["core", "docs"]


def test_boundary_enforcement_blocks_verification_and_links_registry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import record_transition_attempt, request_transition
    from sdlc.io import Paths, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry_with(
        paths,
        subsystems=[
            {"name": "core", "paths": ["src/"]},
            {"name": "docs", "paths": ["docs/"]},
        ],
        artifact_id="boundary-registry-enforce",
    )
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.validated,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    monkeypatch.setenv("SDLC_MAX_FILES_TOUCHED", "1")
    monkeypatch.setenv("SDLC_MAX_SUBSYSTEMS_TOUCHED", "1")
    monkeypatch.setattr(
        "sdlc.engine.detect_changed_files",
        lambda _: ["src/sdlc/engine.py", "docs/guide.md"],
    )

    actor = Actor(kind="system", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    assert result.ok
    assert result.applied_transition == "verification_pending -> aborted:needs-discovery"
    assert "Boundary violation" in result.notes

    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "verification_pending -> verified", result
    )
    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert any(
        link.artifact_type == "boundary_registry" and link.artifact_id == "boundary-registry-enforce"
        for link in last.links
    )


def test_discovery_policy_blocks_production_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import record_transition_attempt, request_transition, _write_ready_acceptance_snapshot
    from sdlc.io import Paths, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry_with(
        paths,
        subsystems=[{"name": "core", "paths": ["src/"]}],
        artifact_id="boundary-registry-discovery",
    )
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.grounding_path(bead_id), grounding)
    _write_ready_acceptance_snapshot(paths, bead)
    monkeypatch.setattr(
        "sdlc.engine.detect_changed_files",
        lambda _: ["src/main.py", "docs/notes.md"],
    )

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert not result.ok
    assert "Discovery policy violation" in result.notes

    record_transition_attempt(
        paths, bead_id, RunPhase.implement, actor, "ready -> in_progress", result
    )
    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.applied_transition is None
    assert any(link.artifact_type == "boundary_registry" for link in last.links)


def test_discovery_policy_allows_allowlist(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import record_transition_attempt, request_transition, _write_ready_acceptance_snapshot
    from sdlc.io import Paths, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry_with(
        paths,
        subsystems=[{"name": "core", "paths": ["src/"]}],
        artifact_id="boundary-registry-discovery",
    )
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.grounding_path(bead_id), grounding)
    _write_ready_acceptance_snapshot(paths, bead)
    monkeypatch.setattr(
        "sdlc.engine.detect_changed_files",
        lambda _: ["docs/notes.md"],
    )

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert result.ok

    record_transition_attempt(
        paths, bead_id, RunPhase.implement, actor, "ready -> in_progress", result
    )
    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.applied_transition == "ready -> in_progress"
    assert any(link.artifact_type == "boundary_registry" for link in last.links)


def test_grounding_generate_writes_bundle(tmp_path: Path) -> None:
    from sdlc.engine import generate_grounding_bundle
    from sdlc.io import Paths, write_model

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    generate_grounding_bundle(paths, bead_id, Actor(kind="system", name="tester"))

    grounding_path = paths.grounding_path(bead_id)
    assert grounding_path.exists()
    GroundingBundle.model_validate_json(grounding_path.read_text(encoding="utf-8"))


def test_schema_export_alias_command_works(tmp_path: Path) -> None:
    from typer.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(app, ["schema", "export", "--out", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert list(tmp_path.glob("*.json"))


def test_manual_check_requires_human_summary() -> None:
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-abc123",
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="agent", name="tester"),
        bead_id=bead.bead_id,
        status=EvidenceStatus.collected,
        items=[
            EvidenceItem(
                name="manual",
                evidence_type=EvidenceType.manual_check,
                summary_md=None,
            )
        ],
    )
    from sdlc.engine import evidence_validation_errors

    errors = evidence_validation_errors(bead, evidence, [])
    assert "Manual check evidence requires summary_md" in errors
    assert "Manual check evidence requires human bundle creator" in errors


def test_acceptance_coverage_missing() -> None:
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-abc123",
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[
            AcceptanceCheck(name="run", command="uv run pytest -q", expect_exit_code=0)
        ],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        status=EvidenceStatus.collected,
        items=[],
    )
    errors = acceptance_coverage_errors(bead, evidence, [])
    assert "Acceptance check 'run' not covered" in errors


def test_acceptance_coverage_exception_waiver_allows_validation() -> None:
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-abc123",
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[
            AcceptanceCheck(name="run", command="uv run pytest -q", expect_exit_code=0)
        ],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        status=EvidenceStatus.collected,
        items=[],
    )
    decision = DecisionLedgerEntry(
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        artifact_id="decision-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        bead_id=bead.bead_id,
        decision_type=DecisionType.exception,
        summary="Waive check",
        waived_acceptance_checks=["run"],
    )
    errors = acceptance_coverage_errors(bead, evidence, [decision])
    assert not errors


def test_find_item_for_check_no_kind_field_does_not_crash() -> None:
    from sdlc.engine import evidence_validation_errors

    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-abc123",
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[
            AcceptanceCheck(name="missing", command="uv run pytest -q", expect_exit_code=0)
        ],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        for_bead_hash=canonical_hash_for_model(bead),
        status=EvidenceStatus.collected,
        items=[
            EvidenceItem(
                name="other",
                evidence_type=EvidenceType.test_run,
                command="uv run pytest -q --not-it",
                exit_code=0,
            )
        ],
    )

    errors = evidence_validation_errors(bead, evidence, [])
    assert "Missing evidence for command check 'missing'" in errors


def test_illegal_transition_record_shape(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import record_transition_attempt, TransitionResult
    from sdlc.models import RunPhase

    repo = tmp_path
    paths = Paths(repo)
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-abc123",
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead.bead_id), bead)
    actor = Actor(kind="system", name="tester")
    result = TransitionResult(False, "Illegal transition")
    record = record_transition_attempt(
        paths,
        bead.bead_id,
        RunPhase.plan,
        actor,
        "draft -> ready",
        result,
    )
    assert record.exit_code == 1
    assert record.requested_transition == "draft -> ready"
    assert record.applied_transition is None
    assert record.phase == RunPhase.plan
    assert record.notes_md


def test_transition_authority_system_only(tmp_path: Path) -> None:
    from sdlc.engine import request_transition
    from sdlc.io import Paths, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)

    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    actor = Actor(kind="agent", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    assert not result.ok
    assert "Authority violation" in result.notes


def test_illegal_transition_notes_are_specific(tmp_path: Path) -> None:
    from sdlc.engine import request_transition
    from sdlc.io import Paths, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)

    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "sized -> in_progress", actor)
    assert result.ok is False
    assert "bead is 'ready'" in result.notes
    assert "sized -> in_progress" in result.notes


def test_request_records_phase_from_transition(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from sdlc.io import Paths, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)

    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    request(bead_id, "draft -> sized", actor_kind="system", actor_name="tester")

    journal_path = paths.runs_dir / "journal.jsonl"
    lines = journal_path.read_text(encoding="utf-8").splitlines()
    assert lines, "journal.jsonl should have at least one entry"
    last = json.loads(lines[-1])
    assert last["phase"] == RunPhase.plan.value
    assert last["requested_transition"] == "draft -> sized"


def test_exception_profile_links_decision_on_start(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.io import Paths, load_decision_ledger, load_execution_records, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        execution_profile="exception",
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.M,
        tightened_acceptance_checks=bead.acceptance_checks,
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)
    write_model(paths.grounding_path(bead_id), grounding)

    from sdlc.engine import append_decision_entry, _write_ready_acceptance_snapshot

    _write_ready_acceptance_snapshot(paths, bead)
    decision = DecisionLedgerEntry(
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        artifact_id="decision-exc-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="approver"),
        bead_id=bead_id,
        decision_type=DecisionType.exception,
        summary="Exception granted",
    )
    append_decision_entry(paths, decision)

    request(bead_id, "ready -> in_progress", actor_kind="human", actor_name="tester")

    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.applied_transition == "ready -> in_progress"
    assert any(
        link.artifact_id == decision.artifact_id and link.artifact_type == "decision_ledger_entry"
        for link in last.links
    )
    assert list(load_decision_ledger(paths))


def test_approval_links_decision_on_done(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from sdlc.io import Paths, load_execution_records, write_model
    from sdlc.engine import record_transition_attempt, request_transition

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    actor = Actor(kind="human", name="tester")
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.approval_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    from sdlc.engine import append_decision_entry

    decision = DecisionLedgerEntry(
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        artifact_id="decision-appr-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="approver"),
        bead_id=bead_id,
        decision_type=DecisionType.approval,
        summary="APPROVAL: ok",
    )
    append_decision_entry(paths, decision)

    result = request_transition(paths, bead_id, "approval_pending -> done", actor)
    assert result.ok
    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "approval_pending -> done", result
    )

    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.applied_transition == "approval_pending -> done"
    assert any(
        link.artifact_id == decision.artifact_id and link.artifact_type == "decision_ledger_entry"
        for link in last.links
    )


def test_exception_profile_requires_decision_and_no_applied_transition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.io import Paths, load_execution_records, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        execution_profile="exception",
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.M,
        tightened_acceptance_checks=bead.acceptance_checks,
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)
    write_model(paths.grounding_path(bead_id), grounding)

    from sdlc.engine import _write_ready_acceptance_snapshot

    _write_ready_acceptance_snapshot(paths, bead)

    with pytest.raises(typer.Exit):
        request(bead_id, "ready -> in_progress", actor_kind="human", actor_name="tester")

    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.applied_transition is None

def test_approve_allows_non_prefixed_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from sdlc.io import Paths, load_decision_ledger

    monkeypatch.chdir(tmp_path)
    approve("work-abc123", summary="Looks good to me")
    captured = capsys.readouterr()
    assert 'Warning: summary should start with "APPROVAL:"' in captured.err
    entries = list(load_decision_ledger(Paths(Path.cwd())))
    assert entries
    assert entries[-1].decision_type == DecisionType.approval
    assert entries[-1].created_by.kind == "human"


def test_authority_blocks_system_only_transition_for_human(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    assert result.ok is False
    assert "Authority violation" in result.notes


def test_request_failure_journals_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from sdlc.io import Paths, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.draft,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    with pytest.raises(typer.Exit):
        request(bead_id, "draft -> ready", actor_kind="human", actor_name="tester")

    journal_path = paths.runs_dir / "journal.jsonl"
    lines = journal_path.read_text(encoding="utf-8").splitlines()
    assert lines
    last = json.loads(lines[-1])
    assert last["requested_transition"] == "draft -> ready"
    assert last["applied_transition"] is None
    assert last["exit_code"] != 0
    assert last["phase"] == RunPhase.plan.value


def test_evidence_validate_requires_expected_exit_code_match(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import validate_evidence_bundle

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=2)],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        items=[EvidenceItem(name="cmd", evidence_type=EvidenceType.test_run, command="run", exit_code=0)],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    _, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert any("expected exit_code 2" in error for error in errors)


def test_evidence_validate_allows_nonzero_expected_exit_code(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import validate_evidence_bundle, canonical_hash_for_model

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=2)],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[EvidenceItem(name="cmd", evidence_type=EvidenceType.test_run, command="run", exit_code=2)],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    evidence_after, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert evidence_after is not None
    assert evidence_after.status == EvidenceStatus.validated
    assert not errors


def test_evidence_validation_prefers_name_over_command(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import validate_evidence_bundle, canonical_hash_for_model

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[
            AcceptanceCheck(name="cmd-ok", command="run", expect_exit_code=0),
            AcceptanceCheck(name="cmd-fail", command="run", expect_exit_code=2),
        ],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[
            EvidenceItem(
                name="cmd-ok",
                evidence_type=EvidenceType.test_run,
                command="run",
                exit_code=0,
            ),
            EvidenceItem(
                name="cmd-fail",
                evidence_type=EvidenceType.test_run,
                command="run",
                exit_code=2,
            ),
        ],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    evidence_after, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert evidence_after is not None
    assert evidence_after.status == EvidenceStatus.validated
    assert not errors


def test_evidence_validate_rejects_bead_hash_mismatch(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import validate_evidence_bundle

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=0)],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        for_bead_hash=HashRef(hash_alg="sha256", hash="0" * 64),
        items=[EvidenceItem(name="cmd", evidence_type=EvidenceType.test_run, command="run", exit_code=0)],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    evidence_after, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert evidence_after is not None
    assert evidence_after.status == EvidenceStatus.collected
    assert any("bead hash" in error for error in errors)


def test_evidence_validate_sets_status_validated_on_success(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import validate_evidence_bundle, canonical_hash_for_model

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=0)],
    )
    bead_hash = canonical_hash_for_model(bead)
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        for_bead_hash=bead_hash,
        items=[EvidenceItem(name="cmd", evidence_type=EvidenceType.test_run, command="run", exit_code=0)],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    evidence_after, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert evidence_after is not None
    assert not errors
    assert evidence_after.status == EvidenceStatus.validated


def test_acceptance_checks_frozen_after_ready_requires_snapshot_match(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.sized,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=0)],
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.M,
        tightened_acceptance_checks=bead.acceptance_checks,
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)
    write_model(paths.grounding_path(bead_id), grounding)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "sized -> ready", actor)
    assert result.ok

    bead = Bead.model_validate_json(paths.bead_path(bead_id).read_text(encoding="utf-8"))
    bead.acceptance_checks.append(
        AcceptanceCheck(name="mutated", command="other", expect_exit_code=0)
    )
    write_model(paths.bead_path(bead_id), bead)

    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert not result.ok
    assert "Acceptance checks changed after ready" in result.notes


def test_full_flow_smoke(tmp_path: Path) -> None:
    from sdlc.engine import (
        append_decision_entry,
        create_approval_entry,
        record_transition_attempt,
        request_transition,
        validate_evidence_bundle,
    )
    from sdlc.io import Paths, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    actor = Actor(kind="human", name="tester")
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.sized,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="run", command="run", expect_exit_code=0)],
        openspec_ref=ArtifactLink(artifact_type="openspec_ref", artifact_id="openspec-abc123"),
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.M,
        tightened_acceptance_checks=bead.acceptance_checks,
    )
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    openspec_ref = OpenSpecRef(
        schema_name="sdlc.openspec_ref",
        schema_version=1,
        artifact_id="openspec-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        change_id="add-thing",
        state=OpenSpecState.approved,
        path="openspec/changes/add-thing",
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)
    write_model(paths.grounding_path(bead_id), grounding)
    write_model(paths.bead_dir(bead_id) / "openspec_ref.json", openspec_ref)

    result = request_transition(paths, bead_id, "sized -> ready", actor)
    assert result.ok
    record_transition_attempt(paths, bead_id, RunPhase.plan, actor, "sized -> ready", result)

    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert result.ok
    record_transition_attempt(paths, bead_id, RunPhase.implement, actor, "ready -> in_progress", result)

    current_bead = Bead.model_validate_json(paths.bead_path(bead_id).read_text(encoding="utf-8"))
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        for_bead_hash=canonical_hash_for_model(current_bead),
        status=EvidenceStatus.collected,
        items=[
            EvidenceItem(
                name="run",
                evidence_type=EvidenceType.test_run,
                command="run",
                exit_code=0,
            )
        ],
    )
    write_model(paths.evidence_path(bead_id), evidence)
    evidence_after, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="tester"))
    assert evidence_after is not None
    assert not errors
    assert evidence_after.status == EvidenceStatus.validated

    result = request_transition(paths, bead_id, "in_progress -> verification_pending", actor)
    assert result.ok
    record_transition_attempt(
        paths, bead_id, RunPhase.implement, actor, "in_progress -> verification_pending", result
    )

    system_actor = Actor(kind="system", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", system_actor)
    assert result.ok
    record_transition_attempt(
        paths, bead_id, RunPhase.verify, system_actor, "verification_pending -> verified", result
    )

    entry = create_approval_entry(bead_id, "APPROVAL: ok", Actor(kind="human", name="approver"))
    append_decision_entry(paths, entry)

    result = request_transition(paths, bead_id, "verified -> approval_pending", actor)
    assert result.ok
    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "verified -> approval_pending", result
    )

    result = request_transition(paths, bead_id, "approval_pending -> done", actor)
    assert result.ok
    record_transition_attempt(paths, bead_id, RunPhase.verify, actor, "approval_pending -> done", result)

    final_bead = Bead.model_validate_json(paths.bead_path(bead_id).read_text(encoding="utf-8"))
    assert final_bead.status == BeadStatus.done

    records = load_execution_records(paths)
    assert len(records) == 6
    assert records[-1].applied_transition == "approval_pending -> done"


def test_evidence_validate_records_git_and_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.io import Paths, load_execution_records, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[AcceptanceCheck(name="cmd", command="run", expect_exit_code=0)],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.collected,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[EvidenceItem(name="cmd", evidence_type=EvidenceType.test_run, command="run", exit_code=0)],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)

    evidence_validate(bead_id)
    records = load_execution_records(paths)
    assert records
    last = records[-1]
    assert last.phase == RunPhase.verify
    assert last.produced_artifacts
    assert any(ref.path == f"runs/{bead_id}/evidence.json" for ref in last.produced_artifacts)
    assert last.git is not None
    assert last.git.head_before is None or isinstance(last.git.head_before, str)


def test_evidence_invalidation_uses_validation_git_ref(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import invalidate_evidence_if_stale
    from sdlc.io import Paths, load_execution_records, write_execution_record, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    bead_id = "work-abc123"
    actor = Actor(kind="system", name="tester")
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=actor,
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=actor,
        bead_id=bead_id,
        status=EvidenceStatus.validated,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)

    validation_record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        exit_code=0,
        git=GitRef(head_before="old-head", dirty_before=False),
        produced_artifacts=[FileRef(path=f"runs/{bead_id}/evidence.json")],
    )
    write_execution_record(paths, validation_record)

    monkeypatch.setattr("sdlc.engine.git_head", lambda _: "new-head")
    monkeypatch.setattr("sdlc.engine.git_is_dirty", lambda _: False)

    reason = invalidate_evidence_if_stale(paths, bead_id, actor)
    assert reason is not None
    assert "git head changed" in reason

    evidence_after = EvidenceBundle.model_validate_json(
        paths.evidence_path(bead_id).read_text(encoding="utf-8")
    )
    assert evidence_after.status == EvidenceStatus.invalidated
    records = load_execution_records(paths)
    assert records[-1].exit_code == 1


def test_start_rejected_when_dependency_not_done(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition

    paths = Paths(tmp_path)
    bead_a = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-a12345",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-a12345",
        title="A",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        depends_on=["work-b12345"],
    )
    bead_b = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-b12345",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-b12345",
        title="B",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_a.bead_id), bead_a)
    write_model(paths.bead_path(bead_b.bead_id), bead_b)
    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_a.bead_id, "ready -> in_progress", actor)
    assert not result.ok
    assert "work-b12345" in result.notes


def test_start_allowed_when_dependency_done(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition, _write_ready_acceptance_snapshot

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_a = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-a12345",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-a12345",
        title="A",
        bead_type=BeadType.discovery,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        depends_on=["work-b12345"],
    )
    bead_b = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id="work-b12345",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id="work-b12345",
        title="B",
        bead_type=BeadType.implementation,
        status=BeadStatus.done,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_a.bead_id), bead_a)
    write_model(paths.bead_path(bead_b.bead_id), bead_b)
    _write_ready_acceptance_snapshot(paths, bead_a)
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-a12345",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_a.bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.grounding_path(bead_a.bead_id), grounding)
    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_a.bead_id, "ready -> in_progress", actor)
    assert result.ok


def test_spec_gate_requires_openspec_ref_file_for_implementation(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition, _write_ready_acceptance_snapshot

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        openspec_ref=ArtifactLink(artifact_type="openspec_ref", artifact_id="openspec-abc123"),
    )
    write_model(paths.bead_path(bead_id), bead)
    _write_ready_acceptance_snapshot(paths, bead)
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.grounding_path(bead_id), grounding)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert not result.ok
    assert "OpenSpecRef artifact missing" in result.notes


def test_spec_gate_passes_when_openspec_ref_approved(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition, _write_ready_acceptance_snapshot

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        openspec_ref=ArtifactLink(artifact_type="openspec_ref", artifact_id="openspec-abc123"),
    )
    write_model(paths.bead_path(bead_id), bead)
    _write_ready_acceptance_snapshot(paths, bead)
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.grounding_path(bead_id), grounding)
    openspec_ref = OpenSpecRef(
        schema_name="sdlc.openspec_ref",
        schema_version=1,
        artifact_id="openspec-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        change_id="add-thing",
        state=OpenSpecState.approved,
        path="openspec/changes/add-thing",
    )
    write_model(paths.bead_dir(bead_id) / "openspec_ref.json", openspec_ref)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert result.ok


def test_spec_gate_rejects_openspec_ref_mismatch(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition, _write_ready_acceptance_snapshot

    paths = Paths(tmp_path)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        openspec_ref=ArtifactLink(artifact_type="openspec_ref", artifact_id="openspec-A"),
    )
    write_model(paths.bead_path(bead_id), bead)
    _write_ready_acceptance_snapshot(paths, bead)
    grounding = GroundingBundle(
        schema_name="sdlc.grounding_bundle",
        schema_version=1,
        artifact_id="grounding-work-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead.bead_id,
        items=[],
        allowed_commands=[],
        disallowed_commands=[],
        excluded_paths=[],
    )
    write_model(paths.grounding_path(bead_id), grounding)
    openspec_ref = OpenSpecRef(
        schema_name="sdlc.openspec_ref",
        schema_version=1,
        artifact_id="openspec-B",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        change_id="add-thing",
        state=OpenSpecState.approved,
        path="openspec/changes/add-thing",
    )
    write_model(paths.bead_dir(bead_id) / "openspec_ref.json", openspec_ref)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "ready -> in_progress", actor)
    assert not result.ok
    assert "OpenSpecRef mismatch" in result.notes


def test_openspec_sync_writes_runs_openspec_ref(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from sdlc.io import Paths, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.ready,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        openspec_ref=ArtifactLink(artifact_type="openspec_ref", artifact_id="openspec-abc123"),
    )
    write_model(paths.bead_path(bead_id), bead)

    ref_dir = paths.repo_root / "openspec" / "refs"
    ref_dir.mkdir(parents=True, exist_ok=True)
    openspec_ref = OpenSpecRef(
        schema_name="sdlc.openspec_ref",
        schema_version=1,
        artifact_id="openspec-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        change_id="add-thing",
        state=OpenSpecState.approved,
        path="openspec/changes/add-thing",
    )
    write_model(ref_dir / "openspec-abc123.json", openspec_ref)

    openspec_sync(bead_id)
    out_path = paths.bead_dir(bead_id) / "openspec_ref.json"
    assert out_path.exists()
    loaded = OpenSpecRef.model_validate_json(out_path.read_text(encoding="utf-8"))
    assert loaded.artifact_id == "openspec-abc123"


def test_abort_command_transitions_and_records_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.io import Paths, load_decision_ledger, load_execution_records, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.in_progress,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    abort(bead_id, reason="needs discovery", actor_kind="human", actor_name="tester")

    updated = Bead.model_validate_json(paths.bead_path(bead_id).read_text(encoding="utf-8"))
    assert updated.status == BeadStatus.aborted_needs_discovery

    entries = list(load_decision_ledger(paths))
    assert entries
    assert entries[-1].decision_type == DecisionType.scope_change
    assert entries[-1].summary.startswith("ABORT:")

    records = load_execution_records(paths)
    assert len(records) == 2
    decision_record, transition_record = records
    assert decision_record.exit_code == 0
    assert decision_record.requested_transition is None
    assert decision_record.applied_transition is None
    assert any(
        link.artifact_id == entries[-1].artifact_id for link in decision_record.links
    )
    assert transition_record.applied_transition == "in_progress -> aborted:needs-discovery"
    assert any(
        link.artifact_id == entries[-1].artifact_id for link in transition_record.links
    )


def test_abort_command_records_decision_even_if_transition_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.io import Paths, load_decision_ledger, load_execution_records, write_model

    monkeypatch.chdir(tmp_path)
    paths = Paths(Path.cwd())
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.discovery,
        status=BeadStatus.done,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)

    with pytest.raises(typer.Exit):
        abort(bead_id, reason="needs discovery", actor_kind="human", actor_name="tester")

    entries = list(load_decision_ledger(paths))
    assert entries
    assert entries[-1].decision_type == DecisionType.scope_change

    records = load_execution_records(paths)
    assert len(records) == 2
    decision_record, transition_record = records
    assert decision_record.exit_code == 0
    assert decision_record.requested_transition is None
    assert decision_record.applied_transition is None
    assert transition_record.exit_code == 1
    assert transition_record.applied_transition is None


def test_plan_gate_bucket_l_requires_split_or_justification(tmp_path: Path) -> None:
    from sdlc.io import Paths, load_decision_ledger, write_model
    from sdlc.engine import append_decision_entry, request_transition

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.sized,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.L,
        tightened_acceptance_checks=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "sized -> ready", actor)
    assert not result.ok
    assert "bucket L" in result.notes

    decision = DecisionLedgerEntry(
        schema_name="sdlc.decision_ledger_entry",
        schema_version=1,
        artifact_id="decision-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="tester"),
        bead_id=bead_id,
        decision_type=DecisionType.tradeoff,
        summary="Justify bucket L scope",
    )
    append_decision_entry(paths, decision)
    assert list(load_decision_ledger(paths))

    result = request_transition(paths, bead_id, "sized -> ready", actor)
    assert result.ok


def test_plan_gate_bucket_l_accepts_split_proposal(tmp_path: Path) -> None:
    from sdlc.io import Paths, write_model
    from sdlc.engine import request_transition

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.sized,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    review = BeadReview(
        schema_name="sdlc.bead_review",
        schema_version=1,
        artifact_id="review-abc123",
        created_at=_now(),
        created_by=Actor(kind="human", name="reviewer"),
        bead_id=bead_id,
        effort_bucket=EffortBucket.L,
        tightened_acceptance_checks=[],
        split_required=True,
        split_proposal={
            "rationale": "Too large",
            "proposed_beads": [
                {
                    "title": "Split A",
                    "bead_type": "implementation",
                    "requirements_md": "req",
                    "acceptance_criteria_md": "acc",
                    "context_md": "ctx",
                    "depends_on": [],
                }
            ],
        },
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.bead_dir(bead_id) / "bead_review.json", review)

    actor = Actor(kind="human", name="tester")
    result = request_transition(paths, bead_id, "sized -> ready", actor)
    assert result.ok


def test_boundary_violation_forces_abort_and_records_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import record_transition_attempt, request_transition
    from sdlc.io import Paths, load_decision_ledger, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry_with(
        paths,
        subsystems=[
            {"name": "core", "paths": ["src/"]},
            {"name": "docs", "paths": ["docs/"]},
        ],
        artifact_id="boundary-registry-enforce",
    )
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.validated,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    monkeypatch.setenv("SDLC_MAX_FILES_TOUCHED", "1")
    monkeypatch.setenv("SDLC_MAX_SUBSYSTEMS_TOUCHED", "1")
    monkeypatch.setattr(
        "sdlc.engine.detect_changed_files",
        lambda _: ["src/sdlc/engine.py", "docs/guide.md"],
    )

    actor = Actor(kind="system", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    assert result.ok
    assert result.applied_transition == "verification_pending -> aborted:needs-discovery"

    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "verification_pending -> verified", result
    )
    updated = Bead.model_validate_json(paths.bead_path(bead_id).read_text(encoding="utf-8"))
    assert updated.status == BeadStatus.aborted_needs_discovery

    entries = list(load_decision_ledger(paths))
    assert entries
    assert entries[-1].decision_type == DecisionType.scope_change
    assert entries[-1].summary.startswith("ABORT:")

    records = load_execution_records(paths)
    assert len(records) == 2
    decision_record, transition_record = records
    assert decision_record.exit_code == 0
    assert decision_record.requested_transition is None
    assert decision_record.applied_transition is None
    assert transition_record.exit_code == 0
    assert "Boundary limit exceeded" in (transition_record.notes_md or "")
    assert "Engine-applied abort" in (transition_record.notes_md or "")


def test_engine_abort_decision_type_scope_change(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from sdlc.engine import record_transition_attempt, request_transition
    from sdlc.io import Paths, load_decision_ledger, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry_with(
        paths,
        subsystems=[
            {"name": "core", "paths": ["src/"]},
            {"name": "docs", "paths": ["docs/"]},
        ],
    )
    bead_id = "work-abc123"
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.validated,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)
    monkeypatch.setenv("SDLC_MAX_FILES_TOUCHED", "1")
    monkeypatch.setenv("SDLC_MAX_SUBSYSTEMS_TOUCHED", "1")
    monkeypatch.setattr(
        "sdlc.engine.detect_changed_files",
        lambda _: ["src/sdlc/engine.py", "docs/guide.md"],
    )

    actor = Actor(kind="system", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "verification_pending -> verified", result
    )

    entries = list(load_decision_ledger(paths))
    assert entries
    assert entries[-1].decision_type == DecisionType.scope_change


def test_anti_stall_blocks_verification_pending_to_verified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sdlc.engine import record_transition_attempt, request_transition
    from sdlc.io import Paths, load_execution_records, write_model

    paths = Paths(tmp_path)
    _write_boundary_registry(paths)
    bead_id = "work-abc123"
    past = _now() - timedelta(minutes=120)
    bead = Bead(
        schema_name="sdlc.bead",
        schema_version=1,
        artifact_id=bead_id,
        created_at=past,
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        title="Test",
        bead_type=BeadType.implementation,
        status=BeadStatus.verification_pending,
        requirements_md="req",
        acceptance_criteria_md="acc",
        context_md="ctx",
        acceptance_checks=[],
        max_elapsed_minutes=30,
    )
    evidence = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id="evidence-abc123",
        created_at=_now(),
        created_by=Actor(kind="system", name="tester"),
        bead_id=bead_id,
        status=EvidenceStatus.validated,
        for_bead_hash=canonical_hash_for_model(bead),
        items=[],
    )
    write_model(paths.bead_path(bead_id), bead)
    write_model(paths.evidence_path(bead_id), evidence)

    actor = Actor(kind="system", name="tester")
    result = request_transition(paths, bead_id, "verification_pending -> verified", actor)
    assert not result.ok
    assert "Anti-stall" in result.notes

    record_transition_attempt(
        paths, bead_id, RunPhase.verify, actor, "verification_pending -> verified", result
    )
    records = load_execution_records(paths)
    assert records[-1].exit_code == 1
    assert "abort required" in (records[-1].notes_md or "")


def test_policy_violation_record_helper(tmp_path: Path) -> None:
    from sdlc.io import Paths, load_execution_records, write_execution_record
    from sdlc.engine import policy_violation_record

    paths = Paths(tmp_path)
    actor = Actor(kind="system", name="tester")
    record = policy_violation_record("work-abc123", actor, "policy_violation: out-of-grounding access")
    write_execution_record(paths, record)
    records = load_execution_records(paths)
    assert records
    assert "out-of-grounding access" in (records[-1].notes_md or "")
````
