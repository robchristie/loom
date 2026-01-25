from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from .codec import sha256_canonical_json
from .io import (
    Paths,
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
    Bead,
    BeadReview,
    BeadStatus,
    BeadType,
    DecisionLedgerEntry,
    DecisionType,
    EvidenceBundle,
    EvidenceItem,
    EvidenceStatus,
    EvidenceType,
    ExecutionProfile,
    ExecutionRecord,
    GitRef,
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


@dataclass
class GateResult:
    ok: bool
    notes: str = ""


def canonical_hash_for_model(model: Bead | BeadReview | EvidenceBundle) -> HashRef:
    payload = model.model_dump(mode="json")
    return HashRef(hash=sha256_canonical_json(payload))


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
    for entry in load_decision_ledger(paths):
        if entry.decision_type != DecisionType.exception:
            continue
        if entry.bead_id != bead.bead_id:
            continue
        if entry.expires_at is not None and entry.expires_at <= now_utc():
            continue
        if entry.summary.strip():
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
    for entry in load_decision_ledger(paths):
        if entry.decision_type != DecisionType.approval:
            continue
        if entry.bead_id != bead.bead_id:
            continue
        if entry.created_by.kind != "human":
            continue
        if entry.summary.strip():
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
        else:
            apply_acceptance_checks_from_review(bead, review)
    elif bead.status == BeadStatus.ready and to_status == BeadStatus.in_progress.value:
        review = load_bead_review(paths, bead_id)
        if review and not acceptance_checks_equal(
            bead.acceptance_checks, review.tightened_acceptance_checks
        ):
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
    elif bead.status == BeadStatus.verified and to_status == BeadStatus.approval_pending.value:
        pass
    elif bead.status == BeadStatus.approval_pending and to_status == BeadStatus.done.value:
        approval_error = _approval_gate(paths, bead)
        if approval_error:
            errors.append(approval_error)
    elif to_status in FAILURE_TARGETS:
        pass

    if errors:
        return TransitionResult(False, "; ".join(errors), phase=phase_hint)

    _apply_transition(bead, BeadStatus(to_status))
    write_model(paths.bead_path(bead_id), bead)
    return TransitionResult(True, "", applied_transition=f"{from_status} -> {to_status}", phase=phase_hint)


def build_execution_record(
    bead_id: str,
    phase: RunPhase,
    actor: Actor,
    requested_transition: Optional[str] = None,
    applied_transition: Optional[str] = None,
    exit_code: Optional[int] = None,
    notes_md: Optional[str] = None,
    git: Optional[GitRef] = None,
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
        schema_name="sdlc.execution_record",
        schema_version=1,
    )


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
        item = next((candidate for candidate in evidence.items if candidate.command == check.command), None)
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
    last_record = None
    for record in reversed(load_execution_records(paths)):
        if record.bead_id == bead_id:
            last_record = record
            break
    if last_record and last_record.git:
        if head is not None and last_record.git.head_before and last_record.git.head_before != head:
            reasons.append("git head changed")
        if dirty is not None and last_record.git.dirty_before is not None and last_record.git.dirty_before != dirty:
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


def record_transition_attempt(
    paths: Paths,
    bead_id: str,
    phase: RunPhase,
    actor: Actor,
    requested: str,
    result: TransitionResult,
) -> ExecutionRecord:
    phase_value = result.phase or phase
    git_ref = GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths))
    record = build_execution_record(
        bead_id,
        phase_value,
        actor,
        requested_transition=requested,
        applied_transition=result.applied_transition if result.ok else None,
        exit_code=0 if result.ok else 1,
        notes_md=result.notes or None,
        git=git_ref,
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
