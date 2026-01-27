from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing import Any, cast
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
        # pydantic's BaseModel metaclass typing doesn't expose model_fields cleanly.
        model_fields = getattr(cls, "model_fields")
        default = cast(Any, model_fields)["schema_name"].default
        if isinstance(default, str):
            registry[default] = cast(type[SchemaBase], cls)
    return registry
