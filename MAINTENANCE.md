# Maintaining

## Note

For the detail about version specifier, please see [version specifier](https://packaging.python.org/en/latest/specifications/version-specifiers/)

## First time setup

TBD

## Building the package

Install the build-time dependencies.

```console
python -m pip install --upgrade build twine
```

To build, run

```console
python -m build
```

## Installing the editable version

To locally install, run

```console
python -m pip install -e ".[dev,doc]" --config-settings editable_mode=compat
```

## Running the tests

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

## Building the docs

```console
cd docs
make html
```

## Deployment flow

- Run tox.
- Update `grading_lib/VERSION` file.
- Update `CHANGELOG.md` file.
- Make a commit
- Tag the commit
- Push
- Approve the deployment flow on GitHub Actions.

### Manually publish to PyPI

There should be no need of running these commands manually now that
the workflow is setup to auto publish to both PyPI and GitHub's Releases.

Howver, if the workflow is breaking, for example, you can run these
commands to manually publish.

#### Publish to the real PyPI

Make sure you build the package.

```console
python -m twine upload dist/*
```

#### Publish to the test PyPI

If you want to test something out.

```console
python -m twine upload -r testpypi dist/*
```