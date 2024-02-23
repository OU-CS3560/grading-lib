import os
import tempfile
import time
from pathlib import Path

import pytest

from grading_lib import is_debug_mode
from grading_lib.common import get_mtime_as_datetime, has_file_changed


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


@pytest.fixture
def a_temp_file():
    f = tempfile.NamedTemporaryFile()
    f.seek(0)
    yield f
    f.close()


def test_has_file_changed(a_temp_file):
    path = Path(a_temp_file.name)

    last_known_mtime = get_mtime_as_datetime(path)
    assert not has_file_changed(last_known_mtime, path)

    time.sleep(2)
    path.touch()
    assert has_file_changed(last_known_mtime, path)
