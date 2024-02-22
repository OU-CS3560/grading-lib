# Changelog

## Unreleased / Changes on the main branch

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
