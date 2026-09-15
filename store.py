# ruff: noqa: D100, D101
from typing import ClassVar

from products import Product


class Store:
    _EVALD_FIELDS: ClassVar[dict] = {
        "product": Product,
    }

    def __init__(self, products: list[Product] | None) -> None:
        self.products = products or []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product: Product):
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
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products[0], 1), (products[1], 2)]))
