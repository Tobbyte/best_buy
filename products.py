"""Product class for the Best Buy application."""
from __future__ import annotations  # needed to return Class in Class def

from typing import Any, ClassVar

from config import PRODUCT_ERR_OUTOFSTOCK
from fields_validator import validate


class Product:
    """A class representing a product in the Best Buy application."""

    # good way to do? not sure
    ERR_OUTOFSTOCK = PRODUCT_ERR_OUTOFSTOCK

    _EVALD_FIELDS: ClassVar[dict] = {
        "name": str,
        "price": float | int,
        "quantity": int,
        "active": bool,
    }

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Initialize a Product instance."""
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Set the quantity of the product.

        Ensures it doesn't go below zero.
        """
        self.quantity = max(0, self.quantity + quantity)
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether product is available for purchase (active)."""
        return self.active

    def activate(self) -> Product:
        """Activate the product, making it available for purchase."""
        self.active = True
        return self

    def deactivate(self) -> Product:
        """Deactivate the product, that is unavailable for purchase."""
        self.active = False
        return self

    def show(self) -> None:
        """Print product details in a user-friendly format."""
        print(
            f"'{self.name}', Price: {self.price:.2f} ¤, "
            f"Quantity: {self.quantity}",
        )

    def buy(self, quantity: int) -> float:
        """Buy a specified quantity of the product."""
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
