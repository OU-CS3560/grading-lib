"""Set of utilities for quality assurance of the grading script."""

from importlib import import_module


def import_as_non_testcase(module_name, name, package=None):
    """Import the name from a module and prevent pytest from running it as testcase."""
    mod = import_module(module_name, package=package)
    cls = mod.__dict__[name]
    cls.__test__ = False
    return cls


class SetupThenTearDown:
    """Automatically call setUp and tearDown.

    Intended to be used in the QA script.
    """

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        if hasattr(self.obj, "setUp"):
            self.obj.setUp()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.obj, "tearDown"):
            self.obj.tearDown()
