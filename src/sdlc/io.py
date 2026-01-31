from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import subprocess

from pydantic import BaseModel

from .models import (
    Bead,
    BeadReview,
    DecisionLedgerEntry,
    EvidenceBundle,
    ExecutionRecord,
    GroundingBundle,
)


@dataclass(frozen=True)
class Paths:
    repo_root: Path

    @property
    def runs_dir(self) -> Path:
        return self.repo_root / "runs"

    @property
    def journal_path(self) -> Path:
        return self.runs_dir / "journal.jsonl"

    @property
    def decision_ledger_path(self) -> Path:
        return self.repo_root / "decision_ledger.jsonl"

    def bead_dir(self, bead_id: str) -> Path:
        return self.runs_dir / bead_id

    def bead_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "bead.json"

    def grounding_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "grounding.json"

    def evidence_path(self, bead_id: str) -> Path:
        return self.bead_dir(bead_id) / "evidence.json"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n")


def load_bead(paths: Paths, bead_id: str) -> Bead:
    bead_path = paths.bead_path(bead_id)
    if bead_path.exists():
        return Bead.model_validate_json(bead_path.read_text(encoding="utf-8"))
    return _load_bead_from_bd(paths, bead_id)


def _load_bead_from_bd(paths: Paths, bead_id: str) -> Bead:
    issues_path = paths.repo_root / "beads" / "issues.jsonl"
    if not issues_path.exists():
        issues_path = paths.repo_root / "beads" / "issues.json"
    if not issues_path.exists():
        issues_path = paths.repo_root / ".beads" / "issues.jsonl"
    if not issues_path.exists():
        raise FileNotFoundError("No bead artifact or bd issues store found")

    bead_data: Optional[dict[str, Any]] = None
    with issues_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            data = json.loads(line)
            if data.get("id") == bead_id:
                bead_data = data
                break

    if bead_data is None:
        raise FileNotFoundError(f"Bead {bead_id} not found in bd store")

    created_at = bead_data.get("created_at") or bead_data.get("created")
    if created_at is None:
        created_at = now_utc().isoformat()

    acceptance = bead_data.get("acceptance") or bead_data.get("acceptance_criteria") or ""
    description = bead_data.get("description") or bead_data.get("body") or ""
    title = bead_data.get("title") or bead_id
    status = bead_data.get("status") or "draft"

    owner = bead_data.get("owner") or bead_data.get("assignee")
    priority = bead_data.get("priority")
    if isinstance(priority, str) and priority.upper().startswith("P"):
        try:
            priority = int(priority[1:]) + 1
        except ValueError:
            priority = 3
    if isinstance(priority, int):
        priority = max(1, min(5, priority))
    else:
        priority = 3

    bead_payload = {
        "schema_name": "sdlc.bead",
        "schema_version": 1,
        "artifact_id": bead_id,
        "created_at": created_at,
        "created_by": {
            "kind": "system",
            "name": "bd",
        },
        "bead_id": bead_id,
        "title": title,
        "bead_type": bead_data.get("bead_type", "implementation"),
        "status": status,
        "priority": priority,
        "owner": owner,
        "requirements_md": description,
        "acceptance_criteria_md": acceptance,
        "context_md": bead_data.get("notes") or bead_data.get("context") or "",
        "acceptance_checks": [],
    }

    return Bead.model_validate(bead_payload)


def load_bead_review(paths: Paths, bead_id: str) -> Optional[BeadReview]:
    review_path = paths.bead_dir(bead_id) / "bead_review.json"
    if not review_path.exists():
        return None
    return BeadReview.model_validate_json(review_path.read_text(encoding="utf-8"))


def load_grounding(paths: Paths, bead_id: str) -> Optional[GroundingBundle]:
    path = paths.grounding_path(bead_id)
    if not path.exists():
        return None
    return GroundingBundle.model_validate_json(path.read_text(encoding="utf-8"))


def load_evidence(paths: Paths, bead_id: str) -> Optional[EvidenceBundle]:
    path = paths.evidence_path(bead_id)
    if not path.exists():
        return None
    return EvidenceBundle.model_validate_json(path.read_text(encoding="utf-8"))


def write_model(path: Path, model: BaseModel) -> None:
    dump_json(path, model.model_dump(mode="json"))


def write_execution_record(paths: Paths, record: ExecutionRecord) -> None:
    append_jsonl(paths.journal_path, record.model_dump(mode="json"))


def write_decision_entry(paths: Paths, entry: DecisionLedgerEntry) -> None:
    append_jsonl(paths.decision_ledger_path, entry.model_dump(mode="json"))


def load_decision_ledger(paths: Paths) -> Iterable[DecisionLedgerEntry]:
    if not paths.decision_ledger_path.exists():
        return []
    entries: list[DecisionLedgerEntry] = []
    with paths.decision_ledger_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            entries.append(DecisionLedgerEntry.model_validate_json(line))
    return entries


def load_execution_records(paths: Paths) -> list[ExecutionRecord]:
    if not paths.journal_path.exists():
        return []
    records: list[ExecutionRecord] = []
    with paths.journal_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records.append(ExecutionRecord.model_validate_json(line))
    return records


def git_head(paths: Paths) -> Optional[str]:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=paths.repo_root,
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        return None


def git_is_dirty(paths: Paths) -> Optional[bool]:
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=paths.repo_root,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None
    return bool(output.strip())
