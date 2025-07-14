from project.customer import Customer
from project.equipment import Equipment
from project.exercise_plan import ExercisePlan
from project.subscription import Subscription
from project.trainer import Trainer


class Gym:
    def __init__(self):
        self.customers: list[Customer] = []
        self.trainers: list[Trainer] = []
        self.equipment: list[Equipment] = []
        self.plans: list[ExercisePlan] = []
        self.subscriptions: list[Subscription] = []

    def add_customer(self, customer: Customer):
        self.__add_object(customer, self.customers)

    def add_trainer(self, trainer: Trainer):
        self.__add_object(trainer, self.trainers)

    def add_equipment(self, equipment: Equipment):
        self.__add_object(equipment, self.equipment)

    def add_plan(self, plan: ExercisePlan):
        self.__add_object(plan, self.plans)

    def add_subscription(self, subscription: Subscription):
        self.__add_object(subscription, self.subscriptions)

    def subscription_info(self, subscription_id: int):
        subscription = next((s for s in self.subscriptions if s.id == subscription_id), None)
        customer = next((c for c in self.customers if c.id == subscription.customer_id), None)
        trainer = next((t for t in self.trainers if t.id == subscription.trainer_id), None)
        plan = next((p for p in self.plans if p.id == subscription.exercise_id), None)
        equipments = next((e for e in self.equipment if e.id == plan.equipment_id), None)
        return '\n'.join([repr(subscription), repr(customer), repr(trainer), repr(equipments), repr(plan)])


    @staticmethod
    def __add_object(curr_object, object_list: list):
        if curr_object not in object_list:
            object_list.append(curr_object)