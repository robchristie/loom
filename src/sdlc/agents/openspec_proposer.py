from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, List, Sequence, cast

from pydantic_ai import Agent

from .schemas import OpenSpecDraft, OpenSpecInterview


@dataclass(frozen=True)
class OpenSpecProposerDeps:
    bead_markdown: str
    grounding_markdown: str
    openspec_instructions_md: str
    openspec_project_md: str
    change_id: str
    interview_transcript_md: str
    non_interactive: bool


_SYSTEM_CONSTRAINTS_MD = """\
## Hard constraints (MUST follow)
- Generate OpenSpec artifacts ONLY (no code changes).
- NEVER auto-approve any OpenSpecRef (approval is human-only via CLI).
- Do NOT create DecisionLedgerEntry records of restricted types (approval/exception/assumption/tradeoff/scope_change).
- Outputs MUST be valid Markdown.

## OpenSpec formatting rules (MUST follow)
- Delta specs use sections: `## ADDED Requirements`, `## MODIFIED Requirements`, etc.
- Each delta requirement uses `### Requirement: ...`
- Each requirement MUST have at least one `#### Scenario:` with WHEN/THEN bullets.
"""


def _interview_agent() -> Agent[OpenSpecProposerDeps, OpenSpecInterview]:
    return Agent(
        output_type=OpenSpecInterview,
        system_prompt=(
            "You are an OpenSpec proposal interviewer.\n"
            "Your task: ask clarifying questions to draft an OpenSpec change proposal.\n\n"
            + _SYSTEM_CONSTRAINTS_MD
        ),
    )


def _drafter_agent() -> Agent[OpenSpecProposerDeps, OpenSpecDraft]:
    return Agent(
        output_type=OpenSpecDraft,
        system_prompt=(
            "You are an OpenSpec proposal drafter.\n"
            "Your task: generate OpenSpec change artifacts for the requested change-id.\n\n"
            + _SYSTEM_CONSTRAINTS_MD
            + "\n## Output rules (MUST follow)\n"
            + "- proposal_md: full contents of `openspec/changes/<change-id>/proposal.md`\n"
            + "- tasks_md: full contents of `openspec/changes/<change-id>/tasks.md` (checkbox list)\n"
            + "- design_md: ONLY if needed (otherwise null)\n"
            + "- delta_files: at least one file under `openspec/changes/<change-id>/specs/<capability>/spec.md`\n"
            + "- Ensure delta spec content includes scenarios (`#### Scenario:` headers).\n"
        ),
    )


def _synth_agent() -> Agent[OpenSpecProposerDeps, OpenSpecDraft]:
    return Agent(
        output_type=OpenSpecDraft,
        system_prompt=(
            "You are an OpenSpec council synthesizer.\n"
            "Your task: merge multiple draft proposals into one consistent final OpenSpecDraft.\n\n"
            + _SYSTEM_CONSTRAINTS_MD
            + "\n## Council synthesis rules\n"
            + "- Prefer clarity and consistency over novelty.\n"
            + "- Output ONE final artifact set; do not include multiple alternatives.\n"
        ),
    )


def run_openspec_interview(model: object, deps: OpenSpecProposerDeps) -> OpenSpecInterview:
    prompt = (
        f"Change-id: `{deps.change_id}`\n\n"
        "Ask the minimum set of clarifying questions needed to author an OpenSpec proposal.\n"
        "If the user context is already sufficient, return an empty questions list.\n\n"
        "## Bead\n"
        + deps.bead_markdown
        + "\n\n## Grounding\n"
        + deps.grounding_markdown
        + "\n\n## OpenSpec instructions\n"
        + deps.openspec_instructions_md
        + "\n\n## OpenSpec project conventions\n"
        + deps.openspec_project_md
    )
    agent = _interview_agent()
    result = asyncio.run(agent.run(prompt, deps=deps, model=cast(Any, model)))
    return result.output


def run_openspec_draft(model: object, deps: OpenSpecProposerDeps) -> OpenSpecDraft:
    prompt = (
        f"Change-id: `{deps.change_id}`\n\n"
        "Draft the OpenSpec change artifacts for this change-id.\n"
        "If running non-interactively, you MUST record key assumptions in the proposal.\n\n"
        "## Bead\n"
        + deps.bead_markdown
        + "\n\n## Grounding\n"
        + deps.grounding_markdown
        + "\n\n## Interview transcript\n"
        + (deps.interview_transcript_md or "(none)")
        + "\n\n## OpenSpec instructions\n"
        + deps.openspec_instructions_md
        + "\n\n## OpenSpec project conventions\n"
        + deps.openspec_project_md
    )
    agent = _drafter_agent()
    result = asyncio.run(agent.run(prompt, deps=deps, model=cast(Any, model)))
    return result.output


def run_openspec_synth(
    model: object, deps: OpenSpecProposerDeps, drafts: Sequence[OpenSpecDraft]
) -> OpenSpecDraft:
    # Provide drafts in-band as markdown for simplicity/determinism.
    blocks: List[str] = []
    for i, d in enumerate(drafts, start=1):
        delta_paths = ", ".join([f.path for f in d.delta_files]) or "(none)"
        blocks.append(
            "\n".join(
                [
                    f"## Draft {i}",
                    f"- change_id: `{d.change_id}`",
                    f"- delta_files: {delta_paths}",
                    "",
                    "### proposal_md",
                    d.proposal_md,
                    "",
                    "### tasks_md",
                    d.tasks_md,
                    "",
                    "### design_md",
                    d.design_md or "(none)",
                    "",
                ]
            )
        )
    prompt = (
        f"Change-id: `{deps.change_id}`\n\n"
        "Synthesize ONE final OpenSpecDraft from the following drafts.\n\n" + "\n\n".join(blocks)
    )
    agent = _synth_agent()
    result = asyncio.run(agent.run(prompt, deps=deps, model=cast(Any, model)))
    return result.output
