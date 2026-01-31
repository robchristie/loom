from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class _AgentBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentPlanStep(_AgentBase):
    title: str
    description_md: str = ""


class AgentPlan(_AgentBase):
    summary_md: str
    step_plan: List[AgentPlanStep] = Field(default_factory=list)
    files_to_focus: List[str] = Field(default_factory=list)
    codex_prompt_md: str


class VerifyVerdict(str, Enum):
    passed = "pass"
    needs_changes = "needs_changes"


class AgentVerify(_AgentBase):
    summary_md: str
    risks: List[str] = Field(default_factory=list)
    recommended_acceptance_checks: List[str] = Field(default_factory=list)
    verdict: VerifyVerdict = VerifyVerdict.passed


class OpenSpecInterview(_AgentBase):
    questions: List[str] = Field(default_factory=list)


class OpenSpecDraftFile(_AgentBase):
    path: str
    content: str


class OpenSpecDraft(_AgentBase):
    change_id: str
    proposal_md: str
    tasks_md: str
    design_md: str | None = None
    delta_files: List[OpenSpecDraftFile] = Field(default_factory=list)
