from abc import ABC, abstractmethod

from project.guild_members.base_guild_member import BaseGuildMember


class BaseGuildHall(ABC):
    def __init__(self, alias: str):
        self.alias = alias
        self.members: list[BaseGuildMember] = []

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        if len(value.strip()) < 2 or not all(ch.isalpha() or ch.isspace() for ch in value.strip()):
            raise ValueError("Guild hall alias is invalid!")
        self.__alias = value

    @property
    @abstractmethod
    def max_member_count(self):
        pass

    def calculate_total_gold(self):
        return sum(member.gold for member in self.members)

    def status(self):
        if self.members:
            sorted_tags = sorted(member.tag for member in self.members)
            members_str = " *".join(sorted_tags)
        else:
            members_str = "N/A"

        return f"Guild hall: {self.alias}; Members: {members_str}; Total gold: {self.calculate_total_gold()}"

    @abstractmethod
    def increase_gold(self, min_skill_level_value: int):
        pass