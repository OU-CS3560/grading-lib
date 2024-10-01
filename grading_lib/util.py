from pathlib import Path
from typing import Any

import mistletoe
import tomli
from mistletoe.block_token import (
    BlockToken,
    Heading,
    List,
    Paragraph,
    SetextHeading,
)
from mistletoe.span_token import InlineCode, SpanToken


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


class FindProblemList:
    """
    Parse the AST of the markdown file from mistletoe for the problem list.

    The section that has the problem list must be marked with "`::problem-list`"
    with
    """

    def __init__(self):
        self.after_problem_list_marker = False
        self.in_a_list = False
        self.problem_names = []

    @classmethod
    def from_file(cls, file_path: Path) -> list[str]:
        with open(file_path) as f:
            data = f.read()
            document = mistletoe.Document(data)
            obj = cls()
            obj.visit_block(document)
            return obj.problem_names

    def visit_text(self, token: SpanToken) -> None:
        if isinstance(token, InlineCode):
            if hasattr(token, "children") and len(token.children) != 0:
                if self.after_problem_list_marker and self.in_a_list:
                    # print(token.children[0].content)
                    self.problem_names.append(token.children[0].content)
                else:
                    # print(token.children[0].content)
                    if token.children[0].content == ":problem-list:":
                        # print("found marker")
                        self.after_problem_list_marker = True

        elif hasattr(token, "children") and token.children is not None:
            for child in token.children:
                self.visit_text(child)

    def visit_block(self, token: BlockToken) -> None:
        if isinstance(token, Paragraph | SetextHeading | Heading):
            for child in token.children:
                self.visit_text(child)

        if isinstance(token, List):
            self.in_a_list = True
            for child in token.children:
                self.visit_block(child)
            self.in_a_list = False

            if self.after_problem_list_marker:
                self.after_problem_list_marker = False

        for child in token.children:
            if isinstance(child, BlockToken):
                self.visit_block(child)
