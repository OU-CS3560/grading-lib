<!-- This file is included in the documentation so the header is removed. -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://packaging.python.org/en/latest/discussions/versioning/).

Note that the log for version before v0.1.1 may not be in the mentioned format.

## [Unreleased]

## v0.1.2a4 - 2024-10-01

### Changed

- Force `sys.stdout` for `MinimalistTestRunner.stream` to prevent stdout and stderr weaving output on GitHub Actions.

## v0.1.2a3 - 2024-10-01

### Changed

- Add non-zero exit code when the points is less than the total points.

## v0.1.2a2 - 2024-10-01

### Changed

- Flush stdout in the grade command.

## v0.1.2a1 - 2024-10-01

### Added

- Add `grade` command that runs all test in the homework.
- Add `util.FindProblemList` that parse a README.md file for `:problem-list:` token and the list of problem names.

### Changed

- Fix some mypy error messages for function's return type and argument type.

## v0.1.1 - 2024-09-25

Please see changelog from v0.1.1a1 to v0.1.1rc3.

## v0.1.1rc3 - 2024-09-25

### Added

- Add `common.points` for decorating the test method for points.
- Add `common.file_has_correct_sha512_checksum` for checking file checksum.
- Add `common.MinimalistTestRunner` that show collected points at the end.
- Add `repository.RepositoryBaseTestCase.assertHasOnlyGitCommand` that check if file contain only Git command and nothing else.

### Changed

- `common.MinimalistTestResult` now track points if they are presence.
- Some test cases now use the builtin `tmp_path` instead of our own version of it.

## v0.1.1rc2

- Fix gunzip is not available on Windows.
- Fix mypy errors.

## v0.1.1rc1

- Add `qa.SetupThenTearDown`
- Add `qa.import_as_non_testcase`

## v0.1.1a3

- Fix warnings by mypy.
- Add a default user's identity to the `Repository`. Git on GitHub's Actions will complain
  when a command like `git commit` is run without user's identity.
- Fix bug in the `MakefileBaseTestCase.setUpClass` where the conversion from `if` to `assert` was incorrect.
- Handle a command's timeout in `common.run_executable`.
- Add `repository.ensure_git_author_identity`.

## v0.1.1a2

- Add `ensure_lf_line_ending`.
- Account for the different of `tempfile.TemporaryDirectory` between 3.12 and 3.10.
- Add `BaseTestCase.assertArchiveFileIsGzip`
- Add sanity checks to `Repository` when working with `.tar.gz` file.
- Add `Repository.run_executable` where `cwd` is always set to working directory of the repository.
- Remove extra dependencies `doc` since we cannot list Git repository as a dependency and upload to PyPI.

## v0.1.1a1

- (docs) Switch to manual API listing.
- (docs) Pin `sphinx-autodoc2` to our own fork before its [#17](https://github.com/sphinx-extensions2/sphinx-autodoc2/issues/17) is fixed.
- Add timeout to `run_executable` since some commands may require human's input and get stuck.
- Add `grading_lib.repository.RepositoryBaseTestCase`.
- Add `Repository.get_all_tag_refs`.
- Add `Repository.get_tag_refs_at`.
- Fix `Repository` from an archive file is using the archive's filename instead of the "repo".

## v0.1.0

See changelog from v0.1.0a1 to v0.1.0rc2.

## v0.1.0rc2

- Fix `BaseTestCase.assertCommandOutputEqual` not checking if the outputs are equal.
- Fix `BaseTestCase.assertAllFilesExist` raise exception if file does not exist too early.

## v0.1.0rc1

- Add `BaseTestCase.with_temporary_dir`. A metaclass `BaseTestCaseMeta`
  is added to support it.
- Add `BaseTestCase.assertCommandOutputEqual`.
- BREAKING CHANGE: `run_targets` now take Makefile's name. The default name is `answer.mk`
- BREAKING CHANGE: Rename `MakefileBaseTestCase.makefie_name` to `MakefileBaseTestCase.makefile_path`.
- Add `MakefileBaseTestCase.copy_makefile`.

## v0.1.0a4

- Fix `internal collect-autograding-tests` command by allow
  problem to have no test case.

## v0.1.0a3

- Fix errors/warnings from mypy.
- Add `py.typed` file.
- Add `BaseTestCase.assertAllFilesExist`
- Add `cli` module.
- Add `dev mypy` CLI command.
- Add `internal collect-autograding-tests` CLI command.
- Add `summary` CLI command.
- Deprecate `grading_lib.tools.collect_autograding_tests` module.

## v0.1.0a2

- Use `tomli` instead of the builtin `tomllib`.

## v0.1.0a1

- Remove the requirement for Python 3.12. Change `datetime.UTC` to `datetime.timezone.utc` (requires Python >= 3.11).
  Avoid using `delete_on_close` parameter of `tempfile.NamedTemporaryFile` (requires Python >= 3.12).
- Rename package from `cs356_grading_lib` to `grading_lib`.
- Switch to a centralized version number scheme.

## v0.0.4

- Fix parsing problem with Makefile where there is no empty line
  between the rules.

## v0.0.3

- Add `cs3560_grading_lib.common.populate_folder_with_filenames`.
- Include all changes from `v0.0.3a1` to `v0.0.3a4`.

## v0.0.3a4

- Add `cs3560_grading_lib.makefile.MakefileBaseTestCase`.

## v0.0.3a3

- Add `cs3560_grading_lib.common.get_mtime_as_datetime`.
- Add `cs3560_grading_lib.common.has_file_changed`.
- (BREAKING CHANGE) Remove variable definition parsing of a Makefile.

## v0.0.3a2

- Fix debug mode left on.
- Fix test case using the same seed.

## v0.0.3a1

- Add `Makefile` representation and parser.
- Fix the variable definition bug where two `:` will crash the parser.
- Allow target dir for `cs3560_grading_lib.tools.collect_autograding_tests` to be non-existence.

## v0.0.2

## v0.0.1

- Initial release.
- Consoliate common piece of code from problems in make homework.
