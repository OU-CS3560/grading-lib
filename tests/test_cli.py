import json
import sys
from pathlib import Path

from click.testing import CliRunner

from grading_lib.cli import summary_command
from grading_lib.cli.internal import collect_autograding_tests_command


def test_collect_autograding_tests_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        problem_path = Path("lorem-ipsum")
        problem_path.mkdir()

        with open(problem_path / "problem.toml", "w") as f:
            f.write("""
[problem]
name = "lorem-ipsum"
difficulty = 1
objective = "Example problem for testing the cli command"

[problem.tests.test-1]
name = "cast some spells"
setup = ""
run = "python scripts/grade.py -k cast"
input = ""
output = ""
comparison = "included"
timeout = 10
points = 25
""")

        result = runner.invoke(collect_autograding_tests_command)
        assert result.exit_code == 0
        if sys.platform == "win32":
            assert result.output == "processing lorem-ipsum\\problem.toml\n"
        else:
            assert result.output == "processing lorem-ipsum/problem.toml\n"
        expected_file_path = Path(".github") / "classroom" / "autograding.json"
        assert expected_file_path.exists()
        with open(expected_file_path) as f:
            data = json.load(f)
            assert len(data["tests"]) == 1
            assert data["tests"][0]["name"] == "lorem-ipsum - cast some spells"


def test_summary_command():
    runner = CliRunner()

    # When there is no problem,
    result = runner.invoke(summary_command)
    assert result.exit_code == 0
    assert "Problem Count: 0" in result.output
    assert "Total Points: 0.0" in result.output

    # When there is one problem,
    with runner.isolated_filesystem():
        problem_path = Path("lorem-ipsum")
        problem_path.mkdir()

        with open(problem_path / "problem.toml", "w") as f:
            f.write("""
[problem]
name = "lorem-ipsum"
difficulty = 1
objective = "Example problem for testing the cli command"

[problem.tests.test-1]
name = "cast some spells"
setup = ""
run = "python scripts/grade.py -k cast"
input = ""
output = ""
comparison = "included"
timeout = 10
points = 25
""")

        result = runner.invoke(summary_command)
        assert result.exit_code == 0
        assert "Problem Count: 1" in result.output
        assert "Total Points: 25.0" in result.output
