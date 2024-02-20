# problem.toml Specification

The grading library uses `problem.toml` file to store problem's metadata.

## `[problem]` section

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

## `[problem.tests.<id>]` section

The keys in this section are the same keys found in `.github/classroom/autograding.json`
for `education/autograding` action.

We store them here instead so that we can add or remove problem as we please. The `cs3560_grading_lib.tools.collect_autograding_tests` that is run as part of the step of the `grading.yml` workflow will automatically collect these tests and create
`.github/classroom/autograding.json` for you. It will also modify the `[problem.tests.<id>.run]` command so that it is prefixed with change directory command (`cd`)

## `[problem.grading-script-tests.<id>]` section

These sections specify the test cases for the grading script itself. These does not contribute
to the student points. They exist so that we can ensure that the grading script behave correctly.

`is-encrypted` is a flag use to indicate if the `content` is encrypted or not.

`expected-result` is used to tell if the grading script behave correctly or not.

`path` is a path to the file that its content will be overriden with value in the `content` key.

`content` can be a plain text or encrypted text. When in plain text, it can be used to override
the content of file at `path`. Then the grading script can be run against this new content to verify if the script behave as designed or not.
