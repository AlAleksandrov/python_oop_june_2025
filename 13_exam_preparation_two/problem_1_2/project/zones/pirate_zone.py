from project.battleships.royal_battleship import RoyalBattleship
from project.zones.base_zone import BaseZone


class PirateZone(BaseZone):
    VOLUME = 8

    def __init__(self, code: str):
        super().__init__(code,self.VOLUME)

    def zone_info(self):
        royal_ships_count = len([s for s in self.ships if isinstance(s, RoyalBattleship)])
        result = ["@Pirate Zone Statistics@",
                  f"Code: {self.code}; Volume: {self.volume}",
                  f"Battleships currently in the Pirate Zone: {len(self.ships)}, {royal_ships_count} out of them are Royal Battleships."
        ]

        if self.ships:
            ship_names = [s.name for s in self.get_ships()]
            result.append("#" + ', '.join(ship_names) + "#")

        return '\n'.join(result)