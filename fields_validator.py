"""A module to validate fields of a class."""

from collections.abc import Callable
from functools import wraps
from typing import Any


def validate(eval_fields: dict) -> Callable:
    """Validate against eval_fields.

    Args:
        eval_fields (dict): A dic of field names and their expected
        types which are valid for that class.

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

    # alternativ
    # @classmethod
    # def _is_valid(cls, sets: list[tuple[Any, (tuple | type)]]) -> bool:
    #     for val, data_type in sets:
    #         if not isinstance(val, (data_type,)):
    #             err_msg = f"{val} is not of type {data_type}"
    #             raise TypeError(err_msg)
    #     return True

    # in set_prod:
    # Product._is_valid([
    #     (name, str),
    #     (price, (float, int)),
    #     (quantity, int),
    # ])
