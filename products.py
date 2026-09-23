"""Product class for the Best Buy application."""
from __future__ import annotations  # needed to return Class in Class def

from typing import Any, ClassVar

from config import (
    PRODUCT_ERR_CANTACTIVATENULLQUANT,
    PRODUCT_ERR_CANTBYINACTIVE,
    PRODUCT_ERR_CANTBYNEGATIVQUANT,
    PRODUCT_ERR_CANTHAVENEGATIVEQUANT,
    PRODUCT_ERR_OUTOFSTOCK,
)
from fields_validator import validate


class Product:
    """A class representing a product in the Best Buy application."""

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
        self.active = quantity > 0

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Set the quantity of the product.

        Ensures it doesn't go below zero.
        Deactivates the product if quantity is zero.
        Be aware that setting a quantity above 0 when its not active
        - whether deliberately set or automatically because of 0
        quantity - will not automatically activate the product.
        Use activate() for that.
        """
        if quantity < 0:
            raise ValueError(PRODUCT_ERR_CANTHAVENEGATIVEQUANT)

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether product is available for purchase (active)."""
        return self.active

    def activate(self) -> None:
        """Activate the product, making it available for purchase.

        Raises ValueError if the product has zero quantity.
        """
        if self.quantity == 0:
            raise ValueError(PRODUCT_ERR_CANTACTIVATENULLQUANT)
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the product, that is unavailable for purchase."""
        self.active = False

    def show(self) -> None:
        """Print product details in a user-friendly format."""
        print(
            f"'{self.name}', Price: {self.price:.2f} ¤, "
            f"Quantity: {self.quantity}",
            (" (inactive)" if not self.is_active() else ""),
        )

    def buy(self, quantity: int) -> float:
        """Buy a specified quantity of the product.

        Raises ValueError if the product is inactive, if the quantity is
        negative, or if the requested quantity exceeds available stock.
        """
        if not self.active:
            raise ValueError(PRODUCT_ERR_CANTBYINACTIVE.format(name=self.name))

        if quantity <= 0:
            raise ValueError(
                PRODUCT_ERR_CANTBYNEGATIVQUANT.format(
                    quantity=quantity,
                    name=self.name,
                ),
            )

        if quantity > self.quantity:
            err_msg = f"{self.name}: "
            raise ValueError(err_msg + PRODUCT_ERR_OUTOFSTOCK)
        self.set_quantity(self.quantity - quantity)

        return quantity * self.price


## debug
if __name__ == "__main__":
    # bose = Product("", price=250, quantity=500)
    bose = Product("as", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(500))
    bose.activate()
    # print(mac.buy(100))
    # print(mac.is_active())

    # bose.show()
    # mac.show()
    # bose.buy(0)
    # bose.set_quantity(1000)
    # bose.show()
