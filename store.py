# ruff: noqa: D100, D101
from typing import Any, ClassVar

from fields_validator import validate
from products import Product


class Store:
    _EVALD_FIELDS: ClassVar[dict] = {
        "products": list | None,
    }

    @staticmethod
    def guard_valid_product(product: Any):  # noqa: ANN401
        if not isinstance(product, Product):
            err_msg = "add_product: 'product' is not of type Product"
            raise TypeError(err_msg)

    @validate(_EVALD_FIELDS)
    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set attribute with validation."""
        super().__setattr__(name, value)

    def __init__(self, products: list[Product] | None = None) -> None:
        if products:
            for p in products:
                Store.guard_valid_product(p)
        self.products = products or []

    def add_product(self, product: Product) -> None:
        Store.guard_valid_product(product)
        self.products.append(product)

    def remove_product(self, product: Product):
        Store.guard_valid_product(product)
        map(
            self.products.remove,
            (
                prod_in_store
                for prod_in_store in self.products
                if prod_in_store.name == product.name
            ),
        )

    def get_total_quantity(self) -> int:
        return sum(prod.quantity for prod in self.products)

    def get_all_products(self) -> list[Product]:
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
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
