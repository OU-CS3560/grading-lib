# Maintaining

## Build

Build time dependencies

```console
python -m pip install --upgrade build twine
```

To build

```console
python -m build
```

To locally install

```console
python -m pip install -e ".[dev]"
```

## Testing

To run the test cases,

```console
$ pytest
```

## Publishing

For the detail about version specifier, please see [version specifier](https://packaging.python.org/en/latest/specifications/version-specifiers/)

### Publish to the test PyPI

```console
python -m twine upload -r testpypi dist/*
```

### Publish to the real PyPI

```console
python -m twine upload dist/*
```
