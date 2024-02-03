import pytest

from cs3560_grading_lib.makefile import (
    Makefile,
    VariableDefinition,
)


@pytest.fixture
def makefile_1():
    """
    First line is empty and two equal signs on a var-def line.
    """
    return """
CXXFLAGS = -std=c++17
LDFLAGS :=
GIT_BRANCH_DEL_CMD=git push origin :branch
TWO ::=value
EXPAND_NOW :::= value
"""


def test_makefile_from_text(makefile_1):
    """
    A verification test.
    """

    try:
        mk = Makefile.from_text(makefile_1)
    except Exception:
        assert False, "Exception raises while parsing a makefile."

    assert isinstance(mk.variable_definitions[0], VariableDefinition)
    assert mk.variable_definitions[0].name == "CXXFLAGS"
    assert mk.variable_definitions[1].name == "LDFLAGS"
    assert mk.variable_definitions[2].name == "GIT_BRANCH_DEL_CMD"
    assert mk.variable_definitions[3].name == "TWO"
    assert mk.variable_definitions[4].name == "EXPAND_NOW"
