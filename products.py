# ruff: noqa: D100, D107, D101, D102,ERA001
from typing import Any


class Product:
    ERR_INIT = "Wrong init params."
    ERR_BUY = "BUY err"
    _FIELD_TYPES = {"name": str, "price": float | int, "quantity": int}

    def __setattr__(self, name: str, value: Any) -> None:
        """Validate."""
        expected_type = self._FIELD_TYPES.get(name)
        if expected_type and not isinstance(value, expected_type):
            err_msg = f"{name} is not of type {expected_type}"
            raise TypeError(err_msg)
        super().__setattr__(name, value)

    # @classmethod
    # def _is_valid(cls, sets: list[tuple[Any, (tuple | type)]]) -> bool:
    #     for val, data_type in sets:
    #         if not isinstance(val, (data_type,)):
    #             err_msg = f"{val} is not of type {data_type}"
    #             raise TypeError(err_msg)
    #     return True

    def __init__(self, name: str, price: float, quantity: int) -> None:
        # Product._is_valid([
        #     (name, str),
        #     (price, (float, int)),
        #     (quantity, int),
        # ])

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = min(0, self.quantity + quantity)
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> bool:
        self.active = True
        return self.active

    def deactivate(self) -> bool:
        self.active = False
        return self.active

    def show(self) -> None:
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float:
        if quantity > self.quantity:
            raise ValueError(Product.ERR_BUY)
        self.set_quantity(-quantity)

        return quantity * self.price
