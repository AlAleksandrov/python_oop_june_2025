from project.battleships.base_battleship import BaseBattleship
from project.battleships.pirate_battleship import PirateBattleship
from project.battleships.royal_battleship import RoyalBattleship
from project.zones.base_zone import BaseZone
from project.zones.pirate_zone import PirateZone
from project.zones.royal_zone import RoyalZone


class BattleManager:
    ZONE_TYPES = {
        "RoyalZone": RoyalZone,
        "PirateZone": PirateZone
    }

    SHIP_TYPES = {
        "RoyalBattleship": RoyalBattleship,
        "PirateBattleship": PirateBattleship
    }

    def __init__(self):
        self.zones: list[BaseZone] = []
        self.ships: list[BaseBattleship] = []

    def add_zone(self, zone_type: str, zone_code: str):
        if zone_type not in self.ZONE_TYPES:
            raise Exception("Invalid zone type!")
        # if zone_code in self.ZONE_TYPES[zone_type].code:
        #     raise Exception("Zone already exists!")
        zone = next((z for z in self.zones if z.code == zone_code), None)
        if zone is not None:
            raise Exception("Zone already exists!")
        zone = self.ZONE_TYPES[zone_type](zone_code)
        self.zones.append(zone)
        return f"A zone of type {zone_type} was successfully added."

    def add_battleship(self, ship_type: str, name: str, health: int, hit_strength: int):
        if ship_type not in self.SHIP_TYPES:
            raise Exception(f"{ship_type} is an invalid type of ship!")
        ship = self.SHIP_TYPES[ship_type](name, health, hit_strength)
        self.ships.append(ship)
        return f"A new {ship_type} was successfully added."

    @staticmethod
    def add_ship_to_zone(zone: BaseZone, ship: BaseBattleship):
        if zone.volume <= 0:
            return f"Zone {zone.code} does not allow more participants!"
        if ship.health <= 0:
            return f"Ship {ship.name} is considered sunk! Participation not allowed!"
        if not ship.is_available:
            return f"Ship {ship.name} is not available and could not participate!"

        if ((isinstance(ship, PirateBattleship) and isinstance(zone, PirateZone))
                or (isinstance(ship, RoyalBattleship) and isinstance(zone, RoyalZone))):
            ship.is_attacking = True
        else:
            ship.is_attacking = False

        zone.ships.append(ship)
        ship.is_available = False
        zone.volume -= 1
        return f"Ship {ship.name} successfully participated in zone {zone.code}."

    def remove_battleship(self, ship_name: str):
        ship = next((s for s in self.ships if s.name == ship_name), None)
        if ship is None:
            return "No ship with this name!"
        if not ship.is_available:
            return "The ship participates in zone battles! Removal is impossible!"
        self.ships.remove(ship)
        return f"Successfully removed ship {ship_name}."

    def start_battle(self, zone: BaseZone):
        attacking_ships = [s for s in zone.ships if s.is_attacking]
        target_ships = [t for t in zone.ships if not t.is_attacking]

        ship_type = RoyalBattleship
        if isinstance(zone, PirateZone):
            ship_type = PirateBattleship

        target_ship_type = RoyalBattleship if isinstance(zone, PirateZone) else PirateBattleship

        if not attacking_ships or not target_ships:
            return "Not enough participants. The battle is canceled."

        sorted_attackers = sorted(attacking_ships, key=lambda a: -a.hit_strength)
        attacker = next(a for a in sorted_attackers if isinstance(a, ship_type))
        sorted_targets = sorted(target_ships, key=lambda t: -t.health)
        target = next(t for t in sorted_targets if isinstance(t, target_ship_type))

        attacker.attack()
        target.take_damage(attacker)
        if target.health <= 0:
            # self.remove_battleship(target.name)
            zone.ships.remove(target)
            self.ships.remove(target)
            return f"{target.name} lost the battle and was sunk."
        if attacker.ammunition <= 0:
            # self.remove_battleship(attacker.name)
            zone.ships.remove(attacker)
            self.ships.remove(attacker)
            return f"{attacker.name} ran out of ammunition and leaves."
        return "Both ships survived the battle."

    def get_statistics(self):
        available_ships = [s.name for s in self.ships if s.is_available]
        result = [f"Available Battleships: {len(available_ships)}"]
        if available_ships:
            result.append(f"#{', '.join(available_ships)}#")
        result.append("***Zones Statistics:***")
        result.append(f"Total Zones: {len(self.zones)}")
        ordered_zones = sorted(self.zones, key=lambda z: z.code)
        for zone in ordered_zones:
            result.append(zone.zone_info())

        return '\n'.join(result).strip()