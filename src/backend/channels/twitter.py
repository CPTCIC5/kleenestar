from twitter_ads.client import Client
from twitter_ads.campaign import Campaign
from twitter_ads.enum import ENTITY_STATUS

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Fetch campaign data
def fetch_campaign_data():
    # Retrieve all campaigns associated with the account
    campaigns = Campaign.all(account=ACCOUNT_ID, client=client)
    
    for campaign in campaigns:
        campaign_name = campaign.name
        campaign_id = campaign.id
        print(f"Campaign Name: {campaign_name}, Campaign ID: {campaign_id}")

if __name__ == '__main__':
    fetch_campaign_data()

"""
# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# load and update a specific campaign
campaign = account.campaigns().next()
campaign.name = 'updated campaign name'
campaign.entity_status = ENTITY_STATUS.PAUSED
campaign.save()

# iterate through campaigns
for campaign in account.campaigns():
    print(campaign.id)
"""