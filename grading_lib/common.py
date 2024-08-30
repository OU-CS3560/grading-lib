import datetime
import os
import subprocess
import sys
import tempfile
import time
import unittest
from collections import namedtuple
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")

COMMAND_FAILED_TEXT_TEMPLATE = "An error occurred while trying to run a command '{command}'. The command's output is\n\n{output}"
FILE_NOT_EXIST_TEXT_TEMPLATE = "File '{path}' does not exist"
DEFAULT_FILENAME_POOL = ["main.cpp", "file.txt"]
FILE_SUFFIX_POOL = [".cpp", ".txt", ".md", ".zip", ".py", ".toml", ".yml", ".yaml"]
NAME_POOL = ["herta", "cat", "dog", "dolphin", "falcon", "dandilion", "fox", "jett"]


def is_debug_mode(
    variable_name: str = "DEBUG",
    vals_for_true: tuple[str, ...] = ("true", "t", "on", "1"),
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
        except ValueError:
            pass

    return seed_val


def get_mtime_as_datetime(path: Path | str) -> datetime.datetime:
    if isinstance(path, str):
        path = Path(path)

    return datetime.datetime.fromtimestamp(
        path.stat().st_mtime, tz=datetime.timezone.utc
    )


def has_file_changed(last_known_mtime: datetime.datetime, path: Path | str) -> bool:
    new_mtime = get_mtime_as_datetime(path)
    return new_mtime > last_known_mtime


def populate_folder_with_filenames(path: Path | str, filnames: list[str]) -> None:
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


def run_executable(
    args: list[str], cwd: str | Path | None = None, timeout: float = 15.0
) -> CommandResult:
    """
    Run a command at the cwd.

    Return
    - (True, command, output) when the command completes without any error.
    - (False, command, output) when the command completes with error.

    It will redirect stderr to stdout and capture stdout as output.
    """
    try:
        make_cmd_output = subprocess.check_output(
            args, stderr=subprocess.STDOUT, cwd=cwd, timeout=timeout
        )
        return CommandResult(True, " ".join(args), make_cmd_output.decode())
    except subprocess.CalledProcessError as e:
        return CommandResult(False, " ".join(args), e.output.decode())
    except subprocess.TimeoutExpired:
        return CommandResult(
            False, " ".join(args), f"Command timed out after {timeout} seconds."
        )


def ensure_lf_line_ending(path: Path | str) -> CommandResult:
    """Run dos2unix on the file at path.

    Students who are using Windows OS may submit answer.sh that has CRLF as its line
    ending. The CR will ofen get mixed into shell commands in the file and produces
    strange result / error.
    """
    return run_executable(["dos2unix", str(path)])


class MinimalistTestResult(unittest.TextTestResult):
    """TextTestResult without the traceback.

    Traceback is too verbose for our purpose.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dots = False

    def getDescription(self, test: unittest.TestCase) -> str:
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def addFailure(self, test: unittest.TestCase, err) -> None:
        self.failures.append((test, str(err[1]) + "\n"))
        self._mirrorOutput = True

        if self.showAll:
            self._write_status(test, "FAIL")
        elif self.dots:
            self.stream.write("F")
            self.stream.flush()


class BaseTestCaseMeta(type):
    def __new__(cls: T, name: str, bases: list[Any], attrs: dict[str, Any]) -> T:
        if "with_temporary_dir" not in attrs:
            attrs["with_temporary_dir"] = False

        o = super().__new__(cls, name, bases, attrs)
        return o


class BaseTestCase(unittest.TestCase, metaclass=BaseTestCaseMeta):
    """
    A base class for test case.

    :cvar with_temporary_dir: When `True`, create a temporary directory for each test.
    """

    with_temporary_dir: bool  # Added by metaclass.

    def setUp(self) -> None:
        self.is_debug_mode = is_debug_mode()
        self.seed = get_seed_from_env()

        self.temporary_dir = None
        if self.with_temporary_dir:
            if sys.version_info < (3, 12, 0):
                self.temporary_dir = tempfile.TemporaryDirectory(dir=Path("."))
            else:
                self.temporary_dir = tempfile.TemporaryDirectory(
                    dir=Path("."), delete=False
                )
            self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self) -> None:
        if not self.is_debug_mode and self.temporary_dir is not None:
            self.temporary_dir.cleanup()
        elif self.is_debug_mode and self.temporary_dir is not None:
            print(
                f"[info]: The temporary directory at '{self.temporary_dir_path}' is not deleted since the DEBUG is set to True."
            )

    def assertArchiveFileIsGzip(self, path: Path) -> None:
        cmd_result = run_executable(["gunzip", "-t", str(path)])
        self.assertTrue(
            "not in gzip format" not in cmd_result.output,
            msg="Hint: Did you forget to use '-z' flag when creating the archive?",
        )
        self.assertCommandSuccessful(
            cmd_result,
        )

    def assertFileExists(
        self, path: Path, msg_template: str = FILE_NOT_EXIST_TEXT_TEMPLATE
    ) -> None:
        """Pass if the file at `path` exist."""
        if not path.exists():
            msg = msg_template.format(path=str(path))
            raise self.failureException(msg)

    def assertAllFilesExist(self, paths: list[Path], msg: str | None = None) -> None:
        """Pass if all the listed files exist."""
        not_exist: list[Path] = []
        for path in paths:
            if not path.exists():
                not_exist.append(path)
            elif not path.is_file():
                raise self.failureException(
                    f"Expect a file, but '{path!s}' is not a file."
                )

        if len(not_exist) != 0:
            path_strs = [str(p) for p in paths]
            not_exist_strs = [str(p) for p in not_exist]
            if msg is None:
                if len(path_strs) == len(not_exist_strs):
                    msg = """Expect to see all of these files: {paths}.\n\nHowever, none of them can be found."""
                else:
                    msg = """Expect to see all of these files: {paths}.\n\nHowever, these files cannot be found: {not_exist}"""
            raise self.failureException(
                msg.format(paths=path_strs, not_exist=not_exist_strs)
            )

    def assertCommandSuccessful(
        self, result: CommandResult, msg_template: str = COMMAND_FAILED_TEXT_TEMPLATE
    ) -> None:
        """Pass if the command run successfully."""
        if not result.success:
            msg = msg_template.format(command=result.command, output=result.output)
            raise self.failureException(msg)

    def assertCommandOutputEqual(
        self, result: CommandResult, expected_output: str, msg: str | None = None
    ) -> None:
        """
        Pass if the command's output is equal to `output`.

        The `msg` will be formatted with  `command`, `expected_output`, `output`
        """
        if result.output != expected_output:
            if msg is None:
                msg = """
Expect to see output:\n\n{expected_output}
\nHowever, the command '{command}' produces the following output:\n\n{output}
"""
            raise self.failureException(
                msg.format(
                    expected_output=expected_output,
                    command=result.command,
                    output=result.output,
                )
            )


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
