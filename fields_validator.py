"""A module to validate fields of a class."""

from collections.abc import Callable
from functools import wraps
from typing import Any


def validate(eval_fields: dict) -> Callable:
    """Validate against eval_fields.

    Args:
        eval_fields (dict): A dic of field names and their expected
        types which are valid for that class.

    Note:
    isinstance(value, expected_type) fails for parameterized generics,
    e.g. 'list[int]'. Won't fix, too much for this project.

    """

    def deco(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: Callable, name: str, value: Any) -> TypeError | None:  # noqa: ANN401
            """Validate."""
            expected_type = eval_fields.get(name)
            if expected_type and not isinstance(value, expected_type):
                err_msg = f"{name} is not of type {expected_type}"
                raise TypeError(err_msg)
            func(self, name, value)

        return wrapper

    return deco
