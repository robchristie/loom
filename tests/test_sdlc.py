from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from sdlc.codec import sha256_canonical_json
from sdlc.engine import acceptance_coverage_errors
from sdlc.models import (
    Actor,
    AcceptanceCheck,
    Bead,
    BeadStatus,
    BeadType,
    EvidenceBundle,
    EvidenceItem,
    EvidenceStatus,
    EvidenceType,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


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
