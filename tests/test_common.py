import os
import time
from pathlib import Path

import pytest

from grading_lib import is_debug_mode
from grading_lib.common import (
    BaseTestCase,
    file_has_correct_sha512_checksum,
    get_mtime_as_datetime,
    get_seed_from_env,
    has_file_changed,
    populate_folder_with_filenames,
    run_executable,
)


def test_is_debug_mode() -> None:
    vals_for_true = ["1", "True", "T", "On", "ON", "t", "true"]
    for val in vals_for_true:
        os.environ["test_DEBUG"] = val
        assert is_debug_mode("test_DEBUG")

    vals_for_false = ["", None, "False", "false", "lorem", "0"]
    for v in vals_for_false:
        if v is None:
            del os.environ["test_DEBUG"]
        else:
            os.environ["test_DEBUG"] = v
        assert is_debug_mode("test_DEBUG") is False


def test_get_seed_from_env() -> None:
    """
    If value is set, should properly parse and use it.

    If not, the value should be the scaled time (to avoid same seed
    for multiple tests). Does not currently check if the return value is
    the scaled time.
    """
    val1 = 123
    os.environ["test_SEED"] = str(val1)
    assert get_seed_from_env("test_SEED") == val1

    val2 = "123not-a-number"
    os.environ["test_SEED"] = str(val2)
    res = get_seed_from_env("test_SEED")
    assert isinstance(res, int)
    assert res != 0


def test_has_file_changed(tmp_path) -> None:
    temp_file = tmp_path / "README.md"
    temp_file.write_text("Hello World!")

    # Take snapshot of the mtime.
    last_known_mtime = get_mtime_as_datetime(temp_file)
    assert not has_file_changed(last_known_mtime, temp_file)

    # Modify the mtime and test.
    time.sleep(1.2)
    temp_file.touch()
    assert has_file_changed(last_known_mtime, temp_file)

    # Take another snapshot.
    last_known_mtime = get_mtime_as_datetime(str(temp_file))
    assert not has_file_changed(last_known_mtime, temp_file)


def test_populate_folder_with_filenames(tmp_path) -> None:
    expected_files = ["a", "b", "c"]
    populate_folder_with_filenames(tmp_path, expected_files)

    # Order should not matter, we just want check that all files are created.
    result_names = sorted([item.name for item in tmp_path.iterdir()])

    assert result_names == expected_files


def test_populate_folder_with_filenames_error_handling(tmp_path) -> None:
    with pytest.raises(ValueError):
        (tmp_path / "a.txt").touch()
        populate_folder_with_filenames(tmp_path / "a.txt", ["a", "b", "c"])

    with pytest.raises(ValueError):
        populate_folder_with_filenames(tmp_path / "src", ["a", "b", "c"])


def test_run_executable() -> None:
    cmd_result = run_executable(["git", "version"])
    assert cmd_result.success
    assert "git version" in cmd_result.output


def test_BaseTestCase() -> None:
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


def test_BaseTestCase_assertArchiveFileIsGzip(tmp_path) -> None:
    class ChildClsWithTempDir(BaseTestCase):
        with_temporary_dir = True

    instance = ChildClsWithTempDir()
    instance.setUp()

    try:
        tmp_file = tmp_path / "sdist.tar.gz"
        tmp_file.write_bytes(b"\x1f\x65")
        with pytest.raises(AssertionError):
            instance.assertArchiveFileIsGzip(str(tmp_file))
    finally:
        instance.tearDown()


def test_file_has_correct_sha512_checksum(tmp_path):
    file_path = tmp_path / "repo.tar.gz"
    with open(file_path, "wb") as f:
        f.write(
            b";fb\xc80^\xd1u*p\x00\xf50\xd1\xc1\x17\xb6\xec\x13\xb6\x1fd\xd5\xe2\xe1\xa0\xc4\xe5a\x0f"
        )

    assert file_has_correct_sha512_checksum(
        "f58345b442700529c9f488df0eb76b805bd26fc347b83f9ff5aead0e06fee6b7fc480a556578be9a202813da0c322b48c5004a9c764f1f6b051a6467827338c8",
        file_path,
    )
