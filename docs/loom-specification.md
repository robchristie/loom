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

On abort, the system MUST:

 * create a DecisionLedgerEntry describing why
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
