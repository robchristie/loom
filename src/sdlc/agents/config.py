from __future__ import annotations

from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """Env-driven settings for agentic runs.

    Note: API keys MUST NOT be logged.
    """

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    # Defaults are set via BaseSettings, but we also give mypy explicit defaults.
    openrouter_api_key: str = Field(default="", validation_alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", validation_alias="LOOM_OPENROUTER_BASE_URL"
    )
    planner_model: str = Field(default="openai/gpt-4o-mini", validation_alias="LOOM_PLANNER_MODEL")
    verifier_model: str = Field(default="openai/gpt-4o-mini", validation_alias="LOOM_VERIFIER_MODEL")

    # OpenSpec proposal authoring
    openspec_model: str = Field(default="", validation_alias="LOOM_OPENSPEC_MODEL")
    openspec_council_models: List[str] = Field(default_factory=list, validation_alias="LOOM_OPENSPEC_COUNCIL_MODELS")
    openspec_synth_model: str = Field(default="", validation_alias="LOOM_OPENSPEC_SYNTH_MODEL")
    openspec_interview_rounds_max: int = Field(default=2, validation_alias="LOOM_OPENSPEC_INTERVIEW_ROUNDS_MAX")
    openspec_interactive_default: bool = Field(default=True, validation_alias="LOOM_OPENSPEC_INTERACTIVE_DEFAULT")

    codex_bin: str = Field(default="codex", validation_alias="LOOM_CODEX_BIN")
    codex_args: List[str] = Field(default_factory=list, validation_alias="LOOM_CODEX_ARGS")

    agent_auto_transition: bool = Field(default=False, validation_alias="LOOM_AGENT_AUTO_TRANSITION")

    @field_validator("codex_args", mode="before")
    @classmethod
    def _parse_codex_args(cls, v: object) -> List[str]:
        # Support both JSON array and a simple whitespace-separated string.
        if v is None:
            return []
        if isinstance(v, list):
            return [str(item) for item in v]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            # JSON array is preferred if args include spaces/quotes.
            if s.startswith("["):
                import json

                loaded = json.loads(s)
                if not isinstance(loaded, list):
                    raise ValueError("LOOM_CODEX_ARGS must be a JSON list or a string")
                return [str(item) for item in loaded]
            return s.split()
        raise ValueError("LOOM_CODEX_ARGS must be a JSON list or a string")

    @field_validator("openspec_model", mode="before")
    @classmethod
    def _default_openspec_model(cls, v: object) -> str:
        if v is None:
            return ""
        if isinstance(v, str):
            return v.strip()
        return str(v)

    @field_validator("openspec_synth_model", mode="before")
    @classmethod
    def _default_openspec_synth_model(cls, v: object) -> str:
        if v is None:
            return ""
        if isinstance(v, str):
            return v.strip()
        return str(v)

    @field_validator("openspec_council_models", mode="before")
    @classmethod
    def _parse_openspec_council_models(cls, v: object) -> List[str]:
        # Support JSON array, comma-separated string, or empty.
        if v is None:
            return []
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):
                import json

                loaded = json.loads(s)
                if not isinstance(loaded, list):
                    raise ValueError("LOOM_OPENSPEC_COUNCIL_MODELS must be a JSON list or a string")
                return [str(item).strip() for item in loaded if str(item).strip()]
            return [p.strip() for p in s.split(",") if p.strip()]
        raise ValueError("LOOM_OPENSPEC_COUNCIL_MODELS must be a JSON list or a string")

    def openspec_primary_model(self) -> str:
        return self.openspec_model or self.planner_model

    def openspec_synth_model_name(self) -> str:
        return self.openspec_synth_model or self.openspec_primary_model()
