from __future__ import annotations

import json
from pathlib import Path
import typer
from pydantic import ValidationError

from .codec import sha256_canonical_json
from .engine import (
    append_decision_entry,
    build_execution_record,
    collect_evidence_skeleton,
    create_approval_entry,
    generate_grounding_bundle,
    invalidate_evidence_if_stale,
    record_transition_attempt,
    request_transition,
    validate_evidence_bundle,
)
from .io import Paths, load_bead, load_evidence, write_model
from .models import Actor, RunPhase, schema_registry


app = typer.Typer(add_completion=False)


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


@app.command()
def request(bead_id: str, transition: str) -> None:
    paths = Paths(Path.cwd())
    actor = Actor(kind="system", name="sdlc")
    result = request_transition(paths, bead_id, transition, actor)
    record_transition_attempt(paths, bead_id, RunPhase.implement, actor, transition, result)
    if not result.ok:
        raise typer.Exit(code=1)


evidence_app = typer.Typer(add_completion=False)
app.add_typer(evidence_app, name="evidence")


grounding_app = typer.Typer(add_completion=False)
app.add_typer(grounding_app, name="grounding")


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
    record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0 if not errors else 1,
        notes_md="; ".join(errors) if errors else None,
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
    entry = create_approval_entry(bead_id, summary, actor)
    append_decision_entry(paths, entry)
