import subprocess
import sys
from pathlib import Path

import click

from ..util import load_problems_metadata


@click.group()
def dev() -> None:
    """Grading script's development related commands."""
    pass


@dev.command(name="mypy")
def run_mypy_command() -> None:
    """
    Run mypy on each problem's scripts/ individually.

    If mypy is run on the template's root. It will complain saying that
    there are multiple grade.py module.
    """
    problems = load_problems_metadata()
    for metadata in problems:
        target_dir = Path(".") / metadata["problem"]["name"] / "scripts"
        click.echo(f"Running mypy for {target_dir!s} ...")
        subprocess.run([sys.executable, "-m", "mypy", target_dir])
