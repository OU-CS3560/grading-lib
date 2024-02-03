"""
Makefile related routines.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional
import re


from .common import run_executable, CommandResult, is_debug_mode

VAR_DEF_PATTERN = re.compile(r"(?P<name>[\w\.-]+)\s*:*=\s*(?P<value>.*)")
# This pattern will fail if it is checked before the VAR_DEF_PATTERN. e.g. := :::=
RULE_PATTERN = re.compile(r"(?P<name>[\w\.\-%$()\ +]+):(?P<prereq>[\w\.\-%$()\ +]*)")


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
        variable_definitions: list[VariableDefinition],
        rules: list[Rule],
    ):
        self.path = path
        self.variable_definitions = variable_definitions
        self.rules = rules

    @classmethod
    def from_path(cls, path: Path | str) -> Makefile:
        with open(path, "r") as f:
            content = f.read()
            return cls.from_text(content)

    @classmethod
    def from_text(cls, text: str):
        DEBUG: bool = is_debug_mode()

        var_defs: list[VariableDefinition] = []
        rules: list[Rule] = []

        lines = [l.replace("\r", "") for l in text.split("\n")]
        current_rule: Optional[Rule] = None
        for line in lines:
            line = line.strip()

            if DEBUG:
                print(f"parsing '{line}'")

            if len(line.strip()) != 0:
                if line[0] == "#":
                    continue
                if (res := re.match(VAR_DEF_PATTERN, line)) is not None:
                    if DEBUG:
                        print("line is a variable definition")

                    name = res.group("name")
                    value = res.group("value")

                    var_defs.append(
                        VariableDefinition(name=name.strip(), value=value.strip())
                    )
                elif line[0] != "\t" and ":" in line:
                    if DEBUG:
                        print("line is the begining of a rule")
                    if current_rule is not None:
                        rules.append(current_rule)

                    target_token, prerequisite_token = line.split(":")
                    if " " in target_token:
                        targets = target_token.split(" ")
                    else:
                        targets = target_token

                    prereqs = [
                        t.strip()
                        for t in prerequisite_token.split(" ")
                        if len(t.strip()) != 0
                    ]
                    current_rule = Rule(
                        targets=targets, prerequisites=prereqs, recipe=list()
                    )
                else:
                    if DEBUG:
                        print("line is part of the recipe")
                    current_rule.recipe.append(line[1:])
            else:
                if current_rule is not None:
                    rules.append(current_rule)
                    current_rule = None

        if current_rule is not None:
            rules.append(current_rule)
        return cls("memory://Makefile", var_defs, rules)

    def get_rule(self, targets: str | list[str]) -> Optional[Rule]:
        for rule in self.rules:
            if rule.targets == targets:
                return rule

        return None

    def has_rule(self, targets: str | list[str]) -> bool:
        rule = self.get_rule(targets)
        return rule is not None
