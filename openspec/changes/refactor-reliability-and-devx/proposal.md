# Proposal: Refactor reliability and developer experience

## Why

The SDLC kernel currently includes defensive patterns that compensate for a few reliability and DX gaps:

- The web UI reads JSON files that may be mid-write, so it must tolerate truncated JSON.
- Several code paths swallow broad exceptions to avoid crashing the UI, but provide limited visibility when failures occur.
- Formatting is enforced via `ruff check`, but `ruff format --check` is not consistently enforced, so formatting drift can accumulate.
- Transition-to-phase mapping logic exists in multiple places, increasing the chance of lifecycle drift.

Addressing these improves correctness, reduces flakiness in the UI, and makes contributions more consistent.

## What changes

- Use atomic write semantics for JSON files written by the kernel so readers never observe partial content.
- Keep UI resilience, but ensure errors swallowed for safety are recorded with enough context to debug.
- Enforce `ruff format --check` as part of project quality gates (local and/or CI) to prevent style drift.
- Centralize lifecycle mapping (transition → phase) and reuse it across CLI/server/engine.

## Impact

- No user-facing behavior changes intended, except improved reliability and clearer error reporting.
- Low-risk refactor with targeted changes in I/O and server/engine helpers.
- Developers get consistent formatting and fewer “works on my machine” issues when the environment is invoked via `uv run`.

