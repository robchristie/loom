from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable, List, Optional

from ..engine import build_execution_record, detect_changed_files, request_transition, validate_evidence_bundle
from ..io import Paths, load_bead, load_execution_records, load_grounding, write_execution_record
from ..models import Actor, BeadStatus, FileRef, GitRef, RunPhase
from .codex_runner import run_codex
from .codex_runner import CodexRunResult
from .config import AgentSettings
from .evidence_runner import EvidenceRunResult, run_acceptance_checks_to_evidence
from .openrouter import openrouter_model
from .planner import PlannerDeps, run_planner
from .schemas import AgentPlan, OpenSpecDraft, OpenSpecInterview
from .verifier import VerifierDeps, run_verifier
from .openspec_proposer import OpenSpecProposerDeps, run_openspec_draft, run_openspec_interview, run_openspec_synth


def _bead_markdown(bead_id: str, paths: Paths) -> str:
    bead = load_bead(paths, bead_id)
    checks = "\n".join([f"- {c.name}: `{c.command}`" for c in bead.acceptance_checks])
    return (
        f"## {bead.bead_id}: {bead.title}\n"
        f"Status: `{bead.status.value}`\n\n"
        f"### Requirements\n{bead.requirements_md}\n\n"
        f"### Acceptance criteria\n{bead.acceptance_criteria_md}\n\n"
        f"### Context\n{bead.context_md}\n\n"
        f"### Acceptance checks\n{checks or '(none)'}\n"
    )


def _openspec_markdown(paths: Paths, bead_id: str) -> str:
    bead = load_bead(paths, bead_id)
    if bead.openspec_ref is None:
        return "(no openspec_ref linked)"
    ref_path = paths.bead_dir(bead_id) / "openspec_ref.json"
    if not ref_path.exists():
        return f"(openspec_ref.json missing in runs/{bead_id}/; run `sdlc openspec sync {bead_id}`)"
    from ..models import OpenSpecRef

    ref = OpenSpecRef.model_validate_json(ref_path.read_text(encoding="utf-8"))
    return f"Change: `{ref.change_id}`\nState: `{ref.state.value}`\nPath: `{ref.path}`"


def _grounding_markdown(paths: Paths, bead_id: str) -> str:
    bundle = load_grounding(paths, bead_id)
    if bundle is None:
        return "(no grounding bundle present)"
    lines: List[str] = []
    if bundle.summary_md:
        lines.append(bundle.summary_md)
        lines.append("")
    for item in bundle.items[:25]:
        loc = f" ({item.file_ref.path})" if item.file_ref else ""
        snippet = item.content_md
        if len(snippet) > 600:
            snippet = snippet[:600] + "..."
        lines.append(f"- {item.kind}: {item.title}{loc}\n\n{snippet}\n")
    if bundle.allowed_commands:
        lines.append("Allowed commands:")
        lines.extend([f"- `{c}`" for c in bundle.allowed_commands])
    if bundle.disallowed_commands:
        lines.append("Disallowed commands:")
        lines.extend([f"- `{c}`" for c in bundle.disallowed_commands])
    if bundle.excluded_paths:
        lines.append("Excluded paths:")
        lines.extend([f"- `{p}`" for p in bundle.excluded_paths])
    return "\n".join(lines)


def _grounding_policy_markdown(paths: Paths, bead_id: str) -> str:
    """Render command/path constraints from GroundingBundle for prompts."""

    bundle = load_grounding(paths, bead_id)
    if bundle is None:
        return "(no grounding policy present)"

    lines: List[str] = []
    if bundle.allowed_commands:
        lines.append("Allowed commands (prefer these):")
        lines.extend([f"- `{c}`" for c in bundle.allowed_commands])
        lines.append("")
    if bundle.disallowed_commands:
        lines.append("Disallowed commands (do not run):")
        lines.extend([f"- `{c}`" for c in bundle.disallowed_commands])
        lines.append("")
    if bundle.excluded_paths:
        lines.append("Excluded paths (do not modify):")
        lines.extend([f"- `{p}`" for p in bundle.excluded_paths])
        lines.append("")
    return "\n".join(lines).strip() or "(no grounding policy constraints set)"


def build_codex_prompt_md(paths: Paths, bead_id: str) -> str:
    """Build a codex-cli prompt when planner output isn't present.

    This is intentionally deterministic and explicit about constraints.
    """

    return (
        "# Loom Implementation Prompt\n\n"
        + _bead_markdown(bead_id, paths)
        + "\n\n## OpenSpec\n"
        + _openspec_markdown(paths, bead_id)
        + "\n\n## Grounding context\n"
        + _grounding_markdown(paths, bead_id)
        + "\n\n## Grounding policy\n"
        + _grounding_policy_markdown(paths, bead_id)
        + "\n\n## Hard constraints\n"
        + "- Use `uv run` for tests/linters/typecheck\n"
        + "- Do NOT log API keys or secrets\n"
        + "- Prefer modifying files referenced in grounding\n"
    )


def _recent_runs_markdown(paths: Paths, bead_id: str, *, limit: int = 10) -> str:
    records = [r for r in load_execution_records(paths) if r.bead_id == bead_id]
    records = records[-limit:]
    lines: List[str] = []
    for r in records:
        lines.append(
            f"- {r.created_at.isoformat()} phase={r.phase.value} exit={r.exit_code} notes={bool(r.notes_md)}"
        )
    return "\n".join(lines) or "(no prior runs)"


def _grounded_files(paths: Paths, bead_id: str) -> set[str]:
    bundle = load_grounding(paths, bead_id)
    if bundle is None:
        return set()
    file_paths: set[str] = set()
    for item in bundle.items:
        if item.file_ref:
            file_paths.add(item.file_ref.path.lstrip("./"))
    return file_paths


def _policy_violation_notes(changed_files: List[str], grounded_files: set[str]) -> Optional[str]:
    # Exclude runs artifacts and empty grounding.
    relevant = [p for p in changed_files if not p.startswith("runs/")]
    if not grounded_files or not relevant:
        return None
    violations = [p for p in relevant if p not in grounded_files]
    if not violations:
        return None
    return "Out-of-grounding modifications detected: " + ", ".join(sorted(set(violations))[:25])


def _write_json(path: Path, obj: object) -> None:
    from ..io import ensure_parent

    ensure_parent(path)
    if hasattr(obj, "model_dump_json"):
        path.write_text(getattr(obj, "model_dump_json")(indent=2) + "\n", encoding="utf-8")
    else:
        import json

        path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def _write_agent_model(paths: Paths, path: Path, model: object) -> None:
    """Write a non-SDLC artifact JSON (e.g. agent outputs).

    We intentionally do NOT shoehorn these into SchemaBase to avoid breaking existing schemas.
    """

    from ..io import dump_json

    if hasattr(model, "model_dump"):
        # pydantic v2 models
        dump_json(path, getattr(model, "model_dump")(mode="json"))
    else:
        _write_json(path, model)


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _default_openspec_instructions_md(paths: Paths) -> str:
    # These are part of the repo and should be safe to include as grounding for formatting.
    p = paths.repo_root / "openspec" / "AGENTS.md"
    return _read_text_if_exists(p)


def _default_openspec_project_md(paths: Paths) -> str:
    p = paths.repo_root / "openspec" / "project.md"
    return _read_text_if_exists(p)


def _derive_openspec_ref_id(change_id: str) -> str:
    return f"openspec-ref-{change_id}"


def _write_text(path: Path, content: str) -> None:
    from ..io import ensure_parent

    ensure_parent(path)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def run_openspec_propose(
    paths: Paths,
    bead_id: str,
    change_id: str,
    *,
    actor: Actor,
    interactive: bool,
    council: bool,
    settings: AgentSettings | None = None,
    model_override: object | None = None,
    overwrite: bool = False,
    openspec_ref_id: str | None = None,
    answers: list[str] | None = None,
) -> OpenSpecDraft:
    """Draft OpenSpec proposal artifacts for a bead.

    This is an authoring workflow only; it must NOT approve refs or write restricted decision types.
    """

    settings = settings or AgentSettings()
    bead = load_bead(paths, bead_id)

    change_dir = paths.repo_root / "openspec" / "changes" / change_id
    if change_dir.exists() and not overwrite:
        raise FileExistsError(f"OpenSpec change dir exists (use --overwrite): {change_dir}")

    # Models
    model = model_override
    if model is None:
        model = openrouter_model(settings.openspec_primary_model(), settings=settings)

    # Context
    bead_md = _bead_markdown(bead_id, paths)
    grounding_md = _grounding_markdown(paths, bead_id)
    openspec_instr = _default_openspec_instructions_md(paths)
    openspec_proj = _default_openspec_project_md(paths)

    transcript_lines: list[str] = []
    transcript_lines.append(f"# OpenSpec Proposal Interview Transcript\n\nBead: `{bead_id}`\nChange: `{change_id}`\n")

    deps = OpenSpecProposerDeps(
        bead_markdown=bead_md,
        grounding_markdown=grounding_md,
        openspec_instructions_md=openspec_instr,
        openspec_project_md=openspec_proj,
        change_id=change_id,
        interview_transcript_md="",
        non_interactive=not interactive,
    )

    # Interview loop (optional). In server mode, interactive will be False and answers may be provided.
    interview_rounds = 0
    max_rounds = max(0, int(settings.openspec_interview_rounds_max))
    provided_answers = list(answers or [])

    while interactive and interview_rounds < max_rounds:
        deps = OpenSpecProposerDeps(
            bead_markdown=deps.bead_markdown,
            grounding_markdown=deps.grounding_markdown,
            openspec_instructions_md=deps.openspec_instructions_md,
            openspec_project_md=deps.openspec_project_md,
            change_id=deps.change_id,
            interview_transcript_md="\n".join(transcript_lines),
            non_interactive=deps.non_interactive,
        )
        interview: OpenSpecInterview = run_openspec_interview(model, deps)
        if not interview.questions:
            break
        transcript_lines.append(f"\n## Interview round {interview_rounds + 1}\n")
        for q in interview.questions:
            transcript_lines.append(f"### Q: {q}\n")
            a = input("> ").strip()
            transcript_lines.append(f"**A:** {a}\n")
        interview_rounds += 1

    # Non-interactive: include provided Q/A as transcript.
    if not interactive and provided_answers:
        transcript_lines.append("\n## Provided answers\n")
        for idx, a in enumerate(provided_answers, start=1):
            transcript_lines.append(f"- Answer {idx}: {a}\n")

    deps = OpenSpecProposerDeps(
        bead_markdown=deps.bead_markdown,
        grounding_markdown=deps.grounding_markdown,
        openspec_instructions_md=deps.openspec_instructions_md,
        openspec_project_md=deps.openspec_project_md,
        change_id=deps.change_id,
        interview_transcript_md="\n".join(transcript_lines),
        non_interactive=deps.non_interactive,
    )

    # Drafting (single model) or council mode (multiple independent drafts + synth)
    draft: OpenSpecDraft
    models_used: list[str] = []
    if council and settings.openspec_council_models:
        drafts: list[OpenSpecDraft] = []
        for name in settings.openspec_council_models:
            council_model = model_override or openrouter_model(name, settings=settings)
            models_used.append(name)
            drafts.append(run_openspec_draft(council_model, deps))
        synth_model_name = settings.openspec_synth_model_name()
        synth_model = model_override or openrouter_model(synth_model_name, settings=settings)
        models_used.append(synth_model_name)
        draft = run_openspec_synth(synth_model, deps, drafts)
    else:
        # If council requested but no council models configured, fall back to single-model.
        models_used.append(settings.openspec_primary_model())
        draft = run_openspec_draft(model, deps)

    # Write change files
    if not overwrite and change_dir.exists():
        raise FileExistsError(f"OpenSpec change dir exists (use --overwrite): {change_dir}")
    (change_dir / "specs").mkdir(parents=True, exist_ok=True)
    _write_text(change_dir / "proposal.md", draft.proposal_md)
    _write_text(change_dir / "tasks.md", draft.tasks_md)
    if draft.design_md:
        _write_text(change_dir / "design.md", draft.design_md)
    for df in draft.delta_files:
        out = paths.repo_root / df.path
        # Safety: enforce deltas are written under this change-id.
        expected_prefix = f"openspec/changes/{change_id}/specs/"
        if not df.path.startswith(expected_prefix):
            raise ValueError(f"Delta file path must start with {expected_prefix}: {df.path}")
        _write_text(out, df.content)

    # Ensure refs dir exists (repo may not have it yet).
    refs_dir = paths.repo_root / "openspec" / "refs"
    refs_dir.mkdir(parents=True, exist_ok=True)

    from ..models import OpenSpecRef, OpenSpecState
    from ..io import now_utc, write_model

    ref_id = openspec_ref_id or _derive_openspec_ref_id(change_id)
    ref_path = refs_dir / f"{ref_id}.json"
    ref = OpenSpecRef(
        artifact_id=ref_id,
        created_at=now_utc(),
        created_by=Actor(kind="agent", name="sdlc"),
        change_id=change_id,
        state=OpenSpecState.proposal,
        path=f"openspec/changes/{change_id}",
        approved_at=None,
        approved_by=None,
        content_hash=None,
        links=[],
        schema_name="sdlc.openspec_ref",
        schema_version=1,
    )
    write_model(ref_path, ref)

    # Runs artifacts
    agent_json_path = paths.bead_dir(bead_id) / "agent_openspec.json"
    agent_md_path = paths.bead_dir(bead_id) / "agent_openspec.md"
    _write_agent_model(paths, agent_json_path, draft)
    _write_text(agent_md_path, "\n".join(transcript_lines) + "\n\n## Summary\n\n- Generated OpenSpec change artifacts.\n")

    # Journal
    from ..io import git_head, git_is_dirty, write_execution_record
    produced: list[FileRef] = [
        FileRef(path=f"runs/{bead_id}/agent_openspec.json"),
        FileRef(path=f"runs/{bead_id}/agent_openspec.md"),
        FileRef(path=f"openspec/refs/{ref_id}.json"),
        FileRef(path=f"openspec/changes/{change_id}/proposal.md"),
        FileRef(path=f"openspec/changes/{change_id}/tasks.md"),
    ]
    if draft.design_md:
        produced.append(FileRef(path=f"openspec/changes/{change_id}/design.md"))
    for df in draft.delta_files:
        produced.append(FileRef(path=df.path))

    record = build_execution_record(
        bead_id,
        RunPhase.plan,
        actor=actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0,
        commands=[],
        produced_artifacts=sorted({p.path: p for p in produced}.values(), key=lambda r: r.path),
        notes_md="OpenSpec proposal drafted"
        + (f"; council={council}" if council else "")
        + (f"; models={','.join(models_used)}" if models_used else ""),
        git=GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths)),
    )
    write_execution_record(paths, record)

    # Link to bead.openspec_ref is intentionally not done here; that's a separate sync/approval flow.
    _ = bead  # explicitly unused, but ensures bead was loaded for context
    return draft

def run_plan(
    paths: Paths,
    bead_id: str,
    actor: Actor,
    *,
    settings: Optional[AgentSettings] = None,
    model_override: object | None = None,
) -> AgentPlan:
    settings = settings or AgentSettings()

    model = model_override
    if model is None:
        model = openrouter_model(settings.planner_model, settings=settings)

    deps = PlannerDeps(
        bead_markdown=_bead_markdown(bead_id, paths),
        grounding_markdown=_grounding_markdown(paths, bead_id),
        openspec_markdown=_openspec_markdown(paths, bead_id),
    )

    plan = asyncio.run(run_planner(model, deps=deps))

    plan_path = paths.bead_dir(bead_id) / "agent_plan.json"
    prompt_path = paths.bead_dir(bead_id) / "codex_prompt.md"

    _write_agent_model(paths, plan_path, plan)
    prompt_path.write_text(plan.codex_prompt_md + "\n", encoding="utf-8")

    record = build_execution_record(
        bead_id,
        RunPhase.plan,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0,
        commands=[],
        produced_artifacts=[
            FileRef(path=f"runs/{bead_id}/agent_plan.json"),
            FileRef(path=f"runs/{bead_id}/codex_prompt.md"),
        ],
        notes_md="Planner run completed",
    )
    write_execution_record(paths, record)
    return plan


def run_implement(
    paths: Paths,
    bead_id: str,
    actor: Actor,
    *,
    auto_transition: Optional[bool] = None,
    settings: Optional[AgentSettings] = None,
    subprocess_runner: Callable[..., CodexRunResult] = run_codex,
) -> int:
    settings = settings or AgentSettings()
    if auto_transition is None:
        auto_transition = settings.agent_auto_transition

    bead = load_bead(paths, bead_id)
    if auto_transition and bead.status == BeadStatus.ready:
        # Transition requests are always validated by the engine.
        request_transition(paths, bead_id, "ready -> in_progress", Actor(kind="system", name="sdlc"))

    prompt_path = paths.bead_dir(bead_id) / "codex_prompt.md"
    if not prompt_path.exists():
        # Fallback prompt if no planner output exists.
        prompt_path.write_text(build_codex_prompt_md(paths, bead_id) + "\n", encoding="utf-8")

    grounded = _grounded_files(paths, bead_id)

    log_path = paths.bead_dir(bead_id) / "codex.log"
    result = subprocess_runner(
        paths,
        bead_id,
        codex_bin=settings.codex_bin,
        codex_args=settings.codex_args,
        prompt_path=prompt_path,
        log_path=log_path,
    )

    changed_files = detect_changed_files(paths, head_before=result.head_before)
    violation = _policy_violation_notes(changed_files, grounded)

    record = build_execution_record(
        bead_id,
        RunPhase.implement,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=result.exit_code,
        commands=[" ".join(result.command)],
        produced_artifacts=[FileRef(path=f"runs/{bead_id}/codex.log")],
        git=GitRef(
            head_before=result.head_before,
            head_after=result.head_after,
            dirty_before=result.dirty_before,
            dirty_after=result.dirty_after,
        ),
        notes_md=violation,
    )
    write_execution_record(paths, record)

    if auto_transition and result.exit_code == 0:
        bead2 = load_bead(paths, bead_id)
        if bead2.status == BeadStatus.in_progress:
            request_transition(
                paths,
                bead_id,
                "in_progress -> verification_pending",
                Actor(kind="system", name="sdlc"),
            )
    return result.exit_code


def run_verify(
    paths: Paths,
    bead_id: str,
    actor: Actor,
    *,
    auto_transition: Optional[bool] = None,
    settings: Optional[AgentSettings] = None,
    model_override: object | None = None,
    evidence_subprocess_runner: Callable[..., EvidenceRunResult] = run_acceptance_checks_to_evidence,
) -> int:
    settings = settings or AgentSettings()
    if auto_transition is None:
        auto_transition = settings.agent_auto_transition

    bead = load_bead(paths, bead_id)

    # 1) Run acceptance checks and write evidence.json + logs
    evidence_path = paths.evidence_path(bead_id)
    evidence_dir = paths.bead_dir(bead_id) / "evidence"
    result = evidence_subprocess_runner(
        paths,
        bead_id,
        actor=Actor(kind="system", name="sdlc"),
        acceptance_checks=bead.acceptance_checks,
        evidence_path=evidence_path,
        evidence_dir=evidence_dir,
    )

    # Evidence validation requires for_bead_hash; set it prior to engine validation.
    from ..engine import canonical_hash_for_model

    evidence = result.evidence
    evidence.for_bead_hash = canonical_hash_for_model(bead)
    from ..io import write_model

    write_model(evidence_path, evidence)

    # 2) Validate evidence via engine (engine-authored status updates)
    _, errors = validate_evidence_bundle(paths, bead_id, Actor(kind="system", name="sdlc"))
    ok = not errors

    # 3) Optional verifier agent output (advisory)
    verify_artifacts: List[FileRef] = [FileRef(path=f"runs/{bead_id}/evidence.json")]
    verify_path = paths.bead_dir(bead_id) / "agent_verify.json"
    if model_override is not None or settings.openrouter_api_key.strip():
        model = model_override or openrouter_model(settings.verifier_model, settings=settings)
        deps = VerifierDeps(
            bead_markdown=_bead_markdown(bead_id, paths),
            evidence_markdown=evidence_path.read_text(encoding="utf-8")[:4000],
            recent_runs_markdown=_recent_runs_markdown(paths, bead_id),
        )
        verify = asyncio.run(run_verifier(model, deps=deps))
        _write_agent_model(paths, verify_path, verify)
        verify_artifacts.append(FileRef(path=f"runs/{bead_id}/agent_verify.json"))

    # 4) Journal verify run (commands are recorded from the acceptance run)
    from ..io import git_head, git_is_dirty

    record = build_execution_record(
        bead_id,
        RunPhase.verify,
        actor,
        requested_transition=None,
        applied_transition=None,
        exit_code=0 if ok else 1,
        commands=result.commands,
        produced_artifacts=sorted(
            {ref.path: ref for ref in (verify_artifacts + [FileRef(path=p) for p in result.produced_paths if p.startswith("runs/")])}.values(),
            key=lambda r: r.path,
        ),
        notes_md="; ".join(errors) if errors else None,
        git=GitRef(head_before=git_head(paths), dirty_before=git_is_dirty(paths)),
    )
    write_execution_record(paths, record)

    # 5) Optional transition: verification_pending -> verified MUST be system.
    if auto_transition and ok:
        bead_after = load_bead(paths, bead_id)
        if bead_after.status == BeadStatus.verification_pending:
            request_transition(
                paths,
                bead_id,
                "verification_pending -> verified",
                Actor(kind="system", name="sdlc"),
            )
    return 0 if ok else 1
