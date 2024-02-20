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

## Similar Projects / More Mature Projects

If you are looking for a more mature projects, please see

- [OK](https://okpy.org/) which is used in [CS 61A](https://cs61a.org/) at University of California, Berkeley. It implements the concept of
  "test case unlocking" that promotes "multi-stage problem solving process." [paper](http://denero.org/content/pubs/las15_basu_unlocking.pdf).
- [check50](https://cs50.readthedocs.io/projects/check50/en/latest/) which is used in [CS 50](https://cs50.harvard.edu/x/2024/) at Harvard University. There are also [various other command line tools](https://cs50.readthedocs.io/).
- Cafe Grader's [judge-script](https://github.com/cafe-grader-team/cafe-grader-judge-scripts) and its [web UI](https://github.com/cafe-grader-team/cafe-grader-web) which is (was?; well at least in 2010-ish) used by Department of Computer Engineering at Kasetsart University, Thailand.

This library is somewhat inspired by Cafe Grader Suite and OK.
