from pathlib import Path

import click

from ..util import get_problem_total_points, load_problems_metadata
from .dev import dev
from .internal import internal


@click.group()
def cli() -> None:
    pass


@cli.command(name="help")
@click.pass_context
def show_help(ctx: click.Context) -> None:
    """Show this help messages."""
    click.echo(cli.get_help(ctx))


@cli.command(name="summary")
def summary_command() -> None:
    """
    Summarize the problem set.
    """
    problems = load_problems_metadata()

    problem_points: list[float] = []
    for problem in problems:
        problem_points.append(get_problem_total_points(problem))

    total_points = sum(problem_points)
    print(f"Problem Count: {len(problems)}")
    print(f"Total Points: {total_points:.2f}")
    for problem, points in zip(problems, problem_points, strict=False):
        name = problem["problem"]["name"]
        score_section = f"{points:.2f} / {total_points:.2f}"
        print(f" - {name:<40} {score_section:>20}")


@cli.command(name="rebase-todo-injector")
@click.argument("todo_items_file_path")
@click.argument("path")
def rebase_todo_injector_command(todo_items_file_path, path) -> None:
    """
    An 'editor' that inject pre-made todo items for git interactive rebase.

    It assumes that the pre-made todo items file is named 'rebase-todo-items.txt'
    and it is in the current working directory.

    This command cannot be used directly, you want to create a script file that call
    this command.

    Example script file:
    #!/bin/bash
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    python -m grading_lib rebase-todo-injector $SCRIPT_DIR/../rebase-todo-items.txt $1
    """
    todo_items_file_path = Path(todo_items_file_path)
    if not todo_items_file_path.exists():
        # formatter does not correctly format this expression if use in f-string.
        cwd = Path(".").absolute()
        raise FileNotFoundError(
            f"Cannot find '{todo_items_file_path}' in the current working directory (cwd='{cwd}')"
        )
    with open(todo_items_file_path) as in_f:
        todo_items_content = in_f.read()

        with open(path, "w") as out_f:
            out_f.write(todo_items_content)


cli.add_command(dev)
cli.add_command(internal)
