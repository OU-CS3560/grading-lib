"""
Makefile related routines.
"""
from pathlib import Path
from typing import Optional, Tuple

from .common import run_executable, CommandResult


def run_targets(targets: list[str], cwd: Optional[str | Path] = None) -> CommandResult:
    """
    Invoke the target(s) in the Makefile.

    Return True if the call is successful, False otherwise.
    Also return the output of the executation.
    """
    return run_executable(["make"] + targets, cwd=cwd)
