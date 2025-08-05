from project.clients.base_client import BaseClient
from project.clients.regular_client import RegularClient
from project.clients.vip_client import VIPClient
from project.waiters.base_waiter import BaseWaiter
from project.waiters.full_time_waiter import FullTimeWaiter
from project.waiters.half_time_waiter import HalfTimeWaiter


class SphereRestaurantApp:
    WAITER_TYPES = {
        "FullTimeWaiter": FullTimeWaiter,
        "HalfTimeWaiter": HalfTimeWaiter
    }

    CLIENT_TYPES = {
        "RegularClient": RegularClient,
        "VIPClient": VIPClient
    }

    def __init__(self):
        self.waiters: list[BaseWaiter] = []
        self.clients: list[BaseClient] = []

    def hire_waiter(self, waiter_type: str, waiter_name: str, hours_worked: int):
        if waiter_type not in self.WAITER_TYPES:
            return f"{waiter_type} is not a recognized waiter type."
        waiter = [w for w in self.waiters if w.name == waiter_name]
        if waiter:
            return f"{waiter_name} is already on the staff."

        waiter = self.WAITER_TYPES[waiter_type](waiter_name, hours_worked)
        self.waiters.append(waiter)
        return f"{waiter_name} is successfully hired as a {waiter_type}."

    def admit_client(self, client_type: str, client_name: str):
        if client_type not in self.CLIENT_TYPES:
            return f"{client_type} is not a recognized client type."
        client = [c for c in self.clients if c.name == client_name]
        if client:
            return f"{client_name} is already a client."

        client = self.CLIENT_TYPES[client_type](client_name)
        self.clients.append(client)
        return f"{client_name} is successfully admitted as a {client_type}."

    def process_shifts(self, waiter_name: str):
        waiter = next((w for w in self.waiters if w.name == waiter_name), None)
        if waiter is None:
            return f"No waiter found with the name {waiter_name}."
        return waiter.report_shift()

    def process_client_order(self, client_name: str, order_amount: float):
        client = next((c for c in self.clients if c.name == client_name), None)
        if client is None:
            return f"{client_name} is not a registered client."
        points_earned = client.earning_points(order_amount)
        return f"{client_name} earned {points_earned} points from the order."

    def apply_discount_to_client(self, client_name: str):
        client = next((c for c in self.clients if c.name == client_name), None)
        if client is None:
            return f"{client_name} cannot get a discount because this client is not admitted!"
        discount = client.apply_discount()[0]
        return f"{client_name} received a {discount}% discount. Remaining points {client.points}"

    def generate_report(self):
        total_earnings = sum(w.calculate_earnings() for w in self.waiters)
        total_client_points = sum(c.points for c in self.clients)
        result = ["$$ Monthly Report $$",
                f"Total Earnings: ${total_earnings:.2f}",
                f"Total Clients Unused Points: {total_client_points}",
                f"Total Clients Count: {len(self.clients)}",
                "** Waiter Details **"
        ]

        sorted_waiters = sorted(self.waiters, key=lambda w: -w.calculate_earnings())
        for waiter in sorted_waiters:
            result.append(waiter.__str__())

        return '\n'.join(result)