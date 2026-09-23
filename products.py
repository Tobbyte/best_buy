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


class Product:
    """A class representing a product in the Best Buy application.

    Attributes are protected and can be accessed via getters.
    Public setters are provided for quantity and active status.
    """

    # Note to self: these are instance attribute annotations that define
    # the schema, and do not create a shared class state
    __name: str
    __price: float | int
    __quantity: int
    __active: bool

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Initialize a Product instance."""
        self._set_name(name)
        self._set_price(price)
        self.set_quantity(quantity)
        self.__active = quantity > 0

    @property
    def name(self) -> str:
        """Return the name of the product."""
        return self.__name

    def _set_name(self, name: str) -> None:
        """Set the name of the product.

        Changing the name of a product is not planned for now, so
        no public setter is provided.
        """
        if not name:
            raise ValueError(
                VALIDATE_ERR_STR_EMPTY.format(name="name"),
            )

        if not isinstance(name, str):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="name",
                    type="str",
                ),
            )
        self.__name = name

    @property
    def price(self) -> float:
        """Return the price of the product."""
        return self.__price

    def _set_price(self, price: float) -> None:
        """Set the price of the product.

        Changing the price of a product is not planned for now, so
        no public setter is provided.
        """
        if not isinstance(price, (int, float)):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="price",
                    type="int or float",
                ),
            )
        if price < 0:
            raise ValueError(
                VALIDATE_ERR_MUST_BE_POSITIVE.format(name="price"),
            )
        self.__price = price

    @property
    def quantity(self) -> int:
        """Return the current quantity of the product.

        Use set_quantity() to modify the quantity, which includes
        validation and automatic deactivation.
        """
        return self.__quantity

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
