"""
Collect the tests from the problems and write to .github/classroom/autograding.json

Hopefully, this make the problem in the assignment modular enough
that we can add or remove them as we please.
"""

import json
import os
import sys
import warnings
from argparse import Namespace
from pathlib import Path

import tomli


def main(args: Namespace) -> None:
    warnings.warn(
        "This is depreated in the favor of cli module", DeprecationWarning, stacklevel=2
    )
    target_dir = args.dir
    if isinstance(target_dir, str):
        target_dir = Path(target_dir)

    if not target_dir.exists():
        print(f"[error]: target directory '{target_dir!s}' does not exist")
        sys.exit(1)

    out_dir = args.out_dir
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    tests = []
    for problem_file_path in target_dir.glob("*/problem.toml"):
        print(f"processing {problem_file_path}")
        with open(problem_file_path, "rb") as in_file:
            data = tomli.load(in_file)
            problem_name = data["problem"]["name"]
            for _, test_entry in data["problem"]["tests"].items():
                # Modify the run command by preprend it with the
                # cd command.
                test = dict()
                test.update(test_entry)
                test["name"] = f"{problem_name} - {test['name']}"
                if len(test["run"].strip()) != 0:
                    test["run"] = f"cd {problem_name} && {test['run']}"

                tests.append(test)

    autograding_filepath = out_dir / "autograding.json"
    with open(autograding_filepath, "w") as out_file:
        json.dump({"tests": tests}, out_file, indent=2)


if __name__ == "__main__":
    # Using argparse, so we have one less dependency.
    # Eventually, click may be used.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", default=os.getcwd())
    parser.add_argument(
        "--out-dir", action="store", default=Path(".") / ".github" / "classroom"
    )
    args = parser.parse_args()
    main(args)
