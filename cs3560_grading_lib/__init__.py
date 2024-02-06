__version__ = "0.0.3"
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
