from project.artifacts.base_artifact import BaseArtifact
from project.artifacts.contemporary_artifact import ContemporaryArtifact
from project.artifacts.renaissance_artifact import RenaissanceArtifact
from project.collectors.base_collector import BaseCollector
from project.collectors.museum import Museum
from project.collectors.private_collector import PrivateCollector


class AuctionHouseManagerApp:
    ARTIFACT_TYPES = {
        "RenaissanceArtifact": RenaissanceArtifact,
        "ContemporaryArtifact": ContemporaryArtifact
    }

    COLLECTOR_TYPES = {
        "Museum": Museum,
        "PrivateCollector": PrivateCollector
    }

    def __init__(self):
        self.artifacts: list[BaseArtifact] = []
        self.collectors: list[BaseCollector] = []

    def register_artifact(self, artifact_type: str, artifact_name: str, artifact_price: float, artifact_space: int):
        if artifact_type not in self.ARTIFACT_TYPES:
            raise ValueError("Unknown artifact type!")
        artifact = next((a for a in self.artifacts if a.name == artifact_name), None)
        if artifact:
            raise ValueError(f"{artifact_name} has been already registered!")

        artifact = self.ARTIFACT_TYPES[artifact_type](artifact_name, artifact_price, artifact_space)
        self.artifacts.append(artifact)
        return f"{artifact_name} is successfully added to the auction as {artifact_type}."

    def register_collector(self, collector_type: str, collector_name: str):
        if collector_type not in self.COLLECTOR_TYPES:
            raise ValueError("Unknown collector type!")
        collector = [c for c in self.collectors if c.name == collector_name]
        if collector:
            raise ValueError(f"{collector_name} has been already registered!")

        collector = self.COLLECTOR_TYPES[collector_type](collector_name)
        self.collectors.append(collector)
        return f"{collector_name} is successfully registered as a {collector_type}."

    def perform_purchase(self, collector_name: str, artifact_name: str):
        collector = next((c for c in self.collectors if c.name == collector_name), None)
        if collector is None:
            raise ValueError(f"Collector {collector_name} is not registered to the auction!")

        artifact = next((a for a in self.artifacts if a.name ==artifact_name), None)
        if artifact is None:
            raise ValueError(f"Artifact {artifact_name} is not registered to the auction!")

        if not collector.can_purchase(artifact.price, artifact.space_required):
            return "Purchase is impossible."

        collector.purchased_artifacts.append(artifact)
        self.artifacts.remove(artifact)
        collector.available_money -= artifact.price
        collector.available_space -= artifact.space_required

        return f"{collector_name} purchased {artifact_name} for a price of {artifact.price:.2f}."

    def remove_artifact(self, artifact_name: str):
        artifact = next((a for a in self.artifacts if a.name == artifact_name), None)
        if not artifact:
            return "No such artifact."

        self.artifacts.remove(artifact)
        return f"Removed {artifact.artifact_information()}"

    def fundraising_campaigns(self, max_money: float):
        collectors = [c for c in self.collectors if c.available_money <= max_money]
        count = 0
        for collector in collectors:
            collector.increase_money()
            count += 1
        return  f"{count} collector/s increased their available money."

    def get_auction_report(self):
        count_of_sold_artifacts = sum(len(s.purchased_artifacts) for s in self.collectors)
        result = [
            "**Auction statistics**",
            f"Total number of sold artifacts: {count_of_sold_artifacts}",
            f"Available artifacts for sale: {len(self.artifacts)}",
            "***"
        ]

        sorted_collectors = sorted(self.collectors, key=lambda c: (-len(c.purchased_artifacts), c.name))
        for collector in sorted_collectors:
            result.append(str(collector))

        return '\n'.join(result)