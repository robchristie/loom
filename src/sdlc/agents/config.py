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
