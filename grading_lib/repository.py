import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from git import Head, Repo
from git.repo.fun import is_git_dir


class Repository:
    """
    A wrapper over git.Repo with our own utilities.

    :param path: A path to repository folder. A path to a `.tar.gz` file is also
    acceptable, but [cleanup()](#grading_lib.repository.Repository.cleanup) must be called to delete the temporary
    directory.
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
            subprocess.run(["tar", "-xzf", temp_dir_path / path.name])

            # .stem is name.tar; .stem[:-4] is then the name.
            self.repo = Repo(temp_dir_path / path.stem[:-4], *args, **kwargs)
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
