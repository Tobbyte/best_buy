# ruff: noqa: D100, D107, D101, D102
from typing import Any, ClassVar

from fields_validator import validate


class Product:
    ERR_INIT = "Wrong init params."
    ERR_OUTOFSTOCK = "Out of stock"
    ERR_BUY = "BUY err"
    _EVALD_FIELDS: ClassVar[dict] = {
        "name": str,
        "price": float | int,
        "quantity": int,
        "active": bool,
    }

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, name: str, price: float, quantity: int) -> None:

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = max(0, self.quantity + quantity)
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
            err_msg = f"{self.name}: "
            raise ValueError(err_msg + Product.ERR_OUTOFSTOCK)
        self.set_quantity(-quantity)

        return quantity * self.price


## debug
if __name__ == "__main__":
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()
