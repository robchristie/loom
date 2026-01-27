"""
FastAPI web server for Loom SDLC observability + interaction.

Design goals:
- Filesystem artifacts remain the source of truth (reads are direct).
- Lifecycle mutations go through the engine (request_transition, validate_evidence_bundle, etc.).
- Journaling is preserved (ExecutionRecord written for transition attempts, and
  optionally for other actions like grounding/evidence collection).
- SSE endpoint streams appended ExecutionRecord + DecisionLedgerEntry lines.

Run (from repo root):
  uv run uvicorn sdlc.server:app --reload --port 8000
or set SDLC_REPO_ROOT if you run elsewhere:
  SDLC_REPO_ROOT=/path/to/repo uv run uvicorn sdlc.server:app --reload
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Iterable, List, Optional

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .engine import (
    append_decision_entry,
    build_execution_record,
    collect_evidence_skeleton,
    create_abort_entry,
    create_approval_entry,
    decision_ledger_link,
    generate_grounding_bundle,
    invalidate_evidence_if_stale,
    record_decision_action,
    record_transition_attempt,
    request_transition,
    validate_evidence_bundle,
)
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
    write_model,
    write_execution_record,
)
from .models import (
    Actor,
    Bead,
    BeadReview,
    BeadStatus,
    DecisionLedgerEntry,
    EvidenceBundle,
    FileRef,
    GitRef,
    GroundingBundle,
    OpenSpecRef,
    RunPhase,
)

BEAD_ID_RE = re.compile(r"^work-[a-z0-9]+(\.[a-z0-9]+)?$")


# ----------------------------
# API models (thin wrappers)
# ----------------------------

class RepoInfo(BaseModel):
    repo_root: str
    git_head: Optional[str] = None
    git_dirty: Optional[bool] = None


class BeadSummary(BaseModel):
    bead_id: str
    title: str
    bead_type: str
    status: str
    priority: int = 3
    owner: Optional[str] = None
    created_at: Optional[str] = None  # serialized ISO string for easy UI use


class ArtifactStatus(BaseModel):
    name: str
    path: str
    exists: bool


class BeadArtifactsIndex(BaseModel):
    bead_id: str
    artifacts: List[ArtifactStatus]


class TransitionRequest(BaseModel):
    transition: str = Field(..., examples=["draft -> sized", "ready -> in_progress"])
    actor: Optional[Actor] = None


class TransitionResponse(BaseModel):
    ok: bool
    notes: str = ""
    requested_transition: str
    applied_transition: Optional[str] = None
    auto_abort: bool = False
    execution_record: Optional[dict] = None  # JSON-serializable ExecutionRecord dump


class ApproveRequest(BaseModel):
    summary: str = Field(..., examples=["APPROVAL: shipped"])
    actor: Optional[Actor] = None


class AbortRequest(BaseModel):
    reason: str = Field(..., examples=["needs discovery (unknown unknowns)"])
    actor: Optional[Actor] = None


class ActionResponse(BaseModel):
    ok: bool
    notes: Optional[str] = None
    produced_artifacts: List[str] = Field(default_factory=list)


# ----------------------------
# Utilities / dependencies
# ----------------------------

def _default_actor(kind: str = "human") -> Actor:
    return Actor(kind=kind, name=os.getenv("USER", "unknown"))


def get_paths() -> Paths:
    root = os.getenv("SDLC_REPO_ROOT")
    repo_root = Path(root).resolve() if root else Path.cwd().resolve()
    return Paths(repo_root)


def _phase_for_transition(transition: str) -> RunPhase:
    """
    Same mapping concept as CLI: journaling phase should reflect where in lifecycle
    the request sits (plan/implement/verify). Best-effort.
    """
    m = re.match(r"^\s*([^-\s>]+)\s*->\s*([^-\s>]+)\s*$", transition)
    if not m:
        return RunPhase.implement
    to_status = m.group(2).strip()

    if to_status in {"sized", "ready"}:
        return RunPhase.plan
    if to_status in {"in_progress", "verification_pending"}:
        return RunPhase.implement
    if to_status in {"verified", "approval_pending", "done"}:
        return RunPhase.verify
    return RunPhase.implement


def _decision_action_phase_for_bead(paths: Paths, bead_id: str) -> RunPhase:
    bead = load_bead(paths, bead_id)
    if bead.status in {BeadStatus.draft, BeadStatus.sized, BeadStatus.ready}:
        return RunPhase.plan
    return RunPhase.verify


def _safe_read_json(path: Path) -> Optional[dict[str, Any]]:
    """
    Defensive read: if a file is mid-write or truncated, avoid crashing the UI.
    (Your current dump_json isn't atomic; this helps the web UI be resilient.)
    """
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _runs_bead_ids(paths: Paths) -> set[str]:
    ids: set[str] = set()
    if not paths.runs_dir.exists():
        return ids
    for child in paths.runs_dir.iterdir():
        if child.is_dir() and BEAD_ID_RE.match(child.name):
            ids.add(child.name)
    return ids


def _bd_issues_path(paths: Paths) -> Optional[Path]:
    candidates = [
        paths.repo_root / "beads" / "issues.jsonl",
        paths.repo_root / "beads" / "issues.json",
        paths.repo_root / ".beads" / "issues.jsonl",
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    return None


def _iter_bd_issue_dicts(paths: Paths) -> Iterable[dict[str, Any]]:
    """
    Attempts to parse bd issues store in a tolerant way:
    - JSONL (preferred)
    - JSON list/dict (fallback)
    - "JSONL but named .json" (fallback)
    """
    p = _bd_issues_path(paths)
    if p is None:
        return []

    text = p.read_text(encoding="utf-8")

    # Try whole-file JSON first
    try:
        payload = json.loads(text)
        if isinstance(payload, list):
            return [x for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            # common patterns: {"issues":[...]} or similar
            for key in ("issues", "items", "data"):
                val = payload.get(key)
                if isinstance(val, list):
                    return [x for x in val if isinstance(x, dict)]
            # if it's a single issue dict
            return [payload]
    except Exception:
        pass

    # Fallback: parse line-by-line JSONL
    out: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def _bead_from_bd_issue(data: dict[str, Any]) -> Optional[Bead]:
    bead_id = data.get("id")
    if not isinstance(bead_id, str) or not BEAD_ID_RE.match(bead_id):
        return None

    created_at = data.get("created_at") or data.get("created")
    if not created_at:
        created_at = now_utc().isoformat()

    acceptance = data.get("acceptance") or data.get("acceptance_criteria") or ""
    description = data.get("description") or data.get("body") or ""
    title = data.get("title") or bead_id
    status = data.get("status") or "draft"

    owner = data.get("owner") or data.get("assignee")
    priority: Any = data.get("priority")

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
        "created_by": {"kind": "system", "name": "bd"},
        "bead_id": bead_id,
        "title": title,
        "bead_type": data.get("bead_type", "implementation"),
        "status": status,
        "priority": priority,
        "owner": owner,
        "requirements_md": description,
        "acceptance_criteria_md": acceptance,
        "context_md": data.get("notes") or data.get("context") or "",
        "acceptance_checks": [],
    }
    try:
        return Bead.model_validate(bead_payload)
    except Exception:
        return None


def _list_beads(paths: Paths) -> List[Bead]:
    by_id: Dict[str, Bead] = {}

    # 1) Prefer Loom-managed artifacts in runs/
    for bead_id in sorted(_runs_bead_ids(paths)):
        try:
            by_id[bead_id] = load_bead(paths, bead_id)
        except Exception:
            continue

    # 2) Also include bd store items not yet materialized into runs/<id>/bead.json
    for issue in _iter_bd_issue_dicts(paths):
        bead = _bead_from_bd_issue(issue)
        if bead is None:
            continue
        if bead.bead_id not in by_id:
            by_id[bead.bead_id] = bead

    return list(by_id.values())


def _journal_simple_action(
    paths: Paths,
    bead_id: str,
    phase: RunPhase,
    actor: Actor,
    *,
    notes_md: Optional[str] = None,
    produced_paths: Optional[List[str]] = None,
    exit_code: int = 0,
) -> None:
    produced = [FileRef(path=p) for p in (produced_paths or [])]
    record = build_execution_record(
        bead_id=bead_id,
        phase=phase,
        actor=actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=exit_code,
        notes_md=notes_md,
        git=GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths)),
        produced_artifacts=produced,
    )
    write_execution_record(paths, record)


# ----------------------------
# FastAPI app
# ----------------------------

app = FastAPI(title="Loom SDLC API", version="0.1")

# If your frontend runs on a different origin, this is convenient for dev.
# Tighten this for real usage.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/api/repo", response_model=RepoInfo)
def repo_info(paths: Paths = Depends(get_paths)) -> RepoInfo:
    return RepoInfo(
        repo_root=str(paths.repo_root),
        git_head=git_head(paths),
        git_dirty=git_is_dirty(paths),
    )


@app.get("/api/beads", response_model=List[BeadSummary])
def list_beads(
    status: Optional[str] = Query(None, description="Filter by bead status (exact match)"),
    q: Optional[str] = Query(None, description="Substring match against id/title"),
    limit: int = Query(200, ge=1, le=2000),
    paths: Paths = Depends(get_paths),
) -> List[BeadSummary]:
    beads = _list_beads(paths)

    def matches(b: Bead) -> bool:
        if status and b.status.value != status:
            return False
        if q:
            needle = q.lower()
            if needle not in b.bead_id.lower() and needle not in b.title.lower():
                return False
        return True

    filtered = [b for b in beads if matches(b)]
    # Stable sort: status then priority then created_at (best-effort)
    filtered.sort(key=lambda b: (b.status.value, b.priority, b.created_at))
    out: List[BeadSummary] = []
    for b in filtered[:limit]:
        out.append(
            BeadSummary(
                bead_id=b.bead_id,
                title=b.title,
                bead_type=b.bead_type.value,
                status=b.status.value,
                priority=b.priority,
                owner=b.owner,
                created_at=b.created_at.isoformat() if getattr(b, "created_at", None) else None,
            )
        )
    return out


@app.get("/api/beads/{bead_id}", response_model=Bead)
def get_bead(bead_id: str, paths: Paths = Depends(get_paths)) -> Bead:
    if not BEAD_ID_RE.match(bead_id):
        raise HTTPException(status_code=400, detail="Invalid bead_id format")
    try:
        return load_bead(paths, bead_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Bead not found")


@app.get("/api/beads/{bead_id}/artifacts", response_model=BeadArtifactsIndex)
def bead_artifacts(bead_id: str, paths: Paths = Depends(get_paths)) -> BeadArtifactsIndex:
    bead_dir = paths.bead_dir(bead_id)
    candidates = [
        ("bead", paths.bead_path(bead_id)),
        ("bead_review", bead_dir / "bead_review.json"),
        ("grounding", paths.grounding_path(bead_id)),
        ("evidence", paths.evidence_path(bead_id)),
        ("openspec_ref", bead_dir / "openspec_ref.json"),
        ("ready_acceptance_snapshot", bead_dir / "ready_acceptance_hash.json"),
    ]
    artifacts = [
        ArtifactStatus(name=name, path=str(p.relative_to(paths.repo_root)), exists=p.exists())
        for (name, p) in candidates
    ]
    return BeadArtifactsIndex(bead_id=bead_id, artifacts=artifacts)


@app.get("/api/beads/{bead_id}/review", response_model=Optional[BeadReview])
def get_review(bead_id: str, paths: Paths = Depends(get_paths)) -> Optional[BeadReview]:
    return load_bead_review(paths, bead_id)


@app.get("/api/beads/{bead_id}/grounding", response_model=Optional[GroundingBundle])
def get_grounding(bead_id: str, paths: Paths = Depends(get_paths)) -> Optional[GroundingBundle]:
    return load_grounding(paths, bead_id)


@app.get("/api/beads/{bead_id}/evidence", response_model=Optional[EvidenceBundle])
def get_evidence(bead_id: str, paths: Paths = Depends(get_paths)) -> Optional[EvidenceBundle]:
    return load_evidence(paths, bead_id)


@app.get("/api/beads/{bead_id}/journal", response_model=List[dict])
def bead_journal(
    bead_id: str,
    limit: int = Query(500, ge=1, le=5000),
    paths: Paths = Depends(get_paths),
) -> List[dict]:
    records = [r for r in load_execution_records(paths) if r.bead_id == bead_id]
    records = records[-limit:]
    return [r.model_dump(mode="json") for r in records]


@app.get("/api/beads/{bead_id}/decisions", response_model=List[dict])
def bead_decisions(
    bead_id: str,
    limit: int = Query(500, ge=1, le=5000),
    paths: Paths = Depends(get_paths),
) -> List[dict]:
    entries = [e for e in load_decision_ledger(paths) if e.bead_id == bead_id]
    entries = entries[-limit:]
    return [e.model_dump(mode="json") for e in entries]


@app.post("/api/beads/{bead_id}/transition", response_model=TransitionResponse)
def transition_bead(
    bead_id: str,
    req: TransitionRequest = Body(...),
    paths: Paths = Depends(get_paths),
) -> TransitionResponse:
    actor = req.actor or _default_actor("human")
    result = request_transition(paths, bead_id, req.transition, actor)
    phase = _phase_for_transition(req.transition)
    record = record_transition_attempt(paths, bead_id, phase, actor, req.transition, result)

    return TransitionResponse(
        ok=result.ok,
        notes=result.notes,
        requested_transition=req.transition,
        applied_transition=result.applied_transition if result.ok else None,
        auto_abort=result.auto_abort,
        execution_record=record.model_dump(mode="json"),
    )


@app.post("/api/beads/{bead_id}/grounding/generate", response_model=ActionResponse)
def grounding_generate(
    bead_id: str,
    actor: Optional[Actor] = Body(None),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    actor = actor or Actor(kind="system", name="sdlc-web")
    generate_grounding_bundle(paths, bead_id, actor)

    # Optional: journal this action for the UI timeline
    _journal_simple_action(
        paths,
        bead_id,
        RunPhase.plan,
        actor,
        notes_md="Grounding generated",
        produced_paths=[f"runs/{bead_id}/grounding.json"],
        exit_code=0,
    )

    return ActionResponse(ok=True, produced_artifacts=[f"runs/{bead_id}/grounding.json"])


@app.post("/api/beads/{bead_id}/evidence/collect", response_model=ActionResponse)
def evidence_collect(
    bead_id: str,
    actor: Optional[Actor] = Body(None),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    actor = actor or Actor(kind="system", name="sdlc-web")
    bead = load_bead(paths, bead_id)
    bundle = collect_evidence_skeleton(bead, actor)
    write_model(paths.evidence_path(bead_id), bundle)

    _journal_simple_action(
        paths,
        bead_id,
        RunPhase.verify,
        actor,
        notes_md="Evidence skeleton collected",
        produced_paths=[f"runs/{bead_id}/evidence.json"],
        exit_code=0,
    )

    return ActionResponse(ok=True, produced_artifacts=[f"runs/{bead_id}/evidence.json"])


@app.post("/api/beads/{bead_id}/evidence/validate", response_model=ActionResponse)
def evidence_validate(
    bead_id: str,
    mark_validated: bool = Query(True, description="If true, set EvidenceBundle.status=validated on success"),
    actor: Optional[Actor] = Body(None),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    # Mimic CLI behavior: if the evidence bundle is human-authored, journal under that actor.
    evidence = load_evidence(paths, bead_id)
    effective_actor = actor or Actor(kind="system", name="sdlc-web")
    if evidence and evidence.created_by.kind == "human":
        effective_actor = evidence.created_by

    evidence_after, errors = validate_evidence_bundle(
        paths, bead_id, effective_actor, mark_validated=mark_validated
    )

    git_ref = GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths))
    record = build_execution_record(
        bead_id=bead_id,
        phase=RunPhase.verify,
        actor=effective_actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0 if not errors else 1,
        notes_md="; ".join(errors) if errors else "Evidence validated",
        git=git_ref,
        produced_artifacts=[FileRef(path=f"runs/{bead_id}/evidence.json")] if evidence_after else [],
    )
    write_execution_record(paths, record)

    return ActionResponse(
        ok=not errors,
        notes="; ".join(errors) if errors else "ok",
        produced_artifacts=[f"runs/{bead_id}/evidence.json"] if evidence_after else [],
    )


@app.post("/api/beads/{bead_id}/evidence/invalidate-if-stale", response_model=ActionResponse)
def evidence_invalidate_stale(
    bead_id: str,
    actor: Optional[Actor] = Body(None),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    actor = actor or Actor(kind="system", name="sdlc-web")
    reason = invalidate_evidence_if_stale(paths, bead_id, actor)
    return ActionResponse(ok=True, notes=reason or "not stale")


@app.post("/api/beads/{bead_id}/openspec/sync", response_model=ActionResponse)
def openspec_sync(
    bead_id: str,
    actor: Optional[Actor] = Body(None),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    actor = actor or Actor(kind="system", name="sdlc-web")
    bead = load_bead(paths, bead_id)

    if bead.openspec_ref is None:
        raise HTTPException(status_code=409, detail="Bead.openspec_ref missing")
    artifact_id = bead.openspec_ref.artifact_id
    ref_path = paths.repo_root / "openspec" / "refs" / f"{artifact_id}.json"
    if not ref_path.exists():
        raise HTTPException(status_code=404, detail=f"OpenSpecRef not found: {ref_path}")

    try:
        ref = OpenSpecRef.model_validate_json(ref_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"OpenSpecRef invalid: {exc}")

    out_path = paths.bead_dir(bead_id) / "openspec_ref.json"
    write_model(out_path, ref)

    _journal_simple_action(
        paths,
        bead_id,
        RunPhase.plan,
        actor,
        notes_md="OpenSpecRef synced into runs/<bead_id>/openspec_ref.json",
        produced_paths=[f"runs/{bead_id}/openspec_ref.json"],
        exit_code=0,
    )

    return ActionResponse(ok=True, produced_artifacts=[f"runs/{bead_id}/openspec_ref.json"])


@app.post("/api/beads/{bead_id}/approve", response_model=ActionResponse)
def approve_bead(
    bead_id: str,
    req: ApproveRequest = Body(...),
    paths: Paths = Depends(get_paths),
) -> ActionResponse:
    actor = req.actor or _default_actor("human")
    if actor.kind != "human":
        raise HTTPException(status_code=409, detail="Approval must be created_by.kind == human")
    if not req.summary.strip():
        raise HTTPException(status_code=400, detail="summary must be non-empty")

    entry = create_approval_entry(bead_id, req.summary, actor)
    append_decision_entry(paths, entry)

    # Optional: journal decision action (nice for the timeline)
    record_decision_action(paths, entry, RunPhase.verify, actor, notes_md="Approval recorded")

    return ActionResponse(ok=True, notes="approval recorded", produced_artifacts=[])


@app.post("/api/beads/{bead_id}/abort", response_model=TransitionResponse)
def abort_bead(
    bead_id: str,
    req: AbortRequest = Body(...),
    paths: Paths = Depends(get_paths),
) -> TransitionResponse:
    actor = req.actor or _default_actor("human")
    if not req.reason.strip():
        raise HTTPException(status_code=400, detail="reason must be non-empty")

    # 1) Create + append abort decision
    entry = create_abort_entry(bead_id, req.reason, actor)
    append_decision_entry(paths, entry)

    # 2) Journal the decision action itself (spec-friendly)
    record_decision_action(
        paths,
        entry,
        _decision_action_phase_for_bead(paths, bead_id),
        actor,
        notes_md="Abort requested",
    )

    # 3) Request transition to aborted:needs-discovery
    bead = load_bead(paths, bead_id)
    requested = f"{bead.status.value} -> {BeadStatus.aborted_needs_discovery.value}"
    result = request_transition(paths, bead_id, requested, actor)

    # 4) Journal the transition attempt, linking the decision entry
    phase = _phase_for_transition(requested)
    record = record_transition_attempt(
        paths,
        bead_id,
        phase,
        actor,
        requested,
        result,
        extra_links=[decision_ledger_link(entry)],
    )

    return TransitionResponse(
        ok=result.ok,
        notes=result.notes,
        requested_transition=requested,
        applied_transition=result.applied_transition if result.ok else None,
        auto_abort=result.auto_abort,
        execution_record=record.model_dump(mode="json"),
    )


# ----------------------------
# Server-Sent Events (SSE)
# ----------------------------

async def _tail_jsonl(
    path: Path,
    *,
    event_name: str,
    bead_id: Optional[str],
    poll_seconds: float,
    start_at_end: bool,
) -> AsyncIterator[str]:
    """
    Async generator that yields SSE frames for new JSONL lines appended to `path`.
    """
    # We keep our own file position to support tailing.
    pos = 0
    if start_at_end and path.exists():
        pos = path.stat().st_size

    while True:
        if not path.exists():
            await asyncio.sleep(poll_seconds)
            continue

        try:
            with path.open("r", encoding="utf-8") as f:
                f.seek(pos)
                while True:
                    line = f.readline()
                    if not line:
                        break
                    pos = f.tell()

                    raw = line.strip()
                    if not raw:
                        continue

                    # Filter by bead_id (parse minimal JSON)
                    if bead_id is not None:
                        try:
                            obj = json.loads(raw)
                        except Exception:
                            continue
                        obj_bead = obj.get("bead_id")
                        if obj_bead != bead_id:
                            continue
                        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

                    yield f"event: {event_name}\ndata: {raw}\n\n"
        except Exception:
            # If file is mid-rotate or transiently unreadable, just retry.
            await asyncio.sleep(poll_seconds)

        await asyncio.sleep(poll_seconds)


@app.get("/api/events")
async def events(
    bead_id: Optional[str] = Query(None, description="If set, only stream events for this bead_id"),
    start_at_end: bool = Query(True, description="If true, don't replay old events"),
    poll_seconds: float = Query(0.5, ge=0.1, le=5.0),
    paths: Paths = Depends(get_paths),
) -> StreamingResponse:
    """
    Streams:
      - event: execution_record   data: <json>
      - event: decision_entry     data: <json>

    Tip: if you put nginx in front, disable proxy buffering for this route.
    """
    async def stream() -> AsyncIterator[str]:
        # small initial hello (helps some clients)
        yield "event: hello\ndata: {}\n\n"

        journal_task = _tail_jsonl(
            paths.journal_path,
            event_name="execution_record",
            bead_id=bead_id,
            poll_seconds=poll_seconds,
            start_at_end=start_at_end,
        )
        decision_task = _tail_jsonl(
            paths.decision_ledger_path,
            event_name="decision_entry",
            bead_id=bead_id,
            poll_seconds=poll_seconds,
            start_at_end=start_at_end,
        )

        # Interleave both streams (simple, fair-ish)
        iters = [journal_task.__aiter__(), decision_task.__aiter__()]
        i = 0
        while True:
            # keep-alive comment every ~15s to prevent idle timeouts
            # (with poll_seconds default 0.5, this is about every 30 iterations)
            if i % 30 == 0:
                yield ": keep-alive\n\n"

            # round-robin pull
            for _ in range(len(iters)):
                idx = i % len(iters)
                i += 1
                try:
                    msg = await iters[idx].__anext__()
                    yield msg
                except StopAsyncIteration:
                    # shouldn't happen, but just continue
                    continue

            await asyncio.sleep(0)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )

@app.get("/api/beads/{bead_id}/openspec-ref", response_model=Optional[OpenSpecRef])
def get_openspec_ref(bead_id: str, paths: Paths = Depends(get_paths)) -> Optional[OpenSpecRef]:
    p = paths.bead_dir(bead_id) / "openspec_ref.json"
    if not p.exists():
        return None
    return OpenSpecRef.model_validate_json(p.read_text(encoding="utf-8"))
