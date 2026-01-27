from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import List, Optional

from ..io import Paths, ensure_parent, git_head, git_is_dirty


@dataclass(frozen=True)
class CodexRunResult:
    command: List[str]
    exit_code: int
    head_before: Optional[str]
    head_after: Optional[str]
    dirty_before: Optional[bool]
    dirty_after: Optional[bool]


def run_codex(
    paths: Paths,
    bead_id: str,
    *,
    codex_bin: str,
    codex_args: List[str],
    prompt_path: Path,
    log_path: Path,
) -> CodexRunResult:
    """Run codex-cli.

    This is a thin wrapper around subprocess execution so it can be stubbed in tests.
    """

    ensure_parent(log_path)

    head_before = git_head(paths)
    dirty_before = git_is_dirty(paths)

    cmd = [codex_bin, *codex_args]

    # Feed the prompt via stdin to avoid codex-specific flags.
    stdin_bytes = prompt_path.read_bytes()
    proc = subprocess.run(
        cmd,
        cwd=paths.repo_root,
        input=stdin_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    log_path.write_bytes(proc.stdout)

    head_after = git_head(paths)
    dirty_after = git_is_dirty(paths)

    return CodexRunResult(
        command=cmd,
        exit_code=proc.returncode,
        head_before=head_before,
        head_after=head_after,
        dirty_before=dirty_before,
        dirty_after=dirty_after,
    )

