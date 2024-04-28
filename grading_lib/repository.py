import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from git import Head, Repo
from git.refs.tag import Tag
from git.repo.fun import is_git_dir
from git.util import IterableList

from .common import BaseTestCase


class Repository:
    """
    A wrapper over git.Repo with our own utilities.

    :param path: A path to repository folder. A path to a `.tar.gz` file is also
    acceptable, but [cleanup()](#grading_lib.repository.Repository.cleanup) must be called to delete the temporary
    directory. The name of the folder inside the archive file must be "repo".
    :raise ValueError: When the repository does not have a working tree directory.
    """

    def __init__(self, path: str | Path, *args, **kwargs):
        self.repo: Repo
        self.temp_dir: tempfile.TemporaryDirectory | None = None

        if isinstance(path, str):
            path = Path(path)

        if "".join(path.suffixes) == ".tar.gz":
            self.temp_dir = tempfile.TemporaryDirectory(delete=False)
            temp_dir_path = Path(self.temp_dir.name)
            shutil.copy(path, temp_dir_path / path.name)
            subprocess.run(
                ["tar", "-xzf", temp_dir_path / path.name], cwd=temp_dir_path
            )

            # We are not trying to find out what the root folder in the archive file is.
            # We do not create an archive file that does not have the root folder because
            # whens student extract the archive file, files will be everywhere.
            self.repo = Repo(temp_dir_path / "repo", *args, **kwargs)
        else:
            if is_git_dir(path):
                self.repo = Repo(path, *args, **kwargs)
            else:
                self.repo = Repo.init(path)

        if self.repo.working_tree_dir is None:
            raise ValueError(
                "A repository must have a working tree directory (Repo.working_tree_dir must not be None)."
            )

        self.working_tree_dir = Path(self.repo.working_tree_dir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self) -> None:
        """Remove the temporary directory.

        Must be called when the path given to the `__init__` is a gzipped archive file.
        """
        if self.temp_dir is not None:
            self.temp_dir.cleanup()

    def to_gzip_archive(self, path: Path) -> None:
        """
        Create an archive file of the repository.

        This function will not clean up the archive file. However, if this
        repository is part of the temporary directory `self.temp_dir`, the archive
        will get deleted when the temporary directory is deleted.
        """
        subprocess.check_call(
            [
                "tar",
                "-czf",
                path,
                "-C",
                self.working_tree_dir / "..",
                self.working_tree_dir.name,
            ]
        )

    def create_and_add_random_file(
        self, name: str | None = None, content: str | None = None
    ) -> str:
        """
        Create a file with `name` and `content` then add it to the index.

        :param name: If specified, this name will be used instead of the uuid4.
        :param content: If specified, this will be used as content of the file.
        Otherwise, the name will be used.
        """
        if name is None:
            name = str(uuid.uuid4())

        if content is None:
            content = name + "\n"

        with open(self.working_tree_dir / name, "w") as f:
            f.write(content)

        self.repo.index.add(name, write=True)

        return name

    def create_random_commits(self, amount: int, branch: Head | None = None) -> None:
        """Create random commits on current branch.

        :param amount: The amount of commits to be created.
        :param head: If specified, this branch will be checked out before any
        commit is made. Once done, the current branch will be checked out.
        """
        previous_branch = self.repo.active_branch
        if branch is not None:
            branch.checkout()

        for _ in range(amount):
            name = self.create_and_add_random_file()
            self.repo.index.commit(f"Add file {name}")

        if branch is not None:
            previous_branch.checkout()

    def get_all_tag_refs(self) -> IterableList:
        return Tag.list_items(self.repo)

    def get_tag_refs_at(self, commit_hash: str) -> list[Tag]:
        tag_refs = self.get_all_tag_refs()
        matched_tag_refs = []
        for tag_ref in tag_refs:
            if tag_ref.commit.hexsha == commit_hash:
                matched_tag_refs.append(tag_ref)
        return matched_tag_refs


class RepositoryBaseTestCase(BaseTestCase):
    def assertHasTagWithNameAt(self, repo: Repository, name: str, commit_hash: str):
        tag_path = "refs/tags/" + name
        tag_refs = repo.get_tag_refs_at(commit_hash)
        for tag_ref in tag_refs:
            if tag_ref.path == tag_path:
                return

        raise self.failureException(
            f"Expect to see a tag '{name}' at commit '{commit_hash}', but found none."
        )

    def assertHasTagWithNameAndMessageAt(
        self, repo: Repository, name: str, message: str, commit_hash: str
    ):
        tag_path = "refs/tags/" + name
        tag_refs = repo.get_tag_refs_at(commit_hash)
        for tag_ref in tag_refs:
            if (
                tag_ref.tag is not None
                and tag_ref.tag.message is not None
                and tag_ref.path == tag_path
                and tag_ref.tag.message == message
            ):
                return

        raise self.failureException(
            f"Expect to see a tag '{name}' with message '{message}' at commit '{commit_hash}', but found none."
        )
