# Changelog

## Unreleased

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
