import pytest

from grading_lib.makefile import Makefile


@pytest.fixture
def makefile_1() -> str:
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
def makefile_2() -> str:
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
def makefile_3() -> str:
    """Continuous Makefile."""
    return """
a: e f
b: g
c: h
	@echo hi
d: i j
"""


@pytest.fixture
def makefile_var_defs() -> str:
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


def test_makefile_from_text(makefile_1: str) -> None:
    """
    A verification test for `:` showing up twice.
    """

    try:
        _ = Makefile.from_text(makefile_1)
    except Exception:
        pytest.fail("Exception raises while parsing a makefile.")


def test_makefile_from_text_2(makefile_2) -> None:
    try:
        mk = Makefile.from_text(makefile_2)
    except Exception:
        pytest.fail("Exception raises while parsing a makefile.")

    assert mk.rules[0].is_empty()
    assert not mk.rules[1].is_empty()


def test_makefile_from_text_3(makefile_3) -> None:
    try:
        mk = Makefile.from_text(makefile_3)
    except Exception:
        pytest.fail("Exception raises while parsing a makefile.")

    assert mk.has_rule("a")
    rule = mk.get_rule("a")
    assert rule is not None
    if rule:
        assert rule.prerequisites == ["e", "f"]

    assert mk.has_rule("b")
    rule = mk.get_rule("b")
    assert rule is not None
    if rule:
        assert rule.prerequisites == ["g"]

    assert mk.has_rule("c")
    rule = mk.get_rule("c")
    assert rule is not None
    if rule:
        assert rule.prerequisites == ["h"]
        assert not rule.is_empty()

    assert mk.has_rule("d")
    rule = mk.get_rule("d")
    assert rule is not None
    if rule:
        assert rule.prerequisites == ["i", "j"]


def test_makefile_var_defs_parsing(makefile_var_defs) -> None:
    try:
        _ = Makefile.from_text(makefile_var_defs)
    except Exception:
        pytest.fail("Exception raises while parsing a makefile.")
