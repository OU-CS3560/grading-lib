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
GIT_BRANCH_DEL_CMD=git push origin :branch
TWO ::=value
EXPAND_NOW :::= value
"""


@pytest.fixture
def makefile_2():
    return """
# https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html

.PHONY: Date 

weekend := $(shell date  | grep -E '^(Sat|Sun)' | wc -l | tr -d ' ')

ifeq ($(weekend),0)
	output := Weekday
else
	output := Weekend
endif

Date:
	date
	@echo "weekend = " $(weekend)
	@echo "output  = " $(output)
"""


@pytest.fixture
def makefile_var_defs():
    """
    Various variable definitions.
    """
    return """
# Assignments.
RECURSE_EXPAND = $(ANOTHER_VAR)
SIMPLY_EXPAND:= val
SIMPLY_EXPAND_2 ::= val2
IMMEDIATELY_EXPAND :::= val3
DEFAULT_VALE ?= default-value
SHELL_RESULT != printf 'hi'

# Appending.
TEXT_VAR = hello
TEXT_VAR += world

# Directive
override TEXT_VAR = new-val
"""


def test_makefile_from_text(makefile_1):
    """
    A verification test for `:` showing up twice.
    """

    try:
        mk = Makefile.from_text(makefile_1)
    except Exception:
        assert False, "Exception raises while parsing a makefile."


def test_makefile_from_text_2(makefile_2):
    try:
        mk = Makefile.from_text(makefile_2)
    except Exception:
        assert False, "Exception raises while parsing a makefile."

    assert mk.rules[0].is_empty()
    assert not mk.rules[1].is_empty()


def test_makefile_var_defs_parsing(makefile_var_defs):
    try:
        mk = Makefile.from_text(makefile_var_defs)
    except Exception:
        assert False, "Exception raises while parsing a makefile."
