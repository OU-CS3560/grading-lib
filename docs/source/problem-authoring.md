# Problem Authoring

This section outlines how to structure a problem.

## Problem Folder Structure

The following structure is the problem when it is deployed in an assignment.

```plain
problem-name/                    - Root of the problem folder.
problem-name/README.md           - Contain instructions for the problem.
problem-name/scripts/grade.py    - Contains the grading script to be run by `grading.yml` workflow.
problem-name/scripts/generate.py - Contains the script o be run during the generation phase.
problem-name/problem.toml        - A metadata file of the problem. See its own section for detail.
```

When the problem is in the catalog, it will be in this structure.

```plain
problem-name/                    - Root of the problem folder in the catalog.
problem-name/README.md           - Contain instructions for the problem.
problem-name/problem-name/       - A folder contains content in the previous structure.
problem-name/tests/              - A folder of test cases for the grading script of the problem itself.
```
