from project.stores.base_store import BaseStore


class ToyStore(BaseStore):
    CAPACITY = 100

    def __init__(self, name: str, location: str):
        super().__init__(name, location, self.CAPACITY)

    @property
    def store_type(self):
        return "ToyStore"

    def __str__(self):
        return "Toys"