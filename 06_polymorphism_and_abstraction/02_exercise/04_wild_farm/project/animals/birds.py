from project.animals.animal import Bird
from project.food import Meat, Vegetable, Fruit, Seed


class Owl(Bird):
    @property
    def allowed_food(self):
        return [Meat]

    @property
    def weight_coefficient(self):
        return 0.25

    @staticmethod
    def make_sound():
        return "Hoot Hoot"

class Hen(Bird):
    @property
    def allowed_food(self):
        return [Vegetable, Fruit, Meat, Seed]

    @property
    def weight_coefficient(self):
        return 0.35

    @staticmethod
    def make_sound():
        return "Cluck"