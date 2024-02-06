import datetime
import os
import random
import subprocess
import time
import unittest
from collections import namedtuple
from pathlib import Path
from typing import Optional

COMMAND_FAILED_TEXT_TEMPLATE = "An error occurred while trying to run a command '{command}'. The command's output is\n\n{output}"
FILE_NOT_EXIST_TEXT_TEMPLATE = "File '{path}' does not exist"
DEFAULT_FILENAME_POOL = ["main.cpp", "file.txt"]
FILE_SUFFIX_POOL = [".cpp", ".txt", ".md", ".zip", ".py", ".toml", ".yml", ".yaml"]
NAME_POOL = ["herta", "cat", "dog", "dolphin", "falcon", "dandilion", "fox", "jett"]


def is_debug_mode(
    variable_name: str = "DEBUG", vals_for_true: list[str] = ["true", "t", "on", "1"]
) -> bool:
    """Return True if the DEBUG envrionment variable is presence with value representing 'True'."""
    raw_val = os.environ.get(variable_name, None)

    if raw_val is not None:
        val = raw_val.strip().lower()
        return val in vals_for_true
    return False


def get_seed_from_env(variable_name: str = "SEED") -> int:
    raw_val = os.environ.get(variable_name, None)
    # The test case is done too quickly to use second.
    seed_val = int(time.time() * 1000.0)

    if raw_val is not None:
        try:
            seed_val = int(raw_val)
        except:
            pass

    return seed_val


def get_mtime_as_datetime(path: Path | str) -> datetime.datetime:
    if isinstance(path, str):
        path = Path(path)

    return datetime.datetime.fromtimestamp(path.stat().st_mtime, tz=datetime.UTC)


def has_file_changed(last_known_mtime: datetime.datetime, path: Path | str) -> bool:
    new_mtime = get_mtime_as_datetime(path)
    return new_mtime > last_known_mtime


def populate_folder_with_filenames(path: Path | str, filnames: list[str]):
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        raise ValueError("'path' does not exist")
    if not path.is_dir():
        raise ValueError("'path' is not a directory")

    for name in filnames:
        with open(path / name, "w") as f:
            f.write("")


CommandResult = namedtuple("CommandResult", ["success", "command", "output"])


def run_executable(args, cwd: Optional[str | Path] = None) -> CommandResult:
    """
    Run a command at the cwd.

    Return
    - (True, command, output) when the command completes without any error.
    - (False, command, output) when the command completes with error.

    It will redirect stderr to stdout and capture stdout as output.
    """
    try:
        make_cmd_output = subprocess.check_output(
            args, stderr=subprocess.STDOUT, cwd=cwd
        )
        return CommandResult(True, " ".join(args), make_cmd_output.decode())
    except subprocess.CalledProcessError as e:
        return CommandResult(False, " ".join(args), e.output.decode())


class MinimalistTestResult(unittest.TextTestResult):
    """TextTestResult without the traceback.

    Traceback is too verbose for our purpose.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dots = False

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def addFailure(self, test, err):
        self.failures.append((test, str(err[1]) + "\n"))
        self._mirrorOutput = True

        if self.showAll:
            self._write_status(test, "FAIL")
        elif self.dots:
            self.stream.write("F")
            self.stream.flush()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.is_debug_mode = is_debug_mode()
        self.seed = get_seed_from_env()

    def assertFileExists(
        self, path: Path, msg_template: str = FILE_NOT_EXIST_TEXT_TEMPLATE
    ):
        if not path.exists():
            msg = msg_template.format(path=str(path))
            raise self.failureException(msg)

    def assertCommandSuccessful(
        self, result: CommandResult, msg_template: str = COMMAND_FAILED_TEXT_TEMPLATE
    ):
        if not result.success:
            msg = msg_template.format(command=result.command, output=result.output)
            raise self.failureException(msg)


class GeneratorBase:
    """
    A generator that will be run during the generation.yml workflow.

    It may be called by the grading script to prepare a clean
    copy of the content generated during the generation phase.
    """

    def generate(self, path: Path | str) -> None:
        raise NotImplementedError()

    def run(self, path: Path | str) -> None:
        return self.generate(path)
