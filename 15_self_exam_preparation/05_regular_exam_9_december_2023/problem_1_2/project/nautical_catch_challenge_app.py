from project.divers.base_diver import BaseDiver
from project.divers.free_diver import FreeDiver
from project.divers.scuba_diver import ScubaDiver
from project.fish.base_fish import BaseFish
from project.fish.deep_sea_fish import DeepSeaFish
from project.fish.predatory_fish import PredatoryFish


class NauticalCatchChallengeApp:
    DIVERS_TYPES = {
        "FreeDiver": FreeDiver,
        "ScubaDiver": ScubaDiver
    }

    FISH_TYPES = {
        "PredatoryFish": PredatoryFish,
        "DeepSeaFish": DeepSeaFish
    }

    def __init__(self):
        self.divers: list[BaseDiver] = []
        self.fish_list: list[BaseFish] = []

    def dive_into_competition(self, diver_type: str, diver_name: str):
        if diver_type not in self.DIVERS_TYPES:
            return f"{diver_type} is not allowed in our competition."

        if any(d.name == diver_name for d in self.divers):
            return f"{diver_name} is already a participant."

        self.divers.append(self.DIVERS_TYPES[diver_type](diver_name))
        return f"{diver_name} is successfully registered for the competition as a {diver_type}."

    def swim_into_competition(self, fish_type: str, fish_name: str, points: float):
        if fish_type not in self.FISH_TYPES:
            return f"{fish_type} is forbidden for chasing in our competition."

        if any(f.name == fish_name for f in self.fish_list):
            return f"{fish_name} is already permitted."

        self.fish_list.append(self.FISH_TYPES[fish_type](fish_name, points))
        return f"{fish_name} is allowed for chasing as a {fish_type}."

    def chase_fish(self, diver_name: str, fish_name: str, is_lucky: bool):
        diver = next((d for d in self.divers if d.name == diver_name), None)
        if diver is None:
            return f"{diver_name} is not registered for the competition."

        fish = next((f for f in self.fish_list if f.name == fish_name), None)
        if fish is None:
            return f"The {fish_name} is not allowed to be caught in this competition."

        if diver.has_health_issue:
            return f"{diver_name} will not be allowed to dive, due to health issues."

        if diver.oxygen_level < fish.time_to_catch:
            diver.miss(fish.time_to_catch)
            if diver.oxygen_level == 0:
                diver.update_health_status()
            return f"{diver_name} missed a good {fish_name}."

        elif diver.oxygen_level == fish.time_to_catch:
            if is_lucky:
                diver.hit(fish)
                if diver.oxygen_level == 0:
                    diver.update_health_status()
                return f"{diver_name} hits a {fish.points}pt. {fish_name}."
            else:
                diver.miss(fish.time_to_catch)
                if diver.oxygen_level == 0:
                    diver.update_health_status()
                return f"{diver_name} missed a good {fish_name}."

        else:
            diver.hit(fish)
            if diver.oxygen_level == 0:
                diver.update_health_status()
            return f"{diver_name} hits a {fish.points}pt. {fish_name}."

    def health_recovery(self):
        divers_to_recovery = [d for d in self.divers if d.has_health_issue]
        count = 0
        for diver in divers_to_recovery:
            diver.update_health_status()
            diver.renew_oxy()
            count += 1
        return f"Divers recovered: {count}"

    def diver_catch_report(self, diver_name: str):
        result = [f"**{diver_name} Catch Report**"]
        diver = next(d for d in self.divers if d.name == diver_name)
        for fish in diver.catch:
            result.append(f"{fish.fish_details()}")
        return '\n'.join(result)


    def competition_statistics(self):
        result = [f"**Nautical Catch Challenge Statistics**"]
        sorted_divers = sorted(self.divers, key=lambda d: (-d.competition_points, -len(d.catch), d.name))

        for diver in sorted_divers:
            if not diver.has_health_issue:
                result.append(diver.__str__())

        return '\n'.join(result)