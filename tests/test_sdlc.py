from __future__ import annotations

import json
from datetime import datetime, timezone
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
    assert not result.ok
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
    assert records
    last = records[-1]
    assert last.applied_transition == "in_progress -> aborted:needs-discovery"
