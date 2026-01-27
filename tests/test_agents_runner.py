from __future__ import annotations

import json
from pathlib import Path

from pydantic_ai.models.test import TestModel

from sdlc.agents.runner import run_implement, run_plan, run_verify
from sdlc.io import Paths, dump_json
from sdlc.models import Actor


def _write_min_bead(paths: Paths, bead_id: str) -> None:
    bead = {
        "schema_name": "sdlc.bead",
        "schema_version": 1,
        "artifact_id": bead_id,
        "created_at": "2026-01-27T00:00:00Z",
        "created_by": {"kind": "system", "name": "test"},
        "bead_id": bead_id,
        "title": "Test bead",
        "bead_type": "implementation",
        "status": "ready",
        "priority": 3,
        "requirements_md": "Do the thing.",
        "acceptance_criteria_md": "It works.",
        "context_md": "",
        "acceptance_checks": [
            {
                "name": "pytest",
                "command": "python -c \"import sys; sys.exit(0)\"",
                "expect_exit_code": 0,
            }
        ],
    }
    dump_json(paths.bead_path(bead_id), bead)


def test_plan_persists_outputs_and_journals(tmp_path: Path) -> None:
    paths = Paths(tmp_path)
    bead_id = "work-test.agent"
    _write_min_bead(paths, bead_id)
    actor = Actor(kind="agent", name="tester")

    # Use TestModel so no network calls happen.
    plan_model = TestModel(
        custom_output_args={
            "summary_md": "ok",
            "step_plan": [{"title": "step", "description_md": ""}],
            "files_to_focus": ["src/sdlc/cli.py"],
            "codex_prompt_md": "Run codex to implement changes.",
        }
    )
    plan = run_plan(paths, bead_id, actor, model_override=plan_model)

    assert (paths.bead_dir(bead_id) / "agent_plan.json").exists()
    assert (paths.bead_dir(bead_id) / "codex_prompt.md").exists()
    assert "codex" in (paths.bead_dir(bead_id) / "codex_prompt.md").read_text(encoding="utf-8").lower()
    assert plan.codex_prompt_md

    journal = paths.journal_path.read_text(encoding="utf-8").splitlines()
    assert len(journal) >= 1
    last = json.loads(journal[-1])
    assert last["phase"] == "plan"
    assert last["exit_code"] == 0


def test_implement_writes_log_and_journals(tmp_path: Path) -> None:
    paths = Paths(tmp_path)
    bead_id = "work-test.impl"
    _write_min_bead(paths, bead_id)
    actor = Actor(kind="agent", name="tester")

    prompt = paths.bead_dir(bead_id) / "codex_prompt.md"
    # Ensure we exercise the fallback prompt builder.
    if prompt.exists():
        prompt.unlink()

    def fake_codex(
        paths: Paths,
        bead_id: str,
        *,
        codex_bin: str,
        codex_args: list[str],
        prompt_path: Path,
        log_path: Path,
    ):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("ok", encoding="utf-8")
        from sdlc.agents.codex_runner import CodexRunResult

        return CodexRunResult(
            command=[codex_bin, *codex_args],
            exit_code=0,
            head_before=None,
            head_after=None,
            dirty_before=None,
            dirty_after=None,
        )

    code = run_implement(paths, bead_id, actor, subprocess_runner=fake_codex)
    assert code == 0
    assert (paths.bead_dir(bead_id) / "codex.log").exists()

    # Fallback prompt includes grounding policy + uv run guidance.
    prompt_text = (paths.bead_dir(bead_id) / "codex_prompt.md").read_text(encoding="utf-8")
    assert "allowed commands" in prompt_text.lower() or "no grounding policy" in prompt_text.lower()
    assert "uv run" in prompt_text.lower()

    last = json.loads(paths.journal_path.read_text(encoding="utf-8").splitlines()[-1])
    assert last["phase"] == "implement"
    assert last["exit_code"] == 0


def test_verify_runs_acceptance_checks_and_validates(tmp_path: Path) -> None:
    paths = Paths(tmp_path)
    bead_id = "work-test.verify"
    _write_min_bead(paths, bead_id)
    actor = Actor(kind="agent", name="tester")

    verify_model = TestModel(
        custom_output_args={
            "summary_md": "ok",
            "risks": [],
            "recommended_acceptance_checks": [],
            "verdict": "pass",
        }
    )
    code = run_verify(paths, bead_id, actor, model_override=verify_model)
    assert code == 0
    evidence_path = paths.evidence_path(bead_id)
    assert evidence_path.exists()
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence["status"] == "validated"
    assert (paths.bead_dir(bead_id) / "evidence" / "pytest.log").exists()
