import click

from ..util import get_problem_total_points, load_problems_metadata
from .dev import dev
from .internal import internal


@click.group()
def cli():
    pass


@cli.command(name="help")
@click.pass_context
def show_help(ctx):
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
    for problem, points in zip(problems, problem_points):
        name = problem["problem"]["name"]
        score_section = f"{points:.2f} / {total_points:.2f}"
        print(f" - {name:<40} {score_section:>20}")


cli.add_command(dev)
cli.add_command(internal)
