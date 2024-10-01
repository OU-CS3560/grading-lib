
from grading_lib.util import FindProblemList


def test_FindProblemList(tmp_path) -> None:
    with open(tmp_path / "README.md", "w") as f:
        f.write("""
# Homework 0

## Problem List `:problem-list:`

Some paragraph.

- `problem-a`
- `problem-b`

## Fake Problem List

- `problem-c`
""")

    problem_names = FindProblemList.from_file(tmp_path / "README.md")
    assert len(problem_names) == 2

    with open(tmp_path / "README2.md", "w") as f:
        f.write("""
# Homework 0

## Problem List

Some paragraph.

- `problem-a`
- `problem-b`

## Fake Problem List

- `problem-c`
""")

    problem_names = FindProblemList.from_file(tmp_path / "README2.md")
    assert len(problem_names) == 0
