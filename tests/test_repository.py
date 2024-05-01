import sys
import tempfile
from pathlib import Path

import pytest

from grading_lib.repository import Repository


@pytest.fixture
def an_empty_folder():
    if sys.version_info < (3, 12, 0):
        temp_dir = tempfile.TemporaryDirectory()
    else:
        temp_dir = tempfile.TemporaryDirectory(delete=False)
    yield temp_dir
    temp_dir.cleanup()


def test_Repository_init_with_an_empty_folder(an_empty_folder):
    repo = Repository(an_empty_folder.name)
    assert isinstance(repo.working_tree_dir, Path)


def test_Repository_create_and_add_random_file(an_empty_folder):
    repo = Repository(an_empty_folder.name)
    assert isinstance(repo.working_tree_dir, Path)

    repo.create_and_add_random_file(name="a.txt")
    assert len(repo.repo.index.entries) == 1
    assert next(iter(repo.repo.index.entries.keys()))[0] == "a.txt"

    repo.create_and_add_random_file()
    assert len(repo.repo.index.entries) == 2
