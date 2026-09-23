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
    """A class representing a product in the Best Buy application.

    Attributes are protected and can be accessed via getters.
    Setters are provided for quantity and active status.
    """

    _EVALD_FIELDS: ClassVar[dict] = {
        "name": str,
        "price": float | int,
        "quantity": int,
    }

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Initialize a Product instance."""
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__active = quantity > 0

    @property
    def quantity(self) -> int:
        """Return the current quantity of the product.

        Use set_quantity() to modify the quantity, which includes
        validation and automatic deactivation.
        """
        return self.__quantity

    @property
    def name(self) -> str:
        """Return the name of the product.

        Changing the name of a product is not planned for now, so
        no setter is provided.
        """
        return self.__name

    @property
    def price(self) -> float:
        """Return the price of the product.

        Changing the price of a product is not planned for now, so
        no setter is provided.
        """
        return self.__price

    @property
    def active(self) -> bool:
        """Return whether the product is active.

        Use activate() and deactivate() methods instead, which include
        validation.
        """
        return self.__active

    def get_quantity(self) -> int:
        """Return the current quantity of the product."""
        return self.__quantity

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

        if quantity == 0:
            self.deactivate()

        self.__quantity = quantity

    def is_active(self) -> bool:
        """Return whether product is available for purchase (active)."""
        return self.__active

    def activate(self) -> None:
        """Activate the product, making it available for purchase.

        Raises ValueError if the product has zero quantity.
        """
        if self.__quantity == 0:
            raise ValueError(PRODUCT_ERR_CANTACTIVATENULLQUANT)
        self.__active = True

    def deactivate(self) -> None:
        """Deactivate the product, that is unavailable for purchase."""
        self.__active = False

    def show(self) -> None:
        """Print product details in a user-friendly format."""
        print(
            f"'{self.__name}', Price: {self.__price:.2f} ¤, "
            f"Quantity: {self.__quantity}",
            (" (inactive)" if not self.is_active() else ""),
        )

    def buy(self, quantity: int) -> float:
        """Buy a specified quantity of the product.

        Raises ValueError if the product is inactive, if the quantity is
        negative, or if the requested quantity exceeds available stock.
        """
        if not self.__active:
            raise ValueError(
                PRODUCT_ERR_CANTBYINACTIVE.format(name=self.__name),
            )

        if quantity <= 0:
            raise ValueError(
                PRODUCT_ERR_CANTBYNEGATIVQUANT.format(
                    quantity=quantity,
                    name=self.__name,
                ),
            )

        if quantity > self.__quantity:
            err_msg = f"{self.__name}: "
            raise ValueError(err_msg + PRODUCT_ERR_OUTOFSTOCK)
        self.set_quantity(self.__quantity - quantity)

        return quantity * self.__price


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
