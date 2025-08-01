from project.products.base_product import BaseProduct
from project.products.chair import Chair
from project.products.hobby_horse import HobbyHorse
from project.stores.base_store import BaseStore
from project.stores.furniture_store import FurnitureStore
from project.stores.toy_store import ToyStore


class FactoryManager:
    PRODUCT_TYPES = {"Chair": Chair,
                     "HobbyHorse": HobbyHorse
    }

    STORE_TYPES = {'FurnitureStore': FurnitureStore,
                   'ToyStore': ToyStore
    }

    def __init__(self, name: str):
        self.name = name
        self.income: float = 0.0
        self.products: list[BaseProduct] = []
        self.stores: list[BaseStore] = []

    def produce_item(self, product_type: str, model: str, price: float):
        if product_type not in self.PRODUCT_TYPES:
            raise Exception("Invalid product type!")
        product = self.PRODUCT_TYPES[product_type](model, price)
        self.products.append(product)
        return f"A product of sub-type {product.sub_type} was produced."

    def register_new_store(self, store_type: str, name: str, location: str):
        if store_type not in self.STORE_TYPES:
            raise Exception(f"{store_type} is an invalid type of store!")
        store = self.STORE_TYPES[store_type](name, location)
        self.stores.append(store)
        return f"A new {store_type} was successfully registered."

    def sell_products_to_store(self, store: BaseStore, *products: BaseProduct):
        if store.capacity < len(products):
            return f"Store {store.name} has no capacity for this purchase."

        # Filter products based on store type
        suitable_products = []
        for product in products:
            if (store.store_type == "FurnitureStore" and product.sub_type == "Furniture") or \
               (store.store_type == "ToyStore" and product.sub_type == "Toys"):
                suitable_products.append(product)

        if not suitable_products:
            return "Products do not match in type. Nothing sold."

        # Process the sale
        for product in suitable_products:
            self.products.remove(product)
            store.products.append(product)
            self.income += product.price

        store.capacity -= len(suitable_products)
        return f"Store {store.name} successfully purchased {len(suitable_products)} items."

    def unregister_store(self, store_name: str):
        store = self.__find_store(store_name)
        if store is None:
            raise Exception("No such store!")
        if store.products:
            return "The store is still having products in stock! Unregistering is inadvisable."
        self.stores.remove(store)
        return f"Successfully unregistered store {store_name}, location: {store.location}."

    def discount_products(self, product_model: str):
        filtered_product = [p for p in self.products if p.model == product_model]
        for product in filtered_product:
            product.discount()
        return f"Discount applied to {len(filtered_product)} products with model: {product_model}"

    def request_store_stats(self, store_name: str):
        store = self.__find_store(store_name)
        if store is None:
            return "There is no store registered under this name!"
        return store.store_stats()

    def statistics(self):
        products = {}
        total_price = 0
        for product in self.products:
            products[product.model] = products.get(product.model, 0) + 1
            total_price += product.price

        result = [f"Factory: {self.name}",
                    f"Income: {self.income:.2f}",
                  "***Products Statistics***",
                  f"Unsold Products: {len(self.products)}. Total net price: {total_price:.2f}"
        ]

        for model in sorted(products.keys()):
            result.append(f"{model}: {products[model]}")

        result.append(f'***Partner Stores: {len(self.stores)}***')

        for store in sorted(self.stores, key=lambda s: s.name):
            result.append(store.name)

        return '\n'.join(result)

    def __find_store(self, name):
        return next((s for s in self.stores if s.name == name), None)
