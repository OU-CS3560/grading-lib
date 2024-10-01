from pathlib import Path

import pytest

from grading_lib.repository import Repository, RepositoryBaseTestCase


def test_Repository_init_with_an_empty_folder(tmp_path) -> None:
    repo = Repository(tmp_path)
    assert isinstance(repo.working_tree_dir, Path)


def test_Repository_create_and_add_random_file(tmp_path) -> None:
    repo = Repository(tmp_path)
    assert isinstance(repo.working_tree_dir, Path)

    repo.create_and_add_random_file(name="a.txt")
    assert len(repo.repo.index.entries) == 1
    assert next(iter(repo.repo.index.entries.keys()))[0] == "a.txt"

    repo.create_and_add_random_file()
    assert len(repo.repo.index.entries) == 2


def test_RepositoryBaseTestCase_assertHasOnlyGitCommand(tmp_path) -> None:
    class Child(RepositoryBaseTestCase):
        pass

    instance = Child()
    instance.setUp()
    try:
        file_path = tmp_path / "answer.sh"
        with open(file_path, "w") as f:
            f.write("# Comment\ntar -xzf repo.tar.gz\ngit status")

        with pytest.raises(AssertionError):
            instance.assertHasOnlyGitCommand(file_path)
    finally:
        instance.tearDown()

    instance.setUp()
    try:
        file_path = tmp_path / "answer.sh"
        with open(file_path, "w") as f:
            f.write("# Comment\n# tar -xzf repo.tar.gz\ngit status")

        instance.assertHasOnlyGitCommand(file_path)

    finally:
        instance.tearDown()
