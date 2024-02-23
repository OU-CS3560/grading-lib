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

- {py:obj}`grading_lib.makefile.run_targets` that runs a target (or targets)
  in a `Makefile` and return the {py:obj}`grading_lib.common.CommandResult`.
- A class {py:obj}`grading_lib.makefile.Makefile` that offer high-level parsing
  for a `Makefile`.

## Git Problems

Similarly, grading lib has these utilies that will help you write 
a problem for Git.

## Tools

