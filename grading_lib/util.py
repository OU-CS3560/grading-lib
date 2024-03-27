from pathlib import Path
from typing import Any

import tomli


def load_problems_metadata(path: Path = Path(".")) -> list[dict[str, Any]]:
    """Parse all problem.toml of problems."""
    problems: list[dict[str, Any]] = []
    for problem_file_path in path.glob("*/problem.toml"):
        with open(problem_file_path, "rb") as in_file:
            data = tomli.load(in_file)
            problems.append(data)
    return problems


def get_problem_total_points(problem: dict[str, Any]) -> float:
    total_points = 0.0

    if "tests" not in problem["problem"]:
        return total_points

    for _, test in problem["problem"]["tests"].items():
        total_points += test["points"]
    return total_points
