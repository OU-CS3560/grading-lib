import copy
import importlib
import os
import sys
import unittest
from pathlib import Path

import click

from ..common import MinimalistTestResult, MinimalistTestRunner
from ..util import FindProblemList, get_problem_total_points, load_problems_metadata
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
def rebase_todo_injector_command(todo_items_file_path: str, path: str) -> None:
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


@cli.command(name="grade")
@click.argument("path", default=".", type=click.Path(exists=True))
def grade_command(path: str | Path) -> None:
    """Grade problems at path"""
    # Steps:
    # 1. Using mistletoe, parse the README.md in the path for the problem order.
    #    By extracting the list after the inline code token with `:problem-list:` on a heading token.
    # 2. Prepare the tests to execute in that order. Remove or skip the test where the students did not change the content of the target file.
    if isinstance(path, str):
        path = Path(path)
    problem_names = FindProblemList.from_file(path / "README.md")

    if len(problem_names) == 0:
        print("No problem found.")

    current_directory = os.getcwd()
    current_sys_path = copy.copy(sys.path)
    test_programs = []
    for idx, problem_name in enumerate(problem_names, start=1):
        print(f"{idx} - Grading {problem_name} ", flush=True)

        try:
            os.chdir(problem_name)

            # Prepare sys.path for module import.
            sys.path.append(os.getcwd())
            importlib.invalidate_caches()
            mod = importlib.import_module("scripts.grade")

            runner = MinimalistTestRunner(stream=sys.stdout, resultclass=MinimalistTestResult)
            test_program = unittest.main(
                mod, testRunner=runner, argv=[sys.argv[0]], exit=False
            )
            test_programs.append((problem_name, test_program))
        finally:
            os.chdir(current_directory)
            # Without copy, sys.path will be a ref to current_sys_path.
            sys.path = copy.copy(current_sys_path)
            if "scripts.grade" in sys.modules.keys():
                # This will be re-used by Python since we have the same module name in
                # every problem.
                del sys.modules["scripts.grade"]

        print("\n\n", flush=True)

    # Summary.
    print("==== Summary ====")
    total_points = sum([test_program.result.total_points for _, test_program in test_programs])
    student_total_points = 0.0
    for idx, item in enumerate(test_programs, start=1):
        problem_name, test_program = item
        print(f"{idx:>3} - {problem_name:<30}{test_program.result.points:>5} / {test_program.result.total_points:>5}")
        student_total_points += test_program.result.points
    print(f"Total: {student_total_points:>5} / {total_points:>5}")

    if student_total_points < total_points:
        sys.exit(1)


cli.add_command(dev)
cli.add_command(internal)
