from __future__ import annotations

from dataclasses import dataclass

from typing import Any

from pydantic_ai import Agent

from .schemas import AgentVerify


@dataclass(frozen=True)
class VerifierDeps:
    bead_markdown: str
    evidence_markdown: str
    recent_runs_markdown: str


def build_verifier_agent(model: Any) -> Agent[VerifierDeps, AgentVerify]:
    system_prompt = (
        "You are the Loom Verifier Agent. Review evidence and recent runs. "
        "You MUST NOT propose mutating bead artifacts or requesting transitions. "
        "You may suggest additional acceptance checks as advisory text only."
    )
    return Agent(
        model=model,
        output_type=AgentVerify,
        system_prompt=system_prompt,
        deps_type=VerifierDeps,
    )


async def run_verifier(model: object, *, deps: VerifierDeps) -> AgentVerify:
    agent = build_verifier_agent(model)
    prompt = (
        "Verify the bead using available evidence.\n\n"
        "# Bead\n"
        f"{deps.bead_markdown}\n\n"
        "# Evidence\n"
        f"{deps.evidence_markdown}\n\n"
        "# Recent execution records\n"
        f"{deps.recent_runs_markdown}\n"
    )
    result = await agent.run(prompt, deps=deps)
    return result.output
