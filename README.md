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

The `cs3560_grading_lib.BaseTestCase` that provide `assertFileExists` and `assertCommandSuccessful`.
The later takes the result from `cs3560_grading_lib.run_executable` or `cs3560_grading_lib.run_targets`.
