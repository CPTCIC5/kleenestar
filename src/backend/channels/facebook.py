import requests
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adreportrun import AdReportRun
import pandas as pd

app_id = 'app id from developer account'
app_secret = 'app secret'
access_token = 'access token'

FacebookAdsApi.init(app_id,app_secret,access_token)
my_account = AdAccount('act_xyz') #xyx is the account id in the business manager

#Fetch all the campaigns id that are associated with you account
campaigns = my_account.get_campaigns(fields=[Campaign.Field.name])
for campaign in campaigns:
    print(campaign[Campaign.Field.id])