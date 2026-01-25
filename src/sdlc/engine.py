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
        else:
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
                errors.append(
                    boundary_violation_notes(evaluation, max_files, max_subsystems)
                )
                errors.append(
                    "Boundary limit exceeded: abort bead (aborted:needs-discovery) "
                    "or split via BeadReview"
                )
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
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
    if result.ok and result.applied_transition:
        transition = result.applied_transition.strip()
        if transition == "ready -> in_progress":
            bead = load_bead(paths, bead_id)
            if bead.execution_profile == ExecutionProfile.exception:
                entry = find_active_exception_decision(paths, bead_id)
                if entry is not None:
                    links.append(
                        ArtifactLink(
                            artifact_type="decision_ledger_entry",
                            artifact_id=entry.artifact_id,
                            schema_name="sdlc.decision_ledger_entry",
                            schema_version=1,
                        )
                    )
        elif transition == "approval_pending -> done":
            entry = find_approval_decision(paths, bead_id)
            if entry is not None:
                links.append(
                    ArtifactLink(
                        artifact_type="decision_ledger_entry",
                        artifact_id=entry.artifact_id,
                        schema_name="sdlc.decision_ledger_entry",
                        schema_version=1,
                    )
                )
    record = build_execution_record(
        bead_id,
        phase_value,
        actor,
        requested_transition=requested,
        applied_transition=result.applied_transition if result.ok else None,
        exit_code=0 if result.ok else 1,
        notes_md=result.notes or None,
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
