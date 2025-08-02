from project.battleships.pirate_battleship import PirateBattleship
from project.zones.base_zone import BaseZone


class RoyalZone(BaseZone):
    VOLUME = 10

    def __init__(self, code: str):
        super().__init__(code,self.VOLUME)

    def zone_info(self):
        pirate_ships_count = len([s for s in self.ships if isinstance(s, PirateBattleship)])
        result = ["@Royal Zone Statistics@",
                  f"Code: {self.code}; Volume: {self.volume}",
                  f"Battleships currently in the Royal Zone: {len(self.ships)}, {pirate_ships_count} out of them are Pirate Battleships."
        ]

        if self.ships:
            ship_names = [s.name for s in self.get_ships()]
            result.append("#" + ', '.join(ship_names) + "#")

        return '\n'.join(result)