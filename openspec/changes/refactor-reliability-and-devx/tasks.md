## 1. Atomic JSON writes
- [ ] 1.1 Identify JSON write helpers used for run artifacts and UI inputs.
- [ ] 1.2 Implement atomic write for JSON (temp file + replace) and ensure parent dirs exist.
- [ ] 1.3 Add/adjust tests to prove readers never see truncated JSON during write.

## 2. UI-safe exception handling with visibility
- [ ] 2.1 Audit `except Exception` blocks in server/UI-facing paths.
- [ ] 2.2 Replace bare `except Exception` with narrow exceptions where feasible.
- [ ] 2.3 Where broad catches remain, log exception + context (path/op) without crashing.

## 3. Formatting gate
- [ ] 3.1 Add a documented quality gate that runs `uv run ruff format --check .`.
- [ ] 3.2 Ensure the repo passes `ruff format` and add guidance for contributors.

## 4. Centralize transition phase mapping
- [ ] 4.1 Extract transition→phase mapping into a shared helper.
- [ ] 4.2 Update engine/CLI/server to use the shared helper.
- [ ] 4.3 Add tests to prevent phase mapping drift.

