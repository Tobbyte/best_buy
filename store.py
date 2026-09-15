"""Store class for the Best Buy application."""
from typing import Any, ClassVar

from fields_validator import validate
from products import Product


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
            err_msg = "add_product: 'product' is not of type Product"
            raise TypeError(err_msg)

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, products: list[Product] | None = None) -> None:
        """Initialize a Store instance."""
        if products:
            for p in products:
                Store.guard_valid_product(p)
        self.products = products or []

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        Store.guard_valid_product(product)
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """Remove a product from the store."""
        Store.guard_valid_product(product)
        list(
            map(
                self.products.remove,  # assumes products never double
                (
                    prod_in_store
                    for prod_in_store in self.products
                    if prod_in_store.name == product.name
                ),
            ),
        )

    def get_total_quantity(self) -> int:
        """Return the total quantity of all products in the store."""
        return sum(prod.quantity for prod in self.products)

    def get_all_products(self) -> list[Product]:
        """Return a list of all products in the store."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """Place an order of a list of products and their quantities."""
        # No validation of shopping_list bc parameterized generic.
        # Would need deep nasty nested checks or better param. Won't fix
        # See in 'validate' doc.
        total: float = 0
        for item, quant in shopping_list:
            total += item.price * quant
            item.buy(quant)
        return total


## debug
if __name__ == "__main__":
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)
    products = best_buy.get_all_products()
    best_buy.add_product(
        Product("MacBook Air M2222", price=1450, quantity=100),
    )
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products[0], 1), (products[1], 2)]))
    # ^ not caught by validate
