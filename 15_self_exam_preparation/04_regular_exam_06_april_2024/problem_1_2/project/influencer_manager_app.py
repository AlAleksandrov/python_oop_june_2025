from project.campaigns.base_campaign import BaseCampaign
from project.campaigns.high_budget_campaign import HighBudgetCampaign
from project.campaigns.low_budget_campaign import LowBudgetCampaign
from project.influencers.base_influencer import BaseInfluencer
from project.influencers.premium_influencer import PremiumInfluencer
from project.influencers.standard_influencer import StandardInfluencer


class InfluencerManagerApp:
    INFLUENCER_TYPES = {
        "PremiumInfluencer": PremiumInfluencer,
        "StandardInfluencer": StandardInfluencer
    }

    CAMPAIGN_TYPES = {
        "HighBudgetCampaign": HighBudgetCampaign,
        "LowBudgetCampaign": LowBudgetCampaign
    }

    def __init__(self):
        self.influencers: list[BaseInfluencer] = []
        self.campaigns: list[BaseCampaign] = []

    def register_influencer(self, influencer_type: str, username: str, followers: int, engagement_rate: float):
        if influencer_type not in self.INFLUENCER_TYPES:
            return f"{influencer_type} is not an allowed influencer type."
        if any(i.username == username for i in self.influencers):
            return f"{username} is already registered."

        self.influencers.append(self.INFLUENCER_TYPES[influencer_type](username, followers, engagement_rate))
        return f"{username} is successfully registered as a {influencer_type}."

    def create_campaign(self, campaign_type: str, campaign_id: int, brand: str, required_engagement: float):
        if campaign_type not in self.CAMPAIGN_TYPES:
            return f"{campaign_type} is not a valid campaign type."
        if any(c.campaign_id == campaign_id for c in self.campaigns):
            return f"Campaign ID {campaign_id} has already been created."

        self.campaigns.append(self.CAMPAIGN_TYPES[campaign_type](campaign_id, brand, required_engagement))
        return f"Campaign ID {campaign_id} for {brand} is successfully created as a {campaign_type}."

    def participate_in_campaign(self, influencer_username: str, campaign_id: int):
        influencer = next((i for i in self.influencers if i.username == influencer_username), None)
        if influencer is None:
            return f"Influencer '{influencer_username}' not found."

        campaign = next((c for c in self.campaigns if c.campaign_id == campaign_id), None)
        if campaign is None:
            return f"Campaign with ID {campaign_id} not found."

        if not campaign.check_eligibility(influencer.engagement_rate):
            return f"Influencer '{influencer_username}' does not meet the eligibility criteria for the campaign with ID {campaign_id}."

        if influencer.calculate_payment(campaign) > 0.0:
            campaign.budget -= influencer.calculate_payment(campaign)
            influencer.campaigns_participated.append(campaign.campaign_id)
            campaign.approved_influencers.append(influencer.username)
            return f"Influencer '{influencer_username}' has successfully participated in the campaign with ID {campaign_id}."

        return f"Influencer '{influencer_username}' did not receive payment for campaign with ID {campaign_id}."

    def calculate_total_reached_followers(self):
        result = {}

        for campaign in self.campaigns:
            if campaign.approved_influencers:
                total_followers = 0

                for username in campaign.approved_influencers:
                    influencer = next((i for i in self.influencers if i.username == username), None)
                    if influencer:
                        campaign_type = campaign.__class__.__name__
                        total_followers += influencer.reached_followers(campaign_type)

                result[campaign] = total_followers
        return result

    def influencer_campaign_report(self, username: str):
        influencer = None
        for inf in self.influencers:
            if inf.username == username:
                influencer = inf
                break

        if influencer is None:
            return f"{username} has not participated in any campaigns."

        if not influencer.campaigns_participated:
            return f"{username} has not participated in any campaigns."

        result = f"{influencer.__class__.__name__} :) {username} :) participated in the following campaigns:\n"

        for campaign_id in influencer.campaigns_participated:
            campaign = next((c for c in self.campaigns if c.campaign_id == campaign_id), None)
            if campaign:
                reached_followers = influencer.reached_followers(campaign.__class__.__name__)
                result += f"  - Campaign ID: {campaign.campaign_id}, Brand: {campaign.brand}, Reached followers: {reached_followers}\n"

        return result.strip()

    def campaign_statistics(self):
        for campaign in self.campaigns:
            total_followers = 0
            for username in campaign.approved_influencers:
                influencer = next((i for i in self.influencers if i.username == username), None)
                if influencer:
                    total_followers += influencer.reached_followers(campaign.__class__.__name__)
            campaign.total_reached_followers = total_followers

        self.campaigns.sort(key=lambda c: (len(c.approved_influencers), -c.budget))

        result = "$$ Campaign Statistics $$\n"
        for c in self.campaigns:
            result += (f"  * Brand: {c.brand}, Total influencers: {len(c.approved_influencers)}, Total budget: "
                       f"${c.budget:.2f}, Total reached followers: {c.total_reached_followers}\n")
        return result.strip()