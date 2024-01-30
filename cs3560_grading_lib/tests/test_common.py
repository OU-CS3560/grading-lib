import os

from cs3560_grading_lib import is_debug_mode


def test_is_debug_mode():
    vals_for_true = ["1", "True", "T", "On", "ON", "t", "true"]
    for val in vals_for_true:
        os.environ["DEBUG"] = val
        assert is_debug_mode()

    vals_for_false = ["", None, "False", "false", "lorem", "0"]
    for val in vals_for_false:
        if val is None:
            del os.environ["DEBUG"]
        else:
            os.environ["DEBUG"] = val
        assert is_debug_mode() is False
