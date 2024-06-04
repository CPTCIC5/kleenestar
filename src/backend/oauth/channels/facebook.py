from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel
import hashlib
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from dotenv import load_dotenv
from django.shortcuts import redirect
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.adobjects.adaccount import AdAccount
from users.models import User
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
load_dotenv()


def get_channel(email,channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]
    return get_object_or_404(Channel, channel_type=channel_type_num, workspace=workspace)


#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

"""
APP - CONFIGURATIONS
"""
#facebook
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
facebook_authorization_base_url = 'https://www.facebook.com/dialog/oauth'
facebook_redirect_uri = 'https://127.0.0.1:8000/api/oauth/facebook-callback/'
facebook_scopes = ['ads_read','ads_management','public_profile','email']  
facebook = OAuth2Session(facebook_client_id, redirect_uri=facebook_redirect_uri, scope=facebook_scopes)
facebook = facebook_compliance_fix(facebook)
facebook_token_url = 'https://graph.facebook.com/oauth/access_token'





@api_view(("GET",))
def facebook_oauth(request):
    try:
        authorization_url, state = facebook.authorization_url(url=facebook_authorization_base_url, state=passthrough_val)
        return Response({
            "url": authorization_url},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def facebook_oauth_callback(request):   
    redirect_response = request.build_absolute_uri()
    if request.query_params.get("state") != passthrough_val:
        return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        token = facebook.fetch_token(token_url=facebook_token_url, client_secret=facebook_client_secret, # 60days validity
                                     authorization_response=redirect_response) # access_token

        access_token = token.get("access_token")
        user_info_url = 'https://graph.facebook.com/v10.0/me?fields=id,name,email'
        user_info_response = facebook.get(user_info_url)
        email = user_info_response.json()['email']  # email

        FacebookAdsApi.init(access_token=access_token)
        me = AdUser(fbid='me')
        
        ad_accounts = me.get_ad_accounts()
        ad_accounts_list = []
        for account in ad_accounts:
            ad_accounts_list.append(account.get("id")) # account id list
        
        facebook_channel = get_channel(
            email=request.user.email,
            channel_type_num=2
        )

        facebook_channel.credentials.key_1 = access_token
        facebook_channel.credentials.key_2 = ad_accounts_list
        facebook_channel.credentials.save()

        print(access_token, ad_accounts_list, "creds")
        return redirect("http://localhost:3001/channels/")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 

def get_facebook_marketing_data(access_token, ad_account_list):
    marketing_data = []
    try:
        for account in ad_account_list:
            FacebookAdsApi.init(access_token=access_token)
            ad_account = AdAccount(account)
            
            params = {
                'level': 'ad',
                'time_range': {'since': '2024-01-01', 'until': '2024-5-20'},
            }
            
            fields = [
                'campaign_id', 'adset_id', 'ad_id',
                'impressions', 'reach', 'frequency', 'unique_clicks', 'cpm', 'cpp',
                'conversions', 'cost_per_conversion', 'website_ctr',
                'clicks', 'spend', 'purchase_roas', 
                'date_start', 'date_stop'
            ]

            insights = ad_account.get_insights(fields=fields, params=params)
            
            results = []
            for insight in insights:
                result = {}

                # Campaign details
                campaign_id = insight['campaign_id']
                campaign = Campaign(campaign_id).api_get(fields=[
                    Campaign.Field.id, Campaign.Field.name, Campaign.Field.objective, Campaign.Field.status,
                    Campaign.Field.effective_status, Campaign.Field.start_time, Campaign.Field.stop_time,
                    Campaign.Field.daily_budget, Campaign.Field.lifetime_budget
                ])
                result['campaign'] = campaign

                # AdSet details
                adset_id = insight['adset_id']
                adset = AdSet(adset_id).api_get(fields=[
                    AdSet.Field.id, AdSet.Field.name, AdSet.Field.status, AdSet.Field.effective_status,
                    AdSet.Field.billing_event, AdSet.Field.optimization_goal, AdSet.Field.targeting
                ])
                result['adset'] = adset

                ad_id = insight['ad_id']
                ad = Ad(ad_id).api_get(fields=[
                    Ad.Field.id, Ad.Field.name, Ad.Field.status, Ad.Field.effective_status,
                    Ad.Field.creative
                ])
                ad_creative = ad['creative']
                ad_creative_details = Ad(ad_creative['id']).api_get(fields=[
                    'body', 'title', 'image_url'
                ])
                ad['creative_details'] = ad_creative_details
                result['ad'] = ad

                audience_metrics = {
                    'impressions': insight['impressions'],
                    'reach': insight['reach'],
                    'frequency': insight['frequency'],
                    'unique_clicks': insight['unique_clicks'],
                    'cpm': insight['cpm'],
                    'cpp': insight['cpp'],
                }
                result['audience_metrics'] = audience_metrics

                conversion_metrics = {
                    'conversions': insight['conversions'],
                    'cost_per_conversion': insight['cost_per_conversion'],
                    'website_ctr': insight['website_ctr'],
                }
                result['conversion_metrics'] = conversion_metrics

                engagement_metrics = {
                    'clicks': insight['clicks'],
                }
                result['engagement_metrics'] = engagement_metrics

                revenue_metrics = {
                    'spend': insight['spend'],
                    'purchase_roas': insight['purchase_roas'],
                }
                result['revenue_metrics'] = revenue_metrics

                time_metrics = {
                    'date_start': insight['date_start'],
                    'date_stop': insight['date_stop'],
                }
                result['time_metrics'] = time_metrics

                results.append(result)
            marketing_data.append(results)
        return Response(
            marketing_data, status=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"Error with message {e}.")
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
