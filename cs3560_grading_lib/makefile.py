"""
Makefile related routines.

The parser is high-level by design since
the homework requirement do not need the full
Makefile to be parsed. So far we only need
the target names of a rule. If this parser is
too much to mataintain we can offload checking-
if-a-target-exist to GNU Make itself as well.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .common import BaseTestCase, CommandResult, is_debug_mode, run_executable

RULE_PATTERN = re.compile(
    r"(?P<targets>[\w\.\-%$()\ +]+):(?!=|:=|::=)(?P<prereqs>[\w\.\-%$()\ +]*)"
)

# FIXME: This need to take directives into account e.g. override, undefine, etc.
# Thus, parsing variable definition is dropped in v0.0.3
VAR_DEF_PATTERN = re.compile(r"(?P<name>[\w\.-]+)\s*(:*|\?|!|\+)?=\s*(?P<value>.*)")


def run_targets(targets: list[str], cwd: Optional[str | Path] = None) -> CommandResult:
    """
    Invoke the target(s) in the Makefile.

    Return True if the call is successful, False otherwise.
    Also return the output of the executation.
    """
    return run_executable(["make"] + targets, cwd=cwd)


class Rule:
    def __init__(
        self, targets: str | list[str], prerequisites: list[str], recipe: list[str]
    ):
        self.targets = targets
        self.prerequisites = prerequisites
        self.recipe = recipe

    @property
    def prereqs(self) -> list[str]:
        """Alias for `prerequisites`."""
        return self.prerequisites

    def __str__(self) -> str:
        targets = self.targets
        if isinstance(self.targets, list):
            targets = " ".join(self.targets)
        return f"{targets}"

    def __repr__(self) -> str:
        return str(self)

    def is_empty(self) -> bool:
        return len(self.recipe) == 0


class VariableDefinition:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class Makefile:
    """
    A high-level representation of a Makefile.

    Alternative includes a tree-sitter's one (https://github.com/alemuller/tree-sitter-make)
    via its python binding at https://github.com/tree-sitter/py-tree-sitter.

    A Python one https://github.com/linuxlizard/pymake.
    """

    def __init__(
        self,
        path: Path | str,
        rules: list[Rule],
    ):
        self.path = path
        self.rules = rules

    @classmethod
    def from_path(cls, path: Path | str) -> Makefile:
        with open(path, "r") as f:
            content = f.read()
            return cls.from_text(content)

    @classmethod
    def from_text(cls, text: str):
        DEBUG: bool = is_debug_mode()

        rules: list[Rule] = []

        lines = [l.replace("\r", "") for l in text.split("\n")]
        current_rule: Optional[Rule] = None
        for line in lines:
            line = line.strip()

            if DEBUG:
                print(f"parsing '{line}'")

            if len(line.strip()) != 0:
                if line[0] == "#":
                    if DEBUG:
                        print("  line is a comment")
                    continue
                if (res := re.match(RULE_PATTERN, line)) is not None:
                    target_token = res.group("targets")
                    prereq_token = res.group("prereqs")

                    if " " in target_token:
                        targets = target_token.split(" ")
                    else:
                        targets = target_token

                    prereqs = [
                        t.strip()
                        for t in prereq_token.split(" ")
                        if len(t.strip()) != 0
                    ]
                    current_rule = Rule(
                        targets=targets, prerequisites=prereqs, recipe=list()
                    )
                elif current_rule is not None:
                    # Everything else will be marked as part of the rule
                    # if we are in one.
                    if DEBUG:
                        print("  line is part of the rule")

                    current_rule.recipe.append(line)
                else:
                    if DEBUG:
                        print("  no current rule, ignore this line")
                    pass
            else:
                if current_rule is not None:
                    # Closing the rule when an empty line is found.
                    rules.append(current_rule)
                    current_rule = None

        if current_rule is not None:
            rules.append(current_rule)
        return cls("memory://Makefile", rules)

    def get_rule(self, targets: str | list[str]) -> Optional[Rule]:
        for rule in self.rules:
            if rule.targets == targets:
                return rule

        return None

    def has_rule(self, targets: str | list[str]) -> bool:
        rule = self.get_rule(targets)
        return rule is not None


class MakefileBaseTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not hasattr(cls, "makefile_name"):
            raise AttributeError("'makefile_name' is required")

        if isinstance(cls.makefile_name, str):
            cls.makefile_name = Path(cls.makefile_name)

        if not cls.makefile_name.exists():
            assert False, f"Expect a file '{cls.makefile_name}', but it does not exist."

        cls.makefile = Makefile.from_path(cls.makefile_name)

    def assertHasRuleForTarget(
        self,
        target_name: str,
        msg_template: str = "Rule for a target '{target_name}' does not exist. Its behavior cannot be verified.",
    ):
        """
        The Makefile must have target `target_name`.
        """
        if not self.makefile.has_rule(target_name):
            msg = msg_template.format(target_name=target_name)
            raise self.failureException(msg)

    def assertRuleRecipeIsEmpty(
        self,
        target_name: str,
        msg_template: str = "Recipe of the rule for a target '{target_name}' is not empty.",
    ):
        rule = self.makefile.get_rule(target_name)
        if rule is None:
            msg = "Rule for a target '{target_name}' does not exist. Its behavior cannot be verified.".format(
                target_name=target_name
            )
            raise self.failureException(msg)
        if not rule.is_empty():
            msg = msg_template.format(target_name=target_name)
            raise self.failureException(msg)
