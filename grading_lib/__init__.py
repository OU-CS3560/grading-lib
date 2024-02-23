import os

with open(os.path.join(os.path.dirname(__file__), "VERSION")) as version_file:
    version = version_file.read().strip()

__version__ = version
__all__ = [
    "COMMAND_FAILED_TEXT_TEMPLATE",
    "BaseTestCase",
    "CommandResult",
    "MinimalistTestResult",
    "get_seed_from_env",
    "is_debug_mode",
    "run_executable",
    "Makefile",
    "run_targets",
]

from .common import (
    COMMAND_FAILED_TEXT_TEMPLATE,
    BaseTestCase,
    CommandResult,
    MinimalistTestResult,
    get_seed_from_env,
    is_debug_mode,
    run_executable,
)
from .makefile import Makefile, run_targets
