import json
import os
from pathlib import Path

import click
import tomli


@click.group()
def internal():
    """
    Commands that are not meant for user's direct use.

    These commands are menat to be used by CI or to facilitate a step
    in CI.
    """
    pass


@internal.command(name="collect-autograding-tests")
@click.argument("src_dir", required=False, default=os.getcwd())
@click.option("--out-dir", default=Path(".") / ".github" / "classroom")
def collect_autograding_tests_command(src_dir, out_dir):
    """
    Collect all test cases and put them in .github/classroom/autograding.json.

    This is meant to be used by the GitHub Action's workflow.
    """
    if isinstance(src_dir, str):
        src_dir = Path(src_dir)

    if not src_dir.exists():
        print(f"[error]: target directory '{str(src_dir)}' does not exist")
        click.exit(1)

    if isinstance(out_dir, str):
        out_dir = Path(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    tests = []
    for problem_file_path in src_dir.glob("*/problem.toml"):
        print(f"processing {problem_file_path}")
        with open(problem_file_path, "rb") as in_file:
            data = tomli.load(in_file)
            problem_name = data["problem"]["name"]

            if "tests" in data["problem"]:
                for key, data in data["problem"]["tests"].items():
                    # Modify the run command by preprend it with the
                    # cd command.
                    test = dict()
                    test.update(data)
                    test["name"] = f"{problem_name} - {test['name']}"
                    if len(test["run"].strip()) != 0:
                        test["run"] = f"cd {problem_name} && {test['run']}"

                    tests.append(test)
            else:
                print(
                    " - warning: No test cases found. They may be hidden from the students or not yet implemented."
                )

    autograding_filepath = out_dir / "autograding.json"
    with open(autograding_filepath, "w") as out_file:
        json.dump({"tests": tests}, out_file, indent=2)
