# Getting Started

The grading lib provides common components for a grading scripts. For example,
you can create a simple grading script by

```python
# file: scripts/grade.py
import unittest

from cs3560_grading_lib.common import BaseTestCase, MinimalistTestResult

class TestExampleProblem:
    def test_example_problem(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=MinimalistTestResult)
    unittest.main(testRunner=runner)    
```