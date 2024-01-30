"""
Makefile related routines.
"""
from pathlib import Path
from typing import Optional, Tuple

from .common import run_executable, CommandResult


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
    def from_path(cls, path: Path | str):
        with open(path, "r") as f:
            var_defs: list[VariableDefinition] = []
            rules: list[Rule] = []

            lines = f.readlines()
            current_rule: Optional[Rule] = None
            for line in lines:
                line = line.strip()

                if DEBUG:
                    print(f"parsing '{line}'")

                if len(line) != 0:
                    if line[0] == "#":
                        continue

                    if line[0] != "\t" and ":" in line:
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
                    elif line[0] != "\t" and "=" in line:
                        if DEBUG:
                            print("line is a variable definition")
                        # Only act on the first '='.
                        equal_pos = line.find("=")
                        name = line[:equal_pos]
                        value = line[equal_pos + 1 :]

                        var_defs.append(
                            VariableDefinition(name=name.strip(), value=value.strip())
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
            return cls(path, var_defs, rules)

    def get_rule(self, targets: str | list[str]) -> Optional[Rule]:
        for rule in self.rules:
            if rule.targets == targets:
                return rule

        return None

    def has_rule(self, targets: str | list[str]) -> bool:
        rule = self.get_rule(targets)
        return rule is not None
