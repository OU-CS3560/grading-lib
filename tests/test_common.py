import os
import tempfile
import time
from pathlib import Path

import pytest

from grading_lib import is_debug_mode
from grading_lib.common import (
    BaseTestCase,
    get_mtime_as_datetime,
    get_seed_from_env,
    has_file_changed,
    populate_folder_with_filenames,
    run_executable,
)


def test_is_debug_mode():
    vals_for_true = ["1", "True", "T", "On", "ON", "t", "true"]
    for val in vals_for_true:
        os.environ["test_DEBUG"] = val
        assert is_debug_mode("test_DEBUG")

    vals_for_false = ["", None, "False", "false", "lorem", "0"]
    for val in vals_for_false:
        if val is None:
            del os.environ["test_DEBUG"]
        else:
            os.environ["test_DEBUG"] = val
        assert is_debug_mode("test_DEBUG") is False


def test_get_seed_from_env():
    """
    If value is set, should properly parse and use it.

    If not, the value should be the scaled time (to avoid same seed
    for multiple tests). Does not currently check if the return value is
    the scaled time.
    """
    val = 123
    os.environ["test_SEED"] = str(val)
    assert get_seed_from_env("test_SEED") == val

    val = "123not-a-number"
    os.environ["test_SEED"] = str(val)
    res = get_seed_from_env("test_SEED")
    assert isinstance(res, int)
    assert res != 0


@pytest.fixture
def a_temp_file():
    f = tempfile.NamedTemporaryFile()
    f.seek(0)
    yield f
    f.close()


def test_has_file_changed(a_temp_file):
    path = Path(a_temp_file.name)

    # Take snapshot of the mtime.
    last_known_mtime = get_mtime_as_datetime(path)
    assert not has_file_changed(last_known_mtime, path)

    # Modify the mtime and test.
    time.sleep(1.2)
    path.touch()
    assert has_file_changed(last_known_mtime, path)

    # Take another snapshot.
    last_known_mtime = get_mtime_as_datetime(str(path))
    assert not has_file_changed(last_known_mtime, path)


def test_populate_folder_with_filenames():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        with pytest.raises(ValueError):
            (tmpdir_path / "a.txt").touch()
            populate_folder_with_filenames(tmpdir_path / "a.txt", ["a", "b", "c"])

        with pytest.raises(ValueError):
            populate_folder_with_filenames(tmpdir_path / "src", ["a", "b", "c"])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        expected_files = ["a", "b", "c"]
        populate_folder_with_filenames(tmpdir, expected_files)

        # Order should not matter, we just want check that all files are created.
        result_names = sorted([item.name for item in tmpdir_path.iterdir()])

        assert result_names == expected_files


def test_run_executable():
    cmd_result = run_executable(["git", "version"])
    assert cmd_result.success
    assert "git version" in cmd_result.output


def test_BaseTestCase():
    """Tests for the BaseTestCase."""

    # When with_temporary_dir is not specified,
    class ChildClsWithoutTempDir(BaseTestCase):
        pass

    assert ChildClsWithoutTempDir.with_temporary_dir is False

    # When with_temporary_dir is specified,
    class ChildClsWithTempDir(BaseTestCase):
        with_temporary_dir = True

    instance = ChildClsWithTempDir()
    instance.setUp()
    try:
        assert instance.temporary_dir is not None
        assert isinstance(instance.temporary_dir_path, Path)
    finally:
        instance.tearDown()


def test_BaseTestCase_assertArchiveFileIsGzip():
    class ChildClsWithTempDir(BaseTestCase):
        with_temporary_dir = True

    instance = ChildClsWithTempDir()
    instance.setUp()

    try:
        with tempfile.TemporaryFile() as tmp_file:
            with pytest.raises(AssertionError):
                instance.assertArchiveFileIsGzip(tmp_file)
    finally:
        instance.tearDown()
