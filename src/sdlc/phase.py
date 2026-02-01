from __future__ import annotations

import re

from .models import RunPhase

_TRANSITION_RE = re.compile(r"^\s*([^-\s>]+)\s*->\s*([^-\s>]+)\s*$")


def phase_for_status_transition(from_status: str, to_status: str) -> RunPhase:
    """
    Best-effort mapping from lifecycle status to RunPhase for journaling.

    Phase should reflect where the request sits in the lifecycle (plan/implement/verify).
    """
    if to_status in {"sized", "ready"}:
        return RunPhase.plan
    if to_status in {"in_progress", "verification_pending"}:
        return RunPhase.implement
    if to_status in {"verified", "approval_pending", "done"}:
        return RunPhase.verify
    return RunPhase.implement


def phase_for_transition_str(transition: str) -> RunPhase:
    """
    Convenience wrapper for mapping a transition string like "ready -> in_progress".
    """
    match = _TRANSITION_RE.match(transition)
    if not match:
        return RunPhase.implement
    to_status = match.group(2).strip()
    return phase_for_status_transition(match.group(1).strip(), to_status)
