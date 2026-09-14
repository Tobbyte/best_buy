# ruff: noqa: D100, D107, D101, D102
class Product:
    ERR_INIT = "Wrong init params."
    ERR_BUY = "BUY err"

    def __init__(self, name: str, price: float, quantity: int) -> None:
        print(name, price, quantity)
        if (
            not name
            or not isinstance(name, str)
            or not isinstance(price, (float, int))
            or not isinstance(quantity, int)
        ):
            raise ValueError(Product.ERR_INIT)

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = min(0, self.quantity + quantity)
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> bool:
        self.active = True
        return self.active

    def deactivate(self) -> bool:
        self.active = False
        return self.active

    def show(self) -> None:
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float:
        if quantity > self.quantity:
            raise ValueError(Product.ERR_BUY)
        self.set_quantity(-quantity)

        return quantity * self.price
