"""Product class for the Best Buy application."""

from typing import Any

from config import (
    PRODUCT_ERR_CANTACTIVATENULLQUANT,
    PRODUCT_ERR_CANTBYINACTIVE,
    PRODUCT_ERR_CANTBYZEROQUANT,
    PRODUCT_ERR_OUTOFSTOCK,
    PRODUCT_PRETTY_PRINT,
    VALIDATE_ERR_MUST_BE_POSITIVE,
    VALIDATE_ERR_NOT_OF_TYPE,
    VALIDATE_ERR_STR_EMPTY,
)


def validate_non_empty_str(name: str, value: Any) -> str:  # noqa: ANN401
    """Validate that value is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="str"))
    if not value.strip():
        raise ValueError(VALIDATE_ERR_STR_EMPTY.format(name=name))
    return value


def validate_non_negative_num(name: str, value: Any) -> float | int:  # noqa: ANN401
    """Validate that value is a non-negative int or float."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="int or float"),
        )
    if value < 0:
        raise ValueError(VALIDATE_ERR_MUST_BE_POSITIVE.format(name=name))
    return value


def validate_non_negative_int(name: str, value: Any) -> int:  # noqa: ANN401
    """Validate that value is a non-negative integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(VALIDATE_ERR_NOT_OF_TYPE.format(name=name, type="int"))
    if value < 0:
        raise ValueError(VALIDATE_ERR_MUST_BE_POSITIVE.format(name=name))
    return value


class Product:
    """A class representing a product in the Best Buy application.

    Attributes are protected and can be accessed via getters.
    Public setters are provided for quantity and active status.

    - TBD:
        - Raising ValueError when trying to buy more than available
          stock, trying to buy an inactive product or activating
          a product with 0 quantity is pretty harsh.

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
        self.__name = validate_non_empty_str("name", name)

    @property
    def price(self) -> float | int:
        """Return the price of the product."""
        return self.__price

    def _set_price(self, price: float) -> None:
        """Set the price of the product.

        Changing the price of a product is not planned for now, so
        no public setter is provided.
        """
        self.__price = validate_non_negative_num("price", price)

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

        Use activate() and deactivate() methods to modify.
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
        validated_qty = validate_non_negative_int("quantity", quantity)
        if validated_qty == 0:
            self.deactivate()

        self.__quantity = validated_qty

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
            PRODUCT_PRETTY_PRINT(
                self.__name,
                self.__price,
                self.__quantity,
                self.__active,
            ),
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

        quantity = validate_non_negative_int("quantity", quantity)

        if quantity == 0:
            raise ValueError(
                PRODUCT_ERR_CANTBYZEROQUANT.format(
                    name=self.__name,
                ),
            )

        if quantity > self.__quantity:
            raise ValueError(PRODUCT_ERR_OUTOFSTOCK.format(name=self.__name))

        self.set_quantity(self.__quantity - quantity)

        return quantity * self.__price


## debug
if __name__ == "__main__":
    # bose = Product("", price=250, quantity=500)
    bose = Product("as", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(500))
    bose.activate()
    # print(mac.is_active())

    # bose.show()
    # mac.show()
    # bose.buy(0)
    # bose.set_quantity(1000)
    # bose.show()
