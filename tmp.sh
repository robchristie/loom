#!/usr/bin/env bash

bd create "bootstrap-agentic-sdlc-v1" -t epic -p 1 -l "openspec:bootstrap-agentic-sdlc-v1" -d "## Requirements
- Implement minimal SDLC lifecycle engine per Agentic SDLC v1 spec (bootstrap scope).
- Integrate with existing Beads workflow (bd) without replacing it.

## Acceptance Criteria
- Commands exist: validate, request transitions, grounding generate, evidence validate/invalidate, approve.
- ExecutionRecord JSONL append-only with deterministic content for tests.
- Evidence validation enforces acceptance coverage and manual_check rules.

## Context
- OpenSpec change: openspec/changes/bootstrap-agentic-sdlc-v1/
- Spec excerpt: Agentic SDLC v1 in chat / local docs to be added"

