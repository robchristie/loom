from __future__ import annotations

from dataclasses import dataclass

from typing import Any

from pydantic_ai import Agent

from .schemas import AgentPlan


@dataclass(frozen=True)
class PlannerDeps:
    bead_markdown: str
    grounding_markdown: str
    openspec_markdown: str


def build_planner_agent(model: Any) -> Agent[PlannerDeps, AgentPlan]:
    # The system prompt is intentionally explicit about outputs: we want a typed
    # plan with a copy/pastable codex prompt.
    system_prompt = (
        "You are the Loom Planner Agent. Produce a concise plan and a codex-cli prompt. "
        "Do not invent files; prefer repo paths mentioned in grounding. "
        "Never include secrets."
    )
    return Agent(
        model=model,  # tests can pass a pydantic_ai.models.test.TestModel
        output_type=AgentPlan,
        system_prompt=system_prompt,
        deps_type=PlannerDeps,
    )


async def run_planner(model: object, *, deps: PlannerDeps) -> AgentPlan:
    agent = build_planner_agent(model)
    prompt = (
        "Plan the work for this bead and create a codex prompt.\n\n"
        "Your codex prompt MUST include:\n"
        "- the bead requirements + acceptance checks\n"
        "- grounding policy constraints (allowed/disallowed commands, excluded paths)\n"
        "- instruction to use `uv run` for tests/linters/typecheck\n\n"
        "# Bead\n"
        f"{deps.bead_markdown}\n\n"
        "# OpenSpec\n"
        f"{deps.openspec_markdown}\n\n"
        "# Grounding\n"
        f"{deps.grounding_markdown}\n"
    )
    result = await agent.run(prompt, deps=deps)
    return result.output
