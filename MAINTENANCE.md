# Maintaining

## Note

### Why are we supporting Python 3.10 to 3.13?

Our lab machines still using Python 3.10.x. GitHub Codespace should still be using Python 3.12.x.
Student who want to run the grading script locally may download 3.13 from python.org website.

## First Time Setup

Install the pinned dependencies.

```console
python -m pip install -r dev-requirements.txt
```

## Building the Package

Install the build-time dependencies.

```console
python -m pip install --upgrade build twine
```

To build, run

```console
python -m build
```

## Installing the Editable Version

To locally install, run

```console
python -m pip install -e ".[dev,doc]" --config-settings editable_mode=compat
```

## Running the Tests

Please make sure that the package is installed with `.[dev]`, then run

```console
pytest tests/
```

Run the test for various python's versions, run

```console
tox
```

With test coverage

```console
pytest --cov=grading_lib tests/
```

If you want to view the HTML report instead, run 

```console
coverage html
```

then open the HTML file in your browser.

## Building the Documentation

```console
tox -edocs
```

## Deployment Flow

- Check that unit testing on Windows and MacOs do not fail.

- Run tox.
- Update `grading_lib/VERSION` file.
- Update `CHANGELOG.md` file.
- Make a commit.
- Tag the commit.
- Push to GitHub.
- Approve the deployment flow on GitHub Actions.

### Manually publish to PyPI

There should be no need of running these commands manually now that
the workflow is setup to auto publish to both PyPI and GitHub's Releases.

However, if the workflow is breaking, for example, you can run these
commands to manually publish.

#### Publish to the Real PyPI

Make sure you build the package.

```console
python -m twine upload dist/*
```

#### Publish to the Test PyPI

If you want to test something out.

```console
python -m twine upload -r testpypi dist/*
```

## Pinning the Dependencies

After new depenency is added, please pin the dependencies by running

```console
python -m piptools compile -o requirements.txt pyproject.toml
python -m piptools compile --extra=dev --output-file=dev-requirements.txt pyproject.toml
```

Please install [`pip-tools`](https://pypi.org/project/pip-tools/) if it is not installed.

## Update the Pinned Dependencies

```console
python -m piptools compile --upgrade
```
