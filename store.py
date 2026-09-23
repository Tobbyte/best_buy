"""Store class for the Best Buy application."""
from typing import Any, ClassVar

from products import Product

from standalones.best_buy.config import (
    VALIDATE_ERR_MUST_BE_POSITIVE,
    VALIDATE_ERR_NOT_OF_TYPE,
)


class Store:
    """A class representing a class in the Best Buy application.

    TODOs:
    - guard against inputting identical item. Won't fix.
    TBD:
    - It's questionable if order should be a method of Store.
    """

    __products: list[Product] | list


    def __init__(self, products: list[Product] | None = None) -> None:
        """Initialize a Store instance."""
        self._set_products(products)

    @property
    def products(self) -> list[Product]:
        """Return the list of products in the store.

        Use add_product() and remove_product() methods to modify
        the products in store.
        """
        return self.__products

    def _set_products(self, products: list[Product] | None) -> None:
        """Set the list of products in the store."""
        if not products:
            self.__products = []
            return

        if not isinstance(products, list):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="products",
                    type="list[Product]",
                ),
            )

        for prod in products:
            if not isinstance(prod, Product):
                raise TypeError(
                    VALIDATE_ERR_NOT_OF_TYPE.format(
                        name="product",
                        type="Product",
                    ),
                )

        self.__products = products

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        if not isinstance(product, Product):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="product",
                    type="Product",
                ),
            )
        self.__products.append(product)

    def remove_product(self, prod_to_rem: Product) -> None:
        """Remove a product from the store."""
        if not isinstance(prod_to_rem, Product):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="product",
                    type="Product",
                ),
            )

        self.__products = [
            prod_in_store
            for prod_in_store in self.__products
            if prod_in_store.name != prod_to_rem.name
        ]

    def get_total_quantity(self) -> int:
        """Return the total quantity of all active products in store."""
        return sum(
            prod.quantity for prod in self.__products if prod.is_active()
        )

    def get_all_products(self) -> list[Product]:
        """Return a list of all active products in the store."""
        return [prod for prod in self.__products if prod.is_active()]

    @staticmethod
    def order(shopping_list: list[tuple[Product, int]]) -> float:
        """Place an order of a list of products and their quantities."""
        if not isinstance(shopping_list, list):
            raise TypeError(
                VALIDATE_ERR_NOT_OF_TYPE.format(
                    name="shopping_list",
                    type="list[tuple[Product, int]]",
                ),
            )
        for item, quant in shopping_list:
            if not isinstance(item, Product):
                raise TypeError(
                    VALIDATE_ERR_MUST_BE_POSITIVE.format(name="product"),
                )
            if not isinstance(quant, int):
                raise TypeError(
                    VALIDATE_ERR_NOT_OF_TYPE.format(
                        name="quantity",
                        type="int",
                    ),
                )
            if quant < 0:
                raise ValueError(
                    VALIDATE_ERR_MUST_BE_POSITIVE.format(name="quantity"),
                )

        return sum(item.buy(quant) for item, quant in shopping_list)


## debug
if __name__ == "__main__":
    inactive = Product("Google Pixel 7", price=1, quantity=10)
    active = Product("Bose QuietComfort Earbuds", price=2, quantity=10)
    product_list = [inactive, active]
    best_buy = Store(product_list)
    allproducts = best_buy.get_all_products()
    for produ in allproducts:
        produ.show()
    print(best_buy.order([(active, 10), (inactive, 10)]))
