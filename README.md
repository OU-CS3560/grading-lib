# cs3560-grading-lib

A common library for the grading scripts.

## Install

```console
$ python -m pip install cs3560-grading-lib
```

## Features

Collecting the tests of problems into `.github/classroom/autograding.json`.

```console
python -m cs3560_grading_lib.tools.collect_autograding_tests
```

The `cs3560_grading_lib.BaseTestCase` that provides `assertFileExists` and `assertCommandSuccessful`.
The later takes the result from `cs3560_grading_lib.run_executable` or `cs3560_grading_lib.run_targets`.

## Problem Folder Structure

```plain
problem-name/                    - Root of the problem folder.
problem-name/README.md           - Contain instructions for the problem.
problem-name/scripts/grade.py    - Contains the grading script to be run by `grading.yml` workflow.
problem-name/scripts/generate.py - Contains the script o be run during generation phase.
problem-name/problem.toml        - A metadata file of the problem. See its own section for detail.
```

## problem.toml Reference

A metadata file about the problem.

### `[problem]` section

`name` specifies the name of the problem. It must match the folder name of the problem.
This name will be use in the prefix for the `[problem.tests.<id>.run]`'s value to change
the current working directory to the problem's folder.

`difficulty` is an integer specifies the difficulty level of the problem. Currently these
values are defined.

- `1` - basic/easy problem.
- `2` - intermediate problem.
- `3` - advance/hard problem.

`objective` is a string that describe the objective of this problem. It is here mainly to
help instructor/TA decide on which problem to use in the assignment.

### `[problem.tests.<id>]` section

The keys in this section are the same keys found in `.github/classroom/autograding.json`
for `education/autograding` action.

We store them here instead so that we can add or remove problem as we please. The `cs3560_grading_lib.tools.collect_autograding_tests` that is run as part of the step of the `grading.yml` workflow will automatically collect these tests and create
`.github/classroom/autograding.json` for you. It will also modify the `[problem.tests.<id>.run]` command so that it is prefixed with change directory command (`cd`)

### `[problem.grading-script-tests.<id>]` section

These sections specify the test cases for the grading script itself. These does not contribute
to the student points. They exist so that we can ensure that the grading script behave correctly.

`is-encrypted` is a flag use to indicate if the `content` is encrypted or not.

`expected-result` is used to tell if the grading script behave correctly or not.

`path` is a path to the file that its content will be overriden with value in the `content` key.

`content` can be a plain text or encrypted text. When in plain text, it can be used to override
the content of file at `path`. Then the grading script can be run against this new content to verify if the script behave as designed or not.
