from __future__ import annotations

import json
import os
import re
from pathlib import Path
import typer
from pydantic import ValidationError

from .codec import sha256_canonical_json
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
from .io import Paths, git_head, git_is_dirty, load_bead, load_evidence, write_model
from .models import Actor, BeadStatus, FileRef, GitRef, OpenSpecRef, RunPhase, schema_registry


app = typer.Typer(add_completion=False)
schema_app = typer.Typer(add_completion=False)


def _phase_for_transition(transition: str) -> RunPhase:
    """
    Best-effort mapping from requested transition to RunPhase for journaling.
    Keeps journal compliant with the Loom spec rule that phase reflects where the
    request sits in the lifecycle (plan/implement/verify).
    """
    match = re.match(r"^\s*([^-\s>]+)\s*->\s*([^-\s>]+)\s*$", transition)
    if not match:
        return RunPhase.implement
    to_status = match.group(2).strip()

    if to_status in {"sized", "ready"}:
        return RunPhase.plan
    if to_status in {"in_progress", "verification_pending"}:
        return RunPhase.implement
    if to_status in {"verified", "approval_pending", "done"}:
        return RunPhase.verify

    return RunPhase.implement


def _decision_action_phase(paths: Paths, bead_id: str) -> RunPhase:
    bead = load_bead(paths, bead_id)
    if bead.status in {BeadStatus.draft, BeadStatus.sized, BeadStatus.ready}:
        return RunPhase.plan
    return RunPhase.verify


@app.command()
def validate(path: Path) -> None:
    """Validate an SDLC artifact."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema_name = payload.get("schema_name")
    if not schema_name:
        typer.echo("Missing schema_name")
        raise typer.Exit(code=2)
    registry = schema_registry()
    model = registry.get(schema_name)
    if model is None:
        typer.echo(f"Unknown schema_name: {schema_name}")
        raise typer.Exit(code=2)
    try:
        model.model_validate(payload)
    except ValidationError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2)


@app.command()
def hash(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    typer.echo(sha256_canonical_json(payload))


@app.command("schema-export")
def schema_export(out: Path = Path("sdlc/schemas")) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for schema_name, cls in schema_registry().items():
        schema_version = cls.model_fields["schema_version"].default
        if isinstance(schema_version, int):
            filename = f"{schema_name}.v{schema_version}.json"
            (out / filename).write_text(
                json.dumps(cls.model_json_schema(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )


@schema_app.command("export")
def schema_export_alias(out: Path = Path("sdlc/schemas")) -> None:
    schema_export(out)


@app.command()
def request(
    bead_id: str,
    transition: str,
    actor_kind: str = typer.Option("human", "--actor-kind"),
    actor_name: str = typer.Option(os.getenv("USER", "unknown"), "--actor-name"),
) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind=actor_kind, name=actor_name)
    result = request_transition(paths, bead_id, transition, actor)
    phase = _phase_for_transition(transition)
    record_transition_attempt(paths, bead_id, phase, actor, transition, result)
    if not result.ok:
        raise typer.Exit(code=1)


evidence_app = typer.Typer(add_completion=False)
app.add_typer(evidence_app, name="evidence")


app.add_typer(schema_app, name="schema")


grounding_app = typer.Typer(add_completion=False)
app.add_typer(grounding_app, name="grounding")
openspec_app = typer.Typer(add_completion=False)
app.add_typer(openspec_app, name="openspec")


@evidence_app.command("collect")
def evidence_collect(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    bead = load_bead(paths, bead_id)
    bundle = collect_evidence_skeleton(bead, actor)
    write_model(paths.evidence_path(bead_id), bundle)


@evidence_app.command("validate")
def evidence_validate(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    evidence = load_evidence(paths, bead_id)
    actor = Actor(kind="system", name="sdlc")
    if evidence and evidence.created_by.kind == "human":
        actor = evidence.created_by
    evidence, errors = validate_evidence_bundle(paths, bead_id, actor, mark_validated=True)
    git_ref = GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths))
    record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0 if not errors else 1,
        notes_md="; ".join(errors) if errors else None,
        git=git_ref,
        produced_artifacts=[FileRef(path=f"runs/{bead_id}/evidence.json")],
    )
    from .io import write_execution_record

    write_execution_record(paths, record)
    if errors:
        typer.echo("; ".join(errors))
        raise typer.Exit(code=1)


@evidence_app.command("invalidate-if-stale")
def evidence_invalidate_if_stale(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    reason = invalidate_evidence_if_stale(paths, bead_id, actor)
    if reason:
        typer.echo(reason)


@grounding_app.command("generate")
def grounding_generate(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    generate_grounding_bundle(paths, bead_id, actor)


@app.command()
def approve(bead_id: str, summary: str = typer.Option(..., "--summary")) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="human", name="sdlc")
    if not summary.strip():
        typer.echo("Summary must be non-empty")
        raise typer.Exit(code=2)
    if not summary.startswith("APPROVAL:"):
        typer.echo('Warning: summary should start with "APPROVAL:"', err=True)
    entry = create_approval_entry(bead_id, summary, actor)
    append_decision_entry(paths, entry)


@app.command()
def abort(
    bead_id: str,
    reason: str = typer.Option(..., "--reason"),
    actor_kind: str = typer.Option("human", "--actor-kind"),
    actor_name: str = typer.Option(os.getenv("USER", "unknown"), "--actor-name"),
) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind=actor_kind, name=actor_name)
    entry = create_abort_entry(bead_id, reason, actor)
    append_decision_entry(paths, entry)
    record_decision_action(
        paths,
        entry,
        _decision_action_phase(paths, bead_id),
        actor,
        notes_md="Abort requested",
    )
    bead = load_bead(paths, bead_id)
    requested = f"{bead.status.value} -> {BeadStatus.aborted_needs_discovery.value}"
    result = request_transition(paths, bead_id, requested, actor)
    record_transition_attempt(
        paths,
        bead_id,
        _phase_for_transition(requested),
        actor,
        requested,
        result,
        extra_links=[decision_ledger_link(entry)],
    )
    if not result.ok:
        raise typer.Exit(code=1)


@openspec_app.command("sync")
def openspec_sync(bead_id: str) -> None:
    paths = Paths(Path.cwd())
    bead = load_bead(paths, bead_id)
    if bead.openspec_ref is None:
        typer.echo("Bead.openspec_ref missing")
        raise typer.Exit(code=2)
    artifact_id = bead.openspec_ref.artifact_id
    ref_path = paths.repo_root / "openspec" / "refs" / f"{artifact_id}.json"
    if not ref_path.exists():
        typer.echo(f"OpenSpecRef artifact not found: {ref_path}")
        raise typer.Exit(code=2)
    try:
        ref = OpenSpecRef.model_validate_json(ref_path.read_text(encoding="utf-8"))
    except ValidationError as exc:
        typer.echo(f"OpenSpecRef invalid: {exc}")
        raise typer.Exit(code=2)
    out_path = paths.bead_dir(bead_id) / "openspec_ref.json"
    write_model(out_path, ref)
    typer.echo(str(out_path))
