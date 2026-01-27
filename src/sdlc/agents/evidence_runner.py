from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import List, Optional

import hashlib

from ..codec import sha256_canonical_json
from ..io import Paths, ensure_parent, now_utc
from ..models import AcceptanceCheck, Actor, EvidenceBundle, EvidenceItem, EvidenceType, FileRef, HashRef


@dataclass(frozen=True)
class EvidenceRunResult:
    evidence: EvidenceBundle
    exit_code: int
    commands: List[str]
    produced_paths: List[str]


def _file_hash(paths: Paths, rel_path: str) -> Optional[HashRef]:
    full = paths.repo_root / rel_path
    if not full.exists() or not full.is_file():
        return None
    data = full.read_bytes()
    # Use a stable wrapper so we can reuse sha256_canonical_json.
    # This isn't the artifact hash rule; it's just a content hash stored in HashRef.
    return HashRef(hash=sha256_canonical_json({"bytes_sha256": hashlib.sha256(data).hexdigest()}))


def run_acceptance_checks_to_evidence(
    paths: Paths,
    bead_id: str,
    *,
    actor: Actor,
    acceptance_checks: list[AcceptanceCheck],
    evidence_path: Path,
    evidence_dir: Path,
    extra_attachments: Optional[List[FileRef]] = None,
) -> EvidenceRunResult:
    ensure_parent(evidence_path)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    items: List[EvidenceItem] = []
    commands_run: List[str] = []
    produced_paths: List[str] = []
    worst_exit = 0

    for check in acceptance_checks:
        started_at = now_utc()
        cmd_str = check.command
        cwd = paths.repo_root
        if check.cwd:
            cwd = paths.repo_root / check.cwd
        log_rel = f"runs/{bead_id}/evidence/{check.name}.log"
        log_path = paths.repo_root / log_rel
        ensure_parent(log_path)

        proc = subprocess.run(
            cmd_str,
            cwd=cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=check.timeout_seconds,
        )
        finished_at = now_utc()

        log_path.write_bytes(proc.stdout)

        produced_paths.append(log_rel)
        commands_run.append(cmd_str)

        attachments: List[FileRef] = [FileRef(path=log_rel, content_hash=_file_hash(paths, log_rel))]

        # Include expected output file refs if they exist.
        for expected in check.expected_outputs:
            attachments.append(
                FileRef(path=expected.path, content_hash=_file_hash(paths, expected.path))
            )

        items.append(
            EvidenceItem(
                name=check.name,
                evidence_type=EvidenceType.test_run,
                command=cmd_str,
                exit_code=proc.returncode,
                started_at=started_at,
                finished_at=finished_at,
                attachments=attachments,
            )
        )
        if proc.returncode != check.expect_exit_code:
            worst_exit = 1

    if extra_attachments:
        items.append(
            EvidenceItem(
                name="agent:attachments",
                evidence_type=EvidenceType.test_run,
                attachments=extra_attachments,
            )
        )

    bundle = EvidenceBundle(
        schema_name="sdlc.evidence_bundle",
        schema_version=1,
        artifact_id=f"evidence-{bead_id}",
        created_at=now_utc(),
        created_by=actor,
        bead_id=bead_id,
        items=items,
    )

    evidence_path.write_text(bundle.model_dump_json(indent=2) + "\n", encoding="utf-8")
    produced_paths.append(f"runs/{bead_id}/evidence.json")

    return EvidenceRunResult(
        evidence=bundle,
        exit_code=worst_exit,
        commands=commands_run,
        produced_paths=produced_paths,
    )
