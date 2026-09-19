"""Configuration file for the Best Buy application."""

ORDER_PRODUCT_PROMPT = "Which product # do you want? (empty to exit) "
ORDER_EXIT_PROMPT = "When you want to finish order, enter empty text."
ORDER_AMOUNT_PROMPT = "What amount do you want? (empty to exit) "
ORDER_ADDED_TO_CART = "Product added to list!"
ORDER_PLACED = "Order made! Total payment: $"
ORDER_ABORT = "Abort ordering."
ORDER_ERR_QUANT = (
    "Error placing item in cart: "
    "Quantity larger than what exists. Items available: "
)
MENU_PROMPT = "Choose an item by its number [1 - {count}]: "
NO_PRODUCTS_MSG = "There are no products in the store."
PRODUCT_ERR_OUTOFSTOCK = "Out of stock"
PRODUCT_ERR_CANTBYINACTIVE = "Can't buy inactive {name}"
PRODUCT_ERR_CANTBYNEGATIVQUANT = "Can't buy {quantity} pcs of {name}"

VALIDATE_ERR_NOT_OF_TYPE = "{name} is not of type {type}."
VALIDATE_ERR_STR_EMPTY = "{name} can't be empty."
VALIDATE_ERR_MUST_BE_POSITIVE = "{name} can't be negativ."
