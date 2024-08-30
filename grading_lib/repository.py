import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

from git import Head, Repo, Tag
from git.repo.fun import is_git_dir

from .common import BaseTestCase, CommandResult, run_executable


def ensure_git_author_identity(
    name="ou-cs3560-grading-script", email="cs3560-grading-script@ohio.edu"
):
    """
    Set user.name and user.email is not set unless they are already set.
    """
    existing_user_name = subprocess.run(
        "git config --get user.name", shell=True, capture_output=True
    )
    existing_user_email = subprocess.run(
        "git config --get user.email", shell=True, capture_output=True
    )

    if existing_user_name is not None or len(existing_user_name.strip()) == 0:
        subprocess.run(["git", "config", "--global", "user.name", name])

    if existing_user_email is not None or len(existing_user_email.strip()) == 0:
        subprocess.run(["git", "config", "--global", "user.email", email])


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

        if path.is_file() and "".join(path.suffixes) == ".tar.gz":
            if sys.version_info < (3, 12, 0):
                self.temp_dir = tempfile.TemporaryDirectory()
            else:
                self.temp_dir = tempfile.TemporaryDirectory(delete=False)
            temp_dir_path = Path(self.temp_dir.name)
            shutil.copy(path, temp_dir_path / path.name)
            subprocess.run(
                ["tar", "-xzf", temp_dir_path / path.name], cwd=temp_dir_path
            )

            # We are not trying to find out what the root folder in the archive file is.
            # We do not create an archive file that does not have the root folder because
            # whens student extract the archive file, files will be everywhere.
            if not (temp_dir_path / "repo").exists():
                raise FileNotFoundError(
                    f"Expect the archive to have folder 'repo', but this 'repo' folder cannot be found after extracting '{path.name}'"
                )
            if not (temp_dir_path / "repo" / ".git").exists():
                raise FileNotFoundError(
                    f"Expect the 'repo' to be a Git repository (it must have .git folder), but '.git' is missing from the 'repo' extracted from '{path.name}'"
                )

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

        # Some git commands when run on GitHub's Actions need a user's indentity.
        with self.repo.config_writer(config_level="repository") as conf_writer:
            conf_writer.set_value("user", "name", "ou-cs3560-grading-script")
            conf_writer.set_value("user", "email", "cs3560-grading-script@ohio.edu")

        self.working_tree_dir = Path(self.repo.working_tree_dir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
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

    def run_executable(self, args: list[str], timeout: float = 15.0) -> CommandResult:
        """
        Run a command using repostiory's working directory as cwd.
        """
        return run_executable(args, cwd=self.repo.working_tree_dir, timeout=timeout)

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

    def get_all_tag_refs(self) -> list[Tag]:
        return Tag.list_items(self.repo)

    def get_tag_refs_at(self, commit_hash: str) -> list[Tag]:
        tag_refs = self.get_all_tag_refs()
        matched_tag_refs = []
        for tag_ref in tag_refs:
            if tag_ref.commit.hexsha == commit_hash:
                matched_tag_refs.append(tag_ref)
        return matched_tag_refs

    def visualize(self) -> str:
        """
        Run 'git log --oneline --all --graph --decorate' and returns the output.
        """
        res = self.repo.git.log("--graph", "--all", "--decorate", "--oneline")
        return res


class RepositoryBaseTestCase(BaseTestCase):
    def assertHasTagWithNameAt(
        self, repo: Repository, name: str, commit_hash: str
    ) -> None:
        tag_path = "refs/tags/" + name
        tag_refs = repo.get_tag_refs_at(commit_hash)
        for tag_ref in tag_refs:
            if tag_ref.path == tag_path:
                return

        tags_text = "\n".join(tag_ref.path for tag_ref in tag_refs)
        raise self.failureException(
            f"Expect to see a tag '{name}' at commit '{commit_hash}', but found none. Tags at commit {commit_hash}:\n{tags_text}"
        )

    def assertHasTagWithNameAndMessageAt(
        self, repo: Repository, name: str, message: str, commit_hash: str
    ) -> None:
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

        tags_texts = []
        for tag_ref in tag_refs:
            if tag_ref.tag is None:
                text = f"{tag_ref.path}"
            else:
                text = f"{tag_ref.path}: {tag_ref.tag.message}"
            tags_texts.append(text)
        tags_text = "\n".join(tags_texts)
        raise self.failureException(
            f"Expect to see a tag '{name}' with message '{message}' at commit '{commit_hash}', but found none. Tags at commit {commit_hash}:\n{tags_text}"
        )
