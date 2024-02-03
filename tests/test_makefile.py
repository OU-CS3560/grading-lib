import pytest

from cs3560_grading_lib.makefile import Makefile, VariableDefinition


@pytest.fixture
def makefile_1():
    """
    First line is empty and two equal signs on a var-def line.
    """
    return """
CXXFLAGS = -std=c++17
LDFLAGS :=
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
