<!-- This file is included in the documentation so the header is removed. -->

## Unreleased

- Switch to manual API listing.

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
