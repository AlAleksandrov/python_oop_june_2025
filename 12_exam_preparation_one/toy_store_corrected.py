from project.stores.base_store import BaseStore


class ToyStore(BaseStore):
    CAPACITY = 100

    def __init__(self, name: str, location: str):
        super().__init__(name, location, self.CAPACITY)

    @property
    def store_type(self):
        return "ToyStore"

    def store_stats(self):
        result = [f"Store: {self.name}, location: {self.location}, available capacity: {self.capacity}",
                  self.get_estimated_profit(),
                  "**Toys for sale:"]

        products = {}
        for product in self.products:
            if product.model not in products:
                products[product.model] = {"count": 0, "total_price": 0.0}
            products[product.model]["count"] += 1
            products[product.model]["total_price"] += product.price

        for model in sorted(products.keys()):
            num_of_product_pieces = products[model]["count"]
            avg_price = products[model]["total_price"] / num_of_product_pieces
            result.append(f"{model}: {num_of_product_pieces}pcs, average price: {avg_price:.2f}")

        return '\n'.join(result)
