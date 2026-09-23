"""Store class for the Best Buy application."""
from typing import Any, ClassVar

from fields_validator import validate
from products import Product

from standalones.best_buy.config import PRODUCT_ERR_NOT_OF_TYPE


class Store:
    """A class representing a class in the Best Buy application.

    TODOs:
    - guard against inputting identical item. Won't fix.
    """

    _EVALD_FIELDS: ClassVar[dict] = {
        "products": list | None,
    }

    @staticmethod
    def guard_valid_product(product: Any) -> None:  # noqa: ANN401
        """Guard to ensure the product is an instance of Product.

        Raises TypeError if the product is not an instance of Product.
        """
        if not isinstance(product, Product):
            raise TypeError(PRODUCT_ERR_NOT_OF_TYPE)

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, products: list[Product] | None = None) -> None:
        """Initialize a Store instance."""
        if products:
            for prod in products:
                Store.guard_valid_product(prod)
        self.products = products or []

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        Store.guard_valid_product(product)
        self.products.append(product)

    def remove_product(self, prod_to_rem: Product) -> None:
        """Remove a product from the store."""
        Store.guard_valid_product(prod_to_rem)
        self.products = [
            prod_in_store
            for prod_in_store in self.products
            if prod_in_store.name != prod_to_rem.name
        ]

    def get_total_quantity(self) -> int:
        """Return the total quantity of all active products in store."""
        return sum(prod.quantity for prod in self.products if prod.is_active())

    def get_all_products(self) -> list[Product]:
        """Return a list of all active products in the store."""
        return [prod for prod in self.products if prod.is_active()]

    @staticmethod
    def order(shopping_list: list[tuple[Product, int]]) -> float:
        """Place an order of a list of products and their quantities."""
        # No validation of shopping_list bc parameterized generic.
        # Would need deep nasty nested checks or better param. Won't fix
        # See in 'validate' doc.
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
