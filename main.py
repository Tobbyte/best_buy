"""Main module for the Best Buy application."""

import sys

from config import (
    MENU_PROMPT,
    ORDER_ABORT,
    ORDER_ADDED_TO_CART,
    ORDER_AMOUNT_PROMPT,
    ORDER_ERR_QUANT,
    ORDER_EXIT_PROMPT,
    ORDER_PLACED,
    ORDER_PRODUCT_PROMPT,
)
from products import Product
from store import Store
from valid_tobbyte_module.valid_tobbyte.validator_fn import (
    validate_fn as get_valid_input,
)

_CACHE_STORE = None  # until I know valid singletons


def _store(product_list: list | None = None) -> Store:
    """Create a singleton Store instance.

    If product_list is provided, initialized with those products.
    """
    global _CACHE_STORE  # noqa: PLW0603
    if not _CACHE_STORE:
        _CACHE_STORE = Store(product_list)
    return _CACHE_STORE


def _place_order() -> None:
    """Place an order for products."""
    print("Available products:")
    shopping_card = []
    product_selection = None
    amount_selection = None
    available_products = _store().get_all_products()
    products_dispatch = {}

    def get_amount_in_cart(product: Product) -> int:
        return sum([tup[1] for tup in shopping_card if tup[0] is product])

    # construct and print product selection menu
    for i in range(len(available_products)):
        products_dispatch[i + 1] = available_products[i]
        print(f"{i + 1}: ", end="")
        available_products[i].show()
    print(ORDER_EXIT_PROMPT)
    print()

    # loop ordering
    while True:
        new_product_selection = get_valid_input(
            valid_inputs=[
                *list(range(1, len(products_dispatch) + 1)),
                "Enter",
            ],
            prompt=ORDER_PRODUCT_PROMPT,
            exit_promt="",
        )

        if not new_product_selection:
            # returned from product selection menu wo selection
            if not shopping_card:
                # made not prev. placement, abort to main menu
                print("\n" + ORDER_ABORT)
                return
            break

        product_selection = new_product_selection - 1  # reset from display

        new_amount_selection = get_valid_input(
            valid_inputs=[int, "Enter"],
            prompt=ORDER_AMOUNT_PROMPT,
            exit_promt="",
        )
        if not new_amount_selection:
            # returned from amount selection menu wo selection
            if not shopping_card:
                # made not prev. placement, abort to main menu
                print("\n" + ORDER_ABORT)
                return
            break

        items_of_product_availale = available_products[
            product_selection
        ].get_quantity() - get_amount_in_cart(
            available_products[product_selection],
        )

        if new_amount_selection > items_of_product_availale:
            print(f"{ORDER_ERR_QUANT} {items_of_product_availale}")
        else:
            amount_selection = new_amount_selection

            shopping_card.append((
                available_products[product_selection],
                amount_selection,
            ))

            print(ORDER_ADDED_TO_CART)
            print()

    if product_selection is not None and amount_selection is not None:
        print("\n\n***********")
        total = _store().order(shopping_card)
        print(ORDER_PLACED + str(total))
        print("***********")
    return


def _print_all_products() -> None:
    """Print all products in the store."""
    print("Products in store:")
    for p in _store().get_all_products():
        p.show()


def _get_total_store_stock() -> None:
    """Print the total quantity of all products in the store."""
    print(f"Total of {_store().get_total_quantity()} items in store")


def _start() -> None:
    """Start the Best Buy application with a menu-driven interface."""
    print()
    print("Store Menu")
    print("------")
    menu_dispatch = {
        1: ("List all products in store", _print_all_products),
        2: ("Show total amount in store", _get_total_store_stock),
        3: ("Make an order", _place_order),
        4: ("Quit", sys.exit),
    }
    while True:
        list(
            map(
                print,
                (f"{tup[0]} {tup[1][0]}" for tup in menu_dispatch.items()),
            ),
        )  # unnecessary complex but fun
        print()
        selection = get_valid_input(
            valid_inputs=list(range(1, len(menu_dispatch) + 1)),
            prompt=MENU_PROMPT(len(menu_dispatch)),
        )

        if not selection:  # exit by double enter none in get_valid_input
            sys.exit()

        print()
        print("------")
        menu_dispatch[selection][1]()
        print()


def init_superstore() -> None:
    """Initialize the Best Buy application.

    Use a predefined set of products and start the menu interface.
    """
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]
    _store(product_list)
    _start()


if __name__ == "__main__":
    init_superstore()
