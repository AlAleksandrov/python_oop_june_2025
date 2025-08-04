from abc import ABC, abstractmethod

from project.artifacts.base_artifact import BaseArtifact


class BaseCollector(ABC):
    def __init__(self, name: str, available_money: float, available_space: int):
        self.name = name
        self.available_money = available_money
        self.available_space = available_space
        self.purchased_artifacts: list[BaseArtifact] = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.strip() or any(not (ch.isalnum() or ch == ' ') for ch in value):
            raise ValueError("Collector name must contain letters, numbers, and optional white spaces between them!")
        self.__name = value

    @property
    def available_money(self):
        return self.__available_money

    @available_money.setter
    def available_money(self, value):
        if value < 0.0:
            raise ValueError("A collector cannot have a negative amount of money!")
        self.__available_money = value

    @property
    def available_space(self):
        return self.__available_space

    @available_space.setter
    def available_space(self, value):
        if value < 0:
            raise ValueError("A collector cannot have a negative space available for exhibitions!")
        self.__available_space = value

    @abstractmethod
    def increase_money(self):
        pass

    def can_purchase(self, artifact_price: float, artifact_space_required: int):
        if self.available_money >= artifact_price and self.available_space >= artifact_space_required:
            return True
        return False

    def __str__(self):
        artifacts = sorted((a.name for a in self.purchased_artifacts), reverse=True)


        result = f"Collector name: {self.name}; Money available: {self.available_money:.2f}; Space available: {self.available_space}; Artifacts: "

        if artifacts:
            result += ', '.join(artifacts)
        else:
            result += "none"
        return result