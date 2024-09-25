"""Set of utilities for quality assurance of the grading script."""

import typing as ty
from importlib import import_module
from types import TracebackType

from typing_extensions import Self


def import_as_non_testcase(
    module_name: str, name: str, package: str | None = None
) -> ty.Any:
    """Import the name from a module and prevent pytest from running it as a testcase."""
    mod = import_module(module_name, package=package)
    cls = mod.__dict__[name]
    cls.__test__ = False
    return cls


class SetupThenTearDown:
    """Automatically call setUp and tearDown.

    Intended to be used in the QA script.
    """

    def __init__(self, obj: ty.Any) -> None:
        self.obj = obj

    def __enter__(self) -> Self:
        if hasattr(self.obj, "setUp"):
            self.obj.setUp()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if hasattr(self.obj, "tearDown"):
            self.obj.tearDown()
