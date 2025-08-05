from project.campaigns.base_campaign import BaseCampaign
from project.influencers.base_influencer import BaseInfluencer


class StandardInfluencer(BaseInfluencer):
    INITIAL_PAYMENT = 0.45
    CAMPAIGN_TYPE = {
        "HighBudgetCampaign": 1.2,
        "LowBudgetCampaign": 0.9
    }

    def __init__(self, username: str, followers: int, engagement_rate: float):
        super().__init__(username, followers, engagement_rate)

    def calculate_payment(self, campaign: "BaseCampaign"):
        return self.INITIAL_PAYMENT * campaign.budget

    def reached_followers(self, campaign_type: str):
        if campaign_type in self.CAMPAIGN_TYPE:
            return int(self.followers * self.engagement_rate * self.CAMPAIGN_TYPE[campaign_type])
        return 0