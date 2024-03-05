# Getting Started

The grading lib provides common components for a grading scripts. For example,
you can create a simple grading script by

```python
# file: scripts/grade.py
import unittest

from grading_lib.common import BaseTestCase, MinimalistTestResult

class TestExampleProblem:
    def test_example_problem(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=MinimalistTestResult)
    unittest.main(testRunner=runner)    
```

## Build System Problems

The grading lib offers powerful utilities for authoring a grading script
for a build system related problem. Here are some notable example of such
utilities.

- {py:obj}`makefile.run_targets <grading_lib.makefile.run_targets>` that runs a target (or targets)
  in a `Makefile` and return the {py:obj}`CommandResult <grading_lib.common.CommandResult>`.
- A class {py:obj}`makefile.Makefile <grading_lib.makefile.Makefile>` that offer high-level parsing
  for a `Makefile`.

## Git Problems

Similarly, grading lib has these utilies that will help you write 
a problem for Git.

## Useful CLI Commands

grading-lib provides command-line interface (CLI) with some useful commands.

- A `summary` command that shows the number of problems, total points and points per problem.
- A `dev mypy` command that runs Mypy aginst the grading scripts in the `scripts/` folder.
