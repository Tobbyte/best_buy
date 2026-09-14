from products import Product
from store import Store

bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
mac = Product("MacBook Air M2", price=1450, quantity=100)

print("bose.buy(50)", bose.buy(50))
print("mac.buy(10)", mac.buy(10))
print("mac.is_active()", mac.is_active())

bose.show()
mac.show()

bose.set_quantity(1000)
bose.show()

# instance of a store
best_buy = Store([bose, mac])

pixel = Product("Google Pixel 7", price=500, quantity=250)
best_buy.add_product(pixel)


price = best_buy.order([(bose, 5), (mac, 30), (bose, 10)])
print(f"Order cost: {price} dollars.")


product_list = [
    Product("MacBook Air M2", price=1450, quantity=100),
    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    Product("Google Pixel 7", price=500, quantity=250),
]

best_buy = Store(product_list)
products = best_buy.get_all_products()
print("total quant:", best_buy.get_total_quantity())
print(
    "order product_list:",
    best_buy.order([(products[0], 1), (products[1], 2)]),
)
