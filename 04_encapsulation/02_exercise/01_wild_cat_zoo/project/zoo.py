from project.animal import Animal
from project.worker import Worker


class Zoo:
    def __init__(self, name: str, budget: int, animal_capacity: int, workers_capacity: int):
        self.name = name
        self.__budget = budget
        self.__animal_capacity = animal_capacity
        self.__workers_capacity = workers_capacity
        self.animals: list[Animal] = []
        self.workers: list[Worker] = []

    def add_animal(self, animal: Animal, price: int):
        if self.__budget >= price and self.__animal_capacity > len(self.animals):
            self.__budget -= price
            self.animals.append(animal)
            return f"{animal.name} the {animal.__class__.__name__} added to the zoo"
        elif self.__budget < price and self.__animal_capacity > len(self.animals):
            return "Not enough budget"
        return "Not enough space for animal"

    def hire_worker(self, worker: Worker):
        if self.__workers_capacity > len(self.workers):
            self.workers.append(worker)
            return f"{worker.name} the {worker.__class__.__name__} hired successfully"
        return "Not enough space for worker"

    def fire_worker(self, worker_name: str):
        worker = next((w for w in self.workers if w.name == worker_name), None)
        if worker:
            self.workers.remove(worker)
            return f"{worker_name} fired successfully"
        return f"There is no {worker_name} in the zoo"

    def pay_workers(self):
        total_salaries = sum(w.salary for w in self.workers)
        if total_salaries > self.__budget:
            return "You have no budget to pay your workers. They are unhappy"
        self.__budget -= total_salaries
        return f"You payed your workers. They are happy. Budget left: {self.__budget}"

    def tend_animals(self):
        total_money_for_care = sum(a.money_for_care for a in self.animals)
        if total_money_for_care > self.__budget:
            return "You have no budget to tend the animals. They are unhappy."
        self.__budget -= total_money_for_care
        return f"You tended all the animals. They are happy. Budget left: {self.__budget}"

    def profit(self, amount):
        self.__budget += amount

    def animals_status(self):
        return self.__print_status(self.animals, "Lion", "Tiger", "Cheetah")

    def workers_status(self):
        return self.__print_status(self.workers, "Keeper", "Caretaker", "Vet")

    @staticmethod
    def __print_status(category: list [Animal | Worker], *args):
        elements = {arg: [] for arg in args}
        for element in category:
            elements[element.__class__.__name__].append(repr(element))

        result = [f"You have {len(category)} {category[0].__class__.__bases__[0].__name__.lower()}s"]
        for key, value in elements.items():
            result.append(f"----- {len(value)} {key}s:")
            result.extend(value)

        return '\n'.join(result)