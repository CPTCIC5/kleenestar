from linkedin_api import LinkedIn
from linkedin_api.client import LinkedInAdapter

# LinkedIn App Credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# LinkedIn User Credentials
USERNAME = 'your_linkedin_username'
PASSWORD = 'your_linkedin_password'

# Create a LinkedIn API client
linkedin = LinkedIn(
    adapter=LinkedInAdapter(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD
    )
)

# Fetch campaign data
def fetch_campaign_data():
    # Example: Get all ad campaigns
    campaigns = linkedin.get_ad_campaigns()
    for campaign in campaigns:
        campaign_name = campaign['campaignName']
        campaign_id = campaign['campaignId']
        print(f"Campaign Name: {campaign_name}, Campaign ID: {campaign_id}")

if __name__ == '__main__':
    fetch_campaign_data()