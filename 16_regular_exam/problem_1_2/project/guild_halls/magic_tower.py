from project.guild_halls.base_guild_hall import BaseGuildHall


class MagicTower(BaseGuildHall):
    def __init__(self, alias: str):
        super().__init__(alias)

    @property
    def max_member_count(self):
        return 4

    def increase_gold(self, min_skill_level_value: int):
        for member in self.members:
            if member.role == "Mage" and member.skill_level >= min_skill_level_value:
                member.gold *= 2