from __future__ import annotations

from pydantic_ai.models.openrouter import OpenRouterModel

# OpenRouterProvider isn't re-exported cleanly in type stubs in some versions.
from pydantic_ai.models.openrouter import OpenRouterProvider  # type: ignore[attr-defined]

from .config import AgentSettings


def openrouter_model(model_name: str, *, settings: AgentSettings) -> OpenRouterModel:
    """Create an OpenRouterModel without leaking secrets.

    OpenRouterModel pulls credentials from the environment by default.
    We validate config ourselves to provide actionable errors.
    """

    if not settings.openrouter_api_key.strip():
        raise ValueError(
            "OPENROUTER_API_KEY is required for planner/verifier runs. "
            "Set OPENROUTER_API_KEY or disable agent calls in tests."
        )

    provider = OpenRouterProvider(api_key=settings.openrouter_api_key)
    # base_url override isn't currently exposed on the Provider; we keep the
    # setting for forward compatibility.
    return OpenRouterModel(model_name, provider=provider)
