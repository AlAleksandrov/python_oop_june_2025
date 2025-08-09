from project.guild_halls.base_guild_hall import BaseGuildHall
from project.guild_halls.combat_hall import CombatHall
from project.guild_halls.magic_tower import MagicTower
from project.guild_members.base_guild_member import BaseGuildMember
from project.guild_members.mage import Mage
from project.guild_members.warrior import Warrior


class GuildMaster:
    MEMBERS_TYPE = {
        "Warrior": Warrior,
        "Mage": Mage
    }

    GUILD_HALLS_TYPE = {
        "CombatHall": CombatHall,
        "MagicTower": MagicTower
    }

    def __init__(self):
        self.members: list[BaseGuildMember] = []
        self.guild_halls: list[BaseGuildHall] = []

    def add_member(self, member_type: str, member_tag: str, member_gold: int):
        if member_type not in self.MEMBERS_TYPE:
            raise ValueError(f"Invalid member type!")

        if any(m.tag == member_tag for m in self.members):
            raise ValueError(f"{member_tag} has already been added!")

        member = self.MEMBERS_TYPE[member_type](member_tag, member_gold)
        self.members.append(member)
        return f"{member_tag} is successfully added as {member_type}."

    def add_guild_hall(self, guild_hall_type: str, guild_hall_alias: str):
        if guild_hall_type not in self.GUILD_HALLS_TYPE:
            raise ValueError(f"Invalid guild hall type!")

        if any(h.alias == guild_hall_alias for h in self.guild_halls):
            raise ValueError(f"{guild_hall_alias} has already been added!")

        guild_hall = self.GUILD_HALLS_TYPE[guild_hall_type](guild_hall_alias)
        self.guild_halls.append(guild_hall)
        return f"{guild_hall_alias} is successfully added as a {guild_hall_type}."

    def assign_member(self, guild_hall_alias: str, member_type: str):
        guild_hall = next((h for h in self.guild_halls if h.alias == guild_hall_alias), None)
        if guild_hall is None:
            raise ValueError(f"Guild hall {guild_hall_alias} does not exist!")

        member_to_assign = next((m for m in self.members if m.role == member_type), None)
        if member_to_assign is None:
            raise ValueError("No available members of the type!")

        if len(guild_hall.members) >= guild_hall.max_member_count:
            return "Maximum member count reached. Assignment is impossible."

        self.members.remove(member_to_assign)
        guild_hall.members.append(member_to_assign)

        return f"{member_to_assign.tag} was assigned to {guild_hall_alias}."

    @staticmethod
    def practice_members(guild_hall: BaseGuildHall, sessions_number: int):
        for _ in range(sessions_number):
            for member in guild_hall.members:
                member.practice()

        total_skill_level = sum(m.skill_level for m in guild_hall.members)

        return f"{guild_hall.alias} members have {total_skill_level} total skill level after {sessions_number} practice session/s."

    def unassign_member(self, guild_hall: BaseGuildHall, member_tag: str):
        member_to_unassign = next((m for m in guild_hall.members if m.tag == member_tag), None)

        if member_to_unassign is None or member_to_unassign.skill_level == 10:
            return "The unassignment process was canceled."

        guild_hall.members.remove(member_to_unassign)
        self.members.append(member_to_unassign)

        return f"Unassigned member {member_tag}."

    def guild_update(self, min_skill_level_value: int):
        for hall in self.guild_halls:
            hall.increase_gold(min_skill_level_value)

        sorted_halls = sorted(self.guild_halls, key=lambda h: (-len(h.members), h.alias))

        result = "<<<Guild Updated Status>>>\n"
        result += f"Unassigned members count: {len(self.members)}\n"
        result += f"Guild halls count: {len(self.guild_halls)}"

        for hall in sorted_halls:
            result += f"\n>>>{hall.status()}"

        return result