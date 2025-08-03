from project.clients.base_client import BaseClient
from project.clients.business_client import BusinessClient
from project.clients.regular_client import RegularClient
from project.plants.base_plant import BasePlant
from project.plants.flower import Flower
from project.plants.leaf_plant import LeafPlant


class FlowerShopManager:
    PLANT_TYPES = {
        "Flower": Flower,
        "LeafPlant": LeafPlant
    }
    CLIENT_TYPES = {
        "RegularClient": RegularClient,
        "BusinessClient": BusinessClient
    }

    def __init__(self):
        self.income: float = 0.0
        self.plants: list[BasePlant] = []
        self.clients: list[BaseClient] = []

    def add_plant(self, plant_type: str, plant_name: str, plant_price: float, plant_water_needed: int, plant_extra_data: str):
        if plant_type not in self.PLANT_TYPES:
            raise ValueError("Unknown plant type!")
        plant = self.PLANT_TYPES[plant_type](plant_name, plant_price, plant_water_needed, plant_extra_data)
        self.plants.append(plant)
        return f"{plant_name} is added to the shop as {plant_type}."

    def add_client(self, client_type: str, client_name: str, client_phone_number: str):
        if client_type not in self.CLIENT_TYPES:
            raise ValueError("Unknown client type!")
        if any(c.phone_number == client_phone_number for c in self.clients):
            raise ValueError("This phone number has been used!")
        client = self.CLIENT_TYPES[client_type](client_name, client_phone_number)
        self.clients.append(client)
        return f"{client_name} is successfully added as a {client_type}."

    def sell_plants(self, client_phone_number: str, plant_name: str, plant_quantity: int):
        client = next((c for c in self.clients if c.phone_number == client_phone_number), None)
        if client is None:
            raise ValueError("Client not found!")
        plants = [p for p in self.plants if p.name == plant_name]
        if not plants:
            raise ValueError("Plants not found!")
        if plant_quantity > len(plants):
            return "Not enough plant quantity."

        amount = plants[0].price * plant_quantity * ((100 - client.discount) / 100)
        self.income += amount
        for _ in range(plant_quantity):
            plant = next(p for p in self.plants if p.name == plant_name)
            self.plants.remove(plant)
        client.update_total_orders()
        client.update_discount()
        return f"{plant_quantity}pcs. of {plant_name} plant sold for {amount:.2f}"

    def remove_plant(self, plant_name: str):
        plant = next((p for p in self.plants if p.name == plant_name), None)
        if plant is None:
            return "No such plant name."
        self.plants.remove(plant)
        return f"Removed {plant.plant_details()}"

    def remove_clients(self):
        count = 0
        to_remove = [c for c in self.clients if c.total_orders == 0]
        for client in to_remove:
            count += 1
            self.clients.remove(client)
        return f"{count} client/s removed."

    def shop_report(self):
        count_of_all_orders = sum(c.total_orders for c in self.clients)

        result = ["~Flower Shop Report~",
                    f"Income: {self.income:.2f}",
                    f"Count of orders: {count_of_all_orders}",
                    f"~~Unsold plants: {len(self.plants)}~~"
        ]

        plant_counts = {}
        for plant in self.plants:
            if plant.name not in plant_counts:
                plant_counts[plant.name] = 0
            plant_counts[plant.name] += 1
        sorted_plants = sorted(plant_counts.items(), key=lambda x: (-x[1], x[0]))
        for name, count in sorted_plants:
            result.append(f"{name}: {count}")

        result.append(f"~~Clients number: {len(self.clients)}~~")

        sorted_clients = sorted(self.clients, key=lambda c: (-c.total_orders, c.phone_number))
        for client in sorted_clients:
            result.append(client.client_details())

        return '\n'.join(result)