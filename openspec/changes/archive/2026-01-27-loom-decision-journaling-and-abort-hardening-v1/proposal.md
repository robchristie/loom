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
